from .color_shades import ColorShades
from .design_tokens import DesignTokenValidator


class Colors:
    def __init__(self) -> None:
        self._colors = {
            # Dark palette (for dark themes)
            "dark": ColorShades(
                [
                    "#C9C9C9",  # 0 - lightest
                    "#b8b8b8",
                    "#828282",
                    "#696969",
                    "#424242",
                    "#3b3b3b",
                    "#2e2e2e",
                    "#242424",
                    "#1f1f1f",
                    "#141414",  # 9 - darkest
                ]
            ),
            # Neutral gray palette - updated for modern look
            "gray": ColorShades(
                [
                    "#f8f9fa",  # 0 - lightest
                    "#f1f3f5",
                    "#e9ecef",
                    "#dee2e6",
                    "#ced4da",
                    "#adb5bd",
                    "#868e96",
                    "#495057",
                    "#343a40",
                    "#212529",  # 9 - darkest
                ]
            ),
            # Red palette
            "red": ColorShades(
                [
                    "#fff5f5",  # 0 - lightest
                    "#ffe3e3",
                    "#ffc9c9",
                    "#ffa8a8",
                    "#ff8787",
                    "#ff6b6b",
                    "#fa5252",
                    "#f03e3e",
                    "#e03131",
                    "#c92a2a",  # 9 - darkest
                ]
            ),
            # Pink palette
            "pink": ColorShades(
                [
                    "#fff0f6",  # 0 - lightest
                    "#ffdeeb",
                    "#fcc2d7",
                    "#faa2c1",
                    "#f783ac",
                    "#f06595",
                    "#e64980",
                    "#d6336c",
                    "#c2255c",
                    "#a61e4d",  # 9 - darkest
                ]
            ),
            # Grape palette
            "grape": ColorShades(
                [
                    "#f8f0fc",  # 0 - lightest
                    "#f3d9fa",
                    "#eebefa",
                    "#e599f7",
                    "#da77f2",
                    "#cc5de8",
                    "#be4bdb",
                    "#ae3ec9",
                    "#9c36b5",
                    "#862e9c",  # 9 - darkest
                ]
            ),
            # Violet palette
            "violet": ColorShades(
                [
                    "#f3f0ff",  # 0 - lightest
                    "#e5dbff",
                    "#d0bfff",
                    "#b197fc",
                    "#9775fa",
                    "#845ef7",
                    "#7950f2",
                    "#7048e8",
                    "#6741d9",
                    "#5f3dc4",  # 9 - darkest
                ]
            ),
            # Indigo palette
            "indigo": ColorShades(
                [
                    "#edf2ff",  # 0 - lightest
                    "#dbe4ff",
                    "#bac8ff",
                    "#91a7ff",
                    "#748ffc",
                    "#5c7cfa",
                    "#4c6ef5",
                    "#4263eb",
                    "#3b5bdb",
                    "#364fc7",  # 9 - darkest
                ]
            ),
            # Blue palette - modern vibrant blue
            "blue": ColorShades(
                [
                    "#e7f5ff",  # 0 - lightest
                    "#d0ebff",
                    "#a5d8ff",
                    "#74c0fc",
                    "#4dabf7",
                    "#339af0",
                    "#228be6",
                    "#1c7ed6",
                    "#1971c2",
                    "#1864ab",  # 9 - darkest
                ]
            ),
            # Cyan palette
            "cyan": ColorShades(
                [
                    "#e3fafc",  # 0 - lightest
                    "#c5f6fa",
                    "#99e9f2",
                    "#66d9e8",
                    "#3bc9db",
                    "#22b8cf",
                    "#15aabf",
                    "#1098ad",
                    "#0c8599",
                    "#0b7285",  # 9 - darkest
                ]
            ),
            # Teal palette
            "teal": ColorShades(
                [
                    "#e6fcf5",  # 0 - lightest
                    "#c3fae8",
                    "#96f2d7",
                    "#63e6be",
                    "#38d9a9",
                    "#20c997",
                    "#12b886",
                    "#0ca678",
                    "#099268",
                    "#087f5b",  # 9 - darkest
                ]
            ),
            # Green palette - modern green
            "green": ColorShades(
                [
                    "#ebfbee",  # 0 - lightest
                    "#d3f9d8",
                    "#b2f2bb",
                    "#8ce99a",
                    "#69db7c",
                    "#51cf66",
                    "#40c057",
                    "#37b24d",
                    "#2f9e44",
                    "#2b8a3e",  # 9 - darkest
                ]
            ),
            # Lime palette
            "lime": ColorShades(
                [
                    "#f4fce3",  # 0 - lightest
                    "#e9fac8",
                    "#d8f5a2",
                    "#c0eb75",
                    "#a9e34b",
                    "#94d82d",
                    "#82c91e",
                    "#74b816",
                    "#66a80f",
                    "#5c940d",  # 9 - darkest
                ]
            ),
            # Yellow palette
            "yellow": ColorShades(
                [
                    "#fff9db",  # 0 - lightest
                    "#fff3bf",
                    "#ffec99",
                    "#ffe066",
                    "#ffd43b",
                    "#fcc419",
                    "#fab005",
                    "#f59f00",
                    "#f08c00",
                    "#e67700",  # 9 - darkest
                ]
            ),
            # Orange palette - modern orange
            "orange": ColorShades(
                [
                    "#fff4e6",  # 0 - lightest
                    "#ffe8cc",
                    "#ffd8a8",
                    "#ffc078",
                    "#ffa94d",
                    "#ff922b",
                    "#fd7e14",
                    "#f76707",
                    "#e8590c",
                    "#d9480f",  # 9 - darkest
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

    def get_available_colors(self) -> list[str]:
        """Get list of available color names."""
        return list(self._colors.keys())

    def has_color(self, color_name: str) -> bool:
        """Check if a color exists in the palette."""
        return color_name in self._colors

    def add_custom_color(self, name: str, shades: list[str]) -> None:
        """
        Add a custom color to the palette.

        Args:
            name: Color name
            shades: List of 10 hex color shades from lightest (0) to darkest (9)
        """
        if len(shades) != 10:
            raise ValueError(f"Color '{name}' must have exactly 10 shades")

        self._colors[name] = ColorShades(shades)
        self.validate()

    def get_shades(self, color_name: str) -> list[str]:
        """Get all shades for a specific color."""
        if color_name not in self._colors:
            raise ValueError(f"Color '{color_name}' not found")
        return self._colors[color_name].shades.copy()

    def generate_css_variables(self, color_scheme: str = "light") -> dict[str, str]:
        """
        Generate CSS variables for all colors.

        Args:
            color_scheme: 'light' or 'dark' - affects which variables are generated

        Returns:
            Dictionary of CSS variable names to values
        """
        css_vars = {}

        # Basic color variables
        css_vars["--mantine-color-white"] = "#fff"
        css_vars["--mantine-color-black"] = "#000"

        # Generate variables for each color palette
        for color_name, color_shades in self._colors.items():
            for i, shade in enumerate(color_shades.shades):
                css_vars[f"--mantine-color-{color_name}-{i}"] = shade

        # Generate semantic color variables (light theme)
        if color_scheme == "light":
            css_vars["--mantine-color-text"] = "#000"
            css_vars["--mantine-color-body"] = "#fff"
            css_vars["--mantine-color-error"] = css_vars["--mantine-color-red-6"]
            css_vars["--mantine-color-placeholder"] = css_vars["--mantine-color-gray-5"]
            css_vars["--mantine-color-dimmed"] = css_vars["--mantine-color-gray-6"]
            css_vars["--mantine-color-bright"] = css_vars["--mantine-color-black"]
            css_vars["--mantine-color-anchor"] = css_vars["--mantine-color-blue-6"]
            css_vars["--mantine-color-default"] = css_vars["--mantine-color-white"]
            css_vars["--mantine-color-default-hover"] = css_vars[
                "--mantine-color-gray-0"
            ]
            css_vars["--mantine-color-default-color"] = css_vars[
                "--mantine-color-black"
            ]
            css_vars["--mantine-color-default-border"] = css_vars[
                "--mantine-color-gray-4"
            ]
        else:
            # Dark theme semantic colors
            css_vars["--mantine-color-text"] = css_vars["--mantine-color-dark-0"]
            css_vars["--mantine-color-body"] = css_vars["--mantine-color-dark-7"]
            css_vars["--mantine-color-error"] = css_vars["--mantine-color-red-8"]
            css_vars["--mantine-color-placeholder"] = css_vars["--mantine-color-dark-3"]
            css_vars["--mantine-color-dimmed"] = css_vars["--mantine-color-dark-2"]
            css_vars["--mantine-color-bright"] = css_vars["--mantine-color-white"]
            css_vars["--mantine-color-anchor"] = css_vars["--mantine-color-blue-4"]
            css_vars["--mantine-color-default"] = css_vars["--mantine-color-dark-6"]
            css_vars["--mantine-color-default-hover"] = css_vars[
                "--mantine-color-dark-5"
            ]
            css_vars["--mantine-color-default-color"] = css_vars[
                "--mantine-color-white"
            ]
            css_vars["--mantine-color-default-border"] = css_vars[
                "--mantine-color-dark-4"
            ]

        return css_vars

    def get_variant_colors(self, variant: str, color_name: str) -> dict[str, str]:
        """
        Get colors for a specific component variant.

        Args:
            variant: Component variant ('filled', 'light', 'outline', 'default', 'white')
            color_name: Color name for the variant

        Returns:
            Dictionary of CSS variables for the variant
        """
        if color_name not in self._colors:
            raise ValueError(f"Color '{color_name}' not found")

        color_prefix = f"--mantine-color-{color_name}"
        variant_colors = {}

        if variant == "filled":
            variant_colors[f"{color_prefix}-filled"] = self._colors[color_name].shades[
                6
            ]
            variant_colors[f"{color_prefix}-filled-hover"] = self._colors[
                color_name
            ].shades[7]
        elif variant == "light":
            # Create light variant with transparency
            base_color = self._colors[color_name].shades[6]
            variant_colors[
                f"{color_prefix}-light"
            ] = f"rgba({self._hex_to_rgb(base_color)}, 0.1)"
            variant_colors[
                f"{color_prefix}-light-hover"
            ] = f"rgba({self._hex_to_rgb(base_color)}, 0.12)"
            variant_colors[f"{color_prefix}-light-color"] = self._colors[
                color_name
            ].shades[6]
        elif variant == "outline":
            variant_colors[f"{color_prefix}-outline"] = self._colors[color_name].shades[
                6
            ]
            variant_colors[
                f"{color_prefix}-outline-hover"
            ] = f"rgba({self._hex_to_rgb(self._colors[color_name].shades[6])}, 0.05)"
        elif variant == "default":
            variant_colors[f"{color_prefix}-default"] = "#fff"
            variant_colors[f"{color_prefix}-default-hover"] = "#f8f9fa"
            variant_colors[f"{color_prefix}-default-color"] = "#000"
            variant_colors[f"{color_prefix}-default-border"] = "#dee2e6"
        elif variant == "white":
            variant_colors[f"{color_prefix}-white"] = "#fff"
            variant_colors[f"{color_prefix}-white-hover"] = "#f8f9fa"
            variant_colors[f"{color_prefix}-white-color"] = "#000"
            variant_colors[f"{color_prefix}-white-border"] = "#e9ecef"

        return variant_colors

    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])

        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
