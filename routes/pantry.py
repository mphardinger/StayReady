from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import BadQuantity, PANTRY_CATEGORIES, household_id, norm_name, parse_qty, require_auth

bp = Blueprint('pantry', __name__, url_prefix='/api/pantry')


def _row(item):
    return {'id': item['id'], 'name': item['name'], 'quantity': item['quantity'],
            'unit': item['unit'], 'category': item['category'], 'updated_at': item['updated_at']}


def _clean_category(value):
    cat = (value or 'other').strip().lower()
    return cat if cat in PANTRY_CATEGORIES else 'other'


def find_stock(db, hh_id, name, unit):
    """The pantry row matching name+unit (normalized), or None. Shared so the
    shopping 'purchase' flow can capture prior state for undo."""
    target = (norm_name(name), (unit or '').strip().lower())
    return next(
        (r for r in db.execute('SELECT * FROM pantry_items WHERE household_id = ?', (hh_id,))
         if (norm_name(r['name']), (r['unit'] or '').strip().lower()) == target), None)


def add_stock(db, hh_id, name, quantity, unit, category='other'):
    """Upsert-increment a pantry item, matching on normalized name + unit.

    Shared with the shopping list's "mark purchased" flow.
    """
    name = (name or '').strip()
    unit = (unit or '').strip()
    existing = find_stock(db, hh_id, name, unit)
    if existing:
        db.execute(
            '''UPDATE pantry_items SET quantity = quantity + ?, updated_at = datetime('now')
               WHERE id = ?''', (quantity, existing['id']))
        item_id = existing['id']
    else:
        cur = db.execute(
            'INSERT INTO pantry_items (household_id, name, quantity, unit, category) VALUES (?, ?, ?, ?, ?)',
            (hh_id, name, quantity, unit, _clean_category(category)))
        item_id = cur.lastrowid
    return db.execute('SELECT * FROM pantry_items WHERE id = ?', (item_id,)).fetchone()


@bp.get('')
@require_auth
def list_items():
    rows = get_db().execute(
        'SELECT * FROM pantry_items WHERE household_id = ? ORDER BY category, lower(name)',
        (household_id(),)).fetchall()
    return jsonify([_row(i) for i in rows])


@bp.post('')
@require_auth
def add_item():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error='Item needs a name'), 400
    try:
        quantity = parse_qty(data.get('quantity', 1))
    except BadQuantity as err:
        return jsonify(error=str(err)), 400
    db = get_db()
    item = add_stock(db, household_id(), name, quantity,
                     (data.get('unit') or '').strip(), data.get('category'))
    db.commit()
    return jsonify(_row(item)), 201


@bp.post('/add_stock')
@require_auth
def add_stock_route():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error='Item needs a name'), 400
    try:
        quantity = parse_qty(data.get('quantity', 0))
    except BadQuantity as err:
        return jsonify(error=str(err)), 400
    db = get_db()
    item = add_stock(db, household_id(), name, quantity,
                     (data.get('unit') or '').strip(), data.get('category'))
    db.commit()
    return jsonify(_row(item))


@bp.put('/<int:item_id>')
@require_auth
def update_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM pantry_items WHERE id = ? AND household_id = ?',
                      (item_id, household_id())).fetchone()
    if item is None:
        return jsonify(error='Item not found'), 404
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or item['name']).strip() or item['name']
    # dict.get(key, default) only falls back when the key is ABSENT — an
    # explicit JSON null (key present, value None) would return None and wipe
    # unit/category, so treat null the same as "not provided" instead.
    unit = data.get('unit') if data.get('unit') is not None else item['unit']
    category = _clean_category(data.get('category')) if data.get('category') is not None else item['category']
    try:
        # data.get('quantity') collapses "absent" and "explicit null" to the
        # same None, and parse_qty falls back to its `default` arg for None —
        # pass item['quantity'] there so either case preserves the existing value.
        quantity = parse_qty(data.get('quantity'), item['quantity'])
    except BadQuantity as err:
        return jsonify(error=str(err)), 400
    db.execute(
        '''UPDATE pantry_items SET name = ?, quantity = ?, unit = ?, category = ?,
           updated_at = datetime('now') WHERE id = ?''',
        (name, quantity, (unit or '').strip(), category, item_id))
    db.commit()
    item = db.execute('SELECT * FROM pantry_items WHERE id = ?', (item_id,)).fetchone()
    return jsonify(_row(item))


@bp.delete('/<int:item_id>')
@require_auth
def delete_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM pantry_items WHERE id = ? AND household_id = ?',
                      (item_id, household_id())).fetchone()
    if item is None:
        return jsonify(error='Item not found'), 404
    db.execute('DELETE FROM pantry_items WHERE id = ?', (item_id,))
    db.commit()
    return jsonify(ok=True)
