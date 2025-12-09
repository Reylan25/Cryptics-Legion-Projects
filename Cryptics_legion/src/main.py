# src/main.py
"""
Smart Expense Tracker - Main Application
Flash-free navigation using a persistent container system.
"""
import flet as ft
from core import db
from core.theme import get_theme, ThemeManager
import core.auth as auth

# Import view CONTENT builders (we'll create these)
from ui.login_page import build_login_content
from ui.register_page import build_register_content
from ui.onboarding_page import build_onboarding_content
from ui.forgot_password_page import create_forgot_password_view
from ui.personal_details import build_personal_details_content
from ui.currency_selection_page import build_currency_selection_content
from ui.my_balance import build_my_balance_content
from ui.home_page import build_home_content
from ui.Expenses import build_expenses_content
from ui.statistics_page import build_statistics_content
from ui.profile_page import build_profile_content
from ui.account_settings_page import build_account_settings_content
from ui.add_expense_page import build_add_expense_content
from ui.all_expenses_page import build_all_expenses_content
from ui.exchange_rates_page import build_exchange_rates_content
from ui.privacy_page import build_privacy_content
from ui.passcode_lock_page import create_passcode_setup, create_passcode_verify
from ui.admin_dashboard_page import AdminDashboardPage
from ui.admin_users_page import AdminUserManagementPage
from components.notification import NotificationHistory
from ui.admin_logs_page import AdminLogsPage
from ui.admin_main_layout import AdminMainLayout
from ui.admin_profile_page import AdminProfilePage
from utils.statistics import create_charts_view


def main(page: ft.Page):
    """Main application entry point with flash-free navigation."""
    
    # ============ APP CONFIGURATION ============
    page.title = "Smart Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#0a0a14"
    
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
    
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = True
    page.window.maximizable = True
    page.scroll = None
    page.on_keyboard_event = lambda e: None

    # ============ PERSISTENT APP CONTAINER ============
    # This container stays on the page forever - we only swap its content
    app_container = ft.Container(
        expand=True,
        bgcolor="#0a0a14",
        padding=0,
    )

    # ============ APPLICATION STATE ============
    state = {
        "user_id": None,
        "editing_id": None,
        "current_view": "login",
        "previous_view": None,
        "is_admin": False,
        "admin": None,
    }

    # ============ HELPER FUNCTIONS ============
    def update_theme():
        """Update page background based on current theme."""
        theme = get_theme()
        page.bgcolor = theme.bg_primary
        app_container.bgcolor = theme.bg_primary
    
    def toast(message: str, color: str = "#2E7D32"):
        """Show a toast notification."""
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()
    
    def navigate_to(view_name: str, content_builder):
        """Navigate to a view by swapping container content - NO page.clean()!"""
        try:
            print(f"DEBUG: Navigating to {view_name}")
            state["previous_view"] = state["current_view"]
            state["current_view"] = view_name
            update_theme()
            
            # Close notification panel if open
            if "notification_center" in state:
                notification_center = state["notification_center"]
                if hasattr(notification_center, 'close_panel'):
                    notification_center.close_panel()
            
            # Build the new content and swap it in
            print(f"DEBUG: Building content for {view_name}")
            new_content = content_builder()
            print(f"DEBUG: Content built successfully for {view_name}")
            app_container.content = new_content
            page.update()
            print(f"DEBUG: Successfully navigated to {view_name}")
        except Exception as ex:
            print(f"ERROR in navigate_to({view_name}): {ex}")
            import traceback
            traceback.print_exc()

    # ============ VIEW NAVIGATION FUNCTIONS ============
    def show_login():
        # Check if app_container still exists (forgot password uses page.clean())
        if not page.controls or app_container not in page.controls:
            # Recreate the app structure
            page.clean()
            page.add(app_container)
        
        navigate_to("login", lambda: build_login_content(
            page, on_login_success, show_register, show_onboarding, toast, show_forgot_password
        ))
    
    def show_forgot_password():
        # Navigate properly - the forgot password page will handle its own rendering
        state["previous_view"] = state["current_view"]
        state["current_view"] = "forgot_password"
        update_theme()
        # Call the view function which uses page.clean() and page.add()
        forgot_password_view = create_forgot_password_view(page, show_login, toast)
        forgot_password_view()
    
    def show_register():
        navigate_to("register", lambda: build_register_content(
            page, on_register_success, show_login, toast, state
        ))
    
    def show_onboarding():
        navigate_to("onboarding", lambda: build_onboarding_content(
            page, show_home, state
        ))
    
    def show_personal_details():
        navigate_to("personal_details", lambda: build_personal_details_content(
            page, state, toast, show_passcode_setup, show_register
        ))
    
    def show_currency_selection():
        navigate_to("currency_selection", lambda: build_currency_selection_content(
            page, state, toast, show_my_balance
        ))
    
    def show_my_balance():
        navigate_to("my_balance", lambda: build_my_balance_content(
            page, state, toast, show_onboarding, show_personal_details
        ))
    
    def show_home():
        print("DEBUG: show_home() called")
        navigate_to("home", lambda: build_home_content(
            page, state, toast, show_expenses, do_logout, 
            show_statistics, show_profile, show_add_expense, show_all_expenses
        ))
    
    def show_expenses():
        navigate_to("expenses", lambda: build_expenses_content(
            page, state, toast, show_home, show_statistics, 
            show_profile, show_add_expense, show_expenses
        ))
    
    def show_statistics():
        navigate_to("statistics", lambda: build_statistics_content(
            page, state, toast, show_home, show_expenses, 
            show_profile, show_add_expense, show_exchange_rates
        ))
    
    def show_exchange_rates():
        navigate_to("exchange_rates", lambda: build_exchange_rates_content(
            page, state, toast, show_statistics
        ))
    
    def show_profile():
        navigate_to("profile", lambda: build_profile_content(
            page, state, toast, show_home, do_logout, 
            show_account_settings, refresh_current_view, show_privacy
        ))
    
    def show_account_settings():
        navigate_to("account_settings", lambda: build_account_settings_content(
            page, state, toast, show_profile
        ))
    
    def show_privacy():
        navigate_to("privacy", lambda: build_privacy_content(
            page, state, toast, show_profile, do_logout
        ))
    
    def show_add_expense():
        navigate_to("add_expense", lambda: build_add_expense_content(
            page, state, toast, show_expenses, show_home, 
            show_expenses, show_statistics, show_profile
        ))
    
    def show_all_expenses():
        navigate_to("all_expenses", lambda: build_all_expenses_content(
            page, state, toast, show_home, show_all_expenses
        ))
    
    def show_passcode_setup():
        """Show passcode setup screen (after signup)."""
        navigate_to("passcode_setup", lambda: create_passcode_setup(
            page, state, on_passcode_setup_complete
        ))
    
    def show_passcode_verify():
        """Show passcode verification screen (after login)."""
        navigate_to("passcode_verify", lambda: create_passcode_verify(
            page, state, on_passcode_verify_success, show_forgot_password
        ))
    
    # ============ ADMIN NAVIGATION FUNCTIONS ============
    def show_admin_dashboard():
        """Show admin dashboard with new layout."""
        navigate_to("admin_dashboard", lambda: AdminMainLayout(
            page, state, lambda route: show_login() if route == "login" else None
        ).build())
    
    def show_admin_users():
        """Show admin user management page (legacy - now part of main layout)."""
        show_admin_dashboard()
    
    def show_admin_logs():
        """Show admin activity logs page (legacy - now part of main layout)."""
        show_admin_dashboard()
    
    def navigate_admin(page_name: str):
        """Navigate between admin pages (legacy - now handled by AdminMainLayout)."""
        if page_name == "login":
            show_login()
        else:
            show_admin_dashboard()

    # ============ AUTH CALLBACKS ============
    def on_login_success(user_id: int, is_admin: bool = False, admin_data: dict = None):
        """Handle successful login - check if admin or regular user."""
        
        if is_admin:
            # Admin login - go directly to admin dashboard
            state["is_admin"] = True
            state["admin"] = admin_data
            state["user_id"] = user_id
            show_admin_dashboard()
        else:
            # Regular user login - check passcode
            state["user_id"] = user_id
            state["is_admin"] = False
            state["admin"] = None
            
            # Check if user has a passcode set up
            if db.has_passcode(user_id):
                # Show passcode verification before entering app
                show_passcode_verify()
            else:
                # No passcode set up, proceed normally
                if db.has_user_seen_onboarding(user_id):
                    show_home()
                else:
                    show_onboarding()
    
    def on_passcode_verify_success():
        """Handle successful passcode verification."""
        user_id = state.get("user_id")
        if user_id:
            if db.has_user_seen_onboarding(user_id):
                show_home()
            else:
                show_onboarding()
    
    def on_register_success(password: str):
        """Handle successful registration - proceed to personal details, then passcode setup."""
        state["temp_password"] = password
        show_personal_details()
    
    def on_passcode_setup_complete():
        """Handle completion of passcode setup after registration."""
        # After passcode is set up, continue to currency selection
        show_currency_selection()
    
    def do_logout():
        """Handle logout."""
        # Save notification read states before clearing
        NotificationHistory.on_user_logout()
        
        # Clear user session
        state["user_id"] = None
        state["editing_id"] = None
        show_login()

    # ============ REFRESH FUNCTIONS ============
    def refresh_current_view():
        """Force refresh the current view (e.g., after theme change)."""
        view_map = {
            "login": show_login,
            "register": show_register,
            "onboarding": show_onboarding,
            "personal_details": show_personal_details,
            "my_balance": show_my_balance,
            "home": show_home,
            "expenses": show_expenses,
            "statistics": show_statistics,
            "profile": show_profile,
            "account_settings": show_account_settings,
            "privacy": show_privacy,
            "add_expense": show_add_expense,
        }
        current = state.get("current_view", "login")
        if current in view_map:
            view_map[current]()

    # ============ INITIALIZE APP ============
    db.connect_db()
    
    # Initialize default admin account if not exists
    try:
        import bcrypt
        existing_admin = db.get_admin_by_username("ADMIN")
        if not existing_admin:
            password_hash = bcrypt.hashpw("ADMIN256".encode("utf-8"), bcrypt.gensalt())
            db.insert_admin(
                username="ADMIN",
                password_blob=password_hash,
                full_name="System Administrator",
                email="admin@expensetracker.com"
            )
            print("✓ Default admin account created (ADMIN / ADMIN256)")
    except Exception as e:
        print(f"Admin initialization note: {e}")
    
    # Add the persistent container ONCE - never call page.clean() again!
    page.add(app_container)
    
    # Start at login
    show_login()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
