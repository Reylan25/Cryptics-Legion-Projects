# src/utils/brand_recognition.py
"""
AI-like brand and category recognition for expense tracking.
Identifies brands, stores, and services to auto-categorize expenses with appropriate icons.
"""

import flet as ft

# Brand database with categories and icons
BRAND_DATABASE = {
    # Fashion & Apparel Brands
    "nike": {"category": "Fashion & Apparel", "icon": ft.Icons.SPORTS_BASKETBALL, "color": "#FF6B35"},
    "adidas": {"category": "Fashion & Apparel", "icon": ft.Icons.SPORTS_SOCCER, "color": "#000000"},
    "puma": {"category": "Fashion & Apparel", "icon": ft.Icons.SPORTS_HANDBALL, "color": "#E31937"},
    "reebok": {"category": "Fashion & Apparel", "icon": ft.Icons.SPORTS_GYMNASTICS, "color": "#CC0000"},
    "under armour": {"category": "Fashion & Apparel", "icon": ft.Icons.FITNESS_CENTER, "color": "#1D1D1D"},
    "uniqlo": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#FF0000"},
    "zara": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#000000"},
    "h&m": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#E50010"},
    "gucci": {"category": "Fashion & Apparel", "icon": ft.Icons.DIAMOND, "color": "#1B4D3E"},
    "louis vuitton": {"category": "Fashion & Apparel", "icon": ft.Icons.DIAMOND, "color": "#8B6914"},
    "lv": {"category": "Fashion & Apparel", "icon": ft.Icons.DIAMOND, "color": "#8B6914"},
    "chanel": {"category": "Fashion & Apparel", "icon": ft.Icons.DIAMOND, "color": "#000000"},
    "prada": {"category": "Fashion & Apparel", "icon": ft.Icons.DIAMOND, "color": "#000000"},
    "gap": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#1E3A5F"},
    "levis": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#C41230"},
    "levi's": {"category": "Fashion & Apparel", "icon": ft.Icons.CHECKROOM, "color": "#C41230"},
    "converse": {"category": "Fashion & Apparel", "icon": ft.Icons.SNOWSHOEING, "color": "#000000"},
    "vans": {"category": "Fashion & Apparel", "icon": ft.Icons.SKATEBOARDING, "color": "#C41230"},
    "new balance": {"category": "Fashion & Apparel", "icon": ft.Icons.DIRECTIONS_RUN, "color": "#CF0A2C"},
    "skechers": {"category": "Fashion & Apparel", "icon": ft.Icons.DIRECTIONS_WALK, "color": "#0033A0"},
    "crocs": {"category": "Fashion & Apparel", "icon": ft.Icons.SNOWSHOEING, "color": "#00A651"},
    
    # Electronics & Tech
    "apple": {"category": "Electronics", "icon": ft.Icons.PHONE_IPHONE, "color": "#A2AAAD"},
    "iphone": {"category": "Electronics", "icon": ft.Icons.PHONE_IPHONE, "color": "#A2AAAD"},
    "ipad": {"category": "Electronics", "icon": ft.Icons.TABLET_MAC, "color": "#A2AAAD"},
    "macbook": {"category": "Electronics", "icon": ft.Icons.LAPTOP_MAC, "color": "#A2AAAD"},
    "airpods": {"category": "Electronics", "icon": ft.Icons.HEADPHONES, "color": "#A2AAAD"},
    "samsung": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#1428A0"},
    "galaxy": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#1428A0"},
    "sony": {"category": "Electronics", "icon": ft.Icons.TV, "color": "#000000"},
    "playstation": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#003791"},
    "ps5": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#003791"},
    "xbox": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#107C10"},
    "nintendo": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#E60012"},
    "switch": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#E60012"},
    "dell": {"category": "Electronics", "icon": ft.Icons.COMPUTER, "color": "#007DB8"},
    "hp": {"category": "Electronics", "icon": ft.Icons.COMPUTER, "color": "#0096D6"},
    "lenovo": {"category": "Electronics", "icon": ft.Icons.COMPUTER, "color": "#E2231A"},
    "asus": {"category": "Electronics", "icon": ft.Icons.COMPUTER, "color": "#000000"},
    "acer": {"category": "Electronics", "icon": ft.Icons.COMPUTER, "color": "#83B81A"},
    "microsoft": {"category": "Electronics", "icon": ft.Icons.WINDOW, "color": "#00A4EF"},
    "google": {"category": "Electronics", "icon": ft.Icons.SEARCH, "color": "#4285F4"},
    "pixel": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#4285F4"},
    "huawei": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#FF0000"},
    "xiaomi": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#FF6900"},
    "oppo": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#1BA784"},
    "vivo": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#415FFF"},
    "realme": {"category": "Electronics", "icon": ft.Icons.SMARTPHONE, "color": "#F5C700"},
    "jbl": {"category": "Electronics", "icon": ft.Icons.SPEAKER, "color": "#FF6600"},
    "bose": {"category": "Electronics", "icon": ft.Icons.HEADPHONES, "color": "#000000"},
    "beats": {"category": "Electronics", "icon": ft.Icons.HEADPHONES, "color": "#E31937"},
    "logitech": {"category": "Electronics", "icon": ft.Icons.MOUSE, "color": "#00B8FC"},
    "razer": {"category": "Electronics", "icon": ft.Icons.GAMEPAD, "color": "#44D62C"},
    "gopro": {"category": "Electronics", "icon": ft.Icons.VIDEOCAM, "color": "#00A0D6"},
    "canon": {"category": "Electronics", "icon": ft.Icons.CAMERA_ALT, "color": "#BC0024"},
    "nikon": {"category": "Electronics", "icon": ft.Icons.CAMERA_ALT, "color": "#F6CE13"},
    "fujifilm": {"category": "Electronics", "icon": ft.Icons.CAMERA_ALT, "color": "#ED1A3A"},
    
    # Food & Restaurants
    "mcdonalds": {"category": "Food & Dining", "icon": ft.Icons.FASTFOOD, "color": "#FFC72C"},
    "mcdonald's": {"category": "Food & Dining", "icon": ft.Icons.FASTFOOD, "color": "#FFC72C"},
    "mcd": {"category": "Food & Dining", "icon": ft.Icons.FASTFOOD, "color": "#FFC72C"},
    "burger king": {"category": "Food & Dining", "icon": ft.Icons.LUNCH_DINING, "color": "#FF8732"},
    "bk": {"category": "Food & Dining", "icon": ft.Icons.LUNCH_DINING, "color": "#FF8732"},
    "kfc": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#F40027"},
    "wendys": {"category": "Food & Dining", "icon": ft.Icons.FASTFOOD, "color": "#E2164B"},
    "wendy's": {"category": "Food & Dining", "icon": ft.Icons.FASTFOOD, "color": "#E2164B"},
    "subway": {"category": "Food & Dining", "icon": ft.Icons.BAKERY_DINING, "color": "#00953A"},
    "pizza hut": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#EE3A43"},
    "dominos": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#0078AE"},
    "domino's": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#0078AE"},
    "papa johns": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#008145"},
    "starbucks": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#00704A"},
    "dunkin": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#FF671F"},
    "dunkin donuts": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#FF671F"},
    "krispy kreme": {"category": "Food & Dining", "icon": ft.Icons.DONUT_LARGE, "color": "#00873C"},
    "tim hortons": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#C8102E"},
    "taco bell": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#702082"},
    "chipotle": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#441500"},
    "chick-fil-a": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#E51636"},
    "popeyes": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#FF6700"},
    "jollibee": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#E31B23"},
    "chowking": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#FFC600"},
    "greenwich": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#008000"},
    "shakeys": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#E31937"},
    "shakey's": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#E31937"},
    "yellow cab": {"category": "Food & Dining", "icon": ft.Icons.LOCAL_PIZZA, "color": "#FFD100"},
    "mang inasal": {"category": "Food & Dining", "icon": ft.Icons.RESTAURANT, "color": "#FDB813"},
    "pancake house": {"category": "Food & Dining", "icon": ft.Icons.BREAKFAST_DINING, "color": "#8B4513"},
    "denny's": {"category": "Food & Dining", "icon": ft.Icons.BREAKFAST_DINING, "color": "#FFCC00"},
    "ihop": {"category": "Food & Dining", "icon": ft.Icons.BREAKFAST_DINING, "color": "#00468C"},
    
    # Coffee Shops
    "coffee bean": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#683016"},
    "costa": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#6F1E24"},
    "nescafe": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#C8102E"},
    "bo's coffee": {"category": "Food & Dining", "icon": ft.Icons.COFFEE, "color": "#4A2C2A"},
    
    # Transport & Rideshare
    "uber": {"category": "Transport", "icon": ft.Icons.LOCAL_TAXI, "color": "#000000"},
    "lyft": {"category": "Transport", "icon": ft.Icons.LOCAL_TAXI, "color": "#FF00BF"},
    "grab": {"category": "Transport", "icon": ft.Icons.LOCAL_TAXI, "color": "#00B14F"},
    "angkas": {"category": "Transport", "icon": ft.Icons.TWO_WHEELER, "color": "#00A551"},
    "joyride": {"category": "Transport", "icon": ft.Icons.TWO_WHEELER, "color": "#FF8C00"},
    "gojek": {"category": "Transport", "icon": ft.Icons.TWO_WHEELER, "color": "#00AA13"},
    "bolt": {"category": "Transport", "icon": ft.Icons.LOCAL_TAXI, "color": "#34D186"},
    "didi": {"category": "Transport", "icon": ft.Icons.LOCAL_TAXI, "color": "#FF7F0E"},
    "shell": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#FFD500"},
    "petron": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#1F4E8C"},
    "caltex": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#E31937"},
    "chevron": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#0066CC"},
    "exxon": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#FF0000"},
    "mobil": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#FF0000"},
    "total": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#D40000"},
    "bp": {"category": "Transport", "icon": ft.Icons.LOCAL_GAS_STATION, "color": "#009900"},
    
    # Grocery & Retail
    "walmart": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#0071CE"},
    "costco": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#E31837"},
    "target": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#CC0000"},
    "sm supermarket": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#0052A5"},
    "sm": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#0052A5"},
    "robinsons": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#1E3A8A"},
    "puregold": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#FFD700"},
    "savemore": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#FF6600"},
    "landmark": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#E31937"},
    "rustan's": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#000000"},
    "metro": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#003087"},
    "landers": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#004C97"},
    "s&r": {"category": "Groceries", "icon": ft.Icons.SHOPPING_CART, "color": "#1E4D78"},
    "7-eleven": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#00854A"},
    "711": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#00854A"},
    "ministop": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#0066CC"},
    "family mart": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#00B8A9"},
    "lawson": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#004C97"},
    "alfamart": {"category": "Groceries", "icon": ft.Icons.STORE, "color": "#ED1C24"},
    "mercury drug": {"category": "Health", "icon": ft.Icons.LOCAL_PHARMACY, "color": "#FF6600"},
    "watsons": {"category": "Health", "icon": ft.Icons.LOCAL_PHARMACY, "color": "#00A99D"},
    "southstar drug": {"category": "Health", "icon": ft.Icons.LOCAL_PHARMACY, "color": "#0066CC"},
    
    # E-commerce
    "amazon": {"category": "Shopping", "icon": ft.Icons.LOCAL_SHIPPING, "color": "#FF9900"},
    "lazada": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#0F146D"},
    "shopee": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#EE4D2D"},
    "zalora": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#000000"},
    "ebay": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#E53238"},
    "aliexpress": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#FF4747"},
    "temu": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#FB7701"},
    "shein": {"category": "Shopping", "icon": ft.Icons.SHOPPING_BAG, "color": "#000000"},
    
    # Streaming & Entertainment
    "netflix": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#E50914"},
    "spotify": {"category": "Subscription", "icon": ft.Icons.MUSIC_NOTE, "color": "#1DB954"},
    "youtube": {"category": "Subscription", "icon": ft.Icons.PLAY_CIRCLE, "color": "#FF0000"},
    "youtube premium": {"category": "Subscription", "icon": ft.Icons.PLAY_CIRCLE, "color": "#FF0000"},
    "disney+": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#113CCF"},
    "disney plus": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#113CCF"},
    "hbo": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#000000"},
    "hbo max": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#5822B4"},
    "amazon prime": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#00A8E1"},
    "prime video": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#00A8E1"},
    "apple tv": {"category": "Subscription", "icon": ft.Icons.TV, "color": "#000000"},
    "hulu": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#1CE783"},
    "paramount+": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#0064FF"},
    "viu": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#FFB700"},
    "iqiyi": {"category": "Subscription", "icon": ft.Icons.MOVIE, "color": "#00C800"},
    "apple music": {"category": "Subscription", "icon": ft.Icons.MUSIC_NOTE, "color": "#FC3C44"},
    "deezer": {"category": "Subscription", "icon": ft.Icons.MUSIC_NOTE, "color": "#FEAA2D"},
    "tidal": {"category": "Subscription", "icon": ft.Icons.MUSIC_NOTE, "color": "#000000"},
    
    # Gaming
    "steam": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#1B2838"},
    "epic games": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#2F2D2E"},
    "riot games": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#D32936"},
    "valorant": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#FF4655"},
    "league of legends": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#C8AA6E"},
    "lol": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#C8AA6E"},
    "mobile legends": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#3E73B9"},
    "mlbb": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#3E73B9"},
    "genshin": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#00C8FF"},
    "genshin impact": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#00C8FF"},
    "roblox": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#E2231A"},
    "minecraft": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#62B47A"},
    "fortnite": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#9D4DFF"},
    "call of duty": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#000000"},
    "cod": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#000000"},
    "pubg": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#F2A900"},
    "ea games": {"category": "Entertainment", "icon": ft.Icons.SPORTS_ESPORTS, "color": "#FF4747"},
    "fifa": {"category": "Entertainment", "icon": ft.Icons.SPORTS_SOCCER, "color": "#326295"},
    "nba 2k": {"category": "Entertainment", "icon": ft.Icons.SPORTS_BASKETBALL, "color": "#C8102E"},
    
    # Airlines & Travel
    "philippine airlines": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#0033A0"},
    "pal": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#0033A0"},
    "cebu pacific": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#FDB813"},
    "airasia": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#FF0000"},
    "singapore airlines": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#0C2340"},
    "cathay pacific": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#005A43"},
    "emirates": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#D71921"},
    "qatar airways": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#5C0632"},
    "japan airlines": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#CC0000"},
    "jal": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#CC0000"},
    "ana": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#00467F"},
    "delta": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#003A70"},
    "united": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#0033A0"},
    "american airlines": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#0078D2"},
    "jetstar": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#FF6600"},
    "scoot": {"category": "Travel", "icon": ft.Icons.FLIGHT, "color": "#FFD100"},
    "booking.com": {"category": "Travel", "icon": ft.Icons.HOTEL, "color": "#003580"},
    "agoda": {"category": "Travel", "icon": ft.Icons.HOTEL, "color": "#5391D0"},
    "airbnb": {"category": "Travel", "icon": ft.Icons.HOTEL, "color": "#FF5A5F"},
    "expedia": {"category": "Travel", "icon": ft.Icons.TRAVEL_EXPLORE, "color": "#FFCC00"},
    "trivago": {"category": "Travel", "icon": ft.Icons.HOTEL, "color": "#007FAD"},
    "klook": {"category": "Travel", "icon": ft.Icons.TRAVEL_EXPLORE, "color": "#FF5722"},
    
    # Banks & Finance
    "bpi": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#C41230"},
    "bdo": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#003087"},
    "metrobank": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#005BAC"},
    "unionbank": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#F26722"},
    "landbank": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#00703C"},
    "pnb": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#002E6D"},
    "security bank": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#00A651"},
    "chinabank": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#C41230"},
    "eastwest": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE, "color": "#00467F"},
    "gcash": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#007DFE"},
    "maya": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#00D1A0"},
    "paymaya": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#00D1A0"},
    "grabpay": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#00B14F"},
    "paypal": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#003087"},
    "wise": {"category": "Bills & Utilities", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#9FE870"},
    
    # Utilities & Telecoms
    "meralco": {"category": "Bills & Utilities", "icon": ft.Icons.BOLT, "color": "#F7941D"},
    "manila water": {"category": "Bills & Utilities", "icon": ft.Icons.WATER_DROP, "color": "#0066B3"},
    "maynilad": {"category": "Bills & Utilities", "icon": ft.Icons.WATER_DROP, "color": "#00529B"},
    "pldt": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#E31937"},
    "globe": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#0066B3"},
    "smart": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#00A850"},
    "converge": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#00ADEF"},
    "sky cable": {"category": "Bills & Utilities", "icon": ft.Icons.TV, "color": "#0066B3"},
    "cignal": {"category": "Bills & Utilities", "icon": ft.Icons.TV, "color": "#E31937"},
    "verizon": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#CD040B"},
    "at&t": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#00A8E0"},
    "t-mobile": {"category": "Bills & Utilities", "icon": ft.Icons.WIFI, "color": "#E20074"},
    
    # Education
    "udemy": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#A435F0"},
    "coursera": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#0056D2"},
    "skillshare": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#00FF84"},
    "linkedin learning": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#0A66C2"},
    "duolingo": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#58CC02"},
    "masterclass": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#000000"},
    "khan academy": {"category": "Education", "icon": ft.Icons.SCHOOL, "color": "#14BF96"},
    "grammarly": {"category": "Education", "icon": ft.Icons.EDIT, "color": "#15C39A"},
    
    # Health & Fitness
    "gym": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#FF4444"},
    "fitness first": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#003366"},
    "gold's gym": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#FFD700"},
    "anytime fitness": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#662D91"},
    "planet fitness": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#5C2D91"},
    "equinox": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#000000"},
    "peloton": {"category": "Health", "icon": ft.Icons.FITNESS_CENTER, "color": "#000000"},
    "hospital": {"category": "Health", "icon": ft.Icons.LOCAL_HOSPITAL, "color": "#FF0000"},
    "clinic": {"category": "Health", "icon": ft.Icons.MEDICAL_SERVICES, "color": "#00A99D"},
    "pharmacy": {"category": "Health", "icon": ft.Icons.LOCAL_PHARMACY, "color": "#00A99D"},
    "doctor": {"category": "Health", "icon": ft.Icons.MEDICAL_SERVICES, "color": "#00A99D"},
    "dentist": {"category": "Health", "icon": ft.Icons.MEDICAL_SERVICES, "color": "#00A99D"},
    
    # Beauty & Personal Care
    "sephora": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#000000"},
    "ulta": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#F26B38"},
    "mac": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#000000"},
    "maybelline": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#000000"},
    "loreal": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#000000"},
    "l'oreal": {"category": "Shopping", "icon": ft.Icons.FACE_RETOUCHING_NATURAL, "color": "#000000"},
    "salon": {"category": "Shopping", "icon": ft.Icons.CONTENT_CUT, "color": "#FF69B4"},
    "spa": {"category": "Shopping", "icon": ft.Icons.SPA, "color": "#00CED1"},
    "barbershop": {"category": "Shopping", "icon": ft.Icons.CONTENT_CUT, "color": "#8B4513"},
    "barber": {"category": "Shopping", "icon": ft.Icons.CONTENT_CUT, "color": "#8B4513"},
    "haircut": {"category": "Shopping", "icon": ft.Icons.CONTENT_CUT, "color": "#8B4513"},
    
    # Furniture & Home
    "ikea": {"category": "Shopping", "icon": ft.Icons.CHAIR, "color": "#0051BA"},
    "sm home": {"category": "Shopping", "icon": ft.Icons.HOME, "color": "#0052A5"},
    "ace hardware": {"category": "Shopping", "icon": ft.Icons.HARDWARE, "color": "#E31937"},
    "handyman": {"category": "Shopping", "icon": ft.Icons.HARDWARE, "color": "#00A551"},
    "cw home": {"category": "Shopping", "icon": ft.Icons.HOME, "color": "#00529B"},
    "our home": {"category": "Shopping", "icon": ft.Icons.HOME, "color": "#8B4513"},
    
    # Food Delivery
    "foodpanda": {"category": "Food & Dining", "icon": ft.Icons.DELIVERY_DINING, "color": "#D70F64"},
    "grabfood": {"category": "Food & Dining", "icon": ft.Icons.DELIVERY_DINING, "color": "#00B14F"},
    "doordash": {"category": "Food & Dining", "icon": ft.Icons.DELIVERY_DINING, "color": "#FF3008"},
    "uber eats": {"category": "Food & Dining", "icon": ft.Icons.DELIVERY_DINING, "color": "#06C167"},
    "deliveroo": {"category": "Food & Dining", "icon": ft.Icons.DELIVERY_DINING, "color": "#00CCBC"},
    "instacart": {"category": "Groceries", "icon": ft.Icons.DELIVERY_DINING, "color": "#43B02A"},
}

