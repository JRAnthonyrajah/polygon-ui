    from typing import Optional

from PySide6.QtWidgets import QApplication

from ..styles.qss_generator import QSSGenerator


from typing import Optional
from ..theme.theme import ColorScheme
from PySide6.QtWidgets import QApplication
from ..styles.qss_generator import QSSGenerator


def _load_preferences(self) -> None:
        """Load saved theme preferences."""
        saved_scheme = self._settings.value("color_scheme", "light")
        saved_primary = self._settings.value("primary_color", "blue")

        # Update current theme if different
        current_scheme = self.theme.color_scheme.value
        if saved_scheme != current_scheme:
            self.update_theme(color_scheme=saved_scheme)

        if saved_primary != self.theme.primary_color:
            self.update_theme(primary_color=saved_primary)

    def _save_preferences(self) -> None:
        \"\"\"Save current theme preferences.\"\"\"
        self._settings.setValue("color_scheme", self.theme.color_scheme.value)
        self._settings.setValue("primary_color", self.theme.primary_color)

    def toggle_color_scheme(self) -> None:
        \"\"\"Toggle between light and dark themes.\"\"\"
        self._theme_provider.toggle_color_scheme()
        self.update_theme()

    def update_theme(self, color_scheme: Optional[str] = None, primary_color: Optional[str] = None) -> None:
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
