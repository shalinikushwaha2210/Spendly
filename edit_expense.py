import sys
from datetime import datetime

from database.db import get_db, CATEGORIES

EDITABLE_FIELDS = ("amount", "category", "date", "description")


def main():
    if len(sys.argv) != 4:
        print("Usage: python edit_expense.py <expense_id> <field> <value>")
        sys.exit(1)

    try:
        expense_id = int(sys.argv[1])
    except ValueError:
        print("Error: expense_id must be an integer.")
        sys.exit(1)

    field = sys.argv[2]
    value = sys.argv[3]

    if field not in EDITABLE_FIELDS:
        print(f"Error: field must be one of {EDITABLE_FIELDS}.")
        sys.exit(1)

    if field == "amount":
        try:
            value = float(value)
        except ValueError:
            print("Error: amount must be a number.")
            sys.exit(1)
    elif field == "category":
        if value not in CATEGORIES:
            print(f"Error: category must be one of {CATEGORIES}.")
            sys.exit(1)
    elif field == "date":
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Error: date must be in YYYY-MM-DD format.")
            sys.exit(1)

    conn = get_db()
    try:
        expense = conn.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        if not expense:
            print(f"Error: no expense with id {expense_id} exists.")
            sys.exit(1)

        conn.execute(f"UPDATE expenses SET {field} = ? WHERE id = ?", (value, expense_id))
        conn.commit()
        print(f"Updated expense id={expense_id}: {field} = {value}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
