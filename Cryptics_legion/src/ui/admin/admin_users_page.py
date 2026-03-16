"""
Admin User Management Page
View, search, and manage all user accounts
"""

import flet as ft
from core import db
from utils.currency import get_currency_symbol


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
            content=ft.Column([
                ft.Row([
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
                        f"₱{total_spent:,.2f} Total",
                        ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        ft.Colors.GREEN_400
                    ),
                ], spacing=12, wrap=True),
                ft.Text(
                    "Note: Total amounts shown in mixed currencies",
                    size=10,
                    color=ft.Colors.GREY_500,
                    italic=True
                )
            ], spacing=4),
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
        """Create an enhanced user card with detailed information"""
        
        # user from DB: (id, username, full_name, email, last_login, has_seen_onboarding, expense_count, total_spent, preferred_currency)
        user_id = user[0]
        username = user[1]
        full_name = user[2] or username
        email = user[3]
        last_login = user[4]
        has_seen_onboarding = user[5]
        expense_count = int(user[6]) if user[6] else 0
        total_spent = float(user[7]) if user[7] else 0.0
        user_currency = user[8] if len(user) > 8 and user[8] else "PHP"
        
        # Get currency symbol
        currency_symbol = get_currency_symbol(user_currency)
        
        # Format date and calculate activity
        from datetime import datetime, timedelta
        try:
            if last_login:
                dt = datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%b %d, %Y")
                time_str = dt.strftime("%I:%M %p")
                
                # Calculate days since last login
                days_ago = (datetime.now() - dt).days
                if days_ago == 0:
                    activity_status = "Active Today"
                    status_color = ft.Colors.GREEN_400
                elif days_ago <= 7:
                    activity_status = f"Active {days_ago}d ago"
                    status_color = ft.Colors.BLUE_400
                elif days_ago <= 30:
                    activity_status = f"Active {days_ago}d ago"
                    status_color = ft.Colors.ORANGE_400
                else:
                    activity_status = "Inactive"
                    status_color = ft.Colors.RED_400
            else:
                date_str = "Never"
                time_str = "--"
                activity_status = "Never Logged In"
                status_color = ft.Colors.GREY_500
        except:
            date_str = "Unknown"
            time_str = "--"
            activity_status = "Unknown"
            status_color = ft.Colors.GREY_500
        
        # Calculate average expense
        avg_expense = total_spent / expense_count if expense_count > 0 else 0.0
        
        # Onboarding status
        onboarding_status = "Completed" if has_seen_onboarding else "Pending"
        onboarding_color = ft.Colors.GREEN_400 if has_seen_onboarding else ft.Colors.AMBER_400
        
        # User initials for avatar
        initials = "".join([word[0].upper() for word in full_name.split()[:2]])
        if not initials:
            initials = username[0].upper()
        
        return ft.Container(
            content=ft.Column([
                # Header Row with Avatar and Actions
                ft.Row([
                    # Enhanced Avatar
                    ft.Container(
                        content=ft.Text(
                            initials,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.BLUE_700,
                        border_radius=30,
                        width=60,
                        height=60,
                        alignment=ft.alignment.center,
                        border=ft.border.all(2, ft.Colors.BLUE_400)
                    ),
                    # User Info
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                username.upper(),
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            ft.Container(
                                content=ft.Text(
                                    activity_status,
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                bgcolor=status_color,
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=10
                            )
                        ], spacing=8),
                        ft.Text(
                            full_name,
                            size=13,
                            color=ft.Colors.GREY_300,
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Row([
                            ft.Icon(ft.Icons.EMAIL_OUTLINED, size=12, color=ft.Colors.GREY_500),
                            ft.Text(
                                email or "No email provided",
                                size=11,
                                color=ft.Colors.GREY_500,
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                        ], spacing=4),
                    ], spacing=2, expand=True),
                    # Action Buttons
                    ft.Column([
                        ft.IconButton(
                            icon=ft.Icons.VISIBILITY_ROUNDED,
                            icon_color=ft.Colors.BLUE_400,
                            icon_size=20,
                            tooltip="View Details",
                            on_click=lambda _, u=user: self.show_user_details(u)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                            icon_color=ft.Colors.ERROR,
                            icon_size=20,
                            tooltip="Delete User",
                            on_click=lambda _, uid=user_id, uname=username: self.confirm_delete_user(uid, uname)
                        ),
                    ], spacing=0),
                ], spacing=12),
                
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                
                # Statistics Grid
                ft.Container(
                    content=ft.Row([
                        # Expenses Count
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.RECEIPT_LONG_ROUNDED, size=24, color=ft.Colors.ORANGE_400),
                                ft.Text(
                                    str(expense_count),
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "Expenses",
                                    size=11,
                                    color=ft.Colors.GREY_500
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#1C1C1E",
                            border_radius=10,
                            padding=12,
                            expand=True,
                            border=ft.border.all(1, ft.Colors.GREY_800)
                        ),
                        # Total Spent
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=24, color=ft.Colors.GREEN_400),
                                ft.Text(
                                    f"{currency_symbol}{total_spent:,.0f}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "Total Spent",
                                    size=11,
                                    color=ft.Colors.GREY_500
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#1C1C1E",
                            border_radius=10,
                            padding=12,
                            expand=True,
                            border=ft.border.all(1, ft.Colors.GREY_800)
                        ),
                        # Average
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.TRENDING_UP_ROUNDED, size=24, color=ft.Colors.PURPLE_400),
                                ft.Text(
                                    f"{currency_symbol}{avg_expense:,.0f}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "Average",
                                    size=11,
                                    color=ft.Colors.GREY_500
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            bgcolor="#1C1C1E",
                            border_radius=10,
                            padding=12,
                            expand=True,
                            border=ft.border.all(1, ft.Colors.GREY_800)
                        ),
                    ], spacing=8),
                    margin=ft.margin.only(top=4, bottom=4)
                ),
                
                # Additional Info Row
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(ft.Icons.LOGIN_ROUNDED, size=14, color=ft.Colors.CYAN_400),
                            ft.Column([
                                ft.Text("Last Login", size=9, color=ft.Colors.GREY_500),
                                ft.Text(date_str, size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                                ft.Text(time_str, size=9, color=ft.Colors.GREY_400),
                            ], spacing=0),
                        ], spacing=6),
                        ft.Container(width=1, height=30, bgcolor=ft.Colors.GREY_800),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, size=14, color=onboarding_color),
                            ft.Column([
                                ft.Text("Onboarding", size=9, color=ft.Colors.GREY_500),
                                ft.Text(onboarding_status, size=11, weight=ft.FontWeight.W_500, color=onboarding_color),
                            ], spacing=0),
                        ], spacing=6),
                        ft.Container(width=1, height=30, bgcolor=ft.Colors.GREY_800),
                        ft.Row([
                            ft.Icon(ft.Icons.FINGERPRINT_ROUNDED, size=14, color=ft.Colors.PINK_400),
                            ft.Column([
                                ft.Text("User ID", size=9, color=ft.Colors.GREY_500),
                                ft.Text(f"#{user_id}", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            ], spacing=0),
                        ], spacing=6),
                    ], spacing=12, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor="#1C1C1E",
                    border_radius=8,
                    padding=10,
                    margin=ft.margin.only(top=4)
                ),
            ], spacing=8),
            padding=16,
            bgcolor="#2C2C2E",
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_700),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
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
    
    def show_user_details(self, user: tuple):
        """Show detailed user information in a modal"""
        
        user_id = user[0]
        username = user[1]
        full_name = user[2] or username
        email = user[3]
        last_login = user[4]
        has_seen_onboarding = user[5]
        expense_count = int(user[6]) if user[6] else 0
        total_spent = float(user[7]) if user[7] else 0.0
        user_currency = user[8] if len(user) > 8 and user[8] else "PHP"
        
        # Get currency symbol
        currency_symbol = get_currency_symbol(user_currency)
        
        # Get user's recent expenses
        expenses = db.get_user_expenses_for_admin(user_id, limit=5)
        
        # Get user accounts
        accounts = db.get_user_accounts_for_admin(user_id)
        
        from datetime import datetime
        try:
            if last_login:
                dt = datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S")
                last_login_formatted = dt.strftime("%B %d, %Y at %I:%M %p")
            else:
                last_login_formatted = "Never logged in"
        except:
            last_login_formatted = "Unknown"
        
        avg_expense = total_spent / expense_count if expense_count > 0 else 0.0
        
        details_dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.PERSON_ROUNDED, color=ft.Colors.BLUE_400),
                ft.Text(f"User Details: {username}", size=18, weight=ft.FontWeight.BOLD)
            ], spacing=8),
            content=ft.Container(
                content=ft.Column([
                    # Personal Information Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Personal Information", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                            ft.Divider(height=1, color=ft.Colors.GREY_700),
                            self.create_info_row("Full Name", full_name, ft.Icons.PERSON_OUTLINE),
                            self.create_info_row("Username", username, ft.Icons.ACCOUNT_CIRCLE_OUTLINED),
                            self.create_info_row("Email", email or "Not provided", ft.Icons.EMAIL_OUTLINED),
                            self.create_info_row("User ID", f"#{user_id}", ft.Icons.FINGERPRINT),
                        ], spacing=8),
                        padding=12,
                        bgcolor="#2C2C2E",
                        border_radius=10
                    ),
                    
                    # Activity Information Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Activity Information", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                            ft.Divider(height=1, color=ft.Colors.GREY_700),
                            self.create_info_row("Last Login", last_login_formatted, ft.Icons.LOGIN),
                            self.create_info_row("Onboarding", "Completed" if has_seen_onboarding else "Pending", ft.Icons.CHECK_CIRCLE),
                            self.create_info_row("Status", "Active" if last_login else "Inactive", ft.Icons.CIRCLE),
                        ], spacing=8),
                        padding=12,
                        bgcolor="#2C2C2E",
                        border_radius=10
                    ),
                    
                    # Financial Summary Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Financial Summary", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_400),
                            ft.Divider(height=1, color=ft.Colors.GREY_700),
                            ft.Row([
                                self.create_stat_box("Total Expenses", str(expense_count), ft.Icons.RECEIPT_LONG, ft.Colors.ORANGE_400),
                                self.create_stat_box("Total Spent", f"{currency_symbol}{total_spent:,.2f}", ft.Icons.ACCOUNT_BALANCE_WALLET, ft.Colors.GREEN_400),
                            ], spacing=12),
                            ft.Row([
                                self.create_stat_box("Average/Expense", f"{currency_symbol}{avg_expense:,.2f}", ft.Icons.TRENDING_UP, ft.Colors.PURPLE_400),
                                self.create_stat_box("Accounts", str(len(accounts)), ft.Icons.ACCOUNT_BALANCE, ft.Colors.CYAN_400),
                            ], spacing=12),
                        ], spacing=8),
                        padding=12,
                        bgcolor="#2C2C2E",
                        border_radius=10
                    ),
                    
                    # Recent Expenses Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Recent Expenses (Last 5)", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_400),
                            ft.Divider(height=1, color=ft.Colors.GREY_700),
                            ft.Column([
                                self.create_expense_row(exp, currency_symbol) for exp in expenses
                            ] if expenses else [
                                ft.Text("No expenses yet", size=12, color=ft.Colors.GREY_500, italic=True)
                            ], spacing=6),
                        ], spacing=8),
                        padding=12,
                        bgcolor="#2C2C2E",
                        border_radius=10
                    ),
                    
                    # Accounts Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("User Accounts", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400),
                            ft.Divider(height=1, color=ft.Colors.GREY_700),
                            ft.Column([
                                self.create_account_row(acc, currency_symbol) for acc in accounts
                            ] if accounts else [
                                ft.Text("No accounts created", size=12, color=ft.Colors.GREY_500, italic=True)
                            ], spacing=6),
                        ], spacing=8),
                        padding=12,
                        bgcolor="#2C2C2E",
                        border_radius=10
                    ),
                ], spacing=12, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=600
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.page.close(details_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#1C1C1E",
        )
        
        self.page.open(details_dialog)
    
    def create_info_row(self, label: str, value: str, icon):
        """Create an information row"""
        return ft.Row([
            ft.Icon(icon, size=16, color=ft.Colors.GREY_400),
            ft.Text(f"{label}:", size=12, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_500),
            ft.Text(value, size=12, color=ft.Colors.WHITE, expand=True),
        ], spacing=8)
    
    def create_stat_box(self, label: str, value: str, icon, color):
        """Create a stat box"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=20, color=color),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text(label, size=10, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            bgcolor="#1C1C1E",
            border_radius=8,
            padding=12,
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_800)
        )
    
    def create_expense_row(self, expense: tuple, currency_symbol: str = "₱"):
        """Create an expense row for details modal"""
        # expense: (id, description, amount, category, date, ...)
        description = expense[1]
        amount = float(expense[2])
        category = expense[3]
        date = expense[4]
        
        from datetime import datetime
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            date_str = dt.strftime("%b %d, %Y")
        except:
            date_str = date
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.RECEIPT, size=14, color=ft.Colors.ORANGE_400),
                ft.Column([
                    ft.Text(description[:30] + "..." if len(description) > 30 else description, 
                           size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                    ft.Text(f"{category} • {date_str}", size=9, color=ft.Colors.GREY_500),
                ], spacing=2, expand=True),
                ft.Text(f"{currency_symbol}{amount:,.2f}", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
            ], spacing=8),
            padding=8,
            bgcolor="#1C1C1E",
            border_radius=6,
            border=ft.border.all(1, ft.Colors.GREY_800)
        )
    
    def create_account_row(self, account: tuple, currency_symbol: str = "₱"):
        """Create an account row for details modal"""
        # account: (id, name, balance, currency, ...)
        name = account[1]
        balance = float(account[2])
        currency = account[3] if len(account) > 3 else "PHP"
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_BALANCE, size=14, color=ft.Colors.CYAN_400),
                ft.Text(name, size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500, expand=True),
                ft.Text(f"{currency_symbol}{balance:,.2f}", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400),
            ], spacing=8),
            padding=8,
            bgcolor="#1C1C1E",
            border_radius=6,
            border=ft.border.all(1, ft.Colors.GREY_800)
        )
    
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



