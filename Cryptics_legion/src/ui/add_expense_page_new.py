# src/ui/add_expense_page.py
import flet as ft
from datetime import datetime
from core import db


# Category options
CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Health",
    "Education",
    "Electronics",
    "Groceries",
    "Rent",
    "Travel",
    "Subscription",
    "Other",
]

# Payment methods
PAYMENT_METHODS = [
    "Physical Cash",
    "Credit Card",
    "Debit Card",
    "Bank Transfer",
    "E-Wallet",
    "Other",
]

# Currencies
CURRENCIES = [
    "Peso (₱)",
    "Dollar ($)",
    "Euro (€)",
    "Yen (¥)",
]


def create_add_expense_view(page: ft.Page, state: dict, toast, go_back):
    """Create the add expense page with modern glass design."""
    
    # State variables
    selected_category = {"value": "Electronics"}
    selected_payment = {"value": "Physical Cash"}
    selected_currency = {"value": "Peso (₱)"}
    amount_value = {"value": ""}
    
    # Current date/time
    now = datetime.now()
    current_time = now.strftime("%I:%M %p").lower()
    current_date = now.strftime("%b %d, %Y")
    
    def go_home(e):
        """Navigate back to home."""
        go_back()
    
    def save_expense(e):
        """Save the expense to database."""
        if not amount_value['value'] or amount_value['value'] == "":
            toast("Please enter an amount", "#b71c1c")
            return
        
        try:
            amount = float(amount_value['value'].replace(',', '').replace('₱', '').strip())
        except ValueError:
            toast("Invalid amount", "#b71c1c")
            return
        
        if amount <= 0:
            toast("Amount must be greater than 0", "#b71c1c")
            return
        
        # Save to database
        db.insert_expense(
            state["user_id"],
            amount,
            selected_category['value'],
            f"{selected_payment['value']}",
            datetime.now().strftime("%Y-%m-%d")
        )
        
        toast("Expense added successfully!", "#2E7D32")
        go_back()
    
    def show_view():
        page.clean()
        
        # Amount text field
        amount_field = ft.TextField(
            value=amount_value['value'],
            hint_text="0",
            hint_style=ft.TextStyle(color="#6666aa"),
            keyboard_type=ft.KeyboardType.NUMBER,
            border="none",
            bgcolor="transparent",
            color="white",
            text_size=18,
            content_padding=0,
            width=150,
            cursor_color="white",
            on_change=lambda e: amount_value.update({'value': e.control.value}),
        )
        
        # Category text display
        category_text = ft.Text(selected_category['value'], size=16, color="white")
        
        # Payment text display
        payment_text = ft.Text(selected_payment['value'], size=16, color="white")
        
        # Currency text display
        currency_text = ft.Text(selected_currency['value'], size=16, color="white")
        
        def show_category_picker(e):
            """Show category selection dialog."""
            def select_cat(cat):
                selected_category['value'] = cat
                category_text.value = cat
                page.close(dlg)
                page.update()
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select Category", color="white"),
                bgcolor="#1a1a3e",
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(cat, color="white"),
                            on_click=lambda e, c=cat: select_cat(c),
                        ) for cat in CATEGORIES
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=300,
                ),
            )
            page.open(dlg)
        
        def show_payment_picker(e):
            """Show payment method selection dialog."""
            def select_pay(pay):
                selected_payment['value'] = pay
                payment_text.value = pay
                page.close(dlg)
                page.update()
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select Payment Method", color="white"),
                bgcolor="#1a1a3e",
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(pay, color="white"),
                            on_click=lambda e, p=pay: select_pay(p),
                        ) for pay in PAYMENT_METHODS
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=250,
                ),
            )
            page.open(dlg)
        
        def show_currency_picker(e):
            """Show currency selection dialog."""
            def select_curr(curr):
                selected_currency['value'] = curr
                currency_text.value = curr
                page.close(dlg)
                page.update()
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select Currency", color="white"),
                bgcolor="#1a1a3e",
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(curr, color="white"),
                            on_click=lambda e, c=curr: select_curr(c),
                        ) for curr in CURRENCIES
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=200,
                ),
            )
            page.open(dlg)
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Add Expenses", size=26, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(
                        content=ft.CircleAvatar(
                            bgcolor="#4F46E5",
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                            radius=22,
                        ),
                        on_click=go_home,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=20),
        )
        
        # Transaction card (date/time)
        transaction_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("TRANSACTION", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Text(f"{current_time}  |  {current_date}", size=16, color="white"),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
        )
        
        # Category card
        category_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("CATEGORY", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            category_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#8888aa", size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
            on_click=show_category_picker,
            ink=True,
        )
        
        # Amount card
        amount_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("AMOUNT", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("₱", size=18, color="white", weight=ft.FontWeight.W_500),
                                    amount_field,
                                ],
                                spacing=4,
                            ),
                            ft.Icon(ft.Icons.EDIT, color="#8888aa", size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
        )
        
        # Currency card
        currency_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("CURRENCY", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            currency_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#8888aa", size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
            on_click=show_currency_picker,
            ink=True,
        )
        
        # Payment method card
        payment_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("PAYMENT METHOD", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            payment_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#8888aa", size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
            on_click=show_payment_picker,
            ink=True,
        )
        
        # Save button
        save_button = ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ADD, color="white"),
                    ft.Text("Add Expense", color="white", weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#6366F1",
            width=280,
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=save_expense,
        )
        
        # Bottom navigation bar
        bottom_nav = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.HOME_ROUNDED,
                        icon_color="#A855F7",
                        icon_size=28,
                        on_click=go_home,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.BAR_CHART_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=go_home,
                    ),
                    ft.Container(width=56),  # Space for FAB
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=go_home,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PERSON_ROUNDED,
                        icon_color="#6B7280",
                        icon_size=28,
                        on_click=go_home,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor="#0d0d1a",
            border_radius=ft.border_radius.only(top_left=24, top_right=24),
            padding=ft.padding.symmetric(vertical=12, horizontal=8),
        )
        
        # Scrollable content
        scroll_content = ft.Column(
            controls=[
                transaction_card,
                ft.Container(height=12),
                category_card,
                ft.Container(height=12),
                amount_card,
                ft.Container(height=12),
                currency_card,
                ft.Container(height=12),
                payment_card,
                ft.Container(height=24),
                ft.Container(
                    content=save_button,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=100),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
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
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    header,
                                    scroll_content,
                                ],
                                expand=True,
                            ),
                            padding=ft.padding.only(left=20, right=20, top=10),
                            expand=True,
                        ),
                        bottom_nav,
                    ],
                    spacing=0,
                    expand=True,
                ),
            )
        )
        
        page.update()
    
    return show_view
