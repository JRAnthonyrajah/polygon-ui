"""
Spacing system for Polygon UI - similar to Mantine's spacing scale.
"""

from typing import Dict, Union, Optional
from dataclasses import dataclass


@dataclass
class SpacingScale:
    """Represents a spacing scale with predefined sizes."""

    xs: int = 4  # Extra small
    sm: int = 8  # Small
    md: int = 16  # Medium
    lg: int = 24  # Large
    xl: int = 32  # Extra large

    # Additional sizes for more granular control
    xxs: int = 2  # Extra extra small
    xxl: int = 48  # Extra extra large

    def get_size(self, size: Union[str, int]) -> int:
        """Get spacing size by name or return the integer value."""
        if isinstance(size, int):
            return size

        if isinstance(size, str):
            size_map = {
                "xxs": self.xxs,
                "xs": self.xs,
                "sm": self.sm,
                "md": self.md,
                "lg": self.lg,
                "xl": self.xl,
                "xxl": self.xxl,
            }
            return size_map.get(size.lower(), self.md)  # Default to md

        raise ValueError(f"Invalid spacing size type: {type(size)}")


class Spacing:
    """Spacing management system."""

    def __init__(self, custom_scale: Optional[SpacingScale] = None):
        self.scale = custom_scale or SpacingScale()

    def get_spacing(self, size: Union[str, int]) -> int:
        """Get spacing value."""
        return self.scale.get_size(size)

    def get_margin(self, size: Union[str, int]) -> str:
        """Get margin CSS value."""
        return f"{self.get_spacing(size)}px"

    def get_padding(self, size: Union[str, int]) -> str:
        """Get padding CSS value."""
        return f"{self.get_spacing(size)}px"

    def get_all_sizes(self) -> Dict[str, int]:
        """Get all available spacing sizes."""
        return {
            "xxs": self.scale.xxs,
            "xs": self.scale.xs,
            "sm": self.scale.sm,
            "md": self.scale.md,
            "lg": self.scale.lg,
            "xl": self.scale.xl,
            "xxl": self.scale.xxl,
        }

    def to_dict(self) -> Dict[str, int]:
        """Convert spacing scale to dictionary."""
        return {
            "xxs": self.scale.xxs,
            "xs": self.scale.xs,
            "sm": self.scale.sm,
            "md": self.scale.md,
            "lg": self.scale.lg,
            "xl": self.scale.xl,
            "xxl": self.scale.xxl,
        }
