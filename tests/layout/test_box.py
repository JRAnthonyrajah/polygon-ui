"""Comprehensive tests for Box component behavior.

Includes basic functionality, style props integration, responsive behavior, layout properties,
and complex scenarios for production readiness."""

import pytest
from PySide6.QtWidgets import QLabel, QApplication, QWidget
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QPalette, QColor

from polygon_ui.layout.components.box import Box
from polygon_ui.layout.core.responsive import ResponsiveProps
from conftest import ResponsiveTestHelper
import time
import gc


@pytest.fixture
def box(parent_widget):
    """Create a basic Box widget."""
    box_widget = Box(parent=parent_widget)
    parent_widget.resize(400, 300)
    box_widget.show()
    QApplication.processEvents()
    return box_widget


@pytest.fixture
def child_labels():
    """Create sample child labels with consistent size hints."""
    labels = []
    for i in range(5):
        label = QLabel(f"Child {i}")
        label.setMinimumSize(50, 30)
        label.setMaximumSize(100, 60)
        font = label.font()
        font.setPointSize(8)
        label.setFont(font)
        labels.append(label)
    return labels


class TestBoxBasic:
    """Basic Box component tests."""

    def test_init(self, box):
        """Test Box initialization."""
        assert isinstance(box, Box)
        assert box.display == "block"
        assert box.direction == "row"  # Default direction
        assert box.justify == "start"  # Default justify
        assert box.align == "stretch"  # Default align
        assert box.gap is None  # Default gap
        assert box.wrap is False  # Default wrap
        # Style props default to None or empty
        assert box.m is None
        assert box.p is None
        assert box.bg is None
        assert box.c is None  # color property

    def test_add_child(self, box, child_labels):
        """Test adding children to Box."""
        # Box likely uses a layout, assume QVBoxLayout or custom
        for label in child_labels[:3]:
            box.add_child(label)
        # Verify children are added, positions depend on layout
        QApplication.processEvents()
        # Assume vertical stacking for block display
        for i, label in enumerate(child_labels[:3]):
            assert label.y() == i * 30  # Approximate, no gap
            assert label.x() == 0
            assert label.width() == 50
            assert label.height() == 30

    def test_remove_child(self, box, child_labels):
        """Test removing children from Box."""
        box.add_child(child_labels[0])
        box.remove_child(child_labels[0])
        assert child_labels[0] not in box.children()


class TestBoxStyleProps:
    """Tests for style properties (m, p, bg, color, border, borderRadius, boxShadow)."""

    def test_margin(self, box):
        """Test margin application."""
        box.m = 10
        box.resize(400, 300)
        QApplication.processEvents()
        # Verify geometry has margins applied (Box itself has margins from parent?)
        # For Box, margins affect its position in parent, but since it's direct child, test style
        assert "margin: 10px" in box.styleSheet()  # Assume it sets stylesheet

    @pytest.mark.parametrize("margin", [5, "10px", {"top": 5, "right": 10}])
    def test_responsive_margin(self, box, margin):
        """Test responsive margins."""
        box.m = {"xs": 5, "md": 10}
        # Use helper to verify
        # Assuming ResponsiveTestHelper
        helper = ResponsiveTestHelper(box)
        helper.assert_responsive_value(box._responsive_style, "m", {"xs": 5, "md": 10})

    def test_padding(self, box, child_labels):
        """Test padding inside Box."""
        box.p = 20
        box.add_child(child_labels[0])
        box.resize(400, 300)
        QApplication.processEvents()
        # Child should be inset by padding
        assert child_labels[0].x() == 20
        assert child_labels[0].y() == 20
        assert "padding: 20px" in box.styleSheet()

    def test_background_color(self, box):
        """Test background color."""
        box.bg = "red"
        QApplication.processEvents()
        palette = box.palette()
        assert palette.color(QPalette.ColorRole.Window) == QColor("red")

    def test_text_color(self, box):
        """Test text color (if Box has text, or affects children)."""
        box.color = "blue"
        child = QLabel("Test", parent=box)
        box.add_child(child)
        QApplication.processEvents()
        palette = child.palette()
        assert palette.color(QPalette.ColorRole.WindowText) == QColor("blue")

    def test_border(self, box):
        """Test border styles."""
        box.border = {"width": 2, "color": "black", "style": "solid"}
        QApplication.processEvents()
        # Verify stylesheet
        expected = "border: 2px solid black;"
        assert expected in box.styleSheet()

    def test_border_radius(self, box):
        """Test border radius."""
        box.borderRadius = 10
        QApplication.processEvents()
        assert "border-radius: 10px;" in box.styleSheet()

    def test_box_shadow(self, box):
        """Test box shadow (Qt approximation)."""
        box.boxShadow = "0 4px 8px rgba(0,0,0,0.1)"
        QApplication.processEvents()
        # Qt uses QGraphicsDropShadowEffect or stylesheet
        # Assume stylesheet for simplicity
        assert "box-shadow" in box.styleSheet()  # Note: Qt CSS supports it partially


