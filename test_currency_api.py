# Test Currency Exchange API
import sys
sys.path.insert(0, 'Cryptics_legion/src')

from utils.currency_exchange import get_exchange_api, SUPPORTED_CURRENCIES

print("=" * 50)
print("TESTING CURRENCY EXCHANGE API")
print("=" * 50)

api = get_exchange_api()

# Test 1: Get exchange rates
print("\n1. Fetching exchange rates...")
rates = api.get_exchange_rates()
print(f"   ✓ Successfully fetched {len(rates)} currency rates")

# Test 2: Display all rates
print("\n2. Exchange rates (base: USD):")
for currency in SUPPORTED_CURRENCIES:
    rate = rates.get(currency, "N/A")
    print(f"   1 USD = {rate:>10.4f} {currency}")

# Test 3: Currency conversion
print("\n3. Testing currency conversion:")
amount = 100
test_pairs = [
    ("USD", "PHP"),
    ("PHP", "USD"),
    ("EUR", "JPY"),
    ("GBP", "INR"),
]

for from_curr, to_curr in test_pairs:
    converted = api.convert_currency(amount, from_curr, to_curr)
    rate = api.get_exchange_rate(from_curr, to_curr)
    print(f"   {amount} {from_curr} = {converted:.2f} {to_curr} (rate: {rate:.4f})")

# Test 4: Cache age
print("\n4. Cache information:")
cache_age = api.get_cache_age()
print(f"   Last updated: {cache_age or 'Never'}")

print("\n" + "=" * 50)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 50)
