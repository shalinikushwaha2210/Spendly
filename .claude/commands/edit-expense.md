---
description: Edit a single field on an existing expense
---

Edit an expense using these arguments: $ARGUMENTS

Arguments are positional: `<expense_id> <field> <value>`

- `expense_id` — id of an existing row in the `expenses` table
- `field` — one of `amount`, `category`, `date`, `description`
- `value` — the new value for that field

Behavior (implemented in `edit_expense.py`):

1. Validate `expense_id` exists in `expenses` — if not, error out.
2. Validate `field` is one of the editable fields above — if not, error out.
   - `user_id`, `id`, and `created_at` are not editable through this command.
3. Validate `value` against the field's type/constraints:
   - `amount` — must parse as a float.
   - `category` — must be one of the fixed `CATEGORIES` in `database/db.py`.
   - `date` — must match `YYYY-MM-DD` format.
   - `description` — any string (no validation).
4. Update the row via `get_db()` from `database/db.py`, using a parameterized query.
5. Print a confirmation showing the expense id and the new value.

Usage:

```bash
python edit_expense.py <expense_id> <field> <value>
```
