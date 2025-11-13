"""
Tests for the responsive design system.
"""

import pytest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QObject, QTimer
from PySide6.QtTest import QTest  # If needed for events

from polygon_ui.layout.core.responsive import (
    Breakpoint,
    BreakpointSystem,
    ResponsiveProps,
    responsive,
    cols,
    spacing,
)

from tests.layout.conftest import ResponsiveTestHelper


@pytest.fixture
def app():
    """Create QApplication for tests."""
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    return app


# Use qt_widget from conftest.py
# The responsive_helper fixture is now available


class TestBreakpointSystem:
    """Test the BreakpointSystem class."""

    def test_get_breakpoint_for_width(self):
        """Test breakpoint calculation for different widths."""
        assert BreakpointSystem.get_breakpoint_for_width(0) == Breakpoint.BASE
        assert BreakpointSystem.get_breakpoint_for_width(400) == Breakpoint.BASE
        assert BreakpointSystem.get_breakpoint_for_width(600) == Breakpoint.SM
        assert BreakpointSystem.get_breakpoint_for_width(800) == Breakpoint.MD
        assert BreakpointSystem.get_breakpoint_for_width(1000) == Breakpoint.LG
        assert BreakpointSystem.get_breakpoint_for_width(1400) == Breakpoint.XL

    def test_get_min_width(self):
        """Test getting minimum width for breakpoints."""
        assert BreakpointSystem.get_min_width(Breakpoint.BASE) == 0
        assert BreakpointSystem.get_min_width(Breakpoint.SM) == 576
        assert BreakpointSystem.get_min_width(Breakpoint.MD) == 768
        assert BreakpointSystem.get_min_width(Breakpoint.LG) == 992
        assert BreakpointSystem.get_min_width(Breakpoint.XL) == 1200

    def test_breakpoint_comparisons(self):
        """Test breakpoint comparison functions."""
        assert BreakpointSystem.breakpoint_ge(Breakpoint.LG, Breakpoint.MD)
        assert not BreakpointSystem.breakpoint_ge(Breakpoint.SM, Breakpoint.MD)
        assert BreakpointSystem.breakpoint_le(Breakpoint.SM, Breakpoint.MD)
        assert not BreakpointSystem.breakpoint_le(Breakpoint.XL, Breakpoint.LG)


class TestResponsiveProps:
    """Test the ResponsiveProps class."""

    def test_set_get_simple_value(self, widget):
        """Test setting and getting simple values."""
        props = ResponsiveProps(widget)
        props.set("gap", "md")
        assert props.get("gap") == "md"

    def test_set_get_responsive_value(self, widget):
        """Test setting and getting responsive values."""
        props = ResponsiveProps(widget)
        responsive_value = {"base": 1, "sm": 2, "md": 3}
        props.set("columns", responsive_value)

        # Mock widget width for testing
        widget.resize(800, 600)  # Should be MD breakpoint
        assert props.get("columns") == 3

    def test_default_value(self, widget):
        """Test getting default value when property not set."""
        props = ResponsiveProps(widget)
        assert props.get("nonexistent", "default") == "default"

    def test_cache_invalidation(self, widget):
        """Test cache invalidation on breakpoint changes."""
        props = ResponsiveProps(widget)
        responsive_value = {"base": 1, "sm": 2}
        props.set("test", responsive_value)

        # Get value to cache it
        widget.resize(400, 600)  # BASE breakpoint
        cached_value = props.get("test")

        # Change breakpoint and get new value
        widget.resize(600, 600)  # SM breakpoint
        new_value = props.get("test")

        assert cached_value == 1
        assert new_value == 2


class TestUtilityFunctions:
    """Test utility functions for responsive design."""

    def test_responsive_single_value(self):
        """Test responsive function with single value."""
        result = responsive(4)
        assert result == {"base": 4}

    def test_responsive_dict_value(self):
        """Test responsive function with dict value."""
        input_dict = {"base": 1, "sm": 2}
        result = responsive(input_dict)
        assert result == input_dict

    def test_cols_function(self):
        """Test cols utility function."""
        result = cols(base=1, sm=2, md=3)
        expected = {"base": 1, "sm": 2, "md": 3}
        assert result == expected

    def test_spacing_function(self):
        """Test spacing utility function."""
        result = spacing(base="sm", md="lg")
        expected = {"base": "sm", "md": "lg"}
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__])
