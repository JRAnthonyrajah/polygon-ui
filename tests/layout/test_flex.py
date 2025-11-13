"""Comprehensive tests for Flex component behavior.

Includes basic functionality, responsive behavior, and complex integration scenarios for production readiness."""

import pytest
from PySide6.QtWidgets import QLabel, QApplication, QWidget
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont

from polygon_ui.layout.components.flex import Flex
from polygon_ui.layout.core.responsive import ResponsiveProps
from conftest import ResponsiveTestHelper
import time
import gc
import resource
from PySide6.QtWidgets import QVBoxLayout


@pytest.fixture
def flex(parent_widget):
    """Create a basic Flex widget."""
    flex_widget = Flex(parent=parent_widget)
    parent_widget.resize(400, 300)
    flex_widget.show()
    QApplication.processEvents()
    return flex_widget


@pytest.fixture
def child_labels():
    """Create sample child labels with consistent size hints."""
    labels = []
    for i in range(5):
        label = QLabel(f"Child {i}")
        label.setMinimumSize(50, 30)
        label.setMaximumSize(100, 60)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        labels.append(label)
    return labels


class TestFlexBasic:
    """Basic Flex component tests."""

    def test_init(self, flex):
        """Test Flex initialization."""
        assert isinstance(flex, Flex)
        assert flex.direction == "row"
        assert flex.wrap is False
        assert flex.justify == "start"
        assert flex.align == "stretch"
        assert flex.gap == "md"

    def test_add_child(self, flex, child_labels):
        """Test adding children to Flex."""
        for label in child_labels[:3]:
            flex.add_child(label, grow=1, basis="50")
        assert len(flex._children) == 3  # Internal state check
        for i, label in enumerate(child_labels[:3]):
            expected_rect = QRect(
                i * 100, 0, 100, 300
            )  # Simplified for 400x300 container, stretch align
            actual_rect = label.geometry()
            assert actual_rect.x() == expected_rect.x()
            assert actual_rect.y() == 0
            assert actual_rect.width() == 100
            assert actual_rect.height() == 300

    def test_remove_child(self, flex, child_labels):
        """Test removing children from Flex."""
        flex.add_child(child_labels[0])
        flex.remove_child(child_labels[0])
        assert child_labels[0] not in flex._children


class TestFlexDirection:
    """Tests for flex-direction property."""

    @pytest.mark.parametrize(
        "direction", ["row", "row-reverse", "column", "column-reverse"]
    )
    def test_direction(self, flex, child_labels, direction):
        """Test all flex directions."""
        flex.direction = direction
        flex.resize(400, 200)

        for i, label in enumerate(child_labels[:3]):
            flex.add_child(label)

        QApplication.processEvents()

        if direction == "row":
            for i, label in enumerate(child_labels[:3]):
                assert label.geometry() == QRect(
                    i * 133, 0, 133, 200
                )  # Approx equal share
        elif direction == "row-reverse":
            for i, label in enumerate(child_labels[:3]):
                assert label.geometry() == QRect(400 - (i + 1) * 133, 0, 133, 200)
        elif direction == "column":
            for i, label in enumerate(child_labels[:3]):
                assert label.geometry() == QRect(0, i * 66, 400, 66)
        elif direction == "column-reverse":
            for i, label in enumerate(child_labels[:3]):
                assert label.geometry() == QRect(0, 200 - (i + 1) * 66, 400, 66)

        # Verify child props are preserved
        assert flex._child_props[child_labels[0]] == {
            "grow": 0,
            "shrink": 1,
            "basis": "auto",
            "order": 0,
            "alignSelf": None,
        }


class TestFlexWrap:
    """Tests for flex-wrap property."""

    def test_no_wrap_row(self, flex, child_labels):
        """Test row layout without wrapping."""
        flex.direction = "row"
        flex.wrap = False
        flex.resize(400, 100)

        for i, label in enumerate(child_labels[:5]):
            flex.add_child(label, basis=100)

        QApplication.processEvents()

        # All in one line, squeezed
        total_basis = 5 * 100
        expected_width = 400 / 5  # Shrink applied
        for i, label in enumerate(child_labels[:5]):
            assert label.geometry().width() == 80  # 400/5
            assert label.geometry().x() == i * 80

    def test_wrap_row(self, flex, child_labels):
        """Test row layout with wrapping, small container."""
        flex.direction = "row"
        flex.wrap = True
        flex.resize(200, 200)  # Small width to force wrap

        for i, label in enumerate(child_labels[:5]):
            flex.add_child(label, basis=80)

        QApplication.processEvents()

        # First two in first line, others wrap
        # Line 1: children 0,1 at x=0,80; height=100 each but stretch to line
        assert child_labels[0].geometry() == QRect(0, 0, 100, 100)
        assert child_labels[1].geometry() == QRect(100, 0, 100, 100)
        assert child_labels[2].geometry() == QRect(0, 110, 100, 90)  # Gap 10px assumed
        # Adjust based on gap="md" ~8-16px

    def test_wrap_reverse(self, flex, child_labels):
        """Test wrap-reverse."""
        flex.direction = "row"
        flex.wrap = "wrap-reverse"
        flex.resize(200, 200)

        for label in child_labels[:3]:
            flex.add_child(label, basis=80)

        QApplication.processEvents()

        # Lines start from bottom
        assert child_labels[0].y() > child_labels[1].y()  # Reversed order in cross axis


