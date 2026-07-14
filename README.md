# 🥕 Stay Ready

Meal planning for people who like knowing what's for dinner. Plan a whole month of
breakfasts, lunches, and dinners; keep a live pantry; get smart recipe picks by
**time to make**, **nutrition**, and **cost**; and generate the shopping list for
your next month of meal prep.

## Run it (local / LAN)

```
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:8008** (or `http://<this-PC's-LAN-IP>:8008` from your
phone on the same WiFi) and create an account. The first account creates your
household (with 12 starter recipes); housemates join with your invite code from the
Household page.

## Running in production

Local mode above is fine for LAN-only use. Before putting this on the public
internet, run it behind a real server with HTTPS:

```
STAYREADY_HTTPS=1 PORT=8008 python wsgi.py
```

`STAYREADY_HTTPS=1` tells the app it's behind a TLS-terminating reverse proxy (what
every PaaS host — Render, Fly.io, etc. — does automatically): it requires HTTPS for
session cookies and trusts one hop of `X-Forwarded-*` headers from that proxy. Leave
it **unset** for local/LAN use, or logins will silently fail (the cookie won't be set
over plain HTTP). `wsgi.py` serves via waitress instead of Flask's dev server, and
honors the host's `$PORT` if set.

Also before going live:
- **Back up the database regularly**: `python backup_db.py` snapshots
  `stayready.db` into `backups/` with a 14-day rotation. Schedule it daily
  (cron / Task Scheduler) and, once you've picked a host, also copy `backups/`
  off-host on whatever schedule that platform supports.
- Login and registration are rate-limited (10 attempts/min on login, 10
  registrations/hour) per IP — no extra setup needed, but it assumes a single
  server process; a multi-worker deployment would need a shared limiter
  backend (see `extensions.py`).
- **`STAYREADY_DATA_DIR`** controls where `stayready.db` and the session
  secret key live — defaults to next to the code, which is fine locally but
  wrong on any host whose filesystem doesn't survive a redeploy (most PaaS
  hosts). Point it at a mounted persistent volume in that case.

### Deploying to PythonAnywhere

PythonAnywhere's free tier gives you one web app at
`<username>.pythonanywhere.com` on a **persistent** filesystem, so the SQLite
database survives reloads with no extra volume setup. This app makes no
outbound network calls, so the free tier's outbound whitelist is a non-issue.

Do these in the PythonAnywhere dashboard (see `pythonanywhere_wsgi.py` for the
WSGI file contents):

1. **Bash console** (Consoles tab → Bash) — clone the repo and build a
   virtualenv:
   ```
   git clone https://github.com/mphardinger/StayReady.git stayready
   mkvirtualenv --python=/usr/bin/python3.10 stayready-venv
   pip install -r stayready/requirements.txt
   ```
2. **Web tab** → *Add a new web app* → **Manual configuration** (not "Flask") →
   Python 3.10.
3. Set **Source code** to `/home/<username>/stayready` and **Virtualenv** to
   `stayready-venv` (or the full `/home/<username>/.virtualenvs/stayready-venv`).
4. Click the **WSGI configuration file** link and replace its contents with the
   version in `pythonanywhere_wsgi.py` (it sets `STAYREADY_HTTPS=1` and points
   at the app).
5. **Reload** the web app, then open `<username>.pythonanywhere.com` and
   register the first account (creates your household + starter recipes).

To ship an update later: `git pull` in the Bash console, then **Reload** the
web app. If the update added or improved seed recipes, also run
`python add_recipes.py` once (idempotent — it only fills in what's missing).
Free accounts must click **Run until 3 months from today** on the Web tab
periodically to keep the app alive.

**Daily backups** (one-time setup): PythonAnywhere's free tier includes one
scheduled task. On the **Tasks** tab, create a daily task with the command:

```
python3.10 /home/StayReady/stayready/backup_db.py
```

That snapshots the database into `~/stayready/backups/` with 14-day rotation.
Occasionally download a copy off-host (Files tab → backups → download) in
case the hosting account itself is ever lost.

## What's inside

- **Today** — today's meals, who's cooking, the week ahead, smart picks, and a
  per-person nutrition summary of the day's planned meals.
- **Meal Plan** — month calendar; click any breakfast/lunch/dinner slot to plan it.
  Recommendations ranked ⚡ quickest, 💪 healthiest, 💰 cheapest, with filter chips
  for time, budget, and diet. **Build my week** drafts 7 dinners around a
  $/day budget (e.g. a strict $5/day), max cook time, diet limits, and this
  week's sale items — review and shuffle every pick before saving. Export the
  month to Google Calendar (.ics download).
- **Recipes** — 45 starter recipes with per-serving nutrition estimates
  (calories, macros, fiber, sugar, sodium, potassium, phosphorus) and
  documented diet tags: kidney-friendly, low-FODMAP, diabetic-friendly,
  vegetarian. Filter by any of those plus "15 min or less" and "under
  $2/serving". *Estimates are not medical advice — the app says so wherever
  they appear.*
- **Pantry** — everything you have on hand, by category. "Mark cooked" on a meal
  deducts its ingredients automatically.
- **Shopping List** — pick a date range and get exactly what to buy: planned
  needs minus pantry stock. Type in **this week's sale items** from your store
  flyer; the list flags them and the planner favors recipes that use them.
- **Household** — members (the assignable cooks) and your invite code.
- **Settings** — light/dark theme, accent colors, dietary focus, week start,
  and which meal slots you plan (all per device).

## Tech

Flask + SQLite (`stayready.db`, created on first run) with a vanilla-JS single-page
frontend — no build step. Data model and API contract are documented in `SPEC.md`.
