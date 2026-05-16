# src/ui/user/reminders_page.py
"""
Reminders & Notifications Settings Page
Provides UI for configuring daily reminders, budget warnings,
weekly summaries, idle reminders, and recurring expenses.
"""

import flet as ft
from core import db
from core.theme import get_theme


def build_reminders_content(page: ft.Page, state: dict, toast, go_back):
    """Build the reminders and notifications settings page."""
    theme = get_theme()
    user_id = state["user_id"]
    
    # Initialize defaults if none exist
    try:
        db.init_default_reminders(user_id)
    except Exception as e:
        print(f"Init defaults error: {e}")
    
    # Refresh engine config if running
    def notify_engine():
        if "_reminder_engine" in state:
            # The engine checks db directly on next tick, but we could add force_check here
            pass

    # ============ HELPER FUNCTIONS ============
    def save_setting(rtype: str, enabled: bool, **kwargs):
        db.upsert_reminder(user_id, rtype, enabled=enabled, **kwargs)
        notify_engine()
        toast("Settings saved", "#10B981")

    # ============ LOAD DATA ============
    reminders = {r[1]: r for r in db.get_user_reminders(user_id)}
    # r is (id, type, enabled, time, threshold, days_inactive, custom_message, last_triggered, created_at)
    
    daily_rem = reminders.get("daily_expense", (0, "daily_expense", 1, "20:00", 20.0, 3, "", None, ""))
    budget_rem = reminders.get("budget_warning", (0, "budget_warning", 1, "20:00", 20.0, 3, "", None, ""))
    weekly_rem = reminders.get("weekly_summary", (0, "weekly_summary", 1, "09:00", 20.0, 3, "", None, ""))
    idle_rem = reminders.get("idle_reminder", (0, "idle_reminder", 1, "20:00", 20.0, 3, "", None, ""))
    
    # ============ STATE VARS ============
    ui_state = {
        "daily_enabled": bool(daily_rem[2]),
        "daily_time": daily_rem[3],
        "budget_enabled": bool(budget_rem[2]),
        "budget_threshold": budget_rem[4],
        "weekly_enabled": bool(weekly_rem[2]),
        "weekly_time": weekly_rem[3],
        "idle_enabled": bool(idle_rem[2]),
        "idle_days": idle_rem[5],
    }

    # ============ UI BUILDERS ============
    
    def create_setting_card(title: str, subtitle: str, icon: str, control, is_last: bool = False):
        """Standardized setting card."""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(icon, size=20),
                    width=40, height=40, border_radius=12,
                    bgcolor=f"{theme.accent_primary}15",
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(title, size=15, weight=ft.FontWeight.W_600, color=theme.text_primary),
                    ft.Text(subtitle, size=12, color=theme.text_muted),
                ], spacing=2, expand=True),
                control,
            ]),
            padding=16,
            border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary)) if not is_last else None,
        )

    # --- Daily Expense Reminder ---
    def on_daily_toggle(e):
        ui_state["daily_enabled"] = e.control.value
        save_setting("daily_expense", ui_state["daily_enabled"], time_str=ui_state["daily_time"])
        page.update()
        
    def show_daily_time_picker(e):
        if not ui_state["daily_enabled"]:
            return
            
        def on_change(e):
            if e.control.value:
                time_str = e.control.value.strftime("%H:%M")
                ui_state["daily_time"] = time_str
                daily_time_btn.text = time_str
                save_setting("daily_expense", ui_state["daily_enabled"], time_str=time_str)
                page.update()
                
        picker = ft.TimePicker(
            on_change=on_change,
        )
        page.open(picker)

    daily_toggle = ft.Switch(value=ui_state["daily_enabled"], active_color=theme.accent_primary, on_change=on_daily_toggle)
    daily_time_btn = ft.TextButton(
        text=ui_state["daily_time"],
        on_click=show_daily_time_picker,
        style=ft.ButtonStyle(color=theme.accent_primary),
        disabled=not ui_state["daily_enabled"]
    )
    
    daily_controls = ft.Row([daily_time_btn, daily_toggle], spacing=4)

    # --- Budget Warning ---
    def on_budget_toggle(e):
        ui_state["budget_enabled"] = e.control.value
        save_setting("budget_warning", ui_state["budget_enabled"], threshold=ui_state["budget_threshold"])
        budget_slider_container.visible = ui_state["budget_enabled"]
        page.update()
        
    def on_budget_threshold_change(e):
        val = round(e.control.value)
        ui_state["budget_threshold"] = float(val)
        budget_val_text.value = f"{val}%"
        page.update()
        
    def on_budget_threshold_change_end(e):
        save_setting("budget_warning", ui_state["budget_enabled"], threshold=ui_state["budget_threshold"])

    budget_toggle = ft.Switch(value=ui_state["budget_enabled"], active_color=theme.accent_primary, on_change=on_budget_toggle)
    budget_val_text = ft.Text(f"{int(ui_state['budget_threshold'])}%", size=14, color=theme.accent_primary, weight=ft.FontWeight.BOLD)
    
    budget_slider_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Warn when balance drops below:", size=12, color=theme.text_muted),
                ft.Container(expand=True),
                budget_val_text,
            ]),
            ft.Slider(
                min=5, max=50, divisions=9, label="{value}%",
                value=ui_state["budget_threshold"],
                active_color="#F59E0B",
                on_change=on_budget_threshold_change,
                on_change_end=on_budget_threshold_change_end,
            ),
            ft.Row([
                ft.Text("Critical (5%)", size=10, color="#EF4444"),
                ft.Container(expand=True),
                ft.Text("Early Warning (50%)", size=10, color=theme.text_muted),
            ])
        ]),
        padding=ft.padding.only(left=60, right=16, bottom=16),
        visible=ui_state["budget_enabled"],
        border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary))
    )

    # --- Weekly Summary ---
    def on_weekly_toggle(e):
        ui_state["weekly_enabled"] = e.control.value
        save_setting("weekly_summary", ui_state["weekly_enabled"], time_str=ui_state["weekly_time"])
        page.update()

    weekly_toggle = ft.Switch(value=ui_state["weekly_enabled"], active_color=theme.accent_primary, on_change=on_weekly_toggle)

    # --- Idle Reminder ---
    def on_idle_toggle(e):
        ui_state["idle_enabled"] = e.control.value
        save_setting("idle_reminder", ui_state["idle_enabled"], days_inactive=ui_state["idle_days"])
        idle_slider_container.visible = ui_state["idle_enabled"]
        page.update()
        
    def on_idle_days_change(e):
        val = round(e.control.value)
        ui_state["idle_days"] = val
        idle_val_text.value = f"{val} days"
        page.update()
        
    def on_idle_days_change_end(e):
        save_setting("idle_reminder", ui_state["idle_enabled"], days_inactive=ui_state["idle_days"])

    idle_toggle = ft.Switch(value=ui_state["idle_enabled"], active_color=theme.accent_primary, on_change=on_idle_toggle)
    idle_val_text = ft.Text(f"{int(ui_state['idle_days'])} days", size=14, color=theme.accent_primary, weight=ft.FontWeight.BOLD)
    
    idle_slider_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Remind me after inactivity of:", size=12, color=theme.text_muted),
                ft.Container(expand=True),
                idle_val_text,
            ]),
            ft.Slider(
                min=1, max=14, divisions=13, label="{value} days",
                value=ui_state["idle_days"],
                active_color=theme.accent_primary,
                on_change=on_idle_days_change,
                on_change_end=on_idle_days_change_end,
            ),
        ]),
        padding=ft.padding.only(left=60, right=16, bottom=16),
        visible=ui_state["idle_enabled"],
        border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary))
    )

    # ============ RECURRING EXPENSES ============
    recurring_list = ft.Column(spacing=0)
    
    def load_recurring():
        recurring_list.controls.clear()
        expenses = db.get_recurring_expenses(user_id)
        
        if not expenses:
            recurring_list.controls.append(
                ft.Container(
                    content=ft.Text("No recurring expenses added yet.", color=theme.text_muted, size=13, text_align=ft.TextAlign.CENTER),
                    padding=20, alignment=ft.alignment.center
                )
            )
        else:
            for exp in expenses:
                eid, name, amount, cat, due_day, freq, enabled, _, _ = exp
                
                # Suffix for day (st, nd, rd, th)
                suffix = "th"
                if due_day % 10 == 1 and due_day != 11: suffix = "st"
                elif due_day % 10 == 2 and due_day != 12: suffix = "nd"
                elif due_day % 10 == 3 and due_day != 13: suffix = "rd"
                
                def make_toggle(eid_val):
                    def toggle(e):
                        db.update_recurring_expense(eid_val, user_id, enabled=1 if e.control.value else 0)
                        toast("Recurring expense updated", "#10B981")
                    return toggle
                
                def make_delete(eid_val, name_val):
                    def delete(e):
                        db.delete_recurring_expense(eid_val, user_id)
                        toast(f"Deleted {name_val}", "#EF4444")
                        load_recurring()
                        page.update()
                    return delete
                
                recurring_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Icon(ft.Icons.EVENT_REPEAT, color="white", size=18),
                                width=36, height=36, border_radius=10,
                                bgcolor="#8B5CF6", alignment=ft.alignment.center,
                            ),
                            ft.Container(width=10),
                            ft.Column([
                                ft.Text(name, size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Text(f"{freq.capitalize()} on the {due_day}{suffix} • {amount:,.2f}", size=11, color=theme.text_muted),
                            ], spacing=2, expand=True),
                            ft.Switch(value=bool(enabled), active_color="#8B5CF6", scale=0.8, on_change=make_toggle(eid)),
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=theme.text_muted, icon_size=20, on_click=make_delete(eid, name)),
                        ]),
                        padding=12,
                        border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary))
                    )
                )
    
    def show_add_recurring_dialog(e):
        name_field = ft.TextField(label="Expense Name (e.g. Rent, Netflix)", color=theme.text_primary, border_color=theme.border_primary)
        amount_field = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER, color=theme.text_primary, border_color=theme.border_primary)
        day_field = ft.TextField(label="Due Day (1-31)", keyboard_type=ft.KeyboardType.NUMBER, color=theme.text_primary, border_color=theme.border_primary)
        
        def save(e):
            if not name_field.value or not amount_field.value or not day_field.value:
                toast("Please fill all fields", "#EF4444")
                return
            try:
                amt = float(amount_field.value)
                day = int(day_field.value)
                if not (1 <= day <= 31):
                    toast("Day must be between 1 and 31", "#EF4444")
                    return
                
                db.insert_recurring_expense(user_id, name_field.value, amt, "Other", day, "monthly")
                toast("Recurring expense added", "#10B981")
                page.close(dlg)
                load_recurring()
                page.update()
            except ValueError:
                toast("Invalid amount or day", "#EF4444")
        
        dlg = ft.AlertDialog(
            title=ft.Text("Add Recurring Expense", color=theme.text_primary),
            bgcolor=theme.bg_secondary,
            content=ft.Column([name_field, amount_field, day_field], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.ElevatedButton("Save", bgcolor=theme.accent_primary, color="white", on_click=save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)
        
    load_recurring()

    # ============ LAYOUT ============
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=theme.text_primary,
                icon_size=20,
                on_click=lambda e: go_back() if go_back else None,
            ),
            ft.Text("Reminders & Alerts", size=18, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.Container(width=40), # Spacer
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=16),
    )
    
    settings_card = ft.Container(
        content=ft.Column([
            create_setting_card(
                "Daily Expense Log", "Remind me to log my expenses", "📝", daily_controls
            ),
            create_setting_card(
                "Budget Warning", "Alert when balance drops", "⚠️", budget_toggle
            ),
            budget_slider_container,
            create_setting_card(
                "Weekly Summary", "Show spending recap on Sunday", "📊", weekly_toggle
            ),
            create_setting_card(
                "Idle Reminder", "Remind if I haven't logged in a while", "💤", idle_toggle, is_last=True
            ),
            idle_slider_container,
        ], spacing=0),
        bgcolor=theme.bg_card,
        border_radius=16,
        border=ft.border.all(1, theme.border_primary),
        margin=ft.margin.only(bottom=24),
    )
    
    recurring_card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text("Recurring Expenses", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                    ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=theme.accent_primary, on_click=show_add_recurring_dialog),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=16,
                border=ft.border.only(bottom=ft.BorderSide(1, theme.border_primary))
            ),
            recurring_list,
        ], spacing=0),
        bgcolor=theme.bg_card,
        border_radius=16,
        border=ft.border.all(1, theme.border_primary),
    )
    
    return ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=16, right=16, top=10),
        content=ft.Column([
            header,
            ft.Column([
                settings_card,
                recurring_card,
                ft.Container(height=40),
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True, spacing=0),
    )