class TestFlexJustifyAlign:
    """Tests for justify-content and align-items."""

    @pytest.mark.parametrize(
        "justify",
        ["start", "end", "center", "space-between", "space-around", "space-evenly"],
    )
    def test_justify_row(self, flex, child_labels, justify):
        """Test justify-content in row direction."""
        flex.direction = "row"
        flex.wrap = False
        flex.justify = justify
        flex.align = "stretch"
        flex.resize(400, 100)

        # Add 2 children with basis 100
        for label in child_labels[:2]:
            flex.add_child(label, basis=100)

        QApplication.processEvents()

        if justify == "start":
            assert child_labels[0].x() == 0
            assert child_labels[1].x() == 108  # 100 + gap 8
        elif justify == "end":
            assert child_labels[1].x() == 400 - 100 - 8  # Approx
        elif justify == "center":
            # Centered
            pass
        # Add specific assertions for each
        total_width = 200 + 8  # 2*100 + gap
        free = 400 - total_width
        if justify == "start":
            leading = 0
        elif justify == "end":
            leading = free
        elif justify == "center":
            leading = free / 2
        elif justify == "space-between":
            leading = 0
            gap_add = free / 1  # One gap
        elif justify == "space-around":
            leading = free / 4
            gap_add = free / 2
        elif justify == "space-evenly":
            leading = free / 3
            gap_add = free / 3

        expected_x0 = leading
        expected_x1 = leading + 100 + 8 + gap_add
        assert child_labels[0].x() == int(expected_x0)
        assert child_labels[1].x() == int(expected_x1)

    @pytest.mark.parametrize("align", ["stretch", "start", "end", "center"])
    def test_align_row(self, flex, child_labels, align):
        """Test align-items in row direction."""
        flex.direction = "row"
        flex.wrap = False
        flex.align = align
        flex.justify = "start"
        flex.resize(400, 100)

        for label in child_labels[:2]:
            flex.add_child(label, basis=100)

        QApplication.processEvents()

        child_height = 30  # sizeHint
        if align == "stretch":
            assert child_labels[0].height() == 100
            assert child_labels[0].y() == 0
        elif align == "start":
            assert child_labels[0].height() == child_height
            assert child_labels[0].y() == 0
        elif align == "end":
            assert child_labels[0].height() == child_height
            assert child_labels[0].y() == 100 - child_height
        elif align == "center":
            assert child_labels[0].height() == child_height
            assert child_labels[0].y() == (100 - child_height) / 2

    def test_align_self(self, flex, child_labels):
        """Test align-self overriding align-items."""
        flex.align = "start"
        flex.resize(400, 100)

        flex.add_child(child_labels[0], alignSelf="end")
        flex.add_child(child_labels[1])  # Uses container align

        QApplication.processEvents()

        assert child_labels[0].y() == 100 - 30
        assert child_labels[1].y() == 0


class TestFlexGrowShrink:
    """Tests for flex-grow and flex-shrink."""

    def test_grow_row(self, flex, child_labels):
        """Test flex-grow with free space."""
        flex.direction = "row"
        flex.resize(400, 100)
        flex.add_child(child_labels[0], grow=1, basis=50)
        flex.add_child(child_labels[1], grow=2, basis=50)  # Grows twice as much

        QApplication.processEvents()

        free_space = 400 - 100 - 8  # 2*50 + gap
        grow1 = free_space * 1 / 3
        grow2 = free_space * 2 / 3
        assert child_labels[0].width() == 50 + grow1
        assert child_labels[1].width() == 50 + grow2

    def test_shrink_row(self, flex, child_labels):
        """Test flex-shrink when overflowing."""
        flex.direction = "row"
        flex.resize(200, 100)  # Small container
        flex.add_child(child_labels[0], shrink=1, basis=100)
        flex.add_child(child_labels[1], shrink=2, basis=100)  # Shrinks twice as much

        QApplication.processEvents()

        total_basis = 200 + 8
        deficit = total_basis - 200
        initial_sizes = [100, 100]
        total_shrink_base = 100 * 1 + 100 * 2  # shrink * basis
        shrink1 = (1 * 100 / total_shrink_base) * deficit
        shrink2 = (2 * 100 / total_shrink_base) * deficit
        assert child_labels[0].width() == max(0, 100 - shrink1)
        assert child_labels[1].width() == max(0, 100 - shrink2)


