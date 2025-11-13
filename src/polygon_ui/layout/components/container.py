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


class Container(LayoutComponent):
    """
    Container component that provides centered content with configurable sizing
    and padding. Supports fluid behavior and theme-integrated spacing.
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        size: str = "md",
        fluid: bool = False,
        px: Union[str, int] = "md",
        py: Union[str, int] = "md",
        center: bool = True,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Container-specific properties
        self._size: str = size
        self._fluid: bool = fluid
        self._px: Union[str, int] = px
        self._py: Union[str, int] = py
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
        # Update padding
        px_pixels = self._get_spacing_pixels(self._px)
        py_pixels = self._get_spacing_pixels(self._py)
        if self._layout:
            self._layout.setContentsMargins(px_pixels, py_pixels, px_pixels, py_pixels)

        # Update sizing
        if self._fluid:
            self.setMaximumWidth(16777215)  # QWidget max size
            self.setMaximumHeight(16777215)
        else:
            max_width = self._size_map.get(self._size, 960)
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
        """Get the container size (xs, sm, md, lg, xl)."""
        return self._size

    @size.setter
    def size(self, value: str) -> None:
        """Set the container size."""
        if value in self._size_map:
            self._size = value
            self._update_container_styling()
        else:
            raise ValueError(
                f"Invalid size: {value}. Must be one of {list(self._size_map.keys())}"
            )

    # Property: fluid
    @Property(bool)
    def fluid(self) -> bool:
        """Get fluid behavior (no max-width limit)."""
        return self._fluid

    @fluid.setter
    def fluid(self, value: bool) -> None:
        """Set fluid behavior."""
        self._fluid = value
        self._update_container_styling()

    # Property: px (horizontal padding)
    @Property(Union[str, int])
    def px(self) -> Union[str, int]:
        """Get horizontal padding."""
        return self._px

    @px.setter
    def px(self, value: Union[str, int]) -> None:
        """Set horizontal padding (theme spacing key or pixels)."""
        self._px = value
        self._update_container_styling()

    # Property: py (vertical padding)
    @Property(Union[str, int])
    def py(self) -> Union[str, int]:
        """Get vertical padding."""
        return self._py

    @py.setter
    def py(self, value: Union[str, int]) -> None:
        """Set vertical padding (theme spacing key or pixels)."""
        self._py = value
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
        """Handle resize events (basic support; responsive in Task #16)."""
        super().resizeEvent(event)
        # For now, no responsive updates; defer to Task #16
