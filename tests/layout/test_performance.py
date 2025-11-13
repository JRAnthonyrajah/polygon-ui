import pytest
import time
from pytest_benchmark import fixture
from memory_profiler import profile

from polygon_ui.layout.core.base import LayoutComponent
from polygon_ui.layout.core.responsive import ResponsiveLayout
from polygon_ui.layout.utils.qss import generate_qss_for_component
from polygon_ui.core.styles import StyleProps

# Assume Qt is available via conftest.py
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer


@pytest.fixture(scope="session")
def app():
    """Ensure QApplication is available for performance tests."""
    if QApplication.instance() is None:
        app = QApplication([])
    else:
        app = QApplication.instance()
    return app


@profile
def memory_intensive_layout_creation():
    """Function to profile memory usage for creating multiple layout components."""
    components = []
    for i in range(1000):
        component = LayoutComponent(styles=StyleProps())
        components.append(component)
    return components


class TestLayoutPerformance:
    """Performance benchmarks for layout system."""

    def test_layout_calculation_benchmark(self, benchmark):
        """Benchmark layout calculation time."""
        component = LayoutComponent()

        def calculations():
            # Simulate layout calculations
            for i in range(1000):
                component.update_geometry(100, 100, 200, 200)
                component.set_responsive_breakpoint("md")

        benchmark(calculations)

    def test_responsive_breakpoint_switching(self, benchmark):
        """Benchmark responsive breakpoint switching."""
        resp_layout = ResponsiveLayout()

        def switch_breakpoints():
            breakpoints = ["xs", "sm", "md", "lg", "xl"]
            for _ in range(500):
                for bp in breakpoints:
                    resp_layout.set_breakpoint(bp)

        benchmark(switch_breakpoints)

    def test_qss_generation_benchmark(self, benchmark):
        """Benchmark QSS generation for components."""
        component = LayoutComponent(styles=StyleProps(padding="md", margin="sm"))

        def generate_qss():
            for i in range(1000):
                qss = generate_qss_for_component(component)
                assert isinstance(qss, str)

        benchmark(generate_qss)

    def test_memory_usage_profile(self, capsys):
        """Profile memory usage for layout creation."""
        # This will output memory profile to console
        memory_intensive_layout_creation()
        captured = capsys.readouterr()
        assert "Memory usage" in captured.out  # Basic check

    def test_rendering_performance(self, benchmark, app):
        """Benchmark widget rendering time."""
        from PySide6.QtWidgets import QWidget

        def render_widgets():
            widgets = []
            for i in range(100):
                widget = QWidget()
                layout = LayoutComponent(parent=widget)
                layout.add_widget(QWidget())
                widgets.append(widget)
                # Simulate show and hide for rendering
                widget.show()
                QTimer.singleShot(0, widget.hide)

        benchmark(render_widgets)

    # Regression detection is handled by pytest-benchmark's built-in features
    # When running with --benchmark-compare=baseline, it will detect regressions
