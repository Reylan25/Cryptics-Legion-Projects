"""
Currency Exchange Rate API Integration
Fetches live exchange rates and handles currency conversions
"""

import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

# API Configuration
# Using exchangerate-api.com (free tier: 1,500 requests/month)
API_BASE_URL = "https://api.exchangerate-api.com/v4/latest"
BACKUP_API_URL = "https://open.er-api.com/v6/latest"  # Backup API

# Cache configuration
CACHE_DURATION_HOURS = 6  # Update rates every 6 hours
CACHE_FILE = Path(__file__).parent.parent / "storage" / "data" / "exchange_rates_cache.json"

# Supported currencies in the app
SUPPORTED_CURRENCIES = ["PHP", "USD", "EUR", "GBP", "JPY", "KRW", "SGD", "AUD", "CAD", "INR"]
BASE_CURRENCY = "USD"  # Use USD as base for all conversions


class CurrencyExchangeAPI:
    """Handles currency exchange rate fetching and caching."""
    
    def __init__(self):
        self.cache_file = CACHE_FILE
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_cache(self) -> Optional[Dict]:
        """Load cached exchange rates if valid."""
        try:
            if not self.cache_file.exists():
                return None
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
            if datetime.now() - cached_time < timedelta(hours=CACHE_DURATION_HOURS):
                return cache_data.get('rates', {})
            
        except (json.JSONDecodeError, ValueError, OSError):
            pass
        
        return None
    
    def _save_cache(self, rates: Dict):
        """Save exchange rates to cache."""
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'base': BASE_CURRENCY,
                'rates': rates
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        
        except OSError as e:
            print(f"Warning: Could not save exchange rate cache: {e}")
    
    def _fetch_from_api(self, base: str = BASE_CURRENCY) -> Optional[Dict]:
        """Fetch exchange rates from API."""
        try:
            # Try primary API
            response = requests.get(f"{API_BASE_URL}/{base}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('rates', {})
        
        except requests.RequestException:
            # Try backup API
            try:
                response = requests.get(f"{BACKUP_API_URL}/{base}", timeout=5)
                response.raise_for_status()
                data = response.json()
                return data.get('rates', {})
            except requests.RequestException as e:
                print(f"Error fetching exchange rates: {e}")
                return None
    
    def get_exchange_rates(self, base: str = BASE_CURRENCY, force_refresh: bool = False) -> Dict:
        """
        Get exchange rates for all supported currencies.
        
        Args:
            base: Base currency code (default: USD)
            force_refresh: Force fetch from API even if cache is valid
        
        Returns:
            dict: Exchange rates with currency codes as keys
        """
        # Try cache first
        if not force_refresh:
            cached_rates = self._load_cache()
            if cached_rates:
                return cached_rates
        
        # Fetch from API
        rates = self._fetch_from_api(base)
        
        if rates:
            # Filter to only supported currencies
            filtered_rates = {code: rate for code, rate in rates.items() 
                            if code in SUPPORTED_CURRENCIES}
            # Add base currency
            filtered_rates[base] = 1.0
            
            self._save_cache(filtered_rates)
            return filtered_rates
        
        # If API fails, try to return cached data even if expired
        cached_rates = self._load_cache()
        if cached_rates:
            print("Warning: Using expired exchange rate cache")
            return cached_rates
        
        # Last resort: return default rates (1:1)
        print("Warning: Using default exchange rates (1:1)")
        return {code: 1.0 for code in SUPPORTED_CURRENCIES}
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another.
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
        
        Returns:
            float: Converted amount
        """
        if from_currency == to_currency:
            return amount
        
        rates = self.get_exchange_rates()
        
        # Convert to USD first (base currency), then to target
        if from_currency != BASE_CURRENCY:
            # Convert from_currency to USD
            from_rate = rates.get(from_currency, 1.0)
            amount_in_usd = amount / from_rate
        else:
            amount_in_usd = amount
        
        # Convert USD to target currency
        to_rate = rates.get(to_currency, 1.0)
        converted_amount = amount_in_usd * to_rate
        
        return round(converted_amount, 2)
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate between two currencies.
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
        
        Returns:
            float: Exchange rate (1 from_currency = X to_currency)
        """
        if from_currency == to_currency:
            return 1.0
        
        rates = self.get_exchange_rates()
        
        from_rate = rates.get(from_currency, 1.0)
        to_rate = rates.get(to_currency, 1.0)
        
        # Calculate direct exchange rate
        exchange_rate = to_rate / from_rate
        
        return round(exchange_rate, 4)
    
    def get_cache_age(self) -> Optional[str]:
        """Get the age of cached data in human-readable format."""
        try:
            if not self.cache_file.exists():
                return None
            
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
            age = datetime.now() - cached_time
            
            if age.total_seconds() < 60:
                return "Just now"
            elif age.total_seconds() < 3600:
                minutes = int(age.total_seconds() / 60)
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            elif age.total_seconds() < 86400:
                hours = int(age.total_seconds() / 3600)
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                days = int(age.total_seconds() / 86400)
                return f"{days} day{'s' if days > 1 else ''} ago"
        
        except (json.JSONDecodeError, ValueError, OSError):
            return None
    
    def get_all_rates_formatted(self, base_currency: str = "USD") -> Dict[str, Tuple[float, str]]:
        """
        Get all exchange rates with formatted display.
        
        Args:
            base_currency: Base currency for comparison
        
        Returns:
            dict: {currency_code: (rate, formatted_string)}
        """
        rates = self.get_exchange_rates()
        formatted_rates = {}
        
        for code in SUPPORTED_CURRENCIES:
            if code == base_currency:
                formatted_rates[code] = (1.0, f"1.00 {code}")
            else:
                rate = self.get_exchange_rate(base_currency, code)
                formatted_rates[code] = (rate, f"{rate:.4f} {code}")
        
        return formatted_rates


# Global instance
_exchange_api = None

def get_exchange_api() -> CurrencyExchangeAPI:
    """Get global exchange API instance."""
    global _exchange_api
    if _exchange_api is None:
        _exchange_api = CurrencyExchangeAPI()
    return _exchange_api


# Convenience functions
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency amount."""
    api = get_exchange_api()
    return api.convert_currency(amount, from_currency, to_currency)


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate between two currencies."""
    api = get_exchange_api()
    return api.get_exchange_rate(from_currency, to_currency)


def get_all_rates(base_currency: str = "USD") -> Dict[str, float]:
    """Get all exchange rates for supported currencies."""
    api = get_exchange_api()
    rates = api.get_exchange_rates()
    
    # Convert all rates to be relative to base_currency
    result = {}
    for code in SUPPORTED_CURRENCIES:
        if code == base_currency:
            result[code] = 1.0
        else:
            result[code] = api.get_exchange_rate(base_currency, code)
    
    return result


def refresh_rates() -> bool:
    """Force refresh exchange rates from API."""
    api = get_exchange_api()
    rates = api.get_exchange_rates(force_refresh=True)
    return len(rates) > 0


def get_last_update_time() -> Optional[str]:
    """Get when exchange rates were last updated."""
    api = get_exchange_api()
    return api.get_cache_age()
