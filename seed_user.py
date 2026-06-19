import sys
import sqlite3

from werkzeug.security import generate_password_hash

from database.db import get_db


def main():
    if len(sys.argv) != 4:
        print("Usage: python seed_user.py \"<name>\" \"<email>\" \"<password>\"")
        sys.exit(1)

    name, email, password = sys.argv[1], sys.argv[2], sys.argv[3]
    password_hash = generate_password_hash(password)

    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        print(f"Created user id={cur.lastrowid} email={email}")
    except sqlite3.IntegrityError:
        print(f"Error: a user with email '{email}' already exists.")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
