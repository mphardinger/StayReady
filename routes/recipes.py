import math

from flask import Blueprint, jsonify, request

from db import get_db, nutrition_score
from routes.common import MEAL_TYPES, household_id, norm_name, require_auth

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

RECIPE_MEAL_TYPES = MEAL_TYPES + ['any']

# (column, cast, POST default, user-facing label)
NUMBER_FIELDS = [
    ('time_minutes', int, 30, 'Time'),
    ('servings', int, 4, 'Servings'),
    ('cost_total', float, 0.0, 'Cost'),
    ('calories', int, 0, 'Calories'),
    ('protein_g', float, 0.0, 'Protein'),
    ('carbs_g', float, 0.0, 'Carbs'),
    ('fat_g', float, 0.0, 'Fat'),
]


class _BadInput(ValueError):
    """Malformed request value; message is user-facing."""


def _number(value, default, cast, label):
    """Coerce a request value to a number; missing/blank -> default, junk -> 400."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return default
    try:
        f = float(value)
        if not math.isfinite(f):
            raise ValueError
        return cast(f)
    except (TypeError, ValueError, OverflowError):
        raise _BadInput(label + ' must be a number')


def _get(data, key, current, default):
    if key in data:
        return data[key]
    return current[key] if current is not None else default


def _parse_fields(data, current=None):
    """Validated recipe column values. current (existing row) supplies defaults
    on update; current=None means create, with schema-style defaults."""
    if current is None:
        name = str(data.get('name') or '').strip()
        if not name:
            raise _BadInput('Recipe needs a name')
    else:
        name = str(data.get('name') or '').strip() or current['name']
    meal_type = str(_get(data, 'meal_type', current, 'dinner') or 'dinner').strip().lower()
    if meal_type not in RECIPE_MEAL_TYPES:
        raise _BadInput('Meal type must be breakfast, lunch, dinner, or any')
    fields = {
        'name': name,
        'emoji': str(_get(data, 'emoji', current, '') or '').strip() or '🍽️',
        'description': str(_get(data, 'description', current, '') or '').strip(),
        'meal_type': meal_type,
        'instructions': str(_get(data, 'instructions', current, '') or '').strip(),
    }
    for key, cast, default, label in NUMBER_FIELDS:
        base = current[key] if current is not None else default
        fields[key] = max(0, _number(data.get(key), base, cast, label))
    fields['servings'] = max(1, fields['servings'])
    return fields


def _parse_ingredients(data):
    """None if the body doesn't touch ingredients; else a clean list of
    (name, quantity, unit) tuples (blank names dropped)."""
    if 'ingredients' not in data or data['ingredients'] is None:
        return None
    raw = data['ingredients']
    if not isinstance(raw, list):
        raise _BadInput('Ingredients must be a list')
    rows = []
    for ing in raw:
        if not isinstance(ing, dict):
            raise _BadInput('Each ingredient needs a name, quantity, and unit')
        name = str(ing.get('name') or '').strip()
        if not name:
            continue
        quantity = max(0, _number(ing.get('quantity'), 0.0, float, 'Ingredient quantity'))
        rows.append((name, quantity, str(ing.get('unit') or '').strip()))
    return rows


def _insert_ingredients(db, recipe_id, ingredients):
    for name, quantity, unit in ingredients:
        db.execute(
            'INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)',
            (recipe_id, name, quantity, unit))


def _pantry_norms(db, hh_id):
    """Normalized names of pantry items actually in stock — ONE query."""
    rows = db.execute(
        'SELECT name FROM pantry_items WHERE household_id = ? AND quantity > 0',
        (hh_id,)).fetchall()
    return {norm_name(r['name']) for r in rows}


def _ingredients_for(db, recipe_id):
    return db.execute(
        'SELECT * FROM recipe_ingredients WHERE recipe_id = ? ORDER BY id',
        (recipe_id,)).fetchall()


def _recipe_json(recipe, ingredients, pantry_norms, include_instructions=False):
    data = {
        'id': recipe['id'],
        'name': recipe['name'],
        'emoji': recipe['emoji'],
        'description': recipe['description'],
        'meal_type': recipe['meal_type'],
        'time_minutes': recipe['time_minutes'],
        'servings': recipe['servings'],
        'cost_total': recipe['cost_total'],
        'cost_per_serving': round(recipe['cost_total'] / max(recipe['servings'], 1), 2),
        'calories': recipe['calories'],
        'protein_g': recipe['protein_g'],
        'carbs_g': recipe['carbs_g'],
        'fat_g': recipe['fat_g'],
        'nutrition_score': nutrition_score(recipe['calories'], recipe['protein_g'], len(ingredients)),
        'ingredients': [{'id': i['id'], 'name': i['name'],
                         'quantity': i['quantity'], 'unit': i['unit']} for i in ingredients],
        'have_count': sum(1 for i in ingredients if norm_name(i['name']) in pantry_norms),
        'ingredient_count': len(ingredients),
    }
    if include_instructions:
        data['instructions'] = recipe['instructions']
    return data


@bp.get('')
@require_auth
def list_recipes():
    db = get_db()
    hh_id = household_id()
    recipes = db.execute(
        'SELECT * FROM recipes WHERE household_id = ? ORDER BY lower(name)',
        (hh_id,)).fetchall()
    ing_rows = db.execute(
        '''SELECT ri.* FROM recipe_ingredients ri
           JOIN recipes r ON r.id = ri.recipe_id
           WHERE r.household_id = ? ORDER BY ri.id''', (hh_id,)).fetchall()
    by_recipe = {}
    for row in ing_rows:
        by_recipe.setdefault(row['recipe_id'], []).append(row)
    pantry_norms = _pantry_norms(db, hh_id)
    return jsonify([_recipe_json(r, by_recipe.get(r['id'], []), pantry_norms)
                    for r in recipes])


@bp.get('/<int:recipe_id>')
@require_auth
def get_recipe(recipe_id):
    db = get_db()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ? AND household_id = ?',
                        (recipe_id, household_id())).fetchone()
    if recipe is None:
        return jsonify(error='Recipe not found'), 404
    return jsonify(_recipe_json(recipe, _ingredients_for(db, recipe_id),
                                _pantry_norms(db, household_id()),
                                include_instructions=True))


@bp.post('')
@require_auth
def create_recipe():
    data = request.get_json(silent=True) or {}
    try:
        fields = _parse_fields(data)
        ingredients = _parse_ingredients(data) or []
    except _BadInput as err:
        return jsonify(error=str(err)), 400
    db = get_db()
    cur = db.execute(
        '''INSERT INTO recipes (household_id, name, emoji, description, meal_type,
               time_minutes, servings, cost_total, calories, protein_g, carbs_g,
               fat_g, instructions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (household_id(), fields['name'], fields['emoji'], fields['description'],
         fields['meal_type'], fields['time_minutes'], fields['servings'],
         fields['cost_total'], fields['calories'], fields['protein_g'],
         fields['carbs_g'], fields['fat_g'], fields['instructions']))
    recipe_id = cur.lastrowid
    _insert_ingredients(db, recipe_id, ingredients)
    db.commit()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    return jsonify(_recipe_json(recipe, _ingredients_for(db, recipe_id),
                                _pantry_norms(db, household_id()),
                                include_instructions=True)), 201


@bp.put('/<int:recipe_id>')
@require_auth
def update_recipe(recipe_id):
    db = get_db()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ? AND household_id = ?',
                        (recipe_id, household_id())).fetchone()
    if recipe is None:
        return jsonify(error='Recipe not found'), 404
    data = request.get_json(silent=True) or {}
    try:
        fields = _parse_fields(data, current=recipe)
        ingredients = _parse_ingredients(data)
    except _BadInput as err:
        return jsonify(error=str(err)), 400
    db.execute(
        '''UPDATE recipes SET name = ?, emoji = ?, description = ?, meal_type = ?,
               time_minutes = ?, servings = ?, cost_total = ?, calories = ?,
               protein_g = ?, carbs_g = ?, fat_g = ?, instructions = ?
           WHERE id = ?''',
        (fields['name'], fields['emoji'], fields['description'], fields['meal_type'],
         fields['time_minutes'], fields['servings'], fields['cost_total'],
         fields['calories'], fields['protein_g'], fields['carbs_g'], fields['fat_g'],
         fields['instructions'], recipe_id))
    if ingredients is not None:
        db.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (recipe_id,))
        _insert_ingredients(db, recipe_id, ingredients)
    db.commit()
    recipe = db.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    return jsonify(_recipe_json(recipe, _ingredients_for(db, recipe_id),
                                _pantry_norms(db, household_id()),
                                include_instructions=True))


@bp.delete('/<int:recipe_id>')
@require_auth
def delete_recipe(recipe_id):
    db = get_db()
    recipe = db.execute('SELECT id FROM recipes WHERE id = ? AND household_id = ?',
                        (recipe_id, household_id())).fetchone()
    if recipe is None:
        return jsonify(error='Recipe not found'), 404
    db.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    db.commit()
    return jsonify(ok=True)
