"""
Currency Exchange Rates Viewer
Shows live exchange rates and allows currency conversion
"""

import flet as ft
from datetime import datetime
from core.theme import get_theme
from utils.currency import get_currency_symbol, get_currency_name, CURRENCY_CONFIGS
from utils.currency_exchange import get_exchange_api, SUPPORTED_CURRENCIES


def build_exchange_rates_content(page: ft.Page, state: dict, toast, go_back):
    """
    Build exchange rates viewer page with live rates and conversion calculator.
    """
    theme = get_theme()
    api = get_exchange_api()
    
    # State
    base_currency = {"value": "USD"}
    amount_to_convert = {"value": "1"}
    target_currency = {"value": "PHP"}
    
    # UI component references for cross-function access
    result_display = {"result_text": None, "rate_info": None}
    
    # Main container reference for updating
    main_container = ft.Container(expand=True)
    
    def refresh_rates(e=None):
        """Refresh exchange rates from API."""
        toast("Refreshing exchange rates...", theme.accent_primary)
        success = api.get_exchange_rates(force_refresh=True)
        if success:
            toast("Exchange rates updated!", "#10B981")
            # Refresh the page
            main_container.content = build_view()
            page.update()
        else:
            toast("Failed to fetch rates. Using cached data.", "#EF4444")
    
    def update_base_currency(currency: str):
        """Update base currency and refresh display."""
        base_currency["value"] = currency
        main_container.content = build_view()
        page.update()
    
    def show_currency_picker(e, callback):
        """Show currency selection dialog."""
        def select_currency(code):
            callback(code)
            page.close(dlg)
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select Currency", color=theme.text_primary),
            bgcolor=theme.bg_card,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.Text(
                                get_currency_symbol(code),
                                size=20,
                                color=theme.text_primary,
                                weight=ft.FontWeight.BOLD,
                            ),
                            title=ft.Text(
                                f"{code} - {get_currency_name(code)}",
                                color=theme.text_primary,
                            ),
                            on_click=lambda e, c=code: select_currency(c),
                        ) for code in SUPPORTED_CURRENCIES
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    tight=True,
                ),
                height=400,
            ),
        )
        page.open(dlg)
    
    def convert_currency_interactive(e=None):
        """Perform currency conversion."""
        # Validate amount input
        if not amount_to_convert["value"] or str(amount_to_convert["value"]).strip() == "":
            if result_display["result_text"]:
                result_display["result_text"].value = "Amount cannot be empty"
            if result_display["rate_info"]:
                result_display["rate_info"].value = ""
            page.update()
            toast("Please enter an amount", "#EF4444")
            return
        
        try:
            amount_str = str(amount_to_convert["value"]).strip().replace(",", "")
            amount = float(amount_str)
            
            if amount <= 0:
                if result_display["result_text"]:
                    result_display["result_text"].value = "Amount must be greater than 0"
                if result_display["rate_info"]:
                    result_display["rate_info"].value = ""
                page.update()
                toast("Amount must be greater than 0", "#EF4444")
                return
            
            from_curr = base_currency["value"]
            to_curr = target_currency["value"]
            
            converted = api.convert_currency(amount, from_curr, to_curr)
            
            # Use the stored references
            if result_display["result_text"]:
                result_display["result_text"].value = f"{get_currency_symbol(to_curr)}{converted:,.2f}"
            if result_display["rate_info"]:
                rate = api.get_exchange_rate(from_curr, to_curr)
                result_display["rate_info"].value = f"1 {from_curr} = {rate:.4f} {to_curr}"
            page.update()
        except ValueError:
            if result_display["result_text"]:
                result_display["result_text"].value = "Please enter a valid numeric amount"
            if result_display["rate_info"]:
                result_display["rate_info"].value = ""
            page.update()
            toast("Please enter a valid numeric amount", "#EF4444")
    
    def build_view():
        """Build and return the page content."""
        # Get exchange rates
        rates = api.get_all_rates_formatted(base_currency["value"])
        last_update = api.get_cache_age() or "Never"
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=theme.text_primary,
                        on_click=lambda e: go_back() if go_back else None,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Exchange Rates", size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.Text(f"Updated: {last_update}", size=11, color=theme.text_secondary),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        icon_color=theme.accent_primary,
                        tooltip="Refresh rates",
                        on_click=refresh_rates,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(top=10, bottom=16),
        )
        
        # Base currency selector
        base_selector = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Base Currency", size=12, color=theme.text_secondary),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    get_currency_symbol(base_currency["value"]),
                                    size=24,
                                    color=theme.accent_primary,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            base_currency["value"],
                                            size=16,
                                            weight=ft.FontWeight.W_600,
                                            color=theme.text_primary,
                                        ),
                                        ft.Text(
                                            get_currency_name(base_currency["value"]),
                                            size=12,
                                            color=theme.text_secondary,
                                        ),
                                    ],
                                    spacing=0,
                                    expand=True,
                                ),
                                ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=theme.text_muted),
                            ],
                            spacing=12,
                        ),
                        bgcolor=theme.bg_field,
                        border_radius=12,
                        padding=12,
                        on_click=lambda e: show_currency_picker(e, update_base_currency),
                        ink=True,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Exchange rates list
        rates_list = ft.Column(spacing=8)
        
        for code in SUPPORTED_CURRENCIES:
            if code == base_currency["value"]:
                continue
            
            rate, formatted = rates.get(code, (1.0, "N/A"))
            symbol = get_currency_symbol(code)
            name = get_currency_name(code)
            
            rates_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    symbol,
                                    size=20,
                                    color="white",
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor=theme.accent_primary,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{code}",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=theme.text_primary,
                                    ),
                                    ft.Text(
                                        name,
                                        size=11,
                                        color=theme.text_secondary,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{rate:.4f}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.text_primary,
                                    ),
                                    ft.Text(
                                        f"per {base_currency['value']}",
                                        size=10,
                                        color=theme.text_muted,
                                    ),
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor=theme.bg_field if theme.is_dark else theme.bg_secondary,
                    border_radius=12,
                    padding=12,
                    border=ft.border.all(1, theme.border_primary),
                )
            )
        
        rates_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Exchange Rates", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                    ft.Container(height=8),
                    rates_list,
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Currency converter
        amount_input = ft.TextField(
            value=amount_to_convert["value"],
            label="Amount",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            text_size=18,
            on_change=lambda e: amount_to_convert.update({"value": e.control.value}),
            on_submit=convert_currency_interactive,
        )
        
        def update_from_currency(code):
            """Update from currency in converter."""
            base_currency["value"] = code
            main_container.content = build_view()
            page.update()
        
        def update_to_currency(code):
            """Update to currency in converter."""
            target_currency["value"] = code
            main_container.content = build_view()
            page.update()
        
        from_currency_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        get_currency_symbol(base_currency["value"]),
                        size=20,
                        color=theme.accent_primary,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        base_currency["value"],
                        size=16,
                        color=theme.text_primary,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=theme.text_muted, size=20),
                ],
                spacing=8,
            ),
            bgcolor=theme.bg_field,
            border_radius=10,
            padding=12,
            on_click=lambda e: show_currency_picker(e, lambda c: update_from_currency(c)),
            ink=True,
        )
        
        to_currency_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        get_currency_symbol(target_currency["value"]),
                        size=20,
                        color=theme.accent_primary,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        target_currency["value"],
                        size=16,
                        color=theme.text_primary,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=theme.text_muted, size=20),
                ],
                spacing=8,
            ),
            bgcolor=theme.bg_field,
            border_radius=10,
            padding=12,
            on_click=lambda e: show_currency_picker(e, lambda c: update_to_currency(c)),
            ink=True,
        )
        
        # Result display (defined before used in converter section)
        result_text = ft.Text(
            "0.00",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=theme.accent_primary,
            text_align=ft.TextAlign.CENTER,
        )
        
        rate_info = ft.Text(
            "",
            size=12,
            color=theme.text_secondary,
            text_align=ft.TextAlign.CENTER,
        )
        
        # Store references for use in convert_currency_interactive
        result_display["result_text"] = result_text
        result_display["rate_info"] = rate_info
        
        converter_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CALCULATE, color=theme.accent_primary, size=20),
                            ft.Text("Currency Converter", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=16),
                    amount_input,
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            ft.Container(content=from_currency_btn, expand=True),
                            ft.Icon(ft.Icons.ARROW_FORWARD, color=theme.text_muted, size=24),
                            ft.Container(content=to_currency_btn, expand=True),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=16),
                    ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.SWAP_HORIZ, size=20),
                                ft.Text("Convert", size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        bgcolor=theme.accent_primary,
                        color="white",
                        width=200,
                        height=48,
                        on_click=convert_currency_interactive,
                    ),
                    ft.Container(height=16),
                    ft.Divider(color=theme.border_primary, height=1),
                    ft.Container(height=16),
                    ft.Column(
                        controls=[
                            ft.Text("Result", size=12, color=theme.text_secondary),
                            result_text,
                            rate_info,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary),
        )
        
        # Info card
        info_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=theme.accent_primary, size=20),
                    ft.Text(
                        "Exchange rates are updated every 6 hours from live market data.",
                        size=11,
                        color=theme.text_secondary,
                        expand=True,
                    ),
                ],
                spacing=12,
            ),
            bgcolor=f"{theme.accent_primary}15",
            border_radius=10,
            padding=12,
            border=ft.border.all(1, f"{theme.accent_primary}30"),
        )
        
        # Scrollable content
        scrollable = ft.Column(
            controls=[
                base_selector,
                ft.Container(height=16),
                converter_section,
                ft.Container(height=16),
                rates_section,
                ft.Container(height=16),
                info_card,
                ft.Container(height=80),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # Main container
        main_content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.gradient_start, theme.gradient_end],
            ),
            padding=ft.padding.only(left=20, right=20, top=10),
            content=ft.Column(
                controls=[header, scrollable],
                expand=True,
                spacing=0,
            ),
        )
        
        return main_content
    
    # Build initial content and set it
    main_container.content = build_view()
    return main_container
