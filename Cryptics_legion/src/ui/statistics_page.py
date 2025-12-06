# src/ui/statistics_page.py
import flet as ft
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav
from datetime import datetime, timedelta
from utils.statistics import (
    get_expense_summary_by_period,
    get_daily_expenses,
    get_weekly_expenses,
    get_monthly_expenses,
    get_spending_trend,
    get_top_spending_categories,
    get_category_color,
    get_statistics_summary,
    get_average_daily_spending,
)
from utils.currency import format_currency, get_currency_from_user_profile


def get_clearbit_logo(domain: str) -> str:
    """Get brand logo URL from Clearbit API."""
    return f"https://logo.clearbit.com/{domain}"


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
                content=ft.Text(photo_value, size=radius * 0.8),
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


def _get_brand_info(text: str):
    """Get brand info from text."""
    text_lower = text.lower()
    for brand, info in BRAND_DATABASE.items():
        if brand in text_lower:
            return info
    return None


def _get_category_fallback(category: str):
    """Get category icon as fallback."""
    cat_lower = category.lower()
    for key, info in CATEGORY_ICONS.items():
        if key in cat_lower:
            return info
    return {"icon": "📦", "bg": "#6B7280"}


def create_statistics_view(page: ft.Page, state: dict, toast, go_back, 
                           show_expenses=None, show_profile=None, show_add_expense=None):
    """Create the Statistics page with spending graph and transactions."""
    
    # State for time period selection
    selected_period = {"value": "1W"}
    
    def nav_home():
        if go_back:
            go_back()
    
    def nav_expenses():
        if show_expenses:
            show_expenses()
    
    def nav_profile():
        if show_profile:
            show_profile()
    
    def nav_add_expense():
        if show_add_expense:
            show_add_expense()
    
    def get_period_data(period: str):
        """Get expense data for the selected time period."""
        expenses = db.select_expenses_by_user(state["user_id"])
        today = datetime.now()
        
        if period == "1D":
            start_date = today - timedelta(days=1)
        elif period == "1W":
            start_date = today - timedelta(weeks=1)
        elif period == "1M":
            start_date = today - timedelta(days=30)
        elif period == "3M":
            start_date = today - timedelta(days=90)
        elif period == "1Y":
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(weeks=1)
        
        filtered = []
        for exp in expenses:
            try:
                exp_date = datetime.strptime(exp[5], "%Y-%m-%d")
                if exp_date >= start_date:
                    filtered.append(exp)
            except:
                pass
        
        total = sum(exp[2] for exp in filtered)
        return filtered, total
    
    def create_spending_graph(expenses, period, theme=None):
        """Create a line chart showing spending over time."""
        if theme is None:
            theme = get_theme()
        
        if not expenses:
            # Empty state
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.SHOW_CHART, color=theme.accent_primary, size=36),
                        ft.Text("No data for this period", color=theme.text_muted, size=12),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                height=120,
                alignment=ft.alignment.center,
            )
        
        # Group expenses by day
        daily_totals = {}
        for exp in expenses:
            try:
                date_str = exp[5]
                if date_str in daily_totals:
                    daily_totals[date_str] += exp[2]
                else:
                    daily_totals[date_str] = exp[2]
            except:
                pass
        
        if not daily_totals:
            return ft.Container(height=200)
        
        # Sort by date
        sorted_dates = sorted(daily_totals.keys())
        values = [daily_totals[d] for d in sorted_dates]
        max_val = max(values) if values else 1
        
        # Create data points for line chart
        data_points = []
        for i, val in enumerate(values):
            data_points.append(
                ft.LineChartDataPoint(i, val)
            )
        
        # Chart border color based on theme
        chart_border_color = theme.border_primary
        
        return ft.Container(
            content=ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=data_points,
                        stroke_width=2,
                        color=theme.accent_primary,
                        curved=True,
                        stroke_cap_round=True,
                        below_line_gradient=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=[f"{theme.accent_primary}20", f"{theme.accent_primary}00"],
                        ),
                    )
                ],
                border=ft.Border(
                    bottom=ft.BorderSide(1, chart_border_color),
                    left=ft.BorderSide(1, chart_border_color),
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    color=chart_border_color,
                    width=1,
                    dash_pattern=[3, 3],
                ),
                tooltip_bgcolor=theme.bg_card,
                min_y=0,
                max_y=max_val * 1.2,
                min_x=0,
                max_x=len(values) - 1 if len(values) > 1 else 1,
                expand=True,
            ),
            height=120,
            padding=ft.padding.only(right=8),
        )
    
    def show_transaction_detail(expense, theme=None):
        """Show transaction detail bottom sheet."""
        if theme is None:
            theme = get_theme()
        # Unpack with account_id (position 6)
        eid, uid, amount, category, description, date_str = expense[:6]
        
        # Generate mock transaction details
        transaction_id = f"TXN{eid:08d}"
        
        def close_sheet(e):
            page.close(detail_sheet)
        
        detail_sheet = ft.BottomSheet(
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
                            padding=ft.padding.only(top=12, bottom=20),
                        ),
                        # Header
                        ft.Row(
                            controls=[
                                ft.Text("Transaction Details", size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_secondary,
                                    on_click=close_sheet,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=16),
                        # Amount
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Amount", size=12, color=theme.text_secondary),
                                    ft.Text(format_currency(amount, user_currency), size=32, weight=ft.FontWeight.BOLD, color="#EF4444"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                        ft.Divider(color=theme.border_primary, height=1),
                        # Details list
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    _detail_row("Transaction ID", transaction_id, theme=theme),
                                    _detail_row("Category", category, theme=theme),
                                    _detail_row("Description", description or "No description", theme=theme),
                                    _detail_row("Date", _format_date(date_str), theme=theme),
                                    _detail_row("Time", datetime.now().strftime("%I:%M %p"), theme=theme),
                                    _detail_row("Status", "Completed", color="#10B981", theme=theme),
                                    _detail_row("Payment Method", "Cash", theme=theme),
                                ],
                                spacing=16,
                            ),
                            padding=ft.padding.symmetric(vertical=20),
                        ),
                        ft.Container(height=20),
                        # Action buttons
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.SHARE, size=18),
                                            ft.Text("Share"),
                                        ],
                                        spacing=8,
                                    ),
                                    bgcolor=theme.bg_card,
                                    color=theme.text_primary,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                                    ),
                                    on_click=lambda e: toast("Receipt shared!", "#2E7D32"),
                                ),
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.DOWNLOAD, size=18),
                                            ft.Text("Download"),
                                        ],
                                        spacing=8,
                                    ),
                                    bgcolor=theme.accent_primary,
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                                    ),
                                    on_click=lambda e: toast("Receipt downloaded!", "#2E7D32"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_primary,
                padding=20,
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_primary,
        )
        
        page.open(detail_sheet)
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Get expense data for selected period
        expenses, total_spent = get_period_data(selected_period["value"])
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Statistics", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=create_user_avatar(state["user_id"], radius=22, theme=theme),
                        on_click=lambda e: nav_profile(),
                        ink=True,
                        border_radius=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=10),
        )
        
        # Time period selector
        def on_period_change(period):
            selected_period["value"] = period
            show_view()
        
        period_buttons = ft.Row(
            controls=[
                _period_button("1D", selected_period["value"], on_period_change, theme),
                _period_button("1W", selected_period["value"], on_period_change, theme),
                _period_button("1M", selected_period["value"], on_period_change, theme),
                _period_button("3M", selected_period["value"], on_period_change, theme),
                _period_button("1Y", selected_period["value"], on_period_change, theme),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Spending summary card
        spending_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(f"{selected_period['value']} Spending", size=12, color=theme.text_secondary),
                            ft.Text(format_currency(total_spent, user_currency), size=24, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ],
                        spacing=2,
                    ),
                    ft.Container(height=6),
                    period_buttons,
                    ft.Container(height=10),
                    # Line graph
                    create_spending_graph(expenses, selected_period["value"], theme),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border_radius=12,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Recent transactions header
        transactions_header = ft.Row(
            controls=[
                ft.Text("Recent Transactions", size=18, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.TextButton(
                    content=ft.Text("See All", color=theme.accent_primary),
                    on_click=lambda e: nav_expenses(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Recent transactions list
        transactions_list = ft.Column(spacing=8)
        
        # Cache account names for efficiency
        account_cache = {}
        def get_account_name(acc_id):
            if acc_id is None:
                return None
            if acc_id not in account_cache:
                acc = db.get_account_by_id(acc_id, state["user_id"])
                account_cache[acc_id] = acc[1] if acc else None
            return account_cache[acc_id]
        
        for exp in expenses[:5]:  # Show last 5
            # Unpack with account_id (position 6)
            eid, uid, amount, category, description, date_str, acc_id = exp[:7]
            acc_name = get_account_name(acc_id)
            transactions_list.controls.append(
                _transaction_item(
                    category=category,
                    description=description or category,
                    amount=amount,
                    date=_format_date(date_str),
                    on_click=lambda e, ex=exp, t=theme: show_transaction_detail(ex, t),
                    theme=theme,
                    account_name=acc_name,
                    user_currency=user_currency,
                )
            )
        
        if not expenses:
            transactions_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG, color=theme.text_hint, size=48),
                            ft.Text("No transactions yet", color=theme.text_muted, size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        # Main scrollable content
        scrollable_content = ft.Column(
            controls=[
                spending_card,
                ft.Container(height=24),
                transactions_header,
                ft.Container(height=12),
                transactions_list,
                ft.Container(height=100),
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
            active_index=2,  # Statistics (was Wallet) is active
            on_home=nav_home,
            on_expenses=nav_expenses,
            on_wallet=None,  # Already on statistics
            on_profile=nav_profile,
            on_fab_click=nav_add_expense,
            theme=theme,
        )
        
        page.add(full_view)
        page.update()
    
    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_statistics_content(page: ft.Page, state: dict, toast, 
                              go_back, show_expenses, show_profile, show_add_expense):
    """
    Builds and returns statistics page content WITHOUT calling page.clean() or page.add().
    Enhanced with comprehensive statistics, pie charts, bar charts, and trend analysis.
    """
    theme = get_theme()
    user_id = state["user_id"]
    user_profile = db.get_user_profile(user_id)
    user_currency = get_currency_from_user_profile(user_profile)
    
    # State for period and chart type selection
    selected_period = {"value": "1M"}
    selected_chart = {"value": "pie"}  # "pie", "bar_daily", "bar_weekly", "bar_monthly"
    
    # Get user profile for avatar
    user_profile = db.get_user_profile(user_id)
    
    # Create avatar
    user_avatar = create_user_avatar(user_id, radius=22, theme=theme)
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Statistics", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.Text("Your spending insights", size=13, color=theme.text_secondary),
                    ],
                    spacing=0,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                            icon_color=theme.text_primary,
                            icon_size=22,
                        ),
                        ft.Container(
                            content=user_avatar,
                            on_click=lambda e: show_profile() if show_profile else None,
                            ink=True,
                            border_radius=22,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(top=10, bottom=16),
    )
    
    # Get comprehensive statistics
    stats = get_statistics_summary(user_id, selected_period["value"])
    trend = stats["trend"]
    top_categories = stats["top_categories"]
    
    # Trend indicator
    trend_icon = ft.Icons.TRENDING_UP if trend["trend"] == "up" else (
        ft.Icons.TRENDING_DOWN if trend["trend"] == "down" else ft.Icons.TRENDING_FLAT
    )
    trend_color = "#EF4444" if trend["trend"] == "up" else (
        "#10B981" if trend["trend"] == "down" else theme.text_secondary
    )
    
    # Summary Card with trend
    summary_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Total Spent", size=12, color=theme.text_secondary),
                                ft.Text(format_currency(stats['total_spent'], user_currency), size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ],
                            spacing=2,
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(trend_icon, color=trend_color, size=16),
                                    ft.Text(
                                        f"{abs(trend['change_percent']):.1f}%",
                                        size=12,
                                        color=trend_color,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                                spacing=4,
                            ),
                            bgcolor=f"{trend_color}20",
                            border_radius=12,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        _stat_mini_card("📊", f"{stats['transaction_count']}", "Transactions", theme),
                        _stat_mini_card("📁", f"{stats['category_count']}", "Categories", theme),
                        _stat_mini_card("📅", format_currency(get_average_daily_spending(user_id), user_currency), "Daily Avg", theme),
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
    
    # Period selector
    def on_period_change(period):
        selected_period["value"] = period
        # Refresh the page content
        page.update()
    
    period_buttons = ft.Row(
        controls=[
            _create_period_chip("1W", selected_period["value"], on_period_change, theme),
            _create_period_chip("1M", selected_period["value"], on_period_change, theme),
            _create_period_chip("3M", selected_period["value"], on_period_change, theme),
            _create_period_chip("6M", selected_period["value"], on_period_change, theme),
            _create_period_chip("1Y", selected_period["value"], on_period_change, theme),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )
    
    # Create Pie Chart with colors
    expense_summary = get_expense_summary_by_period(user_id, selected_period["value"])
    total = sum(row[1] for row in expense_summary) if expense_summary else 0
    
    pie_sections = []
    for category, amount in expense_summary:
        percentage = (amount / total * 100) if total > 0 else 0
        color = get_category_color(category)
        pie_sections.append(
            ft.PieChartSection(
                value=float(amount),
                title=f"{percentage:.0f}%",
                title_style=ft.TextStyle(
                    size=10,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                color=color,
                radius=80 if percentage >= 15 else 70,
            )
        )
    
    pie_chart = ft.Container(
        content=ft.PieChart(
            sections=pie_sections if pie_sections else [
                ft.PieChartSection(value=1, title="No data", color=theme.text_muted, radius=60)
            ],
            center_space_radius=40,
            sections_space=2,
        ),
        height=200,
        alignment=ft.alignment.center,
    ) if pie_sections else ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.PIE_CHART_OUTLINE, size=48, color=theme.text_hint),
                ft.Text("No expense data", size=14, color=theme.text_muted),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        height=200,
        alignment=ft.alignment.center,
    )
    
    # Create Bar Chart for daily spending
    daily_data = get_daily_expenses(user_id, 7)
    bar_groups = []
    max_val = max([d[1] for d in daily_data]) if daily_data else 1
    
    for i, (date_str, amount) in enumerate(daily_data):
        try:
            day_label = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a")
        except:
            day_label = f"D{i+1}"
        
        bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=amount if amount > 0 else 0.1,
                        width=20,
                        color=theme.accent_primary,
                        tooltip=f"{day_label}: {format_currency(amount, user_currency)}",
                        border_radius=ft.border_radius.only(top_left=4, top_right=4),
                    ),
                ],
            )
        )
    
    bar_chart = ft.Container(
        content=ft.BarChart(
            bar_groups=bar_groups,
            border=ft.Border(
                bottom=ft.BorderSide(1, theme.border_primary),
                left=ft.BorderSide(1, theme.border_primary),
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=theme.border_primary,
                width=1,
                dash_pattern=[3, 3],
            ),
            tooltip_bgcolor=theme.bg_card,
            max_y=max_val * 1.2 if max_val > 0 else 100,
            interactive=True,
            expand=True,
        ),
        height=150,
        padding=ft.padding.only(right=16, top=8),
    )
    
    # Chart type tabs
    chart_tabs = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PIE_CHART, size=16, color=theme.text_primary),
                            ft.Text("Categories", size=12, color=theme.text_primary),
                        ],
                        spacing=4,
                    ),
                    bgcolor=theme.accent_primary + "30",
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.BAR_CHART, size=16, color=theme.text_secondary),
                            ft.Text("Daily", size=12, color=theme.text_secondary),
                        ],
                        spacing=4,
                    ),
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                ),
            ],
            spacing=8,
        ),
        padding=ft.padding.only(bottom=12),
    )
    
    # Charts section
    charts_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Spending Breakdown", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Container(height=8),
                period_buttons,
                ft.Container(height=16),
                pie_chart,
                ft.Container(height=16),
                ft.Divider(color=theme.border_primary, height=1),
                ft.Container(height=16),
                ft.Text("Daily Spending (Last 7 Days)", size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Container(height=8),
                bar_chart,
            ],
        ),
        padding=16,
        border_radius=16,
        bgcolor=theme.bg_card,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Category legend
    category_legend = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Top Categories", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Container(height=12),
                *[_category_legend_item(cat["category"], cat["amount"], cat["percentage"], cat["color"], theme, user_currency) 
                  for cat in top_categories[:5]],
            ] if top_categories else [
                ft.Text("Top Categories", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Container(height=12),
                ft.Text("No categories yet", size=14, color=theme.text_muted),
            ],
        ),
        padding=16,
        border_radius=16,
        bgcolor=theme.bg_card,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Highest expense card
    highest = stats.get("highest_expense")
    if highest:
        highest_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.ARROW_UPWARD, color="#EF4444", size=20),
                        width=40,
                        height=40,
                        border_radius=20,
                        bgcolor="#EF444420",
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Highest Expense", size=12, color=theme.text_secondary),
                            ft.Text(highest[3] or highest[2], size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Text(format_currency(highest[1], user_currency), size=16, weight=ft.FontWeight.BOLD, color="#EF4444"),
                ],
                spacing=12,
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
    else:
        highest_card = ft.Container()
    
    # Recent transactions
    all_expenses = db.select_expenses_by_user(user_id)
    transactions_header = ft.Row(
        controls=[
            ft.Text("Recent Transactions", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.TextButton(
                content=ft.Text("See All", color=theme.accent_primary, size=12),
                on_click=lambda e: show_expenses() if show_expenses else None,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    transactions_list = ft.Column(spacing=8)
    
    # Cache account names
    account_cache = {}
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, user_id)
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    for exp in all_expenses[:5]:
        eid, uid, amount, category, description, date_str, acc_id = exp[:7]
        acc_name = get_account_name(acc_id)
        transactions_list.controls.append(
            _transaction_item(
                category=category,
                description=description or category,
                amount=amount,
                date=_format_date(date_str),
                theme=theme,
                account_name=acc_name,
                user_currency=user_currency,
            )
        )
    
    if not all_expenses:
        transactions_list.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.RECEIPT_LONG, color=theme.text_hint, size=48),
                        ft.Text("No transactions yet", color=theme.text_muted, size=14),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=40,
                alignment=ft.alignment.center,
            )
        )

    # Main scrollable content
    scrollable_content = ft.Column(
        controls=[
            summary_card,
            ft.Container(height=16),
            charts_section,
            ft.Container(height=16),
            category_legend,
            ft.Container(height=16),
            highest_card,
            ft.Container(height=16),
            transactions_header,
            ft.Container(height=12),
            transactions_list,
            ft.Container(height=100),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    main_content = ft.Container(
        expand=True,
        bgcolor=theme.bg_primary,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.bg_gradient_start, theme.bg_gradient_end],
        ),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
        content=ft.Column(
            controls=[header, scrollable_content],
            expand=True,
            spacing=0,
        ),
    )
    
    return create_page_with_nav(
        page=page,
        main_content=main_content,
        active_index=2,
        on_home=go_back,
        on_expenses=show_expenses,
        on_wallet=None,
        on_profile=show_profile,
        on_fab_click=show_add_expense,
        theme=theme,
    )


