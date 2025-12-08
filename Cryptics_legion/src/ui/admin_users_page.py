"""
Admin User Management Page
View, search, and manage all user accounts
"""

import flet as ft
from core import db


class AdminUserManagementPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        self.users = []
        self.filtered_users = []
        self.search_query = ""
        
    def build(self):
        """Build user management page"""
        
        # Load all users
        self.users = db.get_all_users_for_admin()
        self.filtered_users = self.users.copy()
        
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
                    "User Management",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
            ]),
            bgcolor=ft.Colors.BLUE_700,
            padding=16,
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Search bar
        self.search_field = ft.TextField(
            hint_text="Search users by username or email...",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_radius=10,
            filled=True,
            bgcolor="#2C2C2E",
            on_change=self.handle_search
        )
        
        search_bar = ft.Container(
            content=self.search_field,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )
        
        # Summary
        total_users = len(self.users)
        total_expenses = sum(int(user[6]) if user[6] else 0 for user in self.users)  # expense_count
        total_spent = sum(float(user[7]) if user[7] else 0.0 for user in self.users)  # total_spent
        
        summary = ft.Container(
            content=ft.Row([
                self.create_summary_chip(
                    f"{total_users} Users",
                    ft.Icons.PEOPLE_ROUNDED,
                    ft.Colors.BLUE_400
                ),
                self.create_summary_chip(
                    f"{total_expenses} Expenses",
                    ft.Icons.RECEIPT_LONG_ROUNDED,
                    ft.Colors.ORANGE_400
                ),
                self.create_summary_chip(
                    f"â‚±{total_spent:,.2f} Total",
                    ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                    ft.Colors.GREEN_400
                ),
            ], spacing=12, wrap=True),
            padding=ft.padding.symmetric(horizontal=20, vertical=0)
        )
        
        # User list
        self.user_list_column = ft.Column(
            [self.create_user_card(user) for user in self.filtered_users],
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )
        
        user_list = ft.Container(
            content=self.user_list_column,
            padding=ft.padding.only(left=20, right=20, top=12, bottom=20),
            expand=True
        )
        
        # Empty state
        if not self.filtered_users:
            user_list = ft.Container(
                content=ft.Column([
                    ft.Icon(
                        ft.Icons.SEARCH_OFF_ROUNDED,
                        size=80,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "No users found",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Text(
                        "Try adjusting your search",
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
            search_bar,
            summary,
            user_list,
        ], spacing=0, expand=True)
        
        return content
    
    def create_summary_chip(self, text: str, icon, color):
        """Create a summary chip"""
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color=color),
                ft.Text(
                    text,
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.WHITE
                ),
            ], spacing=8),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor="#2C2C2E",
            border_radius=20,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def create_user_card(self, user: tuple):
        """Create a user card"""
        
        # user from DB: (id, username, full_name, email, last_login, has_seen_onboarding, expense_count, total_spent)
        user_id = user[0]
        username = user[1]
        full_name = user[2] or username
        email = user[3]
        last_login = user[4]
        expense_count = int(user[6]) if user[6] else 0
        total_spent = float(user[7]) if user[7] else 0.0
        
        # Format date
        from datetime import datetime
        try:
            if last_login:
                dt = datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%b %d, %Y")
            else:
                date_str = "Never"
        except:
            date_str = "Unknown"
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                            size=40,
                            color=ft.Colors.PRIMARY
                        ),
                        bgcolor=ft.Colors.BLUE_900,
                        border_radius=25,
                        width=50,
                        height=50,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text(
                            username,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            email or "No email",
                            size=12,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=2, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                        icon_color=ft.Colors.ERROR,
                        tooltip="Delete User",
                        on_click=lambda _, uid=user_id, uname=username: self.confirm_delete_user(uid, uname)
                    )
                ], spacing=12),
                ft.Divider(height=12, color=ft.Colors.GREY_700),
                ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.RECEIPT_LONG_ROUNDED, size=16, color=ft.Colors.GREY_400),
                        ft.Text(
                            f"{expense_count} expenses",
                            size=13,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=16, color=ft.Colors.GREY_400),
                        ft.Text(
                            f"â‚±{total_spent:,.2f}",
                            size=13,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=6),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, size=16, color=ft.Colors.GREY_400),
                        ft.Text(
                            date_str,
                            size=13,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=6),
                ], spacing=16, wrap=True),
            ], spacing=8),
            padding=16,
            bgcolor="#2C2C2E",
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def handle_search(self, e):
        """Handle search input"""
        
        self.search_query = e.control.value.lower()
        
        if not self.search_query:
            self.filtered_users = self.users.copy()
        else:
            self.filtered_users = [
                user for user in self.users
                if self.search_query in user[1].lower() or  # username
                   (user[2] and self.search_query in user[2].lower()) or  # full_name
                   (user[3] and self.search_query in user[3].lower())  # email
            ]
        
        # Update user list
        self.user_list_column.controls = [
            self.create_user_card(user) for user in self.filtered_users
        ]
        
        if not self.filtered_users:
            self.user_list_column.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.SEARCH_OFF_ROUNDED,
                            size=60,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            "No users found",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_400
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=40,
                    alignment=ft.alignment.center
                )
            ]
        
        self.page.update()
    
    def confirm_delete_user(self, user_id: int, username: str):
        """Show confirmation dialog before deleting user"""
        
        def handle_confirm(e):
            dialog.open = False
            self.page.update()
            self.delete_user(user_id, username)
        
        def handle_cancel(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete User?"),
            content=ft.Text(
                f"Are you sure you want to delete user '{username}'?\n\n"
                "This will permanently delete:\n"
                "â€¢ User account\n"
                "â€¢ All expenses\n"
                "â€¢ All accounts\n"
                "â€¢ All personal data\n\n"
                "This action cannot be undone!",
                size=14
            ),
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.TextButton(
                    "Delete",
                    on_click=handle_confirm,
                    style=ft.ButtonStyle(color=ft.Colors.ERROR)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def delete_user(self, user_id: int, username: str):
        """Delete user and refresh list"""
        
        # Delete user
        success = db.delete_user_by_admin(user_id)
        
        if success:
            # Log activity
            db.log_admin_activity(
                self.admin_data.get("id"),
                "delete_user",
                user_id,
                f"Deleted user '{username}'"
            )
            
            # Show success message
            snackbar = ft.SnackBar(
                content=ft.Text(f"User '{username}' deleted successfully"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.show_snack_bar(snackbar)
            
            # Reload users
            self.users = db.get_all_users_for_admin()
            self.handle_search(type('obj', (object,), {'control': type('obj', (object,), {'value': self.search_query})()})())
        else:
            # Show error message
            snackbar = ft.SnackBar(
                content=ft.Text(f"Failed to delete user '{username}'"),
                bgcolor=ft.Colors.ERROR
            )
            self.page.show_snack_bar(snackbar)



