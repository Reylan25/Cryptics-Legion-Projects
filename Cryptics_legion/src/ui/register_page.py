# src/ui/register_page.py
import flet as ft
from core import auth


def create_register_view(page: ft.Page, on_registered, show_login, toast):
    """
    on_registered() -> called after successful registration (optional)
    show_login() -> callable to show login
    toast(message, color) -> helper
    """
    def show_view():
        page.clean()
        new_user = ft.TextField(hint_text="Create Username", width=280, border="none", color="white",
                                prefix_icon=ft.Icons.PERSON_OUTLINE)
        new_pass = ft.TextField(hint_text="Create Password", width=220, border="none", password=True, color="white",
                                prefix_icon=ft.Icons.LOCK_OUTLINE)
        new_pass_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color="white")
        confirm_pass = ft.TextField(hint_text="Confirm Password", width=220, border="none", password=True, color="white",
                                    prefix_icon=ft.Icons.LOCK_OUTLINE)
        confirm_pass_eye = ft.IconButton(icon=ft.Icons.VISIBILITY_OFF, icon_color="white")

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

        username_cont = ft.Container(content=ft.Row([new_user]), border=ft.Border(bottom=ft.BorderSide(1, "white")),
                                     padding=ft.padding.only(bottom=6), width=300)
        pass_cont = ft.Container(content=ft.Row([new_pass, new_pass_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                 border=ft.Border(bottom=ft.BorderSide(1, "white")), padding=ft.padding.only(bottom=6), width=300)
        confirm_cont = ft.Container(content=ft.Row([confirm_pass, confirm_pass_eye], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    border=ft.Border(bottom=ft.BorderSide(1, "white")), padding=ft.padding.only(bottom=6), width=300)

        def do_register_click(e):
            u = new_user.value.strip()
            p = new_pass.value
            c = confirm_pass.value
            if not u or not p:
                toast("Fill username and password.", "#b71c1c")
                return
            if p != c:
                toast("Passwords do not match.", "#b71c1c")
                return
            ok = auth.register_user(u, p)
            if ok:
                toast("Account created. You can login now.", "#2E7D32")
                show_login()
                if on_registered:
                    on_registered()
            else:
                toast("Username already exists.", "#b71c1c")

        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=["#2b0057", "#000000"]),
                content=ft.Column([
                    ft.Container(height=80),
                    ft.Text("Create Account", size=26, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(height=30),
                    username_cont,
                    ft.Container(height=16),
                    pass_cont,
                    ft.Container(height=16),
                    confirm_cont,
                    ft.Container(height=30),
                    ft.ElevatedButton("Register", width=300, height=48, bgcolor="#8B4513", color="white", on_click=do_register_click,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))),
                    ft.Container(height=16),
                    ft.TextButton("Back to Login", on_click=lambda e: show_login(), style=ft.ButtonStyle(color="#FFD700")),
                    ft.Container(height=60),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=20
            )
        )
        page.update()

    return show_view