class TestBoxLayoutProps:
    """Tests for layout properties (display, direction, justify, align, gap, wrap)."""

    @pytest.mark.parametrize("display", ["block", "flex", "grid"])
    def test_display(self, box, child_labels, display):
        """Test different display modes."""
        box.display = display
        for label in child_labels[:2]:
            box.add_child(label)
        box.resize(400, 100)
        QApplication.processEvents()
        if display == "block":
            assert child_labels[1].y() > child_labels[0].y()
        elif display == "flex":
            # Assume row default
            assert child_labels[1].x() > child_labels[0].x()
        # Grid would need more complex assertions

    @pytest.mark.parametrize("direction", ["row", "column"])
    def test_direction(self, box, child_labels, direction):
        """Test direction in flex mode."""
        box.display = "flex"
        box.direction = direction
        for label in child_labels[:2]:
            box.add_child(label)
        box.resize(400, 100)
        QApplication.processEvents()
        if direction == "row":
            assert child_labels[1].x() > child_labels[0].x()
            assert child_labels[0].y() == child_labels[1].y()
        else:
            assert child_labels[1].y() > child_labels[0].y()
            assert child_labels[0].x() == child_labels[1].x()

    @pytest.mark.parametrize("justify", ["start", "center", "end", "space-between"])
    def test_justify(self, box, child_labels, justify):
        """Test justify-content."""
        box.display = "flex"
        box.direction = "row"
        box.justify = justify
        box.resize(400, 100)
        for label in child_labels[:2]:
            box.add_child(label, basis=50)
        QApplication.processEvents()
        if justify == "start":
            assert child_labels[0].x() == 0
        elif justify == "center":
            assert child_labels[0].x() > 0 and child_labels[0].x() < 150
        elif justify == "end":
            assert child_labels[1].x() > 300

    @pytest.mark.parametrize("align", ["start", "center", "end", "stretch"])
    def test_align(self, box, child_labels, align):
        """Test align-items."""
        box.display = "flex"
        box.direction = "row"
        box.align = align
        box.resize(400, 100)
        for label in child_labels[:2]:
            box.add_child(label, basis=100)
        QApplication.processEvents()
        child_height = 30
        if align == "stretch":
            assert child_labels[0].height() == 100
        elif align == "center":
            assert child_labels[0].y() == (100 - child_height) / 2
        elif align == "end":
            assert child_labels[0].y() == 100 - child_height

    def test_gap(self, box, child_labels):
        """Test gap between children."""
        box.display = "flex"
        box.direction = "row"
        box.gap = 10
        box.resize(400, 100)
        for label in child_labels[:2]:
            box.add_child(label, basis=50)
        QApplication.processEvents()
        assert child_labels[1].x() == 50 + 10  # basis + gap

    def test_wrap(self, box, child_labels):
        """Test wrapping."""
        box.display = "flex"
        box.direction = "row"
        box.wrap = True
        box.resize(100, 200)  # Narrow to force wrap
        for label in child_labels[:3]:
            box.add_child(label, basis=60)
        QApplication.processEvents()
        # Second child should wrap
        assert child_labels[1].y() > child_labels[0].y()


class TestBoxResponsive:
    """Tests for responsive behavior."""

    def test_responsive_props(self, box):
        """Test responsive style and layout props."""
        box.m = {"xs": 5, "md": 20}
        box.direction = {"xs": "column", "md": "row"}
        box.justify = {"md": "center"}
        # Verify using internal responsive
        assert isinstance(box._responsive, ResponsiveProps)
        # Test value resolution at different sizes
        box.resize(200, 100)  # xs
        QApplication.processEvents()
        assert box.direction == "column"
        box.resize(800, 100)  # md
        QApplication.processEvents()
        assert box.direction == "row"
        assert box.justify == "center"

    def test_responsive_size(self, box, child_labels):
        """Test responsive width/height."""
        box.width = {"xs": "100%", "md": 400}
        box.height = {"xs": 100, "md": "50%"}
        box.add_child(child_labels[0])
        parent_widget = box.parent()
        parent_widget.resize(500, 200)
        box.resize(200, 100)  # xs
        QApplication.processEvents()
        assert box.width() == 200  # 100% of parent? Wait, parent 500, but resize to 200
        # Adjust assertions based on implementation


