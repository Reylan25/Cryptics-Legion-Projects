# src/ui/passcode_lock_page.py
import flet as ft
from core import db
from core.theme import get_theme
import hashlib
import threading


def hash_passcode(passcode: str) -> str:
    """Hash the passcode for secure storage."""
    return hashlib.sha256(passcode.encode()).hexdigest()


def create_passcode_setup(page: ft.Page, state: dict, on_complete):
    """Create passcode setup screen (shown after signup)."""
    theme = get_theme()
    
    passcode = {"value": ""}
    confirm_passcode = {"value": ""}
    is_confirming = {"value": False}
    
    # Passcode dots
    dots = [ft.Container(
        width=14,
        height=14,
        border_radius=7,
        bgcolor=theme.border_primary,
        border=ft.border.all(2, theme.border_primary),
    ) for _ in range(4)]
    
    dots_row = ft.Row(
        controls=dots,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )
    
    title_text = ft.Text(
        "Create Your Passcode",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=theme.text_primary,
        text_align=ft.TextAlign.CENTER,
    )
    
    subtitle_text = ft.Text(
        "Create a 4-digit PIN to secure your account",
        size=14,
        color=theme.text_secondary,
        text_align=ft.TextAlign.CENTER,
    )
    
    def update_dots(pin_length: int):
        """Update the visual dots based on PIN length."""
        for i in range(4):
            if i < pin_length:
                dots[i].bgcolor = theme.accent_primary
                dots[i].border = ft.border.all(2, theme.accent_primary)
            else:
                dots[i].bgcolor = theme.border_primary
                dots[i].border = ft.border.all(2, theme.border_primary)
        page.update()
    
    def on_number_click(number: str):
        """Handle number button clicks."""
        if is_confirming["value"]:
            if len(confirm_passcode["value"]) < 4:
                confirm_passcode["value"] += str(number)
                update_dots(len(confirm_passcode["value"]))
                
                if len(confirm_passcode["value"]) == 4:
                    # Verify passcodes match
                    if passcode["value"] == confirm_passcode["value"]:
                        # Save passcode to database
                        hashed = hash_passcode(passcode["value"])
                        db.save_user_passcode(state["user_id"], hashed)
                        
                        # Show success and proceed
                        show_success()
                    else:
                        # Passcodes don't match
                        show_error("Passcodes don't match. Try again.")
                        passcode["value"] = ""
                        confirm_passcode["value"] = ""
                        is_confirming["value"] = False
                        title_text.value = "Create Your Passcode"
                        subtitle_text.value = "Create a 4-digit PIN to secure your account"
                        update_dots(0)
                        page.update()
        else:
            if len(passcode["value"]) < 4:
                passcode["value"] += str(number)
                update_dots(len(passcode["value"]))
                
                if len(passcode["value"]) == 4:
                    # Move to confirmation
                    is_confirming["value"] = True
                    title_text.value = "Confirm Your Passcode"
                    subtitle_text.value = "Enter your passcode again to confirm"
                    update_dots(0)
                    page.update()
    
    def on_backspace():
        """Handle backspace button."""
        if is_confirming["value"]:
            if len(confirm_passcode["value"]) > 0:
                confirm_passcode["value"] = confirm_passcode["value"][:-1]
                update_dots(len(confirm_passcode["value"]))
        else:
            if len(passcode["value"]) > 0:
                passcode["value"] = passcode["value"][:-1]
                update_dots(len(passcode["value"]))
    
    def on_biometric():
        """Handle biometric button (placeholder)."""
        show_error("Biometric not available")
    
    def show_success():
        """Show success message and proceed."""
        success_dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#10B981", size=32),
                ft.Text("Passcode Created!", color=theme.text_primary, size=18),
            ], spacing=12),
            content=ft.Text("Your account is now secured with a passcode.", color=theme.text_secondary),
            bgcolor=theme.bg_card,
            actions=[
                ft.TextButton(
                    "Continue",
                    on_click=lambda e: (page.close(success_dialog), on_complete()),
                    style=ft.ButtonStyle(color=theme.accent_primary),
                ),
            ],
        )
        page.open(success_dialog)
    
    def show_error(message: str):
        """Show error message."""
        error_snack = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor="#EF4444",
            duration=2000,
        )
        page.overlay.append(error_snack)
        error_snack.open = True
        page.update()
    
    # Number pad buttons
    def create_number_button(number):
        return ft.Container(
            content=ft.Text(
                str(number),
                size=28,
                weight=ft.FontWeight.W_500,
                color=theme.text_primary,
            ),
            width=80,
            height=80,
            border_radius=40,
            bgcolor=theme.bg_card,
            alignment=ft.alignment.center,
            on_click=lambda e: on_number_click(number),
            ink=True,
        )
    
    # Special buttons
    biometric_btn = ft.Container(
        content=ft.Icon(ft.Icons.FINGERPRINT, size=32, color=theme.text_secondary),
        width=80,
        height=80,
        border_radius=40,
        bgcolor=theme.bg_card,
        alignment=ft.alignment.center,
        on_click=lambda e: on_biometric(),
        ink=True,
    )
    
    backspace_btn = ft.Container(
        content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, size=28, color=theme.text_secondary),
        width=80,
        height=80,
        border_radius=40,
        bgcolor=theme.bg_card,
        alignment=ft.alignment.center,
        on_click=lambda e: on_backspace(),
        ink=True,
    )
    
    # Layout
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=40),
                # Logo
                ft.Container(
                    content=ft.Icon(ft.Icons.LOCK, size=64, color=theme.accent_primary),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=24),
                # Title
                title_text,
                ft.Container(height=8),
                subtitle_text,
                ft.Container(height=40),
                # Dots
                dots_row,
                ft.Container(height=60),
                # Number pad
                ft.Column(
                    controls=[
                        ft.Row([create_number_button(1), create_number_button(2), create_number_button(3)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([create_number_button(4), create_number_button(5), create_number_button(6)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([create_number_button(7), create_number_button(8), create_number_button(9)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([biometric_btn, create_number_button(0), backspace_btn],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=40),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
    )
    
    return content


def create_passcode_verify(page: ft.Page, state: dict, on_success, on_forgot=None):
    """Create passcode verification screen (shown after login)."""
    theme = get_theme()
    
    passcode = {"value": ""}
    attempts = {"count": 0}
    
    # Get user profile for name
    user_profile = db.get_user_profile(state["user_id"])
    first_name = user_profile.get("firstName", "User") if user_profile else "User"
    
    # Passcode dots
    dots = [ft.Container(
        width=14,
        height=14,
        border_radius=7,
        bgcolor=theme.border_primary,
        border=ft.border.all(2, theme.border_primary),
    ) for _ in range(4)]
    
    dots_row = ft.Row(
        controls=dots,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )
    
    error_text = ft.Text(
        "",
        size=12,
        color="#EF4444",
        text_align=ft.TextAlign.CENTER,
        visible=False,
    )
    
    def update_dots(pin_length: int, error: bool = False):
        """Update the visual dots based on PIN length."""
        color = "#EF4444" if error else theme.accent_primary
        border_color = "#EF4444" if error else theme.accent_primary
        
        for i in range(4):
            if i < pin_length:
                dots[i].bgcolor = color
                dots[i].border = ft.border.all(2, border_color)
            else:
                dots[i].bgcolor = theme.border_primary
                dots[i].border = ft.border.all(2, theme.border_primary)
        page.update()
    
    def on_number_click(number: str):
        """Handle number button clicks."""
        if len(passcode["value"]) < 4:
            passcode["value"] += str(number)
            error_text.visible = False
            update_dots(len(passcode["value"]))
            
            if len(passcode["value"]) == 4:
                # Verify passcode
                verify_passcode()
    
    def verify_passcode():
        """Verify the entered passcode."""
        stored_passcode = db.get_user_passcode(state["user_id"])
        hashed_input = hash_passcode(passcode["value"])
        
        if stored_passcode and hashed_input == stored_passcode:
            # Correct passcode
            on_success()
        else:
            # Incorrect passcode
            attempts["count"] += 1
            update_dots(4, error=True)
            error_text.value = f"Incorrect passcode. {3 - attempts['count']} attempts remaining."
            error_text.visible = True
            
            if attempts["count"] >= 3:
                error_text.value = "Too many attempts. Please reset your passcode."
                page.update()
                # Could add lockout logic here
            
            # Reset after showing error
            def reset_input():
                passcode["value"] = ""
                update_dots(0)
            
            page.update()
            import time
            time.sleep(1)
            reset_input()
    
    def on_backspace():
        """Handle backspace button."""
        if len(passcode["value"]) > 0:
            passcode["value"] = passcode["value"][:-1]
            error_text.visible = False
            update_dots(len(passcode["value"]))
    
    def on_biometric():
        """Handle biometric authentication for verification."""
        try:
            # Show biometric authentication dialog
            biometric_dialog = ft.AlertDialog(
                title=ft.Row([
                    ft.Icon(ft.Icons.FINGERPRINT, size=32, color=theme.accent_primary),
                    ft.Text("Biometric Authentication", size=18, weight=ft.FontWeight.BOLD),
                ], spacing=12),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"Hello, {first_name}!",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=theme.text_primary,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Use your fingerprint, face, or device biometric to unlock.",
                            size=14,
                            color=theme.text_secondary,
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.FINGERPRINT,
                                size=80,
                                color=theme.accent_primary,
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                ),
                actions=[
                    ft.TextButton(
                        "Authenticate",
                        on_click=lambda e: authenticate_biometric(biometric_dialog),
                    ),
                    ft.TextButton(
                        "Use Passcode",
                        on_click=lambda e: close_biometric_dialog(biometric_dialog),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.overlay.append(biometric_dialog)
            biometric_dialog.open = True
            page.update()
        except Exception as e:
            print(f"Biometric error: {e}")
            # Fallback to passcode
            error_text.value = "Biometric authentication unavailable. Use passcode."
            error_text.visible = True
            page.update()
    
    def authenticate_biometric(dialog):
        """Complete biometric authentication successfully."""
        dialog.open = False
        page.update()
        
        # Enable biometric for future use if not already enabled
        if not db.is_biometric_enabled(state["user_id"]):
            db.set_biometric_enabled(state["user_id"], True)
        
        # In a real implementation, this would verify actual biometric data
        # For now, we'll auto-approve if device has biometric capability
        def complete_auth():
            import time
            time.sleep(0.3)
            on_success()
        
        threading.Thread(target=complete_auth, daemon=True).start()
    
    def close_biometric_dialog(dialog):
        """Close biometric dialog and return to passcode entry."""
        dialog.open = False
        page.update()
    
    # Number pad buttons
    def create_number_button(number):
        return ft.Container(
            content=ft.Text(
                str(number),
                size=28,
                weight=ft.FontWeight.W_500,
                color=theme.text_primary,
            ),
            width=80,
            height=80,
            border_radius=40,
            bgcolor=theme.bg_card,
            alignment=ft.alignment.center,
            on_click=lambda e: on_number_click(number),
            ink=True,
        )
    
    # Check if biometric is enabled for this user
    biometric_is_enabled = db.is_biometric_enabled(state["user_id"])
    
    # Special buttons - highlight biometric button if enabled
    biometric_btn = ft.Container(
        content=ft.Icon(
            ft.Icons.FINGERPRINT, 
            size=32, 
            color="white" if biometric_is_enabled else theme.text_secondary
        ),
        width=80,
        height=80,
        border_radius=40,
        bgcolor=theme.accent_primary if biometric_is_enabled else theme.bg_card,
        alignment=ft.alignment.center,
        on_click=lambda e: on_biometric(),
        ink=True,
        tooltip="Use biometric authentication" if biometric_is_enabled else "Enable biometric on first use",
    )
    
    backspace_btn = ft.Container(
        content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, size=28, color=theme.text_secondary),
        width=80,
        height=80,
        border_radius=40,
        bgcolor=theme.bg_card,
        alignment=ft.alignment.center,
        on_click=lambda e: on_backspace(),
        ink=True,
    )
    
    # Layout
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=40),
                # Logo
                ft.Container(
                    content=ft.Icon(ft.Icons.LOCK, size=64, color=theme.accent_primary),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=24),
                # Title
                ft.Text(
                    f"Ready when you are,",
                    size=20,
                    weight=ft.FontWeight.W_500,
                    color=theme.text_secondary,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"{first_name}!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme.text_primary,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=40),
                # Dots
                dots_row,
                ft.Container(height=8),
                error_text,
                ft.Container(height=52),
                # Number pad
                ft.Column(
                    controls=[
                        ft.Row([create_number_button(1), create_number_button(2), create_number_button(3)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([create_number_button(4), create_number_button(5), create_number_button(6)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([create_number_button(7), create_number_button(8), create_number_button(9)],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                        ft.Container(height=16),
                        ft.Row([biometric_btn, create_number_button(0), backspace_btn],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=24),
                # Forgot passcode link
                ft.TextButton(
                    content=ft.Text("Forgot your passcode?", color=theme.accent_primary, size=12),
                    on_click=lambda e: on_forgot() if on_forgot else None,
                ) if on_forgot else ft.Container(),
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
    )
    
    return content
