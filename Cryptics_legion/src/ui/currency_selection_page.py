# src/ui/currency_selection_page.py
import flet as ft
from core import db
from utils.currency import CURRENCY_LIST


def build_currency_selection_content(page: ft.Page, state: dict, toast, on_complete):
    """Build the currency selection page content during onboarding."""
    
    # Theme colors
    BG_COLOR = "#0a0a0a"
    BG_GRADIENT_START = "#1a1a2e"
    BG_GRADIENT_MID = "#16213e"
    BG_GRADIENT_END = "#0f3460"
    CARD_BG = "#1a1a2e"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#9CA3AF"
    TEAL_ACCENT = "#14B8A6"
    TEAL_LIGHT = "#2DD4BF"
    
    selected_currency = ft.Ref[str]()
    selected_currency.current = "PHP"  # Default
    
    # Currency icon/illustration
    currency_icon = ft.Container(
            content=ft.Stack(
                controls=[
                    # Background circle
                    ft.Container(
                        width=140,
                        height=140,
                        border_radius=70,
                        bgcolor=TEAL_ACCENT,
                    ),
                    # Currency bill icon
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ATTACH_MONEY_ROUNDED,
                                    size=50,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Container(
                                    width=80,
                                    height=50,
                                    border_radius=8,
                                    bgcolor="#ffffff20",
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                width=60,
                                                height=4,
                                                bgcolor="#ffffff60",
                                                border_radius=2,
                                            ),
                                            ft.Text(
                                                "?",
                                                size=24,
                                                color=TEXT_PRIMARY,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Container(
                                                width=40,
                                                height=3,
                                                bgcolor="#ffffff40",
                                                border_radius=2,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=4,
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        width=140,
                        height=140,
                        alignment=ft.alignment.center,
                    ),
            ],
            alignment=ft.alignment.center,
        ),
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=24),
    )
    
    # Title
    title = ft.Text(
        "Select base currency",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
        text_align=ft.TextAlign.CENTER,
    )
    
    # Currency dropdown
    currency_dropdown = ft.Dropdown(
        value="PHP",
        options=[ft.dropdown.Option(key=c['code'], text=f"{c['code']} - {c['name']}") for c in CURRENCY_LIST],
        hint_text="Select currency",
        filled=True,
        bgcolor="#2a2a3e",
        border_color="#3a3a5a",
        focused_border_color=TEAL_ACCENT,
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=14),
        label_style=ft.TextStyle(color=TEXT_SECONDARY, size=14),
        border_radius=12,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        width=350,
    )
    
    # Description text
    description = ft.Text(
        "Your base currency should ideally be the one you use most often. Your balance & statistics will be shown in this currency.",
        size=14,
        color=TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
        width=350,
    )
    
    def on_confirm(e):
        """Save currency and proceed to home page."""
        try:
            # Extract currency code - value is now the key (currency code)
            currency_code = currency_dropdown.value if currency_dropdown.value else "PHP"
            print(f"Selected currency: {currency_code}")
            
            # Update user profile with currency
            user_profile = db.get_user_profile(state["user_id"])
            if user_profile:
                form_data = {
                    "first_name": user_profile.get("first_name", ""),
                    "last_name": user_profile.get("last_name", ""),
                    "full_name": user_profile.get("full_name", ""),
                    "email": user_profile.get("email", ""),
                    "phone": user_profile.get("phone", ""),
                    "currency": currency_code,
                    "timezone": user_profile.get("timezone", "Asia/Manila"),
                    "first_day": user_profile.get("first_day_of_week", "Monday"),
                    "photo": user_profile.get("photo"),
                }
                db.save_personal_details(state["user_id"], form_data)
                print("Currency saved to profile")
            
            # Create default Cash account with currency
            existing_accounts = db.get_accounts_by_user(state["user_id"])
            print(f"Existing accounts: {len(existing_accounts) if existing_accounts else 0}")
            if not existing_accounts:
                # Create Cash account with the selected currency
                from datetime import datetime
                account_id = db.insert_account(
                    user_id=state["user_id"],
                    name="Cash",
                    account_number="",
                    account_type="Cash",
                    balance=0.0,
                    currency=currency_code,
                    color="#4CAF50",
                    created_at=datetime.now().isoformat()
                )
                print(f"Created Cash account with ID: {account_id}")
            
            toast(f"Currency set to {currency_code}", TEAL_ACCENT)
            print("Calling on_complete()")
            on_complete()
        except Exception as ex:
            print(f"Error in on_confirm: {ex}")
            import traceback
            traceback.print_exc()
            toast(f"Error: {str(ex)}", "#EF4444")
    
    # Confirm button
    confirm_button = ft.Container(
        content=ft.Text(
            "Confirm",
            size=16,
            weight=ft.FontWeight.W_600,
            color=TEXT_PRIMARY,
        ),
        width=350,
        height=52,
        bgcolor=TEAL_ACCENT,
        border_radius=26,
        alignment=ft.alignment.center,
        on_click=on_confirm,
        animate=ft.Animation(100, "easeOut"),
        ink=True,
    )
    
    # Main content
    content = ft.Container(
        content=ft.Column(
            controls=[
                currency_icon,
                title,
                ft.Container(height=24),
                currency_dropdown,
                ft.Container(height=16),
                description,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=40),
        alignment=ft.alignment.center,
    )
    
    # Return the main view
    return ft.Container(
        content=ft.Column(
            controls=[
                content,
                ft.Container(expand=True),  # Spacer
                confirm_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BG_GRADIENT_START, BG_GRADIENT_MID, BG_GRADIENT_END],
        ),
        padding=ft.padding.only(left=24, right=24, top=40, bottom=40),
        expand=True,
    )
