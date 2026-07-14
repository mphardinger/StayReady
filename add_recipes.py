"""Backfill seed recipes into existing households.

Two jobs, both idempotent:
1. INSERT any seed recipe a household is missing (matched by name,
   case-insensitive).
2. UPDATE the extended-nutrition fields (sodium/potassium/phosphorus/fiber/
   sugar + diet tags) on recipes whose names match seed data — these fields
   shipped after the original recipes, so existing rows have zeros. Only the
   new fields are touched; user edits to cost, servings, instructions, etc.
   are preserved.

Usage (from the app directory):  python add_recipes.py
"""

import db
from seed_recipes import SEED_RECIPES, insert_recipe


def main():
    conn = db.connect()
    households = conn.execute('SELECT id, name FROM households').fetchall()
    if not households:
        print('No households yet — nothing to do.')
        return

    seed_by_name = {r['name'].lower(): r for r in SEED_RECIPES}
    total_added = total_updated = 0
    for hh in households:
        existing = conn.execute(
            'SELECT id, name, sodium_mg, potassium_mg, phosphorus_mg, fiber_g, '
            'sugar_g, tags FROM recipes WHERE household_id = ?', (hh['id'],)).fetchall()
        existing_names = {row['name'].lower() for row in existing}

        added = 0
        for r in SEED_RECIPES:
            if r['name'].lower() not in existing_names:
                insert_recipe(conn, hh['id'], r)
                added += 1

        updated = 0
        for row in existing:
            seed = seed_by_name.get(row['name'].lower())
            if seed is None:
                continue
            new_vals = (seed.get('sodium_mg', 0), seed.get('potassium_mg', 0),
                        seed.get('phosphorus_mg', 0), seed.get('fiber_g', 0),
                        seed.get('sugar_g', 0), ','.join(seed.get('tags', [])))
            current = (row['sodium_mg'], row['potassium_mg'], row['phosphorus_mg'],
                       row['fiber_g'], row['sugar_g'])
            # Only touch rows that clearly haven't been hand-edited: all five
            # nutrition fields still zero and no tags set.
            has_new_data = any(new_vals[:5]) or bool(new_vals[5])
            if not any(current) and not row['tags'] and has_new_data:
                conn.execute(
                    '''UPDATE recipes SET sodium_mg = ?, potassium_mg = ?,
                           phosphorus_mg = ?, fiber_g = ?, sugar_g = ?, tags = ?
                       WHERE id = ?''', new_vals + (row['id'],))
                updated += 1

        conn.commit()
        total_added += added
        total_updated += updated
        print(f'{hh["name"]}: added {added}, nutrition-updated {updated}')

    print(f'Done — {total_added} added, {total_updated} updated across '
          f'{len(households)} household(s).')


if __name__ == '__main__':
    main()
