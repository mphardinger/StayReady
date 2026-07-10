from datetime import datetime

from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import BadQuantity, household_id, norm_name, parse_qty, require_auth
from routes.pantry import add_stock, find_stock

bp = Blueprint('shopping', __name__, url_prefix='/api/shopping')


def _parse_date(value):
    return datetime.strptime(value or '', '%Y-%m-%d').date()


@bp.get('')
@require_auth
def shopping_list():
    """Everything to buy for the planned (not yet cooked) meals in a date range,
    with pantry stock subtracted where the name AND unit match."""
    try:
        start = _parse_date(request.args.get('start'))
        end = _parse_date(request.args.get('end'))
    except ValueError:
        return jsonify(error='Dates must look like YYYY-MM-DD'), 400
    if end < start:
        return jsonify(error='End date must be on or after the start date'), 400
    start_s, end_s = start.isoformat(), end.isoformat()
    db = get_db()
    hh_id = household_id()

    # leftover = 0 everywhere: leftover lunches reuse a dinner already bought/cooked.
    meals_count = db.execute(
        '''SELECT COUNT(*) FROM meal_plan
           WHERE household_id = ? AND cooked = 0 AND leftover = 0 AND date BETWEEN ? AND ?''',
        (hh_id, start_s, end_s)).fetchone()[0]

    # Estimated grocery cost of the planned (not-yet-cooked) meals in range.
    # Ingredients have no per-item price, so we sum each planned meal's whole
    # recipe cost_total — the best available proxy for what you'll spend.
    estimated_cost = db.execute(
        '''SELECT COALESCE(SUM(r.cost_total), 0) FROM meal_plan mp
           JOIN recipes r ON r.id = mp.recipe_id
           WHERE mp.household_id = ? AND mp.cooked = 0 AND mp.leftover = 0 AND mp.date BETWEEN ? AND ?''',
        (hh_id, start_s, end_s)).fetchone()[0]
    members_count = db.execute(
        'SELECT COUNT(*) FROM members WHERE household_id = ?', (hh_id,)).fetchone()[0]
    weekly_budget = db.execute(
        'SELECT weekly_budget FROM households WHERE id = ?', (hh_id,)).fetchone()[0]

    rows = db.execute(
        '''SELECT ri.name, ri.quantity, ri.unit, r.name AS recipe_name
           FROM meal_plan mp
           JOIN recipes r ON r.id = mp.recipe_id
           JOIN recipe_ingredients ri ON ri.recipe_id = r.id
           WHERE mp.household_id = ? AND mp.cooked = 0 AND mp.leftover = 0 AND mp.date BETWEEN ? AND ?
           ORDER BY mp.date, mp.id''',
        (hh_id, start_s, end_s)).fetchall()

    # Aggregate needs keyed by (normalized name, lowercased unit).
    needed = {}
    for row in rows:
        key = (norm_name(row['name']), (row['unit'] or '').strip().lower())
        if not key[0]:
            continue
        agg = needed.get(key)
        if agg is None:
            agg = needed[key] = {'name': (row['name'] or '').strip(),
                                 'unit': (row['unit'] or '').strip(),
                                 'needed': 0.0, 'recipes': []}
        agg['needed'] += row['quantity'] or 0
        if row['recipe_name'] not in agg['recipes']:
            agg['recipes'].append(row['recipe_name'])

    # One pantry pass: exact (name, unit) stock totals, plus a name-only
    # category fallback so a unit-mismatched match still files under the
    # right aisle (its `have` stays 0 — the math is unit-aware).
    have_by_key = {}
    category_by_name = {}
    for p in db.execute(
            'SELECT name, quantity, unit, category FROM pantry_items WHERE household_id = ?',
            (hh_id,)).fetchall():
        pkey = (norm_name(p['name']), (p['unit'] or '').strip().lower())
        entry = have_by_key.setdefault(pkey, {'have': 0.0, 'category': p['category']})
        entry['have'] += p['quantity'] or 0
        category_by_name.setdefault(pkey[0], p['category'])

    items = []
    for key, agg in needed.items():
        match = have_by_key.get(key)
        have = match['have'] if match else 0.0  # unit mismatch -> have 0
        to_buy = round(max(0.0, agg['needed'] - have), 2)
        if to_buy <= 0:
            continue
        category = match['category'] if match else category_by_name.get(key[0], 'other')
        items.append({'name': agg['name'], 'unit': agg['unit'],
                      'needed': round(agg['needed'], 2), 'have': round(have, 2),
                      'to_buy': to_buy, 'category': category,
                      'recipes': agg['recipes'][:3]})
    items.sort(key=lambda i: (i['category'], i['name'].lower()))

    return jsonify({'meals_count': meals_count,
                    'days': (end - start).days + 1,
                    'items': items,
                    'estimated_cost': round(estimated_cost, 2),
                    'members_count': members_count,
                    'weekly_budget': weekly_budget})


@bp.post('/purchase')
@require_auth
def purchase():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error='Item needs a name'), 400
    try:
        quantity = parse_qty(data.get('quantity', 0))
    except BadQuantity as err:
        return jsonify(error=str(err)), 400
    db = get_db()
    unit = (data.get('unit') or '').strip()
    # Capture prior state so the client can offer a clean Undo.
    existing = find_stock(db, household_id(), name, unit)
    previous_quantity = existing['quantity'] if existing else 0
    created = existing is None
    item = add_stock(db, household_id(), name, quantity, unit, data.get('category'))
    db.commit()
    return jsonify({'id': item['id'], 'name': item['name'], 'quantity': item['quantity'],
                    'unit': item['unit'], 'category': item['category'],
                    'previous_quantity': previous_quantity, 'created': created})
