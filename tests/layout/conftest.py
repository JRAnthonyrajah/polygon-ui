"""Shared fixtures and utilities for layout testing."""
import pytest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, Qt


@pytest.fixture(scope="session")
def app():
    """Create QApplication for tests. Session scope to avoid multiple instances."""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    yield app
    if QApplication.instance() == app:
        app.quit()


@pytest.fixture
def qt_widget(app):
    """Create a basic QWidget for testing layouts."""
    widget = QWidget()
    widget.show()  # Show to enable sizing
    yield widget
    widget.deleteLater()


@pytest.fixture
def parent_widget(app, qt_widget):
    """Create a parent widget for layout components."""
    return qt_widget


class ResponsiveTestHelper:
    """Helper for testing responsive behavior by simulating different screen widths."""

    def __init__(self, widget):
        self.widget = widget
        from polygon_ui.layout.core.responsive import BreakpointSystem

        self.breakpoint_system = BreakpointSystem

    def set_width(self, width):
        """Set widget width and process events to trigger responsive updates."""
        self.widget.resize(width, 600)  # Fixed height for consistency
        QTimer.singleShot(0, lambda: app.processEvents())  # Process events

    def get_current_breakpoint(self):
        """Get the current breakpoint based on widget width."""
        width = self.widget.width()
        return self.breakpoint_system.get_breakpoint_for_width(width)

    def assert_responsive_value(self, props, prop_name, expected_values):
        """
        Assert that a responsive prop resolves to expected values at different breakpoints.

        :param props: ResponsiveProps instance
        :param prop_name: Property name
        :param expected_values: Dict of {breakpoint_name: expected_value}
        """
        for bp_name, expected in expected_values.items():
            min_width = self.breakpoint_system.get_min_width(
                self.breakpoint_system.BREAKPOINTS[bp_name]
            )
            self.set_width(min_width)
            actual = props.get(prop_name)
            assert (
                actual == expected
            ), f"At {bp_name} (width {min_width}), {prop_name} should be {expected}, got {actual}"


@pytest.fixture
def responsive_helper(qt_widget):
    """Fixture providing ResponsiveTestHelper."""
    return ResponsiveTestHelper(qt_widget)
