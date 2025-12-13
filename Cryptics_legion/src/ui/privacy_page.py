"""
Personal Data & Privacy Page
Displays privacy policy, terms of service, and data management options
"""

import flet as ft
from core.theme import get_theme
from core import db


def build_privacy_content(page: ft.Page, state: dict, toast, go_back, logout_callback=None):
    """
    Build Personal Data & Privacy page with documents and settings.
    """
    theme = get_theme()
    
    def delete_all_data(e):
        """Confirm and delete all user data."""
        def confirm_delete(e):
            page.close(confirm_dialog)
            # Delete all user data
            user_id = state.get("user_id")
            if user_id:
                try:
                    # Create a connection for this operation
                    conn = db.connect_db()
                    cursor = conn.cursor()
                    
                    # Delete all expenses
                    cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
                    # Delete all accounts
                    cursor.execute("DELETE FROM accounts WHERE user_id = ?", (user_id,))
                    # Delete passcode
                    cursor.execute("DELETE FROM passcodes WHERE user_id = ?", (user_id,))
                    # Delete user profile
                    cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
                    # Delete user
                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                    conn.close()
                    
                    # Clear state immediately
                    state["user_id"] = None
                    state["editing_id"] = None
                    
                    # Logout directly - no delay needed
                    if logout_callback:
                        logout_callback()
                    
                except Exception as ex:
                    if 'conn' in locals():
                        conn.rollback()
                        conn.close()
                    toast(f"Error deleting data: {str(ex)}", "#EF4444")
        
        def cancel_delete(e):
            page.close(confirm_dialog)
        
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete profile and all data?", color=theme.text_primary, weight=ft.FontWeight.BOLD, size=18),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "All financial transaction, bank connection and profile information is irreversibly deleted and all data is lost.",
                        color=theme.text_secondary,
                        size=13,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "No ongoing subscription can be used for a new registration and must be terminated manually.",
                        color=theme.text_secondary,
                        size=13,
                    ),
                ],
                tight=True,
            ),
            bgcolor=theme.bg_card,
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=cancel_delete,
                    style=ft.ButtonStyle(color=theme.accent_primary),
                ),
                ft.TextButton(
                    "Delete",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color="#EF4444"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(confirm_dialog)
    
    def show_privacy_policy(e):
        """Show privacy policy dialog."""
        policy_content = """
Our Privacy Policy

1. Data Collection
We collect only the data necessary to provide our expense tracking services:
- Personal information (name, email)
- Financial data (expenses, accounts, balances)
- Usage data (preferences, settings)

2. Data Usage
Your data is used exclusively for:
- Providing expense tracking functionality
- Generating financial reports and statistics
- Improving user experience

3. Data Storage
- All data is stored locally on your device
- No data is shared with third parties
- You have full control over your data

4. Your Rights
You have the right to:
- Access your data at any time
- Modify or delete your data
- Export your data
- Request data portability

5. Security
We implement industry-standard security measures to protect your data.

6. Contact
For privacy concerns, contact us at support@expensetracker.com
        """
        
        policy_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Privacy Policy", color=theme.text_primary, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Text(
                    policy_content,
                    color=theme.text_secondary,
                    size=13,
                    selectable=True,
                ),
                height=400,
                padding=10,
            ),
            bgcolor=theme.bg_card,
            actions=[
                ft.TextButton("Close", on_click=lambda e: page.close(policy_dialog)),
            ],
        )
        page.open(policy_dialog)
    
    def show_terms_of_service(e):
        """Show terms of service dialog."""
        terms_content = """
Terms of Service

1. Acceptance of Terms
By using this expense tracker application, you agree to these terms.

2. Service Description
This application provides personal expense tracking and financial management tools.

3. User Responsibilities
You are responsible for:
- Maintaining the security of your account
- Accuracy of the data you input
- Compliance with applicable laws

4. Data Accuracy
While we strive for accuracy, we are not responsible for financial decisions based on the app's data or calculations.

5. Modifications
We reserve the right to modify these terms at any time. Continued use of the app constitutes acceptance of changes.

6. Termination
You may terminate your account at any time by deleting all user data.

7. Limitation of Liability
The app is provided "as is" without warranties. We are not liable for any damages arising from use of the app.

8. Governing Law
These terms are governed by applicable local laws.

9. Contact
For questions about these terms, contact us at support@expensetracker.com
        """
        
        terms_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Terms of Service", color=theme.text_primary, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Text(
                    terms_content,
                    color=theme.text_secondary,
                    size=13,
                    selectable=True,
                ),
                height=400,
                padding=10,
            ),
            bgcolor=theme.bg_card,
            actions=[
                ft.TextButton("Close", on_click=lambda e: page.close(terms_dialog)),
            ],
        )
        page.open(terms_dialog)
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=theme.text_primary,
                    on_click=lambda e: go_back() if go_back else None,
                ),
                ft.Text(
                    "Personal data & Privacy",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=theme.text_primary,
                    expand=True,
                ),
            ],
        ),
        padding=ft.padding.only(top=10, bottom=16),
    )
    
    # Documents section
    documents_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "DOCUMENTS TO REVIEW",
                    size=11,
                    color=theme.text_muted,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=12),
                # Privacy Policy
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SHIELD_OUTLINED, color="#3B82F6", size=24),
                            ft.Text(
                                "Privacy Policy",
                                size=16,
                                color=theme.text_primary,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                    ink=True,
                    on_click=show_privacy_policy,
                ),
                ft.Container(height=8),
                # Terms of Service
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color="#3B82F6", size=24),
                            ft.Text(
                                "Terms of Services",
                                size=16,
                                color=theme.text_primary,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=theme.text_muted, size=20),
                        ],
                        spacing=12,
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                    ink=True,
                    on_click=show_terms_of_service,
                ),
            ],
        ),
    )
    
    # Email toggle (state management)
    email_toggle_value = {"enabled": True}
    
    def toggle_emails(e):
        email_toggle_value["enabled"] = e.control.value
        if email_toggle_value["enabled"]:
            toast("Email notifications enabled", "#10B981")
        else:
            toast("Email notifications disabled", "#EF4444")
    
    email_toggle = ft.Switch(
        value=email_toggle_value["enabled"],
        active_color=theme.accent_primary,
        on_change=toggle_emails,
    )
    
    # Email settings section
    email_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "EMAILS & MESSAGES SETTINGS",
                    size=11,
                    color=theme.text_muted,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=12),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Email and messages",
                                size=16,
                                color=theme.text_primary,
                                expand=True,
                            ),
                            email_toggle,
                        ],
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor=theme.bg_card,
                ),
                ft.Container(height=8),
                ft.Text(
                    "You can turn off all promotional and commercial content using the button above. This will not affect service messages like password change alerts.",
                    size=12,
                    color=theme.text_secondary,
                ),
            ],
        ),
    )
    
    # Data portability section
    data_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "DATA PORTABILITY",
                    size=11,
                    color=theme.text_muted,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=12),
                ft.Text(
                    "You have right to change your personal data by editing your profile information, change your transaction data for cash accounts by editing them. You can delete your transactions from linked account by deleting the whole set of transaction - those data are not editable.",
                    size=13,
                    color=theme.text_secondary,
                ),
                ft.Container(height=16),
                ft.Text(
                    "You have right to be informed about the data we hold about you and you can transfer your data and you have right to be forgotten and delete all your data - all of which you can do by sending us an email to support@expensetracker.com. In case you have any specific issues or request, please contact our Data Protection Officer on email: dpo@expensetracker.com",
                    size=13,
                    color=theme.text_secondary,
                ),
            ],
        ),
    )
    
    # Delete section
    delete_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Delete all user data",
                    size=16,
                    color="#EF4444",
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=16),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Delete Profile and all data",
                        size=16,
                        color="white",
                        weight=ft.FontWeight.W_600,
                    ),
                    bgcolor="#EF4444",
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=16,
                    ),
                    width=300,
                    height=56,
                    on_click=delete_all_data,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    
    # Scrollable content
    scrollable = ft.Column(
        controls=[
            documents_section,
            ft.Container(height=24),
            email_section,
            ft.Container(height=24),
            data_section,
            ft.Container(height=32),
            delete_section,
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
