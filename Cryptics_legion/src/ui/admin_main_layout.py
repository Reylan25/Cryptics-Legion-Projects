"""
Admin Main Layout with Sidebar Navigation
Comprehensive admin interface matching the ExpenseWise design
"""

import flet as ft
from components.admin_sidebar import AdminSidebar
from ui.admin_dashboard_page import AdminDashboardPage
from ui.admin_users_page import AdminUserManagementPage
from ui.admin_logs_page import AdminLogsPage
from ui.admin_expense_categories_page import AdminExpenseCategoriesPage
from ui.admin_policy_rules_page import AdminPolicyRulesPage
from ui.admin_currency_rates_page import AdminCurrencyRatesPage
from ui.admin_accounting_integration_page import AdminAccountingIntegrationPage


class AdminMainLayout:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.current_route = "admin_dashboard"
        self.admin_data = state.get("admin", {})
        self.sidebar_visible = True
        
    def build(self):
        """Build the main admin layout with sidebar"""
        
        # Create sidebar
        self.sidebar_container = ft.Container(
            content=None,  # Will be set below
            width=220,
            visible=True,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        )
        
        self.sidebar = AdminSidebar(
            self.page,
            self.current_route,
            self.handle_navigation
        )
        self.sidebar_container.content = self.sidebar.build()
        
        # Create main content area
        self.content_area = ft.Container(
            content=self.get_page_content(self.current_route),
            expand=True,
            bgcolor="#1C1C1E"
        )
        
        # Create top bar
        top_bar = self.create_top_bar()
        
        # Main layout - responsive
        layout = ft.Row([
            self.sidebar_container,
            ft.Column([
                top_bar,
                self.content_area,
            ], spacing=0, expand=True)
        ], spacing=0, expand=True)
        
        return layout
    
    def create_top_bar(self):
        """Create top navigation bar"""
        
        # Hamburger menu button for mobile
        menu_button = ft.IconButton(
            icon=ft.Icons.MENU_ROUNDED,
            icon_size=24,
            icon_color=ft.Colors.GREY_400,
            tooltip="Toggle Menu",
            on_click=self.toggle_sidebar
        )
        
        # Search field - responsive
        search_field = ft.Container(
            content=ft.TextField(
                hint_text="Universal Search...",
                hint_style=ft.TextStyle(size=13, color=ft.Colors.GREY_500),
                bgcolor="#2C2C2E",
                border_color="transparent",
                focused_border_color=ft.Colors.BLUE_400,
                color=ft.Colors.WHITE,
                text_size=13,
                height=40,
                content_padding=ft.padding.symmetric(horizontal=12, vertical=8)
            ),
            expand=True
        )
        
        return ft.Container(
            content=ft.ResponsiveRow([
                ft.Container(
                    content=ft.Row([
                        menu_button,
                        ft.Row([
                            ft.Icon(ft.Icons.SEARCH_ROUNDED, size=20, color=ft.Colors.GREY_500),
                            ft.Text(
                                "ExpenseWise Admin",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREY_400
                            ),
                        ], spacing=8, visible=self.page.width > 600),
                    ], spacing=12),
                    col={"xs": 3, "sm": 3, "md": 3, "lg": 2}
                ),
                ft.Container(
                    content=search_field,
                    col={"xs": 6, "sm": 6, "md": 5, "lg": 6}
                ),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                            icon_size=20,
                            icon_color=ft.Colors.GREY_400,
                            tooltip="Notifications"
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.CircleAvatar(
                                    content=ft.Text(
                                        self.admin_data.get("username", "A")[0].upper(),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE
                                    ),
                                    bgcolor=ft.Colors.BLUE_700,
                                    radius=16
                                ),
                                ft.Text(
                                    "Admin User",
                                    size=13,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE,
                                    visible=self.page.width > 800
                                ),
                                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=16, color=ft.Colors.GREY_400, visible=self.page.width > 800),
                            ], spacing=8),
                            on_click=self.show_user_menu
                        ),
                    ], spacing=12, alignment=ft.MainAxisAlignment.END),
                    col={"xs": 3, "sm": 3, "md": 4, "lg": 4}
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor="#2D2D30",
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_800))
        )
    
    def toggle_sidebar(self, e):
        """Toggle sidebar visibility"""
        self.sidebar_container.visible = not self.sidebar_container.visible
        self.page.update()
    
    def handle_navigation(self, route: str):
        """Handle navigation between admin pages"""
        self.current_route = route
        self.content_area.content = self.get_page_content(route)
        
        # Rebuild sidebar with updated current route
        self.sidebar = AdminSidebar(
            self.page,
            self.current_route,
            self.handle_navigation
        )
        self.sidebar_container.content = self.sidebar.build()
        
        # Auto-hide sidebar on mobile after navigation
        if self.page.width <= 768:
            self.sidebar_container.visible = False
        
        self.page.update()
    
    def get_page_content(self, route: str):
        """Get page content based on route"""
        
        if route == "admin_dashboard":
            # Dashboard page with welcome header
            page = AdminDashboardPage(self.page, self.state, self.handle_navigation)
            dashboard_content = page.build()
            
            # Add welcome header - responsive
            header = ft.Container(
                content=ft.ResponsiveRow([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"Welcome, {self.admin_data.get('full_name', 'System Administrator')}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                "System Administration Dashboard",
                                size=14,
                                color=ft.Colors.WHITE70
                            ),
                        ], spacing=4),
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12}
                    ),
                ]),
                bgcolor=ft.Colors.BLUE_700,
                padding=ft.padding.symmetric(horizontal=20, vertical=16),
            )
            
            return ft.Column([
                header,
                dashboard_content
            ], spacing=0, expand=True)
        
        elif route == "users":
            page = AdminUserManagementPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        elif route == "logs":
            page = AdminLogsPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        elif route == "expense_categories":
            page = AdminExpenseCategoriesPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        elif route == "policy_rules":
            page = AdminPolicyRulesPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        elif route == "currency_rates":
            page = AdminCurrencyRatesPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        elif route == "accounting_integration":
            page = AdminAccountingIntegrationPage(self.page, self.state, self.handle_navigation)
            return page.build()
        
        else:
            # Default placeholder for other routes
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CONSTRUCTION_ROUNDED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        f"{route.replace('_', ' ').title()}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "This page is under construction",
                        size=14,
                        color=ft.Colors.GREY_500
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                padding=50,
                alignment=ft.alignment.center,
                expand=True
            )
    
    def show_user_menu(self, e):
        """Show user dropdown menu"""
        
        def handle_logout(e):
            self.page.close(menu)
            # Log logout
            from core import admin_auth
            admin_auth.logout_admin(
                self.admin_data.get("id"),
                self.admin_data.get("username", "")
            )
            # Clear state
            self.state.pop("admin", None)
            self.state.pop("is_admin", None)
            # Navigate to login
            self.on_navigate("login")
        
        menu = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON_ROUNDED, color=ft.Colors.BLUE_400),
                        title=ft.Text("Profile", color=ft.Colors.WHITE),
                        on_click=lambda e: self.page.close(menu)
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SETTINGS_ROUNDED, color=ft.Colors.GREY_400),
                        title=ft.Text("Settings", color=ft.Colors.WHITE),
                        on_click=lambda e: self.page.close(menu)
                    ),
                    ft.Divider(height=1, color=ft.Colors.GREY_800),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=ft.Colors.RED_400),
                        title=ft.Text("Logout", color=ft.Colors.RED_400),
                        on_click=handle_logout
                    ),
                ], spacing=0, tight=True),
                width=200
            ),
            bgcolor="#2D2D30",
        )
        
        self.page.open(menu)
