"""
Tests for AspectRatio component layout behavior and responsive functionality.
"""

import pytest
from PySide6.QtWidgets import QLabel, QWidget, QPushButton
from PySide6.QtCore import QSize

from polygon_ui.layout.components.aspect_ratio import AspectRatio


class TestAspectRatioBasics:
    """Test basic AspectRatio component functionality."""

    def test_aspect_ratio_creation(self, qt_widget):
        """Test AspectRatio component can be created."""
        aspect = AspectRatio()
        assert aspect is not None
        assert aspect.ratio == "square"  # Default
        assert aspect.preserve_content
        assert aspect.overflow == "hidden"

    def test_aspect_ratio_initialization(self, qt_widget):
        """Test AspectRatio component initialization with parameters."""
        aspect = AspectRatio(
            ratio=16 / 9,
            preserve_content=False,
            overflow="visible",
            min_width=200,
            min_height=150,
        )
        assert aspect.ratio == 16 / 9
        assert not aspect.preserve_content
        assert aspect.overflow == "visible"
        assert aspect.min_width == 200
        assert aspect.min_height == 150

    def test_aspect_ratio_add_child(self, qt_widget):
        """Test adding children to AspectRatio component."""
        aspect = AspectRatio()
        child = QLabel("Test Content")

        aspect.add_child(child)
        assert child in aspect._content_container.children()
        assert child.parent() == aspect._content_container

    def test_aspect_ratio_add_multiple_children(self, qt_widget):
        """Test adding multiple children to AspectRatio component."""
        aspect = AspectRatio()
        children = [QLabel(f"Child {i}") for i in range(3)]

        for child in children:
            aspect.add_child(child)

        for child in children:
            assert child in aspect._content_container.children()

    def test_aspect_ratio_size_calculation(self, qt_widget):
        """Test aspect ratio size calculation."""
        aspect = AspectRatio(ratio=2.0)  # 2:1 ratio
        aspect.resize(400, 200)

        # Should maintain 2:1 ratio
        target_size = aspect.get_target_size(400, 200)
        assert target_size[0] / target_size[1] == 2.0


class TestAspectRatioRatios:
    """Test different aspect ratio values."""

    def test_numeric_ratio(self, qt_widget):
        """Test numeric ratio values."""
        aspect = AspectRatio(ratio=1.5)
        assert aspect.get_current_ratio() == 1.5

        aspect.ratio = 2.0
        assert aspect.get_current_ratio() == 2.0

    def test_fraction_string_ratio(self, qt_widget):
        """Test fraction string ratio values."""
        aspect = AspectRatio(ratio="16/9")
        assert abs(aspect.get_current_ratio() - (16 / 9)) < 0.001

        aspect.ratio = "4/3"
        assert abs(aspect.get_current_ratio() - (4 / 3)) < 0.001

    def test_preset_ratios(self, qt_widget):
        """Test preset ratio values."""
        # Test all preset ratios
        presets = {
            "square": 1.0,
            "widescreen": 16 / 9,
            "standard": 4 / 3,
            "portrait": 3 / 4,
            "golden": 1.618,
        }

        for preset, expected in presets.items():
            aspect = AspectRatio(ratio=preset)
            assert abs(aspect.get_current_ratio() - expected) < 0.001

    def test_invalid_ratio_fallback(self, qt_widget):
        """Test fallback to square for invalid ratios."""
        aspect = AspectRatio(ratio="invalid")
        assert aspect.get_current_ratio() == 1.0  # Falls back to square

        aspect.ratio = "0/0"  # Division by zero
        assert aspect.get_current_ratio() == 1.0  # Falls back to square

    def test_decimal_string_ratio(self, qt_widget):
        """Test decimal string ratio values."""
        aspect = AspectRatio(ratio="1.5")
        assert aspect.get_current_ratio() == 1.5

        aspect.ratio = "2.25"
        assert aspect.get_current_ratio() == 2.25


