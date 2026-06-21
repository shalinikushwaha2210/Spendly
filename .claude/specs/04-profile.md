# Spec: Profile

## Overview

Replace the `/profile` stub (currently a plain string) with the logged-in user's dashboard: a greeting with their name/email and a list of their expenses with a running total. There is no separate "list expenses" route anywhere in the roadmap (Steps 7-9 only cover add/edit/delete), so `/profile` is the page where a user actually sees their data — it doubles as the home dashboard. This is also the first protected route in the app: it must require a session and redirect anonymous visitors to `/login`.

## Depends on

- Step 1 — database setup (`database/db.py`: `get_db()`, `users`/`expenses` tables, seeded demo data). Complete.
- Step 2 — registration (`app.py`: `session["user_id"]`, `session["name"]`). Complete.
- Step 3 — login/logout (same session keys, nav conditional on `session.user_id`). Complete.

## Routes

- `GET /profile` — show the logged-in user's name/email and their expenses with a total — logged-in only. If `session.get("user_id")` is missing, redirect to `/login` (no error message needed — they were never logged in, this isn't a failed action).

## Database changes

No database changes. Reads from the existing `users` and `expenses` tables (`expenses.user_id` foreign key already links them).

## Templates

- **Create:** `templates/profile.html` — extends `base.html`. Shows:
  - A header greeting using `session["name"]` (e.g. "Welcome back, {{ session['name'] }}").
  - The user's email (fetched from `users`, not stored in session, to keep session payload small and to always reflect the current DB value).
  - A running total of all their expenses, formatted as `₹` + comma-grouped, no decimals (e.g. `₹12,450`) — matches `landing.html`'s mock card exactly; do not show raw Python floats like `₹250.0`.
  - A list/table of their expenses (category, amount, date, description), most recent first.
  - Links/buttons to `/expenses/add`, and per-row links to `/expenses/<id>/edit` and `/expenses/<id>/delete` (these remain stubs returning plain strings until Steps 7-9 — linking to them now is fine and expected).
  - An empty state (e.g. "No expenses yet — add your first one") for a user with zero expenses, since not every user will be the seeded demo user.
- **Modify:** none. `base.html`'s nav already conditionally shows "Sign out" when logged in (Step 3) — no changes needed there.

## Files to change

- `app.py` — replace the `/profile` stub with the real implementation (auth check, DB queries, render).
- `static/css/style.css` — add dashboard/profile layout rules (no per-page stylesheet).

## Files to create

- `templates/profile.html`

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs.
- Parameterised queries only — no string formatting in SQL.
- Passwords hashed with werkzeug (n/a here — no password handling on this page, just noting the project-wide rule).
- Use CSS variables — never hardcode hex values. New rules for the profile/dashboard layout go in `static/css/style.css` (no per-page stylesheet), reusing existing variables (`--paper-card`, `--border`, `--radius-md`, etc.) and existing class patterns (e.g. `.feature-card`/`.mock-card` styling conventions) where it makes sense rather than inventing a parallel set of names.
- All templates extend `base.html`.
- The login-required check is a simple guard clause at the top of the view (`if not session.get("user_id"): return redirect(url_for("login"))`) — no decorator, no Flask-Login, no blueprint-level `before_request`. This keeps the pattern consistent with the project's flat, single-file, non-abstracted style; if more routes need the same guard in later steps (expense add/edit/delete), revisit then rather than introducing an abstraction for one route now.
- Query the user's expenses with `SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC` (parameterised) — the `id DESC` tie-break keeps same-day expenses ordered newest-added-first, since `date` alone doesn't disambiguate. Never trust `session["user_id"]` blindly without it being the bound parameter in a `WHERE` clause scoping every query to that user.
- Compute the total in Python (`sum(e["amount"] for e in expenses)`) rather than a second query — the expense list is already being fetched and is not expected to be large enough to need `SUM()` at the DB level for this teaching project.

## Definition of done

- [ ] Visiting `/profile` while logged out redirects to `/login`.
- [ ] Visiting `/profile` while logged in as the demo user (`demo@spendly.com`) shows their name, email, all of their expenses, and the correct (₹, comma-grouped) total.
- [ ] A freshly registered user with no expenses sees the empty state instead of a broken/empty table.
- [ ] Expense rows show category, amount (₹-formatted), date, and description.
- [ ] Links to add/edit/delete are present and point at the correct URLs (clicking them still shows the existing stub strings — that's expected, not a bug).
- [ ] App starts without errors; `/`, `/register`, `/login`, `/logout`, `/terms`, `/privacy` are unaffected.
