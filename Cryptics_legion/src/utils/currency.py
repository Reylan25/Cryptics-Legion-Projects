"""
Currency Management Module
Handles currency formatting, conversion, and display across the app
"""

# Currency symbols and configurations
CURRENCY_CONFIGS = {
    "PHP": {
        "symbol": "₱",
        "name": "Philippine Peso",
        "decimal_places": 2,
        "symbol_position": "before",  # Symbol before amount
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "USD": {
        "symbol": "$",
        "name": "US Dollar",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "EUR": {
        "symbol": "€",
        "name": "Euro",
        "decimal_places": 2,
        "symbol_position": "after",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "GBP": {
        "symbol": "£",
        "name": "British Pound",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "JPY": {
        "symbol": "¥",
        "name": "Japanese Yen",
        "decimal_places": 0,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "KRW": {
        "symbol": "₩",
        "name": "Korean Won",
        "decimal_places": 0,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "SGD": {
        "symbol": "S$",
        "name": "Singapore Dollar",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "AUD": {
        "symbol": "A$",
        "name": "Australian Dollar",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "CAD": {
        "symbol": "C$",
        "name": "Canadian Dollar",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
    "INR": {
        "symbol": "₹",
        "name": "Indian Rupee",
        "decimal_places": 2,
        "symbol_position": "before",
        "thousands_separator": ",",
        "decimal_separator": ".",
    },
}

DEFAULT_CURRENCY = "PHP"

# List of currencies for dropdown selection
CURRENCY_LIST = [
    {"code": "PHP", "name": "Philippine Peso", "symbol": "₱"},
    {"code": "USD", "name": "US Dollar", "symbol": "$"},
    {"code": "EUR", "name": "Euro", "symbol": "€"},
    {"code": "GBP", "name": "British Pound", "symbol": "£"},
    {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
    {"code": "KRW", "name": "Korean Won", "symbol": "₩"},
    {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$"},
    {"code": "AUD", "name": "Australian Dollar", "symbol": "A$"},
    {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$"},
    {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
]


def get_currency_config(currency_code: str = None) -> dict:
    """
    Get currency configuration.
    
    Args:
        currency_code: Currency code (e.g., 'PHP', 'USD'). Uses DEFAULT_CURRENCY if None.
    
    Returns:
        dict: Currency configuration
    """
    if currency_code is None:
        currency_code = DEFAULT_CURRENCY
    
    # Extract currency code if it includes description (e.g., "PHP - Philippine Peso")
    if " - " in currency_code:
        currency_code = currency_code.split(" - ")[0].strip()
    
    return CURRENCY_CONFIGS.get(currency_code.upper(), CURRENCY_CONFIGS[DEFAULT_CURRENCY])


def format_currency(amount: float, currency_code: str = None, include_symbol: bool = True) -> str:
    """
    Format amount as currency string with proper symbol placement and decimal places.
    
    Args:
        amount: Numeric amount to format
        currency_code: Currency code (e.g., 'PHP', 'USD'). Uses user preference if None.
        include_symbol: Whether to include currency symbol
    
    Returns:
        str: Formatted currency string (e.g., "₱1,234.56" or "1,234.56 EUR")
    """
    config = get_currency_config(currency_code)
    decimal_places = config["decimal_places"]
    thousands_sep = config["thousands_separator"]
    decimal_sep = config["decimal_separator"]
    symbol = config["symbol"] if include_symbol else ""
    
    # Format the amount
    if decimal_places == 0:
        formatted_amount = f"{int(amount):,}".replace(",", thousands_sep)
    else:
        formatted_amount = f"{amount:,.{decimal_places}f}".replace(",", thousands_sep).replace(".", decimal_sep)
    
    # Place symbol based on configuration
    if include_symbol:
        if config["symbol_position"] == "before":
            return f"{symbol}{formatted_amount}"
        else:  # after
            return f"{formatted_amount} {symbol}"
    else:
        return formatted_amount


def format_currency_short(amount: float, currency_code: str = None) -> str:
    """
    Format currency in short form (e.g., "₱1.2K", "₱50M").
    
    Args:
        amount: Numeric amount
        currency_code: Currency code
    
    Returns:
        str: Shortened currency format
    """
    config = get_currency_config(currency_code)
    symbol = config["symbol"]
    
    if amount >= 1_000_000:
        return f"{symbol}{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{symbol}{amount / 1_000:.1f}K"
    else:
        return format_currency(amount, currency_code)


def get_currency_symbol(currency_code: str = None) -> str:
    """Get the currency symbol for a currency code."""
    config = get_currency_config(currency_code)
    return config["symbol"]


def get_currency_name(currency_code: str = None) -> str:
    """Get the full currency name."""
    config = get_currency_config(currency_code)
    return config["name"]


def parse_currency_string(currency_str: str) -> str:
    """
    Parse currency selection string and return currency code.
    
    Args:
        currency_str: String like "PHP - Philippine Peso" or "PHP"
    
    Returns:
        str: Currency code (e.g., "PHP")
    """
    if " - " in currency_str:
        return currency_str.split(" - ")[0].strip()
    return currency_str.strip().upper()


def get_currency_options() -> list:
    """Get list of formatted currency options for dropdown."""
    return [f"{code} - {config['name']}" for code, config in CURRENCY_CONFIGS.items()]


def format_currency_with_context(amount: float, user_currency: str = None, 
                                  prefix: str = "", suffix: str = "") -> str:
    """
    Format currency with optional prefix/suffix for context.
    
    Args:
        amount: Amount to format
        user_currency: User's preferred currency
        prefix: Prefix text (e.g., "Spent: ")
        suffix: Suffix text (e.g., " this month")
    
    Returns:
        str: Formatted string with context
    """
    formatted = format_currency(amount, user_currency)
    result = formatted
    if prefix:
        result = f"{prefix}{result}"
    if suffix:
        result = f"{result}{suffix}"
    return result


def get_currency_from_user_profile(profile: dict) -> str:
    """
    Extract currency from user profile dictionary.
    
    Args:
        profile: User profile dict with 'currency' key
    
    Returns:
        str: Currency code (defaults to PHP)
    """
    if not profile:
        return DEFAULT_CURRENCY
    
    currency = profile.get("currency", DEFAULT_CURRENCY)
    return parse_currency_string(currency)