# ============ Helper functions for statistics page ============

def _stat_mini_card(icon: str, value: str, label: str, theme):
    """Create a mini statistic card."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(icon, size=16),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.Text(label, size=10, color=theme.text_secondary),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=8,
        bgcolor=theme.bg_primary,
    )


def _create_period_chip(period: str, selected: str, on_click, theme):
    """Create a period selection chip."""
    is_selected = period == selected
    return ft.Container(
        content=ft.Text(
            period,
            size=12,
            color="white" if is_selected else theme.text_muted,
            weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
        ),
        bgcolor=theme.accent_primary if is_selected else "transparent",
        border_radius=16,
        padding=ft.padding.symmetric(horizontal=14, vertical=6),
        on_click=lambda e: on_click(period),
        ink=True,
    )


def _category_legend_item(category: str, amount: float, percentage: float, color: str, theme, user_currency: str = None):
    """Create a category legend item with progress bar."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=12,
                    height=12,
                    border_radius=3,
                    bgcolor=color,
                ),
                ft.Text(category, size=13, color=theme.text_primary, expand=True),
                ft.Text(format_currency(amount, user_currency), size=13, color=theme.text_secondary, weight=ft.FontWeight.W_500),
                ft.Container(
                    content=ft.Text(f"{percentage:.0f}%", size=11, color=theme.text_muted),
                    width=40,
                    alignment=ft.alignment.center_right,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=6),
    )


