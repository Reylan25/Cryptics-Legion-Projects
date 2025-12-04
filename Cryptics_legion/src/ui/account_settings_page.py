# src/ui/account_settings_page.py
import flet as ft
from core import db
from core.theme import get_theme


def create_account_settings_view(page: ft.Page, state: dict, toast, go_back):
    """Create the Account Settings page for managing user profile."""
    
    def show_view():
        """Render the account settings view."""
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Theme colors from theme manager
        BG_COLOR = theme.bg_primary
        CARD_BG = theme.bg_card
        FIELD_BG = theme.bg_field
        BORDER_COLOR = theme.border_primary
        TEXT_PRIMARY = theme.text_primary
        TEXT_SECONDARY = theme.text_secondary
        TEXT_MUTED = theme.text_muted
        ACCENT_COLOR = theme.accent_primary
        ACCENT_LIGHT = theme.accent_secondary
        SUCCESS_COLOR = theme.success
        
        # Load user profile from database
        user_profile = db.get_user_profile(state["user_id"]) or {}
        
        # Create text field references for editing
        full_name_field = ft.TextField(
            value=user_profile.get("full_name", ""),
            hint_text="Enter your full name",
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
        )
        
        email_field = ft.TextField(
            value=user_profile.get("email", ""),
            hint_text="Enter your email",
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
            keyboard_type=ft.KeyboardType.EMAIL,
        )
        
        phone_field = ft.TextField(
            value=user_profile.get("phone", ""),
            hint_text="+63 9XX XXX XXXX",
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
            keyboard_type=ft.KeyboardType.PHONE,
        )
        
        # Currency dropdown
        currency_options = [
            "PHP - Philippine Peso",
            "USD - US Dollar", 
            "EUR - Euro",
            "GBP - British Pound",
            "JPY - Japanese Yen",
            "KRW - Korean Won",
            "SGD - Singapore Dollar"
        ]
        current_currency = user_profile.get("currency", "PHP")
        # Match to full option if only code is stored
        currency_value = next((opt for opt in currency_options if opt.startswith(current_currency)), currency_options[0])
        
        currency_dropdown = ft.Dropdown(
            value=currency_value,
            options=[ft.dropdown.Option(opt) for opt in currency_options],
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=8),
            icon_enabled_color=ACCENT_COLOR,
        )
        
        # Timezone dropdown
        timezone_options = [
            "Asia/Manila (GMT+8)",
            "Asia/Singapore (GMT+8)",
            "Asia/Tokyo (GMT+9)",
            "America/New_York (GMT-5)",
            "America/Los_Angeles (GMT-8)",
            "Europe/London (GMT+0)",
            "Australia/Sydney (GMT+11)"
        ]
        current_tz = user_profile.get("timezone", "Asia/Manila")
        tz_value = next((opt for opt in timezone_options if current_tz in opt), timezone_options[0])
        
        timezone_dropdown = ft.Dropdown(
            value=tz_value,
            options=[ft.dropdown.Option(opt) for opt in timezone_options],
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=8),
            icon_enabled_color=ACCENT_COLOR,
        )
        
        # First day of week dropdown
        first_day_options = ["Monday", "Sunday", "Saturday"]
        first_day_dropdown = ft.Dropdown(
            value=user_profile.get("first_day_of_week", "Monday"),
            options=[ft.dropdown.Option(opt) for opt in first_day_options],
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color=TEXT_PRIMARY,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=8, vertical=8),
            icon_enabled_color=ACCENT_COLOR,
        )
        
        # Load photo state from user profile (moved here so save_changes can access it)
        saved_photo = user_profile.get("photo")
        if saved_photo and isinstance(saved_photo, dict):
            photo_state = {"type": saved_photo.get("type", "default"), "value": saved_photo.get("value"), "bg": saved_photo.get("bg")}
        else:
            photo_state = {"type": "default", "value": None, "bg": None}
        
        def create_field_container(label, icon, field, is_dropdown=False):
            """Create a styled field container."""
            return ft.Column(
                controls=[
                    ft.Text(label, size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(icon, size=20, color=TEXT_MUTED),
                                ft.Container(content=field, expand=True),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=FIELD_BG,
                        border_radius=12,
                        border=ft.border.all(1, BORDER_COLOR),
                        padding=ft.padding.only(left=16, right=8) if is_dropdown else ft.padding.only(left=16, right=12),
                        height=52,
                    ),
                ],
                spacing=8,
            )
        
        # Success message container (initially hidden)
        success_message = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=20, color=SUCCESS_COLOR),
                    ft.Text("Settings saved successfully!", size=14, color=SUCCESS_COLOR, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.only(top=12),
            visible=False,
        )
        
        def save_changes(e):
            """Save changes to the database."""
            # Collect form data including photo
            form_data = {
                "full_name": full_name_field.value or "",
                "email": email_field.value or "",
                "phone": phone_field.value or "",
                "currency": currency_dropdown.value.split(" - ")[0] if currency_dropdown.value else "PHP",
                "timezone": timezone_dropdown.value.split(" (")[0] if timezone_dropdown.value else "Asia/Manila",
                "first_day": first_day_dropdown.value or "Monday",
                "photo": photo_state.copy(),
            }
            
            # Validate
            if not form_data["full_name"].strip():
                toast("Please enter your full name", "#b71c1c")
                return
            
            # Save to database
            saved = db.save_personal_details(state["user_id"], form_data)
            if saved:
                # Show success message below button
                success_message.visible = True
                page.update()
                
                # Update state
                state["personal_details"] = form_data
                
                # Navigate to profile page after a short delay using threading
                import threading
                def delayed_navigate():
                    import time
                    time.sleep(1)
                    go_back()
                threading.Thread(target=delayed_navigate, daemon=True).start()
            else:
                toast("Failed to save settings", "#b71c1c")
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=24, color=TEXT_PRIMARY),
                        on_click=lambda e: go_back(),
                        ink=True,
                        border_radius=12,
                        padding=8,
                    ),
                    ft.Text("Account Settings", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Container(width=40),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(bottom=16),
        )
        
        # Avatar options - emoji-based avatars with different colors
        avatars = [
            {"emoji": "😊", "bg": "#FF6B6B", "name": "Happy"},
            {"emoji": "😎", "bg": "#4ECDC4", "name": "Cool"},
            {"emoji": "🤖", "bg": "#45B7D1", "name": "Robot"},
            {"emoji": "🦊", "bg": "#F7931E", "name": "Fox"},
            {"emoji": "🐱", "bg": "#FFB6C1", "name": "Cat"},
            {"emoji": "🦁", "bg": "#FFD93D", "name": "Lion"},
            {"emoji": "🐼", "bg": "#6BCB77", "name": "Panda"},
            {"emoji": "🦄", "bg": "#C9B1FF", "name": "Unicorn"},
            {"emoji": "🐺", "bg": "#5D5D5D", "name": "Wolf"},
            {"emoji": "🦅", "bg": "#8B4513", "name": "Eagle"},
        ]
        
        # State for bottom sheet reference
        bs_state = {"current_bs": None}
        
        # Photo display container
        def create_photo_display():
            if photo_state["type"] == "avatar":
                return ft.Container(
                    content=ft.Text(photo_state["value"], size=40),
                    width=100,
                    height=100,
                    bgcolor=photo_state["bg"],
                    border_radius=50,
                    alignment=ft.alignment.center,
                    border=ft.border.all(3, ACCENT_COLOR),
                )
            elif photo_state["type"] == "file":
                return ft.Container(
                    content=ft.Image(
                        src_base64=photo_state["value"],
                        width=96,
                        height=96,
                        fit=ft.ImageFit.COVER,
                        border_radius=48,
                    ),
                    width=100,
                    height=100,
                    bgcolor="transparent",
                    border_radius=50,
                    alignment=ft.alignment.center,
                    border=ft.border.all(3, ACCENT_COLOR),
                )
            else:
                return ft.CircleAvatar(
                    bgcolor=ACCENT_COLOR,
                    content=ft.Icon(ft.Icons.PERSON, color="white", size=40),
                    radius=50,
                )
        
        photo_display_ref = ft.Ref[ft.Container]()
        
        def update_photo_display():
            """Update the photo display and save to database."""
            new_display = create_photo_display()
            avatar_stack.controls[0] = new_display
            # Save photo to database
            form_data = {
                "full_name": full_name_field.value or user_profile.get("full_name", ""),
                "email": email_field.value or user_profile.get("email", ""),
                "phone": phone_field.value or user_profile.get("phone", ""),
                "currency": (currency_dropdown.value.split(" - ")[0] if currency_dropdown.value else "PHP"),
                "timezone": (timezone_dropdown.value.split(" (")[0] if timezone_dropdown.value else "Asia/Manila"),
                "first_day": first_day_dropdown.value or "Monday",
                "photo": photo_state.copy(),
            }
            db.save_personal_details(state["user_id"], form_data)
            page.update()
        
        def on_file_picked(e: ft.FilePickerResultEvent):
            """Handle file picker result."""
            if e.files and len(e.files) > 0:
                file = e.files[0]
                import base64
                with open(file.path, "rb") as f:
                    file_data = base64.b64encode(f.read()).decode("utf-8")
                photo_state["type"] = "file"
                photo_state["value"] = file_data
                photo_state["bg"] = None
                update_photo_display()
                if bs_state["current_bs"]:
                    page.close(bs_state["current_bs"])
                toast("Photo uploaded successfully!", SUCCESS_COLOR)
        
        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.clear()
        page.overlay.append(file_picker)
        
        def show_photo_picker(e):
            """Show bottom sheet with avatar selection and upload options."""
            
            def select_avatar(avatar):
                def handler(e):
                    photo_state["type"] = "avatar"
                    photo_state["value"] = avatar["emoji"]
                    photo_state["bg"] = avatar["bg"]
                    update_photo_display()
                    page.close(photo_picker_bs)
                    toast(f"{avatar['name']} avatar selected!", SUCCESS_COLOR)
                return handler
            
            def pick_file(e):
                file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["png", "jpg", "jpeg", "gif", "webp"],
                    dialog_title="Select Profile Photo"
                )
            
            def remove_photo(e):
                photo_state["type"] = "default"
                photo_state["value"] = None
                photo_state["bg"] = None
                update_photo_display()
                page.close(photo_picker_bs)
                toast("Photo removed", TEXT_SECONDARY)
            
            # Create avatar grid
            avatar_items = []
            for avatar in avatars:
                avatar_items.append(
                    ft.Container(
                        content=ft.Text(avatar["emoji"], size=32),
                        width=56,
                        height=56,
                        bgcolor=avatar["bg"],
                        border_radius=28,
                        alignment=ft.alignment.center,
                        on_click=select_avatar(avatar),
                        ink=True,
                        border=ft.border.all(2, "transparent") if photo_state["value"] != avatar["emoji"] else ft.border.all(3, TEXT_PRIMARY),
                    )
                )
            
            photo_picker_bs = ft.BottomSheet(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            # Header
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Text("Choose Profile Photo", size=18, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                                        ft.IconButton(
                                            icon=ft.Icons.CLOSE_ROUNDED,
                                            icon_color=TEXT_MUTED,
                                            icon_size=20,
                                            on_click=lambda e: page.close(photo_picker_bs),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.only(left=20, right=8, top=8, bottom=8),
                            ),
                            ft.Divider(height=1, color=BORDER_COLOR),
                            
                            # Avatar section
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Choose an Avatar", size=14, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                                        ft.Container(height=8),
                                        ft.Row(
                                            controls=avatar_items[:5],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        ft.Container(height=8),
                                        ft.Row(
                                            controls=avatar_items[5:],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                    ],
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=16),
                            ),
                            
                            ft.Divider(height=1, color=BORDER_COLOR),
                            
                            # Upload option
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.PHOTO_LIBRARY_ROUNDED, size=24, color=ACCENT_COLOR),
                                            width=44,
                                            height=44,
                                            bgcolor=f"{ACCENT_COLOR}20",
                                            border_radius=22,
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text("Upload from Device", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                                                ft.Text("Choose a photo from your files", size=12, color=TEXT_MUTED),
                                            ],
                                            spacing=2,
                                            expand=True,
                                        ),
                                        ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=20, color=TEXT_MUTED),
                                    ],
                                    spacing=12,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=14),
                                on_click=pick_file,
                                ink=True,
                                border_radius=8,
                            ),
                            
                            # Remove photo option
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=24, color="#EF4444"),
                                            width=44,
                                            height=44,
                                            bgcolor="#3D1A1A",
                                            border_radius=22,
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text("Remove Photo", size=14, color="#EF4444", weight=ft.FontWeight.W_500),
                                                ft.Text("Use default avatar", size=12, color=TEXT_MUTED),
                                            ],
                                            spacing=2,
                                            expand=True,
                                        ),
                                        ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, size=20, color=TEXT_MUTED),
                                    ],
                                    spacing=12,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=ft.padding.symmetric(horizontal=20, vertical=14),
                                on_click=remove_photo,
                                ink=True,
                                border_radius=8,
                                visible=photo_state["type"] != "default",
                            ),
                            
                            ft.Container(height=20),
                        ],
                        spacing=0,
                    ),
                    bgcolor=CARD_BG,
                    border_radius=ft.border_radius.only(top_left=20, top_right=20),
                    padding=0,
                ),
                bgcolor="transparent",
            )
            bs_state["current_bs"] = photo_picker_bs
            page.open(photo_picker_bs)
        
        # Build avatar stack
        avatar_stack = ft.Stack(
            controls=[
                create_photo_display(),
                ft.Container(
                    content=ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, size=16, color=TEXT_PRIMARY),
                    width=28,
                    height=28,
                    bgcolor=SUCCESS_COLOR,
                    border_radius=14,
                    alignment=ft.alignment.center,
                    right=0,
                    bottom=0,
                ),
            ],
            width=100,
            height=100,
        )
        
        # Profile avatar section
        avatar_section = ft.Container(
            content=ft.Column(
                controls=[
                    avatar_stack,
                    ft.Container(height=8),
                    ft.Text("Tap to change photo", size=12, color=ACCENT_COLOR),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(vertical=16),
            on_click=show_photo_picker,
            ink=True,
            ink_color=f"{ACCENT_COLOR}20",
            border_radius=16,
        )
        
        # Username display
        username_display = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ALTERNATE_EMAIL_ROUNDED, size=18, color=TEXT_MUTED),
                    ft.Text(f"Username: {state.get('username', 'N/A')}", size=14, color=TEXT_SECONDARY),
                ],
                spacing=8,
            ),
            padding=ft.padding.only(left=4, bottom=8),
        )
        
        # Form sections
        personal_info_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=20, color=ACCENT_COLOR),
                            ft.Text("Personal Information", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    create_field_container("Full Name", ft.Icons.BADGE_OUTLINED, full_name_field),
                    ft.Container(height=12),
                    create_field_container("Email Address", ft.Icons.EMAIL_OUTLINED, email_field),
                    ft.Container(height=12),
                    create_field_container("Phone Number", ft.Icons.PHONE_OUTLINED, phone_field),
                ],
            ),
            bgcolor=CARD_BG,
            border_radius=16,
            padding=20,
            border=ft.border.all(1, BORDER_COLOR),
        )
        
        financial_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, size=20, color=ACCENT_COLOR),
                            ft.Text("Financial Settings", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    create_field_container("Primary Currency", ft.Icons.CURRENCY_EXCHANGE_ROUNDED, currency_dropdown, is_dropdown=True),
                ],
            ),
            bgcolor=CARD_BG,
            border_radius=16,
            padding=20,
            border=ft.border.all(1, BORDER_COLOR),
        )
        
        locale_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.LANGUAGE_ROUNDED, size=20, color=ACCENT_COLOR),
                            ft.Text("Locale Settings", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    create_field_container("Time Zone", ft.Icons.ACCESS_TIME_ROUNDED, timezone_dropdown, is_dropdown=True),
                    ft.Container(height=12),
                    create_field_container("First Day of Week", ft.Icons.VIEW_WEEK_ROUNDED, first_day_dropdown, is_dropdown=True),
                ],
            ),
            bgcolor=CARD_BG,
            border_radius=16,
            padding=20,
            border=ft.border.all(1, BORDER_COLOR),
        )
        
        # Save button
        save_button = ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SAVE_ROUNDED, size=20),
                        ft.Text("Save Changes", size=16, weight=ft.FontWeight.W_600),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                style=ft.ButtonStyle(
                    bgcolor={
                        ft.ControlState.DEFAULT: ACCENT_COLOR,
                        ft.ControlState.HOVERED: ACCENT_LIGHT,
                    },
                    color={ft.ControlState.DEFAULT: TEXT_PRIMARY},
                    elevation=0,
                    padding=ft.padding.symmetric(vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=14),
                ),
                on_click=save_changes,
                width=float("inf"),
            ),
            padding=ft.padding.only(top=8, bottom=32),
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Column(
                        controls=[
                            avatar_section,
                            username_display,
                            personal_info_section,
                            ft.Container(height=16),
                            financial_section,
                            ft.Container(height=16),
                            locale_section,
                            save_button,
                            success_message,
                        ],
                        spacing=0,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.gradient_start, theme.gradient_end],
            ),
            padding=20,
            expand=True,
        )
        
        page.add(content)
        page.bgcolor = theme.bg_primary
        page.update()
    
    return show_view
