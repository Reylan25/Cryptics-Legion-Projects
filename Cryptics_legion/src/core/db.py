# src/core/db.py
import sqlite3
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up to src folder, then to database folder
SRC_DIR = os.path.dirname(SCRIPT_DIR)
DB_DIR = os.path.join(SRC_DIR, "database")
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
        password BLOB NOT NULL,
        has_seen_onboarding INTEGER NOT NULL DEFAULT 0
    )
    """)

    # Migration: Add has_seen_onboarding column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN has_seen_onboarding INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Migration: Add personal details columns
    personal_columns = [
        ("full_name", "TEXT DEFAULT ''"),
        ("email", "TEXT DEFAULT ''"),
        ("phone", "TEXT DEFAULT ''"),
        ("currency", "TEXT DEFAULT 'PHP'"),
        ("timezone", "TEXT DEFAULT 'Asia/Manila'"),
        ("first_day_of_week", "TEXT DEFAULT 'Monday'"),
        ("photo", "TEXT DEFAULT ''"),
    ]
    for col_name, col_type in personal_columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists

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

    # accounts table (linked to users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        account_number TEXT,
        type TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0,
        currency TEXT NOT NULL DEFAULT 'PHP',
        color TEXT NOT NULL DEFAULT '#3B82F6',
        is_primary INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'active',
        sort_order INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Migration: Add status and sort_order columns if they don't exist
    try:
        cursor.execute("ALTER TABLE accounts ADD COLUMN status TEXT NOT NULL DEFAULT 'active'")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE accounts ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists

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


def get_user_profile(user_id: int) -> dict:
    """Get user profile including personal details."""
    import json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, full_name, email, phone, currency, 
               timezone, first_day_of_week, photo
        FROM users WHERE id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        # Parse photo JSON
        photo_data = None
        if row[8]:
            try:
                photo_data = json.loads(row[8])
            except:
                photo_data = None
        
        return {
            "id": row[0],
            "username": row[1],
            "full_name": row[2] or "",
            "email": row[3] or "",
            "phone": row[4] or "",
            "currency": row[5] or "PHP",
            "timezone": row[6] or "Asia/Manila",
            "first_day_of_week": row[7] or "Monday",
            "photo": photo_data,
        }
    return None


def save_personal_details(user_id: int, details: dict) -> bool:
    """Save personal details for a user."""
    import json
    conn = connect_db()
    cur = conn.cursor()
    try:
        # Convert photo dict to JSON string for storage
        photo_data = details.get("photo")
        photo_json = json.dumps(photo_data) if photo_data else ""
        
        cur.execute("""
            UPDATE users SET 
                full_name = ?,
                email = ?,
                phone = ?,
                currency = ?,
                timezone = ?,
                first_day_of_week = ?,
                photo = ?
            WHERE id = ?
        """, (
            details.get("full_name", ""),
            details.get("email", ""),
            details.get("phone", ""),
            details.get("currency", "PHP"),
            details.get("timezone", "Asia/Manila"),
            details.get("first_day", "Monday"),
            photo_json,
            user_id
        ))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error saving personal details: {e}")
        return False
    finally:
        conn.close()


def has_user_seen_onboarding(user_id: int) -> bool:
    """Check if user has already seen the onboarding screen."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT has_seen_onboarding FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return bool(row[0]) if row else False


def mark_onboarding_seen(user_id: int) -> bool:
    """Mark that user has seen the onboarding screen."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET has_seen_onboarding = 1 WHERE id = ?", (user_id,))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


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


# ----- ACCOUNT CRUD -----
def insert_account(user_id: int, name: str, account_number: str, account_type: str, 
                   balance: float, currency: str, color: str, created_at: str) -> int:
    """Insert a new account and return its ID."""
    conn = connect_db()
    cur = conn.cursor()
    # Get next sort order
    cur.execute("SELECT COALESCE(MAX(sort_order), 0) + 1 FROM accounts WHERE user_id = ?", (user_id,))
    next_order = cur.fetchone()[0]
    cur.execute(
        """INSERT INTO accounts (user_id, name, account_number, type, balance, currency, color, is_primary, status, sort_order, created_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'active', ?, ?)""",
        (user_id, name, account_number, account_type, balance, currency, color, next_order, created_at),
    )
    conn.commit()
    account_id = cur.lastrowid
    conn.close()
    return account_id


def get_accounts_by_user(user_id: int, include_all: bool = False):
    """Get all accounts for a user. If include_all is False, only active accounts are returned."""
    conn = connect_db()
    cur = conn.cursor()
    if include_all:
        cur.execute(
            """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at, status, sort_order 
               FROM accounts WHERE user_id = ? ORDER BY sort_order ASC, created_at DESC""",
            (user_id,),
        )
    else:
        cur.execute(
            """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at 
               FROM accounts WHERE user_id = ? AND status = 'active' ORDER BY sort_order ASC, created_at DESC""",
            (user_id,),
        )
    rows = cur.fetchall()
    conn.close()
    return rows


def update_account(account_id: int, user_id: int, name: str = None, account_number: str = None,
                   account_type: str = None, balance: float = None, currency: str = None,
                   color: str = None, status: str = None) -> bool:
    """Update an account's details."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Build dynamic update query
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    if account_number is not None:
        updates.append("account_number = ?")
        values.append(account_number)
    if account_type is not None:
        updates.append("type = ?")
        values.append(account_type)
    if balance is not None:
        updates.append("balance = ?")
        values.append(balance)
    if currency is not None:
        updates.append("currency = ?")
        values.append(currency)
    if color is not None:
        updates.append("color = ?")
        values.append(color)
    if status is not None:
        updates.append("status = ?")
        values.append(status)
    
    if not updates:
        conn.close()
        return False
    
    values.extend([account_id, user_id])
    query = f"UPDATE accounts SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
    cur.execute(query, values)
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def update_account_balance(account_id: int, user_id: int, new_balance: float) -> bool:
    """Update an account's balance."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE accounts SET balance = ? WHERE id = ? AND user_id = ?",
        (new_balance, account_id, user_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def delete_account(account_id: int, user_id: int) -> bool:
    """Delete an account."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM accounts WHERE id = ? AND user_id = ?", (account_id, user_id))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted > 0


def get_total_balance_by_user(user_id: int) -> float:
    """Get total balance across all accounts for a user."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(balance) FROM accounts WHERE user_id = ?", (user_id,))
    total = cur.fetchone()[0]
    conn.close()
    return float(total) if total else 0.0