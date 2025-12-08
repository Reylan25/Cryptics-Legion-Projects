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
        ("first_name", "TEXT DEFAULT ''"),
        ("last_name", "TEXT DEFAULT ''"),
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

    # Migration: Add selected_account_id column to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN selected_account_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Migration: Add last_login column to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Migration: Add passcode column to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN passcode TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Migration: Add biometric_enabled column to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN biometric_enabled INTEGER DEFAULT 0")
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

    # Migration: Add account_id column to expenses table
    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN account_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # OTP table for password reset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS password_reset_otps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        otp TEXT NOT NULL,
        created_at TEXT NOT NULL,
        is_used INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Admin table for system administrators
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        full_name TEXT DEFAULT '',
        email TEXT DEFAULT '',
        role TEXT DEFAULT 'admin',
        created_at TEXT NOT NULL,
        last_login TEXT,
        is_active INTEGER NOT NULL DEFAULT 1
    )
    """)

    # Admin activity logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        target_user_id INTEGER,
        details TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY(admin_id) REFERENCES admins(id),
        FOREIGN KEY(target_user_id) REFERENCES users(id)
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


def update_last_login(user_id: int):
    """Update the last login timestamp for a user."""
    from datetime import datetime
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    conn.close()


def get_recent_usernames(limit: int = 3):
    """Get the most recently logged in usernames."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT username FROM users 
        WHERE last_login IS NOT NULL 
        ORDER BY last_login DESC 
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]


def update_username(user_id: int, new_username: str) -> tuple:
    """Update the username for a user. Returns (success, error_message)."""
    if not new_username or len(new_username.strip()) < 3:
        return (False, "Username must be at least 3 characters")
    
    new_username = new_username.strip()
    
    conn = connect_db()
    cur = conn.cursor()
    
    # Check if username already exists (for another user)
    cur.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_username, user_id))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return (False, "Username already taken")
    
    try:
        cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        conn.commit()
        conn.close()
        return (True, None)
    except Exception as e:
        conn.close()
        return (False, str(e))


def get_user_profile(user_id: int) -> dict:
    """Get user profile including personal details."""
    import json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, full_name, first_name, last_name, email, phone, currency, 
               timezone, first_day_of_week, photo
        FROM users WHERE id = ?
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        # Parse photo JSON
        photo_data = None
        if row[10]:
            try:
                photo_data = json.loads(row[10])
            except:
                photo_data = None
        
        return {
            "id": row[0],
            "username": row[1],
            "full_name": (row[2] or "").strip(),
            "first_name": (row[3] or "").strip(),
            "last_name": (row[4] or "").strip(),
            "email": (row[5] or "").strip(),
            "phone": (row[6] or "").strip(),
            "currency": row[7] or "PHP",
            "timezone": row[8] or "Asia/Manila",
            "first_day_of_week": row[9] or "Monday",
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
                first_name = ?,
                last_name = ?,
                email = ?,
                phone = ?,
                currency = ?,
                timezone = ?,
                first_day_of_week = ?,
                photo = ?
            WHERE id = ?
        """, (
            (details.get("full_name", "") or "").strip(),
            (details.get("first_name", "") or "").strip(),
            (details.get("last_name", "") or "").strip(),
            (details.get("email", "") or "").strip(),
            (details.get("phone", "") or "").strip(),
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
def insert_expense(user_id: int, amount: float, category: str, description: str, date_str: str, account_id: int = None):
    """Insert an expense and deduct the amount from the linked account balance."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Insert the expense with account_id
    cur.execute(
        "INSERT INTO expenses (user_id, amount, category, description, date, account_id) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, amount, category, description, date_str, account_id),
    )
    expense_id = cur.lastrowid
    
    # Deduct amount from account balance if account_id is provided
    if account_id:
        cur.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ? AND user_id = ?",
            (amount, account_id, user_id),
        )
    
    conn.commit()
    conn.close()
    return expense_id


def select_expenses_by_user(user_id: int, account_id: int = None):
    """Get expenses for a user, optionally filtered by account."""
    conn = connect_db()
    cur = conn.cursor()
    
    if account_id:
        cur.execute(
            "SELECT id, user_id, amount, category, description, date, account_id FROM expenses WHERE user_id = ? AND account_id = ? ORDER BY date DESC",
            (user_id, account_id),
        )
    else:
        cur.execute(
            "SELECT id, user_id, amount, category, description, date, account_id FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,),
        )
    rows = cur.fetchall()
    conn.close()
    return rows


