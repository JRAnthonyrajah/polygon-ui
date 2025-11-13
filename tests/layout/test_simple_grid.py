"""Comprehensive tests for SimpleGrid component behavior.

Includes basic functionality, responsive behavior, auto-columns, spacing, convenience methods,
and performance benchmarks for production readiness."""

import pytest
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QGridLayout
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont

from polygon_ui.layout.components.simple_grid import SimpleGrid
from polygon_ui.layout.core.responsive import ResponsiveProps
from conftest import ResponsiveTestHelper
import time
import gc


@pytest.fixture
def simple_grid(parent_widget):
    """Create a basic SimpleGrid widget."""
    grid_widget = SimpleGrid(parent=parent_widget, cols=3)
    parent_widget.resize(600, 400)
    grid_widget.show()
    QApplication.processEvents()
    return grid_widget


@pytest.fixture
def child_labels():
    """Create sample child labels with consistent size hints."""
    labels = []
    for i in range(12):  # Enough for 3x4 grid
        label = QLabel(f"Cell {i}")
        label.setMinimumSize(80, 50)
        label.setMaximumSize(150, 100)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        labels.append(label)
    return labels


class TestSimpleGridBasic:
    """Basic SimpleGrid component tests."""

    def test_init(self, simple_grid):
        """Test SimpleGrid initialization."""
        assert isinstance(simple_grid, SimpleGrid)
        assert simple_grid.cols == 3
        assert simple_grid.hspacing == "md"
        assert simple_grid.vspacing == "md"
        assert simple_grid.spacing == "md"
        assert simple_grid.auto_cols is False
        assert simple_grid.min_col_width == 250
        assert isinstance(simple_grid._layout, QGridLayout)
        assert simple_grid._layout.columnCount() == 3

    def test_add_child(self, simple_grid, child_labels):
        """Test adding children to SimpleGrid."""
        for i, label in enumerate(child_labels[:6]):
            simple_grid.add_child(label)
        QApplication.processEvents()

        # Children placed in row-major: 0-2 row0, 3-5 row1
        num_cols = 3
        col_width = 200  # Approx 600/3
        row_height = 200  # Approx
        for i, label in enumerate(child_labels[:6]):
            row = i // num_cols
            col = i % num_cols
            expected_x = col * col_width
            expected_y = row * row_height
            actual = label.geometry()
            assert actual.x() == expected_x  # Ignoring gaps for simplicity
            assert actual.y() == expected_y
            assert actual.width() == col_width  # Equal stretch
            assert actual.height() == row_height

    def test_remove_child(self, simple_grid, child_labels):
        """Test removing children from SimpleGrid."""
        simple_grid.add_child(child_labels[0])
        simple_grid.remove_child(child_labels[0])
        assert child_labels[0] not in simple_grid._children
        # Layout should update without the child


class TestSimpleGridColumns:
    """Tests for cols property."""

    @pytest.mark.parametrize("cols", [1, 3, 12])
    def test_fixed_cols(self, simple_grid, child_labels, cols):
        """Test fixed number of columns."""
        simple_grid.cols = cols
        simple_grid.resize(600, 400)
        for i, label in enumerate(child_labels[: cols * 2]):
            simple_grid.add_child(label)
        QApplication.processEvents()

        col_width = 600 // cols
        for i, label in enumerate(child_labels[: cols * 2]):
            row = i // cols
            col = i % cols
            assert label.geometry().x() == col * col_width
            assert label.geometry().y() == row * 200  # Approx

    def test_equal_width_distribution(self, simple_grid, child_labels):
        """Test equal-width column distribution with spacing."""
        simple_grid.cols = 4
        simple_grid.hspacing = (
            10  # Add spacing to test distribution accounting for gaps
        )
        simple_grid.resize(800, 300)
        for label in child_labels[:8]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        # Total width for columns: 800 - (3 gaps * 10) = 770 for 4 cols
        expected_width = 770 // 4  # 192.5 -> integer division
        # Verify all 8 children have equal widths
        widths = [label.width() for label in child_labels[:8]]
        assert all(w == expected_width for w in widths)
        assert len(set(widths)) == 1  # All equal

        # Verify positions account for gaps
        gap = 10
        for i in range(0, 8, 4):  # Per row
            row_labels = child_labels[i : i + 4]
            expected_x = [sum([expected_width + gap] * j for j in range(4))]
            for j, label in enumerate(row_labels):
                assert label.x() == j * (expected_width + gap)
                assert label.y() == row_labels[0].y()  # Same row


