# src/ui/Expenses.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav


# Brand database for recognition - with real brand logos from reliable CDNs
BRAND_DATABASE = {
    # Shopping & E-commerce
    "amazon": {
        "icon": "a", "color": "#FF9900", "bg": "#232F3E", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"
    },
    "shopee": {
        "icon": "🛒", "color": "#EE4D2D", "bg": "#EE4D2D", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Shopee_logo.svg"
    },
    "lazada": {
        "icon": "L", "color": "#0F146D", "bg": "#0F146D", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/55/Lazada_%282019%29.svg"
    },
    "zalora": {
        "icon": "Z", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/7/77/Zalora_Logo.svg"
    },
    "ebay": {
        "icon": "e", "color": "#E53238", "bg": "#FFFFFF", "text": "#E53238",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/1/1b/EBay_logo.svg"
    },
    
    # Food & Restaurants
    "mcdonalds": {
        "icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg"
    },
    "mcdonald's": {
        "icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg"
    },
    "starbucks": {
        "icon": "☕", "color": "#00704A", "bg": "#00704A", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg"
    },
    "jollibee": {
        "icon": "🐝", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/8/84/Jollibee_2011_logo.svg"
    },
    "kfc": {
        "icon": "🍗", "color": "#F40027", "bg": "#F40027", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/b/bf/KFC_logo.svg"
    },
    "burger king": {
        "icon": "🍔", "color": "#FF8732", "bg": "#502314", "text": "#FF8732",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/8/85/Burger_King_logo_%281999%29.svg"
    },
    "pizza hut": {
        "icon": "🍕", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/sco/d/d2/Pizza_Hut_logo.svg"
    },
    "subway": {
        "icon": "🥪", "color": "#008C15", "bg": "#FFC600", "text": "#008C15",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Subway_2016_logo.svg"
    },
    "dunkin": {
        "icon": "🍩", "color": "#FF671F", "bg": "#FF671F", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/b/b8/Dunkin%27_Donuts_logo.svg"
    },
    "chowking": {
        "icon": "🥡", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/b/b2/Chowking_Logo_2019.png"
    },
    "greenwich": {
        "icon": "🍕", "color": "#006B3F", "bg": "#006B3F", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Greenwich_Pizza_logo.png"
    },
    
    # Tech & Electronics
    "apple": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    },
    "ipad": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    },
    "iphone": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    },
    "macbook": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    },
    "samsung": {
        "icon": "S", "color": "#1428A0", "bg": "#1428A0", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg"
    },
    "google": {
        "icon": "G", "color": "#4285F4", "bg": "#FFFFFF", "text": "#4285F4",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"
    },
    "microsoft": {
        "icon": "⊞", "color": "#00A4EF", "bg": "#737373", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg"
    },
    "sony": {
        "icon": "S", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg"
    },
    
    # Finance & Payment
    "mastercard": {
        "icon": "●●", "color": "#EB001B", "bg": "#FF5F00", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Mastercard_2019_logo.svg"
    },
    "visa": {
        "icon": "V", "color": "#1A1F71", "bg": "#1A1F71", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg"
    },
    "paypal": {
        "icon": "P", "color": "#003087", "bg": "#003087", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg"
    },
    "gcash": {
        "icon": "G", "color": "#007DFE", "bg": "#007DFE", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/ed/GCash_logo.svg"
    },
    "maya": {
        "icon": "M", "color": "#00D66C", "bg": "#00D66C", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Maya_%28digital_wallet%29_logo.svg"
    },
    "bpi": {
        "icon": "B", "color": "#9E1B34", "bg": "#9E1B34", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/5/57/BPI_logo.svg"
    },
    "bdo": {
        "icon": "B", "color": "#003478", "bg": "#003478", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/0/07/BDO_Unibank.svg"
    },
    
    # Streaming & Entertainment
    "netflix": {
        "icon": "N", "color": "#E50914", "bg": "#000000", "text": "#E50914",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"
    },
    "spotify": {
        "icon": "♪", "color": "#1DB954", "bg": "#191414", "text": "#1DB954",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg"
    },
    "youtube": {
        "icon": "▶", "color": "#FF0000", "bg": "#282828", "text": "#FF0000",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_of_YouTube_%282015-2017%29.svg"
    },
    "disney": {
        "icon": "D", "color": "#113CCF", "bg": "#040814", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg"
    },
    "hbo": {
        "icon": "H", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/d/de/HBO_logo.svg"
    },
    
    # Transport
    "grab": {
        "icon": "G", "color": "#00B14F", "bg": "#00B14F", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/1/12/Grab_Logo.svg"
    },
    "uber": {
        "icon": "U", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png"
    },
    "angkas": {
        "icon": "A", "color": "#F16521", "bg": "#F16521", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/9/96/Angkas_app_icon.png"
    },
    "shell": {
        "icon": "🐚", "color": "#FBCE07", "bg": "#DD1D21", "text": "#FBCE07",
        "logo": "https://upload.wikimedia.org/wikipedia/en/e/e8/Shell_logo.svg"
    },
    "petron": {
        "icon": "P", "color": "#1E4D8C", "bg": "#1E4D8C", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/2/2c/Petron_Corporation_Logo.svg"
    },
    "caltex": {
        "icon": "★", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/1/16/Caltex_logo.svg"
    },
    
    # Utilities
    "meralco": {
        "icon": "⚡", "color": "#FF6B00", "bg": "#FF6B00", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/8/82/Meralco_logo.svg"
    },
    "pldt": {
        "icon": "P", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/ec/PLDT_Logo.svg"
    },
    "globe": {
        "icon": "G", "color": "#0056A3", "bg": "#0056A3", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/35/Globe_Telecom_Logo.svg"
    },
    "smart": {
        "icon": "S", "color": "#00913A", "bg": "#00913A", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Smart_Communications_logo.svg"
    },
    "maynilad": {
        "icon": "M", "color": "#0072CE", "bg": "#0072CE", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/7/73/Maynilad_Logo.png"
    },
    
    # Retail & Supermarkets
    "sm": {
        "icon": "SM", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3a/SM_Supermalls_logo.svg"
    },
    "robinsons": {
        "icon": "R", "color": "#00529B", "bg": "#00529B", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/en/c/c5/Robinsons_Supermarket_logo.svg"
    },
    "uniqlo": {
        "icon": "U", "color": "#FF0000", "bg": "#FFFFFF", "text": "#FF0000",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/9/92/UNIQLO_logo.svg"
    },
    "h&m": {
        "icon": "H&M", "color": "#E50010", "bg": "#FFFFFF", "text": "#E50010",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg"
    },
    "nike": {
        "icon": "✓", "color": "#111111", "bg": "#111111", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg"
    },
    "adidas": {
        "icon": "⫿", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg"
    },
}


