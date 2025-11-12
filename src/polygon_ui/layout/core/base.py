"""
Base classes for layout components in Polygon UI.
"""

from typing import Dict, Any, Optional, Union, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout, QGridLayout
from PySide6.QtCore import Qt, QMargins, Signal, Property

from ...core.component import PolygonComponent


class LayoutComponent(PolygonComponent):
    """
    Base class for all layout components in Polygon UI.

    Provides Qt layout management integration, responsive props handling,
    and enhanced styling capabilities for layout components.
    """

    def __init__(self, parent: Optional[QWidget] = None, **kwargs):
        super().__init__(parent, **kwargs)

        # Layout-specific properties
        self._children: List[QWidget] = []
        self._layout: Optional[QLayout] = None
        self._responsive_props: Dict[str, Any] = {}

        # Common layout props
        self._gap = kwargs.get("gap", "md")
        self._justify = kwargs.get("justify", "start")
        self._align = kwargs.get("align", "stretch")

        # Initialize layout
        self._setup_layout()

    def _setup_layout(self) -> None:
        """Set up the Qt layout for this component."""
        # Override in subclasses
        pass

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """
        Add a child widget to this layout component.

        Args:
            child: The widget to add
            **layout_props: Layout-specific properties for the child
        """
        if child not in self._children:
            self._children.append(child)

            # Apply layout properties if provided
            self._apply_child_layout_props(child, layout_props)

            # Add to Qt layout
            if self._layout:
                self._layout.addWidget(child)
            else:
                # Fallback to direct parenting
                child.setParent(self)

    def remove_child(self, child: QWidget) -> None:
        """
        Remove a child widget from this layout component.

        Args:
            child: The widget to remove
        """
        if child in self._children:
            self._children.remove(child)

            if self._layout:
                self._layout.removeWidget(child)
            else:
                child.setParent(None)

    def _apply_child_layout_props(self, child: QWidget, props: Dict[str, Any]) -> None:
        """
        Apply layout-specific properties to a child widget.

        Args:
            child: The child widget
            props: Layout properties to apply
        """
        # Override in subclasses to implement specific layout logic
        pass

    def set_responsive_prop(self, prop_name: str, value: Union[Any, Dict[str, Any]]) -> None:
        """
        Set a responsive property that can vary by breakpoint.

        Args:
            prop_name: Name of the property
            value: Either a single value or a dict of breakpoint values
              e.g., {"base": 1, "sm": 2, "md": 3}
        """
        self._responsive_props[prop_name] = value
        self._update_responsive_props()

    def get_responsive_value(self, prop_name: str, default: Any = None) -> Any:
        """
        Get the current value for a responsive property based on current breakpoint.

        Args:
            prop_name: Name of the responsive property
            default: Default value if property is not set

        Returns:
            The value for the current breakpoint or default
        """
        if prop_name not in self._responsive_props:
            return default

        value = self._responsive_props[prop_name]

        if isinstance(value, dict):
            # Get value for current breakpoint
            current_breakpoint = self._get_current_breakpoint()

            # Find the best matching breakpoint value
            for bp in ["xl", "lg", "md", "sm", "base"]:
                if bp in value and (bp == current_breakpoint or
                                  self._breakpoint_ge(bp, current_breakpoint)):
                    return value[bp]

            # Fallback to first available value
            return next(iter(value.values()))

        return value

    def _get_current_breakpoint(self) -> str:
        """
        Get the current breakpoint based on widget width.

        Returns:
            Current breakpoint: "base", "sm", "md", "lg", or "xl"
        """
        # Define breakpoints
        breakpoints = {
            "base": 0,
            "sm": 576,
            "md": 768,
            "lg": 992,
            "xl": 1200
        }

        width = self.width()

        # Find the largest breakpoint that fits
        current_bp = "base"
        for bp_name, bp_width in breakpoints.items():
            if width >= bp_width:
                current_bp = bp_name

        return current_bp

    def _breakpoint_ge(self, bp1: str, bp2: str) -> bool:
        """
        Check if breakpoint 1 is greater than or equal to breakpoint 2.

        Args:
            bp1: First breakpoint
            bp2: Second breakpoint

        Returns:
            True if bp1 >= bp2
        """
        bp_order = ["base", "sm", "md", "lg", "xl"]
        return bp_order.index(bp1) >= bp_order.index(bp2)

    def _update_responsive_props(self) -> None:
        """Update all responsive properties based on current breakpoint."""
        # Override in subclasses to handle responsive updates
        pass

    # Property setters/getters for common layout props
    @Property(str)
    def gap(self) -> str:
        """Get the gap spacing."""
        return self._gap

    @gap.setter
    def gap(self, value: str) -> None:
        """Set the gap spacing."""
        self._gap = value
        self._update_layout_styling()

    @Property(str)
    def justify(self) -> str:
        """Get the justify content alignment."""
        return self._justify

    @justify.setter
    def justify(self, value: str) -> None:
        """Set the justify content alignment."""
        self._justify = value
        self._update_layout_styling()

    @Property(str)
    def align(self) -> str:
        """Get the align items."""
        return self._align

    @align.setter
    def align(self, value: str) -> None:
        """Set the align items."""
        self._align = value
        self._update_layout_styling()

    def _update_layout_styling(self) -> None:
        """Update the layout styling based on current properties."""
        if not self._provider:
            return

        # Convert gap to pixels based on theme spacing
        if hasattr(self._provider, 'get_theme_value'):
            gap_pixels = self._provider.get_theme_value(f"spacing.{self._gap}", 8)
        else:
            gap_pixels = 8  # Fallback

        # Apply spacing to layout
        if self._layout:
            if isinstance(self._layout, (QVBoxLayout, QHBoxLayout)):
                self._layout.setSpacing(gap_pixels)
            elif isinstance(self._layout, QGridLayout):
                self._layout.setSpacing(gap_pixels)

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive properties."""
        super().resizeEvent(event)
        self._update_responsive_props()


class GridComponent(LayoutComponent):
    """
    Base class for grid-based layout components.

    Extends LayoutComponent with grid-specific functionality including
    spans, offsets, and responsive grid behavior.
    """

    def __init__(self, parent: Optional[QWidget] = None, **kwargs):
        super().__init__(parent, **kwargs)

        # Grid-specific properties
        self._columns = kwargs.get("columns", 12)
        self._gutter = kwargs.get("gutter", "md")

    @Property(int)
    def columns(self) -> int:
        """Get the number of grid columns."""
        return self._columns

    @columns.setter
    def columns(self, value: int) -> None:
        """Set the number of grid columns."""
        self._columns = value
        self._update_grid_layout()

    @Property(str)
    def gutter(self) -> str:
        """Get the gutter spacing."""
        return self._gutter

    @gutter.setter
    def gutter(self, value: str) -> None:
        """Set the gutter spacing."""
        self._gutter = value
        self._update_grid_layout()

    def _update_grid_layout(self) -> None:
        """Update the grid layout based on current properties."""
        # Override in subclasses to implement grid-specific logic
        pass


class UtilityComponent(LayoutComponent):
    """
    Base class for utility layout components.

    Provides simplified layout behavior for utility components like
    Center, AspectRatio, Paper, etc.
    """

    def __init__(self, parent: Optional[QWidget] = None, **kwargs):
        super().__init__(parent, **kwargs)

        # Utility-specific properties
        self._inline = kwargs.get("inline", False)
        self._fluid = kwargs.get("fluid", False)

    @Property(bool)
    def inline(self) -> bool:
        """Get whether the component should display inline."""
        return self._inline

    @inline.setter
    def inline(self, value: bool) -> None:
        """Set whether the component should display inline."""
        self._inline = value
        self._update_utility_styling()

    @Property(bool)
    def fluid(self) -> bool:
        """Get whether the component should be fluid (max-width: none)."""
        return self._fluid

    @fluid.setter
    def fluid(self, value: bool) -> None:
        """Set whether the component should be fluid."""
        self._fluid = value
        self._update_utility_styling()

    def _update_utility_styling(self) -> None:
        """Update utility-specific styling."""
        # Override in subclasses to implement utility-specific logic
        pass