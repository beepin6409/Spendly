# Spec: Login and Logout

## Overview
This step wires up the login and logout flows so existing users can authenticate and end their session. It handles `POST /login` — validating credentials, checking the password hash, and starting a Flask session — and converts the `/logout` stub into a real session-clearing redirect. A new `get_user_by_email()` helper is added to `database/db.py` so the login route can look up a user without duplicating query logic in `app.py`.

## Depends on
- Step 01 — Database Setup: `users` table must exist with `id`, `name`, `email`, `password_hash` columns.
- Step 02 — Registration: `get_db()`, `init_db()`, `create_user()`, and session handling patterns must already be in place.

## Routes
- `GET /login` — render the login form; redirect to `/` if already logged in — public
- `POST /login` — validate credentials, set session, redirect to `/` on success or re-render form on failure — public
- `GET /logout` — clear the session and redirect to `/` — logged-in (no hard guard needed at this step)

## Database changes
No new tables or columns. One new helper function must be added to `database/db.py`:

- `get_user_by_email(email)` — returns a `sqlite3.Row` with `id`, `name`, `password_hash` for the matching email, or `None` if not found.

## Templates
- **Modify:** `templates/login.html` — already has `{% if error %}` block and POSTs to `/login`; no structural changes needed. Verify the `action` attribute uses `url_for('login')` rather than a hardcoded path.
- **No new templates.**

## Files to change
- `app.py` — convert `GET /login` to accept both methods; add `POST /login` logic (look up user, verify hash, set session, redirect); implement `GET /logout` (clear session, redirect to `/`); import `check_password_hash` from `werkzeug.security` and `get_user_by_email` from `database.db`
- `database/db.py` — add `get_user_by_email(email)` function

## Files to create
None.

## New dependencies
No new pip packages. `werkzeug.security.check_password_hash` ships with Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` only
- Parameterised queries only — never format user input into SQL strings
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- On successful login store `session["user_id"]` and `session["user_name"]`, then redirect to `/`
- On failed login re-render `login.html` with a generic `error` message: `"Invalid email or password"` (do not reveal which field was wrong)
- `GET /login` while already logged in must redirect to `/` — never show the form to an authenticated user
- `GET /logout` must call `session.clear()` (not just pop individual keys) then redirect to `/`

## Definition of done
- [ ] Visiting `/login` while already logged in redirects to `/` without rendering the form
- [ ] Submitting the login form with a correct email and password sets `session["user_id"]` and redirects to `/`; the navbar shows "Dashboard"
- [ ] Submitting with an unrecognised email re-renders the form with "Invalid email or password"
- [ ] Submitting with a correct email but wrong password re-renders the form with "Invalid email or password"
- [ ] Submitting with either field empty re-renders the form with "All fields are required"
- [ ] Visiting `/logout` clears the session and redirects to `/`; the navbar reverts to "Sign in / Get started"
- [ ] After logout, navigating back with the browser back button does not restore the authenticated session
- [ ] `get_user_by_email()` returns `None` for a non-existent email and a valid `sqlite3.Row` for a known email
