# src/ui/nav_bar_buttom.py
import flet as ft
from core.theme import get_theme


def create_fab_button(page: ft.Page, on_click: callable = None, theme=None):
    """
    Creates the hexagon FAB button with hover animation.
    
    Args:
        page: The Flet page instance
        on_click: Callback when FAB is clicked
        theme: Theme colors (optional)
    """
    if theme is None:
        theme = get_theme()
    
    size = 56
    
    # Create hexagon shape using stacked rotated rectangles with gradient background
    hex_gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#5D4157", "#A8CABA"],
    )

    hex_part1 = ft.Container(
        width=size,
        height=size * 0.58,
        border_radius=4,
        gradient=hex_gradient,
    )

    hex_part2 = ft.Container(
        width=size,
        height=size * 0.58,
        border_radius=4,
        rotate=ft.Rotate(angle=1.0472),  # 60 degrees
        gradient=hex_gradient,
    )

    hex_part3 = ft.Container(
        width=size,
        height=size * 0.58,
        border_radius=4,
        rotate=ft.Rotate(angle=-1.0472),  # -60 degrees
        gradient=hex_gradient,
    )
    
    fab_icon = ft.Icon(ft.Icons.ADD_ROUNDED, color="white", size=32, weight=1200)
    
    hexagon_stack = ft.Stack(
        controls=[
            ft.Container(content=hex_part1, alignment=ft.alignment.center),
            ft.Container(content=hex_part2, alignment=ft.alignment.center),
            ft.Container(content=hex_part3, alignment=ft.alignment.center),
            ft.Container(content=fab_icon, alignment=ft.alignment.center),
        ],
        width=size,
        height=size,
    )
    
    fab_container = ft.Container(
        content=hexagon_stack,
        width=size + 4,
        height=size + 4,
        alignment=ft.alignment.center,
        animate=200,
        animate_scale=200,
        scale=1,
    )
    
    def handle_click(e):
        if on_click:
            on_click()
    
    def on_fab_hover(e):
        if e.data == "true":
            fab_container.scale = 1.1
        else:
            fab_container.scale = 1
        page.update()
    
    fab_container.on_click = handle_click
    fab_container.on_hover = on_fab_hover
    
    return fab_container


def create_bottom_nav_bar(
    page: ft.Page,
    active_index: int,
    on_home: callable = None,
    on_expenses: callable = None,
    on_wallet: callable = None,
    on_profile: callable = None,
    theme=None,
):
    """
    Creates a consistent bottom navigation bar component.
    
    Args:
        page: The Flet page instance
        active_index: Which icon is active (0=Home, 1=Expenses, 2=Wallet, 3=Profile)
        on_home: Callback when Home is clicked
        on_expenses: Callback when Expenses is clicked
        on_wallet: Callback when Wallet is clicked
        on_profile: Callback when Profile is clicked
        theme: Theme colors (optional)
    """
    if theme is None:
        theme = get_theme()
    
    active_color = theme.nav_active  # Purple for active
    inactive_color = theme.nav_inactive  # Gray for inactive
    nav_bg = theme.nav_bg
    
    def handle_home(e):
        if on_home and active_index != 0:
            on_home()
    
    def handle_expenses(e):
        if on_expenses and active_index != 1:
            on_expenses()
    
    def handle_wallet(e):
        if on_wallet and active_index != 2:
            on_wallet()
    
    def handle_profile(e):
        if on_profile and active_index != 3:
            on_profile()
    
    def create_nav_item(icon, label, is_active, on_click):
        """Create a nav item with icon and label."""
        return ft.Container(
            content=ft.Icon(
                icon,
                color=active_color if is_active else inactive_color,
                size=32,
            ),
            on_click=on_click,
            ink=True,
            border_radius=16,
            padding=ft.padding.symmetric(horizontal=8, vertical=10),
            expand=True,
            alignment=ft.alignment.center,
        )
    
    nav_bar_inner = ft.Container(
        content=ft.Row(
            controls=[
                create_nav_item(ft.Icons.DASHBOARD_ROUNDED, None, active_index == 0, handle_home),
                create_nav_item(ft.Icons.PAYMENTS_ROUNDED, None, active_index == 1, handle_expenses),
                ft.Container(width=60),  # Space for FAB
                create_nav_item(ft.Icons.INSIGHTS_ROUNDED, None, active_index == 2, handle_wallet),
                create_nav_item(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, None, active_index == 3, handle_profile),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            expand=True,
        ),
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=0.8,
            colors=[theme.bg_gradient_start, theme.bg_primary, theme.bg_gradient_end],
        ),
        padding=ft.padding.symmetric(vertical=8, horizontal=4),
        bgcolor=theme.bg_primary,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color="#00000040" if theme.is_dark else "#00000020",
            offset=ft.Offset(0, -4),
        ),
    )
    
    # Remove outer padding so nav bar fits the screen width
    return ft.Container(
        content=nav_bar_inner,
        padding=ft.padding.only(bottom=0),
        bgcolor="transparent",
    )


def create_page_with_nav(
    page: ft.Page,
    main_content: ft.Control,
    active_index: int,
    on_home: callable = None,
    on_expenses: callable = None,
    on_wallet: callable = None,
    on_profile: callable = None,
    on_fab_click: callable = None,
    theme=None,
):
    """
    Creates the full page layout with content, bottom nav, and FAB.
    
    Args:
        page: The Flet page instance
        main_content: The main scrollable content
        active_index: Which nav icon is active (0=Home, 1=Expenses, 2=Wallet, 3=Profile)
        on_home: Callback for Home navigation
        on_expenses: Callback for Expenses navigation
        on_wallet: Callback for Wallet navigation
        on_profile: Callback for Profile navigation
        on_fab_click: Callback for FAB click
        theme: Theme colors (optional)
    
    Returns:
        A Stack containing everything
    """
    if theme is None:
        theme = get_theme()
    
    bottom_nav = create_bottom_nav_bar(
        page=page,
        active_index=active_index,
        on_home=on_home,
        on_expenses=on_expenses,
        on_wallet=on_wallet,
        on_profile=on_profile,
        theme=theme,
    )
    
    fab = create_fab_button(page=page, on_click=on_fab_click, theme=theme)
    
    return ft.Stack(
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
                bottom=35,
                left=0,
                right=0,
                alignment=ft.alignment.center,
            ),
        ],
        expand=True,
    )
