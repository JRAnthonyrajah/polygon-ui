"""Accessibility utilities for PolyBook.

Provides keyboard navigation and ARIA-like properties for WCAG compliance.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QShortcut


class AccessibilityManager:
    """
    Manages keyboard navigation and accessibility features for PolyBook.
    """

    SHORTCUTS = {
        Qt.Key_F1: "Focus documentation panel",
        Qt.Key_F5: "Refresh component preview",
        Qt.Key_Escape: "Clear search and reset list",
        Qt.Key_Tab: "Navigate between focusable elements",
        Qt.Key_Return: "Activate selected component",
        Qt.Key_Up: "Previous component in list",
        Qt.Key_Down: "Next component in list",
    }

    @classmethod
    def setup_shortcuts(cls, parent):
        """
        Setup global keyboard shortcuts for accessibility.
        """
        for key, description in cls.SHORTCUTS.items():
            shortcut = QShortcut(key, parent)
            shortcut.setContext(Qt.ApplicationShortcut)
            shortcut.setAutoRepeat(False)
            # Connect to parent keyPressEvent or specific handlers

    @staticmethod
    def announce_change(widget, message):
        """
        Announce changes for screen readers (Qt accessibility API).
        """
        widget.setAccessibleName(message)
        # Qt's built-in accessibility will pick this up
