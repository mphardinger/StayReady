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


def _norm_recovery_code(raw):
    """Recovery codes compare case-insensitively, ignoring dashes/spaces."""
    return ''.join(ch for ch in str(raw or '').upper() if ch.isalnum())


# Unlike passwords, recovery codes are CSPRNG-random (32^8 ≈ 1.1e12 space), so
# they don't need scrypt-grade stretching — pbkdf2 at 50k iterations keeps an
# offline attack on a leaked DB infeasible while making signup (9 hashes: the
# password + 8 codes) fast enough for budget hosting CPUs.
_CODE_HASH_METHOD = 'pbkdf2:sha256:50000'


def _issue_recovery_codes(db, user_id, count=8):
    """Replace the user's recovery codes with a fresh set. Returns the
    plaintext codes — the only time they ever exist outside a hash."""
    db.execute('DELETE FROM recovery_codes WHERE user_id = ?', (user_id,))
    codes = []
    for _ in range(count):
        code = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(8))
        codes.append(code[:4] + '-' + code[4:])
        db.execute('INSERT INTO recovery_codes (user_id, code_hash) VALUES (?, ?)',
                   (user_id, generate_password_hash(code, method=_CODE_HASH_METHOD)))
    return codes


# Burned on lookups for nonexistent usernames so response timing doesn't
# reveal whether an account exists.
_DUMMY_HASH = generate_password_hash('dummy-timing-pad')


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
    recovery_codes = _issue_recovery_codes(db, cur.lastrowid)
    db.commit()

    user = db.execute('SELECT * FROM users WHERE id = ?', (cur.lastrowid,)).fetchone()
    session.permanent = True
    session['user_id'] = user['id']
    # recovery_codes appear in this response ONCE — the client shows them and
    # they are never retrievable again (only regenerable).
    return jsonify(user=_user_payload(db, user), recovery_codes=recovery_codes), 201


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


@bp.post('/reset_password')
@limiter.limit('5 per hour')
def reset_password():
    """Forgot-password flow: username + one unused recovery code -> new
    password. The error message never reveals whether the username exists."""
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    code = _norm_recovery_code(data.get('code'))
    new_password = data.get('new_password') or ''
    if len(new_password) < 6:
        return jsonify(error='New password must be at least 6 characters'), 400
    generic = (jsonify(error='No match for that username and recovery code'), 403)

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None or not code:
        check_password_hash(_DUMMY_HASH, code or 'x')  # keep timing flat
        return generic
    rows = db.execute(
        'SELECT * FROM recovery_codes WHERE user_id = ? AND used = 0',
        (user['id'],)).fetchall()
    matched = next((r for r in rows if check_password_hash(r['code_hash'], code)), None)
    if matched is None:
        return generic
    db.execute('UPDATE recovery_codes SET used = 1 WHERE id = ?', (matched['id'],))
    db.execute('UPDATE users SET password_hash = ? WHERE id = ?',
               (generate_password_hash(new_password), user['id']))
    db.commit()
    session.permanent = True
    session['user_id'] = user['id']
    remaining = db.execute(
        'SELECT COUNT(*) AS c FROM recovery_codes WHERE user_id = ? AND used = 0',
        (user['id'],)).fetchone()['c']
    return jsonify(user=_user_payload(db, user), codes_left=remaining)


@bp.post('/recovery_codes')
@require_auth
@limiter.limit('5 per hour')
def regenerate_recovery_codes():
    """Fresh set of codes (invalidates all old ones). Password-confirmed so an
    open session on a borrowed phone can't mint codes for later takeover."""
    data = request.get_json(silent=True) or {}
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (g.user['id'],)).fetchone()
    if not check_password_hash(user['password_hash'], data.get('password') or ''):
        return jsonify(error='Wrong password'), 403
    codes = _issue_recovery_codes(db, user['id'])
    db.commit()
    return jsonify(recovery_codes=codes)


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
