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

    Arranges children in equal-width columns with responsive column counts, separate
    horizontal/vertical spacing, auto-fit sizing, and smooth resize handling.
    Designed for simple, mobile-first responsive layouts without complex spanning
    or offsetting.

    Mobile-first approach: starts with fewer columns on small screens and increases
    on larger breakpoints. Supports auto-fit columns that dynamically adjust based
    on available width and minimum column width for optimal responsive behavior.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        cols: Union[int, Dict[str, int]] = 1,
        hspacing: Union[str, int, Dict[str, Union[str, int]]] = "md",
        vspacing: Union[str, int, Dict[str, Union[str, int]]] = None,
        auto_cols: Union[bool, int] = False,
        min_col_width: int = 250,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties (mobile-first)
        self._responsive.set("cols", cols)
        if vspacing is None:
            vspacing = hspacing
        self._responsive.set("hspacing", hspacing)
        self._responsive.set("vspacing", vspacing)

        self._auto_cols = auto_cols
        self._min_col_width = min_col_width
        self._last_width = 0

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

    def _get_min_col_width(self) -> int:
        """Get the minimum column width, from theme or prop."""
        if self._provider:
            theme_min = self._provider.get_theme_value("layout.gridMinColWidth", None)
            if theme_min is not None:
                return theme_min
        return self._min_col_width

    def _update_simple_grid_layout(self) -> None:
        """Compute and apply simple grid layout properties."""
        if not self._layout:
            return

        # Get current responsive values
        cols_val = self._responsive.get("cols", 1)

        # Determine number of columns
        if self._auto_cols:
            available_width = self.width()
            if available_width <= 0:
                num_columns = 1
            else:
                min_width = self._get_min_col_width()
                max_possible = available_width // min_width
                if isinstance(self._auto_cols, int):
                    num_columns = min(max_possible, self._auto_cols)
                else:
                    num_columns = max_possible
                num_columns = max(1, num_columns)
        else:
            num_columns = int(cols_val)

        # Set column stretches to ensure equal widths (QGridLayout doesn't have setColumnCount)
        # The actual column count is determined by where items are placed
        min_width = self._get_min_col_width() if self._auto_cols else 0
        for i in range(num_columns):
            self._layout.setColumnStretch(i, 1)
            self._layout.setColumnMinimumWidth(i, min_width)

        # Apply spacing (horizontal and vertical)
        hspacing_val = self._responsive.get("hspacing", "md")
        vspacing_val = self._responsive.get("vspacing", "md")
        self._layout.setHorizontalSpacing(self._get_spacing_pixels(hspacing_val))
        self._layout.setVerticalSpacing(self._get_spacing_pixels(vspacing_val))

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
    def hspacing(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current horizontal spacing value (responsive)."""
        return self._responsive.get("hspacing", "md")

    @hspacing.setter
    def hspacing(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the horizontal spacing (responsive)."""
        self._responsive.set("hspacing", value)
        self._update_simple_grid_layout()

    @Property(object)
    def vspacing(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current vertical spacing value (responsive)."""
        return self._responsive.get("vspacing", "md")

    @vspacing.setter
    def vspacing(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the vertical spacing (responsive)."""
        self._responsive.set("vspacing", value)
        self._update_simple_grid_layout()

    @Property(object)
    def spacing(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current uniform spacing value (responsive, for backward compatibility)."""
        return self._responsive.get("hspacing", "md")  # Use hspacing as representative

    @spacing.setter
    def spacing(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the uniform spacing for both horizontal and vertical (responsive)."""
        self._responsive.set("hspacing", value)
        self._responsive.set("vspacing", value)
        self._update_simple_grid_layout()

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props and relayout."""
        super().resizeEvent(event)
        new_width = event.size().width()
        if not hasattr(self, "_last_width"):
            self._last_width = new_width
        if abs(new_width - self._last_width) >= 5:
            self._last_width = new_width
            self._update_simple_grid_layout()

    def responsive_cols(self, breakpoints: Dict[str, int]) -> "SimpleGrid":
        """Convenience method to set responsive column counts (mobile-first)."""
        self.cols = breakpoints
        return self

    @Property(bool)
    def auto_cols(self) -> Union[bool, int]:
        """Get whether auto-columns mode is enabled."""
        return self._auto_cols

    @auto_cols.setter
    def auto_cols(self, value: Union[bool, int]) -> None:
        """Set auto-columns mode (True for unlimited, int for max columns)."""
        self._auto_cols = value
        self._update_simple_grid_layout()

    @Property(int)
    def min_col_width(self) -> int:
        """Get the minimum column width in pixels."""
        return self._min_col_width

    @min_col_width.setter
    def min_col_width(self, value: int) -> None:
        """Set the minimum column width in pixels."""
        self._min_col_width = value
        self._update_simple_grid_layout()

    def auto_fit(
        self, max_columns: Optional[int] = None, min_width: Optional[int] = None
    ) -> "SimpleGrid":
        """Convenience method to enable auto-fit columns (CSS Grid auto-fit like)."""
        self.auto_cols = max_columns if max_columns is not None else True
        if min_width is not None:
            self.min_col_width = min_width
        return self

    def responsive_hspacing(
        self, breakpoints: Dict[str, Union[str, int]]
    ) -> "SimpleGrid":
        """Convenience method to set responsive horizontal spacing."""
        self.hspacing = breakpoints
        return self

    def responsive_vspacing(
        self, breakpoints: Dict[str, Union[str, int]]
    ) -> "SimpleGrid":
        """Convenience method to set responsive vertical spacing."""
        self.vspacing = breakpoints
        return self

    def fixed_cols(self, count: int) -> "SimpleGrid":
        """Convenience method to set fixed number of columns."""
        self.cols = count
        self.auto_cols = False
        return self
