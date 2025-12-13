# Live Currency Exchange Rates - Feature Documentation

## Overview
The Smart Expense Tracker now includes **live currency exchange rate integration** that automatically fetches real-time exchange rates from online APIs and caches them for offline use.

## Features

### 1. **Live Exchange Rates**
- Fetches real-time exchange rates from reliable APIs
- Supports 10 major currencies: PHP, USD, EUR, GBP, JPY, KRW, SGD, AUD, CAD, INR
- Updates rates every 6 hours automatically
- Caches rates locally for offline access

### 2. **Currency Conversion**
- Convert any amount between supported currencies
- Accurate calculations using live market rates
- Instant conversion in the UI

### 3. **Exchange Rates Viewer**
- Dedicated page to view all exchange rates
- Interactive currency converter
- Shows last update time
- Manual refresh option

### 4. **Multi-Currency Support**
- Track expenses in different currencies
- Automatic conversion when viewing totals
- Display original and converted amounts

## How It Works

### API Integration
The system uses two free exchange rate APIs:
1. **Primary**: exchangerate-api.com (1,500 requests/month free)
2. **Backup**: open.er-api.com (fallback if primary fails)

### Caching Strategy
- Exchange rates are cached locally for 6 hours
- Reduces API calls and provides offline functionality
- Auto-refreshes when cache expires
- Cache file: `storage/data/exchange_rates_cache.json`

### Conversion Logic
1. All currencies convert through USD as base currency
2. Formula: `amount_in_usd = amount / from_rate`
3. Then: `converted = amount_in_usd * to_rate`
4. Results rounded to 2 decimal places

## Installation

### 1. Install Required Package
```bash
# Activate virtual environment
cd Cryptics-Legion-Projects
.\env_Cryptics\Scripts\Activate.ps1

# Install requests library
pip install requests
```

### 2. Test the API
```bash
python test_currency_api.py
```

Expected output:
```
==================================================
TESTING CURRENCY EXCHANGE API
==================================================

1. Fetching exchange rates...
   ✓ Successfully fetched 10 currency rates

2. Exchange rates (base: USD):
   1 USD =    56.5000 PHP
   1 USD =     0.9200 EUR
   1 USD =     0.7800 GBP
   ...

3. Testing currency conversion:
   100 USD = 5650.00 PHP (rate: 56.5000)
   100 PHP = 1.77 USD (rate: 0.0177)
   ...

4. Cache information:
   Last updated: Just now

==================================================
ALL TESTS COMPLETED SUCCESSFULLY!
==================================================
```

## Usage in Code

### Basic Conversion
```python
from utils.currency import convert_amount

# Convert 100 USD to PHP
php_amount = convert_amount(100, "USD", "PHP")
print(f"100 USD = {php_amount} PHP")
```

### Get Exchange Rate
```python
from utils.currency import get_live_exchange_rate

# Get current USD to PHP rate
rate = get_live_exchange_rate("USD", "PHP")
print(f"1 USD = {rate} PHP")
```

### Format with Conversion
```python
from utils.currency import format_currency_with_conversion

# Show amount in both currencies
formatted = format_currency_with_conversion(100, "USD", "PHP", show_original=True)
print(formatted)  # "₱5,650.00 ($100.00)"
```

### Refresh Rates Manually
```python
from utils.currency_exchange import refresh_rates

success = refresh_rates()
if success:
    print("Rates updated!")
```

## API Functions

### Currency Exchange Module (`utils/currency_exchange.py`)

#### `convert_currency(amount, from_currency, to_currency)`
Convert amount between currencies.

#### `get_exchange_rate(from_currency, to_currency)`
Get exchange rate between two currencies.

#### `get_all_rates(base_currency="USD")`
Get all exchange rates relative to base currency.

#### `refresh_rates()`
Force refresh exchange rates from API.

#### `get_last_update_time()`
Get when rates were last updated.

### Currency Module (`utils/currency.py`)

