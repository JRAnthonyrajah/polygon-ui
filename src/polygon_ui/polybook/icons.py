"""Icon management system for PolyBook UI components.

Provides consistent icons using Qt's standard icons and Unicode fallbacks for cross-platform compatibility.
"""

from typing import Optional

from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize, Qt


class IconManager:
    """
    Centralized icon manager for PolyBook.

    Supports standard Qt icons and Unicode symbols for custom icons.
    """

    # Standard Qt icon mappings
    STANDARD_ICONS = {
        "search": QApplication.style().standardIcon(QApplication.style().SP_FileDialogFindIcon),
        "settings": QApplication.style().standardIcon(QApplication.style().SP_Settings),
        "info": QApplication.style().standardIcon(QApplication.style().SP_MessageBoxInformation),
        "warning": QApplication.style().standardIcon(QApplication.style().SP_MessageBoxWarning),
        "error": QApplication.style().standardIcon(QApplication.style().SP_MessageBoxCritical),
        "close": QApplication.style().standardIcon(QApplication.style().SP_TitleBarCloseButton),
        "maximize": QApplication.style().standardIcon(QApplication.style().SP_TitleBarMaxButton),
        "minimize": QApplication.style().standardIcon(QApplication.style().SP_TitleBarMinButton),
        "copy": QApplication.style().standardIcon(QApplication.style().SP_FileDialogListView),
        "export": QApplication.style().standardIcon(QApplication.style().SP_FileDialogSaveButton),
        "theme": QApplication.style().standardIcon(QApplication.style().SP_ComputerIcon),  # Fallback for theme toggle
        "component": QApplication.style().standardIcon(QApplication.style().SP_DirIcon),  # For component items
    }

    @staticmethod
    def get_standard_icon(name: str, size: Optional[int] = 16) -> QIcon:
        """
        Get a standard Qt icon by name.

        Args:
            name (str): Icon name (e.g., 'search', 'settings').
            size (int, optional): Icon size in pixels. Defaults to 16.

        Returns:
            QIcon: The requested icon.
        """
        icon = IconManager.STANDARD_ICONS.get(name, IconManager.STANDARD_ICONS["info"])
        if size:
            pixmap = icon.pixmap(QSize(size, size))
            return QIcon(pixmap)
        return icon

    @staticmethod
    def get_unicode_icon(symbol: str, font_name: str = "Arial Unicode MS", size: int = 16, color: str = "#000000") -> QIcon:
        """
        Create an icon from Unicode symbol (fallback for custom icons).

        Args:
            symbol (str): Unicode symbol (e.g., '🔍' for search).
            font_name (str): Font name supporting Unicode.
            size (int): Icon size.
            color (str): Icon color in hex.

        Returns:
            QIcon: Icon from Unicode symbol.
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        painter = QPixmap.painter(pixmap)
        painter.setRenderHint(painter.Antialiasing)

        font = QFont(font_name, size)
        painter.setFont(font)
        painter.setPen(color)
        painter.drawText(0, 0, size, size, Qt.AlignCenter, symbol)
        painter.end()

        return QIcon(pixmap)

    @staticmethod
    def get_icon(name: str, size: int = 16, use_unicode_fallback: bool = True) -> QIcon:
        """
        Get icon by name, with Unicode fallback if standard not available.

        Args:
            name (str): Icon name.
            size (int): Size.
            use_unicode_fallback (bool): Use Unicode if standard icon missing.

        Returns:
            QIcon: The icon.
        """
        if name in IconManager.STANDARD_ICONS:
            return IconManager.get_standard_icon(name, size)

        # Unicode fallbacks
        unicode_map = {
            "search": "🔍",
            "gear": "⚙️",
            "sun": "☀️",
            "moon": "🌙",
            "code": "💻",
            "docs": "📖",
            "export": "📤",
            "copy": "📋",
            "theme_dark": "🌙",
            "theme_light": "☀️",
        }

        if name in unicode_map and use_unicode_fallback:
            symbol = unicode_map[name]
            return IconManager.get_unicode_icon(symbol, size=size)

        # Default fallback
        return IconManager.get_standard_icon("info", size)