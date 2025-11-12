"""
Layout Components for Polygon UI

This module provides a comprehensive layout system for Qt/PySide applications,
offering modern layout patterns similar to Mantine for web applications.
"""

# Core layout components (will be implemented in future phases)
# from .core.container import Container
# from .core.stack import Stack
# from .core.group import Group
# from .core.flex import Flex
# from .core.box import Box

# Grid system components (will be implemented in future phases)
# from .grid.grid import Grid
# from .grid.simple_grid import SimpleGrid
# from .grid.col import Col

# Utility layout components (will be implemented in future phases)
# from .utilities.center import Center
# from .utilities.aspect_ratio import AspectRatio
# from .utilities.paper import Paper
# from .utilities.divider import Divider
# from .utilities.space import Space

# Advanced layout components (will be implemented in future phases)
# from .advanced.accordion import Accordion
# from .advanced.tabs import Tabs
# from .advanced.stepper import Stepper
# from .advanced.timeline import Timeline
# from .advanced.timeline_item import TimelineItem

# For now, only import the core infrastructure
from .core import LayoutComponent, GridComponent, UtilityComponent

__all__ = [
    # Core infrastructure (available now)
    "LayoutComponent",
    "GridComponent",
    "UtilityComponent",
    # Layout components (coming soon)
    # "Container",
    # "Stack",
    # "Group",
    # "Flex",
    # "Box",
    # "Grid",
    # "SimpleGrid",
    # "Col",
    # "Center",
    # "AspectRatio",
    # "Paper",
    # "Divider",
    # "Space",
    # "Accordion",
    # "Tabs",
    # "Stepper",
    # "Timeline",
    # "TimelineItem",
]
