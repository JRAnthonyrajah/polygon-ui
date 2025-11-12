"""
Style props system for Polygon UI components.
Implements Mantine-style shorthand properties and responsive styling.
"""

from typing import Dict, Any, Union, Optional, List
import re
from ..theme.theme import Theme


class StyleProps:
    """
    Manages style props for components with Mantine-style shorthand support.

    Supports shorthand properties like:
    - c (color), bg (background), bd (border)
    - w (width), h (height), mi (min-width), mx (max-width)
    - m (margin), p (padding), mt, mb, ml, mr, mx, my
    - fz (font-size), fw (font-weight), ff (font-family)
    - lh (line-height), ta (text-align), td (text-decoration)
    """

    # Mantine-style shorthand property mappings
    SHORTHAND_MAPPINGS = {
        # Colors
        "c": "color",
        "bg": "background-color",
        "bc": "border-color",
        "bgc": "background-color",
        "opc": "opacity",
        # Sizing
        "w": "width",
        "h": "height",
        "mi": "min-width",
        "ma": "max-width",
        "mih": "min-height",
        "mah": "max-height",
        # Spacing - margins
        "m": "margin",
        "mt": "margin-top",
        "mb": "margin-bottom",
        "ml": "margin-left",
        "mr": "margin-right",
        "mx": ["margin-left", "margin-right"],
        "my": ["margin-top", "margin-bottom"],
        # Spacing - padding
        "p": "padding",
        "pt": "padding-top",
        "pb": "padding-bottom",
        "pl": "padding-left",
        "pr": "padding-right",
        "px": ["padding-left", "padding-right"],
        "py": ["padding-top", "padding-bottom"],
        # Borders
        "bd": "border",
        "bdt": "border-top",
        "bdr": "border-right",
        "bdb": "border-bottom",
        "bdl": "border-left",
        "bdw": "border-width",
        "bds": "border-style",
        # Border radius
        "br": "border-radius",
        "btlr": "border-top-left-radius",
        "btrr": "border-top-right-radius",
        "bblr": "border-bottom-left-radius",
        "bbrr": "border-bottom-right-radius",
        # Typography
        "fz": "font-size",
        "fw": "font-weight",
        "ff": "font-family",
        "fs": "font-style",
        "lh": "line-height",
        "ls": "letter-spacing",
        "tt": "text-transform",
        "ta": "text-align",
        "td": "text-decoration",
        "ti": "text-indent",
        "tsh": "text-shadow",
        "ws": "white-space",
        # Display and layout
        "d": "display",
        "pos": "position",
        "top": "top",
        "rig": "right",
        "bot": "bottom",
        "lef": "left",
        "z": "z-index",
        "ov": "overflow",
        "ovx": "overflow-x",
        "ovy": "overflow-y",
        # Flexbox
        "fxd": "flex-direction",
        "fxw": "flex-wrap",
        "jc": "justify-content",
        "ai": "align-items",
        "ac": "align-content",
        "as": "align-self",
        "fg": "flex-grow",
        "fsk": "flex-shrink",
        "fb": "flex-basis",
        "gap": "gap",
        "rgap": "row-gap",
        "cgap": "column-gap",
        # Grid
        "gtc": "grid-template-columns",
        "gtr": "grid-template-rows",
        "gta": "grid-template-areas",
        "gac": "grid-auto-columns",
        "gar": "grid-auto-rows",
        "gaf": "grid-auto-flow",
        "gc": "grid-column",
        "gr": "grid-row",
        "ga": "grid-area",
        "jai": "justify-items",
        "jic": "justify-self",
        "ais": "align-self",
        # Effects
        "sh": "box-shadow",
        "bsh": "box-shadow",  # Alternative
        "tsh": "text-shadow",
        "of": "outline",
        "ofc": "outline-color",
        "ofs": "outline-style",
        "ofw": "outline-width",
        "curs": "cursor",
        # Transform
        "tf": "transform",
        "tfo": "transform-origin",
        "trs": "transition",
        # Visibility
        "vis": "visibility",
        "op": "opacity",
    }

    # CSS properties that accept multiple values
    MULTI_VALUE_PROPS = {
        "margin",
        "padding",
        "border",
        "border-width",
        "border-style",
        "border-color",
        "border-radius",
        "background",
        "font-family",
        "transition",
        "transform",
    }

    def __init__(self, props: Dict[str, Any] = None, theme: Optional[Theme] = None):
        self.props = props or {}
        self.theme = theme
        self._expanded_cache = {}

    def set_prop(self, name: str, value: Any) -> None:
        """Set a style prop."""
        self.props[name] = value
        # Clear cache when props change
        self._expanded_cache.clear()

    def get_prop(self, name: str, default: Any = None) -> Any:
        """Get a style prop value."""
        return self.props.get(name, default)

    def update_props(self, props: Dict[str, Any]) -> None:
        """Update multiple style props."""
        self.props.update(props)
        # Clear cache when props change
        self._expanded_cache.clear()

    def _expand_shorthand(self, name: str, value: Any) -> Dict[str, Any]:
        """Expand shorthand property to CSS properties."""
        if name not in self.SHORTHAND_MAPPINGS:
            return {name: value}

        css_prop = self.SHORTHAND_MAPPINGS[name]

        # Handle multi-value shorthand properties
        if isinstance(css_prop, list):
            return {prop: value for prop in css_prop}

        # Handle spacing values with theme integration
        if name in ["m", "p", "mx", "my", "px", "py"] and self.theme:
            resolved_value = self._resolve_spacing_value(value)
            return {css_prop: resolved_value}

        # Handle color values with theme integration
        if name in ["c", "bg", "bc"] and self.theme:
            resolved_value = self._resolve_color_value(value)
            return {css_prop: resolved_value}

        # Handle font size values with theme integration
        if name in ["fz"] and self.theme:
            resolved_value = self._resolve_font_size_value(value)
            return {css_prop: resolved_value}

        return {css_prop: value}

    def _resolve_spacing_value(self, value: Any) -> str:
        """Resolve spacing value using theme tokens."""
        if value is None:
            return None

        # Handle negative spacing
        is_negative = False
        if isinstance(value, str) and value.startswith("-"):
            is_negative = True
            value = value[1:]

        if isinstance(value, (int, float)):
            # Convert pixels to rem for web-like consistency
            # In Qt, we might want to keep as pixels, but let's follow web patterns
            base_value = f"{value}px"
        elif isinstance(value, str):
            # Check if it's a theme spacing key
            if (
                self.theme
                and hasattr(self.theme, "spacing")
                and hasattr(self.theme.spacing, "get_spacing")
            ):
                base_value = self.theme.spacing.get_spacing(value)
                base_value = f"{base_value}px"
            else:
                # Pass through other values (like "1rem", "2em", etc.)
                base_value = value
        else:
            base_value = str(value)

        return f"-{base_value}" if is_negative else base_value

    def _resolve_color_value(self, value: Any) -> str:
        """Resolve color value using theme tokens."""
        if value is None:
            return None

        if isinstance(value, str):
            # Handle theme colors (e.g., "blue", "blue.5", "primary")
            if "." in value:
                color_name, shade = value.split(".", 1)
                if hasattr(self.theme, "colors") and color_name in self.theme.colors:
                    return f"var(--mantine-color-{color_name}-{shade})"

            # Handle simple theme colors
            if hasattr(self.theme, "colors") and value in self.theme.colors:
                return f"var(--mantine-color-{value}-6)"  # Default to shade 6

            # Handle special color keywords
            if value == "dimmed":
                return "var(--mantine-color-dimmed)"
            elif value == "bright":
                return "var(--mantine-color-bright)"
            elif value == "primary":
                return "var(--mantine-primary-color-6)"

            # Handle CSS variables
            if value.startswith("var("):
                return value

            # Handle hex colors, rgb, etc.
            return value

        return str(value)

    def _resolve_font_size_value(self, value: Any) -> str:
        """Resolve font size value using theme tokens."""
        if value is None:
            return None

        if isinstance(value, str):
            # Check if it's a theme font size key
            if hasattr(self.theme, "font_sizes") and value in self.theme.font_sizes:
                return f"var(--mantine-font-size-{value})"

            # Handle heading font sizes
            if value.startswith("h"):
                return f"var(--mantine-{value}-font-size)"

        return str(value)

    def _handle_responsive_value(self, name: str, value: Any) -> Dict[str, Any]:
        """Handle responsive values (dictionary with breakpoints)."""
        if not isinstance(value, dict):
            return self._expand_shorthand(name, value)

        expanded_styles = {}
        for breakpoint, breakpoint_value in value.items():
            # Skip if this is just a regular property value, not a breakpoint
            if breakpoint not in ["base", "xs", "sm", "md", "lg", "xl"]:
                # This might be a regular property, not responsive
                return self._expand_shorthand(name, value)

            # Expand the shorthand for this breakpoint
            breakpoint_styles = self._expand_shorthand(name, breakpoint_value)

            for css_prop, css_value in breakpoint_styles.items():
                if breakpoint == "base":
                    expanded_styles[css_prop] = css_value
                else:
                    # Create media query for responsive breakpoints
                    if "responsive" not in expanded_styles:
                        expanded_styles["responsive"] = {}
                    if breakpoint not in expanded_styles["responsive"]:
                        expanded_styles["responsive"][breakpoint] = {}
                    expanded_styles["responsive"][breakpoint][css_prop] = css_value

        return expanded_styles

    def to_css_dict(self) -> Dict[str, Any]:
        """Convert style props to CSS dictionary with expanded shorthands."""
        if self.props in self._expanded_cache:
            return self._expanded_cache[self.props]

        css_styles = {}
        responsive_styles = {}

        for prop_name, prop_value in self.props.items():
            # Skip None values
            if prop_value is None:
                continue

            # Handle responsive values
            if isinstance(prop_value, dict):
                result = self._handle_responsive_value(prop_name, prop_value)
                if "responsive" in result:
                    # Merge responsive styles
                    for breakpoint, styles in result["responsive"].items():
                        if breakpoint not in responsive_styles:
                            responsive_styles[breakpoint] = {}
                        responsive_styles[breakpoint].update(styles)

                    # Add base styles (non-responsive)
                    for key, value in result.items():
                        if key != "responsive":
                            css_styles[key] = value
                else:
                    # Regular expanded styles
                    css_styles.update(result)
            else:
                # Expand shorthand
                expanded = self._expand_shorthand(prop_name, prop_value)
                css_styles.update(expanded)

        # Combine styles
        final_styles = css_styles.copy()
        if responsive_styles:
            final_styles["responsive"] = responsive_styles

        # Cache the result
        self._expanded_cache[self.props.copy()] = final_styles
        return final_styles

    def to_qss_string(self) -> str:
        """Convert style props to QSS (Qt Style Sheet) string."""
        css_dict = self.to_css_dict()
        qss_parts = []

        for prop, value in css_dict.items():
            if prop == "responsive":
                continue  # Handle responsive styles separately

            if isinstance(value, (list, tuple)):
                # Handle multi-value properties
                qss_parts.append(f"{prop}: {' '.join(str(v) for v in value)};")
            else:
                qss_parts.append(f"{prop}: {value};")

        return "\n".join(qss_parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert style props to dictionary (original format)."""
        return self.props.copy()

    def get_media_queries(self) -> Dict[str, str]:
        """Get responsive media queries for breakpoints."""
        css_dict = self.to_css_dict()
        media_queries = {}

        if "responsive" in css_dict:
            responsive = css_dict["responsive"]

            # Default breakpoints (can be customized via theme)
            breakpoints = {
                "xs": "36em",  # 576px
                "sm": "48em",  # 768px
                "md": "62em",  # 992px
                "lg": "75em",  # 1200px
                "xl": "88em",  # 1408px
            }

            # Override with theme breakpoints if available
            if self.theme and hasattr(self.theme, "breakpoints"):
                breakpoints.update(self.theme.breakpoints)

            for breakpoint, styles in responsive.items():
                if breakpoint in breakpoints:
                    min_width = breakpoints[breakpoint]
                    css_rules = []

                    for prop, value in styles.items():
                        css_rules.append(f"  {prop}: {value};")

                    media_queries[breakpoint] = (
                        f"@media (min-width: {min_width}) {{\n"
                        + "\n".join(css_rules)
                        + "\n}"
                    )

        return media_queries

    def __str__(self) -> str:
        """String representation."""
        return f"StyleProps({self.props})"
