# src/ui/profile_page.py
import flet as ft
from core import db
from core.theme import ThemeManager, get_theme
from utils.currency import format_currency, get_currency_from_user_profile


def create_user_avatar(user_id: int, radius: int = 50, theme=None):
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


def create_profile_view(page: ft.Page, state: dict, toast, go_back, logout_callback, show_account_settings=None, refresh_app=None):
    """Create the profile/settings page with theme support."""
    user_id = state["user_id"]
    user_profile = db.get_user_profile(user_id)
    user_currency = get_currency_from_user_profile(user_profile)
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Get user profile from database
        user_profile = db.get_user_profile(state["user_id"])
        display_name = user_profile.get("full_name", "") if user_profile else ""
        if not display_name:
            display_name = user_profile.get("username", f"User #{state['user_id']}") if user_profile else f"User #{state['user_id']}"
        
        # Get user stats
        total_spent = db.total_expenses_by_user(state["user_id"])
        transactions = len(db.select_expenses_by_user(state["user_id"]))
        categories = len(db.category_summary_by_user(state["user_id"]))
        
        # Header
        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=theme.text_primary,
                    on_click=lambda e: go_back(),
                ),
                ft.Text("Profile", size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.Container(width=48),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Profile avatar and info - make avatar tappable to change photo
        avatar_display = ft.Stack(
            controls=[
                create_user_avatar(state["user_id"], radius=50, theme=theme),
                ft.Container(
                    content=ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, size=14, color="white"),
                    width=28,
                    height=28,
                    bgcolor=theme.accent_primary,
                    border_radius=14,
                    alignment=ft.alignment.center,
                    right=0,
                    bottom=0,
                ),
            ],
            width=100,
            height=100,
        )
        
        profile_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=avatar_display,
                        on_click=lambda e: show_account_settings() if show_account_settings else None,
                        ink=True,
                        border_radius=50,
                    ),
                    ft.Container(height=8),
                    ft.Text("Tap to change photo", size=11, color=theme.accent_secondary),
                    ft.Container(height=4),
                    ft.Text(display_name, size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Text("Smart Expense Tracker", size=14, color=theme.text_secondary),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )
        
        # Stats cards
        stats_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(format_currency(total_spent, user_currency), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.Text("Total Spent", size=11, color=theme.text_secondary),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                    border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(str(transactions), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.Text("Transactions", size=11, color=theme.text_secondary),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                    border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(str(categories), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.Text("Categories", size=11, color=theme.text_secondary),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                    border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
                    expand=True,
                ),
            ],
            spacing=8,
        )
        
        # Theme Toggle Switch
        def toggle_theme(e):
            ThemeManager.toggle_theme()
            # Refresh the page to apply theme
            if refresh_app:
                refresh_app()
            else:
                show_view()  # Re-render this page with new theme
        
        is_dark = ThemeManager.is_dark_mode()
        
        # Theme toggle item (special styling)
        theme_toggle = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.DARK_MODE if is_dark else ft.Icons.LIGHT_MODE, 
                            color=theme.accent_primary, 
                            size=22
                        ),
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=theme.bg_elevated,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Theme", size=14, weight=ft.FontWeight.W_500, color=theme.text_primary),
                            ft.Text(
                                "Dark Mode" if is_dark else "Light Mode", 
                                size=12, 
                                color=theme.text_muted
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Switch(
                        value=is_dark,
                        active_color=theme.accent_primary,
                        active_track_color=theme.accent_bg if theme.is_dark else theme.accent_light,
                        inactive_thumb_color=theme.text_muted,
                        inactive_track_color=theme.border_primary,
                        on_change=toggle_theme,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border_radius=12,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
        )
        
        # Menu items
        def create_menu_item(icon, title, subtitle=None, on_click=None, color=None):
            item_color = color if color else theme.text_primary
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color=item_color, size=22),
                            width=44,
                            height=44,
                            border_radius=12,
                            bgcolor=theme.bg_elevated,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=item_color),
                                ft.Text(subtitle, size=12, color=theme.text_muted) if subtitle else ft.Container(),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=12,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
                on_click=on_click,
                ink=True,
            )
        
        menu_section = ft.Column(
            controls=[
                create_menu_item(ft.Icons.PERSON_OUTLINE, "Account Settings", "Manage your account", on_click=lambda e: show_account_settings() if show_account_settings else None),
                ft.Container(height=8),
                theme_toggle,  # Theme toggle in settings
                ft.Container(height=8),
                create_menu_item(ft.Icons.NOTIFICATIONS_OUTLINED, "Notifications", "Manage alerts"),
                ft.Container(height=8),
                create_menu_item(ft.Icons.SECURITY, "Privacy & Security", "Protect your data"),
                ft.Container(height=8),
                create_menu_item(ft.Icons.HELP_OUTLINE, "Help & Support", "Get assistance"),
                ft.Container(height=8),
                create_menu_item(ft.Icons.INFO_OUTLINE, "About", "App version 1.0.0"),
            ],
        )
        
        # Logout button
        logout_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.LOGOUT, color=theme.error, size=22),
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=theme.bg_elevated,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text("Logout", size=14, weight=ft.FontWeight.W_500, color=theme.error, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border_radius=12,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.error),
            on_click=lambda e: logout_callback(),
            ink=True,
        )
        
        # Main layout
        full_view = ft.Container(
            expand=True,
            bgcolor=theme.bg_primary,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.bg_gradient_start, theme.bg_gradient_end],
            ),
            padding=20,
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(height=10),
                    profile_section,
                    ft.Container(height=16),
                    stats_row,
                    ft.Container(height=24),
                    ft.Text("Settings", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                    ft.Container(height=12),
                    menu_section,
                    ft.Container(height=24),
                    logout_btn,
                    ft.Container(height=20),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
        
        page.add(full_view)
        page.update()
    
    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_profile_content(page: ft.Page, state: dict, toast, 
                           go_back, logout_callback, show_account_settings, refresh_app, show_privacy=None):
    """
    Builds and returns profile page content WITHOUT calling page.clean() or page.add().
    """
    theme = get_theme()
    
    # Get user profile from database
    user_profile = db.get_user_profile(state["user_id"])
    display_name = user_profile.get("full_name", "") if user_profile else ""
    if not display_name:
        display_name = user_profile.get("username", f"User #{state['user_id']}") if user_profile else f"User #{state['user_id']}"
    
    # Get user currency
    user_currency = get_currency_from_user_profile(user_profile) if user_profile else "PHP"
    
    # Get user stats
    total_spent = db.total_expenses_by_user(state["user_id"])
    transactions = len(db.select_expenses_by_user(state["user_id"]))
    categories = len(db.category_summary_by_user(state["user_id"]))
    
    # Header
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=theme.text_primary,
                on_click=lambda e: go_back() if go_back else None,
            ),
            ft.Text("Profile", size=20, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.Container(width=40),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Avatar
    avatar = create_user_avatar(state["user_id"], radius=50, theme=theme)
    
    # Profile section
    profile_section = ft.Container(
        content=ft.Column(
            controls=[
                avatar,
                ft.Container(height=16),
                ft.Text(display_name, size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.Text("Premium Member", size=12, color=theme.accent_primary),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )
    
    # Stats row
    stats_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(format_currency(total_spent, user_currency), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.Text("Total Spent", size=11, color=theme.text_secondary),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(color=theme.border_primary),
                ft.Column(
                    controls=[
                        ft.Text(str(transactions), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.Text("Transactions", size=11, color=theme.text_secondary),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(color=theme.border_primary),
                ft.Column(
                    controls=[
                        ft.Text(str(categories), size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.Text("Categories", size=11, color=theme.text_secondary),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        padding=16,
        border_radius=12,
        bgcolor=theme.bg_card,
    )
    
    # Menu items
    def menu_item(icon, title, subtitle, on_click=None):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=theme.accent_primary, size=22),
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=theme.bg_elevated,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=theme.text_primary),
                            ft.Text(subtitle, size=11, color=theme.text_secondary),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border_radius=12,
            bgcolor=theme.bg_card,
            on_click=on_click,
            ink=True,
        )
    
    def toggle_theme(e):
        ThemeManager.toggle_theme()
        if refresh_app:
            refresh_app()
    
    menu_section = ft.Column(
        controls=[
            menu_item(ft.Icons.SETTINGS, "Account Settings", "Manage your account", 
                      lambda e: show_account_settings() if show_account_settings else None),
            ft.Container(height=8),
            menu_item(ft.Icons.SHIELD_OUTLINED, "Personal data & Privacy", "Privacy policy and data management",
                      lambda e: show_privacy() if show_privacy else None),
            ft.Container(height=8),
            menu_item(ft.Icons.NOTIFICATIONS, "Notifications", "Manage alerts"),
            ft.Container(height=8),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.DARK_MODE if theme.is_dark else ft.Icons.LIGHT_MODE, 
                                           color=theme.accent_primary, size=22),
                            width=44,
                            height=44,
                            border_radius=12,
                            bgcolor=theme.bg_elevated,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Dark Mode" if theme.is_dark else "Light Mode", 
                                       size=14, weight=ft.FontWeight.W_500, color=theme.text_primary),
                                ft.Text("Switch theme", size=11, color=theme.text_secondary),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Switch(value=theme.is_dark, on_change=toggle_theme),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=12,
                bgcolor=theme.bg_card,
            ),
        ],
    )
    
    # Logout button
    logout_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.LOGOUT, color=theme.error, size=22),
                    width=44,
                    height=44,
                    border_radius=12,
                    bgcolor=theme.bg_elevated,
                    alignment=ft.alignment.center,
                ),
                ft.Text("Logout", size=14, weight=ft.FontWeight.W_500, color=theme.error, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=12,
        border_radius=12,
        bgcolor=theme.bg_card,
        border=ft.border.all(1, theme.error),
        on_click=lambda e: logout_callback(),
        ink=True,
    )
    
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=20,
        content=ft.Column(
            controls=[
                header,
                ft.Container(height=10),
                profile_section,
                ft.Container(height=16),
                stats_row,
                ft.Container(height=24),
                ft.Text("Settings", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                ft.Container(height=12),
                menu_section,
                ft.Container(height=24),
                logout_btn,
                ft.Container(height=20),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )
