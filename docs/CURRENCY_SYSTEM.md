# Currency Management System - Implementation Guide

## Overview

A comprehensive currency formatting and management system for the Cryptics Legion expense tracker application that supports multiple currencies with proper formatting, symbol placement, and localization.

## Supported Currencies

| Code | Name | Symbol | Position | Decimals |
|------|------|--------|----------|----------|
| PHP | Philippine Peso | ₱ | Before | 2 |
| USD | US Dollar | $ | Before | 2 |
| EUR | Euro | € | After | 2 |
| GBP | British Pound | £ | Before | 2 |
| JPY | Japanese Yen | ¥ | Before | 0 |
| KRW | Korean Won | ₩ | Before | 0 |
| SGD | Singapore Dollar | S$ | Before | 2 |
| AUD | Australian Dollar | A$ | Before | 2 |
| CAD | Canadian Dollar | C$ | Before | 2 |
| INR | Indian Rupee | ₹ | Before | 2 |

## Core Functions

### `format_currency(amount, currency_code=None, include_symbol=True)`

Formats an amount as a properly formatted currency string.

**Parameters:**
- `amount` (float): The numeric amount to format
- `currency_code` (str, optional): Currency code (e.g., 'PHP', 'USD'). Uses default if None
- `include_symbol` (bool): Whether to include the currency symbol

**Returns:** Formatted string (e.g., "₱1,234.56")

**Examples:**
```python
from utils.currency import format_currency

format_currency(1234.56, 'PHP')      # ₱1,234.56
format_currency(1234.56, 'USD')      # $1,234.56
format_currency(1234.56, 'EUR')      # 1,234.56 €
format_currency(100000, 'JPY')       # ¥100,000
```

### `format_currency_short(amount, currency_code=None)`

Formats currency in abbreviated form for compact displays.

**Returns:** Shortened format (e.g., "₱1.2K", "₱50M")

**Examples:**
```python
from utils.currency import format_currency_short

format_currency_short(1000, 'PHP')       # ₱1.0K
format_currency_short(1000000, 'USD')   # $1.0M
```

### `get_currency_symbol(currency_code=None)`

Gets the currency symbol for a code.

**Returns:** Currency symbol string

```python
get_currency_symbol('PHP')  # ₱
get_currency_symbol('USD')  # $
get_currency_symbol('EUR')  # €
```

### `get_currency_name(currency_code=None)`

Gets the full name of a currency.

**Returns:** Currency name string

```python
get_currency_name('PHP')  # Philippine Peso
get_currency_name('USD')  # US Dollar
```

### `parse_currency_string(currency_str)`

Parses currency selection strings and extracts the currency code.

**Parameters:**
- `currency_str` (str): String like "PHP - Philippine Peso" or "PHP"

**Returns:** Currency code (e.g., "PHP")

```python
parse_currency_string("PHP - Philippine Peso")  # PHP
parse_currency_string("USD")                    # USD
```

### `get_currency_options()`

Gets list of formatted currency options for dropdown menus.

**Returns:** List of formatted currency option strings

```python
get_currency_options()
# ['PHP - Philippine Peso', 'USD - US Dollar', 'EUR - Euro', ...]
```

### `get_currency_from_user_profile(profile)`

Extracts and returns currency from user profile dictionary.

**Parameters:**
- `profile` (dict): User profile dict with 'currency' key

**Returns:** Currency code (defaults to 'PHP')

```python
user_profile = db.get_user_profile(user_id)
currency = get_currency_from_user_profile(user_profile)
```

### `format_currency_with_context(amount, user_currency=None, prefix="", suffix="")`

Formats currency with optional prefix/suffix for contextual display.

**Returns:** Formatted string with context

```python
format_currency_with_context(1000, 'PHP', 'You spent ', ' this month')
# You spent ₱1,000.00 this month

format_currency_with_context(5000, 'USD', 'Balance: ', ' available')
# Balance: $5,000.00 available
```

## Integration Examples

### In Flet UI Components

```python
from utils.currency import format_currency, get_currency_from_user_profile
from core import db

# Get user's preferred currency
user_profile = db.get_user_profile(user_id)
user_currency = get_currency_from_user_profile(user_profile)

# Use in text displays
ft.Text(format_currency(1234.56, user_currency), size=18, weight=ft.FontWeight.BOLD)

# Use in tooltips
tooltip=f"Spent: {format_currency(amount, user_currency)}"

# Use in summary cards
ft.Text(f"Total: {format_currency(total, user_currency)}")
```

### In Statistics Pages

```python
from utils.statistics import get_statistics_summary
from utils.currency import format_currency, get_currency_from_user_profile

stats = get_statistics_summary(user_id, period)
user_currency = get_currency_from_user_profile(user_profile)

# Display formatted statistics
total_text = format_currency(stats['total_spent'], user_currency)
```

### Dropdown Selection

```python
from utils.currency import get_currency_options, parse_currency_string

# In dropdown
ft.Dropdown(
    options=[ft.dropdown.Option(opt) for opt in get_currency_options()],
    value="PHP - Philippine Peso",
    on_change=lambda e: handle_currency_change(parse_currency_string(e.control.value))
)
```

## Updated Files

The following files have been updated to use proper currency formatting:

1. **utils/currency.py** - New module with all currency functions
2. **utils/__init__.py** - Exports currency utilities
3. **ui/statistics_page.py** - Uses format_currency for all displays
4. **ui/wallet_page.py** - Uses format_currency for budget displays
5. **ui/profile_page.py** - Uses format_currency for statistics
6. **ui/all_expenses_page.py** - Uses format_currency for transaction displays

## Migration Path

When adding currency formatting to a new page:

1. **Import the utilities:**
```python
from utils.currency import format_currency, get_currency_from_user_profile
```

2. **Get user currency in function/view:**
```python
user_profile = db.get_user_profile(user_id)
user_currency = get_currency_from_user_profile(user_profile)
```

3. **Replace hardcoded ₱ symbols:**
```python
# Before:
ft.Text(f"₱{amount:,.2f}")

# After:
ft.Text(format_currency(amount, user_currency))
```

4. **For optional context:**
```python
text = format_currency_with_context(
    amount, 
    user_currency, 
    prefix="Total: ",
    suffix=" this month"
)
```

## Configuration

Default currency can be changed in `utils/currency.py`:

```python
DEFAULT_CURRENCY = "PHP"  # Change this to preferred default
```

Add new currencies by extending `CURRENCY_CONFIGS` dictionary:

```python
CURRENCY_CONFIGS = {
    "MYR": {
        "symbol": "RM",
        "name": "Malaysian Ringgit",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    # ... other currencies
}
```

## Testing

Run the test script to verify all currency functions:

```bash
python test_currency.py
```

Expected output shows:
- All supported currencies listed
- Proper formatting for various amounts
- Correct symbol placement by locale
- Proper decimal place handling
- Context formatting working correctly

## Notes

- **Symbol Positioning**: Handled automatically per currency locale (e.g., € after amount, $ before)
- **Decimal Places**: JPY and KRW use 0 decimal places; others use 2
- **Thousands Separator**: Consistent comma formatting across all currencies
- **User Preference**: Always retrieves from user profile to respect their selection
- **Graceful Fallback**: Defaults to PHP if currency code not found

## Future Enhancements

Potential additions:
- Real-time exchange rates (optional)
- Currency conversion utilities
- Historical exchange rate tracking
- Multi-currency account support
- Currency-specific formatting rules (some locales use space as thousands separator)
