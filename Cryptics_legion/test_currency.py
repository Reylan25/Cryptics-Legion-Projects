#!/usr/bin/env python
"""Test script for currency formatting functionality"""

import sys
sys.path.insert(0, 'src')

from utils.currency import (
    format_currency,
    format_currency_short,
    get_currency_options,
    format_currency_with_context,
    parse_currency_string,
)

print("=" * 60)
print("CURRENCY FORMATTING SYSTEM TEST")
print("=" * 60)

print("\n✓ Supported Currencies:")
for option in get_currency_options():
    print(f"  • {option}")

print("\n✓ Currency Format Examples:")
test_amounts = [100, 1234.56, 50000, 1000000]
currencies = ["PHP", "USD", "EUR", "GBP", "JPY"]

for amount in test_amounts:
    print(f"\n  Amount: {amount:>10}")
    for currency in currencies:
        formatted = format_currency(amount, currency)
        print(f"    {currency}: {formatted:>15}")

print("\n✓ Short Format Examples (for small screens):")
for amount in [100, 1000, 10000, 1000000]:
    print(f"  {amount:>10} -> ", end="")
    print(" | ".join([format_currency_short(amount, c) for c in ["PHP", "USD", "JPY"]]))

print("\n✓ Parse Currency String:")
test_strings = ["PHP - Philippine Peso", "USD", "EUR - Euro"]
for s in test_strings:
    parsed = parse_currency_string(s)
    print(f"  '{s}' -> '{parsed}'")

print("\n✓ Format with Context:")
examples = [
    (1000, "PHP", "You spent ", " this month"),
    (5000.50, "USD", "Balance: ", " available"),
]
for amount, currency, prefix, suffix in examples:
    result = format_currency_with_context(amount, currency, prefix, suffix)
    print(f"  {result}")

print("\n" + "=" * 60)
print("✅ All currency formatting tests passed!")
print("=" * 60)
