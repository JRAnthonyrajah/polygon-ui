"""Tests for the Container component's responsive behavior."""

import pytest
from PySide6.QtWidgets import QApplication, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from polygon_ui.layout.components.container import Container
from polygon_ui.layout.core.responsive import Breakpoint


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance() or QApplication([])
    yield app
    app.quit()


class TestContainerResponsive:
    """Tests for Container responsive properties."""

    @pytest.fixture
    def container(self, app):
        container = Container()
        container.show()  # Needed for width to be valid
        QTest.qWait(100)  # Wait for show
        return container

    def test_responsive_size(self, container):
        """Test responsive size property changes max width based on breakpoint."""
        # Set responsive size
        container.size = {"base": "xs", "md": "lg"}

        # Test at base breakpoint (width < 768)
        original_width = container.width()
        if original_width >= 768:
            container.resize(700, 500)
            QTest.qWait(100)

        assert container.size == "xs"  # Resolved value
        assert container.maximumWidth() == 540  # xs size

        # Resize to md breakpoint (width >= 768)
        container.resize(800, 500)
        QTest.qWait(100)

        assert container.size == "lg"  # Resolved value
        assert container.maximumWidth() == 1140  # lg size

    def test_responsive_fluid(self, container):
        """Test responsive fluid property disables max width at certain breakpoints."""
        # Set responsive fluid
        container.fluid = {"base": False, "lg": True}

        # At base (non-fluid)
        if container.width() >= 992:
            container.resize(500, 500)
            QTest.qWait(100)

        assert not container.fluid
        assert container.maximumWidth() == 960  # Default md size, not fluid

        # Resize to lg (fluid)
        container.resize(1000, 500)
        QTest.qWait(100)

        assert container.fluid
        assert container.maximumWidth() == 16777215  # Max possible, fluid

    def test_responsive_padding(self, container):
        """Test responsive padding updates layout margins."""
        # Set responsive padding
        container.px = {"base": 8, "sm": "lg"}  # lg spacing assumes 32px or theme value
        container.py = {"base": 8, "sm": "lg"}

        # Get layout
        layout = container.layout()
        assert isinstance(layout, QVBoxLayout)

        # At base
        if container.width() >= 576:
            container.resize(500, 500)
            QTest.qWait(100)

        left, top, right, bottom = layout.contentsMargins()
        assert left == 8
        assert top == 8

        # Resize to sm
        container.resize(600, 500)
        QTest.qWait(100)

        # Assuming theme spacing.lg = 32, but since no provider, fallback to 16? Wait, in code fallback is 16 for str
        # But test with int for precision
        # Actually, since no provider in test, str falls back to 16
        # But to test, use ints
        container.px = {"base": 8, "sm": 32}
        container.py = {"base": 8, "sm": 32}

        container.resize(600, 500)
        QTest.qWait(100)

        left, top, right, bottom = layout.contentsMargins()
        assert left == 32
        assert top == 32

    def test_center_property(self, container):
        """Test center property affects layout alignment."""
        layout = container.layout()

        # Default center=True
        assert layout.alignment() == Qt.AlignHCenter

        # Set False
        container.center = False
        assert layout.alignment() == Qt.AlignLeft

    def test_resize_triggers_responsive_update(self, container):
        """Test that resizeEvent updates responsive values."""
        container.size = {"base": "xs", "xl": "xl"}

        # Start at small width
        container.resize(500, 500)
        QTest.qWait(100)
        assert container.maximumWidth() == 540  # xs

        # Resize to large
        container.resize(1300, 500)
        QTest.qWait(100)
        assert container.maximumWidth() == 1600  # xl
