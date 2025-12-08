# src/ui/add_expense_page.py
import flet as ft
from datetime import datetime
from core import db
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


def create_add_expense_view(page: ft.Page, state: dict, toast, go_back):
    """Create the add expense page with modern glass design."""
    
    # Get selected account to initialize currency
    selected_account = db.get_selected_account(state["user_id"])
    account_currency = selected_account[5] if selected_account else "PHP"
    
    # State variables
    selected_category = {"value": "Electronics"}
    selected_payment = {"value": "Physical Cash"}
    selected_currency = {"value": "Peso (₱)"}
    selected_currency_code = {"value": account_currency}
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
                if cat == "Other":
                    # Show custom category input dialog
                    page.close(dlg)
                    show_custom_category_dialog()
                else:
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
        
        def show_currency_picker_amount(e):
            """Show currency selection dialog for amount."""
            def select_curr_code(code, symbol, name):
                selected_currency_code['value'] = code
                currency_display_text.value = f"{symbol} {code}"
                page.close(dlg)
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
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Select Currency", color="white"),
                bgcolor="#1a1a3e",
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.Text(symbol, size=20, color="white", weight=ft.FontWeight.BOLD),
                            title=ft.Text(f"{code} - {name}", color="white"),
                            on_click=lambda e, c=code, s=symbol, n=name: select_curr_code(c, s, n),
                        ) for code, symbol, name in currencies
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=400,
                ),
            )
            page.open(dlg)
        
        # Currency display for amount card
        currency_symbol = get_currency_symbol(selected_currency_code["value"])
        currency_display_text = ft.Text(
            f"{currency_symbol} {selected_currency_code['value']}",
            size=16,
            color="white",
            weight=ft.FontWeight.W_500,
        )
        
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
                            amount_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor="#1a1a3e",
            border=ft.border.all(1, "#2d2d5a"),
        )
        
        # Currency card - for amount currency selection
        currency_selector_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("CURRENCY", size=11, color="#8888aa", weight=ft.FontWeight.W_500),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            currency_display_text,
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
            on_click=show_currency_picker_amount,
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
                currency_selector_card,
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
