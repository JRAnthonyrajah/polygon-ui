"""
Divider component for Polygon UI layout system.

A visual separation component for creating dividers between content sections.
Supports horizontal and vertical orientation, customizable size and color,
labels for text dividers, and responsive behavior.
"""

from typing import Optional, Any, Dict, Union
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Property

from ...core.provider import PolygonProvider
from ..core.base import LayoutComponent
from ..core.responsive import ResponsiveProps


class Divider(LayoutComponent):
    """
    Divider component that provides visual separation between content.

    Supports:
    - Horizontal and vertical orientation
    - Customizable size (thickness) and color
    - Label support for text dividers
    - Responsive behavior
    - Accessibility integration
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        orientation: Union[str, Dict[str, str]] = "horizontal",
        size: Union[int, str, Dict[str, Union[int, str]]] = "sm",
        color: Union[str, Dict[str, str]] = "gray.3",
        label: Union[str, Dict[str, str]] = "",
        label_position: str = "center",
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)

        # Responsive props handler
        self._responsive = ResponsiveProps(self)

        # Set initial responsive properties
        self._set_orientation(orientation)
        self._set_size(size)
        self._set_color(color)
        self._set_label(label)
        self._responsive.set("label_position", label_position)

        # Setup divider layout
        self._setup_divider_layout()

    def _setup_divider_layout(self) -> None:
        """Set up the divider layout and appearance."""
        # Main layout
        if self._get_current_orientation() == "horizontal":
            self._main_layout = QHBoxLayout(self)
        else:
            self._main_layout = QVBoxLayout(self)

        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        # Create divider line
        self._create_divider_line()

        # Apply initial properties
        self._update_divider_properties()

    def _create_divider_line(self) -> None:
        """Create the divider line widget."""
        self._line = QWidget()
        self._line.setObjectName("divider_line")

        # Add to layout
        self._main_layout.addWidget(self._line)

        # Create label if needed
        current_label = self._responsive._resolve_value(
            self._responsive.get("label", "")
        )
        if current_label:
            self._create_label()

    def _create_label(self) -> None:
        """Create the divider label."""
        self._label_widget = QLabel()
        self._label_widget.setObjectName("divider_label")
        self._label_widget.setAlignment(Qt.AlignCenter)

        # Insert label based on position
        label_position = self._responsive.get("label_position", "center")
        orientation = self._get_current_orientation()

        if orientation == "horizontal":
            if label_position == "start":
                self._main_layout.insertWidget(0, self._label_widget)
            elif label_position == "end":
                self._main_layout.addWidget(self._label_widget)
            else:  # center
                # Remove line and recreate with label in center
                self._main_layout.removeWidget(self._line)
                self._main_layout.addWidget(self._line)
                self._main_layout.insertWidget(1, self._label_widget)
        else:  # vertical
            if label_position == "start":
                self._main_layout.insertWidget(0, self._label_widget)
            elif label_position == "end":
                self._main_layout.addWidget(self._label_widget)
            else:  # center
                self._main_layout.removeWidget(self._line)
                self._main_layout.addWidget(self._line)
                self._main_layout.insertWidget(1, self._label_widget)

    def _get_current_orientation(self) -> str:
        """Get the current resolved orientation."""
        orientation = self._responsive._resolve_value(
            self._responsive.get("orientation", "horizontal")
        )
        if orientation is None:
            return "horizontal"
        return orientation.lower() if orientation else "horizontal"

    def _update_divider_properties(self) -> None:
        """Update divider properties based on responsive values."""
        size = self._responsive._resolve_value(self._responsive.get("size", "sm"))
        color = self._responsive._resolve_value(self._responsive.get("color", "gray.3"))
        label = self._responsive._resolve_value(self._responsive.get("label", ""))

        # Apply size and color
        self._apply_line_styling(size, color)

        # Update label
        self._update_label(label)

    def _update_orientation(self, new_orientation: str) -> None:
        """Update the divider orientation."""
        if new_orientation is None:
            new_orientation = "horizontal"

        # Note: For simplicity, we won't change orientation after creation
        # This would require more complex layout management
        pass

    def _apply_line_styling(self, size: Union[int, str], color: str) -> None:
        """Apply styling to the divider line."""
        # Convert size to pixels
        if size is None:
            size_pixels = 2  # Default to "sm"
        elif isinstance(size, str):
            size_map = {"xs": 1, "sm": 2, "md": 3, "lg": 4, "xl": 6}
            size_pixels = size_map.get(size.lower(), 2)
        else:
            size_pixels = int(size)

        # Resolve color
        color_map = {
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
        if color is None:
            bg_color = "#dee2e6"  # Default to gray.3
        else:
            bg_color = color_map.get(color.lower(), color)

        # Apply styling based on orientation
        orientation = self._get_current_orientation()
        if orientation == "horizontal":
            self._line.setFixedHeight(size_pixels)
            self._line.setMinimumHeight(size_pixels)
            self._line.setMaximumHeight(size_pixels)
            self._line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:  # vertical
            self._line.setFixedWidth(size_pixels)
            self._line.setMinimumWidth(size_pixels)
            self._line.setMaximumWidth(size_pixels)
            self._line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Apply background color
        if bg_color:
            self._line.setStyleSheet(
                f"#divider_line {{ background-color: {bg_color}; }}"
            )

    def _update_label(self, label_text: str) -> None:
        """Update the divider label."""
        if label_text and hasattr(self, "_label_widget"):
            self._label_widget.setText(label_text)
            self._label_widget.show()
        elif hasattr(self, "_label_widget"):
            self._label_widget.hide()

    # Private setters for responsive properties
    def _set_orientation(self, value: Union[str, Dict[str, str]]) -> None:
        """Private method to set orientation with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_orientation = {}

        if isinstance(value, str):
            full_orientation = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "horizontal"
            full_orientation["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_orientation[bp] = current
        else:
            full_orientation = {bp: "horizontal" for bp in breakpoints_order}

        self._responsive.set("orientation", full_orientation)

    def _set_size(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Private method to set size with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_size = {}

        if isinstance(value, (int, str)):
            full_size = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = "sm"
            full_size["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_size[bp] = current
        else:
            full_size = {bp: "sm" for bp in breakpoints_order}

        self._responsive.set("size", full_size)

    def _set_color(self, value: Union[str, Dict[str, str]]) -> None:
        """Private method to set color with responsive support."""
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

        self._responsive.set("color", full_color)

    def _set_label(self, value: Union[str, Dict[str, str]]) -> None:
        """Private method to set label with responsive support."""
        breakpoints_order = ["base", "sm", "md", "lg", "xl"]
        full_label = {}

        if isinstance(value, str):
            full_label = {bp: value for bp in breakpoints_order}
        elif isinstance(value, dict):
            current = ""
            full_label["base"] = value.get("base", current)
            for bp in breakpoints_order[1:]:
                current = value.get(bp, current)
                full_label[bp] = current
        else:
            full_label = {bp: "" for bp in breakpoints_order}

        self._responsive.set("label", full_label)

    def _update_responsive_props(self) -> None:
        """Update responsive properties and divider appearance."""
        super()._update_responsive_props()
        self._update_divider_properties()

    # Divider Properties (with responsive support)

    @Property(object)
    def orientation(self) -> Union[str, Dict[str, str]]:
        """Get the current orientation (responsive)."""
        return self._responsive.get("orientation", "horizontal")

    @orientation.setter
    def orientation(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the orientation (responsive)."""
        self._set_orientation(value)
        self._update_responsive_props()

    @Property(object)
    def size(self) -> Union[int, str, Dict[str, Union[int, str]]]:
        """Get the current size (thickness) (responsive)."""
        return self._responsive.get("size", "sm")

    @size.setter
    def size(self, value: Union[int, str, Dict[str, Union[int, str]]]) -> None:
        """Set the size/thickness (responsive)."""
        self._set_size(value)
        self._update_responsive_props()

    @Property(object)
    def color(self) -> Union[str, Dict[str, str]]:
        """Get the current color (responsive)."""
        return self._responsive.get("color", "gray.3")

    @color.setter
    def color(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the color (responsive)."""
        self._set_color(value)
        self._update_responsive_props()

    @Property(object)
    def label(self) -> Union[str, Dict[str, str]]:
        """Get the current label text (responsive)."""
        return self._responsive.get("label", "")

    @label.setter
    def label(self, value: Union[str, Dict[str, str]]) -> None:
        """Set the label text (responsive)."""
        self._set_label(value)
        self._update_responsive_props()

    # Convenience methods

    def set_horizontal(self) -> None:
        """Convenience method: Set horizontal orientation."""
        self.orientation = "horizontal"

    def set_vertical(self) -> None:
        """Convenience method: Set vertical orientation."""
        self.orientation = "vertical"

    def set_thin(self) -> None:
        """Convenience method: Set thin divider."""
        self.size = "xs"

    def set_thick(self) -> None:
        """Convenience method: Set thick divider."""
        self.size = "lg"

    def set_light(self) -> None:
        """Convenience method: Set light color."""
        self.color = "gray.2"

    def set_dark(self) -> None:
        """Convenience method: Set dark color."""
        self.color = "gray.6"

    def set_label_position(self, position: str) -> None:
        """Convenience method: Set label position."""
        if position in ["start", "center", "end"]:
            self._responsive.set("label_position", position)
            self._update_divider_properties()
