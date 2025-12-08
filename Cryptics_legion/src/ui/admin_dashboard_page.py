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
                "all_expenses",
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Total Amount",
                f"₱{stats.get('total_amount', 0):,.2f}",
                ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                ft.Colors.GREEN_400,
                "all_expenses",
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Active Users (30d)",
                str(stats.get("active_users", 0)),
                ft.Icons.TRENDING_UP_ROUNDED,
                ft.Colors.PURPLE_400,
                "users",
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "New Users (This Month)",
                str(stats.get("new_users_this_month", 0)),
                ft.Icons.PERSON_ADD_ROUNDED,
                ft.Colors.CYAN_400,
                "users",
                col={"xs": 6, "sm": 6, "md": 4, "lg": 2}
            ),
            self.create_stat_card(
                "Total Accounts",
                str(stats.get("total_accounts", 0)),
                ft.Icons.ACCOUNT_BALANCE_ROUNDED,
                ft.Colors.PINK_400,
                "all_accounts",
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
        recent_logs = db.get_admin_logs(limit=10)
        
        recent_activity = ft.Container(
            content=ft.Column([
                # Responsive Header
                ft.ResponsiveRow([
                    ft.Column([
                        ft.Text(
                            "Recent Activity",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Latest admin actions and system events",
                            size=13,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=2, col={"xs": 12, "sm": 12, "md": 8}),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.HISTORY_ROUNDED, size=16, color=ft.Colors.BLUE_400),
                            ft.Text(
                                f"{len(recent_logs)} recent",
                                size=12,
                                color=ft.Colors.BLUE_400,
                                weight=ft.FontWeight.W_500
                            )
                        ], spacing=6, alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor="#0A2540",
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20,
                        border=ft.border.all(1, ft.Colors.BLUE_800),
                        col={"xs": 12, "sm": 12, "md": 4},
                        margin=ft.margin.only(top=10) if self.page.width < 768 else None
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Container(height=16),
                ft.Column([
                    self.create_enhanced_activity_item(log, idx) for idx, log in enumerate(recent_logs)
                ] if recent_logs else [
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.EVENT_NOTE_OUTLINED, size=48, color=ft.Colors.GREY_700),
                            ft.Text(
                                "No recent activity",
                                size=15,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREY_500
                            ),
                            ft.Text(
                                "Admin actions will appear here",
                                size=12,
                                color=ft.Colors.GREY_600
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                        padding=40,
                        alignment=ft.alignment.center
                    )
                ], spacing=6)
            ]),
            padding=ft.padding.all(12) if self.page.width < 768 else 20,
            bgcolor="#2C2C2E",
            border_radius=12,
            margin=ft.margin.only(top=8),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
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
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1
                ),
                ft.Text(
                    title,
                    size=12,
                    color=ft.Colors.GREY_400,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=2
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
        """Create an activity log item (deprecated - use create_enhanced_activity_item)"""
        
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
                        f"{admin_username} • {time_str}",
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
    
    def create_enhanced_activity_item(self, log: tuple, index: int):
        """Create an enhanced activity log item with better visuals"""
        
        # log: (id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username)
        log_id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username = log
        
        # Check if mobile view
        is_mobile = self.page.width < 768
        
        # Format timestamp - relative time
        from datetime import datetime
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = now - dt
            
            if diff.days == 0:
                if diff.seconds < 60:
                    time_str = "Just now"
                elif diff.seconds < 3600:
                    minutes = diff.seconds // 60
                    time_str = f"{minutes}m ago"
                else:
                    hours = diff.seconds // 3600
                    time_str = f"{hours}h ago"
            elif diff.days == 1:
                time_str = "Yesterday"
            elif diff.days < 7:
                time_str = f"{diff.days}d ago"
            else:
                time_str = dt.strftime("%b %d, %Y")
            
            # Full timestamp for tooltip
            full_time = dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            time_str = timestamp
            full_time = timestamp
        
        # Enhanced icon and color based on action with categories
        action_config = {
            "login": {
                "icon": ft.Icons.LOGIN_ROUNDED,
                "color": ft.Colors.GREEN_400,
                "bg": "#0A3A2A",
                "border": ft.Colors.GREEN_800,
                "category": "Authentication"
            },
            "logout": {
                "icon": ft.Icons.LOGOUT_ROUNDED,
                "color": ft.Colors.BLUE_400,
                "bg": "#0A2540",
                "border": ft.Colors.BLUE_800,
                "category": "Authentication"
            },
            "delete_user": {
                "icon": ft.Icons.DELETE_FOREVER_ROUNDED,
                "color": ft.Colors.RED_400,
                "bg": "#3A0A0A",
                "border": ft.Colors.RED_800,
                "category": "User Management"
            },
            "view_users": {
                "icon": ft.Icons.PEOPLE_OUTLINED,
                "color": ft.Colors.PURPLE_400,
                "bg": "#2A0A3A",
                "border": ft.Colors.PURPLE_800,
                "category": "User Management"
            },
            "view_logs": {
                "icon": ft.Icons.DESCRIPTION_OUTLINED,
                "color": ft.Colors.ORANGE_400,
                "bg": "#3A2A0A",
                "border": ft.Colors.ORANGE_800,
                "category": "System"
            },
            "create_announcement": {
                "icon": ft.Icons.CAMPAIGN_ROUNDED,
                "color": ft.Colors.AMBER_400,
                "bg": "#3A2A0A",
                "border": ft.Colors.AMBER_800,
                "category": "Communications"
            },
            "add_policy_rule": {
                "icon": ft.Icons.RULE_ROUNDED,
                "color": ft.Colors.CYAN_400,
                "bg": "#0A2A3A",
                "border": ft.Colors.CYAN_800,
                "category": "Policy"
            },
        }
        
        config = action_config.get(action, {
            "icon": ft.Icons.INFO_ROUNDED,
            "color": ft.Colors.GREY_400,
            "bg": "#1C1C1E",
            "border": ft.Colors.GREY_700,
            "category": "General"
        })
        
        # Format action text
        action_text = details or action.replace("_", " ").title()
        
        # Add target user info if available
        if target_username and target_username != "None":
            action_text += f" → {target_username}"
        
        # Responsive sizing
        icon_size = 14 if is_mobile else 16
        icon_container_size = 32 if is_mobile else 36
        timeline_width = 36 if is_mobile else 40
        content_padding = 10 if is_mobile else 14
        text_size = 13 if is_mobile else 14
        meta_text_size = 11 if is_mobile else 12
        
        return ft.Container(
            content=ft.Row([
                # Timeline dot with connecting line
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(config["icon"], size=icon_size, color=config["color"]),
                            width=icon_container_size,
                            height=icon_container_size,
                            border_radius=icon_container_size // 2,
                            bgcolor=config["bg"],
                            border=ft.border.all(2, config["border"]),
                            alignment=ft.alignment.center,
                        ),
                        # Connecting line (hide for last item)
                        ft.Container(
                            width=2,
                            height=40 if not is_mobile else 36,
                            bgcolor=ft.Colors.GREY_800,
                            visible=index < 9  # Hide line for last item
                        ) if index < 9 else ft.Container()
                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    width=timeline_width
                ),
                # Content
                ft.Container(
                    content=ft.Column([
                        # Action text and category badge - wrap on mobile
                        ft.Column([
                            ft.Text(
                                action_text,
                                size=text_size,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.WHITE,
                                max_lines=2 if is_mobile else None,
                                overflow=ft.TextOverflow.ELLIPSIS if is_mobile else None
                            ),
                            ft.Container(
                                content=ft.Text(
                                    config["category"],
                                    size=9 if is_mobile else 10,
                                    weight=ft.FontWeight.BOLD,
                                    color=config["color"]
                                ),
                                bgcolor=config["bg"],
                                padding=ft.padding.symmetric(horizontal=6 if is_mobile else 8, vertical=2 if is_mobile else 3),
                                border_radius=10,
                                border=ft.border.all(1, config["border"])
                            )
                        ], spacing=8),
                        # Meta info - stack on mobile
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON_OUTLINE, size=meta_text_size, color=ft.Colors.GREY_500),
                                ft.Text(
                                    admin_username,
                                    size=meta_text_size,
                                    color=ft.Colors.GREY_400,
                                    weight=ft.FontWeight.W_500
                                ),
                            ], spacing=4),
                            ft.Row([
                                ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=meta_text_size, color=ft.Colors.GREY_500),
                                ft.Text(
                                    time_str,
                                    size=meta_text_size,
                                    color=ft.Colors.GREY_400,
                                    tooltip=full_time
                                ),
                            ], spacing=4),
                        ], spacing=4) if is_mobile else ft.Row([
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=meta_text_size, color=ft.Colors.GREY_500),
                            ft.Text(
                                admin_username,
                                size=meta_text_size,
                                color=ft.Colors.GREY_400,
                                weight=ft.FontWeight.W_500
                            ),
                            ft.Container(
                                content=ft.Text("•", size=meta_text_size, color=ft.Colors.GREY_600),
                                margin=ft.margin.symmetric(horizontal=4)
                            ),
                            ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=meta_text_size, color=ft.Colors.GREY_500),
                            ft.Text(
                                time_str,
                                size=meta_text_size,
                                color=ft.Colors.GREY_400,
                                tooltip=full_time
                            ),
                        ], spacing=6),
                    ], spacing=6),
                    bgcolor="#1C1C1E",
                    padding=content_padding,
                    border_radius=8 if is_mobile else 10,
                    border=ft.border.all(1, ft.Colors.GREY_800),
                    expand=True,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                        offset=ft.Offset(0, 1)
                    )
                ),
            ], spacing=8 if is_mobile else 12),
            margin=ft.margin.only(bottom=0)
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