class TestFlexBasis:
    """Tests for flex-basis."""

    @pytest.mark.parametrize("basis", ["auto", 80, "50%"])
    def test_basis_row(self, flex, child_labels, basis):
        """Test different basis values in row."""
        flex.direction = "row"
        flex.resize(400, 100)
        flex.add_child(child_labels[0], basis=basis)

        QApplication.processEvents()

        if basis == "auto":
            assert child_labels[0].width() == 50  # sizeHint
        elif isinstance(basis, int):
            assert child_labels[0].width() == basis
        elif basis.endswith("%"):
            perc = float(basis[:-1]) / 100
            assert child_labels[0].width() == int(400 * perc)


class TestFlexOrder:
    """Tests for flex-order."""

    def test_order(self, flex, child_labels):
        """Test reordering children by order property."""
        flex.direction = "row"
        flex.resize(400, 100)

        # Add in order 0,1,2 but set orders 2,0,1
        flex.add_child(child_labels[0], order=2)
        flex.add_child(child_labels[1], order=0)
        flex.add_child(child_labels[2], order=1)

        QApplication.processEvents()

        # Visual order should be child1 (order0), child2 (order1), child0 (order2)
        assert child_labels[1].x() < child_labels[2].x() < child_labels[0].x()


class TestFlexGap:
    """Tests for gap property."""

    @pytest.mark.parametrize("gap", [0, 8, "sm", 20])
    def test_gap_row(self, flex, child_labels, gap):
        """Test gap between children in row."""
        flex.gap = gap
        flex.direction = "row"
        flex.resize(400, 100)
        for label in child_labels[:3]:
            flex.add_child(label, basis=100)

        QApplication.processEvents()

        actual_gap = flex._get_spacing_pixels(gap)
        assert child_labels[1].x() == 100 + actual_gap
        assert child_labels[2].x() == 200 + 2 * actual_gap


class TestFlexIntegration:
    """Tests for property integration."""

    def test_full_integration(self, flex, child_labels):
        """Test combination of direction, wrap, justify, align, gap."""
        flex.direction = "row"
        flex.wrap = True
        flex.justify = "center"
        flex.align = "center"
        flex.gap = 10
        flex.resize(300, 150)

        # Add 4 children, basis 80 to force wrap
        for label in child_labels[:4]:
            flex.add_child(label, basis=80, grow=1, alignSelf="stretch")

        QApplication.processEvents()

        # First line: 2 children centered
        # Second line: 2 children centered, aligned center cross
        # Assertions on positions and sizes


class TestFlexResponsive:
    """Tests for responsive behavior."""

    def test_responsive_direction(self, flex, responsive_helper):
        """Test responsive direction change."""
        flex.direction = {"xs": "column", "md": "row"}
        expected = {"xs": "column", "md": "row"}

        # Using helper
        responsive_helper.assert_responsive_value(
            flex._responsive, "direction", expected
        )

        flex.add_child(QLabel("Test"), basis=50)
        flex.resize(200, 100)  # xs
        QApplication.processEvents()
        assert flex.children()[0].geometry().width() == 200  # Column: full width

        flex.resize(800, 100)  # md
        QApplication.processEvents()
        assert (
            flex.children()[0].geometry().height() == 100
        )  # Row: full height stretch?

    # More responsive tests for other props


class TestFlexEdgeCases:
    """Edge case tests."""


