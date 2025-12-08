# src/ui/home_page.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav
from utils.currency import format_currency, format_currency_short, get_currency_from_user_profile, get_currency_symbol
from components.notification import NotificationCenter, NotificationHistory
from components.enhanced_icons import EnhancedIcon, CategoryIcon, EnhancedIconButton
import random
import math


def get_time_based_greeting():
    """Get greeting based on current time of day."""
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    elif 18 <= current_hour < 22:
        return "Good Evening"
    else:
        return "Welcome back"


def get_clearbit_logo(domain: str) -> str:
    """Get brand logo URL from Clearbit API."""
    return f"https://logo.clearbit.com/{domain}"


# Brand database for recognition - using Clearbit Logo API for clear, high-quality logos
BRAND_DATABASE = {
    # Shopping & E-commerce
    "amazon": {"icon": "a", "color": "#FF9900", "bg": "#232F3E", "text": "white", "logo": get_clearbit_logo("amazon.com")},
    "shopee": {"icon": "🛒", "color": "#EE4D2D", "bg": "#EE4D2D", "text": "white", "logo": get_clearbit_logo("shopee.com")},
    "lazada": {"icon": "L", "color": "#0F146D", "bg": "#0F146D", "text": "white", "logo": get_clearbit_logo("lazada.com")},
    "zalora": {"icon": "Z", "color": "#000000", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("zalora.com")},
    "ebay": {"icon": "e", "color": "#E53238", "bg": "#FFFFFF", "text": "#E53238", "logo": get_clearbit_logo("ebay.com")},
    
    # Food & Restaurants
    "mcdonalds": {"icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C", "logo": get_clearbit_logo("mcdonalds.com")},
    "mcdonald's": {"icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C", "logo": get_clearbit_logo("mcdonalds.com")},
    "starbucks": {"icon": "☕", "color": "#00704A", "bg": "#00704A", "text": "white", "logo": get_clearbit_logo("starbucks.com")},
    "jollibee": {"icon": "🐝", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": get_clearbit_logo("jollibee.com.ph")},
    "kfc": {"icon": "🍗", "color": "#F40027", "bg": "#F40027", "text": "white", "logo": get_clearbit_logo("kfc.com")},
    "burger king": {"icon": "🍔", "color": "#FF8732", "bg": "#502314", "text": "#FF8732", "logo": get_clearbit_logo("bk.com")},
    "pizza hut": {"icon": "🍕", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": get_clearbit_logo("pizzahut.com")},
    "subway": {"icon": "🥪", "color": "#008C15", "bg": "#FFC600", "text": "#008C15", "logo": get_clearbit_logo("subway.com")},
    "dunkin": {"icon": "🍩", "color": "#FF671F", "bg": "#FF671F", "text": "white", "logo": get_clearbit_logo("dunkindonuts.com")},
    "chowking": {"icon": "🥡", "color": "#E31837", "bg": "#E31837", "text": "white", "logo": get_clearbit_logo("chowkingdelivery.com")},
    "greenwich": {"icon": "🍕", "color": "#006B3F", "bg": "#006B3F", "text": "white", "logo": get_clearbit_logo("greenwichdelivery.com")},
    "mang inasal": {"icon": "🍗", "color": "#FDB813", "bg": "#FDB813", "text": "#1E1E1E", "logo": get_clearbit_logo("manginasal.com")},
    
    # Tech & Electronics
    "apple": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("apple.com")},
    "ipad": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("apple.com")},
    "iphone": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("apple.com")},
    "macbook": {"icon": "", "color": "#555555", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("apple.com")},
    "samsung": {"icon": "S", "color": "#1428A0", "bg": "#1428A0", "text": "white", "logo": get_clearbit_logo("samsung.com")},
    "google": {"icon": "G", "color": "#4285F4", "bg": "#FFFFFF", "text": "#4285F4", "logo": get_clearbit_logo("google.com")},
    "microsoft": {"icon": "⊞", "color": "#00A4EF", "bg": "#737373", "text": "white", "logo": get_clearbit_logo("microsoft.com")},
    "sony": {"icon": "S", "color": "#000000", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("sony.com")},
    "xiaomi": {"icon": "Mi", "color": "#FF6900", "bg": "#FF6900", "text": "white", "logo": get_clearbit_logo("mi.com")},
    "huawei": {"icon": "H", "color": "#FF0000", "bg": "#FF0000", "text": "white", "logo": get_clearbit_logo("huawei.com")},
    
    # Finance & Payment
    "gcash": {"icon": "G", "color": "#007DFE", "bg": "#007DFE", "text": "white", "logo": get_clearbit_logo("gcash.com")},
    "maya": {"icon": "M", "color": "#00D66C", "bg": "#00D66C", "text": "white", "logo": get_clearbit_logo("maya.ph")},
    "bpi": {"icon": "B", "color": "#9E1B34", "bg": "#9E1B34", "text": "white", "logo": get_clearbit_logo("bpi.com.ph")},
    "bdo": {"icon": "B", "color": "#003478", "bg": "#003478", "text": "white", "logo": get_clearbit_logo("bdo.com.ph")},
    "paypal": {"icon": "P", "color": "#003087", "bg": "#003087", "text": "white", "logo": get_clearbit_logo("paypal.com")},
    
    # Streaming & Entertainment
    "netflix": {"icon": "N", "color": "#E50914", "bg": "#000000", "text": "#E50914", "logo": get_clearbit_logo("netflix.com")},
    "spotify": {"icon": "♪", "color": "#1DB954", "bg": "#191414", "text": "#1DB954", "logo": get_clearbit_logo("spotify.com")},
    "youtube": {"icon": "▶", "color": "#FF0000", "bg": "#282828", "text": "#FF0000", "logo": get_clearbit_logo("youtube.com")},
    "disney": {"icon": "D", "color": "#113CCF", "bg": "#040814", "text": "white", "logo": get_clearbit_logo("disneyplus.com")},
    
    # Transport
    "grab": {"icon": "G", "color": "#00B14F", "bg": "#00B14F", "text": "white", "logo": get_clearbit_logo("grab.com")},
    "uber": {"icon": "U", "color": "#000000", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("uber.com")},
    "angkas": {"icon": "A", "color": "#F16521", "bg": "#F16521", "text": "white", "logo": get_clearbit_logo("angkas.com")},
    "shell": {"icon": "🐚", "color": "#FBCE07", "bg": "#DD1D21", "text": "#FBCE07", "logo": get_clearbit_logo("shell.com")},
    "petron": {"icon": "P", "color": "#1E4D8C", "bg": "#1E4D8C", "text": "white", "logo": get_clearbit_logo("petron.com")},
    "caltex": {"icon": "★", "color": "#E31937", "bg": "#E31937", "text": "white", "logo": get_clearbit_logo("caltex.com")},
    "foodpanda": {"icon": "🐼", "color": "#D70F64", "bg": "#D70F64", "text": "white", "logo": get_clearbit_logo("foodpanda.com")},
    
    # Utilities
    "meralco": {"icon": "⚡", "color": "#FF6B00", "bg": "#FF6B00", "text": "white", "logo": get_clearbit_logo("meralco.com.ph")},
    "pldt": {"icon": "P", "color": "#E31937", "bg": "#E31937", "text": "white", "logo": get_clearbit_logo("pldthome.com")},
    "globe": {"icon": "G", "color": "#0056A3", "bg": "#0056A3", "text": "white", "logo": get_clearbit_logo("globe.com.ph")},
    "smart": {"icon": "S", "color": "#00913A", "bg": "#00913A", "text": "white", "logo": get_clearbit_logo("smart.com.ph")},
    "maynilad": {"icon": "M", "color": "#0072CE", "bg": "#0072CE", "text": "white", "logo": get_clearbit_logo("mayniladwater.com.ph")},
    "converge": {"icon": "C", "color": "#FF6600", "bg": "#FF6600", "text": "white", "logo": get_clearbit_logo("convergeict.com")},
    
    # Retail & Supermarkets
    "sm": {"icon": "SM", "color": "#003DA5", "bg": "#003DA5", "text": "white", "logo": get_clearbit_logo("smsupermalls.com")},
    "robinsons": {"icon": "R", "color": "#00529B", "bg": "#00529B", "text": "white", "logo": get_clearbit_logo("robinsonsmalls.com")},
    "uniqlo": {"icon": "U", "color": "#FF0000", "bg": "#FFFFFF", "text": "#FF0000", "logo": get_clearbit_logo("uniqlo.com")},
    "h&m": {"icon": "H&M", "color": "#E50010", "bg": "#FFFFFF", "text": "#E50010", "logo": get_clearbit_logo("hm.com")},
    "nike": {"icon": "✓", "color": "#111111", "bg": "#111111", "text": "white", "logo": get_clearbit_logo("nike.com")},
    "adidas": {"icon": "⫿", "color": "#000000", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("adidas.com")},
    "zara": {"icon": "Z", "color": "#000000", "bg": "#000000", "text": "white", "logo": get_clearbit_logo("zara.com")},
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


