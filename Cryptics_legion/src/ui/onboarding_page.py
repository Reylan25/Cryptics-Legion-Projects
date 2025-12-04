# src/ui/onboarding_page.py
import flet as ft
from core import db
from core.theme import get_theme


def create_onboarding_view(page: ft.Page, on_get_started, state=None):
    def handle_get_started(e):
        # Mark onboarding as seen for this user
        if state and state.get("user_id"):
            db.mark_onboarding_seen(state["user_id"])
        on_get_started()
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
                                           colors=[theme.bg_gradient_start, theme.accent_primary, theme.accent_secondary]),
                content=ft.Column([
                    ft.Container(height=120),
                    ft.Container(content=ft.Text("CL", size=80, weight=ft.FontWeight.BOLD, color="white"), padding=ft.padding.only(bottom=10)),
                    ft.Text("Cryptics Labs", size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(height=40),
                    ft.Container(content=ft.Text("Going cashless has never been this easier with the world's most leading expense manager.",
                                                size=15, color=theme.text_secondary if theme.mode == "light" else "#E1BEE7", text_align=ft.TextAlign.CENTER),
                                 width=340, padding=ft.padding.symmetric(horizontal=20)),
                    ft.Container(expand=True),
                    ft.Container(content=ft.ElevatedButton("Get Started", width=340, height=55, bgcolor=theme.accent_primary, color="white",
                                                           style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                                                           on_click=handle_get_started),
                                 padding=ft.padding.only(bottom=50))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
            )
        )
        page.update()
    return show_view
