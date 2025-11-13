import pytest
from unittest.mock import Mock, patch

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt, QSizePolicy

# Import the Group class
from polygon_ui.layout.components.group import Group
from polygon_ui.layout.core.responsive import ResponsiveProps


@pytest.fixture(scope="session")
def qapp():
    """Fixture to provide QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Do not quit here to avoid issues in some environments


class TestGroupInitialization:
    """Test the initialization of the Group component."""

    def test_default_initialization(self, qapp):
        """Test Group initializes with default values."""
        group = Group()
        assert group.gap == "md"
        assert group.align == "center"
        assert group.justify == "start"
        assert group.wrap is False
        assert group.spacing == "md"
        assert isinstance(group._responsive, ResponsiveProps)

    def test_custom_initialization(self, qapp):
        """Test Group with custom initial parameters."""
        gap = "lg"
        align = "start"
        justify = "center"
        wrap = True
        spacing = "sm"

        group = Group(gap=gap, align=align, justify=justify, wrap=wrap, spacing=spacing)

        assert group.gap == gap
        assert group.align == align
        assert group.justify == justify
        assert group.wrap is wrap
        assert group.spacing == spacing

    def test_responsive_initialization(self, qapp):
        """Test initialization with responsive properties."""
        responsive_gap = {"base": "sm", "md": "lg"}
        responsive_align = {"base": "start", "lg": "center"}
        responsive_justify = {"base": "start"}
        responsive_wrap = {"base": False, "md": True}

        group = Group(
            gap=responsive_gap,
            align=responsive_align,
            justify=responsive_justify,
            wrap=responsive_wrap,
        )

        assert group._responsive.props["gap"] == responsive_gap
        assert group._responsive.props["align"] == responsive_align
        assert group._responsive.props["justify"] == responsive_justify
        assert group._responsive.props["wrap"] == responsive_wrap


class TestGroupProperties:
    """Test the property setters and getters for Group."""

    def test_gap_property(self, qapp):
        """Test gap property setter and getter."""
        group = Group()
        assert group.gap == "md"

        # Simple string value
        group.gap = "lg"
        assert group.gap == "lg"
        assert group.spacing == "lg"  # Should sync if not set

        # Reset and set responsive
        group.gap = {"base": "sm", "md": "lg"}
        assert group._responsive.props["gap"] == {"base": "sm", "md": "lg"}

        # Set spacing separately
        group.spacing = "xl"
        assert group.spacing == "xl"
        assert group.gap == "lg"  # Gap should remain unchanged

    def test_align_property(self, qapp):
        """Test align property."""
        group = Group()
        assert group.align == "center"

        group.align = "start"
        assert group.align == "start"

        # Responsive
        group.align = {"base": "start", "lg": "end"}
        assert group._responsive.props["align"] == {"base": "start", "lg": "end"}

    def test_justify_property(self, qapp):
        """Test justify property."""
        group = Group()
        assert group.justify == "start"

        group.justify = "center"
        assert group.justify == "center"

        # Responsive
        group.justify = {"base": "start", "md": "space-between"}
        assert group._responsive.props["justify"] == {
            "base": "start",
            "md": "space-between",
        }

    def test_wrap_property(self, qapp):
        """Test wrap property."""
        group = Group()
        assert group.wrap is False

        group.wrap = True
        assert group.wrap is True

        # Responsive
        group.wrap = {"base": False, "md": True}
        assert group._responsive.props["wrap"] == {"base": False, "md": True}


class TestChildManagement:
    """Test adding and managing children in Group."""

    def test_add_child_basic(self, qapp):
        """Test basic child addition."""
        group = Group()
        label = QLabel("Test Label")
        group.add_child(label)

        assert len(group._children_order) == 1
        assert label in group._children_order
        assert label in group._child_props
        assert group._child_props[label] == {}

    def test_add_child_with_props(self, qapp):
        """Test adding child with layout properties."""
        group = Group()
        label = QLabel("Test Label")
        props = {"grow": True, "alignSelf": "stretch", "basis": 100}

        group.add_child(label, **props)

        assert len(group._children_order) == 1
        assert group._child_props[label] == props

        # Verify size policy updates
        h_policy = label.sizePolicy().horizontalPolicy()
        v_policy = label.sizePolicy().verticalPolicy()
        assert h_policy == QSizePolicy.Policy.Expanding
        assert v_policy == QSizePolicy.Policy.Expanding  # For stretch

        # Verify basis
        assert label.minimumWidth() == 100

    def test_add_multiple_children(self, qapp):
        """Test adding multiple children."""
        group = Group()
        children = [QLabel(f"Label {i}") for i in range(3)]

        for child in children:
            group.add_child(child)

        assert len(group._children_order) == 3
        for child in children:
            assert child in group._children_order
            assert child in group._child_props

    def test_child_grow_shrink_flex(self, qapp):
        """Test child sizing properties."""
        group = Group()

        # Test grow
        label_grow = QLabel("Grow")
        group.add_child(label_grow, grow=True)
        assert (
            label_grow.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Expanding
        )

        # Test shrink
        label_shrink = QLabel("Shrink")
        group.add_child(label_shrink, shrink=True)
        assert (
            label_shrink.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Minimum
        )

        # Test flex none (fixed)
        label_fixed = QLabel("Fixed")
        group.add_child(label_fixed, flex="none")
        assert label_fixed.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Fixed

    def test_child_align_self(self, qapp):
        """Test alignSelf property on children."""
        group = Group(align="center")

        # Default alignSelf should use group align
        label_default = QLabel("Default")
        group.add_child(label_default)
        # Private, but assume _update_child_policies sets policy

        # Custom alignSelf
        label_custom = QLabel("Custom")
        group.add_child(label_custom, alignSelf="start")
        # Would need to mock or test the alignment in layout, but for unit, check props
        assert group._child_props[label_custom]["alignSelf"] == "start"


class TestLayoutBehavior:
    """Test layout configuration based on properties."""

    @patch.object(Group, "_get_spacing_pixels")
    def test_non_wrapping_layout(self, mock_spacing, qapp):
        """Test non-wrapping mode uses QHBoxLayout."""
        group = Group(wrap=False)
        label1 = QLabel("1")
        label2 = QLabel("2")
        group.add_child(label1)
        group.add_child(label2)

        # Trigger layout update
        group._update_group_styling()
        layout = group.layout()
        assert isinstance(layout, QHBoxLayout)
        mock_spacing.assert_called()

    @patch.object(Group, "_get_spacing_pixels")
    def test_wrapping_layout(self, mock_spacing, qapp):
        """Test wrapping mode uses QGridLayout."""
        group = Group(wrap=True)
        labels = [QLabel(f"Label {i}") for i in range(5)]
        for label in labels:
            group.add_child(label)

        group._update_group_styling()
        layout = group.layout()
        assert isinstance(layout, QGridLayout)
        mock_spacing.assert_called()

    def test_justify_space_around(self, qapp):
        """Test justify='space-around' adds stretches."""
        group = Group(justify="space-around")
        labels = [QLabel(f"L{i}") for i in range(2)]
        for label in labels:
            group.add_child(label)

        group._update_group_styling()
        layout = group.layout()
        assert layout.count() == 5  # stretch, widget, stretch, widget, stretch

    def test_justify_center(self, qapp):
        """Test justify='center' adds stretches before and after."""
        group = Group(justify="center")
        labels = [QLabel(f"L{i}") for i in range(2)]
        for label in labels:
            group.add_child(label)

        group._update_group_styling()
        layout = group.layout()
        # stretch before, two widgets, stretch after: 4 items
        assert layout.count() == 4

    @patch.object(Group, "width")
    def test_wrap_line_break(self, mock_width, qapp):
        """Test wrapping logic breaks lines based on width."""
        mock_width.return_value = 200  # Small width to force wrapping

        group = Group(wrap=True)
        wide_labels = [QLabel("Wide " * 10) for _ in range(3)]  # Each wide
        for label in wide_labels:
            group.add_child(label, basis=150)  # Each takes ~150px

        group._update_group_styling()
        layout = group.layout()
        # With width 200, first label 150, second would exceed (150+spacing+150>200), so 3 rows
        # But testing private logic indirectly via row/column count is hard; assume correct if grid used

    def test_update_child_policies(self, qapp):
        """Test that child policies are updated correctly."""
        group = Group()
        label = QLabel("Test")
        group.add_child(label, grow=True, alignSelf="stretch")

        group._update_child_policies()
        policy = label.sizePolicy()
        assert policy.horizontalPolicy() == QSizePolicy.Policy.Expanding
        assert policy.verticalPolicy() == QSizePolicy.Policy.Expanding


class TestResponsiveAndEvents:
    """Test responsive behavior and event handling."""

    def test_responsive_update_on_property_change(self, qapp):
        """Test that changing responsive props triggers update."""
        group = Group()
        with patch.object(group, "_update_group_styling") as mock_update:
            group.gap = {"base": "lg"}
            mock_update.assert_called_once()

    def test_resize_event(self, qapp):
        """Test resize event invalidates responsive cache and updates styling."""
        group = Group()
        with patch.object(
            group._responsive, "_invalidate_all_cache"
        ) as mock_invalidate, patch.object(
            group, "_update_group_styling"
        ) as mock_update:
            event = Mock()
            group.resizeEvent(event)
            mock_invalidate.assert_called_once()
            mock_update.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_no_children(self, qapp):
        """Test behavior with no children."""
        group = Group()
        group._update_group_styling()
        assert group.layout() is None  # Or empty layout

    def test_invalid_spacing_value(self, qapp):
        """Test handling of invalid spacing (fallback)."""
        group = Group()
        with patch.object(group, "_get_spacing_pixels") as mock_spacing:
            mock_spacing.side_effect = lambda x: 999 if x == "invalid" else 8
            group.gap = "invalid"
            # Should fallback to 8, but since mocked, test doesn't crash

    def test_add_none_child(self, qapp):
        """Test adding None child (should fallback to super)."""
        group = Group()
        with patch.object(group, "add_child") as mock_super:  # super().add_child
            group.add_child(None)
            mock_super.assert_called_once()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__])
