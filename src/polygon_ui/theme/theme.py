from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum

from .colors import Colors
from .theme_types import ColorScheme, Radius
from .typography import Typography
from .spacing import Spacing
from .components import ComponentStyles


class Theme:
    """Complete theme definition with colors, typography, spacing, and design tokens."""

    def __init__(
        self,
        color_scheme: ColorScheme = ColorScheme.LIGHT,
        primary_color: str = "blue",
        colors: Colors = None,
        radius: Dict[str, int] = None,
        spacing: Spacing = None,
        typography: Typography = None,
        shadows: Dict[str, str] = None,
        breakpoints: Dict[str, int] = None,
        **kwargs: Any,
    ):
        self.color_scheme = color_scheme
        self.primary_color = primary_color
        self.colors = colors or Colors()
        self.radius = radius or {"xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16}
        self.spacing = spacing or Spacing()
        self.typography = typography or Typography()
        self.components = ComponentStyles(self.colors)

        # Store theme state for dark mode detection
        self.colors._is_dark = color_scheme == ColorScheme.DARK

        self.shadows = shadows or {
            "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        }
        self.breakpoints = breakpoints or {
            "sm": 640,
            "md": 768,
            "lg": 1024,
            "xl": 1280,
            "2xl": 1536,
        }

        # Apply any additional keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

    def validate(self) -> None:
        """Validate theme design tokens."""
        # Validate colors
        self.colors.validate()

        # Validate radius
        for size, value in self.radius.items():
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"Radius '{size}' must be non-negative int: {value}")

        # Validate shadows (basic string check)
        for size, shadow in self.shadows.items():
            if not isinstance(shadow, str) or (
                "rgba" not in shadow and "rgb" not in shadow
            ):
                raise ValueError(f"Shadow '{size}' must be valid CSS shadow: {shadow}")

        # Validate breakpoints
        for size, value in self.breakpoints.items():
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"Breakpoint '{size}' must be positive int: {value}")

        # Validate spacing and typography via their methods if available
        if hasattr(self.spacing, "validate"):
            self.spacing.validate()
        if hasattr(self.typography, "validate"):
            self.typography.validate()

    def get_color(self, color_name: str, shade: int = None) -> str:
        """Get a specific color shade from the palette."""
        return self.colors.get_color(color_name, shade)

    def get_primary_color(self, shade: int = 5) -> str:
        """Get the primary color at a specific shade."""
        return self.colors.get_color(self.primary_color, shade)

    def get_button_style(
        self, variant: str = "primary", size: str = "md", state: str = "default"
    ) -> str:
        """Get button styling with current theme."""
        return self.components.get_button_style(variant, size, state)

    def get_input_style(
        self, variant: str = "default", state: str = "default", has_error: bool = False
    ) -> str:
        """Get input field styling with current theme."""
        return self.components.get_input_style(variant, state, has_error)

    def get_card_style(self, elevation: str = "md", is_hoverable: bool = False) -> str:
        """Get card styling with current theme."""
        return self.components.get_card_style(elevation, is_hoverable)

    def get_panel_style(self, variant: str = "default") -> str:
        """Get panel styling with current theme."""
        return self.components.get_panel_style(variant)

    def is_dark_mode(self) -> bool:
        """Check if current theme is dark mode."""
        return self.color_scheme == ColorScheme.DARK

    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary representation."""
        return {
            "color_scheme": self.color_scheme.value,
            "primary_color": self.primary_color,
            "colors": self.colors.to_dict(),
            "radius": self.radius,
            "spacing": self.spacing.to_dict(),
            "typography": self.typography.to_dict(),
            "shadows": self.shadows,
            "breakpoints": self.breakpoints,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """Create theme from dictionary."""
        # This would need proper implementation with ColorScheme conversion
        pass


class ThemeProvider:
    """Provides theme management and context throughout the application."""

    def __init__(self, theme: Theme):
        self.theme = theme

    def get_current_theme(self) -> Theme:
        """Get the currently active theme."""
        return self.theme

    def update_theme(self, theme: Theme) -> None:
        """Update the current theme."""
        self.theme = theme

    def toggle_color_scheme(self) -> None:
        """Toggle between light and dark color schemes."""
        if self.theme.color_scheme == ColorScheme.LIGHT:
            self.theme.color_scheme = ColorScheme.DARK
            self.theme.colors._is_dark = True
        else:
            self.theme.color_scheme = ColorScheme.LIGHT
            self.theme.colors._is_dark = False

        # Update component styles with new theme state
        self.theme.components = ComponentStyles(self.theme.colors)

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        """Set a specific color scheme."""
        self.theme.color_scheme = color_scheme
        self.theme.colors._is_dark = color_scheme == ColorScheme.DARK
        self.theme.components = ComponentStyles(self.theme.colors)

    def update_theme_colors(self, primary_color: str = None) -> None:
        """Update theme colors and reinitialize component styles."""
        if primary_color:
            self.theme.primary_color = primary_color

        # Reinitialize component styles with updated theme
        self.theme.components = ComponentStyles(self.theme.colors)
