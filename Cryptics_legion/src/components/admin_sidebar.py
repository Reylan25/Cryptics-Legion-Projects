"""
Admin Sidebar Navigation Component
Comprehensive sidebar with sections for Dashboard, Expense Management, Configuration & Policy
"""

import flet as ft


class AdminSidebar:
    def __init__(self, page: ft.Page, current_route: str, on_navigate):
        self.page = page
        self.current_route = current_route
        self.on_navigate = on_navigate
        self.expanded_sections = {
            "expense_management": False,
            "config_policy": False,
            "reporting": False
        }
    
    def build(self):
        """Build the admin sidebar"""
        
        return ft.Container(
            content=ft.Column([
                # Logo/Brand
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=28, color=ft.Colors.BLUE_400),
                        ft.Text(
                            "ExpenseWise ",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Admin",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_400
                        ),
                    ], spacing=8),
                    padding=20,
                    bgcolor="#1E1E1E",
                ),
                
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                
                # Navigation Menu
                ft.Container(
                    content=ft.Column([
                        # Overview Section
                        self.create_section_header("Overview"),
                        self.create_nav_item(
                            "Dashboard",
                            ft.Icons.DASHBOARD_ROUNDED,
                            "admin_dashboard",
                            is_active=self.current_route == "admin_dashboard"
                        ),
                        
                        ft.Container(height=8),
                        
                        # Expense Management Section
                        self.create_expandable_section(
                            "Expense Management",
                            ft.Icons.RECEIPT_LONG_ROUNDED,
                            "expense_management",
                            [
                                ("Expense Reports", "expense_reports"),
                                ("Individual Expenses", "individual_expenses"),
                                ("Reimbursement", "reimbursement"),
                                ("Processing", "processing"),
                            ]
                        ),
                        
                        ft.Container(height=8),
                        
                        # User & Group Section
                        self.create_nav_item(
                            "User & Group",
                            ft.Icons.PEOPLE_ROUNDED,
                            "users",
                            expandable=True,
                            sub_items=[
                                ("Users & Roles", "users"),
                                ("Departments / Teams", "departments"),
                            ]
                        ),
                        
                        ft.Container(height=8),
                        
                        # Configuration & Policy Section
                        self.create_expandable_section(
                            "Configuration & Policy",
                            ft.Icons.SETTINGS_ROUNDED,
                            "config_policy",
                            [
                                ("Policy Rules", "policy_rules"),
                                ("Currencies & Exchange Rates", "currency_rates"),
                                ("Accounting Integration", "accounting_integration"),
                            ]
                        ),
                        
                        ft.Container(height=8),
                        
                        # Reporting & Analytics
                        self.create_nav_item(
                            "Reporting & Analytics",
                            ft.Icons.BAR_CHART_ROUNDED,
                            "reporting",
                            expandable=True,
                            sub_items=[
                                ("Export Data", "export_data"),
                            ]
                        ),
                        
                    ], spacing=4, scroll=ft.ScrollMode.AUTO),
                    expand=True,
                    padding=ft.padding.only(top=12, bottom=12, left=8, right=8)
                ),
                
            ], spacing=0),
            width=220,
            bgcolor="#2D2D30",
            border=ft.border.only(right=ft.BorderSide(1, ft.Colors.GREY_800))
        )
    
    def create_section_header(self, title: str):
        """Create a section header"""
        return ft.Container(
            content=ft.Text(
                title,
                size=11,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.GREY_500
            ),
            padding=ft.padding.only(left=12, right=12, top=8, bottom=4)
        )
    
    def create_nav_item(self, title: str, icon, route: str, is_active=False, expandable=False, sub_items=None):
        """Create a navigation item"""
        
        bg_color = ft.Colors.BLUE_700 if is_active else "transparent"
        text_color = ft.Colors.WHITE if is_active else ft.Colors.GREY_400
        hover_color = ft.Colors.BLUE_700 if is_active else "#383838"
        
        item = ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color=text_color),
                ft.Text(
                    title,
                    size=13,
                    weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL,
                    color=text_color
                ),
                ft.Container(expand=True),
                ft.Icon(
                    ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED if expandable else None,
                    size=16,
                    color=text_color
                ) if expandable else ft.Container()
            ], spacing=10),
            padding=ft.padding.only(left=12, right=12, top=10, bottom=10),
            bgcolor=bg_color,
            border_radius=6,
            ink=True,
            on_click=lambda _: self.on_navigate(route) if not expandable else None,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
        
        # Add hover effect
        def on_hover(e):
            if not is_active:
                item.bgcolor = hover_color if e.data == "true" else "transparent"
                item.update()
        
        item.on_hover = on_hover
        
        return item
    
    def create_expandable_section(self, title: str, icon, section_key: str, sub_items: list):
        """Create an expandable section with sub-items"""
        
        is_expanded = self.expanded_sections.get(section_key, False)
        
        # Main section header
        header = ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=18, color=ft.Colors.GREY_400),
                ft.Text(
                    title,
                    size=13,
                    weight=ft.FontWeight.NORMAL,
                    color=ft.Colors.GREY_400
                ),
                ft.Container(expand=True),
                ft.Icon(
                    ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED if is_expanded else ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
                    size=16,
                    color=ft.Colors.GREY_400
                )
            ], spacing=10),
            padding=ft.padding.only(left=12, right=12, top=10, bottom=10),
            bgcolor="transparent",
            border_radius=6,
            ink=True,
            on_click=lambda _: self.toggle_section(section_key),
            data=section_key
        )
        
        # Sub-items
        sub_items_col = ft.Column(
            [
                self.create_sub_nav_item(name, route)
                for name, route in sub_items
            ],
            spacing=2,
            visible=is_expanded
        )
        
        return ft.Column([header, sub_items_col], spacing=0)
    
    def create_sub_nav_item(self, title: str, route: str):
        """Create a sub-navigation item"""
        
        is_active = self.current_route == route
        text_color = ft.Colors.WHITE if is_active else ft.Colors.GREY_500
        bg_color = "#383838" if is_active else "transparent"
        
        item = ft.Container(
            content=ft.Row([
                ft.Container(width=30),  # Indent
                ft.Text(
                    title,
                    size=12,
                    weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.NORMAL,
                    color=text_color
                ),
            ], spacing=0),
            padding=ft.padding.only(left=12, right=12, top=8, bottom=8),
            bgcolor=bg_color,
            border_radius=6,
            ink=True,
            on_click=lambda _: self.on_navigate(route)
        )
        
        # Hover effect
        def on_hover(e):
            if not is_active:
                item.bgcolor = "#383838" if e.data == "true" else "transparent"
                item.update()
        
        item.on_hover = on_hover
        
        return item
    
    def toggle_section(self, section_key: str):
        """Toggle section expansion"""
        self.expanded_sections[section_key] = not self.expanded_sections.get(section_key, False)
        # Trigger rebuild
        if hasattr(self.page, 'update'):
            self.page.update()
