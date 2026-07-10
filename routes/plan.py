import re
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import MEAL_TYPES, household_id, norm_name, require_auth
from routes.pantry import find_stock

bp = Blueprint('plan', __name__, url_prefix='/api/plan')

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

ENTRY_SQL = '''
    SELECT mp.id, mp.date, mp.meal_type, mp.cooked, mp.leftover,
           r.id AS recipe_id, r.name AS recipe_name, r.emoji AS recipe_emoji,
           r.time_minutes AS recipe_time_minutes, r.servings AS recipe_servings,
           r.meal_type AS recipe_meal_type,
           m.id AS cook_id, m.name AS cook_name, m.color AS cook_color
    FROM meal_plan mp
    JOIN recipes r ON r.id = mp.recipe_id
    LEFT JOIN members m ON m.id = mp.cook_member_id
'''


def _entry(row):
    cook = None
    if row['cook_id'] is not None:
        cook = {'id': row['cook_id'], 'name': row['cook_name'], 'color': row['cook_color']}
    return {
        'id': row['id'],
        'date': row['date'],
        'meal_type': row['meal_type'],
        'cooked': row['cooked'],
        'leftover': row['leftover'],
        'recipe': {'id': row['recipe_id'], 'name': row['recipe_name'],
                   'emoji': row['recipe_emoji'], 'time_minutes': row['recipe_time_minutes'],
                   'servings': row['recipe_servings'], 'meal_type': row['recipe_meal_type']},
        'cook': cook,
    }


def _restock_ingredients(db, hh_id, recipe_id):
    """Add a recipe's ingredients back to pantry — used when an already-cooked
    slot's recipe is swapped for a different one, so the old recipe's
    consumption isn't silently lost forever. Best-effort: adds the recipe's
    full ingredient amounts back, matched the same way mark_cooked deducts
    (norm_name + unit). If a matching pantry item no longer exists, there's
    nothing sensible to restock into, so it's skipped rather than recreated.
    """
    ingredients = db.execute(
        'SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?',
        (recipe_id,)).fetchall()
    for ing in ingredients:
        name = (ing['name'] or '').strip()
        unit = (ing['unit'] or '').strip()
        qty = ing['quantity'] or 0
        if not name or qty <= 0:
            continue
        existing = find_stock(db, hh_id, name, unit)
        if existing:
            db.execute(
                "UPDATE pantry_items SET quantity = quantity + ?, updated_at = datetime('now') WHERE id = ?",
                (qty, existing['id']))


def _valid_date(value):
    if not value or not DATE_RE.match(value):
        return False
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        return False
    return True


@bp.get('')
@require_auth
def list_entries():
    start = request.args.get('start', '')
    end = request.args.get('end', '')
    if not _valid_date(start) or not _valid_date(end):
        return jsonify(error='start and end must be YYYY-MM-DD dates'), 400
    rows = get_db().execute(
        ENTRY_SQL + ' WHERE mp.household_id = ? AND mp.date BETWEEN ? AND ?'
                    ' ORDER BY mp.date, mp.meal_type',
        (household_id(), start, end)).fetchall()
    return jsonify([_entry(r) for r in rows])