def create_circular_gauge(balance: float, total_budget: float = 100000, size: int = 250, theme=None, account_name: str = None, user_currency: str = "PHP"):
    """
    Creates a premium circular gauge with smooth gradient arc and glassmorphism effect.
    The colored portion represents the remaining balance percentage.
    """
    
    # Get theme colors (use defaults if not provided)
    if theme is None:
        from core.theme import get_theme
        theme = get_theme()
    
    is_dark = theme.is_dark
    
    # Premium color palette
    bg_ring_color = "#1e293b" if is_dark else "#e2e8f0"
    inner_shadow_color = "#0f172a" if is_dark else "#cbd5e1"
    label_color = theme.text_secondary
    
    # Calculate percentage (0.0 to 1.0)
    percent = max(0, min(balance / total_budget, 1.0)) if total_budget > 0 else 0
    spent = total_budget - balance
    
    # Gauge parameters - slightly thicker for premium look
    stroke_width = 18
    radius = (size - stroke_width) / 2 - 20
    center = size / 2
    
    arc_controls = []
    
    # Outer decorative ring with subtle gradient dots
    outer_radius = radius + 28
    for i in range(60):
        angle = math.radians(i * 6 - 90)  # Start from top
        x = center + outer_radius * math.cos(angle) - 2
        y = center + outer_radius * math.sin(angle) - 2
        # Subtle pulsing opacity effect
        dot_opacity = 0.15 + (0.1 * math.sin(i * 0.3))
        arc_controls.append(
            ft.Container(
                width=4,
                height=4,
                border_radius=2,
                bgcolor="#64748b" if is_dark else "#94a3b8",
                opacity=dot_opacity,
                left=x,
                top=y,
            )
        )
    
    # Inner shadow ring for depth effect
    inner_shadow_radius = radius - 8
    for i in range(48):
        angle = math.radians(i * 7.5 - 90)
        x = center + inner_shadow_radius * math.cos(angle) - 3
        y = center + inner_shadow_radius * math.sin(angle) - 3
        arc_controls.append(
            ft.Container(
                width=6,
                height=6,
                border_radius=3,
                bgcolor=inner_shadow_color,
                opacity=0.3,
                left=x,
                top=y,
            )
        )
    
    # Background ring (full circle with subtle texture)
    for i in range(90):
        angle = math.radians(i * 4 - 90)
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
    
    # Progress arc - starts from top (-90°) and goes clockwise
    max_arc_degrees = 360
    filled_degrees = int(max_arc_degrees * percent)
    start_angle = -90  # Start from top
    
    # Premium gradient colors based on health status
    if percent > 0.6:
        # Healthy - Green gradient
        gradient_colors = ["#22c55e", "#16a34a", "#15803d", "#166534"]
        glow_color = "#22c55e"
        status_icon = "✓"
        status_text = "Healthy"
    elif percent > 0.3:
        # Warning - Amber gradient
        gradient_colors = ["#f59e0b", "#d97706", "#b45309", "#92400e"]
        glow_color = "#f59e0b"
        status_icon = "!"
        status_text = "Caution"
    else:
        # Critical - Red gradient
        gradient_colors = ["#ef4444", "#dc2626", "#b91c1c", "#991b1b"]
        glow_color = "#ef4444"
        status_icon = "⚠"
        status_text = "Low"
    
    if filled_degrees > 0:
        # Create smooth progress arc with gradient
        segments = max(1, filled_degrees)  # More segments for smoother arc
        
        for i in range(0, segments + 1, 2):  # Step by 2 for performance
            progress = i / max_arc_degrees  # Progress through full circle
            angle_deg = start_angle + i
            angle = math.radians(angle_deg)
            
            x = center + radius * math.cos(angle) - stroke_width / 2
            y = center + radius * math.sin(angle) - stroke_width / 2
            
            # Smooth color interpolation
            color_index = min(int(progress * len(gradient_colors)), len(gradient_colors) - 1)
            color = gradient_colors[color_index]
            
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
        
        # Glowing end cap
        end_angle = math.radians(start_angle + filled_degrees)
        cap_x = center + radius * math.cos(end_angle)
        cap_y = center + radius * math.sin(end_angle)
        
        # Outer glow
        arc_controls.append(
            ft.Container(
                width=32,
                height=32,
                border_radius=16,
                bgcolor=glow_color,
                opacity=0.25,
                left=cap_x - 16,
                top=cap_y - 16,
            )
        )
        
        # Inner glow
        arc_controls.append(
            ft.Container(
                width=24,
                height=24,
                border_radius=12,
                bgcolor=glow_color,
                opacity=0.4,
                left=cap_x - 12,
                top=cap_y - 12,
            )
        )
        
        # Bright cap
        arc_controls.append(
            ft.Container(
                width=stroke_width + 4,
                height=stroke_width + 4,
                border_radius=(stroke_width + 4) / 2,
                bgcolor=gradient_colors[0],
                border=ft.border.all(2, "#ffffff" if is_dark else "#f8fafc"),
                left=cap_x - (stroke_width + 4) / 2,
                top=cap_y - (stroke_width + 4) / 2,
            )
        )
    
    # Text color based on balance health
    if percent > 0.5:
        balance_color = "#22c55e" if is_dark else "#16a34a"
    elif percent > 0.25:
        balance_color = "#f59e0b"
    else:
        balance_color = "#ef4444"
    
    # Format balance for display using currency utilities
    balance_display = format_currency_short(balance, user_currency)
    
    # Center glassmorphism container
    center_bg = ft.Container(
        width=size - 100,
        height=size - 100,
        border_radius=(size - 100) / 2,
        bgcolor="#1e293b" if is_dark else "#ffffff",
        border=ft.border.all(1, "#334155" if is_dark else "#e2e8f0"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color="#00000033",
            offset=ft.Offset(0, 4),
        ),
    )
    
    # Build center content
    center_content = ft.Column(
        controls=[
            # Status indicator
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=8,
                            height=8,
                            border_radius=4,
                            bgcolor=glow_color if filled_degrees > 0 else "#64748b",
                        ),
                        ft.Text(
                            status_text if filled_degrees > 0 else "Empty",
                            size=11,
                            weight=ft.FontWeight.W_600,
                            color=glow_color if filled_degrees > 0 else "#64748b",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4,
                ),
                margin=ft.margin.only(bottom=4),
            ),
            # Main balance amount
            ft.Text(
                balance_display,
                size=32,
                weight=ft.FontWeight.BOLD,
                color=theme.text_primary,
                text_align=ft.TextAlign.CENTER,
            ),
            # Account name
            ft.Text(
                account_name or "Cash",
                size=14,
                weight=ft.FontWeight.W_600,
                color=label_color,
                text_align=ft.TextAlign.CENTER,
            ),
            # Subtitle
            ft.Text(
                "Available Balance",
                size=10,
                color=label_color,
                text_align=ft.TextAlign.CENTER,
                opacity=0.7,
            ),
            # Percentage indicator
            ft.Container(
                content=ft.Text(
                    f"{int(percent * 100)}% remaining",
                    size=10,
                    weight=ft.FontWeight.W_500,
                    color=balance_color,
                ),
                bgcolor=f"{balance_color}15",
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                margin=ft.margin.only(top=6),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )
    
    return ft.Stack(
        controls=[
            # Arc segments container
            ft.Container(
                content=ft.Stack(controls=arc_controls),
                width=size,
                height=size,
            ),
            # Center background
            ft.Container(
                content=center_bg,
                width=size,
                height=size,
                alignment=ft.alignment.center,
            ),
            # Center text content
            ft.Container(
                content=center_content,
                width=size,
                height=size,
                alignment=ft.alignment.center,
            ),
        ],
        width=size,
        height=size,
    )


