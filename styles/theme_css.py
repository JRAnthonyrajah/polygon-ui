"""
Theme CSS generation utilities for Polygon UI.
Provides comprehensive CSS generation with optimization and minification.
"""

from typing import Dict, Any, Optional, List, Tuple
import re
from dataclasses import dataclass
from ..theme.theme import Theme
from .css_variables import CSSVariableGenerator
from .qss_generator import QSSGenerator


@dataclass
class CSSGenerationOptions:
    """Options for CSS generation."""

    include_comments: bool = True
    minify: bool = False
    include_media_queries: bool = True
    include_vendor_prefixes: bool = True
    optimize_variables: bool = True
    source_map: bool = False
    pretty_print: bool = True


class ThemeCSSGenerator:
    """
    Generates comprehensive CSS for theme systems.

    Features:
    - Complete CSS variable generation
    - Component-specific CSS
    - Responsive design support
    - CSS optimization and minification
    - Cross-browser compatibility
    - Source map generation
    """

    def __init__(self, theme: Theme, options: Optional[CSSGenerationOptions] = None):
        self.theme = theme
        self.options = options or CSSGenerationOptions()
        self.variable_generator = CSSVariableGenerator(theme)
        self.qss_generator = QSSGenerator(theme)

    def generate_theme_css(self) -> str:
        """
        Generate complete theme CSS.

        Returns:
            Complete CSS string for the theme
        """
        css_parts = []

        # Add header comment
        if self.options.include_comments:
            css_parts.append(self._generate_header_comment())

        # CSS variables
        css_parts.append(self._generate_variables_css())

        # Component CSS
        css_parts.append(self._generate_components_css())

        # Responsive CSS
        if self.options.include_media_queries:
            css_parts.append(self._generate_responsive_css())

        # Utility CSS
        css_parts.append(self._generate_utilities_css())

        # Combine all parts
        full_css = "\n\n".join(css_parts)

        # Apply post-processing
        if self.options.minify:
            full_css = self._minify_css(full_css)
        elif self.options.pretty_print:
            full_css = self._prettify_css(full_css)

        return full_css

    def generate_qss(self) -> str:
        """
        Generate Qt Style Sheet (QSS) for the theme.

        Returns:
            QSS string for Qt styling
        """
        return self.qss_generator.generate_theme_qss()

    def generate_variables_css(self) -> str:
        """
        Generate CSS variables only.

        Returns:
            CSS variables string
        """
        css_parts = []

        if self.options.include_comments:
            css_parts.append("/* CSS Variables */")

        # Generate all variables
        variables = self.variable_generator.generate_all_variables()

        if self.options.optimize_variables:
            # Optimize variable usage
            variables = self._optimize_variables(variables)

        css_parts.append(":root {")
        for var_name, var_value in variables.items():
            css_parts.append(f"  {var_name}: {var_value};")
        css_parts.append("}")

        return "\n".join(css_parts)

    def generate_component_css(self, component_name: str) -> str:
        """
        Generate CSS for a specific component.

        Args:
            component_name: Name of the component

        Returns:
            Component CSS string
        """
        if not hasattr(self.theme, "components"):
            return ""

        css_parts = []
        config = self.theme.components.get_component_config(component_name)

        if not config:
            return f'/* Component "{component_name}" not found */'

        if self.options.include_comments:
            css_parts.append(f"/* {component_name} Component */")

        # Generate base styles
        styles = self.theme.components.get_component_styles(component_name)
        for selector, style_dict in styles.items():
            css_parts.append(
                self._generate_selector_css(
                    f".mantine-{component_name}-{selector}", style_dict
                )
            )

        # Generate variant styles
        variants = self.theme.components.get_component_variants(component_name)
        for variant_name, variant_dict in variants.items():
            css_parts.append(
                self._generate_variant_css(component_name, variant_name, variant_dict)
            )

        # Generate size styles
        sizes = self.theme.components.get_component_sizes(component_name)
        for size_name, size_dict in sizes.items():
            css_parts.append(
                self._generate_size_css(component_name, size_name, size_dict)
            )

        return "\n\n".join(css_parts)

    def _generate_components_css(self) -> str:
        """Generate CSS for all components."""
        if not hasattr(self.theme, "components"):
            return ""

        css_parts = []

        if self.options.include_comments:
            css_parts.append("/* Component Styles */")

        component_names = self.theme.components.get_all_component_names()
        for component_name in sorted(component_names):
            css_parts.append(self.generate_component_css(component_name))

        return "\n\n".join(css_parts)

    def _generate_responsive_css(self) -> str:
        """Generate responsive CSS with media queries."""
        css_parts = []
        media_queries = self.variable_generator.generate_media_queries()

        if self.options.include_comments:
            css_parts.append("/* Responsive Styles */")

        # Add responsive utility classes
        css_parts.extend(self._generate_responsive_utilities(media_queries))

        return "\n\n".join(css_parts)

    def _generate_utilities_css(self) -> str:
        """Generate utility CSS classes."""
        css_parts = []

        if self.options.include_comments:
            css_parts.append("/* Utility Classes */")

        # Spacing utilities
        css_parts.extend(self._generate_spacing_utilities())

        # Color utilities
        css_parts.extend(self._generate_color_utilities())

        # Display utilities
        css_parts.extend(self._generate_display_utilities())

        return "\n\n".join(css_parts)

    def _generate_selector_css(self, selector: str, styles: Dict[str, Any]) -> str:
        """Generate CSS for a specific selector."""
        css_lines = [f"{selector} {{"]

        for prop, value in styles.items():
            if self.options.include_vendor_prefixes:
                value = self._add_vendor_prefixes(prop, value)

            css_lines.append(f"  {prop}: {value};")

        css_lines.append("}}")
        return "\n".join(css_lines)

    def _generate_variant_css(
        self, component_name: str, variant_name: str, variant_dict: Dict[str, Any]
    ) -> str:
        """Generate CSS for component variant."""
        base_selector = f'.mantine-{component_name}[data-variant="{variant_name}"]'
        return self._generate_selector_css(base_selector, variant_dict)

    def _generate_size_css(
        self, component_name: str, size_name: str, size_dict: Dict[str, Any]
    ) -> str:
        """Generate CSS for component size."""
        base_selector = f'.mantine-{component_name}[data-size="{size_name}"]'
        return self._generate_selector_css(base_selector, size_dict)

    def _generate_responsive_utilities(
        self, media_queries: Dict[str, str]
    ) -> List[str]:
        """Generate responsive utility classes."""
        css_parts = []

        # Generate hidden/visible classes
        for bp_name in media_queries.keys():
            css_parts.extend(
                [
                    f".mantine-hidden-from-{bp_name} {{",
                    f"  display: none !important;",
                    f"}}",
                    "",
                    f".mantine-visible-from-{bp_name} {{",
                    f"  display: block !important;",
                    f"}}",
                    "",
                ]
            )

        return css_parts

    def _generate_spacing_utilities(self) -> List[str]:
        """Generate spacing utility classes."""
        css_parts = []

        # Margin utilities
        spacing_props = [
            "margin",
            "margin-top",
            "margin-bottom",
            "margin-left",
            "margin-right",
        ]
        for prop in spacing_props:
            css_parts.append(
                f'.mantine-{prop.replace("-", "")} {{ {prop}: var(--mantine-spacing-md); }}'
            )

        # Padding utilities
        spacing_props = [
            "padding",
            "padding-top",
            "padding-bottom",
            "padding-left",
            "padding-right",
        ]
        for prop in spacing_props:
            css_parts.append(
                f'.mantine-{prop.replace("-", "")} {{ {prop}: var(--mantine-spacing-md); }}'
            )

        return css_parts

    def _generate_color_utilities(self) -> List[str]:
        """Generate color utility classes."""
        css_parts = []

        available_colors = self.variable_generator.get_used_colors()
        for color_name in available_colors:
            for i in range(10):
                css_parts.append(
                    f".mantine-{color_name}-{i} {{ color: var(--mantine-color-{color_name}-{i}); }}"
                )
                css_parts.append(
                    f".mantine-bg-{color_name}-{i} {{ background-color: var(--mantine-color-{color_name}-{i}); }}"
                )

        return css_parts

    def _generate_display_utilities(self) -> List[str]:
        """Generate display utility classes."""
        css_parts = [
            ".mantine-block { display: block; }",
            ".mantine-inline-block { display: inline-block; }",
            ".mantine-inline { display: inline; }",
            ".mantine-flex { display: flex; }",
            ".mantine-grid { display: grid; }",
            ".mantine-hidden { display: none; }",
            ".mantine-invisible { visibility: hidden; }",
            ".mantine-visible { visibility: visible; }",
        ]

        return css_parts

    def _generate_header_comment(self) -> str:
        """Generate CSS header comment."""
        return f"""/*
 * Polygon UI Theme CSS
 * Generated: Theme with {len(self.variable_generator.get_used_colors())} colors
 * Color Scheme: {self.theme.color_scheme.value}
 * Primary Color: {self.theme.primary_color}
 */

"""

    def _add_vendor_prefixes(self, property: str, value: str) -> str:
        """Add vendor prefixes to CSS properties."""
        prefixed_properties = {
            "transform": True,
            "transition": True,
            "animation": True,
            "border-radius": True,
            "box-shadow": True,
            "user-select": True,
        }

        if (
            not self.options.include_vendor_prefixes
            or property not in prefixed_properties
        ):
            return value

        prefixes = []
        if property == "transform":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
            prefixes.append(f"-ms-{property}: {value}")
        elif property == "transition":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
            prefixes.append(f"-ms-{property}: {value}")
        elif property == "animation":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
            prefixes.append(f"-o-{property}: {value}")
        elif property == "border-radius":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
        elif property == "box-shadow":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
        elif property == "user-select":
            prefixes.append(f"-webkit-{property}: {value}")
            prefixes.append(f"-moz-{property}: {value}")
            prefixes.append(f"-ms-{property}: {value}")

        # Include original property
        prefixes.append(f"{property}: {value}")

        return ";\n  ".join(prefixes)

    def _optimize_variables(self, variables: Dict[str, str]) -> Dict[str, str]:
        """Optimize CSS variables by removing unused ones."""
        # For now, return all variables
        # In a real implementation, this would analyze usage patterns
        return variables

    def _minify_css(self, css: str) -> str:
        """Minify CSS by removing whitespace and comments."""
        # Remove comments
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

        # Remove extra whitespace
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r";\s*}", "}", css)
        css = re.sub(r"{\s*", "{", css)

        # Remove unnecessary newlines
        css = css.strip()

        return css

    def _prettify_css(self, css: str) -> str:
        """Prettify CSS by adding proper formatting."""
        lines = css.split("\n")
        prettified_lines = []
        indent_level = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle opening/closing braces
            if line.endswith("{"):
                prettified_lines.append("  " * indent_level + line)
                indent_level += 1
            elif line.startswith("}"):
                indent_level = max(0, indent_level - 1)
                prettified_lines.append("  " * indent_level + line)
            else:
                prettified_lines.append("  " * (indent_level + 1) + line)

        return "\n".join(prettified_lines)

    def generate_source_map(self, css: str, source_file: str = None) -> str:
        """
        Generate a basic source map for CSS.

        Args:
            css: Generated CSS
            source_file: Optional source file path

        Returns:
            Source map JSON string
        """
        # Basic source map generation
        # In a real implementation, this would be more sophisticated
        source_map = {
            "version": 3,
            "file": source_file or "theme.css",
            "sourceRoot": "",
            "sources": [source_file or "theme.scss"],
            "names": [],
            "mappings": "",
        }

        import json

        return json.dumps(source_map, indent=2)

    def validate_css(self, css: str) -> List[str]:
        """
        Validate generated CSS for common issues.

        Args:
            css: CSS to validate

        Returns:
            List of validation errors
        """
        errors = []

        # Check for CSS syntax errors (basic validation)
        open_braces = css.count("{")
        close_braces = css.count("}")
        if open_braces != close_braces:
            errors.append(f"Unmatched braces: {open_braces} open, {close_braces} close")

        # Check for invalid CSS variables
        variables = self.variable_generator.get_used_variables()
        for var in variables:
            if var not in css:
                errors.append(f"Unused variable: {var}")

        # Check for undefined variables
        var_pattern = r"var\((--mantine-[\w-]+)\)"
        used_vars = re.findall(var_pattern, css)
        for var in used_vars:
            if var not in variables:
                errors.append(f"Undefined variable: {var}")

        return errors


