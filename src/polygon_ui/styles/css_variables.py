"""
CSS variable generation and management for Polygon UI.
Provides comprehensive CSS variable system matching Mantine patterns.
"""

from typing import Dict, Any, Optional, List, Set
from ..theme.theme import Theme
from ..theme.theme_types import ColorScheme


class CSSVariableGenerator:
    """
    Generates CSS variables from theme tokens.

    Creates variables for:
    - Colors (including variants and semantic colors)
    - Spacing
    - Typography (font sizes, weights, line heights)
    - Border radius
    - Shadows
    - Breakpoints
    - Transitions
    - Z-index values
    """

    def __init__(self, theme: Theme):
        self.theme = theme
        self._generated_variables: Dict[str, str] = {}
        self._generated_media_queries: Dict[str, str] = {}

    def generate_all_variables(
        self, color_scheme: Optional[ColorScheme] = None
    ) -> Dict[str, str]:
        """
        Generate all CSS variables for the theme.

        Args:
            color_scheme: Force a specific color scheme, or None for current

        Returns:
            Complete CSS variables dictionary
        """
        scheme = color_scheme or self.theme.color_scheme
        variables = {}

        # Core theme variables
        variables.update(self._generate_core_variables(scheme))

        # Color variables
        variables.update(self._generate_color_variables(scheme))

        # Semantic color variables
        variables.update(self._generate_semantic_color_variables(scheme))

        # Variant color variables
        variables.update(self._generate_variant_color_variables())

        # Typography variables
        variables.update(self._generate_typography_variables())

        # Layout variables
        variables.update(self._generate_layout_variables())

        # Component variables
        variables.update(self._generate_component_variables())

        # System variables
        variables.update(self._generate_system_variables())

        return variables

    def _generate_core_variables(self, color_scheme: ColorScheme) -> Dict[str, str]:
        """Generate core theme variables."""
        variables = {}

        # Scale and cursor
        variables["--mantine-scale"] = "1"
        variables["--mantine-cursor-type"] = "default"

        # Color scheme
        variables["--mantine-color-scheme"] = color_scheme.value

        # Font smoothing
        if hasattr(self.theme, "font_smoothing") and self.theme.font_smoothing:
            variables["--mantine-webkit-font-smoothing"] = "antialiased"
            variables["--mantine-moz-font-smoothing"] = "grayscale"
        else:
            variables["--mantine-webkit-font-smoothing"] = "auto"
            variables["--mantine-moz-font-smoothing"] = "auto"

        # Basic colors
        variables["--mantine-color-white"] = "#fff"
        variables["--mantine-color-black"] = "#000"

        return variables

    def _generate_color_variables(self, color_scheme: ColorScheme) -> Dict[str, str]:
        """Generate color palette variables."""
        variables = {}
        color_vars = self.theme.colors.generate_css_variables(color_scheme.value)
        variables.update(color_vars)

        # Primary color variables (these get generated based on theme.primary_color)
        primary_color = self.theme.primary_color or "blue"
        primary_shade = 6  # Default primary shade

        # Generate primary color variables
        for i in range(10):
            variables[
                f"--mantine-primary-color-{i}"
            ] = f"var(--mantine-color-{primary_color}-{i})"

        # Generate primary color variant variables
        if self.theme.colors.has_color(primary_color):
            colors = self.theme.colors.get_variant_colors("filled", primary_color)
            variables.update(colors)

            colors = self.theme.colors.get_variant_colors("light", primary_color)
            variables.update(colors)

            colors = self.theme.colors.get_variant_colors("outline", primary_color)
            variables.update(colors)

        return variables

    def _generate_semantic_color_variables(
        self, color_scheme: ColorScheme
    ) -> Dict[str, str]:
        """Generate semantic color variables."""
        variables = {}

        if color_scheme == ColorScheme.LIGHT:
            variables.update(
                {
                    "--mantine-color-text": "#000",
                    "--mantine-color-body": "#fff",
                    "--mantine-color-error": "var(--mantine-color-red-6)",
                    "--mantine-color-placeholder": "var(--mantine-color-gray-5)",
                    "--mantine-color-dimmed": "var(--mantine-color-gray-6)",
                    "--mantine-color-bright": "#000",
                    "--mantine-color-anchor": "var(--mantine-primary-color-6)",
                    "--mantine-color-default": "#fff",
                    "--mantine-color-default-hover": "var(--mantine-color-gray-0)",
                    "--mantine-color-default-color": "#000",
                    "--mantine-color-default-border": "var(--mantine-color-gray-4)",
                    "--mantine-color-disabled": "var(--mantine-color-gray-1)",
                    "--mantine-color-disabled-color": "var(--mantine-color-gray-5)",
                    "--mantine-color-disabled-border": "var(--mantine-color-gray-3)",
                }
            )

            # Dark theme variants for light mode
            dark_base = "var(--mantine-color-dark-6)"
            variables.update(
                {
                    "--mantine-color-dark-text": "var(--mantine-color-dark-filled)",
                    "--mantine-color-dark-filled": dark_base,
                    "--mantine-color-dark-filled-hover": "var(--mantine-color-dark-7)",
                    "--mantine-color-dark-light": "rgba(46, 46, 46, 0.1)",
                    "--mantine-color-dark-light-hover": "rgba(46, 46, 46, 0.12)",
                    "--mantine-color-dark-light-color": dark_base,
                    "--mantine-color-dark-outline": dark_base,
                    "--mantine-color-dark-outline-hover": "rgba(46, 46, 46, 0.05)",
                }
            )

            # Gray theme variants for light mode
            gray_base = "var(--mantine-color-gray-6)"
            variables.update(
                {
                    "--mantine-color-gray-text": "var(--mantine-color-gray-filled)",
                    "--mantine-color-gray-filled": gray_base,
                    "--mantine-color-gray-filled-hover": "var(--mantine-color-gray-7)",
                    "--mantine-color-gray-light": "rgba(134, 142, 150, 0.1)",
                    "--mantine-color-gray-light-hover": "rgba(134, 142, 150, 0.12)",
                    "--mantine-color-gray-light-color": gray_base,
                    "--mantine-color-gray-outline": gray_base,
                    "--mantine-color-gray-outline-hover": "rgba(134, 142, 150, 0.05)",
                }
            )

        else:  # Dark mode
            variables.update(
                {
                    "--mantine-color-text": "var(--mantine-color-dark-0)",
                    "--mantine-color-body": "var(--mantine-color-dark-7)",
                    "--mantine-color-error": "var(--mantine-color-red-8)",
                    "--mantine-color-placeholder": "var(--mantine-color-dark-3)",
                    "--mantine-color-dimmed": "var(--mantine-color-dark-2)",
                    "--mantine-color-bright": "#fff",
                    "--mantine-color-anchor": "var(--mantine-primary-color-4)",
                    "--mantine-color-default": "var(--mantine-color-dark-6)",
                    "--mantine-color-default-hover": "var(--mantine-color-dark-5)",
                    "--mantine-color-default-color": "#fff",
                    "--mantine-color-default-border": "var(--mantine-color-dark-4)",
                    "--mantine-color-disabled": "var(--mantine-color-dark-6)",
                    "--mantine-color-disabled-color": "var(--mantine-color-dark-3)",
                    "--mantine-color-disabled-border": "var(--mantine-color-dark-4)",
                }
            )

        # Generate variant variables for all available colors
        available_colors = self.theme.colors.get_available_colors()
        for color_name in available_colors:
            if color_name not in [
                "dark",
                "gray",
            ]:  # Skip these as they're handled above
                colors = self.theme.colors.get_variant_colors("filled", color_name)
                variables.update(colors)

                colors = self.theme.colors.get_variant_colors("light", color_name)
                variables.update(colors)

                colors = self.theme.colors.get_variant_colors("outline", color_name)
                variables.update(colors)

        return variables

    def _generate_variant_color_variables(self) -> Dict[str, str]:
        """Generate variant-specific color variables."""
        variables = {}

        # These will be generated dynamically per color in _generate_semantic_color_variables
        # This method can be extended for additional variant types
        return variables

    def _generate_typography_variables(self) -> Dict[str, str]:
        """Generate typography variables."""
        variables = {}

        # Font family variables
        if hasattr(self.theme, "font_family"):
            variables["--mantine-font-family"] = self.theme.font_family
        else:
            variables[
                "--mantine-font-family"
            ] = "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"

        if hasattr(self.theme, "font_family_monospace"):
            variables[
                "--mantine-font-family-monospace"
            ] = self.theme.font_family_monospace
        else:
            variables[
                "--mantine-font-family-monospace"
            ] = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace"

        # Heading font family
        if hasattr(self.theme, "typography") and hasattr(
            self.theme.typography, "font_family_headings"
        ):
            variables[
                "--mantine-font-family-headings"
            ] = self.theme.typography.font_family_headings
        else:
            variables["--mantine-font-family-headings"] = variables[
                "--mantine-font-family"
            ]

        # Font weight variables
        if hasattr(self.theme, "typography") and hasattr(
            self.theme.typography, "font_weight"
        ):
            variables["--mantine-heading-font-weight"] = str(
                self.theme.typography.font_weight.get("heading", 700)
            )
        else:
            variables["--mantine-heading-font-weight"] = "700"

        variables["--mantine-heading-text-wrap"] = "wrap"

        # Font size variables
        font_sizes = {
            "xs": "0.75rem",  # 12px
            "sm": "0.875rem",  # 14px
            "md": "1rem",  # 16px
            "lg": "1.125rem",  # 18px
            "xl": "1.25rem",  # 20px
        }

        for size, value in font_sizes.items():
            variables[f"--mantine-font-size-{size}"] = value

        # Add heading font sizes
        heading_sizes = {
            "h1": "2.125rem",  # 34px
            "h2": "1.625rem",  # 26px
            "h3": "1.375rem",  # 22px
            "h4": "1.125rem",  # 18px
            "h5": "1rem",  # 16px
            "h6": "0.875rem",  # 14px
        }

        for heading, value in heading_sizes.items():
            variables[f"--mantine-{heading}-font-size"] = value

        # Line height variables
        line_heights = {
            "xs": "1.4",
            "sm": "1.45",
            "md": "1.55",
            "lg": "1.6",
            "xl": "1.65",
        }

        for size, value in line_heights.items():
            variables[f"--mantine-line-height-{size}"] = value

        # Default line height
        variables["--mantine-line-height"] = "1.55"

        # Heading line heights
        heading_line_heights = {
            "h1": "1.3",
            "h2": "1.35",
            "h3": "1.4",
            "h4": "1.45",
            "h5": "1.5",
            "h6": "1.5",
        }

        for heading, value in heading_line_heights.items():
            variables[f"--mantine-{heading}-line-height"] = value

        return variables

    def _generate_layout_variables(self) -> Dict[str, str]:
        """Generate layout variables (spacing, radius, shadows, breakpoints)."""
        variables = {}

        # Spacing variables
        if hasattr(self.theme, "spacing") and hasattr(
            self.theme.spacing, "get_all_sizes"
        ):
            spacing_sizes = self.theme.spacing.get_all_sizes()
            for size_name, size_value in spacing_sizes.items():
                variables[f"--mantine-spacing-{size_name}"] = f"{size_value}px"

        # Border radius variables
        radius_sizes = {
            "xs": "0.125rem",  # 2px
            "sm": "0.25rem",  # 4px
            "md": "0.5rem",  # 8px
            "lg": "1rem",  # 16px
            "xl": "2rem",  # 32px
        }

        for size, value in radius_sizes.items():
            variables[f"--mantine-radius-{size}"] = value

        # Default radius
        if hasattr(self.theme, "default_radius"):
            default_radius = self.theme.default_radius
            variables["--mantine-radius-default"] = radius_sizes.get(
                default_radius, radius_sizes["md"]
            )
        else:
            variables["--mantine-radius-default"] = radius_sizes["md"]

        # Shadow variables
        if hasattr(self.theme, "shadows"):
            shadow_sizes = {
                "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            }

            for size, value in shadow_sizes.items():
                variables[f"--mantine-shadow-{size}"] = value

        # Breakpoint variables
        if hasattr(self.theme, "breakpoints"):
            breakpoints = {
                "xs": "36em",  # 576px
                "sm": "48em",  # 768px
                "md": "62em",  # 992px
                "lg": "75em",  # 1200px
                "xl": "88em",  # 1408px
            }

            for bp_name, bp_value in breakpoints.items():
                variables[f"--mantine-breakpoint-{bp_name}"] = bp_value

        return variables

    def _generate_component_variables(self) -> Dict[str, str]:
        """Generate component-specific variables."""
        variables = {}

        if hasattr(self.theme, "components"):
            component_vars = self.theme.components.generate_css_variables()
            variables.update(component_vars)

        return variables

    def _generate_system_variables(self) -> Dict[str, str]:
        """Generate system variables (transitions, z-index, etc.)."""
        variables = {}

        # Transition variables
        variables.update(
            {
                "--mantine-transition-all": "all 0.2s ease",
                "--mantine-transition-transform": "transform 0.2s ease",
                "--mantine-transition-opacity": "opacity 0.2s ease",
                "--mantine-transition-colors": "color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease",
            }
        )

        # Z-index variables
        variables.update(
            {
                "--mantine-z-index-app": "100",
                "--mantine-z-index-modal": "200",
                "--mantine-z-index-popover": "300",
                "--mantine-z-index-overlay": "400",
                "--mantine-z-index-max": "9999",
            }
        )

        return variables

    def generate_css_string(self, variables: Optional[Dict[str, str]] = None) -> str:
        """
        Generate CSS string from variables.

        Args:
            variables: Variables to include, or None for all

        Returns:
            CSS string with variables
        """
        if variables is None:
            variables = self.generate_all_variables()

        css_parts = [":root {"]
        for var_name, var_value in variables.items():
            css_parts.append(f"  {var_name}: {var_value};")
        css_parts.append("}")

        return "\n".join(css_parts)

    def generate_media_queries(self) -> Dict[str, str]:
        """
        Generate media queries for responsive design.

        Returns:
            Dictionary of breakpoint names to media query strings
        """
        if not hasattr(self.theme, "breakpoints"):
            return {}

        media_queries = {}
        breakpoints = {
            "xs": "36em",  # 576px
            "sm": "48em",  # 768px
            "md": "62em",  # 992px
            "lg": "75em",  # 1200px
            "xl": "88em",  # 1408px
        }

        # Override with theme breakpoints if available
        theme_bps = self.theme.breakpoints
        breakpoints.update(theme_bps)

        for bp_name, bp_value in breakpoints.items():
            media_queries[bp_name] = f"@media (min-width: {bp_value})"

        return media_queries

    def get_used_colors(self) -> Set[str]:
        """Get set of color names used in the theme."""
        return set(self.theme.colors.get_available_colors())

    def get_used_variables(self) -> Set[str]:
        """Get set of variable names used in the theme."""
        variables = self.generate_all_variables()
        return set(variables.keys())

    def validate_variables(self) -> List[str]:
        """
        Validate generated CSS variables.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        variables = self.generate_all_variables()

        # Check for valid CSS variable format
        for var_name in variables.keys():
            if not var_name.startswith("--mantine-"):
                errors.append(f"Invalid variable name format: {var_name}")

            # Check for valid CSS values (basic validation)
            var_value = variables[var_name]
            if not var_value or var_value.strip() == "":
                errors.append(f"Empty value for variable: {var_name}")

        return errors

    def get_variable_by_pattern(self, pattern: str) -> Dict[str, str]:
        """
        Get variables matching a pattern.

        Args:
            pattern: Pattern to match (supports simple substring matching)

        Returns:
            Dictionary of matching variables
        """
        all_variables = self.generate_all_variables()
        matching_vars = {}

        for var_name, var_value in all_variables.items():
            if pattern in var_name:
                matching_vars[var_name] = var_value

        return matching_vars

    def update_variables(self, updates: Dict[str, str]) -> None:
        """
        Update specific variables with custom values.

        Args:
            updates: Dictionary of variable updates
        """
        self._generated_variables.update(updates)