@bp.put('')
@require_auth
def upsert_slot():
    data = request.get_json(silent=True) or {}
    date = (data.get('date') or '').strip()
    meal_type = (data.get('meal_type') or '').strip()
    if not _valid_date(date):
        return jsonify(error='date must be a YYYY-MM-DD date'), 400
    if meal_type not in MEAL_TYPES:
        return jsonify(error='meal_type must be breakfast, lunch, or dinner'), 400
    try:
        recipe_id = int(data.get('recipe_id'))
    except (TypeError, ValueError):
        return jsonify(error='recipe_id is required'), 400

    db = get_db()
    hh_id = household_id()
    recipe = db.execute('SELECT id FROM recipes WHERE id = ? AND household_id = ?',
                        (recipe_id, hh_id)).fetchone()
    if recipe is None:
        return jsonify(error='Recipe not found'), 404

    cook_member_id = data.get('cook_member_id')
    if cook_member_id in (None, ''):
        cook_member_id = None
    else:
        try:
            cook_member_id = int(cook_member_id)
        except (TypeError, ValueError):
            return jsonify(error='cook_member_id must be a member id'), 400
        member = db.execute('SELECT id FROM members WHERE id = ? AND household_id = ?',
                            (cook_member_id, hh_id)).fetchone()
        if member is None:
            return jsonify(error='Member not found'), 404

    # If this slot was already cooked for a DIFFERENT recipe, that recipe's
    # ingredients were deducted from pantry and are about to be replaced —
    # restock them so swapping the recipe doesn't silently shrink the pantry.
    existing_slot = db.execute(
        'SELECT recipe_id, cooked FROM meal_plan WHERE household_id = ? AND date = ? AND meal_type = ?',
        (hh_id, date, meal_type)).fetchone()
    if existing_slot and existing_slot['cooked'] and existing_slot['recipe_id'] != recipe_id:
        _restock_ingredients(db, hh_id, existing_slot['recipe_id'])

    db.execute(
        '''INSERT INTO meal_plan (household_id, date, meal_type, recipe_id, cook_member_id, cooked, leftover)
           VALUES (?, ?, ?, ?, ?, 0, 0)
           ON CONFLICT (household_id, date, meal_type)
           DO UPDATE SET recipe_id = excluded.recipe_id,
                         cook_member_id = excluded.cook_member_id,
                         leftover = CASE WHEN meal_plan.recipe_id = excluded.recipe_id
                                         THEN meal_plan.leftover ELSE 0 END,
                         cooked = CASE WHEN meal_plan.recipe_id = excluded.recipe_id
                                       THEN meal_plan.cooked ELSE 0 END''',
        (hh_id, date, meal_type, recipe_id, cook_member_id))

    # Cook once, eat twice: optionally fill the next day's lunch with leftovers
    # of this dinner (only if that lunch slot is currently empty).
    leftover_added = False
    if data.get('leftover_lunch') and meal_type == 'dinner':
        next_date = (datetime.strptime(date, '%Y-%m-%d').date() + timedelta(days=1)).isoformat()
        occupied = db.execute(
            'SELECT 1 FROM meal_plan WHERE household_id = ? AND date = ? AND meal_type = ?',
            (hh_id, next_date, 'lunch')).fetchone()
        if occupied is None:
            db.execute(
                '''INSERT INTO meal_plan (household_id, date, meal_type, recipe_id, cook_member_id, cooked, leftover)
                   VALUES (?, ?, 'lunch', ?, NULL, 0, 1)''',
                (hh_id, next_date, recipe_id))
            leftover_added = True

    db.commit()
    row = db.execute(ENTRY_SQL + ' WHERE mp.household_id = ? AND mp.date = ? AND mp.meal_type = ?',
                     (hh_id, date, meal_type)).fetchone()
    payload = _entry(row)
    payload['leftover_added'] = leftover_added
    return jsonify(payload)


@bp.delete('')
@require_auth
def clear_slot():
    date = request.args.get('date', '')
    meal_type = request.args.get('meal_type', '')
    if not _valid_date(date) or meal_type not in MEAL_TYPES:
        return jsonify(error='date (YYYY-MM-DD) and meal_type are required'), 400
    db = get_db()
    row = db.execute(
        'SELECT id FROM meal_plan WHERE household_id = ? AND date = ? AND meal_type = ?',
        (household_id(), date, meal_type)).fetchone()
    if row is None:
        return jsonify(error='That slot is already empty'), 404
    db.execute('DELETE FROM meal_plan WHERE id = ?', (row['id'],))
    db.commit()
    return jsonify(ok=True)


@bp.post('/<int:entry_id>/cooked')
@require_auth
def mark_cooked(entry_id):
    db = get_db()
    hh_id = household_id()
    row = db.execute(ENTRY_SQL + ' WHERE mp.id = ? AND mp.household_id = ?',
                     (entry_id, hh_id)).fetchone()
    if row is None:
        return jsonify(error='Plan entry not found'), 404
    if row['cooked']:
        return jsonify(entry=_entry(row), deducted=[])
    # Leftovers reuse the dinner already cooked — mark eaten, deduct nothing.
    if row['leftover']:
        db.execute('UPDATE meal_plan SET cooked = 1 WHERE id = ?', (entry_id,))
        db.commit()
        row = db.execute(ENTRY_SQL + ' WHERE mp.id = ?', (entry_id,)).fetchone()
        return jsonify(entry=_entry(row), deducted=[])

    db.execute('UPDATE meal_plan SET cooked = 1 WHERE id = ?', (entry_id,))

    ingredients = db.execute(
        'SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = ?',
        (row['recipe_id'],)).fetchall()
    pantry = db.execute(
        'SELECT id, name, quantity, unit FROM pantry_items WHERE household_id = ?',
        (hh_id,)).fetchall()
    by_key = {}
    remaining = {}
    for item in pantry:
        key = (norm_name(item['name']), (item['unit'] or '').strip().lower())
        by_key.setdefault(key, []).append(item)
        remaining[item['id']] = item['quantity']

    deducted = []
    for ing in ingredients:
        key = (norm_name(ing['name']), (ing['unit'] or '').strip().lower())
        items = by_key.get(key)
        if not items:
            continue
        need = ing['quantity'] or 0
        taken = 0.0
        for item in items:
            if need <= 0:
                break
            amount = min(remaining[item['id']], need)
            if amount <= 0:
                continue
            remaining[item['id']] -= amount
            need -= amount
            taken += amount
            db.execute(
                "UPDATE pantry_items SET quantity = ?, updated_at = datetime('now') WHERE id = ?",
                (remaining[item['id']], item['id']))
        if taken > 0:
            deducted.append({'name': items[0]['name'], 'amount': round(taken, 2)})

    db.commit()
    row = db.execute(ENTRY_SQL + ' WHERE mp.id = ?', (entry_id,)).fetchone()
    return jsonify(entry=_entry(row), deducted=deducted)
