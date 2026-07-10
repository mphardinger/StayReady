import math
import re
from functools import wraps

from flask import g, jsonify, session

from db import get_db

# Muted, serious set of cook colors (distinguishable without the rainbow):
# red, near-black, slate, taupe, grey, muted brass.
MEMBER_COLORS = ['#C0271F', '#2C2C33', '#3F5060', '#8C6D5B', '#6E6E76', '#A6863C']

PANTRY_CATEGORIES = ['produce', 'meat', 'dairy', 'grains', 'canned', 'frozen',
                     'spices', 'snacks', 'other']

MEAL_TYPES = ['breakfast', 'lunch', 'dinner']


def require_auth(view):
    """Loads the signed-in user onto g.user or returns 401."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(error='Not signed in'), 401
        row = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if row is None:
            session.clear()
            return jsonify(error='Not signed in'), 401
        g.user = row
        return view(*args, **kwargs)
    return wrapped


def household_id():
    return g.user['household_id']


def norm_name(name):
    """Canonical form for matching ingredient/pantry names: lowercase, collapsed whitespace."""
    return ' '.join((name or '').strip().lower().split())


class BadQuantity(ValueError):
    """Malformed quantity input; message is user-facing."""


def parse_qty(value, default=0.0):
    """Coerce a request value to a non-negative finite quantity; missing -> default, junk -> raise."""
    try:
        q = float(value) if value is not None else default
        if not math.isfinite(q):
            raise ValueError
    except (TypeError, ValueError):
        raise BadQuantity('Quantity must be a number')
    return max(0.0, q)


HEX_COLOR_RE = re.compile(r'^#[0-9A-Fa-f]{6}$')
