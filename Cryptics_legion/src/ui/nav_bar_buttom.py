# src/ui/nav_bar_buttom.py
import flet as ft
from core.theme import get_theme


def create_fab_button(page: ft.Page, on_click: callable = None, theme=None):
    """
    Creates the square FAB button with hover animation.
    
    Args:
        page: The Flet page instance
        on_click: Callback when FAB is clicked
        theme: Theme colors (optional)
    """
    if theme is None:
        theme = get_theme()
    
    fab_icon = ft.Icon(ft.Icons.ADD_ROUNDED, color="white", size=28)
    fab_container = ft.Container(
        content=fab_icon,
        width=56,
        height=56,
        border_radius=12,
        bgcolor=theme.accent_primary,
        alignment=ft.alignment.center,
        ink=True,
        animate=200,
        animate_scale=200,
        scale=1,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=f"{theme.accent_primary}40",
            offset=ft.Offset(0, 4),
        ),
    )
    
    def handle_click(e):
        if on_click:
            on_click()
    
    def on_fab_hover(e):
        if e.data == "true":
            fab_container.scale = 1.1
            fab_container.bgcolor = theme.accent_secondary
            fab_container.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=f"{theme.accent_primary}80",
                offset=ft.Offset(0, 6),
            )
        else:
            fab_container.scale = 1
            fab_container.bgcolor = theme.accent_primary
            fab_container.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=f"{theme.accent_primary}40",
                offset=ft.Offset(0, 4),
            )
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
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.HOME_ROUNDED,
                    icon_color=active_color if active_index == 0 else inactive_color,
                    icon_size=28,
                    on_click=handle_home,
                    style=ft.ButtonStyle(padding=ft.padding.all(12)),
                ),
                ft.IconButton(
                    icon=ft.Icons.ANALYTICS_ROUNDED,
                    icon_color=active_color if active_index == 1 else inactive_color,
                    icon_size=28,
                    on_click=handle_expenses,
                    style=ft.ButtonStyle(padding=ft.padding.all(12)),
                ),
                ft.Container(width=60),  # Space for FAB
                ft.IconButton(
                    icon=ft.Icons.INSERT_CHART_ROUNDED,  # Statistics icon
                    icon_color=active_color if active_index == 2 else inactive_color,
                    icon_size=28,
                    on_click=handle_wallet,
                    style=ft.ButtonStyle(padding=ft.padding.all(12)),
                ),
                ft.IconButton(
                    icon=ft.Icons.PERSON_ROUNDED,
                    icon_color=active_color if active_index == 3 else inactive_color,
                    icon_size=28,
                    on_click=handle_profile,
                    style=ft.ButtonStyle(padding=ft.padding.all(12)),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=nav_bg,
        border_radius=ft.border_radius.only(top_left=24, top_right=24),
        padding=ft.padding.symmetric(vertical=12, horizontal=8),
        border=ft.border.only(top=ft.BorderSide(1, theme.border_primary)) if not theme.is_dark else None,
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
