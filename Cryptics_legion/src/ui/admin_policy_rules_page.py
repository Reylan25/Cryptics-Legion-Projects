"""
Admin Policy Rules Management Page
Configure expense policy rules, announcements, and user notifications
"""

import flet as ft
from core import db
from datetime import datetime, timedelta
from components.notification import ImmersiveNotification


class AdminPolicyRulesPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.rules = []
        self.categories = []
        self.announcements = []
        self.current_tab = "rules"
        self.notification = ImmersiveNotification(page)
        
    def build(self):
        """Build policy rules and announcements management page"""
        
        # Initialize tables
        db.init_admin_config_tables()
        
        # Load data
        self.load_rules()
        self.load_categories()
        self.load_announcements()
        
        # Header with tabs
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(
                            "Policy & Communications",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Manage expense policies and system announcements",
                            size=14,
                            color=ft.Colors.GREY_400
                        ),
                    ], spacing=4),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SHIELD_OUTLINED, size=20, color=ft.Colors.BLUE_400),
                            ft.Text(f"{len(self.rules)} Rules", size=14, weight=ft.FontWeight.W_500),
                        ], spacing=8),
                        bgcolor="#1E1E1E",
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        border_radius=20,
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CAMPAIGN_OUTLINED, size=20, color=ft.Colors.ORANGE_400),
                            ft.Text(f"{len(self.announcements)} Announcements", size=14, weight=ft.FontWeight.W_500),
                        ], spacing=8),
                        bgcolor="#1E1E1E",
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        border_radius=20,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=20),
                # Tabs
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.RULE_FOLDER_OUTLINED, size=20),
                            ft.Text("Policy Rules", size=15, weight=ft.FontWeight.W_500),
                        ], spacing=10),
                        bgcolor=ft.Colors.BLUE_700 if self.current_tab == "rules" else "#2C2C2E",
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        border_radius=10,
                        on_click=lambda e: self.switch_tab("rules"),
                        ink=True,
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ANNOUNCEMENT_OUTLINED, size=20),
                            ft.Text("Announcements", size=15, weight=ft.FontWeight.W_500),
                        ], spacing=10),
                        bgcolor=ft.Colors.BLUE_700 if self.current_tab == "announcements" else "#2C2C2E",
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        border_radius=10,
                        on_click=lambda e: self.switch_tab("announcements"),
                        ink=True,
                    ),
                ], spacing=12),
            ], spacing=0),
            padding=20,
            bgcolor="#2D2D30",
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_800))
        )
        
        # Content area
        self.content_container = ft.Container(
            content=self.get_tab_content(),
            expand=True,
            padding=20
        )
        
        # Main layout
        return ft.Column([
            header,
            self.content_container
        ], spacing=0, expand=True)
    
    def switch_tab(self, tab_name):
        """Switch between tabs"""
        self.current_tab = tab_name
        self.content_container.content = self.get_tab_content()
        self.page.update()
    
    def get_tab_content(self):
        """Get content for current tab"""
        if self.current_tab == "rules":
            return self.build_rules_tab()
        else:
            return self.build_announcements_tab()
    
    def get_tab_content(self):
        """Get content for current tab"""
        if self.current_tab == "rules":
            return self.build_rules_tab()
        else:
            return self.build_announcements_tab()
    
    def build_rules_tab(self):
        """Build policy rules tab content"""
        # Action buttons
        action_row = ft.Row([
            ft.Container(expand=True),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.ADD_ROUNDED, size=18),
                    ft.Text("Add Rule", size=14, weight=ft.FontWeight.W_500)
                ], spacing=8),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                on_click=self.show_add_rule_dialog
            )
        ], spacing=12)
        
        # Rules content
        rules_content = self.create_rules_table()
        
        return ft.Column([
            action_row,
            ft.Container(height=20),
            rules_content
        ], scroll=ft.ScrollMode.AUTO)
    
    def build_announcements_tab(self):
        """Build announcements tab content"""
        # Action buttons
        action_row = ft.Row([
            ft.Container(expand=True),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.CAMPAIGN_ROUNDED, size=18),
                    ft.Text("Create Announcement", size=14, weight=ft.FontWeight.W_500)
                ], spacing=8),
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
                on_click=self.show_add_announcement_dialog
            )
        ], spacing=12)
        
        # Announcements grid
        announcements_grid = self.create_announcements_grid()
        
        return ft.Column([
            action_row,
            ft.Container(height=20),
            announcements_grid
        ], scroll=ft.ScrollMode.AUTO)
    
    def load_announcements(self):
        """Load announcements from database"""
        self.announcements = db.get_announcements(include_inactive=True)
    
    def load_announcements(self):
        """Load announcements from database"""
        self.announcements = db.get_announcements(include_inactive=True)
    
    def load_rules(self):
        """Load policy rules from database"""
        self.rules = db.get_policy_rules(include_inactive=True)
    
    def load_rules(self):
        """Load policy rules from database"""
        self.rules = db.get_policy_rules(include_inactive=True)
    
    def load_categories(self):
        """Load expense categories"""
        self.categories = db.get_expense_categories()
    
    def create_announcements_grid(self):
        """Create announcements grid view"""
        if not self.announcements:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CAMPAIGN_OUTLINED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No announcements yet",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_500
                    ),
                    ft.Text(
                        "Create your first announcement to notify all users",
                        size=14,
                        color=ft.Colors.GREY_600
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=80,
                alignment=ft.alignment.center
            )
        
        cards = []
        for announcement in self.announcements:
            ann_id, title, message, ann_type, priority, admin_id, admin_username, \
            target_users, start_date, end_date, is_active, is_pinned, \
            created_at, updated_at, notification_count, read_count = announcement
            
            # Type icon and color
            type_icons = {
                'info': (ft.Icons.INFO_OUTLINE, ft.Colors.BLUE_400),
                'warning': (ft.Icons.WARNING_AMBER_OUTLINED, ft.Colors.ORANGE_400),
                'success': (ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Colors.GREEN_400),
                'urgent': (ft.Icons.PRIORITY_HIGH_ROUNDED, ft.Colors.RED_400),
            }
            icon, color = type_icons.get(ann_type, (ft.Icons.INFO_OUTLINE, ft.Colors.BLUE_400))
            
            # Priority badge
            priority_badge = None
            if priority == 'high':
                priority_badge = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color=ft.Colors.AMBER_400),
                        ft.Text("HIGH PRIORITY", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)
                    ], spacing=4),
                    bgcolor="#332A00",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=6,
                    border=ft.border.all(1, ft.Colors.AMBER_800)
                )
            
            # Read statistics
            read_percentage = (read_count / notification_count * 100) if notification_count > 0 else 0
            
            card = ft.Container(
                content=ft.Column([
                    # Header
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(icon, size=24, color=color),
                            bgcolor=f"{color}20",
                            padding=10,
                            border_radius=8
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Icon(ft.Icons.PUSH_PIN_ROUNDED, size=16, color=ft.Colors.AMBER_400) if is_pinned else ft.Container(),
                            ], spacing=8),
                            ft.Text(
                                f"by {admin_username or 'System'} • {self.format_date(created_at)}",
                                size=12,
                                color=ft.Colors.GREY_500
                            ),
                        ], spacing=2, expand=True),
                        priority_badge if priority_badge else ft.Container(),
                    ], spacing=12),
                    
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    
                    # Message preview
                    ft.Text(
                        message[:150] + "..." if len(message) > 150 else message,
                        size=13,
                        color=ft.Colors.GREY_400,
                        max_lines=3,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    
                    # Statistics
                    ft.Container(
                        content=ft.Row([
                            ft.Row([
                                ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color=ft.Colors.BLUE_400),
                                ft.Text(
                                    f"{notification_count} recipients",
                                    size=12,
                                    color=ft.Colors.GREY_400
                                ),
                            ], spacing=6),
                            ft.Row([
                                ft.Icon(ft.Icons.VISIBILITY_OUTLINED, size=16, color=ft.Colors.GREEN_400),
                                ft.Text(
                                    f"{read_count} read ({read_percentage:.0f}%)",
                                    size=12,
                                    color=ft.Colors.GREY_400
                                ),
                            ], spacing=6),
                            ft.Container(
                                content=ft.Text(
                                    "Active" if is_active else "Inactive",
                                    size=11,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.GREEN_700 if is_active else ft.Colors.GREY_700,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.only(top=8)
                    ),
                    
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    
                    # Actions
                    ft.Row([
                        ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.VISIBILITY_OUTLINED, size=16),
                                ft.Text("View Details", size=13)
                            ], spacing=6),
                            on_click=lambda e, a=announcement: self.show_announcement_details(a)
                        ),
                        ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.EDIT_OUTLINED, size=16),
                                ft.Text("Edit", size=13)
                            ], spacing=6),
                            on_click=lambda e, a=announcement: self.show_edit_announcement_dialog(a)
                        ),
                        ft.TextButton(
                            content=ft.Row([
                                ft.Icon(ft.Icons.DELETE_OUTLINE, size=16, color=ft.Colors.RED_400),
                                ft.Text("Delete", size=13, color=ft.Colors.RED_400)
                            ], spacing=6),
                            on_click=lambda e, a=announcement: self.confirm_delete_announcement(a)
                        ),
                    ], spacing=0),
                ], spacing=12),
                bgcolor="#2C2C2E",
                padding=20,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREY_800),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2)
                )
            )
            
            cards.append(card)
        
        return ft.Column(cards, spacing=16)
        """Create rules data table"""
        
        if not self.rules:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.RULE_FOLDER_OUTLINED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No policy rules yet",
                        size=16,
                        color=ft.Colors.GREY_500
                    ),
                    ft.Text(
                        "Click 'Add Rule' to create your first policy rule",
                        size=13,
                        color=ft.Colors.GREY_600
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=50,
                alignment=ft.alignment.center
            )
        
        rows = []
        for rule in self.rules:
            rule_id, rule_name, rule_type, category_id, category_name, max_amount, currency, \
            requires_receipt, requires_approval, disallowed_vendors, per_diem_rate, description, \
            is_active, created_at, updated_at = rule
            
            # Build constraint details
            constraints = []
            if max_amount:
                constraints.append(f"Max: {currency} {max_amount:,.2f}")
            if per_diem_rate:
                constraints.append(f"Per Diem: {currency} {per_diem_rate:,.2f}")
            if requires_receipt:
                constraints.append("Receipt Required")
            if disallowed_vendors:
                constraints.append("Vendor Restrictions")
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Column([
                                ft.Text(rule_name, size=13, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                                ft.Text(
                                    rule_type.replace("_", " ").title(),
                                    size=11,
                                    color=ft.Colors.BLUE_400
                                ),
                            ], spacing=2)
                        ),
                        ft.DataCell(
                            ft.Text(category_name or "All Categories", size=12, color=ft.Colors.GREY_400)
                        ),
                        ft.DataCell(
                            ft.Column([
                                ft.Text(c, size=11, color=ft.Colors.GREY_400)
                                for c in constraints[:2]
                            ] if constraints else [ft.Text("-", size=11, color=ft.Colors.GREY_500)], spacing=2)
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "Active" if is_active else "Inactive",
                                    size=11,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.GREEN_700 if is_active else ft.Colors.GREY_700,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_size=18,
                                    icon_color=ft.Colors.BLUE_400,
                                    tooltip="Edit",
                                    on_click=lambda e, r=rule: self.show_edit_dialog(r)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Delete",
                                    on_click=lambda e, r=rule: self.confirm_delete(r)
                                ),
                            ], spacing=0)
                        ),
                    ],
                    data=rule
                )
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Rule Name", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Category", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Constraints", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Status", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Actions", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_800),
            border_radius=10,
            bgcolor="#2C2C2E",
            heading_row_color="#232325",
            data_row_color={"hovered": "#383838"},
        )
        
        return ft.Container(content=table, border_radius=10)
    
    def format_date(self, date_str):
        """Format date string to relative time"""
        if not date_str:
            return "Unknown"
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = now - date
            
            if diff.days == 0:
                if diff.seconds < 3600:
                    return f"{diff.seconds // 60}m ago"
                return f"{diff.seconds // 3600}h ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days}d ago"
            else:
                return date.strftime("%b %d, %Y")
        except:
            return date_str
    
    def show_add_rule_dialog(self, e):
        """Show add rule dialog"""
        
        rule_name_field = ft.TextField(
            label="Rule Name",
            hint_text="e.g., Travel Expense Limit, Meal Allowance",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        rule_type_dropdown = ft.Dropdown(
            label="Rule Type",
            options=[
                ft.dropdown.Option("spending_limit", "Spending Limit"),
                ft.dropdown.Option("per_diem", "Per Diem Rate"),
                ft.dropdown.Option("receipt_required", "Receipt Required"),
                ft.dropdown.Option("approval_required", "Approval Required"),
                ft.dropdown.Option("vendor_restriction", "Vendor Restriction"),
            ],
            value="spending_limit",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        category_dropdown = ft.Dropdown(
            label="Category (Optional)",
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in self.categories],
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        max_amount_field = ft.TextField(
            label="Maximum Amount",
            hint_text="e.g., 5000",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        currency_field = ft.TextField(
            label="Currency",
            value="PHP",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        per_diem_field = ft.TextField(
            label="Per Diem Rate",
            hint_text="e.g., 1500",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        receipt_switch = ft.Switch(
            label="Receipt Required",
            value=False,
            active_color=ft.Colors.GREEN_400
        )
        
        approval_switch = ft.Switch(
            label="Approval Required",
            value=True,
            active_color=ft.Colors.GREEN_400
        )
        
        vendors_field = ft.TextField(
            label="Disallowed Vendors (comma-separated)",
            hint_text="e.g., Vendor1, Vendor2",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True
        )
        
        description_field = ft.TextField(
            label="Description",
            hint_text="Rule description",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True,
            min_lines=2
        )
        
        def handle_add(e):
            if not rule_name_field.value:
                rule_name_field.error_text = "Rule name is required"
                rule_name_field.update()
                return
            
            rule_id = db.add_policy_rule(
                rule_name=rule_name_field.value,
                rule_type=rule_type_dropdown.value,
                category_id=int(category_dropdown.value) if category_dropdown.value else None,
                max_amount=float(max_amount_field.value) if max_amount_field.value else None,
                currency=currency_field.value,
                requires_receipt=1 if receipt_switch.value else 0,
                requires_approval=1 if approval_switch.value else 0,
                disallowed_vendors=vendors_field.value or "",
                per_diem_rate=float(per_diem_field.value) if per_diem_field.value else None,
                description=description_field.value or ""
            )
            
            if rule_id:
                self.page.close(dialog)
                # Show immersive notification
                self.notification.show(
                    message=f"Policy rule '{rule_name_field.value}' has been created successfully!",
                    type="success",
                    title="Rule Created"
                )
                self.load_rules()
                self.content_container.content = self.get_tab_content()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Policy Rule", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    rule_name_field,
                    rule_type_dropdown,
                    category_dropdown,
                    ft.Row([
                        ft.Container(content=max_amount_field, expand=True),
                        ft.Container(content=currency_field, width=100),
                    ], spacing=12),
                    per_diem_field,
                    ft.Row([receipt_switch, approval_switch], spacing=20),
                    vendors_field,
                    description_field,
                ], spacing=16, tight=True, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=600,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Add Rule",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def create_rules_table(self):
        """Create rules data table"""
        
        if not self.rules:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.RULE_FOLDER_OUTLINED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No policy rules yet",
                        size=16,
                        color=ft.Colors.GREY_500
                    ),
                    ft.Text(
                        "Click 'Add Rule' to create your first policy rule",
                        size=13,
                        color=ft.Colors.GREY_600
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=50,
                alignment=ft.alignment.center
            )
        
        rows = []
        for rule in self.rules:
            rule_id, rule_name, rule_type, category_id, category_name, max_amount, currency, \
            requires_receipt, requires_approval, disallowed_vendors, per_diem_rate, description, \
            is_active, created_at, updated_at = rule
            
            # Build constraint details
            constraints = []
            if max_amount:
                constraints.append(f"Max: {currency} {max_amount:,.2f}")
            if per_diem_rate:
                constraints.append(f"Per Diem: {currency} {per_diem_rate:,.2f}")
            if requires_receipt:
                constraints.append("Receipt Required")
            if disallowed_vendors:
                constraints.append("Vendor Restrictions")
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Column([
                                ft.Text(rule_name, size=13, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                                ft.Text(
                                    rule_type.replace("_", " ").title(),
                                    size=11,
                                    color=ft.Colors.BLUE_400
                                ),
                            ], spacing=2)
                        ),
                        ft.DataCell(
                            ft.Text(category_name or "All Categories", size=12, color=ft.Colors.GREY_400)
                        ),
                        ft.DataCell(
                            ft.Column([
                                ft.Text(c, size=11, color=ft.Colors.GREY_400)
                                for c in constraints[:2]
                            ] if constraints else [ft.Text("-", size=11, color=ft.Colors.GREY_500)], spacing=2)
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    "Active" if is_active else "Inactive",
                                    size=11,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.GREEN_700 if is_active else ft.Colors.GREY_700,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12
                            )
                        ),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_size=18,
                                    icon_color=ft.Colors.BLUE_400,
                                    tooltip="Edit",
                                    on_click=lambda e, r=rule: self.show_edit_dialog(r)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Delete",
                                    on_click=lambda e, r=rule: self.confirm_delete(r)
                                ),
                            ], spacing=0)
                        ),
                    ],
                    data=rule
                )
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Rule Name", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Category", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Constraints", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Status", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Actions", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_800),
            border_radius=10,
            bgcolor="#2C2C2E",
            heading_row_color="#232325",
            data_row_color={"hovered": "#383838"},
        )
        
        return ft.Container(content=table, border_radius=10)
    
    def show_add_announcement_dialog(self, e):
        """Show add announcement dialog"""
        
        title_field = ft.TextField(
            label="Announcement Title",
            hint_text="e.g., System Maintenance, Policy Update",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        message_field = ft.TextField(
            label="Message",
            hint_text="Enter announcement message",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True,
            min_lines=5,
            max_lines=10
        )
        
        type_dropdown = ft.Dropdown(
            label="Type",
            options=[
                ft.dropdown.Option("info", "Information"),
                ft.dropdown.Option("warning", "Warning"),
                ft.dropdown.Option("success", "Success"),
                ft.dropdown.Option("urgent", "Urgent"),
            ],
            value="info",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        priority_dropdown = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option("normal", "Normal"),
                ft.dropdown.Option("high", "High Priority"),
            ],
            value="normal",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        target_dropdown = ft.Dropdown(
            label="Target Audience",
            options=[
                ft.dropdown.Option("all", "All Users"),
                ft.dropdown.Option("specific", "Specific Users (comma-separated IDs)"),
            ],
            value="all",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        target_ids_field = ft.TextField(
            label="User IDs (if specific)",
            hint_text="e.g., 1,2,3",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True,
            visible=False
        )
        
        # Preview of recipients
        recipients_preview = ft.Container(
            visible=True,
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.BLUE_400),
                ft.Text(
                    f"Will notify: All registered users ({len(db.get_all_users_for_admin())} users)",
                    size=12,
                    color=ft.Colors.BLUE_400
                )
            ], spacing=8),
            bgcolor="#1A2332",
            padding=12,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_800)
        )
        
        def on_target_change(e):
            target_ids_field.visible = target_dropdown.value == "specific"
            
            # Update recipients preview
            if target_dropdown.value == "all":
                total_users = len(db.get_all_users_for_admin())
                recipients_preview.content = ft.Row([
                    ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=16, color=ft.Colors.BLUE_400),
                    ft.Text(
                        f"Will notify: All registered users ({total_users} user{'s' if total_users != 1 else ''})",
                        size=12,
                        color=ft.Colors.BLUE_400
                    )
                ], spacing=8)
            else:
                recipients_preview.content = ft.Row([
                    ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=ft.Colors.ORANGE_400),
                    ft.Text(
                        "Will notify: Specific users (enter IDs above)",
                        size=12,
                        color=ft.Colors.ORANGE_400
                    )
                ], spacing=8)
            
            target_ids_field.update()
            recipients_preview.update()
        
        target_dropdown.on_change = on_target_change
        
        end_date_field = ft.TextField(
            label="End Date (optional, YYYY-MM-DD HH:MM:SS)",
            hint_text="Leave empty for no expiry",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        pinned_switch = ft.Switch(
            label="Pin to Top",
            value=False,
            active_color=ft.Colors.AMBER_400
        )
        
        def handle_add(e):
            if not title_field.value or not message_field.value:
                title_field.error_text = "Title is required" if not title_field.value else None
                message_field.error_text = "Message is required" if not message_field.value else None
                title_field.update()
                message_field.update()
                return
            
            target_users = "all" if target_dropdown.value == "all" else target_ids_field.value
            admin_id = self.state.get("admin_id")
            
            announcement_id = db.add_announcement(
                title=title_field.value,
                message=message_field.value,
                type=type_dropdown.value,
                priority=priority_dropdown.value,
                admin_id=admin_id,
                target_users=target_users,
                end_date=end_date_field.value if end_date_field.value else None,
                is_pinned=1 if pinned_switch.value else 0
            )
            
            if announcement_id:
                self.page.close(dialog)
                # Get notification count for feedback
                users_notified = db.get_all_users_for_admin()
                total_users = len(users_notified) if target_users == "all" else len([uid for uid in target_users.split(',') if uid.strip()])
                
                # Show immersive notification
                self.notification.show(
                    message=f"Announcement sent to {total_users} user(s). They will see it in their notification center!",
                    type="success",
                    title="📢 Announcement Sent",
                    duration=5000
                )
                self.load_announcements()
                self.content_container.content = self.get_tab_content()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.CAMPAIGN_ROUNDED, color=ft.Colors.ORANGE_400),
                ft.Text("Create Announcement", weight=ft.FontWeight.BOLD),
            ], spacing=10),
            content=ft.Container(
                content=ft.Column([
                    title_field,
                    message_field,
                    ft.Row([
                        ft.Container(content=type_dropdown, expand=True),
                        ft.Container(content=priority_dropdown, expand=True),
                    ], spacing=12),
                    target_dropdown,
                    target_ids_field,
                    recipients_preview,
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    end_date_field,
                    pinned_switch,
                ], spacing=16, tight=True, scroll=ft.ScrollMode.AUTO),
                width=600,
                height=550,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SEND_ROUNDED, size=18),
                        ft.Text("Send Announcement")
                    ], spacing=8),
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def show_announcement_details(self, announcement):
        """Show detailed announcement view"""
        ann_id, title, message, ann_type, priority, admin_id, admin_username, \
        target_users, start_date, end_date, is_active, is_pinned, \
        created_at, updated_at, notification_count, read_count = announcement
        
        read_percentage = (read_count / notification_count * 100) if notification_count > 0 else 0
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ANNOUNCEMENT_ROUNDED, color=ft.Colors.ORANGE_400),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=18),
            ], spacing=10),
            content=ft.Container(
                content=ft.Column([
                    # Message
                    ft.Container(
                        content=ft.Text(message, size=14, color=ft.Colors.WHITE),
                        bgcolor="#1E1E1E",
                        padding=16,
                        border_radius=8
                    ),
                    
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    
                    # Details
                    ft.Column([
                        self.create_detail_row("Type", ann_type.title()),
                        self.create_detail_row("Priority", priority.title()),
                        self.create_detail_row("Created By", admin_username or "System"),
                        self.create_detail_row("Created At", created_at),
                        self.create_detail_row("Target", "All Users" if target_users == "all" else f"{target_users} (IDs)"),
                        self.create_detail_row("Status", "Active" if is_active else "Inactive"),
                        self.create_detail_row("Pinned", "Yes" if is_pinned else "No"),
                    ], spacing=8),
                    
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    
                    # Statistics
                    ft.Text("Delivery Statistics", size=15, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(notification_count), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                                ft.Text("Sent", size=12, color=ft.Colors.GREY_400),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                            bgcolor="#1E1E1E",
                            padding=16,
                            border_radius=8,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(read_count), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                                ft.Text("Read", size=12, color=ft.Colors.GREY_400),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                            bgcolor="#1E1E1E",
                            padding=16,
                            border_radius=8,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"{read_percentage:.0f}%", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400),
                                ft.Text("Read Rate", size=12, color=ft.Colors.GREY_400),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                            bgcolor="#1E1E1E",
                            padding=16,
                            border_radius=8,
                            expand=True
                        ),
                    ], spacing=12),
                ], spacing=16, scroll=ft.ScrollMode.AUTO),
                width=600,
                height=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.page.close(dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def create_detail_row(self, label, value):
        """Create a detail row for announcement details"""
        return ft.Row([
            ft.Text(f"{label}:", size=13, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_400, width=120),
            ft.Text(str(value), size=13, color=ft.Colors.WHITE),
        ], spacing=12)
    
    def show_edit_announcement_dialog(self, announcement):
        """Show edit announcement dialog"""
        ann_id = announcement[0]
        title = announcement[1]
        message = announcement[2]
        
        # Similar to add dialog but with pre-filled values and update logic
        # Implementation here...
        pass
    
    def confirm_delete_announcement(self, announcement):
        """Confirm announcement deletion"""
        ann_id, title = announcement[0], announcement[1]
        
        def handle_delete(e):
            success = db.delete_announcement(ann_id)
            if success:
                self.page.close(dialog)
                self.notification.show(
                    message=f"Announcement '{title}' and all related notifications have been deleted.",
                    type="warning",
                    title="Announcement Deleted"
                )
                self.load_announcements()
                self.content_container.content = self.get_tab_content()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Announcement", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete '{title}'? All associated notifications will also be deleted."),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Delete",
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_delete
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def show_add_rule_dialog(self, e):
        """Show edit rule dialog"""
        
        rule_id, rule_name, rule_type, category_id, category_name, max_amount, currency, \
        requires_receipt, requires_approval, disallowed_vendors, per_diem_rate, description, \
        is_active, created_at, updated_at = rule
        
        # Similar dialog to add but with pre-filled values
        # Implementation similar to show_add_dialog but with update logic
        pass
    
    def show_add_rule_dialog(self, e):
        """Show add rule dialog"""
        
        rule_name_field = ft.TextField(
            label="Rule Name",
            hint_text="e.g., Travel Expense Limit, Meal Allowance",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        rule_type_dropdown = ft.Dropdown(
            label="Rule Type",
            options=[
                ft.dropdown.Option("spending_limit", "Spending Limit"),
                ft.dropdown.Option("per_diem", "Per Diem Rate"),
                ft.dropdown.Option("receipt_required", "Receipt Required"),
                ft.dropdown.Option("approval_required", "Approval Required"),
                ft.dropdown.Option("vendor_restriction", "Vendor Restriction"),
            ],
            value="spending_limit",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        category_dropdown = ft.Dropdown(
            label="Category (Optional)",
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in self.categories],
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        max_amount_field = ft.TextField(
            label="Maximum Amount",
            hint_text="e.g., 5000",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        currency_field = ft.TextField(
            label="Currency",
            value="PHP",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        per_diem_field = ft.TextField(
            label="Per Diem Rate",
            hint_text="e.g., 1500",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        receipt_switch = ft.Switch(
            label="Receipt Required",
            value=False,
            active_color=ft.Colors.GREEN_400
        )
        
        approval_switch = ft.Switch(
            label="Approval Required",
            value=True,
            active_color=ft.Colors.GREEN_400
        )
        
        vendors_field = ft.TextField(
            label="Disallowed Vendors (comma-separated)",
            hint_text="e.g., Vendor1, Vendor2",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True
        )
        
        description_field = ft.TextField(
            label="Description",
            hint_text="Rule description",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True,
            min_lines=2
        )
        
        def handle_add(e):
            if not rule_name_field.value:
                rule_name_field.error_text = "Rule name is required"
                rule_name_field.update()
                return
            
            rule_id = db.add_policy_rule(
                rule_name=rule_name_field.value,
                rule_type=rule_type_dropdown.value,
                category_id=int(category_dropdown.value) if category_dropdown.value else None,
                max_amount=float(max_amount_field.value) if max_amount_field.value else None,
                currency=currency_field.value,
                requires_receipt=1 if receipt_switch.value else 0,
                requires_approval=1 if approval_switch.value else 0,
                disallowed_vendors=vendors_field.value or "",
                per_diem_rate=float(per_diem_field.value) if per_diem_field.value else None,
                description=description_field.value or ""
            )
            
            if rule_id:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Policy rule added successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_rules()
                self.content_container.content = self.get_tab_content()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Policy Rule", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    rule_name_field,
                    rule_type_dropdown,
                    category_dropdown,
                    ft.Row([
                        ft.Container(content=max_amount_field, expand=True),
                        ft.Container(content=currency_field, width=100),
                    ], spacing=12),
                    per_diem_field,
                    ft.Row([receipt_switch, approval_switch], spacing=20),
                    vendors_field,
                    description_field,
                ], spacing=16, tight=True, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=600,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Add Rule",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def show_edit_dialog(self, rule):
        """Confirm rule deletion"""
        
        rule_id, rule_name = rule[0], rule[1]
        
        def handle_delete(e):
            success = db.delete_policy_rule(rule_id)
            if success:
                self.page.close(dialog)
                self.notification.show(
                    message=f"Policy rule '{rule_name}' has been deleted.",
                    type="info",
                    title="Rule Deleted"
                )
                self.load_rules()
                self.content_container.content = self.get_tab_content()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Policy Rule", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete '{rule_name}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Delete",
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_delete
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
