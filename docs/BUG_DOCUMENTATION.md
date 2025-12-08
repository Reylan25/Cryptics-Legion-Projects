# Bug Documentation - Cryptics Legion Project

## Bug Report: Account Currency Display Issue

### Date Discovered
December 8, 2025

---

## Issue Summary
All accounts in the Account Settings page were displaying "INR" (Indian Rupee) currency regardless of their actual stored currency values in the database. Additionally, the currency dropdown was not visible or accessible when editing accounts.

---

## How the Bug Was Encountered

### Initial Observation
1. **User Action**: Navigated to Expenses page → Clicked Account Settings icon
2. **Expected Behavior**: Each account should display its own currency (PHP, USD, KRW, etc.)
3. **Actual Behavior**: All accounts showed "INR" in the account list:
   - Cash → INR 50,000.00
   - Reyanaldo → INR 20,000.00
   - roger → INR 200,000.00

### Steps to Reproduce
1. Open the application
2. Go to "Expenses" page
3. Click the settings icon (⚙️) to open "Account Settings"
4. Observe that all accounts display "INR" currency
5. Click on any account to edit
6. Scroll through the edit form
7. Notice: Currency dropdown was missing or not visible

---

## Root Cause Analysis

### Investigation Process

#### Step 1: Database Verification
Queried the database to check actual stored currency values:

```sql
SELECT id, name, currency FROM accounts WHERE user_id = 11;
```

**Result**: Database had correct values stored:
- Cash: INR
- Reyanaldo: KRW (Korean Won)
- roger: KRW (Korean Won)
- jehan: USD (US Dollar)
- LUIS: PHP (Philippine Peso)

**Conclusion**: Data was correct in database, issue was in display logic.

---

#### Step 2: Code Analysis - Duplicate Functions

**Discovery**: Found TWO `show_account_settings()` functions in `Expenses.py`:
- **Function 1**: Line 1185 (inside `create_expenses_view`) - Had currency support
- **Function 2**: Line 2652 (inside `build_expenses_content`) - Missing currency support

**Issue**: The application was using Function 2 which had outdated code.

---

### The Bugs Found

#### Bug #1: Incorrect Currency Display (Line 2755)
**Location**: `src/ui/Expenses.py` line 2755

**Problematic Code**:
```python
ft.Text(f"{user_currency} {acc_balance:,.2f}", size=12, color=theme.text_secondary)
```

**Problem**: Used `user_currency` (user's default: INR) instead of `acc_currency` (account's actual currency)

**Result**: All accounts displayed INR because that was the logged-in user's default currency preference.

---

#### Bug #2: Missing Currency Dropdown in Edit Form
**Location**: `src/ui/Expenses.py` function `show_edit_form` (line 2658)

**Problem**: The edit form layout was missing:
1. Currency dropdown field
2. Currency value in save function

**Edit Form Had**:
- Account name field ✓
- Balance field ✓
- Type dropdown ✓
- Color selection ✓

**Edit Form Missing**:
- Currency dropdown ✗
- Currency save logic ✗

---

#### Bug #3: Undefined Variable Scope
**Location**: `src/ui/Expenses.py` line 1185 `show_account_settings()` function

**Problem**: Function used `user_currency` variable in fallback logic, but `user_currency` was never defined in that function's scope.

**Code**:
```python
def show_account_settings():
    theme = get_theme()
    # user_currency was NOT defined here!
    
    def create_account_settings_card(account_data):
        if not acc_currency:
            acc_currency = user_currency  # ← UNDEFINED VARIABLE
```

---

## The Fix

### Fix #1: Display Each Account's Own Currency
**File**: `src/ui/Expenses.py` line ~2740

**Before**:
```python
ft.Text(f"{user_currency} {acc_balance:,.2f}", size=12, color=theme.text_secondary)
```

**After**:
```python
# Use account's own currency, fallback to user currency if NULL
display_currency = acc_currency if acc_currency else user_currency

ft.Row([
    ft.Text(acc_name, size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
    ft.Container(
        content=ft.Text(display_currency, size=10, weight=ft.FontWeight.W_600, color="white"),
        padding=ft.padding.symmetric(horizontal=8, vertical=3), 
        bgcolor=theme.accent_primary,
        border_radius=6,
    ),
], spacing=8),
ft.Text(f"{acc_balance:,.2f}", size=12, color=theme.text_secondary),
```

**Changes**:
- Separated currency from balance display
- Added currency badge next to account name
- Used `display_currency` variable with proper fallback

---

### Fix #2: Added Currency Dropdown to Edit Form
**File**: `src/ui/Expenses.py` line ~2676

**Added**:
```python
currency_dropdown = ft.Dropdown(
    label="Currency", 
    value=acc_currency if acc_currency else "PHP",
    options=[
        ft.dropdown.Option(key="PHP", text="₱ PHP"),
        ft.dropdown.Option(key="USD", text="$ USD"),
        ft.dropdown.Option(key="EUR", text="€ EUR"),
        ft.dropdown.Option(key="JPY", text="¥ JPY"),
        ft.dropdown.Option(key="GBP", text="£ GBP"),
        ft.dropdown.Option(key="KRW", text="₩ KRW"),
        ft.dropdown.Option(key="SGD", text="S$ SGD"),
        ft.dropdown.Option(key="AUD", text="A$ AUD"),
        ft.dropdown.Option(key="CAD", text="C$ CAD"),
        ft.dropdown.Option(key="INR", text="₹ INR"),
    ],
    border_color=theme.border_primary,
    focused_border_color=theme.accent_primary,
    bgcolor=theme.bg_card,
    color=theme.text_primary,
    label_style=ft.TextStyle(color=theme.text_secondary),
    border_radius=12
)
```

