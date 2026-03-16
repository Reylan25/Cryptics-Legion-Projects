# Data Model

## Entity Relationship Diagram (ERD)


![alt text](image.png)


---

## Table Schemas

### **users**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    base_currency TEXT DEFAULT 'PHP',
    passcode_enabled BOOLEAN DEFAULT 0,
    passcode_hash TEXT,
    biometric_enabled BOOLEAN DEFAULT 0
);
```

### **accounts**
```sql
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    account_number TEXT,
    account_type TEXT,  -- Cash, Savings, Credit Card, etc.
    balance REAL DEFAULT 0,
    currency TEXT DEFAULT 'PHP',
    color TEXT DEFAULT '#3B82F6',
    is_primary BOOLEAN DEFAULT 0,
    status TEXT DEFAULT 'active',  -- active, excluded, archived
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sort_order INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
```

### **expenses**
```sql
CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'PHP',
    category TEXT,
    date DATE NOT NULL,
    time TIME,
    payment_method TEXT,
    tags TEXT,  -- JSON array or comma-separated
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES accounts(account_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
```

### **password_reset_otps**
```sql
CREATE TABLE password_reset_otps (
    otp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    otp_code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_used BOOLEAN DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
```

---

## Key Relationships

### **Users → Accounts** (1:N)
- One user can have multiple accounts (Cash, Savings, Credit Card, E-Wallet, etc.)
- Each account belongs to exactly one user
- Primary key: `account_id`, Foreign key: `user_id`

### **Accounts → Expenses** (1:N)
- One account can have multiple expenses
- Each expense is recorded against a specific account
- Primary key: `expense_id`, Foreign key: `account_id`

### **Users → Expenses** (1:N)
- Expenses are also directly linked to users for querying purposes
- Allows filtering expenses by user across all accounts

### **Users → PasswordResetOTPs** (1:N)
- Users can have multiple OTP requests over time
- Each OTP is single-use and time-limited (expires in 15 minutes)

---

## Currency Support Matrix

| Code | Symbol | Name | Status |
|------|--------|------|--------|
| PHP | ₱ | Philippine Peso | ✅ Active |
| USD | $ | US Dollar | ✅ Active |
| EUR | € | Euro | ✅ Active |
| GBP | £ | British Pound | ✅ Active |
| JPY | ¥ | Japanese Yen | ✅ Active |
| KRW | ₩ | Korean Won | ✅ Active |
| SGD | S$ | Singapore Dollar | ✅ Active |
| AUD | A$ | Australian Dollar | ✅ Active |
| CAD | C$ | Canadian Dollar | ✅ Active |
| INR | ₹ | Indian Rupee | ✅ Active |

---

## Data Constraints & Validation

| Field | Type | Validation | Rules |
|-------|------|-----------|-------|
| username | TEXT | 3-50 chars, alphanumeric | UNIQUE, NOT NULL |
| password_hash | BLOB | bcrypt hash | NOT NULL |
| email | TEXT | Valid email format | Optional |
| amount | REAL | > 0 | NOT NULL |
| balance | REAL | Any value | Can be negative |
| account_type | TEXT | Predefined list | One of: Cash, Savings, Credit Card, Debit Card, E-Wallet, Other |
| date | DATE | Valid date | NOT NULL |
| otp_code | TEXT | 6 digits | Single-use, 15-min expiry |

---

## Data Storage Details

- **Format**: SQLite3 database (`cryptics_legion.db`)
- **Location**: `storage/` directory (persistent)
- **Encryption**: Passwords hashed with bcrypt, OTPs encrypted
- **Backup**: Users should regularly backup `cryptics_legion.db`

