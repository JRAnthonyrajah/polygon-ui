"""
Box component for Polygon UI - versatile styled container with layout support.

Supports style props (m, p, bg, c, border) with responsive capabilities,
and layout modes (block, flex, grid) using Qt layouts for basic behavior.
For advanced flex/grid, consider using dedicated Flex/Grid components.
Integrates with theme system via PolygonProvider for spacing and colors.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Box(LayoutComponent):
    """
    Box component that extends QWidget with full StyleProps integration.

    Provides support for all major style properties (margin, padding, background,
    color, border) with responsive design capabilities. Also supports layout
    properties for flex and grid behavior using Qt's built-in layouts for basic
    functionality. For advanced flexbox/grid features, use dedicated Flex/Grid
    components.

    Enhanced with advanced responsive style props: width, height, borderRadius, boxShadow.
    Layout properties: justify, align, gap, wrap (basic implementation).
    Supports component composition via add_child and nesting.
    Convenience methods for common layout patterns: center_content, vertical_stack, horizontal_stack.
    Class method for common use cases: Box.card().

    Integrates with the theme system for consistent spacing, colors, and typography.
    Includes basic event handling overrides for mouse and resize events. Responsive
    behavior updates on resize using breakpoint system (base, sm, md, lg, xl).

    Example:
        box = Box(m="md", p="lg", bg="gray.100", display="flex", justify="center")
        box.add_child(child_widget)
        # Or use convenience
        card = Box.card(p="lg")
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        # Style props (short forms for convenience)
        m: Union[str, Dict[str, str], None] = None,  # margin
        p: Union[str, Dict[str, str], None] = None,  # padding
        bg: Union[str, Dict[str, str], None] = None,  # background-color
        c: Union[str, Dict[str, str], None] = None,  # color
        border: Union[str, Dict[str, str], None] = None,
        # Layout props
        display: str = "block",  # 'block', 'flex', 'grid'
        direction: str = "row",  # for flex/grid
        justify: Union[str, Dict[str, str]] = "start",
        align: Union[str, Dict[str, str]] = "stretch",
        gap: Union[str, int, Dict[str, Union[str, int]], None] = None,
        wrap: Union[bool, str, Dict[str, Union[bool, str]], None] = None,
        # Size props
        width: Union[str, Dict[str, str], None] = None,
        height: Union[str, Dict[str, str], None] = None,
        # Advanced style props
        borderRadius: Union[str, Dict[str, str], None] = None,
        boxShadow: Union[str, Dict[str, str], None] = None,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive handler for both style and layout props
        self._responsive = ResponsiveProps(self)

        # Initialize style props (responsive)
        self._responsive.set("m", m or {})
        self._responsive.set("p", p or {})
        self._responsive.set("bg", bg or {})
        self._responsive.set("c", c or {})
        self._responsive.set("border", border or {})

        # Layout props
        self._responsive.set("display", display)
        self._responsive.set("direction", direction)
        self._responsive.set("justify", justify)
        self._responsive.set("align", align)
        self._responsive.set("gap", gap or {})
        self._responsive.set("wrap", wrap or False)
        self._responsive.set("width", width or {})
        self._responsive.set("height", height or {})
        self._responsive.set("borderRadius", borderRadius or {})
        self._responsive.set("boxShadow", boxShadow or {})

        # Internal state
        self._display = display
        self._direction = direction
        self._layout_mode_set = False

        # Setup layout mode based on display
        self._setup_layout_mode()

        # Initial updates
        self._update_styling()
        self._update_layout_styling()

    def _setup_layout_mode(self) -> None:
        """
        Set up the internal Qt layout based on the display mode.
        - 'block': No layout (manual child management)
        - 'flex': QBoxLayout (H/V based on direction)
        - 'grid': QGridLayout (basic grid)
        """
        if self._layout_mode_set:
            # Clear existing layout if changing mode
            if self._layout:
                while self._layout.count():
                    child = self._layout.takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)
                self._layout = None

        display_val = self._responsive.get("display", "block")

        if display_val == "flex":
            direction_val = self._responsive.get("direction", "row")
            if direction_val in ["row", "row-reverse"]:
                self._layout = QHBoxLayout(self)
            else:
                self._layout = QVBoxLayout(self)
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setSpacing(0)  # Gap handled via theme in styling
            self._layout_mode_set = True
        elif display_val == "grid":
            self._layout = QGridLayout(self)
            self._layout.setContentsMargins(0, 0, 0, 0)
            self._layout.setSpacing(0)  # Gutter via theme
            self._layout_mode_set = True
        else:
            # Block mode: no automatic layout, children added manually
            self._layout = None
            self._layout_mode_set = True

        # Re-add existing children to new layout
        for child in self._children[:]:
            self.add_child(child)

    def _get_responsive_style_value(self, prop_key: str, default: str = "") -> str:
        """
        Get the current responsive value for a style property and convert to CSS string.
        Uses theme provider for spacing and colors.
        """
        # Handle case where _responsive hasn't been initialized yet (during parent __init__)
        if not hasattr(self, "_responsive"):
            return default

        value = self._responsive.get(prop_key, default)
        if not value:
            return ""

        if isinstance(value, dict):
            # Use current breakpoint value
            current_bp = self._get_current_breakpoint()
            # Simple fallback to 'base' or first value
            value = value.get("base", next(iter(value.values()), default))

        if prop_key in ["m", "p"] and isinstance(value, str) and self._provider:
            # Spacing from theme
            px_value = self._provider.get_theme_value(f"spacing.{value}", 8)
            return f"{px_value}px"
        elif prop_key in ["bg", "c"] and isinstance(value, str) and self._provider:
            # Color from theme
            theme_key = f"colors.{value}" if "." not in value else value
            color_value = self._provider.get_theme_value(theme_key, value)
            return color_value
        elif prop_key == "border" and isinstance(value, str):
            # Border string like "1px solid gray"
            if self._provider:
                # Could parse and resolve colors/spacing, but keep simple
                pass
            return value
        elif prop_key == "borderRadius" and isinstance(value, str) and self._provider:
            px_value = self._provider.get_theme_value(f"spacing.{value}", 4)
            return f"{px_value}px"
        return str(value)

    def _update_styling(self) -> None:
        """Generate and apply QSS based on current style props."""
        super()._update_styling()

        qss_parts = []

        # Margin
        margin_val = self._get_responsive_style_value("m")
        if margin_val:
            qss_parts.append(f"margin: {margin_val};")

        # Padding
        padding_val = self._get_responsive_style_value("p")
        if padding_val:
            qss_parts.append(f"padding: {padding_val};")

        # Background
        bg_val = self._get_responsive_style_value("bg")
        if bg_val:
            qss_parts.append(f"background-color: {bg_val};")

        # Color
        color_val = self._get_responsive_style_value("c")
        if color_val:
            qss_parts.append(f"color: {color_val};")

        # Border
        border_val = self._get_responsive_style_value("border")
        if border_val:
            qss_parts.append(f"border: {border_val};")

        # Border Radius
        br_val = self._get_responsive_style_value("borderRadius")
        if br_val:
            qss_parts.append(f"border-radius: {br_val};")

        # Box Shadow
        shadow_val = self._get_responsive_style_value("boxShadow")
        if shadow_val:
            qss_parts.append(f"box-shadow: {shadow_val};")

        if qss_parts:
            self.setStyleSheet(" ".join(qss_parts))

    def _update_layout_styling(self) -> None:
        """Update layout-specific styling (gaps, alignment)."""

        if self._layout:
            # Gap
            gap_val = self._responsive.get("gap", "none")
            if gap_val != "none":
                spacing = self._get_spacing_pixels(gap_val)
                self._layout.setSpacing(spacing)

            # Alignment
            justify_val = self._responsive.get("justify", "start")
            align_val = self._responsive.get("align", "stretch")
            if isinstance(self._layout, QHBoxLayout):
                h_align = Qt.AlignLeft
                if justify_val == "center":
                    h_align = Qt.AlignHCenter
                elif justify_val == "end":
                    h_align = Qt.AlignRight
                v_align = Qt.AlignVCenter
                if align_val == "start":
                    v_align = Qt.AlignTop
                elif align_val == "center":
                    v_align = Qt.AlignVCenter
                elif align_val == "end":
                    v_align = Qt.AlignBottom
                elif align_val == "stretch":
                    v_align = Qt.AlignTop
                self._layout.setAlignment(h_align | v_align)
            elif isinstance(self._layout, QVBoxLayout):
                v_align = Qt.AlignTop
                if justify_val == "center":
                    v_align = Qt.AlignVCenter
                elif justify_val == "end":
                    v_align = Qt.AlignBottom
                h_align = Qt.AlignLeft
                if align_val == "start":
                    h_align = Qt.AlignLeft
                elif align_val == "center":
                    h_align = Qt.AlignHCenter
                elif align_val == "end":
                    h_align = Qt.AlignRight
                self._layout.setAlignment(h_align | v_align)
            # For GridLayout, basic alignment can be added if needed

    # Style Properties (responsive)
    @Property(str)
    def m(self) -> str:
        """Get current margin value."""
        return self._responsive.get("m", "")

    @m.setter
    def m(self, value: Union[str, Dict[str, str]]) -> None:
        """Set margin (e.g., 'md', {'base': 'sm', 'md': 'lg'})."""
        self._responsive.set("m", value)
        self._update_styling()

    @Property(str)
    def p(self) -> str:
        """Get current padding value."""
        return self._responsive.get("p", "")

    @p.setter
    def p(self, value: Union[str, Dict[str, str]]) -> None:
        """Set padding (e.g., 'lg', {'sm': 'md'})."""
        self._responsive.set("p", value)
        self._update_styling()

    @Property(str)
    def bg(self) -> str:
        """Get current background color key."""
        return self._responsive.get("bg", "")

    @bg.setter
    def bg(self, value: Union[str, Dict[str, str]]) -> None:
        """Set background (e.g., 'blue.500', {'dark': 'gray.900'})."""
        self._responsive.set("bg", value)
        self._update_styling()

    @Property(str)
    def c(self) -> str:
        """Get current text color key."""
        return self._responsive.get("c", "")

    @c.setter
    def c(self, value: Union[str, Dict[str, str]]) -> None:
        """Set color (e.g., 'text', {'base': 'black'})."""
        self._responsive.set("c", value)
        self._update_styling()

    @Property(str)
    def border(self) -> str:
        """Get current border style."""
        return self._responsive.get("border", "")

    @border.setter
    def border(self, value: Union[str, Dict[str, str]]) -> None:
        """Set border (e.g., '1px solid gray.300')."""
        self._responsive.set("border", value)
        self._update_styling()

    # Layout Properties
    @Property(str)
    def display(self) -> str:
        """Get current display mode."""
        return self._responsive.get("display", "block")

    @display.setter
    def display(self, value: Union[str, Dict[str, str]]) -> None:
        """Set display mode ('block', 'flex', 'grid')."""
        self._responsive.set("display", value)
        self._display = self._responsive.get("display", "block")
        self._setup_layout_mode()
        self._update_layout_styling()

    @Property(str)
    def direction(self) -> str:
        """Get current direction for flex/grid."""
        return self._responsive.get("direction", "row")

    @direction.setter
    def direction(self, value: Union[str, Dict[str, str]]) -> None:
        """Set direction ('row', 'column', etc.)."""
        self._responsive.set("direction", value)
        self._direction = self._responsive.get("direction", "row")
        if self.display == "flex":
            self._setup_layout_mode()
        self._update_layout_styling()

    # Additional Layout Properties
    @Property(str)
    def justify(self) -> str:
        """Get the current justify-content value."""
        return self._responsive.get("justify", "start")

    @justify.setter
    def justify(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the justify-content."""
        self._responsive.set("justify", value)
        self._update_layout_styling()

    @Property(str)
    def align(self) -> str:
        """Get the current align-items value."""
        return self._responsive.get("align", "stretch")

    @align.setter
    def align(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the align-items."""
        self._responsive.set("align", value)
        self._update_layout_styling()

    @Property(str)
    def gap(self) -> str:
        """Get the current gap spacing."""
        return self._responsive.get("gap", "none")

    @gap.setter
    def gap(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the gap spacing."""
        self._responsive.set("gap", value)
        self._update_layout_styling()

    @Property(bool)
    def wrap(self) -> bool:
        """Get the current wrap behavior."""
        return self._responsive.get("wrap", False)

    @wrap.setter
    def wrap(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set the wrap behavior. Note: Basic support only in Box."""
        self._responsive.set("wrap", value)
        if self.display == "flex" and value:
            print("Warning: For full wrapping support, use the Flex component.")
        self._update_layout_styling()

    # Additional Style Properties
    @Property(str)
    def size_width(self) -> str:
        """Get the current width value."""
        return self._responsive.get("width", "auto")

    @size_width.setter
    def size_width(self, value: Union[str, Dict[str, str]]) -> None:
        """Set width (supports px, %, auto, theme keys)."""
        self._responsive.set("width", value)
        self._update_size_props()

    @Property(str)
    def size_height(self) -> str:
        """Get the current height value."""
        return self._responsive.get("height", "auto")

    @size_height.setter
    def size_height(self, value: Union[str, Dict[str, str]]) -> None:
        """Set height (supports px, %, auto, theme keys)."""
        self._responsive.set("height", value)
        self._update_size_props()

    @Property(str)
    def borderRadius(self) -> str:
        """Get the current border-radius value."""
        return self._responsive.get("borderRadius", "")

    @borderRadius.setter
    def borderRadius(self, value: Union[str, Dict[str, str]]) -> None:
        """Set border-radius (e.g., "md", "8px")."""
        self._responsive.set("borderRadius", value)
        self._update_styling()

    @Property(str)
    def boxShadow(self) -> str:
        """Get the current box-shadow value."""
        return self._responsive.get("boxShadow", "")

    @boxShadow.setter
    def boxShadow(self, value: Union[str, Dict[str, str]]) -> None:
        """Set box-shadow (full CSS string)."""
        self._responsive.set("boxShadow", value)
        self._update_styling()

    # Event Handling Integration
    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events. Can be extended for click handlers.
        Emits no specific signal by default; override for custom behavior.
        """
        super().mousePressEvent(event)
        # Example: self.clicked.emit() if signal defined

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release events."""
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        """Handle resize to update responsive props and relayout."""
        super().resizeEvent(event)
        if hasattr(self, "_responsive"):
            self._responsive._invalidate_all_cache()
        self._update_styling()
        self._update_responsive_props()
        self._update_layout_styling()

    # Override add_child to respect layout mode
    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add child, respecting current layout mode."""
        super().add_child(child, **layout_props)
        if self._layout and child not in self._children:
            self._layout.addWidget(child)
        # For grid/flex advanced props, extend here (e.g., grid span)

    def center_content(self) -> None:
        """Convenience method to center content both horizontally and vertically."""
        self.justify = "center"
        self.align = "center"

    def vertical_stack(self) -> None:
        """Convenience method to set up as a vertical flex stack."""
        self.display = "flex"
        self.direction = "column"
        self.wrap = False
        self.align = "stretch"

    def horizontal_stack(self) -> None:
        """Convenience method to set up as a horizontal flex stack."""
        self.display = "flex"
        self.direction = "row"
        self.wrap = False
        self.align = "stretch"

    @classmethod
    def card(cls, **kwargs) -> "Box":
        """Class method to create a card-style Box with common defaults."""
        defaults = {
            "p": "md",
            "bg": "white",
            "c": "text",
            "border": "1px solid gray.300",
            "borderRadius": "md",
            "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.12)",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    def _get_current_breakpoint(self) -> str:
        """Helper from base, but ensure it's available."""
        # Copied from base.py for completeness
        breakpoints = {"base": 0, "sm": 576, "md": 768, "lg": 992, "xl": 1200}
        width = self.width()
        current_bp = "base"
        for bp_name, bp_width in breakpoints.items():
            if width >= bp_width:
                current_bp = bp_name
        return current_bp

    def _get_spacing_pixels(self, spacing_value: Union[str, int]) -> int:
        """Convert spacing value to pixels using theme."""
        if self._provider:
            if isinstance(spacing_value, str):
                return self._provider.get_theme_value(f"spacing.{spacing_value}", 8)
            elif isinstance(spacing_value, int):
                return spacing_value
        return 8 if isinstance(spacing_value, str) else int(spacing_value)
