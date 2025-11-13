"""
Space component for Polygon UI layout system.

A flexible spacing utility component for creating gaps and whitespace.
Supports height and width dimensions, flex grow/shrink behavior,
responsive sizing, and negative space support.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Space(LayoutComponent):
    """
    Space component that provides flexible spacing between elements.

    Supports:
    - Height (h) and width (w) dimensions
    - Flex grow/shrink behavior
    - Responsive sizing support
    - Negative space support
    - Conditional spacing
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        h: Union[int, str, Dict[str, Union[int, str]]] = 0,
        w: Union[int, str, Dict[str, Union[int, str]]] = 0,
        flex: Union[int, str, Dict[str, Union[int, str]]] = None,
        shrink: Union[int, str, Dict[str, Union[int, str]]] = 1,
        negative: Union[bool, Dict[str, bool]] = False,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_h(h)
        self._set_w(w)
        self._set_flex(flex)
        self._set_shrink(shrink)
        self._set_negative(negative)

        # Setup space properties
        self._setup_space_properties()

    def _setup_space_properties(self) -> None:
        """Set up the space component properties."""
        # Apply initial responsive properties
        self._update_space_properties()

    def _update_space_properties(self) -> None:
        """Update space properties based on responsive values."""
        h = self._responsive._resolve_value(self._responsive.get("h", 0))
        w = self._responsive._resolve_value(self._responsive.get("w", 0))
        flex = self._responsive._resolve_value(self._responsive.get("flex", None))
        shrink = self._responsive._resolve_value(self._responsive.get("shrink", 1))
        negative = self._responsive._resolve_value(
            self._responsive.get("negative", False)
        )

        # Convert values to pixels
        h_px = self._resolve_size_value(h)
        w_px = self._resolve_size_value(w)
        flex_val = self._resolve_flex_value(flex)
        shrink_val = self._resolve_flex_value(shrink)

        # Apply sizing
        if h_px > 0:
            actual_h = -h_px if negative else h_px
            self.setFixedHeight(max(1, actual_h))  # Minimum 1px for Qt
        else:
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)  # Qt max

        if w_px > 0:
            actual_w = -w_px if negative else w_px
            self.setFixedWidth(max(1, actual_w))  # Minimum 1px for Qt
        else:
            self.setMinimumWidth(0)
            self.setMaximumWidth(16777215)  # Qt max

        # Apply flex behavior
        if flex_val is not None:
            # Flex grow behavior
            if h_px > 0:
                # Vertical flex
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            elif w_px > 0:
                # Horizontal flex
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            else:
                # Both dimensions flex
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            # Fixed size behavior
            if h_px > 0 and w_px > 0:
                self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            elif h_px > 0:
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            elif w_px > 0:
                self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            else:
                self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def _resolve_size_value(self, size_value: Union[int, str]) -> int:
        """Convert size value to pixels."""
        if isinstance(size_value, int):
            return max(0, size_value)
        elif isinstance(size_value, str):
            # Theme spacing values
            spacing_map = {
                "xs": 4,
                "sm": 8,
                "md": 16,
                "lg": 24,
                "xl": 32,
                "2xl": 48,
                "3xl": 64,
                "4xl": 96,
                "5xl": 128,
            }
            return spacing_map.get(size_value.lower(), 0)
        return 0

    def _resolve_flex_value(self, flex_value: Union[int, str, None]) -> Optional[int]:
        """Convert flex value to integer."""
        if flex_value is None:
            return None
        elif isinstance(flex_value, int):
            return max(0, flex_value)
        elif isinstance(flex_value, str):
            if flex_value.lower() in ["auto", "true", "1"]:
                return 1
            elif flex_value.lower() in ["false", "0"]:
                return 0
            else:
                try:
                    return max(0, int(flex_value))
                except ValueError:
                    return 1
        return 0

    # Private setters for responsive properties
    def _set_h(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Private method to set height with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_h = {}

        if isinstance(value, (int, str)):
            full_h = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_h["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_h[bp] = current
        else:
            full_h = {bp: 0 for bp in breakpoints_order}

        self._responsive.set("h", full_h)

    def _set_w(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Private method to set width with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_w = {}

        if isinstance(value, (int, str)):
            full_w = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_w["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_w[bp] = current
        else:
            full_w = {bp: 0 for bp in breakpoints_order}

        self._responsive.set("w", full_w)

    def _set_flex(
        self, value: Union[int, str, Dict[str, Union[int, str]], None]
    ) -> None:
        """Private method to set flex with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_flex = {}

        if value is None:
            full_flex = {bp: None for bp in breakpoints_order}
        elif isinstance(value, (int, str)):
            full_flex = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = None
            full_flex["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_flex[bp] = current
        else:
            full_flex = {bp: None for bp in breakpoints_order}

        self._responsive.set("flex", full_flex)

    def _set_shrink(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Private method to set shrink with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_shrink = {}

        if isinstance(value, (int, str)):
            full_shrink = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 1
            full_shrink["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_shrink[bp] = current
        else:
            full_shrink = {bp: 1 for bp in breakpoints_order}

        self._responsive.set("shrink", full_shrink)

    def _set_negative(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Private method to set negative with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_negative = {}

        if isinstance(value, bool):
            full_negative = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = False
            full_negative["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_negative[bp] = current
        else:
            full_negative = {bp: False for bp in breakpoints_order}

        self._responsive.set("negative", full_negative)

    def _update_responsive_props(self) -> None:
        """Update responsive properties and space behavior."""
        super()._update_responsive_props()
        self._update_space_properties()

    # Space Properties (with responsive support)

    @Property(object)
    def h(self) -> Union[int, str, Dict[str, Union[int, str]]]:
        """Get the current height (responsive)."""
        return self._responsive.get("h", 0)

    @h.setter
    def h(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Set the height (responsive)."""
        self._set_h(value)
        self._update_responsive_props()

    @Property(object)
    def w(self) -> Union[int, str, Dict[str, Union[int, str]]]:
        """Get the current width (responsive)."""
        return self._responsive.get("w", 0)

    @w.setter
    def w(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Set the width (responsive)."""
        self._set_w(value)
        self._update_responsive_props()

    @Property(object)
    def flex(self) -> Union[int, str, Dict[str, Union[int, str]], None]:
        """Get the current flex value (responsive)."""
        return self._responsive.get("flex", None)

    @flex.setter
    def flex(self, value: Union[int, str, Dict[str, Union[int, str]], None]) -> None:
        """Set the flex value (responsive)."""
        self._set_flex(value)
        self._update_responsive_props()

    @Property(object)
    def shrink(self) -> Union[int, str, Dict[str, Union[int, str]]]:
        """Get the current shrink value (responsive)."""
        return self._responsive.get("shrink", 1)

    @shrink.setter
    def shrink(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Set the shrink value (responsive)."""
        self._set_shrink(value)
        self._update_responsive_props()

    @Property(object)
    def negative(self) -> Union[bool, Dict[str, bool]]:
        """Get the current negative setting (responsive)."""
        return self._responsive.get("negative", False)

    @negative.setter
    def negative(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the negative space setting (responsive)."""
        self._set_negative(value)
        self._update_responsive_props()

    # Convenience methods

    def set_height(self, height: Union[int, str]) -> None:
        """Convenience method: Set height."""
        self.h = height

    def set_width(self, width: Union[int, str]) -> None:
        """Convenience method: Set width."""
        self.w = width

    def set_size(self, size: Union[int, str]) -> None:
        """Convenience method: Set both height and width."""
        self.h = size
        self.w = size

    def set_flex_grow(self, flex: int = 1) -> None:
        """Convenience method: Set flex grow."""
        self.flex = flex

    def set_flex_none(self) -> None:
        """Convenience method: Remove flex behavior."""
        self.flex = None

    def enable_negative(self) -> None:
        """Convenience method: Enable negative space."""
        self.negative = True

    def disable_negative(self) -> None:
        """Convenience method: Disable negative space."""
        self.negative = False

    # Preset spacing methods
    def spacing_xs(self) -> None:
        """Set extra small spacing (4px)."""
        self.set_size("xs")

    def spacing_sm(self) -> None:
        """Set small spacing (8px)."""
        self.set_size("sm")

    def spacing_md(self) -> None:
        """Set medium spacing (16px)."""
        self.set_size("md")

    def spacing_lg(self) -> None:
        """Set large spacing (24px)."""
        self.set_size("lg")

    def spacing_xl(self) -> None:
        """Set extra large spacing (32px)."""
        self.set_size("xl")

    # Vertical/horizontal specific methods
    def vertical_space(self, height: Union[int, str]) -> None:
        """Create vertical space only."""
        self.h = height
        self.w = 0

    def horizontal_space(self, width: Union[int, str]) -> None:
        """Create horizontal space only."""
        self.h = 0
        self.w = width

    def flexible_space(self) -> None:
        """Create flexible space that grows."""
        self.flex = 1

    def fixed_space(self, size: Union[int, str]) -> None:
        """Create fixed space."""
        self.set_size(size)
        self.flex = None