def create_user_avatar(user_id: int, radius: int = 22, theme=None):
    """Create a user avatar based on their profile settings."""
    if theme is None:
        theme = get_theme()
    
    user_profile = db.get_user_profile(user_id)
    photo = user_profile.get("photo") if user_profile else None
    
    if photo and isinstance(photo, dict):
        photo_type = photo.get("type", "default")
        photo_value = photo.get("value")
        photo_bg = photo.get("bg")
        
        if photo_type == "avatar" and photo_value:
            # Emoji avatar
            return ft.Container(
                content=ft.Text(photo_value, size=radius * 0.9),
                width=radius * 2,
                height=radius * 2,
                bgcolor=photo_bg or theme.accent_primary,
                border_radius=radius,
                alignment=ft.alignment.center,
            )
        elif photo_type == "file" and photo_value:
            # Custom uploaded image
            return ft.Container(
                content=ft.Image(
                    src_base64=photo_value,
                    width=radius * 2 - 4,
                    height=radius * 2 - 4,
                    fit=ft.ImageFit.COVER,
                    border_radius=radius - 2,
                ),
                width=radius * 2,
                height=radius * 2,
                bgcolor="transparent",
                border_radius=radius,
                alignment=ft.alignment.center,
            )
    
    # Default avatar with user icon
    return ft.CircleAvatar(
        bgcolor=theme.accent_primary,
        content=ft.Icon(ft.Icons.PERSON, color="white", size=radius * 0.8),
        radius=radius,
    )


