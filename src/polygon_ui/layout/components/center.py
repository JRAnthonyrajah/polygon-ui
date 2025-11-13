"""
Center component for Polygon UI layout system.

A utility component that perfectly centers its content both horizontally and vertically.
Supports inline/block behavior, fluid positioning, and max-width constraints.
Uses Qt's built-in layout capabilities for optimal performance and reliability.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Property, QSize

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Center(LayoutComponent):
    """
    Center component that provides perfect centering for its content.

    Supports both horizontal and vertical centering with options for:
    - Inline vs block behavior (affects layout flow)
    - Fluid positioning options
    - Max-width constraints for content
    - Responsive behavior for all properties
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        inline: Union[bool, Dict[str, bool]] = False,
        fluid: Union[bool, Dict[str, bool]] = True,
        max_width: Union[int, str, Dict[str, Union[int, str, None]]] = None,
        max_height: Union[int, str, Dict[str, Union[int, str, None]]] = None,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_inline(inline)
        self._set_fluid(fluid)
        self._set_max_width(max_width)
        self._set_max_height(max_height)

        # Setup centering layout
        self._setup_center_layout()

    def _setup_center_layout(self) -> None:
        """Set up the layout for perfect centering."""
        # Main layout that provides centering
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # Center container that holds content
        self._center_container = QWidget()
        self._center_container.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        # Layout for center container
        self._center_layout = QVBoxLayout(self._center_container)
        self._center_layout.setContentsMargins(0, 0, 0, 0)
        self._center_layout.setSpacing(0)

        # Set center alignment
        self._center_layout.setAlignment(Qt.AlignCenter)

        # Add center container to main layout
        self._main_layout.addWidget(self._center_container)

        # Content container (will hold added children)
        self._content_container = QWidget()
        self._content_layout = QVBoxLayout(self._content_container)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        self._content_layout.setAlignment(Qt.AlignCenter)

        # Add content container to center layout
        self._center_layout.addWidget(self._content_container)

        # Apply initial responsive properties
        self._update_centering_properties()

    def _update_centering_properties(self) -> None:
        """Update centering properties based on responsive values."""
        inline = self._responsive._resolve_value(self._responsive.get("inline", False))
        fluid = self._responsive.get("fluid", True)
        max_width = self._responsive._resolve_value(
            self._responsive.get("max_width", None)
        )
        max_height = self._responsive._resolve_value(
            self._responsive.get("max_height", None)
        )

        # Handle inline vs block behavior
        if inline:
            # Inline behavior: don't expand to fill available space
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self._center_container.setSizePolicy(
                QSizePolicy.Preferred, QSizePolicy.Preferred
            )
        else:
            # Block behavior: expand to fill available space
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self._center_container.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Expanding
            )

        # Handle fluid positioning
        if isinstance(fluid, dict):
            resolved_fluid = self._responsive._resolve_value(fluid)
        else:
            resolved_fluid = fluid

        if not resolved_fluid:
            # Not fluid: use content size
            self._content_container.setSizePolicy(
                QSizePolicy.Preferred, QSizePolicy.Preferred
            )
        else:
            # Fluid: expand within constraints
            self._content_container.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Expanding
            )

        # Apply max-width constraint
        if max_width is not None:
            if isinstance(max_width, str):
                # Theme value (e.g., "md", "lg", "xl")
                if self._provider:
                    max_width_px = self._provider.get_theme_value(
                        f"maxWidths.{max_width}", None
                    )
                else:
                    max_width_px = None
            else:
                # Pixel value
                max_width_px = max_width

            if max_width_px is not None:
                self._content_container.setMaximumWidth(max_width_px)
            else:
                self._content_container.setMaximumWidth(16777215)  # Qt's max value
        else:
            self._content_container.setMaximumWidth(16777215)

        # Apply max-height constraint
        if max_height is not None:
            if isinstance(max_height, str):
                # Theme value
                if self._provider:
                    max_height_px = self._provider.get_theme_value(
                        f"maxHeights.{max_height}", None
                    )
                else:
                    max_height_px = None
            else:
                # Pixel value
                max_height_px = max_height

            if max_height_px is not None:
                self._content_container.setMaximumHeight(max_height_px)
            else:
                self._content_container.setMaximumHeight(16777215)  # Qt's max value
        else:
            self._content_container.setMaximumHeight(16777215)

    def _set_inline(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Private method to set inline property with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_inline = {}

        if isinstance(value, bool):
            full_inline = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = False
            full_inline["base"] = value.get("base", False)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_inline[bp] = current
        else:
            full_inline = {bp: False for bp in breakpoints_order}

        self._responsive.set("inline", full_inline)

    def _set_fluid(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Private method to set fluid property with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_fluid = {}

        if isinstance(value, bool):
            full_fluid = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = True
            full_fluid["base"] = value.get("base", True)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_fluid[bp] = current
        else:
            full_fluid = {bp: True for bp in breakpoints_order}

        self._responsive.set("fluid", full_fluid)

    def _set_max_width(
        self, value: Union[int, str, Dict[str, Union[int, str, None]]]
    ) -> None:
        """Private method to set max_width with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_max_width = {}

        if value is None:
            full_max_width = {bp: None for bp in breakpoints_order}
        elif isinstance(value, (int, str)):
            full_max_width = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = None
            full_max_width["base"] = value.get("base")
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_max_width[bp] = current
        else:
            full_max_width = {bp: None for bp in breakpoints_order}

        self._responsive.set("max_width", full_max_width)

    def _set_max_height(
        self, value: Union[int, str, Dict[str, Union[int, str, None]]]
    ) -> None:
        """Private method to set max_height with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_max_height = {}

        if value is None:
            full_max_height = {bp: None for bp in breakpoints_order}
        elif isinstance(value, (int, str)):
            full_max_height = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = None
            full_max_height["base"] = value.get("base")
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_max_height[bp] = current
        else:
            full_max_height = {bp: None for bp in breakpoints_order}

        self._responsive.set("max_height", full_max_height)

    def _update_responsive_props(self) -> None:
        """Update responsive properties and centering behavior."""
        super()._update_responsive_props()
        self._update_centering_properties()

    # Center Properties (with responsive support)

    @Property(object)
    def inline(self) -> Union[bool, Dict[str, bool]]:
        """Get the current inline setting (responsive)."""
        return self._responsive.get("inline", False)

    @inline.setter
    def inline(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the inline behavior (responsive)."""
        self._set_inline(value)
        self._update_responsive_props()

    @Property(object)
    def fluid(self) -> Union[bool, Dict[str, bool]]:
        """Get the current fluid setting (responsive)."""
        return self._responsive.get("fluid", True)

    @fluid.setter
    def fluid(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the fluid behavior (responsive)."""
        self._set_fluid(value)
        self._update_responsive_props()

    @Property(object)
    def max_width(self) -> Union[int, str, Dict[str, Union[int, str, None]]]:
        """Get the current max_width constraint (responsive)."""
        return self._responsive.get("max_width", None)

    @max_width.setter
    def max_width(
        self, value: Union[int, str, Dict[str, Union[int, str, None]]]
    ) -> None:
        """Set the max_width constraint (responsive)."""
        self._set_max_width(value)
        self._update_responsive_props()

    @Property(object)
    def max_height(self) -> Union[int, str, Dict[str, Union[int, str, None]]]:
        """Get the current max_height constraint (responsive)."""
        return self._responsive.get("max_height", None)

    @max_height.setter
    def max_height(
        self, value: Union[int, str, Dict[str, Union[int, str, None]]]
    ) -> None:
        """Set the max_height constraint (responsive)."""
        self._set_max_height(value)
        self._update_responsive_props()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the centered content area."""
        super().add_child(child, **layout_props)
        # Add to content layout which handles centering
        if self._content_layout:
            self._content_layout.addWidget(child)

    def resizeEvent(self, event) -> None:
        """Handle resize events to update responsive props."""
        super().resizeEvent(event)
        self._update_responsive_props()

    # Convenience methods

    def make_inline(self) -> None:
        """Convenience method: Set inline=True (don't expand to fill space)."""
        self.inline = True

    def make_block(self) -> None:
        """Convenience method: Set inline=False (expand to fill space)."""
        self.inline = False

    def make_fluid(self) -> None:
        """Convenience method: Set fluid=True (expand within constraints)."""
        self.fluid = True

    def make_fixed(self) -> None:
        """Convenience method: Set fluid=False (use content size)."""
        self.fluid = False

    def constrain_width(self, max_width: Union[int, str]) -> None:
        """Convenience method: Set max-width constraint."""
        self.max_width = max_width

    def constrain_height(self, max_height: Union[int, str]) -> None:
        """Convenience method: Set max-height constraint."""
        self.max_height = max_height

    def constrain_both(
        self, max_width: Union[int, str], max_height: Union[int, str]
    ) -> None:
        """Convenience method: Set both max-width and max-height constraints."""
        self.max_width = max_width
        self.max_height = max_height

    def remove_constraints(self) -> None:
        """Convenience method: Remove all width/height constraints."""
        self.max_width = None
        self.max_height = None
