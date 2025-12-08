"""
Admin Profile Page
Professional admin profile with account details, statistics, and settings
"""

import flet as ft
from core import db
from datetime import datetime
import base64
from components.notification import ImmersiveNotification


class AdminProfilePage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.admin_data = state.get("admin", {})
        self.admin_id = self.admin_data.get("id")
        self.admin_username = self.admin_data.get("username", "Admin")
        
        # Load full admin profile from database
        admin_profile = db.get_admin_profile(self.admin_id) if self.admin_id else {}
        if admin_profile:
            self.admin_data.update(admin_profile)
            # Load avatar if exists
            if admin_profile.get("avatar"):
                self.avatar_base64 = admin_profile.get("avatar")
        
        # Notification system
        self.notification = ImmersiveNotification(page)
        
        # Avatar management (will be set from database if available)
        if not hasattr(self, 'avatar_base64'):
            self.avatar_base64 = None
        self.avatar_display = None
        
        # File picker for avatar upload
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        page.overlay.append(self.file_picker)
        
        # Form fields - Account Details (Editable)
        self.full_name_field = ft.TextField(
            label="Full Name",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("full_name", "System Administrator"),
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        self.email_field = ft.TextField(
            label="Email Address",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("email", "admin@expensetracker.com"),
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        self.employee_id_field = ft.TextField(
            label="Employee ID",
            border_radius=8,
            filled=True,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_800,
            value=f"EMP{self.admin_id:04d}",
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            read_only=True
        )
        
        # Profile Settings (Editable)
        self.job_title_field = ft.TextField(
            label="Job Title",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("job_title", "System Administrator"),
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        self.department_field = ft.Dropdown(
            label="Department",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("department", "Admin user"),
            options=[
                ft.dropdown.Option("Admin user"),
                ft.dropdown.Option("IT Department"),
                ft.dropdown.Option("Management"),
                ft.dropdown.Option("Operations"),
                ft.dropdown.Option("Finance"),
                ft.dropdown.Option("Human Resources")
            ],
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        self.currency_field = ft.Dropdown(
            label="Default Currency",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("currency", "PHP"),
            options=[
                ft.dropdown.Option("PHP"),
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY"),
            ],
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        self.reporting_manager_field = ft.Dropdown(
            label="Reporting Manager",
            border_radius=8,
            filled=True,
            bgcolor="#3C3C3E",
            border_color=ft.Colors.GREY_700,
            value=self.admin_data.get("reporting_manager", "None"),
            options=[
                ft.dropdown.Option("None"),
                ft.dropdown.Option("Flava Chen"),
                ft.dropdown.Option("John Doe"),
                ft.dropdown.Option("Jane Smith"),
            ],
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
            on_change=self.mark_as_modified
        )
        
        # Track changes
        self.has_unsaved_changes = False
    
    def mark_as_modified(self, e):
        """Mark that changes have been made"""
        self.has_unsaved_changes = True
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle file picker result for avatar upload"""
        if e.files and len(e.files) > 0:
            file = e.files[0]
            try:
                # Read file and convert to base64
                with open(file.path, "rb") as f:
                    file_bytes = f.read()
                    self.avatar_base64 = base64.b64encode(file_bytes).decode()
                
                # Update avatar display
                self.update_avatar_display()
                self.has_unsaved_changes = True
                
                self.notification.show(
                    "Avatar uploaded successfully. Click Save Changes to apply.",
                    "success",
                    3000,
                    "Avatar Uploaded"
                )
            except Exception as ex:
                self.notification.show(
                    str(ex),
                    "error",
                    3000,
                    "Upload Failed"
                )
    
    def update_avatar_display(self):
        """Update the avatar display with new image"""
        if self.avatar_display and self.avatar_base64:
            # Update the avatar stack
            new_avatar = ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src_base64=self.avatar_base64,
                        width=96,
                        height=96,
                        fit=ft.ImageFit.COVER,
                        border_radius=50
                    ),
                    width=100,
                    height=100,
                    border_radius=50,
                    border=ft.border.all(4, ft.Colors.WHITE10)
                ),
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.CHECK_CIRCLE_ROUNDED,
                        size=16,
                        color=ft.Colors.WHITE
                    ),
                    width=32,
                    height=32,
                    border_radius=16,
                    bgcolor=ft.Colors.GREEN_600,
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, "#0D1117"),
                    right=0,
                    bottom=0
                )
            ], width=100, height=100)
            
            self.avatar_display.content = new_avatar
            self.page.update()
        
    def build(self):
        """Build the admin profile page"""
        is_mobile = self.page.width < 768
        
        # Get admin statistics
        stats = db.get_system_statistics()
        admin_logs = db.get_admin_logs(limit=5)
        
        # Calculate admin-specific stats
        total_actions = len(db.get_admin_logs(limit=1000))
        
        # Profile Header with Avatar
        avatar_container = ft.Stack([
            ft.Container(
                content=ft.Icon(
                    ft.Icons.PERSON_ROUNDED,
                    size=50,
                    color=ft.Colors.WHITE
                ) if not self.avatar_base64 else ft.Image(
                    src_base64=self.avatar_base64,
                    width=96,
                    height=96,
                    fit=ft.ImageFit.COVER,
                    border_radius=50
                ),
                width=100,
                height=100,
                border_radius=50,
                bgcolor="#0066CC",
                alignment=ft.alignment.center,
                border=ft.border.all(4, ft.Colors.WHITE10)
            ),
            ft.Container(
                content=ft.Icon(
                    ft.Icons.ADD_ROUNDED,
                    size=16,
                    color=ft.Colors.WHITE
                ),
                width=32,
                height=32,
                border_radius=16,
                bgcolor="#0066CC",
                alignment=ft.alignment.center,
                border=ft.border.all(2, "#0D1117"),
                right=0,
                bottom=0,
                on_click=lambda e: self.file_picker.pick_files(
                    allowed_extensions=["png", "jpg", "jpeg"],
                    dialog_title="Select Profile Picture"
                ),
                ink=True
            )
        ], width=100, height=100)
        
        # Store reference for updates
        self.avatar_display = ft.Container(content=avatar_container)
        
        profile_header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_size=24,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self.on_navigate("admin_dashboard")
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH_ROUNDED,
                        icon_size=24,
                        icon_color=ft.Colors.GREY_400,
                        tooltip="Refresh Statistics",
                        on_click=lambda e: self.refresh_stats()
                    ),
                ]),
                ft.Container(height=10),
                self.avatar_display,
                ft.TextButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.UPLOAD_ROUNDED, size=16, color=ft.Colors.BLUE_400),
                        ft.Text("Upload Photo", color=ft.Colors.BLUE_400, weight=ft.FontWeight.W_500)
                    ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e: self.file_picker.pick_files(
                        allowed_extensions=["png", "jpg", "jpeg"],
                        dialog_title="Select Profile Picture"
                    ),
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=20, vertical=8)
                    )
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=ft.padding.only(top=20, bottom=20),
            alignment=ft.alignment.center
        )
        
        # Account Details Section
        account_details_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Account Details",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_400
                ),
                ft.Container(height=12),
                self.full_name_field,
                ft.Container(height=12),
                self.email_field,
                ft.Container(height=12),
                self.employee_id_field,
            ], spacing=0),
            bgcolor="#2C2C2E",
            padding=20,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_800),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
        
        # Profile Settings Section
        profile_settings_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Account Details",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_400
                ),
                ft.Container(height=12),
                self.job_title_field,
                ft.Container(height=12),
                self.department_field,
                ft.Container(height=12),
                self.currency_field,
                ft.Container(height=12),
                self.reporting_manager_field,
            ], spacing=0),
            bgcolor="#2C2C2E",
            padding=20,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_800),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
        
        # Action Buttons
        action_buttons = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        "Save Changes",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.WHITE
                    ),
                    bgcolor="#0066CC",
                    padding=ft.padding.symmetric(horizontal=24, vertical=14),
                    border_radius=8,
                    on_click=self.save_changes,
                    ink=True,
                    expand=True,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Text(
                        "Cancel",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE
                    ),
                    bgcolor="#2C2C2E",
                    border=ft.border.all(1, ft.Colors.GREY_700),
                    padding=ft.padding.symmetric(horizontal=24, vertical=14),
                    border_radius=8,
                    on_click=self.cancel_changes,
                    ink=True,
                    width=120,
                    alignment=ft.alignment.center
                ),
            ], spacing=12),
            padding=ft.padding.only(bottom=16)
        )
        
        # Danger Zone Section
        danger_zone = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Danger Zone",
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.RED_400
                ),
                ft.Container(height=12),
                ft.Row([
                    ft.Container(
                        content=ft.Text(
                            "Delete Account",
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.RED_600,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        border_radius=6,
                        on_click=self.show_delete_confirmation,
                        ink=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Permanently remove admin access",
                                size=12,
                                color=ft.Colors.GREY_400,
                                weight=ft.FontWeight.W_500
                            ),
                            ft.Text(
                                "Requires IT administrator confirmation",
                                size=11,
                                color=ft.Colors.GREY_500
                            ),
                        ], spacing=2),
                        expand=True
                    )
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
            ], spacing=0),
            bgcolor="#2C2C2E",
            padding=20,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_800),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
        
        # Admin Statistics Cards
        stats_section = ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(
                            ft.Icons.PEOPLE_ROUNDED,
                            size=24,
                            color=ft.Colors.BLUE_400
                        ),
                        ft.Container(expand=True),
                        ft.Icon(
                            ft.Icons.TRENDING_UP_ROUNDED,
                            size=18,
                            color=ft.Colors.GREEN_400
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Text(
                        str(stats.get("total_users", 0)),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Total Users",
                        size=13,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=4),
                    ft.Container(
                        content=ft.Text(
                            "+12% from last month",
                            size=11,
                            color=ft.Colors.GREEN_400
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=6
                    )
                ], spacing=0),
                bgcolor="#2C2C2E",
                padding=20,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREY_800),
                col={"xs": 12, "sm": 6, "md": 4}
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(
                            ft.Icons.RECEIPT_LONG_ROUNDED,
                            size=24,
                            color=ft.Colors.ORANGE_400
                        ),
                        ft.Container(expand=True),
                        ft.Icon(
                            ft.Icons.TRENDING_UP_ROUNDED,
                            size=18,
                            color=ft.Colors.GREEN_400
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Text(
                        str(stats.get("total_expenses", 0)),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Total Expenses",
                        size=13,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=4),
                    ft.Container(
                        content=ft.Text(
                            "+8% from last month",
                            size=11,
                            color=ft.Colors.GREEN_400
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=6
                    )
                ], spacing=0),
                bgcolor="#2C2C2E",
                padding=20,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREY_800),
                col={"xs": 12, "sm": 6, "md": 4}
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(
                            ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED,
                            size=24,
                            color=ft.Colors.PURPLE_400
                        ),
                        ft.Container(expand=True),
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE_ROUNDED,
                            size=18,
                            color=ft.Colors.GREEN_400
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Text(
                        str(total_actions),
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Admin Actions",
                        size=13,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=4),
                    ft.Container(
                        content=ft.Text(
                            "All time activity",
                            size=11,
                            color=ft.Colors.GREY_500
                        ),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=6
                    )
                ], spacing=0),
                bgcolor="#2C2C2E",
                padding=20,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREY_800),
                col={"xs": 12, "sm": 12, "md": 4}
            ),
        ], spacing=16)
        
        # Responsive Layout
        if is_mobile:
            # Mobile: Single column layout
            content = ft.Column([
                profile_header,
                ft.Container(height=16),
                stats_section,
                ft.Container(height=20),
                account_details_section,
                ft.Container(height=16),
                profile_settings_section,
                ft.Container(height=16),
                action_buttons,
                ft.Container(height=16),
                danger_zone,
                ft.Container(height=30),
            ], spacing=0, scroll=ft.ScrollMode.AUTO)
        else:
            # Desktop: Two-column layout
            content = ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED,
                        icon_size=24,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self.on_navigate("admin_dashboard")
                    ),
                    ft.Text(
                        "Admin Profile",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Container(expand=True),
                ]),
                ft.Container(height=20),
                stats_section,
                ft.Container(height=24),
                ft.ResponsiveRow([
                    ft.Column([
                        profile_header,
                        ft.Container(height=20),
                        account_details_section,
                        ft.Container(height=20),
                        action_buttons,
                        ft.Container(height=20),
                        danger_zone,
                    ], col={"md": 5}),
                    ft.Column([
                        profile_settings_section,
                    ], col={"md": 7}),
                ], spacing=20),
                ft.Container(height=30),
            ], spacing=0, scroll=ft.ScrollMode.AUTO)
        
        return ft.Container(
            content=content,
            padding=ft.padding.all(16 if is_mobile else 24),
            bgcolor="#0D1117",
            expand=True
        )
    
    def save_changes(self, e):
        """Save profile changes to database"""
        if not self.has_unsaved_changes:
            self.notification.show(
                "Make some changes first",
                "info",
                3000,
                "No Changes to Save"
            )
            return
        
        try:
            # Prepare update data
            full_name = self.full_name_field.value
            email = self.email_field.value
            job_title = self.job_title_field.value
            department = self.department_field.value
            currency = self.currency_field.value
            reporting_manager = self.reporting_manager_field.value
            avatar = self.avatar_base64 if self.avatar_base64 else None
            
            # Update in database
            db.update_admin_profile(
                self.admin_id,
                full_name=full_name,
                email=email,
                job_title=job_title,
                department=department,
                currency=currency,
                reporting_manager=reporting_manager,
                avatar=avatar
            )
            
            # Update state
            self.admin_data["full_name"] = full_name
            self.admin_data["email"] = email
            self.admin_data["job_title"] = job_title
            self.admin_data["department"] = department
            self.admin_data["currency"] = currency
            self.admin_data["reporting_manager"] = reporting_manager
            if avatar:
                self.admin_data["avatar"] = avatar
            
            # Log the admin action
            db.log_admin_activity(
                self.admin_id,
                "update_profile",
                None,
                f"Updated profile settings"
            )
            
            self.has_unsaved_changes = False
            
            self.notification.show(
                "Your changes have been saved",
                "success",
                3000,
                "Profile Updated"
            )
            
        except Exception as ex:
            self.notification.show(
                f"Error: {str(ex)}",
                "error",
                3000,
                "Save Failed"
            )
    
    def cancel_changes(self, e):
        """Cancel changes and return to dashboard"""
        if self.has_unsaved_changes:
            # Show confirmation dialog
            def confirm_cancel(e):
                self.page.close(dialog)
                self.on_navigate("admin_dashboard")
            
            def stay(e):
                self.page.close(dialog)
            
            dialog = ft.AlertDialog(
                title=ft.Text("Unsaved Changes", color=ft.Colors.WHITE),
                content=ft.Text(
                    "You have unsaved changes. Are you sure you want to leave?",
                    color=ft.Colors.WHITE70
                ),
                actions=[
                    ft.TextButton("Stay", on_click=stay),
                    ft.TextButton(
                        "Leave",
                        on_click=confirm_cancel,
                        style=ft.ButtonStyle(color=ft.Colors.RED_400)
                    ),
                ],
                bgcolor="#2C2C2E"
            )
            self.page.open(dialog)
        else:
            self.on_navigate("admin_dashboard")
    
    def refresh_stats(self):
        """Refresh statistics"""
        self.notification.show(
            "Latest data loaded",
            "info",
            2000,
            "Statistics Refreshed"
        )
        # Rebuild the page to get fresh stats
        self.page.update()
    
    def show_delete_confirmation(self, e):
        """Show account deletion confirmation dialog"""
        def confirm_delete(e):
            self.page.close(dialog)
            self.delete_account()
        
        def cancel_delete(e):
            self.page.close(dialog)
        
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.RED_400, size=28),
                ft.Text("Delete Admin Account?", color=ft.Colors.RED_400)
            ], spacing=10),
            content=ft.Column([
                ft.Text(
                    "This action cannot be undone!",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(height=8),
                ft.Text(
                    "Deleting your admin account will:",
                    color=ft.Colors.WHITE70,
                    size=13
                ),
                ft.Text("• Remove all your admin privileges", color=ft.Colors.WHITE70, size=12),
                ft.Text("• Delete your activity logs", color=ft.Colors.WHITE70, size=12),
                ft.Text("• Require IT to restore access", color=ft.Colors.WHITE70, size=12),
                ft.Container(height=12),
                ft.Text(
                    "Type 'DELETE' to confirm:",
                    color=ft.Colors.WHITE70,
                    size=13
                ),
                ft.TextField(
                    hint_text="DELETE",
                    border_color=ft.Colors.RED_400,
                    on_change=lambda e: setattr(confirm_btn, "disabled", e.control.value != "DELETE") or self.page.update()
                )
            ], spacing=4, tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.TextButton(
                    "Delete Account",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_600
                    ),
                    disabled=True,
                    ref=ft.Ref[ft.TextButton]()
                ),
            ],
            bgcolor="#2C2C2E"
        )
        
        confirm_btn = dialog.actions[1]
        self.page.open(dialog)
    
    def delete_account(self):
        """Delete admin account (restricted)"""
        self.notification.show(
            "Please contact IT administrator to delete admin accounts",
            "warning",
            4000,
            "Action Restricted"
        )
