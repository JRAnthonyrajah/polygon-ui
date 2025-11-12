from .color_shades import ColorShades
from .design_tokens import DesignTokenValidator


class Colors:
    def __init__(self) -> None:
        self._colors = {
            # Neutral gray palette - updated for modern look
            "gray": ColorShades(
                [
                    "#ffffff",
                    "#fafbfc",
                    "#f1f3f4",
                    "#e8eaed",
                    "#dadce0",
                    "#9aa0a6",
                    "#5f6368",
                    "#3c4043",
                    "#202124",
                    "#000000",
                ]
            ),
            # Primary blue palette - modern vibrant blue
            "blue": ColorShades(
                [
                    "#e8f0fe",
                    "#d2e3fc",
                    "#aecbfa",
                    "#8ab4f8",
                    "#669df6",
                    "#4285f4",
                    "#1a73e8",
                    "#185abc",
                    "#174ea6",
                    "#103f8f",
                ]
            ),
            # Success green palette - modern green
            "green": ColorShades(
                [
                    "#e6f4ea",
                    "#ceead6",
                    "#a8dab5",
                    "#81c995",
                    "#5bb974",
                    "#34a853",
                    "#188038",
                    "#137333",
                    "#0d652d",
                    "#0a4d22",
                ]
            ),
            # Warning orange palette - modern orange
            "orange": ColorShades(
                [
                    "#fef7e0",
                    "#feefc3",
                    "#fde293",
                    "#fdcc4d",
                    "#fbaf34",
                    "#f9ab00",
                    "#ea8600",
                    "#d17e00",
                    "#b56c00",
                    "#8b5a00",
                ]
            ),
            # Error red palette - modern red
            "red": ColorShades(
                [
                    "#fce8e6",
                    "#fadbd8",
                    "#f1c7c0",
                    "#e8b0a6",
                    "#de9593",
                    "#d93025",
                    "#c5221f",
                    "#b31412",
                    "#9c1917",
                    "#8a0a06",
                ]
            ),
            # Accent purple palette - modern purple
            "purple": ColorShades(
                [
                    "#f3e8fd",
                    "#e9d2ff",
                    "#d7bbff",
                    "#c49eff",
                    "#b17fff",
                    "#9f5fff",
                    "#8a3ffc",
                    "#7619da",
                    "#6207d1",
                    "#4c0a8f",
                ]
            ),
        }
        # Basic validation
        self.validate()

        # WCAG AA compliance validation - only in strict mode or testing
        # validator = DesignTokenValidator(self)
        # validator.validate()

    def validate(self) -> None:
        """Validate all colors in the palette."""
        for name, color in self._colors.items():
            # Check shades length and format (already in __post_init__, but revalidate)
            if len(color.shades) != 10:
                raise ValueError(f"Color '{name}' must have 10 shades")
            for i, shade in enumerate(color.shades):
                if not (isinstance(shade, str) and len(shade) == 7 and shade[0] == "#"):
                    raise ValueError(f"Invalid hex shade {i} for '{name}': {shade}")
        # Ensure no duplicate names
        if len(self._colors) != len(set(self._colors.keys())):
            raise ValueError("Duplicate color names detected")

    def get_color(self, color_name: str, shade: int = 5) -> str:
        """Get a specific color shade by name and index (0-9)."""
        if color_name not in self._colors:
            raise ValueError(f"Color '{color_name}' not found")
        if shade < 0 or shade >= 10:
            raise ValueError(f"Shade index {shade} out of range (0-9)")
        return self._colors[color_name].shades[shade]

    def get_background(self, is_dark: bool = False) -> str:
        """Get appropriate background color for theme."""
        return self.get_color("gray", 9 if is_dark else 0)

    def get_surface(self, is_dark: bool = False) -> str:
        """Get surface/card background color."""
        return self.get_color("gray", 8 if is_dark else 1)

    def get_surface_elevated(self, is_dark: bool = False) -> str:
        """Get elevated surface color for cards."""
        return self.get_color("gray", 7 if is_dark else 0)

    def get_text(self, is_dark: bool = False) -> str:
        """Get primary text color."""
        return self.get_color("gray", 0 if is_dark else 9)

    def get_text_secondary(self, is_dark: bool = False) -> str:
        """Get secondary text color."""
        return self.get_color("gray", 1 if is_dark else 6)

    def get_text_muted(self, is_dark: bool = False) -> str:
        """Get muted text color for subtitles."""
        return self.get_color("gray", 3 if is_dark else 5)

    def get_border(self, is_dark: bool = False) -> str:
        """Get border color."""
        return self.get_color("gray", 7 if is_dark else 3)

    def get_border_focus(self, is_dark: bool = False) -> str:
        """Get focus border color."""
        return self.get_color("blue", 4)

    def get_shadow(self, is_dark: bool = False) -> str:
        """Get appropriate shadow for theme."""
        if is_dark:
            return (
                "0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)"
            )
        else:
            return (
                "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
            )

    def to_dict(self) -> dict:
        """Convert colors to dictionary representation."""
        return {name: color.shades for name, color in self._colors.items()}
