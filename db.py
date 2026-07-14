import os
import sqlite3

from flask import g

# Where the database (and instance/secret_key.txt, see app.py) live. Defaults
# to next to the code for local/LAN use. On a host with an ephemeral
# filesystem (the code directory doesn't survive a redeploy), set
# STAYREADY_DATA_DIR to a mounted persistent volume instead.
DATA_DIR = os.environ.get('STAYREADY_DATA_DIR') or os.path.dirname(os.path.abspath(__file__))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'stayready.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS households (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    invite_code TEXT NOT NULL UNIQUE,
    weekly_budget REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    color TEXT NOT NULL DEFAULT '#3E7C4F'
);

CREATE TABLE IF NOT EXISTS pantry_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    quantity REAL NOT NULL DEFAULT 0,
    unit TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'other',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL DEFAULT '🍽️',
    description TEXT NOT NULL DEFAULT '',
    meal_type TEXT NOT NULL DEFAULT 'dinner' CHECK (meal_type IN ('breakfast','lunch','dinner','any')),
    time_minutes INTEGER NOT NULL DEFAULT 30,
    servings INTEGER NOT NULL DEFAULT 4,
    cost_total REAL NOT NULL DEFAULT 0,
    calories INTEGER NOT NULL DEFAULT 0,
    protein_g REAL NOT NULL DEFAULT 0,
    carbs_g REAL NOT NULL DEFAULT 0,
    fat_g REAL NOT NULL DEFAULT 0,
    -- Extended nutrition (per serving, ESTIMATES) for dietary tracking:
    -- renal diets watch sodium/potassium/phosphorus; diabetic tracking watches
    -- carbs/sugar/fiber. 0 means "not entered", the UI shows an em dash.
    sodium_mg INTEGER NOT NULL DEFAULT 0,
    potassium_mg INTEGER NOT NULL DEFAULT 0,
    phosphorus_mg INTEGER NOT NULL DEFAULT 0,
    fiber_g REAL NOT NULL DEFAULT 0,
    sugar_g REAL NOT NULL DEFAULT 0,
    -- Comma-separated diet tag slugs from routes/recipes.py DIET_TAGS
    -- (kidney, fodmap, diabetic, vegetarian). Criteria documented there.
    tags TEXT NOT NULL DEFAULT '',
    instructions TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    quantity REAL NOT NULL DEFAULT 0,
    unit TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS meal_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    date TEXT NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast','lunch','dinner')),
    recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    cook_member_id INTEGER REFERENCES members(id) ON DELETE SET NULL,
    cooked INTEGER NOT NULL DEFAULT 0,
    leftover INTEGER NOT NULL DEFAULT 0,
    UNIQUE (household_id, date, meal_type)
);

-- Password-recovery codes: shown once at signup (or regenerated from the
-- Account card), stored only as hashes, single-use. The app collects no
-- email, so these are the way back into a forgotten-password account.
CREATE TABLE IF NOT EXISTS recovery_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code_hash TEXT NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- "On sale this week" list typed in from a store flyer; the recipe
-- recommendations and week builder prioritize recipes using these items.
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    price REAL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    paid_by INTEGER REFERENCES members(id) ON DELETE SET NULL,
    note TEXT NOT NULL DEFAULT '',
    settled INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def get_db():
    if 'db' not in g:
        g.db = connect()
    return g.db


def close_db(_exc=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Columns added after initial release — applied to existing databases on startup.
# (name, DDL to add it) keyed by table.
MIGRATIONS = {
    'households': [
        ('weekly_budget', 'ALTER TABLE households ADD COLUMN weekly_budget REAL NOT NULL DEFAULT 0'),
    ],
    'meal_plan': [
        ('leftover', 'ALTER TABLE meal_plan ADD COLUMN leftover INTEGER NOT NULL DEFAULT 0'),
    ],
    'expenses': [
        ('settled', 'ALTER TABLE expenses ADD COLUMN settled INTEGER NOT NULL DEFAULT 0'),
    ],
    'recipes': [
        ('sodium_mg', 'ALTER TABLE recipes ADD COLUMN sodium_mg INTEGER NOT NULL DEFAULT 0'),
        ('potassium_mg', 'ALTER TABLE recipes ADD COLUMN potassium_mg INTEGER NOT NULL DEFAULT 0'),
        ('phosphorus_mg', 'ALTER TABLE recipes ADD COLUMN phosphorus_mg INTEGER NOT NULL DEFAULT 0'),
        ('fiber_g', 'ALTER TABLE recipes ADD COLUMN fiber_g REAL NOT NULL DEFAULT 0'),
        ('sugar_g', 'ALTER TABLE recipes ADD COLUMN sugar_g REAL NOT NULL DEFAULT 0'),
        ('tags', "ALTER TABLE recipes ADD COLUMN tags TEXT NOT NULL DEFAULT ''"),
    ],
}


def _apply_migrations(conn):
    for table, cols in MIGRATIONS.items():
        existing = {row['name'] for row in conn.execute('PRAGMA table_info(' + table + ')')}
        for col_name, ddl in cols:
            if col_name not in existing:
                conn.execute(ddl)


def init_db():
    conn = connect()
    conn.executescript(SCHEMA)
    _apply_migrations(conn)
    conn.commit()
    conn.close()


def nutrition_score(calories, protein_g, ingredient_count):
    """0-100 per serving: protein density (up to 40) + calorie balance around
    ~500 kcal (up to 30) + ingredient variety (up to 30)."""
    if not calories or calories <= 0:
        return 50
    protein_pts = min(40, (protein_g or 0) * 4 / calories * 133)
    balance_pts = max(0, 30 - abs(calories - 500) * 30 / 500)
    variety_pts = min(30, (ingredient_count or 0) * 3)
    return round(min(100, protein_pts + balance_pts + variety_pts))
