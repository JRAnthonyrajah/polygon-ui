"""
Main Theme system for Polygon UI - equivalent to Mantine's Theme object.
"""

from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from .colors import Colors
from .spacing import Spacing
from .typography import Typography


class ColorScheme(Enum):
    """Color scheme options."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


@dataclass
class OtherThemeSettings:
    """Other theme settings for extensions."""

    # Can be extended with custom settings
    custom: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentThemeOverrides:
    """Component-specific theme overrides."""

    # This will be populated with component-specific default props and styles
    components: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class Theme:
    """Main theme class - central configuration for Polygon UI."""

    def __init__(
        self,
        color_scheme: Union[ColorScheme, str] = ColorScheme.LIGHT,
        primary_color: str = "blue",
        primary_shade: Union[int, Dict[str, int]] = 6,
        colors: Optional[Colors] = None,
        spacing: Optional[Spacing] = None,
        typography: Optional[Typography] = None,
        font_family: Optional[str] = None,
        font_family_monospace: Optional[str] = None,
        radius: Optional[Dict[str, int]] = None,
        shadows: Optional[Dict[str, str]] = None,
        breakpoints: Optional[Dict[str, int]] = None,
        components: Optional[Dict[str, Dict[str, Any]]] = None,
        other: Optional[Dict[str, Any]] = None,
        auto_contrast: bool = True,
        respect_reduced_motion: bool = True,
        focus_ring: Union[bool, str] = "auto",
        cursor_type: str = "default",
    ):
        # Color scheme management
        if isinstance(color_scheme, str):
            color_scheme = ColorScheme(color_scheme.lower())
        self.color_scheme = color_scheme
        self.primary_color = primary_color
        self.primary_shade = primary_shade

        # Initialize theme systems
        self.colors = colors or Colors()
        self.spacing = spacing or Spacing()
        self.typography = typography or Typography()

        # Font settings
        self.font_family = font_family or self.typography.get_font_family("sans")
        self.font_family_monospace = (
            font_family_monospace or self.typography.get_font_family("mono")
        )

        # Design tokens
        self.radius = radius or {"xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16}
        self.shadows = shadows or {
            "xs": "0 1px 3px rgba(0, 0, 0, 0.1)",
            "sm": "0 2px 6px rgba(0, 0, 0, 0.15)",
            "md": "0 4px 12px rgba(0, 0, 0, 0.2)",
            "lg": "0 8px 24px rgba(0, 0, 0, 0.25)",
            "xl": "0 16px 48px rgba(0, 0, 0, 0.3)",
        }
        self.breakpoints = breakpoints or {
            "xs": 576,
            "sm": 768,
            "md": 992,
            "lg": 1200,
            "xl": 1400,
        }

        # Component overrides
        self.components = components or {}

        # Other settings
        self.other = other or {}
        self.auto_contrast = auto_contrast
        self.respect_reduced_motion = respect_reduced_motion
        self.focus_ring = focus_ring
        self.cursor_type = cursor_type

    def get_primary_color(self, shade: Optional[Union[int, str]] = None) -> str:
        """Get the primary color with specified shade."""
        if shade is None:
            if isinstance(self.primary_shade, dict):
                # Use different shades for light/dark mode
                shade = self.primary_shade.get(
                    self.color_scheme.value, self.primary_shade.get("light", 6)
                )
            else:
                shade = self.primary_shade

        return self.colors.get_color(self.primary_color, shade)

    def get_color(self, name: str, shade: Union[int, str] = 5) -> str:
        """Get any color from the theme."""
        return self.colors.get_color(name, shade)

    def get_spacing(self, size: Union[str, int]) -> int:
        """Get spacing value."""
        return self.spacing.get_spacing(size)

    def get_radius(self, size: Union[str, int]) -> int:
        """Get border radius value."""
        if isinstance(size, int):
            return size

        radius_map = {"xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16}
        return radius_map.get(size, 8)  # Default to medium

    def get_font_size(self, size: Union[str, int]) -> int:
        """Get font size."""
        return self.typography.get_font_size(size)

    def get_font_weight(self, weight: Union[str, int]) -> int:
        """Get font weight."""
        return self.typography.get_font_weight(weight)

    def get_font_family(self, family: str = "sans") -> str:
        """Get font family."""
        return self.typography.get_font_family(family)

    def get_line_height(self, height: Union[str, float]) -> float:
        """Get line height."""
        return self.typography.get_line_height(height)

    def get_shadow(self, size: str = "md") -> str:
        """Get box shadow."""
        return self.shadows.get(size, self.shadows["md"])

    def get_breakpoint(self, size: str) -> int:
        """Get breakpoint value."""
        return self.breakpoints.get(size, 992)  # Default to medium

    def get_component_overrides(self, component_name: str) -> Dict[str, Any]:
        """Get theme overrides for a specific component."""
        return self.components.get(component_name, {})

    def set_component_override(
        self, component_name: str, overrides: Dict[str, Any]
    ) -> None:
        """Set theme overrides for a specific component."""
        self.components[component_name] = overrides

    def merge_with(self, other_theme: "Theme") -> "Theme":
        """Merge this theme with another theme, with other_theme taking precedence."""
        # Create a new theme with merged settings
        merged_theme = Theme(
            color_scheme=other_theme.color_scheme or self.color_scheme,
            primary_color=other_theme.primary_color or self.primary_color,
            primary_shade=other_theme.primary_shade or self.primary_shade,
            colors=other_theme.colors or self.colors,
            spacing=other_theme.spacing or self.spacing,
            typography=other_theme.typography or self.typography,
            font_family=other_theme.font_family or self.font_family,
            font_family_monospace=other_theme.font_family_monospace
            or self.font_family_monospace,
            radius={**self.radius, **(other_theme.radius or {})},
            shadows={**self.shadows, **(other_theme.shadows or {})},
            breakpoints={**self.breakpoints, **(other_theme.breakpoints or {})},
            components={**self.components, **(other_theme.components or {})},
            other={**self.other, **(other_theme.other or {})},
            auto_contrast=other_theme.auto_contrast
            if other_theme.auto_contrast != self.auto_contrast
            else self.auto_contrast,
            respect_reduced_motion=other_theme.respect_reduced_motion
            if other_theme.respect_reduced_motion != self.respect_reduced_motion
            else self.respect_reduced_motion,
            focus_ring=other_theme.focus_ring
            if other_theme.focus_ring != self.focus_ring
            else self.focus_ring,
            cursor_type=other_theme.cursor_type
            if other_theme.cursor_type != self.cursor_type
            else self.cursor_type,
        )
        return merged_theme

    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary format."""
        return {
            "color_scheme": self.color_scheme.value,
            "primary_color": self.primary_color,
            "primary_shade": self.primary_shade,
            "colors": self.colors.to_dict(),
            "spacing": self.spacing.to_dict(),
            "typography": self.typography.to_dict(),
            "font_family": self.font_family,
            "font_family_monospace": self.font_family_monospace,
            "radius": self.radius,
            "shadows": self.shadows,
            "breakpoints": self.breakpoints,
            "components": self.components,
            "other": self.other,
            "auto_contrast": self.auto_contrast,
            "respect_reduced_motion": self.respect_reduced_motion,
            "focus_ring": self.focus_ring,
            "cursor_type": self.cursor_type,
        }


