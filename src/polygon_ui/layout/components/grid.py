"""
Grid component for Polygon UI layout system.

A CSS Grid-like component using QGridLayout for two-dimensional layout.
Supports responsive columns, gutter spacing, justify-content, and align-items.
Children are placed sequentially in row-major order across the grid columns.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Grid(LayoutComponent):
    """
    Grid component that provides CSS Grid-like layout behavior using QGridLayout.

    Arranges children in a two-dimensional grid with responsive column counts,
    configurable gutters, and alignment options for justify-content and align-items.
    Supports equal-width columns by default with column stretches.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        columns: Union[int, Dict[str, int]] = 1,
        gutter: Union[str, int, Dict[str, Union[str, int]]] = "md",
        justify: Union[str, Dict[str, str]] = "start",
        align: Union[str, Dict[str, str]] = "start",
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("columns", columns)
        self._responsive.set("gutter", gutter)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)

        # Setup grid layout
        self._setup_layout()

        # Initial layout computation
        self._update_grid_layout()

    def _setup_layout(self) -> None:
        """Set up the QGridLayout for this component."""
        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

    def _get_gutter_pixels(self, gutter_value: Union[str, int]) -> int:
        """Convert gutter value (theme key or pixels) to actual pixel value."""
        if self._provider:
            if isinstance(gutter_value, str):
                return self._provider.get_theme_value(f"spacing.{gutter_value}", 8)
            elif isinstance(gutter_value, int):
                return gutter_value
        return 8 if isinstance(gutter_value, str) else gutter_value

    def _update_grid_layout(self) -> None:
        """Compute and apply grid layout properties."""
        if not self._layout:
            return

        # Get current responsive values
        columns_val = self._responsive.get("columns", 1)
        num_columns = int(columns_val)
        self._layout.setColumnCount(num_columns)

        # Set equal stretch for columns (CSS Grid default behavior)
        for i in range(num_columns):
            self._layout.setColumnStretch(i, 1)

        gutter_val = self._responsive.get("gutter", "md")
        gutter_pixels = self._get_gutter_pixels(gutter_val)
        self._layout.setHorizontalSpacing(gutter_pixels)
        self._layout.setVerticalSpacing(gutter_pixels)

        # Justify (horizontal alignment)
        justify_val = self._responsive.get("justify", "start")
        if justify_val == "start":
            h_align = Qt.AlignLeft
        elif justify_val == "center":
            h_align = Qt.AlignHCenter
        elif justify_val == "end":
            h_align = Qt.AlignRight
        elif justify_val == "stretch":
            h_align = Qt.AlignJustify  # Approximate stretch
        else:
            h_align = Qt.AlignLeft

        # Align (vertical alignment)
        align_val = self._responsive.get("align", "start")
        if align_val == "start":
            v_align = Qt.AlignTop
        elif align_val == "center":
            v_align = Qt.AlignVCenter
        elif align_val == "end":
            v_align = Qt.AlignBottom
        elif align_val == "stretch":
            v_align = Qt.AlignVCenter  # QGridLayout items stretch vertically by default
        else:
            v_align = Qt.AlignTop

        # Set default alignment for grid items
        self._layout.setAlignment(h_align | v_align)

    def _update_responsive_props(self) -> None:
        """Update all responsive properties based on current breakpoint."""
        super()._update_responsive_props()
        self._update_grid_layout()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """
        Add a child widget to the grid container.
        Children are placed sequentially in row-major order.
        """
        if child and child not in self._children:
            super().add_child(child, **layout_props)
            # QGridLayout handles sequential placement with addWidget(child)
            # Future: Support span/offset props for Col children
        else:
            super().add_child(child, **layout_props)

    # Grid Properties (integrated with responsive system)

    @Property(object)
    def columns(self) -> Union[int, Dict[str, int]]:
        """Get the current number of columns (responsive)."""
        return self._responsive.get("columns", 1)

    @columns.setter
    def columns(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the number of columns (responsive)."""
        self._responsive.set("columns", value)
        self._update_grid_layout()

    @Property(object)
    def gutter(self) -> Union[str, int]:
        """Get the current gutter spacing (responsive)."""
        return self._responsive.get("gutter", "md")

    @gutter.setter
    def gutter(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the gutter spacing (responsive)."""
        self._responsive.set("gutter", value)
        self._update_grid_layout()

    @Property(str)
    def justify(self) -> str:
        """Get the current justify-content value."""
        return self._responsive.get("justify", "start")

    @justify.setter
    def justify(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the justify-content."""
        self._responsive.set("justify", value)
        self._update_grid_layout()

    @Property(str)
    def align(self) -> str:
        """Get the current align-items value."""
        return self._responsive.get("align", "start")

    @align.setter
    def align(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the align-items."""
        self._responsive.set("align", value)
        self._update_grid_layout()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props and relayout."""
        super().resizeEvent(event)
        # Responsive updates handled in base, but ensure grid update
        self._update_grid_layout()
