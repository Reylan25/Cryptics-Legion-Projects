# src/components/notification.py
import flet as ft
from typing import Literal
import asyncio
from datetime import datetime
from core import db

class NotificationHistory:
    """
    Manages notification history and displays a notification center UI.
    """
    _instance = None
    _notifications = []
    _current_user_id = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationHistory, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def add_notification(cls, title: str, message: str, type: str, timestamp: datetime = None):
        """Add a notification to history."""
        if timestamp is None:
            timestamp = datetime.now()
        
        notification = {
            "title": title,
            "message": message,
            "type": type,
            "timestamp": timestamp,
            "read": False,
        }
        cls._notifications.insert(0, notification)  # Add to beginning
        
        # Keep only last 50 notifications
        if len(cls._notifications) > 50:
            cls._notifications = cls._notifications[:50]
    
    @classmethod
    def load_user_notifications(cls, user_id: int):
        """Load notifications from database for a user."""
        cls._current_user_id = user_id  # Store for future operations
        notifications = db.get_user_notifications(user_id, include_read=True, limit=50)
        cls._notifications.clear()
        
        for notif in notifications:
            notif_id, announcement_id, title, message, notif_type, is_read, read_at, created_at = notif
            
            # Parse datetime
            try:
                timestamp = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            except:
                timestamp = datetime.now()
            
            cls._notifications.append({
                "id": notif_id,
                "title": title,
                "message": message,
                "type": notif_type,
                "timestamp": timestamp,
                "read": bool(is_read),
            })
    
    @classmethod
    def get_all_notifications(cls):
        """Get all notifications."""
        return cls._notifications
    
    @classmethod
    def get_unread_count(cls):
        """Get count of unread notifications."""
        return sum(1 for n in cls._notifications if not n["read"])
    
    @classmethod
    def mark_all_read(cls):
        """Mark all notifications as read and save to database."""
        for n in cls._notifications:
            if not n["read"] and "id" in n:
                try:
                    db.mark_notification_read(n["id"])
                except Exception as e:
                    print(f"Error marking notification {n.get('id')} as read: {e}")
            n["read"] = True
    
    @classmethod
    def mark_notification_read(cls, notification_id: int):
        """Mark a specific notification as read in database."""
        try:
            db.mark_notification_read(notification_id)
            # Update in memory
            for n in cls._notifications:
                if n.get("id") == notification_id:
                    n["read"] = True
                    break
        except Exception as e:
            print(f"Error marking notification {notification_id} as read: {e}")
    
    @classmethod
    def clear_all(cls):
        """Clear all notifications from memory (does not delete from database)."""
        cls._notifications.clear()
    
    @classmethod
    def refresh_from_database(cls, user_id: int):
        """Reload notifications from database for the current user."""
        cls.load_user_notifications(user_id)
    
    @classmethod
    def on_user_logout(cls):
        """Clean up notifications when user logs out."""
        # Save any pending read states before clearing
        for n in cls._notifications:
            if n["read"] and "id" in n:
                try:
                    db.mark_notification_read(n["id"])
                except:
                    pass
        # Clear memory
        cls._notifications.clear()
        cls._current_user_id = None


