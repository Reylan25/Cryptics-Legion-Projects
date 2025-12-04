# src/main.py
import flet as ft
from ui.login_page import create_login_view
from ui.register_page import create_register_view
from ui.onboarding_page import create_onboarding_view
from ui.personal_details import create_personal_details_view
from ui.home_page import create_home_view
from ui.Expenses import create_expenses_view
from ui.statistics_page import create_statistics_view  # Replaced wallet_page with statistics_page
from ui.profile_page import create_profile_view
from ui.account_settings_page import create_account_settings_view
from ui.add_expense_page import create_add_expense_view
from utils.statistics import create_charts_view
from core import db  # ensure DB is created at least once
from core.theme import get_theme, ThemeManager
import core.auth as auth

def main(page: ft.Page):
    # App configuration
    page.title = "Smart Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Mobile-friendly settings
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#0a0a14"
    
    # Fonts and styling
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
    
    # For desktop testing - simulate mobile screen size
    # These are ignored on actual mobile devices
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = True
    page.window.maximizable = True
    
    # Scroll behavior
    page.scroll = None  # Let individual views control scrolling
    
    # Prevent keyboard from resizing the view
    page.on_keyboard_event = lambda e: None

    # mutable state
    state = {"user_id": None, "editing_id": None, "current_view": "login"}

    # Update page bg based on theme
    def update_page_theme():
        theme = get_theme()
        page.bgcolor = theme.bg_primary
        page.update()

    # toast helper
    def toast(message: str, color: str = "#2E7D32"):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # Navigation handlers (we create view functions and call them)
    # will be set later
    def on_login_success(user_id: int):
        state["user_id"] = user_id
        # Check if user has seen onboarding before
        if db.has_user_seen_onboarding(user_id):
            show_home_view()  # Existing user - go directly to home
        else:
            show_onboarding_view()  # New user - show onboarding

    # Forward declarations for navigation
    def show_login_view():
        state["current_view"] = "login"
        login_view()

    def show_register_view():
        state["current_view"] = "register"
        register_view()

    def show_onboarding_view():
        state["current_view"] = "onboarding"
        onboarding_view()
    
    def show_personal_details_view():
        state["current_view"] = "personal_details"
        personal_details_view()

    def show_home_view():
        state["current_view"] = "home"
        update_page_theme()
        home_view()

    def show_expenses_view():
        state["current_view"] = "expenses"
        update_page_theme()
        expenses_view()

    def show_charts_view():
        state["current_view"] = "charts"
        charts_view()

    def show_statistics_view():
        state["current_view"] = "statistics"
        update_page_theme()
        statistics_view()

    def show_profile_view():
        state["current_view"] = "profile"
        update_page_theme()
        profile_view()

    def show_account_settings_view():
        state["current_view"] = "account_settings"
        update_page_theme()
        account_settings_view()

    def show_add_expense_view():
        state["current_view"] = "add_expense"
        update_page_theme()
        add_expense_view()

    # Refresh current view with new theme
    def refresh_current_view():
        update_page_theme()
        current = state.get("current_view", "login")
        view_map = {
            "login": show_login_view,
            "register": show_register_view,
            "onboarding": show_onboarding_view,
            "personal_details": show_personal_details_view,
            "home": show_home_view,
            "expenses": show_expenses_view,
            "statistics": show_statistics_view,
            "profile": show_profile_view,
            "account_settings": show_account_settings_view,
            "add_expense": show_add_expense_view,
        }
        if current in view_map:
            view_map[current]()

    def do_logout():
        state["user_id"] = None
        state["editing_id"] = None
        show_login_view()

    # Callback for after registration - go to personal details with password
    def on_register_success(password: str):
        state["temp_password"] = password
        show_personal_details_view()

    # Pre-create ALL view factory functions for instant navigation
    login_view = create_login_view(page, on_login_success, lambda: show_register_view(), lambda: show_onboarding_view(), toast)
    register_view = create_register_view(page, on_register_success, lambda: show_login_view(), toast, state)
    onboarding_view = create_onboarding_view(page, lambda: show_home_view(), state)
    personal_details_view = create_personal_details_view(
        page, state, toast,
        on_complete=lambda: show_onboarding_view(),
        on_back=lambda: show_register_view()
    )
    
    home_view = create_home_view(
        page, state, toast, 
        show_dashboard=lambda: show_expenses_view(), 
        logout_callback=lambda: do_logout(),
        show_wallet_cb=lambda: show_statistics_view(),
        show_profile_cb=lambda: show_profile_view(),
        show_add_expense_cb=lambda: show_add_expense_view()
    )
    
    expenses_view = create_expenses_view(
        page, state, toast,
        show_home=lambda: show_home_view(),
        show_wallet=lambda: show_statistics_view(),
        show_profile=lambda: show_profile_view(),
        show_add_expense=lambda: show_add_expense_view()
    )
    
    statistics_view = create_statistics_view(
        page, state, toast, 
        go_back=lambda: show_home_view(),
        show_expenses=lambda: show_expenses_view(),
        show_profile=lambda: show_profile_view(),
        show_add_expense=lambda: show_add_expense_view()
    )
    
    profile_view = create_profile_view(
        page, state, toast, 
        go_back=lambda: show_home_view(), 
        logout_callback=lambda: do_logout(),
        show_account_settings=lambda: show_account_settings_view(),
        refresh_app=lambda: refresh_current_view()
    )
    
    account_settings_view = create_account_settings_view(
        page, state, toast,
        go_back=lambda: show_profile_view()
    )
    
    add_expense_view = create_add_expense_view(
        page, state, toast, 
        go_back=lambda: show_expenses_view(),
        show_home=lambda: show_home_view(),
        show_expenses=lambda: show_expenses_view(),
        show_wallet=lambda: show_statistics_view(),
        show_profile=lambda: show_profile_view()
    )
    
    charts_view = create_charts_view(page)

    # ensure DB exists
    db.connect_db()

    # start app at login
    show_login_view()


if __name__ == "__main__":
    # Run as mobile app
    # For web/desktop testing:
    ft.app(target=main, assets_dir="assets")
    
    # To build for Android/iOS, use:
    # flet build apk (for Android)
    # flet build ipa (for iOS)