# Helper functions
def _format_date(date_str: str) -> str:
    """Format date string to display format."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except:
        return date_str


def _period_button(period: str, selected: str, on_click, theme=None):
    """Create a time period selector button."""
    is_selected = period == selected
    if theme is None:
        from core.theme import get_theme
        theme = get_theme()
    
    return ft.Container(
        content=ft.Text(
            period,
            size=13,
            color=theme.text_primary if is_selected else theme.text_muted,
            weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.NORMAL,
        ),
        bgcolor=theme.accent_primary if is_selected else "transparent",
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=14, vertical=8),
        on_click=lambda e: on_click(period),
        ink=True,
    )


def _detail_row(label: str, value: str, color: str = None, theme=None):
    """Create a detail row for transaction details."""
    if theme is None:
        theme = get_theme()
    if color is None:
        color = theme.text_primary
    return ft.Row(
        controls=[
            ft.Text(label, size=14, color=theme.text_secondary, width=120),
            ft.Text(value, size=14, color=color, expand=True, text_align=ft.TextAlign.RIGHT),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def _get_category_icon(category: str):
    """Get icon for category."""
    icons = {
        "food": ft.Icons.RESTAURANT,
        "dining": ft.Icons.RESTAURANT,
        "transport": ft.Icons.DIRECTIONS_CAR,
        "shopping": ft.Icons.SHOPPING_BAG,
        "entertainment": ft.Icons.MOVIE,
        "bills": ft.Icons.RECEIPT,
        "utilities": ft.Icons.BOLT,
        "health": ft.Icons.LOCAL_HOSPITAL,
        "education": ft.Icons.SCHOOL,
        "electronics": ft.Icons.DEVICES,
        "groceries": ft.Icons.LOCAL_GROCERY_STORE,
        "travel": ft.Icons.FLIGHT,
        "subscription": ft.Icons.SUBSCRIPTIONS,
    }
    
    cat_lower = category.lower()
    for key, icon in icons.items():
        if key in cat_lower:
            return icon
    return ft.Icons.PAYMENTS


def _get_category_color(category: str):
    """Get color for category."""
    colors = {
        "food": "#F59E0B",
        "dining": "#F59E0B",
        "transport": "#3B82F6",
        "shopping": "#EC4899",
        "entertainment": "#8B5CF6",
        "bills": "#6366F1",
        "utilities": "#06B6D4",
        "health": "#EF4444",
        "education": "#10B981",
        "electronics": "#6366F1",
        "groceries": "#10B981",
        "travel": "#F97316",
        "subscription": "#8B5CF6",
    }
    
    cat_lower = category.lower()
    for key, color in colors.items():
        if key in cat_lower:
            return color
    return "#6366F1"


def _transaction_item(category: str, description: str, amount: float, date: str, on_click=None, theme=None, account_name: str = None, user_currency: str = None):
    """Create a transaction list item with brand logos."""
    if theme is None:
        from core.theme import get_theme
        theme = get_theme()
    
    # Get brand info first, then category fallback
    brand_info = _get_brand_info(description)
    
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
                width=48,
                height=48,
                border_radius=12,
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
                width=48,
                height=48,
                border_radius=12,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
    else:
        # Use category fallback
        cat_info = _get_category_fallback(category)
        icon_container = ft.Container(
            content=ft.Text(
                cat_info["icon"],
                size=20,
                text_align=ft.TextAlign.CENTER,
            ),
            width=48,
            height=48,
            border_radius=12,
            bgcolor=cat_info["bg"],
            alignment=ft.alignment.center,
        )
    
    # Amount badge
    amount_badge = ft.Container(
        content=ft.Text(
            f"-{format_currency(amount, user_currency)}",
            size=12,
            weight=ft.FontWeight.W_600,
            color=theme.error,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=theme.error_bg,
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
                # Description and date
                ft.Column(
                    controls=[
                        ft.Text(description[:25] + "..." if len(description) > 25 else description, 
                               size=14, color=theme.text_primary, weight=ft.FontWeight.W_500),
                        ft.Text(date, size=12, color=theme.text_secondary),
                    ],
                    spacing=2,
                    expand=True,
                ),
                # Amount and Account badge - fixed position right side
                ft.Column([
                    amount_badge,
                    account_badge,
                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END),
                # Arrow
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_hint, size=20),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.bg_card,
        border_radius=12,
        padding=12,
        border=ft.border.all(1, theme.border_primary),
        on_click=on_click,
        ink=True,
    )
