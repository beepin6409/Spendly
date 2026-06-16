# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a personal expense tracking web app built with Flask and Jinja2 server-side rendering. No JavaScript framework; vanilla JS only.

## Commands

```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server (starts on http://localhost:5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_auth.py
```

## Architecture

**Stack:** Flask 3.1.x · SQLite · Jinja2 templates · pure CSS · vanilla JS

**Folder layout:**
- `app.py` — Flask app, all route definitions
- `database/db.py` — SQLite connection helpers (`get_db`, `init_db`, `seed_db`) — **not yet implemented**
- `templates/` — Jinja2 HTML; `base.html` is the master layout (navbar + footer)
- `static/css/style.css` — all styling; uses CSS variables defined in `:root`
- `static/js/main.js` — client-side JS stub

**Routing pattern:** All pages are server-rendered. Public routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) return rendered templates. Protected routes (`/logout`, `/profile`, `/expenses/*`) are stubbed with placeholder strings and await auth + DB implementation.

**CSS variables** (defined in `:root`): `--ink`, `--paper`, `--accent`, `--accent-2`, `--danger`, `--font-serif`, `--font-sans`, `--max-w`, `--auth-w`, `--radius-*`. Use these rather than hardcoding values.

**Database layer (to implement):** `database/db.py` should provide:
- `get_db()` — returns `sqlite3.connect(...)` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — `CREATE TABLE IF NOT EXISTS` for `users` and `expenses`
- `seed_db()` — inserts sample data for development

Expected tables: `users(id, name, email, password_hash)` and `expenses(id, user_id, category, amount, date, description)`.

**Auth flow (planned):** Form POST to `/register` and `/login` → session-based auth via `flask.session`. No REST/JSON layer; keep everything server-rendered unless there's a specific reason to add API endpoints.

## Current Status

Frontend UI and all static pages are complete. The critical missing pieces are:
1. `database/db.py` implementation
2. Auth logic in `/register` and `/login` POST handlers
3. Expense CRUD routes
4. Tests (pytest + pytest-flask are installed)
