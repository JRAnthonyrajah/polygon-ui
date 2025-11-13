"""
Stack component for Polygon UI layout system.

A simple vertical stacking component using QVBoxLayout, similar to Mantine's Stack component.
Supports gap spacing and alignment between children.
"""

from typing import Optional, Any, Dict, Union

from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Stack(LayoutComponent):
    """
    Stack component that arranges children vertically with configurable spacing
    and alignment. Provides a simple way to stack elements with consistent gaps.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        gap: Union[str, Dict[str, str]] = "md",
        justify: str = "start",
        align: str = "stretch",
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("gap", gap)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)

        # Set default direction to column for Stack
        self._direction = "column"

        # Set up vertical layout for stacking children
        self._setup_layout()

        # Apply initial styling
        self._update_layout_styling()

    def _setup_layout(self) -> None:
        """Set up the Qt layout for the Stack (vertical by default)."""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(
            0, 0, 0, 0
        )  # No default margins, handled via props if needed
        # Default alignment for vertical stack
        self._layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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

        # Update spacing
        gap_pixels = self._get_spacing_pixels(gap_val)
        if self._layout:
            self._layout.setSpacing(gap_pixels)

        # Update alignment based on justify and align
        if self._layout:
            alignment = Qt.AlignTop  # Default for vertical
            if justify_val == "center":
                alignment |= Qt.AlignVCenter
            elif justify_val == "end":
                alignment |= Qt.AlignBottom

            if align_val == "center":
                alignment |= Qt.AlignHCenter
            elif align_val == "right":
                alignment |= Qt.AlignRight
            # For stretch, no additional horizontal alignment needed

            self._layout.setAlignment(alignment)

            # For individual child alignment if needed (e.g., align-items)
            for i in range(self._layout.count()):
                item = self._layout.itemAt(i)
                if item and item.widget():
                    child_align = Qt.AlignLeft  # Default
                    if align_val == "center":
                        child_align = Qt.AlignHCenter
                    elif align_val == "right":
                        child_align = Qt.AlignRight
                    item.widget().setAlignment(child_align)

        # Generate QSS if needed
        self._update_styling()

    # Property: gap
    @Property(str)
    def gap(self) -> str:
        """Get the current resolved gap spacing."""
        return self._responsive.get("gap", "md")

    @gap.setter
    def gap(self, value: Union[str, Dict[str, str]]) -> None:
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

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the stack."""
        super().add_child(child, **layout_props)
        # Additional stack-specific child props can be handled here if needed

    def resizeEvent(self, event) -> None:
        """Handle resize events with responsive updates."""
        super().resizeEvent(event)
        # Invalidate responsive cache and update styling
        self._responsive._invalidate_all_cache()
        self._update_layout_styling()
