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

    # Standard Qt icon mappings - Enhanced with more professional icons
    STANDARD_ICONS = {
        "search": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogFindIcon
        ),
        "settings": QApplication.style().standardIcon(QApplication.style().SP_Settings),
        "info": QApplication.style().standardIcon(
            QApplication.style().SP_MessageBoxInformation
        ),
        "warning": QApplication.style().standardIcon(
            QApplication.style().SP_MessageBoxWarning
        ),
        "error": QApplication.style().standardIcon(
            QApplication.style().SP_MessageBoxCritical
        ),
        "close": QApplication.style().standardIcon(
            QApplication.style().SP_TitleBarCloseButton
        ),
        "maximize": QApplication.style().standardIcon(
            QApplication.style().SP_TitleBarMaxButton
        ),
        "minimize": QApplication.style().standardIcon(
            QApplication.style().SP_TitleBarMinButton
        ),
        "copy": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogListView
        ),
        "export": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogSaveButton
        ),
        "theme": QApplication.style().standardIcon(
            QApplication.style().SP_ComputerIcon
        ),  # Fallback for theme toggle
        "component": QApplication.style().standardIcon(
            QApplication.style().SP_DirIcon
        ),  # For component items
        "preview": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogDetailedView
        ),  # Eye/view
        "code": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogContentsView
        ),
        "docs": QApplication.style().standardIcon(
            QApplication.style().SP_DialogHelpButton
        ),
        "plus": QApplication.style().standardIcon(
            QApplication.style().SP_FileDialogNewFolder
        ),
        "refresh": QApplication.style().standardIcon(
            QApplication.style().SP_BrowserReload
        ),
        "undo": QApplication.style().standardIcon(QApplication.style().SP_Undo),
        "redo": QApplication.style().standardIcon(QApplication.style().SP_Redo),
        "save": QApplication.style().standardIcon(
            QApplication.style().SP_DialogSaveButton
        ),
        "palette": QApplication.style().standardIcon(
            QApplication.style().SP_ColorPicker
        ),  # For theme
        "play": QApplication.style().standardIcon(QApplication.style().SP_MediaPlay),
        "pause": QApplication.style().standardIcon(QApplication.style().SP_MediaPause),
        "stop": QApplication.style().standardIcon(QApplication.style().SP_MediaStop),
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
    def get_unicode_icon(
        symbol: str,
        font_name: str = "Segoe UI Symbol",
        size: int = 16,
        color: str = "#000000",
    ) -> QIcon:
        """
        Create an icon from Unicode symbol (fallback for custom icons).

        Args:
            symbol (str): Unicode symbol (e.g., '🔍' for search).
            font_name (str): Font name supporting Unicode (Segoe UI Symbol for better coverage).
            size (int): Icon size.
            color (str): Icon color in hex (supports theme integration).

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
    def apply_theme_color(icon: QIcon, color: str, size: int = 16) -> QIcon:
        """
        Recolor an icon to match theme (useful for SVG or simple icons).

        Args:
            icon (QIcon): Original icon.
            color (str): New color in hex.
            size (int): Size for pixmap.

        Returns:
            QIcon: Recolored icon.
        """
        pixmap = icon.pixmap(QSize(size, size))
        painter = QPixmap.painter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
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

        # Enhanced Unicode fallbacks for professional look
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
            "plus": "+",
            "minus": "−",
            "refresh": "↻",
            "play": "▶",
            "pause": "⏸",
            "component": "⚡",  # Spark for components
            "preview": "👁",
        }

        if name in unicode_map and use_unicode_fallback:
            symbol = unicode_map[name]
            return IconManager.get_unicode_icon(symbol, size=size)

        # Default fallback
        return IconManager.get_standard_icon("info", size)
