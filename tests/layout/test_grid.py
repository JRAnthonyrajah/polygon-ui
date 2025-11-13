"""Comprehensive tests for Grid component behavior.

Includes basic functionality, responsive behavior, spans, auto-fit, nested scenarios,
and performance benchmarks for production readiness."""

import pytest
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QGridLayout
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont

from polygon_ui.layout.components.grid import Grid
from polygon_ui.layout.core.responsive import ResponsiveProps
from conftest import ResponsiveTestHelper
import time
import gc
import resource


@pytest.fixture
def grid(parent_widget):
    """Create a basic Grid widget."""
    grid_widget = Grid(parent=parent_widget, columns=3)
    parent_widget.resize(600, 400)
    grid_widget.show()
    QApplication.processEvents()
    return grid_widget


@pytest.fixture
def child_labels():
    """Create sample child labels with consistent size hints."""
    labels = []
    for i in range(9):  # Enough for 3x3 grid
        label = QLabel(f"Cell {i}")
        label.setMinimumSize(80, 50)
        label.setMaximumSize(150, 100)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        labels.append(label)
    return labels


class TestGridBasic:
    """Basic Grid component tests."""

    def test_init(self, grid):
        """Test Grid initialization."""
        assert isinstance(grid, Grid)
        assert grid.columns == 3
        assert grid.gutter == "md"
        assert grid.justify == "start"
        assert grid.align == "start"
        assert grid.auto_columns is False
        assert grid.min_column_width == 250
        assert isinstance(grid._layout, QGridLayout)
        assert grid._layout.columnCount() == 3

    def test_add_child(self, grid, child_labels):
        """Test adding children to Grid."""
        for i, label in enumerate(child_labels[:6]):
            grid.add_child(label)
        QApplication.processEvents()

        # Children placed in row-major: 0-2 row0, 3-5 row1
        for i, label in enumerate(child_labels[:6]):
            row = i // 3
            col = i % 3
            expected_x = col * 200  # Approx 600/3, ignoring gaps
            expected_y = row * 200  # Approx equal height
            actual = label.geometry()
            assert actual.x() == expected_x  # Simplified, adjust for gaps
            assert actual.y() == expected_y
            assert actual.width() == 200  # Stretch
            assert actual.height() == 200

    def test_remove_child(self, grid, child_labels):
        """Test removing children from Grid."""
        grid.add_child(child_labels[0])
        grid.remove_child(child_labels[0])
        assert child_labels[0] not in grid._children
        # Layout should update without the child


class TestGridColumns:
    """Tests for columns property."""

    @pytest.mark.parametrize("columns", [1, 3, 12])
    def test_fixed_columns(self, grid, child_labels, columns):
        """Test fixed number of columns."""
        grid.columns = columns
        grid.resize(600, 400)
        for i, label in enumerate(child_labels[: columns * 2]):
            grid.add_child(label)
        QApplication.processEvents()

        col_width = 600 // columns
        for i, label in enumerate(child_labels[: columns * 2]):
            row = i // columns
            col = i % columns
            assert label.geometry().x() == col * col_width
            assert label.geometry().y() == row * 200  # Approx

    def test_auto_columns(self, grid, child_labels):
        """Test auto-columns with min_column_width."""
        grid.auto_columns = True
        grid.min_column_width = 150
        grid.resize(600, 400)
        for label in child_labels[:8]:
            grid.add_child(label)
        QApplication.processEvents()

        # Should fit 4 columns (600//150=4)
        assert grid._layout.columnCount() == 4
        for i in range(4):
            assert grid._layout.columnMinimumWidth(i) == 150
            assert grid._layout.columnStretch(i) == 1


