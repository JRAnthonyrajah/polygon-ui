"""
Responsive design system for Polygon UI layout components.

Provides breakpoint management, responsive props handling, and
window resize monitoring for adaptive layouts.
"""

from typing import Dict, Any, Optional, Union, Callable
from enum import Enum
from PySide6.QtCore import QObject, Signal, QTimer, QEvent
from PySide6.QtWidgets import QWidget


class Breakpoint(Enum):
    """Responsive breakpoints following mobile-first design."""

    BASE = "base"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"


class BreakpointSystem:
    """
    Manages responsive breakpoints and provides utilities for
    responsive design calculations.
    """

    # Standard breakpoint widths in pixels
    BREAKPOINTS = {
        Breakpoint.BASE: 0,
        Breakpoint.SM: 576,
        Breakpoint.MD: 768,
        Breakpoint.LG: 992,
        Breakpoint.XL: 1200,
    }

    @classmethod
    def get_breakpoint_for_width(cls, width: int) -> Breakpoint:
        """
        Get the breakpoint for a given width.

        Args:
            width: Width in pixels

        Returns:
            The largest breakpoint that fits the width
        """
        current_bp = Breakpoint.BASE
        for bp in [Breakpoint.SM, Breakpoint.MD, Breakpoint.LG, Breakpoint.XL]:
            if width >= cls.BREAKPOINTS[bp]:
                current_bp = bp

        return current_bp

    @classmethod
    def get_min_width(cls, breakpoint: Breakpoint) -> int:
        """
        Get the minimum width for a breakpoint.

        Args:
            breakpoint: The breakpoint

        Returns:
            Minimum width in pixels
        """
        return cls.BREAKPOINTS[breakpoint]

    @classmethod
    def breakpoint_ge(cls, bp1: Breakpoint, bp2: Breakpoint) -> bool:
        """
        Check if breakpoint 1 is greater than or equal to breakpoint 2.

        Args:
            bp1: First breakpoint
            bp2: Second breakpoint

        Returns:
            True if bp1 >= bp2
        """
        bp_order = [
            Breakpoint.BASE,
            Breakpoint.SM,
            Breakpoint.MD,
            Breakpoint.LG,
            Breakpoint.XL,
        ]
        return bp_order.index(bp1) >= bp_order.index(bp2)

    @classmethod
    def breakpoint_le(cls, bp1: Breakpoint, bp2: Breakpoint) -> bool:
        """
        Check if breakpoint 1 is less than or equal to breakpoint 2.

        Args:
            bp1: First breakpoint
            bp2: Second breakpoint

        Returns:
            True if bp1 <= bp2
        """
        bp_order = [
            Breakpoint.BASE,
            Breakpoint.SM,
            Breakpoint.MD,
            Breakpoint.LG,
            Breakpoint.XL,
        ]
        return bp_order.index(bp1) <= bp_order.index(bp2)


class ResponsiveProps:
    """
    Handles responsive property values that can vary by breakpoint.
    """

    def __init__(self, widget: QWidget):
        self._widget = widget
        self._props: Dict[str, Union[Any, Dict[str, Any]]] = {}
        self._cached_values: Dict[str, Any] = {}
        self._current_breakpoint: Optional[Breakpoint] = None

    def set(self, prop_name: str, value: Union[Any, Dict[str, Any]]) -> None:
        """
        Set a responsive property.

        Args:
            prop_name: Name of the property
            value: Either a single value or dict of breakpoint values
                  e.g., {"base": 1, "sm": 2, "md": 3}
        """
        self._props[prop_name] = value
        self._invalidate_cache(prop_name)

    def get(self, prop_name: str, default: Any = None) -> Any:
        """
        Get the current value for a responsive property.

        Args:
            prop_name: Name of the property
            default: Default value if property is not set

        Returns:
            The value for the current breakpoint or default
        """
        # Check cache first
        if prop_name in self._cached_values:
            return self._cached_values[prop_name]

        if prop_name not in self._props:
            return default

        value = self._props[prop_name]
        result = self._resolve_value(value)

        # Cache the result
        self._cached_values[prop_name] = result
        return result

    def _resolve_value(self, value: Union[Any, Dict[str, Any]]) -> Any:
        """
        Resolve a responsive value to a concrete value for current breakpoint.

        Args:
            value: Either a single value or dict of breakpoint values

        Returns:
            Resolved value for current breakpoint
        """
        if not isinstance(value, dict):
            return value

        current_bp = BreakpointSystem.get_breakpoint_for_width(self._widget.width())

        # Find the best matching breakpoint value
        # Start with the exact match or closest smaller breakpoint
        result = None
        for bp in [
            Breakpoint.XL,
            Breakpoint.LG,
            Breakpoint.MD,
            Breakpoint.SM,
            Breakpoint.BASE,
        ]:
            if bp in value and BreakpointSystem.breakpoint_le(bp, current_bp):
                result = value[bp]
                break

        # If no smaller breakpoint found, use the smallest available
        if result is None:
            bp_order = [
                Breakpoint.BASE,
                Breakpoint.SM,
                Breakpoint.MD,
                Breakpoint.LG,
                Breakpoint.XL,
            ]
            for bp in bp_order:
                if bp in value:
                    result = value[bp]
                    break

        return result

    def update_breakpoint(self, breakpoint: Breakpoint) -> None:
        """
        Update the current breakpoint and invalidate cache if changed.

        Args:
            breakpoint: The new current breakpoint
        """
        if self._current_breakpoint != breakpoint:
            self._current_breakpoint = breakpoint
            self._invalidate_all_cache()

    def _invalidate_cache(self, prop_name: str) -> None:
        """Invalidate cache for a specific property."""
        self._cached_values.pop(prop_name, None)

    def _invalidate_all_cache(self) -> None:
        """Invalidate all cached values."""
        self._cached_values.clear()


