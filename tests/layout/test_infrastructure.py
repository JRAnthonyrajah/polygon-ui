"""
Basic tests for layout infrastructure components.
"""

import pytest
from PySide6.QtWidgets import QApplication, QWidget, QLabel

# Test that the foundation components can be imported and instantiated
from src.polygon_ui.layout.core.base import LayoutComponent, GridComponent, UtilityComponent


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


def test_layout_component_creation(parent_widget):
    """Test basic LayoutComponent creation."""
    component = LayoutComponent(parent_widget)
    assert component is not None
    assert component.gap == "md"  # Default value
    assert component.justify == "start"  # Default value
    assert component.align == "stretch"  # Default value


def test_grid_component_creation(parent_widget):
    """Test basic GridComponent creation."""
    component = GridComponent(parent_widget)
    assert component is not None
    assert component.columns == 12  # Default value
    assert component.gutter == "md"  # Default value


def test_utility_component_creation(parent_widget):
    """Test basic UtilityComponent creation."""
    component = UtilityComponent(parent_widget)
    assert component is not None
    assert component.inline is False  # Default value
    assert component.fluid is False  # Default value


def test_add_child_to_layout(parent_widget):
    """Test adding children to layout components."""
    component = LayoutComponent(parent_widget)
    child = QLabel("Test Label")

    component.add_child(child)
    assert child in component._children


def test_remove_child_from_layout(parent_widget):
    """Test removing children from layout components."""
    component = LayoutComponent(parent_widget)
    child = QLabel("Test Label")

    component.add_child(child)
    component.remove_child(child)
    assert child not in component._children


if __name__ == "__main__":
    pytest.main([__file__])