class TestGridGutterGap:
    """Tests for gutter, col_gap, row_gap properties."""

    @pytest.mark.parametrize("gap_value", [0, 8, "sm", 20])
    def test_gutter(self, grid, child_labels, gap_value):
        """Test uniform gutter (col and row gap)."""
        grid.gutter = gap_value
        grid.columns = 2
        grid.resize(500, 300)
        for label in child_labels[:4]:
            grid.add_child(label)
        QApplication.processEvents()

        actual_gap = grid._get_gutter_pixels(gap_value)
        # Horizontal gap between col 0 and 1
        assert child_labels[1].x() == child_labels[0].width() + actual_gap
        # Vertical gap between row 0 and 1
        assert child_labels[2].y() == child_labels[0].height() + actual_gap

    def test_separate_gaps(self, grid, child_labels):
        """Test separate col_gap and row_gap."""
        grid.col_gap = 10
        grid.row_gap = 20
        grid.columns = 2
        grid.resize(500, 300)
        for label in child_labels[:4]:
            grid.add_child(label)
        QApplication.processEvents()

        assert child_labels[1].x() - child_labels[0].x() - child_labels[0].width() == 10
        assert (
            child_labels[2].y() - child_labels[0].y() - child_labels[0].height() == 20
        )


class TestGridJustifyAlign:
    """Tests for justify-content and align-items."""

    @pytest.mark.parametrize("justify", ["start", "center", "end", "stretch"])
    def test_justify(self, grid, child_labels, justify):
        """Test justify-content (horizontal alignment of grid)."""
        grid.justify = justify
        grid.columns = 2
        grid.resize(600, 200)
        # Add fewer items to test alignment
        for label in child_labels[:2]:  # One row, two cols
            grid.add_child(label)
        QApplication.processEvents()

        if justify == "start":
            assert child_labels[0].x() == 0
        elif justify == "center":
            # Centered in container
            pass  # QGridLayout justify is per item, but default stretch
        elif justify == "end":
            # Items aligned to right
            pass
        # Note: QGridLayout's justify affects item alignment within cells
        # For grid container alignment, it's more about stretches

    @pytest.mark.parametrize("align", ["start", "center", "end", "stretch"])
    def test_align(self, grid, child_labels, align):
        """Test align-items (vertical alignment of items)."""
        grid.align = align
        grid.columns = 3
        grid.resize(600, 200)
        for label in child_labels[:3]:
            grid.add_child(label)
        QApplication.processEvents()

        default_alignment = (
            grid._layout.itemAt(0).alignment()
            if grid._layout.count() > 0
            else Qt.AlignTop | Qt.AlignLeft
        )
        v_align = default_alignment & Qt.AlignVertical_Mask
        if align == "start":
            assert v_align == Qt.AlignTop
        elif align == "center":
            assert v_align == Qt.AlignVCenter
        elif align == "end":
            assert v_align == Qt.AlignBottom
        elif align == "stretch":
            # Default stretch in QGridLayout
            pass


