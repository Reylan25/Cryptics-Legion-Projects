# src/core/theme.py
"""
Theme Manager for Smart Expense Tracker
Provides consistent color palettes for Light and Dark modes
"""

class ThemeColors:
    """Color palette container for a theme."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Dark Mode Theme (Default)
DARK_THEME = ThemeColors(
    # Backgrounds
    bg_primary="#0a0a14",
    bg_secondary="#0f0f23",
    bg_card="#1a1a2e",
    bg_field="#252538",
    bg_elevated="#1F2937",
    bg_gradient_start="#0f0f23",
    bg_gradient_end="#12002e",
    
    # Text
    text_primary="#FFFFFF",
    text_secondary="#9CA3AF",
    text_muted="#6B7280",
    text_hint="#4B5563",
    
    # Borders
    border_primary="#333355",
    border_secondary="#2D2D44",
    border_light="#404060",
    
    # Accent Colors (Purple/Indigo)
    accent_primary="#6366F1",
    accent_secondary="#818CF8",
    accent_light="#A5B4FC",
    accent_bg="#1e1b4b",
    
    # Teal Accent
    teal_primary="#14B8A6",
    teal_secondary="#2DD4BF",
    teal_bg="#0D3D38",
    
    # Status Colors
    success="#10B981",
    success_bg="#064E3B",
    warning="#F59E0B",
    warning_bg="#78350F",
    error="#EF4444",
    error_bg="#7F1D1D",
    info="#3B82F6",
    info_bg="#1E3A5F",
    
    # Gradients
    gradient_start="#0f0f23",
    gradient_end="#0a0a14",
    gradient_purple_start="#2b0057",
    gradient_purple_end="#000000",
    
    # Navigation
    nav_bg="#0a0a14",
    nav_active="#6366F1",
    nav_inactive="#6B7280",
    
    # Category Colors (kept consistent in both themes)
    category_food="#FF6B6B",
    category_transport="#4ECDC4",
    category_shopping="#45B7D1",
    category_bills="#96CEB4",
    category_entertainment="#DDA0DD",
    category_health="#F7DC6F",
    category_education="#BB8FCE",
    category_other="#85C1E9",
    
    # Mode identifier
    is_dark=True,
    mode_name="dark",
    mode="dark",
)


# Light Mode Theme
LIGHT_THEME = ThemeColors(
    # Backgrounds
    bg_primary="#F8FAFC",
    bg_secondary="#FFFFFF",
    bg_card="#FFFFFF",
    bg_field="#F1F5F9",
    bg_elevated="#FFFFFF",
    bg_gradient_start="#E0E7FF",
    bg_gradient_end="#FFFFFF",
    
    # Text
    text_primary="#1E293B",
    text_secondary="#475569",
    text_muted="#64748B",
    text_hint="#94A3B8",
    
    # Borders
    border_primary="#E2E8F0",
    border_secondary="#CBD5E1",
    border_light="#F1F5F9",
    
    # Accent Colors (Purple/Indigo - slightly adjusted for light mode)
    accent_primary="#6366F1",
    accent_secondary="#4F46E5",
    accent_light="#C7D2FE",
    accent_bg="#EEF2FF",
    
    # Teal Accent
    teal_primary="#0D9488",
    teal_secondary="#14B8A6",
    teal_bg="#CCFBF1",
    
    # Status Colors
    success="#059669",
    success_bg="#D1FAE5",
    warning="#D97706",
    warning_bg="#FEF3C7",
    error="#DC2626",
    error_bg="#FEE2E2",
    info="#2563EB",
    info_bg="#DBEAFE",
    
    # Gradients
    gradient_start="#FFFFFF",
    gradient_end="#F8FAFC",
    gradient_purple_start="#E0E7FF",
    gradient_purple_end="#FFFFFF",
    
    # Navigation
    nav_bg="#FFFFFF",
    nav_active="#6366F1",
    nav_inactive="#94A3B8",
    
    # Category Colors (kept consistent in both themes)
    category_food="#FF6B6B",
    category_transport="#4ECDC4",
    category_shopping="#45B7D1",
    category_bills="#96CEB4",
    category_entertainment="#DDA0DD",
    category_health="#F7DC6F",
    category_education="#BB8FCE",
    category_other="#85C1E9",
    
    # Mode identifier
    is_dark=False,
    mode_name="light",
    mode="light",
)


class ThemeManager:
    """Manages theme state and switching."""
    
    _current_theme = DARK_THEME
    _listeners = []
    
    @classmethod
    def get_theme(cls) -> ThemeColors:
        """Get the current theme."""
        return cls._current_theme
    
    @classmethod
    def set_dark_mode(cls):
        """Switch to dark mode."""
        cls._current_theme = DARK_THEME
        cls._notify_listeners()
    
    @classmethod
    def set_light_mode(cls):
        """Switch to light mode."""
        cls._current_theme = LIGHT_THEME
        cls._notify_listeners()
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark mode."""
        if cls._current_theme.is_dark:
            cls.set_light_mode()
        else:
            cls.set_dark_mode()
        return cls._current_theme
    
    @classmethod
    def is_dark_mode(cls) -> bool:
        """Check if current theme is dark mode."""
        return cls._current_theme.is_dark
    
    @classmethod
    def add_listener(cls, callback):
        """Add a listener for theme changes."""
        cls._listeners.append(callback)
    
    @classmethod
    def remove_listener(cls, callback):
        """Remove a theme change listener."""
        if callback in cls._listeners:
            cls._listeners.remove(callback)
    
    @classmethod
    def _notify_listeners(cls):
        """Notify all listeners of theme change."""
        for listener in cls._listeners:
            try:
                listener(cls._current_theme)
            except:
                pass


# Convenience function
def get_theme() -> ThemeColors:
    """Get the current theme colors."""
    return ThemeManager.get_theme()