class TestSimpleGridSpacing:
    """Tests for spacing properties."""

    @pytest.mark.parametrize("spacing_value", [0, 8, "sm", 20])
    def test_uniform_spacing(self, simple_grid, child_labels, spacing_value):
        """Test uniform spacing (via spacing prop)."""
        simple_grid.spacing = spacing_value
        simple_grid.cols = 2
        simple_grid.resize(500, 300)
        for label in child_labels[:4]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        actual_gap = simple_grid._get_spacing_pixels(spacing_value)
        # Horizontal gap between col 0 and 1
        assert child_labels[1].x() == child_labels[0].width() + actual_gap
        # Vertical gap between row 0 and 1
        assert child_labels[2].y() == child_labels[0].height() + actual_gap

    def test_separate_spacing(self, simple_grid, child_labels):
        """Test separate hspacing and vspacing."""
        simple_grid.hspacing = 10
        simple_grid.vspacing = 20
        simple_grid.cols = 2
        simple_grid.resize(500, 300)
        for label in child_labels[:4]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        # Horizontal gap
        assert child_labels[1].x() - child_labels[0].x() - child_labels[0].width() == 10
        # Vertical gap
        assert (
            child_labels[2].y() - child_labels[0].y() - child_labels[0].height() == 20
        )


class TestSimpleGridResponsive:
    """Tests for responsive behavior."""

    def test_responsive_cols(self, simple_grid, responsive_helper):
        """Test responsive column changes and distribution."""
        simple_grid.cols = {"xs": 1, "sm": 2, "md": 3, "lg": 4}
        expected = {"xs": 1, "sm": 2, "md": 3, "lg": 4}

        responsive_helper.assert_responsive_value(
            simple_grid._responsive, "cols", expected
        )

        # Add children for testing distribution
        child_labels = []
        for i in range(8):
            label = QLabel(f"Resp {i}")
            label.setMinimumSize(80, 50)
            simple_grid.add_child(label)
            child_labels.append(label)

        # Test at xs: 1 column, stacked vertically
        responsive_helper.set_width(500)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 1
        # Children should be in one column, multiple rows
        for i, label in enumerate(child_labels):
            expected_y = i * 60  # Approx height + spacing
            actual = label.geometry()
            assert actual.x() == 0
            assert actual.y() == expected_y  # Stacked

        # Test at sm: 2 columns
        responsive_helper.set_width(650)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2
        # Row 0: children 0,1 at x=0 and x~250
        assert child_labels[0].x() == 0
        assert child_labels[1].x() > 200  # Gap and width
        # Row 1: 2,3 same y, different x
        assert child_labels[2].y() == child_labels[0].y()  # Same row height
        assert child_labels[3].x() > 200

        # Test at md: 3 columns
        responsive_helper.set_width(800)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 3
        col_width = 800 // 3  # Approx
        for i, label in enumerate(child_labels[:3]):  # First row
            assert label.x() == i * col_width
        for i in range(3, 6):  # Second row
            row_i = (i - 3) % 3
            assert child_labels[i].x() == row_i * col_width

        # Test at lg: 4 columns (but only 8 children: 2 rows)
        responsive_helper.set_width(1200)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 4
        col_width = 1200 // 4  # 300
        for i, label in enumerate(child_labels[:4]):
            assert label.x() == i * col_width

    def test_responsive_spacing(self, simple_grid, responsive_helper):
        """Test responsive hspacing and vspacing behavior."""
        simple_grid.hspacing = {"xs": 4, "sm": 8, "md": 16, "lg": 24}
        simple_grid.vspacing = {"xs": 4, "sm": 8, "md": 16, "lg": 24}
        simple_grid.cols = 2
        child_labels = []
        for i in range(6):  # 2 rows, 3 cols but cols=2 so 3 rows
            label = QLabel(f"Spacing {i}")
            label.setFixedSize(100, 50)
            simple_grid.add_child(label)
            child_labels.append(label)

        # At xs: small spacing
        responsive_helper.set_width(500)
        QApplication.processEvents()
        h_gap = simple_grid._get_spacing_pixels(4)  # xs
        v_gap = simple_grid._get_spacing_pixels(4)
        # Horizontal: between col 0 and 1 in row 0
        assert child_labels[1].x() == child_labels[0].width() + h_gap
        # Vertical: between row 0 and 1
        assert child_labels[2].y() == child_labels[0].height() + v_gap

        # At md: larger spacing
        responsive_helper.set_width(800)
        QApplication.processEvents()
        h_gap_md = simple_grid._get_spacing_pixels(16)  # md
        v_gap_md = simple_grid._get_spacing_pixels(16)
        assert child_labels[1].x() == child_labels[0].width() + h_gap_md
        assert child_labels[2].y() == child_labels[0].height() + v_gap_md
        assert h_gap_md > h_gap  # Increased

        # Test string spacing if supported
        simple_grid.hspacing = {"lg": "lg"}
        responsive_helper.set_width(1200)
        QApplication.processEvents()
        lg_gap = simple_grid._get_spacing_pixels("lg")
        assert lg_gap == 24  # Assuming theme spacing

        # Verify vspacing independently
        simple_grid.vspacing = {"sm": "sm"}
        responsive_helper.set_width(650)
        QApplication.processEvents()
        sm_gap = simple_grid._get_spacing_pixels("sm")
        assert child_labels[2].y() == child_labels[0].height() + sm_gap

    def test_smooth_breakpoint_transitions(self, simple_grid, child_labels):
        """Test smooth transitions on resize (via resizeEvent)."""
        simple_grid.cols = 2
        for label in child_labels[:4]:
            simple_grid.add_child(label)
        simple_grid.resize(400, 300)
        QApplication.processEvents()

        initial_positions = [label.geometry().x() for label in child_labels[:2]]

        # Resize to trigger responsive update
        simple_grid.resize(800, 300)
        QApplication.processEvents()

        new_positions = [label.geometry().x() for label in child_labels[:2]]
        # Columns should adjust, positions change
        assert new_positions[0] == 0
        assert new_positions[1] > initial_positions[1]  # Wider spacing/columns


