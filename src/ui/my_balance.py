# src/ui/my_balance.py
import flet as ft
from datetime import datetime
from core import db


def create_my_balance_view(page: ft.Page, state: dict, toast, on_complete, on_back=None):
    """Create the 'Set up your cash balance' page after personal details."""
    
    # Theme colors
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#1a1a1a"
    FIELD_BG = "#252525"
    BORDER_COLOR = "#333333"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#9CA3AF"
    TEXT_MUTED = "#6B7280"
    TEAL_ACCENT = "#14B8A6"
    TEAL_LIGHT = "#2DD4BF"
    
    def show_view():
        """Render the balance setup view."""
        page.clean()
        
        # Balance state
        balance_state = {"value": "0", "currency": "PHP"}
        
        # Get user's currency preference from personal details
        if state.get("personal_details"):
            currency = state["personal_details"].get("currency", "PHP")
            if " - " in currency:
                currency = currency.split(" - ")[0]
            balance_state["currency"] = currency
        
        # Display text for amount
        amount_display = ft.Text(
            f"0 {balance_state['currency']}",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=TEXT_PRIMARY,
        )
        
        def update_display():
            """Update the amount display."""
            value = balance_state["value"]
            if value == "0":
                amount_display.value = f"0 {balance_state['currency']}"
            else:
                # Format with commas for readability
                try:
                    num = float(value)
                    if "." in value:
                        amount_display.value = f"{num:,.2f} {balance_state['currency']}"
                    else:
                        amount_display.value = f"{int(num):,} {balance_state['currency']}"
                except:
                    amount_display.value = f"{value} {balance_state['currency']}"
            page.update()
        
        def on_number_press(num: str):
            """Handle number button press."""
            def handler(e):
                current = balance_state["value"]
                
                if num == ".":
                    # Only allow one decimal point
                    if "." in current:
                        return
                    balance_state["value"] = current + "."
                elif current == "0":
                    balance_state["value"] = num
                else:
                    # Limit to reasonable length
                    if len(current.replace(".", "")) < 12:
                        balance_state["value"] = current + num
                
                update_display()
            return handler
        
        def on_backspace(e):
            """Handle backspace button press."""
            current = balance_state["value"]
            if len(current) > 1:
                balance_state["value"] = current[:-1]
            else:
                balance_state["value"] = "0"
            update_display()
        
        def handle_next(e):
            """Handle the Next button click - save balance and continue."""
            try:
                amount = float(balance_state["value"])
            except:
                amount = 0.0
            
            user_id = state.get("user_id")
            if not user_id:
                toast("Session error. Please try again.", "#EF4444")
                return
            
            # Create the primary Cash account with the initial balance
            try:
                # Check if primary account already exists
                accounts = db.get_accounts_by_user(user_id)
                primary_exists = any(acc[7] == 1 for acc in accounts) if accounts else False  # is_primary column
                
                if not primary_exists:
                    # Create primary cash account (db.insert_account auto-sets first as primary)
                    account_id = db.insert_account(
                        user_id=user_id,
                        name="Cash",
                        account_number="",
                        account_type="Cash",
                        balance=amount,
                        currency=balance_state["currency"],
                        color="#10B981",  # Green color for cash
                        created_at=datetime.now().isoformat(),
                    )
                    toast("Cash balance set successfully!", TEAL_ACCENT)
                else:
                    # Update existing primary account balance
                    for acc in accounts:
                        if acc[7] == 1:  # is_primary
                            db.update_account_balance(acc[0], user_id, amount)
                            toast("Balance updated!", TEAL_ACCENT)
                            break
                
                # Save to state for immediate use
                state["initial_balance"] = amount
                state["primary_currency"] = balance_state["currency"]
                
                # Continue to next step (onboarding)
                if on_complete:
                    on_complete()
                    
            except Exception as ex:
                toast(f"Error saving balance: {str(ex)}", "#EF4444")
        
        def create_number_button(num: str, size: int = 70):
            """Create a number pad button."""
            return ft.Container(
                content=ft.Text(
                    num,
                    size=28,
                    weight=ft.FontWeight.W_400,
                    color=TEXT_SECONDARY,
                ),
                width=size,
                height=size,
                border_radius=size // 2,
                alignment=ft.alignment.center,
                on_click=on_number_press(num),
                ink=True,
                ink_color="#ffffff10",
            )
        
        def create_backspace_button(size: int = 70):
            """Create the backspace button."""
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.BACKSPACE_OUTLINED,
                    size=24,
                    color=TEXT_SECONDARY,
                ),
                width=size,
                height=size,
                border_radius=size // 2,
                alignment=ft.alignment.center,
                on_click=on_backspace,
                ink=True,
                ink_color="#ffffff10",
            )
        
        def create_confirm_button(size: int = 70):
            """Create the confirm/next button."""
            return ft.Container(
                content=ft.Icon(
                    ft.Icons.CHECK_ROUNDED,
                    size=28,
                    color=TEXT_PRIMARY,
                ),
                width=size,
                height=size,
                border_radius=size // 2,
                bgcolor=TEAL_ACCENT,
                alignment=ft.alignment.center,
                on_click=handle_next,
                ink=True,
                ink_color="#ffffff30",
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,
                    color="#14B8A640",
                ),
            )
        
        # Number pad layout
        number_pad = ft.Container(
            content=ft.Column(
                controls=[
                    # Row 1: 1, 2, 3
                    ft.Row(
                        controls=[
                            create_number_button("1"),
                            create_number_button("2"),
                            create_number_button("3"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    # Row 2: 4, 5, 6
                    ft.Row(
                        controls=[
                            create_number_button("4"),
                            create_number_button("5"),
                            create_number_button("6"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    # Row 3: 7, 8, 9
                    ft.Row(
                        controls=[
                            create_number_button("7"),
                            create_number_button("8"),
                            create_number_button("9"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    # Row 4: ., 0, confirm
                    ft.Row(
                        controls=[
                            create_number_button("."),
                            create_number_button("0"),
                            create_confirm_button(),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                ],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=CARD_BG,
            border_radius=ft.border_radius.only(top_left=32, top_right=32),
            padding=ft.padding.only(left=24, right=24, top=32, bottom=40),
        )
        
        # Coin/Money icon
        coin_icon = ft.Container(
            content=ft.Text("🪙", size=64),
            width=120,
            height=120,
            bgcolor="#38BDF8",
            border_radius=60,
            alignment=ft.alignment.center,
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column(
                controls=[
                    # Header with Next button
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(width=50),  # Spacer
                                ft.Container(expand=True),  # Center spacer
                                ft.TextButton(
                                    text="Next",
                                    style=ft.ButtonStyle(
                                        color=TEAL_ACCENT,
                                    ),
                                    on_click=handle_next,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        padding=ft.padding.only(left=16, right=8, top=8),
                    ),
                    
                    # Expandable top section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(height=20),
                                
                                # Coin icon
                                coin_icon,
                                
                                ft.Container(height=24),
                                
                                # Title
                                ft.Text(
                                    "Set up your cash balance",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                
                                ft.Container(height=8),
                                
                                # Subtitle
                                ft.Text(
                                    "How much cash do you have in your physical wallet?",
                                    size=14,
                                    color=TEXT_SECONDARY,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                
                                ft.Container(height=32),
                                
                                # Amount display with backspace
                                ft.Row(
                                    controls=[
                                        ft.Container(expand=True),
                                        amount_display,
                                        ft.Container(width=16),
                                        create_backspace_button(size=44),
                                        ft.Container(expand=True),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                    
                    # Number pad at bottom
                    number_pad,
                ],
                spacing=0,
                expand=True,
            ),
            bgcolor=BG_COLOR,
            expand=True,
        )
        
        page.add(content)
        page.update()
    
    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_my_balance_content(page: ft.Page, state: dict, toast, on_complete, on_back=None):
    """
    Builds and returns balance setup page content WITHOUT calling page.clean() or page.add().
    """
    # Theme colors
    BG_COLOR = "#0a0a0a"
    CARD_BG = "#1a1a1a"
    FIELD_BG = "#252525"
    BORDER_COLOR = "#333333"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#9CA3AF"
    TEXT_MUTED = "#6B7280"
    TEAL_ACCENT = "#14B8A6"
    
    balance_state = {"value": "0", "currency": "PHP"}
    
    if state.get("personal_details"):
        currency = state["personal_details"].get("currency", "PHP")
        if " - " in currency:
            currency = currency.split(" - ")[0]
        balance_state["currency"] = currency
    
    amount_display = ft.Text(
        f"0 {balance_state['currency']}",
        size=36, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY,
    )
    
    def update_display():
        value = balance_state["value"]
        if value == "0":
            amount_display.value = f"0 {balance_state['currency']}"
        else:
            try:
                num = float(value)
                formatted = f"{num:,.0f}" if num == int(num) else f"{num:,.2f}"
                amount_display.value = f"{formatted} {balance_state['currency']}"
            except:
                amount_display.value = f"{value} {balance_state['currency']}"
        page.update()
    
    def on_number_click(num):
        def handler(e):
            if balance_state["value"] == "0":
                balance_state["value"] = num
            else:
                balance_state["value"] += num
            update_display()
        return handler
    
    def on_decimal_click(e):
        if "." not in balance_state["value"]:
            balance_state["value"] += "."
            update_display()
    
    def on_backspace_click(e):
        if len(balance_state["value"]) > 1:
            balance_state["value"] = balance_state["value"][:-1]
        else:
            balance_state["value"] = "0"
        update_display()
    
    def on_continue_click(e):
        try:
            amount = float(balance_state["value"])
        except:
            amount = 0
        
        if amount <= 0:
            toast("Please enter an amount greater than 0", "#EF4444")
            return
        
        user_id = state.get("user_id")
        if user_id:
            from datetime import datetime
            # Check if primary account already exists
            accounts = db.get_accounts_by_user(user_id)
            primary_exists = any(acc[7] == 1 for acc in accounts) if accounts else False
            
            if not primary_exists:
                # Create primary cash account
                db.insert_account(
                    user_id=user_id,
                    name="Cash",
                    account_number="",
                    account_type="Cash",
                    balance=amount,
                    currency=balance_state["currency"],
                    color="#10B981",
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                toast("Balance saved!", TEAL_ACCENT)
            else:
                # Update existing primary account balance
                for acc in accounts:
                    if acc[7] == 1:  # is_primary
                        db.update_account_balance(acc[0], user_id, amount)
                        toast("Balance updated!", TEAL_ACCENT)
                        break
            on_complete()
        else:
            toast("User not found", "#EF4444")
    
    def create_number_button(num, size=64):
        return ft.Container(
            content=ft.Text(num, size=24, weight=ft.FontWeight.W_500, color=TEXT_PRIMARY),
            width=size, height=size, border_radius=size/2,
            bgcolor=FIELD_BG,
            alignment=ft.alignment.center,
            on_click=on_number_click(num) if num.isdigit() else on_decimal_click,
            ink=True,
        )
    
    backspace_btn = ft.Container(
        content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, color=TEXT_PRIMARY, size=24),
        width=44, height=44, border_radius=22,
        bgcolor=FIELD_BG,
        alignment=ft.alignment.center,
        on_click=on_backspace_click,
        ink=True,
    )
    
    # Number pad
    number_pad = ft.Container(
        content=ft.Column([
            ft.Row([create_number_button("1"), create_number_button("2"), create_number_button("3")],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=16),
            ft.Row([create_number_button("4"), create_number_button("5"), create_number_button("6")],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=16),
            ft.Row([create_number_button("7"), create_number_button("8"), create_number_button("9")],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=16),
            ft.Row([create_number_button("."), create_number_button("0"),
                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Icon(ft.Icons.CHECK, color="white", size=24),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.DEFAULT: TEAL_ACCENT},
                                shape=ft.CircleBorder(),
                                padding=16,
                            ),
                            on_click=on_continue_click,
                        ),
                        width=64, height=64,
                    )],
                   alignment=ft.MainAxisAlignment.CENTER, spacing=16),
        ], spacing=12),
        padding=ft.padding.only(left=32, right=32, bottom=32, top=16),
        bgcolor=CARD_BG,
        border_radius=ft.border_radius.only(top_left=24, top_right=24),
    )
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                icon_color=TEXT_PRIMARY,
                icon_size=22,
                on_click=lambda e: on_back() if on_back else None,
            ),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Text("2/2", size=12, color=TEXT_SECONDARY),
                bgcolor=FIELD_BG,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
            ),
        ]),
        padding=ft.padding.only(left=8, right=16, top=16),
    )
    
    # Coin icon
    coin_icon = ft.Container(
        content=ft.Stack([
            ft.Container(
                width=80, height=80, border_radius=40,
                bgcolor=f"{TEAL_ACCENT}30",
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=40, color=TEAL_ACCENT),
                width=80, height=80,
                alignment=ft.alignment.center,
            ),
        ]),
    )
    
    return ft.Container(
        content=ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    ft.Container(height=20),
                    coin_icon,
                    ft.Container(height=24),
                    ft.Text("Set up your cash balance", size=22, weight=ft.FontWeight.BOLD,
                           color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Text("How much cash do you have in your physical wallet?",
                           size=14, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=32),
                    ft.Row([
                        ft.Container(expand=True),
                        amount_display,
                        ft.Container(width=16),
                        backspace_btn,
                        ft.Container(expand=True),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                expand=True,
                alignment=ft.alignment.center,
            ),
            number_pad,
        ], spacing=0, expand=True),
        bgcolor=BG_COLOR,
        expand=True,
    )
