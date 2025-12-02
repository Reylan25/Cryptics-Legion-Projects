# src/ui/profile_page.py
import flet as ft
from core import db


def create_profile_view(page: ft.Page, state: dict, toast, go_back, logout_callback):
    """Create the profile/settings page."""
    
    def show_view():
        page.clean()
        
        # Get user stats
        total_spent = db.total_expenses_by_user(state["user_id"])
        transactions = len(db.select_expenses_by_user(state["user_id"]))
        categories = len(db.category_summary_by_user(state["user_id"]))
        
        # Header
        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: go_back(),
                ),
                ft.Text("Profile", size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(width=48),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Profile avatar and info
        profile_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.CircleAvatar(
                        foreground_image_src="/assets/icon.png",
                        bgcolor="#4F46E5",
                        content=ft.Icon(ft.Icons.PERSON, color="white", size=40),
                        radius=50,
                    ),
                    ft.Container(height=12),
                    ft.Text(f"User #{state['user_id']}", size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Smart Expense Tracker", size=14, color="#9CA3AF"),
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
                            ft.Text(f"₱{total_spent:,.0f}", size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Total Spent", size=11, color="#9CA3AF"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor="#1a1a2e",
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(str(transactions), size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Transactions", size=11, color="#9CA3AF"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor="#1a1a2e",
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(str(categories), size=18, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Categories", size=11, color="#9CA3AF"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=12,
                    border_radius=12,
                    bgcolor="#1a1a2e",
                    expand=True,
                ),
            ],
            spacing=8,
        )
        
        # Menu items
        def create_menu_item(icon, title, subtitle=None, on_click=None, color="white"):
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color=color, size=22),
                            width=44,
                            height=44,
                            border_radius=12,
                            bgcolor="#1F2937",
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=color),
                                ft.Text(subtitle, size=12, color="#6B7280") if subtitle else ft.Container(),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#6B7280", size=20),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=12,
                bgcolor="#1a1a2e",
                on_click=on_click,
                ink=True,
            )
        
        menu_section = ft.Column(
            controls=[
                create_menu_item(ft.Icons.PERSON_OUTLINE, "Account Settings", "Manage your account"),
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
                        content=ft.Icon(ft.Icons.LOGOUT, color="#EF4444", size=22),
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor="#1F2937",
                        alignment=ft.alignment.center,
                    ),
                    ft.Text("Logout", size=14, weight=ft.FontWeight.W_500, color="#EF4444", expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#6B7280", size=20),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border_radius=12,
            bgcolor="#1a1a2e",
            border=ft.border.all(1, "#EF4444"),
            on_click=lambda e: logout_callback(),
            ink=True,
        )
        
        # Main layout
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["#0f0f23", "#0a0a14"],
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
                        ft.Text("Settings", size=16, weight=ft.FontWeight.W_600, color="white"),
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
        )
        page.update()
    
    return show_view
