# src/ui/statistics_page.py
import flet as ft
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav
from datetime import datetime, timedelta


# Brand database for recognition - with real brand logos (synced with Expenses.py and home_page.py)
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
        eid, uid, amount, category, description, date_str = expense
        
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
                                    ft.Text(f"₱{amount:,.2f}", size=32, weight=ft.FontWeight.BOLD, color="#EF4444"),
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
                        content=ft.CircleAvatar(
                            foreground_image_src="/assets/icon.png",
                            bgcolor=theme.accent_primary,
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                            radius=22,
                        ),
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
                            ft.Text(f"₱{total_spent:,.2f}", size=24, weight=ft.FontWeight.BOLD, color=theme.text_primary),
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
        
        for exp in expenses[:5]:  # Show last 5
            eid, uid, amount, category, description, date_str = exp
            transactions_list.controls.append(
                _transaction_item(
                    category=category,
                    description=description or category,
                    amount=amount,
                    date=_format_date(date_str),
                    on_click=lambda e, ex=exp, t=theme: show_transaction_detail(ex, t),
                    theme=theme,
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
        page.add(
            create_page_with_nav(
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
        )
        page.update()
    
    return show_view


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


def _transaction_item(category: str, description: str, amount: float, date: str, on_click=None, theme=None):
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
            f"-₱{amount:,.2f}",
            size=12,
            weight=ft.FontWeight.W_600,
            color=theme.error,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=theme.error_bg,
    )
    
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
                amount_badge,
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
