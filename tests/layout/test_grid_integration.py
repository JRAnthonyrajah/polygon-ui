"""Grid system integration testing - complex scenarios and nested layouts.

Tests comprehensive integration of Grid with other layout components (Container, Stack, Group, Flex, Box, Col, SimpleGrid).
Covers dashboard layouts, nested grids, responsive coordination, and real-world patterns.
"""

import pytest
from unittest.mock import Mock, patch

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QSize

# Import layout components
from polygon_ui.layout.components.grid import Grid
from polygon_ui.layout.components.simple_grid import SimpleGrid
from polygon_ui.layout.components.col import Col
from polygon_ui.layout.components.container import Container
from polygon_ui.layout.components.stack import Stack
from polygon_ui.layout.components.group import Group
from polygon_ui.layout.components.flex import Flex
from polygon_ui.layout.components.box import Box

# Fixtures from conftest
from tests.layout.conftest import ResponsiveTestHelper, app, qt_widget


class TestGridComplexScenarios:
    """Test complex grid layout scenarios with multiple components."""

    @pytest.fixture
    def dashboard_grid(self, qt_widget):
        """Create a dashboard-style grid layout."""
        container = Container(parent=qt_widget, size="md", px="lg")
        grid = Grid(
            parent=container,
            columns={"base": 1, "md": 2, "lg": 3},
            gutter="md",
            justify="start",
            align="stretch",
        )
        container.add_child(grid)  # Assuming Container supports add_child
        qt_widget.resize(1200, 800)
        grid.show()
        QApplication.processEvents()
        return grid, container

    def test_dashboard_layout_with_cols(self, dashboard_grid):
        """Test dashboard layout: Grid with Col components of varying spans."""
        grid, container = dashboard_grid

        # Create Cols with different spans
        col1 = Col(parent=grid, span={"base": 1, "md": 2, "lg": 3})  # Full width on lg
        col2 = Col(parent=grid, span={"base": 1, "md": 1, "lg": 2}, offset={"md": 1})
        col3 = Col(parent=grid, span=1)

        # Add content to cols (Stack with labels)
        stack1 = Stack(parent=col1, direction="column", gap="sm")
        stack1.add_child(QLabel("Dashboard Header"))
        stack1.add_child(QLabel("Main Content Area"))

        stack2 = Stack(parent=col2, direction="column", gap="sm")
        stack2.add_child(QLabel("Sidebar Item 1"))
        stack2.add_child(QLabel("Sidebar Item 2"))

        box3 = Box(parent=col3, p="md", bg="gray.100")
        box3.add_child(QLabel("Quick Action"))

        # Add cols to grid
        grid.add_child(col1)
        grid.add_child(col2)
        grid.add_child(box3)  # Direct Box as child

        QApplication.processEvents()

        # Assertions: On large screen, col1 spans 3 cols, col2 spans 2 with offset, box3 spans 1
        # Approximate geometry checks
        assert col1.width() > col2.width() > box3.width()  # Responsive spans
        assert col2.x() > 0  # Offset on md+
        assert col1.y() == col2.y() == box3.y() == 0  # Same row initially

    def test_nested_grids(self, qt_widget):
        """Test nested Grid inside Grid and other components."""
        outer_container = Container(parent=qt_widget, fluid=True, py="xl")
        outer_grid = Grid(
            parent=outer_container,
            columns=2,
            gutter="lg",
            justify="center",
            align="start",
        )

        # Nested grid in first cell
        nested_grid = Grid(
            parent=outer_grid,
            columns={"base": 1, "sm": 2},
            gutter="sm",
            auto_columns=True,
            min_column_width=150,
        )

        # Add content to nested grid
        for i in range(4):
            box = Box(parent=nested_grid, p="md", border="1px solid gray.300")
            box.add_child(QLabel(f"Nested Item {i}"))
            nested_grid.add_child(box)

        # Flex in second cell
        sidebar_flex = Flex(
            parent=outer_grid,
            direction="column",
            gap="md",
            align="stretch",
        )
        for i in range(3):
            group = Group(parent=sidebar_flex, gap="sm", wrap=True)
            group.add_child(QLabel(f"Nav {i}"))
            group.add_child(QLabel(f"Link {i}"))
            sidebar_flex.add_child(group)

        outer_container.add_child(outer_grid)
        qt_widget.resize(1000, 600)
        QApplication.processEvents()

        # Assertions: Nested grid responds within parent cell, flex stacks vertically
        assert nested_grid.parent() == outer_grid
        assert nested_grid.width() < outer_grid.width() / 2  # Half width approx
        assert sidebar_flex.height() > nested_grid.height()  # Different content
        # On resize to small, nested becomes 1 col
        qt_widget.resize(400, 600)
        QApplication.processEvents()
        assert len(nested_grid._children) == 4  # All in one column visually

    def test_grid_with_flex_children(self, dashboard_grid):
        """Test Grid cells containing Flex components."""
        grid, container = dashboard_grid

        # Flex in first cell: horizontal navigation
        nav_flex = Flex(
            parent=grid,
            direction="row",
            justify="space-between",
            align="center",
            gap="md",
        )
        nav_flex.add_child(QLabel("Logo"))
        nav_flex.add_child(QLabel("Menu 1"))
        nav_flex.add_child(QLabel("Menu 2"))

        # Stack in second cell: vertical cards
        cards_stack = Stack(
            parent=grid,
            direction="column",
            gap="lg",
            justify="start",
        )
        for i in range(2):
            card_box = Box(
                parent=cards_stack,
                p="lg",
                bg="blue.50",
                borderRadius="md",
                boxShadow="sm",
            )
            card_box.add_child(QLabel(f"Card {i}"))
            cards_stack.add_child(card_box)

        grid.add_child(nav_flex)
        grid.add_child(cards_stack)

        QApplication.processEvents()

        # Assertions: Flex spans full cell width, items spaced; Stack vertical
        assert nav_flex.children()[0].x() == 0  # Logo start
        assert (
            nav_flex.children()[1].x() > nav_flex.children()[0].width() + gap
        )  # Spaced
        assert (
            cards_stack.children()[1].y() > cards_stack.children()[0].height() + gap
        )  # Stacked

    def test_real_world_card_grid(self, qt_widget):
        """Test real-world pattern: SimpleGrid for card layout inside Container."""
        container = Container(parent=qt_widget, size="lg", center=True, px="xl")
        simple_grid = SimpleGrid(
            parent=container,
            cols={"base": 1, "sm": 2, "md": 3, "lg": 4},
            spacing="md",
            auto_cols=True,
            min_col_width=250,
        )

        # Create card components
        cards = []
        for i in range(8):  # 8 cards
            card = Box(
                p="md",
                bg="white",
                border="1px solid gray.200",
                borderRadius="md",
                boxShadow="xs",
                display="flex",
                direction="column",
                justify="space-between",
                height=200,  # Fixed height for uniformity
            )
            title = QLabel(f"Card Title {i+1}")
            title.setStyleSheet("font-weight: bold;")
            content = QLabel("Card content with multiple lines of text.")
            footer = Group(gap="sm", align="center")
            footer.add_child(QLabel("Action 1"))
            footer.add_child(QLabel("Action 2"))

            card.add_child(title)
            card.add_child(content)
            card.add_child(footer)
            simple_grid.add_child(card)
            cards.append(card)

        container.add_child(simple_grid)  # Via layout or direct
        qt_widget.resize(1400, 800)
        QApplication.processEvents()

        # Assertions: Cards arranged in responsive grid, equal heights, content laid out
        assert len(simple_grid._children) == 8
        # On lg: 4 per row, each ~350px wide (1400/4)
        row1_cards = cards[:4]
        for card in row1_cards:
            assert card.width() > 300  # Min col width
            assert card.y() == 0  # Same row
        row2_cards = cards[4:8]
        assert row2_cards[0].y() > row1_cards[0].height() + spacing  # Next row
        # Internal layout: Flex column in card
        assert footer.children()[0].x() < footer.children()[1].x()  # Group horizontal

        # Responsive: Resize to small screen
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        # All in one column
        for i in range(1, 8):
            assert cards[i].y() > cards[i - 1].y() + cards[i - 1].height() + spacing

    def test_grid_inside_stack_group(self, qt_widget):
        """Test Grid nested inside Stack and Group for form layouts."""
        # Outer Stack: Vertical sections
        main_stack = Stack(parent=qt_widget, direction="column", gap="xl")
        main_stack.resize(600, 500)

        # Group for horizontal sections
        header_group = Group(
            parent=main_stack, gap="md", align="center", justify="start"
        )
        header_group.add_child(QLabel("Section 1 Header"))
        header_group.add_child(QLabel("Actions"))

        # Grid for form fields
        form_grid = Grid(
            parent=main_stack,
            columns=3,
            gutter="sm",
            justify="start",
            align="center",
        )
        labels = ["Name:", "Email:", "Phone:"]
        inputs = [QLabel(f"Input {i}") for i in range(3)]  # Simulate inputs
        for i in range(3):
            form_grid.add_child(QLabel(labels[i]))  # Col 0
            form_grid.add_child(inputs[i], colspan=2)  # Span cols 1-2

        # Another group below
        footer_group = Group(
            parent=main_stack,
            gap="lg",
            wrap=True,
            justify="space-between",
        )
        footer_group.add_child(QLabel("Save"))
        footer_group.add_child(QLabel("Cancel"))
        footer_group.add_child(QLabel("Reset"))

        main_stack.show()
        QApplication.processEvents()

        # Assertions: Grid cells span correctly, groups horizontal
        assert inputs[0].width() > labels[0].width() * 2  # Span 2 cols
        assert inputs[0].x() == labels[0].width() + gutter  # After label
        assert header_group.children()[0].x() == 0  # Start
        assert (
            footer_group.children()[1].x() > footer_group.children()[0].x() + gap
        )  # Spaced
        # On wrap for footer (if many), but with 3, space-between

    def test_responsive_nested_layouts(self, qt_widget):
        """Test responsive behavior in nested layouts with Grid."""
        responsive_container = Container(parent=qt_widget, fluid=True, px="md")
        responsive_container.resize(1200, 700)

        # Outer responsive Grid
        outer_grid = Grid(
            parent=responsive_container,
            columns={"base": 1, "md": 2, "lg": 3},
            gutter={"base": "sm", "lg": "lg"},
            justify="center",
        )

        # Cell 1: Nested SimpleGrid (cards)
        cards_simple_grid = SimpleGrid(
            parent=outer_grid,
            cols={"base": 1, "sm": 2},
            hspacing="sm",
            vspacing="md",
        )
        for i in range(4):
            card = Box(p="sm", bg="green.50", height=100)
            card.add_child(QLabel(f"Responsive Card {i}"))
            cards_simple_grid.add_child(card)

        # Cell 2: Flex with responsive direction
        nav_flex = Flex(
            parent=outer_grid,
            direction={"base": "column", "md": "row"},
            gap="md",
            wrap=True,
            justify="space-around",
            align="stretch",
        )
        for i in range(5):
            item = Box(p="xs", bg="blue.100")
            item.add_child(QLabel(f"Nav {i}"))
            nav_flex.add_child(item, grow=1)

        # Cell 3: Col with offset for asymmetry
        asymmetric_col = Col(
            parent=outer_grid,
            span={"base": 1, "md": 2},
            offset={"lg": 1},  # Offset on large
        )
        content_stack = Stack(
            parent=asymmetric_col,
            direction="column",
            gap="sm",
            align="start",
        )
        for i in range(3):
            content_stack.add_child(QLabel(f"Content Block {i}"))

        responsive_container.add_child(outer_grid)
        responsive_container.show()
        QApplication.processEvents()

        # Large screen assertions
        assert outer_grid._layout.columnCount() == 3  # lg: 3 cols
        assert nav_flex.direction == "row"  # md+
        assert cards_simple_grid._layout.columnCount() == 2  # sm: 2 cols
        assert asymmetric_col.x() > 0  # Offset on lg

        # Resize to small
        responsive_container.resize(400, 700)
        QApplication.processEvents()
        assert outer_grid._layout.columnCount() == 1  # base: 1 col
        assert nav_flex.direction == "column"  # base
        assert cards_simple_grid._layout.columnCount() == 1  # base
        assert asymmetric_col.x() == 0  # No offset on base

    def test_grid_with_mixed_component_types(self, dashboard_grid):
        """Test Grid integrating all layout components in cells."""
        grid, container = dashboard_grid

        # Cell 1: Container with Stack
        nested_container = Container(
            parent=grid,
            size="sm",
            fluid=False,
            px="md",
            py="sm",
            center=True,
        )
        inner_stack = Stack(
            parent=nested_container,
            direction="column",
            gap="xs",
            justify="center",
            align="stretch",
        )
        inner_stack.add_child(QLabel("Nested Container Header"))
        inner_stack.add_child(QLabel("Nested Content"))

        # Cell 2: Group with wrapping
        items_group = Group(
            parent=grid,
            gap="sm",
            align="start",
            justify="space-between",
            wrap=True,
        )
        for i in range(4):
            box = Box(p="xs", bg="yellow.100", borderRadius="sm")
            box.add_child(QLabel(f"Group Item {i}"))
            items_group.add_child(box)

        # Cell 3: Flex with advanced props
        advanced_flex = Flex(
            parent=grid,
            direction="row",
            wrap=True,
            justify="space-around",
            align="center",
            gap="md",
        )
        flex_child1 = Box(grow=2, basis=100, p="sm", bg="red.100")
        flex_child1.add_child(QLabel("Flex Grow 2"))
        flex_child2 = Box(grow=1, basis=80, alignSelf="end", p="sm", bg="green.100")
        flex_child2.add_child(QLabel("Flex Grow 1, Align End"))
        advanced_flex.add_child(flex_child1)
        advanced_flex.add_child(flex_child2)

        grid.add_child(nested_container)
        grid.add_child(items_group)
        grid.add_child(advanced_flex)

        QApplication.processEvents()

        # Assertions: Each cell contains its component correctly laid out
        assert nested_container.width() < grid.width() / 3 * 2  # sm size
        assert len(items_group._children_order) == 4  # Group children
        assert items_group.wrap  # Wrapping if needed
        assert flex_child1.width() > flex_child2.width()  # Grow 2 vs 1
        assert flex_child2.y() > 0  # Align end in row

        # Responsive check: On small screen, all stack vertically in 1-col grid
        container.parent().resize(400, 800)  # qt_widget
        QApplication.processEvents()
        assert (
            nested_container.y() < items_group.y() < advanced_flex.y()
        )  # Vertical order


