"""
Flex component for Polygon UI layout system.

A flexible flexbox-like component using manual positioning and sizing with QWidget.resize() and move().
Supports direction, wrap, justify, align, gap, and child flex properties (grow, shrink, basis, order).
Implements custom flex layout without relying on Qt's built-in layouts for full flexbox control.
"""

from typing import Optional, Any, Dict, Union, List
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QRect, QSize

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Flex(LayoutComponent):
    """
    Flex component that provides flexbox-like layout behavior using manual positioning.
    Arranges children according to flex properties: direction, wrap, justify, align, gap.
    Child widgets can have individual flex properties: grow, shrink, basis, order, alignSelf.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        direction: Union[str, Dict[str, str]] = "row",
        wrap: Union[bool, str, Dict[str, Union[bool, str]]] = False,
        justify: str = "start",
        align: str = "stretch",
        gap: Union[str, int, Dict[str, Union[str, int]]] = "md",
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler (integrated with base class responsive support)
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("direction", direction)
        self._responsive.set("wrap", wrap)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)
        self._responsive.set("gap", gap)

        # Flex-specific properties
        self._children: List[
            QWidget
        ] = []  # Ordered list of children (will respect order prop)
        self._child_props: Dict[QWidget, Dict[str, Any]] = {}  # Props per child

        # Initial layout computation
        self._update_flex_layout()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the flex container with optional flex props."""
        if child and child not in self._children:
            # Store child props
            self._child_props[child] = {
                "grow": layout_props.get("grow", 0),
                "shrink": layout_props.get("shrink", 1),
                "basis": layout_props.get("basis", "auto"),
                "order": layout_props.get("order", 0),
                "alignSelf": layout_props.get("alignSelf", None),
            }

            # Set parent and add to children list
            child.setParent(self)
            self._children.append(child)

            # Trigger layout update
            self._update_flex_layout()
        else:
            # Fallback to base implementation
            super().add_child(child, **layout_props)

    def remove_child(self, child: QWidget) -> None:
        """Remove a child widget from the flex container."""
        if child in self._children:
            self._children.remove(child)
            if child in self._child_props:
                del self._child_props[child]
            child.setParent(None)
            self._update_flex_layout()
        else:
            super().remove_child(child)

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value (theme key or pixels) to actual pixel value."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            elif isinstance(spacing_value, int):
                return spacing_value
        return 8 if isinstance(spacing_value, str) else spacing_value

    def _resolve_basis(
        self, child: QWidget, get_main_size, container_main: float
    ) -> float:
        """Resolve flex-basis to main axis size in pixels."""
        props = self._child_props.get(child, {})
        basis = props.get("basis", "auto")
        if basis == "auto":
            return float(get_main_size(child.sizeHint()))
        if isinstance(basis, str) and basis.endswith("%"):
            try:
                perc = float(basis[:-1]) / 100.0
                return perc * container_main
            except (ValueError, TypeError):
                pass
        try:
            return float(basis)
        except (ValueError, TypeError):
            return float(get_main_size(child.sizeHint()))

    def _update_flex_layout(self) -> None:
        """Compute and apply flex layout by manually positioning and sizing children."""
        if not self._children:
            return

        # Get current responsive values
        direction_val = self._responsive.get("direction", "row")
        wrap_val = self._responsive.get("wrap", "nowrap")
        gap_val = self._responsive.get("gap", "md")
        gap_pixels = self._get_spacing_pixels(gap_val)

        if isinstance(wrap_val, bool):
            wrap_val = "wrap" if wrap_val else "nowrap"

        is_wrapping = wrap_val != "nowrap"

        # Container dimensions
        container_rect = self.contentsRect()
        container_width = container_rect.width()
        container_height = container_rect.height()

        # Sort children by order
        ordered_children = sorted(
            self._children, key=lambda c: self._child_props.get(c, {}).get("order", 0)
        )

        # Determine axes
        if direction_val in ["row", "row-reverse"]:
            is_row = True
            container_main = container_width
            container_cross = container_height
            get_main_size = lambda size: size.width()
            get_cross_size = lambda size: size.height()
            reverse_main = direction_val == "row-reverse"
        else:
            is_row = False
            container_main = container_height
            container_cross = container_width
            get_main_size = lambda size: size.height()
            get_cross_size = lambda size: size.width()
            reverse_main = direction_val == "column-reverse"

        if not is_wrapping:
            # Single line layout
            self._place_line_items(
                ordered_children,
                container_main,
                gap_pixels,
                reverse_main,
                is_row,
                get_main_size,
                get_cross_size,
                0,
                container_cross,
            )
        else:
            # Multi-line wrapping layout
            self._place_wrapped_items(
                ordered_children,
                container_main,
                container_cross,
                gap_pixels,
                reverse_main,
                is_row,
                get_main_size,
                get_cross_size,
            )

    def _place_line_items(
        self,
        line: List[QWidget],
        container_main: int,
        gap_pixels: int,
        reverse_main: bool,
        is_row: bool,
        get_main_size,
        get_cross_size,
        line_cross_pos: int,
        line_cross_size: int,
    ) -> None:
        """Place items in a single line according to justify-content."""
        if not line:
            return

        num_items = len(line)

        # Compute initial main sizes using basis
        initial_main_sizes = [
            self._resolve_basis(child, get_main_size, container_main) for child in line
        ]

        # Get flex properties
        grows = [self._child_props.get(child, {}).get("grow", 0) for child in line]
        shrinks = [self._child_props.get(child, {}).get("shrink", 1) for child in line]

        # Calculate gaps
        num_gaps = max(0, num_items - 1)
        base_gap_total = gap_pixels * num_gaps
        sum_initial = sum(initial_main_sizes) + base_gap_total
        free_space = float(container_main) - sum_initial

        # Distribute free space or handle deficit
        if free_space >= 0:
            total_grow = sum(g for g in grows)
            if total_grow > 0:
                main_sizes = [
                    initial_main_sizes[i] + (grows[i] / total_grow * free_space)
                    for i in range(num_items)
                ]
            else:
                main_sizes = initial_main_sizes[:]
        else:
            deficit = -free_space
            total_flex_shrink = sum(
                shrinks[i] * initial_main_sizes[i] for i in range(num_items)
            )
            if total_flex_shrink > 0:
                main_sizes = [
                    max(
                        0.0,
                        initial_main_sizes[i]
                        - (
                            shrinks[i]
                            * initial_main_sizes[i]
                            / total_flex_shrink
                            * deficit
                        ),
                    )
                    for i in range(num_items)
                ]
            else:
                main_sizes = initial_main_sizes[:]

        # Calculate total used space
        total_items_size = sum(main_sizes)
        used = total_items_size + base_gap_total
        free = container_main - used

        # Get justify value and calculate spacing
        justify_val = self._responsive.get("justify", "start")

        leading_space = 0
        trailing_space = 0
        item_gap_addition = 0

        if justify_val == "start":
            leading_space = 0
            trailing_space = free
        elif justify_val == "end":
            leading_space = free
            trailing_space = 0
        elif justify_val == "center":
            leading_space = free / 2
            trailing_space = free / 2
        elif justify_val == "space-between":
            if num_items <= 1:
                leading_space = 0
                trailing_space = free
            else:
                item_gap_addition = free / num_gaps
        elif justify_val == "space-around":
            if num_items > 0:
                space_per_half = free / (2 * num_items)
                leading_space = space_per_half
                trailing_space = space_per_half
                item_gap_addition = 2 * space_per_half
        elif justify_val == "space-evenly":
            if num_items > 0:
                num_dist_spaces = num_items + 1
                dist_space = free / num_dist_spaces
                leading_space = dist_space
                trailing_space = dist_space
                item_gap_addition = dist_space

        effective_gap = gap_pixels + item_gap_addition

        # Get align value
        align_val = self._responsive.get("align", "stretch")

        # Place items
        if not reverse_main:
            current = leading_space
            for i, child in enumerate(line):
                # Calculate cross-axis alignment
                child_props = self._child_props.get(child, {})
                align_self = child_props.get("alignSelf")
                effective_align = (
                    align_val
                    if align_self is None or align_self == "auto"
                    else align_self
                )

                child_size = child.sizeHint()
                child_main_size = main_sizes[i]
                child_cross_size = get_cross_size(child_size)

                # Apply stretch if needed
                if effective_align == "stretch":
                    child_cross_size = line_cross_size
                    child_cross_offset = 0
                elif effective_align in ["start", "baseline"]:
                    child_cross_offset = 0
                elif effective_align == "end":
                    child_cross_offset = line_cross_size - child_cross_size
                elif effective_align == "center":
                    child_cross_offset = (line_cross_size - child_cross_size) / 2
                else:
                    child_cross_offset = 0

                # Set position and size
                if is_row:
                    new_width = int(child_main_size)
                    new_height = (
                        int(child_cross_size)
                        if effective_align == "stretch"
                        else child_size.height()
                    )
                    pos_x = int(current)
                    pos_y = int(line_cross_pos + child_cross_offset)
                else:
                    new_width = (
                        int(child_cross_size)
                        if effective_align == "stretch"
                        else child_size.width()
                    )
                    new_height = int(child_main_size)
                    pos_x = int(line_cross_pos + child_cross_offset)
                    pos_y = int(current)

                child.move(pos_x, pos_y)
                child.resize(new_width, new_height)
                current += child_main_size + (effective_gap if i < num_items - 1 else 0)
        else:
            # Reverse placement logic
            current_end = container_main - trailing_space
            for i, child in enumerate(line):
                child_props = self._child_props.get(child, {})
                align_self = child_props.get("alignSelf")
                effective_align = (
                    align_val
                    if align_self is None or align_self == "auto"
                    else align_self
                )

                child_size = child.sizeHint()
                child_main_size = main_sizes[i]
                child_cross_size = get_cross_size(child_size)

                if effective_align == "stretch":
                    child_cross_size = line_cross_size
                    child_cross_offset = 0
                elif effective_align in ["start", "baseline"]:
                    child_cross_offset = 0
                elif effective_align == "end":
                    child_cross_offset = line_cross_size - child_cross_size
                elif effective_align == "center":
                    child_cross_offset = (line_cross_size - child_cross_size) / 2
                else:
                    child_cross_offset = 0

                if is_row:
                    new_width = int(child_main_size)
                    new_height = (
                        int(child_cross_size)
                        if effective_align == "stretch"
                        else child_size.height()
                    )
                    child_main_pos = current_end - child_main_size
                    pos_x = int(child_main_pos)
                    pos_y = int(line_cross_pos + child_cross_offset)
                else:
                    new_width = (
                        int(child_cross_size)
                        if effective_align == "stretch"
                        else child_size.width()
                    )
                    new_height = int(child_main_size)
                    child_main_pos = current_end - child_main_size
                    pos_x = int(line_cross_pos + child_cross_offset)
                    pos_y = int(child_main_pos)

                child.move(pos_x, pos_y)
                child.resize(new_width, new_height)
                if i < num_items - 1:
                    current_end = child_main_pos - effective_gap

    def _place_wrapped_items(
        self,
        ordered_children: List[QWidget],
        container_main: int,
        container_cross: int,
        gap_pixels: int,
        reverse_main: bool,
        is_row: bool,
        get_main_size,
        get_cross_size,
    ) -> None:
        """Place items with wrapping behavior."""
        # Collect lines
        lines = []
        current_line = []
        current_main = 0

        for child in ordered_children:
            child_main = self._resolve_basis(child, get_main_size, container_main)
            if current_line:
                next_main = current_main + gap_pixels + child_main
            else:
                next_main = child_main

            if current_line and next_main > container_main and len(current_line) > 0:
                lines.append(current_line)
                current_line = [child]
                current_main = child_main
            else:
                current_line.append(child)
                current_main = next_main

        if current_line:
            lines.append(current_line)

        if not lines:
            return

        # Calculate line cross sizes
        line_cross_sizes = []
        for line in lines:
            if len(lines) == 1:
                line_cross_sizes.append(container_cross)
            else:
                line_cross_sizes.append(
                    max((get_cross_size(c.sizeHint()) for c in line), default=0)
                )

        # Place each line
        current_cross = 0
        for line_idx, line in enumerate(lines):
            line_cross_size = line_cross_sizes[line_idx]
            line_cross_pos = current_cross

            # Place items in this line
            self._place_line_items(
                line,
                container_main,
                gap_pixels,
                reverse_main,
                is_row,
                get_main_size,
                get_cross_size,
                line_cross_pos,
                line_cross_size,
            )

            # Update cross position for next line
            if line_idx < len(lines) - 1:
                current_cross += line_cross_size + gap_pixels

    # Flex Properties (integrated with responsive system)

    @Property(str)
    def direction(self) -> str:
        """Get the current flex direction."""
        return self._responsive.get("direction", "row")

    @direction.setter
    def direction(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the flex direction."""
        self._responsive.set("direction", value)
        self._update_flex_layout()

    @Property(object)
    def wrap(self) -> Union[bool, str]:
        """Get the current wrap behavior."""
        return self._responsive.get("wrap", False)

    @wrap.setter
    def wrap(self, value: Union[bool, str, Dict[str, Union[bool, str]]]) -> None:
        """Set the wrap behavior."""
        self._responsive.set("wrap", value)
        self._update_flex_layout()

    @Property(str)
    def justify(self) -> str:
        """Get the current justify-content value."""
        return self._responsive.get("justify", "start")

    @justify.setter
    def justify(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the justify-content."""
        self._responsive.set("justify", value)
        self._update_flex_layout()

    @Property(str)
    def align(self) -> str:
        """Get the current align-items value."""
        return self._responsive.get("align", "stretch")

    @align.setter
    def align(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the align-items."""
        self._responsive.set("align", value)
        self._update_flex_layout()

    @Property(object)
    def gap(self) -> Union[str, int]:
        """Get the current gap spacing."""
        return self._responsive.get("gap", "md")

    @gap.setter
    def gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the gap spacing."""
        self._responsive.set("gap", value)
        self._update_flex_layout()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props and relayout."""
        super().resizeEvent(event)
        # Invalidate responsive cache
        if hasattr(self, "_responsive"):
            self._responsive._invalidate_all_cache()
        self._update_flex_layout()