class TestAspectRatioProperties:
    """Test AspectRatio component properties."""

    def test_ratio_property(self, qt_widget):
        """Test ratio property setter and getter."""
        aspect = AspectRatio()

        # Test setting numeric value
        aspect.ratio = 2.0
        assert aspect.ratio == 2.0

        # Test setting string value
        aspect.ratio = "16/9"
        assert aspect.ratio == "16/9"

        # Test setting preset
        aspect.ratio = "widescreen"
        assert aspect.ratio == "widescreen"

    def test_preserve_content_property(self, qt_widget):
        """Test preserve_content property."""
        aspect = AspectRatio()

        # Test default
        assert aspect.preserve_content

        # Test setting to False
        aspect.preserve_content = False
        assert not aspect.preserve_content

        # Test setting to True
        aspect.preserve_content = True
        assert aspect.preserve_content

    def test_overflow_property(self, qt_widget):
        """Test overflow property."""
        aspect = AspectRatio()

        # Test default
        assert aspect.overflow == "hidden"

        # Test valid values
        for value in ["hidden", "visible", "scroll"]:
            aspect.overflow = value
            assert aspect.overflow == value

        # Test invalid value (should be ignored)
        original_value = aspect.overflow
        aspect.overflow = "invalid"
        assert aspect.overflow == original_value

    def test_min_width_property(self, qt_widget):
        """Test min_width property."""
        aspect = AspectRatio()

        # Test default
        assert aspect.min_width == 0

        # Test setting value
        aspect.min_width = 300
        assert aspect.min_width == 300

        # Test negative value (should be clamped to 0)
        aspect.min_width = -100
        assert aspect.min_width == 0

    def test_min_height_property(self, qt_widget):
        """Test min_height property."""
        aspect = AspectRatio()

        # Test default
        assert aspect.min_height == 0

        # Test setting value
        aspect.min_height = 200
        assert aspect.min_height == 200

        # Test negative value (should be clamped to 0)
        aspect.min_height = -50
        assert aspect.min_height == 0


class TestAspectRatioResponsive:
    """Test AspectRatio component responsive behavior."""

    def test_responsive_ratio(self, qt_widget):
        """Test responsive ratio property."""
        aspect = AspectRatio()

        # Set responsive ratio
        aspect.ratio = {"base": "square", "sm": "4/3", "md": "16/9", "lg": "widescreen"}

        # Verify it's stored as responsive config
        ratio_config = aspect.ratio
        assert isinstance(ratio_config, dict)
        assert ratio_config["base"] == "square"
        assert ratio_config["sm"] == "4/3"
        assert ratio_config["md"] == "16/9"
        assert ratio_config["lg"] == "widescreen"

    def test_responsive_min_width(self, qt_widget):
        """Test responsive min_width property."""
        aspect = AspectRatio()

        # Set responsive min_width
        aspect.min_width = {"base": 200, "sm": 300, "md": 400}

        # Verify it's stored as responsive config
        min_width_config = aspect.min_width
        assert isinstance(min_width_config, dict)
        assert min_width_config["base"] == 200
        assert min_width_config["sm"] == 300
        assert min_width_config["md"] == 400

    def test_responsive_min_height(self, qt_widget):
        """Test responsive min_height property."""
        aspect = AspectRatio()

        # Set responsive min_height
        aspect.min_height = {"base": 150, "sm": 200, "md": 250}

        # Verify it's stored as responsive config
        min_height_config = aspect.min_height
        assert isinstance(min_height_config, dict)
        assert min_height_config["base"] == 150
        assert min_height_config["sm"] == 200
        assert min_height_config["md"] == 250


class TestAspectRatioConvenienceMethods:
    """Test AspectRatio component convenience methods."""

    def test_set_square(self, qt_widget):
        """Test set_square convenience method."""
        aspect = AspectRatio()
        aspect.set_square()
        assert aspect.ratio == "square"

    def test_set_widescreen(self, qt_widget):
        """Test set_widescreen convenience method."""
        aspect = AspectRatio()
        aspect.set_widescreen()
        assert aspect.ratio == "widescreen"

    def test_set_standard(self, qt_widget):
        """Test set_standard convenience method."""
        aspect = AspectRatio()
        aspect.set_standard()
        assert aspect.ratio == "standard"

    def test_set_portrait(self, qt_widget):
        """Test set_portrait convenience method."""
        aspect = AspectRatio()
        aspect.set_portrait()
        assert aspect.ratio == "portrait"

    def test_set_golden(self, qt_widget):
        """Test set_golden convenience method."""
        aspect = AspectRatio()
        aspect.set_golden()
        assert aspect.ratio == "golden"

    def test_set_custom_ratio(self, qt_widget):
        """Test set_custom_ratio convenience method."""
        aspect = AspectRatio()
        aspect.set_custom_ratio(16, 9)
        assert abs(aspect.get_current_ratio() - (16 / 9)) < 0.001

        aspect.set_custom_ratio(4, 3)
        assert abs(aspect.get_current_ratio() - (4 / 3)) < 0.001

    def test_show_overflow(self, qt_widget):
        """Test show_overflow convenience method."""
        aspect = AspectRatio()
        aspect.show_overflow()
        assert aspect.overflow == "visible"

    def test_hide_overflow(self, qt_widget):
        """Test hide_overflow convenience method."""
        aspect = AspectRatio()
        aspect.overflow = "visible"
        aspect.hide_overflow()
        assert aspect.overflow == "hidden"


