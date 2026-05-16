import flet as ft
from core.theme import get_theme
from utils.gamification import BadgeEngine

def build_badges_content(page: ft.Page, state: dict, toast, go_back):
    """Builds the badges collection page."""
    theme = get_theme()
    user_id = state["user_id"]
    
    # Get all badges and their status
    badges_data = BadgeEngine.get_all_badges_status(user_id)
    
    # Categorize badges
    categories = {
        "tracking": {"title": "Tracking Achievements", "badges": []},
        "streak": {"title": "Streak Milestones", "badges": []},
        "budget": {"title": "Budget Keepers", "badges": []},
        "special": {"title": "Special Challenges", "badges": []},
        "level": {"title": "Level Unlocks", "badges": []},
    }
    
    total_unlocked = 0
    for b in badges_data:
        if b["unlocked"]:
            total_unlocked += 1
        cat = b.get("category", "special")
        if cat in categories:
            categories[cat]["badges"].append(b)
            
    # Header
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=theme.text_primary,
                on_click=lambda e: go_back() if go_back else None,
            ),
            ft.Text("Badges & Achievements", size=20, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.Container(width=40),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Summary Card
    summary_card = ft.Container(
        content=ft.Column([
            ft.Text("Collection Progress", size=14, color=theme.text_secondary),
            ft.Row([
                ft.Text(f"{total_unlocked}", size=32, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.Text(f"/ {len(badges_data)} unlocked", size=16, color=theme.text_muted),
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.BASELINE),
            ft.ProgressBar(
                value=total_unlocked / len(badges_data) if badges_data else 0,
                color="#F59E0B",
                bgcolor=theme.border_primary,
                height=8,
                border_radius=4,
            ),
        ]),
        padding=20,
        bgcolor=theme.bg_card,
        border_radius=16,
        border=ft.border.all(1, theme.border_primary),
    )
    
    def show_badge_dialog(badge):
        icon_color = "#F59E0B" if badge["unlocked"] else theme.text_muted
        bg_color = f"{icon_color}15" if badge["unlocked"] else theme.bg_elevated
        
        dialog = ft.AlertDialog(
            title=ft.Text(badge["title"], size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            content=ft.Column([
                ft.Container(
                    content=ft.Text(badge["icon"], size=64),
                    width=120, height=120,
                    bgcolor=bg_color,
                    border_radius=60,
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, f"{icon_color}50") if badge["unlocked"] else None,
                ),
                ft.Container(height=16),
                ft.Text(badge["desc"], size=16, text_align=ft.TextAlign.CENTER, color=theme.text_primary),
                ft.Container(height=8),
                ft.Text(
                    f"Unlocked on {badge['unlocked_at'][:10]}" if badge["unlocked"] else "Locked",
                    size=12,
                    color="#10B981" if badge["unlocked"] else theme.text_muted,
                    weight=ft.FontWeight.BOLD if badge["unlocked"] else ft.FontWeight.NORMAL,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()
        page.overlay.remove(dialog)

    # Build badge grid
    content_list = [header, ft.Container(height=16), summary_card, ft.Container(height=24)]
    
    for cat_key, cat_data in categories.items():
        if not cat_data["badges"]: continue
        
        content_list.append(ft.Text(cat_data["title"], size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary))
        content_list.append(ft.Container(height=12))
        
        grid = ft.GridView(
            expand=False,
            runs_count=3,
            max_extent=120,
            child_aspect_ratio=0.85,
            spacing=16,
            run_spacing=16,
        )
        
        for badge in cat_data["badges"]:
            is_unlocked = badge["unlocked"]
            
            icon_container = ft.Container(
                content=ft.Text(badge["icon"] if is_unlocked else "🔒", size=32),
                width=64, height=64,
                bgcolor="#F59E0B15" if is_unlocked else theme.bg_elevated,
                border_radius=32,
                alignment=ft.alignment.center,
                border=ft.border.all(2, "#F59E0B50") if is_unlocked else ft.border.all(1, theme.border_primary),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=10, color="#F59E0B40") if is_unlocked else None,
            )
            
            card = ft.Container(
                content=ft.Column([
                    icon_container,
                    ft.Container(height=8),
                    ft.Text(
                        badge["title"],
                        size=11,
                        weight=ft.FontWeight.W_600 if is_unlocked else ft.FontWeight.NORMAL,
                        color=theme.text_primary if is_unlocked else theme.text_muted,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                padding=12,
                border_radius=16,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, "#F59E0B30") if is_unlocked else ft.border.all(1, theme.border_primary),
                on_click=lambda e, b=badge: show_badge_dialog(b),
                ink=True,
            )
            grid.controls.append(card)
            
        content_list.append(grid)
        content_list.append(ft.Container(height=24))

    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=20,
        content=ft.Column(
            controls=content_list,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
    )
