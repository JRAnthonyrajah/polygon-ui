"""
Polygon UI

Description: A library/framework of UI components for Qt/PySide, similar to Mantine for webapps
"""

__version__ = "0.1.0"

# Core imports
from .core import PolygonProvider, PolygonComponent, ComponentFactory
from .theme import Theme, ThemeProvider, Colors, Spacing, Typography
from .styles import StyleProps, StylesAPI, QSSGenerator
from .utils import css_var_to_qss, generate_color_shades, VariantSystem
from .polybook import PolyBookApp, ComponentRegistry, Story, StoryManager

# Layout system
try:
    from .layout.core import (
        LayoutComponent,
        GridComponent,
        UtilityComponent,
        Breakpoint,
        BreakpointSystem,
        ResponsiveProps,
        responsive,
        cols,
        spacing,
    )

    _layout_core_available = True
except ImportError:
    # Layout core not available
    _layout_core_available = False

# Layout components (not yet implemented)
_layout_components_available = False

__all__ = [
    # Core
    "PolygonProvider",
    "PolygonComponent",
    "ComponentFactory",
    # Theme
    "Theme",
    "ThemeProvider",
    "Colors",
    "Spacing",
    "Typography",
    # Styles
    "StyleProps",
    "StylesAPI",
    "QSSGenerator",
    # Utils
    "css_var_to_qss",
    "generate_color_shades",
    "VariantSystem",
    # PolyBook
    "PolyBookApp",
    "ComponentRegistry",
    "Story",
    "StoryManager",
]

# Add layout components to exports if available
if _layout_core_available:
    __all__.extend(
        [
            # Layout Core
            "LayoutComponent",
            "GridComponent",
            "UtilityComponent",
            "Breakpoint",
            "BreakpointSystem",
            "ResponsiveProps",
            "responsive",
            "cols",
            "spacing",
        ]
    )


def hello():
    return "Hello from polygon_ui!"