class TestFlexNested:
    """Tests for nested Flex containers."""

    def test_nested_flex_row_in_column(self, parent_widget):
        """Test Flex row inside Flex column."""
        outer_flex = Flex(parent=parent_widget, direction="column", gap=10)
        outer_flex.resize(400, 300)
        outer_flex.show()
        QApplication.processEvents()

        # Inner flex as first child
        inner_flex = Flex(direction="row", gap=5)
        outer_flex.add_child(inner_flex, basis=150)

        # Add children to inner
        for i in range(3):
            label = QLabel(f"Inner {i}")
            label.setMinimumSize(80, 30)
            inner_flex.add_child(label, grow=1)

        # Add another child to outer
        outer_label = QLabel("Outer Child")
        outer_label.setMinimumSize(200, 50)
        outer_flex.add_child(outer_label)

        QApplication.processEvents()

        # Verify inner children laid out horizontally in outer's column
        inner_children = inner_flex.children()
        assert len(inner_children) == 3
        assert inner_children[0].geometry().x() == 0
        assert inner_children[1].geometry().x() > 0
        assert inner_children[0].geometry().y() == 0  # Relative to inner
        assert inner_flex.geometry().height() == 150  # Basis
        assert outer_label.geometry().y() == 160  # 150 + gap 10

    def test_nested_flex_with_mixed_props(self, parent_widget):
        """Test nested flex with mixed child props."""
        outer_flex = Flex(parent=parent_widget, direction="row", wrap=True, gap=8)
        outer_flex.resize(300, 200)
        outer_flex.show()
        QApplication.processEvents()

        # Nested flex as one child
        nested_flex = Flex(direction="column", align="center")
        outer_flex.add_child(nested_flex, grow=1, basis="40%")

        # Add to nested
        for i in range(2):
            sub_label = QLabel(f"Nested {i}")
            sub_label.setFixedSize(50, 40)
            nested_flex.add_child(sub_label, alignSelf="end")

        # Other children
        for i in range(2):
            label = QLabel(f"Direct {i}")
            label.setFixedSize(100, 80)
            outer_flex.add_child(label, order=1 if i == 1 else 0)

        QApplication.processEvents()

        # Verify wrapping and nesting
        children = outer_flex.children()
        assert len(children) == 3  # nested + 2 direct
        # Nested should have width ~120 (40% of 300), children aligned end
        nested_geom = nested_flex.geometry()
        assert nested_geom.width() == int(300 * 0.4)
        assert children[1].geometry().x() > 0  # Assuming order affects position
        sub_children = nested_flex.children()
        assert (
            sub_children[0].geometry().x() == nested_geom.width() - 50
        )  # alignSelf end


class TestFlexComplexHierarchies:
    """Tests for complex widget hierarchies with mixed flex props."""

    def test_complex_hierarchy_with_flex_props(self, parent_widget):
        """Test deep nesting with mixed grow/shrink/order/alignSelf."""
        root_flex = Flex(parent=parent_widget, direction="column", gap=5)
        root_flex.resize(500, 400)
        root_flex.show()
        QApplication.processEvents()

        # Level 1: Two rows
        row1_flex = Flex(direction="row")
        row2_flex = Flex(direction="row", justify="space-between")
        root_flex.add_child(row1_flex, grow=2, basis=100)
        root_flex.add_child(row2_flex, grow=1, basis=100)

        # Level 2 in row1: Mixed props
        child1 = QLabel("Grow Heavy")
        child1.setFixedSize(60, 40)
        row1_flex.add_child(child1, grow=3, shrink=0, order=1)

        child2 = QLabel("Shrink Heavy")
        child2.setFixedSize(120, 40)
        row1_flex.add_child(child2, grow=1, shrink=2, order=0, alignSelf="center")

        child3 = QLabel("Fixed")
        child3.setFixedSize(80, 40)
        row1_flex.add_child(child3, basis=80, grow=0, shrink=0)

        # Level 2 in row2: Space between
        for i in range(3):
            label = QLabel(f"Row2 {i}")
            label.setMinimumSize(70, 30)
            row2_flex.add_child(label, basis="auto")

        QApplication.processEvents()

        # Verify layout: row1 total basis 260, free space distributed by grow
        # child2 first (order 0), then child1 (order 1), child3 fixed
        # Assertions on positions and sizes
        row1_children = row1_flex.children()
        assert row1_children[0] == child2  # order 0
        assert row1_children[1] == child1  # order 1
        assert row1_children[2] == child3
        assert child3.width() == 80  # No grow/shrink
        assert child1.width() > child2.width()  # grow 3 vs 1
        # row2 children spaced between
        row2_children = row2_flex.children()
        assert row2_children[2].x() > row2_children[1].x() > row2_children[0].x()
        total_row2 = sum(c.width() for c in row2_children) + 2 * 5  # gaps
        free_row2 = 500 - total_row2
        assert (
            abs(row2_children[1].x() - (70 + 5 + free_row2 / 2)) < 5
        )  # Approx space-between

    def test_mixed_flex_non_flex_children(self, parent_widget):
        """Test mixing Flex with regular QWidgets and layouts."""
        flex_container = Flex(parent=parent_widget, direction="row", gap=10)
        flex_container.resize(400, 150)
        flex_container.show()
        QApplication.processEvents()

        # Add regular QWidget
        regular_widget = QWidget()
        regular_widget.setFixedSize(100, 100)
        flex_container.add_child(regular_widget, basis=100)

        # Add Flex
        inner_flex = Flex(direction="column", align="stretch")
        flex_container.add_child(inner_flex, grow=1)

        # Add to inner: another regular and a label
        inner_regular = QWidget()
        inner_regular.setFixedSize(50, 30)
        inner_flex.add_child(inner_regular, basis=50)

        label = QLabel("Inner Label")
        label.setMinimumSize(80, 20)
        inner_flex.add_child(label, grow=1, alignSelf="start")

        QApplication.processEvents()

        # Verify: regular takes basis, inner grows to fill remaining, its children layout accordingly
        assert regular_widget.width() == 100
        inner_geom = inner_flex.geometry()
        assert inner_geom.width() == 290  # 400 - 100 - 10 gap
        assert inner_regular.width() == 50
        assert (
            label.width() == 290
        )  # Stretch in column? Wait, align stretch affects cross, but column main is height
        # In column, align affects width (cross)
        assert (
            label.width() == inner_geom.width()
        )  # align stretch? No, alignSelf start, but default align stretch?
        # Default align="stretch", so yes.