class ImmersiveNotification:
    """
    Beautiful, immersive notification system with animations and icons.
    Supports success, error, warning, and info notification types.
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.notification_queue = []
        self.current_notification = None
        
    def show(
        self, 
        message: str, 
        type: Literal["success", "error", "warning", "info"] = "success",
        duration: int = 3000,
        title: str = None
    ):
        """
        Show an immersive notification.
        
        Args:
            message: The notification message
            type: Type of notification (success, error, warning, info)
            duration: Duration in milliseconds (default 3000)
            title: Optional title for the notification
        """
        
        # Define notification styles based on type
        styles = {
            "success": {
                "bg_color": "#10B981",
                "icon": ft.Icons.CHECK_CIRCLE_ROUNDED,
                "icon_color": "#FFFFFF",
                "title": title or "Success",
                "gradient": ["#10B981", "#059669"],
            },
            "error": {
                "bg_color": "#EF4444",
                "icon": ft.Icons.ERROR_ROUNDED,
                "icon_color": "#FFFFFF",
                "title": title or "Error",
                "gradient": ["#EF4444", "#DC2626"],
            },
            "warning": {
                "bg_color": "#F59E0B",
                "icon": ft.Icons.WARNING_ROUNDED,
                "icon_color": "#FFFFFF",
                "title": title or "Warning",
                "gradient": ["#F59E0B", "#D97706"],
            },
            "info": {
                "bg_color": "#3B82F6",
                "icon": ft.Icons.INFO_ROUNDED,
                "icon_color": "#FFFFFF",
                "title": title or "Info",
                "gradient": ["#3B82F6", "#2563EB"],
            },
        }
        
        style = styles.get(type, styles["success"])
        
        # Add to notification history
        NotificationHistory.add_notification(
            title=style["title"],
            message=message,
            type=type,
            timestamp=datetime.now()
        )
        
        # Create notification container
        notification_container = ft.Container(
            content=ft.Row(
                controls=[
                    # Icon
                    ft.Container(
                        content=ft.Icon(
                            style["icon"],
                            size=28,
                            color=style["icon_color"],
                        ),
                        width=50,
                        height=50,
                        border_radius=25,
                        bgcolor=f"{style['bg_color']}30",
                        alignment=ft.alignment.center,
                    ),
                    # Message content
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    style["title"],
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF",
                                ),
                                ft.Text(
                                    message,
                                    size=12,
                                    color="#FFFFFF",
                                    opacity=0.9,
                                ),
                            ],
                            spacing=2,
                            tight=True,
                        ),
                        expand=True,
                    ),
                    # Close button
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_size=18,
                        icon_color="#FFFFFF",
                        on_click=lambda e: self._hide_notification(),
                        tooltip="Close",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            bgcolor=style["bg_color"],
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=style["gradient"],
            ),
            padding=ft.padding.only(left=16, right=8, top=12, bottom=12),
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=f"{style['bg_color']}60",
                offset=ft.Offset(0, 4),
            ),
            width=350,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            offset=(-2, 0),
            opacity=0,
        )
        
        # Create banner at the top of the page
        banner = ft.Container(
            content=notification_container,
            alignment=ft.alignment.top_center,
            padding=ft.padding.only(top=20),
        )
        
        # Store reference
        self.current_notification = banner
        
        # Add to page overlay
        self.page.overlay.append(banner)
        self.page.update()
        
        # Animate in
        notification_container.offset = (0, 0)
        notification_container.opacity = 1
        self.page.update()
        
        # Auto-hide after duration
        import threading
        def auto_hide():
            import time
            time.sleep(duration / 1000)
            self._hide_notification()
        
        threading.Thread(target=auto_hide, daemon=True).start()
    
    def _hide_notification(self):
        """Hide the current notification with animation."""
        if self.current_notification and len(self.page.overlay) > 0:
            try:
                notification_container = self.current_notification.content
                
                # Animate out
                notification_container.offset = (-2, 0)
                notification_container.opacity = 0
                self.page.update()
                
                # Remove after animation
                import threading
                def remove():
                    import time
                    time.sleep(0.3)
                    if self.current_notification in self.page.overlay:
                        self.page.overlay.remove(self.current_notification)
                        self.current_notification = None
                        self.page.update()
                
                threading.Thread(target=remove, daemon=True).start()
            except Exception:
                pass


class SnackbarNotification:
    """
    Bottom snackbar notification (alternative style).
    """
    
    @staticmethod
    def show(
        page: ft.Page,
        message: str,
        type: Literal["success", "error", "warning", "info"] = "success",
        duration: int = 3000,
        action_label: str = None,
        action_callback = None
    ):
        """Show a snackbar notification at the bottom of the screen."""
        
        styles = {
            "success": {"bg": "#10B981", "icon": ft.Icons.CHECK_CIRCLE},
            "error": {"bg": "#EF4444", "icon": ft.Icons.ERROR},
            "warning": {"bg": "#F59E0B", "icon": ft.Icons.WARNING},
            "info": {"bg": "#3B82F6", "icon": ft.Icons.INFO},
        }
        
        style = styles.get(type, styles["success"])
        
        snackbar_content = ft.Row(
            controls=[
                ft.Icon(style["icon"], size=20, color="#FFFFFF"),
                ft.Text(message, size=14, color="#FFFFFF", expand=True),
            ],
            spacing=12,
        )
        
        if action_label and action_callback:
            snackbar_content.controls.append(
                ft.TextButton(
                    action_label,
                    style=ft.ButtonStyle(color="#FFFFFF"),
                    on_click=action_callback,
                )
            )
        
        snackbar = ft.SnackBar(
            content=snackbar_content,
            bgcolor=style["bg"],
            duration=duration,
            action="CLOSE" if not action_label else None,
        )
        
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()


def show_success_notification(page: ft.Page, message: str, title: str = None):
    """Quick helper to show success notification."""
    notif = ImmersiveNotification(page)
    notif.show(message, "success", title=title)


def show_error_notification(page: ft.Page, message: str, title: str = None):
    """Quick helper to show error notification."""
    notif = ImmersiveNotification(page)
    notif.show(message, "error", title=title)


def show_warning_notification(page: ft.Page, message: str, title: str = None):
    """Quick helper to show warning notification."""
    notif = ImmersiveNotification(page)
    notif.show(message, "warning", title=title)


def show_info_notification(page: ft.Page, message: str, title: str = None):
    """Quick helper to show info notification."""
    notif = ImmersiveNotification(page)
    notif.show(message, "info", title=title)


class NotificationCenter:
    """
    Notification Center UI with bell icon and history panel.
    """
    
    def __init__(self, page: ft.Page, theme):
        self.page = page
        self.theme = theme
        self.panel_visible = False
        self.notification_panel = None
        self.badge = None
        self.bell_button = None
        
    def create_bell_icon(self):
        """Create the notification bell icon with badge."""
        unread_count = NotificationHistory.get_unread_count()
        
        # Badge for unread count with pulsing animation
        self.badge = ft.Container(
            content=ft.Text(
                str(unread_count) if unread_count > 0 else "",
                size=10,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            width=18,
            height=18,
            border_radius=9,
            bgcolor="#EF4444",
            alignment=ft.alignment.center,
            visible=unread_count > 0,
            top=-2,
            right=-2,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#EF444460",
                offset=ft.Offset(0, 2),
            ),
        )
        
        # Bell icon button with hover effect
        bell_icon = ft.IconButton(
            icon=ft.Icons.NOTIFICATIONS_OUTLINED,
            selected_icon=ft.Icons.NOTIFICATIONS_ROUNDED,
            icon_size=24,
            icon_color=self.theme.text_secondary,
            selected_icon_color=self.theme.accent_primary,
            on_click=self._toggle_panel,
            tooltip="Notifications",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                overlay_color={
                    ft.ControlState.HOVERED: f"{self.theme.accent_primary}15",
                    ft.ControlState.PRESSED: f"{self.theme.accent_primary}25",
                },
            ),
        )
        
        # Stack to show badge over icon
        self.bell_button = ft.Stack(
            controls=[
                bell_icon,
                self.badge,
            ],
            width=48,
            height=48,
        )
        
        return self.bell_button
    
    def update_badge(self):
        """Update the notification badge count."""
        if self.badge:
            unread_count = NotificationHistory.get_unread_count()
            self.badge.content.value = str(unread_count) if unread_count > 0 else ""
            self.badge.visible = unread_count > 0
            self.page.update()
    
    def _toggle_panel(self, e):
        """Toggle notification panel visibility."""
        if self.panel_visible:
            self._hide_panel()
        else:
            self._show_panel()
    
    def _show_panel(self):
        """Show the notification panel."""
        # Mark all as read
        NotificationHistory.mark_all_read()
        self.update_badge()
        
        # Get all notifications
        notifications = NotificationHistory.get_all_notifications()
        
        # Create notification items
        notification_items = []
        
        if not notifications:
            notification_items.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.NOTIFICATIONS_OFF_OUTLINED, size=48, color=self.theme.text_muted),
                            ft.Text("No notifications yet", size=14, color=self.theme.text_muted, weight=ft.FontWeight.W_500),
                            ft.Text("You're all caught up!", size=11, color=self.theme.text_muted),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=30,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for notif in notifications:
                notification_items.append(self._create_notification_item(notif))
        
        # Create panel - responsive sizing for mobile
        panel_width = min(self.page.width - 40, 380) if self.page.width else 380
        panel_height = min(self.page.height - 100, 500) if self.page.height else 500
        
        self.notification_panel = ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    "Notifications",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.theme.text_primary,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            "Clear All",
                                            on_click=self._clear_all,
                                            style=ft.ButtonStyle(
                                                color=self.theme.text_secondary,
                                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                            ),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CLOSE,
                                            icon_size=20,
                                            icon_color=self.theme.text_secondary,
                                            on_click=lambda e: self._hide_panel(),
                                        ),
                                    ],
                                    spacing=0,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=ft.padding.only(left=16, right=4, top=12, bottom=8),
                        border=ft.border.only(bottom=ft.BorderSide(1, self.theme.border_primary)),
                    ),
                    # Notification list
                    ft.Container(
                        content=ft.Column(
                            controls=notification_items,
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
            width=panel_width,
            height=panel_height,
            bgcolor=self.theme.bg_secondary,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=24,
                color="#00000040",
                offset=ft.Offset(0, 8),
            ),
            right=20,
            top=70,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            opacity=0,
            scale=0.95,
        )
        
        # Add to overlay
        self.page.overlay.append(self.notification_panel)
        self.page.update()
        
        # Animate in
        self.notification_panel.opacity = 1
        self.notification_panel.scale = 1
        self.page.update()
        
        self.panel_visible = True
    
    def _hide_panel(self):
        """Hide the notification panel."""
        if self.notification_panel:
            # Animate out
            self.notification_panel.opacity = 0
            self.notification_panel.scale = 0.95
            self.page.update()
            
            # Remove after animation
            import threading
            def remove():
                import time
                time.sleep(0.3)
                if self.notification_panel in self.page.overlay:
                    self.page.overlay.remove(self.notification_panel)
                    self.notification_panel = None
                    self.page.update()
            
            threading.Thread(target=remove, daemon=True).start()
        
        self.panel_visible = False
    
    def close_panel(self):
        """Close the notification panel immediately (called during navigation)."""
        if self.notification_panel and self.panel_visible:
            # Remove immediately without animation
            if self.notification_panel in self.page.overlay:
                self.page.overlay.remove(self.notification_panel)
            self.notification_panel = None
            self.panel_visible = False
    
    def _create_notification_item(self, notif):
        """Create a single notification item."""
        # Icon based on type
        icon_map = {
            "success": (ft.Icons.CHECK_CIRCLE_ROUNDED, "#10B981"),
            "error": (ft.Icons.ERROR_ROUNDED, "#EF4444"),
            "warning": (ft.Icons.WARNING_ROUNDED, "#F59E0B"),
            "info": (ft.Icons.INFO_ROUNDED, "#3B82F6"),
        }
        
        icon, color = icon_map.get(notif["type"], icon_map["info"])
        
        # Format timestamp
        timestamp = notif["timestamp"]
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            time_str = f"{diff.days}d ago"
        elif diff.seconds >= 3600:
            time_str = f"{diff.seconds // 3600}h ago"
        elif diff.seconds >= 60:
            time_str = f"{diff.seconds // 60}m ago"
        else:
            time_str = "Just now"
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Icon
                    ft.Container(
                        content=ft.Icon(icon, size=18, color=color),
                        width=36,
                        height=36,
                        border_radius=18,
                        bgcolor=f"{color}20",
                        alignment=ft.alignment.center,
                    ),
                    # Content
                    ft.Column(
                        controls=[
                            ft.Text(
                                notif["title"],
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme.text_primary,
                            ),
                            ft.Text(
                                notif["message"],
                                size=11,
                                color=self.theme.text_secondary,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                time_str,
                                size=10,
                                color=self.theme.text_muted,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            padding=12,
            border=ft.border.only(bottom=ft.BorderSide(1, self.theme.border_primary)),
            ink=True,
            on_click=lambda e: None,  # Could add detail view here
        )
    
    def _clear_all(self, e):
        """Clear all notifications."""
        NotificationHistory.clear_all()
        self._hide_panel()
        self.update_badge()

