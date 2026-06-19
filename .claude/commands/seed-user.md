# Spec Document

## 1. Overview

Add a standalone CLI script, `seed_user.py`, that lets a developer create a single new user in the database by passing name, email, and password as command-line arguments.

This is separate from `seed_db()`, which only ever inserts the fixed demo user (`demo@spendly.com`). This script is for creating additional/custom users on demand, e.g. for manual testing.

---

## 2. Depends on

- `database/db.py` — `get_db()` must exist and work (already implemented).

---

## 3. Routes

- No new routes.

---

## 4. Files to Create

- `seed_user.py` (project root)

---

## 5. CLI Usage

```bash
python seed_user.py "<name>" "<email>" "<password>"
```

Example:

```bash
python seed_user.py "Jane Doe" "jane@example.com" "secret123"
```

- All three arguments are required and positional, in that order.
- If the wrong number of arguments is given, print a usage message and exit with a non-zero status.

---

## 6. Behavior

- Hash the password using `werkzeug.security.generate_password_hash` before inserting.
- Insert into the `users` table using `get_db()` from `database/db.py`:

  ```sql
  INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)
  ```

- Use parameterized queries only — no string formatting in SQL.
- Commit and close the connection.
- On success, print a confirmation message including the new user's `id` and `email`.

---

## 7. Error Handling

- If the email already exists, the `UNIQUE` constraint on `users.email` will raise `sqlite3.IntegrityError`.
  - Catch this, print a clear error message (e.g. `Error: a user with email '<email>' already exists.`), and exit with a non-zero status.
  - Do not let the raw traceback surface to the user.

---

## 8. Rules for Implementation

- No ORMs (no SQLAlchemy).
- Use parameterized queries only.
- Reuse `get_db()` from `database/db.py` — do not open a separate raw `sqlite3.connect()`.
- Do not call `init_db()` from this script — assume the schema already exists (created on app startup).
- No sample expenses are created for this user (name/email/password only).

---

## 9. Definition of Done

- [ ]  `python seed_user.py "<name>" "<email>" "<password>"` inserts a new row into `users` with a hashed password.
- [ ]  Running with a duplicate email fails gracefully with a clear error message, not a traceback.
- [ ]  Running with the wrong number of arguments prints usage info instead of crashing.
- [ ]  No changes required to `app.py` or `database/db.py`.