class ResponsiveMixin(QObject):
    """
    Mixin class that adds responsive functionality to Qt widgets.

    Provides automatic breakpoint detection and responsive prop handling.
    """

    # Signal emitted when breakpoint changes
    breakpoint_changed = Signal(Breakpoint)

    def __init__(self):
        super().__init__()
        self._responsive_props = (
            ResponsiveProps(self) if isinstance(self, QWidget) else None
        )
        self._current_breakpoint: Optional[Breakpoint] = None
        self._resize_timer = QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self._handle_resize_timeout)

        # Callback registry for breakpoint changes
        self._breakpoint_callbacks: List[Callable[[Breakpoint], None]] = []

    def set_responsive_prop(
        self, prop_name: str, value: Union[Any, Dict[str, Any]]
    ) -> None:
        """
        Set a responsive property that can vary by breakpoint.

        Args:
            prop_name: Name of the property
            value: Either a single value or dict of breakpoint values
        """
        if self._responsive_props:
            self._responsive_props.set(prop_name, value)

    def get_responsive_value(self, prop_name: str, default: Any = None) -> Any:
        """
        Get the current value for a responsive property.

        Args:
            prop_name: Name of the responsive property
            default: Default value if property is not set

        Returns:
            The value for the current breakpoint or default
        """
        if self._responsive_props:
            return self._responsive_props.get(prop_name, default)
        return default

    def add_breakpoint_callback(self, callback: Callable[[Breakpoint], None]) -> None:
        """
        Add a callback that will be called when the breakpoint changes.

        Args:
            callback: Function to call with new breakpoint
        """
        self._breakpoint_callbacks.append(callback)

    def remove_breakpoint_callback(
        self, callback: Callable[[Breakpoint], None]
    ) -> None:
        """
        Remove a breakpoint callback.

        Args:
            callback: Function to remove
        """
        if callback in self._breakpoint_callbacks:
            self._breakpoint_callbacks.remove(callback)

    def get_current_breakpoint(self) -> Breakpoint:
        """
        Get the current breakpoint based on widget width.

        Returns:
            Current breakpoint
        """
        if isinstance(self, QWidget):
            return BreakpointSystem.get_breakpoint_for_width(self.width())
        return Breakpoint.BASE

    def _check_breakpoint_change(self) -> None:
        """Check if breakpoint has changed and emit signals if needed."""
        if not isinstance(self, QWidget):
            return

        new_breakpoint = self.get_current_breakpoint()

        if self._current_breakpoint != new_breakpoint:
            old_breakpoint = self._current_breakpoint
            self._current_breakpoint = new_breakpoint

            # Update responsive props
            if self._responsive_props:
                self._responsive_props.update_breakpoint(new_breakpoint)

            # Emit signal
            self.breakpoint_changed.emit(new_breakpoint)

            # Call callbacks
            for callback in self._breakpoint_callbacks:
                try:
                    callback(new_breakpoint)
                except Exception:
                    # Log error but don't crash
                    pass

    def resizeEvent(self, event) -> None:
        """Handle resize events with debounced breakpoint checking."""
        super().resizeEvent(event) if hasattr(super(), "resizeEvent") else None

        # Debounce resize events to avoid excessive recalculations
        self._resize_timer.start(100)  # 100ms debounce

    def _handle_resize_timeout(self) -> None:
        """Handle debounced resize timeout."""
        self._check_breakpoint_change()


# Utility functions for responsive design
def responsive(value: Union[Any, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Helper function to create responsive values.

    Args:
        value: Either a single value or dict of breakpoint values

    Returns:
        Dict formatted for responsive props

    Examples:
        responsive(4)  # Same value for all breakpoints
        responsive({"base": 1, "sm": 2, "md": 3})
    """
    if not isinstance(value, dict):
        # Single value applies to all breakpoints
        return {"base": value}

    return value


def cols(**kwargs) -> Dict[str, int]:
    """
    Helper function to create responsive column specifications.

    Args:
        **kwargs: Column counts for different breakpoints

    Returns:
        Dict formatted for responsive columns

    Examples:
        cols(base=1, sm=2, md=3)  # 1 column on mobile, 2 on tablet, 3 on desktop
    """
    return kwargs


def spacing(**kwargs) -> Dict[str, str]:
    """
    Helper function to create responsive spacing specifications.

    Args:
        **kwargs: Spacing values for different breakpoints

    Returns:
        Dict formatted for responsive spacing

    Examples:
        spacing(base="sm", md="lg")  # Small spacing on mobile, large on desktop
    """
    return kwargs
