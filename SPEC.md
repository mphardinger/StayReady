# Stay Ready — build spec & conventions

Meal-planning app: Flask + SQLite backend, vanilla-JS SPA frontend. Households share
one pantry, recipe box, and meal plan; users belong to a household; members are the
assignable cooks.

## Run

`python app.py` → http://127.0.0.1:8008 (requires `pip install flask`).

## Files & ownership

- `app.py` — Flask app, registers all blueprints (already lists every route module).
- `db.py` — schema, `get_db()`, `nutrition_score(calories, protein_g, ingredient_count)`.
- `routes/common.py` — `require_auth` (sets `g.user`), `household_id()`, `norm_name()`,
  `PANTRY_CATEGORIES`, `MEAL_TYPES`, `MEMBER_COLORS`.
- `routes/pantry.py` — also exports `add_stock(db, hh_id, name, quantity, unit, category)`
  (upsert-increment by normalized name + unit; caller commits).
- `static/js/app.js` — `h()` DOM builder, `App.api`, router, `App.modal`, `App.toast`,
  date/format helpers, `App.recommend`. Read it before writing any view.
- `static/js/views/pantry.js` — the exemplar view; copy its structure and style.
- `static/index.html` — already includes every view's `<script>` tag. Do not edit.

## Conventions (mandatory)

- **Backend**: every data route uses `@require_auth` and scopes ALL queries by
  `household_id()` (including `WHERE id = ? AND household_id = ?` on single-row ops).
  Errors: `jsonify(error='human readable message'), 4xx`. Commit after writes.
  Parameterized SQL only.
- **Frontend**: build DOM only with `h()` — never innerHTML with data (XSS).
  Views: `App.registerView(name, {title, icon, async render(container)})`.
  Dates: `App.fmtDate/parseDate/addDays/today` (local time — NEVER `toISOString()`).
  Money `App.fmtMoney`, minutes `App.fmtMinutes`, quantities `App.fmtQty`.
  Errors → `App.toast(msg, 'error')`. Re-render a view via `this.render(container)`.
- Ingredient/pantry matching is by `norm_name` (lowercase, trimmed, collapsed spaces).
  "Do we have it" indicators ignore units; shopping-list math is unit-aware.

## Data model (SQLite, see db.py)

households(id, name, invite_code) · users(id, household_id, username, password_hash, display_name)
· members(id, household_id, name, color) · pantry_items(id, household_id, name, quantity, unit, category, updated_at)
· recipes(id, household_id, name, emoji, description, meal_type[breakfast|lunch|dinner|any],
time_minutes, servings, cost_total, calories, protein_g, carbs_g, fat_g, instructions)
· recipe_ingredients(id, recipe_id, name, quantity, unit)
· meal_plan(id, household_id, date 'YYYY-MM-DD', meal_type[breakfast|lunch|dinner], recipe_id,
cook_member_id NULLABLE→members ON DELETE SET NULL, cooked 0/1, UNIQUE(household_id, date, meal_type)).
recipes/recipe rows cascade-delete their plan entries. Macros are PER SERVING; cost_total is whole-recipe.

## API contract

Existing (built): `/api/auth/*` (register/login/logout/me), `/api/members` CRUD,
`/api/pantry` (GET, POST, PUT /<id>, DELETE /<id>, POST /add_stock {name,quantity,unit,category?}).

### routes/recipes.py — blueprint `recipes`, prefix `/api/recipes`

Recipe JSON shape (used everywhere):
```
{id, name, emoji, description, meal_type, time_minutes, servings, cost_total,
 cost_per_serving,            // round(cost_total / max(servings,1), 2)
 calories, protein_g, carbs_g, fat_g,
 sodium_mg, potassium_mg, phosphorus_mg, fiber_g, sugar_g,  // per serving, ESTIMATES (0 = not entered)
 tags,                        // list of diet slugs from routes/recipes.py DIET_TAGS
                              // (kidney|fodmap|diabetic|vegetarian); criteria documented there.
                              // UI must show the not-medical-advice disclaimer near diet features.
 nutrition_score,             // db.nutrition_score(calories, protein_g, len(ingredients))
 ingredients: [{id, name, quantity, unit}],
 have_count, ingredient_count // pantry match: norm_name equal AND pantry quantity > 0
}
```
- `GET ''` → list of the above (no `instructions`), ordered by name. Compute pantry
  matches with ONE pantry query, not per-recipe queries.
