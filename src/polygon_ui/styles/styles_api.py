"""
Styles API for Polygon UI components.
Implements Mantine-like styling with classNames, styles, and data attributes.
"""

from typing import Dict, Any, Callable, Optional, Union, List
from ..theme.theme import Theme


class StylesAPI:
    """
    Styles API for component customization following Mantine patterns.

    Supports:
    - `classNames` prop for CSS class names on specific elements
    - `styles` prop for inline styles on specific elements
    - `attributes` prop for custom element attributes
    - `stylesNames` selectors for component element targeting
    - Data attribute generation for state-based styling
    """

    def __init__(
        self,
        styles: Dict[str, Any] = None,
        classNames: Dict[str, str] = None,
        attributes: Dict[str, Dict[str, Any]] = None,
        theme: Optional[Theme] = None,
        component_name: str = None,
    ):
        """
        Initialize StylesAPI.

        Args:
            styles: Dictionary of inline styles for component elements
            classNames: Dictionary of CSS class names for component elements
            attributes: Dictionary of custom attributes for component elements
            theme: Theme instance for CSS variable resolution
            component_name: Name of the component (for CSS class generation)
        """
        self.styles = styles or {}
        self.classNames = classNames or {}
        self.attributes = attributes or {}
        self.theme = theme
        self.component_name = component_name
        self._selectors = {}
        self._data_attributes = {}

    def set_style(self, selector: str, style: Dict[str, Any]) -> None:
        """
        Set inline style for a specific selector/element.

        Args:
            selector: Element selector (e.g., 'root', 'label', 'input')
            style: CSS properties dictionary
        """
        self.styles[selector] = style

    def get_style(self, selector: str) -> Optional[Dict[str, Any]]:
        """Get inline style for a specific selector."""
        return self.styles.get(selector)

    def set_class_name(self, selector: str, class_name: str) -> None:
        """
        Set CSS class name for a specific selector/element.

        Args:
            selector: Element selector (e.g., 'root', 'label', 'input')
            class_name: CSS class name(s)
        """
        self.classNames[selector] = class_name

    def get_class_name(self, selector: str) -> Optional[str]:
        """Get CSS class name for a specific selector."""
        return self.classNames.get(selector)

    def set_attribute(self, selector: str, attribute: str, value: Any) -> None:
        """
        Set custom attribute for a specific selector/element.

        Args:
            selector: Element selector (e.g., 'root', 'label', 'input')
            attribute: Attribute name (e.g., 'data-test-id', 'aria-label')
            value: Attribute value
        """
        if selector not in self.attributes:
            self.attributes[selector] = {}
        self.attributes[selector][attribute] = value

    def get_attributes(self, selector: str) -> Optional[Dict[str, Any]]:
        """Get custom attributes for a specific selector."""
        return self.attributes.get(selector)

    def set_data_attribute(self, selector: str, attribute: str, value: Any) -> None:
        """
        Set data attribute for state-based styling.

        Args:
            selector: Element selector
            attribute: Data attribute name (e.g., 'loading', 'disabled')
            value: Attribute value
        """
        data_attr = f"data-{attribute}"
        self.set_attribute(selector, data_attr, value)

        # Track data attributes for CSS generation
        if selector not in self._data_attributes:
            self._data_attributes[selector] = {}
        self._data_attributes[selector][attribute] = value

    def get_data_attributes(self, selector: str) -> Optional[Dict[str, Any]]:
        """Get data attributes for a specific selector."""
        return self._data_attributes.get(selector)

    def register_selector(self, name: str, css_selector: str) -> None:
        """
        Register a CSS selector for component element targeting.

        Args:
            name: Internal selector name (e.g., 'root', 'label', 'input')
            css_selector: CSS selector string (e.g., '.mantine-Button-root')
        """
        self._selectors[name] = css_selector

    def get_selectors(self) -> Dict[str, str]:
        """Get all registered selectors."""
        return self._selectors.copy()

    def get_css_selector(self, name: str) -> Optional[str]:
        """Get CSS selector for a specific element."""
        return self._selectors.get(name)

    def apply_function(self, style_func: Callable) -> Dict[str, Any]:
        """
        Apply a function to generate styles.

        Args:
            style_func: Function that returns style dictionary

        Returns:
            Generated styles dictionary
        """
        return style_func()

    def resolve_theme_variables(self, styles: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve theme variables in style values.

        Args:
            styles: Styles dictionary with potential theme variables

        Returns:
            Styles with resolved CSS variables
        """
        if not self.theme:
            return styles

        resolved = {}
        for prop, value in styles.items():
            if isinstance(value, str):
                # Handle theme color references
                if "." in value:
                    color_name, shade = value.split(".", 1)
                    if (
                        hasattr(self.theme, "colors")
                        and color_name in self.theme.colors
                    ):
                        resolved[prop] = f"var(--mantine-color-{color_name}-{shade})"
                        continue

                # Handle simple theme colors
                if hasattr(self.theme, "colors") and value in self.theme.colors:
                    resolved[prop] = f"var(--mantine-color-{value}-6)"
                    continue

                # Handle spacing tokens
                if hasattr(self.theme, "spacing") and hasattr(
                    self.theme.spacing, "get_spacing"
                ):
                    try:
                        spacing_value = self.theme.spacing.get_spacing(value)
                        resolved[prop] = f"{spacing_value}px"
                        continue
                    except:
                        pass

                # Handle font size tokens
                if hasattr(self.theme, "typography") and hasattr(
                    self.theme.typography, "font_sizes"
                ):
                    if value in self.theme.typography.font_sizes:
                        resolved[prop] = f"var(--mantine-font-size-{value})"
                        continue

                # Handle special color keywords
                if value == "dimmed":
                    resolved[prop] = "var(--mantine-color-dimmed)"
                    continue
                elif value == "bright":
                    resolved[prop] = "var(--mantine-color-bright)"
                    continue
                elif value == "primary":
                    resolved[prop] = "var(--mantine-primary-color-6)"
                    continue

            resolved[prop] = value

        return resolved

    def generate_css_classes(self) -> Dict[str, str]:
        """
        Generate CSS class names for component elements.

        Returns:
            Dictionary mapping selectors to CSS class names
        """
        if not self.component_name:
            return {}

        css_classes = {}
        for selector in self._selectors.keys():
            # Generate consistent class name like "mantine-Button-root"
            class_name = f"mantine-{self.component_name}-{selector}"
            css_classes[selector] = class_name

        return css_classes

    def to_css_dict(self) -> Dict[str, Any]:
        """
        Convert all styles to CSS dictionary with theme resolution.

        Returns:
            Combined styles dictionary
        """
        combined_styles = {}

        # Resolve theme variables in all styles
        for selector, style in self.styles.items():
            combined_styles[selector] = self.resolve_theme_variables(style)

        return combined_styles

    def to_qss_string(self, selector: str = None) -> str:
        """
        Convert styles to QSS string for Qt styling.

        Args:
            selector: Specific selector to generate QSS for, or None for all

        Returns:
            QSS string
        """
        if selector:
            return self._generate_selector_qss(selector)
        else:
            return self._generate_all_qss()

    def _generate_selector_qss(self, selector: str) -> str:
        """Generate QSS for a specific selector."""
        css_selector = self.get_css_selector(selector)
        if not css_selector:
            css_selector = f".{selector}"

        styles = self.get_style(selector)
        if not styles:
            return ""

        # Resolve theme variables
        resolved_styles = self.resolve_theme_variables(styles)

        # Convert to QSS properties
        qss_parts = [f"{css_selector} {{"]
        for prop, value in resolved_styles.items():
            qss_parts.append(f"  {prop}: {value};")
        qss_parts.append("}")

        return "\n".join(qss_parts)

    def _generate_all_qss(self) -> str:
        """Generate QSS for all selectors."""
        qss_parts = []

        for selector in self._selectors.keys():
            qss = self._generate_selector_qss(selector)
            if qss:
                qss_parts.append(qss)

        return "\n\n".join(qss_parts)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert StylesAPI to dictionary representation.

        Returns:
            Dictionary with styles, classNames, and attributes
        """
        return {
            "styles": self.styles.copy(),
            "classNames": self.classNames.copy(),
            "attributes": self.attributes.copy(),
            "selectors": self._selectors.copy(),
            "dataAttributes": self._data_attributes.copy(),
        }

    def merge_with(self, other: "StylesAPI") -> "StylesAPI":
        """
        Merge this StylesAPI with another one.

        Args:
            other: Another StylesAPI instance

        Returns:
            New StylesAPI with merged properties
        """
        merged = StylesAPI(
            styles=self.styles.copy(),
            classNames=self.classNames.copy(),
            attributes=self.attributes.copy(),
            theme=self.theme,
            component_name=self.component_name,
        )

        # Merge styles
        for selector, style in other.styles.items():
            if selector in merged.styles:
                merged.styles[selector].update(style)
            else:
                merged.styles[selector] = style

        # Merge classNames
        merged.classNames.update(other.classNames)

        # Merge attributes
        for selector, attrs in other.attributes.items():
            if selector in merged.attributes:
                merged.attributes[selector].update(attrs)
            else:
                merged.attributes[selector] = attrs

        # Merge selectors
        merged._selectors.update(other._selectors)

        # Merge data attributes
        merged._data_attributes.update(other._data_attributes)

        return merged

    def clone(self) -> "StylesAPI":
        """Create a deep copy of this StylesAPI."""
        return StylesAPI(
            styles={
                k: v.copy() if isinstance(v, dict) else v
                for k, v in self.styles.items()
            },
            classNames=self.classNames.copy(),
            attributes={
                k: v.copy() if isinstance(v, dict) else v
                for k, v in self.attributes.items()
            },
            theme=self.theme,
            component_name=self.component_name,
        )

    def __str__(self) -> str:
        """String representation."""
        return f"StylesAPI(component={self.component_name}, selectors={list(self._selectors.keys())})"
