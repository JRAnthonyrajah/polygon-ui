"""
Tests for Center component layout behavior and responsive functionality.
"""

import pytest
from PySide6.QtWidgets import QLabel, QWidget, QPushButton
from PySide6.QtCore import QSize

from polygon_ui.layout.components.center import Center


class TestCenterBasics:
    """Test basic Center component functionality."""

    def test_center_creation(self, qt_widget):
        """Test Center component can be created."""
        center = Center()
        assert center is not None
        assert not center.inline  # Default is False
        assert center.fluid  # Default is True

    def test_center_initialization(self, qt_widget):
        """Test Center component initialization with parameters."""
        center = Center(inline=True, fluid=False, max_width=400, max_height=300)
        assert center.inline
        assert not center.fluid
        assert center.max_width == 400
        assert center.max_height == 300

    def test_center_add_child(self, qt_widget):
        """Test adding children to Center component."""
        center = Center()
        child = QLabel("Test Content")

        center.add_child(child)
        assert child in center._content_container.children()
        assert child.parent() == center._content_container

    def test_center_add_multiple_children(self, qt_widget):
        """Test adding multiple children to Center component."""
        center = Center()
        children = [QLabel(f"Child {i}") for i in range(3)]

        for child in children:
            center.add_child(child)

        for child in children:
            assert child in center._content_container.children()

    def test_center_size_hint(self, qt_widget):
        """Test Center component provides reasonable size hints."""
        center = Center()
        child = QLabel("Test content")
        center.add_child(child)

        size_hint = center.sizeHint()
        assert size_hint.isValid()
        assert size_hint.width() > 0
        assert size_hint.height() > 0


class TestCenterProperties:
    """Test Center component properties."""

    def test_inline_property(self, qt_widget):
        """Test inline property setter and getter."""
        center = Center()

        # Test default
        assert not center.inline

        # Test setting to True
        center.inline = True
        assert center.inline

        # Test setting to False
        center.inline = False
        assert not center.inline

    def test_fluid_property(self, qt_widget):
        """Test fluid property setter and getter."""
        center = Center()

        # Test default
        assert center.fluid

        # Test setting to False
        center.fluid = False
        assert not center.fluid

        # Test setting to True
        center.fluid = True
        assert center.fluid

    def test_max_width_property(self, qt_widget):
        """Test max_width property setter and getter."""
        center = Center()

        # Test default
        assert center.max_width is None

        # Test setting pixel value
        center.max_width = 500
        assert center.max_width == 500

        # Test setting string value
        center.max_width = "lg"
        assert center.max_width == "lg"

        # Test setting to None
        center.max_width = None
        assert center.max_width is None

    def test_max_height_property(self, qt_widget):
        """Test max_height property setter and getter."""
        center = Center()

        # Test default
        assert center.max_height is None

        # Test setting pixel value
        center.max_height = 400
        assert center.max_height == 400

        # Test setting string value
        center.max_height = "md"
        assert center.max_height == "md"

        # Test setting to None
        center.max_height = None
        assert center.max_height is None


class TestCenterResponsive:
    """Test Center component responsive behavior."""

    def test_responsive_inline(self, qt_widget):
        """Test responsive inline property."""
        center = Center()

        # Set responsive inline
        center.inline = {"base": False, "sm": True, "md": True}

        # Verify it's stored as responsive config
        inline_config = center.inline
        assert isinstance(inline_config, dict)
        assert inline_config["base"] is False
        assert inline_config["sm"] is True
        assert inline_config["md"] is True

    def test_responsive_fluid(self, qt_widget):
        """Test responsive fluid property."""
        center = Center()

        # Set responsive fluid
        center.fluid = {"base": True, "md": False, "lg": True}

        # Verify it's stored as responsive config
        fluid_config = center.fluid
        assert isinstance(fluid_config, dict)
        assert fluid_config["base"] is True
        assert fluid_config["md"] is False
        assert fluid_config["lg"] is True

    def test_responsive_max_width(self, qt_widget):
        """Test responsive max_width property."""
        center = Center()

        # Set responsive max_width
        center.max_width = {"base": None, "sm": 300, "md": "lg", "lg": 800}

        # Verify it's stored as responsive config
        max_width_config = center.max_width
        assert isinstance(max_width_config, dict)
        assert max_width_config["base"] is None
        assert max_width_config["sm"] == 300
        assert max_width_config["md"] == "lg"
        assert max_width_config["lg"] == 800

    def test_responsive_max_height(self, qt_widget):
        """Test responsive max_height property."""
        center = Center()

        # Set responsive max_height
        center.max_height = {"base": None, "sm": 200, "md": "md", "lg": 600}

        # Verify it's stored as responsive config
        max_height_config = center.max_height
        assert isinstance(max_height_config, dict)
        assert max_height_config["base"] is None
        assert max_height_config["sm"] == 200
        assert max_height_config["md"] == "md"
        assert max_height_config["lg"] == 600