# Generic category keywords for fallback matching
CATEGORY_KEYWORDS = {
    "Food & Dining": ["food", "restaurant", "eat", "dining", "meal", "lunch", "dinner", "breakfast", "snack", "cafe", "diner", "bistro", "grill", "kitchen", "eatery", "canteen"],
    "Transport": ["taxi", "bus", "train", "mrt", "lrt", "jeep", "jeepney", "tricycle", "gas", "fuel", "parking", "toll", "fare", "ride", "commute", "car", "vehicle", "motorcycle"],
    "Shopping": ["shop", "mall", "store", "buy", "purchase", "retail", "boutique", "outlet", "market", "bazaar"],
    "Entertainment": ["movie", "cinema", "theater", "concert", "show", "game", "arcade", "karaoke", "club", "bar", "party", "event", "ticket"],
    "Bills & Utilities": ["bill", "utility", "electric", "water", "internet", "phone", "cable", "rent", "insurance", "tax", "fee", "payment"],
    "Health": ["medical", "medicine", "health", "hospital", "clinic", "doctor", "dental", "pharmacy", "drug", "vitamin", "checkup", "therapy", "treatment"],
    "Education": ["school", "course", "class", "book", "tuition", "training", "learn", "study", "education", "tutorial", "seminar", "workshop"],
    "Electronics": ["gadget", "phone", "laptop", "computer", "tablet", "camera", "speaker", "headphone", "charger", "cable", "accessory", "device", "tech"],
    "Groceries": ["grocery", "supermarket", "market", "vegetables", "fruits", "meat", "fish", "rice", "bread", "milk", "eggs", "household"],
    "Travel": ["travel", "trip", "vacation", "holiday", "flight", "hotel", "resort", "tour", "booking", "airfare", "luggage", "passport", "visa"],
    "Subscription": ["subscription", "membership", "premium", "plan", "monthly", "annual", "renewal"],
    "Fashion & Apparel": ["clothes", "clothing", "shoes", "sneakers", "shirt", "pants", "dress", "jacket", "bag", "watch", "jewelry", "accessories", "fashion", "apparel", "wear"],
}

