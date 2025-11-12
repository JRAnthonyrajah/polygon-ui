import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from polygon_ui.polybook.app import PolyBookApp, run_polybook
from polygon_ui.core.provider import PolygonProvider


@pytest.fixture
def app_qt(qtbot):
    app = QApplication.instance() or QApplication([])
    yield app
    app.quit()


def test_theme_switching(app_qt, qtbot):
    # Launch PolyBook
    window = PolyBookApp().window
    qtbot.addWidget(window)
    window.show()

    # Initial light theme
    provider = PolygonProvider.get_instance()
    assert provider.theme.color_scheme == ColorScheme.LIGHT

    # Toggle to dark
    window.theme_toggle.click()
    qtbot.wait(500)  # Wait for update
    assert provider.theme.color_scheme == ColorScheme.DARK

    # Check stylesheet changes (basic assertion)
    stylesheet = window.styleSheet()
    assert "background-color: #f1f3f5" not in stylesheet  # Light bg gone
    assert "#0f172a" in stylesheet  # Dark bg present (slate/gray)

    # Change primary color
    window.primary_color_combo.setCurrentText("red")
    qtbot.wait(500)
    assert provider.theme.primary_color == "red"
    assert "#ff6b6b" in window.styleSheet()  # Red shade


def test_persistence(app_qt, qtbot):
    provider = PolygonProvider()
    provider.update_theme(color_scheme="dark", primary_color="green")

    # New instance should load persisted
    new_provider = PolygonProvider()
    assert new_provider.theme.color_scheme == ColorScheme.DARK
    assert new_provider.theme.primary_color == "green"
