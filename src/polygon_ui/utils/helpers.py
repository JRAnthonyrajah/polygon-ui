"""
Helper utilities for Polygon UI.
"""

from typing import Union


def css_var_to_qss(css_variable: str) -> str:
    """
    Convert CSS variable format to QSS format.

    Args:
        css_variable: CSS variable (e.g., '--mantine-color-blue-6')

    Returns:
        QSS property name (e.g., 'polygon-color-blue-6')
    """
    return css_variable.replace("--", "").replace("_", "-")


def generate_color_shades(base_color: str, count: int = 10) -> list[str]:
    """
    Generate color shades from a base color.
    This is a simplified implementation.

    Args:
        base_color: Base hex color
        count: Number of shades to generate

    Returns:
        List of color shades
    """
    # For now, return a simple variation
    # In a real implementation, you'd use proper color space manipulation
    return [base_color] * count
