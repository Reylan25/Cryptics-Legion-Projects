"""
Admin Activity Logs Page
View all admin activities and system events
"""

import flet as ft
from core import db


class AdminLogsPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        self.logs = []
        
    def build(self):
        """Build activity logs page"""
        
        # Load logs
        self.logs = db.get_admin_logs(limit=100)
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Back to Dashboard",
                    on_click=lambda _: self.on_navigate("admin_dashboard")
                ),
                ft.Text(
                    "Activity Logs",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.REFRESH_ROUNDED,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Refresh",
                    on_click=self.refresh_logs
                ),
            ]),
            bgcolor=ft.Colors.ORANGE_700,
            padding=16,
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Summary
        total_logs = len(self.logs)
        unique_admins = len(set(log[1] for log in self.logs))  # admin_id
        
        summary = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.HISTORY_ROUNDED, size=20, color=ft.Colors.PRIMARY),
                    ft.Text(
                        f"{total_logs} Activities",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE
                    ),
                ], spacing=8),
                ft.Row([
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, size=20, color=ft.Colors.PRIMARY),
                    ft.Text(
                        f"{unique_admins} Admin(s)",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE
                    ),
                ], spacing=8),
            ], spacing=20),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            bgcolor="#2C2C2E",
            margin=ft.margin.symmetric(horizontal=20, vertical=12),
            border_radius=10
        )
        
        # Logs list
        self.logs_column = ft.Column(
            [self.create_log_item(log) for log in self.logs],
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )
        
        logs_list = ft.Container(
            content=self.logs_column,
            padding=ft.padding.only(left=20, right=20, top=0, bottom=20),
            expand=True
        )
        
        # Empty state
        if not self.logs:
            logs_list = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.Icons.HISTORY_ROUNDED,
                        size=80,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "No activity logs yet",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "Admin activities will appear here",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=40,
                expand=True,
                alignment=ft.alignment.center
            )
        
        # Main content
        content = ft.Column([
            header,
            summary,
            logs_list,
        ], spacing=0, expand=True)
        
        return content
    
    def create_log_item(self, log: tuple):
        """Create a log item"""
        
        # log: (id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username)
        log_id, admin_id, action, target_user_id, details, timestamp, admin_username, target_username = log
        
        # Format timestamp
        from datetime import datetime
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%b %d, %Y")
            time_str = dt.strftime("%I:%M %p")
        except:
            date_str = timestamp
            time_str = ""
        
        # Icon and color based on action
        action_config = {
            "login": {
                "icon": ft.Icons.LOGIN_ROUNDED,
                "color": ft.Colors.GREEN_400,
                "label": "Login"
            },
            "logout": {
                "icon": ft.Icons.LOGOUT_ROUNDED,
                "color": ft.Colors.BLUE_400,
                "label": "Logout"
            },
            "delete_user": {
                "icon": ft.Icons.DELETE_FOREVER_ROUNDED,
                "color": ft.Colors.ERROR,
                "label": "Delete User"
            },
            "view_users": {
                "icon": ft.Icons.VISIBILITY_ROUNDED,
                "color": ft.Colors.PURPLE_400,
                "label": "View Users"
            },
            "view_logs": {
                "icon": ft.Icons.HISTORY_ROUNDED,
                "color": ft.Colors.ORANGE_400,
                "label": "View Logs"
            },
        }
        
        config = action_config.get(action, {
            "icon": ft.Icons.INFO_ROUNDED,
            "color": ft.Colors.GREY_400,
            "label": action.replace("_", " ").title()
        })
        
        # Build description
        if target_username:
            description = f"{config['label']} - Target: {target_username}"
        else:
            description = config['label']
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(
                        config["icon"],
                        size=24,
                        color=config["color"]
                    ),
                    bgcolor="#2C2C2E",
                    border_radius=25,
                    width=48,
                    height=48,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(
                        description,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        details or "No details",
                        size=12,
                        color=ft.Colors.GREY_400,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    ft.Row([
                        ft.Icon(
                            ft.Icons.PERSON_ROUNDED,
                            size=14,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            admin_username,
                            size=11,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text("â€¢", size=11, color=ft.Colors.GREY_400),
                        ft.Icon(
                            ft.Icons.CALENDAR_TODAY_ROUNDED,
                            size=14,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            date_str,
                            size=11,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text("â€¢", size=11, color=ft.Colors.GREY_400),
                        ft.Icon(
                            ft.Icons.ACCESS_TIME_ROUNDED,
                            size=14,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            time_str,
                            size=11,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=4),
                ], spacing=4, expand=True),
            ], spacing=12),
            padding=14,
            bgcolor="#2C2C2E",
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def refresh_logs(self, e):
        """Refresh activity logs"""
        
        # Reload logs
        self.logs = db.get_admin_logs(limit=100)
        
        # Log this action
        db.log_admin_activity(
            self.admin_data.get("id"),
            "view_logs",
            None,
            "Refreshed activity logs"
        )
        
        # Update list
        self.logs_column.controls = [
            self.create_log_item(log) for log in self.logs
        ]
        
        if not self.logs:
            self.logs_column.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.HISTORY_ROUNDED,
                            size=60,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            "No activity logs yet",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_400
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=40,
                    alignment=ft.alignment.center
                )
            ]
        
        # Show success message
        snackbar = ft.SnackBar(
            content=ft.Text(f"Refreshed - {len(self.logs)} activities loaded"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.show_snack_bar(snackbar)
        
        self.page.update()



