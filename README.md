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

### Deploying to Fly.io

A `Dockerfile` and `fly.toml` are included, with a persistent volume already
wired up for the database (Fly's free tier includes real persistent storage,
unlike most free tiers — that matters here since SQLite needs a disk that
survives redeploys).

1. Create a free account at fly.io and install `flyctl`, then `fly auth login`
   (both need your own browser/credentials — not something I can do for you).
2. Edit `fly.toml`: change `app = "CHANGE-ME-stay-ready"` to something unique.
3. Create the volume once: `fly volumes create stayready_data --region iad --size 1`
4. Deploy: `fly deploy`
5. Open it: `fly open`

## What's inside

- **Today** — today's meals, who's cooking, the week ahead, and smart picks.
- **Meal Plan** — month calendar; click any breakfast/lunch/dinner slot to plan it.
  Recommendations ranked ⚡ quickest, 💪 healthiest, 💰 cheapest. Assign a cook to
  every meal. Export the month to Google Calendar (.ics download → import at
  calendar.google.com, or Settings → Import & export).
- **Recipes** — add/remove recipes easily; each knows its time, cost, macros, and
  how many of its ingredients are already in your pantry.
- **Pantry** — everything you have on hand, by category. "Mark cooked" on a meal
  deducts its ingredients automatically.
- **Shopping List** — pick a date range (defaults to the next month) and get exactly
  what to buy: planned needs minus pantry stock. "Bought ✓" restocks the pantry.
- **Household** — members (the assignable cooks) and your invite code.

## Tech

Flask + SQLite (`stayready.db`, created on first run) with a vanilla-JS single-page
frontend — no build step. Data model and API contract are documented in `SPEC.md`.
