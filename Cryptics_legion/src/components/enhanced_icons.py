# src/components/enhanced_icons.py
import flet as ft

class EnhancedIconButton:
    """
    Enhanced icon button with hover effects, ripple animations, and better styling.
    """
    
    @staticmethod
    def create(
        icon: str,
        on_click=None,
        icon_size: int = 24,
        icon_color: str = None,
        tooltip: str = None,
        selected_icon: str = None,
        bg_color: str = None,
        hover_color: str = None,
        theme=None,
        enable_ripple: bool = True,
    ):
        """Create an enhanced icon button."""
        
        # Default colors from theme if provided
        if theme:
            icon_color = icon_color or theme.text_secondary
            bg_color = bg_color or "transparent"
            hover_color = hover_color or f"{theme.accent_primary}15"
        else:
            icon_color = icon_color or "#6B7280"
            bg_color = bg_color or "transparent"
            hover_color = hover_color or "#3B82F615"
        
        return ft.IconButton(
            icon=icon,
            selected_icon=selected_icon or icon,
            icon_size=icon_size,
            icon_color=icon_color,
            on_click=on_click,
            tooltip=tooltip,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                bgcolor=bg_color,
                overlay_color={
                    ft.MaterialState.HOVERED: hover_color,
                    ft.MaterialState.PRESSED: hover_color.replace("15", "25") if "15" in hover_color else hover_color,
                },
                shadow_color=f"{icon_color}20" if enable_ripple else None,
            ),
        )


class EnhancedIcon:
    """
    Enhanced icon with container, background, and animation options.
    """
    
    @staticmethod
    def create(
        icon: str,
        size: int = 24,
        color: str = None,
        bg_color: str = None,
        border_radius: int = None,
        padding: int = None,
        shadow: bool = False,
        gradient: list = None,
        theme=None,
    ):
        """Create an enhanced icon with optional container styling."""
        
        # Default color from theme if provided
        if theme:
            color = color or theme.text_primary
        else:
            color = color or "#FFFFFF"
        
        icon_widget = ft.Icon(icon, size=size, color=color)
        
        # If no container styling needed, return plain icon
        if not (bg_color or border_radius or padding or shadow or gradient):
            return icon_widget
        
        # Create container with styling
        container_kwargs = {
            "content": icon_widget,
            "alignment": ft.alignment.center,
        }
        
        if bg_color:
            container_kwargs["bgcolor"] = bg_color
        
        if gradient:
            container_kwargs["gradient"] = ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=gradient,
            )
        
        if border_radius:
            container_kwargs["border_radius"] = border_radius
        
        if padding:
            container_kwargs["padding"] = padding
        
        if shadow:
            container_kwargs["shadow"] = ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=f"{color}30",
                offset=ft.Offset(0, 4),
            )
        
        # Calculate container size if padding is specified
        if padding:
            container_kwargs["width"] = size + (padding * 2)
            container_kwargs["height"] = size + (padding * 2)
        
        return ft.Container(**container_kwargs)


class CategoryIcon:
    """
    Category-specific icon with branded colors and styling.
    """
    
    @staticmethod
    def create(category: str, size: int = 40, theme=None):
        """Create a category icon with appropriate styling."""
        
        # Category icon mapping with gradients
        categories = {
            "Food & Dining": {
                "icon": ft.Icons.RESTAURANT_ROUNDED,
                "gradient": ["#F59E0B", "#D97706"],
                "shadow_color": "#F59E0B40",
            },
            "Transport": {
                "icon": ft.Icons.DIRECTIONS_CAR_ROUNDED,
                "gradient": ["#3B82F6", "#2563EB"],
                "shadow_color": "#3B82F640",
            },
            "Shopping": {
                "icon": ft.Icons.SHOPPING_BAG_ROUNDED,
                "gradient": ["#EC4899", "#DB2777"],
                "shadow_color": "#EC489940",
            },
            "Entertainment": {
                "icon": ft.Icons.MOVIE_ROUNDED,
                "gradient": ["#8B5CF6", "#7C3AED"],
                "shadow_color": "#8B5CF640",
            },
            "Bills & Utilities": {
                "icon": ft.Icons.RECEIPT_LONG_ROUNDED,
                "gradient": ["#EF4444", "#DC2626"],
                "shadow_color": "#EF444440",
            },
            "Health": {
                "icon": ft.Icons.FAVORITE_ROUNDED,
                "gradient": ["#EF4444", "#DC2626"],
                "shadow_color": "#EF444440",
            },
            "Education": {
                "icon": ft.Icons.SCHOOL_ROUNDED,
                "gradient": ["#3B82F6", "#2563EB"],
                "shadow_color": "#3B82F640",
            },
            "Groceries": {
                "icon": ft.Icons.LOCAL_GROCERY_STORE_ROUNDED,
                "gradient": ["#10B981", "#059669"],
                "shadow_color": "#10B98140",
            },
            "Travel": {
                "icon": ft.Icons.FLIGHT_ROUNDED,
                "gradient": ["#06B6D4", "#0891B2"],
                "shadow_color": "#06B6D440",
            },
            "Other": {
                "icon": ft.Icons.MORE_HORIZ_ROUNDED,
                "gradient": ["#6B7280", "#4B5563"],
                "shadow_color": "#6B728040",
            },
        }
        
        cat_data = categories.get(category, categories["Other"])
        
        return ft.Container(
            content=ft.Icon(
                cat_data["icon"],
                size=size * 0.55,
                color="#FFFFFF",
            ),
            width=size,
            height=size,
            border_radius=size // 2,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=cat_data["gradient"],
            ),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=cat_data["shadow_color"],
                offset=ft.Offset(0, 4),
            ),
        )


class ActionButton:
    """
    Enhanced action button with icon and styling.
    """
    
    @staticmethod
    def create(
        icon: str,
        on_click=None,
        size: int = 56,
        icon_size: int = 28,
        bg_gradient: list = None,
        bg_color: str = "#10B981",
        tooltip: str = None,
        theme=None,
    ):
        """Create a floating action button style button."""
        
        if bg_gradient is None:
            bg_gradient = [bg_color, bg_color]
        
        return ft.Container(
            content=ft.Icon(icon, size=icon_size, color="#FFFFFF"),
            width=size,
            height=size,
            border_radius=size // 2,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=bg_gradient,
            ),
            alignment=ft.alignment.center,
            on_click=on_click,
            ink=True,
            tooltip=tooltip,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=16,
                color=f"{bg_gradient[0]}60",
                offset=ft.Offset(0, 6),
            ),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
