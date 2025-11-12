"""
Base component class for Polygon UI components.
"""

from typing import Dict, Any, Optional, Union
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal, Property

from .provider import PolygonProvider


class PolygonComponent(QWidget):
    """
    Base class for all Polygon UI components.
    Provides theme integration, style props, and component utilities.
    """

    def __init__(self, parent: Optional[QWidget] = None, **kwargs):
        super().__init__(parent)

        # Style props
        self._style_props = {}

        # Component variant
        self._variant = kwargs.get("variant", "default")
        self._size = kwargs.get("size", "md")

        # Get PolygonProvider instance
        self._provider = (
            PolygonProvider.get_instance() if PolygonProvider.is_initialized() else None
        )

        # Apply initial style props
        style_props = {
            k: v for k, v in kwargs.items() if k not in ["parent", "variant", "size"]
        }
        self.set_style_props(style_props)

        # Apply theme-based styling
        self._apply_theme_styling()

        # Set object name for CSS targeting
        self.setObjectName(self.__class__.__name__.lower())

    def set_style_props(self, props: Dict[str, Any]) -> None:
        """
        Set style props for the component.

        Args:
            props: Dictionary of style props
        """
        self._style_props.update(props)
        self._update_styling()

    def get_style_prop(self, prop_name: str, default: Any = None) -> Any:
        """
        Get a specific style prop value.

        Args:
            prop_name: Name of the style prop
            default: Default value if prop is not set

        Returns:
            Style prop value or default
        """
        return self._style_props.get(prop_name, default)

    def set_style_prop(self, prop_name: str, value: Any) -> None:
        """
        Set a single style prop.

        Args:
            prop_name: Name of the style prop
            value: Value to set
        """
        self._style_props[prop_name] = value
        self._update_styling()

    @Property(str)
    def variant(self) -> str:
        """Get component variant."""
        return self._variant

    @variant.setter
    def variant(self, value: str) -> None:
        """Set component variant."""
        self._variant = value
        self._apply_theme_styling()

    @Property(str)
    def size(self) -> str:
        """Get component size."""
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        """Set component size."""
        self._size = value
        self._apply_theme_styling()

    def _apply_theme_styling(self) -> None:
        """Apply theme-based styling to the component."""
        if not self._provider:
            return

        # Apply component-specific theme overrides
        component_type = self.__class__.__name__.lower()
        self._provider.apply_component_theme_overrides(self, component_type)

        # Apply variant and size based styling
        variant_styles = self._get_variant_styles()
        size_styles = self._get_size_styles()

        if variant_styles or size_styles:
            combined_styles = {**variant_styles, **size_styles}
            component_qss = self._provider.generate_component_qss(
                component_type, combined_styles
            )
            current_style = self.styleSheet()
            self.setStyleSheet(current_style + "\n" + component_qss)

    def _get_variant_styles(self) -> Dict[str, Any]:
        """Get styles based on component variant."""
        # Base implementation - should be overridden by subclasses
        variant_styles = {
            "filled": {"bg": "primary"},
            "outline": {"bd": "1px solid primary", "bg": "transparent"},
            "light": {"bg": "primary.1"},
            "subtle": {"bg": "gray.1"},
            "transparent": {"bg": "transparent"},
        }
        return variant_styles.get(self._variant, {})

    def _get_size_styles(self) -> Dict[str, Any]:
        """Get styles based on component size."""
        # Base implementation - should be overridden by subclasses
        size_styles = {
            "xs": {"py": "xs", "px": "sm"},
            "sm": {"py": "sm", "px": "md"},
            "md": {"py": "md", "px": "lg"},
            "lg": {"py": "lg", "px": "xl"},
            "xl": {"py": "xl", "px": "xxl"},
        }
        return size_styles.get(self._size, {})

    def _update_styling(self) -> None:
        """Update component styling based on current style props."""
        if not self._provider:
            return

        component_name = self.__class__.__name__.lower()
        combined_props = {
            **self._style_props,
            "variant": self._variant,
            "size": self._size,
        }

        # Add layout-specific props to combined if it's a layout component
        if hasattr(self, "_gap"):
            combined_props.update(
                {
                    "gap": self._gap,
                    "justify": self._justify,
                    "align": self._align,
                    "direction": getattr(self, "_direction", "column"),
                }
            )
        if hasattr(self, "_columns"):
            combined_props.update(
                {
                    "columns": self._columns,
                    "gutter": self._gutter,
                }
            )
        # Add responsive props
        if hasattr(self, "_responsive_props"):
            combined_props["responsive"] = self._responsive_props

        # Generate QSS from style props
        component_qss = self._provider.generate_component_qss(
            component_name, combined_props
        )

        # Apply to widget
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + "\n" + component_qss)

    def get_theme_value(self, path: str, default: Any = None) -> Any:
        """
        Get a theme value by path.

        Args:
            path: Dot-separated path to the theme value
            default: Default value if path is not found

        Returns:
            Theme value or default
        """
        if self._provider:
            return self._provider.get_theme_value(path, default)
        return default

    def showEvent(self, event) -> None:
        """Handle widget show event."""
        super().showEvent(event)
        # Ensure styling is applied when widget becomes visible
        self._apply_theme_styling()

    def changeEvent(self, event) -> None:
        """Handle widget change events."""
        super().changeEvent(event)
        # Reapply styling when theme changes
        if event.type() == event.Type.PaletteChange:
            self._apply_theme_styling()
