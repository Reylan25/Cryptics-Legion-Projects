"""
Admin Policy Rules Management Page
Configure expense policy rules and constraints
"""

import flet as ft
from core import db


class AdminPolicyRulesPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.rules = []
        self.categories = []
        
    def build(self):
        """Build policy rules management page"""
        
        # Initialize tables
        db.init_admin_config_tables()
        
        # Load data
        self.load_rules()
        self.load_categories()
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Policy Rules",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Configure expense policies, limits, and constraints",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                ], spacing=4),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED, size=18),
                        ft.Text("Add Rule", size=14, weight=ft.FontWeight.W_500)
                    ], spacing=8),
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=self.show_add_dialog
                )
            ]),
            padding=20,
            bgcolor="#2D2D30",
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_800))
        )
        
        # Rules Table
        self.rules_table = self.create_rules_table()
        
        # Main content
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    self.rules_table
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=20
            )
        ], spacing=0, expand=True)
        
        return content
    
    def load_rules(self):
        """Load policy rules from database"""
        self.rules = db.get_policy_rules(include_inactive=True)
    
    def load_categories(self):
        """Load expense categories"""
        self.categories = db.get_expense_categories()
    
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
    
    def show_add_dialog(self, e):
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
                self.rules_table = self.create_rules_table()
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
        """Show edit rule dialog"""
        
        rule_id, rule_name, rule_type, category_id, category_name, max_amount, currency, \
        requires_receipt, requires_approval, disallowed_vendors, per_diem_rate, description, \
        is_active, created_at, updated_at = rule
        
        # Similar dialog to add but with pre-filled values
        # Implementation similar to show_add_dialog but with update logic
        pass
    
    def confirm_delete(self, rule):
        """Confirm rule deletion"""
        
        rule_id, rule_name = rule[0], rule[1]
        
        def handle_delete(e):
            success = db.delete_policy_rule(rule_id)
            if success:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Policy rule deleted successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_rules()
                self.rules_table = self.create_rules_table()
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