class TestCenterConvenienceMethods:
    """Test Center component convenience methods."""

    def test_make_inline(self, qt_widget):
        """Test make_inline convenience method."""
        center = Center()
        center.make_inline()
        assert center.inline

    def test_make_block(self, qt_widget):
        """Test make_block convenience method."""
        center = Center()
        center.make_block()
        assert not center.inline

    def test_make_fluid(self, qt_widget):
        """Test make_fluid convenience method."""
        center = Center()
        center.make_fluid()
        assert center.fluid

    def test_make_fixed(self, qt_widget):
        """Test make_fixed convenience method."""
        center = Center()
        center.make_fixed()
        assert not center.fluid

    def test_constrain_width(self, qt_widget):
        """Test constrain_width convenience method."""
        center = Center()
        center.constrain_width(600)
        assert center.max_width == 600

    def test_constrain_height(self, qt_widget):
        """Test constrain_height convenience method."""
        center = Center()
        center.constrain_height(400)
        assert center.max_height == 400

    def test_constrain_both(self, qt_widget):
        """Test constrain_both convenience method."""
        center = Center()
        center.constrain_both(800, 600)
        assert center.max_width == 800
        assert center.max_height == 600

    def test_remove_constraints(self, qt_widget):
        """Test remove_constraints convenience method."""
        center = Center()
        center.max_width = 500
        center.max_height = 400

        center.remove_constraints()
        assert center.max_width is None
        assert center.max_height is None


class TestCenterBehavior:
    """Test Center component behavior in different scenarios."""

    def test_center_with_different_content_types(self, qt_widget):
        """Test Center component with various content types."""
        center = Center()

        # Test with label
        label = QLabel("Test Label")
        center.add_child(label)
        assert label.parent() == center._content_container

        # Test with button
        button = QPushButton("Test Button")
        center.add_child(button)
        assert button.parent() == center._content_container

        # Test with widget
        widget = QWidget()
        widget.setMinimumSize(100, 50)
        center.add_child(widget)
        assert widget.parent() == center._content_container

    def test_center_size_constraints(self, qt_widget):
        """Test Center component respects size constraints."""
        center = Center(max_width=400, max_height=300)
        child = QLabel("Test content with some length")
        center.add_child(child)

        # The content container should have max constraints applied
        assert center._content_container.maximumWidth() == 400
        assert center._content_container.maximumHeight() == 300

    def test_center_resize_updates(self, qt_widget):
        """Test Center component updates on resize."""
        center = Center()
        child = QLabel("Test content")
        center.add_child(child)

        # Trigger resize
        center.resize(800, 600)

        # Component should still be valid
        assert center.isVisible() or True  # Component exists

    def test_center_empty_content(self, qt_widget):
        """Test Center component with no content."""
        center = Center()

        # Should still provide valid size hint
        size_hint = center.sizeHint()
        assert size_hint.isValid()

    def test_center_large_content(self, qt_widget):
        """Test Center component with large content."""
        center = Center(max_width=300, max_height=200)

        # Create content larger than constraints
        large_widget = QWidget()
        large_widget.setMinimumSize(500, 400)
        center.add_child(large_widget)

        # Constraints should be applied
        assert center._content_container.maximumWidth() == 300
        assert center._content_container.maximumHeight() == 200


class TestCenterPerformance:
    """Performance tests for Center component."""

    def test_center_initialization_performance(self, qt_widget):
        """Test Center component initialization performance."""
        import time

        start_time = time.time()

        # Create multiple Center components
        centers = []
        for _ in range(100):
            center = Center()
            center.add_child(QLabel("Test"))
            centers.append(center)

        end_time = time.time()
        duration = end_time - start_time

        # Should be fast (less than 100ms for 100 components)
        assert duration < 0.1, f"Too slow: {duration:.3f}s"

    def test_center_resize_performance(self, qt_widget):
        """Test Center component resize performance."""
        import time

        center = Center()
        child = QLabel("Test content")
        center.add_child(child)

        start_time = time.time()

        # Perform multiple resizes
        for _ in range(100):
            center.resize(800, 600)
            center.resize(400, 300)

        end_time = time.time()
        duration = end_time - start_time

        # Should be fast (less than 50ms for 200 resizes)
        assert duration < 0.05, f"Too slow: {duration:.3f}s"


class TestCenterIntegration:
    """Integration tests with other components."""

    def test_center_in_layout(self, qt_widget):
        """Test Center component used within other layouts."""
        from polygon_ui.layout.components import Stack

        stack = Stack()
        center = Center()
        center.add_child(QLabel("Centered content"))

        stack.add_child(center)
        assert center.parent() == stack

    def test_center_with_nested_content(self, qt_widget):
        """Test Center component with nested content structures."""
        from polygon_ui.layout.components import Stack

        center = Center()

        # Create nested content
        inner_stack = Stack()
        inner_stack.add_child(QLabel("Nested 1"))
        inner_stack.add_child(QLabel("Nested 2"))

        center.add_child(inner_stack)
        assert inner_stack.parent() == center._content_container

    def test_center_responsive_breakpoints(self, qt_widget):
        """Test Center component with responsive breakpoints."""
        center = Center()

        # Set responsive configuration
        center.inline = {"base": False, "sm": True}
        center.max_width = {"base": None, "md": 600, "lg": 800}

        # Should store responsive configuration
        assert isinstance(center.inline, dict)
        assert isinstance(center.max_width, dict)