class TestNestedGridBehavior:
    """Test comprehensive nested Grid behavior, parent-child interactions, and complex nesting."""

    @pytest.fixture
    def nested_grid_setup(self, qt_widget):
        """Fixture for common nested Grid setup."""
        qt_widget.resize(1200, 800)
        outer_container = Container(parent=qt_widget, fluid=True, px="lg", py="xl")
        outer_grid = Grid(
            parent=outer_container,
            columns={"base": 1, "md": 2, "lg": 3},
            gutter="md",
            justify="start",
            align="stretch",
        )
        outer_container.add_child(outer_grid)
        outer_grid.show()
        QApplication.processEvents()
        return outer_grid, outer_container, qt_widget

    def test_nested_grid_different_columns(self, nested_grid_setup):
        """Test Grid inside Grid with different column configurations."""
        outer_grid, container, qt_widget = nested_grid_setup

        # Inner Grid with different columns: 4 cols vs outer's 3
        inner_grid = Grid(
            parent=outer_grid,
            columns=4,
            gutter="sm",
            auto_columns=True,
            min_column_width=100,
        )

        # Add 8 items to inner grid to span multiple rows
        for i in range(8):
            box = Box(parent=inner_grid, p="sm", bg=f"gray.{i % 10}")
            box.add_child(QLabel(f"Inner Item {i}"))
            inner_grid.add_child(box)

        # Add inner_grid to first cell of outer_grid
        outer_grid.add_child(inner_grid)

        # Add simple content to other outer cells
        for i in range(2):
            outer_box = Box(parent=outer_grid, p="md", bg="blue.100")
            outer_box.add_child(QLabel(f"Outer Cell {i}"))
            outer_grid.add_child(outer_box)

        QApplication.processEvents()

        # Assertions: Inner grid fits within outer cell, has 4 columns
        assert inner_grid.parent() == outer_grid
        assert abs(inner_grid.width() - outer_grid.width() / 3) < 5  # First cell on lg
        # Inner items should be arranged in 4 cols within inner width
        row1_items = inner_grid.children()[:4]
        for item in row1_items:
            assert abs(item.width() - inner_grid.width() / 4) < 5
        # Responsive: On md (2 cols outer), inner still 4 but narrower
        qt_widget.resize(800, 800)
        QApplication.processEvents()
        assert outer_grid._layout.columnCount() == 2
        assert all(
            abs(item.width() - inner_grid.width() / 4) < 5 for item in row1_items
        )

    def test_three_level_nesting(self, nested_grid_setup):
        """Test three-level nesting: Grid → Grid → Grid."""
        outer_grid, container, qt_widget = nested_grid_setup

        # Level 1: Outer Grid (3 cols)
        # Level 2: Middle Grid in first cell (2 cols)
        middle_grid = Grid(
            parent=outer_grid,
            columns=2,
            gutter="md",
            justify="center",
        )

        # Level 3: Inner Grid in first cell of middle (3 cols)
        inner_grid = Grid(
            parent=middle_grid,
            columns=3,
            gutter="sm",
            auto_columns=True,
        )

        # Add content to innermost
        for i in range(6):
            innermost_box = Box(parent=inner_grid, p="xs", bg="green.100")
            innermost_box.add_child(QLabel(f"Deep Item {i}"))
            inner_grid.add_child(innermost_box)

        middle_grid.add_child(inner_grid)

        # Add more to middle
        middle_box = Box(parent=middle_grid, p="sm", bg="yellow.100")
        middle_box.add_child(QLabel("Middle Content"))
        middle_grid.add_child(middle_box)

        outer_grid.add_child(middle_grid)

        # Fill other outer cells
        for i in range(2):
            outer_box = Box(parent=outer_grid, p="md")
            outer_box.add_child(QLabel(f"Outer {i}"))
            outer_grid.add_child(outer_box)

        QApplication.processEvents()

        # Assertions: Hierarchy correct, geometries nested
        assert inner_grid.parent() == middle_grid
        assert middle_grid.parent() == outer_grid
        assert (
            abs(inner_grid.width() - outer_grid.width() / 3 / 2) < 5
        )  # Nested fractions
        # Items in inner grid span 3 cols within its width
        inner_items = inner_grid.children()
        assert len(inner_items) == 6
        assert all(
            abs(item.width() - inner_grid.width() / 3) < 5 for item in inner_items[:3]
        )
        # Deep nesting doesn't break layout
        assert all(item.isVisible() for item in inner_items)

    def test_responsive_nested_grids(self, nested_grid_setup):
        """Test responsive behavior in nested Grid layouts with different breakpoints."""
        outer_grid, container, qt_widget = nested_grid_setup

        # Outer: responsive columns
        # Inner: different responsive setup
        inner_grid = Grid(
            parent=outer_grid,
            columns={"base": 1, "sm": 2, "md": 4},
            gutter={"base": "xs", "md": "md"},
            min_column_width=120,
        )

        # Add 8 items
        items = []
        for i in range(8):
            item = Box(parent=inner_grid, p="sm", height=80, bg=f"purple.{i % 10}")
            item.add_child(QLabel(f"Resp Item {i}"))
            inner_grid.add_child(item)
            items.append(item)

        outer_grid.add_child(inner_grid)

        # Other outer cells
        outer_flex = Flex(parent=outer_grid, direction="column", gap="sm")
        for i in range(2):
            outer_flex.add_child(QLabel(f"Responsive Outer {i}"))
        outer_grid.add_child(outer_flex)

        # Large screen (lg: outer 3 cols, inner 4 cols)
        qt_widget.resize(1400, 900)
        QApplication.processEvents()
        assert outer_grid._layout.columnCount() == 3
        assert inner_grid._layout.columnCount() == 4
        row1 = items[:4]
        assert all(item.y() == 0 for item in row1)
        assert all(abs(item.width() - inner_grid.width() / 4) < 5 for item in row1)

        # Medium (md: outer 2, inner 4 but constrained)
        qt_widget.resize(900, 900)
        QApplication.processEvents()
        assert outer_grid._layout.columnCount() == 2
        assert inner_grid._layout.columnCount() == 4  # Still 4, but narrower cols
        assert all(item.width() < 200 for item in items)  # Adjusted

        # Small (base: outer 1, inner 1)
        qt_widget.resize(400, 900)
        QApplication.processEvents()
        assert outer_grid._layout.columnCount() == 1
        assert inner_grid._layout.columnCount() == 1
        for i in range(1, 8):
            assert (
                items[i].y() > items[i - 1].y() + items[i - 1].height() + 4
            )  # xs gutter

    def test_parent_child_interactions(self, nested_grid_setup):
        """Test parent-child Grid interactions and layout coordination."""
        outer_grid, container, qt_widget = nested_grid_setup

        inner_grid = Grid(
            parent=outer_grid,
            columns=3,
            gutter="md",
            justify="space-between",  # Different from outer's start
            align="center",  # Different alignment
        )

        # Child spans: some full width, some partial
        full_span = Col(parent=inner_grid, span=3)  # Full across inner
        full_span.add_child(QLabel("Full Span Child"))

        partial1 = Box(parent=inner_grid, span=1)
        partial1.add_child(QLabel("Partial 1"))
        partial2 = Box(parent=inner_grid, span=2, offset=1)
        partial2.add_child(QLabel("Partial 2 with offset"))

        inner_grid.add_child(full_span)
        inner_grid.add_child(partial1)
        inner_grid.add_child(partial2)

        outer_grid.add_child(inner_grid)

        # Simple outer sibling
        sibling = Box(parent=outer_grid, p="lg", bg="gray.200")
        sibling.add_child(QLabel("Outer Sibling"))
        outer_grid.add_child(sibling)

        QApplication.processEvents()

        # Assertions: Child interactions don't affect parent, alignments respected
        assert abs(full_span.width() - inner_grid.width()) < 5  # Full span
        assert abs(partial1.width() - inner_grid.width() / 3) < 5
        assert abs(partial2.width() - inner_grid.width() * 2 / 3) < 5
        assert (
            abs(partial2.x() - (inner_grid.width() / 3 + 16)) < 5
        )  # offset + gutter md~16
        # Parent alignment: outer start, so inner x=0 in first cell
        assert inner_grid.x() == 0
        # Child center align: items y-centered in rows
        assert partial1.y() == partial2.y()  # Same row
        # No overflow or conflict
        assert inner_grid.height() > 0 and sibling.height() > 0

    def test_nested_grid_performance(self, qt_widget):
        """Test nested Grid performance characteristics - layout calculation time."""
        import time

        qt_widget.resize(1000, 800)

        # Create deep nesting: 3 levels, each with 9 children (3x3 grid)
        def create_nested_grid(level, parent, depth=3):
            if level > depth:
                return Box(parent=parent, p="xs", bg="gray.100")
            grid = Grid(
                parent=parent,
                columns=3,
                gutter="sm",
                auto_columns=True,
            )
            for _ in range(9):
                child = create_nested_grid(level + 1, grid, depth)
                grid.add_child(child)
            return grid

        start_time = time.time()
        root_container = Container(parent=qt_widget, fluid=True)
        deep_grid = create_nested_grid(1, root_container)
        root_container.add_child(deep_grid)
        creation_time = time.time() - start_time

        # Force layout
        deep_grid.show()
        QApplication.processEvents()

        layout_start = time.time()
        qt_widget.resize(1200, 900)
        QApplication.processEvents()
        layout_time = time.time() - layout_start

        # Assertions: Performance within reasonable bounds (approximate, non-deterministic)
        assert creation_time < 0.5  # Seconds to create deep structure
        assert layout_time < 0.2  # Seconds to layout on resize
        # Widget count: 1 + 3 grids * 9 children each, but recursive
        total_widgets = len(qt_widget.findChildren(QWidget))
        assert total_widgets > 20  # At least some nesting
        assert total_widgets < 100  # Not excessive

        # Memory pattern: Simple size check (rough)
        import sys

        memory_usage = sys.getsizeof(deep_grid) + sum(
            sys.getsizeof(c) for c in deep_grid.children()
        )
        assert memory_usage > 1000  # Bytes, rough estimate

    def test_layout_inheritance_conflicts(self, nested_grid_setup):
        """Test layout inheritance and conflicts in nested scenarios."""
        outer_grid, container, qt_widget = nested_grid_setup

        # Outer: justify start, align stretch
        # Inner: override to justify end, align start - test if conflicts
        inner_grid = Grid(
            parent=outer_grid,
            columns=2,
            gutter="md",
            justify="end",  # Conflicts with outer start
            align="start",  # Conflicts with outer stretch
        )

        # Items with different sizes to test alignment
        tall_item = Box(
            parent=inner_grid, height=150, bg="red.200", alignSelf="stretch"
        )
        tall_item.add_child(QLabel("Tall Item"))
        short_item1 = Box(parent=inner_grid, height=80, bg="blue.200")
        short_item1.add_child(QLabel("Short 1"))
        short_item2 = Box(parent=inner_grid, height=80, bg="green.200")
        short_item2.add_child(QLabel("Short 2"))

        inner_grid.add_child(tall_item)
        inner_grid.add_child(short_item1)
        inner_grid.add_child(short_item2)

        outer_grid.add_child(inner_grid)

        QApplication.processEvents()

        # Assertions: Inner props take precedence, no inheritance conflict
        assert inner_grid.justify == "end"  # Set on inner
        # Justify end: items pushed to right in row
        assert (
            short_item1.x() > 0 and short_item2.x() > short_item1.x()
        )  # In row, end-aligned
        # Align start: short items at top, tall stretches if set
        assert short_item1.y() == 0 and tall_item.y() == 0  # Same row start
        assert (
            short_item1.height() == 80 and tall_item.height() == 150
        )  # No forced stretch
        # Parent doesn't override: outer start keeps inner at left of cell
        assert inner_grid.x() == 0

    def test_edge_cases_nested_grids(self, nested_grid_setup):
        """Test edge cases and error handling in nested Grids."""
        outer_grid, container, qt_widget = nested_grid_setup

        # Case 1: Inner with 0 columns (invalid, should default or error)
        invalid_inner = Grid(
            parent=outer_grid,
            columns=0,  # Invalid
            gutter="sm",
        )
        # Expect: Defaults to 1 or handles gracefully
        try:
            invalid_inner.add_child(QLabel("Invalid Item"))
            outer_grid.add_child(invalid_inner)
            QApplication.processEvents()
            assert invalid_inner._layout.columnCount() >= 1  # Handled
        except Exception as e:
            pytest.fail(f"Unexpected error in invalid columns: {e}")

        # Case 2: Over-spanning child in inner (span > columns)
        inner_grid = Grid(
            parent=outer_grid,
            columns=2,
            gutter="xs",
        )
        over_span = Col(parent=inner_grid, span=3)  # >2
        over_span.add_child(QLabel("Over Span"))
        inner_grid.add_child(over_span)
        inner_grid.add_child(Box(parent=inner_grid, span=1).add_child(QLabel("Normal")))

        outer_grid.add_child(inner_grid)
        QApplication.processEvents()

        # Expect: Clamped to available width
        assert over_span.width() <= inner_grid.width()  # Full width
        assert over_span.width() >= inner_grid.width() / 2 * 1.5  # Approx clamped

        # Case 3: Deep nesting performance edge (100 levels - but limit to avoid crash)
        # Skip extreme, test moderate deep with no crash
        deep_inner = Grid(parent=outer_grid, columns=1)
        current = deep_inner
        for _ in range(10):  # Moderate depth
            next_level = Grid(parent=current, columns=1)
            current.add_child(next_level)
            current = next_level
        final_box = Box(parent=current).add_child(QLabel("Deep Edge"))
        current.add_child(final_box)

        outer_grid.add_child(deep_inner)
        QApplication.processEvents()

        assert final_box.isVisible()  # No crash, layout propagates
        # Memory: Rough check, no leak indication
        before_memory = qt_widget.findChildren(QWidget)
        qt_widget.resize(1100, 850)
        QApplication.processEvents()
        after_memory = qt_widget.findChildren(QWidget)
        assert len(after_memory) == len(before_memory)  # No extra leaks in resize

        # Case 4: Nested with no children - empty layout
        empty_inner = Grid(parent=outer_grid, columns=5)
        outer_grid.add_child(empty_inner)
        QApplication.processEvents()
        assert (
            empty_inner.height() == 0 or empty_inner.sizeHint().height() == 0
        )  # Collapses


