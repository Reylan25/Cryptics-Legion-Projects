# src/ui/add_expense_page.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
from utils.brand_recognition import identify_brand, get_brand_suggestions
from utils.currency import get_currency_symbol


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


def create_add_expense_view(page: ft.Page, state: dict, toast, go_back,
                            show_home=None, show_expenses=None, show_wallet=None, show_profile=None):
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
    
    def nav_back(e=None):
        """Navigate back - defaults to expenses page."""
        if show_expenses:
            show_expenses()
        elif go_back:
            go_back()
    
    def nav_home():
        """Navigate to home."""
        if show_home:
            show_home()
        elif go_back:
            go_back()
    
    def nav_expenses():
        """Navigate to expenses."""
        if show_expenses:
            show_expenses()
    
    def nav_wallet():
        """Navigate to wallet."""
        if show_wallet:
            show_wallet()
    
    def nav_profile():
        """Navigate to profile."""
        if show_profile:
            show_profile()
    
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
        
        # Get the selected account (to deduct balance from)
        selected_account = db.get_selected_account(state["user_id"])
        account_id = selected_account[0] if selected_account else None
        account_name = selected_account[1] if selected_account else "Unknown"
        account_currency = selected_account[5] if selected_account else "PHP"
        currency_symbol = get_currency_symbol(account_currency)
        
        # Check if account has enough balance
        if selected_account:
            account_balance = selected_account[4]  # balance column
            if amount > account_balance:
                toast(f"Insufficient balance in {account_name} ({currency_symbol}{account_balance:,.2f})", "#b71c1c")
                return
        
        # Get the proper category and description
        # If brand was detected, use the detected_category, otherwise use the selected value as category
        expense_category = selected_category.get('detected_category', selected_category['value'])
        # Use the display name (brand name or custom category) as description
        expense_description = selected_category['value']
        
        # Save to database with account_id - this will also deduct from account balance
        db.insert_expense(
            state["user_id"],
            amount,
            expense_category,
            expense_description,
            datetime.now().strftime("%Y-%m-%d"),
            account_id
        )
        
        toast(f"Expense added! Deducted {currency_symbol}{amount:,.2f} from {account_name}", "#2E7D32")
        nav_back()
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Amount text field
        amount_field = ft.TextField(
            value=amount_value['value'],
            hint_text="0",
            hint_style=ft.TextStyle(color=theme.text_muted),
            keyboard_type=ft.KeyboardType.NUMBER,
            border="none",
            bgcolor="transparent",
            color=theme.text_primary,
            text_size=18,
            content_padding=0,
            width=150,
            cursor_color=theme.text_primary,
            on_change=lambda e: amount_value.update({'value': e.control.value}),
        )
        
        # Category text display
        category_text = ft.Text(selected_category['value'], size=16, color=theme.text_primary)
        
        # Payment text display
        payment_text = ft.Text(selected_payment['value'], size=16, color=theme.text_primary)
        
        # Currency text display
        currency_text = ft.Text(selected_currency['value'], size=16, color=theme.text_primary)
        
        def show_category_picker(e):
            """Show category selection dialog."""
            def select_cat(cat):
                if cat == "Other":
                    # Show custom category input dialog
                    page.close(dlg)
                    show_custom_category_dialog()
                else:
                    selected_category['value'] = cat
                    # Clear any previous brand detection data
                    selected_category.pop('detected_category', None)
                    selected_category.pop('icon', None)
                    selected_category.pop('color', None)
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
        
        def show_custom_category_dialog():
            """Show dialog to input custom category with AI brand recognition."""
            # Preview state
            preview_state = {"icon": ft.Icons.CATEGORY, "color": "#7C3AED", "category": "", "is_brand": False}
            
            # Preview icon container
            preview_icon = ft.Container(
                content=ft.Icon(ft.Icons.CATEGORY, color="white", size=28),
                width=56,
                height=56,
                border_radius=28,
                bgcolor="#7C3AED",
                alignment=ft.alignment.center,
            )
            
            # Preview category text
            preview_text = ft.Text("Type a brand or category...", size=14, color="#aaaacc", italic=True)
            
            # AI detection badge
            ai_badge = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.AUTO_AWESOME, color="#FFD700", size=14),
                        ft.Text("AI Detected", size=11, color="#FFD700", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=4,
                ),
                visible=False,
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=12,
                bgcolor="#2d2d5a",
            )
            
            # Suggestions container
            suggestions_column = ft.Column(controls=[], spacing=4, visible=False)
            
            def update_preview(e):
                """Update preview based on input - AI brand recognition."""
                input_value = e.control.value.strip() if e.control.value else ""
                
                if input_value:
                    # Use AI brand recognition
                    result = identify_brand(input_value)
                    preview_state["icon"] = result["icon"]
                    preview_state["color"] = result["color"]
                    preview_state["category"] = result["category"]
                    preview_state["is_brand"] = result["is_brand"]
                    preview_state["display_name"] = result["display_name"]
                    
                    # Update preview icon
                    preview_icon.content = ft.Icon(result["icon"], color="white", size=28)
                    preview_icon.bgcolor = result["color"]
                    
                    # Update preview text
                    if result["is_brand"]:
                        preview_text.value = f"✓ {result['display_name']} → {result['category']}"
                        preview_text.color = "#4ADE80"
                        preview_text.italic = False
                        ai_badge.visible = True
                    else:
                        preview_text.value = f"Category: {result['display_name']}"
                        preview_text.color = "#aaaacc"
                        preview_text.italic = False
                        ai_badge.visible = False
                    
                    # Show suggestions
                    suggestions = get_brand_suggestions(input_value, limit=4)
                    if suggestions and len(input_value) >= 2:
                        suggestions_column.controls.clear()
                        for suggestion in suggestions:
                            if suggestion.lower() != input_value.lower():
                                sug_result = identify_brand(suggestion)
                                suggestions_column.controls.append(
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Container(
                                                    content=ft.Icon(sug_result["icon"], color="white", size=16),
                                                    width=28,
                                                    height=28,
                                                    border_radius=14,
                                                    bgcolor=sug_result["color"],
                                                    alignment=ft.alignment.center,
                                                ),
                                                ft.Text(suggestion, color="white", size=13),
                                            ],
                                            spacing=10,
                                        ),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                        border_radius=8,
                                        bgcolor="#1a1a3e",
                                        on_click=lambda e, s=suggestion: select_suggestion(s),
                                        ink=True,
                                    )
                                )
                        suggestions_column.visible = len(suggestions_column.controls) > 0
                    else:
                        suggestions_column.visible = False
                else:
                    preview_icon.content = ft.Icon(ft.Icons.CATEGORY, color="white", size=28)
                    preview_icon.bgcolor = "#7C3AED"
                    preview_text.value = "Type a brand or category..."
                    preview_text.color = "#aaaacc"
                    preview_text.italic = True
                    ai_badge.visible = False
                    suggestions_column.visible = False
                
                page.update()
            
            def select_suggestion(suggestion):
                """Select a brand suggestion."""
                custom_category_field.value = suggestion
                update_preview(type('obj', (object,), {'control': custom_category_field})())
                page.update()
            
            custom_category_field = ft.TextField(
                hint_text="e.g., Nike, Starbucks, Grab...",
                hint_style=ft.TextStyle(color="#6666aa"),
                border_color="#4F46E5",
                focused_border_color="#7C3AED",
                bgcolor="#0d1829",
                color="white",
                text_size=16,
                cursor_color="white",
                content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
                on_change=update_preview,
            )
            
            def save_custom_category(e):
                custom_value = custom_category_field.value.strip() if custom_category_field.value else ""
                if custom_value:
                    # Use the recognized brand/category info
                    result = identify_brand(custom_value)
                    # Store both the display name and category info
                    selected_category['value'] = result["display_name"]
                    selected_category['icon'] = result["icon"]
                    selected_category['color'] = result["color"]
                    selected_category['detected_category'] = result["category"]
                    category_text.value = result["display_name"]
                    page.close(custom_dlg)
                    
                    # Show success message for brand detection
                    if result["is_brand"]:
                        toast(f"✓ {result['display_name']} recognized as {result['category']}", "#4F46E5")
                    
                    page.update()
                else:
                    toast("Please enter a category name", "#b71c1c")
            
            def cancel_custom(e):
                page.close(custom_dlg)
                page.update()
            
            custom_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.AUTO_AWESOME, color="#FFD700", size=20),
                        ft.Text("Smart Category", color="white", weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                ),
                bgcolor="#1a1a3e",
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Enter brand, store, or category:", color="#aaaacc", size=14),
                            custom_category_field,
                            # Preview section
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        preview_icon,
                                        ft.Column(
                                            controls=[
                                                ft.Row(
                                                    controls=[preview_text, ai_badge],
                                                    spacing=8,
                                                ),
                                            ],
                                            spacing=2,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=12,
                                ),
                                padding=ft.padding.all(12),
                                border_radius=12,
                                bgcolor="#0d1829",
                                margin=ft.margin.only(top=10),
                            ),
                            # Suggestions
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Suggestions:", size=12, color="#6666aa"),
                                        suggestions_column,
                                    ],
                                    spacing=6,
                                ),
                                visible=True,
                                margin=ft.margin.only(top=8),
                            ),
                        ],
                        spacing=12,
                        tight=True,
                    ),
                    width=300,
                    padding=ft.padding.only(top=10),
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=cancel_custom, style=ft.ButtonStyle(color="#aaaacc")),
                    ft.ElevatedButton(
                        "Save",
                        on_click=save_custom_category,
                        bgcolor="#4F46E5",
                        color="white",
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(custom_dlg)
        
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
                    ft.Text("Add Expenses", size=26, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=ft.CircleAvatar(
                            bgcolor=theme.accent_primary,
                            content=ft.Icon(ft.Icons.PERSON, color="white"),
                            radius=22,
                        ),
                        on_click=lambda e: nav_profile(),
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
                    ft.Text("TRANSACTION", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Text(f"{current_time}  |  {current_date}", size=16, color=theme.text_primary),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Get selected account for display
        selected_account = db.get_selected_account(state["user_id"])
        account_name = selected_account[1] if selected_account else "No Account"
        account_balance = selected_account[4] if selected_account else 0
        account_currency = selected_account[5] if selected_account else "PHP"
        account_color = selected_account[6] if selected_account else "#3B82F6"
        account_type = selected_account[3] if selected_account else "Cash"
        
        # State for selected currency (initialize with account's currency)
        selected_currency_code = {"value": account_currency}
        currency_symbol = get_currency_symbol(selected_currency_code["value"])
        
        def update_currency_display(e):
            """Update currency symbol when dropdown changes"""
            selected_currency_code["value"] = e.control.value
            currency_symbol_text.value = get_currency_symbol(e.control.value)
            page.update()
        
        # Currency symbol text (will be updated dynamically)
        currency_symbol_text = ft.Text(currency_symbol, size=18, color=theme.text_primary, weight=ft.FontWeight.W_500)
        
        # Currency dropdown
        currency_dropdown = ft.Dropdown(
            value=account_currency,
            options=[
                ft.dropdown.Option(key="PHP", text="₱ PHP"),
                ft.dropdown.Option(key="USD", text="$ USD"),
                ft.dropdown.Option(key="EUR", text="€ EUR"),
                ft.dropdown.Option(key="JPY", text="¥ JPY"),
                ft.dropdown.Option(key="GBP", text="£ GBP"),
                ft.dropdown.Option(key="KRW", text="₩ KRW"),
                ft.dropdown.Option(key="SGD", text="S$ SGD"),
                ft.dropdown.Option(key="AUD", text="A$ AUD"),
                ft.dropdown.Option(key="CAD", text="C$ CAD"),
                ft.dropdown.Option(key="INR", text="₹ INR"),
            ],
            on_change=update_currency_display,
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor="transparent",
            color=theme.text_primary,
            text_size=14,
            height=40,
            content_padding=ft.padding.only(left=8, right=4),
            border_radius=8,
        )
        
        # Account card - shows which account will be charged
        account_card = ft.Container(
            content=ft.Row(
                controls=[
                    # Account icon
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=20),
                        width=40,
                        height=40,
                        border_radius=10,
                        bgcolor=account_color,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(width=12),
                    # Account info
                    ft.Column(
                        controls=[
                            ft.Text("DEDUCT FROM", size=10, color=theme.text_muted, weight=ft.FontWeight.W_500),
                            ft.Text(account_name, size=15, color=theme.text_primary, weight=ft.FontWeight.W_600),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    # Balance
                    ft.Column(
                        controls=[
                            ft.Text("Balance", size=10, color=theme.text_muted),
                            ft.Text(f"{currency_symbol}{account_balance:,.2f}", size=14, color="#10B981", weight=ft.FontWeight.W_600),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=14,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, account_color + "50"),
        )
        
        # Category card
        category_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("CATEGORY", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            category_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.text_muted, size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
            on_click=show_category_picker,
            ink=True,
        )
        
        # Amount card
        amount_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("AMOUNT", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    currency_dropdown,
                                    amount_field,
                                ],
                                spacing=8,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Currency card
        currency_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("CURRENCY", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            currency_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.text_muted, size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
            on_click=show_currency_picker,
            ink=True,
        )
        
        # Payment method card
        payment_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("PAYMENT METHOD", size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            payment_text,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.text_muted, size=24),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
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
            bgcolor=theme.accent_primary,
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
                        icon_color=theme.text_muted,
                        icon_size=28,
                        on_click=lambda e: nav_home(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ANALYTICS_ROUNDED,
                        icon_color=theme.text_muted,
                        icon_size=28,
                        on_click=lambda e: nav_expenses(),
                    ),
                    ft.Container(width=56),  # Space for FAB
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED,
                        icon_color=theme.text_muted,
                        icon_size=28,
                        on_click=lambda e: nav_wallet(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PERSON_ROUNDED,
                        icon_color=theme.text_muted,
                        icon_size=28,
                        on_click=lambda e: nav_profile(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=theme.nav_bg,
            border_radius=ft.border_radius.only(top_left=24, top_right=24),
            padding=ft.padding.symmetric(vertical=12, horizontal=8),
        )
        
        # Scrollable content
        scroll_content = ft.Column(
            controls=[
                account_card,
                ft.Container(height=12),
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
                    colors=[theme.bg_gradient_start, theme.bg_primary],
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


# ============ NEW: Content builder for flash-free navigation ============
def build_add_expense_content(page: ft.Page, state: dict, toast, go_back,
                               show_home, show_expenses, show_wallet, show_profile):
    """
    Builds and returns add expense page content with AI category suggestions,
    date/time picker, and account selection for deduction.
    """
    theme = get_theme()
    
    # State
    now = datetime.now()
    expense_state = {
        "category": "Other",
        "detected_category": None,
        "category_icon": ft.Icons.CATEGORY,
        "category_color": "#7C3AED",
        "is_ai_detected": False,
        "selected_date": now,
        "selected_time": now,
        "selected_account_id": None,
        "selected_currency_code": "PHP",
    }
    
    # Get user accounts
    user_accounts = db.get_accounts_by_user(state["user_id"])
    selected_account = db.get_selected_account(state["user_id"])
    if selected_account:
        expense_state["selected_account_id"] = selected_account[0]
        expense_state["selected_currency_code"] = selected_account[5] if len(selected_account) > 5 else "PHP"
    elif user_accounts:
        expense_state["selected_account_id"] = user_accounts[0][0]
        expense_state["selected_currency_code"] = user_accounts[0][5] if len(user_accounts[0]) > 5 else "PHP"
    
    # ============ UI Components ============
    
    # Amount field
    amount_field = ft.TextField(
        hint_text="0.00",
        hint_style=ft.TextStyle(color=theme.text_muted, size=28),
        border=ft.InputBorder.NONE,
        bgcolor="transparent",
        color=theme.text_primary,
        text_size=28,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        content_padding=0,
        expand=True,
    )
    
    # Description field with AI detection
    description_field = ft.TextField(
        hint_text="What did you spend on?",
        hint_style=ft.TextStyle(color=theme.text_muted),
        border=ft.InputBorder.NONE,
        bgcolor="transparent",
        color=theme.text_primary,
        text_size=15,
        expand=True,
    )
    
    # AI suggestion badge
    ai_badge = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.AUTO_AWESOME, color="#FFD700", size=12),
            ft.Text("AI", size=9, color="#FFD700", weight=ft.FontWeight.BOLD),
        ], spacing=3),
        visible=False,
        padding=ft.padding.symmetric(horizontal=6, vertical=3),
        border_radius=8,
        bgcolor=f"{theme.accent_primary}30",
    )
    
    # Category display
    category_icon_container = ft.Container(
        content=ft.Icon(ft.Icons.CATEGORY, color="white", size=18),
        width=36,
        height=36,
        border_radius=10,
        bgcolor="#7C3AED",
        alignment=ft.alignment.center,
    )
    
    category_text = ft.Text("Select category", size=13, color=theme.text_primary)
    category_subtext = ft.Text("Tap to choose", size=10, color=theme.text_muted)
    
    # Date & Time displays
    date_text = ft.Text(now.strftime("%b %d"), size=12, color=theme.text_primary)
    time_text = ft.Text(now.strftime("%I:%M %p"), size=12, color=theme.text_primary)
    
    # Account display
    def get_account_info(account_id):
        for acc in user_accounts:
            if acc[0] == account_id:
                return acc
        return None
    
    current_acc = get_account_info(expense_state["selected_account_id"])
    current_acc_currency = current_acc[5] if current_acc else "PHP"
    current_acc_symbol = get_currency_symbol(current_acc_currency)
    account_name_text = ft.Text(
        current_acc[1] if current_acc else "Select",
        size=13,
        color=theme.text_primary,
    )
    account_balance_text = ft.Text(
        f"{current_acc_symbol}{current_acc[4]:,.0f}" if current_acc else "",
        size=10,
        color=theme.text_muted,
    )
    account_icon_container = ft.Container(
        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=16),
        width=32,
        height=32,
        border_radius=8,
        bgcolor=current_acc[6] if current_acc else theme.accent_primary,
        alignment=ft.alignment.center,
    )
    
    # Currency display
    currency_symbol_display = get_currency_symbol(expense_state["selected_currency_code"])
    currency_display_text = ft.Text(
        f"{currency_symbol_display} {expense_state['selected_currency_code']}",
        size=13,
        color=theme.text_primary,
    )
    
    # ============ AI Category Detection ============
    def on_description_change(e):
        input_text = e.control.value.strip() if e.control.value else ""
        
        if len(input_text) >= 2:
            result = identify_brand(input_text)
            expense_state["category"] = result["category"]
            expense_state["detected_category"] = result["category"]
            expense_state["category_icon"] = result["icon"]
            expense_state["category_color"] = result["color"]
            expense_state["is_ai_detected"] = result["is_brand"]
            
            category_icon_container.content = ft.Icon(result["icon"], color="white", size=18)
            category_icon_container.bgcolor = result["color"]
            
            if result["is_brand"]:
                category_text.value = result["display_name"]
                category_subtext.value = f"→ {result['category']}"
                ai_badge.visible = True
            else:
                category_text.value = result["category"]
                category_subtext.value = "AI suggested"
                ai_badge.visible = True
            
            page.update()
        else:
            ai_badge.visible = False
            category_text.value = expense_state["category"]
            category_subtext.value = "Tap to choose"
            page.update()
    
    description_field.on_change = on_description_change
    
    # ============ Category Picker ============
    def show_category_picker(e):
        def select_cat(cat):
            expense_state["category"] = cat
            expense_state["is_ai_detected"] = False
            
            cat_icons = {
                "Food & Dining": (ft.Icons.RESTAURANT, "#FF6B35"),
                "Transport": (ft.Icons.DIRECTIONS_CAR, "#3B82F6"),
                "Shopping": (ft.Icons.SHOPPING_BAG, "#EC4899"),
                "Entertainment": (ft.Icons.MOVIE, "#8B5CF6"),
                "Bills & Utilities": (ft.Icons.RECEIPT_LONG, "#F59E0B"),
                "Health": (ft.Icons.MEDICAL_SERVICES, "#10B981"),
                "Education": (ft.Icons.SCHOOL, "#6366F1"),
                "Electronics": (ft.Icons.DEVICES, "#06B6D4"),
                "Groceries": (ft.Icons.LOCAL_GROCERY_STORE, "#84CC16"),
                "Rent": (ft.Icons.HOME, "#EF4444"),
                "Travel": (ft.Icons.FLIGHT, "#14B8A6"),
                "Subscription": (ft.Icons.SUBSCRIPTIONS, "#F43F5E"),
                "Other": (ft.Icons.CATEGORY, "#7C3AED"),
            }
            icon, color = cat_icons.get(cat, (ft.Icons.CATEGORY, "#7C3AED"))
            expense_state["category_icon"] = icon
            expense_state["category_color"] = color
            
            category_icon_container.content = ft.Icon(icon, color="white", size=18)
            category_icon_container.bgcolor = color
            category_text.value = cat
            category_subtext.value = "Selected"
            ai_badge.visible = False
            
            page.close(sheet)
            page.update()
        
        cat_items = [
            ("Food & Dining", ft.Icons.RESTAURANT, "#FF6B35"),
            ("Transport", ft.Icons.DIRECTIONS_CAR, "#3B82F6"),
            ("Shopping", ft.Icons.SHOPPING_BAG, "#EC4899"),
            ("Entertainment", ft.Icons.MOVIE, "#8B5CF6"),
            ("Bills & Utilities", ft.Icons.RECEIPT_LONG, "#F59E0B"),
            ("Health", ft.Icons.MEDICAL_SERVICES, "#10B981"),
            ("Education", ft.Icons.SCHOOL, "#6366F1"),
            ("Electronics", ft.Icons.DEVICES, "#06B6D4"),
            ("Groceries", ft.Icons.LOCAL_GROCERY_STORE, "#84CC16"),
            ("Rent", ft.Icons.HOME, "#EF4444"),
            ("Travel", ft.Icons.FLIGHT, "#14B8A6"),
            ("Subscription", ft.Icons.SUBSCRIPTIONS, "#F43F5E"),
            ("Other", ft.Icons.CATEGORY, "#7C3AED"),
        ]
        
        sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=12),
                    ),
                    ft.Text("Select Category", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(height=12),
                    ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(icon, color="white", size=16),
                                    width=32, height=32, border_radius=8,
                                    bgcolor=color, alignment=ft.alignment.center,
                                ),
                                ft.Container(width=10),
                                ft.Text(cat, size=14, color=theme.text_primary, expand=True),
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.accent_primary, size=18)
                                if cat == expense_state["category"] else ft.Container(),
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=f"{theme.accent_primary}15" if cat == expense_state["category"] else "transparent",
                            on_click=lambda e, c=cat: select_cat(c),
                            ink=True,
                        ) for cat, icon, color in cat_items
                    ], scroll=ft.ScrollMode.AUTO, spacing=4),
                    ft.Container(height=20),
                ]),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=16),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
            ),
            bgcolor=theme.bg_secondary,
        )
        page.open(sheet)
    
    # ============ Date Picker ============
    def show_date_picker(e):
        def on_change(e):
            if e.control.value:
                expense_state["selected_date"] = e.control.value
                date_text.value = e.control.value.strftime("%b %d")
                page.update()
        
        picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
            value=expense_state["selected_date"],
            on_change=on_change,
        )
        page.open(picker)
    
    # ============ Time Picker ============
    def show_time_picker(e):
        def on_change(e):
            if e.control.value:
                expense_state["selected_time"] = datetime.combine(
                    expense_state["selected_date"].date(), e.control.value
                )
                time_text.value = e.control.value.strftime("%I:%M %p")
                page.update()
        
        picker = ft.TimePicker(
            value=expense_state["selected_time"].time(),
            on_change=on_change,
        )
        page.open(picker)
    
    # ============ Account Picker ============
    def show_account_picker(e):
        def select_acc(acc):
            expense_state["selected_account_id"] = acc[0]
            account_name_text.value = acc[1]
            acc_currency = acc[5] if len(acc) > 5 else "PHP"
            acc_symbol = get_currency_symbol(acc_currency)
            account_balance_text.value = f"{acc_symbol}{acc[4]:,.0f}"
            account_icon_container.bgcolor = acc[6] or theme.accent_primary
            page.close(sheet)
            page.update()
        
        sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=12),
                    ),
                    ft.Text("Deduct From", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Text("Select account", size=12, color=theme.text_muted),
                    ft.Container(height=12),
                    ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=16),
                                    width=36, height=36, border_radius=10,
                                    bgcolor=acc[6] or theme.accent_primary,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(width=10),
                                ft.Column([
                                    ft.Text(acc[1], size=13, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                    ft.Text(f"{get_currency_symbol(acc[5])}{acc[4]:,.2f} • {acc[3]}", size=11, color=theme.text_muted),
                                ], spacing=2, expand=True),
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.accent_primary, size=18)
                                if acc[0] == expense_state["selected_account_id"] else ft.Container(),
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=f"{theme.accent_primary}15" if acc[0] == expense_state["selected_account_id"] else "transparent",
                            on_click=lambda e, a=acc: select_acc(a),
                            ink=True,
                        ) for acc in user_accounts
                    ], scroll=ft.ScrollMode.AUTO, spacing=6),
                    ft.Container(height=20),
                ]),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=16),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
            ),
            bgcolor=theme.bg_secondary,
        )
        page.open(sheet)
    
    # ============ Currency Picker ============
    def show_currency_picker(e):
        def select_currency(code, symbol, name):
            expense_state["selected_currency_code"] = code
            currency_display_text.value = f"{symbol} {code}"
            page.close(sheet)
            page.update()
        
        currencies = [
            ("PHP", "₱", "Philippine Peso"),
            ("USD", "$", "US Dollar"),
            ("EUR", "€", "Euro"),
            ("JPY", "¥", "Japanese Yen"),
            ("GBP", "£", "British Pound"),
            ("KRW", "₩", "South Korean Won"),
            ("SGD", "S$", "Singapore Dollar"),
            ("AUD", "A$", "Australian Dollar"),
            ("CAD", "C$", "Canadian Dollar"),
            ("INR", "₹", "Indian Rupee"),
        ]
        
        sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=12),
                    ),
                    ft.Text("Select Currency", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(height=12),
                    ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Text(symbol, size=16, color="white", weight=ft.FontWeight.BOLD),
                                    width=36, height=36, border_radius=10,
                                    bgcolor=theme.accent_primary, alignment=ft.alignment.center,
                                ),
                                ft.Container(width=10),
                                ft.Column([
                                    ft.Text(name, size=13, color=theme.text_primary),
                                    ft.Text(code, size=11, color=theme.text_muted),
                                ], spacing=1, expand=True),
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.accent_primary, size=18)
                                if code == expense_state["selected_currency_code"] else ft.Container(),
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=f"{theme.accent_primary}15" if code == expense_state["selected_currency_code"] else "transparent",
                            on_click=lambda e, c=code, s=symbol, n=name: select_currency(c, s, n),
                            ink=True,
                        ) for code, symbol, name in currencies
                    ], scroll=ft.ScrollMode.AUTO, spacing=4),
                    ft.Container(height=20),
                ]),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=16),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
            ),
            bgcolor=theme.bg_secondary,
        )
        page.open(sheet)
    
    # ============ Save Expense ============
    def save_expense(e):
        try:
            amount = float(amount_field.value.strip().replace(",", "")) if amount_field.value else 0
        except ValueError:
            toast("Please enter a valid amount", "#EF4444")
            return
        
        if amount <= 0:
            toast("Amount must be greater than 0", "#EF4444")
            return
        
        description = description_field.value.strip() if description_field.value else ""
        if not description:
            description = expense_state["category"]
        
        if not expense_state["selected_account_id"]:
            toast("Please select an account", "#EF4444")
            return
        
        acc_info = get_account_info(expense_state["selected_account_id"])
        if acc_info and amount > acc_info[4]:
            toast(f"Insufficient balance in {acc_info[1]}", "#EF4444")
            return
        
        expense_datetime = datetime.combine(
            expense_state["selected_date"].date(),
            expense_state["selected_time"].time()
        )
        date_str = expense_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        category = expense_state.get("detected_category") or expense_state["category"]
        
        db.insert_expense(
            user_id=state["user_id"],
            amount=amount,
            category=category,
            description=description,
            date_str=date_str,
            account_id=expense_state["selected_account_id"],
        )
        
        acc_name = acc_info[1] if acc_info else "account"
        acc_currency = acc_info[5] if acc_info else "PHP"
        acc_symbol = get_currency_symbol(acc_currency)
        toast(f"{acc_symbol}{amount:,.2f} deducted from {acc_name}", "#10B981")
        
        if show_expenses:
            show_expenses()
    
    # ============ Build UI ============
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=theme.text_primary,
                icon_size=20,
                on_click=lambda e: show_expenses() if show_expenses else None,
            ),
            ft.Text("Add Expense", size=18, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.Container(width=40),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=8),
    )
    
    # Amount Card
    amount_card = ft.Container(
        content=ft.Column([
            ft.Text("AMOUNT", size=10, color=theme.text_muted, weight=ft.FontWeight.W_600),
            ft.Container(height=6),
            ft.Row([
                ft.Text(current_acc_symbol, size=28, color=theme.accent_primary, weight=ft.FontWeight.BOLD),
                amount_field,
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=theme.bg_card,
        border_radius=16,
        padding=20,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Description Card with AI
    description_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("DESCRIPTION", size=10, color=theme.text_muted, weight=ft.FontWeight.W_600),
                ai_badge,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT_NOTE, color=theme.text_muted, size=20),
                    ft.Container(width=8),
                    description_field,
                ]),
                bgcolor=theme.bg_field,
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
            ),
        ]),
        bgcolor=theme.bg_card,
        border_radius=16,
        padding=16,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Category Card
    category_card = ft.Container(
        content=ft.Row([
            category_icon_container,
            ft.Container(width=12),
            ft.Column([
                category_text,
                category_subtext,
            ], spacing=1, expand=True),
            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
        ]),
        bgcolor=theme.bg_card,
        border_radius=14,
        padding=14,
        border=ft.border.all(1, theme.border_primary),
        on_click=show_category_picker,
        ink=True,
    )
    
    # Date & Time Row
    date_time_row = ft.Row([
        # Date Card
        ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CALENDAR_TODAY, color="white", size=14),
                    width=28, height=28, border_radius=7,
                    bgcolor="#3B82F6", alignment=ft.alignment.center,
                ),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Date", size=9, color=theme.text_muted),
                    date_text,
                ], spacing=1, expand=True),
            ]),
            bgcolor=theme.bg_card,
            border_radius=12,
            padding=10,
            border=ft.border.all(1, theme.border_primary),
            expand=True,
            on_click=show_date_picker,
            ink=True,
        ),
        ft.Container(width=8),
        # Time Card
        ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ACCESS_TIME, color="white", size=14),
                    width=28, height=28, border_radius=7,
                    bgcolor="#8B5CF6", alignment=ft.alignment.center,
                ),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Time", size=9, color=theme.text_muted),
                    time_text,
                ], spacing=1, expand=True),
            ]),
            bgcolor=theme.bg_card,
            border_radius=12,
            padding=10,
            border=ft.border.all(1, theme.border_primary),
            expand=True,
            on_click=show_time_picker,
            ink=True,
        ),
    ])
    
    # Account Card
    account_card = ft.Container(
        content=ft.Column([
            ft.Text("DEDUCT FROM", size=10, color=theme.text_muted, weight=ft.FontWeight.W_600),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row([
                    account_icon_container,
                    ft.Container(width=10),
                    ft.Column([
                        account_name_text,
                        account_balance_text,
                    ], spacing=1, expand=True),
                    ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.text_muted, size=22),
                ]),
                bgcolor=theme.bg_field,
                border_radius=12,
                padding=10,
                on_click=show_account_picker,
                ink=True,
            ),
        ]),
        bgcolor=theme.bg_card,
        border_radius=16,
        padding=16,
        border=ft.border.all(1, theme.border_primary),
    )
    
    # Currency Selector Card
    currency_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ATTACH_MONEY, color="white", size=16),
                width=32,
                height=32,
                border_radius=8,
                bgcolor=theme.accent_primary,
                alignment=ft.alignment.center,
            ),
            ft.Container(width=10),
            ft.Column([
                ft.Text("Currency", size=10, color=theme.text_muted),
                currency_display_text,
            ], spacing=1, expand=True),
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.text_muted, size=22),
        ]),
        bgcolor=theme.bg_card,
        border_radius=14,
        padding=14,
        border=ft.border.all(1, theme.border_primary),
        on_click=show_currency_picker,
        ink=True,
    )
    
    # Save Button
    save_button = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color="white", size=20),
            ft.Container(width=8),
            ft.Text("Save Expense", size=15, weight=ft.FontWeight.W_600, color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=theme.accent_primary,
        border_radius=14,
        padding=ft.padding.symmetric(vertical=14),
        on_click=save_expense,
        ink=True,
    )
    
    # Main content
    scrollable = ft.Column([
        amount_card,
        ft.Container(height=10),
        description_card,
        ft.Container(height=10),
        category_card,
        ft.Container(height=10),
        currency_card,
        ft.Container(height=10),
        date_time_row,
        ft.Container(height=10),
        account_card,
        ft.Container(height=20),
        save_button,
        ft.Container(height=80),
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=16, right=16, top=10),
        content=ft.Column([header, scrollable], expand=True, spacing=0),
    )
