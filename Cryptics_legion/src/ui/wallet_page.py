# src/ui/wallet_page.py
import flet as ft
from core import db


def create_wallet_view(page: ft.Page, state: dict, toast, go_back):
    """Create the wallet/budget page."""
    
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
        header = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: go_back(),
                ),
                ft.Text("Wallet", size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(width=48),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                        budget_card,
                        ft.Container(height=24),
                        stats_row,
                        ft.Container(height=24),
                        ft.Text("Spending by Category", size=16, weight=ft.FontWeight.W_600, color="white"),
                        ft.Container(height=12),
                        category_list,
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            )
        )
        page.update()
    
    return show_view
