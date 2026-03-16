"""
Admin Accounting Integration Page
Configure integrations with external accounting software
"""

import flet as ft
from core import db
from datetime import datetime
from utils.quickbooks_integration import QuickBooksIntegration


class AdminAccountingIntegrationPage:
    def __init__(self, page: ft.Page, state: dict, on_navigate):
        self.page = page
        self.state = state
        self.on_navigate = on_navigate
        self.integrations = []
        self.sync_logs = []
        
    def build(self):
        """Build accounting integration page"""
        
        # Initialize tables
        db.init_admin_config_tables()
        
        # Load data
        self.load_integrations()
        self.load_sync_logs()
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Accounting Integration",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Connect and sync with external accounting platforms",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                ], spacing=4),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED, size=18),
                        ft.Text("Add Integration", size=14, weight=ft.FontWeight.W_500)
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
        
        # Integration cards
        integration_cards = self.create_integration_cards()
        
        # Sync logs
        sync_logs_section = self.create_sync_logs_section()
        
        # Main content
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Available Integrations",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Container(height=12),
                    integration_cards,
                    ft.Container(height=24),
                    sync_logs_section,
                ], scroll=ft.ScrollMode.AUTO),
                expand=True,
                padding=20
            )
        ], spacing=0, expand=True)
        
        return content
    
    def load_integrations(self):
        """Load integrations from database"""
        self.integrations = db.get_accounting_integrations()
    
    def load_sync_logs(self):
        """Load sync logs"""
        self.sync_logs = db.get_sync_logs(limit=10)
    
    def create_integration_cards(self):
        """Create integration platform cards"""
        
        platforms = [
            {
                "name": "QuickBooks",
                "icon": ft.Icons.ACCOUNT_BALANCE_ROUNDED,
                "color": ft.Colors.GREEN_700,
                "description": "Sync expenses with QuickBooks Online",
                "platform_key": "quickbooks"
            },
            {
                "name": "Xero",
                "icon": ft.Icons.CLOUD_SYNC_ROUNDED,
                "color": ft.Colors.BLUE_700,
                "description": "Connect to Xero accounting platform",
                "platform_key": "xero"
            },
            {
                "name": "SAP",
                "icon": ft.Icons.BUSINESS_ROUNDED,
                "color": ft.Colors.INDIGO_700,
                "description": "Enterprise SAP integration",
                "platform_key": "sap"
            },
            {
                "name": "NetSuite",
                "icon": ft.Icons.CORPORATE_FARE_ROUNDED,
                "color": ft.Colors.ORANGE_700,
                "description": "Oracle NetSuite ERP integration",
                "platform_key": "netsuite"
            },
        ]
        
        cards = []
        for platform in platforms:
            # Check if already configured
            is_configured = any(i[1] == platform["platform_key"] for i in self.integrations)
            
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(platform["icon"], size=32, color=platform["color"]),
                            bgcolor=f"{platform['color']}20",
                            border_radius=10,
                            padding=12
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(
                                "Connected" if is_configured else "Not Connected",
                                size=11,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.WHITE
                            ),
                            bgcolor=ft.Colors.GREEN_700 if is_configured else ft.Colors.GREY_700,
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=12
                        ),
                    ]),
                    ft.Container(height=12),
                    ft.Text(
                        platform["name"],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        platform["description"],
                        size=12,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=16),
                    ft.Row([
                        ft.ElevatedButton(
                            "Configure" if is_configured else "Connect",
                            bgcolor=platform["color"],
                            color=ft.Colors.WHITE,
                            on_click=lambda e, p=platform["platform_key"]: self.configure_integration(p)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.SYNC_ROUNDED,
                            icon_color=ft.Colors.BLUE_400,
                            tooltip="Sync Now",
                            visible=is_configured,
                            on_click=lambda e, p=platform["platform_key"]: self.sync_integration(p)
                        ) if is_configured else ft.Container(),
                    ], spacing=8)
                ], spacing=4),
                bgcolor="#2C2C2E",
                border_radius=12,
                padding=20,
                width=280,
                border=ft.border.all(1, ft.Colors.GREY_800)
            )
            cards.append(card)
        
        return ft.Row(cards, spacing=16, wrap=True)
    
    def create_sync_logs_section(self):
        """Create sync logs section"""
        
        if not self.sync_logs:
            logs_content = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.HISTORY_ROUNDED, size=48, color=ft.Colors.GREY_700),
                    ft.Text(
                        "No sync history yet",
                        size=14,
                        color=ft.Colors.GREY_500
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=40,
                alignment=ft.alignment.center
            )
        else:
            log_items = []
            for log in self.sync_logs:
                log_id, integration_id, platform, sync_type, status, records_synced, error_message, started_at, completed_at = log
                
                # Parse date
                try:
                    dt = datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S")
                    time_str = dt.strftime("%b %d, %I:%M %p")
                except:
                    time_str = started_at
                
                status_color = ft.Colors.GREEN_400 if status == "success" else ft.Colors.RED_400
                status_icon = ft.Icons.CHECK_CIRCLE_ROUNDED if status == "success" else ft.Icons.ERROR_ROUNDED
                
                log_item = ft.Container(
                    content=ft.Row([
                        ft.Icon(status_icon, size=20, color=status_color),
                        ft.Column([
                            ft.Text(
                                f"{platform.title()} - {sync_type.replace('_', ' ').title()}",
                                size=13,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                f"{records_synced} records • {time_str}",
                                size=11,
                                color=ft.Colors.GREY_400
                            ),
                        ], spacing=2, expand=True),
                    ], spacing=12),
                    padding=12,
                    bgcolor="#1C1C1E",
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.GREY_800)
                )
                log_items.append(log_item)
            
            logs_content = ft.Column(log_items, spacing=8)
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Recent Sync Activity",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                ),
                ft.Container(height=12),
                logs_content,
            ]),
            bgcolor="#2D2D30",
            border_radius=12,
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_800)
        )
    
    def show_add_dialog(self, e):
        """Show add integration dialog"""
        
        platform_dropdown = ft.Dropdown(
            label="Platform",
            options=[
                ft.dropdown.Option("quickbooks", "QuickBooks"),
                ft.dropdown.Option("xero", "Xero"),
                ft.dropdown.Option("sap", "SAP"),
                ft.dropdown.Option("netsuite", "NetSuite"),
            ],
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            autofocus=True
        )
        
        api_key_field = ft.TextField(
            label="API Key",
            hint_text="Enter API key",
            password=True,
            can_reveal_password=True,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        api_secret_field = ft.TextField(
            label="API Secret (Optional)",
            hint_text="Enter API secret",
            password=True,
            can_reveal_password=True,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        company_id_field = ft.TextField(
            label="Company ID",
            hint_text="Your company ID in the platform",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        sync_frequency_dropdown = ft.Dropdown(
            label="Sync Frequency",
            options=[
                ft.dropdown.Option("hourly", "Hourly"),
                ft.dropdown.Option("daily", "Daily"),
                ft.dropdown.Option("weekly", "Weekly"),
                ft.dropdown.Option("manual", "Manual Only"),
            ],
            value="daily",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True
        )
        
        auto_sync_switch = ft.Switch(
            label="Enable Auto-Sync",
            value=False,
            active_color=ft.Colors.GREEN_400
        )
        
        def handle_add(e):
            if not all([platform_dropdown.value, api_key_field.value, company_id_field.value]):
                return
            
            integration_id = db.add_accounting_integration(
                platform=platform_dropdown.value,
                api_key=api_key_field.value,
                api_secret=api_secret_field.value or "",
                company_id=company_id_field.value,
                sync_frequency=sync_frequency_dropdown.value,
                auto_sync=1 if auto_sync_switch.value else 0
            )
            
            if integration_id:
                self.page.close(dialog)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Integration added successfully!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_700
                )
                self.page.snack_bar.open = True
                self.load_integrations()
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Accounting Integration", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    platform_dropdown,
                    api_key_field,
                    api_secret_field,
                    company_id_field,
                    sync_frequency_dropdown,
                    auto_sync_switch,
                ], spacing=16, tight=True, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=500,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Add Integration",
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def configure_integration(self, platform: str):
        """Configure existing integration"""
        
        if platform == "quickbooks":
            self.show_quickbooks_config_dialog()
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Opening {platform.title()} configuration...", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE_700
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def show_quickbooks_config_dialog(self):
        """Show QuickBooks configuration dialog"""
        
        # Check if integration already exists
        qb_integration = next((i for i in self.integrations if i[1] == "quickbooks"), None)
        
        client_id_field = ft.TextField(
            label="Client ID",
            hint_text="Your QuickBooks App Client ID",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            value=qb_integration[2] if qb_integration else "",  # company_id field stores client_id
            border_radius=8
        )
        
        client_secret_field = ft.TextField(
            label="Client Secret",
            hint_text="Your QuickBooks App Client Secret",
            password=True,
            can_reveal_password=True,
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            border_radius=8
        )
        
        realm_id_field = ft.TextField(
            label="Realm ID (Company ID)",
            hint_text="Your QuickBooks Company/Realm ID",
            bgcolor="#2C2C2E",
            border_color=ft.Colors.GREY_700,
            focused_border_color=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE,
            filled=True,
            value=qb_integration[3] if qb_integration else "",  # company_id field
            border_radius=8
        )
        
        # Status display for test result
        test_status = ft.Container(
            content=ft.Text(
                "Ready to test credentials",
                size=12,
                color=ft.Colors.GREY_400,
                italic=True
            ),
            padding=10,
            border_radius=8,
            bgcolor="#1C1C1E",
            visible=False
        )
        
        def handle_test(e):
            """Test credentials by validating format"""
            if not all([client_id_field.value, client_secret_field.value, realm_id_field.value]):
                test_status.content = ft.Text(
                    "❌ Please fill in all required fields",
                    size=12,
                    color=ft.Colors.RED_400,
                    weight=ft.FontWeight.W_500
                )
                test_status.bgcolor = "#3D1C1C"
                test_status.visible = True
                self.page.update()
                return
            
            # Test with QuickBooks integration
            qb = QuickBooksIntegration(
                client_id=client_id_field.value,
                client_secret=client_secret_field.value,
                realm_id=realm_id_field.value
            )
            
            success, message = qb.test_connection()
            
            # Update status display
            if success:
                test_status.content = ft.Text(
                    message,
                    size=12,
                    color=ft.Colors.GREEN_400,
                    weight=ft.FontWeight.W_500
                )
                test_status.bgcolor = "#1C3D1C"
            else:
                test_status.content = ft.Text(
                    message,
                    size=12,
                    color=ft.Colors.ORANGE_400,
                    weight=ft.FontWeight.W_500
                )
                test_status.bgcolor = "#3D2D1C"
            
            test_status.visible = True
            self.page.update()
        
        test_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED, size=18),
                ft.Text("Test Connection", size=14, weight=ft.FontWeight.W_500)
            ], spacing=8),
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
            on_click=handle_test
        )
        
        def handle_save(e):
            if not all([client_id_field.value, client_secret_field.value, realm_id_field.value]):
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please fill in all required fields", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            # Save configuration
            if qb_integration:
                # Update existing
                db.update_accounting_integration(
                    qb_integration[0],
                    api_key=client_id_field.value,
                    api_secret=client_secret_field.value,
                    company_id=realm_id_field.value,
                    is_active=1
                )
            else:
                # Create new
                db.add_accounting_integration(
                    platform="quickbooks",
                    api_key=client_id_field.value,
                    api_secret=client_secret_field.value,
                    company_id=realm_id_field.value,
                    sync_frequency="daily",
                    auto_sync=0
                )
            
            self.page.close(dialog)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ QuickBooks configuration saved!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.load_integrations()
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_BALANCE_ROUNDED, color=ft.Colors.GREEN_700, size=24),
                ft.Text("QuickBooks Online Configuration", weight=ft.FontWeight.BOLD)
            ], spacing=12),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📋 Configuration", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                            ft.Text(
                                "Get your credentials from https://developer.intuit.com",
                                size=11,
                                color=ft.Colors.GREY_500,
                                italic=True
                            ),
                        ], spacing=4),
                        padding=12,
                        bgcolor="#1C1C1E",
                        border_radius=8
                    ),
                    
                    client_id_field,
                    client_secret_field,
                    realm_id_field,
                    
                    ft.Container(height=8),
                    
                    ft.Row([
                        test_button,
                        ft.Container(expand=True),
                    ]),
                    
                    test_status,
                    
                    ft.Container(height=8),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📋 Setup Instructions:", size=13, weight=ft.FontWeight.W_500, color=ft.Colors.YELLOW_400),
                            ft.Text("1. Go to https://developer.intuit.com", size=11, color=ft.Colors.GREY_400),
                            ft.Text("2. Create or select your app", size=11, color=ft.Colors.GREY_400),
                            ft.Text("3. Copy Client ID and Secret from Settings", size=11, color=ft.Colors.GREY_400),
                            ft.Text("4. In your QBO account, connect app to get Realm ID", size=11, color=ft.Colors.GREY_400),
                            ft.Text("5. Paste all three values above and test", size=11, color=ft.Colors.GREY_400),
                        ], spacing=4),
                        padding=12,
                        bgcolor="#1C1C1E",
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_800)
                    ),
                ], spacing=12, tight=True, scroll=ft.ScrollMode.AUTO),
                width=550,
                height=650,
                padding=20
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton(
                    "Save Configuration",
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    on_click=handle_save
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor="#2D2D30",
        )
        
        self.page.open(dialog)
    
    def sync_integration(self, platform: str):
        """Sync integration data with QuickBooks"""
        
        if platform != "quickbooks":
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Syncing with {platform.title()}...", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Get QuickBooks integration config
        qb_integration = next((i for i in self.integrations if i[1] == "quickbooks"), None)
        if not qb_integration:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("QuickBooks not configured", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Show progress
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Syncing with QuickBooks...", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.BLUE_700
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        # Initialize QuickBooks client
        try:
            qb = QuickBooksIntegration(
                client_id=qb_integration[2],  # company_id from DB
                client_secret="",  # Would need to decrypt from storage
                realm_id=qb_integration[3]    # company_id field
            )
            
            # Get recent unsync expenses from database
            expenses = self._get_unsync_expenses()
            
            if not expenses:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("No new expenses to sync", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.ORANGE_700
                )
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            # Sync expenses
            synced_count, errors, synced_ids = qb.sync_expenses(expenses)
            
            # Mark expenses as synced in database
            if synced_ids:
                db.mark_expenses_as_synced_batch(synced_ids, synced=True)
            
            # Log sync activity
            db.log_sync_activity(
                integration_id=qb_integration[0],
                sync_type="expense_sync",
                status="success" if synced_count > 0 else "partial",
                records_synced=synced_count,
                error_message="; ".join(errors) if errors else None
            )
            
            # Update last sync timestamp
            db.update_accounting_integration(
                qb_integration[0],
                last_sync=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Show result
            message = f"Synced {synced_count} expenses to QuickBooks"
            if errors:
                message += f" ({len(errors)} errors)"
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700 if synced_count > 0 else ft.Colors.ORANGE_700
            )
            self.page.snack_bar.open = True
            self.load_sync_logs()
            self.page.update()
            
        except Exception as e:
            # Log error
            db.log_sync_activity(
                integration_id=qb_integration[0],
                sync_type="expense_sync",
                status="error",
                records_synced=0,
                error_message=str(e)
            )
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Sync error: {str(e)}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700
            )
            self.page.snack_bar.open = True
            self.load_sync_logs()
            self.page.update()
    
    def _get_unsync_expenses(self) -> list:
        """Get recent expenses that haven't been synced yet"""
        # This would connect to your database to get expenses
        # For now, return empty list - you'll need to implement this
        # based on your expense schema
        try:
            # Get all expenses (you may want to filter by date range)
            conn = db.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.description, e.amount, e.category, e.date, e.account_id
                FROM expenses e
                WHERE e.synced_to_qb = 0 OR e.synced_to_qb IS NULL
                ORDER BY e.date DESC
                LIMIT 50
            """)
            
            expenses = cursor.fetchall()
            conn.close()
            
            formatted_expenses = []
            for exp in expenses:
                formatted_expenses.append({
                    "id": exp[0],
                    "description": exp[1],
                    "amount": exp[2],
                    "category": exp[3],
                    "date": exp[4],
                    "account_id": exp[5] or "1"  # Default account if not specified
                })
            
            return formatted_expenses
        except Exception as e:
            print(f"Error fetching unsync expenses: {e}")
            return []
