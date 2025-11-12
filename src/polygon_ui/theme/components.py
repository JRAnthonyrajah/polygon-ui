"""
Modern component styling system for Polygon UI.
Provides consistent styling for all UI components with theme support.
"""

from typing import Dict, Any, Optional, List
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
    """Main component styling system with Mantine-style component overrides."""

    def __init__(
        self,
        colors,
        border_radius: Optional[BorderRadius] = None,
        shadows: Optional[Shadows] = None,
        transitions: Optional[Transitions] = None,
        component_overrides: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        self.colors = colors
        self.border_radius = border_radius or BorderRadius()
        self.shadows = shadows or Shadows()
        self.transitions = transitions or Transitions()
        self.component_overrides = component_overrides or {}
        self._default_components = self._create_default_components()

    def _create_default_components(self) -> Dict[str, Dict[str, Any]]:
        """Create default component configurations following Mantine patterns."""
        return {
            "Button": {
                "defaultProps": {
                    "variant": "filled",
                    "size": "sm",
                    "color": "blue",
                    "radius": "sm",
                },
                "styles": {
                    "root": {
                        "display": "inline-flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "border": "1px solid",
                        "fontFamily": "var(--mantine-font-family)",
                        "fontWeight": 600,
                        "cursor": "pointer",
                        "outline": "none",
                        "transition": "var(--mantine-transition-all)",
                        "userSelect": "none",
                        "boxSizing": "border-box",
                    },
                    "label": {
                        "display": "block",
                        "whiteSpace": "nowrap",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    },
                    "loader": {},
                    "section": {
                        "display": "flex",
                        "alignItems": "center",
                    },
                    "inner": {
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                },
                "variants": {
                    "filled": {
                        "backgroundColor": "var(--mantine-color-filled)",
                        "color": "var(--mantine-color-filled-color)",
                        "borderColor": "var(--mantine-color-filled)",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-filled-hover)",
                            "borderColor": "var(--mantine-color-filled-hover)",
                        },
                    },
                    "light": {
                        "backgroundColor": "var(--mantine-color-light)",
                        "color": "var(--mantine-color-light-color)",
                        "borderColor": "transparent",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-light-hover)",
                        },
                    },
                    "outline": {
                        "backgroundColor": "transparent",
                        "color": "var(--mantine-color-outline)",
                        "borderColor": "var(--mantine-color-outline)",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-outline-hover)",
                        },
                    },
                    "default": {
                        "backgroundColor": "var(--mantine-color-default)",
                        "color": "var(--mantine-color-default-color)",
                        "borderColor": "var(--mantine-color-default-border)",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-default-hover)",
                        },
                    },
                    "white": {
                        "backgroundColor": "var(--mantine-color-white)",
                        "color": "var(--mantine-color-black)",
                        "borderColor": "var(--mantine-color-default-border)",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-gray-0)",
                        },
                    },
                    "subtle": {
                        "backgroundColor": "transparent",
                        "color": "var(--mantine-color-text)",
                        "borderColor": "transparent",
                        "&:hover": {
                            "backgroundColor": "var(--mantine-color-gray-0)",
                        },
                    },
                },
                "sizes": {
                    "xs": {
                        "height": "var(--button-height-xs)",
                        "minHeight": "var(--button-height-xs)",
                        "padding": "0 var(--button-padding-x-xs)",
                        "fontSize": "var(--mantine-font-size-xs)",
                    },
                    "sm": {
                        "height": "var(--button-height-sm)",
                        "minHeight": "var(--button-height-sm)",
                        "padding": "0 var(--button-padding-x-sm)",
                        "fontSize": "var(--mantine-font-size-sm)",
                    },
                    "md": {
                        "height": "var(--button-height-md)",
                        "minHeight": "var(--button-height-md)",
                        "padding": "0 var(--button-padding-x-md)",
                        "fontSize": "var(--mantine-font-size-md)",
                    },
                    "lg": {
                        "height": "var(--button-height-lg)",
                        "minHeight": "var(--button-height-lg)",
                        "padding": "0 var(--button-padding-x-lg)",
                        "fontSize": "var(--mantine-font-size-lg)",
                    },
                    "xl": {
                        "height": "var(--button-height-xl)",
                        "minHeight": "var(--button-height-xl)",
                        "padding": "0 var(--button-padding-x-xl)",
                        "fontSize": "var(--mantine-font-size-xl)",
                    },
                },
            },
            "TextInput": {
                "defaultProps": {
                    "size": "sm",
                    "radius": "sm",
                },
                "styles": {
                    "root": {
                        "position": "relative",
                        "width": "100%",
                    },
                    "input": {
                        "width": "100%",
                        "height": "var(--input-height)",
                        "padding": "0 var(--input-padding-x)",
                        "border": "1px solid",
                        "borderRadius": "var(--input-radius)",
                        "fontSize": "var(--mantine-font-size-sm)",
                        "lineHeight": 1.5,
                        "backgroundColor": "var(--mantine-color-white)",
                        "color": "var(--mantine-color-text)",
                        "outline": "none",
                        "transition": "var(--mantine-transition-all)",
                        "&::placeholder": {
                            "color": "var(--mantine-color-placeholder)",
                        },
                        "&:disabled": {
                            "backgroundColor": "var(--mantine-color-gray-1)",
                            "color": "var(--mantine-color-gray-5)",
                            "cursor": "not-allowed",
                            "opacity": 0.6,
                        },
                    },
                    "label": {
                        "display": "block",
                        "marginBottom": "var(--mantine-spacing-xs)",
                        "fontSize": "var(--mantine-font-size-sm)",
                        "fontWeight": 500,
                        "color": "var(--mantine-color-text)",
                    },
                    "description": {
                        "marginTop": "var(--mantine-spacing-xs)",
                        "fontSize": "var(--mantine-font-size-xs)",
                        "color": "var(--mantine-color-dimmed)",
                    },
                    "error": {
                        "marginTop": "var(--mantine-spacing-xs)",
                        "fontSize": "var(--mantine-font-size-xs)",
                        "color": "var(--mantine-color-error)",
                    },
                },
                "sizes": {
                    "xs": {
                        "fontSize": "var(--mantine-font-size-xs)",
                        "height": "var(--input-height-xs)",
                        "padding": "0 var(--input-padding-x-xs)",
                    },
                    "sm": {
                        "fontSize": "var(--mantine-font-size-sm)",
                        "height": "var(--input-height-sm)",
                        "padding": "0 var(--input-padding-x-sm)",
                    },
                    "md": {
                        "fontSize": "var(--mantine-font-size-md)",
                        "height": "var(--input-height-md)",
                        "padding": "0 var(--input-padding-x-md)",
                    },
                    "lg": {
                        "fontSize": "var(--mantine-font-size-lg)",
                        "height": "var(--input-height-lg)",
                        "padding": "0 var(--input-padding-x-lg)",
                    },
                    "xl": {
                        "fontSize": "var(--mantine-font-size-xl)",
                        "height": "var(--input-height-xl)",
                        "padding": "0 var(--input-padding-x-xl)",
                    },
                },
            },
            "Card": {
                "defaultProps": {
                    "p": "md",
                    "radius": "sm",
                    "withBorder": True,
                },
                "styles": {
                    "root": {
                        "backgroundColor": "var(--mantine-color-white)",
                        "border": "1px solid var(--mantine-color-default-border)",
                        "borderRadius": "var(--mantine-radius-default)",
                        "padding": "var(--mantine-spacing-md)",
                        "position": "relative",
                        "transition": "var(--mantine-transition-all)",
                    },
                    "section": {
                        "&:not(:last-of-type)": {
                            "borderBottom": "1px solid var(--mantine-color-default-border)",
                        },
                    },
                },
            },
            "Badge": {
                "defaultProps": {
                    "variant": "light",
                    "size": "sm",
                    "radius": "sm",
                },
                "styles": {
                    "root": {
                        "display": "inline-flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "padding": "0 var(--badge-padding-x)",
                        "borderRadius": "var(--mantine-radius-sm)",
                        "fontSize": "var(--mantine-font-size-xs)",
                        "fontWeight": 700,
                        "lineHeight": 1,
                        "whiteSpace": "nowrap",
                        "height": "var(--badge-height)",
                        "userSelect": "none",
                    },
                    "leftSection": {
                        "marginRight": "var(--mantine-spacing-xs)",
                    },
                    "rightSection": {
                        "marginLeft": "var(--mantine-spacing-xs)",
                    },
                },
                "variants": {
                    "filled": {
                        "backgroundColor": "var(--mantine-color-filled)",
                        "color": "var(--mantine-color-filled-color)",
                    },
                    "light": {
                        "backgroundColor": "var(--mantine-color-light)",
                        "color": "var(--mantine-color-light-color)",
                    },
                    "outline": {
                        "backgroundColor": "transparent",
                        "color": "var(--mantine-color-outline)",
                        "border": "1px solid var(--mantine-color-outline)",
                    },
                    "default": {
                        "backgroundColor": "var(--mantine-color-default)",
                        "color": "var(--mantine-color-default-color)",
                    },
                    "dot": {
                        "padding": 0,
                        "backgroundColor": "var(--mantine-color-filled)",
                        "color": "var(--mantine-color-filled-color)",
                        "borderRadius": "var(--mantine-radius-xl)",
                    },
                },
            },
        }

    def get_component_config(self, component_name: str) -> Dict[str, Any]:
        """
        Get component configuration with overrides applied.

        Args:
            component_name: Name of the component (e.g., 'Button', 'TextInput')

        Returns:
            Component configuration dictionary
        """
        # Start with default configuration
        config = self._default_components.get(component_name, {}).copy()

        # Apply user overrides
        if component_name in self.component_overrides:
            self._deep_merge(config, self.component_overrides[component_name])

        return config

    def override_component(
        self, component_name: str, overrides: Dict[str, Any]
    ) -> None:
        """
        Override component styles and props.

        Args:
            component_name: Name of the component
            overrides: Override configuration
        """
        if component_name not in self.component_overrides:
            self.component_overrides[component_name] = {}

        self._deep_merge(self.component_overrides[component_name], overrides)

    def get_component_styles(self, component_name: str) -> Dict[str, Dict[str, Any]]:
        """Get component styles dictionary."""
        config = self.get_component_config(component_name)
        return config.get("styles", {})

    def get_component_variants(self, component_name: str) -> Dict[str, Dict[str, Any]]:
        """Get component variants dictionary."""
        config = self.get_component_config(component_name)
        return config.get("variants", {})

    def get_component_sizes(self, component_name: str) -> Dict[str, Dict[str, Any]]:
        """Get component sizes dictionary."""
        config = self.get_component_config(component_name)
        return config.get("sizes", {})

    def get_component_default_props(self, component_name: str) -> Dict[str, Any]:
        """Get component default props."""
        config = self.get_component_config(component_name)
        return config.get("defaultProps", {})

    def generate_css_variables(self) -> Dict[str, str]:
        """
        Generate all CSS variables for components.

        Returns:
            Dictionary of CSS variable names to values
        """
        css_vars = {}

        # Button variables
        css_vars.update(
            {
                "--button-height-xs": "22px",
                "--button-height-sm": "30px",
                "--button-height-md": "38px",
                "--button-height-lg": "46px",
                "--button-height-xl": "54px",
                "--button-padding-x-xs": "10px",
                "--button-padding-x-sm": "14px",
                "--button-padding-x-md": "18px",
                "--button-padding-x-lg": "22px",
                "--button-padding-x-xl": "26px",
            }
        )

        # Input variables
        css_vars.update(
            {
                "--input-height-xs": "26px",
                "--input-height-sm": "34px",
                "--input-height-md": "42px",
                "--input-height-lg": "50px",
                "--input-height-xl": "58px",
                "--input-padding-x-xs": "10px",
                "--input-padding-x-sm": "12px",
                "--input-padding-x-md": "14px",
                "--input-padding-x-lg": "16px",
                "--input-padding-x-xl": "18px",
            }
        )

        # Badge variables
        css_vars.update(
            {
                "--badge-height": "16px",
                "--badge-padding-x": "6px",
            }
        )

        return css_vars

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        Deep merge two dictionaries.

        Args:
            base: Base dictionary to merge into
            override: Override dictionary to merge from
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def reset_component_overrides(self, component_name: str = None) -> None:
        """
        Reset component overrides.

        Args:
            component_name: Specific component to reset, or None to reset all
        """
        if component_name:
            self.component_overrides.pop(component_name, None)
        else:
            self.component_overrides.clear()

    def get_all_component_names(self) -> List[str]:
        """Get list of all available component configurations."""
        return list(self._default_components.keys()) + list(
            self.component_overrides.keys()
        )

    def validate_component_config(self, component_name: str) -> List[str]:
        """
        Validate component configuration.

        Args:
            component_name: Name of the component to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        config = self.get_component_config(component_name)

        # Check for required sections
        if "styles" not in config:
            errors.append(f"Component '{component_name}' missing 'styles' section")

        # Validate styles structure
        if "styles" in config:
            styles = config["styles"]
            if "root" not in styles:
                errors.append(f"Component '{component_name}' missing 'root' style")

        return errors

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
