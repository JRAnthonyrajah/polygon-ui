import pytest
from polygon_ui.theme.colors import Colors, ColorShades
from polygon_ui.theme.theme import Theme, ColorScheme
from polygon_ui.styles.qss_generator import QSSGenerator


def test_colors_init():
    colors = Colors()
    assert len(colors.list_colors()) >= 15
    assert "blue" in colors.list_colors()
    assert "orange" in colors.list_colors()


def test_get_color():
    colors = Colors()
    assert colors.get_color("blue", 6) == "#228be6"
    with pytest.raises(ValueError):
        colors.get_color("invalid", 5)


def test_color_validation():
    colors = Colors()
    colors.validate()  # Should pass
    # Test invalid
    invalid_shades = ColorShades("test", ["#invalid"] * 9)
    with pytest.raises(ValueError):
        invalid_shades.__post_init__()


def test_theme_init_and_getters():
    theme = Theme()
    assert theme.color_scheme == ColorScheme.LIGHT
    assert theme.get_primary_color() == "#339af0"
    assert theme.get_color("gray", 5) == "#adb5bd"


def test_theme_validation():
    theme = Theme()
    theme.validate()  # Should pass
    # Invalid radius
    invalid_theme = Theme(radius={"xs": -1})
    with pytest.raises(ValueError):
        invalid_theme.validate()


def test_qss_generator_states():
    theme = Theme()
    generator = QSSGenerator()
    props = {"variant": "filled", "bg": "primary"}
    qss = generator.generate_component_qss("test-button", props, theme)
    assert ":hover" in qss  # Auto-generated
    assert ":focus" in qss


def test_theme_persistence():
    from polygon_ui.core.provider import PolygonProvider

    provider = PolygonProvider()
    provider.update_theme(primary_color="red")
    # Reload to test persistence (simulated)
    new_provider = PolygonProvider()
    assert new_provider.theme.primary_color == "red"