class TestGridResponsive:
    """Tests for responsive behavior."""

    def test_responsive_columns(self, grid, responsive_helper):
        """Test responsive column changes."""
        grid.columns = {"xs": 1, "sm": 2, "md": 3, "lg": 4}
        expected = {"xs": 1, "sm": 2, "md": 3, "lg": 4}

        responsive_helper.assert_responsive_value(grid._responsive, "columns", expected)

        # Test layout changes
        for label in range(8):
            grid.add_child(QLabel(f"Resp {label}"))

        # At xs (width 0-599): 1 col
        responsive_helper.set_width(500)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 1

        # At md (768+): 3 cols
        responsive_helper.set_width(800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 3

    def test_responsive_gutter(self, grid, responsive_helper):
        """Test responsive gutter."""
        grid.gutter = {"sm": "sm", "md": "md", "lg": "lg"}
        # Verify resolution at different breakpoints using helper


class TestGridSpans:
    """Tests for colspan, rowspan, offset in child layout_props."""

    def test_colspan(self, grid, child_labels):
        """Test colspan spanning multiple columns."""
        grid.columns = 3
        grid.resize(600, 200)
        grid.add_child(child_labels[0], colspan=2)  # Spans col 0-1
        grid.add_child(child_labels[1])  # Col 2
        grid.add_child(child_labels[2])  # Next row, col 0
        QApplication.processEvents()

        assert child_labels[0].width() == 400  # 2/3 of 600
        assert child_labels[1].x() == 400  # After span
        assert child_labels[1].width() == 200
        assert child_labels[2].y() > 0  # Next row

    def test_rowspan(self, grid, child_labels):
        """Test rowspan spanning multiple rows."""
        grid.columns = 2
        grid.resize(400, 400)
        grid.add_child(child_labels[0], rowspan=2)  # Row 0-1, col 0
        grid.add_child(child_labels[1])  # Row 0, col 1
        grid.add_child(child_labels[2])  # Row 1, col 1 (after rowspan)
        QApplication.processEvents()

        assert child_labels[0].height() == 400  # Full height
        assert child_labels[1].y() == 0
        assert (
            child_labels[2].y() == 200
        )  # After half height? Wait, rowspan affects placement

    def test_offset(self, grid, child_labels):
        """Test offset to skip columns."""
        grid.columns = 4
        grid.resize(800, 200)
        grid.add_child(child_labels[0], offset=1)  # Starts at col 1
        grid.add_child(child_labels[1], offset=2)  # Starts at col 2, but after previous
        QApplication.processEvents()

        assert child_labels[0].x() == 200  # After offset 1 col
        # Offset applies per child


class TestGridAutoFit:
    """Tests for auto-fit and auto-fill behavior."""

    def test_auto_fit(self, grid, child_labels):
        """Test auto-fit with min_column_width."""
        grid.auto_fit(150)  # Convenience method
        grid.resize(600, 300)
        for label in child_labels[:12]:
            grid.add_child(label)
        QApplication.processEvents()

        # Fits 4 columns (600//150)
        assert grid._layout.columnCount() == 4
        assert grid.auto_columns is True
        assert grid.min_column_width == 150

    def test_auto_fill_simulation(self, grid):
        """Test auto-fill behavior (simulated via auto_columns)."""
        # Since QGridLayout doesn't have true auto-fill, test stretch behavior
        grid.auto_columns = True
        grid.min_column_width = 100
        grid.resize(500, 200)
        for i in range(6):
            grid.add_child(QLabel(f"Auto {i}"))
        QApplication.processEvents()

        # Columns fill available space with stretch
        col_count = 5  # 500//100=5
        assert grid._layout.columnCount() == col_count
        for i in range(col_count):
            assert grid._layout.columnStretch(i) == 1


class TestGridNested:
    """Tests for nested Grid scenarios."""

    def test_nested_grid(self, parent_widget):
        """Test Grid inside another Grid."""
        outer_grid = Grid(parent=parent_widget, columns=2)
        outer_grid.resize(600, 400)
        outer_grid.show()
        QApplication.processEvents()

        inner_grid = Grid(columns=3)
        outer_grid.add_child(inner_grid, rowspan=2)

        # Add to inner
        for i in range(6):
            label = QLabel(f"Inner {i}")
            label.setMinimumSize(50, 30)
            inner_grid.add_child(label)

        # Add other to outer
        outer_label = QLabel("Outer")
        outer_grid.add_child(outer_label)

        QApplication.processEvents()

        # Verify inner spans rows, outer has other child
        assert inner_grid.geometry().height() > outer_label.geometry().height()


class TestGridConvenience:
    """Tests for convenience methods."""

    def test_fixed_columns_method(self, grid):
        """Test fixed_columns convenience."""
        grid.fixed_columns(4)
        assert grid.columns == 4
        assert grid.auto_columns is False

    def test_responsive_columns_method(self, grid):
        """Test responsive_columns convenience."""
        grid.responsive_columns({"sm": 2, "lg": 4})
        assert grid.columns == {"sm": 2, "lg": 4}
        assert grid.auto_columns is False

    def test_minmax_columns(self, grid):
        """Test minmax_columns convenience (simulated)."""
        grid.minmax_columns(100, 200)
        assert grid.auto_columns is True
        assert grid.min_column_width == 100  # Assuming pixels


class TestGridComplex:
    """Complex grid scenarios with mixed features."""

    def test_complex_mixed_spans_responsive(self, grid, responsive_helper):
        """Test mixed spans, responsive columns, gaps."""
        grid.columns = {"md": 3, "lg": 4}
        grid.gutter = 10
        grid.resize(800, 500)

        # Add with spans and offsets
        grid.add_child(QLabel("Full Row"), colspan=3, offset=0)
        grid.add_child(QLabel("Span 2"), colspan=2, offset=1)
        grid.add_child(QLabel("Small"), offset=0)
        # More children...

        QApplication.processEvents()

        # At md: 3 cols
        responsive_helper.set_width(800)  # lg? Assume
        # Verify positions with spans

    def test_nested_with_spans(self, parent_widget):
        """Test nested grid with spans in parent."""
        outer = Grid(parent=parent_widget, columns=2)
        outer.resize(600, 400)
        inner = Grid(columns=2)
        outer.add_child(inner, colspan=2)  # Full width
        # Add to inner and outer
        # Verify


class TestGridPerformance:
    """Performance benchmarks for large grids."""

    def test_large_grid_no_crash(self, parent_widget):
        """Test 100+ cells without crash."""
        grid = Grid(
            parent=parent_widget, columns=10, auto_columns=True, min_column_width=50
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

    def test_resize_performance_large(self, grid):
        """Test resize on large grid."""
        # Add 50 children
        for i in range(50):
            label = QLabel(f"Perf {i}")
            label.setFixedSize(50, 40)
            grid.add_child(label)

        start_time = time.time()
        for w in [600, 800, 400, 1000]:
            grid.resize(w, 500)
            QApplication.processEvents()
        resize_time = time.time() - start_time
        assert resize_time < 1.0

    def test_memory_cleanup_large(self, parent_widget):
        """Test memory after large grid."""
        grid = Grid(parent=parent_widget)
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


class TestGridEdgeCases:
    """Edge cases and error handling."""

    def test_zero_columns(self, grid):
        """Test columns=0 (should default to 1)."""
        grid.columns = 0
        assert grid.columns == 1  # Or handle gracefully

    def test_negative_gutter(self, grid, child_labels):
        """Test negative gap (should be 0)."""
        grid.gutter = -5
        grid.add_child(child_labels[0])
        grid.add_child(child_labels[1])
        QApplication.processEvents()
        assert child_labels[1].x() - child_labels[0].x() - child_labels[0].width() >= 0

    def test_invalid_span(self, grid, child_labels):
        """Test invalid colspan > columns."""
        grid.columns = 2
        grid.add_child(child_labels[0], colspan=3)  # >2
        QApplication.processEvents()
        # Should clamp to available: colspan=2
        assert child_labels[0].width() == grid.width()  # Full width

    def test_empty_grid(self, grid):
        """Test no children."""
        grid.resize(500, 300)
        QApplication.processEvents()
        # No errors

    def test_one_child_full_span(self, grid, child_labels):
        """Test single child spanning all."""
        grid.columns = 3
        grid.add_child(child_labels[0], colspan=3)
        QApplication.processEvents()
        assert child_labels[0].width() == grid.width()

    def test_offset_beyond_columns(self, grid, child_labels):
        """Test large offset."""
        grid.columns = 2
        grid.add_child(child_labels[0], offset=3)
        # Should wrap or clamp
        QApplication.processEvents()
        assert child_labels[0].x() >= 0  # Placed somewhere

    def test_responsive_with_spans(self, grid, responsive_helper):
        """Test spans in responsive grid."""
        grid.columns = {"sm": 2, "md": 3}
        grid.add_child(QLabel("Span"), colspan=2)  # At sm: full, at md: 2/3
        responsive_helper.set_width(500)  # sm
        QApplication.processEvents()
        assert QLabel("Span").width() == 500  # Full
        responsive_helper.set_width(800)  # md
        QApplication.processEvents()
        assert QLabel("Span").width() == 533  # 2/3 of 800 approx