def update_expense_row(expense_id: int, user_id: int, amount: float, category: str, description: str, date_str: str, account_id: int = None) -> bool:
    """Update an expense and adjust account balances accordingly."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Get the old expense data to calculate balance difference
    cur.execute("SELECT amount, account_id FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    old_expense = cur.fetchone()
    
    if old_expense:
        old_amount, old_account_id = old_expense
        
        # Restore balance to old account (add back the old amount)
        if old_account_id:
            cur.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ? AND user_id = ?",
                (old_amount, old_account_id, user_id),
            )
        
        # Deduct from new account (or same account with new amount)
        if account_id:
            cur.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ? AND user_id = ?",
                (amount, account_id, user_id),
            )
    
    # Update the expense
    cur.execute(
        "UPDATE expenses SET amount=?, category=?, description=?, date=?, account_id=? WHERE id=? AND user_id=?",
        (amount, category, description, date_str, account_id, expense_id, user_id),
    )
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def delete_expense_row(expense_id: int, user_id: int) -> bool:
    """Delete an expense and restore the amount to the linked account balance."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Get the expense data to restore balance
    cur.execute("SELECT amount, account_id FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    expense = cur.fetchone()
    
    if expense:
        amount, account_id = expense
        
        # Restore balance to account (add back the amount)
        if account_id:
            cur.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ? AND user_id = ?",
                (amount, account_id, user_id),
            )
    
    # Delete the expense
    cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?",(expense_id, user_id))
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


def total_expenses_by_account(user_id: int, account_id: int) -> float:
    """Get total expenses for a specific account."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id=? AND account_id=?", (user_id, account_id))
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
    """Insert a new account and return its ID. If this is the first account, it becomes primary."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Check if user has any existing accounts - if not, this will be primary
    cur.execute("SELECT COUNT(*) FROM accounts WHERE user_id = ? AND status = 'active'", (user_id,))
    existing_count = cur.fetchone()[0]
    is_primary = 1 if existing_count == 0 else 0
    
    # Get next sort order
    cur.execute("SELECT COALESCE(MAX(sort_order), 0) + 1 FROM accounts WHERE user_id = ?", (user_id,))
    next_order = cur.fetchone()[0]
    cur.execute(
        """INSERT INTO accounts (user_id, name, account_number, type, balance, currency, color, is_primary, status, sort_order, created_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)""",
        (user_id, name, account_number, account_type, balance, currency, color, is_primary, next_order, created_at),
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


def set_account_as_primary(user_id: int, account_id: int) -> bool:
    """Set an account as the primary account for a user."""
    conn = connect_db()
    cur = conn.cursor()
    # First, unset all other accounts as primary
    cur.execute("UPDATE accounts SET is_primary = 0 WHERE user_id = ?", (user_id,))
    # Then set the specified account as primary
    cur.execute("UPDATE accounts SET is_primary = 1 WHERE id = ? AND user_id = ?", (account_id, user_id))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return updated > 0


def get_primary_account(user_id: int):
    """Get the primary account for a user."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at 
           FROM accounts WHERE user_id = ? AND is_primary = 1 LIMIT 1""",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_total_balance_by_user(user_id: int) -> float:
    """Get total balance across all accounts for a user."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT SUM(balance) FROM accounts WHERE user_id = ? AND status = 'active'", (user_id,))
    total = cur.fetchone()[0]
    conn.close()
    return float(total) if total else 0.0


def get_selected_account(user_id: int):
    """Get the currently selected account for display on home page.
    If no account is selected, returns the primary account."""
    conn = connect_db()
    cur = conn.cursor()
    
    # First check if user has a selected_account_id stored
    selected_id = None
    try:
        cur.execute("SELECT selected_account_id FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row and row[0] is not None:
            selected_id = row[0]
    except Exception as e:
        print(f"Error getting selected_account_id: {e}")
    
    if selected_id is not None:
        # Get the selected account
        cur.execute(
            """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at 
               FROM accounts WHERE id = ? AND user_id = ? AND status = 'active'""",
            (selected_id, user_id),
        )
        account = cur.fetchone()
        if account:
            conn.close()
            return account
        # If selected account not found (deleted?), clear the selection
        cur.execute("UPDATE users SET selected_account_id = NULL WHERE id = ?", (user_id,))
        conn.commit()
    
    # Fallback to primary account
    cur.execute(
        """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at 
           FROM accounts WHERE user_id = ? AND is_primary = 1 AND status = 'active' LIMIT 1""",
        (user_id,),
    )
    account = cur.fetchone()
    conn.close()
    return account


def set_selected_account(user_id: int, account_id: int) -> bool:
    """Set the selected account for a user to display on home page."""
    conn = connect_db()
    cur = conn.cursor()
    
    # Add column if it doesn't exist
    try:
        cur.execute("ALTER TABLE users ADD COLUMN selected_account_id INTEGER")
        conn.commit()
    except:
        pass  # Column already exists
    
    cur.execute("UPDATE users SET selected_account_id = ? WHERE id = ?", (account_id, user_id))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    print(f"set_selected_account: user_id={user_id}, account_id={account_id}, updated={updated}")
    return updated > 0


def get_account_by_id(account_id: int, user_id: int):
    """Get a specific account by ID."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, name, account_number, type, balance, currency, color, is_primary, created_at 
           FROM accounts WHERE id = ? AND user_id = ?""",
        (account_id, user_id),
    )
    row = cur.fetchone()
    conn.close()
    return row


# ----- OTP/Password Reset helpers -----
def create_password_reset_otp(user_id: int, otp: str) -> bool:
    """Create a new password reset OTP for a user."""
    from datetime import datetime
    conn = connect_db()
    cur = conn.cursor()
    try:
        # Invalidate any existing unused OTPs for this user
        cur.execute("UPDATE password_reset_otps SET is_used = 1 WHERE user_id = ? AND is_used = 0", (user_id,))
        
        # Create new OTP
        cur.execute(
            "INSERT INTO password_reset_otps (user_id, otp, created_at) VALUES (?, ?, ?)",
            (user_id, otp, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating OTP: {e}")
        return False
    finally:
        conn.close()


def verify_password_reset_otp(user_id: int, otp: str) -> tuple:
    """
    Verify a password reset OTP.
    Returns (success, message, otp_id).
    """
    from utils.otp import is_otp_expired
    
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT id, created_at, is_used FROM password_reset_otps WHERE user_id = ? AND otp = ? ORDER BY created_at DESC LIMIT 1",
        (user_id, otp)
    )
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return (False, "Invalid OTP code", None)
    
    otp_id, created_at, is_used = row
    
    if is_used:
        return (False, "This OTP has already been used", None)
    
    if is_otp_expired(created_at):
        return (False, "OTP has expired. Please request a new one", None)
    
    return (True, "OTP verified successfully", otp_id)


def mark_otp_as_used(otp_id: int):
    """Mark an OTP as used after successful password reset."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE password_reset_otps SET is_used = 1 WHERE id = ?", (otp_id,))
    conn.commit()
    conn.close()