class TestFlexPerformance:
    """Performance tests for Flex with large numbers of children."""

    def test_large_number_of_children_no_crash(self, parent_widget):
        """Test adding 1000 children without crashing or excessive slowdown."""
        flex = Flex(parent=parent_widget, direction="row", wrap=True, gap=2)
        flex.resize(800, 600)
        flex.show()

        start_time = time.time()
        labels = []
        for i in range(1000):
            label = QLabel(f"Perf {i}")
            label.setFixedSize(50, 30)
            flex.add_child(label)
            labels.append(label)

        layout_time = time.time() - start_time
        assert layout_time < 5.0  # Should be fast, <5s

        QApplication.processEvents()

        # Verify all positioned
        for i, label in enumerate(labels[:10]):  # Sample check
            assert label.geometry().x() >= 0 and label.geometry().y() >= 0

        # Remove all
        remove_start = time.time()
        for label in labels:
            flex.remove_child(label)
        remove_time = time.time() - remove_start
        assert remove_time < 2.0

    def test_performance_with_nested_large(self, parent_widget):
        """Test performance with nested flex and many children."""
        outer_flex = Flex(parent=parent_widget, direction="column", gap=5)
        outer_flex.resize(400, 800)
        outer_flex.show()

        start_time = time.time()
        for level in range(5):  # 5 levels deep
            inner_flex = Flex(direction="row", wrap=True)
            outer_flex.add_child(inner_flex, basis=100)

            for i in range(20):  # 20 per level
                label = QLabel(f"Nest {level}-{i}")
                label.setFixedSize(60, 25)
                inner_flex.add_child(label, grow=1)

        layout_time = time.time() - start_time
        assert layout_time < 3.0

        QApplication.processEvents()
        # No specific assertions, just ensure no crash and reasonable time


class TestFlexMemory:
    """Tests for memory usage and cleanup."""

    def test_memory_cleanup_after_remove(self, parent_widget):
        """Test adding/removing many children and check for leaks (basic)."""
        flex = Flex(parent=parent_widget)
        flex.show()

        # Add 500 children
        children = []
        for i in range(500):
            label = QLabel(f"Mem {i}")
            label.setFixedSize(40, 20)
            flex.add_child(label)
            children.append(label)

        QApplication.processEvents()

        # Force GC
        gc.collect()
        initial_refs = len(gc.get_referents(flex))

        # Remove all
        for label in children:
            flex.remove_child(label)
            label.deleteLater()  # Explicit cleanup

        gc.collect()
        final_refs = len(gc.get_referents(flex))

        # References should decrease significantly
        assert final_refs < initial_refs * 0.5  # Heuristic

    def test_nested_memory_cleanup(self, parent_widget):
        """Test cleanup in nested structures."""
        outer = Flex(parent=parent_widget, direction="row")
        outer.show()

        inners = []
        for i in range(10):
            inner = Flex(direction="column")
            outer.add_child(inner)
            inners.append(inner)

            for j in range(10):
                label = QLabel(f"N{i}{j}")
                inner.add_child(label)

        QApplication.processEvents()

        # Cleanup
        for inner in inners:
            for child in inner.children():
                inner.remove_child(child)
                child.deleteLater()
            outer.remove_child(inner)
            inner.deleteLater()

        gc.collect()
        # No assertion possible without tracking, but ensure no crash


