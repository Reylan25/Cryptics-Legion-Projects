"""
Admin Dashboard Page
Main landing page for admin users with system statistics and quick actions
"""

import flet as ft
from core import db
from components.enhanced_icons import EnhancedIcon


class AdminDashboardPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        
    def build(self):
        """Build admin dashboard page"""
        
        # Get system statistics
        stats = db.get_system_statistics()
        
        # Statistics Cards - Responsive Grid
        stats_cards = ft.ResponsiveRow([
            self.create_stat_card(
                "Total Users",
                str(stats.get("total_users", 0)),
                ft.Icons.PEOPLE_ROUNDED,
                ft.Colors.BLUE_400,
                "users",
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Total Expenses",
                str(stats.get("total_expenses", 0)),
                ft.Icons.RECEIPT_LONG_ROUNDED,
                ft.Colors.ORANGE_400,
                None,
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Total Amount",
                f"â‚±{stats.get('total_amount', 0):,.2f}",
                ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                ft.Colors.GREEN_400,
                None,
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Active Users (30d)",
                str(stats.get("active_users", 0)),
                ft.Icons.TRENDING_UP_ROUNDED,
                ft.Colors.PURPLE_400,
                None,
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "New Users (This Month)",
                str(stats.get("new_users_this_month", 0)),
                ft.Icons.PERSON_ADD_ROUNDED,
                ft.Colors.CYAN_400,
                None,
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Total Accounts",
                str(stats.get("total_accounts", 0)),
                ft.Icons.ACCOUNT_BALANCE_ROUNDED,
                ft.Colors.PINK_400,
                None,
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
        ], spacing=12, run_spacing=12)
        
        # Quick Actions - Responsive
        quick_actions = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Quick Actions",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Container(height=12),
                ft.ResponsiveRow([
                    self.create_action_button(
                        "User Management",
                        ft.Icons.MANAGE_ACCOUNTS_ROUNDED,
                        ft.Colors.BLUE_700,
                        "users",
                        col={"xs": 12, "sm": 6, "md": 6, "lg": 6}
                    ),
                    self.create_action_button(
                        "Activity Logs",
                        ft.Icons.HISTORY_ROUNDED,
                        ft.Colors.ORANGE_700,
                        "logs",
                        col={"xs": 12, "sm": 6, "md": 6, "lg": 6}
                    ),
                ], spacing=12, run_spacing=12),
            ]),
            padding=20,
            bgcolor="#2C2C2E",
            border_radius=12,
            margin=ft.margin.only(top=8)
        )
        
        # Recent Activity Section
        recent_logs = db.get_admin_logs(limit=5)
        
        recent_activity = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Recent Activity",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Container(height=12),
                ft.Column([
                    self.create_activity_item(log) for log in recent_logs
                ] if recent_logs else [
                    ft.Text(
                        "No recent activity",
                        size=14,
                        color=ft.Colors.GREY_400,
                        italic=True
                    )
                ], spacing=8)
            ]),
            padding=20,
            bgcolor="#2C2C2E",
            border_radius=12,
            margin=ft.margin.only(top=8)
        )
        
        # Main content with responsive padding
        content = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Container(height=12),
                    stats_cards,
                    ft.Container(height=12),
                    quick_actions,
                    recent_activity,
                    ft.Container(height=20),
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=ft.padding.symmetric(horizontal=16, vertical=0)
            )
        ], spacing=0, expand=True)
        
        return content
    
    def create_stat_card(self, title: str, value: str, icon, color, navigate_to=None, col=None):
        """Create a responsive statistics card"""
        
        card_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=32, color=color),
                    ft.Container(expand=True),
                    ft.Icon(
                        ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                        size=16,
                        color=ft.Colors.GREY_400
                    ) if navigate_to else ft.Container()
                ]),
                ft.Container(height=12),
                ft.Text(
                    value,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Text(
                    title,
                    size=13,
                    color=ft.Colors.GREY_400
                ),
            ], spacing=4),
            padding=16,
            bgcolor="#2C2C2E",
            border_radius=12,
            height=140,
            col=col,
            on_click=lambda _: self.on_navigate(navigate_to) if navigate_to else None,
            ink=True if navigate_to else False
        )
        
        return card_content
    
    def create_action_button(self, title: str, icon, color, navigate_to: str, col=None):
        """Create a responsive quick action button"""
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=24, color=ft.Colors.WHITE),
                ft.Text(
                    title,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.WHITE
                ),
            ], spacing=12, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            bgcolor=color,
            border_radius=10,
            col=col,
            on_click=lambda _: self.on_navigate(navigate_to),
            ink=True
        )
    
    def create_activity_item(self, log: tuple):
        """Create an activity log item"""
        
        # log: (id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username)
        log_id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username = log
        
        # Format timestamp
        from datetime import datetime
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            time_str = dt.strftime("%b %d, %I:%M %p")
        except:
            time_str = timestamp
        
        # Icon based on action
        icon_map = {
            "login": ft.Icons.LOGIN_ROUNDED,
            "logout": ft.Icons.LOGOUT_ROUNDED,
            "delete_user": ft.Icons.DELETE_FOREVER_ROUNDED,
            "view_users": ft.Icons.VISIBILITY_ROUNDED,
            "view_logs": ft.Icons.HISTORY_ROUNDED,
        }
        
        action_icon = icon_map.get(action, ft.Icons.INFO_ROUNDED)
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(action_icon, size=20, color=ft.Colors.PRIMARY),
                ft.Column([
                    ft.Text(
                        details or action.replace("_", " ").title(),
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        f"{admin_username} â€¢ {time_str}",
                        size=11,
                        color=ft.Colors.GREY_400
                    ),
                ], spacing=2, expand=True),
            ], spacing=12),
            padding=12,
            bgcolor="#1C1C1E",
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def handle_logout(self, e):
        """Handle admin logout"""
        
        # Log logout activity
        from core import admin_auth
        admin_auth.logout_admin(
            self.admin_data.get("id"),
            self.admin_data.get("username", "")
        )
        
        # Clear state
        self.state.pop("admin", None)
        self.state.pop("is_admin", None)
        
        # Navigate to login
        self.on_navigate("login")



