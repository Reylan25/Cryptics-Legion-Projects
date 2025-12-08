# src/ui/login_page.py
import flet as ft
from core import auth
from core import admin_auth
from core.theme import get_theme
from components.notification import ImmersiveNotification


def create_login_view(page: ft.Page, on_success, show_register, show_onboarding, toast, show_forgot_password=None):
    """
    Returns a callable that will render the login view when called.
    on_success(user_id) -> called when login succeeds.
    show_register() -> callable to show register page
    show_onboarding() -> callable to show onboarding
    toast(message, color) -> helper to show snackbars
    show_forgot_password() -> callable to show forgot password page
    """
    
    # Error message text with icon container
    error_icon = ft.Icon(ft.Icons.ERROR_OUTLINE, color="#EF4444", size=16, visible=False)
    error_text = ft.Text("", color="#EF4444", size=12, visible=False)
    
    # Loading state
    loading = {"value": False}
    
    username_field = ft.TextField(
        hint_text="Enter your username",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=280,
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        cursor_color="white",
    )
    
    username_error = ft.Text("", color="#EF4444", size=11, visible=False)

    password_field = ft.TextField(
        hint_text="Enter your password",
        hint_style=ft.TextStyle(color="#6B7280"),
        border="none",
        color="white",
        width=220,
        password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        cursor_color="white",
    )
    
    password_error = ft.Text("", color="#EF4444", size=11, visible=False)

    password_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color="white", icon_size=20)

    def toggle_password(e):
        password_field.password = not password_field.password
        password_eye.icon = ft.Icons.VISIBILITY if not password_field.password else ft.Icons.VISIBILITY_OFF
        page.update()

    password_eye.on_click = toggle_password
    
    def clear_errors():
        """Clear all error messages."""
        username_error.visible = False
        password_error.visible = False
        error_text.visible = False
        error_icon.visible = False
        page.update()
    
    def show_error(message):
        """Show main error message."""
        error_text.value = message
        error_text.visible = True
        error_icon.visible = True
        page.update()

    def do_login(e=None):
        # Clear previous errors
        clear_errors()
        
        u = username_field.value.strip() if username_field.value else ""
        p = password_field.value.strip() if password_field.value else ""
        
        has_error = False
        
        # Validate username
        if not u:
            username_error.value = "Username is required"
            username_error.visible = True
            has_error = True
        elif len(u) < 3:
            username_error.value = "Username must be at least 3 characters"
            username_error.visible = True
            has_error = True
        
        # Validate password
        if not p:
            password_error.value = "Password is required"
            password_error.visible = True
            has_error = True
        elif len(p) < 4:
            password_error.value = "Password must be at least 4 characters"
            password_error.visible = True
            has_error = True
        
        if has_error:
            page.update()
            return
        
        # Show loading state
        login_btn.disabled = True
        login_btn.text = "Logging in..."
        page.update()
        
        # Check if this is an admin user first
        if admin_auth.is_admin_username(u):
            print(f"Admin username detected: {u}")
            success, admin_data = admin_auth.login_admin(u, p)
            print(f"Admin login result: {success}, data: {admin_data}")
            
            if success:
                username_field.value = ""
                password_field.value = ""
                login_btn.disabled = False
                login_btn.text = "Login"
                
                # Show immersive welcome notification
                notif = ImmersiveNotification(page)
                notif.show(f"Welcome back, Administrator! System access granted", "success", title="Admin Login Successful! 🔐")
                
                # Call success with admin data (special flag for admin)
                on_success(admin_data["id"], is_admin=True, admin_data=admin_data)
                return
            else:
                # Admin login failed
                login_btn.disabled = False
                login_btn.text = "Login"
                show_error("Invalid admin credentials. Please try again.")
                
                # Show error notification
                notif = ImmersiveNotification(page)
                notif.show("Please check your admin password", "error", title="Login Failed")
                return
        
        # Attempt regular user login
        uid = auth.login_user(u, p)
        
        if uid:
            username_field.value = ""
            password_field.value = ""
            login_btn.disabled = False
            login_btn.text = "Login"
            
            # Show immersive welcome notification
            notif = ImmersiveNotification(page)
            notif.show(f"Welcome back! You're successfully logged in", "success", title="Login Successful! 🎉")
            
            on_success(uid)
        else:
            login_btn.disabled = False
            login_btn.text = "Login"
            show_error("Invalid username or password. Please try again.")
            
            # Show error notification
            notif = ImmersiveNotification(page)
            notif.show("Please check your username and password", "error", title="Login Failed")

    # Add on_submit handlers for Enter key to trigger login
    username_field.on_submit = do_login
    password_field.on_submit = do_login

    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Reset fields
        username_field.value = ""
        password_field.value = ""
        username_error.visible = False
        password_error.visible = False
        error_text.visible = False
        error_icon.visible = False
        
        # Update field colors based on theme
        username_field.color = theme.text_primary
        username_field.hint_style = ft.TextStyle(color=theme.text_muted)
        password_field.color = theme.text_primary
        password_field.hint_style = ft.TextStyle(color=theme.text_muted)
        password_eye.icon_color = theme.text_primary
        
        # App logo/icon
        logo = ft.Container(
            content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color=theme.accent_secondary, size=50),
            width=80,
            height=80,
            border_radius=40,
            bgcolor=theme.bg_card,
            alignment=ft.alignment.center,
        )
        
        username_cont = ft.Container(
            content=ft.Column([
                ft.Row([username_field], expand=True),
                username_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )
        
        password_cont = ft.Container(
            content=ft.Column([
                ft.Row([password_field, password_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                password_error,
            ], spacing=4),
            border=ft.Border(bottom=ft.BorderSide(1, theme.border_primary)),
            padding=ft.padding.only(bottom=6),
            width=300
        )

        # Styled login button
        nonlocal login_btn
        login_btn = ft.ElevatedButton(
            "Login",
            width=300, 
            height=50, 
            bgcolor=theme.accent_primary, 
            color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=do_login
        )
        
        # Forgot password link
        forgot_password = ft.TextButton(
            "Forgot Password?",
            style=ft.ButtonStyle(color=theme.text_secondary),
            on_click=lambda e: show_forgot_password() if show_forgot_password else toast("Password reset feature coming soon!", theme.accent_primary),
        )

        page.add(
            ft.Container(
                expand=True,
                gradient=ft.RadialGradient(
                    center=ft.alignment.center,
                    radius=0.8,
                    colors=[theme.bg_gradient_start, theme.bg_primary, theme.bg_gradient_end]
                ),
                padding=20,
                content=ft.Column([
                    ft.Container(height=30),
                    logo,
                    ft.Container(height=15),
                    ft.Text("Welcome Back!", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(height=4),
                    ft.Text("Sign in to continue tracking your expenses", size=13, color=theme.text_secondary),
                    ft.Container(height=25),
                    
                    # Error message container
                    ft.Container(
                        content=ft.Row([
                            error_icon,
                            error_text,
                        ], spacing=8),
                        padding=ft.padding.only(bottom=10),
                    ),
                    
                    username_cont,
                    ft.Container(height=12),
                    password_cont,
                    ft.Container(height=8),
                    
                    # Forgot password aligned right
                    ft.Container(
                        content=forgot_password,
                        width=300,
                        alignment=ft.alignment.center_right,
                    ),
                    
                    ft.Container(height=18),
                    login_btn,
                    ft.Container(height=18),
                    
                    # Divider with "or"
                    ft.Row([
                        ft.Container(height=1, width=100, bgcolor=theme.border_primary),
                        ft.Text("  or  ", color=theme.text_muted, size=12),
                        ft.Container(height=1, width=100, bgcolor=theme.border_primary),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Container(height=18),
                    
                    # Sign up link
                    ft.Row([
                        ft.Text("Don't have an account?", color=theme.text_secondary, size=14),
                        ft.TextButton(
                            "Sign Up", 
                            on_click=lambda e: show_register(), 
                            style=ft.ButtonStyle(color=theme.accent_secondary)
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.top_center
            )
        )
        page.update()
    
    # Initialize login_btn
    login_btn = None

    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_login_content(page: ft.Page, on_success, show_register, show_onboarding, toast, show_forgot_password=None):
    """
    Builds and returns login page content WITHOUT calling page.clean() or page.add().
    """
    from core import db
    theme = get_theme()
    
    # Error message text
    error_icon = ft.Icon(ft.Icons.ERROR_OUTLINE, color="#EF4444", size=16, visible=False)
    error_text = ft.Text("", color="#EF4444", size=12, visible=False)
    
    username_field = ft.TextField(
        hint_text="Username",
        hint_style=ft.TextStyle(color=theme.text_muted, size=16),
        border=ft.InputBorder.NONE,
        color=theme.text_primary,
        text_size=16,
        expand=True,
        cursor_color=theme.text_primary,
        content_padding=ft.padding.symmetric(vertical=12),
    )
    
    password_field = ft.TextField(
        hint_text="Password",
        hint_style=ft.TextStyle(color=theme.text_muted, size=16),
        border=ft.InputBorder.NONE,
        color=theme.text_primary,
        text_size=16,
        expand=True,
        password=True,
        cursor_color=theme.text_primary,
        content_padding=ft.padding.symmetric(vertical=12),
    )
    
    password_eye = ft.IconButton(
        icon=ft.Icons.VISIBILITY_OFF,
        icon_color=theme.text_muted,
        icon_size=20,
        style=ft.ButtonStyle(padding=0),
    )
    
    def toggle_password(e):
        password_field.password = not password_field.password
        password_eye.icon = ft.Icons.VISIBILITY if not password_field.password else ft.Icons.VISIBILITY_OFF
        page.update()
    
    password_eye.on_click = toggle_password
    
    def do_login(e):
        user = username_field.value.strip() if username_field.value else ""
        pwd = password_field.value.strip() if password_field.value else ""
        
        if not user or not pwd:
            error_icon.visible = True
            error_text.visible = True
            error_text.value = "Please enter username and password"
            page.update()
            return
        
        # Check if this is an admin user first
        if admin_auth.is_admin_username(user):
            print(f"DEBUG: Admin username detected: {user}")
            success, admin_data = admin_auth.login_admin(user, pwd)
            print(f"DEBUG: Admin login result: {success}, data: {admin_data}")
            
            if success:
                print("DEBUG: Calling on_success with admin data")
                on_success(admin_data["id"], is_admin=True, admin_data=admin_data)
                return
            else:
                error_icon.visible = True
                error_text.visible = True
                error_text.value = "Invalid admin credentials"
                page.update()
                return
        
        # Regular user login
        user_id = auth.login_user(user, pwd)
        if user_id:
            on_success(user_id)
        else:
            error_icon.visible = True
            error_text.visible = True
            error_text.value = "Invalid credentials"
            page.update()
    
    # Logo
    logo = ft.Container(
        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=60, color=theme.accent_primary),
        width=100,
        height=100,
        bgcolor=theme.bg_card,
        border_radius=20,
        alignment=ft.alignment.center,
    )
    
    # Get recent usernames
    recent_usernames = db.get_recent_usernames(3)
    
    def select_username(username):
        def handler(e):
            username_field.value = username
            recent_users_container.visible = False
            page.update()
        return handler
    
    # Build recent usernames row (hidden by default)
    recent_users_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON, color=theme.accent_secondary, size=14),
                    ft.Text(uname, size=12, color=theme.text_primary),
                ], spacing=4),
                bgcolor=theme.bg_card,
                border_radius=15,
                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                on_click=select_username(uname),
                ink=True,
            )
            for uname in recent_usernames
        ],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    ) if recent_usernames else ft.Container()
    
    # Container for recent users (hidden by default, shown on focus)
    recent_users_container = ft.Container(
        content=recent_users_row,
        width=300,
        padding=ft.padding.only(top=8, bottom=4),
        visible=False,
    ) if recent_usernames else ft.Container()
    
    def on_username_focus(e):
        if recent_usernames:
            recent_users_container.visible = True
            page.update()
    
    def on_username_blur(e):
        # Small delay to allow click on username chip before hiding
        import time
        def hide_after_delay():
            time.sleep(0.2)
            if hasattr(recent_users_container, 'visible'):
                recent_users_container.visible = False
                page.update()
        import threading
        threading.Thread(target=hide_after_delay, daemon=True).start()
    
    username_field.on_focus = on_username_focus
    
    # Username field with icon and underline
    username_cont = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.PERSON_OUTLINE, color=theme.accent_secondary, size=22),
                ft.Container(width=12),
                username_field,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], spacing=0),
        width=300,
        border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary)),
        padding=ft.padding.only(bottom=8),
    )
    
    # Password field with icon, eye toggle, and underline
    password_cont = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LOCK_OUTLINE, color=theme.accent_secondary, size=22),
                ft.Container(width=12),
                password_field,
                password_eye,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], spacing=0),
        width=300,
        border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary)),
        padding=ft.padding.only(bottom=8),
    )
    
    login_btn = ft.Container(
        content=ft.Text("Sign In", color="white", weight=ft.FontWeight.BOLD, size=16),
        width=300,
        height=55,
        bgcolor=theme.accent_primary,
        border_radius=12,
        alignment=ft.alignment.center,
        on_click=do_login,
        ink=True,
    )
    
    forgot_password = ft.TextButton(
        "Forgot Password?",
        style=ft.ButtonStyle(color=theme.accent_secondary),
        on_click=lambda e: show_forgot_password() if show_forgot_password else None,
    )
    
    return ft.Container(
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=0.8,
            colors=[theme.bg_gradient_start, theme.bg_primary, theme.bg_gradient_end]
        ),
        padding=20,
        content=ft.Column([
            ft.Container(height=30),
            logo,
            ft.Container(height=15),
            ft.Text("Welcome Back!", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
            ft.Container(height=4),
            ft.Text("Sign in to continue tracking your expenses", size=13, color=theme.text_secondary),
            ft.Container(height=25),
            ft.Container(
                content=ft.Row([error_icon, error_text], spacing=8),
                padding=ft.padding.only(bottom=10),
            ),
            username_cont,
            # Recent usernames chips (shown on focus)
            recent_users_container,
            ft.Container(height=8),
            password_cont,
            ft.Container(height=8),
            ft.Container(content=forgot_password, width=300, alignment=ft.alignment.center_right),
            ft.Container(height=18),
            login_btn,
            ft.Container(height=18),
            ft.Row([
                ft.Container(height=1, width=100, bgcolor=theme.border_primary),
                ft.Text("  or  ", color=theme.text_muted, size=12),
                ft.Container(height=1, width=100, bgcolor=theme.border_primary),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=18),
            ft.Row([
                ft.Text("Don't have an account?", color=theme.text_secondary, size=14),
                ft.TextButton("Sign Up", on_click=lambda e: show_register(), 
                             style=ft.ButtonStyle(color=theme.accent_secondary))
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.top_center
    )