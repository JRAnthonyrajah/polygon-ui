"""
Stack component for Polygon UI layout system.

A flexible stacking component using QVBoxLayout or QHBoxLayout, similar to Mantine's Stack component.
Supports gap spacing, alignment, and responsive direction switching between vertical and horizontal layouts.
"""

from typing import Optional, Any, Dict, Union

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Stack(LayoutComponent):
    """
    Stack component that arranges children vertically or horizontally with configurable spacing
    and alignment. Provides a simple way to stack elements with consistent gaps and responsive direction switching.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        gap: Union[str, int, Dict[str, Union[str, int]]] = "md",
        justify: str = "start",
        align: str = "stretch",
        direction: Union[str, Dict[str, str]] = "column",
        **kwargs: Any,
    ):
        # Set initial direction before calling super().__init__
        self._direction = "column" if isinstance(direction, str) else "column"

        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("gap", gap)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)
        self._responsive.set("direction", direction)

        # Set up layout for stacking children (now with direction support)
        self._setup_layout()

        # Apply initial styling
        self._update_layout_styling()

    def _setup_layout(self) -> None:
        """Set up the Qt layout for the Stack (vertical by default)."""
        # Get current direction to determine layout type
        if hasattr(self, "_responsive"):
            direction_val = self._responsive.get("direction", "column")
        else:
            direction_val = getattr(self, "_direction", "column")

        # Preserve existing children during layout recreation
        children = []
        if hasattr(self, "_layout") and self._layout:
            # Extract children from current layout
            while self._layout.count():
                item = self._layout.takeAt(0)
                if item.widget():
                    children.append(item.widget())
                    item.widget().setParent(None)
            # Remove old layout
            self.layout().deleteLater()

        # Create new layout based on direction
        if direction_val == "row":
            self._layout = QHBoxLayout(self)
        else:
            self._layout = QVBoxLayout(self)

        self._layout.setContentsMargins(0, 0, 0, 0)  # No default margins
        # Default alignment
        if direction_val == "row":
            self._layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self._layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Restore children to new layout
        for child in children:
            self._layout.addWidget(child)

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value to pixels using theme or fallback."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            else:
                return int(spacing_value)
        return 8 if isinstance(spacing_value, str) else spacing_value

    def _update_layout_styling(self) -> None:
        """Update stack styling based on current properties."""
        # Get responsive values
        gap_val = self._responsive.get("gap", "md")
        justify_val = self._responsive.get("justify", "start")
        align_val = self._responsive.get("align", "stretch")
        direction_val = self._responsive.get("direction", "column")

        # Update spacing
        gap_pixels = self._get_spacing_pixels(gap_val)
        if self._layout:
            self._layout.setSpacing(gap_pixels)

        # Update alignment based on direction, justify, and align
        if self._layout:
            if direction_val == "row":
                # Horizontal layout
                alignment = Qt.AlignVCenter  # Default vertical center
                if justify_val == "center":
                    alignment |= Qt.AlignHCenter
                elif justify_val == "end":
                    alignment |= Qt.AlignRight
                elif justify_val == "space-between":
                    # Handled by layout spacing and widget policies
                    alignment |= Qt.AlignLeft
                elif justify_val == "space-around":
                    # Handled by layout spacing and widget policies
                    alignment |= Qt.AlignLeft

                # Cross-axis alignment for horizontal layout
                if align_val == "start":
                    alignment |= Qt.AlignTop
                elif align_val == "end":
                    alignment |= Qt.AlignBottom
                elif align_val == "center":
                    alignment |= Qt.AlignVCenter  # Already set
                elif align_val == "stretch":
                    alignment |= Qt.AlignTop | Qt.AlignBottom
            else:
                # Vertical layout (column)
                alignment = Qt.AlignTop  # Default vertical top
                if justify_val == "center":
                    alignment |= Qt.AlignVCenter
                elif justify_val == "end":
                    alignment |= Qt.AlignBottom
                elif justify_val == "space-between":
                    alignment |= Qt.AlignTop
                elif justify_val == "space-around":
                    alignment |= Qt.AlignTop

                # Cross-axis alignment for vertical layout
                if align_val == "start":
                    alignment |= Qt.AlignLeft
                elif align_val == "end":
                    alignment |= Qt.AlignRight
                elif align_val == "center":
                    alignment |= Qt.AlignHCenter
                elif align_val == "stretch":
                    alignment |= Qt.AlignLeft | Qt.AlignRight

            self._layout.setAlignment(alignment)

        # Generate QSS if needed
        self._update_styling()

    # Property: gap
    @Property(str)
    def gap(self) -> str:
        """Get the current resolved gap spacing."""
        return self._responsive.get("gap", "md")

    @gap.setter
    def gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the gap spacing. Can be str or responsive dict."""
        self._responsive.set("gap", value)
        self._update_layout_styling()

    # Property: justify
    @Property(str)
    def justify(self) -> str:
        """Get the current resolved justify alignment."""
        return self._responsive.get("justify", "start")

    @justify.setter
    def justify(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the justify alignment. Can be str or responsive dict."""
        self._responsive.set("justify", value)
        self._update_layout_styling()

    # Property: align
    @Property(str)
    def align(self) -> str:
        """Get the current resolved align alignment."""
        return self._responsive.get("align", "stretch")

    @align.setter
    def align(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the align alignment. Can be str or responsive dict."""
        self._responsive.set("align", value)
        self._update_layout_styling()

    # Property: direction
    @Property(str)
    def direction(self) -> str:
        """Get the current resolved direction (column or row)."""
        return self._responsive.get("direction", "column")

    @direction.setter
    def direction(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the direction. Can be str or responsive dict."""
        self._responsive.set("direction", value)
        # Recreate layout when direction changes
        self._setup_layout()
        self._update_layout_styling()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the stack with optional sizing props."""
        if self.layout() and child:
            # Apply child sizing properties
            self._apply_child_sizing(child, layout_props)
            self.layout().addWidget(child)
        else:
            # Fallback to base class implementation
            super().add_child(child, **layout_props)

    def _apply_child_sizing(self, child: QWidget, layout_props: Dict[str, Any]) -> None:
        """Apply sizing properties to a child widget."""
        direction_val = (
            self._responsive.get("direction", "column")
            if hasattr(self, "_responsive")
            else "column"
        )

        # Default size policies based on stack direction
        if direction_val == "row":
            horizontal_policy = getattr(child, "_horizontal_grow", False)
            vertical_policy = getattr(child, "_vertical_grow", False)
        else:
            horizontal_policy = getattr(child, "_horizontal_grow", False)
            vertical_policy = getattr(child, "_vertical_grow", False)

        # Handle grow property
        if layout_props.get("grow", False):
            if direction_val == "row":
                child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            else:
                child.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Handle shrink property
        elif layout_props.get("shrink", False):
            if direction_val == "row":
                child.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            else:
                child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Handle fixed sizing
        elif layout_props.get("flex", "none") == "none":
            child.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Handle flex basis (preferred size)
        if "flex_basis" in layout_props:
            basis = layout_props["flex_basis"]
            if direction_val == "row":
                child.setMinimumWidth(
                    int(basis)
                    if isinstance(basis, (int, str)) and str(basis).isdigit()
                    else 100
                )
            else:
                child.setMinimumHeight(
                    int(basis)
                    if isinstance(basis, (int, str)) and str(basis).isdigit()
                    else 100
                )

        # Handle alignment for individual child
        if "align" in layout_props:
            align = layout_props["align"]
            if direction_val == "row":
                # Vertical alignment for horizontal layout
                if align == "start":
                    child.setAlignment(Qt.AlignTop)
                elif align == "center":
                    child.setAlignment(Qt.AlignVCenter)
                elif align == "end":
                    child.setAlignment(Qt.AlignBottom)
            else:
                # Horizontal alignment for vertical layout
                if align == "start":
                    child.setAlignment(Qt.AlignLeft)
                elif align == "center":
                    child.setAlignment(Qt.AlignHCenter)
                elif align == "end":
                    child.setAlignment(Qt.AlignRight)

    def resizeEvent(self, event) -> None:
        """Handle resize events with responsive updates."""
        super().resizeEvent(event)
        # Invalidate responsive cache and update styling
        self._responsive._invalidate_all_cache()
        self._update_layout_styling()