#### `convert_amount(amount, from_currency, to_currency)`
Wrapper for currency conversion.

#### `get_live_exchange_rate(from_currency, to_currency)`
Get live exchange rate.

#### `format_currency_with_conversion(amount, original_currency, target_currency, show_original=True)`
Format currency with optional conversion display.

## User Interface

### Accessing Exchange Rates Page
The exchange rates viewer can be accessed from:
1. **Profile page** → Settings menu
2. **Wallet page** → Currency info button
3. Direct navigation in main.py

### Page Features
- **Base Currency Selector**: Choose which currency to compare against
- **Exchange Rates List**: View all conversion rates
- **Currency Converter**: 
  - Enter amount
  - Select from/to currencies
  - Click "Convert" button
  - View result with exchange rate
- **Refresh Button**: Manually update rates
- **Last Update Time**: Shows cache age

## Error Handling

### No Internet Connection
- System uses cached rates (up to 6 hours old)
- Shows warning: "Using expired exchange rate cache"
- Continues to function normally

### API Failure
- Automatically tries backup API
- Falls back to cached data if both fail
- Shows user-friendly error messages

### Invalid Currency
- Returns 1:1 rate as fallback
- Logs warning for debugging
- Prevents app crashes

## Configuration

### Supported Currencies
Edit `SUPPORTED_CURRENCIES` in `utils/currency_exchange.py`:
```python
SUPPORTED_CURRENCIES = ["PHP", "USD", "EUR", "GBP", "JPY", "KRW", "SGD", "AUD", "CAD", "INR"]
```

### Cache Duration
Change `CACHE_DURATION_HOURS` in `utils/currency_exchange.py`:
```python
CACHE_DURATION_HOURS = 6  # Update rates every 6 hours
```

### Base Currency
Change `BASE_CURRENCY` in `utils/currency_exchange.py`:
```python
BASE_CURRENCY = "USD"  # Use USD as base for all conversions
```

## Limitations

### Free API Tier
- 1,500 requests per month
- No authentication required
- Rate limited to prevent abuse

### Update Frequency
- Rates update every 6 hours by default
- Can be manually refreshed
- Real-time updates not available (not needed for expense tracking)

### Supported Currencies
- Limited to 10 currencies
- Can be expanded by editing configuration
- API supports 150+ currencies

## Future Enhancements

1. **Historical Rates**: Track exchange rate changes over time
2. **Rate Alerts**: Notify when rate reaches target
3. **Custom Base Currency**: Set user preference for base currency
4. **Offline Mode**: Extended cache for longer offline periods
5. **Rate Charts**: Visualize exchange rate trends
6. **Multi-Currency Reports**: Generate reports showing expenses in multiple currencies

## Troubleshooting

### "Failed to fetch rates"
- Check internet connection
- Verify API is not down (try test script)
- System will use cached data automatically

### "Using expired cache"
- No internet connection for > 6 hours
- Rates may be outdated but still functional
- Refresh when connection available

### "Module 'requests' not found"
```bash
pip install requests
```

### Cache file errors
- Check write permissions in `storage/data/` folder
- Verify folder exists
- Delete cache file and restart app

## Security & Privacy

- No API keys required (uses free tier)
- No user data sent to external APIs
- Only currency codes transmitted
- Cache stored locally only
- No tracking or analytics

## Performance

- **First load**: ~1-2 seconds (API fetch)
- **Cached load**: Instant
- **Conversion**: < 1ms
- **Memory**: ~50KB cache file
- **Network**: ~5KB per API request

---

## Support

For issues or questions:
1. Check console logs for errors
2. Run test script: `python test_currency_api.py`
3. Verify internet connection
4. Check `storage/data/exchange_rates_cache.json` exists
5. Review error messages in UI

---

**Version**: 1.0.0  
**Last Updated**: December 8, 2025  
**API Provider**: exchangerate-api.com & open.er-api.com
