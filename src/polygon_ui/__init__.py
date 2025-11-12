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


def hello():
    return "Hello from polygon_ui!"
