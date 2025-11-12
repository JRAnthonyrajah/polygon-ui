"""Performance monitoring for PolyBook.

Monitors component rendering, memory usage, and displays real-time metrics.
"""

import psutil
import time
from typing import Dict, Any
from PySide6.QtCore import QTimer, pyqtSignal, QObject
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .app import PolyBookApp


class PerformanceMonitor(QObject):
    """
    Real-time performance monitoring dashboard for PolyBook.
    """

    metrics_updated = pyqtSignal(dict)

    def __init__(self, parent: PolyBookApp = None):
        super().__init__(parent)
        self.app = parent
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)  # Update every second

        self.metrics: Dict[str, Any] = {
            "render_time": 0.0,
            "memory_usage": 0.0,
            "cpu_usage": 0.0,
            "fps": 0.0,
        }

    def update_metrics(self):
        """Update performance metrics."""
        # Memory and CPU
        process = psutil.Process()
        self.metrics["memory_usage"] = process.memory_info().rss / 1024 / 1024  # MB
        self.metrics["cpu_usage"] = psutil.cpu_percent()

        # Render time (measure preview updates)
        if self.app and self.app.preview_area:
            start_time = time.time()
            self.app.update_preview()  # Trigger render
            self.metrics["render_time"] = (time.time() - start_time) * 1000  # ms

        # FPS (simple estimate)
        self.metrics["fps"] = 60.0  # Placeholder; use QElapsedTimer for real FPS

        self.metrics_updated.emit(self.metrics)

    def create_dashboard(self) -> QWidget:
        """Create UI dashboard for metrics."""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        layout.setContentsMargins(8, 8, 8, 8)

        self.labels = {}
        for key in self.metrics:
            label = QLabel(f"{key.replace('_', ' ').title()}: --")
            label.setObjectName(f"perf_{key}")
            self.labels[key] = label
            layout.addWidget(label)

        self.metrics_updated.connect(self._update_labels)
        return dashboard

    def _update_labels(self, metrics: Dict[str, Any]):
        """Update label texts with new metrics."""
        for key, value in metrics.items():
            if key in self.labels:
                self.labels[key].setText(f"{key.replace('_', ' ').title()}: {value:.2f}")


# Integration in app
def add_performance_dashboard(app: PolyBookApp):
    """Add performance dashboard to app (e.g., as sidebar or overlay)."""
    monitor = PerformanceMonitor(app)
    dashboard = monitor.create_dashboard()
    # Add to app layout, e.g., app.right_panel.layout().addWidget(dashboard)
    return monitor