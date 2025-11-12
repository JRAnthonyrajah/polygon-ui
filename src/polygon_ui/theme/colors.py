"""
Color system for Polygon UI - similar to Mantine's color system.
"""

from typing import Dict, List, Union, Optional
from dataclasses import dataclass


@dataclass
class ColorShades:
    """Represents a color with 10 shades (0-9, where 0 is lightest, 9 is darkest)."""

    name: str
    shades: List[str]  # 10 shades from lightest to darkest

    def __post_init__(self):
        if len(self.shades) != 10:
            raise ValueError(
                f"Color {self.name} must have exactly 10 shades, got {len(self.shades)}"
            )

    def get_shade(self, shade: Union[int, str]) -> str:
        """Get a specific shade by index or name."""
        if isinstance(shade, str):
            shade_map = {
                "lightest": 0,
                "lighter": 1,
                "light": 2,
                "default": 5,
                "main": 5,
                "dark": 6,
                "darker": 7,
                "darkest": 8,
            }
            shade = shade_map.get(shade.lower(), 5)

        if isinstance(shade, int):
            if 0 <= shade <= 9:
                return self.shades[shade]
            raise ValueError(f"Shade must be between 0-9, got {shade}")

        raise ValueError(f"Invalid shade type: {type(shade)}")


class Colors:
    """Color palette management system."""

    def __init__(self):
        # Initialize with default colors similar to Mantine
        self._colors: Dict[str, ColorShades] = {}
        self._initialize_default_colors()

    def _initialize_default_colors(self):
        """Initialize default color palette."""
        # These are hex color values - in a real implementation,
        # these would be carefully chosen for accessibility
        default_colors = {
            "blue": [
                "#e7f5ff",
                "#cff4fc",
                "#a5d8ff",
                "#74c0fc",
                "#4dabf7",
                "#339af0",
                "#228be6",
                "#1c7ed6",
                "#1971c2",
                "#1864ab",
            ],
            "red": [
                "#fff5f5",
                "#ffe3e3",
                "#ffc9c9",
                "#ffa8a8",
                "#ff8787",
                "#ff6b6b",
                "#fa5252",
                "#e03131",
                "#c92a2a",
                "#a61e4d",
            ],
            "green": [
                "#ebfbee",
                "#d3f9d8",
                "#b2f2bb",
                "#8ce99a",
                "#69db7c",
                "#51cf66",
                "#40c057",
                "#37b24d",
                "#2f9e44",
                "#2b8a3e",
            ],
            "yellow": [
                "#fff9db",
                "#fff3bf",
                "#ffec99",
                "#ffe066",
                "#ffd43b",
                "#fcc419",
                "#fab005",
                "#f59f00",
                "#f08c00",
                "#e67700",
            ],
            "purple": [
                "#f8f0fc",
                "#f3d9fa",
                "#eebefa",
                "#e599f7",
                "#da77f2",
                "#cc5de8",
                "#be4bdb",
                "#ae3ec9",
                "#9c36b5",
                "#862e9c",
            ],
            "gray": [
                "#f8f9fa",
                "#f1f3f5",
                "#e9ecef",
                "#dee2e6",
                "#ced4da",
                "#adb5bd",
                "#868e96",
                "#495057",
                "#343a40",
                "#212529",
            ],
        }

        for color_name, shades in default_colors.items():
            self._colors[color_name] = ColorShades(color_name, shades)

    def add_color(self, name: str, shades: List[str]) -> None:
        """Add a new color to the palette."""
        self._colors[name] = ColorShades(name, shades)

    def get_color(self, name: str, shade: Union[int, str] = 5) -> str:
        """Get a specific color shade."""
        if name not in self._colors:
            raise ValueError(
                f"Color '{name}' not found. Available colors: {list(self._colors.keys())}"
            )
        return self._colors[name].get_shade(shade)

    def get_color_shades(self, name: str) -> ColorShades:
        """Get all shades for a color."""
        if name not in self._colors:
            raise ValueError(f"Color '{name}' not found")
        return self._colors[name]

    def list_colors(self) -> List[str]:
        """List all available color names."""
        return list(self._colors.keys())

    def to_dict(self) -> Dict[str, List[str]]:
        """Convert colors to dictionary format."""
        return {name: color.shades for name, color in self._colors.items()}


def generate_color_shades(base_color: str, name: Optional[str] = None) -> List[str]:
    """
    Generate 10 color shades from a base color.
    This is a simplified implementation - a real one would use proper color theory.
    """
    # For now, return a simple gradient
    # In a real implementation, you'd convert to HSL, adjust lightness, and convert back
    return [
        base_color + "10",  # Much lighter
        base_color + "20",
        base_color + "30",
        base_color + "40",
        base_color + "50",
        base_color + "60",  # Base color
        base_color + "70",
        base_color + "80",
        base_color + "90",
        base_color + "A0",  # Much darker
    ]
