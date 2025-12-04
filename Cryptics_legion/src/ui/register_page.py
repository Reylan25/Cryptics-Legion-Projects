# src/ui/register_page.py
import flet as ft
import re
from core.theme import get_theme


def create_register_view(page: ft.Page, on_registered, show_login, toast, state=None):
    """
    on_registered(password) -> called after successful password creation with password
    show_login() -> callable to show login
    toast(message, color) -> helper
    state -> optional dict to retain password when navigating back
    """
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Colors for validation
        VALID_COLOR = "#10B981"  # Green
        INVALID_COLOR = theme.text_muted
        
        # Password validation state
        validation_state = {
            "length": False,
            "uppercase": False,
            "lowercase": False,
            "number": False,
            "no_special": True,
            "no_spaces": True,
        }
        
        # Create validation indicator rows
        def create_validation_row(text: str, is_valid: bool):
            return ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if is_valid else ft.Icons.RADIO_BUTTON_UNCHECKED,
                        size=16,
                        color=VALID_COLOR if is_valid else INVALID_COLOR,
                    ),
                    ft.Text(
                        text,
                        size=12,
                        color=VALID_COLOR if is_valid else INVALID_COLOR,
                    ),
                ],
                spacing=8,
            )
        
        # Validation indicator controls
        length_check = create_validation_row("8-20 characters", False)
        uppercase_check = create_validation_row("At least one capital letter (A to Z)", False)
        lowercase_check = create_validation_row("At least one lowercase letter (a to z)", False)
        number_check = create_validation_row("At least one number (0 to 9)", False)
        special_check = create_validation_row("Don't use : ; , \" ' / \\", True)
        spaces_check = create_validation_row("No spaces", True)
        
        # Validation container
        validation_container = ft.Container(
            content=ft.Column(
                controls=[
                    length_check,
                    uppercase_check,
                    lowercase_check,
                    number_check,
                    special_check,
                    spaces_check,
                ],
                spacing=6,
            ),
            padding=ft.padding.only(left=10, top=8, bottom=8),
            visible=False,  # Hidden initially
        )
        
        # Password strength indicator
        strength_text = ft.Text("", size=12, weight=ft.FontWeight.W_500)
        strength_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(width=60, height=4, bgcolor=theme.text_muted, border_radius=2),
                    ft.Container(width=60, height=4, bgcolor=theme.text_muted, border_radius=2),
                    ft.Container(width=60, height=4, bgcolor=theme.text_muted, border_radius=2),
                    ft.Container(width=60, height=4, bgcolor=theme.text_muted, border_radius=2),
                ],
                spacing=4,
            ),
            visible=False,
        )
        
        def update_validation_icon(row: ft.Row, is_valid: bool):
            """Update a validation row's icon and color."""
            row.controls[0].name = ft.Icons.CHECK_CIRCLE if is_valid else ft.Icons.RADIO_BUTTON_UNCHECKED
            row.controls[0].color = VALID_COLOR if is_valid else INVALID_COLOR
            row.controls[1].color = VALID_COLOR if is_valid else INVALID_COLOR
        
        def validate_password(password: str):
            """Validate password and update indicators."""
            if not password:
                validation_container.visible = False
                strength_bar.visible = False
                strength_text.value = ""
                return False
            
            validation_container.visible = True
            strength_bar.visible = True
            
            # Check each validation rule
            validation_state["length"] = 8 <= len(password) <= 20
            validation_state["uppercase"] = bool(re.search(r'[A-Z]', password))
            validation_state["lowercase"] = bool(re.search(r'[a-z]', password))
            validation_state["number"] = bool(re.search(r'[0-9]', password))
            validation_state["no_special"] = not bool(re.search(r'[:;,"\'/\\]', password))
            validation_state["no_spaces"] = ' ' not in password
            
            # Update icons
            update_validation_icon(length_check, validation_state["length"])
            update_validation_icon(uppercase_check, validation_state["uppercase"])
            update_validation_icon(lowercase_check, validation_state["lowercase"])
            update_validation_icon(number_check, validation_state["number"])
            update_validation_icon(special_check, validation_state["no_special"])
            update_validation_icon(spaces_check, validation_state["no_spaces"])
            
            # Calculate strength score
            valid_count = sum([
                validation_state["length"],
                validation_state["uppercase"],
                validation_state["lowercase"],
                validation_state["number"],
            ])
            
            # Check if invalid characters are used
            has_invalid = not validation_state["no_special"] or not validation_state["no_spaces"]
            
            # Update strength bar
            bars = strength_bar.content.controls
            colors = {
                0: (theme.text_muted, theme.text_muted, theme.text_muted, theme.text_muted),
                1: ("#EF4444", theme.text_muted, theme.text_muted, theme.text_muted),  # Red - Weak
                2: ("#F59E0B", "#F59E0B", theme.text_muted, theme.text_muted),  # Orange - Fair
                3: ("#10B981", "#10B981", "#10B981", theme.text_muted),  # Green - Good
                4: ("#10B981", "#10B981", "#10B981", "#10B981"),  # Green - Strong
            }
            
            strength_colors = colors.get(valid_count, colors[0])
            for i, bar in enumerate(bars):
                bar.bgcolor = strength_colors[i]
            
            # Update strength text
            strength_labels = {
                0: ("", theme.text_muted),
                1: ("Weak", "#EF4444"),
                2: ("Fair", "#F59E0B"),
                3: ("Good", "#10B981"),
                4: ("Strong", "#10B981"),
            }
            
            if has_invalid:
                strength_text.value = "Invalid characters"
                strength_text.color = "#EF4444"
            else:
                label, color = strength_labels.get(valid_count, ("", theme.text_muted))
                strength_text.value = label
                strength_text.color = color
            
            # Return True if all validations pass
            return all(validation_state.values())
        
        def on_password_change(e):
            """Handle password input change."""
            validate_password(e.control.value or "")
            page.update()
        
        new_pass = ft.TextField(
            hint_text="Create Password", 
            width=220, 
            border="none", 
            password=True, 
            color=theme.text_primary,
            prefix_icon=ft.Icons.LOCK_OUTLINE, 
            hint_style=ft.TextStyle(color=theme.text_muted),
            on_change=on_password_change,
            value=state.get("temp_password", "") if state else "",
        )
        new_pass_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color=theme.text_primary)
        
        confirm_pass = ft.TextField(
            hint_text="Confirm Password", 
            width=220, 
            border="none", 
            password=True, 
            color=theme.text_primary,
            prefix_icon=ft.Icons.LOCK_OUTLINE, 
            hint_style=ft.TextStyle(color=theme.text_muted),
            value=state.get("temp_password", "") if state else "",
        )
        confirm_pass_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color=theme.text_primary)

        def toggle_new_pwd(e):
            new_pass.password = not new_pass.password
            new_pass_eye.icon = ft.Icons.VISIBILITY if not new_pass.password else ft.Icons.VISIBILITY_OFF
            page.update()

        def toggle_confirm(e):
            confirm_pass.password = not confirm_pass.password
            confirm_pass_eye.icon = ft.Icons.VISIBILITY if not confirm_pass.password else ft.Icons.VISIBILITY_OFF
            page.update()

        new_pass_eye.on_click = toggle_new_pwd
        confirm_pass_eye.on_click = toggle_confirm

        pass_cont = ft.Container(
            content=ft.Row([new_pass, new_pass_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)), 
            padding=ft.padding.only(bottom=6), 
            width=300
        )
        confirm_cont = ft.Container(
            content=ft.Row([confirm_pass, confirm_pass_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)), 
            padding=ft.padding.only(bottom=6), 
            width=300
        )

        def do_continue_click(e):
            p = new_pass.value if new_pass.value else ""
            c = confirm_pass.value if confirm_pass.value else ""
            
            # Validate password
            if not p:
                toast("Password is required", "#b71c1c")
                return
            
            # Check all password validations
            if not validate_password(p):
                toast("Please meet all password requirements", "#b71c1c")
                page.update()
                return
            
            # Check password match
            if p != c:
                toast("Passwords do not match", "#b71c1c")
                return
            
            # Pass the password to the next step (personal details)
            if on_registered:
                on_registered(p)

        # Create continue button
        continue_btn = ft.Container(
            content=ft.Text("Continue", size=16, weight=ft.FontWeight.W_600, color="white"),
            width=300,
            height=48,
            bgcolor=theme.accent_primary,
            border_radius=12,
            alignment=ft.alignment.center,
            on_click=do_continue_click,
            ink=True,
        )

        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center, 
                    end=ft.alignment.bottom_center, 
                    colors=[theme.bg_gradient_start, theme.bg_primary]
                ),
                content=ft.Column([
                    ft.Container(height=60),
                    ft.Text("Create Account", size=26, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Text("Set up your secure password", size=14, color=theme.text_secondary),
                    ft.Container(height=30),
                    pass_cont,
                    # Strength bar and text
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                strength_bar,
                                strength_text,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        width=300,
                        padding=ft.padding.only(top=8),
                    ),
                    # Validation checklist
                    ft.Container(
                        content=validation_container,
                        width=300,
                    ),
                    ft.Container(height=16),
                    confirm_cont,
                    ft.Container(height=30),
                    continue_btn,
                    ft.Container(height=16),
                    ft.TextButton(
                        "Back to Login", 
                        on_click=lambda e: show_login(), 
                        style=ft.ButtonStyle(color=theme.accent_secondary)
                    ),
                    ft.Container(height=40),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
                alignment=ft.alignment.center,
                padding=20
            )
        )
        
        # If password was restored from state, trigger validation
        if state and state.get("temp_password"):
            validate_password(state.get("temp_password", ""))
        
        page.update()

    return show_view
