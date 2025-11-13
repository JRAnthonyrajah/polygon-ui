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
        auto_columns: Union[bool, Dict[str, bool]] = False,
        min_column_width: Union[int, Dict[str, int]] = 250,
        col_gap: Union[str, int, Dict[str, Union[str, int]]] = None,
        row_gap: Union[str, int, Dict[str, Union[str, int]]] = None,
        **kwargs: Any,
    ):
        col_gap = col_gap if col_gap is not None else gutter
        row_gap = row_gap if row_gap is not None else gutter

        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("columns", columns)
        self._responsive.set("gutter", gutter)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)
        self._responsive.set("auto_columns", auto_columns)
        self._responsive.set("min_column_width", min_column_width)
        self._responsive.set("col_gap", col_gap)
        self._responsive.set("row_gap", row_gap)

        self._child_layout_props = {}

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
        auto_val = self._responsive.get("auto_columns", False)
        columns_val = self._responsive.get("columns", 1)
        min_w_val = self._responsive.get("min_column_width", 250)
        min_w = int(min_w_val)
        width = self.width()
        if auto_val and width > 0:
            num_columns = max(1, width // min_w)
        else:
            num_columns = int(columns_val)
        self._layout.setColumnCount(num_columns)

        if auto_val:
            for i in range(num_columns):
                self._layout.setColumnMinimumWidth(i, min_w)
                self._layout.setColumnStretch(i, 1)
        else:
            for i in range(num_columns):
                self._layout.setColumnStretch(i, 1)

        col_gap_val = self._responsive.get("col_gap", "md")
        row_gap_val = self._responsive.get("row_gap", "md")
        col_pixels = self._get_gutter_pixels(col_gap_val)
        row_pixels = self._get_gutter_pixels(row_gap_val)
        self._layout.setHorizontalSpacing(col_pixels)
        self._layout.setVerticalSpacing(row_pixels)

        # Justify-items (horizontal alignment for items)
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

        # Align-items (vertical alignment for items)
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

        default_alignment = h_align | v_align
        self._place_children(default_alignment)

    def _update_responsive_props(self) -> None:
        """Update all responsive properties based on current breakpoint."""
        super()._update_responsive_props()
        self._update_grid_layout()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """
        Add a child widget to the grid container.
        Supports layout_props like 'colspan', 'rowspan', 'offset' for Col integration.
        Children are placed sequentially in row-major order with reflow on updates.
        """
        super().add_child(child, **layout_props)
        self._child_layout_props[child] = layout_props
        self._update_grid_layout()

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
        self._responsive.set("col_gap", value)
        self._responsive.set("row_gap", value)
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

    @Property(object)
    def col_gap(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current column gap spacing (responsive)."""
        return self._responsive.get("col_gap", "md")

    @col_gap.setter
    def col_gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the column gap spacing (responsive)."""
        self._responsive.set("col_gap", value)
        self._update_grid_layout()

    @Property(object)
    def row_gap(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current row gap spacing (responsive)."""
        return self._responsive.get("row_gap", "md")

    @row_gap.setter
    def row_gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the row gap spacing (responsive)."""
        self._responsive.set("row_gap", value)
        self._update_grid_layout()

    @Property(bool)
    def auto_columns(self) -> bool:
        """Get whether auto-fit columns are enabled (responsive)."""
        return self._responsive.get("auto_columns", False)

    @auto_columns.setter
    def auto_columns(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set auto-fit columns behavior (responsive)."""
        self._responsive.set("auto_columns", value)
        self._update_grid_layout()

    @Property(int)
    def min_column_width(self) -> int:
        """Get the minimum column width for auto-fit (responsive)."""
        val = self._responsive.get("min_column_width", 250)
        return int(val)

    @min_column_width.setter
    def min_column_width(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the minimum column width for auto-fit (responsive)."""
        self._responsive.set("min_column_width", value)
        self._update_grid_layout()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props and relayout."""
        super().resizeEvent(event)
        # Responsive updates handled in base, but ensure grid update
        self._update_grid_layout()

    def _place_children(self, default_alignment: Qt.Alignment) -> None:
        """Place children in the grid with support for spans, offsets, and reflow."""
        # Clear existing widgets from layout
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Place children sequentially with props handling
        current_row = 0
        current_col = 0
        num_cols = self._layout.columnCount()
        for child in self._children:
            if not isinstance(child, QWidget):
                continue
            props = self._child_layout_props.get(child, {})
            colspan = props.get("colspan", 1)
            rowspan = props.get("rowspan", 1)
            offset = props.get("offset", 0)
            start_col = current_col + offset
            # Handle row wrap
            if start_col >= num_cols:
                current_row += 1
                current_col = 0
                start_col = offset
            if start_col + colspan > num_cols:
                colspan = num_cols - start_col
            self._layout.addWidget(child, current_row, start_col, rowspan, colspan)
            self._layout.setAlignment(child, default_alignment)
            current_col = (start_col + colspan) % num_cols
            if current_col == 0:
                current_row += 1

    def auto_fit(self, min_width: int = 250) -> "Grid":
        """Convenience method to enable auto-fit responsive columns."""
        self.auto_columns = True
        self.min_column_width = min_width
        return self

    def fixed_columns(self, count: int) -> "Grid":
        """Convenience method to set fixed number of columns."""
        self.columns = count
        self.auto_columns = False
        return self

    def responsive_columns(self, breakpoints: Dict[str, int]) -> "Grid":
        """Convenience method to set responsive column counts."""
        self.columns = breakpoints
        self.auto_columns = False
        return self

    def minmax_columns(
        self, min_size: Union[int, str], max_size: Union[int, str]
    ) -> "Grid":
        """Convenience method for minmax column sizing (simulated)."""
        self.auto_columns = True
        self.min_column_width = (
            self._get_gutter_pixels(min_size) if isinstance(min_size, str) else min_size
        )
        # Max size approximated by stretch
        return self
