# src/ui/personal_details.py
import flet as ft
import re
from core import db
from core import auth


def create_personal_details_view(page: ft.Page, state: dict, toast, on_complete, on_back=None):
    """Create the Personal Details form page after account creation."""
    
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
    TEAL_BG = "#0D3D38"
    
    def show_view():
        """Render the personal details view."""
        page.clean()
        
        # Form state - now includes username
        form_data = {
            "username": "",
            "full_name": "",
            "email": "",
            "phone": "",
            "photo": None,
            "currency": "PHP",
            "timezone": "Asia/Manila",
            "first_day": "Monday",
        }
        
        # Store error text references for validation
        error_texts = {}
        field_containers = {}
        
        def create_input_field(label: str, hint: str, icon, key: str, keyboard_type=ft.KeyboardType.TEXT):
            """Create a styled input field with inline error support."""
            
            # Create error text (initially hidden)
            error_text = ft.Text("", size=11, color="#EF4444", visible=False)
            error_texts[key] = error_text
            
            def on_change(e):
                form_data[key] = e.control.value
                # Clear error when user types
                if error_text.visible:
                    error_text.visible = False
                    field_container.border = ft.border.all(1, BORDER_COLOR)
                    page.update()
            
            def on_focus(e):
                e.control.parent.parent.border = ft.border.all(1.5, TEAL_ACCENT)
                e.control.parent.parent.update()
            
            def on_blur(e):
                if not error_text.visible:
                    e.control.parent.parent.border = ft.border.all(1, BORDER_COLOR)
                    e.control.parent.parent.update()
            
            field_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, size=20, color=TEXT_MUTED),
                        ft.TextField(
                            hint_text=hint,
                            hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
                            border=ft.InputBorder.NONE,
                            bgcolor="transparent",
                            color=TEXT_PRIMARY,
                            text_size=14,
                            expand=True,
                            content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
                            keyboard_type=keyboard_type,
                            on_change=on_change,
                            on_focus=on_focus,
                            on_blur=on_blur,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=FIELD_BG,
                border_radius=12,
                border=ft.border.all(1, BORDER_COLOR),
                padding=ft.padding.only(left=16, right=12),
            )
            field_containers[key] = field_container
            
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(label, size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                            error_text,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    field_container,
                ],
                spacing=8,
            )
        
        def create_phone_field():
            """Create a phone input field with country code selector."""
            
            # Common country codes
            country_codes = [
                {"code": "+63", "country": "🇵🇭 Philippines", "flag": "🇵🇭"},
                {"code": "+1", "country": "🇺🇸 United States", "flag": "🇺🇸"},
                {"code": "+44", "country": "🇬🇧 United Kingdom", "flag": "🇬🇧"},
                {"code": "+81", "country": "🇯🇵 Japan", "flag": "🇯🇵"},
                {"code": "+82", "country": "🇰🇷 South Korea", "flag": "🇰🇷"},
                {"code": "+86", "country": "🇨🇳 China", "flag": "🇨🇳"},
                {"code": "+65", "country": "🇸🇬 Singapore", "flag": "🇸🇬"},
                {"code": "+60", "country": "🇲🇾 Malaysia", "flag": "🇲🇾"},
                {"code": "+66", "country": "🇹🇭 Thailand", "flag": "🇹🇭"},
                {"code": "+84", "country": "🇻🇳 Vietnam", "flag": "🇻🇳"},
                {"code": "+62", "country": "🇮🇩 Indonesia", "flag": "🇮🇩"},
                {"code": "+91", "country": "🇮🇳 India", "flag": "🇮🇳"},
                {"code": "+971", "country": "🇦🇪 UAE", "flag": "🇦🇪"},
                {"code": "+966", "country": "🇸🇦 Saudi Arabia", "flag": "🇸🇦"},
                {"code": "+61", "country": "🇦🇺 Australia", "flag": "🇦🇺"},
                {"code": "+49", "country": "🇩🇪 Germany", "flag": "🇩🇪"},
                {"code": "+33", "country": "🇫🇷 France", "flag": "🇫🇷"},
                {"code": "+39", "country": "🇮🇹 Italy", "flag": "🇮🇹"},
                {"code": "+34", "country": "🇪🇸 Spain", "flag": "🇪🇸"},
                {"code": "+7", "country": "🇷🇺 Russia", "flag": "🇷🇺"},
            ]
            
            # State for selected country code
            selected_code = {"value": "+63", "flag": "🇵🇭"}
            
            # Create the code button text
            code_text = ft.Text(f"{selected_code['flag']} {selected_code['value']}", size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.W_500)
            
            # Phone input field
            phone_input = ft.TextField(
                hint_text="9XX XXX XXXX",
                hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
                border=ft.InputBorder.NONE,
                bgcolor="transparent",
                color=TEXT_PRIMARY,
                text_size=14,
                expand=True,
                content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
                keyboard_type=ft.KeyboardType.PHONE,
            )
            
            def update_phone_value(e=None):
                form_data["phone"] = f"{selected_code['value']} {phone_input.value}" if phone_input.value else ""
            
            phone_input.on_change = lambda e: update_phone_value()
            
            def on_focus(e):
                e.control.parent.parent.parent.border = ft.border.all(1.5, TEAL_ACCENT)
                page.update()
            
            def on_blur(e):
                e.control.parent.parent.parent.border = ft.border.all(1, BORDER_COLOR)
                page.update()
            
            phone_input.on_focus = on_focus
            phone_input.on_blur = on_blur
            
            # Create error text for phone field
            phone_error_text = ft.Text("", size=11, color="#EF4444", visible=False)
            error_texts["phone"] = phone_error_text
            
            def show_country_picker(e):
                def select_country(country):
                    def handler(e):
                        selected_code["value"] = country["code"]
                        selected_code["flag"] = country["flag"]
                        code_text.value = f"{country['flag']} {country['code']}"
                        update_phone_value()
                        page.close(bs)
                        page.update()
                    return handler
                
                country_items = [
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(f"{c['country']}", size=14, color=TEXT_PRIMARY, expand=True),
                                ft.Text(c["code"], size=14, color=TEAL_ACCENT, weight=ft.FontWeight.W_600),
                            ],
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        on_click=select_country(c),
                        ink=True,
                        border_radius=8,
                    )
                    for c in country_codes
                ]
                
                bs = ft.BottomSheet(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text("Select Country Code", size=18, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY),
                                            ft.IconButton(
                                                icon=ft.Icons.CLOSE_ROUNDED,
                                                icon_color=TEXT_MUTED,
                                                icon_size=20,
                                                on_click=lambda e: page.close(bs),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=ft.padding.only(left=20, right=8, top=8, bottom=8),
                                ),
                                ft.Divider(height=1, color=BORDER_COLOR),
                                ft.Container(
                                    content=ft.Column(
                                        controls=country_items,
                                        scroll=ft.ScrollMode.AUTO,
                                        spacing=2,
                                    ),
                                    expand=True,
                                    padding=ft.padding.only(bottom=20),
                                ),
                            ],
                            spacing=0,
                        ),
                        bgcolor=CARD_BG,
                        border_radius=ft.border_radius.only(top_left=20, top_right=20),
                        padding=0,
                        height=450,
                    ),
                    bgcolor="transparent",
                )
                page.open(bs)
            
            # Country code selector button
            code_button = ft.Container(
                content=ft.Row(
                    controls=[
                        code_text,
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, size=20, color=TEXT_MUTED),
                    ],
                    spacing=2,
                ),
                on_click=show_country_picker,
                ink=True,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=4, vertical=4),
            )
            
            phone_field_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PHONE_OUTLINED, size=20, color=TEXT_MUTED),
                        code_button,
                        ft.Container(width=1, height=24, bgcolor=BORDER_COLOR),
                        phone_input,
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=FIELD_BG,
                border_radius=12,
                border=ft.border.all(1, BORDER_COLOR),
                padding=ft.padding.only(left=16, right=12),
            )
            field_containers["phone"] = phone_field_container
            
            # Clear error when user types
            original_on_change = phone_input.on_change
            def phone_on_change_with_clear(e):
                if original_on_change:
                    original_on_change(e)
                if phone_error_text.visible:
                    phone_error_text.visible = False
                    phone_field_container.border = ft.border.all(1, BORDER_COLOR)
                    page.update()
            phone_input.on_change = phone_on_change_with_clear
            
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Phone Number", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                            phone_error_text,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    phone_field_container,
                ],
                spacing=8,
            )
        
        def create_dropdown_field(label: str, icon, options: list, default: str, key: str):
            """Create a styled dropdown field."""
            
            def on_change(e):
                form_data[key] = e.control.value
            
            dropdown_items = [
                ft.dropdown.Option(text=opt, key=opt) for opt in options
            ]
            
            return ft.Column(
                controls=[
                    ft.Text(label, size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(icon, size=20, color=TEXT_MUTED),
                                ft.Dropdown(
                                    options=dropdown_items,
                                    value=default,
                                    border=ft.InputBorder.NONE,
                                    bgcolor="transparent",
                                    color=TEXT_PRIMARY,
                                    text_size=14,
                                    expand=True,
                                    content_padding=ft.padding.symmetric(horizontal=8, vertical=8),
                                    on_change=on_change,
                                    icon_enabled_color=TEAL_ACCENT,
                                    focused_bgcolor="transparent",
                                    focused_border_color="transparent",
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor=FIELD_BG,
                        border_radius=12,
                        border=ft.border.all(1, BORDER_COLOR),
                        padding=ft.padding.only(left=16, right=8),
                        height=52,
                    ),
                ],
                spacing=8,
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
        
        # State for selected avatar/photo
        photo_state = {"type": "default", "value": None, "bg": None}
        
        # Photo display container (will be updated)
        photo_display = ft.Container(
            content=ft.Icon(ft.Icons.PERSON_ROUNDED, size=48, color=TEXT_MUTED),
            width=100,
            height=100,
            bgcolor=FIELD_BG,
            border_radius=50,
            border=ft.border.all(2, BORDER_COLOR),
            alignment=ft.alignment.center,
        )
        
        def update_photo_display():
            """Update the photo display based on current state."""
            if photo_state["type"] == "avatar":
                photo_display.content = ft.Text(photo_state["value"], size=48)
                photo_display.bgcolor = photo_state["bg"]
                photo_display.border = ft.border.all(3, TEAL_ACCENT)
            elif photo_state["type"] == "file":
                photo_display.content = ft.Image(
                    src_base64=photo_state["value"],
                    width=96,
                    height=96,
                    fit=ft.ImageFit.COVER,
                    border_radius=48,
                )
                photo_display.bgcolor = "transparent"
                photo_display.border = ft.border.all(3, TEAL_ACCENT)
            else:
                photo_display.content = ft.Icon(ft.Icons.PERSON_ROUNDED, size=48, color=TEXT_MUTED)
                photo_display.bgcolor = FIELD_BG
                photo_display.border = ft.border.all(2, BORDER_COLOR)
            form_data["photo"] = photo_state.copy()
            page.update()
        
        # State to track bottom sheet
        bs_state = {"current_bs": None}
        
        def on_file_picked(e: ft.FilePickerResultEvent):
            """Handle file picker result."""
            if e.files and len(e.files) > 0:
                file = e.files[0]
                # Read file as base64
                import base64
                with open(file.path, "rb") as f:
                    file_data = base64.b64encode(f.read()).decode("utf-8")
                photo_state["type"] = "file"
                photo_state["value"] = file_data
                photo_state["bg"] = None
                update_photo_display()
                if bs_state["current_bs"]:
                    page.close(bs_state["current_bs"])
                toast("Photo uploaded successfully!", TEAL_ACCENT)
        
        # File picker
        file_picker = ft.FilePicker(on_result=on_file_picked)
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
                    toast(f"{avatar['name']} avatar selected!", TEAL_ACCENT)
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
            
            # Build bottom sheet content
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
                                            content=ft.Icon(ft.Icons.PHOTO_LIBRARY_ROUNDED, size=24, color=TEAL_ACCENT),
                                            width=44,
                                            height=44,
                                            bgcolor=TEAL_BG,
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
                            
                            # Remove photo option (only show if photo is set)
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
        
        # Photo upload section with click handler
        photo_container = ft.Container(
            content=ft.Stack(
                controls=[
                    photo_display,
                    ft.Container(
                        content=ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, size=18, color=TEXT_PRIMARY),
                        width=32,
                        height=32,
                        bgcolor=TEAL_ACCENT,
                        border_radius=16,
                        alignment=ft.alignment.center,
                        right=0,
                        bottom=0,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color="#00000040",
                        ),
                    ),
                ],
                width=100,
                height=100,
            ),
            on_click=show_photo_picker,
            ink=True,
            ink_color="#14B8A620",
            border_radius=50,
        )
        
        def create_username_field():
            """Create username input field with inline error support."""
            
            # Create error text for username (initially hidden)
            username_error_text = ft.Text("", size=11, color="#EF4444", visible=False)
            error_texts["username"] = username_error_text
            
            def on_change(e):
                form_data["username"] = e.control.value
                # Clear error when user types
                if username_error_text.visible:
                    username_error_text.visible = False
                    username_field_container.border = ft.border.all(1, BORDER_COLOR)
                    page.update()
            
            def on_focus(e):
                e.control.parent.parent.border = ft.border.all(1.5, TEAL_ACCENT)
                page.update()
            
            def on_blur(e):
                if not username_error_text.visible:
                    e.control.parent.parent.border = ft.border.all(1, BORDER_COLOR)
                    page.update()
            
            username_field_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ALTERNATE_EMAIL_ROUNDED, size=20, color=TEXT_MUTED),
                        ft.TextField(
                            hint_text="Choose a unique username",
                            hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
                            border=ft.InputBorder.NONE,
                            bgcolor="transparent",
                            color=TEXT_PRIMARY,
                            text_size=14,
                            expand=True,
                            content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
                            on_change=on_change,
                            on_focus=on_focus,
                            on_blur=on_blur,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=FIELD_BG,
                border_radius=12,
                border=ft.border.all(1, BORDER_COLOR),
                padding=ft.padding.only(left=16, right=12),
            )
            field_containers["username"] = username_field_container
            
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Username", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_500),
                            username_error_text,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    username_field_container,
                    ft.Text("3-20 characters, letters, numbers, underscore only", size=11, color=TEXT_MUTED),
                    ft.Text("📌 This will be your login username", size=11, color=TEAL_ACCENT, italic=True),
                ],
                spacing=6,
            )
        
        def validate_username(username: str):
            """Validate username."""
            if not username:
                return False, "Username is required"
            if len(username) < 3:
                return False, "Username must be at least 3 characters"
            if len(username) > 20:
                return False, "Username must be 20 characters or less"
            if ' ' in username:
                return False, "Username cannot contain spaces"
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                return False, "Username can only contain letters, numbers, and underscores"
            return True, ""
        
        def show_field_error(key: str, message: str):
            """Show inline error for a field."""
            if key in error_texts:
                error_texts[key].value = message
                error_texts[key].visible = True
            if key in field_containers:
                field_containers[key].border = ft.border.all(1.5, "#EF4444")
            page.update()
        
        def clear_field_error(key: str):
            """Clear inline error for a field."""
            if key in error_texts:
                error_texts[key].visible = False
            if key in field_containers:
                field_containers[key].border = ft.border.all(1, BORDER_COLOR)
        
        def clear_all_errors():
            """Clear all field errors."""
            for key in error_texts:
                clear_field_error(key)
        
        def handle_continue(e):
            """Handle continue button click with validation."""
            # Clear previous errors
            clear_all_errors()
            
            has_errors = False
            
            # Validate username first
            username = form_data["username"].strip() if form_data["username"] else ""
            is_valid_username, username_error = validate_username(username)
            if not is_valid_username:
                show_field_error("username", username_error)
                has_errors = True
            
            # Validate full name
            if not form_data["full_name"].strip():
                show_field_error("full_name", "Please enter full name")
                has_errors = True
            
            # Validate email
            if not form_data["email"].strip():
                show_field_error("email", "Please enter email")
                has_errors = True
            else:
                # Basic email validation
                email = form_data["email"].strip()
                if "@" not in email or "." not in email:
                    show_field_error("email", "Invalid email format")
                    has_errors = True
            
            # Validate phone
            if not form_data["phone"].strip():
                show_field_error("phone", "Please enter phone number")
                has_errors = True
            else:
                # Phone number should have at least 10 digits
                phone_digits = ''.join(filter(str.isdigit, form_data["phone"]))
                if len(phone_digits) < 10:
                    show_field_error("phone", "At least 10 digits required")
                    has_errors = True
            
            if has_errors:
                return
            
            # Get password from state (set by register page)
            password = state.get("temp_password")
            if not password:
                toast("Session expired. Please start registration again.", "#b71c1c")
                return
            
            # Create the user account
            try:
                ok = auth.register_user(username, password)
                if not ok:
                    toast("Username already exists. Please choose another.", "#b71c1c")
                    return
                
                # Get the new user_id
                user_row = db.get_user_by_username(username)
                if not user_row:
                    toast("Failed to create account", "#b71c1c")
                    return
                
                user_id = user_row[0]
                state["user_id"] = user_id
                
                # Clear temp password
                state["temp_password"] = None
                
                # Save personal details to database
                saved = db.save_personal_details(user_id, form_data)
                if saved:
                    toast("Account created successfully!", "#2E7D32")
                else:
                    toast("Account created but failed to save details", "#F59E0B")
                
                # Save to state as well
                state["personal_details"] = form_data
                
                if on_complete:
                    on_complete()
                    
            except Exception as ex:
                toast(f"Error creating account: {str(ex)}", "#b71c1c")
        
        # Main content
        content = ft.Container(
            content=ft.Column(
                controls=[
                    # Header with back button
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, size=20, color=TEXT_PRIMARY),
                                                width=40,
                                                height=40,
                                                border_radius=20,
                                                bgcolor=FIELD_BG,
                                                alignment=ft.alignment.center,
                                                on_click=lambda e: on_back() if on_back else None,
                                                ink=True,
                                            ),
                                            ft.Text("Back", size=14, color=TEXT_SECONDARY),
                                        ],
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.only(top=8),
                                ),
                                ft.Container(height=8),
                                ft.Text(
                                    "Personal Information",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Text(
                                    "Complete your profile to personalize your experience",
                                    size=14,
                                    color=TEXT_SECONDARY,
                                ),
                            ],
                            spacing=4,
                        ),
                        padding=ft.padding.only(left=20, right=20, top=16, bottom=8),
                    ),
                    
                    # Scrollable form
                    ft.Container(
                        content=ft.ListView(
                            controls=[
                                # Main card
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            # Photo upload section
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        photo_container,
                                                        ft.Container(height=8),
                                                        ft.Text("Upload Photo", size=14, color=TEAL_ACCENT, weight=ft.FontWeight.W_500),
                                                        ft.Text("Tap to add your profile picture", size=12, color=TEXT_MUTED),
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    spacing=2,
                                                ),
                                                alignment=ft.alignment.center,
                                                padding=ft.padding.only(top=8, bottom=16),
                                            ),
                                            
                                            ft.Divider(height=1, color=BORDER_COLOR),
                                            ft.Container(height=8),
                                            
                                            # Section: Basic Info
                                            ft.Text("Basic Information", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                            ft.Container(height=8),
                                            
                                            create_username_field(),
                                            ft.Container(height=12),
                                            
                                            create_input_field(
                                                "Full Name",
                                                "Enter your full name",
                                                ft.Icons.PERSON_OUTLINE_ROUNDED,
                                                "full_name"
                                            ),
                                            ft.Container(height=12),
                                            
                                            create_input_field(
                                                "Email Address",
                                                "Enter your email",
                                                ft.Icons.EMAIL_OUTLINED,
                                                "email",
                                                ft.KeyboardType.EMAIL
                                            ),
                                            ft.Container(height=12),
                                            
                                            create_phone_field(),
                                            
                                            ft.Container(height=24),
                                            ft.Divider(height=1, color=BORDER_COLOR),
                                            ft.Container(height=16),
                                            
                                            # Section: Financial Settings
                                            ft.Text("Financial Settings", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                            ft.Container(height=8),
                                            
                                            create_dropdown_field(
                                                "Primary Currency",
                                                ft.Icons.CURRENCY_EXCHANGE_ROUNDED,
                                                ["PHP - Philippine Peso", "USD - US Dollar", "EUR - Euro", "GBP - British Pound", "JPY - Japanese Yen", "KRW - Korean Won", "SGD - Singapore Dollar"],
                                                "PHP - Philippine Peso",
                                                "currency"
                                            ),
                                            
                                            ft.Container(height=24),
                                            ft.Divider(height=1, color=BORDER_COLOR),
                                            ft.Container(height=16),
                                            
                                            # Section: Locale Settings
                                            ft.Text("Locale Settings", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
                                            ft.Container(height=8),
                                            
                                            create_dropdown_field(
                                                "Time Zone",
                                                ft.Icons.ACCESS_TIME_ROUNDED,
                                                ["Asia/Manila (GMT+8)", "Asia/Singapore (GMT+8)", "Asia/Tokyo (GMT+9)", "America/New_York (GMT-5)", "America/Los_Angeles (GMT-8)", "Europe/London (GMT+0)", "Australia/Sydney (GMT+11)"],
                                                "Asia/Manila (GMT+8)",
                                                "timezone"
                                            ),
                                            ft.Container(height=12),
                                            
                                            create_dropdown_field(
                                                "First Day of Week",
                                                ft.Icons.VIEW_WEEK_ROUNDED,
                                                ["Monday", "Sunday", "Saturday"],
                                                "Monday",
                                                "first_day"
                                            ),
                                            
                                            ft.Container(height=24),
                                        ],
                                        spacing=0,
                                    ),
                                    bgcolor=CARD_BG,
                                    border_radius=20,
                                    padding=ft.padding.all(20),
                                    margin=ft.margin.only(left=16, right=16, bottom=16),
                                    border=ft.border.all(1, BORDER_COLOR),
                                ),
                                
                                # Continue button
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Row(
                                            controls=[
                                                ft.Text("Continue", size=16, weight=ft.FontWeight.W_600),
                                                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=20),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=8,
                                        ),
                                        style=ft.ButtonStyle(
                                            bgcolor={
                                                ft.ControlState.DEFAULT: TEAL_ACCENT,
                                                ft.ControlState.HOVERED: TEAL_LIGHT,
                                            },
                                            color={ft.ControlState.DEFAULT: TEXT_PRIMARY},
                                            elevation=0,
                                            padding=ft.padding.symmetric(vertical=16),
                                            shape=ft.RoundedRectangleBorder(radius=14),
                                        ),
                                        on_click=handle_continue,
                                        width=float("inf"),
                                    ),
                                    padding=ft.padding.only(left=16, right=16, bottom=32),
                                ),
                            ],
                            spacing=0,
                            padding=ft.padding.only(bottom=20),
                        ),
                        expand=True,
                    ),
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
def build_personal_details_content(page: ft.Page, state: dict, toast, on_complete, on_back=None):
    """
    Builds and returns personal details page content WITHOUT calling page.clean() or page.add().
    This is a simplified version - for full functionality, use create_personal_details_view.
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
    
    form_data = {"username": "", "full_name": "", "email": "", "phone": "", "currency": "PHP"}
    
    def create_field(label, hint, icon, key):
        def on_change(e):
            form_data[key] = e.control.value
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=TEXT_MUTED),
                ft.TextField(
                    hint_text=hint,
                    hint_style=ft.TextStyle(color=TEXT_MUTED, size=14),
                    border=ft.InputBorder.NONE,
                    bgcolor="transparent",
                    color=TEXT_PRIMARY,
                    text_size=14,
                    expand=True,
                    on_change=on_change,
                ),
            ]),
            bgcolor=FIELD_BG,
            border_radius=12,
            padding=ft.padding.only(left=16, right=8),
            border=ft.border.all(1, BORDER_COLOR),
        )
    
    def handle_continue(e):
        username = form_data["username"].strip()
        full_name = form_data["full_name"].strip()
        email = form_data["email"].strip()
        phone = form_data["phone"].strip()
        
        if not username:
            toast("Please enter a username", "#EF4444")
            return
        if len(username) < 3:
            toast("Username must be at least 3 characters", "#EF4444")
            return
        
        # Check if username exists
        if db.get_user_by_username(username):
            toast("Username already taken", "#EF4444")
            return
        
        # Register user
        password = state.get("temp_password", "")
        if not password:
            toast("Session expired. Please start registration again.", "#EF4444")
            return
            
        ok = auth.register_user(username, password)
        
        if ok:
            # Get the new user_id
            user_row = db.get_user_by_username(username)
            if not user_row:
                toast("Failed to retrieve user account", "#EF4444")
                return
            
            user_id = user_row[0]
            state["user_id"] = user_id
            
            # Clear temp password
            state["temp_password"] = None
            
            # Save profile
            profile_data = {
                "username": username,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "currency": form_data.get("currency", "PHP"),
                "firstName": full_name.split()[0] if full_name else username,
            }
            db.save_personal_details(user_id, profile_data)
            
            toast("Account created successfully!", TEAL_ACCENT)
            on_complete()
        else:
            toast("Failed to create account", "#EF4444")
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_ROUNDED,
                icon_color=TEXT_PRIMARY,
                icon_size=22,
                on_click=lambda e: on_back() if on_back else None,
            ),
            ft.Column([
                ft.Text("Personal Details", size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Text("Tell us about yourself", size=12, color=TEXT_SECONDARY),
            ], spacing=2, expand=True),
            ft.Container(
                content=ft.Text("1/2", size=12, color=TEXT_SECONDARY),
                bgcolor=FIELD_BG,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
            ),
        ]),
        padding=ft.padding.only(left=8, right=16, top=16, bottom=8),
    )
    
    # Form fields
    form = ft.Container(
        content=ft.Column([
            ft.Text("Account Info", size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            create_field("Username", "Choose a username", ft.Icons.ALTERNATE_EMAIL_ROUNDED, "username"),
            ft.Container(height=12),
            create_field("Full Name", "Enter your full name", ft.Icons.PERSON_OUTLINE_ROUNDED, "full_name"),
            ft.Container(height=12),
            create_field("Email", "Enter your email", ft.Icons.EMAIL_OUTLINED, "email"),
            ft.Container(height=12),
            create_field("Phone", "Enter phone number", ft.Icons.PHONE_OUTLINED, "phone"),
        ]),
        bgcolor=CARD_BG,
        border_radius=20,
        padding=20,
        margin=ft.margin.symmetric(horizontal=16),
        border=ft.border.all(1, BORDER_COLOR),
    )
    
    # Continue button
    continue_btn = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row([
                ft.Text("Continue", size=16, weight=ft.FontWeight.W_600),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=20),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: TEAL_ACCENT},
                color={ft.ControlState.DEFAULT: TEXT_PRIMARY},
                padding=ft.padding.symmetric(vertical=16),
                shape=ft.RoundedRectangleBorder(radius=14),
            ),
            on_click=handle_continue,
            width=float("inf"),
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
    )
    
    return ft.Container(
        content=ft.Column([
            header,
            ft.Container(
                content=ft.Column([form, continue_btn], spacing=16),
                expand=True,
            ),
        ], spacing=0, expand=True),
        bgcolor=BG_COLOR,
        expand=True,
    )
