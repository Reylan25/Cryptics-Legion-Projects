"""
Admin Currency & Exchange Rates Management Page
Manage supported currencies and exchange rates
"""

import flet as ft
from core import db
from datetime import datetime


class AdminCurrencyRatesPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.rates = []
        
    def build(self):
        """Build currency rates management page"""
        
        # Initialize tables
        db.init_admin_config_tables()
        
        # Load rates
        self.load_rates()
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Currencies & Exchange Rates",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Manage currency exchange rates for international expenses",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                ], spacing=4),
                ft.Container(expand=True),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH_ROUNDED, size=18),
                            ft.Text("Update Rates", size=14, weight=ft.FontWeight.W_500)
                        ], spacing=8),
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                        on_click=self.update_rates_from_api
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD_ROUNDED, size=18),
                            ft.Text("Add Rate", size=14, weight=ft.FontWeight.W_500)
                        ], spacing=8),
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        on_click=self.show_add_dialog
                    ),
                ], spacing=12)
            ]),
            padding=20,
            bgcolor="#2D2D30",
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_800))
        )
        
        # Currency Stats Cards
        stats_cards = ft.Container(
            content=ft.Row([
                self.create_stat_card("Total Rates", str(len(self.rates)), ft.Icons.CURRENCY_EXCHANGE_ROUNDED, ft.Colors.BLUE_400),
                self.create_stat_card("Base Currency", "PHP", ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, ft.Colors.GREEN_400),
                self.create_stat_card("Last Updated", datetime.now().strftime("%b %d, %Y"), ft.Icons.UPDATE_ROUNDED, ft.Colors.ORANGE_400),
            ], spacing=16, wrap=True),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
        )
        
        # Rates Table
        self.rates_table = self.create_rates_table()
        
        # Main content
        content = ft.Column([
            header,
            stats_cards,
            ft.Container(
                content=ft.Column([
                    self.rates_table
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=20
            )
        ], spacing=0, expand=True)
        
        return content
    
    def create_stat_card(self, title: str, value: str, icon, color):
        """Create stat card"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=24, color=color),
                    bgcolor=f"{color}20",
                    border_radius=8,
                    padding=12
                ),
                ft.Column([
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(title, size=12, color=ft.Colors.GREY_400),
                ], spacing=2),
            ], spacing=12),
            bgcolor="#2C2C2E",
            border_radius=10,
            padding=16,
            width=220
        )
    
    def load_rates(self):
        """Load currency rates from database"""
        self.rates = db.get_currency_rates()
    
    def create_rates_table(self):
        """Create rates data table"""
        
        if not self.rates:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CURRENCY_EXCHANGE_OUTLINED, size=64, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No exchange rates yet",
                        size=16,
                        color=ft.Colors.GREY_500
                    ),
                    ft.Text(
                        "Click 'Add Rate' to add your first exchange rate or 'Update Rates' to fetch from API",
                        size=13,
                        color=ft.Colors.GREY_600
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=50,
                alignment=ft.alignment.center
            )
        
        rows = []
        for rate in self.rates:
            rate_id, from_currency, to_currency, rate_value, effective_date, is_active, source, updated_at = rate
            
            # Parse date
            try:
                dt = datetime.strptime(effective_date, "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%b %d, %Y")
            except:
                date_str = effective_date
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(from_currency, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.BLUE_700,
                                    border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4)
                                ),
                                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=16, color=ft.Colors.GREY_500),
                                ft.Container(
                                    content=ft.Text(to_currency, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.GREEN_700,
                                    border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4)
                                ),
                            ], spacing=8)
                        ),
                        ft.DataCell(
                            ft.Text(f"{rate_value:.6f}", size=13, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
                        ),
                        ft.DataCell(
                            ft.Text(date_str, size=12, color=ft.Colors.GREY_400)
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(
                                    source.title(),
                                    size=11,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.PURPLE_700 if source == "api" else ft.Colors.GREY_700,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=12
                            )
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
                                    on_click=lambda e, r=rate: self.show_edit_dialog(r)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_size=18,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Delete",
                                    on_click=lambda e, r=rate: self.confirm_delete(r)
                                ),
                            ], spacing=0)
                        ),
                    ],
                    data=rate
                )
            )
        
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Currency Pair", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Exchange Rate", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Effective Date", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
                ft.DataColumn(ft.Text("Source", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_400)),
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
        """Show add rate dialog"""
        
        from_currency_field = ft.TextField(
            label="From Currency",
            hint_text="e.g., USD, EUR, JPY",
            value="USD",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        to_currency_field = ft.TextField(
            label="To Currency",
            hint_text="e.g., PHP, USD, EUR",
            value="PHP",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        rate_field = ft.TextField(
            label="Exchange Rate",
            hint_text="e.g., 56.50",
            keyboard_type=ft.KeyboardType.NUMBER,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        def handle_add(e):
            if not all([from_currency_field.value, to_currency_field.value, rate_field.value]):
                return
            
            try:
                rate_value = float(rate_field.value)
            except:
                rate_field.error_text = "Invalid rate"
                rate_field.update()
                return
            
            rate_id = db.add_currency_rate(
                from_currency=from_currency_field.value.upper(),
                to_currency=to_currency_field.value.upper(),
                rate=rate_value,
                source="manual"
            )
            
            if rate_id:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Exchange rate added successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_rates()
                self.rates_table = self.create_rates_table()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Exchange Rate", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    from_currency_field,
                    to_currency_field,
                    rate_field,
                    ft.Container(
                        content=ft.Text(
                            "Example: 1 USD = 56.50 PHP",
                            size=11,
                            color=ft.Colors.GREY_500,
                            italic=True
                        ),
                        padding=ft.padding.only(top=8)
                    ),
                ], spacing=16, tight=True),
                width=400,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Add Rate",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def show_edit_dialog(self, rate):
        """Show edit rate dialog"""
        rate_id, from_currency, to_currency, rate_value, effective_date, is_active, source, updated_at = rate
        
        # Similar to add dialog with pre-filled values
        pass
    
    def confirm_delete(self, rate):
        """Confirm rate deletion"""
        rate_id = rate[0]
        from_curr = rate[1]
        to_curr = rate[2]
        
        def handle_delete(e):
            success = db.update_currency_rate(rate_id, is_active=0)
            if success:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Exchange rate deleted successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_rates()
                self.rates_table = self.create_rates_table()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Exchange Rate", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Are you sure you want to delete {from_curr} → {to_curr} exchange rate?"),
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
    
    def update_rates_from_api(self, e):
        """Update rates from external API"""
        
        # Show loading dialog
        loading_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Updating Exchange Rates", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(),
                    ft.Text("Fetching latest rates from API...", size=13, color=ft.Colors.GREY_400)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                padding=20
            ),
            bgcolor="#2D2D30",
        )
        
        self.page.open(loading_dialog)
        
        # Simulate API call (in real implementation, use currency API)
        import time
        time.sleep(1)
        
        # Add some sample rates
        sample_rates = [
            ("USD", "PHP", 56.50),
            ("EUR", "PHP", 61.20),
            ("GBP", "PHP", 71.30),
            ("JPY", "PHP", 0.38),
        ]
        
        for from_curr, to_curr, rate in sample_rates:
            db.add_currency_rate(from_curr, to_curr, rate, source="api")
        
        self.page.close(loading_dialog)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Updated {len(sample_rates)} exchange rates!", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.load_rates()
        self.rates_table = self.create_rates_table()
        self.page.update()