# Default icons for categories
DEFAULT_CATEGORY_ICONS = {
    "Food & Dining": {"icon": ft.Icons.RESTAURANT, "color": "#FF6B35"},
    "Transport": {"icon": ft.Icons.DIRECTIONS_CAR, "color": "#4CAF50"},
    "Shopping": {"icon": ft.Icons.SHOPPING_BAG, "color": "#9C27B0"},
    "Entertainment": {"icon": ft.Icons.MOVIE, "color": "#E91E63"},
    "Bills & Utilities": {"icon": ft.Icons.RECEIPT, "color": "#FF9800"},
    "Health": {"icon": ft.Icons.LOCAL_HOSPITAL, "color": "#F44336"},
    "Education": {"icon": ft.Icons.SCHOOL, "color": "#3F51B5"},
    "Electronics": {"icon": ft.Icons.DEVICES, "color": "#607D8B"},
    "Groceries": {"icon": ft.Icons.LOCAL_GROCERY_STORE, "color": "#8BC34A"},
    "Rent": {"icon": ft.Icons.HOME, "color": "#795548"},
    "Travel": {"icon": ft.Icons.FLIGHT, "color": "#00BCD4"},
    "Subscription": {"icon": ft.Icons.SUBSCRIPTIONS, "color": "#673AB7"},
    "Fashion & Apparel": {"icon": ft.Icons.CHECKROOM, "color": "#FF4081"},
    "Other": {"icon": ft.Icons.CATEGORY, "color": "#9E9E9E"},
}


