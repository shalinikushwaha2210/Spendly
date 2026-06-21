# Spec: Registration

## Overview

Replace the `/register` stub — which currently only renders `register.html` on `GET` — with a working sign-up flow. A visitor submits their name, email, and password; the app validates the input, hashes the password, creates a row in `users`, and logs the new user in by starting a session. This is the first step in Spendly where a session is established, which subsequent steps (logout, profile, expense CRUD) depend on.

## Depends on

- Step 1 — database setup (`database/db.py`: `get_db()`, `users` table). Already complete.

## Routes

- `GET /register` — render the registration form — public (already implemented, unchanged)
- `POST /register` — create the account and log the user in — public

## Database changes

No database changes. Uses the existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) as defined in `database/db.py`.

## Templates

- **Create:** none
- **Modify:** `templates/register.html` — render `{{ error }}` for each failure case already supported by the existing `{% if error %}` block (no markup changes needed if the block already exists; otherwise add field-level error rendering)

## Files to change

- `app.py` — change `@app.route("/register")` to accept `["GET", "POST"]`; add POST handling (validate, hash, insert, set session, redirect)

## Files to create

None.

## New dependencies

No new dependencies. Use the standard library, `werkzeug.security.generate_password_hash`, and Flask's built-in `session`.

## Rules for implementation

- No SQLAlchemy or ORMs.
- Parameterised queries only — no string formatting in SQL.
- Passwords hashed with `werkzeug.security.generate_password_hash` before insert; never store or log plaintext passwords.
- Use CSS variables — never hardcode hex values (only relevant if `style.css` needs new rules; none are expected for this step).
- All templates extend `base.html`.
- Validate on the server even though the form has `required`/`type="email"` attributes — client-side validation is not trustworthy.
- Required fields: `name` (non-empty), `email` (non-empty, valid format), `password` (minimum 8 characters, matching the placeholder text already in `register.html`).
- On any validation failure or duplicate email (`sqlite3.IntegrityError` on the `UNIQUE` constraint), re-render `register.html` with an `error` message and HTTP 400 — do not redirect.
- On success: insert the user, store `user_id` (and optionally `name`) in `flask.session`, then redirect to `/profile`.
- Flask's `app.secret_key` must be set for `session` to work — add a `SECRET_KEY` (e.g. read from an environment variable with a hardcoded dev fallback) if not already configured.

## Definition of done

- [ ] Submitting valid name/email/password on `/register` creates a new row in `users` with a hashed (not plaintext) password.
- [ ] After successful registration, the browser is redirected to `/profile` and the session contains the new user's id.
- [ ] Submitting an email that already exists re-renders the registration form with a clear error message and does not create a duplicate row.
- [ ] Submitting an empty name, invalid email, or password under 8 characters re-renders the form with a clear error message and does not insert a row.
- [ ] `GET /register` still renders the form as before (unauthenticated visitors can still reach it).
- [ ] App starts without errors and existing routes (`/`, `/login`, `/terms`, `/privacy`) are unaffected.
