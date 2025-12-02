# src/main.py
import flet as ft
from ui.login_page import create_login_view
from ui.register_page import create_register_view
from ui.onboarding_page import create_onboarding_view
from ui.home_page import create_home_view
from utils.charts_page import create_charts_view
from core import db  # ensure DB is created at least once
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
    state = {"user_id": None, "editing_id": None}

    # toast helper
    def toast(message: str, color: str = "#2E7D32"):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # Navigation handlers (we create view functions and call them)
    # will be set later
    def on_login_success(user_id: int):
        state["user_id"] = user_id
        show_onboarding_view()

    # create view factory functions
    login_view = create_login_view(page, on_login_success, lambda: show_register_view(), lambda: show_onboarding_view(), toast)
    register_view = create_register_view(page, None, lambda: show_login_view(), toast)
    onboarding_view = create_onboarding_view(page, lambda: show_home_view())
    home_view = create_home_view(page, state, toast, lambda: show_charts_view(), lambda: do_logout())
    charts_view = lambda: create_charts_view(page, state["user_id"], lambda: show_home_view(), toast)()

    # navigation wrappers to call functions
    def show_login_view():
        login_view()

    def show_register_view():
        register_view()

    def show_onboarding_view():
        onboarding_view()

    def show_home_view():
        home_view()

    def show_charts_view():
        charts_view()

    def do_logout():
        state["user_id"] = None
        state["editing_id"] = None
        show_login_view()

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