class TestAspectRatioBehavior:
    """Test AspectRatio component behavior in different scenarios."""

    def test_aspect_ratio_with_content(self, qt_widget):
        """Test AspectRatio component with content."""
        aspect = AspectRatio(ratio="16/9")
        content = QLabel("Test content with some length")
        aspect.add_child(content)

        # Content should be properly contained
        assert content.parent() == aspect._content_container

    def test_aspect_ratio_resize_behavior(self, qt_widget):
        """Test aspect ratio behavior on resize."""
        aspect = AspectRatio(ratio=2.0)  # 2:1 ratio

        # Resize to different sizes
        aspect.resize(400, 100)
        target_size = aspect.get_target_size(400, 100)
        assert abs(target_size[0] / target_size[1] - 2.0) < 0.001

        aspect.resize(200, 200)
        target_size = aspect.get_target_size(200, 200)
        assert abs(target_size[0] / target_size[1] - 2.0) < 0.001

    def test_aspect_ratio_minimum_sizes(self, qt_widget):
        """Test aspect ratio with minimum size constraints."""
        aspect = AspectRatio(ratio=2.0, min_width=300, min_height=100)

        # Should respect minimum sizes
        assert aspect.minimumWidth() == 300
        assert aspect.minimumHeight() == 100

    def test_aspect_ratio_overflow_handling(self, qt_widget):
        """Test aspect ratio overflow handling."""
        aspect = AspectRatio(ratio=1.0)

        # Test hidden overflow
        aspect.overflow = "hidden"
        assert aspect._content_container.clipChildren()

        # Test visible overflow
        aspect.overflow = "visible"
        assert not aspect._content_container.clipChildren()

    def test_aspect_ratio_different_content_types(self, qt_widget):
        """Test AspectRatio with various content types."""
        aspect = AspectRatio(ratio="4/3")

        # Test with different widget types
        widgets = [QLabel("Label content"), QPushButton("Button content"), QWidget()]

        for widget in widgets:
            aspect.add_child(widget)
            assert widget.parent() == aspect._content_container

    def test_aspect_ratio_size_calculation_edge_cases(self, qt_widget):
        """Test aspect ratio size calculation edge cases."""
        aspect = AspectRatio(ratio=1.0)

        # Test with zero dimensions
        target_size = aspect.get_target_size(0, 100)
        assert target_size == (0, 100)

        target_size = aspect.get_target_size(100, 0)
        assert target_size == (100, 0)

        # Test with very small dimensions
        target_size = aspect.get_target_size(1, 1)
        assert target_size == (1, 1)


class TestAspectRatioPerformance:
    """Performance tests for AspectRatio component."""

    def test_aspect_ratio_initialization_performance(self, qt_widget):
        """Test AspectRatio component initialization performance."""
        import time

        start_time = time.time()

        # Create multiple AspectRatio components
        aspects = []
        for _ in range(100):
            aspect = AspectRatio(ratio="16/9")
            aspect.add_child(QLabel("Test"))
            aspects.append(aspect)

        end_time = time.time()
        duration = end_time - start_time

        # Should be fast (less than 100ms for 100 components)
        assert duration < 0.1, f"Too slow: {duration:.3f}s"

    def test_aspect_ratio_resize_performance(self, qt_widget):
        """Test AspectRatio component resize performance."""
        import time

        aspect = AspectRatio(ratio="16/9")
        aspect.add_child(QLabel("Test content"))

        start_time = time.time()

        # Perform multiple resizes
        for _ in range(100):
            aspect.resize(800, 600)
            aspect.resize(400, 300)

        end_time = time.time()
        duration = end_time - start_time

        # Should be fast (less than 50ms for 200 resizes)
        assert duration < 0.05, f"Too slow: {duration:.3f}s"


class TestAspectRatioIntegration:
    """Integration tests with other components."""

    def test_aspect_ratio_in_layout(self, qt_widget):
        """Test AspectRatio component used within other layouts."""
        from polygon_ui.layout.components import Stack

        stack = Stack()
        aspect = AspectRatio(ratio="16/9")
        aspect.add_child(QLabel("Aspect ratio content"))

        stack.add_child(aspect)
        assert aspect.parent() == stack

    def test_aspect_ratio_with_nested_content(self, qt_widget):
        """Test AspectRatio component with nested content structures."""
        from polygon_ui.layout.components import Stack

        aspect = AspectRatio(ratio="4/3")

        # Create nested content
        inner_stack = Stack()
        inner_stack.add_child(QLabel("Nested 1"))
        inner_stack.add_child(QLabel("Nested 2"))

        aspect.add_child(inner_stack)
        assert inner_stack.parent() == aspect._content_container

    def test_aspect_ratio_responsive_breakpoints(self, qt_widget):
        """Test AspectRatio component with responsive breakpoints."""
        aspect = AspectRatio()

        # Set responsive configuration
        aspect.ratio = {"base": "square", "sm": "4/3", "md": "16/9"}
        aspect.min_width = {"base": 200, "md": 400}

        # Should store responsive configuration
        assert isinstance(aspect.ratio, dict)
        assert isinstance(aspect.min_width, dict)
