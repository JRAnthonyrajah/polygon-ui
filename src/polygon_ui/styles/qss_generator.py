"""
QSS Generator - Converts theme values to Qt Style Sheets.
Equivalent to CSS variables and styling system in Mantine.
"""

from typing import Dict, Any, Optional, Union
from ..theme.theme import Theme, ColorScheme


class QSSGenerator:
    """Generates Qt Style Sheets from theme values."""

    def __init__(self):
        self._css_variables = {}
        self._component_styles = {}

    def generate_theme_qss(self, theme: Theme) -> str:
        """
        Generate global QSS for the entire theme.

        Args:
            theme: Theme object containing all design tokens

        Returns:
            Complete QSS string for the theme
        """
        qss_parts = []

        # CSS Variables (as comments for documentation)
        qss_parts.append("/* Polygon UI Theme Variables */")
        qss_parts.append(self._generate_css_variables_qss(theme))

        # Base styles
        qss_parts.append("/* Base Styles */")
        qss_parts.append(self._generate_base_styles_qss(theme))

        # Color scheme styles
        qss_parts.append(f"/* {theme.color_scheme.value.capitalize()} Theme */")
        qss_parts.append(self._generate_color_scheme_qss(theme))

        # Typography
        qss_parts.append("/* Typography */")
        qss_parts.append(self._generate_typography_qss(theme))

        # Spacing and layout
        qss_parts.append("/* Layout & Spacing */")
        qss_parts.append(self._generate_layout_qss(theme))

        return "\n\n".join(filter(None, qss_parts))

    def generate_component_qss(
        self, component_name: str, props: Dict[str, Any], theme: Theme
    ) -> str:
        """
        Generate QSS for a specific component with given props.

        Args:
            component_name: Name of the component
            props: Component properties
            theme: Current theme

        Returns:
            Component-specific QSS string
        """
        qss_parts = []
        selector = f".{component_name}"

        # Base component style
        style_props = []

        # Handle different prop types
        for prop_name, prop_value in props.items():
            if prop_name.startswith("m") or prop_name.startswith("p"):
                # Margin and padding
                css_prop = self._convert_spacing_prop(prop_name, prop_value, theme)
                if css_prop:
                    style_props.append(css_prop)
            elif prop_name in ["w", "h", "miw", "mih", "maw", "mah"]:
                # Sizing
                css_prop = self._convert_sizing_prop(prop_name, prop_value, theme)
                if css_prop:
                    style_props.append(css_prop)
            elif prop_name in ["c", "bg"]:
                # Colors
                css_prop = self._convert_color_prop(prop_name, prop_value, theme)
                if css_prop:
                    style_props.append(css_prop)
            elif prop_name in ["fz", "fw", "lh"]:
                # Typography
                css_prop = self._convert_typography_prop(prop_name, prop_value, theme)
                if css_prop:
                    style_props.append(css_prop)
            elif prop_name in ["bd", "bdrs", "bdc"]:
                # Borders
                css_prop = self._convert_border_prop(prop_name, prop_value, theme)
                if css_prop:
                    style_props.append(css_prop)
            else:
                # Direct CSS property mapping
                css_prop = self._convert_direct_prop(prop_name, prop_value)
                if css_prop:
                    style_props.append(css_prop)

        if style_props:
            qss_parts.append(f"{selector} {{")
            qss_parts.extend(f"  {prop}" for prop in style_props)
            qss_parts.append("}")

        # Handle states (hover, active, disabled, etc.)
        state_styles = self._generate_state_styles(component_name, props, theme)
        if state_styles:
            qss_parts.append(state_styles)

        return "\n".join(qss_parts)

    def _generate_css_variables_qss(self, theme: Theme) -> str:
        """Generate CSS-like variables as comments for documentation."""
        variables = []

        # Color variables
        for color_name in theme.colors.list_colors():
            color_shades = theme.colors.get_color_shades(color_name)
            for i, shade_value in enumerate(color_shades.shades):
                variables.append(
                    f"/* --polygon-color-{color_name}-{i}: {shade_value}; */"
                )

        # Spacing variables
        spacing_sizes = theme.spacing.to_dict()
        for size_name, size_value in spacing_sizes.items():
            variables.append(f"/* --polygon-spacing-{size_name}: {size_value}px; */")

        # Typography variables
        font_sizes = theme.typography.font_sizes
        for size_name, size_value in font_sizes.__dict__.items():
            if not size_name.startswith("_"):
                variables.append(
                    f"/* --polygon-font-size-{size_name}: {size_value}px; */"
                )

        return "\n".join(variables)

    def _generate_base_styles_qss(self, theme: Theme) -> str:
        """Generate base application styles."""
        base_styles = [
            "QWidget {",
            f"  font-family: {theme.font_family};",
            f"  font-size: {theme.get_font_size('md')}px;",
            f"  color: {theme.get_color('gray', 9 if theme.color_scheme == ColorScheme.LIGHT else 0)};",
            "  background-color: transparent;",
            "  border: none;",
            "  outline: none;",
            "}",
            "",
            "QWidget:focus {",
            f"  border: 2px solid {theme.get_primary_color()};",
            "}",
            "",
            "QPushButton:pressed {",
            "  background-color: rgba(0, 0, 0, 0.1);",
            "}",
        ]

        if theme.color_scheme == ColorScheme.DARK:
            dark_styles = [
                "QWidget {",
                f"  background-color: {theme.get_color('gray', 0)};",
                f"  color: {theme.get_color('gray', 0)};",
                "}",
                "",
                "QFrame, QLabel, QPushButton {",
                f"  background-color: {theme.get_color('gray', 1)};",
                "}",
            ]
            base_styles.extend(dark_styles)

        return "\n".join(base_styles)

    def _generate_color_scheme_qss(self, theme: Theme) -> str:
        """Generate color scheme specific styles."""
        styles = []

        # Primary color applications
        primary_color = theme.get_primary_color()
        styles.extend(
            [
                "QPushButton[class='primary'] {",
                f"  background-color: {primary_color};",
                f"  border: 1px solid {primary_color};",
                "  color: white;",
                "  padding: 8px 16px;",
                f"  border-radius: {theme.get_radius('md')}px;",
                "}",
                "",
                "QPushButton[class='primary']:hover {",
                f"  background-color: {theme.colors.get_color(theme.primary_color, 7 if theme.color_scheme == ColorScheme.LIGHT else 5)};",
                "}",
            ]
        )

        return "\n".join(styles)

    def _generate_typography_qss(self, theme: Theme) -> str:
        """Generate typography styles."""
        styles = []

        # Heading styles
        for i, size in enumerate([32, 28, 24, 20, 18, 16]):
            weight = "bold" if i < 3 else "600"
            styles.extend(
                [
                    f"QLabel[class='h{i+1}'] {{",
                    f"  font-size: {size}px;",
                    f"  font-weight: {weight};",
                    f"  line-height: {theme.get_line_height('md')};",
                    "}",
                ]
            )

        return "\n".join(styles)

    def _generate_layout_qss(self, theme: Theme) -> str:
        """Generate layout and spacing styles."""
        styles = [
            "/* Utility classes for spacing */",
            "[class*='m-'] { margin: 0px; }",
            "[class*='p-'] { padding: 0px; }",
            "",
            "/* Spacing utilities will be generated dynamically */",
        ]

        return "\n".join(styles)

    def _convert_spacing_prop(
        self, prop_name: str, prop_value: Any, theme: Theme
    ) -> Optional[str]:
        """Convert spacing properties to CSS."""
        spacing_map = {
            "m": "margin",
            "mt": "margin-top",
            "mr": "margin-right",
            "mb": "margin-bottom",
            "ml": "margin-left",
            "mx": "margin-left, margin-right",
            "my": "margin-top, margin-bottom",
            "p": "padding",
            "pt": "padding-top",
            "pr": "padding-right",
            "pb": "padding-bottom",
            "pl": "padding-left",
            "px": "padding-left, padding-right",
            "py": "padding-top, padding-bottom",
        }

        if prop_name not in spacing_map:
            return None

        if isinstance(prop_value, (list, tuple)):
            # Handle multiple values
            props = []
            css_props = spacing_map[prop_name].split(", ")
            for i, value in enumerate(prop_value):
                if i < len(css_props):
                    spacing = theme.get_spacing(value)
                    props.append(f"{css_props[i]}: {spacing}px")
            return "; ".join(props)
        else:
            # Single value
            spacing = theme.get_spacing(prop_value)
            css_prop = spacing_map[prop_name]
            if ", " in css_prop:
                # Apply to multiple properties
                props = [
                    f"{prop.strip()}: {spacing}px" for prop in css_prop.split(", ")
                ]
                return "; ".join(props)
            else:
                return f"{css_prop}: {spacing}px"

    def _convert_sizing_prop(
        self, prop_name: str, prop_value: Any, theme: Theme
    ) -> Optional[str]:
        """Convert sizing properties to CSS."""
        size_map = {
            "w": "width",
            "h": "height",
            "miw": "min-width",
            "mih": "min-height",
            "maw": "max-width",
            "mah": "max-height",
        }

        if prop_name not in size_map:
            return None

        if isinstance(prop_value, (int, float)):
            return f"{size_map[prop_name]}: {prop_value}px"
        elif isinstance(prop_value, str):
            # Handle theme values like 'sm', 'md', 'lg'
            if prop_value in ["xs", "sm", "md", "lg", "xl"]:
                spacing = theme.get_spacing(prop_value)
                return f"{size_map[prop_name]}: {spacing}px"
            return f"{size_map[prop_name]}: {prop_value}"

        return None

    def _convert_color_prop(
        self, prop_name: str, prop_value: Any, theme: Theme
    ) -> Optional[str]:
        """Convert color properties to CSS."""
        color_map = {"c": "color", "bg": "background-color"}

        if prop_name not in color_map:
            return None

        if isinstance(prop_value, str):
            # Handle theme colors like 'blue.6' or 'primary'
            if "." in prop_value:
                color_name, shade = prop_value.split(".")
                color = theme.get_color(color_name, int(shade))
            elif prop_value == "primary":
                color = theme.get_primary_color()
            elif prop_value in theme.colors.list_colors():
                color = theme.get_color(prop_value)
            else:
                color = prop_value

            return f"{color_map[prop_name]}: {color}"

        return None

    def _convert_typography_prop(
        self, prop_name: str, prop_value: Any, theme: Theme
    ) -> Optional[str]:
        """Convert typography properties to CSS."""
        typo_map = {"fz": "font-size", "fw": "font-weight", "lh": "line-height"}

        if prop_name not in typo_map:
            return None

        if prop_name == "fz":
            # Font size
            if isinstance(prop_value, str):
                size = theme.get_font_size(prop_value)
            else:
                size = prop_value
            return f"font-size: {size}px"
        elif prop_name == "fw":
            # Font weight
            if isinstance(prop_value, str):
                weight = theme.get_font_weight(prop_value)
            else:
                weight = prop_value
            return f"font-weight: {weight}"
        elif prop_name == "lh":
            # Line height
            if isinstance(prop_value, str):
                height = theme.get_line_height(prop_value)
            else:
                height = prop_value
            return f"line-height: {height}"

        return None

    def _convert_border_prop(
        self, prop_name: str, prop_value: Any, theme: Theme
    ) -> Optional[str]:
        """Convert border properties to CSS."""
        border_map = {"bd": "border", "bdrs": "border-radius", "bdc": "border-color"}

        if prop_name not in border_map:
            return None

        if prop_name == "bdrs":
            # Border radius
            if isinstance(prop_value, str):
                radius = theme.get_radius(prop_value)
            else:
                radius = prop_value
            return f"border-radius: {radius}px"
        elif prop_name == "bdc":
            # Border color
            if isinstance(prop_value, str) and "." in prop_value:
                color_name, shade = prop_value.split(".")
                color = theme.get_color(color_name, int(shade))
            else:
                color = prop_value
            return f"border-color: {color}"
        elif prop_name == "bd":
            # Border (shorthand)
            return f"border: {prop_value}"

        return None

    def _convert_direct_prop(self, prop_name: str, prop_value: Any) -> Optional[str]:
        """Convert direct CSS property names."""
        # Simple mapping for common CSS properties
        css_mapping = {
            "display": "display",
            "flex": "flex",
            "pos": "position",
            "top": "top",
            "left": "left",
            "right": "right",
            "bottom": "bottom",
            "opacity": "opacity",
            "z": "z-index",
        }

        css_prop = css_mapping.get(prop_name)
        if css_prop:
            return f"{css_prop}: {prop_value}"

        return None

    def _generate_state_styles(
        self, component_name: str, props: Dict[str, Any], theme: Theme
    ) -> Optional[str]:
        """Generate state-specific styles (hover, active, disabled, etc.)."""
        state_styles = []

        # Hover state
        hover_props = props.get(":hover", {})
        if hover_props:
            hover_qss = self.generate_component_qss(component_name, hover_props, theme)
            hover_qss = hover_qss.replace(
                f".{component_name}", f".{component_name}:hover"
            )
            state_styles.append(hover_qss)

        # Active state
        active_props = props.get(":active", {})
        if active_props:
            active_qss = self.generate_component_qss(
                component_name, active_props, theme
            )
            active_qss = active_qss.replace(
                f".{component_name}", f".{component_name}:pressed"
            )
            state_styles.append(active_qss)

        # Disabled state
        disabled_props = props.get(":disabled", {})
        if disabled_props:
            disabled_qss = self.generate_component_qss(
                component_name, disabled_props, theme
            )
            disabled_qss = disabled_qss.replace(
                f".{component_name}", f".{component_name}:disabled"
            )
            state_styles.append(disabled_qss)

        return "\n\n".join(filter(None, state_styles)) if state_styles else None
