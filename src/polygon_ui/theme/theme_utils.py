"""
Theme utilities for Polygon UI.
Provides theme merging, inheritance, and customization utilities.
"""

from typing import Dict, Any, Optional, List, Union
from copy import deepcopy
from dataclasses import dataclass

from .theme import Theme
from .colors import Colors
from .components import ComponentStyles
from .spacing import Spacing


@dataclass
class ThemeOverride:
    """Represents a theme override configuration."""

    colors: Optional[Dict[str, Any]] = None
    spacing: Optional[Dict[str, Union[int, str]]] = None
    radius: Optional[Dict[str, int]] = None
    shadows: Optional[Dict[str, str]] = None
    breakpoints: Optional[Dict[str, int]] = None
    components: Optional[Dict[str, Dict[str, Any]]] = None
    fontFamily: Optional[str] = None
    fontSize: Optional[Dict[str, str]] = None
    lineHeight: Optional[Dict[str, str]] = None


class ThemeMerger:
    """
    Handles theme merging and inheritance operations.

    Supports:
    - Deep merging of theme objects
    - Inheritance from base themes
    - Selective overriding of theme sections
    - Theme validation and conflict resolution
    """

    @staticmethod
    def merge_themes(base_theme: Theme, override_theme: Theme) -> Theme:
        """
        Merge two themes, with override_theme taking precedence.

        Args:
            base_theme: Base theme to merge into
            override_theme: Theme with overrides

        Returns:
            New merged theme instance
        """
        if not base_theme:
            return override_theme
        if not override_theme:
            return base_theme

        # Deep copy the base theme to avoid mutation
        merged_theme = deepcopy(base_theme)

        # Merge color schemes
        if override_theme.color_scheme:
            merged_theme.color_scheme = override_theme.color_scheme
            if hasattr(merged_theme.colors, "_is_dark"):
                merged_theme.colors._is_dark = (
                    override_theme.color_scheme.value == "dark"
                )

        # Merge primary color
        if override_theme.primary_color:
            merged_theme.primary_color = override_theme.primary_color

        # Merge colors - deep merge individual color palettes
        if override_theme.colors:
            merged_theme.colors = ThemeMerger._merge_colors(
                merged_theme.colors, override_theme.colors
            )

        # Merge spacing
        if override_theme.spacing:
            merged_theme.spacing = ThemeMerger._merge_spacing(
                merged_theme.spacing, override_theme.spacing
            )

        # Merge radius
        if override_theme.radius:
            merged_theme.radius.update(override_theme.radius)

        # Merge shadows
        if override_theme.shadows:
            merged_theme.shadows.update(override_theme.shadows)

        # Merge breakpoints
        if override_theme.breakpoints:
            merged_theme.breakpoints.update(override_theme.breakpoints)

        # Merge component styles
        if override_theme.components:
            merged_theme.components = ThemeMerger._merge_components(
                merged_theme.components, override_theme.components
            )

        # Apply any additional attributes
        for attr_name in dir(override_theme):
            if (
                not attr_name.startswith("_")
                and attr_name not in ThemeMerger._get_known_attributes()
            ):
                attr_value = getattr(override_theme, attr_name)
                if attr_value is not None:
                    setattr(merged_theme, attr_name, attr_value)

        return merged_theme

    @staticmethod
    def apply_override(theme: Theme, override: ThemeOverride) -> Theme:
        """
        Apply a theme override to a base theme.

        Args:
            theme: Base theme to apply override to
            override: Override configuration

        Returns:
            New theme with overrides applied
        """
        if not override:
            return theme

        # Create override theme from ThemeOverride
        override_theme = ThemeMerger._create_theme_from_override(override)
        return ThemeMerger.merge_themes(theme, override_theme)

    @staticmethod
    def create_inherited_theme(
        base_theme: Theme, customizations: Dict[str, Any]
    ) -> Theme:
        """
        Create a new theme that inherits from a base theme with customizations.

        Args:
            base_theme: Base theme to inherit from
            customizations: Customization dictionary

        Returns:
            New inherited theme
        """
        override = ThemeOverride()

        # Parse customizations
        if "colors" in customizations:
            override.colors = customizations["colors"]

        if "spacing" in customizations:
            override.spacing = customizations["spacing"]

        if "radius" in customizations:
            override.radius = customizations["radius"]

        if "shadows" in customizations:
            override.shadows = customizations["shadows"]

        if "breakpoints" in customizations:
            override.breakpoints = customizations["breakpoints"]

        if "components" in customizations:
            override.components = customizations["components"]

        if "fontFamily" in customizations:
            override.fontFamily = customizations["fontFamily"]

        if "fontSize" in customizations:
            override.fontSize = customizations["fontSize"]

        if "lineHeight" in customizations:
            override.lineHeight = customizations["lineHeight"]

        if "primaryColor" in customizations:
            # Add to components override
            override.components = override.components or {}
            override.components["primary_color"] = customizations["primaryColor"]

        if "colorScheme" in customizations:
            # Add to components override
            override.components = override.components or {}
            override.components["color_scheme"] = customizations["colorScheme"]

        return ThemeMerger.apply_override(base_theme, override)

    @staticmethod
    def _merge_colors(base_colors: Colors, override_colors: Colors) -> Colors:
        """Merge two color objects."""
        merged_colors = deepcopy(base_colors)

        # Override individual color palettes
        for color_name in override_colors.get_available_colors():
            if override_colors.has_color(color_name):
                shades = override_colors.get_shades(color_name)
                merged_colors.add_custom_color(color_name, shades)

        return merged_colors

    @staticmethod
    def _merge_spacing(base_spacing: Spacing, override_spacing: Spacing) -> Spacing:
        """Merge two spacing objects."""
        # For now, use override spacing completely
        # In a more complex implementation, you might want to merge individual values
        return override_spacing

    @staticmethod
    def _merge_components(
        base_components: ComponentStyles, override_components: ComponentStyles
    ) -> ComponentStyles:
        """Merge two component styles objects."""
        merged_components = ComponentStyles(
            colors=base_components.colors,
            border_radius=base_components.border_radius,
            shadows=base_components.shadows,
            transitions=base_components.transitions,
            component_overrides=base_components.component_overrides.copy(),
        )

        # Apply component overrides from the override components
        for component_name in override_components.get_all_component_names():
            config = override_components.get_component_config(component_name)
            merged_components.override_component(component_name, config)

        return merged_components

    @staticmethod
    def _create_theme_from_override(override: ThemeOverride) -> Theme:
        """Create a Theme object from a ThemeOverride."""
        colors = Colors()  # Default colors
        spacing = Spacing()  # Default spacing

        # Apply color overrides
        if override.colors:
            for color_name, shades in override.colors.items():
                if isinstance(shades, list) and len(shades) == 10:
                    colors.add_custom_color(color_name, shades)

        # Apply spacing overrides
        if override.spacing:
            # Create custom spacing
            from .spacing import SpacingScale

            custom_scale = SpacingScale()
            for size, value in override.spacing.items():
                if hasattr(custom_scale, f"spacing_{size}"):
                    setattr(custom_scale, f"spacing_{size}", value)
            spacing = Spacing(custom_scale)

        return Theme(
            colors=colors,
            spacing=spacing,
            radius=override.radius or {},
            shadows=override.shadows or {},
            breakpoints=override.breakpoints or {},
            fontFamily=override.fontFamily,
            **override.components if override.components else {},
        )

    @staticmethod
    def _get_known_attributes() -> set[str]:
        """Get set of known Theme attributes."""
        return {
            "color_scheme",
            "primary_color",
            "colors",
            "radius",
            "spacing",
            "typography",
            "shadows",
            "breakpoints",
            "components",
        }

    @staticmethod
    def validate_theme_merge(base_theme: Theme, override_theme: Theme) -> List[str]:
        """
        Validate that two themes can be safely merged.

        Args:
            base_theme: Base theme
            override_theme: Theme to merge

        Returns:
            List of validation warnings/errors
        """
        warnings = []

        try:
            # Validate both themes individually
            base_theme.validate()
            override_theme.validate()

            # Check for potential conflicts
            if base_theme.color_scheme != override_theme.color_scheme:
                warnings.append(
                    f"Color scheme mismatch: base={base_theme.color_scheme.value}, "
                    f"override={override_theme.color_scheme.value}"
                )

            # Check color palette compatibility
            base_colors = set(base_theme.colors.get_available_colors())
            override_colors = set(override_theme.colors.get_available_colors())

            missing_colors = override_colors - base_colors
            if missing_colors:
                warnings.append(
                    f"Override theme adds new colors: {', '.join(missing_colors)}"
                )

        except Exception as e:
            warnings.append(f"Theme validation failed: {str(e)}")

        return warnings


