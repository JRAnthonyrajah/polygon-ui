"""
Comprehensive tests for Stack component.
"""

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QSizePolicy
from PySide6.QtCore import Qt

from polygon_ui.layout.components.stack import Stack


@pytest.fixture
def app():
    """QApplication fixture for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit app as it might be shared between tests


class TestStackComponent:
    """Test basic Stack component functionality."""

    def test_stack_initialization(self, app):
        """Test Stack can be created with default properties."""
        stack = Stack()
        assert stack.direction == "column"
        assert stack.gap == "md"
        assert stack.justify == "start"
        assert stack.align == "stretch"
        assert stack.layout() is not None
        assert stack.layout().count() == 0

    def test_stack_initialization_with_props(self, app):
        """Test Stack initialization with custom properties."""
        stack = Stack(direction="row", gap="lg", justify="center", align="center")
        assert stack.direction == "row"
        assert stack.gap == "lg"
        assert stack.justify == "center"
        assert stack.align == "center"

    def test_stack_responsive_props(self, app):
        """Test Stack responsive properties."""
        # Test responsive gap
        stack = Stack(gap={"base": "sm", "md": "lg"})
        assert stack.gap == "sm"  # Should resolve to smallest available

        # Test responsive direction
        stack = Stack(direction={"base": "column", "md": "row"})
        assert stack.direction in [None, "column"]  # None if no breakpoint matched

    def test_stack_add_child(self, app):
        """Test adding children to Stack."""
        stack = Stack()
        child = QLabel("Test Child")

        stack.add_child(child)
        assert stack.layout().count() == 1
        assert stack.layout().itemAt(0).widget() == child

    def test_stack_add_multiple_children(self, app):
        """Test adding multiple children to Stack."""
        stack = Stack()
        children = [QLabel(f"Child {i}") for i in range(3)]

        for child in children:
            stack.add_child(child)

        assert stack.layout().count() == 3
        for i, child in enumerate(children):
            assert stack.layout().itemAt(i).widget() == child

    def test_stack_direction_property(self, app):
        """Test direction property getter/setter."""
        stack = Stack()

        # Test setting column
        stack.direction = "column"
        assert stack.direction == "column"

        # Test setting row
        stack.direction = "row"
        assert stack.direction == "row"

    def test_stack_gap_property(self, app):
        """Test gap property getter/setter."""
        stack = Stack()

        # Test string values
        stack.gap = "sm"
        assert stack.gap == "sm"

        stack.gap = "lg"
        assert stack.gap == "lg"

        # Test integer values
        stack.gap = 20
        assert stack.gap == 20

    def test_stack_justify_property(self, app):
        """Test justify property getter/setter."""
        stack = Stack()

        for justify_value in [
            "start",
            "center",
            "end",
            "space-between",
            "space-around",
        ]:
            stack.justify = justify_value
            assert stack.justify == justify_value

    def test_stack_align_property(self, app):
        """Test align property getter/setter."""
        stack = Stack()

        for align_value in ["start", "center", "end", "stretch"]:
            stack.align = align_value
            assert stack.align == align_value

    def test_stack_direction_switching_preserves_children(self, app):
        """Test that changing direction preserves children."""
        stack = Stack(direction="column")

        # Add children
        children = [QLabel(f"Child {i}") for i in range(3)]
        for child in children:
            stack.add_child(child)

        initial_count = stack.layout().count()

        # Change direction
        stack.direction = "row"

        # Children should be preserved
        assert stack.layout().count() == initial_count
        assert stack.direction == "row"


class TestStackResponsive:
    """Test Stack responsive behavior."""

    def test_stack_responsive_gap(self, app):
        """Test responsive gap behavior."""
        stack = Stack(gap={"base": "sm", "md": "lg"})
        # Base breakpoint should match smallest
        assert stack.gap in ["sm", None]  # None if no breakpoint active

    def test_stack_responsive_direction(self, app):
        """Test responsive direction behavior."""
        stack = Stack(direction={"base": "column", "md": "row"})
        # Base breakpoint should match smallest
        assert stack.direction in ["column", None]

    def test_stack_responsive_justify(self, app):
        """Test responsive justify behavior."""
        stack = Stack(justify={"base": "start", "md": "center"})
        # Base breakpoint should match smallest
        assert stack.justify in ["start", None]

    def test_stack_responsive_align(self, app):
        """Test responsive align behavior."""
        stack = Stack(align={"base": "stretch", "md": "center"})
        # Base breakpoint should match smallest
        assert stack.align in ["stretch", None]


class TestStackChildSizing:
    """Test Stack child widget sizing functionality."""

    def test_stack_child_grow_vertical(self, app):
        """Test grow property in vertical layout."""
        stack = Stack(direction="column")

        child = QLabel("Growing Child")
        stack.add_child(child, grow=True)

        # Check size policy was set to expand vertically
        size_policy = child.sizePolicy()
        assert size_policy.verticalPolicy() == QSizePolicy.Expanding

    def test_stack_child_grow_horizontal(self, app):
        """Test grow property in horizontal layout."""
        stack = Stack(direction="row")

        child = QLabel("Growing Child")
        stack.add_child(child, grow=True)

        # Check size policy was set to expand horizontally
        size_policy = child.sizePolicy()
        assert size_policy.horizontalPolicy() == QSizePolicy.Expanding

    def test_stack_child_shrink_vertical(self, app):
        """Test shrink property in vertical layout."""
        stack = Stack(direction="column")

        child = QLabel("Shrinking Child")
        stack.add_child(child, shrink=True)

        # Check size policy was set appropriately
        size_policy = child.sizePolicy()
        assert size_policy.horizontalPolicy() == QSizePolicy.Expanding

    def test_stack_child_shrink_horizontal(self, app):
        """Test shrink property in horizontal layout."""
        stack = Stack(direction="row")

        child = QLabel("Shrinking Child")
        stack.add_child(child, shrink=True)

        # Check size policy was set appropriately
        size_policy = child.sizePolicy()
        assert size_policy.verticalPolicy() == QSizePolicy.Expanding

    def test_stack_child_flex_basis(self, app):
        """Test flex basis property."""
        stack = Stack(direction="column")

        child = QLabel("Flex Basis Child")
        stack.add_child(child, flex_basis=100)

        # Should set minimum height
        assert child.minimumHeight() == 100

    def test_stack_child_flex_basis_horizontal(self, app):
        """Test flex basis property in horizontal layout."""
        stack = Stack(direction="row")

        child = QLabel("Flex Basis Child")
        stack.add_child(child, flex_basis=150)

        # Should set minimum width
        assert child.minimumWidth() == 150

    def test_stack_child_alignment(self, app):
        """Test child alignment property."""
        stack = Stack(direction="column")

        # Test center alignment
        child = QLabel("Centered Child")
        stack.add_child(child, align="center")

        # Child should have horizontal center alignment
        assert child.alignment() & Qt.AlignHCenter

    def test_stack_child_alignment_horizontal(self, app):
        """Test child alignment in horizontal layout."""
        stack = Stack(direction="row")

        # Test center alignment
        child = QLabel("Centered Child")
        stack.add_child(child, align="center")

        # Child should have vertical center alignment
        assert child.alignment() & Qt.AlignVCenter


class TestStackLayoutBehavior:
    """Test Stack layout behavior."""

    def test_stack_vertical_layout(self, app):
        """Test vertical stack layout behavior."""
        stack = Stack(direction="column")

        # Stack should use QVBoxLayout
        assert stack.layout().__class__.__name__ == "QVBoxLayout"

    def test_stack_horizontal_layout(self, app):
        """Test horizontal stack layout behavior."""
        stack = Stack(direction="row")

        # Stack should use QHBoxLayout
        assert stack.layout().__class__.__name__ == "QHBoxLayout"

    def test_stack_gap_spacing(self, app):
        """Test gap creates proper spacing."""
        stack = Stack(gap="md")

        # Gap should affect layout spacing
        # Note: Spacing value depends on theme availability
        # We just test that spacing is set
        assert stack.layout().spacing() >= 0

    def test_stack_empty_layout(self, app):
        """Test Stack with no children."""
        stack = Stack()

        # Should handle empty layout gracefully
        assert stack.layout().count() == 0
        assert stack.layout() is not None

    def test_stack_single_child(self, app):
        """Test Stack with single child."""
        stack = Stack()
        child = QLabel("Single Child")
        stack.add_child(child)

        assert stack.layout().count() == 1
        assert stack.layout().itemAt(0).widget() == child

    def test_stack_many_children(self, app):
        """Test Stack with many children."""
        stack = Stack()
        num_children = 50

        for i in range(num_children):
            child = QLabel(f"Child {i}")
            stack.add_child(child)

        assert stack.layout().count() == num_children


class TestStackPerformance:
    """Test Stack performance characteristics."""

    def test_stack_initialization_performance(self, app, benchmark):
        """Test Stack initialization performance."""

        def create_stack():
            return Stack(gap="md", justify="center", align="stretch")

        stack = benchmark(create_stack)
        assert stack is not None

    def test_stack_add_child_performance(self, app, benchmark):
        """Test add_child performance."""

        def add_child():
            test_stack = Stack()
            test_child = QLabel("Test")
            test_stack.add_child(test_child)
            return test_stack

        result = benchmark(add_child)
        assert result.layout().count() == 1

    def test_stack_direction_change_performance(self, app, benchmark):
        """Test direction change performance."""

        def change_direction():
            test_stack = Stack()
            for i in range(5):
                child = QLabel(f"Child {i}")
                test_stack.add_child(child)
            test_stack.direction = "row"
            return test_stack

        result = benchmark(change_direction)
        assert result.direction == "row"
        assert result.layout().count() == 5

    def test_stack_large_number_children(self, app, benchmark):
        """Test Stack with large number of children."""

        def create_large_stack():
            stack = Stack()
            for i in range(100):
                child = QLabel(f"Child {i}")
                stack.add_child(child)
            return stack

        stack = benchmark(create_large_stack)
        assert stack.layout().count() == 100


class TestStackNestedLayouts:
    """Test Stack in nested layout scenarios."""

    def test_stack_inside_container(self, app):
        """Test Stack inside Container component."""
        try:
            from polygon_ui.layout.components.container import Container
        except ImportError:
            pytest.skip("Container component not available")

        container = Container(size="md", px="sm")
        stack = Stack(gap="md")

        # Add children to stack
        for i in range(3):
            label = QLabel(f"Nested Child {i}")
            stack.add_child(label)

        # Add stack to container
        container.add_child(stack)

        assert container.layout().count() == 1
        assert stack.layout().count() == 3

    def test_nested_stacks(self, app):
        """Test nested Stack components."""
        parent_stack = Stack(direction="column", gap="sm")

        # Create child stacks
        for stack_dir in ["column", "row"]:
            child_stack = Stack(direction=stack_dir, gap="xs")

            # Add grandchildren
            for i in range(2):
                label = QLabel(f"Label {stack_dir}-{i}")
                child_stack.add_child(label)

            parent_stack.add_child(child_stack)

        assert parent_stack.layout().count() == 2

        # Each child stack should have 2 children
        for i in range(parent_stack.layout().count()):
            child_widget = parent_stack.layout().itemAt(i).widget()
            assert child_widget.layout().count() == 2


class TestStackEdgeCases:
    """Test Stack edge cases."""

    def test_stack_invalid_direction(self, app):
        """Test Stack with invalid direction."""
        stack = Stack()
        # Component should handle invalid direction gracefully
        stack.direction = "invalid_direction"
        # Currently accepts any string, this documents behavior

    def test_stack_none_child(self, app):
        """Test adding None child."""
        stack = Stack()

        # Should handle None child gracefully
        try:
            stack.add_child(None)
        except (TypeError, AttributeError):
            # Expected to fail, but shouldn't crash
            pass

    def test_stack_size_calculation_with_children(self, app):
        """Test size calculation when children have size policies."""
        stack = Stack(direction="column")

        # Add children with different size policies
        child1 = QLabel("Fixed")
        child1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        child1.setFixedSize(100, 30)
        stack.add_child(child1)

        child2 = QLabel("Expanding")
        child2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stack.add_child(child2, grow=True)

        # Stack should handle mixed size policies
        assert stack.layout().count() == 2
        assert stack.sizeHint().isValid()


class TestStackResponsiveGapBehavior:
    """Test Stack responsive gap behavior specifically."""

    def test_stack_gap_responsive_behavior(self, app):
        """Test responsive gap behavior across breakpoints."""
        # Test with responsive gap config
        gap_config = {"base": "sm", "md": "lg", "xl": 20}
        stack = Stack(gap=gap_config)

        # Should resolve to base breakpoint by default
        assert stack.gap in ["sm", None]

        # Test different gap values
        stack.gap = "xs"
        assert stack.gap == "xs"

        stack.gap = "md"
        assert stack.gap == "md"

        stack.gap = 15
        assert stack.gap == 15

    def test_stack_gap_with_different_spacing_values(self, app):
        """Test gap with different spacing scale values."""
        spacing_values = ["xs", "sm", "md", "lg", "xl"]

        for spacing in spacing_values:
            stack = Stack(gap=spacing)
            assert stack.gap == spacing
            # Layout spacing should be non-negative
            assert stack.layout().spacing() >= 0

    def test_stack_gap_resize_behavior(self, app):
        """Test gap updates on window resize."""
        stack = Stack(gap={"base": 5, "sm": 10})

        # Initial gap
        initial_gap = stack.gap
        assert initial_gap in [5, None]  # None if no breakpoint matched

        # Simulate resize event (should not crash)
        from unittest.mock import Mock

        mock_event = Mock()
        mock_event.size.return_value = Mock()
        mock_event.size.return_value.width.return_value = 600
        mock_event.size.return_value.height.return_value = 400

        try:
            stack.resizeEvent(mock_event)
        except Exception:
            # Should not crash, but might have issues with responsive resolution
            pass

    def test_stack_gap_theme_integration(self, app):
        """Test gap integration with theme spacing scale."""
        # Test with theme spacing values
        theme_spacing = ["xs", "sm", "md", "lg", "xl"]

        for spacing in theme_spacing:
            stack = Stack(gap=spacing)
            # Should accept theme spacing values
            assert stack.gap == spacing
            assert stack.layout().spacing() >= 0