class ThemeProvider:
    """Provider class for managing theme context across the application."""

    def __init__(self, theme: Optional[Theme] = None):
        self._theme = theme or Theme()
        self._listeners = []

    def get_theme(self) -> Theme:
        """Get the current theme."""
        return self._theme

    def set_theme(self, theme: Theme) -> None:
        """Set a new theme and notify listeners."""
        old_theme = self._theme
        self._theme = theme

        # Notify listeners of theme change
        for listener in self._listeners:
            listener(old_theme, theme)

    def update_theme(self, **kwargs) -> None:
        """Update theme properties."""
        current_dict = self._theme.to_dict()
        current_dict.update(kwargs)
        self._theme = Theme(**current_dict)

        # Notify listeners
        for listener in self._listeners:
            listener(self._theme, self._theme)

    def add_theme_listener(self, listener) -> None:
        """Add a listener that gets called when the theme changes."""
        self._listeners.append(listener)

    def remove_theme_listener(self, listener) -> None:
        """Remove a theme change listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def toggle_color_scheme(self) -> None:
        """Toggle between light and dark color schemes."""
        new_scheme = (
            ColorScheme.DARK
            if self._theme.color_scheme == ColorScheme.LIGHT
            else ColorScheme.LIGHT
        )
        self.update_theme(color_scheme=new_scheme)
