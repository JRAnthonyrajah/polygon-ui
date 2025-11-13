"""
Col component for Polygon UI layout system.

A column component for use within Grid layouts, providing span, offset, order, and positioning props.
Automatically integrates with Grid parent for layout properties.
Uses QVBoxLayout internally for child content arrangement.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps

try:
    from .grid import Grid
except ImportError:
    Grid = None  # Fallback if grid not available yet


class Col(LayoutComponent):
    """
    Col component that provides grid column functionality within a Grid parent.

    Supports span and offset for column width and positioning, with automatic integration when parented to a Grid.
    Uses responsive props for breakpoint-specific behavior.
    Internally uses QVBoxLayout for vertical arrangement of child content.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        span: Union[int, Dict[str, int]] = 1,
        offset: Union[int, Dict[str, int]] = 0,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_span(span)
        self._set_offset(offset)

        # Setup internal layout for children
        self._setup_layout()

        # Auto-integrate if parent is Grid
        self._auto_integrate_parent()

    def _setup_layout(self) -> None:
        """Set up the internal QVBoxLayout for child content."""
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)  # Can be made responsive later

    def _get_layout_props(self) -> Dict[str, Any]:
        """Get layout properties for Grid integration (colspan, offset, etc.)."""
        return {
            "colspan": self._responsive.get("span", 1),
            "offset": self._responsive.get("offset", 0),
            # order, etc. added in future tasks
        }

    def _auto_integrate_parent(self) -> None:
        """Auto-detect and integrate with Grid parent."""
        parent = self.parent()
        if parent and Grid and isinstance(parent, Grid):
            # Ensure in parent's children list
            if hasattr(parent, "_children") and self not in parent._children:
                parent._children.append(self)
            # Set layout props
            if hasattr(parent, "_child_layout_props"):
                parent._child_layout_props[self] = self._get_layout_props()
            # Trigger parent update
            if hasattr(parent, "_update_grid_layout"):
                parent._update_grid_layout()

    def setParent(self, parent: Optional[QWidget]) -> None:
        """Override setParent to auto-integrate with new Grid parent."""
        old_parent = self.parent()
        super().setParent(parent)
        # Revalidate properties with new parent context
        self._set_span(self._responsive.get("span", 1))
        self._set_offset(self._responsive.get("offset", 0))
        if parent != old_parent and parent and Grid and isinstance(parent, Grid):
            self._auto_integrate_parent()

    def _update_responsive_props(self) -> None:
        """Update responsive properties and notify Grid parent if applicable."""
        super()._update_responsive_props()
        parent = self.parent()
        if parent and Grid and isinstance(parent, Grid):
            if hasattr(parent, "_child_layout_props"):
                parent._child_layout_props[self] = self._get_layout_props()
            if hasattr(parent, "_update_grid_layout"):
                parent._update_grid_layout()

    def _set_span(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set span with validation against parent Grid columns."""
        parent = self.parent()
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)
        else:
            max_cols = 12

        def validate_span(v):
            if not isinstance(v, int) or v < 1:
                return 1
            return min(v, max_cols)

        if isinstance(value, int):
            validated_value = validate_span(value)
        elif isinstance(value, dict):
            validated_value = {k: validate_span(v) for k, v in value.items()}
        else:
            validated_value = 1

        self._responsive.set("span", validated_value)

    def _validate_offset_config(
        self, value: Union[int, Dict[str, int]]
    ) -> Union[int, Dict[str, int]]:
        """Validate and clamp offset config against current span and max columns."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)
        span_config = self._responsive.get("span", 1)

        def validate_for_key(v: int, key: str) -> int:
            if not isinstance(v, int) or v < 0:
                return 0
            span_v = (
                span_config if isinstance(span_config, int) else span_config.get(key, 1)
            )
            max_possible = max_cols - span_v
            return min(v, max_possible)

        if isinstance(value, int):
            return validate_for_key(value, "base")
        elif isinstance(value, dict):
            return {
                k: validate_for_key(vv, k)
                for k, vv in value.items()
                if isinstance(vv, (int, float))
            }
        return 0

    def _set_offset(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set offset with validation against parent Grid columns and current span."""
        validated = self._validate_offset_config(value)
        self._responsive.set("offset", validated)

    def _revalidate_offset(self) -> None:
        """Revalidate current offset config after span or parent changes."""
        current = self._responsive.get("offset", 0)
        validated = self._validate_offset_config(current)
        self._responsive.set("offset", validated)

    # Col Properties (integrated with responsive system)

    @Property(object)
    def span(self) -> Union[int, Dict[str, int]]:
        """Get the current column span (responsive)."""
        return self._responsive.get("span", 1)

    @span.setter
    def span(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the column span (responsive)."""
        self._set_span(value)
        self._revalidate_offset()
        self._update_responsive_props()

    @Property(object)
    def offset(self) -> Union[int, Dict[str, int]]:
        """Get the current column offset (responsive)."""
        return self._responsive.get("offset", 0)

    @offset.setter
    def offset(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the column offset (responsive)."""
        self._set_offset(value)
        self._update_responsive_props()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props."""
        super().resizeEvent(event)
        self._update_responsive_props()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the Col's internal layout."""
        super().add_child(child, **layout_props)
        # Since internal layout is QVBoxLayout, add to it
        if self._layout:
            self._layout.addWidget(child)