def cleanup_expired_otps():
    """Clean up OTPs older than 24 hours."""
    from datetime import datetime, timedelta
    conn = connect_db()
    cur = conn.cursor()
    
    cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
    cur.execute("DELETE FROM password_reset_otps WHERE created_at < ?", (cutoff,))
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted


def get_user_by_email(email: str):
    """Get user by email address."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return row  # (id, username, email) or None


def update_password(user_id: int, new_password_blob: bytes) -> bool:
    """Update user password."""
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET password = ? WHERE id = ?", (new_password_blob, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        conn.close()


def save_user_passcode(user_id: int, passcode_hash: str) -> bool:
    """Save hashed passcode for a user."""
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET passcode = ? WHERE id = ?", (passcode_hash, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error saving passcode: {e}")
        return False
    finally:
        conn.close()


def get_user_passcode(user_id: int) -> str:
    """Get stored passcode hash for a user."""
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT passcode FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row and row[0] else None
    except Exception as e:
        print(f"Error getting passcode: {e}")
        return None
    finally:
        conn.close()


def has_passcode(user_id: int) -> bool:
    """Check if user has set up a passcode."""
    passcode = get_user_passcode(user_id)
    return passcode is not None and passcode != ""


# ----- ADMIN functions -----
def insert_admin(username: str, password_blob: bytes, full_name: str = "", email: str = "") -> bool:
    """Insert a new admin user."""
    from datetime import datetime
    conn = connect_db()
    cur = conn.cursor()
    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            "INSERT INTO admins (username, password, full_name, email, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, password_blob, full_name, email, created_at)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_admin_by_username(username: str):
    """Get admin by username."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, full_name, email, role, is_active FROM admins WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def update_admin_last_login(admin_id: int):
    """Update admin last login timestamp."""
    from datetime import datetime
    conn = connect_db()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE admins SET last_login = ? WHERE id = ?", (timestamp, admin_id))
    conn.commit()
    conn.close()


