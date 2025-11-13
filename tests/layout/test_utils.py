"""Layout-specific test utilities for Qt/PySide components."""

import os
from pathlib import Path
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QBuffer, QByteArray
from PySide6.QtGui import QPainter, QImage


def create_test_layout(parent=None):
    """Create a test layout widget with sample children."""
    from polygon_ui.layout.core.base import LayoutComponent

    layout = LayoutComponent(parent)

    # Add sample children
    from PySide6.QtWidgets import QLabel

    for i in range(3):
        label = QLabel(f"Test Child {i}")
        layout.add_child(label)

    return layout


def capture_widget_image(widget, size=(400, 300)):
    """Capture a screenshot of the widget for visual regression testing.

    Note: Requires widget to be shown and painted.
    """
    widget.resize(*size)
    widget.show()
    QApplication.processEvents()

    # Render to image
    image = QImage(widget.size(), QImage.Format_ARGB32_Premultiplied)
    painter = QPainter(image)
    widget.render(painter)
    painter.end()

    # Save to buffer
    buffer = QBuffer()
    buffer.open(QByteArray.OWriteOnly)
    image.save(buffer, "PNG")
    buffer.close()

    return buffer.data()


def compare_images(image1_path, image2_path, tolerance=0.01):
    """Compare two images for visual regression testing.

    This is a basic implementation using pixel difference.
    For production, consider using more advanced tools like imagehash or perceptualdiff.
    """
    from PIL import Image, ImageChops

    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    diff = ImageChops.difference(img1, img2)
    bbox = diff.getbbox()

    if bbox:
        # Calculate difference percentage
        diff_pixels = sum(sum(row) for row in diff.tobytes()) / (
            diff.width * diff.height * 255 * 4
        )
        return diff_pixels < tolerance
    return True


def setup_visual_regression(test_name):
    """Setup for visual regression test: create expected image path."""
    snapshot_dir = Path("tests/snapshots")
    snapshot_dir.mkdir(exist_ok=True)
    expected_path = snapshot_dir / f"{test_name}.png"
    return str(expected_path)


# Note: PIL is not in dependencies, but can be added if needed for visual tests.
# For now, this provides the structure.
