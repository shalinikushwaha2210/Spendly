# Spec: Login and Logout

## Overview

Replace the `/login` stub — which currently only renders `login.html` on `GET` — with a working sign-in flow, and replace the `/logout` stub with one that actually clears the session. Together these complete the authentication loop that registration started: a returning user can sign back in, and any signed-in user can sign out. The nav bar is updated to reflect signed-in state so logout is actually reachable from the UI.

## Depends on

- Step 1 — database setup (`database/db.py`: `get_db()`, `users` table). Complete.
- Step 2 — registration (`app.py`: `app.secret_key`, `flask.session` usage, `EMAIL_RE` pattern). Must be merged to `main` first — this step reuses the same session/secret-key setup rather than re-introducing it.

## Routes

- `POST /login` — validate email/password against the stored hash, start a session, redirect to `/profile` — public
- `GET /logout` — clear the session, redirect to `/` (landing) — logged-in only (a logged-out visitor hitting it directly just gets redirected; no error needed)

`GET /login` stays as-is (renders the form, public, unchanged).

## Database changes

No database changes. Uses the existing `users` table as-is.

## Templates

- **Create:** none
- **Modify:**
  - `templates/login.html` — no markup changes needed; already has `<form method="POST" action="/login">` with `email`/`password` inputs and the existing `{% if error %}<div class="auth-error">{{ error }}</div>{% endif %}` block.
  - `templates/base.html` — nav currently always shows "Sign in" / "Get started" links. Make this conditional on `session.get("user_id")`: when logged in, show a "Sign out" link (pointing to `/logout`) in place of those two links; when logged out, keep the current behaviour unchanged.

## Files to change

- `app.py` — change `@app.route("/login")` to accept `["GET", "POST"]` and add POST handling; implement `/logout` (currently returns a plain stub string).
- `templates/base.html` — conditional nav based on session state.

## Files to create

None.

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs.
- Parameterised queries only — no string formatting in SQL.
- Passwords checked with `werkzeug.security.check_password_hash` against the stored `password_hash` — never compare plaintext.
- Use CSS variables — never hardcode hex values (only relevant if `style.css` needs a new rule for the nav's logged-in state; reuse existing classes where possible).
- All templates extend `base.html`.
- On login failure (no user with that email, or password doesn't match), show one generic error — "Invalid email or password." — for both cases. Do not reveal whether the email exists; this prevents account enumeration.
- Re-render `login.html` with that `error` and HTTP 400 on failure — do not redirect.
- On success: store `session["user_id"]` (and `session["name"]`, matching the pattern from registration) and redirect to `/profile`.
- `/logout` clears the session (e.g. `session.clear()`) and redirects to `/`. No confirmation step needed.

## Definition of done

- [ ] Submitting the demo user's credentials (`demo@spendly.com` / `demo123`) on `/login` redirects to `/profile` and sets `session["user_id"]`.
- [ ] Submitting a non-existent email or a wrong password re-renders `login.html` with "Invalid email or password." and HTTP 400, and does not set a session.
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`; the nav reverts to showing "Sign in" / "Get started".
- [ ] After a successful login, the nav shows a "Sign out" link instead of "Sign in" / "Get started".
- [ ] `GET /login` still renders the form as before for logged-out visitors.
- [ ] App starts without errors and existing routes (`/`, `/register`, `/terms`, `/privacy`) are unaffected.