def log_admin_activity(admin_id: int, action: str, target_user_id: int = None, details: str = ""):
    """Log admin activity."""
    from datetime import datetime
    conn = connect_db()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO admin_logs (admin_id, action, target_user_id, details, timestamp) VALUES (?, ?, ?, ?, ?)",
        (admin_id, action, target_user_id, details, timestamp)
    )
    conn.commit()
    conn.close()


def get_all_users_for_admin():
    """Get all users with their statistics for admin dashboard."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.full_name, u.email, u.last_login, u.has_seen_onboarding,
               (SELECT COUNT(*) FROM expenses WHERE user_id = u.id) as expense_count,
               (SELECT SUM(amount) FROM expenses WHERE user_id = u.id) as total_spent
        FROM users u
        ORDER BY u.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_admin_logs(limit: int = 100):
    """Get recent admin activity logs."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT al.id, al.admin_id, a.username as admin_username, al.action, 
               al.target_user_id, u.username as target_username, al.details, al.timestamp
        FROM admin_logs al
        LEFT JOIN admins a ON al.admin_id = a.id
        LEFT JOIN users u ON al.target_user_id = u.id
        ORDER BY al.timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_system_statistics():
    """Get system-wide statistics for admin dashboard."""
    conn = connect_db()
    cur = conn.cursor()
    
    stats = {}
    
    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    stats['total_users'] = cur.fetchone()[0]
    
    # Total expenses
    cur.execute("SELECT COUNT(*) FROM expenses")
    stats['total_expenses'] = cur.fetchone()[0]
    
    # Total amount spent
    cur.execute("SELECT SUM(amount) FROM expenses")
    result = cur.fetchone()[0]
    stats['total_amount'] = result if result else 0
    
    # Total accounts
    cur.execute("SELECT COUNT(*) FROM accounts")
    stats['total_accounts'] = cur.fetchone()[0]
    
    # Active users (logged in last 30 days)
    cur.execute("""
        SELECT COUNT(*) FROM users 
        WHERE last_login IS NOT NULL 
        AND datetime(last_login) >= datetime('now', '-30 days')
    """)
    stats['active_users'] = cur.fetchone()[0]
    
    # New users this month
    cur.execute("""
        SELECT COUNT(*) FROM users 
        WHERE datetime(last_login) >= datetime('now', 'start of month')
    """)
    stats['new_users_this_month'] = cur.fetchone()[0]
    
    conn.close()
    return stats


def delete_user_by_admin(user_id: int) -> bool:
    """Delete a user and all their data (admin action)."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Delete all expenses
        cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
        # Delete all accounts
        cursor.execute("DELETE FROM accounts WHERE user_id = ?", (user_id,))
        # Delete passcodes
        cursor.execute("DELETE FROM passcodes WHERE user_id = ?", (user_id,))
        # Delete user profile
        cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting user: {e}")
        return False
    finally:
        conn.close()

def set_biometric_enabled(user_id: int, enabled: bool = True) -> bool:
    """Enable or disable biometric authentication for a user."""
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET biometric_enabled = ? WHERE id = ?", (1 if enabled else 0, user_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error setting biometric preference: {e}")
        return False
    finally:
        conn.close()


def is_biometric_enabled(user_id: int) -> bool:
    """Check if user has biometric authentication enabled."""
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT biometric_enabled FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return bool(row[0]) if row and row[0] is not None else False
    except Exception as e:
        print(f"Error checking biometric preference: {e}")
        return False
    finally:
        conn.close()


# ==================== ADMIN CONFIGURATION & POLICY ====================

def init_admin_config_tables():
    """Initialize admin configuration and policy tables"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Expense Categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expense_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        gl_code TEXT,
        icon TEXT DEFAULT 'category',
        color TEXT DEFAULT '#2196F3',
        is_active INTEGER DEFAULT 1,
        parent_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_id) REFERENCES expense_categories(id)
    )
    """)
    
    # Policy Rules table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS policy_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT NOT NULL,
        rule_type TEXT NOT NULL,
        category_id INTEGER,
        max_amount REAL,
        currency TEXT DEFAULT 'PHP',
        requires_receipt INTEGER DEFAULT 0,
        requires_approval INTEGER DEFAULT 1,
        disallowed_vendors TEXT,
        per_diem_rate REAL,
        description TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES expense_categories(id)
    )
    """)
    
    # Currency Exchange Rates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS currency_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_currency TEXT NOT NULL,
        to_currency TEXT NOT NULL,
        rate REAL NOT NULL,
        effective_date TEXT DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1,
        source TEXT DEFAULT 'manual',
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(from_currency, to_currency, effective_date)
    )
    """)
    
    # Accounting Integration Config table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounting_integration (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        api_key TEXT,
        api_secret TEXT,
        company_id TEXT,
        sync_enabled INTEGER DEFAULT 0,
        last_sync TEXT,
        sync_frequency TEXT DEFAULT 'daily',
        auto_sync INTEGER DEFAULT 0,
        config_json TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Sync Logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        integration_id INTEGER,
        sync_type TEXT,
        status TEXT,
        records_synced INTEGER DEFAULT 0,
        error_message TEXT,
        started_at TEXT DEFAULT CURRENT_TIMESTAMP,
        completed_at TEXT,
        FOREIGN KEY (integration_id) REFERENCES accounting_integration(id)
    )
    """)
    
    conn.commit()
    conn.close()


