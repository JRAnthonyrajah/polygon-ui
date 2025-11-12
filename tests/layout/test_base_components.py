"""
Tests for base layout components.
"""

import pytest
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

from src.polygon_ui.layout.core.base import (
    LayoutComponent,
    GridComponent,
    UtilityComponent,
)


@pytest.fixture
def app():
    """Create QApplication for tests."""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    return app


@pytest.fixture
def parent_widget(app):
    """Create a parent widget for testing."""
    widget = QWidget()
    return widget


class TestLayoutComponent:
    """Test the LayoutComponent base class."""

    def test_initialization(self, parent_widget):
        """Test LayoutComponent initialization."""
        component = LayoutComponent(parent_widget, gap="md", justify="center")
        assert component.gap == "md"
        assert component.justify == "center"
        assert component.align == "stretch"

    def test_add_child(self, parent_widget):
        """Test adding children to layout component."""
        component = LayoutComponent(parent_widget)
        child = QLabel("Test")

        component.add_child(child)
        assert child in component._children
        assert child.parent() == component

    def test_remove_child(self, parent_widget):
        """Test removing children from layout component."""
        component = LayoutComponent(parent_widget)
        child = QLabel("Test")

        component.add_child(child)
        component.remove_child(child)
        assert child not in component._children

    def test_responsive_props(self, parent_widget):
        """Test responsive property handling."""
        component = LayoutComponent(parent_widget)

        # Test simple value
        component.set_responsive_prop("test", 4)
        assert component.get_responsive_value("test") == 4

        # Test responsive dict
        responsive_value = {"base": 1, "sm": 2}
        component.set_responsive_prop("columns", responsive_value)
        result = component.get_responsive_value("columns", 1)
        assert result in [1, 2]  # Depends on current width

    def test_gap_property(self, parent_widget):
        """Test gap property setter/getter."""
        component = LayoutComponent(parent_widget)
        component.gap = "lg"
        assert component.gap == "lg"

    def test_justify_property(self, parent_widget):
        """Test justify property setter/getter."""
        component = LayoutComponent(parent_widget)
        component.justify = "space-between"
        assert component.justify == "space-between"

    def test_align_property(self, parent_widget):
        """Test align property setter/getter."""
        component = LayoutComponent(parent_widget)
        component.align = "center"
        assert component.align == "center"


class TestGridComponent:
    """Test the GridComponent base class."""

    def test_initialization(self, parent_widget):
        """Test GridComponent initialization."""
        component = GridComponent(parent_widget, columns=12, gutter="md")
        assert component.columns == 12
        assert component.gutter == "md"

    def test_columns_property(self, parent_widget):
        """Test columns property setter/getter."""
        component = GridComponent(parent_widget)
        component.columns = 8
        assert component.columns == 8

    def test_gutter_property(self, parent_widget):
        """Test gutter property setter/getter."""
        component = GridComponent(parent_widget)
        component.gutter = "lg"
        assert component.gutter == "lg"

    def test_inherits_layout_component(self, parent_widget):
        """Test that GridComponent inherits LayoutComponent functionality."""
        component = GridComponent(parent_widget)
        child = QLabel("Test")

        component.add_child(child)
        assert child in component._children
        assert component.gap == "md"  # Default value


class TestUtilityComponent:
    """Test the UtilityComponent base class."""

    def test_initialization(self, parent_widget):
        """Test UtilityComponent initialization."""
        component = UtilityComponent(parent_widget, inline=True, fluid=True)
        assert component.inline is True
        assert component.fluid is True

    def test_inline_property(self, parent_widget):
        """Test inline property setter/getter."""
        component = UtilityComponent(parent_widget)
        component.inline = True
        assert component.inline is True

    def test_fluid_property(self, parent_widget):
        """Test fluid property setter/getter."""
        component = UtilityComponent(parent_widget)
        component.fluid = True
        assert component.fluid is True

    def test_inherits_layout_component(self, parent_widget):
        """Test that UtilityComponent inherits LayoutComponent functionality."""
        component = UtilityComponent(parent_widget)
        child = QLabel("Test")

        component.add_child(child)
        assert child in component._children
        assert component.gap == "md"  # Default value


if __name__ == "__main__":
    pytest.main([__file__])