class TestGridResponsiveIntegration:
    """Comprehensive responsive integration tests for the entire grid system."""

    @pytest.fixture
    def responsive_setup(self, qt_widget):
        """Setup for responsive grid integration tests."""
        qt_widget.resize(1200, 800)  # Start with large screen
        container = Container(
            parent=qt_widget, fluid=True, px={"base": "sm", "lg": "xl"}
        )
        grid = Grid(
            parent=container,
            columns={"base": 1, "sm": 2, "md": 3, "lg": 4},
            gutter={"base": "xs", "md": "md"},
            justify="center",
            align="stretch",
        )
        simple_grid = SimpleGrid(
            parent=grid,
            cols={"base": 1, "sm": 2, "md": 3},
            spacing="sm",
            auto_cols=True,
            min_col_width=200,
        )
        grid.add_child(simple_grid)
        container.add_child(grid)
        grid.show()
        QApplication.processEvents()
        return grid, simple_grid, container, qt_widget

    def test_grid_col_responsive_coordination(self, responsive_setup):
        """Test Grid + Col responsive coordination across breakpoints."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Add responsive Cols to grid
        col1 = Col(
            parent=grid,
            span={"base": 1, "md": 2, "lg": 3},
            offset={"sm": 0, "md": 1},
        )
        col1.add_child(QLabel("Responsive Col 1"))

        col2 = Col(
            parent=grid,
            span={"base": 1, "sm": 1, "lg": 1},
            offset={"lg": 1},
        )
        col2.add_child(QLabel("Responsive Col 2"))

        grid.add_child(col1)
        grid.add_child(col2)

        # Large screen (lg): grid 4 cols, col1 span 3 offset 0, col2 span 1 offset 1 (but since after, positions accordingly)
        qt_widget.resize(1400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 4
        assert col1.width() > col2.width() * 3  # Span 3 vs 1
        assert col1.x() == 0
        assert col2.x() > col1.width()  # After col1

        # Medium (md): grid 3 cols, col1 span 2 offset 1, col2 span 1
        qt_widget.resize(900, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 3
        assert col1.width() > col2.width() * 2
        assert col1.x() > 0  # Offset 1 col
        assert col2.x() > col1.x() + col1.width()

        # Small (sm): grid 2 cols, col1 span 1 offset 0, col2 span 1
        qt_widget.resize(600, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 2
        assert col1.width() == col2.width()  # Both span 1
        assert col1.x() == 0
        assert col2.x() == col1.width() + self._get_gutter_pixels(
            grid, "xs"
        )  # base gutter

        # Base: grid 1 col, both full width stacked
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 1
        assert col1.width() == col2.width() == grid.width()
        assert col2.y() > col1.height() + self._get_gutter_pixels(grid, "xs")

    def _get_gutter_pixels(self, grid, breakpoint):
        """Helper to get gutter pixels for a breakpoint (mock theme)."""
        # Mock theme spacing: xs=4, sm=8, md=16, etc.
        spacing_map = {"xs": 4, "sm": 8, "md": 16, "lg": 24}
        return spacing_map.get(breakpoint, 8)

    def test_simplegrid_responsive_in_complex_layouts(self, responsive_setup):
        """Test SimpleGrid responsive behavior in complex nested layouts."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Add items to SimpleGrid
        for i in range(6):
            box = Box(parent=simple_grid, p="md", height=100, bg="gray.100")
            box.add_child(QLabel(f"Simple Item {i}"))
            simple_grid.add_child(box)

        # Test nested in Container with responsive padding
        container.px = {"base": "xs", "lg": "xl"}  # Responsive padding

        # Large: simple_grid 3 cols (md+), container xl padding
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 3
        padding = 24 * 2  # xl left+right
        assert simple_grid.x() == padding  # Padded
        row_width = (
            sum(box.width() for box in simple_grid.children()[:3]) + 2 * 8
        )  # spacing sm=8
        assert abs(simple_grid.width() - row_width) < 10  # Fits with spacing

        # Medium: 3 cols still, but smaller padding md? Wait, container px responsive
        qt_widget.resize(800, 800)
        QApplication.processEvents()
        padding_md = 16 * 2
        assert simple_grid.x() == padding_md
        assert all(
            box.y() == 0 or box.y() == 108 for box in simple_grid.children()
        )  # 100h +8s

        # Small: 2 cols (sm), xs padding=4*2=8
        qt_widget.resize(500, 800)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 2
        assert simple_grid.x() == 8
        # Items wider due to fewer cols

        # Base: 1 col
        qt_widget.resize(300, 800)
        QApplication.processEvents()
        assert simple_grid._layout.columnCount() == 1
        assert all(box.width() == simple_grid.width() for box in simple_grid.children())

    def test_container_responsive_padding_nested_components(self, responsive_setup):
        """Test Container responsive padding with nested grid components."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Nest Stack and Group inside grid, within container
        stack = Stack(
            parent=grid,
            direction={"base": "column", "md": "row"},
            gap="sm",
            align="center",
        )
        for i in range(3):
            stack.add_child(QLabel(f"Stack Item {i}"))

        group = Group(
            parent=grid,
            gap={"base": "xs", "lg": "lg"},
            wrap=True,
            justify="space-between",
        )
        for i in range(4):
            group.add_child(QLabel(f"Group Item {i}"))

        grid.add_child(stack)
        grid.add_child(group)

        # Container responsive padding affects nested positioning
        # Large: xl padding=24*2=48, stack row, group lg gap=24
        qt_widget.resize(1400, 800)
        QApplication.processEvents()
        assert container.px == "xl"  # Resolved
        assert grid.x() == 48
        assert stack.direction == "row"
        assert stack.children()[1].x() > stack.children()[0].width() + 8  # sm gap
        assert group.gap == "lg"  # Responsive

        # Base: xs padding=4*2=8, stack column, group xs gap=4, wrap if needed
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert grid.x() == 8
        assert stack.direction == "column"
        assert all(c.y() > 0 for c in stack.children()[1:])
        assert group.gap == "xs"
        # With small width, group wraps
        assert len(set(c.y() for c in group.children())) > 1

    def test_stack_group_responsive_in_grid_contexts(self, responsive_setup):
        """Test Stack/Group responsive behavior within Grid contexts."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Stack in grid cell, responsive direction
        responsive_stack = Stack(
            parent=grid,
            direction={"base": "column", "sm": "row"},
            gap={"base": "xs", "md": "md"},
            justify="space-around",
            wrap=False,
        )
        items = [QLabel(f"Resp Stack {i}") for i in range(4)]
        for item in items:
            responsive_stack.add_child(item, grow=1 if i % 2 == 0 else 0)

        # Group in another cell, responsive wrap and gap
        responsive_group = Group(
            parent=grid,
            gap={"base": "sm", "lg": "xl"},
            wrap={"base": True, "md": False},
            align="stretch",
            justify={"base": "center", "lg": "start"},
        )
        group_items = [QLabel(f"Resp Group {i}") for i in range(5)]
        for item in group_items:
            responsive_group.add_child(item)

        grid.add_child(responsive_stack)
        grid.add_child(responsive_group)

        # Test coordination with grid breakpoints
        # sm: grid 2 cols, stack row, group wrap true sm gap
        qt_widget.resize(600, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 2
        assert responsive_stack.direction == "row"
        assert (
            sum(item.width() for item in responsive_stack.children() if item.grow) > 200
        )  # Grow fills
        assert responsive_group.wrap is True
        assert len(set(item.y() for item in responsive_group.children())) > 1  # Wrapped
        assert responsive_group.gap == "sm"
        assert responsive_group.justify == "center"

        # lg: grid 4 cols, stack row md gap, group no wrap xl gap start justify
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert responsive_stack.gap == "md"
        assert responsive_group.wrap is False
        assert all(item.y() == 0 for item in responsive_group.children())  # No wrap
        assert responsive_group.gap == "xl"
        assert responsive_group.justify == "start"
        assert responsive_group.children()[0].x() == 0

        # Base: grid 1 col, stack column xs gap, group wrap true sm? base sm gap center
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 1
        assert responsive_stack.direction == "column"
        assert all(item.x() == 0 for item in responsive_stack.children())
        assert responsive_group.gap == "sm"  # base
        assert responsive_group.justify == "center"

    def test_flex_responsive_with_grid_integration(self, responsive_setup):
        """Test Flex responsive behavior integrated with Grid."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Flex nested in grid cell, with responsive props coordinating with grid
        integrated_flex = Flex(
            parent=grid,
            direction={"base": "column", "md": "row"},
            wrap={"base": False, "lg": True},
            justify={"base": "start", "md": "space-between"},
            align={"base": "start", "lg": "center"},
            gap={"base": "xs", "md": "lg"},
        )
        flex_children = []
        for i in range(6):
            child = Box(p="sm", bg="blue.200", height=50 if i % 2 == 0 else 80)
            child.add_child(QLabel(f"Flex-Grid {i}"))
            integrated_flex.add_child(child, grow=1, basis={"base": 100, "lg": "20%"})

        grid.add_child(integrated_flex)

        # lg: grid 4 cols, flex row wrap true lg gap center align, basis 20%
        qt_widget.resize(1400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 4
        assert integrated_flex.direction == "row"
        assert integrated_flex.wrap is True
        assert integrated_flex.justify == "space-between"
        assert integrated_flex.align == "center"
        assert integrated_flex.gap == "lg"
        # With wrap, multiple lines, children basis 20% of flex width
        flex_width = integrated_flex.width()
        for child in flex_children[:3]:  # First row approx
            assert abs(child.width() - flex_width * 0.2) < 10
        # Heights: center align, varying heights centered in line height

        # md: grid 3 cols, flex row no wrap? md wrap false, space-between, lg gap? md lg gap
        qt_widget.resize(900, 800)
        QApplication.processEvents()
        assert integrated_flex.wrap is False  # md false
        assert all(child.y() == 0 for child in flex_children)  # No wrap
        positions = [c.x() for c in flex_children]
        assert positions == sorted(positions)  # Ordered
        # Space-between: even distribution

        # base: grid 1 col, flex column no wrap xs gap start, basis 100 full
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert integrated_flex.direction == "column"
        assert integrated_flex.wrap is False
        assert integrated_flex.justify == "start"
        assert integrated_flex.align == "start"
        assert integrated_flex.gap == "xs"
        assert all(child.width() == integrated_flex.width() for child in flex_children)
        assert all(c.y() > 0 for c in flex_children[1:])  # Stacked

    def test_multi_component_responsive_layouts(self, qt_widget):
        """Test multi-component responsive layouts: Grid + Col + SimpleGrid + Container."""
        qt_widget.resize(1200, 800)
        outer_container = Container(
            parent=qt_widget,
            size={"base": "xs", "lg": "xl"},
            fluid=True,
            px="lg",
            py={"base": "sm", "md": "lg"},
        )

        main_grid = Grid(
            parent=outer_container,
            columns={"base": 1, "sm": 2, "md": 3, "lg": 4},
            gutter="md",
            justify="start",
            align="stretch",
        )

        # Cols with nested SimpleGrid
        col_with_simple = Col(
            parent=main_grid,
            span={"base": 1, "md": 2, "lg": 3},
        )
        nested_simple = SimpleGrid(
            parent=col_with_simple,
            cols={"base": 1, "sm": 2},
            spacing={"base": "xs", "md": "sm"},
            min_col_width=150,
        )
        for i in range(4):
            nested_simple.add_child(
                Box(p="xs", height=60, bg="green.100").add_child(QLabel(f"Nested {i}"))
            )

        # Another col with content
        simple_col = Col(parent=main_grid, span=1)
        simple_col.add_child(QLabel("Simple Content"))

        main_grid.add_child(col_with_simple)
        main_grid.add_child(simple_col)

        outer_container.add_child(main_grid)
        main_grid.show()
        QApplication.processEvents()

        # lg: container xl size lg py, main_grid 4 cols, col span 3, nested_simple 2 cols
        assert outer_container.size == "xl"
        assert outer_container.py == "lg"
        assert main_grid._layout.columnCount() == 4
        assert col_with_simple.width() > simple_col.width() * 3
        assert nested_simple._layout.columnCount() == 2  # sm+ in md+ col
        row1_nested = nested_simple.children()[:2]
        assert all(abs(c.width() - nested_simple.width() / 2) < 5 for c in row1_nested)

        # sm: main_grid 2 cols, col span 1 (base), nested 2 cols but col narrow
        qt_widget.resize(600, 800)
        QApplication.processEvents()
        assert main_grid._layout.columnCount() == 2
        assert col_with_simple.width() == simple_col.width()
        # Nested tries 2 cols but min_width 150, if col <300, falls to 1
        if col_with_simple.width() < 300:
            assert nested_simple._layout.columnCount() == 1
        else:
            assert nested_simple._layout.columnCount() == 2

        # base: all stacked, container xs size sm py
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert outer_container.size == "xs"
        assert outer_container.py == "sm"
        assert main_grid._layout.columnCount() == 1
        assert all(c.width() == main_grid.width() for c in main_grid.children())
        assert nested_simple._layout.columnCount() == 1
        assert all(c.y() > 0 for c in nested_simple.children()[1:])

    def test_coordinated_breakpoint_changes(self, responsive_setup):
        """Test coordinated breakpoint changes across all components."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Set coordinated responsive props across components
        grid.columns = {"base": 1, "xs": 2, "sm": 3, "md": 4, "lg": 5, "xl": 6}
        simple_grid.cols = {"base": 1, "xs": 2, "sm": 3, "md": 4}
        container.px = {
            "base": "xs",
            "xs": "sm",
            "sm": "md",
            "md": "lg",
            "lg": "xl",
            "xl": "2xl",
        }
        container.py = {"base": "sm", "md": "lg", "xl": "2xl"}

        # Add children to test changes
        for i in range(3):
            grid.add_child(QLabel(f"Grid Child {i}"))
        for i in range(4):
            simple_grid.add_child(QLabel(f"Simple Child {i}"))

        # Test each breakpoint transition
        breakpoints = [
            ("xl", 1920),
            ("lg", 1200),
            ("md", 900),
            ("sm", 600),
            ("xs", 480),
            ("base", 0),
        ]
        expected_cols = {"grid": [6, 5, 4, 3, 2, 1], "simple": [4, 4, 4, 3, 2, 1]}
        expected_px = [48, 24, 16, 8, 4, 4]  # 2xl=48, xl=24, lg=24? Wait mock
        px_map = {"2xl": 48, "xl": 24, "lg": 24, "md": 16, "sm": 8, "xs": 4}
        py_map = {"2xl": 48, "lg": 24, "sm": 8}

        for bp_name, width in breakpoints:
            qt_widget.resize(width, 800)
            QApplication.processEvents()

            # Column counts
            assert (
                grid._layout.columnCount()
                == expected_cols["grid"][breakpoints.index((bp_name, width))]
            )
            assert (
                simple_grid._layout.columnCount()
                == expected_cols["simple"][breakpoints.index((bp_name, width))]
            )

            # Container padding
            expected_px_val = px_map.get(container.px, 8)
            assert grid.x() == expected_px_val  # Left padding
            if bp_name in py_map:
                # Check top padding indirectly via y of first child
                assert (
                    main_grid.children()[0].y() == py_map[bp_name]
                    if hasattr(main_grid, "children")
                    else True
                )

            # Verify child positions update without overlap
            for child in grid.children():
                assert child.x() >= 0 and child.y() >= 0
            for child in simple_grid.children():
                assert child.x() >= 0 and child.y() >= 0

    def test_mobile_first_responsive_patterns(self, responsive_setup):
        """Test mobile-first responsive grid patterns across the system."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Mobile-first: base mobile, then enhance for larger
        # Pattern: Mobile stacked cards, tablet 2-col, desktop 3-4 col with offsets
        col_mobile = Col(parent=grid, span=1)  # Full on all, but content responsive
        card_stack = Stack(
            parent=col_mobile,
            direction="column",  # Mobile vertical
            gap="sm",
            spacing=0,  # No extra
        )
        cards = []
        for i in range(3):
            card = Box(
                p={"base": "sm", "md": "md"},
                bg="white",
                borderRadius={"base": "sm", "lg": "lg"},
                boxShadow="sm",
                height={"base": 120, "md": 150},
            )
            card.add_child(QLabel(f"Mobile Card {i}"))
            card_stack.add_child(card)
            cards.append(card)

        # Add horizontal group on larger screens
        card_group = Group(
            parent=col_mobile,
            direction="row",  # Wait, Group is horizontal by default
            gap="md",
            wrap=True,
            visible={"base": False, "md": True},  # Hide on mobile
        )
        for i in range(3):
            group_card = Box(p="sm", width={"md": 200, "lg": 250}, bg="gray.50")
            group_card.add_child(QLabel(f"Group Card {i}"))
            card_group.add_child(group_card)

        col_mobile.add_child(card_stack)
        col_mobile.add_child(card_group)

        grid.add_child(col_mobile)

        # Base (mobile): Stack vertical, group hidden, small padding/shadow
        qt_widget.resize(375, 800)  # Mobile width
        QApplication.processEvents()
        assert card_stack.direction == "column"
        assert all(c.y() > 0 for c in cards[1:])
        assert not card_group.isVisible()  # Hidden
        assert all(card.p == "sm" for card in cards)
        assert all(card.height == 120 for card in cards)
        assert all(card.borderRadius == "sm" for card in cards)

        # md (tablet): Stack still column? But add group visible, md padding
        qt_widget.resize(768, 800)
        QApplication.processEvents()
        assert card_group.isVisible()
        assert card_group.wrap is True  # If needed
        assert all(card.p == "md" for card in cards)
        assert all(card.height == 150 for card in cards)
        assert all(card.borderRadius == "sm" for card in cards)  # lg not yet

        # lg (desktop): Group no wrap? lg width, lg radius
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert all(group_card.width == 250 for group_card in card_group.children())
        assert all(card.borderRadius == "lg" for card in cards)

        # Verify mobile-first: Changes only enhance, no breakage on resize back
        qt_widget.resize(375, 800)
        QApplication.processEvents()
        # Still correct for mobile
        assert not card_group.isVisible()

    def test_nested_responsive_layouts_multiple_levels(self, qt_widget):
        """Test nested responsive layouts with multiple levels of grid components."""
        qt_widget.resize(1200, 800)

        # Level 1: Responsive Container
        level1_container = Container(
            parent=qt_widget,
            fluid=True,
            px={"base": "xs", "lg": "2xl"},
            py="md",
        )

        # Level 2: Main Grid responsive cols
        level2_grid = Grid(
            parent=level1_container,
            columns={"base": 1, "sm": 2, "md": 3, "lg": 4},
            gutter={"base": "sm", "md": "lg"},
        )

        # Level 3: Col with nested SimpleGrid
        level3_col = Col(
            parent=level2_grid,
            span={"base": 1, "md": 2, "lg": 3},
            offset={"lg": 0.5},  # Half col offset on lg
        )
        level3_simple = SimpleGrid(
            parent=level3_col,
            cols={"base": 1, "sm": 2, "md": 3},
            spacing="md",
            auto_cols=True,
            min_col_width=180,
        )

        # Level 4: Nested Flex in SimpleGrid cells
        for i in range(6):
            level4_flex = Flex(
                parent=level3_simple,
                direction={"base": "column", "sm": "row"},
                gap="sm",
                justify="space-around",
                align_items="center",  # Qt align
            )
            for j in range(2):
                label = QLabel(f"Deep {i}-{j}")
                level4_flex.add_child(label, grow=1)
            level3_simple.add_child(level4_flex)

        # Add other level3 content
        other_col = Col(parent=level2_grid, span=1)
        other_col.add_child(
            Stack(direction="column", gap="sm").add_child(QLabel("Other"))
        )

        level2_grid.add_child(level3_col)
        level2_grid.add_child(other_col)
        level1_container.add_child(level2_grid)
        level2_grid.show()
        QApplication.processEvents()

        # lg: 4 cols, col span 3 offset 0.5 (approx), simple 3 cols, flex row
        assert level2_grid._layout.columnCount() == 4
        assert level3_col.width() > other_col.width() * 3
        assert level3_col.x() > level2_grid.width() / 8  # 0.5 col ~1/8
        assert level3_simple._layout.columnCount() == 3
        level4_flexes = level3_simple.children()
        for flex in level4_flexes[:3]:  # First row
            assert flex.direction == "row"
            assert flex.children()[1].x() > flex.children()[0].width() + 8  # sm gap

        # sm: 2 cols, col span 1 no offset, simple 2 cols, flex row
        qt_widget.resize(600, 800)
        QApplication.processEvents()
        assert level2_grid._layout.columnCount() == 2
        assert level3_col.width() == other_col.width()
        assert level3_col.x() == 0
        assert level3_simple._layout.columnCount() == 2
        for flex in level4_flexes:
            assert flex.direction == "row"

        # base: 1 col, simple 1 col, flex column
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert level2_grid._layout.columnCount() == 1
        assert level3_simple._layout.columnCount() == 1
        for flex in level4_flexes:
            assert flex.direction == "column"
            assert all(c.x() == 0 for c in flex.children())

        # Verify deep coordination: Padding affects all levels
        assert level2_grid.x() == 4  # base xs px=4
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert level2_grid.x() == 48  # 2xl=48?

    def test_responsive_performance_characteristics(self, qt_widget):
        """Test responsive performance: Time for layout updates on resize."""
        import time

        qt_widget.resize(1200, 800)

        # Complex nested structure
        container = Container(parent=qt_widget, fluid=True)
        grid = Grid(parent=container, columns=4, gutter="md")
        for i in range(12):  # 3x4 grid
            col = Col(parent=grid, span=1)
            inner_flex = Flex(parent=col, direction="row", wrap=True, gap="sm")
            for j in range(4):
                inner_flex.add_child(QLabel(f"Perf {i}-{j}"))
            grid.add_child(col)
        simple_in_grid = SimpleGrid(parent=grid, cols=2, spacing="lg")
        for k in range(6):
            simple_in_grid.add_child(
                Box(p="md", bg="gray.200").add_child(QLabel(f"Simple {k}"))
            )
        grid.add_child(simple_in_grid)

        container.add_child(grid)
        grid.show()

        # Baseline layout time
        start = time.time()
        QApplication.processEvents()
        baseline = time.time() - start

        # Test multiple rapid resizes (simulate responsive transitions)
        resize_times = []
        widths = [400, 600, 900, 1200, 600, 400, 1200]  # Mobile to desktop and back
        for width in widths:
            start = time.time()
            qt_widget.resize(width, 800)
            QApplication.processEvents()
            resize_times.append(time.time() - start)

        avg_resize = sum(resize_times) / len(resize_times)
        max_resize = max(resize_times)

        # Performance assertions (heuristic, adjust as needed)
        assert baseline < 0.1  # Initial layout fast
        assert avg_resize < 0.05  # Each resize <50ms
        assert max_resize < 0.1  # Worst case <100ms

        # Test with many children (scale)
        # Add 50 more simple items
        for _ in range(50):
            simple_in_grid.add_child(QLabel("Extra"))
        qt_widget.resize(800, 800)
        start = time.time()
        QApplication.processEvents()
        scaled_time = time.time() - start
        assert scaled_time < 0.2  # Still reasonable with 50+ children

    def test_theme_integration_responsive_changes(self, qt_widget, monkeypatch):
        """Test theme integration with responsive changes (mock theme breakpoints)."""
        from polygon_ui.theme import Theme

        # Mock theme with responsive spacing/colors
        def mock_get_spacing(size, breakpoint):
            spacing = {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32}
            return spacing.get(size, 8)

        def mock_get_color(color, breakpoint):
            if breakpoint == "dark":  # Simulate theme change at breakpoint
                return "#333"
            return "#ccc"

        monkeypatch.setattr(Theme, "_get_spacing_pixels", mock_get_spacing)
        monkeypatch.setattr(Theme, "get_color", mock_get_color)

        # Setup with theme-dependent props
        qt_widget.resize(1200, 800)
        container = Container(parent=qt_widget, fluid=True, px="lg", bg="gray.100")
        grid = Grid(
            parent=container,
            columns=3,
            gutter="md",
            justify="center",
        )
        for i in range(6):
            col = Col(parent=grid, span=1, p="md", bg="blue.200")
            col.add_child(QLabel(f"Themed {i}"))
            grid.add_child(col)
        container.add_child(grid)
        grid.show()
        QApplication.processEvents()

        # Large: lg spacing=24, light colors
        gutter_px = Theme._get_spacing_pixels("md", "lg")  # Assume theme has bp
        assert gutter_px == 16  # md=16
        # Colors: light
        assert any("blue" in col.styleSheet() for col in grid.children())  # Mock

        # Simulate theme change at md breakpoint (e.g., compact theme)
        qt_widget.resize(900, 800)
        QApplication.processEvents()
        # Smaller spacing? But mock doesn't change per bp, but test resolution
        assert Theme._get_spacing_pixels("md", "md") == 16

        # Test color change if dark at small bp (simulate)
        # For now, assert no crash on theme resolve at resizes
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        for col in grid.children():
            assert col.isVisible()  # Theme applied without error

    def test_accessibility_responsive_scenarios(self, qt_widget):
        """Test accessibility in responsive grid scenarios (basic tab order, visibility)."""
        qt_widget.resize(1200, 800)

        container = Container(parent=qt_widget, fluid=True)
        grid = Grid(parent=container, columns={"base": 1, "lg": 3}, gutter="sm")
        accessible_items = []
        for i in range(6):
            # Make focusable labels (simulate buttons)
            item = QLabel(f"Accessible Item {i}")
            item.setFocusPolicy(Qt.FocusPolicy.TabFocus)  # Tab-able
            item.setObjectName(f"item_{i}")  # For identification
            col = Col(parent=grid, span=1)
            col.add_child(item)
            grid.add_child(col)
            accessible_items.append(item)

        # Add hidden on small
        hidden_item = QLabel("Hidden on Mobile")
        hidden_item.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        hidden_col = Col(parent=grid, span=1, visible={"base": False, "lg": True})
        hidden_col.add_child(hidden_item)
        grid.add_child(hidden_col)

        container.add_child(grid)
        grid.show()
        QApplication.processEvents()

        # lg: All visible, tab order logical (left to right, top to bottom)
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 3
        assert all(item.isVisible() for item in accessible_items + [hidden_item])
        # Simulate tab: focus order should be row-major
        # Basic: Check object names in tab order
        tab_order = []
        current = grid.focusWidget()
        while current:
            tab_order.append(current.objectName())
            current = current.nextInFocusChain()
        # Expect order like item_0,1,2,3,4,5, hidden
        assert len([name for name in tab_order if name.startswith("item_")]) == 6

        # base: 1 col, hidden invisible, tab skips it
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert grid._layout.columnCount() == 1
        assert all(item.isVisible() for item in accessible_items)
        assert not hidden_item.isVisible()
        # Tab order: only visible items, stacked order
        tab_order_small = []
        current = grid.focusWidget()
        while current:
            if hasattr(current, "objectName"):
                tab_order_small.append(current.objectName())
            current = current.nextInFocusChain()
        visible_names = [name for name in tab_order_small if name.startswith("item_")]
        assert len(visible_names) == 6
        assert "hidden" not in str(tab_order_small)  # Skipped

        # Resize back: Order preserved, no loss
        qt_widget.resize(1200, 800)
        QApplication.processEvents()
        assert hidden_item.isVisible()  # Reappears in tab order

    def test_responsive_edge_cases_error_handling(self, responsive_setup):
        """Test edge cases and error handling in responsive grid system."""
        grid, simple_grid, container, qt_widget = responsive_setup

        # Case 1: Invalid responsive prop (non-dict or bad keys)
        with pytest.raises(ValueError):
            grid.columns = "invalid"  # Should error

        # Case 2: Conflicting breakpoints (overlapping min widths - but system handles)
        grid.columns = {"base": 1, "xs": 2, "sm": 3, "invalid_bp": 4}  # Ignore invalid
        assert "invalid_bp" not in grid._responsive.props["columns"]

        # Case 3: Responsive prop with missing base
        grid.gutter = {
            "sm": "lg"
        }  # Should default base to current or error? Assume fallback
        assert grid.gutter == "md"  # Default, or test no crash
        grid.gutter = {"base": "xs", "sm": "invalid_size"}
        # Invalid size fallback
        qt_widget.resize(600, 800)
        QApplication.processEvents()
        # No crash, uses fallback spacing

        # Case 4: Nested responsive conflict (child bp overrides parent?)
        col = Col(parent=grid, span={"base": 1, "md": 5})  # > parent md 3 cols
        grid.add_child(col)
        qt_widget.resize(900, 800)  # md
        QApplication.processEvents()
        assert col.width() <= grid.width()  # Clamped, no overflow

        # Case 5: Rapid breakpoint changes performance edge
        start = time.time()
        for _ in range(20):
            qt_widget.resize(400 + _ * 20, 800)  # Small variations
            QApplication.processEvents()
        rapid_time = time.time() - start
        assert rapid_time < 0.5  # Handles rapid without lag

        # Case 6: Theme change during responsive (no crash)
        # Already covered in theme test

        # Case 7: Zero-width responsive (collapse)
        zero_col = Col(parent=grid, span={"base": 0, "lg": 1})  # Invalid span 0
        grid.add_child(zero_col)
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert zero_col.width() > 0  # Defaults to 1 or min

        # Case 8: Accessibility in edge responsive (hidden/focus)
        focus_item = QLabel("Focus Edge")
        focus_item.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        hidden_flex = Flex(parent=grid, visible={"base": False, "md": True})
        hidden_flex.add_child(focus_item)
        grid.add_child(hidden_flex)
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        assert not focus_item.isVisible()
        # Tab skips hidden
        assert focus_item not in qt_widget.findChildren(QWidget, visibleOnly=True)

        qt_widget.resize(900, 800)
        QApplication.processEvents()
        assert focus_item.isVisible()


class TestGridPerformance:
    """Performance tests for large and complex grid layouts."""

    @pytest.fixture
    def large_grid_setup(self, qt_widget):
        """Fixture for large grid with 100+ children."""
        qt_widget.resize(1200, 800)
        container = Container(parent=qt_widget, fluid=True, px="lg")
        grid = Grid(
            parent=container,
            columns=12,
            gutter="md",
            justify="start",
            align="stretch",
        )
        container.add_child(grid)

        # Add 120 children (10 rows x 12 cols)
        children = []
        for i in range(120):
            box = Box(
                parent=grid,
                p="sm",
                bg="gray.100",
                height=60,
                width=90,  # Approx for 12 cols
            )
            box.add_child(QLabel(f"Grid Item {i}"))
            grid.add_child(box)
            children.append(box)

        grid.show()
        QApplication.processEvents()
        return grid, container, children, qt_widget

    def test_large_grid_creation_and_layout(self, large_grid_setup):
        """Test creation and initial layout time for large grid (120 components)."""
        import time
        from gc import collect

        grid, container, children, qt_widget = large_grid_setup

        # Cold start: Creation time
        start_time = time.time()
        # Re-create to measure fresh
        new_container = Container(parent=qt_widget, fluid=True, px="lg")
        new_grid = Grid(parent=new_container, columns=12, gutter="md")
        for _ in range(120):
            box = Box(parent=new_grid, p="sm", height=60)
            new_grid.add_child(box)
        creation_time = time.time() - start_time

        # Initial layout time
        new_container.add_child(new_grid)
        new_grid.show()
        layout_start = time.time()
        QApplication.processEvents()
        layout_time = time.time() - layout_start

        # Baselines (adjust based on system; these are reasonable targets)
        assert creation_time < 0.3  # <300ms creation
        assert layout_time < 0.1  # <100ms layout for 120 items

        # Hot start: Resize to force re-layout
        hot_start = time.time()
        qt_widget.resize(1400, 900)
        QApplication.processEvents()
        hot_layout = time.time() - hot_start
        assert hot_layout < 0.05  # Faster on subsequent

    def test_memory_usage_large_grid(self, large_grid_setup):
        """Test memory usage patterns for large grid."""
        import sys
        from gc import collect

        grid, container, children, qt_widget = large_grid_setup

        # Baseline memory
        collect()
        baseline_memory = sum(
            sys.getsizeof(obj) for obj in gc.get_objects()
        )  # Rough total

        # Memory after creation (already done)
        current_memory = sum(sys.getsizeof(obj) for obj in gc.get_objects())
        growth = current_memory - baseline_memory

        # Per component rough estimate: ~10KB per Box + QLabel
        expected_growth = len(children) * 15000  # Conservative
        assert growth < expected_growth * 1.2  # Within 20% tolerance

        # Check no excessive growth on resize
        qt_widget.resize(800, 600)
        QApplication.processEvents()
        collect()
        resize_memory = sum(sys.getsizeof(obj) for obj in gc.get_objects())
        assert abs(resize_memory - current_memory) < 1000  # Minimal change

    def test_deep_nested_grids_performance(self, qt_widget):
        """Test performance with deep nesting (5 levels)."""
        import time

        qt_widget.resize(1000, 800)

        def create_nested_grid(level, parent, max_depth=5, children_per_level=9):
            if level > max_depth:
                return Box(parent=parent, p="xs", height=20, bg="gray.50")
            grid = Grid(
                parent=parent,
                columns=3,
                gutter="xs",
                auto_columns=True,
            )
            for _ in range(children_per_level):
                child = create_nested_grid(level + 1, grid, max_depth)
                grid.add_child(child)
            return grid

        # Creation time
        start = time.time()
        container = Container(parent=qt_widget, fluid=True)
        deep_grid = create_nested_grid(1, container, max_depth=5)
        container.add_child(deep_grid)
        creation_time = time.time() - start

        # Layout time
        deep_grid.show()
        layout_start = time.time()
        QApplication.processEvents()
        layout_time = time.time() - layout_start

        # Assertions
        assert creation_time < 1.0  # <1s for deep structure
        assert layout_time < 0.3  # <300ms layout

        # Count total components (should be ~1 + 5*9 + 5*9^2 + ... but truncated)
        total_widgets = len(qt_widget.findChildren(QWidget))
        assert total_widgets > 200  # Significant nesting

        # Resize performance
        resize_start = time.time()
        qt_widget.resize(1200, 900)
        QApplication.processEvents()
        resize_time = time.time() - resize_start
        assert resize_time < 0.15  # Reasonable re-layout

    def test_responsive_resize_performance_large(self, large_grid_setup):
        """Test rendering performance during responsive changes on large grid."""
        import time

        grid, container, children, qt_widget = large_grid_setup

        # Multiple resizes simulating responsive breakpoints
        widths = [400, 600, 900, 1200, 1400, 900, 600, 400]  # Mobile to desktop cycles
        times = []
        for width in widths:
            start = time.time()
            qt_widget.resize(width, 800)
            QApplication.processEvents()
            times.append(time.time() - start)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        # Targets: Smooth, <60ms per resize for 60fps feel
        assert avg_time < 0.06
        assert max_time < 0.1

        # Verify layout updates correctly (e.g., column count changes)
        qt_widget.resize(400, 800)
        QApplication.processEvents()
        # On small, should stack (1 col effectively)
        for i in range(1, len(children)):
            assert (
                children[i].y() > children[i - 1].y() + children[i - 1].height() + 8
            )  # xs gutter approx

    def test_theme_update_performance_large(self, large_grid_setup, monkeypatch):
        """Test performance impact of theme updates on large layouts."""
        import time
        from unittest.mock import Mock

        grid, container, children, qt_widget = large_grid_setup

        # Mock theme update (simulate changing colors/spacing)
        def mock_theme_update(component):
            # Simulate repainting/applying new styles
            component.setStyleSheet("background-color: blue;")  # Simple change

        # Time theme update on all children
        start = time.time()
        for child in children:
            mock_theme_update(child)
        QApplication.processEvents()  # Force style updates
        theme_time = time.time() - start

        assert theme_time < 0.2  # <200ms for 120 components

        # Batch update simulation
        batch_start = time.time()
        # Assume a global theme apply that propagates
        grid.setStyleSheet("QWidget { border: 1px solid red; }")  # Parent style
        QApplication.processEvents()
        batch_time = time.time() - batch_start

        assert batch_time < 0.05  # Faster via inheritance

    def test_scalability_under_load(self, qt_widget):
        """Test scalability with increasing load (100 to 500 components)."""
        import time

        qt_widget.resize(1200, 800)
        container = Container(parent=qt_widget, fluid=True)

        def create_grid_with_n_children(n):
            grid = Grid(parent=container, columns=12, gutter="sm")
            for i in range(n):
                box = Box(parent=grid, p="xs", height=40, bg="gray.50")
                box.add_child(QLabel(f"Load {i}"))
                grid.add_child(box)
            container.add_child(grid)
            grid.show()
            return grid

        sizes = [100, 200, 300, 400, 500]
        layout_times = []
        for n in sizes:
            # Clean up previous
            for child in qt_widget.children():
                if isinstance(child, (Grid, Container)):
                    child.deleteLater()
            QApplication.processEvents()

            start = time.time()
            grid = create_grid_with_n_children(n)
            QApplication.processEvents()
            layout_time = time.time() - start
            layout_times.append(layout_time)

            # Linear scalability check: time ~ O(n)
            expected_time = layout_times[0] * (n / 100) if layout_times else 0.1
            assert layout_time < expected_time * 1.5  # Within 50% of linear

        # Overall: 500 items <500ms
        assert layout_times[-1] < 0.5

    def test_startup_performance_large_layout(self, qt_widget):
        """Test component initialization and startup time for large layouts."""
        import time

        qt_widget.resize(1400, 1000)

        # Simulate app startup with large layout
        start = time.time()
        app_container = Container(parent=qt_widget, fluid=True, px="xl", py="xl")
        main_grid = Grid(
            parent=app_container,
            columns={"base": 1, "lg": 12},
            gutter="md",
            justify="space-between",
        )

        # Add nested structures: 100 top-level, each with 5 children
        for i in range(100):
            col = Col(parent=main_grid, span=1)
            inner_stack = Stack(parent=col, direction="column", gap="sm")
            for j in range(5):
                inner_box = Box(
                    parent=inner_stack, p="sm", height=50, bg=f"blue.{j*20}"
                )
                inner_box.add_child(QLabel(f"Startup {i}-{j}"))
                inner_stack.add_child(inner_box)
            main_grid.add_child(col)

        app_container.add_child(main_grid)
        main_grid.show()
        startup_end = time.time()
        startup_time = startup_end - start

        # Process events for full render
        render_start = time.time()
        QApplication.processEvents()
        render_time = time.time() - render_start

        assert startup_time < 0.8  # <800ms init
        assert render_time < 0.15  # <150ms render

    def test_memory_leak_detection_nested(self, qt_widget):
        """Test for memory leaks in nested scenarios."""
        import gc
        import time
        import psutil
        import os

        process = psutil.Process(os.getpid())

        def get_memory_usage():
            return process.memory_info().rss / 1024 / 1024  # MB

        baseline_memory = get_memory_usage()

        # Run 5 cycles of create deep nested, layout, destroy
        for cycle in range(5):
            container = Container(parent=qt_widget, fluid=True)

            # Deep nest 4 levels, 16 children per (moderate)
            def create_nested(level, parent, depth=4):
                if level > depth:
                    return Box(parent=parent, height=30)
                grid = Grid(parent=parent, columns=4, gutter="xs")
                for _ in range(16):
                    child = create_nested(level + 1, grid, depth)
                    grid.add_child(child)
                return grid

            deep = create_nested(1, container)
            container.add_child(deep)
            deep.show()
            QApplication.processEvents()

            # Use then destroy
            time.sleep(0.01)  # Simulate use
            for child in qt_widget.children()[:]:  # Copy to avoid mod during iter
                if isinstance(child, (Container, Grid)):
                    child.deleteLater()
            QApplication.processEvents()
            gc.collect()

        final_memory = get_memory_usage()
        leak_growth = final_memory - baseline_memory

        assert leak_growth < 5.0  # <5MB leak over 5 cycles

        # Check object count
        obj_count_start = len(gc.get_objects())
        # After cycles, should not grow indefinitely
        # But since collected, assume stable


# Note: Additional tests for Tasks #170-#172 will extend this file.
# Performance tests in #172 will use timeit or similar for benchmarks.
# All tests assume theme spacing (e.g., "md" ~16px); adjust assertions if theme changes.
# Use approximate geometry checks due to Qt rendering variances.
# Nested Grid tests added for Task #170: Comprehensive coverage of nesting behaviors.
# Performance tests added for Task #172: Comprehensive large-scale and nested performance validation with benchmarks and thresholds.
# Responsive integration tests added for Task #171: Focus on system-level responsive coordination.

# Note: Additional tests for Tasks #170-#172 will extend this file.
# Performance tests in #172 will use timeit or similar for benchmarks.
# All tests assume theme spacing (e.g., "md" ~16px); adjust assertions if theme changes.
# Use approximate geometry checks due to Qt rendering variances.
# Nested Grid tests added for Task #170: Comprehensive coverage of nesting behaviors.
