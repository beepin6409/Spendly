# Spec: Registration

## Overview
This step wires up the registration form so new users can create an account. It handles the `POST /register` route, validates input, hashes the password, inserts a new row into the `users` table, starts a Flask session for the newly created user, and redirects them to the dashboard. It also completes `database/db.py` (Step 1 skeleton) with the actual `get_db()`, `init_db()`, and user helper functions the rest of the app depends on.

## Depends on
- Step 1 — Database Setup: the `users` and `expenses` tables must exist in `spendly.db`. The database is already seeded, but `database/db.py` still needs its functions implemented as part of this step.

## Routes
- `GET /register` — render the registration form — public (already exists, no change needed)
- `POST /register` — validate form data, create user, start session, redirect — public

## Database changes
No new tables. The `users` table already exists with the correct schema:

```
users(id INTEGER PK, name TEXT NOT NULL, email TEXT NOT NULL,
      password_hash TEXT NOT NULL, created_at TEXT)
```

Two helper functions must be added to `database/db.py`:
- `email_exists(email)` — returns `True` if the email is already registered
- `create_user(name, email, password_hash)` — inserts a new user and returns the new `id`

## Templates
- **Modify:** `templates/register.html` — already has the form; add flash-message block above the form to display validation errors (e.g. email taken, password too short). No structural changes needed.
- **Modify:** `templates/base.html` — navbar currently always shows "Sign in / Get started"; update the nav links to show a "Dashboard" link and hide the auth links when `session.user_id` is set.

## Files to change
- `app.py` — add `secret_key`, import `request`, `redirect`, `url_for`, `session`, `flash`; implement `POST /register` handler
- `database/db.py` — implement `get_db()`, `init_db()`, `email_exists()`, `create_user()`
- `templates/register.html` — add flash/error display block
- `templates/base.html` — make nav links conditional on session

## Files to create
None.

## New dependencies
No new pip packages. `werkzeug.security` ships with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` only
- Parameterised queries only — never format user input into SQL strings
- Passwords hashed with `werkzeug.security.generate_password_hash` (default method)
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- `get_db()` must set `conn.row_factory = sqlite3.Row` and run `PRAGMA foreign_keys = ON`
- Database filename must come from a single constant in `db.py` (e.g. `DB_PATH = "spendly.db"`) — never hardcode it in `app.py`
- After successful registration, store `session["user_id"]` and `session["user_name"]` then redirect to `/` (landing) until a proper dashboard exists
- Flash errors for: missing fields, password shorter than 8 characters, email already registered

## Definition of done
- [ ] Submitting the form with a new email and valid password creates a row in `users` and redirects to `/`
- [ ] The new user's `password_hash` in the DB is a werkzeug hash (starts with `scrypt:` or `pbkdf2:`)
- [ ] Submitting with an already-registered email re-renders the form with the message "Email already registered"
- [ ] Submitting with a password shorter than 8 characters re-renders the form with "Password must be at least 8 characters"
- [ ] Submitting with any empty field re-renders the form with "All fields are required"
- [ ] After successful registration, the navbar shows "Dashboard" instead of "Sign in / Get started"
- [ ] Navigating directly to `/register` while already logged in redirects to `/` (no re-registration)
- [ ] `database/db.py` functions can be imported and called without error