**Updated Save Function**:
```python
def save_changes(e):
    new_name = name_field.value
    new_balance = float(balance_field.value or 0)
    new_type = type_dropdown.value
    new_currency = currency_dropdown.value  # ← ADDED
    new_color = selected_color["value"]
    
    db.update_account(acc_id, state["user_id"], name=new_name, 
                     account_type=new_type, balance=new_balance, 
                     currency=new_currency, color=new_color)  # ← ADDED
```

**Updated Form Layout**:
```python
name_field, ft.Container(height=16), 
balance_field, ft.Container(height=16),
type_dropdown, ft.Container(height=16), 
currency_dropdown,  # ← ADDED
ft.Container(height=20),
```

---

### Fix #3: Define User Currency in Function Scope
**File**: `src/ui/Expenses.py` line ~1187

**Added**:
```python
def show_account_settings():
    theme = get_theme()
    
    # Get user's default currency for fallback only
    user_profile = db.get_user_profile(state["user_id"])
    from utils.currency import get_currency_from_user_profile
    user_currency = get_currency_from_user_profile(user_profile)
```

---

## Testing & Verification

### Test Case 1: Account List Display
**Action**: Open Account Settings
**Expected**: Each account shows its own currency badge
**Result**: ✅ PASSED
- Cash shows "INR" badge
- Reyanaldo shows "KRW" badge
- roger shows "KRW" badge
- jehan shows "USD" badge
- LUIS shows "PHP" badge

### Test Case 2: Edit Account Currency
**Action**: 
1. Click on "Reyanaldo" account (currently KRW)
2. Scroll down to see Currency dropdown
3. Change from KRW to USD
4. Click "Save Changes"

**Expected**: Currency dropdown shows KRW selected, changes to USD after save
**Result**: ✅ PASSED

### Test Case 3: Currency Persistence
**Action**: 
1. Edit account and change currency
2. Close edit form
3. Reopen edit form for same account

**Expected**: New currency value is displayed in dropdown
**Result**: ✅ PASSED

---

## Lessons Learned

### 1. **Avoid Duplicate Functions**
- Having two `show_account_settings()` functions caused confusion
- One had the fix, but the wrong one was being called
- **Solution**: Use unique function names or consolidate functionality

### 2. **Variable Scope Awareness**
- Always ensure variables are defined before use
- Don't rely on parent scope for critical data
- **Solution**: Define all required variables at function start

### 3. **Database vs Display Logic**
- Database had correct data, but display logic was wrong
- Always verify database first before assuming data corruption
- **Solution**: Query database to confirm data integrity

### 4. **Form Completeness**
- Edit forms should have all fields that can be edited
- Missing currency field led to users being unable to update it
- **Solution**: Audit all edit forms for field completeness

### 5. **Testing Edge Cases**
- Test with different user default currencies
- Test accounts with NULL values
- **Solution**: Implement fallback logic for missing data

---

## Prevention Strategies

### 1. **Code Review Checklist**
- [ ] No duplicate function names
- [ ] All variables defined in scope
- [ ] Edit forms include all editable fields
- [ ] Display logic uses entity data, not user defaults
- [ ] Fallback values for NULL/missing data

### 2. **Testing Protocol**
- [ ] Test with multiple user profiles (different default currencies)
- [ ] Test with accounts having different currencies
- [ ] Test edit form field visibility and functionality
- [ ] Test save and reload to verify persistence

### 3. **Code Standards**
- Use clear variable names (`acc_currency` vs `user_currency`)
- Add comments for fallback logic
- Document which function is being used where
- Regular code consolidation to remove duplicates

---

## Related Issues

### Issue: Enhanced Account Settings UI
After fixing the currency bug, additional enhancements were made:
- Added currency badge with accent color next to account name
- Improved currency dropdown with full currency names (e.g., "₱ Philippine Peso (PHP)")
- Added "Currency Settings" section with visual dividers
- Added helper text: "Each account can have its own currency for multi-currency tracking"
- Enhanced edit form layout with better spacing and organization

**Reference**: See `PERSONAL_DETAILS_IMPROVEMENTS.md` for UI enhancement details

---

## Conclusion

This bug was caused by using outdated code in one of two duplicate functions. The fix required:
1. Using account-specific currency instead of user default
2. Adding currency dropdown to edit form
3. Defining user_currency in proper scope
4. Enhancing UI for better currency visibility

**Total Files Modified**: 1 (`src/ui/Expenses.py`)
**Lines Changed**: ~150 lines across multiple functions
**Testing Time**: 30 minutes
**Status**: ✅ RESOLVED

---

## Additional Notes

### User's Default Currency
The logged-in user (ID: 11) has **INR** set as default currency, which is why all accounts appeared to show INR when using `user_currency` variable.

### Database Schema
The `accounts` table has the following structure:
```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    account_number TEXT,
    type TEXT,
    balance REAL,
    currency TEXT NOT NULL DEFAULT 'PHP',  -- Each account has own currency
    color TEXT,
    is_primary INTEGER,
    created_at TEXT,
    status TEXT,
    sort_order INTEGER
);
```

The `currency` field with `DEFAULT 'PHP'` ensures all accounts have a currency value.

---

**Report Generated**: December 8, 2025
**Last Updated**: December 8, 2025
**Reporter**: Development Team
**Status**: CLOSED - FIXED
