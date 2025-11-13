"""
Col component for Polygon UI layout system.

A column component for use within Grid layouts, providing span, offset, order, and positioning props.
Automatically integrates with Grid parent for layout properties.
Uses QVBoxLayout internally for child content arrangement.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Property, QTimer

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps, BreakpointSystem

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
        span: Union[int, Dict[str, int]] = 12,
        offset: Union[int, Dict[str, int]] = 0,
        order: Union[int, Dict[str, int]] = 0,
        visible: Union[bool, Dict[str, bool]] = True,
        min_width: Union[int, Dict[str, int]] = 0,
        max_width: Union[int, Dict[str, Optional[int]]] = None,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_span(span)
        self._set_offset(offset)
        self._set_order(order)
        self._set_visible(visible)
        self._set_min_width(min_width)
        self._set_max_width(max_width)

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
        """Get layout properties for Grid integration (colspan, offset, order, etc.)."""

        def resolve_prop(prop_name, default):
            val = self._responsive.get(prop_name, default)
            if isinstance(val, dict):
                current_bp = BreakpointSystem.get_breakpoint_for_width(self.width())
                return self._responsive._resolve_value(val)
            return val

        resolved_span = resolve_prop("span", {"base": 12})
        resolved_offset = resolve_prop("offset", {"base": 0})
        resolved_order = resolve_prop("order", {"base": 0})

        return {
            "colspan": resolved_span,
            "offset": resolved_offset,
            "order": resolved_order,
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
        self._set_order(self._responsive.get("order", 0))
        if parent != old_parent and parent and Grid and isinstance(parent, Grid):
            self._auto_integrate_parent()

    def _update_responsive_props(self) -> None:
        """Update responsive properties and notify Grid parent if applicable."""
        super()._update_responsive_props()
        # Invalidate cache to ensure fresh resolution
        if hasattr(self._responsive, "_invalidate_all_cache"):
            self._responsive._invalidate_all_cache()
        parent = self.parent()
        if parent and Grid and isinstance(parent, Grid):
            if hasattr(parent, "_child_layout_props"):
                parent._child_layout_props[self] = self._get_layout_props()
            if hasattr(parent, "_update_grid_layout"):
                parent._update_grid_layout()
        # Update visibility based on responsive props
        resolved_visible = self._responsive._resolve_value(
            self._responsive.get("visible", True)
        )
        self.setVisible(resolved_visible)
        # Smooth transition: slight delay for layout update if needed
        QTimer.singleShot(
            50,
            lambda: self.updateGeometry() if hasattr(self, "updateGeometry") else None,
        )

    def _set_span(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set span with validation against parent Grid columns and inheritance."""
        parent = self.parent()
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)
        else:
            max_cols = 12

        def validate_span(v):
            if not isinstance(v, int) or v < 1:
                return 1
            return min(v, max_cols)

        # Normalize to full breakpoint dict with inheritance (mobile-first)
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_span = {}
        current_span = 12  # Default base span for full width on mobile

        if isinstance(value, int):
            current_span = validate_span(value)
            full_span = {bp: current_span for bp in breakpoints_order}
        elif isinstance(value, dict):
            # Start with default base if not specified
            if "base" not in value:
                current_span = 12
            else:
                current_span = validate_span(value.get("base", 12))
            full_span["base"] = current_span

            # Propagate forward with inheritance for larger breakpoints
            for bp in breakpoints_order[1:]:  # Skip base
                if bp in value:
                    current_span = validate_span(value[bp])
                full_span[bp] = current_span
        else:
            full_span = {bp: 12 for bp in breakpoints_order}

        # Ensure all values are validated
        for bp in breakpoints_order:
            full_span[bp] = validate_span(full_span[bp])

        self._responsive.set("span", full_span)

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
        """Private method to set offset with validation against parent Grid columns and current span.
        Normalizes to full breakpoint dict with mobile-first inheritance."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)

        # Get current span config for validation
        span_config = self._responsive.get(
            "span", {bp: 12 for bp in ["base", "sm", "md", "lg", "xl"]}
        )

        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_offset = {}
        current_offset = 0  # Default base offset

        if isinstance(value, int):
            current_offset = value
            full_offset = {bp: current_offset for bp in breakpoints_order}
        elif isinstance(value, dict):
            # Base
            if "base" not in value:
                current_offset = 0
            else:
                current_offset = value.get("base", 0)
            full_offset["base"] = current_offset

            # Inherit forward for larger breakpoints
            for bp in breakpoints_order[1:]:
                if bp in value:
                    current_offset = value[bp]
                full_offset[bp] = current_offset
        else:
            full_offset = {bp: 0 for bp in breakpoints_order}

        # Validate each breakpoint's offset against corresponding span
        def validate_offset_for_bp(bp: str, off: int) -> int:
            if not isinstance(off, int) or off < 0:
                return 0
            span_bp = (
                span_config.get(bp, 12)
                if isinstance(span_config, dict)
                else span_config
            )
            max_off = max_cols - span_bp
            return min(off, max_off)

        validated_full = {
            bp: validate_offset_for_bp(bp, off) for bp, off in full_offset.items()
        }

        self._responsive.set("offset", validated_full)
        self._update_responsive_props()

    def _revalidate_offset(self) -> None:
        """Revalidate current offset config after span or parent changes."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)

        span_config = self._responsive.get("span", 12)
        current_offset = self._responsive.get("offset", 0)

        # Ensure current_offset is dict
        if isinstance(current_offset, int):
            current_offset = {
                bp: current_offset for bp in ["base", "sm", "md", "lg", "xl"]
            }

        # Validate each
        def validate(bp, off):
            if not isinstance(off, int) or off < 0:
                return 0
            span_bp = (
                span_config if isinstance(span_config, int) else span_config.get(bp, 12)
            )
            max_off = max_cols - span_bp
            return min(off, max_off)

        validated = {bp: validate(bp, off) for bp, off in current_offset.items()}
        self._responsive.set("offset", validated)

    def _validate_order_config(
        self, value: Union[int, Dict[str, int]]
    ) -> Union[int, Dict[str, int]]:
        """Validate order config to positive integers with reasonable upper bound."""
        MAX_ORDER = 100  # Reasonable upper bound for visual ordering

        def validate_order(v: int, key: str = "base") -> int:
            if not isinstance(v, int) or v < 0:
                return 0  # 0 means fallback to DOM order
            return min(v, MAX_ORDER)

        if isinstance(value, int):
            return validate_order(value)
        elif isinstance(value, dict):
            return {
                k: validate_order(vv, k)
                for k, vv in value.items()
                if isinstance(vv, (int, float))
            }
        return 0

    def _set_order(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set order with validation."""
        validated = self._validate_order_config(value)
        self._responsive.set("order", validated)

    def _set_visible(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Private method to set visibility with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_visible = {}

        if isinstance(value, bool):
            full_visible = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = True
            full_visible["base"] = value.get("base", True)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_visible[bp] = current
        else:
            full_visible = {bp: True for bp in breakpoints_order}

        self._responsive.set("visible", full_visible)

    def _set_min_width(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set min_width with responsive support (pixels)."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_min_width = {}

        if isinstance(value, int):
            full_min_width = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_min_width["base"] = value.get("base", 0)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_min_width[bp] = current
        else:
            full_min_width = {bp: 0 for bp in breakpoints_order}

        # Ensure non-negative
        for bp in breakpoints_order:
            full_min_width[bp] = max(0, full_min_width[bp])

        self._responsive.set("min_width", full_min_width)

    def _set_max_width(self, value: Union[int, Dict[str, Optional[int]]]) -> None:
        """Private method to set max_width with responsive support (pixels, None means no max)."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_max_width = {}

        if value is None:
            full_max_width = {bp: None for bp in breakpoints_order}
        elif isinstance(value, int):
            full_max_width = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = None
            full_max_width["base"] = value.get("base")
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_max_width[bp] = current
        else:
            full_max_width = {bp: None for bp in breakpoints_order}

        self._responsive.set("max_width", full_max_width)

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

    @Property(object)
    def order(self) -> Union[int, Dict[str, int]]:
        """Get the current visual order (responsive). Order 0 means fallback to DOM order."""
        return self._responsive.get("order", 0)

    @order.setter
    def order(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the visual order (responsive)."""
        self._set_order(value)
        self._update_responsive_props()

    @Property(bool)
    def visible(self) -> bool:
        """Get the current visibility state (resolved for current breakpoint)."""
        return self._responsive._resolve_value(self._responsive.get("visible", True))

    @visible.setter
    def visible(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the visibility (responsive)."""
        self._set_visible(value)
        self._update_responsive_props()

    @Property(object)
    def min_width(self) -> Union[int, Dict[str, int]]:
        """Get the current min_width constraint (responsive, in pixels)."""
        return self._responsive.get("min_width", 0)

    @min_width.setter
    def min_width(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the min_width constraint (responsive)."""
        self._set_min_width(value)
        self._update_responsive_props()

    @Property(object)
    def max_width(self) -> Union[int, Dict[str, Optional[int]]]:
        """Get the current max_width constraint (responsive, in pixels; None means no max)."""
        return self._responsive.get("max_width", None)

    @max_width.setter
    def max_width(self, value: Union[int, Dict[str, Optional[int]]]) -> None:
        """Set the max_width constraint (responsive)."""
        self._set_max_width(value)
        self._update_responsive_props()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props with smoothing."""
        super().resizeEvent(event)
        self._update_responsive_props()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the Col's internal layout."""
        super().add_child(child, **layout_props)
        # Since internal layout is QVBoxLayout, add to it
        if self._layout:
            self._layout.addWidget(child)

    def half_width(self) -> None:
        """Convenience method: Set span to 12 on base, 6 on md and larger."""
        self.span = {"base": 12, "sm": 12, "md": 6, "lg": 6, "xl": 6}

    def third_width(self) -> None:
        """Convenience method: Set span to 12 on base, 4 on md and larger."""
        self.span = {"base": 12, "sm": 12, "md": 4, "lg": 4, "xl": 4}

    def quarter_width(self) -> None:
        """Convenience method: Set span to 12 on base, 3 on md and larger."""
        self.span = {"base": 12, "sm": 12, "md": 3, "lg": 3, "xl": 3}

    def auto_width(self) -> None:
        """Convenience method: Set dynamic span based on content (fallback to 12)."""
        # For now, default to full width; advanced content-based calculation can be added later
        self.span = 12

    def offset_center(self) -> None:
        """Convenience method: Center the column responsively based on span and grid columns."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)

        span_config = self._responsive.get("span", 12)
        if isinstance(span_config, int):
            span_config = {bp: span_config for bp in ["base", "sm", "md", "lg", "xl"]}

        offset_config = {}
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        for bp in breakpoints_order:
            span_bp = span_config.get(bp, 12)
            offset_config[bp] = (max_cols - span_bp) // 2

        self.offset = offset_config

    def offset_right(self) -> None:
        """Convenience method: Move column to the right edge responsively."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)

        span_config = self._responsive.get("span", 12)
        if isinstance(span_config, int):
            span_config = {bp: span_config for bp in ["base", "sm", "md", "lg", "xl"]}

        offset_config = {}
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        for bp in breakpoints_order:
            span_bp = span_config.get(bp, 12)
            offset_config[bp] = max(0, max_cols - span_bp)

        self.offset = offset_config

    def offset_left(self) -> None:
        """Convenience method: Reset offset to 0 (left alignment) responsively."""
        self.offset = 0

    def offset_auto(self) -> None:
        """Convenience method: Dynamic offset based on span (center if not full width)."""
        parent = self.parent()
        max_cols = 12
        if parent and Grid and isinstance(parent, Grid):
            max_cols = getattr(parent, "columns", 12)

        span_config = self._responsive.get("span", 12)
        if isinstance(span_config, int):
            span_config = {bp: span_config for bp in ["base", "sm", "md", "lg", "xl"]}

        offset_config = {}
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        for bp in breakpoints_order:
            span_bp = span_config.get(bp, 12)
            if span_bp >= max_cols:
                offset_config[bp] = 0
            else:
                offset_config[bp] = (max_cols - span_bp) // 2  # Center as auto

        self.offset = offset_config
