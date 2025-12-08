"""
Admin All Expenses Page
View all expenses from all users in the system
"""

import flet as ft
from core import db
from utils.currency import get_currency_symbol


class AdminAllExpensesPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        self.expenses = []
        self.filtered_expenses = []
        self.search_query = ""
        
    def build(self):
        """Build all expenses page"""
        
        # Load all expenses
        self.expenses = db.get_all_expenses_for_admin()
        self.filtered_expenses = self.expenses.copy()
        
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
                    "All Expenses",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
            ]),
            bgcolor=ft.Colors.ORANGE_700,
            padding=16,
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Search and Filter Bar
        self.search_field = ft.TextField(
            hint_text="Search by description, category, or user...",
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
        total_expenses = len(self.expenses)
        total_amount = sum(float(exp[2]) if exp[2] else 0.0 for exp in self.expenses)  # amount
        
        summary = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.create_summary_chip(
                        f"{total_expenses} Total Expenses",
                        ft.Icons.RECEIPT_LONG_ROUNDED,
                        ft.Colors.ORANGE_400
                    ),
                    self.create_summary_chip(
                        f"₱{total_amount:,.2f} Total Amount",
                        ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        ft.Colors.GREEN_400
                    ),
                ], spacing=12, wrap=True),
                ft.Text(
                    "Note: Amounts shown in mixed currencies",
                    size=10,
                    color=ft.Colors.GREY_500,
                    italic=True
                )
            ], spacing=4),
            padding=ft.padding.symmetric(horizontal=20, vertical=0)
        )
        
        # Expense list
        self.expense_list_column = ft.Column(
            [self.create_expense_card(exp) for exp in self.filtered_expenses],
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )
        
        expense_list = ft.Container(
            content=self.expense_list_column,
            padding=ft.padding.only(left=20, right=20, top=12, bottom=20),
            expand=True
        )
        
        # Main content
        return ft.Column([
            header,
            search_bar,
            summary,
            expense_list,
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
    
    def create_expense_card(self, expense: tuple):
        """Create an expense card"""
        
        # expense: (id, user_id, amount, category, description, date, account_id, username, currency)
        expense_id = expense[0]
        user_id = expense[1]
        amount = float(expense[2])
        category = expense[3]
        description = expense[4]
        date = expense[5]
        account_id = expense[6]
        username = expense[7] if len(expense) > 7 else "Unknown"
        currency = expense[8] if len(expense) > 8 else "PHP"
        
        # Get currency symbol
        currency_symbol = get_currency_symbol(currency)
        
        # Format date
        from datetime import datetime
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            date_str = dt.strftime("%b %d, %Y")
        except:
            date_str = date
        
        # Category icon mapping
        category_icons = {
            "Food": ft.Icons.RESTAURANT_ROUNDED,
            "Transport": ft.Icons.DIRECTIONS_CAR_ROUNDED,
            "Shopping": ft.Icons.SHOPPING_BAG_ROUNDED,
            "Entertainment": ft.Icons.MOVIE_ROUNDED,
            "Bills": ft.Icons.RECEIPT_ROUNDED,
            "Health": ft.Icons.MEDICAL_SERVICES_ROUNDED,
            "Education": ft.Icons.SCHOOL_ROUNDED,
            "Others": ft.Icons.MORE_HORIZ_ROUNDED,
        }
        category_icon = category_icons.get(category, ft.Icons.ATTACH_MONEY_ROUNDED)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    # Category Icon
                    ft.Container(
                        content=ft.Icon(category_icon, size=24, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE_700,
                        border_radius=25,
                        width=50,
                        height=50,
                        alignment=ft.alignment.center
                    ),
                    # Expense Info
                    ft.Column([
                        ft.Text(
                            description or "No description",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Row([
                            ft.Icon(ft.Icons.CATEGORY_ROUNDED, size=12, color=ft.Colors.GREY_400),
                            ft.Text(category, size=12, color=ft.Colors.GREY_400),
                            ft.Text("•", size=12, color=ft.Colors.GREY_400),
                            ft.Icon(ft.Icons.PERSON_ROUNDED, size=12, color=ft.Colors.GREY_400),
                            ft.Text(username, size=12, color=ft.Colors.GREY_400),
                        ], spacing=4),
                    ], spacing=2, expand=True),
                    # Amount and Date
                    ft.Column([
                        ft.Text(
                            f"{currency_symbol}{amount:,.2f}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_400
                        ),
                        ft.Text(
                            date_str,
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
            self.filtered_expenses = self.expenses.copy()
        else:
            self.filtered_expenses = [
                exp for exp in self.expenses
                if self.search_query in (exp[4] or "").lower() or  # description
                   self.search_query in exp[3].lower() or  # category
                   self.search_query in (exp[8] or "").lower()  # username
            ]
        
        # Update expense list
        self.expense_list_column.controls = [
            self.create_expense_card(exp) for exp in self.filtered_expenses
        ]
        
        if not self.filtered_expenses:
            self.expense_list_column.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.SEARCH_OFF_ROUNDED,
                            size=60,
                            color=ft.Colors.GREY_400
                        ),
                        ft.Text(
                            "No expenses found",
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
