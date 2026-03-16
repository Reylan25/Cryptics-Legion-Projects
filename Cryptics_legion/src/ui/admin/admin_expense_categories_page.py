"""
Admin Expense Categories Management Page
CRUD operations for expense categories with GL codes
"""

import flet as ft
from core import db


class AdminExpenseCategoriesPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.categories = []
        self.selected_category = None
        
    def build(self):
        """Build expense categories management page"""
        
        # Initialize tables
        db.init_admin_config_tables()
        
        # Load categories
        self.load_categories()
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Expense Categories",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Manage expense categories and GL codes",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                ], spacing=4),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED, size=18),
                        ft.Text("Add Category", size=14, weight=ft.FontWeight.W_500)
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
        
        # Categories Table
        self.categories_table = self.create_categories_table()
        
        # Main content
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    self.categories_table
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=20
            )
        ], spacing=0, expand=True)
        
        return content
    
    def load_categories(self):
        """Load categories from database"""
        self.categories = db.get_expense_categories(include_inactive=True)
    
    def create_categories_table(self):
        """Create categories data table"""
        
        if not self.categories:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CATEGORY_OUTLINED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No categories yet",
                        size=16,
                        color=ft.Colors.GREY_500
                    ),
                    ft.Text(
                        "Click 'Add Category' to create your first expense category",
                        size=13,
                        color=ft.Colors.GREY_600
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=50,
                alignment=ft.alignment.center
            )
        
        rows = []
        for cat in self.categories:
            cat_id, name, description, gl_code, icon, color, is_active, parent_id, created_at, updated_at = cat
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row([
                                ft.Container(
                                    content=ft.Icon(icon if icon else ft.Icons.CATEGORY, size=16, color=color or ft.Colors.BLUE_400),
                                    bgcolor=f"{color or '#2196F3'}20",
                                    border_radius=6,
                                    padding=6
                                ),
                                ft.Column([
                                    ft.Text(name, size=13, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                                    ft.Text(description or "No description", size=11, color=ft.Colors.GREY_500),
                                ], spacing=2)
                            ], spacing=12)
                        ),
                        ft.DataCell(ft.Text(gl_code or "-", size=13, color=ft.Colors.GREY_400)),
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
                                    on_click=lambda e, c=cat: self.show_edit_dialog(c)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Delete",
                                    on_click=lambda e, c=cat: self.confirm_delete(c)
                                ),
                            ], spacing=0)
                        ),
                    ],
                    data=cat
                )
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Category", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("GL Code", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
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
        
        return ft.Container(
            content=table,
            border_radius=10
        )
    
    def show_add_dialog(self, e):
        """Show add category dialog"""
        
        name_field = ft.TextField(
            label="Category Name",
            hint_text="e.g., Travel, Meals, Office Supplies",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        description_field = ft.TextField(
            label="Description",
            hint_text="Brief description of this category",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        gl_code_field = ft.TextField(
            label="GL Code",
            hint_text="e.g., 6100, EXP-001",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        icon_dropdown = ft.Dropdown(
            label="Icon",
            options=[
                ft.dropdown.Option("flight", "Flight"),
                ft.dropdown.Option("restaurant", "Restaurant"),
                ft.dropdown.Option("local_taxi", "Taxi"),
                ft.dropdown.Option("hotel", "Hotel"),
                ft.dropdown.Option("shopping_cart", "Shopping"),
                ft.dropdown.Option("computer", "Technology"),
                ft.dropdown.Option("category", "General"),
            ],
            value="category",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        color_field = ft.TextField(
            label="Color (Hex)",
            hint_text="#2196F3",
            value="#2196F3",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        def handle_add(e):
            if not name_field.value:
                name_field.error_text = "Name is required"
                name_field.update()
                return
            
            category_id = db.add_expense_category(
                name=name_field.value,
                description=description_field.value or "",
                gl_code=gl_code_field.value or "",
                icon=icon_dropdown.value,
                color=color_field.value
            )
            
            if category_id:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Category added successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_categories()
                self.categories_table = self.create_categories_table()
                self.page.update()
            else:
                name_field.error_text = "Category name already exists"
                name_field.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Expense Category", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    name_field,
                    description_field,
                    gl_code_field,
                    ft.Row([
                        ft.Container(content=icon_dropdown, expand=True),
                        ft.Container(content=color_field, width=150),
                    ], spacing=12),
                ], spacing=16, tight=True),
                width=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Add Category",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def show_edit_dialog(self, category):
        """Show edit category dialog"""
        
        cat_id, name, description, gl_code, icon, color, is_active, parent_id, created_at, updated_at = category
        
        name_field = ft.TextField(
            label="Category Name",
            value=name,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        description_field = ft.TextField(
            label="Description",
            value=description or "",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        gl_code_field = ft.TextField(
            label="GL Code",
            value=gl_code or "",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        icon_dropdown = ft.Dropdown(
            label="Icon",
            options=[
                ft.dropdown.Option("flight", "Flight"),
                ft.dropdown.Option("restaurant", "Restaurant"),
                ft.dropdown.Option("local_taxi", "Taxi"),
                ft.dropdown.Option("hotel", "Hotel"),
                ft.dropdown.Option("shopping_cart", "Shopping"),
                ft.dropdown.Option("computer", "Technology"),
                ft.dropdown.Option("category", "General"),
            ],
            value=icon or "category",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        color_field = ft.TextField(
            label="Color (Hex)",
            value=color or "#2196F3",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        status_switch = ft.Switch(
            label="Active",
            value=bool(is_active),
            active_color=ft.Colors.GREEN_400
        )
        
        def handle_update(e):
            if not name_field.value:
                name_field.error_text = "Name is required"
                name_field.update()
                return
            
            success = db.update_expense_category(
                cat_id,
                name=name_field.value,
                description=description_field.value,
                gl_code=gl_code_field.value,
                icon=icon_dropdown.value,
                color=color_field.value,
                is_active=1 if status_switch.value else 0
            )
            
            if success:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Category updated successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_categories()
                self.categories_table = self.create_categories_table()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Expense Category", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    name_field,
                    description_field,
                    gl_code_field,
                    ft.Row([
                        ft.Container(content=icon_dropdown, expand=True),
                        ft.Container(content=color_field, width=150),
                    ], spacing=12),
                    status_switch,
                ], spacing=16, tight=True),
                width=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Update",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_update
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def confirm_delete(self, category):
        """Confirm category deletion"""
        
        cat_id, name = category[0], category[1]
        
        def handle_delete(e):
            success = db.delete_expense_category(cat_id)
            if success:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Category deleted successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_categories()
                self.categories_table = self.create_categories_table()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Category", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete '{name}'? This action cannot be undone."),
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
