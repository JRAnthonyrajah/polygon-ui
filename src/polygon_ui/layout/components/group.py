"""
Group component for Polygon UI layout system.

A horizontal grouping component using QHBoxLayout, similar to Mantine's Group component.
Supports gap spacing, alignment, wrapping, and child widget sizing.
"""

from typing import Optional, Any, Dict, Union

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Group(LayoutComponent):
    """
    Group component that arranges children horizontally with configurable spacing
    and wrapping. Provides a simple way to group related elements horizontally.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        gap: Union[str, int, Dict[str, Union[str, int]]] = "md",
        align: str = "center",
        justify: str = "start",
        wrap: Union[bool, Dict[str, bool]] = False,
        spacing: Union[str, int, Dict[str, Union[str, int]]] = None,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("gap", gap)
        self._responsive.set("align", align)
        self._responsive.set("justify", justify)
        self._responsive.set("wrap", wrap)
        self._responsive.set("spacing", spacing if spacing is not None else gap)

        # Group-specific properties
        self._wrap_children: bool = False
        self._children_order: list[QWidget] = []
        self._child_props: Dict[QWidget, Dict[str, Any]] = {}
        self._hbox: Optional[QHBoxLayout] = None
        self._grid: Optional[QGridLayout] = None

        # Set up horizontal layout for grouping children
        self._setup_layout()

        # Apply initial styling
        self._update_group_styling()

    def _setup_layout(self) -> None:
        """Initialize layout objects for the Group."""
        # Layouts created dynamically in _relayout_children based on wrap prop

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value to pixels using theme or fallback."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            else:
                return int(spacing_value)
        return 8 if isinstance(spacing_value, str) else spacing_value

    def _update_child_policies(self) -> None:
        """Apply size policies and basis to children based on their props."""
        for child in self._children_order:
            if child not in self._child_props:
                continue
            props = self._child_props[child]

            h_policy = QSizePolicy.Policy.Preferred
            v_policy = QSizePolicy.Policy.Preferred

            # Horizontal sizing (grow, shrink, basis for non-wrap primarily)
            if props.get("grow"):
                h_policy = QSizePolicy.Policy.Expanding
            elif props.get("shrink"):
                h_policy = QSizePolicy.Policy.Minimum
            elif props.get("flex") == "none":
                h_policy = QSizePolicy.Policy.Fixed

            # Vertical sizing (alignSelf already handled in alignment)
            if props.get("alignSelf") == "stretch":
                v_policy = QSizePolicy.Policy.Expanding
            # else use Preferred or based on align

            child.setSizePolicy(QSizePolicy(h_policy, v_policy))

            # Flex basis - set minimum size
            if "basis" in props or "flexBasis" in props:
                basis = props.get("basis") or props.get("flexBasis")
                if isinstance(basis, (int, str)):
                    try:
                        width = int(basis) if isinstance(basis, str) else basis
                        child.setMinimumWidth(width)
                        (
                            child.setMaximumWidth(width)
                            if h_policy == QSizePolicy.Policy.Fixed
                            else None
                        )
                    except ValueError:
                        child.setMinimumWidth(100)  # fallback

            # For wrap mode, basis affects preferred width in grid

    def _update_group_styling(self) -> None:
        """Update group styling based on current properties."""
        # Get responsive values
        gap_val = self._responsive.get("gap", "md")
        align_val = self._responsive.get("align", "center")
        justify_val = self._responsive.get("justify", "start")
        wrap_val = self._responsive.get("wrap", False)
        spacing_val = self._responsive.get("spacing", gap_val)

        self._wrap_children = wrap_val
        self._update_child_policies()
        self._relayout_children()

        # Generate QSS if needed
        self._update_styling()

    def _get_v_alignment(self, align_val: str) -> Qt.Alignment:
        """Get vertical alignment flag based on align value."""
        if align_val == "start":
            return Qt.AlignTop
        elif align_val == "center":
            return Qt.AlignVCenter
        elif align_val == "end":
            return Qt.AlignBottom
        elif align_val == "stretch":
            return Qt.AlignVCenter  # Cells can stretch based on policy
        return Qt.AlignVCenter

    def _get_v_alignment_for_child(self, child: QWidget) -> Qt.Alignment:
        """Get vertical alignment for specific child, respecting alignSelf."""
        if child not in self._child_props:
            return self._get_v_alignment(self.align)
        align_self = self._child_props[child].get("alignSelf", self.align)
        return self._get_v_alignment(align_self)

    def _relayout_children(self) -> None:
        """Relayout children based on current properties and container size."""
        wrap_val = self._responsive.get("wrap", False)
        align_val = self._responsive.get("align", "center")
        justify_val = self._responsive.get("justify", "start")
        spacing_val = self._responsive.get("spacing", self._responsive.get("gap", "md"))
        gap_val = self._responsive.get("gap", "md")

        h_spacing = self._get_spacing_pixels(spacing_val)
        v_spacing = self._get_spacing_pixels(gap_val)
        container_width = self.width() if self.width() > 0 else 800

        num_children = len(self._children_order)
        if num_children == 0:
            return

        if not wrap_val:
            # Non-wrapping: use QHBoxLayout with justify support
            if self._hbox is None:
                self._hbox = QHBoxLayout()
            self.setLayout(self._hbox)
            self._layout = self._hbox
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setSpacing(h_spacing)

            # Clear existing items
            while self._layout.count() > 0:
                item = self._layout.takeAt(0)
                if item and item.widget():
                    item.widget().setParent(self)

            # Add stretches and children based on justify
            if justify_val == "space-around" and num_children > 0:
                self._layout.addStretch(1)
                for i in range(num_children):
                    child = self._children_order[i]
                    v_align = self._get_v_alignment_for_child(child)
                    self._layout.addWidget(child, alignment=v_align)
                    if i < num_children - 1:
                        self._layout.addStretch(2)
                self._layout.addStretch(1)
            else:
                stretches_before = 0
                stretches_after = 0
                between = False
                if justify_val == "start":
                    stretches_before = 0
                    stretches_after = 0
                    between = False
                elif justify_val == "end":
                    stretches_before = 1
                    stretches_after = 0
                    between = False
                elif justify_val == "center":
                    stretches_before = 1
                    stretches_after = 1
                    between = False
                elif justify_val == "space-between":
                    stretches_before = 0
                    stretches_after = 0
                    between = True
                else:
                    stretches_before = 0
                    stretches_after = 0
                    between = False

                if stretches_before > 0:
                    self._layout.addStretch(stretches_before)
                for i in range(num_children):
                    child = self._children_order[i]
                    v_align = self._get_v_alignment_for_child(child)
                    self._layout.addWidget(child, alignment=v_align)
                    if i < num_children - 1 and between:
                        self._layout.addStretch(1)
                if stretches_after > 0:
                    self._layout.addStretch(stretches_after)
        else:
            # Wrapping: use QGridLayout for flow layout
            if self._grid is None:
                self._grid = QGridLayout()
            self.setLayout(self._grid)
            self._layout = self._grid
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setHorizontalSpacing(h_spacing)
            self._layout.setVerticalSpacing(v_spacing)

            # Clear existing items
            while self._layout.count() > 0:
                item = self._layout.takeAt(0)
                if item and item.widget():
                    item.widget().setParent(self)

            row = 0
            col = 0
            current_width = 0
            for child in self._children_order:
                pref_w = max(child.sizeHint().width(), child.minimumWidth())
                space_before = h_spacing if col > 0 else 0
                if current_width + space_before + pref_w > container_width and col > 0:
                    row += 1
                    col = 0
                    current_width = 0
                v_align = self._get_v_alignment_for_child(child)
                self._layout.addWidget(child, row, col, 1, 1, Qt.AlignLeft | v_align)
                current_width += space_before + pref_w
                col += 1

            # Set stretches to 0 for packing
            max_col = col - 1 if col > 0 else 0
            for c in range(max_col + 1):
                self._layout.setColumnStretch(c, 0)

            max_row = row if col > 0 else row
            for r in range(max_row + 1):
                self._layout.setRowStretch(r, 0)
            self._layout.setRowStretch(max_row + 1, 1)  # Space after for vertical start

        self.updateGeometry()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the group with optional layout props."""
        if child:
            self._child_props[child] = dict(layout_props)
            child.setParent(self)
            self._children_order.append(child)
            self._update_group_styling()
        else:
            super().add_child(child, **layout_props)

    # Property: gap
    @Property(str)
    def gap(self) -> str:
        """Get the current resolved gap spacing."""
        return self._responsive.get("gap", "md")

    @gap.setter
    def gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """
        Set the gap spacing. Can be str/int or responsive dict.

        Examples:
        - Simple: gap="md"
        - Responsive: gap={"base": "sm", "md": "md", "lg": "lg"}
        """
        self._responsive.set("gap", value)
        # Also update spacing if it hasn't been explicitly set
        if not self._responsive.is_set("spacing"):
            self._responsive.set("spacing", value)
        self._update_group_styling()

    # Property: spacing (alias for gap)
    @Property(str)
    def spacing(self) -> str:
        """Get the current resolved spacing (alias for gap)."""
        return self._responsive.get("spacing", self.gap)

    @spacing.setter
    def spacing(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the spacing. Can be str/int or responsive dict."""
        self._responsive.set("spacing", value)
        self._update_group_styling()

    # Property: align
    @Property(str)
    def align(self) -> str:
        """Get the current resolved vertical alignment."""
        return self._responsive.get("align", "center")

    @align.setter
    def align(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the vertical alignment. Can be str or responsive dict."""
        self._responsive.set("align", value)
        self._update_group_styling()

    # Property: justify
    @Property(str)
    def justify(self) -> str:
        """Get the current resolved horizontal alignment."""
        return self._responsive.get("justify", "start")

    @justify.setter
    def justify(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the horizontal alignment. Can be str or responsive dict."""
        self._responsive.set("justify", value)
        self._update_group_styling()

    # Property: wrap
    @Property(bool)
    def wrap(self) -> bool:
        """Get the current resolved wrap behavior."""
        return self._responsive.get("wrap", False)

    @wrap.setter
    def wrap(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the wrap behavior. Can be bool or responsive dict."""
        self._responsive.set("wrap", value)
        self._update_group_styling()

    def resizeEvent(self, event) -> None:
        """Handle resize events with responsive updates."""
        super().resizeEvent(event)
        # Invalidate responsive cache and update styling
        self._responsive._invalidate_all_cache()
        self._update_group_styling()

    @property
    def wrap_children(self) -> bool:
        """Get whether children should wrap to next line."""
        return self._wrap_children

    def set_wrap_enabled(self, enabled: bool) -> None:
        """Enable or disable wrapping behavior."""
        self._wrap_children = enabled
        self._update_group_styling()
