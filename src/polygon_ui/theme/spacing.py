"""
Spacing system for Polygon UI - similar to Mantine's spacing scale.
"""

from typing import Dict, Union, Optional
from dataclasses import dataclass


@dataclass
class SpacingScale:
    """Modern 8-point grid spacing scale for consistent layouts."""

    # 8-point grid system (multiples of 4)
    spacing_0: int = 0  # No spacing
    spacing_1: int = 4  # 0.25rem - Extra extra small
    spacing_2: int = 8  # 0.5rem - Extra small
    spacing_3: int = 12  # 0.75rem - Small
    spacing_4: int = 16  # 1rem - Medium (base)
    spacing_5: int = 20  # 1.25rem - Medium large
    spacing_6: int = 24  # 1.5rem - Large
    spacing_8: int = 32  # 2rem - Extra large
    spacing_10: int = 40  # 2.5rem - Extra extra large
    spacing_12: int = 48  # 3rem - Huge
    spacing_16: int = 64  # 4rem - Massive
    spacing_20: int = 80  # 5rem - Extra massive
    spacing_24: int = 96  # 6rem - Ultra massive

    # Legacy aliases for backward compatibility
    xxs: int = 1  # Extra extra small (4px)
    xs: int = 2  # Extra small (8px)
    sm: int = 3  # Small (12px)
    md: int = 4  # Medium (16px)
    lg: int = 6  # Large (24px)
    xl: int = 8  # Extra large (32px)
    xxl: int = 10  # Extra extra large (40px)

    def get_size(self, size: Union[str, int]) -> int:
        """Get spacing size by name or return the integer value."""
        if isinstance(size, int):
            return size

        if isinstance(size, str):
            size_map = {
                # 8-point grid system
                "0": self.spacing_0,
                "1": self.spacing_1,
                "2": self.spacing_2,
                "3": self.spacing_3,
                "4": self.spacing_4,
                "5": self.spacing_5,
                "6": self.spacing_6,
                "8": self.spacing_8,
                "10": self.spacing_10,
                "12": self.spacing_12,
                "16": self.spacing_16,
                "20": self.spacing_20,
                "24": self.spacing_24,
                # Legacy aliases
                "xxs": self.spacing_1,
                "xs": self.spacing_2,
                "sm": self.spacing_3,
                "md": self.spacing_4,
                "lg": self.spacing_6,
                "xl": self.spacing_8,
                "xxl": self.spacing_10,
            }
            return size_map.get(
                size.lower(), self.spacing_4
            )  # Default to spacing_4 (16px)

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
            # 8-point grid
            "0": self.scale.spacing_0,
            "1": self.scale.spacing_1,
            "2": self.scale.spacing_2,
            "3": self.scale.spacing_3,
            "4": self.scale.spacing_4,
            "5": self.scale.spacing_5,
            "6": self.scale.spacing_6,
            "8": self.scale.spacing_8,
            "10": self.scale.spacing_10,
            "12": self.scale.spacing_12,
            "16": self.scale.spacing_16,
            "20": self.scale.spacing_20,
            "24": self.scale.spacing_24,
            # Legacy aliases
            "xxs": self.scale.spacing_1,
            "xs": self.scale.spacing_2,
            "sm": self.scale.spacing_3,
            "md": self.scale.spacing_4,
            "lg": self.scale.spacing_6,
            "xl": self.scale.spacing_8,
            "xxl": self.scale.spacing_10,
        }

    # Utility methods for common spacing patterns
    def get_flex_gap(self, size: Union[str, int]) -> str:
        """Get flex gap value."""
        return f"{self.get_spacing(size)}px"

    def get_grid_gap(self, size: Union[str, int]) -> str:
        """Get CSS grid gap value."""
        return f"{self.get_spacing(size)}px"

    def get_component_padding(self) -> str:
        """Get standard component padding."""
        return f"{self.scale.spacing_4}px"  # 16px

    def get_section_padding(self) -> str:
        """Get section padding."""
        return f"{self.scale.spacing_8}px"  # 32px

    def get_container_padding(self) -> str:
        """Get container padding."""
        return f"{self.scale.spacing_6}px"  # 24px

    def to_dict(self) -> Dict[str, int]:
        """Convert spacing scale to dictionary."""
        return {
            # Modern 8-point grid
            "0": self.scale.spacing_0,
            "1": self.scale.spacing_1,
            "2": self.scale.spacing_2,
            "3": self.scale.spacing_3,
            "4": self.scale.spacing_4,
            "5": self.scale.spacing_5,
            "6": self.scale.spacing_6,
            "8": self.scale.spacing_8,
            "10": self.scale.spacing_10,
            "12": self.scale.spacing_12,
            "16": self.scale.spacing_16,
            "20": self.scale.spacing_20,
            "24": self.scale.spacing_24,
            # Legacy aliases
            "xxs": self.scale.spacing_1,
            "xs": self.scale.spacing_2,
            "sm": self.scale.spacing_3,
            "md": self.scale.spacing_4,
            "lg": self.scale.spacing_6,
            "xl": self.scale.spacing_8,
            "xxl": self.scale.spacing_10,
        }
