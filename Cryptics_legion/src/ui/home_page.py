# src/ui/home_page.py
import flet as ft
from datetime import datetime
from core import db
import random
import math


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


def create_circular_gauge(balance: float, total_budget: float = 100000, size: int = 220):
    """
    Creates a modern circular gauge with multi-colored arcs.
    The colored portion represents the remaining balance percentage.
    When expenses reduce balance, the colored arc shrinks.
    """
    
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
                bgcolor="#0d1829",
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
                bgcolor="#1a2744",
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
        balance_color = "white"
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
                            color="#94a3b8",
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


def create_expense_item(icon_content, title: str, date: str, amount: float, on_click=None):
    """Creates a single expense item row."""
    # Format amount with sign
    amount_str = f"-₱{abs(amount):,.2f}" if amount < 0 else f"+₱{amount:,.2f}"
    amount_color = "#EF4444" if amount < 0 else "#10B981"
    
    return ft.Container(
        content=ft.Row(
            controls=[
                # Icon container
                ft.Container(
                    content=icon_content,
                    width=44,
                    height=44,
                    border_radius=22,
                    bgcolor="#1F2937",
                    alignment=ft.alignment.center,
                ),
                # Title and date
                ft.Column(
                    controls=[
                        ft.Text(title, size=14, weight=ft.FontWeight.W_500, color="white"),
                        ft.Text(date, size=12, color="#6B7280"),
                    ],
                    spacing=2,
                    expand=True,
                ),
                # Amount
                ft.Text(amount_str, size=14, weight=ft.FontWeight.W_600, color=amount_color),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=8, horizontal=4),
        on_click=on_click,
        ink=True,
        border_radius=8,
    )


def get_category_icon(category: str):
    """Returns an appropriate icon for the category."""
    category_lower = category.lower()
    
    icon_map = {
        "food": ft.Icons.RESTAURANT,
        "transport": ft.Icons.DIRECTIONS_CAR,
        "uber": ft.Icons.LOCAL_TAXI,
        "shopping": ft.Icons.SHOPPING_BAG,
        "entertainment": ft.Icons.MOVIE,
        "bills": ft.Icons.RECEIPT,
        "health": ft.Icons.LOCAL_HOSPITAL,
        "education": ft.Icons.SCHOOL,
        "salary": ft.Icons.ACCOUNT_BALANCE_WALLET,
        "income": ft.Icons.TRENDING_UP,
        "electronics": ft.Icons.DEVICES,
        "clothing": ft.Icons.CHECKROOM,
        "groceries": ft.Icons.LOCAL_GROCERY_STORE,
        "utilities": ft.Icons.BOLT,
        "rent": ft.Icons.HOME,
        "travel": ft.Icons.FLIGHT,
        "fitness": ft.Icons.FITNESS_CENTER,
        "subscription": ft.Icons.SUBSCRIPTIONS,
        "gift": ft.Icons.CARD_GIFTCARD,
        "insurance": ft.Icons.SECURITY,
        "investment": ft.Icons.SHOW_CHART,
        "savings": ft.Icons.SAVINGS,
        "other": ft.Icons.CATEGORY,
    }
    
    for key, icon in icon_map.items():
        if key in category_lower:
            return ft.Icon(icon, color="white", size=22)
    
    # Default icon
    return ft.Icon(ft.Icons.PAYMENTS, color="white", size=22)


def create_home_view(page: ft.Page, state: dict, toast, show_dashboard, logout_callback):
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
            icon_content = get_category_icon(cat)
            
            expenses_list.controls.append(
                create_expense_item(
                    icon_content=icon_content,
                    title=display_name,
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
        from ui.add_expense_page import create_add_expense_view
        add_view = create_add_expense_view(page, state, toast, show_view)
        add_view()
    
    def show_all_expenses(e):
        """Navigate to all expenses page."""
        from ui.all_expenses_page import create_all_expenses_view
        all_view = create_all_expenses_view(page, state, toast, show_view)
        all_view()
    
    def show_wallet(e):
        """Navigate to wallet page."""
        from ui.wallet_page import create_wallet_view
        wallet_view = create_wallet_view(page, state, toast, show_view)
        wallet_view()
    
    def show_profile(e):
        """Navigate to profile page."""
        from ui.profile_page import create_profile_view
        profile_view = create_profile_view(page, state, toast, show_view, logout_callback)
        profile_view()
    
    def show_view():
        page.clean()
        
        # Get random tip
        tip = random.choice(TIPS)
        
        # Refresh data
        total_budget = 100000
        total = db.total_expenses_by_user(state["user_id"])
        balance = total_budget - total
        gauge_container.content = create_circular_gauge(balance if balance > 0 else 0, total_budget)
        load_expenses()
        
        # Header with title and profile
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Home", size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(
                        content=ft.CircleAvatar(
                            foreground_image_src="/assets/icon.png",
                            bgcolor="#4F46E5",
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
                    ft.Text("Tip of the Day", size=12, color="#9CA3AF"),
                    ft.Container(height=4),
                    ft.Row(
                        controls=[
                            ft.Text(tip, size=14, color="white", expand=True),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#6B7280", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a2e",
            border=ft.border.all(1, "#2d2d44"),
        )
        
        # Expenses section header
        expenses_header = ft.Row(
            controls=[
                ft.Text("Expenses", size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.TextButton(
                    "See all",
                    style=ft.ButtonStyle(color="#3B82F6"),
                    on_click=show_all_expenses,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Expenses list container
        expenses_section = ft.Container(
            content=ft.Column(
                controls=[
                    expenses_header,
                    ft.Container(height=8),
                    expenses_list,
                ],
            ),
        )
        
        # Floating action button
        fab = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor="#6366F1",
            on_click=show_add_expense,
            mini=False,
        )
        
        # Bottom navigation bar
        bottom_nav = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.HOME_ROUNDED,
                        icon_color="#A855F7",
                        icon_size=28,
                        on_click=lambda e: None,  # Already on home
                    ),
                    ft.IconButton(
                        icon=ft.Icons.BAR_CHART_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=lambda e: show_dashboard(),
                    ),
                    ft.Container(width=56),  # Space for FAB
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=show_wallet,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PERSON_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=show_profile,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor="#0d0d1a",
            border_radius=ft.border_radius.only(top_left=24, top_right=24),
            padding=ft.padding.symmetric(vertical=12, horizontal=8),
        )
        
        # Main content
        main_content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#0f0f23", "#0a0a14"],
            ),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                gauge_section,
                                ft.Container(height=16),
                                tip_card,
                                ft.Container(height=24),
                                expenses_section,
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        )
        
        # Stack with FAB and bottom nav
        page.add(
            ft.Stack(
                controls=[
                    ft.Column(
                        controls=[
                            main_content,
                            bottom_nav,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    ft.Container(
                        content=fab,
                        alignment=ft.alignment.bottom_center,
                        padding=ft.padding.only(bottom=45),
                    ),
                ],
                expand=True,
            )
        )
        
        page.update()
    
    return show_view