- `GET '/<int:id>'` → full shape + `instructions`.
- `POST ''` body `{name*, emoji?, description?, meal_type?, time_minutes?, servings?,
  cost_total?, calories?, protein_g?, carbs_g?, fat_g?, instructions?,
  ingredients?: [{name, quantity, unit}]}` → 201 full shape. Validate: name required;
  numbers coerced with safe fallbacks (bad number → 400); meal_type must be one of the 4.
- `PUT '/<int:id>'` same body, replaces ingredient rows.
- `DELETE '/<int:id>'` → `{ok: true}` (cascades to plan entries).

### routes/plan.py — blueprint `plan`, prefix `/api/plan`

Entry JSON: `{id, date, meal_type, cooked: 0|1,
 recipe: {id, name, emoji, time_minutes, servings, meal_type},
 cook: {id, name, color} | null}`
- `GET '?start=YYYY-MM-DD&end=YYYY-MM-DD'` → list (validate dates, 400 if malformed;
  date BETWEEN start AND end, string compare is fine).
- `PUT ''` body `{date*, meal_type*, recipe_id*, cook_member_id?}` → upsert the slot
  (INSERT ... ON CONFLICT(household_id, date, meal_type) DO UPDATE, or delete+insert).
  Validate recipe and member belong to the household. Returns the entry JSON.
- `DELETE '?date=&meal_type='` → clear that slot, `{ok: true}` (404 if empty).
- `POST '/<int:entry_id>/cooked'` → toggle cooked→1. When newly marked cooked, for each
  recipe ingredient decrement the matching pantry item (norm_name + same unit,
  case-insensitive) down to min 0. Returns `{entry, deducted: [{name, amount}]}`.

### routes/shopping.py — blueprint `shopping`, prefix `/api/shopping`

- `GET '?start=&end='` → what to buy for all planned meals in range:
```
{meals_count, days: <days in range>, items: [
  {name, unit, needed, have, to_buy,      // to_buy = max(0, needed - have), rounded to 2dp
   category,                              // pantry item's category if matched, else 'other'
   recipes: [up to 3 recipe names]}]}
```
  Aggregate `recipe_ingredients` across plan entries in range (skip `cooked=1` entries),
  keyed by (norm_name, unit lowercased). Pantry `have` matches norm_name + unit
  (unit mismatch → have 0). Include only items with `to_buy > 0` in `items`, sorted by
  category then name. Quantities × 1 per planned meal (recipes already make multiple servings).
- `POST '/purchase'` body `{name, quantity, unit, category?}` → calls
  `pantry.add_stock`, commits, returns the pantry item JSON
  `{id, name, quantity, unit, category}`.

### routes/sales.py — blueprint `sales`, prefix `/api/sales`

Household-shared "on sale this week" list (typed in from a store flyer; there is
no live store integration). Matching against recipe ingredients happens
client-side by norm_name substring in either direction.
- `GET ''` → `[{id, name, price|null}]` (name is stored normalized)
- `POST ''` `{name*, price?}` → upserts by normalized name, 201/200
- `DELETE '/<int:id>'` → `{ok: true}` · `DELETE ''` → clear list

### routes/calendar_export.py — blueprint `calendar_export`, prefix `/api/calendar`

- `GET '/export.ics?start=&end='` → `text/calendar` download (`Content-Disposition:
  attachment; filename=stay-ready-meals.ics`). One VEVENT per plan entry in range:
  breakfast 08:00, lunch 12:30, dinner 18:30 local floating time (no TZID), 1 hour.
  SUMMARY: `🍳 Breakfast: Veggie Scramble` (meal emoji from MEAL_META table below;
  🍳/🥪/🍽️). If a cook is set append ` — cooked by <name>`. DESCRIPTION: recipe
  description + `Stay Ready meal plan`. Escape ICS text (backslash, semicolon, comma,
  newlines). UID: `stayready-<entry id>@stayready.local`. Include VCALENDAR wrapper
  with PRODID/VERSION/CALSCALE and DTSTAMP (UTC now) per event. CRLF line endings.

### Frontend views (static/js/views/)

- `recipes.js` — view name `recipes`, title `Recipes`, icon 🍳.
- `plan.js` — view name `plan`, title `Meal Plan`, icon 📅.
- `shopping.js` — view name `shopping`, title `Shopping List`, icon 🛒.
- `dashboard.js` — view name `dashboard`, title `Today`, icon 🌞.

`App.recommend(recipes, category, mealType, limit)` sorts by `time_minutes` /
`nutrition_score` desc / `cost_per_serving`; categories are in `App.REC_CATS`
(`time` ⚡ Quickest, `nutrition` 💪 Healthiest, `cost` 💰 Cheapest).
`App.MEAL_META`, `App.mealTag(mealType)`, `App.CATEGORY_META` exist — use them.