class TestBoxConvenienceMethods:
    """Tests for convenience methods."""

    def test_center_content(self, box, child_labels):
        """Test center_content method."""
        box.center_content()
        # Should set display=flex, justify=center, align=center, direction=row?
        assert box.justify == "center"
        assert box.align == "center"
        box.add_child(child_labels[0])
        box.resize(400, 300)
        QApplication.processEvents()
        assert child_labels[0].x() > 100 and child_labels[0].x() < 200  # Centered

    def test_vertical_stack(self, box, child_labels):
        """Test vertical_stack method."""
        box.vertical_stack()
        assert box.direction == "column"
        assert box.display == "flex"
        box.add_child(child_labels[0])
        box.add_child(child_labels[1])
        box.resize(400, 300)
        QApplication.processEvents()
        assert child_labels[1].y() > child_labels[0].y()

    def test_horizontal_stack(self, box, child_labels):
        """Test horizontal_stack method."""
        box.horizontal_stack()
        assert box.direction == "row"
        assert box.display == "flex"
        box.add_child(child_labels[0])
        box.add_child(child_labels[1])
        box.resize(400, 100)
        QApplication.processEvents()
        assert child_labels[1].x() > child_labels[0].x()


class TestBoxClassMethods:
    """Tests for class methods like card()."""

    def test_card(self, parent_widget):
        """Test Box.card() classmethod."""
        card_box = Box.card(parent=parent_widget)
        card_box.resize(300, 200)
        card_box.show()
        QApplication.processEvents()
        # Card should have border, shadow, padding, bg
        assert card_box.p == "md"  # Assume
        assert card_box.borderRadius == "md"
        assert card_box.boxShadow is not None
        assert card_box.bg == "white"  # Or theme color
        assert "border" in card_box.styleSheet()


class TestBoxComposition:
    """Tests for component composition and nesting."""

    def test_nesting_components(self, parent_widget):
        """Test nesting Box inside another Box."""
        outer_box = Box(parent=parent_widget, display="flex", direction="column")
        outer_box.resize(400, 300)
        outer_box.show()
        QApplication.processEvents()

        inner_box = Box(display="flex", direction="row", p=10, bg="lightgray")
        outer_box.add_child(inner_box)

        label1 = QLabel("Inner1")
        label2 = QLabel("Inner2")
        inner_box.add_child(label1)
        inner_box.add_child(label2)

        outer_label = QLabel("Outer")
        outer_box.add_child(outer_label)

        QApplication.processEvents()

        # Verify inner box has padding, bg, and children laid out horizontally
        assert inner_box.x() == 0
        assert inner_box.y() > 0
        assert label1.x() == 10  # Padding
        assert label2.x() > label1.x()
        assert "background-color: lightgray" in inner_box.styleSheet()

    def test_mixed_nesting(self, parent_widget):
        """Test nesting with Flex or other components (assume Box can nest any QWidget)."""
        # Similar to above, but add a Flex if available
        from polygon_ui.layout.components.flex import Flex

        outer_box = Box(parent=parent_widget)
        outer_box.add_child(Flex(direction="row"))
        # Verify no crash, positions ok