class ThemeValidator:
    """Validates theme configurations and provides helpful error messages."""

    @staticmethod
    def validate_theme(theme: Theme) -> List[str]:
        """
        Validate a complete theme configuration.

        Args:
            theme: Theme to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            # Basic theme validation
            theme.validate()

            # Validate color schemes
            if not hasattr(theme.color_scheme, "value"):
                errors.append("Invalid color scheme format")

            # Validate primary color exists in palette
            if theme.primary_color and not theme.colors.has_color(theme.primary_color):
                errors.append(
                    f"Primary color '{theme.primary_color}' not found in color palette"
                )

            # Validate spacing
            if hasattr(theme.spacing, "scale"):
                spacing_sizes = theme.spacing.get_all_sizes()
                if len(spacing_sizes) == 0:
                    errors.append("No spacing sizes defined")

            # Validate radius values
            for size_name, size_value in theme.radius.items():
                if not isinstance(size_value, (int, str)):
                    errors.append(f"Invalid radius value for {size_name}: {size_value}")

            # Validate breakpoint values
            for bp_name, bp_value in theme.breakpoints.items():
                if not isinstance(bp_value, int) or bp_value <= 0:
                    errors.append(f"Invalid breakpoint value for {bp_name}: {bp_value}")

            # Validate component configurations
            if theme.components:
                for component_name in theme.components.get_all_component_names():
                    component_errors = theme.components.validate_component_config(
                        component_name
                    )
                    errors.extend(component_errors)

        except Exception as e:
            errors.append(f"Theme validation error: {str(e)}")

        return errors

    @staticmethod
    def validate_theme_override(override: ThemeOverride) -> List[str]:
        """
        Validate a theme override configuration.

        Args:
            override: Theme override to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Validate color overrides
        if override.colors:
            for color_name, shades in override.colors.items():
                if not isinstance(shades, list):
                    errors.append(f"Color '{color_name}' shades must be a list")
                elif len(shades) != 10:
                    errors.append(f"Color '{color_name}' must have exactly 10 shades")
                else:
                    for i, shade in enumerate(shades):
                        if not isinstance(shade, str) or not shade.startswith("#"):
                            errors.append(
                                f"Invalid shade {i} for color '{color_name}': {shade}"
                            )

        # Validate spacing overrides
        if override.spacing:
            for size_name, size_value in override.spacing.items():
                if not isinstance(size_value, (int, str)):
                    errors.append(
                        f"Invalid spacing value for {size_name}: {size_value}"
                    )

        # Validate radius overrides
        if override.radius:
            for size_name, size_value in override.radius.items():
                if not isinstance(size_value, int) or size_value < 0:
                    errors.append(f"Invalid radius value for {size_name}: {size_value}")

        # Validate breakpoint overrides
        if override.breakpoints:
            for bp_name, bp_value in override.breakpoints.items():
                if not isinstance(bp_value, int) or bp_value <= 0:
                    errors.append(f"Invalid breakpoint value for {bp_name}: {bp_value}")

        return errors

    @staticmethod
    def get_theme_completeness(theme: Theme) -> Dict[str, Any]:
        """
        Analyze theme completeness and provide suggestions.

        Args:
            theme: Theme to analyze

        Returns:
            Dictionary with completeness analysis
        """
        analysis = {
            "score": 0,
            "max_score": 100,
            "missing_colors": [],
            "missing_components": [],
            "recommendations": [],
        }

        score = 0
        max_score = 100

        # Color completeness (30 points)
        expected_colors = {
            "dark",
            "gray",
            "red",
            "pink",
            "grape",
            "violet",
            "indigo",
            "blue",
            "cyan",
            "teal",
            "green",
            "lime",
            "yellow",
            "orange",
        }
        available_colors = set(theme.colors.get_available_colors())
        missing_colors = expected_colors - available_colors

        color_score = max(0, 30 - len(missing_colors) * 2)
        score += color_score
        analysis["missing_colors"] = list(missing_colors)

        # Component completeness (30 points)
        expected_components = {"Button", "TextInput", "Card", "Badge"}
        available_components = set(theme.components.get_all_component_names())
        missing_components = expected_components - available_components

        component_score = max(0, 30 - len(missing_components) * 7)
        score += component_score
        analysis["missing_components"] = list(missing_components)

        # Theme configuration completeness (20 points)
        config_score = 0
        if theme.spacing:
            config_score += 5
        if theme.radius:
            config_score += 5
        if theme.shadows:
            config_score += 5
        if theme.breakpoints:
            config_score += 5
        score += config_score

        # Customization support (20 points)
        customization_score = 20  # Base score for having customization structure
        score += customization_score

        analysis["score"] = score
        analysis["max_score"] = max_score

        # Generate recommendations
        if missing_colors:
            analysis["recommendations"].append(
                f"Add missing color palettes: {', '.join(missing_colors)}"
            )

        if missing_components:
            analysis["recommendations"].append(
                f"Add missing component configurations: {', '.join(missing_components)}"
            )

        if not theme.spacing or not theme.radius:
            analysis["recommendations"].append(
                "Define spacing and radius tokens for consistency"
            )

        if not theme.shadows:
            analysis["recommendations"].append("Define shadow system for elevation")

        if not theme.breakpoints:
            analysis["recommendations"].append(
                "Define breakpoints for responsive design"
            )

        return analysis