# ==================== EXPENSE CATEGORIES CRUD ====================

def get_expense_categories(include_inactive=False):
    """Get all expense categories"""
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
    SELECT id, name, description, gl_code, icon, color, is_active, parent_id, created_at, updated_at
    FROM expense_categories
    """
    if not include_inactive:
        query += " WHERE is_active = 1"
    query += " ORDER BY name"
    
    cursor.execute(query)
    return cursor.fetchall()


def add_expense_category(name, description="", gl_code="", icon="category", color="#2196F3", parent_id=None):
    """Add new expense category"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO expense_categories (name, description, gl_code, icon, color, parent_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, gl_code, icon, color, parent_id))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def update_expense_category(category_id, name=None, description=None, gl_code=None, icon=None, color=None, is_active=None):
    """Update expense category"""
    conn = connect_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if gl_code is not None:
        updates.append("gl_code = ?")
        params.append(gl_code)
    if icon is not None:
        updates.append("icon = ?")
        params.append(icon)
    if color is not None:
        updates.append("color = ?")
        params.append(color)
    if is_active is not None:
        updates.append("is_active = ?")
        params.append(is_active)
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(category_id)
    
    cursor.execute(f"""
    UPDATE expense_categories
    SET {', '.join(updates)}
    WHERE id = ?
    """, params)
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_expense_category(category_id):
    """Delete expense category (soft delete)"""
    return update_expense_category(category_id, is_active=0)


# ==================== POLICY RULES CRUD ====================

def get_policy_rules(include_inactive=False):
    """Get all policy rules"""
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
    SELECT pr.id, pr.rule_name, pr.rule_type, pr.category_id, ec.name as category_name,
           pr.max_amount, pr.currency, pr.requires_receipt, pr.requires_approval,
           pr.disallowed_vendors, pr.per_diem_rate, pr.description, pr.is_active,
           pr.created_at, pr.updated_at
    FROM policy_rules pr
    LEFT JOIN expense_categories ec ON pr.category_id = ec.id
    """
    if not include_inactive:
        query += " WHERE pr.is_active = 1"
    query += " ORDER BY pr.rule_name"
    
    cursor.execute(query)
    return cursor.fetchall()


def add_policy_rule(rule_name, rule_type, category_id=None, max_amount=None, currency="PHP", 
                   requires_receipt=0, requires_approval=1, disallowed_vendors="", 
                   per_diem_rate=None, description=""):
    """Add new policy rule"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO policy_rules (rule_name, rule_type, category_id, max_amount, currency,
                             requires_receipt, requires_approval, disallowed_vendors,
                             per_diem_rate, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (rule_name, rule_type, category_id, max_amount, currency, requires_receipt,
          requires_approval, disallowed_vendors, per_diem_rate, description))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid


def update_policy_rule(rule_id, **kwargs):
    """Update policy rule"""
    conn = connect_db()
    cursor = conn.cursor()
    
    valid_fields = ['rule_name', 'rule_type', 'category_id', 'max_amount', 'currency',
                   'requires_receipt', 'requires_approval', 'disallowed_vendors',
                   'per_diem_rate', 'description', 'is_active']
    
    updates = []
    params = []
    
    for field, value in kwargs.items():
        if field in valid_fields:
            updates.append(f"{field} = ?")
            params.append(value)
    
    if not updates:
        return False
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(rule_id)
    
    cursor.execute(f"""
    UPDATE policy_rules
    SET {', '.join(updates)}
    WHERE id = ?
    """, params)
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_policy_rule(rule_id):
    """Delete policy rule (soft delete)"""
    return update_policy_rule(rule_id, is_active=0)


