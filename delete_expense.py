import sys

from database.db import get_db


def main():
    if len(sys.argv) != 2:
        print("Usage: python delete_expense.py <expense_id>")
        sys.exit(1)

    try:
        expense_id = int(sys.argv[1])
    except ValueError:
        print("Error: expense_id must be an integer.")
        sys.exit(1)

    conn = get_db()
    try:
        expense = conn.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        if not expense:
            print(f"Error: no expense with id {expense_id} exists.")
            sys.exit(1)

        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        print(f"Deleted expense id={expense_id}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
