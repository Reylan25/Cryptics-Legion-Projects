# src/ui/onboarding_page.py
import flet as ft


def create_onboarding_view(page: ft.Page, on_get_started):
    def show_view():
        page.clean()
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
                                           colors=["#1a0033", "#4a148c", "#6a1b9a"]),
                content=ft.Column([
                    ft.Container(height=120),
                    ft.Container(content=ft.Text("CL", size=80, weight=ft.FontWeight.BOLD, color="white"), padding=ft.padding.only(bottom=10)),
                    ft.Text("Cryptics Labs", size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(height=40),
                    ft.Container(content=ft.Text("Going cashless has never been this easier with the world's most leading expense manager.",
                                                size=15, color="#E1BEE7", text_align=ft.TextAlign.CENTER),
                                 width=340, padding=ft.padding.symmetric(horizontal=20)),
                    ft.Container(expand=True),
                    ft.Container(content=ft.ElevatedButton("Get Started", width=340, height=55, bgcolor="#C51162", color="white",
                                                           style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
                                                           on_click=lambda e: on_get_started()),
                                 padding=ft.padding.only(bottom=50))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
            )
        )
        page.update()
    return show_view
