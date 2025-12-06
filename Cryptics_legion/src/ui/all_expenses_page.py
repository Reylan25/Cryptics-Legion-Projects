# src/ui/all_expenses_page.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
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
        # Handle both date-only and datetime formats
        if " " in date_str:
            dt = datetime.strptime(date_str.split(" ")[0], "%Y-%m-%d")
        else:
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
        
        # Cache account names for efficiency
        account_cache = {}
        def get_account_name(acc_id):
            if acc_id is None:
                return None
            if acc_id not in account_cache:
                acc = db.get_account_by_id(acc_id, state["user_id"])
                account_cache[acc_id] = acc[1] if acc else None
            return account_cache[acc_id]
        
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
                # Unpack with account_id (position 6)
                eid, uid, amt, cat, dsc, dtt, acc_id = r[:7]
                acc_name = get_account_name(acc_id)
                expenses_list.controls.append(
                    create_expense_card(eid, amt, cat, dsc, dtt, acc_name)
                )
        
        page.update()
    
    def create_expense_card(eid, amount, category, description, date, account_name=None):
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
        
        # Build subtitle with account info
        subtitle_parts = [category, format_date(date)]
        subtitle_text = f"{category} • {format_date(date)}"
        
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
                            ft.Row([
                                ft.Text(subtitle_text, size=11, color="#6B7280"),
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=10, color="#7C3AED"),
                                        ft.Text(account_name or "Cash", size=10, color="#7C3AED", weight=ft.FontWeight.W_500),
                                    ], spacing=3),
                                    visible=account_name is not None,
                                ),
                            ], spacing=6),
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


# ============ NEW: Flash-free navigation content builder ============
def build_all_expenses_content(page: ft.Page, state: dict, toast, go_back, show_all_expenses=None):
    """
    Builds and returns all expenses page content with total spending and delete functionality.
    """
    theme = get_theme()
    
    # Get all expenses
    expenses = db.select_expenses_by_user(state["user_id"])
    total_spent = db.total_expenses_by_user(state["user_id"])
    expense_count = len(expenses) if expenses else 0
    
    # Expenses list container
    expenses_list = ft.Column(spacing=8)
    
    def refresh_view():
        """Refresh the view after deletion."""
        if show_all_expenses:
            show_all_expenses()
    
    def delete_expense(expense_id, amount, description):
        """Delete an expense with confirmation."""
        def confirm_delete(e):
            page.close(confirm_dialog)
            # Delete from database
            db.delete_expense_row(expense_id, state["user_id"])
            toast(f"Deleted: ₱{amount:,.2f}", "#10B981")
            refresh_view()
        
        def cancel_delete(e):
            page.close(confirm_dialog)
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Expense?", color=theme.text_primary),
            content=ft.Text(
                f"Are you sure you want to delete this expense?\n\n{description}\nAmount: ₱{amount:,.2f}",
                color=theme.text_secondary,
            ),
            bgcolor=theme.bg_card,
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton(
                    "Delete",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color="#EF4444"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(confirm_dialog)
    
    # Cache account names for efficiency
    account_cache = {}
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    def create_expense_card(expense):
        """Create an expense card with swipe to delete."""
        eid, uid, amount, category, description, date_str, acc_id = expense[:7]
        
        icon = get_category_icon(description or category)
        icon_color = get_category_color(description or category)
        display_name = description if description else category
        formatted_date = format_date(date_str)
        account_name = get_account_name(acc_id)
        
        # Build subtitle text
        subtitle = f"{category} • {formatted_date}"
        
        return ft.Container(
            content=ft.Row([
                # Icon
                ft.Container(
                    content=ft.Icon(icon, color="white", size=20),
                    width=44,
                    height=44,
                    border_radius=12,
                    bgcolor=icon_color,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=12),
                # Details - left side
                ft.Column([
                    ft.Text(
                        display_name,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=theme.text_primary,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(subtitle, size=11, color=theme.text_muted),
                ], spacing=3, expand=True),
                # Amount and Account - right side (fixed width)
                ft.Column([
                    ft.Text(
                        f"-₱{amount:,.2f}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#EF4444",
                    ),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=10, color=theme.accent_primary),
                        ft.Text(
                            account_name or "Cash",
                            size=10,
                            color=theme.accent_primary,
                            weight=ft.FontWeight.W_500,
                        ),
                    ], spacing=3, tight=True) if account_name else ft.Container(),
                ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END, width=100),
                # Delete button
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color="#EF4444",
                    icon_size=20,
                    tooltip="Delete",
                    on_click=lambda e, eid=eid, amt=amount, desc=display_name: delete_expense(eid, amt, desc),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border_radius=14,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
    
    # Build expenses list
    if expenses:
        for expense in expenses:
            expenses_list.controls.append(create_expense_card(expense))
    else:
        expenses_list.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.RECEIPT_LONG, color=theme.text_muted, size=64),
                    ft.Container(height=16),
                    ft.Text("No expenses yet", size=16, color=theme.text_muted),
                    ft.Text("Start tracking your spending!", size=13, color=theme.text_muted),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                padding=60,
                alignment=ft.alignment.center,
            )
        )
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=theme.text_primary,
                icon_size=20,
                on_click=lambda e: go_back(),
            ),
            ft.Text("All Expenses", size=18, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.Container(width=40),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=8),
    )
    
    # Summary Cards Row
    summary_row = ft.Row([
        # Total Spent Card
        ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.TRENDING_DOWN, color="white", size=16),
                    width=32,
                    height=32,
                    border_radius=8,
                    bgcolor="#EF4444",
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Total Spent", size=10, color=theme.text_muted),
                    ft.Text(
                        f"₱{total_spent:,.0f}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#EF4444",
                    ),
                ], spacing=1, expand=True),
            ], spacing=0),
            bgcolor=theme.bg_card,
            border_radius=14,
            padding=12,
            border=ft.border.all(1, theme.border_primary),
            expand=True,
        ),
        ft.Container(width=8),
        # Transaction Count Card
        ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.RECEIPT_LONG, color="white", size=16),
                    width=32,
                    height=32,
                    border_radius=8,
                    bgcolor=theme.accent_primary,
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Transactions", size=10, color=theme.text_muted),
                    ft.Text(
                        str(expense_count),
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=theme.text_primary,
                    ),
                ], spacing=1, expand=True),
            ], spacing=0),
            bgcolor=theme.bg_card,
            border_radius=14,
            padding=12,
            border=ft.border.all(1, theme.border_primary),
            expand=True,
        ),
    ])
    
    # Section header
    section_header = ft.Row([
        ft.Text("Transactions", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
        ft.Text(f"{expense_count} items", size=13, color=theme.text_muted),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Main scrollable content
    scrollable_content = ft.Column([
        summary_row,
        ft.Container(height=20),
        section_header,
        ft.Container(height=12),
        expenses_list,
        ft.Container(height=40),
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=20, right=20, top=10),
        content=ft.Column([
            header,
            scrollable_content,
        ], expand=True, spacing=0),
    )