"""
Group component for Polygon UI layout system.

A horizontal grouping component using QHBoxLayout, similar to Mantine's Group component.
Supports gap spacing, alignment, wrapping, and child widget sizing.
"""

from typing import Optional, Any, Dict, Union

from PySide6.QtWidgets import QHBoxLayout, QWidget, QSizePolicy
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

        # Set up horizontal layout for grouping children
        self._setup_layout()

        # Apply initial styling
        self._update_group_styling()

    def _setup_layout(self) -> None:
        """Set up the Qt layout for the Group (horizontal by default)."""
        # Create horizontal layout for Group
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)  # No default margins

        # Default alignment for horizontal group
        self._layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value to pixels using theme or fallback."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            else:
                return int(spacing_value)
        return 8 if isinstance(spacing_value, str) else spacing_value

    def _update_group_styling(self) -> None:
        """Update group styling based on current properties."""
        # Get responsive values
        gap_val = self._responsive.get("gap", "md")
        align_val = self._responsive.get("align", "center")
        justify_val = self._responsive.get("justify", "start")
        wrap_val = self._responsive.get("wrap", False)
        spacing_val = self._responsive.get("spacing", gap_val)

        # Update spacing between children
        spacing_pixels = self._get_spacing_pixels(spacing_val)
        if self._layout:
            self._layout.setSpacing(spacing_pixels)

        # Update alignment for horizontal layout
        if self._layout:
            # Vertical alignment (cross-axis)
            vertical_alignment = Qt.AlignVCenter  # Default
            if align_val == "start":
                vertical_alignment = Qt.AlignTop
            elif align_val == "end":
                vertical_alignment = Qt.AlignBottom
            elif align_val == "center":
                vertical_alignment = Qt.AlignVCenter
            elif align_val == "stretch":
                vertical_alignment = Qt.AlignTop | Qt.AlignBottom

            # Horizontal alignment (main-axis)
            horizontal_alignment = Qt.AlignLeft  # Default
            if justify_val == "center":
                horizontal_alignment = Qt.AlignHCenter
            elif justify_val == "end":
                horizontal_alignment = Qt.AlignRight
            elif justify_val == "space-between":
                horizontal_alignment = Qt.AlignJustify
            elif justify_val == "space-around":
                horizontal_alignment = Qt.AlignHCenter  # Approximate with center

            # Combined alignment
            self._layout.setAlignment(vertical_alignment | horizontal_alignment)

        # Handle wrapping (simplified - would need custom layout for true wrapping)
        self._wrap_children = wrap_val

        # Generate QSS if needed
        self._update_styling()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the group with optional layout props."""
        if self.layout() and child:
            # Apply child-specific sizing properties
            self._apply_child_sizing(child, layout_props)
            self.layout().addWidget(child)
        else:
            # Fallback to base class implementation
            super().add_child(child, **layout_props)

    def _apply_child_sizing(self, child: QWidget, layout_props: Dict[str, Any]) -> None:
        """Apply sizing properties to a child widget for horizontal layout."""
        # Handle grow property
        if layout_props.get("grow", False):
            child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Handle shrink property
        elif layout_props.get("shrink", False):
            child.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Handle fixed sizing
        elif layout_props.get("flex", "none") == "none":
            child.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Handle flex basis (preferred size)
        if "flex_basis" in layout_props:
            basis = layout_props["flex_basis"]
            if isinstance(basis, (int, str)) and str(basis).isdigit():
                child.setMinimumWidth(int(basis))
            else:
                child.setMinimumWidth(100)  # Default basis

        # Handle vertical alignment for individual child
        if "align" in layout_props:
            align = layout_props["align"]
            if align == "start":
                child.setAlignment(Qt.AlignTop)
            elif align == "center":
                child.setAlignment(Qt.AlignVCenter)
            elif align == "end":
                child.setAlignment(Qt.AlignBottom)

    # Property: gap
    @Property(str)
    def gap(self) -> str:
        """Get the current resolved gap spacing."""
        return self._responsive.get("gap", "md")

    @gap.setter
    def gap(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the gap spacing. Can be str/int or responsive dict."""
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
