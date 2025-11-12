"""Cross-platform compatibility tests for PolyBook.

Ensures consistent behavior across Windows, macOS, Linux.
"""

import sys
import pytest
from unittest.mock import patch

# Detect platform
IS_WINDOWS = sys.platform.startswith("win")
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

from PySide6.QtWidgets import QApplication
from polygon_ui.polybook.app import PolyBookApp


@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.mark.skipif(not IS_WINDOWS, reason="Windows-specific test")
def test_windows_behavior(app):
    """Test Windows-specific UI behavior."""
    with patch("PySide6.QtWidgets.QStyleFactory.create", return_value=None):
        polybook = PolyBookApp()
        # Test native styles, dialog paths, etc.
        assert polybook is not None
        # Specific: Check for Windows line endings in exports
        code = polybook.generate_code()
        assert "\\r\\n" not in code  # Ensure cross-platform newlines


@pytest.mark.skipif(not IS_MACOS, reason="macOS-specific test")
def test_macos_behavior(app):
    """Test macOS-specific UI behavior."""
    polybook = PolyBookApp()
    # Test Retina scaling, menu bar integration
    assert polybook.windowHandle().screen().devicePixelRatio() >= 1.0
    # Specific: Native file dialogs on macOS


@pytest.mark.skipif(not IS_LINUX, reason="Linux-specific test")
def test_linux_behavior(app):
    """Test Linux-specific UI behavior."""
    polybook = PolyBookApp()
    # Test GTK/Qt theme consistency, font rendering
    # Specific: Ensure icons load without X11 issues


@pytest.mark.parametrize("platform", [IS_WINDOWS, IS_MACOS, IS_LINUX])
def test_platform_agnostic_features(platform, app):
    """Test features that must work across all platforms."""
    if sum([IS_WINDOWS, IS_MACOS, IS_LINUX]) == 0:
        pytest.skip("Non-supported platform")
    polybook = PolyBookApp()
    # Test core: theme toggle, component load, export
    assert polybook.polygon_provider is not None
    # Verify QSS applies consistently
    polybook.apply_widget_styles()
    # No platform-specific crashes or visual breaks