def identify_brand(input_text: str) -> dict:
    """
    AI-like brand recognition function.
    Analyzes the input text and returns brand info with category, icon, and color.
    
    Args:
        input_text: The user's input (brand name, store name, etc.)
    
    Returns:
        dict with keys: 'original', 'display_name', 'category', 'icon', 'color', 'is_brand'
    """
    if not input_text:
        return {
            "original": "",
            "display_name": "Other",
            "category": "Other",
            "icon": ft.Icons.CATEGORY,
            "color": "#9E9E9E",
            "is_brand": False
        }
    
    input_lower = input_text.lower().strip()
    
    # 1. Direct brand match
    if input_lower in BRAND_DATABASE:
        brand_info = BRAND_DATABASE[input_lower]
        return {
            "original": input_text,
            "display_name": input_text.title(),
            "category": brand_info["category"],
            "icon": brand_info["icon"],
            "color": brand_info["color"],
            "is_brand": True
        }
    
    # 2. Partial brand match (brand name contained in input)
    for brand_name, brand_info in BRAND_DATABASE.items():
        if brand_name in input_lower or input_lower in brand_name:
            return {
                "original": input_text,
                "display_name": input_text.title(),
                "category": brand_info["category"],
                "icon": brand_info["icon"],
                "color": brand_info["color"],
                "is_brand": True
            }
    
    # 3. Category keyword matching
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in input_lower:
                cat_info = DEFAULT_CATEGORY_ICONS.get(category, DEFAULT_CATEGORY_ICONS["Other"])
                return {
                    "original": input_text,
                    "display_name": input_text.title(),
                    "category": category,
                    "icon": cat_info["icon"],
                    "color": cat_info["color"],
                    "is_brand": False
                }
    
    # 4. Default - unknown category
    return {
        "original": input_text,
        "display_name": input_text.title(),
        "category": input_text.title(),  # Use input as category name
        "icon": ft.Icons.CATEGORY,
        "color": "#7C3AED",  # Purple for custom
        "is_brand": False
    }


def get_icon_for_category(category: str) -> dict:
    """
    Get icon and color for a category name.
    Uses brand recognition to find the best match.
    
    Args:
        category: The category name
    
    Returns:
        dict with 'icon' and 'color' keys
    """
    result = identify_brand(category)
    return {
        "icon": result["icon"],
        "color": result["color"]
    }


def get_brand_suggestions(partial_input: str, limit: int = 5) -> list:
    """
    Get brand suggestions based on partial input (for autocomplete).
    
    Args:
        partial_input: The partial text input
        limit: Maximum number of suggestions
    
    Returns:
        List of matching brand names
    """
    if not partial_input or len(partial_input) < 2:
        return []
    
    input_lower = partial_input.lower().strip()
    suggestions = []
    
    for brand_name in BRAND_DATABASE.keys():
        if brand_name.startswith(input_lower) or input_lower in brand_name:
            suggestions.append(brand_name.title())
            if len(suggestions) >= limit:
                break
    
    return suggestions
