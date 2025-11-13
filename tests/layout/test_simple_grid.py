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
        """Test equal-width column distribution."""
        simple_grid.cols = 4
        simple_grid.resize(800, 300)
        for label in child_labels[:8]:
            simple_grid.add_child(label)
        QApplication.processEvents()

        expected_width = 200  # 800/4
        for label in child_labels[:4]:  # First row
            assert label.width() == expected_width
            assert label.height() == 150  # Approx


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
        """Test responsive column changes."""
        simple_grid.cols = {"xs": 1, "sm": 2, "md": 3, "lg": 4}
        expected = {"xs": 1, "sm": 2, "md": 3, "lg": 4}

        responsive_helper.assert_responsive_value(
            simple_grid._responsive, "cols", expected
        )

        # Test layout changes
        for label in range(8):
            simple_grid.add_child(QLabel(f"Resp {label}"))

        # At xs (width < 640): 1 col
        responsive_helper.set_width(500)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 1

        # At md (768+): 3 cols
        responsive_helper.set_width(800)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 3

    def test_responsive_spacing(self, simple_grid, responsive_helper):
        """Test responsive spacing."""
        simple_grid.hspacing = {"sm": "sm", "md": "md", "lg": "lg"}
        simple_grid.vspacing = {"sm": "sm", "md": "md", "lg": "lg"}
        simple_grid.cols = 2
        for label in range(4):
            simple_grid.add_child(QLabel(f"Spacing {label}"))

        # Verify resolution at different breakpoints
        responsive_helper.set_width(500)  # xs/sm
        QApplication.processEvents()
        h_gap_small = simple_grid._layout.horizontalSpacing()
        responsive_helper.set_width(800)  # md
        QApplication.processEvents()
        h_gap_medium = simple_grid._layout.horizontalSpacing()
        assert h_gap_medium > h_gap_small  # md > sm

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
        """Test auto-sizing with dynamic width changes."""
        simple_grid.auto_cols = True
        simple_grid.min_col_width = 200
        for label in child_labels[:6]:
            simple_grid.add_child(label)

        # Narrow: 2 cols (400//200=2)
        simple_grid.resize(400, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2

        # Wider: 3 cols (600//200=3)
        simple_grid.resize(600, 300)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 3


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
        """Test 100+ cells without crash."""
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
        assert layout_time < 2.0

        QApplication.processEvents()
        # All positioned
        for label in labels[:10]:
            assert label.geometry().x() >= 0 and label.geometry().y() >= 0

        # Cleanup
        for label in labels:
            grid.remove_child(label)

    def test_resize_performance_large(self, simple_grid):
        """Test resize on large SimpleGrid."""
        # Add 50 children
        for i in range(50):
            label = QLabel(f"Perf {i}")
            label.setFixedSize(50, 40)
            simple_grid.add_child(label)

        start_time = time.time()
        for w in [600, 800, 400, 1000]:
            simple_grid.resize(w, 500)
            QApplication.processEvents()
        resize_time = time.time() - start_time
        assert resize_time < 1.0

    def test_memory_cleanup_large(self, parent_widget):
        """Test memory after large SimpleGrid."""
        grid = SimpleGrid(parent=parent_widget)
        children = [QLabel(f"Mem {i}") for i in range(200)]
        for child in children:
            grid.add_child(child)

        QApplication.processEvents()
        gc.collect()
        initial_refs = len(gc.get_referents(grid))

        for child in children:
            grid.remove_child(child)
            child.deleteLater()

        gc.collect()
        final_refs = len(gc.get_referents(grid))
        assert final_refs < initial_refs * 0.6  # Heuristic


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
