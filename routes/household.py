"""Household-level settings (name, weekly grocery budget)."""
import math

from flask import Blueprint, g, jsonify, request

from db import get_db
from routes.common import household_id, require_auth

bp = Blueprint('household', __name__, url_prefix='/api/household')


def _payload(hh):
    return {
        'id': hh['id'],
        'name': hh['name'],
        'invite_code': hh['invite_code'],
        'weekly_budget': hh['weekly_budget'],
    }


@bp.get('')
@require_auth
def get_household():
    hh = get_db().execute('SELECT * FROM households WHERE id = ?', (household_id(),)).fetchone()
    return jsonify(_payload(hh))


@bp.put('')
@require_auth
def update_household():
    db = get_db()
    hh = db.execute('SELECT * FROM households WHERE id = ?', (household_id(),)).fetchone()
    data = request.get_json(silent=True) or {}

    name = hh['name']
    if 'name' in data:
        name = (data.get('name') or '').strip() or hh['name']

    budget = hh['weekly_budget']
    if 'weekly_budget' in data:
        try:
            budget = float(data.get('weekly_budget'))
            if not math.isfinite(budget) or budget < 0:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify(error='Budget must be a number (0 or more)'), 400

    db.execute('UPDATE households SET name = ?, weekly_budget = ? WHERE id = ?',
               (name, round(budget, 2), household_id()))
    db.commit()
    hh = db.execute('SELECT * FROM households WHERE id = ?', (household_id(),)).fetchone()
    return jsonify(_payload(hh))