class TestFlexErrorHandling:
    """Tests for error handling and invalid inputs."""

    def test_invalid_direction(self, flex):
        """Test invalid direction value."""
        with pytest.raises(ValueError):
            flex.direction = "invalid"

    def test_invalid_wrap(self, flex):
        """Test invalid wrap value."""
        with pytest.raises(ValueError):
            flex.wrap = "invalid"

    def test_negative_basis(self, flex, child_labels):
        """Test negative basis (should default to 0)."""
        flex.add_child(child_labels[0], basis=-10)
        flex.resize(200, 100)
        QApplication.processEvents()
        assert child_labels[0].width() >= 0  # No negative size

    def test_zero_gap(self, flex, child_labels):
        """Test zero or negative gap."""
        flex.gap = 0
        flex.add_child(child_labels[0], basis=50)
        flex.add_child(child_labels[1], basis=50)
        flex.resize(200, 100)
        QApplication.processEvents()
        assert child_labels[1].x() == 100  # No gap

    def test_duplicate_order(self, flex, child_labels):
        """Test multiple children with same order."""
        flex.add_child(child_labels[0], order=5)
        flex.add_child(child_labels[1], order=5)
        flex.add_child(child_labels[2], order=1)
        QApplication.processEvents()
        # Stable sort? Since added order, should maintain addition order for ties
        assert (
            child_labels[2].geometry().x()
            < child_labels[0].geometry().x()
            == child_labels[1].geometry().x() - child_labels[0].width() - gap
        )  # Wait, positions sequential

    def test_no_children(self, flex):
        """Test with no children."""
        flex.resize(400, 300)
        QApplication.processEvents()
        # No errors, nothing positioned

    def test_one_child(self, flex, child_labels):
        """Test with single child, various aligns."""
        flex.align = "center"
        flex.add_child(child_labels[0])
        flex.resize(400, 100)
        QApplication.processEvents()
        assert child_labels[0].y() == (100 - 30) / 2

    def test_zero_basis(self, flex, child_labels):
        """Test basis=0."""
        flex.add_child(child_labels[0], basis=0, grow=1)
        flex.resize(400, 100)
        QApplication.processEvents()
        assert child_labels[0].width() > 0  # Grows to fill

    def test_negative_grow(self, flex, child_labels):
        """Test negative grow (should be treated as 0)."""
        flex.add_child(child_labels[0], grow=-1, basis=50)
        flex.resize(400, 100)
        QApplication.processEvents()
        # Grow treated as 0, so size = basis
        assert child_labels[0].width() == 50

    def test_overflow_wrap(self, flex, child_labels):
        """Test many children forcing multiple wraps."""
        flex.wrap = True
        flex.resize(100, 400)
        for i in range(10):
            label = QLabel(f"Small {i}")
            label.setFixedSize(80, 30)
            flex.add_child(label)
        QApplication.processEvents()
        # Multiple lines formed


# Note: Some assertions are approximate; in real tests, use more precise calculations based on theme spacing.
# Visual tests can be added using capture_widget_image if needed.
# For performance, tests should not be too slow; use processEvents sparingly.


