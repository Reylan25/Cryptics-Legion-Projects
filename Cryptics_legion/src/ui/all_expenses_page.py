# src/ui/all_expenses_page.py
import flet as ft
from datetime import datetime
from core import db
from utils.brand_recognition import identify_brand, get_icon_for_category


def get_category_icon(category: str):
    """Returns an appropriate icon for the category using AI brand recognition."""
    result = identify_brand(category)
    return result["icon"]


def get_category_color(category: str):
    """Returns an appropriate color for the category using AI brand recognition."""
    result = identify_brand(category)
    return result["color"]


def format_date(date_str: str) -> str:
    """Format date string to display format."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except:
        return date_str


def create_all_expenses_view(page: ft.Page, state: dict, toast, go_back):
    """Create the all expenses page with edit/delete functionality."""
    
    expenses_list = ft.Column(spacing=8)
    
    def load_expenses():
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        if not rows:
            expenses_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG, color="#6B7280", size=48),
                            ft.Container(height=12),
                            ft.Text("No expenses yet", color="#6B7280", size=16),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for r in rows:
                eid, uid, amt, cat, dsc, dtt = r
                expenses_list.controls.append(
                    create_expense_card(eid, amt, cat, dsc, dtt)
                )
        
        page.update()
    
    def create_expense_card(eid, amount, category, description, date):
        """Create an expense card with edit/delete options."""
        
        def show_edit_dialog(e):
            edit_expense(eid, amount, category, description, date)
        
        def confirm_delete(e):
            def do_delete(e):
                db.delete_expense_row(eid, state["user_id"])
                toast("Expense deleted", "#2E7D32")
                dlg.open = False
                page.update()
                load_expenses()
            
            def cancel(e):
                dlg.open = False
                page.update()
            
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Delete Expense?"),
                content=ft.Text("Are you sure you want to delete this expense?"),
                actions=[
                    ft.TextButton("Cancel", on_click=cancel),
                    ft.TextButton("Delete", on_click=do_delete, style=ft.ButtonStyle(color="#EF4444")),
                ],
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
        
        icon = get_category_icon(category)
        icon_color = get_category_color(category)
        display_name = description if description else category
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Icon with brand color
                    ft.Container(
                        content=ft.Icon(icon, color="white", size=22),
                        width=44,
                        height=44,
                        border_radius=22,
                        bgcolor=icon_color,
                        alignment=ft.alignment.center,
                    ),
                    # Details
                    ft.Column(
                        controls=[
                            ft.Text(display_name, size=14, weight=ft.FontWeight.W_500, color="white"),
                            ft.Text(f"{category} • {format_date(date)}", size=12, color="#6B7280"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    # Amount
                    ft.Text(f"-₱{amount:,.2f}", size=14, weight=ft.FontWeight.W_600, color="#EF4444"),
                    # Actions
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        icon_color="#6B7280",
                        items=[
                            ft.PopupMenuItem(text="Edit", icon=ft.Icons.EDIT, on_click=show_edit_dialog),
                            ft.PopupMenuItem(text="Delete", icon=ft.Icons.DELETE, on_click=confirm_delete),
                        ],
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border_radius=12,
            bgcolor="#1a1a2e",
            border=ft.border.all(1, "#2d2d44"),
        )
    
    def edit_expense(eid, amount, category, description, date):
        """Show edit expense dialog."""
        
        amount_field = ft.TextField(value=str(amount), label="Amount", keyboard_type=ft.KeyboardType.NUMBER)
        category_field = ft.TextField(value=category, label="Category")
        desc_field = ft.TextField(value=description or "", label="Description")
        date_field = ft.TextField(value=date, label="Date (YYYY-MM-DD)")
        
        def save_edit(e):
            try:
                new_amount = float(amount_field.value)
            except ValueError:
                toast("Invalid amount", "#b71c1c")
                return
            
            ok = db.update_expense_row(
                eid,
                state["user_id"],
                new_amount,
                category_field.value,
                desc_field.value,
                date_field.value
            )
            
            if ok:
                toast("Expense updated", "#2E7D32")
            else:
                toast("Update failed", "#b71c1c")
            
            dlg.open = False
            page.update()
            load_expenses()
        
        def cancel(e):
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Expense"),
            content=ft.Column(
                controls=[
                    amount_field,
                    category_field,
                    desc_field,
                    date_field,
                ],
                tight=True,
                spacing=12,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.TextButton("Save", on_click=save_edit),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()
    
    def show_view():
        page.clean()
        
        # Calculate totals
        total = db.total_expenses_by_user(state["user_id"])
        
        # Header
        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: go_back(),
                ),
                ft.Text("All Expenses", size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(width=48),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Total card
        total_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Total Spent", size=14, color="#9CA3AF"),
                            ft.Text(f"₱{total:,.2f}", size=24, weight=ft.FontWeight.BOLD, color="#EF4444"),
                        ],
                        spacing=4,
                    ),
                    ft.Icon(ft.Icons.TRENDING_DOWN, color="#EF4444", size=32),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            border_radius=16,
            bgcolor="#1a1a2e",
            border=ft.border.all(1, "#2d2d44"),
        )
        
        load_expenses()
        
        # Main layout
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["#0f0f23", "#0a0a14"],
                ),
                padding=20,
                content=ft.Column(
                    controls=[
                        header,
                        ft.Container(height=20),
                        total_card,
                        ft.Container(height=20),
                        ft.Text("Recent Transactions", size=16, weight=ft.FontWeight.W_600, color="white"),
                        ft.Container(height=12),
                        expenses_list,
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            )
        )
        page.update()
    
    return show_view
