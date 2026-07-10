"""Calendar export: the household meal plan as a downloadable .ics feed
(imports cleanly into Google Calendar, Outlook, Apple Calendar)."""

from datetime import date, datetime, time, timedelta, timezone

from flask import Blueprint, Response, jsonify, request

from db import get_db
from routes.common import household_id, require_auth

bp = Blueprint('calendar_export', __name__, url_prefix='/api/calendar')

MEAL_TIMES = {'breakfast': time(8, 0), 'lunch': time(12, 30), 'dinner': time(18, 30)}
MEAL_LABELS = {'breakfast': 'Breakfast', 'lunch': 'Lunch', 'dinner': 'Dinner'}


def _parse_date(value):
    """Strict-ish YYYY-MM-DD parse; raises ValueError on garbage."""
    return datetime.strptime(value, '%Y-%m-%d').date()


def _escape(text):
    """Escape ICS TEXT per RFC 5545: backslash first, then ; , and newlines."""
    text = text or ''
    text = text.replace('\\', '\\\\')
    text = text.replace(';', '\\;').replace(',', '\\,')
    return text.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '\\n')


@bp.get('/export.ics')
@require_auth
def export_ics():
    try:
        start = _parse_date(request.args['start']) if request.args.get('start') else date.today()
        end = _parse_date(request.args['end']) if request.args.get('end') else start + timedelta(days=30)
    except ValueError:
        return jsonify(error='Dates must look like YYYY-MM-DD'), 400

    rows = get_db().execute(
        '''SELECT p.id, p.date, p.meal_type,
                  r.name AS recipe_name, r.description AS recipe_description,
                  m.name AS cook_name
           FROM meal_plan p
           JOIN recipes r ON r.id = p.recipe_id
           LEFT JOIN members m ON m.id = p.cook_member_id
           WHERE p.household_id = ? AND p.date BETWEEN ? AND ?
           ORDER BY p.date,
                    CASE p.meal_type WHEN 'breakfast' THEN 0 WHEN 'lunch' THEN 1 ELSE 2 END''',
        (household_id(), start.isoformat(), end.isoformat())).fetchall()

    dtstamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Stay Ready//Meal Plan//EN',
        'CALSCALE:GREGORIAN',
    ]
    for row in rows:
        label = MEAL_LABELS[row['meal_type']]
        start_dt = datetime.combine(_parse_date(row['date']), MEAL_TIMES[row['meal_type']])
        end_dt = start_dt + timedelta(hours=1)
        summary = f"{label}: {row['recipe_name']}"
        if row['cook_name']:
            summary += f" — cooked by {row['cook_name']}"
        description = (row['recipe_description'] or '').strip()
        description = (description + '\n\n' if description else '') + 'Stay Ready meal plan'
        lines += [
            'BEGIN:VEVENT',
            f"UID:stayready-{row['id']}@stayready.local",
            f'DTSTAMP:{dtstamp}',
            'DTSTART:' + start_dt.strftime('%Y%m%dT%H%M%S'),
            'DTEND:' + end_dt.strftime('%Y%m%dT%H%M%S'),
            'SUMMARY:' + _escape(summary),
            'DESCRIPTION:' + _escape(description),
            'END:VEVENT',
        ]
    lines.append('END:VCALENDAR')
    ics = '\r\n'.join(lines) + '\r\n'
    return Response(ics, mimetype='text/calendar',
                    headers={'Content-Disposition': 'attachment; filename=stay-ready-meals.ics'})
