# Passcode Lock Feature Documentation

## Overview
The Passcode Lock feature adds an additional security layer to the Smart Expense Tracker app. Users create a 4-digit PIN during signup and must enter it after logging in to access the app.

## User Flow

### New User Registration Flow
1. **Sign Up** → Enter username and password
2. **Personal Details** → Enter name, email, phone, etc.
3. **🔒 Passcode Setup** (NEW) → Create 4-digit PIN
4. **Passcode Confirmation** → Re-enter PIN to confirm
5. **Currency Selection** → Choose default currency
6. **My Balance** → Set initial cash balance
7. **Onboarding** → View app introduction
8. **Home** → Start using the app

### Returning User Login Flow
1. **Login** → Enter username and password
2. **🔒 Passcode Verification** (NEW) → Enter 4-digit PIN
3. **Home** → Access the app

## Implementation Details

### Files Created/Modified

#### 1. `ui/passcode_lock_page.py` (NEW - 420 lines)
Main UI component for passcode functionality.

**Functions:**
- `create_passcode_setup(page, state, on_complete)` - Setup screen shown after account creation
  - Two-phase entry: Create PIN → Confirm PIN
  - Visual dot indicators show entered digits
  - Number pad (0-9) with backspace
  - PIN mismatch error handling
  - Success animation and feedback
  
- `create_passcode_verify(page, state, on_success, on_forgot)` - Verification screen shown after login
  - Visual dot indicators for PIN entry
  - Number pad (0-9) with backspace
  - Wrong PIN attempt tracking
  - "Forgot Passcode?" option
  - Lock icon and security messaging

- `hash_passcode(passcode)` - SHA256 hashing utility for secure storage

**UI Features:**
- Animated dot indicators (filled/empty circles)
- Haptic-style number pad (3x4 grid)
- Biometric icon placeholder for future enhancement
- Error messages with shake animations
- Success feedback with checkmark icon
- Theme-aware styling using app theme system

#### 2. `core/db.py` (MODIFIED - Added ~40 lines)
Database schema and functions for passcode storage.

**Schema Changes:**
```sql
ALTER TABLE users ADD COLUMN passcode TEXT;
```

**New Functions:**
- `save_user_passcode(user_id, passcode_hash)` - Store hashed PIN
- `get_user_passcode(user_id)` - Retrieve stored hash
- `has_passcode(user_id)` - Check if user has PIN configured

**Location:** Added after `update_password()` function (~line 777)

#### 3. `src/main.py` (MODIFIED)
Integration into main application flow.

**Changes:**
- Added import: `from ui.passcode_lock_page import create_passcode_setup, create_passcode_verify`
- Added navigation functions:
  - `show_passcode_setup()` - Navigate to setup screen
  - `show_passcode_verify()` - Navigate to verify screen
- Modified `on_login_success(user_id)`:
  - Checks if user has passcode using `db.has_passcode(user_id)`
  - If yes → Show verification screen
  - If no → Proceed to onboarding/home
- Added `on_passcode_verify_success()`:
  - Called after successful verification
  - Navigates to onboarding or home
- Modified `show_personal_details()`:
  - Changed completion callback from `show_currency_selection` to `show_passcode_setup`
- Modified `on_passcode_setup_complete()`:
  - Navigates to `show_currency_selection` after passcode setup

## Security Features

### Passcode Storage
- PINs are **never stored in plain text**
- Uses SHA256 hashing via Python's `hashlib` library
- Hash format: `hashlib.sha256(passcode.encode()).hexdigest()`

### Verification Process
1. User enters 4-digit PIN
2. System hashes the entered PIN
3. Compares hash with stored hash in database
4. Access granted only if hashes match

### Attempt Tracking
- Tracks failed verification attempts
- Displays error messages for incorrect PINs
- Future enhancement: Lock account after X failed attempts

## Usage Examples

### Checking if User Has Passcode
```python
from core import db

user_id = 1
if db.has_passcode(user_id):
    print("User has passcode set up")
else:
    print("User needs to set up passcode")
```

### Setting Up New Passcode
```python
from core import db
import hashlib

user_id = 1
passcode = "1234"
passcode_hash = hashlib.sha256(passcode.encode()).hexdigest()
db.save_user_passcode(user_id, passcode_hash)
```

### Verifying Passcode
```python
from core import db
import hashlib

user_id = 1
entered_passcode = "1234"
entered_hash = hashlib.sha256(entered_passcode.encode()).hexdigest()
stored_hash = db.get_user_passcode(user_id)

if entered_hash == stored_hash:
    print("Access granted")
else:
    print("Access denied")
```

## UI Design

