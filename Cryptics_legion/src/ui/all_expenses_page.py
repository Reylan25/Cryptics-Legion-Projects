# src/ui/all_expenses_page.py
import flet as ft
from datetime import datetime
import re
from core import db
from core.theme import get_theme
from utils.brand_recognition import identify_brand, get_icon_for_category
from utils.currency import format_currency, get_currency_from_user_profile, get_currency_symbol
from components.notification import ImmersiveNotification


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


def format_date_time(date_str: str) -> str:
    """Format date string to display format with time."""
    try:
        # Handle both date-only and datetime formats
        if " " in date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d %b %Y at %I:%M %p")
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y")
    except:
        return date_str


def extract_conversion_info(description: str) -> dict:
    """Extract currency conversion information from description."""
    if not description:
        return None
    
    # Pattern: [₱500.00 (PHP) = ¥1,069.52 (JPY) • Rate: 1 PHP = 2.139 JPY]
    pattern = r'\[(.+?)\s+\(([A-Z]{3})\)\s+=\s+(.+?)\s+\(([A-Z]{3})\)\s+•\s+Rate:\s+1\s+([A-Z]{3})\s+=\s+([\d,.]+)\s+([A-Z]{3})\]'
    match = re.search(pattern, description)
    
    if match:
        return {
            'from_amount': match.group(1),
            'from_currency': match.group(2),
            'to_amount': match.group(3),
            'to_currency': match.group(4),
            'rate': match.group(6),
            'description_clean': re.sub(pattern, '', description).strip()
        }
    return None


