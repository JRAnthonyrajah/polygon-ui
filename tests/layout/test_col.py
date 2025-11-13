import pytest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
import sys

from pytestqt.qtbot import QtBot

from polygon_ui.layout.components.col import Col
from polygon_ui.layout.components.grid import Grid  # Assuming Grid exists


@pytest.fixture(scope="session")
def qtbot(qtbot):
    return qtbot


class TestCol:
    @pytest.fixture
    def col(self):
        app = QApplication.instance() or QApplication(sys.argv)
        return Col()

    @pytest.fixture
    def grid_parent(self):
        app = QApplication.instance() or QApplication(sys.argv)
        grid = Grid()
        return grid

    def test_init_default(self, col):
        assert col.span == 12
        assert col.offset == 0
        assert col.order == 0
        assert col.visible is True
        assert col.min_width == 0
        assert col.max_width is None

    def test_span_setter_int(self, col):
        col.span = 6
        assert col.span == {"base": 6, "sm": 6, "md": 6, "lg": 6, "xl": 6}

    def test_span_setter_dict(self, col):
        col.span = {"base": 12, "md": 6}
        assert col.span["base"] == 12
        assert col.span["md"] == 6
        assert col.span["sm"] == 12  # Inherits from base
        assert col.span["lg"] == 6  # Inherits from md
        assert col.span["xl"] == 6

    def test_span_validation(self, col):
        col.span = 13  # Should clamp to 12 if no parent
        assert col.span["base"] == 12
        col.span = 0
        assert col.span["base"] == 1  # Min 1

    def test_offset_setter_int(self, col):
        col.offset = 3
        assert col.offset == {"base": 3, "sm": 3, "md": 3, "lg": 3, "xl": 3}

    def test_offset_setter_dict(self, col):
        col.offset = {"base": 0, "md": 2}
        assert col.offset["base"] == 0
        assert col.offset["md"] == 2
        assert col.offset["sm"] == 0  # Inherits
        assert col.offset["lg"] == 2

    def test_offset_validation_with_span(self, col):
        col.span = 6
        col.offset = 7  # Should clamp to 6 (12-6)
        assert col.offset["base"] == 6

    def test_order_setter(self, col):
        col.order = 2
        assert col.order == 2
        col.order = {"md": 1}
        assert col.order["md"] == 1
        assert col.order["base"] == 0  # Default

    def test_order_validation(self, col):
        col.order = -1
        assert col.order == 0
        col.order = 101
        assert col.order == 100  # Max 100

    def test_visible_setter(self, col, qtbot):
        col.visible = False
        assert not col.isVisible()
        col.visible = True
        assert col.isVisible()

    def test_visible_responsive(self, col, qtbot):
        col.visible = {"base": True, "md": False}
        # Simulate resize to md breakpoint (assume width > 768 for md)
        col.resize(800, 600)
        qtbot.wait(100)
        assert col.isVisible()  # Base true, but need mock for breakpoint
        # Note: Full breakpoint testing requires mocking BreakpointSystem

    def test_min_width_max_width(self, col, qtbot):
        col.min_width = 400
        col.max_width = 800
        col.resize(300, 600)  # Below min
        qtbot.wait(100)
        assert not col.isVisible()
        col.resize(500, 600)  # Within
        qtbot.wait(100)
        assert col.isVisible()
        col.resize(900, 600)  # Above max
        qtbot.wait(100)
        assert not col.isVisible()

    def test_size_visibility_with_parent(self, grid_parent, qtbot):
        col = Col(parent=grid_parent)
        col.min_width = 200
        grid_parent.resize(100, 600)  # Parent small
        qtbot.addWidget(grid_parent)
        qtbot.wait(100)
        assert not col.isVisible()
        grid_parent.resize(300, 600)
        qtbot.wait(100)
        assert col.isVisible()

    def test_auto_integration_with_grid(self, grid_parent):
        col = Col(parent=grid_parent)
        assert hasattr(grid_parent, "_child_layout_props")
        assert col in grid_parent._child_layout_props
        props = grid_parent._child_layout_props[col]
        assert props["colspan"] == 12
        assert props["offset"] == 0

    def test_reparent_integration(self, grid_parent, qtbot):
        col = Col()
        old_parent = QWidget()
        col.setParent(old_parent)
        col.setParent(grid_parent)
        assert col.parent() == grid_parent
        # Check integration triggered
        assert (
            hasattr(grid_parent, "_child_layout_props")
            and col in grid_parent._child_layout_props
        )

    def test_convenience_methods(self, col):
        col.half_width()
        assert col.span["md"] == 6
        col.offset_center()
        assert col.offset["base"] == 0  # Full width, offset 0
        col.offset = 6
        col.offset_center()  # For span 6, offset 3
        assert col.offset["base"] == 3

    # Responsive behavior tests would require mocking resize and breakpoint system
    # For now, test prop resolution
    def test_responsive_resolution(self, col):
        col.span = {"base": 12, "sm": 6}
        # Assume current width 500 (sm breakpoint, assume sm starts at 480)
        # This requires patching BreakpointSystem.get_breakpoint_for_width
        # Mock for testing
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "sm",
            )
            resolved = col._get_layout_props()["colspan"]
            assert resolved == 6  # sm span

    def test_span_with_custom_grid_columns(self, grid_parent):
        """Test span validation with Grid parent having custom columns."""
        grid_parent.columns = 6  # Custom 6-column grid
        col = Col(parent=grid_parent, span=8)  # Should clamp to 6
        props = grid_parent._child_layout_props[col]
        assert props["colspan"] == 6  # Clamped

    def test_span_validation_edge_cases(self, col):
        """Test various edge cases for span validation."""
        col.span = -5  # Negative
        assert col.span["base"] == 1
        col.span = 0  # Zero
        assert col.span["base"] == 1
        col.span = 12  # Max
        assert col.span["base"] == 12
        col.span = {"xl": 13}  # Invalid for xl, should clamp to 12
        assert col.span["xl"] == 12

    def test_offset_validation_edge_cases(self, col):
        """Test offset validation without parent constraints."""
        col.span = 6
        col.offset = -1  # Negative
        assert col.offset["base"] == 0
        col.offset = 7  # > 12-6=6
        assert col.offset["base"] == 6
        col.offset = 6  # Valid max
        assert col.offset["base"] == 6
        col.offset = {"base": 0, "md": -2}  # Negative in dict
        assert col.offset["md"] == 0

    def test_offset_interaction_with_span_change(self, col):
        """Test that offset is revalidated when span changes."""
        col.span = 8
        col.offset = 3  # Valid for span 8 (max 4)
        assert col.offset["base"] == 3
        col.span = 4  # Smaller span, max offset now 8
        # Offset should remain 3 (no clamping needed)
        assert col.offset["base"] == 3
        col.span = 10
        col.offset = 4  # Was valid, but now max=2
        # Should clamp to 2 on revalidation
        col._revalidate_offset()
        assert col.offset["base"] == 2

    def test_span_offset_with_custom_columns(self, grid_parent):
        """Test span and offset with custom Grid columns."""
        grid_parent.columns = 8
        col = Col(parent=grid_parent, span=5, offset=2)
        props = grid_parent._child_layout_props[col]
        assert props["colspan"] == 5
        assert props["offset"] == 2  # Valid: 8-5=3 >2
        col.offset = 4  # Invalid: >3
        assert props["offset"] == 3  # Clamped

    def test_responsive_span_offset_interaction(self, col):
        """Test responsive span and offset interactions across breakpoints."""
        col.span = {"base": 12, "md": 6}
        col.offset = {"base": 0, "md": 3}
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props_base = col._get_layout_props()
            assert props_base["colspan"] == 12
            assert props_base["offset"] == 0
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props_md = col._get_layout_props()
            assert props_md["colspan"] == 6
            assert props_md["offset"] == 3  # Valid for span 6 (max 6)

        # Test invalid responsive offset
        col.offset = {"md": 7}  # Invalid for md span 6
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["offset"] == 6  # Clamped

    def test_responsive_span_mobile_first(self, col):
        """Test mobile-first span patterns across breakpoints."""
        col.span = {"base": 12, "md": 6, "lg": 4}

        # Test base (mobile)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12

        # Test md
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 6

        # Test lg
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "lg",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 4

        # Test xl (inherits from lg)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "xl",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 4  # Inherits from lg

    def test_responsive_offset_changes(self, col):
        """Test offset responsive changes across breakpoints."""
        col.offset = {"base": 0, "md": 2, "lg": 4}
        col.span = 6  # Fixed span for offset testing

        # Base
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["offset"] == 0

        # md
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["offset"] == 2

        # lg
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "lg",
            )
            props = col._get_layout_props()
            assert props["offset"] == 4

        # xl inherits lg
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "xl",
            )
            props = col._get_layout_props()
            assert props["offset"] == 4

    def test_responsive_order_changes(self, col):
        """Test order responsive changes across breakpoints."""
        col.order = {"base": 1, "md": 2, "lg": 3}

        # Base
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["order"] == 1

        # md
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["order"] == 2

        # lg
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "lg",
            )
            props = col._get_layout_props()
            assert props["order"] == 3

    def test_responsive_inheritance_patterns(self, col):
        """Test responsive inheritance (missing breakpoints inherit from previous)."""
        col.span = {"base": 12, "lg": 3}  # Missing sm, md, xl

        # Base
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12

        # sm (inherits base)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "sm",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12

        # md (inherits from sm/base)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12

        # lg
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "lg",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 3

        # xl (inherits lg)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "xl",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 3

    def test_complex_responsive_scenario(self, col):
        """Test complex responsive scenarios with multiple props changing."""
        col.span = {"base": 12, "sm": 6, "md": 4, "lg": 3, "xl": 2}
        col.offset = {"base": 0, "md": 1, "xl": 5}
        col.order = {"base": 0, "lg": 1}

        # Base: span=12, offset=0, order=0
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12
            assert props["offset"] == 0
            assert props["order"] == 0

        # sm: span=6, offset=0 (inherits), order=0 (inherits)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "sm",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 6
            assert props["offset"] == 0
            assert props["order"] == 0

        # md: span=4, offset=1, order=0
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 4
            assert props["offset"] == 1
            assert props["order"] == 0

        # lg: span=3, offset=1 (inherits), order=1
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "lg",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 3
            assert props["offset"] == 1
            assert props["order"] == 1

        # xl: span=2, offset=5, order=1 (inherits)
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "xl",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 2
            assert (
                props["offset"] == 5
            )  # Valid for span 2? Wait, max offset 10, but assuming 12-col
            assert props["order"] == 1

    def test_responsive_prop_validation(self, col):
        """Test responsive prop validation across breakpoints."""
        col.span = {"base": 13, "md": 0, "lg": -1}  # Invalid values
        col.offset = {"base": 13, "md": -1}

        # Base: span clamped to 12, offset to 0
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 12
            assert props["offset"] == 0  # Clamped

        # md: span to 1, offset to 0
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props = col._get_layout_props()
            assert props["colspan"] == 1
            assert props["offset"] == 0

    def test_responsive_with_grid_integration(self, grid_parent):
        """Test responsive Col behavior with Grid parent integration."""
        col1 = Col(parent=grid_parent, span={"base": 12, "md": 6})
        col2 = Col(parent=grid_parent, span={"base": 12, "md": 6})

        # Mock base
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            props1 = grid_parent._child_layout_props[col1]
            props2 = grid_parent._child_layout_props[col2]
            assert props1["colspan"] == 12
            assert props2["colspan"] == 12

        # Mock md - should update
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            # Trigger update by accessing props
            props1 = grid_parent._child_layout_props[col1]
            props2 = grid_parent._child_layout_props[col2]
            assert props1["colspan"] == 6
            assert props2["colspan"] == 6

        # Test offset in grid
        col3 = Col(parent=grid_parent, span=6, offset={"md": 3})
        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            props3 = grid_parent._child_layout_props[col3]
            assert props3["colspan"] == 6
            assert props3["offset"] == 3

    def test_responsive_transitions(self, col, qtbot):
        """Test responsive transitions and layout updates (basic)."""
        # This tests that changing breakpoint mock updates props
        # Full transition testing would require resize events, but here we test prop reactivity
        col.span = {"base": 12, "md": 6}

        with pytest.MonkeyPatch().context() as m:
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "base",
            )
            initial_props = col._get_layout_props()
            assert initial_props["colspan"] == 12

            # "Transition" by changing mock
            m.setattr(
                "polygon_ui.layout.core.responsive.BreakpointSystem.get_breakpoint_for_width",
                lambda w: "md",
            )
            updated_props = col._get_layout_props()
            assert updated_props["colspan"] == 6