def get_brand_info(text: str):
    """Get brand info from text."""
    text_lower = text.lower()
    for brand, info in BRAND_DATABASE.items():
        if brand in text_lower:
            return info
    return None


def create_expense_item(brand_text: str, date: str, amount: float, on_click=None):
    """Creates a modern expense item row matching the design with real brand logos."""
    # Format amount
    amount_str = f"-₱{abs(amount):,.2f}"
    
    # Get brand info
    brand_info = get_brand_info(brand_text)
    
    if brand_info:
        # Check if we have a logo URL
        if "logo" in brand_info and brand_info["logo"]:
            # Use real brand logo image
            icon_container = ft.Container(
                content=ft.Image(
                    src=brand_info["logo"],
                    width=30,
                    height=30,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text(
                        brand_info["icon"],
                        size=20,
                        color=brand_info.get("text", "white"),
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                width=50,
                height=50,
                border_radius=25,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
        else:
            # Fallback to text icon
            icon_container = ft.Container(
                content=ft.Text(
                    brand_info["icon"],
                    size=22,
                    color=brand_info.get("text", "white"),
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                width=50,
                height=50,
                border_radius=25,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
    else:
        # Default icon for unknown brands
        icon_container = ft.Container(
            content=ft.Icon(ft.Icons.PAYMENTS, color="white", size=24),
            width=50,
            height=50,
            border_radius=25,
            bgcolor="#374151",
            alignment=ft.alignment.center,
        )
    
    # Amount badge with rounded pill shape (teal/green color from design)
    amount_badge = ft.Container(
        content=ft.Text(
            amount_str,
            size=12,
            weight=ft.FontWeight.W_600,
            color="#10B981",  # Teal/green color
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=20,
        bgcolor="#0D3D2E",  # Dark green background
    )
    
    return ft.Container(
        content=ft.Row(
            controls=[
                icon_container,
                ft.Container(width=12),
                # Title and date column
                ft.Column(
                    controls=[
                        ft.Text(
                            brand_text,
                            size=15,
                            weight=ft.FontWeight.W_500,
                            color="white",
                        ),
                        ft.Text(
                            date,
                            size=12,
                            color="#6B7280",
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                amount_badge,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=12, horizontal=4),
        on_click=on_click,
        ink=True,
        border_radius=12,
    )


def create_expenses_view(page: ft.Page, state: dict, toast, show_home, show_wallet, show_profile, show_add_expense):
    """
    Creates the Expenses page view matching the design with hexagonal FAB.
    """
    
    expenses_list = ft.Column(spacing=8)
    
    def format_date(date_str: str) -> str:
        """Format date string to display format (e.g., Sept 09, 2022)."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%b %d, %Y")
        except:
            return date_str
    
    def load_expenses():
        """Load and display all expenses."""
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        for r in rows:
            eid, uid, amt, cat, dsc, dtt = r
            display_name = dsc if dsc else cat
            
            expenses_list.controls.append(
                create_expense_item(
                    brand_text=display_name,
                    date=format_date(dtt),
                    amount=-amt,  # Expenses are negative
                )
            )
        
        if not rows:
            expenses_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG, color="#4B5563", size=48),
                            ft.Container(height=8),
                            ft.Text("No expenses yet", color="#6B7280", size=16),
                            ft.Text("Tap + to add your first expense", color="#4B5563", size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        page.update()
    
    def show_new_account_form():
        """Show the 'New account' form for manual input."""
        
        # Get current theme
        theme = get_theme()
        
        # Form state
        selected_type = {"value": "Cash"}
        selected_color = {"value": "#3B82F6"}
        
        # Color options
        color_options = [
            "#3B82F6",  # Blue
            "#10B981",  # Green
            "#F59E0B",  # Orange
            "#EF4444",  # Red
            "#8B5CF6",  # Purple
            "#EC4899",  # Pink
            "#06B6D4",  # Cyan
            "#6B7280",  # Gray
        ]
        
        # Account type options
        account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
        
        def close_form(e):
            page.close(new_account_sheet)
        
        def select_color(color: str):
            selected_color["value"] = color
            # Update color indicators
            for i, ctrl in enumerate(color_row.controls):
                if color_options[i] == color:
                    ctrl.border = ft.border.all(2, "white")
                else:
                    ctrl.border = None
            page.update()
        
        def create_account(e):
            account_name = name_field.value
            if not account_name:
                toast("Please enter account name", "#EF4444")
                return
            
            # Get form values
            account_number = bank_number_field.value or ""
            account_type = type_dropdown.value
            try:
                initial_balance = float(initial_value_field.value or 0)
            except ValueError:
                initial_balance = 0.0
            currency = currency_dropdown.value
            color = selected_color["value"]
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to database
            db.insert_account(
                user_id=state["user_id"],
                name=account_name,
                account_number=account_number,
                account_type=account_type,
                balance=initial_balance,
                currency=currency,
                color=color,
                created_at=created_at
            )
            
            page.close(new_account_sheet)
            toast(f"Account '{account_name}' created!", "#10B981")
            show_view()  # Refresh the view
        
        # Form fields
        name_field = ft.TextField(
            label="Account name",
            hint_text="e.g., My Wallet, Savings",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            cursor_color=theme.accent_primary,
        )
        
        bank_number_field = ft.TextField(
            label="Bank account number (optional)",
            hint_text="Enter account number",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            cursor_color=theme.accent_primary,
        )
        
        # Type dropdown
        type_dropdown = ft.Dropdown(
            label="Type",
            value="Cash",
            options=[ft.dropdown.Option(t) for t in account_types],
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            border_radius=12,
        )
        
        initial_value_field = ft.TextField(
            label="Initial value",
            hint_text="0.00",
            value="0",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="₱ ",
            prefix_style=ft.TextStyle(color=theme.text_secondary),
            cursor_color=theme.accent_primary,
        )
        
        # Currency dropdown
        currency_dropdown = ft.Dropdown(
            label="Currency",
            value="PHP",
            options=[
                ft.dropdown.Option("PHP", "₱ Philippine Peso"),
                ft.dropdown.Option("USD", "$ US Dollar"),
                ft.dropdown.Option("EUR", "€ Euro"),
                ft.dropdown.Option("JPY", "¥ Japanese Yen"),
                ft.dropdown.Option("GBP", "£ British Pound"),
            ],
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            border_radius=12,
        )
        
        # Color selection row
        color_row = ft.Row(
            controls=[
                ft.Container(
                    width=36,
                    height=36,
                    border_radius=18,
                    bgcolor=color,
                    border=ft.border.all(2, "white") if color == selected_color["value"] else None,
                    on_click=lambda e, c=color: select_color(c),
                    ink=True,
                )
                for color in color_options
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        new_account_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header with back button
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=theme.text_secondary,
                                            icon_size=24,
                                            on_click=lambda e: (page.close(new_account_sheet), show_account_type_sheet()),
                                        ),
                                        ft.Text("New account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                    ],
                                    spacing=8,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_secondary,
                                    icon_size=24,
                                    on_click=close_form,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Set up your manual account details",
                            size=14,
                            color=theme.text_muted,
                        ),
                        ft.Container(height=20),
                        # Form fields
                        name_field,
                        ft.Container(height=16),
                        bank_number_field,
                        ft.Container(height=16),
                        type_dropdown,
                        ft.Container(height=16),
                        initial_value_field,
                        ft.Container(height=16),
                        currency_dropdown,
                        ft.Container(height=20),
                        # Color selection
                        ft.Text("Account color", size=14, color=theme.text_secondary),
                        ft.Container(height=12),
                        color_row,
                        ft.Container(height=24),
                        # Create button
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=20),
                                    ft.Container(width=8),
                                    ft.Text("Create Account", size=16, weight=ft.FontWeight.W_600, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(vertical=16),
                            border_radius=12,
                            bgcolor=theme.accent_primary,
                            on_click=create_account,
                            ink=True,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(new_account_sheet)
    
    def show_account_settings():
        """Show the Account Settings screen for managing accounts."""
        
        # Get current theme
        theme = get_theme()
        
        def show_edit_account_form(account_data):
            """Show form to edit an existing account."""
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at, acc_status, sort_order = account_data
            
            # Form state
            selected_type = {"value": acc_type}
            selected_color = {"value": acc_color}
            selected_status = {"value": acc_status}
            
            # Color options
            color_options = [
                "#3B82F6",  # Blue
                "#10B981",  # Green
                "#F59E0B",  # Orange
                "#EF4444",  # Red
                "#8B5CF6",  # Purple
                "#EC4899",  # Pink
                "#06B6D4",  # Cyan
                "#6B7280",  # Gray
            ]
            
            # Account type options
            account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
            
            def close_edit(e):
                page.close(edit_sheet)
            
            def select_color(color: str):
                selected_color["value"] = color
                for i, ctrl in enumerate(color_row.controls):
                    if color_options[i] == color:
                        ctrl.border = ft.border.all(2, "white")
                    else:
                        ctrl.border = None
                page.update()
            
            def select_status(status: str):
                selected_status["value"] = status
                # Update status button styles
                for btn in status_row.controls:
                    if hasattr(btn, 'data') and btn.data == status:
                        btn.bgcolor = "#3B82F6"
                        btn.content.controls[1].color = "white"
                    elif hasattr(btn, 'data'):
                        btn.bgcolor = "#1a1a2e"
                        btn.content.controls[1].color = "#9CA3AF"
                page.update()
            
            def save_account(e):
                new_name = name_field.value
                if not new_name:
                    toast("Please enter account name", "#EF4444")
                    return
                
                # Get form values
                new_account_number = bank_number_field.value or ""
                new_type = type_dropdown.value
                try:
                    new_balance = float(balance_field.value or 0)
                except ValueError:
                    new_balance = acc_balance
                new_currency = currency_dropdown.value
                new_color = selected_color["value"]
                new_status = selected_status["value"]
                
                # Update in database
                db.update_account(
                    account_id=acc_id,
                    user_id=state["user_id"],
                    name=new_name,
                    account_number=new_account_number,
                    account_type=new_type,
                    balance=new_balance,
                    currency=new_currency,
                    color=new_color,
                    status=new_status
                )
                
                page.close(edit_sheet)
                settings_sheet.open = False
                page.update()
                toast(f"Account '{new_name}' updated!", "#10B981")
                show_view()  # Refresh
            
            def delete_account_confirm(e):
                def confirm_delete(e):
                    db.delete_account(acc_id, state["user_id"])
                    page.close(confirm_dialog)
                    page.close(edit_sheet)
                    settings_sheet.open = False
                    page.update()
                    toast(f"Account '{acc_name}' deleted", "#EF4444")
                    show_view()
                
                def cancel_delete(e):
                    page.close(confirm_dialog)
                
                confirm_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Delete Account?", color="white"),
                    content=ft.Text(f"Are you sure you want to delete '{acc_name}'? This action cannot be undone.", color="#9CA3AF"),
                    bgcolor="#1a1a2e",
                    actions=[
                        ft.TextButton("Cancel", on_click=cancel_delete),
                        ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color="#EF4444")),
                    ],
                )
                page.open(confirm_dialog)
            
            # Form fields
            name_field = ft.TextField(
                label="Account name",
                value=acc_name,
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                cursor_color=theme.accent_primary,
            )
            
            bank_number_field = ft.TextField(
                label="Bank account number (optional)",
                value=acc_number or "",
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                cursor_color=theme.accent_primary,
            )
            
            type_dropdown = ft.Dropdown(
                label="Type",
                value=acc_type,
                options=[ft.dropdown.Option(t) for t in account_types],
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
            )
            
            balance_field = ft.TextField(
                label="Balance",
                value=str(acc_balance),
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                keyboard_type=ft.KeyboardType.NUMBER,
                prefix_text="₱ ",
                prefix_style=ft.TextStyle(color=theme.text_secondary),
                cursor_color=theme.accent_primary,
            )
            
            currency_dropdown = ft.Dropdown(
                label="Currency",
                value=acc_currency,
                options=[
                    ft.dropdown.Option("PHP", "₱ Philippine Peso"),
                    ft.dropdown.Option("USD", "$ US Dollar"),
                    ft.dropdown.Option("EUR", "€ Euro"),
                    ft.dropdown.Option("JPY", "¥ Japanese Yen"),
                    ft.dropdown.Option("GBP", "£ British Pound"),
                ],
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
            )
            
            # Status selection buttons
            def create_status_btn(label: str, status_value: str, icon):
                is_selected = acc_status == status_value
                return ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon, color="white" if is_selected else theme.text_secondary, size=16),
                            ft.Text(label, size=12, color="white" if is_selected else theme.text_secondary),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=12),
                    border_radius=8,
                    bgcolor=theme.accent_primary if is_selected else theme.bg_card,
                    border=ft.border.all(1, theme.accent_primary if is_selected else theme.border_primary),
                    on_click=lambda e, s=status_value: select_status(s),
                    data=status_value,
                    ink=True,
                    expand=True,
                )
            
            status_row = ft.Row(
                controls=[
                    create_status_btn("Active", "active", ft.Icons.CHECK_CIRCLE),
                    create_status_btn("Excluded", "excluded", ft.Icons.REMOVE_CIRCLE_OUTLINE),
                    create_status_btn("Archived", "archived", ft.Icons.ARCHIVE),
                ],
                spacing=8,
            )
            
            # Color selection row
            color_row = ft.Row(
                controls=[
                    ft.Container(
                        width=36,
                        height=36,
                        border_radius=18,
                        bgcolor=color,
                        border=ft.border.all(2, "white") if color == selected_color["value"] else None,
                        on_click=lambda e, c=color: select_color(c),
                        ink=True,
                    )
                    for color in color_options
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            
            edit_sheet = ft.BottomSheet(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            # Handle bar
                            ft.Container(
                                content=ft.Container(
                                    width=40,
                                    height=4,
                                    bgcolor=theme.text_muted,
                                    border_radius=2,
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=12, bottom=16),
                            ),
                            # Header
                            ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.ARROW_BACK,
                                                icon_color=theme.text_secondary,
                                                icon_size=24,
                                                on_click=close_edit,
                                            ),
                                            ft.Text("Edit Account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=theme.error,
                                        icon_size=24,
                                        on_click=delete_account_confirm,
                                        tooltip="Delete account",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(height=16),
                            # Form fields
                            name_field,
                            ft.Container(height=12),
                            bank_number_field,
                            ft.Container(height=12),
                            type_dropdown,
                            ft.Container(height=12),
                            balance_field,
                            ft.Container(height=12),
                            currency_dropdown,
                            ft.Container(height=16),
                            # Status selection
                            ft.Text("Account Status", size=14, color=theme.text_secondary),
                            ft.Container(height=8),
                            status_row,
                            ft.Container(height=16),
                            # Color selection
                            ft.Text("Account color", size=14, color=theme.text_secondary),
                            ft.Container(height=8),
                            color_row,
                            ft.Container(height=24),
                            # Save button
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.SAVE, color="white", size=20),
                                        ft.Container(width=8),
                                        ft.Text("Save Changes", size=16, weight=ft.FontWeight.W_600, color="white"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                padding=ft.padding.symmetric(vertical=16),
                                border_radius=12,
                                bgcolor=theme.accent_primary,
                                on_click=save_account,
                                ink=True,
                            ),
                            ft.Container(height=24),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    bgcolor=theme.bg_secondary,
                    padding=ft.padding.symmetric(horizontal=20, vertical=0),
                    border_radius=ft.border_radius.only(top_left=24, top_right=24),
                ),
                bgcolor=theme.bg_secondary,
            )
            
            page.open(edit_sheet)
        
        def create_account_settings_card(account_data):
            """Create a card for the account settings list."""
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at, acc_status, sort_order = account_data
            
            # Status badge
            status_badges = {
                "active": {"text": "Active", "color": "#10B981", "bg": "#10B98120"},
                "excluded": {"text": "Excluded", "color": "#F59E0B", "bg": "#F59E0B20"},
                "archived": {"text": "Archived", "color": "#6B7280", "bg": "#6B728020"},
            }
            badge_info = status_badges.get(acc_status, status_badges["active"])
            
            # Account type icons
            account_type_icons = {
                "Cash": ft.Icons.ACCOUNT_BALANCE_WALLET,
                "Savings": ft.Icons.SAVINGS,
                "Credit Card": ft.Icons.CREDIT_CARD,
                "Debit Card": ft.Icons.PAYMENT,
                "E-Wallet": ft.Icons.PHONE_ANDROID,
                "Other": ft.Icons.WALLET,
            }
            acc_icon = account_type_icons.get(acc_type, ft.Icons.WALLET)
            
            return ft.Container(
                content=ft.Row(
                    controls=[
                        # Drag handle
                        ft.Icon(ft.Icons.DRAG_HANDLE, color=theme.text_muted, size=20),
                        ft.Container(width=8),
                        # Account icon
                        ft.Container(
                            content=ft.Icon(acc_icon, color=acc_color, size=20),
                            width=40,
                            height=40,
                            border_radius=10,
                            bgcolor=f"{acc_color}30",
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=12),
                        # Account info
                        ft.Column(
                            controls=[
                                ft.Text(acc_name, size=15, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Row(
                                    controls=[
                                        ft.Text(acc_type, size=12, color=theme.text_muted),
                                        ft.Container(
                                            content=ft.Text(badge_info["text"], size=10, color=badge_info["color"]),
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=4,
                                            bgcolor=badge_info["bg"],
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=theme.text_muted,
                            icon_size=20,
                            on_click=lambda e, data=account_data: show_edit_account_form(data),
                            tooltip="Edit account",
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=12,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, theme.border_primary),
                on_click=lambda e, data=account_data: show_edit_account_form(data),
                ink=True,
            )
        
        # Get all accounts including archived/excluded
        all_accounts = db.get_accounts_by_user(state["user_id"], include_all=True)
        
        # Build account cards list
        account_settings_cards = []
        for acc in all_accounts:
            account_settings_cards.append(create_account_settings_card(acc))
            account_settings_cards.append(ft.Container(height=8))
        
        # If no accounts, show empty state
        if not all_accounts:
            account_settings_cards.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, color=theme.text_muted, size=48),
                            ft.Container(height=8),
                            ft.Text("No accounts yet", color=theme.text_secondary, size=16),
                            ft.Text("Tap + to add your first account", color=theme.text_muted, size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        settings_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header with back button
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=theme.text_secondary,
                                            icon_size=24,
                                            on_click=lambda e: (page.close(settings_sheet), show_view()),
                                        ),
                                        ft.Text("Accounts settings", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                    ],
                                    spacing=8,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_secondary,
                                    icon_size=24,
                                    on_click=lambda e: (page.close(settings_sheet), show_view()),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Manage your accounts, change status, or reorder them",
                            size=14,
                            color=theme.text_muted,
                        ),
                        ft.Container(height=16),
                        # Accounts list
                        ft.Column(
                            controls=account_settings_cards,
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                        ),
                        ft.Container(height=16),
                        # Add Account Button at bottom
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=20),
                                    ft.Container(width=8),
                                    ft.Text("Add New Account", size=16, weight=ft.FontWeight.W_600, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(vertical=16),
                            border_radius=12,
                            bgcolor=theme.accent_primary,
                            on_click=lambda e: (page.close(settings_sheet), show_account_type_sheet()),
                            ink=True,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(settings_sheet)
    
    def show_account_type_sheet():
        """Show the 'Choose an account type' bottom sheet with account options."""
        
        theme = get_theme()
        
        def close_sheet(e):
            page.close(account_sheet)
        
        def select_account_type(account_type: str):
            page.close(account_sheet)
            if account_type == "Manual Input":
                show_new_account_form()
            else:
                toast(f"{account_type} - Coming soon!", "#3B82F6")
        
        def create_account_type_card(icon, title: str, description: str, on_click):
            """Create an account type option card."""
            return ft.Container(
                content=ft.Row(
                    controls=[
                        # Text content
                        ft.Column(
                            controls=[
                                ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Container(height=4),
                                ft.Text(description, size=12, color=theme.text_muted, max_lines=2),
                            ],
                            spacing=0,
                            expand=True,
                        ),
                        # Icon on right side
                        ft.Container(
                            content=ft.Icon(icon, color="#3B82F6", size=28),
                            width=56,
                            height=56,
                            border_radius=12,
                            bgcolor="#3B82F620",
                            alignment=ft.alignment.center,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=16,
                border_radius=12,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, theme.border_primary),
                on_click=on_click,
                ink=True,
            )
        
        account_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header
                        ft.Row(
                            controls=[
                                ft.Text("Choose an account type", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_muted,
                                    icon_size=24,
                                    on_click=close_sheet,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Select how you want to track your finances",
                            size=14,
                            color=theme.text_secondary,
                        ),
                        ft.Container(height=20),
                        # Account type options
                        create_account_type_card(
                            icon=ft.Icons.ACCOUNT_BALANCE,
                            title="Bank Sync",
                            description="Connect your bank for automatic transaction import and real-time balance updates",
                            on_click=lambda e: select_account_type("Bank Sync"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.TRENDING_UP,
                            title="Investments",
                            description="Track stocks, crypto, mutual funds and other investment assets",
                            on_click=lambda e: select_account_type("Investments"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.UPLOAD_FILE,
                            title="File Import",
                            description="Import transactions from CSV, Excel, or OFX files exported from your bank",
                            on_click=lambda e: select_account_type("File Import"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.EDIT_NOTE,
                            title="Manual Input",
                            description="Manually enter and track all your transactions and expenses",
                            on_click=lambda e: select_account_type("Manual Input"),
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(account_sheet)
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Calculate balance
        total_budget = 100000
        total = db.total_expenses_by_user(state["user_id"])
        balance = total_budget - total
        
        # Load expenses
        load_expenses()
        
        # Header with title and profile avatar
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Expenses", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=ft.CircleAvatar(
                            foreground_image_src="/assets/icon.png",
                            bgcolor=theme.accent_primary,
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                            radius=22,
                        ),
                        on_click=lambda e: show_profile(),
                        ink=True,
                        border_radius=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=16),
        )
        
        # ============ LIST OF ACCOUNT SECTION ============
        # Section header with title and settings icon
        balance_header = ft.Row(
            controls=[
                ft.Text("List of Account", size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    icon_color=theme.text_muted,
                    icon_size=22,
                    tooltip="Account Settings",
                    on_click=lambda e: show_account_settings(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Get accounts from database
        user_accounts = db.get_accounts_by_user(state["user_id"])
        
        # Icon mapping for account types
        account_type_icons = {
            "Cash": ft.Icons.ACCOUNT_BALANCE_WALLET,
            "Savings": ft.Icons.SAVINGS,
            "Credit Card": ft.Icons.CREDIT_CARD,
            "Debit Card": ft.Icons.PAYMENT,
            "E-Wallet": ft.Icons.PHONE_ANDROID,
            "Other": ft.Icons.WALLET,
        }
        
        # Currency symbols
        currency_symbols = {
            "PHP": "₱",
            "USD": "$",
            "EUR": "€",
            "JPY": "¥",
            "GBP": "£",
        }
        
        # Create account cards list
        account_cards = []
        
        # If no accounts exist, show default Cash account
        if not user_accounts:
            cash_account_card = ft.Container(
                content=ft.Row(
                    controls=[
                        # Account icon
                        ft.Container(
                            content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="#3B82F6", size=24),
                            width=48,
                            height=48,
                            border_radius=12,
                            bgcolor="#3B82F640",
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=12),
                        # Account info
                        ft.Column(
                            controls=[
                                ft.Text("Cash", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Text("Primary Account", size=12, color=theme.text_muted),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        # Balance amount
                        ft.Text(
                            f"₱{balance:,.2f}" if balance >= 0 else "₱0.00",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=theme.text_primary,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=16,
                border_radius=12,
                bgcolor=theme.bg_field,
                border=ft.border.all(2, "#3B82F6"),  # Blue border for selected/primary
            )
            account_cards.append(cash_account_card)
        else:
            # Create cards for each account from database
            for i, acc in enumerate(user_accounts):
                # acc: (id, name, account_number, type, balance, currency, color, is_primary, created_at)
                acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at = acc
                
                # Get icon and currency symbol
                acc_icon = account_type_icons.get(acc_type, ft.Icons.WALLET)
                curr_symbol = currency_symbols.get(acc_currency, "₱")
                
                account_card = ft.Container(
                    content=ft.Row(
                        controls=[
                            # Account icon with custom color
                            ft.Container(
                                content=ft.Icon(acc_icon, color=acc_color, size=24),
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor=f"{acc_color}40",
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(width=12),
                            # Account info
                            ft.Column(
                                controls=[
                                    ft.Text(acc_name, size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                    ft.Text(
                                        f"{acc_type}" + (f" • {acc_number[-4:]}" if acc_number else ""),
                                        size=12, 
                                        color=theme.text_muted
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            # Balance amount
                            ft.Text(
                                f"{curr_symbol}{acc_balance:,.2f}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=theme.text_primary if acc_balance >= 0 else theme.error,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor=theme.bg_field,
                    border=ft.border.all(2, acc_color),  # Each account shows its own color
                )
                account_cards.append(account_card)
                account_cards.append(ft.Container(height=8))  # Spacing between cards
        
        # Add Account Button - Secondary outline style
        add_account_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=theme.text_muted, size=20),
                    ft.Container(width=8),
                    ft.Text("Add account", size=14, color=theme.text_muted),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=14),
            border_radius=12,
            border=ft.border.all(1, theme.border_primary),
            bgcolor=theme.bg_field if theme.is_dark else theme.bg_secondary,
            on_click=lambda e: show_account_type_sheet(),
            ink=True,
        )
        
        # Account Detail Button - Blue filled button
        account_detail_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.RECEIPT_LONG, color="white", size=18),
                    ft.Container(width=8),
                    ft.Text("Account Detail", size=14, weight=ft.FontWeight.W_500, color="white"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=12),
            border_radius=10,
            bgcolor="#3B82F6",
            on_click=lambda e: toast("View account details", "#3B82F6"),
            ink=True,
        )
        
        # Balance Card Container - combines all balance elements
        balance_card = ft.Container(
            content=ft.Column(
                controls=[
                    balance_header,
                    ft.Container(height=12),
                    *account_cards,  # Dynamic account cards
                    ft.Container(height=4),
                    add_account_btn,
                    ft.Container(height=12),
                    account_detail_btn,
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
        )
        
        # Main scrollable content
        scrollable_content = ft.Column(
            controls=[
                balance_card,
                ft.Container(height=24),
                expenses_list,
                ft.Container(height=100),  # Space for bottom nav and FAB
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        main_content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.gradient_start, theme.gradient_end],
            ),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
            content=ft.Column(
                controls=[
                    header,
                    scrollable_content,
                ],
                expand=True,
                spacing=0,
            ),
        )
        
        # Use centralized nav bar component
        page.add(
            create_page_with_nav(
                page=page,
                main_content=main_content,
                active_index=1,  # Expenses is active
                on_home=show_home,
                on_expenses=None,  # Already on expenses
                on_wallet=show_wallet,
                on_profile=show_profile,
                on_fab_click=show_add_expense,
                theme=theme,
            )
        )
        
        page.update()
    
    return show_view