def create_all_expenses_view(page: ft.Page, state: dict, toast, go_back):
    """Create the all expenses page with edit/delete functionality."""
    user_id = state["user_id"]
    user_profile = db.get_user_profile(user_id)
    user_currency = get_currency_from_user_profile(user_profile)
    
    expenses_list = ft.Column(spacing=8)
    
    def load_expenses():
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        # Cache full account info for efficiency
        account_cache = {}
        def get_account_info(acc_id):
            if acc_id is None:
                return None, user_currency  # Return None for name, user's currency as default
            if acc_id not in account_cache:
                acc = db.get_account_by_id(acc_id, state["user_id"])
                if acc:
                    # acc structure: id, name, account_number, type, balance, currency, color, is_primary, created_at
                    account_cache[acc_id] = {"name": acc[1], "currency": acc[5]}
                else:
                    account_cache[acc_id] = {"name": None, "currency": user_currency}
            return account_cache[acc_id]["name"], account_cache[acc_id]["currency"]
        
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
                acc_name, acc_currency = get_account_info(acc_id)
                expenses_list.controls.append(
                    create_expense_card(eid, amt, cat, dsc, dtt, acc_name, acc_currency)
                )
        
        page.update()
    
    def create_expense_card(eid, amount, category, description, date, account_name=None, account_currency=None):
        """Create an expense card with edit/delete options."""
        # Use account currency if available, otherwise fall back to user currency
        display_currency = account_currency if account_currency else user_currency
        
        def show_edit_dialog(e):
            edit_expense(eid, amount, category, description, date)
        
        def confirm_delete(e):
            def do_delete(e):
                db.delete_expense_row(eid, state["user_id"])
                
                # Show immersive notification
                notif = ImmersiveNotification(page)
                notif.show("Expense has been deleted successfully", "success", title="Deleted! 🗑️")
                
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
                    # Amount - use account currency instead of user currency
                    ft.Text(format_currency(-amount, display_currency), size=14, weight=ft.FontWeight.W_600, color="#EF4444"),
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
        
        # Error text components
        amount_error = ft.Text("", size=11, color="#EF4444", visible=False)
        category_error = ft.Text("", size=11, color="#EF4444", visible=False)
        date_error = ft.Text("", size=11, color="#EF4444", visible=False)
        
        amount_field = ft.TextField(value=str(amount), label="Amount", keyboard_type=ft.KeyboardType.NUMBER)
        category_field = ft.TextField(value=category, label="Category")
        desc_field = ft.TextField(value=description or "", label="Description")
        date_field = ft.TextField(value=date, label="Date (YYYY-MM-DD)")
        
        def save_edit(e):
            # Clear previous errors
            amount_error.visible = False
            amount_error.value = ""
            category_error.visible = False
            category_error.value = ""
            date_error.visible = False
            date_error.value = ""
            
            has_error = False
            
            # Validate amount field
            if not amount_field.value or not amount_field.value.strip():
                amount_error.value = "⚠️ Amount cannot be empty"
                amount_error.visible = True
                has_error = True
            else:
                try:
                    new_amount = float(amount_field.value.strip().replace(",", ""))
                    if new_amount <= 0:
                        amount_error.value = "⚠️ Amount must be greater than 0"
                        amount_error.visible = True
                        has_error = True
                except ValueError:
                    amount_error.value = "⚠️ Please enter a valid number"
                    amount_error.visible = True
                    has_error = True
            
            # Validate category field
            if not category_field.value or not category_field.value.strip():
                category_error.value = "⚠️ Category cannot be empty"
                category_error.visible = True
                has_error = True
            
            # Validate date field
            if not date_field.value or not date_field.value.strip():
                date_error.value = "⚠️ Date cannot be empty"
                date_error.visible = True
                has_error = True
            
            if has_error:
                page.update()
                return
            
            # Get validated amount
            new_amount = float(amount_field.value.strip().replace(",", ""))
            
            ok = db.update_expense_row(
                eid,
                state["user_id"],
                new_amount,
                category_field.value.strip(),
                desc_field.value.strip() if desc_field.value else "",
                date_field.value.strip()
            )
            
            # Show immersive notification
            notif = ImmersiveNotification(page)
            if ok:
                notif.show("Your expense has been updated successfully", "success", title="Updated! ✏️")
            else:
                notif.show("Failed to update expense. Please try again", "error", title="Update Failed")
            
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
                    ft.Column([amount_field, amount_error], spacing=4),
                    ft.Column([category_field, category_error], spacing=4),
                    desc_field,
                    ft.Column([date_field, date_error], spacing=4),
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
                            ft.Text(format_currency(total, user_currency), size=24, weight=ft.FontWeight.BOLD, color="#EF4444"),
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
    
    # Cache account names and currencies for efficiency
    account_cache = {}
    currency_cache = {}
    
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    def get_account_currency(acc_id):
        """Get the currency of the account used for this expense"""
        if acc_id is None:
            return "PHP"
        if acc_id not in currency_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            currency_cache[acc_id] = acc[5] if acc else "PHP"
        return currency_cache[acc_id]
    
    def show_expense_details(eid, amount, category, description, date_str, acc_id, expense_currency):
        """Show detailed transaction information dialog."""
        account_name = get_account_name(acc_id) or "Cash"
        conversion_info = extract_conversion_info(description)
        display_desc = conversion_info['description_clean'] if conversion_info else (description or category)
        
        # Generate recommendations based on expense
        recommendations = []
        if amount > 1000:
            recommendations.append("💡 Consider creating a budget plan for this category")
        if conversion_info:
            recommendations.append("💱 Currency conversion applied - check if better rates are available")
        if category.lower() in ['food', 'dining', 'restaurant']:
            recommendations.append("🍽️ Track your dining expenses to identify saving opportunities")
        if category.lower() in ['shopping', 'retail']:
            recommendations.append("🛍️ Consider waiting for sales or using discount codes")
        
        # Build details dialog content - start with basic info
        details_controls = [
            # Transaction ID
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.TAG, size=16, color=theme.accent_primary),
                    ft.Text("Transaction ID:", size=12, color=theme.text_muted),
                    ft.Text(f"#{eid}", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ], spacing=6),
                padding=10,
                border_radius=8,
                bgcolor="#1a1a2e",
            ),
            ft.Container(height=8),
            # Date & Time
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=theme.accent_primary),
                        ft.Text("Date & Time", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ], spacing=6),
                    ft.Container(height=4),
                    ft.Text(format_date_time(date_str), size=13, color=theme.text_secondary),
                ], spacing=2),
                padding=10,
                border_radius=8,
                bgcolor="#1a1a2e",
            ),
            ft.Container(height=8),
        ]
        
        # Add conversion info section if available
        if conversion_info:
            details_controls.extend([
                # Exchange Rate Info
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CURRENCY_EXCHANGE, size=16, color="#10B981"),
                            ft.Text("Currency Conversion", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ], spacing=6),
                        ft.Container(height=8),
                        ft.Column([
                            ft.Row([
                                ft.Text("Original:", size=11, color=theme.text_muted, width=70),
                                ft.Text(f"{conversion_info['from_amount']} {conversion_info['from_currency']}", 
                                       size=12, weight=ft.FontWeight.W_500, color=theme.text_primary),
                            ]),
                            ft.Row([
                                ft.Text("Converted:", size=11, color=theme.text_muted, width=70),
                                ft.Text(f"{conversion_info['to_amount']} {conversion_info['to_currency']}", 
                                       size=12, weight=ft.FontWeight.W_500, color=theme.text_primary),
                            ]),
                            ft.Container(height=4),
                            ft.Container(
                                content=ft.Text(f"Rate: 1 {conversion_info['from_currency']} = {conversion_info['rate']} {conversion_info['to_currency']}",
                                              size=11, color="#10B981", weight=ft.FontWeight.W_500),
                                padding=6,
                                border_radius=6,
                                bgcolor="#10B98120",
                            ),
                        ], spacing=4),
                    ], spacing=2),
                    padding=10,
                    border_radius=8,
                    bgcolor="#1a1a2e",
                ),
                ft.Container(height=8),
            ])
        
        # Continue with account info and other details
        details_controls.extend([
            # Account Info
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=16, color=theme.accent_primary),
                        ft.Text("Account", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ], spacing=6),
                    ft.Container(height=4),
                    ft.Text(f"{account_name} ({expense_currency})", size=13, color=theme.text_secondary),
                ], spacing=2),
                padding=10,
                border_radius=8,
                bgcolor="#1a1a2e",
            ),
            ft.Container(height=8),
            # Description
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.DESCRIPTION, size=16, color=theme.accent_primary),
                        ft.Text("Description", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ], spacing=6),
                    ft.Container(height=4),
                    ft.Text(display_desc, size=13, color=theme.text_secondary),
                ], spacing=2),
                padding=10,
                border_radius=8,
                bgcolor="#1a1a2e",
            ),
        ])
        
        # Add recommendations section if available
        if len(recommendations) > 0:
            details_controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=8),
                        ft.Row([
                            ft.Icon(ft.Icons.LIGHTBULB, size=16, color="#F59E0B"),
                            ft.Text("Recommendations", size=12, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ], spacing=6),
                        ft.Container(height=8),
                        ft.Column([
                            ft.Text(rec, size=11, color=theme.text_secondary) for rec in recommendations
                        ], spacing=6),
                    ], spacing=2),
                    padding=10,
                    border_radius=8,
                    bgcolor="#1a1a2e",
                )
            )
        
        # Create the scrollable column with all details
        details_content = ft.Column(details_controls, spacing=0, scroll=ft.ScrollMode.AUTO)
        
        def close_dialog(e):
            page.close(details_dialog)
        
        details_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=theme.accent_primary, size=24),
                ft.Text("Transaction Details", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary),
            ], spacing=8),
            content=ft.Container(
                content=details_content,
                width=400,
                height=500,
            ),
            bgcolor=theme.bg_primary,
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=close_dialog,
                    style=ft.ButtonStyle(color=theme.accent_primary),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(details_dialog)
    
    def create_expense_card(expense):
        """Create an expense card with swipe to delete."""
        eid, uid, amount, category, description, date_str, acc_id = expense[:7]
        
        icon = get_category_icon(description or category)
        icon_color = get_category_color(description or category)
        display_name = description if description else category
        formatted_date = format_date(date_str)
        account_name = get_account_name(acc_id)
        
        # Get currency from the expense's original account
        expense_currency = get_account_currency(acc_id)
        currency_symbol = get_currency_symbol(expense_currency)
        
        # Clean display name if conversion info exists
        conversion_info = extract_conversion_info(description)
        if conversion_info:
            display_name = conversion_info['description_clean'] if conversion_info['description_clean'] else category
        
        # Build subtitle text
        subtitle = f"{category} • {formatted_date}"
        
        return ft.Container(
            content=ft.Row([
                # Icon with gradient background
                ft.Container(
                    content=ft.Icon(icon, color="white", size=22),
                    width=50,
                    height=50,
                    border_radius=14,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[icon_color, f"{icon_color}CC"],
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=f"{icon_color}40",
                        offset=ft.Offset(0, 2),
                    ),
                ),
                ft.Container(width=14),
                # Details - left side
                ft.Column([
                    ft.Text(
                        display_name,
                        size=15,
                        weight=ft.FontWeight.W_600,
                        color=theme.text_primary,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Row([
                        ft.Text(category, size=11, color=theme.text_muted, weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Text("•", size=11, color=theme.text_muted),
                            margin=ft.margin.symmetric(horizontal=4),
                        ),
                        ft.Text(formatted_date, size=11, color=theme.text_muted),
                    ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.END),
                ], spacing=4, expand=True),
                # Amount and Account - right side
                ft.Column([
                    ft.Text(
                        f"-{currency_symbol}{amount:,.2f}",
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
                    ], spacing=3, tight=True) if account_name else ft.Container(height=16),
                ], spacing=3, horizontal_alignment=ft.CrossAxisAlignment.END),
                ft.Container(width=8),
                # Action buttons
                ft.Column([
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="#EF4444",
                        icon_size=18,
                        tooltip="Delete",
                        on_click=lambda e, eid=eid, amt=amount, desc=display_name: delete_expense(eid, amt, desc),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY_OUTLINED,
                        icon_color=theme.accent_primary,
                        icon_size=18,
                        tooltip="See Details",
                        on_click=lambda e, i=eid, a=amount, c=category, d=description, dt=date_str, ac=acc_id, cur=expense_currency: show_expense_details(i, a, c, d, dt, ac, cur),
                    ),
                ], spacing=0),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#00000020",
                offset=ft.Offset(0, 2),
            ),
        )
    
    # Build expenses list
    if expenses:
        for expense in expenses:
            expenses_list.controls.append(create_expense_card(expense))
    else:
        expenses_list.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, color=theme.accent_primary, size=72),
                        width=120,
                        height=120,
                        border_radius=60,
                        bgcolor=f"{theme.accent_primary}15",
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "No expenses yet",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=theme.text_primary,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Start tracking your spending!",
                        size=14,
                        color=theme.text_muted,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Tap the + button to add your first expense",
                        size=12,
                        color=theme.text_muted,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=80,
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
                    content=ft.Icon(ft.Icons.TRENDING_DOWN, color="white", size=20),
                    width=44,
                    height=44,
                    border_radius=12,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#EF4444", "#DC2626"],
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color="#EF444440",
                        offset=ft.Offset(0, 2),
                    ),
                ),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(
                        "Total Spent",
                        size=11,
                        color=theme.text_muted,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        f"₱{total_spent:,.0f}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#EF4444",
                    ),
                ], spacing=2, expand=True),
            ], spacing=0),
            bgcolor=theme.bg_card,
            border_radius=16,
            padding=14,
            border=ft.border.all(1, theme.border_primary),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#00000015",
                offset=ft.Offset(0, 2),
            ),
            expand=True,
        ),
        ft.Container(width=10),
        # Transaction Count Card
        ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.RECEIPT_LONG, color="white", size=20),
                    width=44,
                    height=44,
                    border_radius=12,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[theme.accent_primary, f"{theme.accent_primary}DD"],
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=f"{theme.accent_primary}40",
                        offset=ft.Offset(0, 2),
                    ),
                ),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(
                        "Transactions",
                        size=11,
                        color=theme.text_muted,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        str(expense_count),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=theme.text_primary,
                    ),
                ], spacing=2, expand=True),
            ], spacing=0),
            bgcolor=theme.bg_card,
            border_radius=16,
            padding=14,
            border=ft.border.all(1, theme.border_primary),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#00000015",
                offset=ft.Offset(0, 2),
            ),
            expand=True,
        ),
    ])
    
    # Section header
    section_header = ft.Row([
        ft.Text(
            "Transactions",
            size=17,
            weight=ft.FontWeight.BOLD,
            color=theme.text_primary,
        ),
        ft.Container(
            content=ft.Text(
                f"{expense_count} items",
                size=12,
                color=theme.text_muted,
                weight=ft.FontWeight.W_500,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=12,
            bgcolor=f"{theme.text_muted}15",
        ),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Main scrollable content
    scrollable_content = ft.Column([
        summary_row,
        ft.Container(height=24),
        section_header,
        ft.Container(height=14),
        expenses_list,
        ft.Container(height=60),
    ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0)
    
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