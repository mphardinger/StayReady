"""'On sale this week' list — typed in from a store flyer. Recipe suggestions
and the week builder prioritize recipes whose ingredients match these items
(matching is norm_name substring, client-side). Household-shared."""

from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import BadQuantity, household_id, norm_name, parse_qty, require_auth

bp = Blueprint('sales', __name__, url_prefix='/api/sales')


def _item_json(row):
    return {'id': row['id'], 'name': row['name'], 'price': row['price']}


@bp.get('')
@require_auth
def list_sales():
    rows = get_db().execute(
        'SELECT * FROM sale_items WHERE household_id = ? ORDER BY lower(name)',
        (household_id(),)).fetchall()
    return jsonify([_item_json(r) for r in rows])


@bp.post('')
@require_auth
def add_sale():
    data = request.get_json(silent=True) or {}
    raw_name = data.get('name')
    name = norm_name(raw_name) if isinstance(raw_name, str) else ''
    if not name:
        return jsonify(error='Item needs a name'), 400
    price = None
    if data.get('price') not in (None, ''):
        try:
            price = parse_qty(data.get('price'))
        except BadQuantity:
            return jsonify(error='Price must be a number'), 400
    db = get_db()
    existing = db.execute(
        'SELECT * FROM sale_items WHERE household_id = ? AND name = ?',
        (household_id(), name)).fetchone()
    if existing:
        # Re-adding without a price keeps the stored one (COALESCE) — only an
        # explicit new price replaces it.
        db.execute('UPDATE sale_items SET price = COALESCE(?, price) WHERE id = ?',
                   (price, existing['id']))
        db.commit()
        row = db.execute('SELECT * FROM sale_items WHERE id = ?', (existing['id'],)).fetchone()
        return jsonify(_item_json(row))
    cur = db.execute(
        'INSERT INTO sale_items (household_id, name, price) VALUES (?, ?, ?)',
        (household_id(), name, price))
    db.commit()
    row = db.execute('SELECT * FROM sale_items WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(_item_json(row)), 201


@bp.delete('/<int:item_id>')
@require_auth
def delete_sale(item_id):
    db = get_db()
    row = db.execute('SELECT id FROM sale_items WHERE id = ? AND household_id = ?',
                     (item_id, household_id())).fetchone()
    if row is None:
        return jsonify(error='Item not found'), 404
    db.execute('DELETE FROM sale_items WHERE id = ?', (item_id,))
    db.commit()
    return jsonify(ok=True)


@bp.delete('')
@require_auth
def clear_sales():
    """Clear the whole list — for starting a fresh flyer week."""
    db = get_db()
    db.execute('DELETE FROM sale_items WHERE household_id = ?', (household_id(),))
    db.commit()
    return jsonify(ok=True)