class CSSOptimizer:
    """
    Optimizes CSS for production use.

    Features:
    - Dead code elimination
    - Variable usage optimization
    - CSS compression
    - Critical CSS extraction
    """

    @staticmethod
    def optimize_css(css: str, used_variables: Optional[Set[str]] = None) -> str:
        """
        Optimize CSS by removing unused variables and dead code.

        Args:
            css: CSS to optimize
            used_variables: Set of variables that are actually used

        Returns:
            Optimized CSS
        """
        if used_variables is None:
            return css

        # Remove unused variables
        lines = css.split("\n")
        optimized_lines = []
        in_variable_block = False
        keep_current_var = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith(":root"):
                in_variable_block = True
                optimized_lines.append(line)
            elif stripped == "}":
                in_variable_block = False
                optimized_lines.append(line)
            elif in_variable_block and stripped.startswith("--mantine-"):
                # Check if variable is used
                var_name = stripped.split(":")[0]
                if var_name in used_variables:
                    optimized_lines.append(line)
            else:
                optimized_lines.append(line)

        return "\n".join(optimized_lines)

    @staticmethod
    def extract_critical_css(css: str, above_fold_selectors: List[str]) -> str:
        """
        Extract critical CSS for above-the-fold content.

        Args:
            css: Full CSS
            above_fold_selectors: Selectors that are above the fold

        Returns:
            Critical CSS
        """
        lines = css.split("\n")
        critical_lines = []
        capture = False
        brace_count = 0

        for line in lines:
            # Check if line matches a critical selector
            if any(selector in line for selector in above_fold_selectors):
                capture = True

            if capture:
                critical_lines.append(line)
                brace_count += line.count("{") - line.count("}")

                if brace_count == 0:
                    capture = False

        return "\n".join(critical_lines)

    @staticmethod
    def compress_css(css: str) -> str:
        """
        Compress CSS for production.

        Args:
            css: CSS to compress

        Returns:
            Compressed CSS
        """
        # Remove comments
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

        # Remove whitespace
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r";\s*}", "}", css)
        css = re.sub(r"{\s*", "{", css)
        css = re.sub(r"}\s*", "}", css)

        return css.strip()