### Passcode Setup Screen
```
┌─────────────────────────────┐
│     🔒 Lock Icon (large)    │
│                             │
│    Create Your Passcode     │
│  Enter a 4-digit PIN code   │
│                             │
│       ○ ○ ○ ○              │
│      (dot indicators)       │
│                             │
│   ┌─────┬─────┬─────┐      │
│   │  1  │  2  │  3  │      │
│   ├─────┼─────┼─────┤      │
│   │  4  │  5  │  6  │      │
│   ├─────┼─────┼─────┤      │
│   │  7  │  8  │  9  │      │
│   ├─────┼─────┼─────┤      │
│   │  👆 │  0  │  ⌫  │      │
│   └─────┴─────┴─────┘      │
└─────────────────────────────┘
```

### Passcode Verification Screen
```
┌─────────────────────────────┐
│     🔒 Lock Icon (large)    │
│                             │
│     Enter Your Passcode     │
│   Enter PIN to unlock app   │
│                             │
│       ● ○ ○ ○              │
│      (filled = entered)     │
│                             │
│   ┌─────┬─────┬─────┐      │
│   │  1  │  2  │  3  │      │
│   ├─────┼─────┼─────┤      │
│   │  4  │  5  │  6  │      │
│   ├─────┼─────┼─────┤      │
│   │  7  │  8  │  9  │      │
│   ├─────┼─────┼─────┤      │
│   │  👆 │  0  │  ⌫  │      │
│   └─────┴─────┴─────┘      │
│                             │
│    Forgot Passcode?         │
└─────────────────────────────┘
```

## Testing Checklist

### New User Flow
- [ ] Complete signup with username/password
- [ ] Enter personal details
- [ ] See passcode setup screen
- [ ] Create 4-digit PIN
- [ ] Confirm 4-digit PIN
- [ ] See success message
- [ ] Continue to currency selection
- [ ] Complete remaining setup
- [ ] Access home screen

### Returning User Flow
- [ ] Enter username/password on login
- [ ] See passcode verification screen
- [ ] Enter correct 4-digit PIN
- [ ] Access home screen immediately

### Error Cases
- [ ] Mismatched PINs during setup → Show error
- [ ] Wrong PIN during verification → Show error
- [ ] Empty PIN entry → Disabled continue button
- [ ] Forgot passcode link → Navigate to password reset

### Edge Cases
- [ ] User with no passcode set → Skip verification
- [ ] Session timeout → Require login + passcode again
- [ ] Database error → Show appropriate error message

## Future Enhancements

### 1. Biometric Authentication
- Add fingerprint/face recognition support
- Fallback to PIN if biometric fails
- Settings toggle for biometric preference

### 2. Passcode Settings
- Add "Change Passcode" option in account settings
- Allow disabling passcode lock
- Require current passcode before changes

### 3. Enhanced Security
- Lock account after 5 failed attempts
- Add cooldown timer (e.g., wait 30 seconds)
- Send email notification on failed attempts
- Log security events

### 4. Recovery Options
- Security questions for passcode reset
- Email-based passcode reset flow
- Emergency backup codes

### 5. UI Improvements
- Haptic feedback on number press (mobile)
- Shake animation on wrong PIN
- Custom lock screen background
- Dark/light theme support

## Troubleshooting

### Issue: Passcode screen not showing
**Solution:** Check if `db.has_passcode(user_id)` returns True. User might not have passcode set up yet.

### Issue: Cannot verify passcode
**Solution:** Ensure hashing is consistent. Both setup and verification must use SHA256.

### Issue: Database error on passcode save
**Solution:** Check if passcode column exists in users table. Run database migration if needed.

### Issue: Forgot passcode doesn't work
**Solution:** Implement password reset flow that also resets passcode.

## Code Locations

| Component | File Path | Lines |
|-----------|-----------|-------|
| Setup UI | `ui/passcode_lock_page.py` | 1-200 |
| Verify UI | `ui/passcode_lock_page.py` | 201-420 |
| DB Functions | `core/db.py` | ~777-817 |
| Main Integration | `src/main.py` | Various |
| Navigation | `src/main.py` | ~171-183 |
| Login Callback | `src/main.py` | ~186-199 |

## Database Schema

```sql
-- Users table with passcode column
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    full_name TEXT,
    phone TEXT,
    currency TEXT,
    passcode TEXT,  -- Added: SHA256 hash of 4-digit PIN
    created_at TEXT,
    updated_at TEXT
);
```

## Dependencies
- `flet` - UI framework
- `hashlib` (built-in) - Passcode hashing
- `core.db` - Database operations
- `core.theme` - Theme styling

## Changelog

### Version 1.0.0 (Current)
- ✅ Initial passcode lock implementation
- ✅ Two-phase setup (create + confirm)
- ✅ Verification screen with attempt tracking
- ✅ SHA256 hashing for security
- ✅ Integration into signup/login flow
- ✅ Animated dot indicators
- ✅ Number pad UI with backspace
- ✅ Forgot passcode placeholder

### Planned for Version 1.1.0
- ⏳ Biometric authentication support
- ⏳ Passcode settings page
- ⏳ Account lockout after failed attempts
- ⏳ Security event logging

---

**Author:** Smart Expense Tracker Team  
**Created:** January 2025  
**Last Updated:** January 2025
