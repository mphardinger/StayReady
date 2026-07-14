import secrets

from flask import Blueprint, g, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db
from extensions import limiter
from routes.common import MEMBER_COLORS, require_auth
from seed_recipes import seed_household

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# No lookalike characters (0/O, 1/I) so invite codes are easy to read aloud
CODE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def _new_invite_code(db):
    while True:
        code = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(6))
        if not db.execute('SELECT 1 FROM households WHERE invite_code = ?', (code,)).fetchone():
            return code


def _user_payload(db, user):
    hh = db.execute('SELECT * FROM households WHERE id = ?', (user['household_id'],)).fetchone()
    return {
        'id': user['id'],
        'username': user['username'],
        'display_name': user['display_name'],
        'household_id': user['household_id'],
        'household_name': hh['name'],
        'invite_code': hh['invite_code'],
        'weekly_budget': hh['weekly_budget'],
    }


def _add_member(db, hh_id, name):
    count = db.execute('SELECT COUNT(*) AS c FROM members WHERE household_id = ?',
                       (hh_id,)).fetchone()['c']
    db.execute('INSERT INTO members (household_id, name, color) VALUES (?, ?, ?)',
               (hh_id, name, MEMBER_COLORS[count % len(MEMBER_COLORS)]))


@bp.post('/register')
@limiter.limit('10 per hour')
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    display_name = (data.get('display_name') or '').strip() or username
    household_name = (data.get('household_name') or '').strip()
    invite_code = (data.get('invite_code') or '').strip().upper()

    if len(username) < 3:
        return jsonify(error='Username must be at least 3 characters'), 400
    if len(password) < 6:
        return jsonify(error='Password must be at least 6 characters'), 400
    if not household_name and not invite_code:
        return jsonify(error='Name a new household or enter an invite code'), 400

    db = get_db()
    if db.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone():
        return jsonify(error='That username is taken'), 409

    if invite_code:
        hh = db.execute('SELECT * FROM households WHERE invite_code = ?', (invite_code,)).fetchone()
        if hh is None:
            return jsonify(error='No household found for that invite code'), 404
        hh_id = hh['id']
    else:
        cur = db.execute('INSERT INTO households (name, invite_code) VALUES (?, ?)',
                         (household_name, _new_invite_code(db)))
        hh_id = cur.lastrowid
        seed_household(db, hh_id)

    _add_member(db, hh_id, display_name)
    cur = db.execute(
        'INSERT INTO users (household_id, username, password_hash, display_name) VALUES (?, ?, ?, ?)',
        (hh_id, username, generate_password_hash(password), display_name))
    db.commit()

    user = db.execute('SELECT * FROM users WHERE id = ?', (cur.lastrowid,)).fetchone()
    session.permanent = True
    session['user_id'] = user['id']
    return jsonify(user=_user_payload(db, user)), 201


@bp.post('/login')
@limiter.limit('10 per minute; 30 per hour')
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify(error='Wrong username or password'), 401
    session.permanent = True
    session['user_id'] = user['id']
    return jsonify(user=_user_payload(db, user))


@bp.post('/logout')
def logout():
    session.clear()
    return jsonify(ok=True)


@bp.post('/delete_account')
@require_auth
@limiter.limit('5 per hour')
def delete_account():
    """Permanently delete the signed-in account (Google Play requires this to
    exist in-app and via the web). Re-confirms the password so a borrowed
    phone with an open session can't nuke an account. If this was the
    household's last account, the household and all its data cascade-delete."""
    data = request.get_json(silent=True) or {}
    password = data.get('password') or ''
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    if not check_password_hash(user['password_hash'], password):
        return jsonify(error='Wrong password'), 403
    hh_id = user['household_id']
    db.execute('DELETE FROM users WHERE id = ?', (user['id'],))
    remaining = db.execute('SELECT COUNT(*) AS c FROM users WHERE household_id = ?',
                           (hh_id,)).fetchone()['c']
    household_deleted = remaining == 0
    if household_deleted:
        # Last account: erase the household and everything in it (recipes,
        # meal plan, pantry, shopping/sale items, expenses — FK cascades).
        db.execute('DELETE FROM households WHERE id = ?', (hh_id,))
    db.commit()
    session.clear()
    return jsonify(ok=True, household_deleted=household_deleted)


@bp.get('/me')
@require_auth
def me():
    return jsonify(user=_user_payload(get_db(), g.user))
