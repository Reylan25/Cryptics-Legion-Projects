# src/core/db.py
import sqlite3
import os

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "expense_tracker.db")


def connect_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # users table (password stored as BLOB)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL
    )
    """)

    # expenses table (linked to users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    return conn


# ----- USER helpers (low-level) -----
def insert_user(username: str, password_blob: bytes) -> bool:
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_blob))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_username(username: str):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row  # (id, password_blob) or None


# ----- EXPENSE CRUD (low-level) -----
def insert_expense(user_id: int, amount: float, category: str, description: str, date_str: str):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, description, date_str),
    )
    conn.commit()
    conn.close()


def select_expenses_by_user(user_id: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, amount, category, description, date FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def update_expense_row(expense_id: int, user_id: int, amount: float, category: str, description: str, date_str: str) -> bool:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=? AND user_id=?",
        (amount, category, description, date_str, expense_id, user_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def delete_expense_row(expense_id: int, user_id: int) -> bool:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (expense_id, user_id))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted > 0


# ----- Summary helpers -----
def total_expenses_by_user(user_id: int) -> float:
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?", (user_id,))
    t = cur.fetchone()[0]
    conn.close()
    return float(t) if t else 0.0


def category_summary_by_user(user_id: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
