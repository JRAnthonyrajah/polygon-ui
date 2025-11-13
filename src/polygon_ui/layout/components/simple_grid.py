"""
SimpleGrid component for Polygon UI layout system.

A simplified grid component using QGridLayout for equal-sized columns.
Supports responsive column counts and uniform spacing.
Children are placed sequentially in row-major order.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class SimpleGrid(LayoutComponent):
    """
    SimpleGrid component that provides a basic CSS Grid-like layout using QGridLayout.

    Arranges children in equal-width columns with responsive column counts and
    configurable spacing. Designed for simple, mobile-first responsive layouts
    without complex spanning or offsetting.

    Mobile-first approach: starts with fewer columns on small screens and increases
    on larger breakpoints.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        cols: Union[int, Dict[str, int]] = 1,
        spacing: Union[str, int, Dict[str, Union[str, int]]] = "md",
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties (mobile-first)
        self._responsive.set("cols", cols)
        self._responsive.set("spacing", spacing)

        # Setup grid layout
        self._setup_layout()

        # Initial layout computation
        self._update_simple_grid_layout()

    def _setup_layout(self) -> None:
        """Set up the QGridLayout for this component."""
        self._layout = QGridLayout(self)
        self.setLayout(self._layout)

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value (theme key or pixels) to actual pixel value."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            elif isinstance(spacing_value, int):
                return spacing_value
        return 8 if isinstance(spacing_value, str) else spacing_value

    def _update_simple_grid_layout(self) -> None:
        """Compute and apply simple grid layout properties."""
        if not self._layout:
            return

        # Get current responsive values
        cols_val = self._responsive.get("cols", 1)
        num_columns = int(cols_val)

        # Set column count and ensure equal widths
        self._layout.setColumnCount(num_columns)
        for i in range(num_columns):
            self._layout.setColumnStretch(i, 1)

        # Apply uniform spacing (horizontal and vertical)
        spacing_val = self._responsive.get("spacing", "md")
        spacing_pixels = self._get_spacing_pixels(spacing_val)
        self._layout.setHorizontalSpacing(spacing_pixels)
        self._layout.setVerticalSpacing(spacing_pixels)

        # Default alignment: top-left for items
        default_alignment = Qt.AlignLeft | Qt.AlignTop

        # Place children sequentially in row-major order
        self._place_children_simple(default_alignment)

    def _update_responsive_props(self) -> None:
        """Update all responsive properties based on current breakpoint."""
        super()._update_responsive_props()
        self._update_simple_grid_layout()

    def _place_children_simple(self, default_alignment: Qt.Alignment) -> None:
        """Place children in the grid sequentially without spans or offsets."""
        # Clear existing widgets from layout
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Place children in row-major order
        num_cols = self._layout.columnCount()
        for i, child in enumerate(self._children):
            if not isinstance(child, QWidget):
                continue
            row = i // num_cols
            col = i % num_cols
            self._layout.addWidget(child, row, col, 1, 1)
            self._layout.setAlignment(child, default_alignment)

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """
        Add a child widget to the SimpleGrid container.
        Children are placed sequentially; layout_props are ignored for simplicity.
        """
        super().add_child(child, **layout_props)
        self._update_simple_grid_layout()

    # SimpleGrid Properties (integrated with responsive system)

    @Property(object)
    def cols(self) -> Union[int, Dict[str, int]]:
        """Get the current number of columns (responsive, mobile-first)."""
        return self._responsive.get("cols", 1)

    @cols.setter
    def cols(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the number of columns (responsive, mobile-first)."""
        self._responsive.set("cols", value)
        self._update_simple_grid_layout()

    @Property(object)
    def spacing(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current spacing value (responsive)."""
        return self._responsive.get("spacing", "md")

    @spacing.setter
    def spacing(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the uniform spacing (responsive)."""
        self._responsive.set("spacing", value)
        self._update_simple_grid_layout()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props and relayout."""
        super().resizeEvent(event)
        self._update_simple_grid_layout()

    def responsive_cols(self, breakpoints: Dict[str, int]) -> "SimpleGrid":
        """Convenience method to set responsive column counts (mobile-first)."""
        self.cols = breakpoints
        return self

    def fixed_cols(self, count: int) -> "SimpleGrid":
        """Convenience method to set fixed number of columns."""
        self.cols = count
        return self