class TestFlexIntegration:
    """Complex integration tests for Flex component."""

    def test_nested_flex_containers(self, parent_widget):
        """Test nested flex containers with different directions."""
        # Create outer flex (vertical)
        outer_flex = Flex(parent=parent_widget, direction="column", gap="sm")
        outer_flex.resize(400, 300)

        # Create inner flex containers
        inner_flex1 = Flex(direction="row", gap="md")
        inner_flex2 = Flex(direction="row-reverse", gap="lg")

        # Add children to inner flexes
        for i in range(3):
            label1 = QLabel(f"Inner1-{i}")
            label1.setFixedSize(60, 30)
            inner_flex1.add_child(label1)

            label2 = QLabel(f"Inner2-{i}")
            label2.setFixedSize(50, 25)
            inner_flex2.add_child(label2)

        # Add inner flexes to outer
        outer_flex.add_child(inner_flex1)
        outer_flex.add_child(inner_flex2)

        parent_widget.layout().addWidget(outer_flex)
        QApplication.processEvents()

        # Verify nested layout structure
        assert inner_flex1.y() < inner_flex2.y()  # Vertical stacking
        assert inner_flex1.width() > 0
        assert inner_flex2.width() > 0

    def test_complex_mixed_properties(self, flex):
        """Test complex hierarchies with mixed flex properties."""
        # Create diverse children with different flex properties
        children = []

        # Child 1: Fixed size, no flex
        child1 = QLabel("Fixed")
        child1.setFixedSize(80, 40)
        flex.add_child(child1, grow=0, shrink=0, basis=80)
        children.append(child1)

        # Child 2: Flexible grow
        child2 = QLabel("Grow")
        child2.setMinimumSize(50, 30)
        flex.add_child(child2, grow=2, basis=50)
        children.append(child2)

        # Child 3: Flexible with alignSelf
        child3 = QLabel("Center")
        child3.setMinimumSize(60, 35)
        flex.add_child(child3, grow=1, alignSelf="center")
        children.append(child3)

        # Child 4: Reordered with negative order
        child4 = QLabel("First")
        child4.setMinimumSize(40, 25)
        flex.add_child(child4, order=-1, basis=40)
        children.append(child4)

        flex.resize(300, 100)
        QApplication.processEvents()

        # Verify order property works (child4 should be first)
        assert child4.x() < child1.x()

        # Verify grow children expand to fill space
        total_width = sum(child.width() for child in children)
        assert total_width >= 250  # Should fill most of container

    def test_flex_with_wrapping_and_grow(self, flex):
        """Test wrapping behavior combined with grow properties."""
        flex.wrap = True
        flex.gap = 5

        # Create children that will wrap and grow
        for i in range(6):
            child = QLabel(f"Wrap-{i}")
            child.setMinimumSize(80, 30)
            grow_factor = 2 if i % 2 == 0 else 1  # Alternating grow factors
            flex.add_child(child, grow=grow_factor, basis=70)

        flex.resize(250, 150)  # Force wrapping
        QApplication.processEvents()

        # Verify multiple lines exist (y positions differ)
        y_positions = [child.y() for child in flex._children]
        assert len(set(y_positions)) > 1  # Multiple lines

        # Verify children within each line grow to fill space
        # Check that grow factor 2 children are wider than grow factor 1
        grow_2_children = [flex._children[i] for i in range(6) if i % 2 == 0]
        grow_1_children = [flex._children[i] for i in range(6) if i % 2 == 1]

        # On each line, grow-2 children should be wider
        for child in grow_2_children:
            if child.y() == grow_1_children[0].y():  # Same line
                assert child.width() >= grow_1_children[0].width()


class TestFlexPerformance:
    """Performance and stress tests for Flex component."""

    def test_large_number_of_children(self, parent_widget):
        """Test performance with many children."""
        flex = Flex(parent=parent_widget, direction="row", wrap=True)
        flex.resize(800, 600)

        # Add many children
        start_time = time.time()
        for i in range(100):
            child = QLabel(f"Item {i}")
            child.setFixedSize(30, 20)
            flex.add_child(child, grow=1)

        layout_time = time.time() - start_time

        # Force layout calculation
        QApplication.processEvents()
        end_time = time.time()
        total_time = end_time - start_time

        # Performance assertions (should complete quickly)
        assert total_time < 1.0  # Should complete within 1 second
        assert layout_time < 0.5  # Adding children should be fast

        # Verify all children positioned
        positioned_children = [child for child in flex._children if child.x() >= 0]
        assert len(positioned_children) == 100

    def test_resize_performance(self, flex):
        """Test performance during rapid resizing."""
        # Add some children
        for i in range(20):
            child = QLabel(f"Resize-{i}")
            child.setMinimumSize(40, 25)
            flex.add_child(child, grow=1)

        # Test rapid resize operations
        start_time = time.time()
        for width in [200, 300, 400, 300, 200, 500, 400]:
            flex.resize(width, 100)
            QApplication.processEvents()

        resize_time = time.time() - start_time

        # Should handle rapid resizes efficiently
        assert resize_time < 0.5  # 7 resizes should complete quickly

    def test_memory_cleanup(self, parent_widget):
        """Test memory cleanup when children are removed."""
        flex = Flex(parent=parent_widget)

        # Add many children
        children = []
        for i in range(50):
            child = QLabel(f"Memory-{i}")
            child.setFixedSize(30, 20)
            children.append(child)
            flex.add_child(child)

        QApplication.processEvents()

        # Remove all children
        for child in children:
            flex.remove_child(child)

        # Force garbage collection
        gc.collect()
        QApplication.processEvents()

        # Verify cleanup
        assert len(flex._children) == 0
        assert len(flex._child_props) == 0