# ==================== CURRENCY EXCHANGE RATES ====================

def get_currency_rates(from_currency=None, to_currency=None):
    """Get currency exchange rates"""
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
    SELECT id, from_currency, to_currency, rate, effective_date, is_active, source, updated_at
    FROM currency_rates
    WHERE is_active = 1
    """
    params = []
    
    if from_currency:
        query += " AND from_currency = ?"
        params.append(from_currency)
    if to_currency:
        query += " AND to_currency = ?"
        params.append(to_currency)
    
    query += " ORDER BY effective_date DESC, from_currency, to_currency"
    
    cursor.execute(query, params)
    return cursor.fetchall()


def add_currency_rate(from_currency, to_currency, rate, effective_date=None, source="manual"):
    """Add currency exchange rate"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO currency_rates (from_currency, to_currency, rate, effective_date, source)
        VALUES (?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP), ?)
        """, (from_currency, to_currency, rate, effective_date, source))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Update existing rate
        cursor.execute("""
        UPDATE currency_rates
        SET rate = ?, updated_at = CURRENT_TIMESTAMP, source = ?
        WHERE from_currency = ? AND to_currency = ? AND effective_date = COALESCE(?, CURRENT_TIMESTAMP)
        """, (rate, source, from_currency, to_currency, effective_date))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_currency_rate(rate_id, rate=None, is_active=None):
    """Update currency rate"""
    conn = connect_db()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if rate is not None:
        updates.append("rate = ?")
        params.append(rate)
    if is_active is not None:
        updates.append("is_active = ?")
        params.append(is_active)
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(rate_id)
    
    cursor.execute(f"""
    UPDATE currency_rates
    SET {', '.join(updates)}
    WHERE id = ?
    """, params)
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# ==================== ACCOUNTING INTEGRATION ====================

def get_accounting_integrations():
    """Get all accounting integrations"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, platform, company_id, sync_enabled, last_sync, sync_frequency,
           auto_sync, is_active, created_at, updated_at
    FROM accounting_integration
    WHERE is_active = 1
    ORDER BY platform
    """)
    
    return cursor.fetchall()


def add_accounting_integration(platform, api_key="", api_secret="", company_id="", 
                               sync_enabled=0, sync_frequency="daily", auto_sync=0, config_json="{}"):
    """Add accounting integration"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO accounting_integration (platform, api_key, api_secret, company_id,
                                       sync_enabled, sync_frequency, auto_sync, config_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (platform, api_key, api_secret, company_id, sync_enabled, sync_frequency, auto_sync, config_json))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid


def update_accounting_integration(integration_id, **kwargs):
    """Update accounting integration"""
    conn = connect_db()
    cursor = conn.cursor()
    
    valid_fields = ['platform', 'api_key', 'api_secret', 'company_id', 'sync_enabled',
                   'last_sync', 'sync_frequency', 'auto_sync', 'config_json', 'is_active']
    
    updates = []
    params = []
    
    for field, value in kwargs.items():
        if field in valid_fields:
            updates.append(f"{field} = ?")
            params.append(value)
    
    if not updates:
        return False
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(integration_id)
    
    cursor.execute(f"""
    UPDATE accounting_integration
    SET {', '.join(updates)}
    WHERE id = ?
    """, params)
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def log_sync_activity(integration_id, sync_type, status, records_synced=0, error_message=None):
    """Log sync activity"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO sync_logs (integration_id, sync_type, status, records_synced, error_message, completed_at)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (integration_id, sync_type, status, records_synced, error_message))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid


def get_sync_logs(integration_id=None, limit=50):
    """Get sync logs"""
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """
    SELECT sl.id, sl.integration_id, ai.platform, sl.sync_type, sl.status,
           sl.records_synced, sl.error_message, sl.started_at, sl.completed_at
    FROM sync_logs sl
    JOIN accounting_integration ai ON sl.integration_id = ai.id
    """
    
    if integration_id:
        query += " WHERE sl.integration_id = ?"
        cursor.execute(query + " ORDER BY sl.started_at DESC LIMIT ?", (integration_id, limit))
    else:
        cursor.execute(query + " ORDER BY sl.started_at DESC LIMIT ?", (limit,))
    
    return cursor.fetchall()