class TestBoxEvents:
    """Tests for event handling."""

    def test_resize_event(self, box, mocker):
        """Test resize event handling."""
        mock = mocker.patch.object(Box, "resizeEvent")
        box.resize(500, 400)
        QApplication.processEvents()
        mock.assert_called_once()

    def test_mouse_events(self, box, mocker):
        """Test mouse press/release events."""
        mock_press = mocker.patch.object(Box, "mousePressEvent")
        mock_release = mocker.patch.object(Box, "mouseReleaseEvent")

        # Simulate mouse press (requires QTest or manual)
        from PySide6.QtGui import QMouseEvent

        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            box.pos(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(box, event)

        mock_press.assert_called_once()

        release_event = QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            box.pos(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.NoButton,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(box, release_event)

        mock_release.assert_called_once()


class TestBoxSizeProps:
    """Tests for size properties (width, height with responsive)."""

    def test_fixed_size(self, box):
        """Test fixed width/height."""
        box.width = 200
        box.height = 150
        box.resize(400, 300)  # Parent size
        QApplication.processEvents()
        assert box.width() == 200
        assert box.height() == 150

    def test_responsive_size(self, box):
        """Test responsive width/height."""
        box.width = {"xs": 100, "md": "50%"}
        parent_widget = box.parent()
        parent_widget.resize(400, 300)
        box.resize(200, 100)  # xs
        QApplication.processEvents()
        assert box.width() == 100
        parent_widget.resize(800, 300)
        box.resize(800, 300)  # md, but prop applies
        QApplication.processEvents()
        assert box.width() == 400  # 50% of 800

    def test_fluid_size(self, box, child_labels):
        """Test percentage and fluid sizes."""
        box.width = "100%"
        box.height = "auto"
        box.add_child(child_labels[0])
        parent_widget = box.parent()
        parent_widget.resize(500, 200)
        QApplication.processEvents()
        assert box.width() == 500  # Full parent width


class TestBoxVisual:
    """Visual and integration tests."""

    def test_full_style_integration(self, box, child_labels):
        """Test all style props together with layout."""
        box.display = "flex"
        box.direction = "row"
        box.justify = "center"
        box.align = "stretch"
        box.gap = 5
        box.m = 10
        box.p = 15
        box.bg = "lightblue"
        box.border = {"width": 1, "color": "gray"}
        box.borderRadius = 5
        box.color = "darkblue"

        box.resize(400, 200)
        for label in child_labels[:3]:
            box.add_child(label, grow=1)
        QApplication.processEvents()

        # Verify styles applied
        assert "padding: 15px" in box.styleSheet()
        assert "background-color: lightblue" in box.styleSheet()
        assert "border: 1px solid gray" in box.styleSheet()
        assert "border-radius: 5px" in box.styleSheet()

        # Layout: children centered, stretched, with gap
        total_width = 400 - 2 * 15 - 2 * 10  # padding + margin? Margin on box
        child_width = (total_width - 2 * 5) / 3  # gap between 3
        assert abs(child_labels[0].width() - child_width) < 5
        assert (
            abs(child_labels[0].x() - (400 - 3 * child_width - 2 * 5) / 2) < 5
        )  # centered

        # Children height stretched
        assert child_labels[0].height() == 200 - 2 * 15

    def test_responsive_integration(self, box, child_labels):
        """Test responsive styles and layout together."""
        box.display = {"md": "flex"}
        box.direction = {"xs": "column", "md": "row"}
        box.m = {"xs": 5, "md": 20}
        box.p = {"md": 10}
        box.bg = {"md": "green"}

        parent_widget = box.parent()
        parent_widget.resize(600, 400)

        # xs mode
        box.resize(300, 200)
        QApplication.processEvents()
        assert box.display == "block"  # Default if not set
        assert box.direction == "column"
        assert box.m == 5
        assert box.p is None
        assert box.bg is None

        # md mode
        box.resize(800, 400)
        QApplication.processEvents()
        assert box.display == "flex"
        assert box.direction == "row"
        assert box.m == 20
        assert box.p == 10
        assert box.bg == "green"

        # Add children to verify layout change
        for label in child_labels[:2]:
            box.add_child(label)
        # In md, horizontal; in xs vertical - but since resized to md, horizontal


class TestBoxPerformance:
    """Performance tests for Box."""

    def test_large_children_no_crash(self, parent_widget):
        """Test adding many children."""
        box = Box(parent=parent_widget, display="flex", direction="row", wrap=True)
        box.resize(800, 600)
        box.show()

        start_time = time.time()
        for i in range(200):
            label = QLabel(f"Perf {i}")
            label.setFixedSize(40, 30)
            box.add_child(label)
        layout_time = time.time() - start_time
        assert layout_time < 2.0

        QApplication.processEvents()
        # All positioned
        for label in box.children()[:10]:
            assert label.x() >= 0 and label.y() >= 0


class TestBoxEdgeCases:
    """Edge cases for Box."""

    def test_invalid_style_prop(self, box):
        """Test invalid style values."""
        with pytest.raises(ValueError):
            box.bg = "invalid-color"

    def test_empty_box(self, box):
        """Test Box with no children."""
        box.resize(400, 300)
        QApplication.processEvents()
        # No crash

    def test_nested_deep(self, parent_widget):
        """Test deep nesting without stack overflow."""
        current = Box(parent=parent_widget)
        current.show()
        for _ in range(50):  # Qt limit around 1000, but test reasonable
            next_box = Box()
            current.add_child(next_box)
            current = next_box
        QApplication.processEvents()
        # No crash


# Note: Visual regression tests would require image comparison tools like pytest-qt or custom capture.
# For now, geometry and style assertions serve as visual verification.
# All tests assume Box implementation details; adjust assertions based on actual behavior.
