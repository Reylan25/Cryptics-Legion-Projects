"""
Admin All Accounts Page
View all accounts from all users in the system
"""

import flet as ft
from core import db
from utils.currency import get_currency_symbol


class AdminAllAccountsPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        self.accounts = []
        self.filtered_accounts = []
        self.search_query = ""
        
    def build(self):
        """Build all accounts page"""
        
        # Load all accounts
        self.accounts = db.get_all_accounts_for_admin()
        self.filtered_accounts = self.accounts.copy()
        
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
                    "All Accounts",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
            ]),
            bgcolor=ft.Colors.PINK_700,
            padding=16,
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Search Bar
        self.search_field = ft.TextField(
            hint_text="Search by account name or user...",
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
        total_accounts = len(self.accounts)
        total_balance = sum(float(acc[3]) if acc[3] else 0.0 for acc in self.accounts)  # balance
        
        summary = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.create_summary_chip(
                        f"{total_accounts} Total Accounts",
                        ft.Icons.ACCOUNT_BALANCE_ROUNDED,
                        ft.Colors.PINK_400
                    ),
                    self.create_summary_chip(
                        f"₱{total_balance:,.2f} Total Balance",
                        ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        ft.Colors.CYAN_400
                    ),
                ], spacing=12, wrap=True),
                ft.Text(
                    "Note: Balances shown in mixed currencies",
                    size=10,
                    color=ft.Colors.GREY_500,
                    italic=True
                )
            ], spacing=4),
            padding=ft.padding.symmetric(horizontal=20, vertical=0)
        )
        
        # Account list
        self.account_list_column = ft.Column(
            [self.create_account_card(acc) for acc in self.filtered_accounts],
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )
        
        account_list = ft.Container(
            content=self.account_list_column,
            padding=ft.padding.only(left=20, right=20, top=12, bottom=20),
            expand=True
        )
        
        # Main content
        return ft.Column([
            header,
            search_bar,
            summary,
            account_list,
        ], spacing=0, expand=True)
    
    def create_summary_chip(self, text: str, icon, color):
        """Create a summary chip"""
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=color),
                ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
            ], spacing=8),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor="#2C2C2E",
            border_radius=20,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def create_account_card(self, account: tuple):
        """Create an account card"""
        
        # account: (id, user_id, name, balance, currency, type, is_primary, username, user_currency)
        account_id = account[0]
        user_id = account[1]
        name = account[2]
        balance = float(account[3])
        currency = account[4] if len(account) > 4 else "PHP"
        account_type = account[5] if len(account) > 5 else "Bank"
        is_primary = account[6] if len(account) > 6 else 0
        username = account[7] if len(account) > 7 else "Unknown"
        user_currency = account[8] if len(account) > 8 else "PHP"
        
        # Get currency symbol
        currency_symbol = get_currency_symbol(user_currency)
        
        # Account type icons
        type_icons = {
            "Bank": ft.Icons.ACCOUNT_BALANCE_ROUNDED,
            "Cash": ft.Icons.PAYMENTS_ROUNDED,
            "Credit Card": ft.Icons.CREDIT_CARD_ROUNDED,
            "E-Wallet": ft.Icons.WALLET_ROUNDED,
            "Investment": ft.Icons.TRENDING_UP_ROUNDED,
        }
        type_icon = type_icons.get(account_type, ft.Icons.ACCOUNT_BALANCE_ROUNDED)
        
        # Account type colors
        type_colors = {
            "Bank": ft.Colors.BLUE_700,
            "Cash": ft.Colors.GREEN_700,
            "Credit Card": ft.Colors.PURPLE_700,
            "E-Wallet": ft.Colors.ORANGE_700,
            "Investment": ft.Colors.PINK_700,
        }
        type_color = type_colors.get(account_type, ft.Colors.BLUE_700)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    # Account Type Icon
                    ft.Container(
                        content=ft.Icon(type_icon, size=24, color=ft.Colors.WHITE),
                        bgcolor=type_color,
                        border_radius=25,
                        width=50,
                        height=50,
                        alignment=ft.alignment.center
                    ),
                    # Account Info
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                name,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "PRIMARY",
                                    size=9,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.BLUE_600,
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                border_radius=8
                            ) if is_primary else ft.Container(),
                        ], spacing=8),
                        ft.Row([
                            ft.Icon(ft.Icons.CATEGORY_ROUNDED, size=12, color=ft.Colors.GREY_400),
                            ft.Text(account_type, size=12, color=ft.Colors.GREY_400),
                            ft.Text("•", size=12, color=ft.Colors.GREY_400),
                            ft.Icon(ft.Icons.PERSON_ROUNDED, size=12, color=ft.Colors.GREY_400),
                            ft.Text(username, size=12, color=ft.Colors.GREY_400),
                        ], spacing=4),
                    ], spacing=2, expand=True),
                    # Balance
                    ft.Column([
                        ft.Text(
                            f"{currency_symbol}{balance:,.2f}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_400 if balance >= 0 else ft.Colors.RED_400
                        ),
                        ft.Text(
                            currency,
                            size=11,
                            color=ft.Colors.GREY_400
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2),
                ], spacing=12),
            ], spacing=0),
            padding=16,
            bgcolor="#2C2C2E",
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_700)
        )
    
    def handle_search(self, e):
        """Handle search input"""
        
        self.search_query = e.control.value.lower()
        
        if not self.search_query:
            self.filtered_accounts = self.accounts.copy()
        else:
            self.filtered_accounts = [
                acc for acc in self.accounts
                if self.search_query in acc[2].lower() or  # account name
                   self.search_query in (acc[7] or "").lower()  # username
            ]
        
        # Update account list
        self.account_list_column.controls = [
            self.create_account_card(acc) for acc in self.filtered_accounts
        ]
        
        if not self.filtered_accounts:
            self.account_list_column.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.SEARCH_OFF_ROUNDED,
                            size=60,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            "No accounts found",
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
