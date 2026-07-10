"""Balance: what the meal plan costs, grocery spending, and who owes what."""
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from db import get_db
from routes.common import BadQuantity, household_id, parse_qty, require_auth

bp = Blueprint('balance', __name__)


def _parse_date(value):
    return datetime.strptime(value or '', '%Y-%m-%d').date()


def _week_start(d):
    """Sunday that begins the week containing d."""
    return d - timedelta(days=(d.weekday() + 1) % 7)


@bp.get('/api/balance')
@require_auth
def balance():
    try:
        start = _parse_date(request.args.get('start'))
        end = _parse_date(request.args.get('end'))
    except ValueError:
        return jsonify(error='Dates must look like YYYY-MM-DD'), 400
    if end < start:
        return jsonify(error='End date must be on or after the start date'), 400
    start_s, end_s = start.isoformat(), end.isoformat()

    db = get_db()
    hh = household_id()

    weekly_budget = db.execute(
        'SELECT weekly_budget FROM households WHERE id = ?', (hh,)).fetchone()['weekly_budget']
    members = db.execute(
        'SELECT id, name, color FROM members WHERE household_id = ? ORDER BY id', (hh,)).fetchall()
    members_count = len(members)

    # Cost of the meal plan in the period = sum of each planned meal's recipe cost.
    meal_plan_cost = db.execute(
        '''SELECT COALESCE(SUM(r.cost_total), 0) FROM meal_plan mp
           JOIN recipes r ON r.id = mp.recipe_id
           WHERE mp.household_id = ? AND mp.leftover = 0 AND mp.date BETWEEN ? AND ?''',
        (hh, start_s, end_s)).fetchone()[0]

    days = (end - start).days + 1
    weeks = max(days / 7.0, 0.1)
    budget_for_period = round(weekly_budget * weeks, 2)

    groceries_spent = db.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE household_id = ? AND date BETWEEN ? AND ?',
        (hh, start_s, end_s)).fetchone()[0]

    # Who owes what — over UNSETTLED expenses (settling up zeroes balances but
    # keeps the spending history/chart, which use all expenses). Aggregated in
    # SQL rather than fetching every row into Python.
    total_all = db.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE household_id = ? AND settled = 0',
        (hh,)).fetchone()[0]
    share_each = total_all / members_count if members_count else 0
    paid_by_member = {r['paid_by']: r['total'] for r in db.execute(
        '''SELECT paid_by, SUM(amount) AS total FROM expenses
           WHERE household_id = ? AND settled = 0 AND paid_by IS NOT NULL
           GROUP BY paid_by''', (hh,)).fetchall()}
    balances = [{
        'member_id': m['id'], 'name': m['name'], 'color': m['color'],
        'paid': round(paid_by_member.get(m['id'], 0), 2),
        'share': round(share_each, 2),
        'net': round(paid_by_member.get(m['id'], 0) - share_each, 2),
    } for m in members]

    # Spending over the last 8 weeks (Sunday-start buckets up to the period
    # end). Bounded to that window so this stays cheap as expense history grows
    # over a semester of use, instead of fetching every expense ever logged.
    end_week = _week_start(end)
    window_start = (end_week - timedelta(weeks=7)).isoformat()
    buckets = {(end_week - timedelta(weeks=i)).isoformat(): 0.0 for i in range(8)}
    for e in db.execute(
            'SELECT date, amount FROM expenses WHERE household_id = ? AND date >= ?',
            (hh, window_start)).fetchall():
        try:
            ws = _week_start(_parse_date(e['date'])).isoformat()
        except ValueError:
            continue
        if ws in buckets:
            buckets[ws] += e['amount']
    weekly_spending = [{'week_start': k, 'total': round(v, 2)} for k, v in sorted(buckets.items())]

    # Recent trips for the log list.
    exp_rows = db.execute(
        '''SELECT e.id, e.date, e.amount, e.paid_by, e.note, m.name AS paid_by_name
           FROM expenses e LEFT JOIN members m ON m.id = e.paid_by
           WHERE e.household_id = ? ORDER BY e.date DESC, e.id DESC LIMIT 25''',
        (hh,)).fetchall()
    expenses = [{'id': r['id'], 'date': r['date'], 'amount': r['amount'],
                 'paid_by': r['paid_by'], 'paid_by_name': r['paid_by_name'], 'note': r['note']}
                for r in exp_rows]

    return jsonify({
        'weekly_budget': weekly_budget,
        'members_count': members_count,
        'members': [{'id': m['id'], 'name': m['name'], 'color': m['color']} for m in members],
        'period': {
            'start': start_s, 'end': end_s, 'days': days, 'weeks': round(weeks, 2),
            'meal_plan_cost': round(meal_plan_cost, 2),
            'budget_for_period': budget_for_period,
            'groceries_spent': round(groceries_spent, 2),
            'per_person_meal_share': round(meal_plan_cost / members_count, 2) if members_count else 0,
        },
        'balances': balances,
        'weekly_spending': weekly_spending,
        'expenses': expenses,
    })


@bp.post('/api/expenses')
@require_auth
def add_expense():
    data = request.get_json(silent=True) or {}
    try:
        date = _parse_date(data.get('date'))
    except ValueError:
        return jsonify(error='Date must be a YYYY-MM-DD date'), 400
    try:
        amount = parse_qty(data.get('amount'))
    except BadQuantity:
        return jsonify(error='Amount must be a number'), 400
    if amount <= 0:
        return jsonify(error='Amount must be greater than 0'), 400

    db = get_db()
    hh = household_id()
    paid_by = data.get('paid_by')
    if paid_by in (None, ''):
        paid_by = None
    else:
        try:
            paid_by = int(paid_by)
        except (TypeError, ValueError):
            return jsonify(error='paid_by must be a member id'), 400
        if db.execute('SELECT 1 FROM members WHERE id = ? AND household_id = ?',
                      (paid_by, hh)).fetchone() is None:
            return jsonify(error='Member not found'), 404

    note = (data.get('note') or '').strip()[:120]
    cur = db.execute(
        'INSERT INTO expenses (household_id, date, amount, paid_by, note) VALUES (?, ?, ?, ?, ?)',
        (hh, date.isoformat(), round(amount, 2), paid_by, note))
    db.commit()
    return jsonify(id=cur.lastrowid), 201


@bp.delete('/api/expenses/<int:expense_id>')
@require_auth
def delete_expense(expense_id):
    db = get_db()
    row = db.execute('SELECT id FROM expenses WHERE id = ? AND household_id = ?',
                     (expense_id, household_id())).fetchone()
    if row is None:
        return jsonify(error='Expense not found'), 404
    db.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    db.commit()
    return jsonify(ok=True)


@bp.post('/api/expenses/settle')
@require_auth
def settle_up():
    """Mark all outstanding expenses settled — zeroes balances, keeps history."""
    db = get_db()
    cur = db.execute('UPDATE expenses SET settled = 1 WHERE household_id = ? AND settled = 0',
                     (household_id(),))
    db.commit()
    return jsonify(ok=True, settled=cur.rowcount)
