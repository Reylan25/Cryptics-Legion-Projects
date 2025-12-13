# src/ui/forgot_password_page.py
import flet as ft
from core import auth
from core.theme import get_theme
from components.notification import ImmersiveNotification


def create_forgot_password_view(page: ft.Page, on_back_to_login, toast):
    """
    Create forgot password view with three stages:
    1. Enter username/email
    2. Enter OTP
    3. Enter new password
    
    Args:
        page: Flet page object
        on_back_to_login: Callback to return to login page
        toast: Toast notification function
    """
    
    # State management
    state = {
        "stage": 1,  # 1: identifier, 2: otp, 3: new_password
        "user_id": None,
        "email": None,
        "identifier": None,
    }
    
    # Stage 1: Enter username or email
    identifier_field = ft.TextField(
        hint_text="Username or Email",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=280,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        cursor_color="white",
        autofocus=True,
    )
    identifier_error = ft.Text("", color="#EF4444", size=11, visible=False)
    
    # Stage 2: Enter OTP
    otp_field = ft.TextField(
        hint_text="Enter 6-digit code",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=280,
        prefix_icon=ft.Icons.PIN_OUTLINED,
        cursor_color="white",
        max_length=6,
        keyboard_type=ft.KeyboardType.NUMBER,
        autofocus=True,
    )
    otp_error = ft.Text("", color="#EF4444", size=11, visible=False)
    
    # Stage 3: Enter new password
    new_password_field = ft.TextField(
        hint_text="Enter new password",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=220,
        password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        cursor_color="white",
        autofocus=True,
    )
    new_password_error = ft.Text("", color="#EF4444", size=11, visible=False)
    
    confirm_password_field = ft.TextField(
        hint_text="Confirm new password",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=220,
        password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        cursor_color="white",
    )
    confirm_password_error = ft.Text("", color="#EF4444", size=11, visible=False)
    
    # Password visibility toggles
    password_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color="white", icon_size=20)
    confirm_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color="white", icon_size=20)
    
    def toggle_password(e):
        new_password_field.password = not new_password_field.password
        password_eye.icon = ft.Icons.VISIBILITY if not new_password_field.password else ft.Icons.VISIBILITY_OFF
        page.update()
    
    def toggle_confirm_password(e):
        confirm_password_field.password = not confirm_password_field.password
        confirm_eye.icon = ft.Icons.VISIBILITY if not confirm_password_field.password else ft.Icons.VISIBILITY_OFF
        page.update()
    
    password_eye.on_click = toggle_password
    confirm_eye.on_click = toggle_confirm_password
    
    # Action button (changes based on stage)
    action_btn = ft.ElevatedButton("Send OTP", width=300, height=50)
    
    # Info text
    info_text = ft.Text(
        "Enter your username or email to receive a password reset code",
        size=13,
        color="#6B7280",
        text_align=ft.TextAlign.CENTER,
    )
    
    # Resend OTP button (only visible in stage 2)
    resend_btn = ft.TextButton(
        "Resend OTP",
        visible=False,
        style=ft.ButtonStyle(color="#3B82F6"),
    )
    
    def clear_errors():
        """Clear all error messages."""
        identifier_error.visible = False
        otp_error.visible = False
        new_password_error.visible = False
        confirm_password_error.visible = False
        page.update()
    
    def handle_stage_1(e=None):
        """Handle stage 1: Request OTP."""
        clear_errors()
        
        identifier = identifier_field.value.strip() if identifier_field.value else ""
        
        if not identifier:
            identifier_error.value = "Please enter your username or email"
            identifier_error.visible = True
            page.update()
            return
        
        # Disable button and show loading
        action_btn.disabled = True
        action_btn.text = "Sending..."
        page.update()
        
        # Request password reset
        success, message, user_info = auth.request_password_reset(identifier)
        
        if success:
            state["stage"] = 2
            state["user_id"] = user_info["user_id"]
            state["email"] = user_info["email"]
            state["identifier"] = identifier
            
            # Show masked email
            email = user_info["email"]
            masked_email = email[0] + "***" + email[email.index("@"):] if "@" in email else "your email"
            
            toast(f"OTP sent to {masked_email}", "#2E7D32")
            render_stage_2()
        else:
            action_btn.disabled = False
            action_btn.text = "Send OTP"
            
            # Provide helpful message if no email is configured
            if "No email" in message:
                identifier_error.value = "⚠️ No email address found for this account."
                identifier_error.visible = True
                
                # Show additional help message
                help_msg = ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "To reset your password, you need an email address on file.",
                            size=12,
                            color="#F59E0B",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Please contact support or use your current password to login and add an email in your profile settings.",
                            size=11,
                            color="#6B7280",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=10,
                    bgcolor="#FEF3C7",
                    border_radius=8,
                    width=300,
                )
                
                # Insert help message after identifier container
                for i, control in enumerate(content.controls):
                    if hasattr(control, 'content') and hasattr(control.content, 'controls'):
                        if len(control.content.controls) > 0 and identifier_field in str(control.content.controls):
                            content.controls.insert(i + 2, help_msg)
                            break
            else:
                identifier_error.value = message
                identifier_error.visible = True
            
            page.update()
    
    def handle_stage_2(e=None):
        """Handle stage 2: Verify OTP."""
        clear_errors()
        
        otp = otp_field.value.strip() if otp_field.value else ""
        
        if not otp:
            otp_error.value = "Please enter the OTP code"
            otp_error.visible = True
            page.update()
            return
        
        if len(otp) != 6:
            otp_error.value = "OTP must be 6 digits"
            otp_error.visible = True
            page.update()
            return
        
        # Disable button and show loading
        action_btn.disabled = True
        action_btn.text = "Verifying..."
        page.update()
        
        # Verify OTP (we'll do full verification in stage 3)
        from core import db
        success, message, otp_id = db.verify_password_reset_otp(state["user_id"], otp)
        
        if success:
            state["stage"] = 3
            state["otp"] = otp
            toast("OTP verified! Set your new password", "#2E7D32")
            render_stage_3()
        else:
            action_btn.disabled = False
            action_btn.text = "Verify OTP"
            otp_error.value = message
            otp_error.visible = True
            page.update()
    
    def handle_stage_3(e=None):
        """Handle stage 3: Reset password."""
        clear_errors()
        
        new_pass = new_password_field.value.strip() if new_password_field.value else ""
        confirm_pass = confirm_password_field.value.strip() if confirm_password_field.value else ""
        
        has_error = False
        
        if not new_pass:
            new_password_error.value = "Please enter a new password"
            new_password_error.visible = True
            has_error = True
        elif len(new_pass) < 4:
            new_password_error.value = "Password must be at least 4 characters"
            new_password_error.visible = True
            has_error = True
        
        if not confirm_pass:
            confirm_password_error.value = "Please confirm your password"
            confirm_password_error.visible = True
            has_error = True
        elif new_pass != confirm_pass:
            confirm_password_error.value = "Passwords do not match"
            confirm_password_error.visible = True
            has_error = True
        
        if has_error:
            page.update()
            return
        
        # Disable button and show loading
        action_btn.disabled = True
        action_btn.text = "Resetting..."
        page.update()
        
        # Reset password
        success, message = auth.verify_otp_and_reset_password(
            state["user_id"], 
            state["otp"], 
            new_pass
        )
        
        if success:
            # Show success message
            action_btn.text = "Success! ✓"
            action_btn.bgcolor = "#10B981"  # Green
            action_btn.disabled = False
            page.update()
            
            # Show immersive success notification
            notif = ImmersiveNotification(page)
            notif.show("Your password has been reset successfully", "success", title="Password Reset! 🔒")
            
            # Small delay using page timer
            import threading
            def redirect_after_delay():
                import time
                time.sleep(1.5)
                on_back_to_login()
            
            threading.Thread(target=redirect_after_delay, daemon=True).start()
        else:
            action_btn.disabled = False
            action_btn.text = "Reset Password"
            new_password_error.value = message
            new_password_error.visible = True
            page.update()
    
    def resend_otp(e):
        """Resend OTP to user."""
        resend_btn.disabled = True
        resend_btn.text = "Sending..."
        page.update()
        
        success, message, user_info = auth.request_password_reset(state["identifier"])
        
        resend_btn.disabled = False
        resend_btn.text = "Resend OTP"
        
        if success:
            toast("New OTP sent!", "#2E7D32")
        else:
            toast(message, "#b71c1c")
        
        page.update()
    
    resend_btn.on_click = resend_otp
    
    # Create back button that will be reused
    back_btn = ft.TextButton(
        "← Back to Login",
        style=ft.ButtonStyle(color="#6B7280"),
    )
    
    def go_back_to_login(e):
        """Handle back to login navigation."""
        on_back_to_login()
    
    back_btn.on_click = go_back_to_login
    
    # Add submit handlers
    identifier_field.on_submit = handle_stage_1
    otp_field.on_submit = handle_stage_2
    new_password_field.on_submit = handle_stage_3
    confirm_password_field.on_submit = handle_stage_3
    
    def render_stage_1():
        """Render stage 1: Enter identifier."""
        theme = get_theme()
        
        # Update back button style
        back_btn.style = ft.ButtonStyle(color=theme.text_secondary)
        
        action_btn.text = "Send OTP"
        action_btn.disabled = False
        action_btn.on_click = handle_stage_1
        
        info_text.value = "Enter your username or email to receive a password reset code"
        resend_btn.visible = False
        
        identifier_cont = ft.Container(
            content=ft.Column([
                ft.Row([identifier_field], expand=True),
                identifier_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )
        
        content.controls = [
            logo,
            title,
            info_text,
            ft.Container(height=20),
            identifier_cont,
            ft.Container(height=20),
            action_btn,
            ft.Container(height=10),
            back_btn,
        ]
        page.update()
    
    def render_stage_2():
        """Render stage 2: Enter OTP."""
        theme = get_theme()
        
        action_btn.text = "Verify OTP"
        action_btn.disabled = False
        action_btn.on_click = handle_stage_2
        
        email = state["email"]
        masked_email = email[0] + "***" + email[email.index("@"):] if "@" in email else "your email"
        info_text.value = f"Enter the 6-digit code sent to {masked_email}"
        resend_btn.visible = True
        
        otp_field.value = ""
        otp_error.visible = False
        
        otp_cont = ft.Container(
            content=ft.Column([
                ft.Row([otp_field], expand=True),
                otp_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )
        
        content.controls = [
            logo,
            title,
            info_text,
            ft.Container(height=20),
            otp_cont,
            ft.Container(height=10),
            resend_btn,
            ft.Container(height=10),
            action_btn,
            ft.Container(height=10),
            back_btn,
        ]
        page.update()
    
    def render_stage_3():
        """Render stage 3: Enter new password."""
        theme = get_theme()
        
        action_btn.text = "Reset Password"
        action_btn.disabled = False
        action_btn.on_click = handle_stage_3
        
        info_text.value = "Enter your new password"
        resend_btn.visible = False
        
        new_password_field.value = ""
        confirm_password_field.value = ""
        new_password_error.visible = False
        confirm_password_error.visible = False
        
        new_password_cont = ft.Container(
            content=ft.Column([
                ft.Row([new_password_field, password_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                new_password_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )
        
        confirm_password_cont = ft.Container(
            content=ft.Column([
                ft.Row([confirm_password_field, confirm_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                confirm_password_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )
        
        content.controls = [
            logo,
            title,
            info_text,
            ft.Container(height=20),
            new_password_cont,
            ft.Container(height=15),
            confirm_password_cont,
            ft.Container(height=20),
            action_btn,
            ft.Container(height=10),
            back_btn,
        ]
        page.update()
    
    def show_view():
        """Initialize and show the forgot password view."""
        page.clean()
        
        theme = get_theme()
        
        # Reset state
        state["stage"] = 1
        state["user_id"] = None
        state["email"] = None
        state["identifier"] = None
        
        # Reset fields
        identifier_field.value = ""
        otp_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        clear_errors()
        
        # Update colors
        identifier_field.color = theme.text_primary
        otp_field.color = theme.text_primary
        new_password_field.color = theme.text_primary
        confirm_password_field.color = theme.text_primary
        
        nonlocal logo, title, content
        
        logo = ft.Container(
            content=ft.Icon(ft.Icons.LOCK_RESET, color=theme.accent_secondary, size=50),
            width=80,
            height=80,
            border_radius=40,
            bgcolor=theme.bg_card,
            alignment=ft.alignment.center,
        )
        
        title = ft.Text(
            "Reset Password",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=theme.text_primary,
        )
        
        action_btn.bgcolor = theme.accent_primary
        action_btn.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        
        # Update back button style for current theme
        back_btn.style = ft.ButtonStyle(color=theme.text_secondary)
        
        content = ft.Column(
            controls=[],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        page.add(
            ft.Container(
                content=content,
                alignment=ft.alignment.center,
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[theme.bg_primary, theme.bg_secondary],
                ),
            )
        )
        
        render_stage_1()
    
    # Initialize variables that need to be in outer scope
    logo = None
    title = None
    content = None
    
    return show_view
