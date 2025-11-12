from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from ..theme.theme import ColorScheme, Theme
from ..styles.qss_generator import QSSGenerator


class PolygonProvider:
    """Provides theme management and QSS generation for Polygon UI applications."""

    def __init__(self, theme: Theme):
        self.theme = theme
        self._theme_provider = self  # For compatibility
        self._settings = QSettings("PolygonUI", "PolyBook")

    def _load_preferences(self) -> None:
        """Load saved theme preferences."""
        saved_scheme = self._settings.value("color_scheme", "light")
        saved_primary = self._settings.value("primary_color", "blue")

        # Update current theme if different
        current_scheme = self.theme.color_scheme.value
        if saved_scheme != current_scheme:
            self.update_theme(color_scheme=saved_scheme, primary_color=saved_primary)

    def _save_preferences(self) -> None:
        """Save current theme preferences."""
        self._settings.setValue("color_scheme", self.theme.color_scheme.value)
        self._settings.setValue("primary_color", self.theme.primary_color)

    def toggle_color_scheme(self) -> None:
        """Toggle between light and dark themes."""
        if self.theme.color_scheme == ColorScheme.LIGHT:
            self.update_theme(color_scheme="dark")
        else:
            self.update_theme(color_scheme="light")

    def update_theme(
        self, color_scheme: Optional[str] = None, primary_color: Optional[str] = None
    ) -> None:
        """Update the application theme by regenerating and applying QSS."""
        if color_scheme:
            self.theme.color_scheme = ColorScheme(color_scheme)
        if primary_color:
            self.theme.primary_color = primary_color

        qss_generator = QSSGenerator(self.theme)
        qss = qss_generator.generate_theme_qss()

        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)

        self._save_preferences()
