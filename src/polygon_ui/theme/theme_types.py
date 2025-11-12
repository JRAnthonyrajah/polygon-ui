"""Theme type definitions and enums."""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ColorScheme(Enum):
    """Color scheme options for themes."""

    LIGHT = "light"
    DARK = "dark"


@dataclass
class Spacing:
    """Spacing system for consistent layout."""

    def __init__(self) -> None:
        # 8-point grid system
        self.spacing = {
            "0": 0,
            "px": 1,
            "0_5": 2,
            "1": 4,
            "1_5": 6,
            "2": 8,
            "2_5": 10,
            "3": 12,
            "3_5": 14,
            "4": 16,
            "5": 20,
            "6": 24,
            "7": 28,
            "8": 32,
            "9": 36,
            "10": 40,
            "12": 48,
            "16": 64,
            "20": 80,
            "24": 96,
            "32": 128,
        }

    def get_spacing(self, key: str) -> int:
        """Get spacing value by key."""
        return self.spacing.get(key, 0)

    def to_dict(self) -> Dict[str, int]:
        """Convert spacing to dictionary."""
        return self.spacing.copy()


@dataclass
class Typography:
    """Typography system for consistent text styling."""

    def __init__(self) -> None:
        # Font families
        self.font_family = {
            "sans": "Inter, system-ui, -apple-system, sans-serif",
            "serif": "Georgia, Cambria, serif",
            "mono": "JetBrains Mono, Fira Code, monospace",
        }

        # Font sizes (in px)
        self.font_size = {
            "xs": 12,
            "sm": 14,
            "base": 16,
            "lg": 18,
            "xl": 20,
            "2xl": 24,
            "3xl": 30,
            "4xl": 36,
            "5xl": 48,
            "6xl": 60,
            "7xl": 72,
            "8xl": 96,
            "9xl": 128,
        }

        # Line heights
        self.line_height = {
            "none": 1,
            "tight": 1.25,
            "snug": 1.375,
            "normal": 1.5,
            "relaxed": 1.625,
            "loose": 2,
        }

        # Font weights
        self.font_weight = {
            "thin": 100,
            "extralight": 200,
            "light": 300,
            "normal": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700,
            "extrabold": 800,
            "black": 900,
        }

        # Letter spacing (in px)
        self.letter_spacing = {
            "tighter": -0.05,
            "tight": -0.025,
            "normal": 0,
            "wide": 0.025,
            "wider": 0.05,
            "widest": 0.1,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert typography to dictionary."""
        return {
            "font_family": self.font_family,
            "font_size": self.font_size,
            "line_height": self.line_height,
            "font_weight": self.font_weight,
            "letter_spacing": self.letter_spacing,
        }


@dataclass
class Radius:
    """Border radius system for consistent corner styling."""

    def __init__(self) -> None:
        self.radius = {
            "none": 0,
            "sm": 2,
            "DEFAULT": 4,
            "md": 6,
            "lg": 8,
            "xl": 12,
            "2xl": 16,
            "3xl": 24,
            "full": 9999,
        }

    def get_radius(self, key: str) -> int:
        """Get radius value by key."""
        return self.radius.get(key, self.radius["DEFAULT"])

    def to_dict(self) -> Dict[str, int]:
        """Convert radius to dictionary."""
        return self.radius.copy()
