"""
PolygonProvider - Main provider class for Polygon UI.
Equivalent to MantineProvider, manages theme context and global configuration.
"""

from typing import Optional, Dict, Any, Callable
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QObject, Signal

from ..theme.theme import Theme, ThemeProvider, ColorScheme
from ..styles.qss_generator import QSSGenerator


class PolygonProvider(QObject):
    """
    Main provider class for Polygon UI applications.
    Manages theme context, global styling, and provides utilities for components.
    """

    # Signals for theme changes
    theme_changed = Signal(Theme, Theme)  # old_theme, new_theme

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs) -> "PolygonProvider":
        """Singleton pattern - ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(PolygonProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self, theme: Optional[Theme] = None, parent: Optional[QObject] = None):
        if self._initialized:
            return

        # For singleton with parent, handle the parent properly
        if (
            PolygonProvider._instance is not None
            and PolygonProvider._instance is not self
        ):
            super(PolygonProvider, self).__init__(parent)
            return

        super().__init__(parent)

        # Theme management
        self._theme_provider = ThemeProvider(theme)
        self._theme_provider.add_theme_listener(self._on_theme_changed)

        # QSS generator for styling
        self._qss_generator = QSSGenerator()

        # Component registry
        self._component_registry = {}

        # Global CSS variables (equivalent to CSS custom properties)
        self._css_variables = {}

        # Application reference
        self._app = QApplication.instance()

        self._initialized = True

        # Apply initial theme
        self._apply_theme()

    @property
    def theme(self) -> Theme:
        """Get the current theme."""
        return self._theme_provider.get_theme()

    def set_theme(self, theme: Theme) -> None:
        """Set a new theme and apply it to the application."""
        self._theme_provider.set_theme(theme)

    def update_theme(self, **kwargs) -> None:
        """Update theme properties and apply changes."""
        self._theme_provider.update_theme(**kwargs)

    def get_theme_provider(self) -> ThemeProvider:
        """Get the underlying theme provider."""
        return self._theme_provider

    def toggle_color_scheme(self) -> None:
        """Toggle between light and dark themes."""
        self._theme_provider.toggle_color_scheme()

    def _on_theme_changed(self, old_theme: Theme, new_theme: Theme) -> None:
        """Handle theme changes and update the application."""
        self._apply_theme()
        self.theme_changed.emit(old_theme, new_theme)

    def _apply_theme(self) -> None:
        """Apply the current theme to the application."""
        if not self._app:
            return

        # Generate QSS from theme
        qss = self._qss_generator.generate_theme_qss(self.theme)

        # Apply to application
        self._app.setStyleSheet(qss)

    def register_component(self, name: str, component_class: type) -> None:
        """Register a component class with the provider."""
        self._component_registry[name] = component_class

    def get_component(self, name: str) -> Optional[type]:
        """Get a registered component class."""
        return self._component_registry.get(name)

    def list_components(self) -> list[str]:
        """List all registered component names."""
        return list(self._component_registry.keys())

    def get_css_variable(
        self, name: str, default: Optional[str] = None
    ) -> Optional[str]:
        """Get a CSS variable value."""
        return self._css_variables.get(name, default)

    def set_css_variable(self, name: str, value: str) -> None:
        """Set a CSS variable value."""
        self._css_variables[name] = value
        self._apply_theme()

    def get_theme_value(self, path: str, default: Any = None) -> Any:
        """
        Get a theme value by path (e.g., 'colors.blue.6', 'spacing.md').

        Args:
            path: Dot-separated path to the theme value
            default: Default value if path is not found

        Returns:
            The theme value or default
        """
        theme = self.theme
        parts = path.split(".")

        try:
            current = theme
            for part in parts:
                if hasattr(current, part):
                    current = getattr(current, part)
                elif isinstance(current, dict):
                    current = current[part]
                elif hasattr(current, "get_" + part):
                    method = getattr(current, "get_" + part)
                    # For methods that require parameters, use default
                    if callable(method):
                        current = method()
                    else:
                        current = method
                else:
                    return default
            return current
        except (KeyError, AttributeError, TypeError):
            return default

    def generate_component_qss(self, component_name: str, props: Dict[str, Any]) -> str:
        """Generate QSS for a specific component with given props."""
        return self._qss_generator.generate_component_qss(
            component_name, props, self.theme
        )

    def apply_component_theme_overrides(
        self, widget: QWidget, component_type: str
    ) -> None:
        """Apply theme-specific overrides to a component widget."""
        overrides = self.theme.get_component_overrides(component_type)
        if overrides:
            component_qss = self.generate_component_qss(component_type, overrides)
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + "\n" + component_qss)

    def get_responsive_value(self, value: Any, breakpoint: Optional[str] = None) -> Any:
        """
        Get responsive value based on current breakpoint.

        Args:
            value: Value or dictionary of breakpoint values
            breakpoint: Current breakpoint (if None, will be determined from widget)

        Returns:
            The appropriate value for the current breakpoint
        """
        if not isinstance(value, dict):
            return value

        if breakpoint is None:
            # Default to medium breakpoint for now
            # In a real implementation, this would check the actual widget size
            breakpoint = "md"

        # Find the best matching breakpoint
        breakpoint_order = ["xs", "sm", "md", "lg", "xl"]
        current_index = breakpoint_order.index(breakpoint)

        # Find the largest breakpoint <= current breakpoint
        for i in range(current_index, -1, -1):
            bp = breakpoint_order[i]
            if bp in value:
                return value[bp]

        # Fallback to the smallest breakpoint
        return value.get("xs", list(value.values())[0])

    def add_theme_listener(self, listener: Callable[[Theme, Theme], None]) -> None:
        """Add a listener that gets called when the theme changes."""
        self.theme_changed.connect(listener)

    def remove_theme_listener(self, listener: Callable[[Theme, Theme], None]) -> None:
        """Remove a theme change listener."""
        try:
            self.theme_changed.disconnect(listener)
        except:
            pass  # Listener wasn't connected

    @classmethod
    def get_instance(cls) -> "PolygonProvider":
        """Get the singleton instance."""
        if cls._instance is None:
            raise RuntimeError("PolygonProvider has not been initialized")
        return cls._instance

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if the provider has been initialized."""
        return cls._instance is not None and cls._initialized

    def cleanup(self) -> None:
        """Cleanup resources."""
        if self._app:
            self._app.setStyleSheet("")
