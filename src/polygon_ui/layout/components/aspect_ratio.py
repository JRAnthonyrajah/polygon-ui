"""
AspectRatio component for Polygon UI layout system.

A utility component that maintains a specific aspect ratio for its content.
Supports numeric ratios, preset ratios (16/9, 4/3, 1/1, etc.), and responsive behavior.
Ensures content preserves its proportions while fitting within available space.
"""

from typing import Optional, Any, Dict, Union, Tuple
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Property, QSize, QRect
from fractions import Fraction

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class AspectRatio(LayoutComponent):
    """
    AspectRatio component that maintains a specific aspect ratio for its content.

    Supports:
    - Numeric ratios (e.g., 16/9, 4/3, 1.5)
    - Preset ratios (square, golden, widescreen, etc.)
    - Responsive ratio changes
    - Content scaling and overflow handling
    - Style props integration
    """

    # Common aspect ratio presets
    RATIOS = {
        "square": 1.0,  # 1:1
        "golden": 1.618,  # Golden ratio (~1.618:1)
        "widescreen": 16 / 9,  # 16:9
        "standard": 4 / 3,  # 4:3
        "cinema": 2.39,  # CinemaScope (~2.39:1)
        "portrait": 3 / 4,  # 3:4 (inverse of standard)
        "photo": 4 / 3,  # Photo standard
        "panorama": 3 / 1,  # 3:1 (very wide)
    }

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        ratio: Union[float, str, Dict[str, Union[float, str]]] = "square",
        preserve_content: bool = True,
        overflow: str = "hidden",
        min_width: Union[int, Dict[str, int]] = 0,
        min_height: Union[int, Dict[str, int]] = 0,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_ratio(ratio)
        self._responsive.set("preserve_content", preserve_content)
        self._responsive.set("overflow", overflow)
        self._set_min_width(min_width)
        self._set_min_height(min_height)

        # Setup aspect ratio layout
        self._setup_aspect_layout()

    def _setup_aspect_layout(self) -> None:
        """Set up the layout for maintaining aspect ratio."""
        # Main layout
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # Content container (will maintain aspect ratio)
        self._content_container = QWidget()
        self._content_container.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        # Layout for content container
        self._content_layout = QVBoxLayout(self._content_container)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)
        self._content_layout.setAlignment(Qt.AlignCenter)

        # Add content container to main layout
        self._main_layout.addWidget(self._content_container)

        # Apply initial responsive properties
        self._update_aspect_properties()

    def _get_ratio_value(self, ratio_input: Union[float, str]) -> float:
        """Convert ratio input to float value."""
        if isinstance(ratio_input, (int, float)):
            return float(ratio_input)
        elif isinstance(ratio_input, str):
            # Handle fraction format "16/9"
            if "/" in ratio_input:
                try:
                    num, denom = ratio_input.split("/")
                    return float(num) / float(denom)
                except (ValueError, ZeroDivisionError):
                    pass

            # Handle preset ratios
            ratio_lower = ratio_input.lower()
            if ratio_lower in self.RATIOS:
                return self.RATIOS[ratio_lower]

            # Handle decimal string
            try:
                return float(ratio_input)
            except ValueError:
                pass

        # Default to square if invalid
        return 1.0

    def _update_aspect_properties(self) -> None:
        """Update aspect ratio properties based on responsive values."""
        ratio = self._responsive._resolve_value(self._responsive.get("ratio", 1.0))
        preserve_content = self._responsive.get("preserve_content", True)
        overflow = self._responsive.get("overflow", "hidden")
        min_width = self._responsive._resolve_value(
            self._responsive.get("min_width", 0)
        )
        min_height = self._responsive._resolve_value(
            self._responsive.get("min_height", 0)
        )

        # Convert ratio to float if needed
        if ratio is None:
            self._current_ratio = 1.0  # Default to square
        elif isinstance(ratio, str):
            self._current_ratio = self._get_ratio_value(ratio)
        else:
            self._current_ratio = float(ratio)

        # Store current settings
        self._preserve_content = preserve_content
        self._overflow = overflow

        # Apply minimum size constraints
        if min_width and min_width > 0:
            self.setMinimumWidth(min_width)
        if min_height and min_height > 0:
            self.setMinimumHeight(min_height)

        # Update layout
        self._update_aspect_layout()

    def _update_aspect_layout(self) -> None:
        """Update the layout to maintain aspect ratio."""
        if not hasattr(self, "_current_ratio"):
            return

        # Calculate target size based on available space and aspect ratio
        available_size = self.sizeHint()
        available_width = available_size.width()
        available_height = available_size.height()

        if available_width <= 0 or available_height <= 0:
            return

        # Calculate dimensions that maintain aspect ratio
        target_width = available_height * self._current_ratio
        target_height = available_width / self._current_ratio

        # Choose dimensions that fit within available space
        if target_width <= available_width:
            # Width-limited: use calculated width, full height
            final_width = int(target_width)
            final_height = available_height
        else:
            # Height-limited: use full width, calculated height
            final_width = available_width
            final_height = int(target_height)

        # Apply content container size
        self._content_container.setFixedSize(final_width, final_height)

        # Handle overflow
        if self._overflow == "hidden":
            self._content_container.setClipChildren(True)
        else:
            self._content_container.setClipChildren(False)

    def _set_ratio(
        self, value: Union[float, str, Dict[str, Union[float, str]]]
    ) -> None:
        """Private method to set ratio with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_ratio = {}

        if isinstance(value, (int, float, str)):
            full_ratio = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "square"  # Default
            full_ratio["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_ratio[bp] = current
        else:
            full_ratio = {bp: "square" for bp in breakpoints_order}

        self._responsive.set("ratio", full_ratio)

    def _set_min_width(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set min_width with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_min_width = {}

        if isinstance(value, int):
            full_min_width = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_min_width["base"] = value.get("base", 0)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_min_width[bp] = current
        else:
            full_min_width = {bp: 0 for bp in breakpoints_order}

        # Ensure non-negative values
        for bp in breakpoints_order:
            full_min_width[bp] = max(0, full_min_width[bp])

        self._responsive.set("min_width", full_min_width)

    def _set_min_height(self, value: Union[int, Dict[str, int]]) -> None:
        """Private method to set min_height with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_min_height = {}

        if isinstance(value, int):
            full_min_height = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_min_height["base"] = value.get("base", 0)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_min_height[bp] = current
        else:
            full_min_height = {bp: 0 for bp in breakpoints_order}

        # Ensure non-negative values
        for bp in breakpoints_order:
            full_min_height[bp] = max(0, full_min_height[bp])

        self._responsive.set("min_height", full_min_height)

    def _update_responsive_props(self) -> None:
        """Update responsive properties and aspect ratio behavior."""
        super()._update_responsive_props()
        self._update_aspect_properties()

    def resizeEvent(self, event) -> None:
        """Handle resize events to maintain aspect ratio."""
        super().resizeEvent(event)
        self._update_aspect_layout()

    # AspectRatio Properties (with responsive support)

    @Property(object)
    def ratio(self) -> Union[float, str, Dict[str, Union[float, str]]]:
        """Get the current aspect ratio (responsive)."""
        return self._responsive.get("ratio", "square")

    @ratio.setter
    def ratio(self, value: Union[float, str, Dict[str, Union[float, str]]]) -> None:
        """Set the aspect ratio (responsive)."""
        self._set_ratio(value)
        self._update_responsive_props()

    @Property(bool)
    def preserve_content(self) -> bool:
        """Get whether content preservation is enabled."""
        return self._responsive.get("preserve_content", True)

    @preserve_content.setter
    def preserve_content(self, value: bool) -> None:
        """Set whether to preserve content when scaling."""
        self._responsive.set("preserve_content", value)
        self._update_responsive_props()

    @Property(str)
    def overflow(self) -> str:
        """Get the current overflow behavior."""
        return self._responsive.get("overflow", "hidden")

    @overflow.setter
    def overflow(self, value: str) -> None:
        """Set the overflow behavior ('hidden', 'visible', 'scroll')."""
        valid_values = ["hidden", "visible", "scroll"]
        if value in valid_values:
            self._responsive.set("overflow", value)
            self._update_responsive_props()

    @Property(object)
    def min_width(self) -> Union[int, Dict[str, int]]:
        """Get the current min_width constraint (responsive)."""
        return self._responsive.get("min_width", 0)

    @min_width.setter
    def min_width(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the min_width constraint (responsive)."""
        self._set_min_width(value)
        self._update_responsive_props()

    @Property(object)
    def min_height(self) -> Union[int, Dict[str, int]]:
        """Get the current min_height constraint (responsive)."""
        return self._responsive.get("min_height", 0)

    @min_height.setter
    def min_height(self, value: Union[int, Dict[str, int]]) -> None:
        """Set the min_height constraint (responsive)."""
        self._set_min_height(value)
        self._update_responsive_props()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the aspect ratio container."""
        super().add_child(child, **layout_props)
        # Add to content layout
        if self._content_layout:
            self._content_layout.addWidget(child)

    # Convenience methods

    def set_square(self) -> None:
        """Convenience method: Set ratio to 1:1 (square)."""
        self.ratio = "square"

    def set_widescreen(self) -> None:
        """Convenience method: Set ratio to 16:9 (widescreen)."""
        self.ratio = "widescreen"

    def set_standard(self) -> None:
        """Convenience method: Set ratio to 4:3 (standard)."""
        self.ratio = "standard"

    def set_portrait(self) -> None:
        """Convenience method: Set ratio to 3:4 (portrait)."""
        self.ratio = "portrait"

    def set_golden(self) -> None:
        """Convenience method: Set ratio to golden ratio (~1.618:1)."""
        self.ratio = "golden"

    def set_custom_ratio(self, width: float, height: float) -> None:
        """Convenience method: Set custom ratio from width and height."""
        if height > 0:
            custom_ratio = width / height
            self.ratio = custom_ratio

    def show_overflow(self) -> None:
        """Convenience method: Show overflow content."""
        self.overflow = "visible"

    def hide_overflow(self) -> None:
        """Convenience method: Hide overflow content."""
        self.overflow = "hidden"

    def get_current_ratio(self) -> float:
        """Get the currently resolved aspect ratio value."""
        if hasattr(self, "_current_ratio"):
            return self._current_ratio
        return 1.0

    def get_target_size(
        self, available_width: int, available_height: int
    ) -> Tuple[int, int]:
        """Calculate target size for given available dimensions."""
        if not hasattr(self, "_current_ratio"):
            return available_width, available_height

        target_width = available_height * self._current_ratio
        target_height = available_width / self._current_ratio

        if target_width <= available_width:
            return int(target_width), available_height
        else:
            return available_width, int(target_height)
