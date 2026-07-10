from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import HEX_COLOR_RE, MEMBER_COLORS, household_id, require_auth

bp = Blueprint('members', __name__, url_prefix='/api/members')


def _row(m):
    return {'id': m['id'], 'name': m['name'], 'color': m['color']}


@bp.get('')
@require_auth
def list_members():
    rows = get_db().execute(
        'SELECT * FROM members WHERE household_id = ? ORDER BY id', (household_id(),)).fetchall()
    return jsonify([_row(m) for m in rows])


@bp.post('')
@require_auth
def add_member():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error='Member needs a name'), 400
    db = get_db()
    color = (data.get('color') or '').strip()
    if not color:
        count = db.execute('SELECT COUNT(*) AS c FROM members WHERE household_id = ?',
                           (household_id(),)).fetchone()['c']
        color = MEMBER_COLORS[count % len(MEMBER_COLORS)]
    elif not HEX_COLOR_RE.match(color):
        return jsonify(error='Color must be a hex value like #3E7C4F'), 400
    cur = db.execute('INSERT INTO members (household_id, name, color) VALUES (?, ?, ?)',
                     (household_id(), name, color))
    db.commit()
    m = db.execute('SELECT * FROM members WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(_row(m)), 201


@bp.put('/<int:member_id>')
@require_auth
def update_member(member_id):
    db = get_db()
    m = db.execute('SELECT * FROM members WHERE id = ? AND household_id = ?',
                   (member_id, household_id())).fetchone()
    if m is None:
        return jsonify(error='Member not found'), 404
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or m['name']).strip() or m['name']
    color = (data.get('color') or m['color']).strip() or m['color']
    if not HEX_COLOR_RE.match(color):
        return jsonify(error='Color must be a hex value like #3E7C4F'), 400
    db.execute('UPDATE members SET name = ?, color = ? WHERE id = ?', (name, color, member_id))
    db.commit()
    m = db.execute('SELECT * FROM members WHERE id = ?', (member_id,)).fetchone()
    return jsonify(_row(m))


@bp.delete('/<int:member_id>')
@require_auth
def delete_member(member_id):
    db = get_db()
    m = db.execute('SELECT * FROM members WHERE id = ? AND household_id = ?',
                   (member_id, household_id())).fetchone()
    if m is None:
        return jsonify(error='Member not found'), 404
    db.execute('DELETE FROM members WHERE id = ?', (member_id,))
    db.commit()
    return jsonify(ok=True)
