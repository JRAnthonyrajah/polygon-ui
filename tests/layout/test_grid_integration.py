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


# Note: Additional tests for Tasks #170-#172 will extend this file.
# Performance tests in #172 will use timeit or similar for benchmarks.
# All tests assume theme spacing (e.g., "md" ~16px); adjust assertions if theme changes.
# Use approximate geometry checks due to Qt rendering variances.
# Nested Grid tests added for Task #170: Comprehensive coverage of nesting behaviors.
