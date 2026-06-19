---
description: Seed N sample expenses for an existing user in a given category
---

Seed expenses using these arguments: $ARGUMENTS

Arguments are positional: `<user_id> <count> <category>`

- `user_id` — id of an existing row in the `users` table
- `count` — how many sample expenses to insert
- `category` — must be one of the fixed `CATEGORIES` in `database/db.py` (Food, Transport, Bills, Health, Entertainment, Shopping, Other)

Behavior (implemented in `seed_expense.py`):

1. Validate `user_id` exists in `users` — if not, error out (don't insert, don't auto-create the user).
2. Validate `category` is one of the fixed categories — if not, error out.
3. Insert `count` rows into `expenses` for that `user_id` and `category`, using `get_db()` from `database/db.py`.
   - Use parameterized queries only.
   - Spread `date` values across the current month (`YYYY-MM-DD`).
   - Vary `amount` per row; `description` can be a simple generic placeholder per row.
4. Print a confirmation listing how many expenses were inserted and for which user.

Usage:

```bash
python seed_expense.py <user_id> <count> <category>
```
