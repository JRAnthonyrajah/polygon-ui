"""
Paper component for Polygon UI layout system.

A utility component that provides visual grouping with shadows and borders.
Supports theme-aware elevation, border radius, color scheme integration,
and responsive visual behavior. Perfect for cards, modals, and content containers.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Property, QMargins

from ...core.provider import PolygonProvider
from ...styles.style_props import StyleProps
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Paper(LayoutComponent):
    """
    Paper component that provides visual grouping with shadows and borders.

    Supports:
    - Shadow elevation with theme integration
    - Border support with radius and color
    - Responsive shadow behavior
    - Theme-aware color scheme integration
    - Style props integration
    """

    # Shadow elevation levels (inspired by Material Design)
    SHADOW_LEVELS = {
        "none": 0,
        "xs": 1,
        "sm": 2,
        "md": 4,
        "lg": 8,
        "xl": 12,
        "2xl": 16,
        "3xl": 24,
    }

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        shadow: Union[str, int, Dict[str, Union[str, int]]] = "sm",
        with_border: Union[bool, Dict[str, bool]] = True,
        border_radius: Union[int, str, Dict[str, Union[int, str]]] = "md",
        border_color: Union[str, Dict[str, str]] = "gray.3",
        background: Union[str, Dict[str, str]] = "white",
        padding: Union[str, int, Dict[str, Union[str, int]]] = "md",
        margin: Union[str, int, Dict[str, Union[str, int]]] = 0,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_shadow(shadow)
        self._set_with_border(with_border)
        self._set_border_radius(border_radius)
        self._set_border_color(border_color)
        self._set_background(background)
        self._set_padding(padding)
        self._set_margin(margin)

        # Setup paper layout and styling
        self._setup_paper_layout()

    def _setup_paper_layout(self) -> None:
        """Set up the paper layout and styling."""
        # Main container
        self._main_container = QWidget(self)
        self._main_container.setObjectName("paper_main")

        # Layout for main container
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        self._main_layout.addWidget(self._main_container)

        # Content layout
        self._content_layout = QVBoxLayout(self._main_container)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)

        # Apply initial responsive properties
        self._update_paper_properties()

    def _update_paper_properties(self) -> None:
        """Update paper properties based on responsive values."""
        shadow = self._responsive._resolve_value(self._responsive.get("shadow", "sm"))
        with_border = self._responsive._resolve_value(
            self._responsive.get("with_border", True)
        )
        border_radius = self._responsive._resolve_value(
            self._responsive.get("border_radius", "md")
        )
        border_color = self._responsive._resolve_value(
            self._responsive.get("border_color", "gray.3")
        )
        background = self._responsive._resolve_value(
            self._responsive.get("background", "white")
        )
        padding = self._responsive._resolve_value(self._responsive.get("padding", "md"))
        margin = self._responsive._resolve_value(self._responsive.get("margin", 0))

        # Apply shadow
        self._apply_shadow(shadow)

        # Apply border
        self._apply_border(with_border, border_radius, border_color)

        # Apply background
        self._apply_background(background)

        # Apply padding and margin
        self._apply_spacing(padding, margin)

    def _apply_shadow(self, shadow_level: Union[str, int]) -> None:
        """Apply shadow elevation to the paper component."""
        # Convert shadow level to elevation value
        if shadow_level is None:
            elevation = 2  # Default to "sm"
        elif isinstance(shadow_level, str):
            elevation = self.SHADOW_LEVELS.get(shadow_level.lower(), 2)
        else:
            elevation = int(shadow_level)

        # Generate shadow CSS based on elevation
        shadow_css = self._generate_shadow_css(elevation)

        # Apply to main container
        if shadow_css:
            self._main_container.setStyleSheet(f"#paper_main {{ {shadow_css} }}")

    def _generate_shadow_css(self, elevation: int) -> str:
        """Generate CSS shadow string based on elevation."""
        if elevation <= 0:
            return ""

        # Simplified shadow generation (in real implementation, would use theme colors)
        shadow_configs = {
            1: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            2: "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
            4: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            8: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            12: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            16: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            24: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        }

        # Find closest shadow config
        shadow_values = sorted(shadow_configs.keys())
        closest_elevation = min(shadow_values, key=lambda x: abs(x - elevation))
        shadow_css = shadow_configs.get(closest_elevation, "")

        return f"box-shadow: {shadow_css};" if shadow_css else ""

    def _apply_border(
        self, with_border: bool, border_radius: Union[int, str], border_color: str
    ) -> None:
        """Apply border styling to the paper component."""
        border_style = []

        if with_border:
            border_style.append("border: 1px solid;")
            # Set border color (simplified - would use theme color resolution)
            if border_color:
                border_style.append(
                    f"border-color: {self._resolve_color(border_color)};"
                )

        # Set border radius
        radius_value = self._resolve_size(border_radius, 8)  # Default to 8px for "md"
        border_style.append(f"border-radius: {radius_value}px;")

        # Apply styles
        if border_style:
            border_css = " ".join(border_style)
            current_style = self._main_container.styleSheet() or ""
            # Remove existing border-radius if present, then add new one
            import re

            current_style = re.sub(r"border-radius:\s*[^;]+;", "", current_style)
            current_style = re.sub(r"border:\s*[^;]+;", "", current_style)
            current_style = re.sub(r"border-color:\s*[^;]+;", "", current_style)

            new_style = current_style + f" #paper_main {{ {border_css} }}"
            self._main_container.setStyleSheet(new_style)

    def _apply_background(self, background: str) -> None:
        """Apply background color to the paper component."""
        if background:
            bg_color = self._resolve_color(background)
            if bg_color:
                current_style = self._main_container.styleSheet() or ""
                import re

                current_style = re.sub(
                    r"background(-color)?:\s*[^;]+;", "", current_style
                )

                new_style = (
                    current_style + f" #paper_main {{ background-color: {bg_color}; }}"
                )
                self._main_container.setStyleSheet(new_style)

    def _apply_spacing(self, padding: Union[str, int], margin: Union[str, int]) -> None:
        """Apply padding and margin to the paper component."""
        # Convert padding to pixels
        padding_value = self._resolve_size(padding, 16)  # Default to 16px for "md"
        margin_value = self._resolve_size(margin, 0)

        # Apply padding to content layout
        self._content_layout.setContentsMargins(
            padding_value, padding_value, padding_value, padding_value
        )

        # Apply margin to main layout
        self._main_layout.setContentsMargins(
            margin_value, margin_value, margin_value, margin_value
        )

    def _resolve_color(self, color_value: str) -> str:
        """Resolve color value to actual color string."""
        # Simplified color resolution (in real implementation, would use theme system)
        color_map = {
            "white": "#ffffff",
            "black": "#000000",
            "gray.0": "#f8f9fa",
            "gray.1": "#f1f3f5",
            "gray.2": "#e9ecef",
            "gray.3": "#dee2e6",
            "gray.4": "#ced4da",
            "gray.5": "#adb5bd",
            "gray.6": "#868e96",
            "gray.7": "#495057",
            "gray.8": "#343a40",
            "gray.9": "#212529",
        }
        return color_map.get(color_value.lower(), color_value)

    def _resolve_size(self, size_value: Union[str, int], default: int) -> int:
        """Resolve size value to pixels."""
        if isinstance(size_value, int):
            return size_value
        elif isinstance(size_value, str):
            # Theme spacing values (simplified)
            spacing_map = {
                "xs": 4,
                "sm": 8,
                "md": 16,
                "lg": 24,
                "xl": 32,
                "2xl": 48,
                "3xl": 64,
            }
            return spacing_map.get(size_value.lower(), default)
        return default

    # Private setters for responsive properties
    def _set_shadow(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Private method to set shadow with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_shadow = {}

        if isinstance(value, (str, int)):
            full_shadow = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "sm"
            full_shadow["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_shadow[bp] = current
        else:
            full_shadow = {bp: "sm" for bp in breakpoints_order}

        self._responsive.set("shadow", full_shadow)

    def _set_with_border(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Private method to set with_border with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_border = {}

        if isinstance(value, bool):
            full_border = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = True
            full_border["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_border[bp] = current
        else:
            full_border = {bp: True for bp in breakpoints_order}

        self._responsive.set("with_border", full_border)

    def _set_border_radius(
        self, value: Union[int, str, Dict[str, Union[int, str]]]
    ) -> None:
        """Private method to set border_radius with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_radius = {}

        if isinstance(value, (int, str)):
            full_radius = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "md"
            full_radius["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_radius[bp] = current
        else:
            full_radius = {bp: "md" for bp in breakpoints_order}

        self._responsive.set("border_radius", full_radius)

    def _set_border_color(self, value: Union[str, Dict[str, str]]) -> None:
        """Private method to set border_color with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_color = {}

        if isinstance(value, str):
            full_color = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "gray.3"
            full_color["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_color[bp] = current
        else:
            full_color = {bp: "gray.3" for bp in breakpoints_order}

        self._responsive.set("border_color", full_color)

    def _set_background(self, value: Union[str, Dict[str, str]]) -> None:
        """Private method to set background with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_background = {}

        if isinstance(value, str):
            full_background = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "white"
            full_background["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_background[bp] = current
        else:
            full_background = {bp: "white" for bp in breakpoints_order}

        self._responsive.set("background", full_background)

    def _set_padding(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Private method to set padding with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_padding = {}

        if isinstance(value, (str, int)):
            full_padding = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "md"
            full_padding["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_padding[bp] = current
        else:
            full_padding = {bp: "md" for bp in breakpoints_order}

        self._responsive.set("padding", full_padding)

    def _set_margin(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Private method to set margin with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_margin = {}

        if isinstance(value, (str, int)):
            full_margin = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = 0
            full_margin["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_margin[bp] = current
        else:
            full_margin = {bp: 0 for bp in breakpoints_order}

        self._responsive.set("margin", full_margin)

    def _update_responsive_props(self) -> None:
        """Update responsive properties and paper appearance."""
        super()._update_responsive_props()
        self._update_paper_properties()

    # Paper Properties (with responsive support)

    @Property(object)
    def shadow(self) -> Union[str, int, Dict[str, Union[str, int]]]:
        """Get the current shadow level (responsive)."""
        return self._responsive.get("shadow", "sm")

    @shadow.setter
    def shadow(self, value: Union[str, int, Dict[str, Union[str, int]]]) -> None:
        """Set the shadow level (responsive)."""
        self._set_shadow(value)
        self._update_responsive_props()

    @Property(object)
    def with_border(self) -> Union[bool, Dict[str, bool]]:
        """Get the current border setting (responsive)."""
        return self._responsive.get("with_border", True)

    @with_border.setter
    def with_border(self, value: Union[bool, Dict[str, bool]]) -> None:
        """Set whether to show border (responsive)."""
        self._set_with_border(value)
        self._update_responsive_props()

    @Property(object)
    def border_radius(self) -> Union[int, str, Dict[str, Union[int, str]]]:
        """Get the current border radius (responsive)."""
        return self._responsive.get("border_radius", "md")

    @border_radius.setter
    def border_radius(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Set the border radius (responsive)."""
        self._set_border_radius(value)
        self._update_responsive_props()

    @Property(object)
    def border_color(self) -> Union[str, Dict[str, str]]:
        """Get the current border color (responsive)."""
        return self._responsive.get("border_color", "gray.3")

    @border_color.setter
    def border_color(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the border color (responsive)."""
        self._set_border_color(value)
        self._update_responsive_props()

    @Property(object)
    def background(self) -> Union[str, Dict[str, str]]:
        """Get the current background color (responsive)."""
        return self._responsive.get("background", "white")

    @background.setter
    def background(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the background color (responsive)."""
        self._set_background(value)
        self._update_responsive_props()

    def add_child(self, child: QWidget, **layout_props: Any) -> None:
        """Add a child widget to the paper container."""
        super().add_child(child, **layout_props)
        # Add to content layout
        if self._content_layout:
            self._content_layout.addWidget(child)

    # Convenience methods

    def set_shadow_none(self) -> None:
        """Convenience method: Remove shadow."""
        self.shadow = "none"

    def set_shadow_light(self) -> None:
        """Convenience method: Set light shadow."""
        self.shadow = "xs"

    def set_shadow_medium(self) -> None:
        """Convenience method: Set medium shadow."""
        self.shadow = "md"

    def set_shadow_heavy(self) -> None:
        """Convenience method: Set heavy shadow."""
        self.shadow = "xl"

    def enable_border(self) -> None:
        """Convenience method: Enable border."""
        self.with_border = True

    def disable_border(self) -> None:
        """Convenience method: Disable border."""
        self.with_border = False

    def set_radius_none(self) -> None:
        """Convenience method: Remove border radius."""
        self.border_radius = 0

    def set_radius_small(self) -> None:
        """Convenience method: Set small border radius."""
        self.border_radius = "sm"

    def set_radius_large(self) -> None:
        """Convenience method: Set large border radius."""
        self.border_radius = "lg"

    def set_radius_round(self) -> None:
        """Convenience method: Set fully rounded (circle)."""
        self.border_radius = 9999  # Large value for circular effect