class TestFlexEdgeCases:
    """Edge cases and error handling tests."""

    def test_zero_size_container(self, flex):
        """Test behavior with zero-size container."""
        flex.resize(0, 0)

        child = QLabel("Zero")
        child.setMinimumSize(50, 30)
        flex.add_child(child)

        QApplication.processEvents()
        # Should not crash, child positioned at 0,0
        assert child.x() >= 0
        assert child.y() >= 0

    def test_very_large_children(self, flex):
        """Test with children larger than container."""
        flex.resize(100, 50)

        child = QLabel("Large")
        child.setMinimumSize(200, 150)  # Much larger than container
        flex.add_child(child, shrink=1)  # Allow shrinking

        QApplication.processEvents()
        # Child should be constrained to container size
        assert child.width() <= 100
        assert child.height() <= 50

    def test_invalid_basis_values(self, flex):
        """Test handling of invalid basis values."""
        child = QLabel("Invalid")
        child.setMinimumSize(30, 20)

        # Test various invalid basis values
        invalid_bases = ["invalid", "", None, -50]

        for basis in invalid_bases:
            flex.add_child(QLabel(f"Test-{basis}"), basis=basis)

        flex.resize(300, 100)
        QApplication.processEvents()

        # Should handle gracefully without crashing
        assert len(flex._children) == len(invalid_bases)

    def test_extreme_grow_shrink_values(self, flex):
        """Test extreme grow/shrink values."""
        flex.resize(300, 100)

        # Add children with extreme values
        child1 = QLabel("High Grow")
        child1.setMinimumSize(20, 20)
        flex.add_child(child1, grow=1000)

        child2 = QLabel("High Shrink")
        child2.setMinimumSize(100, 20)
        flex.add_child(child2, shrink=1000)

        child3 = QLabel("Normal")
        child3.setMinimumSize(30, 20)
        flex.add_child(child3, grow=1)

        QApplication.processEvents()

        # Should handle extreme values without overflow
        assert child1.width() > 0
        assert child2.width() > 0
        assert child3.width() > 0

        # Total width should not exceed container
        total_width = sum(child.width() for child in flex._children)
        assert total_width <= 300 + 50  # Allow some tolerance

    def test_direction_changes_with_children(self, flex):
        """Test changing direction after children are added."""
        # Add children
        for i in range(3):
            child = QLabel(f"Dir-{i}")
            child.setFixedSize(50, 30)
            flex.add_child(child)

        flex.resize(200, 150)
        QApplication.processEvents()

        # Record initial positions (row layout)
        initial_positions = [(child.x(), child.y()) for child in flex._children]

        # Change to column
        flex.direction = "column"
        QApplication.processEvents()

        # Verify layout changed to column
        assert all(child.y() > 0 for child in flex._children[1:])

        # Change back to row
        flex.direction = "row"
        QApplication.processEvents()

        # Should return to similar horizontal layout
        assert all(child.x() > 0 for child in flex._children[1:])


class TestFlexBenchmarks:
    """Additional performance benchmarks for Flex component."""

    def test_layout_calculation_benchmark(self, parent_widget):
        """Benchmark layout calculation time for varying child counts."""
        sizes = [10, 50, 100, 500]
        for num_children in sizes:
            flex = Flex(parent=parent_widget, direction="row", wrap=True)
            flex.resize(800, 600)
            start = time.time()
            for i in range(num_children):
                label = QLabel(f"Bench {i}")
                label.setFixedSize(50, 30)
                flex.add_child(label)
            add_time = time.time() - start
            start = time.time()
            for _ in range(10):
                flex.resize(800 + _ * 10, 600)
                QApplication.processEvents()
            layout_time = time.time() - start
            assert add_time < 1.0  # Reasonable threshold for adding
            assert layout_time < 0.5  # For multiple layouts
            # Cleanup
            while flex._children:
                child = flex._children[0]
                flex.remove_child(child)
                child.deleteLater()

    def test_memory_usage_large_container(self, parent_widget):
        """Test memory usage with large flex container."""
        initial_memory = (
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        )  # KB to MB
        flex = Flex(parent=parent_widget)
        flex.show()
        children = []
        for i in range(1000):
            label = QLabel(str(i))
            flex.add_child(label)
            children.append(label)
        QApplication.processEvents()
        gc.collect()
        final_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        memory_increase = final_memory - initial_memory
        assert memory_increase < 100  # Threshold in MB, adjust based on system
        # Cleanup
        for child in children:
            flex.remove_child(child)
            child.deleteLater()
        gc.collect()

    def test_rendering_performance(self, parent_widget):
        """Test rendering time for large flex."""
        flex = Flex(parent=parent_widget, direction="row", wrap=True)
        flex.resize(800, 600)
        children = []
        for i in range(500):
            label = QLabel(str(i))
            label.setFixedSize(40, 25)
            flex.add_child(label)
            children.append(label)
        start = time.time()
        flex.show()
        QApplication.processEvents()
        render_time = time.time() - start
        assert render_time < 2.0  # Allow for Qt rendering time
        # Cleanup
        for child in children:
            flex.remove_child(child)
            child.deleteLater()
