"""
Container component for Polygon UI layout system.

A responsive container component that centers content with configurable max-width
and padding, similar to Mantine's Container component.
"""

from typing import Optional, Union, Dict, Any
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Container(LayoutComponent):
    """
    Container component that provides centered content with configurable sizing
    and padding. Supports fluid behavior and theme-integrated spacing.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        size: Union[str, Dict[str, str]] = "md",
        fluid: Union[bool, Dict[str, bool]] = False,
        px: Union[str, int, Dict[str, Union[str, int]]] = "md",
        py: Union[str, int, Dict[str, Union[str, int]]] = "md",
        center: bool = True,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._responsive.set("size", size)
        self._responsive.set("fluid", fluid)
        self._responsive.set("px", px)
        self._responsive.set("py", py)

        self._center: bool = center

        # Size breakpoints (Mantine-inspired)
        self._size_map = {
            "xs": 540,
            "sm": 720,
            "md": 960,
            "lg": 1140,
            "xl": 1600,
        }

        # Set up vertical layout for stacking children
        self._setup_layout()

        # Apply initial styling
        self._update_container_styling()

    def _setup_layout(self) -> None:
        """Set up the Qt layout for the Container."""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)  # Padding handled via properties
        if self._center:
            self._layout.setAlignment(Qt.AlignHCenter)

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value to pixels using theme or fallback."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 16)
            else:
                return int(spacing_value)
        return 16 if isinstance(spacing_value, str) else spacing_value

    def _update_container_styling(self) -> None:
        """Update container styling based on current properties."""
        # Get responsive values
        size_val = self._responsive.get("size", "md")
        fluid_val = self._responsive.get("fluid", False)
        px_val = self._responsive.get("px", "md")
        py_val = self._responsive.get("py", "md")

        # Update padding
        px_pixels = self._get_spacing_pixels(px_val)
        py_pixels = self._get_spacing_pixels(py_val)
        if self._layout:
            self._layout.setContentsMargins(px_pixels, py_pixels, px_pixels, py_pixels)

        # Update sizing
        if fluid_val:
            self.setMaximumWidth(16777215)  # QWidget max size
            self.setMaximumHeight(16777215)
        else:
            max_width = self._size_map.get(size_val, 960)
            self.setMaximumWidth(max_width)
            self.setMaximumHeight(16777215)  # No height limit

        # Update alignment if center toggled
        if self._layout:
            self._layout.setAlignment(Qt.AlignHCenter if self._center else Qt.AlignLeft)

        # Regenerate QSS if needed (for additional visual styling)
        self._update_styling()

    # Property: size
    @Property(str)
    def size(self) -> str:
        """Get the current resolved container size (xs, sm, md, lg, xl)."""
        return self._responsive.get("size", "md")

    @size.setter
    def size(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the container size. Can be str or responsive dict."""
        self._responsive.set("size", value)
        self._update_container_styling()

    # Property: fluid
    @Property(bool)
    def fluid(self) -> bool:
        """Get the current resolved fluid behavior (no max-width limit)."""
        return self._responsive.get("fluid", False)

    @fluid.setter
    def fluid(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set fluid behavior. Can be bool or responsive dict."""
        self._responsive.set("fluid", value)
        self._update_container_styling()

    # Property: px (horizontal padding)
    @Property(Union[str, int])
    def px(self) -> Union[str, int]:
        """Get the current resolved horizontal padding."""
        return self._responsive.get("px", "md")

    @px.setter
    def px(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set horizontal padding. Can be str/int or responsive dict."""
        self._responsive.set("px", value)
        self._update_container_styling()

    # Property: py (vertical padding)
    @Property(Union[str, int])
    def py(self) -> Union[str, int]:
        """Get the current resolved vertical padding."""
        return self._responsive.get("py", "md")

    @py.setter
    def py(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set vertical padding. Can be str/int or responsive dict."""
        self._responsive.set("py", value)
        self._update_container_styling()

    # Property: center
    @Property(bool)
    def center(self) -> bool:
        """Get centering behavior for children."""
        return self._center

    @center.setter
    def center(self, value: bool) -> None:
        """Set centering behavior."""
        self._center = value
        if self._layout:
            self._layout.setAlignment(Qt.AlignHCenter if value else Qt.AlignLeft)
        self._update_styling()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the container, applying layout props if needed."""
        super().add_child(child, **layout_props)
        # For container, children are centered by default via layout alignment

    def resizeEvent(self, event) -> None:
        """Handle resize events with responsive updates."""
        super().resizeEvent(event)
        # Invalidate responsive cache and update styling
        self._responsive._invalidate_all_cache()
        self._update_container_styling()
