"""Performance benchmarks for the Container component."""
import pytest
import time
import pytest
from memory_profiler import profile

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, Qt

from polygon_ui.layout.components.container import Container
from polygon_ui.layout.core.responsive import ResponsiveProps


@pytest.fixture(scope="session")
def app():
    """Ensure QApplication is available for performance tests."""
    if QApplication.instance() is None:
        app = QApplication([])
    else:
        app = QApplication.instance()
    yield app


class TestContainerPerformance:
    """Performance benchmarks for Container component."""

    def test_container_creation_benchmark(self, benchmark, app):
        """Benchmark Container instantiation time (1000x)."""

        def create_containers():
            containers = []
            for _ in range(1000):
                container = Container()
                containers.append(container)
                # Basic setup to simulate real use
                container.size = "md"
            return containers

        result = benchmark(create_containers)
        # Assert creation succeeded
        assert len(result) == 1000
        # Timing should be <100ms total for perf target

    def test_responsive_size_switching_benchmark(self, benchmark):
        """Benchmark responsive size property switching (500x cycles)."""

        container = Container()
        sizes = ["xs", "sm", "md", "lg", "xl"]

        def switch_sizes():
            for _ in range(500):
                for size in sizes:
                    container.size = size
                    # Trigger update
                    container._update_container_styling()

        benchmark(switch_sizes)
        # Timing should be <16ms per cycle avg

    def test_responsive_padding_update_benchmark(self, benchmark):
        """Benchmark responsive padding updates (px/py, 500x)."""

        container = Container()
        paddings = [{"base": 8, "md": 32}, {"base": 16, "lg": 48}]

        def update_paddings():
            for _ in range(500):
                for pad_config in paddings:
                    container.px = pad_config
                    container.py = pad_config
                    container._update_container_styling()

        benchmark(update_paddings)

    def test_fluid_and_center_toggle_benchmark(self, benchmark):
        """Benchmark fluid and center property toggles (1000x)."""

        container = Container()

        def toggle_properties():
            for _ in range(1000):
                container.fluid = not container.fluid
                container.center = not container.center
                container._update_container_styling()

        benchmark(toggle_properties)

    def test_add_child_performance_benchmark(self, benchmark):
        """Benchmark adding children to Container (200 children x 50 runs)."""

        def add_children_batch():
            container = Container()
            child_widgets = []
            for _ in range(200):
                child = QWidget()
                container.add_child(child)
                child_widgets.append(child)
            return len(container.children())  # Via base class if exposed

        # Run 50 batches
        def full_benchmark():
            results = []
            for _ in range(50):
                result = add_children_batch()
                results.append(result)
            return results

        result = benchmark(full_benchmark)
        assert all(r == 200 for r in result)

    def test_resize_event_benchmark(self, benchmark, app):
        """Benchmark resize event handling with responsive updates (500x)."""

        container = Container()
        container.show()  # Needed for events
        app.processEvents()

        sizes = [(500, 300), (800, 500), (1200, 600), (1600, 800)]
        container.size = {"base": "xs", "sm": "sm", "md": "lg", "xl": "xl"}

        def trigger_resizes():
            for _ in range(500 // len(sizes)):
                for width, height in sizes:
                    container.resize(width, height)
                    app.processEvents()
                    # Responsive should update
                    container._responsive._invalidate_all_cache()

        benchmark(trigger_resizes)


@profile
def memory_profile_container_creation():
    """Profile memory usage for batch Container creation (1000x)."""
    components = []
    for i in range(1000):
        component = Container(size="md", fluid=False, px=16, py=16)
        # Add a child to simulate real use
        child = QWidget()
        component.add_child(child)
        components.append(component)
    return components


def test_memory_usage_profile(self, capsys):
    """Profile and capture memory usage for Container creation."""
    memory_profile_container_creation()
    captured = capsys.readouterr()
    # Basic check for memory output
    assert "Memory usage" in captured.out
    # In CI, parse for delta <10MB