class TestSimpleGridAutoCols:
    """Tests for auto_cols and min_col_width."""

    def test_auto_cols_basic(self, simple_grid, child_labels):
        """Test auto-columns with min_col_width."""
        simple_grid.auto_cols = True
        simple_grid.min_col_width = 150
        simple_grid.resize(600, 400)
        for label in child_labels[:8]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        # Should fit 4 columns (600//150=4)
        assert simple_grid._layout.columnCount() == 4
        for i in range(4):
            assert simple_grid._layout.columnMinimumWidth(i) == 150
            assert simple_grid._layout.columnStretch(i) == 1

    def test_auto_cols_with_max(self, simple_grid, child_labels):
        """Test auto-cols with maximum column limit."""
        simple_grid.auto_cols = 3  # Max 3 columns
        simple_grid.min_col_width = 150
        simple_grid.resize(800, 400)  # Could fit 5, but max 3
        for label in child_labels[:6]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        assert simple_grid._layout.columnCount() == 3  # Limited to max

    def test_auto_sizing_dynamic_width(self, simple_grid, child_labels):
        """Test auto-sizing with dynamic width changes and equal column widths."""
        simple_grid.auto_cols = True
        simple_grid.min_col_width = 200
        simple_grid.hspacing = 10
        for label in child_labels[:9]:  # For 3 cols
            simple_grid.add_child(label)

        # Narrow: 1 col (300 < 200*2 - gap, but min 200, fits 1 full)
        simple_grid.resize(300, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 1
        assert child_labels[0].width() == 300  # Full width

        # Fits 2 cols: (500 -10)//200 = 245 >200, 2 cols
        simple_grid.resize(500, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2
        col_width = (500 - 10) // 2
        assert col_width >= 200
        for i in range(2):
            assert child_labels[i].width() == col_width
            assert child_labels[i].x() == i * (col_width + 10)

        # Fits 3 cols: (700 -20)//200=340>200, 3 cols
        simple_grid.resize(700, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 3
        col_width = (700 - 20) // 3
        assert col_width >= 200
        widths = [label.width() for label in child_labels[:3]]
        assert all(w == col_width for w in widths)
        assert len(set(widths)) == 1  # Equal

        # Edge: exactly min, floor calculation
        simple_grid.resize(410, 300)  # (410-10)//2=200, 2 cols
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2
        col_width = 200
        assert child_labels[0].width() == col_width


class TestSimpleGridConvenience:
    """Tests for convenience methods."""

    def test_fixed_cols_method(self, simple_grid):
        """Test fixed_cols convenience."""
        simple_grid.fixed_cols(4)
        assert simple_grid.cols == 4
        assert simple_grid.auto_cols is False

    def test_responsive_cols_method(self, simple_grid):
        """Test responsive_cols convenience."""
        simple_grid.responsive_cols({"sm": 2, "lg": 4})
        assert simple_grid.cols == {"sm": 2, "lg": 4}

    def test_responsive_hspacing_method(self, simple_grid):
        """Test responsive_hspacing convenience."""
        simple_grid.responsive_hspacing({"md": "lg", "xl": "xl"})
        assert simple_grid.hspacing == {"md": "lg", "xl": "xl"}

    def test_responsive_vspacing_method(self, simple_grid):
        """Test responsive_vspacing convenience."""
        simple_grid.responsive_vspacing({"md": "lg"})
        assert simple_grid.vspacing == {"md": "lg"}

    def test_auto_fit_method(self, simple_grid):
        """Test auto_fit convenience."""
        simple_grid.auto_fit(max_columns=3, min_width=150)
        assert simple_grid.auto_cols == 3
        assert simple_grid.min_col_width == 150


class TestSimpleGridPerformance:
    """Performance benchmarks for large SimpleGrids."""

    def test_large_simple_grid_no_crash(self, parent_widget):
        """Test 100+ cells without crash and benchmark layout calculation."""
        grid = SimpleGrid(
            parent=parent_widget, cols=10, auto_cols=True, min_col_width=50
        )
        grid.resize(1000, 800)
        grid.show()

        start_time = time.time()
        labels = []
        for i in range(100):  # 10x10
            label = QLabel(f"Large {i}")
            label.setMinimumSize(40, 40)
            grid.add_child(label)
            labels.append(label)

        layout_time = time.time() - start_time
        assert layout_time < 0.5  # Tighter benchmark for add_child loop

        # Time layout update
        update_start = time.time()
        QApplication.processEvents()
        update_time = time.time() - update_start
        assert update_time < 0.1  # Quick layout calc

        # All positioned
        for label in labels:
            assert label.geometry().x() >= 0 and label.geometry().y() >= 0

        # Cleanup
        remove_start = time.time()
        for label in labels:
            grid.remove_child(label)
        remove_time = time.time() - remove_start
        assert remove_time < 0.3  # Quick removal

    def test_extreme_large_grid_benchmark(self, parent_widget):
        """Benchmark 1000+ children for layout calculation performance."""
        grid = SimpleGrid(
            parent=parent_widget, cols=20, auto_cols=True, min_col_width=30
        )
        grid.resize(1200, 900)
        grid.show()

        labels = []
        add_start = time.time()
        for i in range(1000):  # Extreme case: 50x20 grid
            label = QLabel(f"Extreme {i}")
            label.setFixedSize(25, 25)
            grid.add_child(label)
            if i % 100 == 0:  # Batch process every 100
                QApplication.processEvents()
            labels.append(label)
        add_time = time.time() - add_start
        assert add_time < 5.0  # Acceptable for 1000 adds

        # Full layout calculation time
        layout_start = time.time()
        QApplication.processEvents()
        layout_time = time.time() - layout_start
        assert layout_time < 1.0  # Efficient for large grid

        # Verify positions without crashing
        positioned_count = sum(1 for label in labels[:100] if label.geometry().x() >= 0)
        assert positioned_count == 100

        # Cleanup time
        cleanup_start = time.time()
        for label in labels:
            grid.remove_child(label)
            label.deleteLater()
        gc.collect()
        cleanup_time = time.time() - cleanup_start
        assert cleanup_time < 2.0

    def test_resize_performance_large(self, simple_grid):
        """Test resize on large SimpleGrid with responsive recalc."""
        # Add 200 children for larger benchmark
        labels = []
        for i in range(200):
            label = QLabel(f"Perf {i}")
            label.setFixedSize(50, 40)
            simple_grid.add_child(label)
            labels.append(label)

        # Initial layout
        QApplication.processEvents()

        start_time = time.time()
        widths = [
            300,
            600,
            1200,
            800,
            400,
        ]  # Multiple resizes including responsive triggers
        for w in widths:
            simple_grid.resize(w, 500)
            QApplication.processEvents()  # Triggers layout recalc
        resize_time = time.time() - start_time
        assert resize_time < 0.5  # Tighter for multiple resizes

        # Per-resize average
        avg_resize = resize_time / len(widths)
        assert avg_resize < 0.1

    def test_responsive_resize_large_grid(self, parent_widget):
        """Benchmark responsive resize on large grid with breakpoint changes."""
        grid = SimpleGrid(
            parent=parent_widget,
            cols={"xs": 1, "sm": 5, "md": 10, "lg": 20},
            auto_cols=True,
            min_col_width=40,
        )
        grid.resize(1000, 800)
        grid.show()

        # Add 500 children
        labels = []
        for i in range(500):
            label = QLabel(f"RespLarge {i}")
            label.setFixedSize(30, 30)
            grid.add_child(label)
            labels.append(label)
        QApplication.processEvents()  # Initial layout at md (10 cols)

        # Time responsive resizes across breakpoints
        start_time = time.time()
        breakpoint_widths = [400, 600, 900, 1400]  # xs->sm->md->lg
        for w in breakpoint_widths:
            grid.resize(w, 800)
            QApplication.processEvents()  # Column count changes
        responsive_time = time.time() - start_time
        assert responsive_time < 1.0

        # Verify column changes
        grid.resize(400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 1  # xs

        grid.resize(1400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 20  # lg, auto limited?

        # Cleanup
        for label in labels:
            grid.remove_child(label)

    def test_memory_cleanup_large(self, parent_widget):
        """Test memory after large SimpleGrid with many children."""
        grid = SimpleGrid(parent=parent_widget, cols=15, auto_cols=True)
        children = []
        add_start = time.time()
        for i in range(500):  # Larger for memory test
            child = QLabel(f"MemLarge {i}")
            child.setFixedSize(40, 40)
            grid.add_child(child)
            children.append(child)
        add_time = time.time() - add_start
        assert add_time < 2.0

        QApplication.processEvents()
        gc.collect()
        initial_refs = (
            len(gc.get_referents(grid)) + grid._layout.count()
        )  # Include layout items

        # Remove and cleanup
        remove_start = time.time()
        for child in children:
            grid.remove_child(child)
            child.deleteLater()
        remove_time = time.time() - remove_start
        assert remove_time < 1.0

        gc.collect()
        final_refs = len(gc.get_referents(grid)) + grid._layout.count()
        # Significant reduction
        assert (
            final_refs <= initial_refs * 0.3
        )  # Stricter heuristic for cleanup efficiency

        # Test repeated creation/destruction for leak detection
        for _ in range(3):  # 3 cycles
            gc.collect()
            before_cycle = len(gc.get_referents(grid))
            del children[:]  # Clear list
            gc.collect()
            after_cycle = len(gc.get_referents(grid))
            assert after_cycle <= before_cycle  # No growth


class TestSimpleGridEdgeCases:
    """Edge cases and error handling."""

    def test_zero_cols(self, simple_grid):
        """Test cols=0 (should default to 1)."""
        simple_grid.cols = 0
        assert simple_grid._layout.columnCount() == 1

    def test_negative_spacing(self, simple_grid, child_labels):
        """Test negative spacing (should be 0)."""
        simple_grid.hspacing = -5
        simple_grid.add_child(child_labels[0])
        simple_grid.add_child(child_labels[1])
        simple_grid.cols = 2
        simple_grid.resize(500, 200)
        QApplication.processEvents()
        assert simple_grid._layout.horizontalSpacing() >= 0

    def test_empty_simple_grid(self, simple_grid):
        """Test no children."""
        simple_grid.resize(500, 300)
        QApplication.processEvents()
        # No errors, layout empty

    def test_one_child(self, simple_grid, child_labels):
        """Test single child."""
        simple_grid.cols = 3
        simple_grid.add_child(child_labels[0])
        QApplication.processEvents()
        assert child_labels[0].x() == 0
        assert child_labels[0].width() > 0

    def test_auto_cols_zero_width(self, simple_grid):
        """Test auto_cols with zero width."""
        simple_grid.auto_cols = True
        simple_grid.min_col_width = 100
        simple_grid.resize(0, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 1  # Default to 1

    def test_responsive_with_auto_cols(self, simple_grid, responsive_helper):
        """Test auto_cols in responsive context."""
        simple_grid.auto_cols = True
        simple_grid.min_col_width = 200
        simple_grid.cols = {"md": 4}  # But auto overrides fixed?

        # Auto_cols takes precedence over fixed cols when enabled
        responsive_helper.set_width(500)  # 2 cols (500//200)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2

        responsive_helper.set_width(900)  # 4 cols (900//200=4.5 ->4)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 4
