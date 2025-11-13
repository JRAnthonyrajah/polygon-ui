import pytest
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from polygon_ui.theme import Theme, ColorScheme
from polygon_ui.styles.qss_generator import QSSGenerator
import os

# Note: For full visual regression, integrate with tools like pytest-qt and image diff (e.g., via PIL)
# Here, we test QSS output consistency and basic rendering properties as proxy for visual consistency


@pytest.fixture(scope="session")
def app():
    app = QApplication.instance() or QApplication([])
    yield app
    app.quit()


class TestThemeSwitchingVisualConsistency:
    @pytest.fixture
    def generator(self):
        return QSSGenerator()

    def test_light_theme_qss_consistency(self, generator):
        """Ensure light theme QSS is consistent across runs."""
        theme_light = Theme(color_scheme=ColorScheme.LIGHT)
        qss_light = generator.generate_theme_qss(theme_light)

        # Re-generate to check consistency
        theme_light2 = Theme(color_scheme=ColorScheme.LIGHT)
        qss_light2 = generator.generate_theme_qss(theme_light2)

        assert qss_light == qss_light2, "Light theme QSS inconsistent"

        # Check key visual elements
        assert "background-color: #f9fafb" in qss_light  # Gray 0 light
        assert "color: #111827" in qss_light  # Dark text

    def test_dark_theme_qss_consistency(self, generator):
        """Ensure dark theme QSS is consistent."""
        theme_dark = Theme(color_scheme=ColorScheme.DARK)
        qss_dark = generator.generate_theme_qss(theme_dark)

        theme_dark2 = Theme(color_scheme=ColorScheme.DARK)
        qss_dark2 = generator.generate_theme_qss(theme_dark2)

        assert qss_dark == qss_dark2, "Dark theme QSS inconsistent"

        assert "background-color: #111827" in qss_dark  # Gray 9 dark
        assert "color: #f9fafb" in qss_dark  # Light text

    def test_theme_switch_no_breakage(self, generator, app):
        """Test switching themes doesn't break component rendering."""
        # Create test widget
        test_widget = QWidget()
        test_widget.setObjectName("test-component")

        light_theme = Theme(color_scheme=ColorScheme.LIGHT)
        dark_theme = Theme(color_scheme=ColorScheme.DARK)

        # Apply light
        qss_light = generator.generate_theme_qss(light_theme)
        test_widget.setStyleSheet(qss_light)
        assert test_widget.styleSheet() == qss_light  # Applies without error

        # Switch to dark
        qss_dark = generator.generate_theme_qss(dark_theme)
        test_widget.setStyleSheet(qss_dark)
        assert test_widget.styleSheet() == qss_dark  # Switches cleanly

        # Check component-specific doesn't conflict
        comp_props = {"bg": "blue.5", "c": "white"}
        comp_qss = generator.generate_component_qss("test", comp_props, dark_theme)
        test_widget.setStyleSheet(qss_dark + "\n" + comp_qss)
        assert "background-color: #3b82f6" in test_widget.styleSheet()

    def test_primary_color_change_visual_impact(self, generator):
        """Test changing primary color updates visuals consistently."""
        theme_blue = Theme(primary_color="blue", color_scheme=ColorScheme.LIGHT)
        theme_red = Theme(primary_color="red", color_scheme=ColorScheme.LIGHT)

        qss_blue = generator.generate_theme_qss(theme_blue)
        qss_red = generator.generate_theme_qss(theme_red)

        assert "background-color: #3b82f6" in qss_blue  # Blue primary
        assert "background-color: #ef4444" in qss_red  # Red primary
        assert qss_blue != qss_red  # Visual change detected

    @pytest.mark.skipif(
        not os.getenv("GUI_TEST"), reason="Requires GUI for visual snapshot"
    )
    def test_widget_snapshot(self, generator, app):
        """Snapshot test for widget appearance (manual verification or image diff)."""
        from PySide6.QtGui import QPixmap

        theme = Theme()
        qss = generator.generate_theme_qss(theme)

        widget = QWidget()
        widget.setStyleSheet(qss)
        widget.resize(400, 300)
        widget.show()
        app.processEvents()

        # Capture pixmap (for diff tools)
        pixmap = QPixmap(widget.size())
        widget.render(pixmap)

        # Save for manual check or diff
        pixmap.save("test_snapshot_light.png", "PNG")
        assert os.path.exists("test_snapshot_light.png")


class TestContainerVisualRegression:
    """Visual regression tests for Container component."""

    @pytest.fixture
    def app(self):
        app = QApplication.instance() or QApplication([])
        yield app
        app.quit()

    @pytest.mark.skipif(
        not os.getenv("GUI_TEST"), reason="Requires GUI for visual snapshot"
    )
    def test_container_basic_snapshot(self, app):
        """Basic Container rendering snapshot."""
        from polygon_ui.layout.components.container import Container
        from polygon_ui.theme import Theme

        theme = Theme()
        container = Container(size="md", px="md", py="md", theme=theme)
        container.setObjectName("test-container")

        # Add child for visibility
        child = QWidget()
        child.setStyleSheet("background-color: red; border: 1px solid black;")
        child.setFixedSize(100, 50)
        container.layout().addWidget(child)

        container.resize(400, 300)
        container.show()
        app.processEvents()

        pixmap = QPixmap(container.size())
        container.render(pixmap)
        pixmap.save("test_container_basic.png", "PNG")
        assert os.path.exists("test_container_basic.png")

    @pytest.mark.skipif(
        not os.getenv("GUI_TEST"), reason="Requires GUI for visual snapshot"
    )
    def test_container_fluid_responsive_snapshot(self, app):
        """Fluid responsive Container snapshot."""
        from polygon_ui.layout.components.container import Container
        from polygon_ui.theme import Theme

        theme = Theme()
        container = Container(fluid=True, size="xl", px="lg", py="lg", theme=theme)
        container.setObjectName("test-fluid-container")

        # Multiple children
        for i in range(3):
            child = QWidget()
            child.setStyleSheet(f"background-color: blue; border: 1px solid black;")
            child.setFixedSize(150, 80)
            container.layout().addWidget(child)

        container.resize(600, 400)
        container.show()
        app.processEvents()

        pixmap = QPixmap(container.size())
        container.render(pixmap)
        pixmap.save("test_container_fluid_responsive.png", "PNG")
        assert os.path.exists("test_container_fluid_responsive.png")

    @pytest.mark.skipif(
        not os.getenv("GUI_TEST"), reason="Requires GUI for visual snapshot"
    )
    def test_container_dark_theme_snapshot(self, app):
        """Container in dark theme snapshot."""
        from polygon_ui.layout.components.container import Container
        from polygon_ui.theme import Theme, ColorScheme

        theme = Theme(color_scheme=ColorScheme.DARK)
        container = Container(size="sm", px="sm", py="sm", theme=theme)
        container.setObjectName("test-dark-container")

        child = QWidget()
        child.setStyleSheet("background-color: yellow; border: 1px solid white;")
        child.setFixedSize(80, 40)
        container.layout().addWidget(child)

        container.resize(300, 200)
        container.show()
        app.processEvents()

        pixmap = QPixmap(container.size())
        container.render(pixmap)
        pixmap.save("test_container_dark.png", "PNG")
        assert os.path.exists("test_container_dark.png")


# Run with: GUI_TEST=1 pytest tests/test_visual_regression.py -v
# For full regression, integrate image diff library like imagehash or loki
# Note: Snapshots saved for manual visual regression verification.
# To automate, add image comparison logic using PIL or similar.
