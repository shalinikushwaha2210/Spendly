---
description: Delete a single expense by id
---

Delete an expense using this argument: $ARGUMENTS

Argument is positional: `<expense_id>`

- `expense_id` — id of an existing row in the `expenses` table

Behavior (implemented in `delete_expense.py`):

1. Validate `expense_id` exists in `expenses` — if not, error out.
2. Delete the row via `get_db()` from `database/db.py`, using a parameterized query.
3. Print a confirmation showing the deleted expense id.

Usage:

```bash
python delete_expense.py <expense_id>
```
