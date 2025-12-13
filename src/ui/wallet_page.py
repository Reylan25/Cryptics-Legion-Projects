# src/ui/wallet_page.py
import flet as ft
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav


def create_user_avatar(user_id: int, radius: int = 22, theme=None):
    """Create a user avatar based on their profile settings."""
    if theme is None:
        theme = get_theme()
    
    user_profile = db.get_user_profile(user_id)
    photo = user_profile.get("photo") if user_profile else None
    
    if photo and isinstance(photo, dict):
        photo_type = photo.get("type", "default")
        photo_value = photo.get("value")
        photo_bg = photo.get("bg")
        
        if photo_type == "avatar" and photo_value:
            # Emoji avatar
            return ft.Container(
                content=ft.Text(photo_value, size=radius * 0.8),
                width=radius * 2,
                height=radius * 2,
                bgcolor=photo_bg or "#4F46E5",
                border_radius=radius,
                alignment=ft.alignment.center,
            )
        elif photo_type == "file" and photo_value:
            # Custom uploaded image
            return ft.Container(
                content=ft.Image(
                    src_base64=photo_value,
                    width=radius * 2 - 4,
                    height=radius * 2 - 4,
                    fit=ft.ImageFit.COVER,
                    border_radius=radius - 2,
                ),
                width=radius * 2,
                height=radius * 2,
                bgcolor="transparent",
                border_radius=radius,
                alignment=ft.alignment.center,
            )
    
    # Default avatar with user icon
    return ft.CircleAvatar(
        bgcolor="#4F46E5",
        content=ft.Icon(ft.Icons.PERSON, color="white", size=radius * 0.8),
        radius=radius,
    )


def create_wallet_view(page: ft.Page, state: dict, toast, go_back, 
                       show_expenses=None, show_profile=None, show_add_expense=None):
    """Create the wallet/budget page."""
    
    def nav_home():
        """Navigate to home."""
        if go_back:
            go_back()
    
    def nav_expenses():
        """Navigate to expenses page."""
        if show_expenses:
            show_expenses()
    
    def nav_profile():
        """Navigate to profile page."""
        if show_profile:
            show_profile()
    
    def nav_add_expense():
        """Navigate to add expense page."""
        if show_add_expense:
            show_add_expense()
    
    def show_view():
        page.clean()
        
        # Get expense data
        total_spent = db.total_expenses_by_user(state["user_id"])
        categories = db.category_summary_by_user(state["user_id"])
        
        # Budget settings (you can make this configurable)
        budget = 100000.0
        remaining = budget - total_spent
        spent_percent = (total_spent / budget * 100) if budget > 0 else 0
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Wallet", size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Container(
                        content=create_user_avatar(state["user_id"], radius=22),
                        on_click=lambda e: show_profile_page(),
                        ink=True,
                        border_radius=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=10),
        )
        
        # Budget overview card
        budget_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Monthly Budget", size=14, color="#9CA3AF"),
                            ft.Text(f"₱{budget:,.2f}", size=14, color="white", weight=ft.FontWeight.W_500),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=16),
                    # Progress bar
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    width=max(0, min(spent_percent, 100)) * 2.8,
                                    height=8,
                                    bgcolor="#EF4444" if spent_percent > 80 else "#6366F1",
                                    border_radius=4,
                                ),
                            ],
                        ),
                        width=280,
                        height=8,
                        bgcolor="#1F2937",
                        border_radius=4,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Spent", size=12, color="#9CA3AF"),
                                    ft.Text(f"₱{total_spent:,.2f}", size=18, weight=ft.FontWeight.BOLD, color="#EF4444"),
                                ],
                                spacing=2,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Remaining", size=12, color="#9CA3AF"),
                                    ft.Text(f"₱{remaining:,.2f}", size=18, weight=ft.FontWeight.BOLD, 
                                           color="#10B981" if remaining > 0 else "#EF4444"),
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=20,
            border_radius=16,
            bgcolor="#1a1a2e",
            border=ft.border.all(1, "#2d2d44"),
        )
        
        # Category breakdown
        category_list = ft.Column(spacing=8)
        
        # Define category colors
        colors = ["#8B5CF6", "#3B82F6", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#EC4899", "#6366F1"]
        
        for i, (cat, amount) in enumerate(categories):
            cat_percent = (amount / total_spent * 100) if total_spent > 0 else 0
            color = colors[i % len(colors)]
            
            category_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=8,
                                height=8,
                                bgcolor=color,
                                border_radius=4,
                            ),
                            ft.Text(cat, size=14, color="white", expand=True),
                            ft.Text(f"₱{amount:,.2f}", size=14, color="#9CA3AF"),
                            ft.Text(f"{cat_percent:.1f}%", size=12, color=color, width=50, text_align=ft.TextAlign.RIGHT),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=12,
                    border_radius=8,
                    bgcolor="#1a1a2e",
                )
            )
        
        if not categories:
            category_list.controls.append(
                ft.Container(
                    content=ft.Text("No expenses to show", color="#6B7280", size=14),
                    padding=20,
                    alignment=ft.alignment.center,
                )
            )
        
        # Quick stats
        stats_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT, color="#6366F1", size=24),
                            ft.Text(str(len(db.select_expenses_by_user(state["user_id"]))), 
                                   size=20, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Transactions", size=12, color="#9CA3AF"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor="#1a1a2e",
                    expand=True,
                ),
                ft.Container(width=12),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CATEGORY, color="#10B981", size=24),
                            ft.Text(str(len(categories)), 
                                   size=20, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Text("Categories", size=12, color="#9CA3AF"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor="#1a1a2e",
                    expand=True,
                ),
            ],
        )
        
        # Main scrollable content
        scrollable_content = ft.Column(
            controls=[
                budget_card,
                ft.Container(height=24),
                stats_row,
                ft.Container(height=24),
                ft.Text("Spending by Category", size=16, weight=ft.FontWeight.W_600, color="white"),
                ft.Container(height=12),
                category_list,
                ft.Container(height=100),  # Space for bottom nav
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        main_content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.bg_gradient_start, theme.bg_gradient_end],
            ),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
            content=ft.Column(
                controls=[
                    header,
                    scrollable_content,
                ],
                expand=True,
                spacing=0,
            ),
        )
        
        # Use centralized nav bar component
        page.add(
            create_page_with_nav(
                page=page,
                main_content=main_content,
                active_index=2,  # Wallet is active
                on_home=nav_home,
                on_expenses=nav_expenses,
                on_wallet=None,  # Already on wallet
                on_profile=nav_profile,
                on_fab_click=nav_add_expense,
            )
        )
        page.update()
    
    return show_view
