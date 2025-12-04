# src/ui/home_page.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav
import random
import math


# Brand database for recognition - with real brand logos (synced with Expenses.py)
BRAND_DATABASE = {
    # Shopping & E-commerce
    "amazon": {"icon": "a", "color": "#FF9900", "bg": "#232F3E", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"},
    "shopee": {"icon": "🛒", "color": "#EE4D2D", "bg": "#EE4D2D", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Shopee_logo.svg"},
    "lazada": {"icon": "L", "color": "#0F146D", "bg": "#0F146D", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/55/Lazada_%282019%29.svg"},
    "zalora": {"icon": "Z", "color": "#000000", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/77/Zalora_Logo.svg"},
    "ebay": {"icon": "e", "color": "#E53238", "bg": "#FFFFFF", "text": "#E53238", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/1b/EBay_logo.svg"},
    
    # Food & Restaurants
    "mcdonalds": {"icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg"},
    "mcdonald's": {"icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg"},
    "starbucks": {"icon": "☕", "color": "#00704A", "bg": "#00704A", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg"},
    "jollibee": {"icon": "🐝", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/8/84/Jollibee_2011_logo.svg"},
    "kfc": {"icon": "🍗", "color": "#F40027", "bg": "#F40027", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/b/bf/KFC_logo.svg"},
    "burger king": {"icon": "🍔", "color": "#FF8732", "bg": "#502314", "text": "#FF8732", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/85/Burger_King_logo_%281999%29.svg"},
    "pizza hut": {"icon": "🍕", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/sco/d/d2/Pizza_Hut_logo.svg"},
    "subway": {"icon": "🥪", "color": "#008C15", "bg": "#FFC600", "text": "#008C15", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Subway_2016_logo.svg"},
    "dunkin": {"icon": "🍩", "color": "#FF671F", "bg": "#FF671F", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/b/b8/Dunkin%27_Donuts_logo.svg"},
    "chowking": {"icon": "🥡", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/b/b2/Chowking_Logo_2019.png"},
    "greenwich": {"icon": "🍕", "color": "#006B3F", "bg": "#006B3F", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Greenwich_Pizza_logo.png"},
    
    # Tech & Electronics
    "apple": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    "ipad": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    "iphone": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    "macbook": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    "samsung": {"icon": "S", "color": "#1428A0", "bg": "#1428A0", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg"},
    "google": {"icon": "G", "color": "#4285F4", "bg": "#FFFFFF", "text": "#4285F4", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"},
    "microsoft": {"icon": "⊞", "color": "#00A4EF", "bg": "#737373", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg"},
    "sony": {"icon": "S", "color": "#000000", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg"},
    
    # Finance & Payment
    "gcash": {"icon": "G", "color": "#007DFE", "bg": "#007DFE", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/ed/GCash_logo.svg"},
    "maya": {"icon": "M", "color": "#00D66C", "bg": "#00D66C", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Maya_%28digital_wallet%29_logo.svg"},
    "bpi": {"icon": "B", "color": "#9E1B34", "bg": "#9E1B34", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/5/57/BPI_logo.svg"},
    "bdo": {"icon": "B", "color": "#003478", "bg": "#003478", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/0/07/BDO_Unibank.svg"},
    
    # Streaming & Entertainment
    "netflix": {"icon": "N", "color": "#E50914", "bg": "#000000", "text": "#E50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"},
    "spotify": {"icon": "♪", "color": "#1DB954", "bg": "#191414", "text": "#1DB954", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg"},
    "youtube": {"icon": "▶", "color": "#FF0000", "bg": "#282828", "text": "#FF0000", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_of_YouTube_%282015-2017%29.svg"},
    "disney": {"icon": "D", "color": "#113CCF", "bg": "#040814", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg"},
    
    # Transport
    "grab": {"icon": "G", "color": "#00B14F", "bg": "#00B14F", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/12/Grab_Logo.svg"},
    "uber": {"icon": "U", "color": "#000000", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png"},
    "angkas": {"icon": "A", "color": "#F16521", "bg": "#F16521", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/96/Angkas_app_icon.png"},
    "shell": {"icon": "🐚", "color": "#FBCE07", "bg": "#DD1D21", "text": "#FBCE07", "logo": "https://upload.wikimedia.org/wikipedia/en/e/e8/Shell_logo.svg"},
    "petron": {"icon": "P", "color": "#1E4D8C", "bg": "#1E4D8C", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/2/2c/Petron_Corporation_Logo.svg"},
    "caltex": {"icon": "★", "color": "#E31937", "bg": "#E31937", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/1/16/Caltex_logo.svg"},
    
    # Utilities
    "meralco": {"icon": "⚡", "color": "#FF6B00", "bg": "#FF6B00", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/8/82/Meralco_logo.svg"},
    "pldt": {"icon": "P", "color": "#E31937", "bg": "#E31937", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/ec/PLDT_Logo.svg"},
    "globe": {"icon": "G", "color": "#0056A3", "bg": "#0056A3", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/35/Globe_Telecom_Logo.svg"},
    "smart": {"icon": "S", "color": "#00913A", "bg": "#00913A", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Smart_Communications_logo.svg"},
    "maynilad": {"icon": "M", "color": "#0072CE", "bg": "#0072CE", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/7/73/Maynilad_Logo.png"},
    
    # Retail & Supermarkets
    "sm": {"icon": "SM", "color": "#003DA5", "bg": "#003DA5", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3a/SM_Supermalls_logo.svg"},
    "robinsons": {"icon": "R", "color": "#00529B", "bg": "#00529B", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/en/c/c5/Robinsons_Supermarket_logo.svg"},
    "uniqlo": {"icon": "U", "color": "#FF0000", "bg": "#FFFFFF", "text": "#FF0000", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/92/UNIQLO_logo.svg"},
    "h&m": {"icon": "H&M", "color": "#E50010", "bg": "#FFFFFF", "text": "#E50010", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg"},
    "nike": {"icon": "✓", "color": "#111111", "bg": "#111111", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg"},
    "adidas": {"icon": "⫿", "color": "#000000", "bg": "#000000", "text": "white", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg"},
}

# Category fallback icons
CATEGORY_ICONS = {
    "food": {"icon": "🍔", "bg": "#EF4444"},
    "transport": {"icon": "🚗", "bg": "#3B82F6"},
    "shopping": {"icon": "🛍️", "bg": "#8B5CF6"},
    "entertainment": {"icon": "🎬", "bg": "#EC4899"},
    "bills": {"icon": "📄", "bg": "#F59E0B"},
    "health": {"icon": "💊", "bg": "#10B981"},
    "education": {"icon": "📚", "bg": "#6366F1"},
    "salary": {"icon": "💰", "bg": "#10B981"},
    "income": {"icon": "📈", "bg": "#10B981"},
    "electronics": {"icon": "📱", "bg": "#6366F1"},
    "groceries": {"icon": "🛒", "bg": "#10B981"},
    "utilities": {"icon": "⚡", "bg": "#F59E0B"},
    "rent": {"icon": "🏠", "bg": "#8B5CF6"},
    "travel": {"icon": "✈️", "bg": "#3B82F6"},
    "fitness": {"icon": "💪", "bg": "#EF4444"},
    "subscription": {"icon": "📺", "bg": "#EC4899"},
    "other": {"icon": "📦", "bg": "#6B7280"},
}


def get_brand_info(text: str):
    """Get brand info from text."""
    text_lower = text.lower()
    for brand, info in BRAND_DATABASE.items():
        if brand in text_lower:
            return info
    return None


def get_category_fallback(category: str):
    """Get category icon as fallback."""
    cat_lower = category.lower()
    for key, info in CATEGORY_ICONS.items():
        if key in cat_lower:
            return info
    return {"icon": "📦", "bg": "#6B7280"}


# Financial tips for the "Tip of the Day" card
TIPS = [
    "Prepare a Budget and Abide by it",
    "Track every expense, no matter how small",
    "Set savings goals and automate transfers",
    "Review your spending weekly",
    "Avoid impulse purchases - wait 24 hours",
    "Use the 50/30/20 budgeting rule",
    "Build an emergency fund first",
    "Cut subscriptions you don't use",
]


def create_circular_gauge(balance: float, total_budget: float = 100000, size: int = 220, theme=None):
    """
    Creates a modern circular gauge with multi-colored arcs.
    The colored portion represents the remaining balance percentage.
    When expenses reduce balance, the colored arc shrinks.
    """
    
    # Get theme colors (use defaults if not provided)
    if theme is None:
        from core.theme import get_theme
        theme = get_theme()
    
    bg_ring_color = "#1a2744" if theme.is_dark else "#E2E8F0"
    outer_glow_color = "#0d1829" if theme.is_dark else "#F1F5F9"
    label_color = theme.text_secondary
    
    # Calculate percentage (0.0 to 1.0)
    percent = max(0, min(balance / total_budget, 1.0)) if total_budget > 0 else 0
    
    # Gauge parameters
    stroke_width = 22
    radius = (size - stroke_width) / 2 - 15
    center = size / 2
    
    arc_controls = []
    
    # Outer glow ring (subtle decorative ring)
    outer_radius = radius + 18
    for i in range(72):
        angle = math.radians(i * 5)
        x = center + outer_radius * math.cos(angle) - 4
        y = center + outer_radius * math.sin(angle) - 4
        arc_controls.append(
            ft.Container(
                width=8,
                height=8,
                border_radius=4,
                bgcolor=outer_glow_color,
                left=x,
                top=y,
            )
        )
    
    # Background ring (dark - full circle)
    for i in range(72):
        angle = math.radians(i * 5)
        x = center + radius * math.cos(angle) - stroke_width / 2
        y = center + radius * math.sin(angle) - stroke_width / 2
        arc_controls.append(
            ft.Container(
                width=stroke_width,
                height=stroke_width,
                border_radius=stroke_width / 2,
                bgcolor=bg_ring_color,
                left=x,
                top=y,
            )
        )
    
    # Calculate how much of the circle to fill (full circle = 360°)
    # We use 270° as "full" so there's always a gap at top-left
    max_arc_degrees = 300  # Maximum arc coverage
    filled_degrees = int(max_arc_degrees * percent)
    
    # Start from bottom (180°) and go clockwise
    start_angle = 120  # Start position
    
    if filled_degrees > 0:
        # Create the colored progress arc
        segments = max(1, filled_degrees // 3)  # Optimize: fewer segments
        
        for i in range(segments + 1):
            progress = i / segments if segments > 0 else 0
            angle_deg = start_angle + (filled_degrees * progress)
            angle = math.radians(angle_deg)
            
            x = center + radius * math.cos(angle) - stroke_width / 2
            y = center + radius * math.sin(angle) - stroke_width / 2
            
            # Color gradient based on position in the arc
            # Purple -> Blue -> Cyan -> Green
            total_progress = progress
            if total_progress < 0.25:
                color = "#7c3aed"  # Purple
            elif total_progress < 0.45:
                color = "#6366f1"  # Blue/Indigo
            elif total_progress < 0.65:
                color = "#06b6d4"  # Cyan
            elif total_progress < 0.85:
                color = "#10b981"  # Green
            else:
                color = "#34d399"  # Light green
            
            arc_controls.append(
                ft.Container(
                    width=stroke_width,
                    height=stroke_width,
                    border_radius=stroke_width / 2,
                    bgcolor=color,
                    left=x,
                    top=y,
                )
            )
        
        # Add glow at the start (purple)
        glow_angle = math.radians(start_angle)
        glow_x = center + radius * math.cos(glow_angle) - 14
        glow_y = center + radius * math.sin(glow_angle) - 14
        arc_controls.append(
            ft.Container(
                width=28,
                height=28,
                border_radius=14,
                bgcolor="#7c3aed",
                opacity=0.5,
                left=glow_x,
                top=glow_y,
            )
        )
        
        # Add glow at the end
        end_angle = math.radians(start_angle + filled_degrees)
        glow_x = center + radius * math.cos(end_angle) - 14
        glow_y = center + radius * math.sin(end_angle) - 14
        # End color based on how far we got
        if percent > 0.85:
            end_color = "#34d399"
        elif percent > 0.65:
            end_color = "#10b981"
        elif percent > 0.45:
            end_color = "#06b6d4"
        else:
            end_color = "#6366f1"
        arc_controls.append(
            ft.Container(
                width=28,
                height=28,
                border_radius=14,
                bgcolor=end_color,
                opacity=0.5,
                left=glow_x,
                top=glow_y,
            )
        )
    
    # Percentage text color based on balance
    if percent > 0.5:
        balance_color = theme.text_primary
    elif percent > 0.25:
        balance_color = "#fbbf24"  # Yellow warning
    else:
        balance_color = "#ef4444"  # Red danger
    
    return ft.Stack(
        controls=[
            # Arc segments container
            ft.Container(
                content=ft.Stack(controls=arc_controls),
                width=size,
                height=size,
            ),
            # Center text
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"₱{balance:,.2f}", 
                            size=24, 
                            weight=ft.FontWeight.BOLD, 
                            color=balance_color,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Available balance", 
                            size=12, 
                            color=label_color,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4,
                ),
                width=size,
                height=size,
                alignment=ft.alignment.center,
            ),
        ],
        width=size,
        height=size,
    )


def create_expense_item(brand_text: str, category: str, date: str, amount: float, on_click=None):
    """Creates a single expense item row with brand logos."""
    # Format amount with sign
    amount_str = f"-₱{abs(amount):,.2f}" if amount < 0 else f"+₱{amount:,.2f}"
    amount_color = "#EF4444" if amount < 0 else "#10B981"
    amount_bg = "#3D1515" if amount < 0 else "#0D3D2E"
    
    # Get brand info first, then category fallback
    brand_info = get_brand_info(brand_text)
    
    if brand_info:
        # Check if we have a logo URL
        if "logo" in brand_info and brand_info["logo"]:
            icon_container = ft.Container(
                content=ft.Image(
                    src=brand_info["logo"],
                    width=26,
                    height=26,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text(
                        brand_info["icon"],
                        size=16,
                        color=brand_info.get("text", "white"),
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                width=44,
                height=44,
                border_radius=22,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
        else:
            icon_container = ft.Container(
                content=ft.Text(
                    brand_info["icon"],
                    size=18,
                    color=brand_info.get("text", "white"),
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                width=44,
                height=44,
                border_radius=22,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
    else:
        # Use category fallback
        cat_info = get_category_fallback(category)
        icon_container = ft.Container(
            content=ft.Text(
                cat_info["icon"],
                size=20,
                text_align=ft.TextAlign.CENTER,
            ),
            width=44,
            height=44,
            border_radius=22,
            bgcolor=cat_info["bg"],
            alignment=ft.alignment.center,
        )
    
    # Amount badge with pill shape
    amount_badge = ft.Container(
        content=ft.Text(
            amount_str,
            size=12,
            weight=ft.FontWeight.W_600,
            color=amount_color,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=amount_bg,
    )
    
    return ft.Container(
        content=ft.Row(
            controls=[
                icon_container,
                ft.Container(width=8),
                # Title and date
                ft.Column(
                    controls=[
                        ft.Text(brand_text, size=14, weight=ft.FontWeight.W_500, color="white"),
                        ft.Text(date, size=12, color="#6B7280"),
                    ],
                    spacing=2,
                    expand=True,
                ),
                amount_badge,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=8, horizontal=4),
        on_click=on_click,
        ink=True,
        border_radius=8,
    )


def create_home_view(page: ft.Page, state: dict, toast, show_dashboard, logout_callback,
                     show_wallet_cb=None, show_profile_cb=None, show_add_expense_cb=None):
    """
    Creates a modern home view with circular gauge, tips, and expense list.
    state is a dict with 'user_id' and 'editing_id' keys (mutable).
    """
    
    expenses_list = ft.Column(spacing=4)
    gauge_container = ft.Container()
    
    def format_date(date_str: str) -> str:
        """Format date string to display format."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y")
        except:
            return date_str
    
    def load_expenses():
        """Load and display expenses."""
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        # Show only recent 5 expenses on home
        for r in rows[:5]:
            eid, uid, amt, cat, dsc, dtt = r
            display_name = dsc if dsc else cat
            
            expenses_list.controls.append(
                create_expense_item(
                    brand_text=display_name,
                    category=cat,
                    date=format_date(dtt),
                    amount=-amt,  # Expenses are negative
                )
            )
        
        if not rows:
            expenses_list.controls.append(
                ft.Container(
                    content=ft.Text("No expenses yet. Tap + to add one!", color="#6B7280", size=14),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            )
        
        page.update()
    
    def refresh_balance():
        """Refresh the balance gauge."""
        total = db.total_expenses_by_user(state["user_id"])
        # Budget is 100,000 - expenses reduce the balance
        total_budget = 100000
        balance = total_budget - total
        gauge_container.content = create_circular_gauge(balance if balance > 0 else 0, total_budget)
        page.update()
    
    def show_add_expense(e):
        """Navigate to add expense page."""
        if show_add_expense_cb:
            show_add_expense_cb()
    
    def show_all_expenses(e):
        """Navigate to all expenses page."""
        from ui.all_expenses_page import create_all_expenses_view
        all_view = create_all_expenses_view(page, state, toast, show_view)
        all_view()
    
    def show_wallet(e):
        """Navigate to wallet page."""
        if show_wallet_cb:
            show_wallet_cb()
    
    def show_profile(e):
        """Navigate to profile page."""
        if show_profile_cb:
            show_profile_cb()
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Get random tip
        tip = random.choice(TIPS)
        
        # Refresh data
        total_budget = 100000
        total = db.total_expenses_by_user(state["user_id"])
        balance = total_budget - total
        gauge_container.content = create_circular_gauge(balance if balance > 0 else 0, total_budget, theme=theme)
        load_expenses()
        
        # Header with title and profile
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Home", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=ft.CircleAvatar(
                            foreground_image_src="/assets/icon.png",
                            bgcolor=theme.accent_primary,
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                            radius=22,
                        ),
                        on_click=show_profile,
                        ink=True,
                        border_radius=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=10),
        )
        
        # Circular gauge section
        gauge_section = ft.Container(
            content=gauge_container,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=20),
        )
        
        # Tip of the day card
        tip_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Tip of the Day", size=12, color=theme.text_secondary),
                    ft.Container(height=4),
                    ft.Row(
                        controls=[
                            ft.Text(tip, size=14, color=theme.text_primary, expand=True),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Expenses section header
        expenses_header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Expenses", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=ft.Text("See all", size=14, color=theme.accent_primary),
                        on_click=show_all_expenses,
                        ink=True,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=8,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        
        # Expenses list container (just the list, header is separate now)
        # expenses_list is already defined at the top
        
        # Main content - scrollable area
        scrollable_content = ft.Column(
            controls=[
                gauge_section,
                ft.Container(height=16),
                tip_card,
                ft.Container(height=24),
                expenses_header,
                ft.Container(height=8),
                expenses_list,
                ft.Container(height=80),  # Space for bottom nav
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
                active_index=0,  # Home is active
                on_home=None,  # Already on home
                on_expenses=lambda: show_dashboard(),
                on_wallet=lambda: show_wallet(None),
                on_profile=lambda: show_profile(None),
                on_fab_click=lambda: show_add_expense(None),
                theme=theme,
            )
        )
        
        page.update()
    
    return show_view