def create_expense_item(brand_text: str, category: str, date: str, amount: float, on_click=None, theme=None, account_name: str = None, user_currency: str = "PHP"):
    """Creates a modern expense item row with brand logos and theme support."""
    from core.theme import get_theme
    if theme is None:
        theme = get_theme()
    
    # Format amount with sign and determine colors
    is_expense = amount < 0
    currency_symbol = get_currency_symbol(user_currency)
    amount_str = f"-{currency_symbol}{abs(amount):,.2f}" if is_expense else f"+{currency_symbol}{amount:,.2f}"
    
    # Theme-aware colors
    if is_expense:
        amount_color = "#EF4444"  # Red for expenses
        amount_bg = "#3D1515" if theme.is_dark else "#FEE2E2"
    else:
        amount_color = "#10B981"  # Green for income
        amount_bg = "#0D3D2E" if theme.is_dark else "#D1FAE5"
    
    # Get brand info first, then category fallback
    brand_info = get_brand_info(brand_text)
    
    if brand_info:
        # Check if we have a logo URL
        if "logo" in brand_info and brand_info["logo"]:
            # Enhanced white background for brand logos with shadow
            icon_container = ft.Container(
                content=ft.Container(
                    content=ft.Image(
                        src=brand_info["logo"],
                        width=30,
                        height=30,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text(
                            brand_info["icon"],
                            size=16,
                            color=brand_info.get("text", "white"),
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                    width=38,
                    height=38,
                    border_radius=8,
                    bgcolor="#FFFFFF",
                    alignment=ft.alignment.center,
                ),
                width=46,
                height=46,
                border_radius=12,
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    offset=ft.Offset(0, 2),
                    color="#00000015",
                ),
                alignment=ft.alignment.center,
            )
        else:
            # Enhanced branded icon with shadow
            icon_container = ft.Container(
                content=ft.Text(
                    brand_info["icon"],
                    size=18,
                    color=brand_info.get("text", "white"),
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                width=46,
                height=46,
                border_radius=14,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    offset=ft.Offset(0, 2),
                    color="#00000020",
                ),
            )
    else:
        # Use CategoryIcon for category fallback
        icon_container = CategoryIcon.create(
            category=category,
            size=46,
            theme=theme,
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
    
    # Account badge
    account_badge = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=10, color=theme.accent_primary),
        ft.Text(account_name or "Cash", size=10, color=theme.accent_primary, weight=ft.FontWeight.W_500),
    ], spacing=3, tight=True) if account_name else ft.Container()
    
    return ft.Container(
        content=ft.Row(
            controls=[
                icon_container,
                ft.Container(width=10),
                # Title and date
                ft.Column(
                    controls=[
                        ft.Text(
                            brand_text, 
                            size=14, 
                            weight=ft.FontWeight.W_500, 
                            color=theme.text_primary,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(date, size=11, color=theme.text_muted),
                    ],
                    spacing=2,
                    expand=True,
                ),
                # Amount and Account badge - fixed position right side
                ft.Column([
                    amount_badge,
                    account_badge,
                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=10, horizontal=8),
        on_click=on_click,
        ink=True,
        border_radius=12,
        bgcolor=theme.bg_card,
    )


def create_home_view(page: ft.Page, state: dict, toast, show_dashboard, logout_callback,
                     show_wallet_cb=None, show_profile_cb=None, show_add_expense_cb=None):
    """
    Creates a modern home view with circular gauge, tips, and expense list.
    state is a dict with 'user_id' and 'editing_id' keys (mutable).
    """
    
    expenses_list = ft.Column(spacing=4)
    gauge_container = ft.Container()
    
    # Get user's currency preference
    user_profile = db.get_user_profile(state["user_id"])
    user_currency = get_currency_from_user_profile(user_profile)
    
    def format_date(date_str: str) -> str:
        """Format date string to display format."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y")
        except:
            return date_str
    
    def load_expenses():
        """Load and display expenses."""
        theme = get_theme()
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        # Cache for account currencies
        currency_cache = {}
        def get_expense_currency(acc_id):
            if acc_id is None:
                return "PHP"
            if acc_id not in currency_cache:
                acc = db.get_account_by_id(acc_id, state["user_id"])
                currency_cache[acc_id] = acc[5] if acc else "PHP"
            return currency_cache[acc_id]
        
        # Show only recent 5 expenses on home
        for r in rows[:5]:
            # Unpack with account_id (position 6)
            eid, uid, amt, cat, dsc, dtt, acc_id = r[:7]
            display_name = dsc if dsc else cat
            expense_currency = get_expense_currency(acc_id)
            
            expenses_list.controls.append(
                create_expense_item(
                    brand_text=display_name,
                    category=cat,
                    date=format_date(dtt),
                    amount=-amt,  # Expenses are negative
                    user_currency=expense_currency,
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
        # Get the selected account (or primary if none selected)
        selected_account = db.get_selected_account(state["user_id"])
        
        if selected_account:
            account_id = selected_account[0]
            current_balance = selected_account[4]  # Current balance
            account_currency = selected_account[5]  # Get account's currency
            state["selected_account_name"] = selected_account[1]
            state["selected_account_id"] = account_id
            
            # Calculate original budget
            account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
            original_budget = current_balance + account_expenses
        else:
            # Fallback to primary account
            primary_account = db.get_primary_account(state["user_id"])
            if primary_account:
                account_id = primary_account[0]
                current_balance = primary_account[4]
                account_currency = primary_account[5]  # Get account's currency
                state["selected_account_name"] = primary_account[1]
                account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
                original_budget = current_balance + account_expenses
            else:
                # Get first available account instead of summing all
                all_accounts = db.get_accounts_by_user(state["user_id"])
                if all_accounts:
                    first_account = all_accounts[0]
                    account_id = first_account[0]
                    current_balance = first_account[4]
                    account_currency = first_account[5]  # Get account's currency
                    state["selected_account_name"] = first_account[1]
                    account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
                    original_budget = current_balance + account_expenses
                else:
                    current_balance = 0
                    original_budget = 100000
                    account_currency = user_currency  # Use user's default
                    state["selected_account_name"] = "Cash"
        
        account_name = state.get("selected_account_name", "Cash")
        gauge_container.content = create_circular_gauge(
            balance=current_balance if current_balance > 0 else 0, 
            total_budget=original_budget if original_budget > 0 else 100000, 
            account_name=account_name,
            user_currency=account_currency
        )
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
        
        # Create notification center and store in state
        if "notification_center" not in state:
            state["notification_center"] = NotificationCenter(page, theme)
        notification_center = state["notification_center"]
        
        # Load user notifications from database
        NotificationHistory.load_user_notifications(state["user_id"])
        
        # Get random tip
        tip = random.choice(TIPS)
        
        # Get the selected account (or primary if none selected)
        selected_account = db.get_selected_account(state["user_id"])
        
        if selected_account:
            account_id = selected_account[0]
            selected_account_name = selected_account[1]
            current_balance = selected_account[4]  # Current balance (already has expenses deducted)
            account_currency = selected_account[5]  # Get account's currency
            
            # Calculate original budget = current balance + expenses spent from this account
            account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
            original_budget = current_balance + account_expenses
            
            state["selected_account_id"] = account_id
            state["selected_account_name"] = selected_account_name
        else:
            # Fallback to primary account
            primary_account = db.get_primary_account(state["user_id"])
            if primary_account:
                account_id = primary_account[0]
                selected_account_name = primary_account[1]
                current_balance = primary_account[4]
                account_currency = primary_account[5]  # Get account's currency
                account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
                original_budget = current_balance + account_expenses
            else:
                # Get first available account instead of summing all
                all_accounts = db.get_accounts_by_user(state["user_id"])
                if all_accounts:
                    first_account = all_accounts[0]
                    account_id = first_account[0]
                    selected_account_name = first_account[1]
                    current_balance = first_account[4]
                    account_currency = first_account[5]  # Get account's currency
                    account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
                    original_budget = current_balance + account_expenses
                else:
                    selected_account_name = "Cash"
                    current_balance = 0
                    original_budget = 100000  # Default fallback
                    account_currency = user_currency  # Use user's default
        
        # Create gauge: current_balance is what's remaining, original_budget is the max
        gauge_container.content = create_circular_gauge(
            balance=current_balance if current_balance > 0 else 0, 
            total_budget=original_budget if original_budget > 0 else 100000, 
            theme=theme, 
            account_name=selected_account_name,
            user_currency=account_currency
        )
        load_expenses()
        
        # Header with title and profile
        user_avatar = create_user_avatar(state["user_id"], radius=22, theme=theme)
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Home", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=user_avatar,
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
        
        # Tip of the day card with enhanced icon
        tip_card = ft.Container(
            content=ft.Row(
                controls=[
                    # Enhanced tip icon with gradient
                    EnhancedIcon.create(
                        icon=ft.Icons.LIGHTBULB_ROUNDED,
                        size=22,
                        color="#FFFFFF",
                        gradient=["#FCD34D", "#F59E0B"],
                        border_radius=10,
                        padding=9,
                        shadow=True,
                    ),
                    ft.Container(width=12),
                    # Tip content
                    ft.Column(
                        controls=[
                            ft.Text("Tip of the Day", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                            ft.Text(
                                tip, 
                                size=13, 
                                color=theme.text_primary,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    EnhancedIcon.create(
                        icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
                        size=18,
                        color=theme.text_muted,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=14,
            border_radius=14,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Expenses section header
        expenses_header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Recent", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.Container(
                                content=ft.Text(
                                    str(len(db.select_expenses_by_user(state["user_id"]))),
                                    size=11,
                                    color="white",
                                    weight=ft.FontWeight.W_600,
                                ),
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                border_radius=10,
                                bgcolor=theme.accent_primary,
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("See all", size=13, color=theme.accent_primary, weight=ft.FontWeight.W_500),
                                EnhancedIcon.create(
                                    icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                                    size=12,
                                    color=theme.accent_primary,
                                ),
                            ],
                            spacing=4,
                        ),
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
        full_view = create_page_with_nav(
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
        
        page.add(full_view)
        page.update()
    
    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_home_content(page: ft.Page, state: dict, toast, 
                       show_dashboard, logout_callback, show_wallet_cb, 
                       show_profile_cb, show_add_expense_cb, show_all_expenses_cb=None):
    """
    Builds and returns home page content WITHOUT calling page.clean() or page.add().
    This is for flash-free navigation where main.py swaps container content.
    """
    theme = get_theme()
    
    # Create notification center and store in state
    if "notification_center" not in state:
        state["notification_center"] = NotificationCenter(page, theme)
    notification_center = state["notification_center"]
    
    # Load user notifications from database
    NotificationHistory.load_user_notifications(state["user_id"])
    
    expenses_list = ft.Column(spacing=4)
    
    def format_date(date_str: str) -> str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y")
        except:
            return date_str
    
    def show_all_expenses(e=None):
        if show_all_expenses_cb:
            show_all_expenses_cb()
        else:
            show_dashboard()
    
    def show_wallet(e=None):
        if show_wallet_cb:
            show_wallet_cb()
    
    def show_profile(e=None):
        if show_profile_cb:
            show_profile_cb()
    
    def show_add_expense(e=None):
        if show_add_expense_cb:
            show_add_expense_cb()
    
    # Get user profile for name and avatar
    user_profile = db.get_user_profile(state["user_id"])
    first_name = user_profile.get("first_name") or user_profile.get("firstName", "User") if user_profile else "User"
    last_name = user_profile.get("last_name") or user_profile.get("lastName", "") if user_profile else ""
    full_name = f"{first_name} {last_name}".strip() if last_name else first_name
    username = user_profile.get("username", f"user_{state['user_id']}") if user_profile else f"user_{state['user_id']}"
    
    # Get time-based greeting
    greeting = get_time_based_greeting()
    
    # Get user's default currency preference
    user_default_currency = get_currency_from_user_profile(user_profile)
    
    # Get selected account and balance data
    selected_account = db.get_selected_account(state["user_id"])
    if selected_account:
        account_id = selected_account[0]
        current_balance = selected_account[4]
        account_currency = selected_account[5]  # Get account's currency
        account_name = selected_account[1]
        account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
        original_budget = current_balance + account_expenses
        user_currency = account_currency  # Use account's currency
    else:
        primary_account = db.get_primary_account(state["user_id"])
        if primary_account:
            account_id = primary_account[0]
            current_balance = primary_account[4]
            account_currency = primary_account[5]  # Get account's currency
            account_name = primary_account[1]
            account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
            original_budget = current_balance + account_expenses
            user_currency = account_currency  # Use account's currency
        else:
            # Get first available account instead of defaulting to 0
            all_accounts = db.get_accounts_by_user(state["user_id"])
            if all_accounts:
                first_account = all_accounts[0]
                account_id = first_account[0]
                current_balance = first_account[4]
                account_currency = first_account[5]  # Get account's currency
                account_name = first_account[1]
                account_expenses = db.total_expenses_by_account(state["user_id"], account_id)
                original_budget = current_balance + account_expenses
                user_currency = account_currency  # Use account's currency
            else:
                account_name = "Cash"
                current_balance = 0
                original_budget = 100000
                user_currency = user_default_currency  # Fallback to user's default
    
    # Load expenses
    rows = db.select_expenses_by_user(state["user_id"])
    
    # Cache account names and currencies for efficiency
    account_cache = {}
    currency_cache = {}
    
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    def get_expense_currency(acc_id):
        """Get currency from the expense's original account"""
        if acc_id is None:
            return "PHP"
        if acc_id not in currency_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            currency_cache[acc_id] = acc[5] if acc else "PHP"
        return currency_cache[acc_id]
    
    for r in rows[:5]:
        eid, uid, amt, cat, dsc, dtt, acc_id = r[:7]
        display_name = dsc if dsc else cat
        acc_name = get_account_name(acc_id)
        expense_currency = get_expense_currency(acc_id)
        expenses_list.controls.append(
            create_expense_item(
                brand_text=display_name,
                category=cat,
                date=format_date(dtt),
                amount=-amt,
                theme=theme,
                account_name=acc_name,
                user_currency=expense_currency,
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
    
    # Create avatar
    user_avatar = create_user_avatar(state["user_id"], radius=22, theme=theme)
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(f"{greeting},", size=13, color=theme.text_secondary, weight=ft.FontWeight.W_400),
                        ft.Text(first_name, size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        notification_center.create_bell_icon(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        f"@{username}",
                                        size=12,
                                        color=theme.text_primary,
                                        weight=ft.FontWeight.W_500,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            padding=ft.padding.only(right=8),
                        ),
                        ft.Container(
                            content=user_avatar,
                            on_click=show_profile,
                            ink=True,
                            border_radius=22,
                        ),
                    ],
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(top=20, bottom=16),
    )
    
    # Gauge
    gauge = create_circular_gauge(
        balance=current_balance,
        total_budget=original_budget,
        account_name=account_name,
        user_currency=user_currency,
    )
    
    gauge_section = ft.Container(
        content=gauge,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=10, bottom=10),
    )
    
    # Tip card
    tips = [
        ("Track every expense!", "Small purchases add up fast."),
        ("Set a weekly budget", "Helps you stay on track."),
        ("Review monthly", "Spot trends in your spending."),
    ]
    tip = random.choice(tips)
    tip_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color="#FFC107", size=20),
                    bgcolor="#FFC10715",
                    border_radius=10,
                    padding=10,
                ),
                ft.Column(
                    controls=[
                        ft.Text(tip[0], size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                        ft.Text(tip[1], size=12, color=theme.text_secondary),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=12,
        ),
        bgcolor=theme.bg_card,
        border_radius=16,
        padding=16,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Expenses header
    expenses_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Recent Expenses", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("See all", size=13, color=theme.accent_primary, weight=ft.FontWeight.W_500),
                            ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=theme.accent_primary, size=12),
                        ],
                        spacing=4,
                    ),
                    on_click=show_all_expenses,
                    ink=True,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )
    
    # Scrollable content
    scrollable_content = ft.Column(
        controls=[
            gauge_section,
            ft.Container(height=16),
            tip_card,
            ft.Container(height=24),
            expenses_header,
            ft.Container(height=8),
            expenses_list,
            ft.Container(height=80),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    main_content = ft.Container(
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=0.8,
            colors=[theme.bg_gradient_start, theme.bg_primary, theme.bg_gradient_end],
        ),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
        content=ft.Column(
            controls=[header, scrollable_content],
            expand=True,
            spacing=0,
        ),
    )
    
    # Return the full view with nav bar
    return create_page_with_nav(
        page=page,
        main_content=main_content,
        active_index=0,
        on_home=None,
        on_expenses=show_dashboard,
        on_wallet=show_wallet,
        on_profile=show_profile,
        on_fab_click=show_add_expense,
        theme=theme,
    )
