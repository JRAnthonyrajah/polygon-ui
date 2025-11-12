"""
Typography system for Polygon UI - similar to Mantine's typography scale.
"""

from typing import Dict, Union, Optional
from dataclasses import dataclass


@dataclass
class FontSizes:
    """Font size scale."""

    xs: int = 12  # Extra small
    sm: int = 14  # Small
    md: int = 16  # Medium (base)
    lg: int = 18  # Large
    xl: int = 20  # Extra large

    # Additional sizes
    xxl: int = 24  # Extra extra large
    xxxl: int = 32  # Triple extra large

    def get_size(self, size: Union[str, int]) -> int:
        """Get font size by name or return the integer value."""
        if isinstance(size, int):
            return size

        if isinstance(size, str):
            size_map = {
                "xs": self.xs,
                "sm": self.sm,
                "md": self.md,
                "lg": self.lg,
                "xl": self.xl,
                "xxl": self.xxl,
                "xxxl": self.xxxl,
            }
            return size_map.get(size.lower(), self.md)  # Default to md

        raise ValueError(f"Invalid font size type: {type(size)}")


@dataclass
class LineHeights:
    """Line height scale."""

    xs: float = 1.0  # Extra small
    sm: float = 1.25  # Small
    md: float = 1.5  # Medium (base)
    lg: float = 1.75  # Large
    xl: float = 2.0  # Extra large

    def get_height(self, height: Union[str, float]) -> float:
        """Get line height by name or return the float value."""
        if isinstance(height, (int, float)):
            return float(height)

        if isinstance(height, str):
            height_map = {
                "xs": self.xs,
                "sm": self.sm,
                "md": self.md,
                "lg": self.lg,
                "xl": self.xl,
            }
            return height_map.get(height.lower(), self.md)  # Default to md

        raise ValueError(f"Invalid line height type: {type(height)}")


@dataclass
class FontWeights:
    """Font weight scale."""

    light: int = 300
    normal: int = 400
    medium: int = 500
    semibold: int = 600
    bold: int = 700
    extrabold: int = 800

    def get_weight(self, weight: Union[str, int]) -> int:
        """Get font weight by name or return the integer value."""
        if isinstance(weight, int):
            return weight

        if isinstance(weight, str):
            weight_map = {
                "light": self.light,
                "normal": self.normal,
                "medium": self.medium,
                "semibold": self.semibold,
                "bold": self.bold,
                "extrabold": self.extrabold,
            }
            return weight_map.get(weight.lower(), self.normal)  # Default to normal

        raise ValueError(f"Invalid font weight type: {type(weight)}")


@dataclass
class FontFamilies:
    """Font family definitions."""

    sans: str = "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    mono: str = "SFMono-Regular, Consolas, Liberation Mono, Menlo, Courier, monospace"

    def get_family(self, family: Union[str, None]) -> str:
        """Get font family by name."""
        if family is None:
            return self.sans

        if isinstance(family, str):
            family_map = {"sans": self.sans, "mono": self.mono}
            return family_map.get(
                family.lower(), family
            )  # Return custom font if not predefined

        raise ValueError(f"Invalid font family type: {type(family)}")


class Typography:
    """Typography management system."""

    def __init__(
        self,
        font_sizes: Optional[FontSizes] = None,
        line_heights: Optional[LineHeights] = None,
        font_weights: Optional[FontWeights] = None,
        font_families: Optional[FontFamilies] = None,
    ):
        self.font_sizes = font_sizes or FontSizes()
        self.line_heights = line_heights or LineHeights()
        self.font_weights = font_weights or FontWeights()
        self.font_families = font_families or FontFamilies()

    def get_font_size(self, size: Union[str, int]) -> int:
        """Get font size."""
        return self.font_sizes.get_size(size)

    def get_line_height(self, height: Union[str, float]) -> float:
        """Get line height."""
        return self.line_heights.get_height(height)

    def get_font_weight(self, weight: Union[str, int]) -> int:
        """Get font weight."""
        return self.font_weights.get_weight(weight)

    def get_font_family(self, family: Union[str, None]) -> str:
        """Get font family."""
        return self.font_families.get_family(family)

    def to_dict(self) -> Dict:
        """Convert typography settings to dictionary."""
        return {
            "font_sizes": {
                "xs": self.font_sizes.xs,
                "sm": self.font_sizes.sm,
                "md": self.font_sizes.md,
                "lg": self.font_sizes.lg,
                "xl": self.font_sizes.xl,
                "xxl": self.font_sizes.xxl,
                "xxxl": self.font_sizes.xxxl,
            },
            "line_heights": {
                "xs": self.line_heights.xs,
                "sm": self.line_heights.sm,
                "md": self.line_heights.md,
                "lg": self.line_heights.lg,
                "xl": self.line_heights.xl,
            },
            "font_weights": {
                "light": self.font_weights.light,
                "normal": self.font_weights.normal,
                "medium": self.font_weights.medium,
                "semibold": self.font_weights.semibold,
                "bold": self.font_weights.bold,
                "extrabold": self.font_weights.extrabold,
            },
            "font_families": {
                "sans": self.font_families.sans,
                "mono": self.font_families.mono,
            },
        }
