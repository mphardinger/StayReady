"""Backfill seed recipes into existing households.

New households get the full SEED_RECIPES list at registration, but households
created before a recipe was added never see it. This script inserts any seed
recipe a household is missing (matched by name, case-insensitive), so it is
safe to run repeatedly — reruns are no-ops.

Usage (from the app directory):  python add_recipes.py
"""

import db
from seed_recipes import SEED_RECIPES


def main():
    conn = db.connect()
    households = conn.execute('SELECT id, name FROM households').fetchall()
    if not households:
        print('No households yet — nothing to do.')
        return

    total_added = 0
    for hh in households:
        existing = {
            row['name'].lower()
            for row in conn.execute(
                'SELECT name FROM recipes WHERE household_id = ?', (hh['id'],))
        }
        missing = [r for r in SEED_RECIPES if r['name'].lower() not in existing]
        for r in missing:
            cur = conn.execute(
                '''INSERT INTO recipes (household_id, name, emoji, description, meal_type,
                                        time_minutes, servings, cost_total, calories,
                                        protein_g, carbs_g, fat_g, instructions)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (hh['id'], r['name'], r['emoji'], r['description'], r['meal_type'],
                 r['time_minutes'], r['servings'], r['cost_total'], r['calories'],
                 r['protein_g'], r['carbs_g'], r['fat_g'], r['instructions']))
            conn.executemany(
                'INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)',
                [(cur.lastrowid, name, qty, unit) for (name, qty, unit) in r['ingredients']])
        conn.commit()
        total_added += len(missing)
        print(f'{hh["name"]}: added {len(missing)} recipe(s)')

    print(f'Done — {total_added} recipe(s) added across {len(households)} household(s).')


if __name__ == '__main__':
    main()
