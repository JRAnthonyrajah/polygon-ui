"""
Modern component styling system for Polygon UI.
Provides consistent styling for all UI components with theme support.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class BorderRadius:
    """Border radius system for modern UI."""

    none: int = 0  # No radius
    xs: int = 2  # Extra small
    sm: int = 4  # Small
    md: int = 6  # Medium
    lg: int = 8  # Large
    xl: int = 12  # Extra large
    xxl: int = 16  # Extra extra large
    full: str = "50%"  # Full circle

    def get_radius(self, size: str) -> str:
        """Get border radius value."""
        radius_map = {
            "none": str(self.none),
            "xs": f"{self.xs}px",
            "sm": f"{self.sm}px",
            "md": f"{self.md}px",
            "lg": f"{self.lg}px",
            "xl": f"{self.xl}px",
            "xxl": f"{self.xxl}px",
            "full": self.full,
        }
        return radius_map.get(size, f"{self.md}px")


@dataclass
class Shadows:
    """Modern shadow system for depth and elevation."""

    none: str = "none"
    sm: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    xl: str = (
        "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    )
    inner: str = "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)"

    def get_shadow(self, size: str) -> str:
        """Get shadow value."""
        shadow_map = {
            "none": self.none,
            "sm": self.sm,
            "md": self.md,
            "lg": self.lg,
            "xl": self.xl,
            "inner": self.inner,
        }
        return shadow_map.get(size, self.sm)


@dataclass
class Transitions:
    """Transition system for smooth animations."""

    fast: str = "150ms ease-in-out"
    normal: str = "200ms ease-in-out"
    slow: str = "300ms ease-in-out"

    def get_transition(self, speed: str = "normal") -> str:
        """Get transition timing."""
        transition_map = {
            "fast": self.fast,
            "normal": self.normal,
            "slow": self.slow,
        }
        return transition_map.get(speed, self.normal)


class ComponentStyles:
    """Main component styling system."""

    def __init__(
        self,
        colors,
        border_radius: Optional[BorderRadius] = None,
        shadows: Optional[Shadows] = None,
        transitions: Optional[Transitions] = None,
    ):
        self.colors = colors
        self.border_radius = border_radius or BorderRadius()
        self.shadows = shadows or Shadows()
        self.transitions = transitions or Transitions()

    def get_button_style(
        self, variant: str = "primary", size: str = "md", state: str = "default"
    ) -> str:
        """Get button styling."""
        is_dark = hasattr(self.colors, "_is_dark") and self.colors._is_dark

        # Base button styles
        base_styles = [
            f"border: 1px solid",
            f"border-radius: {self.border_radius.get_radius('md')}",
            f"font-weight: 600",
            f"cursor: pointer",
            f"outline: none",
            f"font-family: {self.colors.get_font_family() if hasattr(self.colors, 'get_font_family') else 'Inter, sans-serif'}",
        ]

        # Size styles
        size_styles = self._get_button_size_styles(size)

        # Variant styles
        variant_styles = self._get_button_variant_styles(variant, state, is_dark)

        return "; ".join(base_styles + size_styles + variant_styles)

    def _get_button_size_styles(self, size: str) -> list:
        """Get button size styles."""
        size_map = {
            "xs": ["font-size: 11px", "padding: 6px 12px", "min-height: 24px"],
            "sm": ["font-size: 13px", "padding: 8px 16px", "min-height: 32px"],
            "md": ["font-size: 15px", "padding: 10px 20px", "min-height: 40px"],
            "lg": ["font-size: 17px", "padding: 12px 24px", "min-height: 48px"],
            "xl": ["font-size: 19px", "padding: 14px 28px", "min-height: 56px"],
        }
        return size_map.get(size, size_map["md"])

    def _get_button_variant_styles(
        self, variant: str, state: str, is_dark: bool
    ) -> list:
        """Get button variant styles."""
        styles = []

        if variant == "primary":
            if state == "hover":
                bg = self.colors.get_color("blue", 5)
                text = "#ffffff"
                border = self.colors.get_color("blue", 6)
            elif state == "pressed":
                bg = self.colors.get_color("blue", 6)
                text = "#ffffff"
                border = self.colors.get_color("blue", 7)
            else:  # default
                bg = self.colors.get_color("blue", 4)
                text = "#ffffff"
                border = self.colors.get_color("blue", 5)

        elif variant == "secondary":
            if state == "hover":
                bg = self.colors.get_surface(is_dark)
                text = self.colors.get_text(is_dark)
                border = self.colors.get_border(is_dark)
            elif state == "pressed":
                bg = self.colors.get_color("gray", 2 if is_dark else 8)
                text = self.colors.get_text(is_dark)
                border = self.colors.get_color("gray", 6 if is_dark else 4)
            else:  # default
                bg = self.colors.get_surface(is_dark)
                text = self.colors.get_text(is_dark)
                border = self.colors.get_border(is_dark)

        elif variant == "ghost":
            if state == "hover":
                bg = self.colors.get_color("blue", 0 if is_dark else 1)
                text = self.colors.get_color("blue", 6)
                border = "transparent"
            elif state == "pressed":
                bg = self.colors.get_color("blue", 1 if is_dark else 2)
                text = self.colors.get_color("blue", 7)
                border = "transparent"
            else:  # default
                bg = "transparent"
                text = self.colors.get_color("blue", 5)
                border = "transparent"

        styles.extend(
            [
                f"background-color: {bg}",
                f"color: {text}",
                f"border-color: {border}",
            ]
        )

        return styles

    def get_input_style(
        self, variant: str = "default", state: str = "default", has_error: bool = False
    ) -> str:
        """Get input field styling."""
        is_dark = hasattr(self.colors, "_is_dark") and self.colors._is_dark

        base_styles = [
            f"border: 1px solid",
            f"border-radius: {self.border_radius.get_radius('md')}",
            f"padding: 10px 12px",
            f"font-size: 15px",
            f"font-family: {self.colors.get_font_family() if hasattr(self.colors, 'get_font_family') else 'Inter, sans-serif'}",
            f"outline: none",
            f"background-color: {self.colors.get_surface(is_dark)}",
            f"color: {self.colors.get_text(is_dark)}",
        ]

        # State styles
        if has_error:
            border_color = self.colors.get_color("red", 5)
            shadow_color = self.colors.get_color("red", 0)
        elif state == "focus":
            border_color = self.colors.get_color("blue", 5)
            shadow_color = self.colors.get_color("blue", 0)
        elif state == "hover":
            border_color = self.colors.get_color("blue", 4)
            shadow_color = "transparent"
        else:  # default
            border_color = self.colors.get_border(is_dark)
            shadow_color = "transparent"

        state_styles = [
            f"border-color: {border_color}",
        ]

        if shadow_color != "transparent":
            state_styles.append(f"box-shadow: 0 0 0 3px {shadow_color}")

        return "; ".join(base_styles + state_styles)

    def get_card_style(self, elevation: str = "md", is_hoverable: bool = False) -> str:
        """Get card container styling."""
        is_dark = hasattr(self.colors, "_is_dark") and self.colors._is_dark

        base_styles = [
            f"background-color: {self.colors.get_surface(is_dark)}",
            f"border: 1px solid {self.colors.get_border(is_dark)}",
            f"border-radius: {self.border_radius.get_radius('lg')}",
        ]

        # Elevation styles
        elevation_map = {
            "none": self.shadows.none,
            "sm": self.shadows.sm,
            "md": self.shadows.md,
            "lg": self.shadows.lg,
            "xl": self.shadows.xl,
        }

        shadow = elevation_map.get(elevation, self.shadows.md)
        base_styles.append(f"box-shadow: {shadow}")

        if is_hoverable:
            hover_styles = [
                ":hover {",
                f"  box-shadow: {self.shadows.lg}",
                f"  border-color: {self.colors.get_color('blue', 4) if not is_dark else self.colors.get_color('blue', 6)}",
                "}",
            ]
            base_styles.extend(hover_styles)

        return "; ".join(base_styles)

    def get_panel_style(self, variant: str = "default") -> str:
        """Get panel/container styling."""
        is_dark = hasattr(self.colors, "_is_dark") and self.colors._is_dark

        base_styles = [
            f"background-color: {self.colors.get_background(is_dark)}",
            f"border-radius: {self.border_radius.get_radius('lg')}",
            f"padding: 16px",
        ]

        if variant == "card":
            base_styles.extend(
                [
                    f"background-color: {self.colors.get_surface(is_dark)}",
                    f"border: 1px solid {self.colors.get_border(is_dark)}",
                    f"box-shadow: {self.shadows.sm}",
                ]
            )
        elif variant == "elevated":
            base_styles.extend(
                [
                    f"background-color: {self.colors.get_surface(is_dark)}",
                    f"border: 1px solid {self.colors.get_border(is_dark)}",
                    f"box-shadow: {self.shadows.md}",
                ]
            )

        return "; ".join(base_styles)

    def to_dict(self) -> Dict[str, Any]:
        """Convert component styles to dictionary."""
        return {
            "border_radius": {
                "none": self.border_radius.none,
                "xs": self.border_radius.xs,
                "sm": self.border_radius.sm,
                "md": self.border_radius.md,
                "lg": self.border_radius.lg,
                "xl": self.border_radius.xl,
                "xxl": self.border_radius.xxl,
                "full": self.border_radius.full,
            },
            "shadows": {
                "none": self.shadows.none,
                "sm": self.shadows.sm,
                "md": self.shadows.md,
                "lg": self.shadows.lg,
                "xl": self.shadows.xl,
                "inner": self.shadows.inner,
            },
            "transitions": {
                "fast": self.transitions.fast,
                "normal": self.transitions.normal,
                "slow": self.transitions.slow,
            },
        }
