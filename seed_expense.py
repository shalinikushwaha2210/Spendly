import sys
from calendar import monthrange
from datetime import date

from database.db import get_db, CATEGORIES


def main():
    if len(sys.argv) != 4:
        print("Usage: python seed_expense.py <user_id> <count> <category>")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
        count = int(sys.argv[2])
    except ValueError:
        print("Error: user_id and count must be integers.")
        sys.exit(1)

    category = sys.argv[3]
    if category not in CATEGORIES:
        print(f"Error: category must be one of {CATEGORIES}.")
        sys.exit(1)

    conn = get_db()
    try:
        user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            print(f"Error: no user with id {user_id} exists.")
            sys.exit(1)

        today = date.today()
        days_in_month = monthrange(today.year, today.month)[1]

        rows = []
        for i in range(count):
            day = (i % days_in_month) + 1
            expense_date = today.replace(day=day).isoformat()
            amount = 100.0 + (i * 50.0)
            description = f"{category} expense #{i + 1}"
            rows.append((user_id, amount, category, expense_date, description))

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
        print(f"Inserted {count} '{category}' expenses for user_id={user_id}.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
