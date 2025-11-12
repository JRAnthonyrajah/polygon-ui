"""
Core layout components and utilities for Polygon UI.

This module provides the foundation for the layout system including
base classes and responsive design utilities.
"""

from .base import LayoutComponent, GridComponent, UtilityComponent
from .responsive import (
    Breakpoint,
    BreakpointSystem,
    ResponsiveProps,
    ResponsiveMixin,
    responsive,
    cols,
    spacing
)

__all__ = [
    # Base classes
    "LayoutComponent",
    "GridComponent",
    "UtilityComponent",
    # Responsive system
    "Breakpoint",
    "BreakpointSystem",
    "ResponsiveProps",
    "ResponsiveMixin",
    # Utilities
    "responsive",
    "cols",
    "spacing",
]