"""
Variant system for Polygon UI components.
"""

from typing import Dict, Any, List, Optional
from enum import Enum


class VariantType(Enum):
    """Types of variants."""

    COLOR = "color"
    SIZE = "size"
    STATE = "state"
    STYLE = "style"


class VariantSystem:
    """System for managing component variants."""

    def __init__(self):
        self._variants: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def register_variant(
        self,
        component_name: str,
        variant_type: VariantType,
        variant_name: str,
        styles: Dict[str, Any],
    ) -> None:
        """
        Register a variant for a component.

        Args:
            component_name: Name of the component
            variant_type: Type of variant
            variant_name: Name of the variant
            styles: Style definitions for the variant
        """
        if component_name not in self._variants:
            self._variants[component_name] = {}

        if variant_type.value not in self._variants[component_name]:
            self._variants[component_name][variant_type.value] = {}

        self._variants[component_name][variant_type.value][variant_name] = styles

    def get_variant(
        self, component_name: str, variant_type: VariantType, variant_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get variant styles for a component.

        Args:
            component_name: Name of the component
            variant_type: Type of variant
            variant_name: Name of the variant

        Returns:
            Style definitions or None if not found
        """
        return (
            self._variants.get(component_name, {})
            .get(variant_type.value, {})
            .get(variant_name)
        )

    def list_variants(self, component_name: str) -> Dict[str, List[str]]:
        """
        List all variants for a component.

        Args:
            component_name: Name of the component

        Returns:
            Dictionary mapping variant types to variant names
        """
        component_variants = self._variants.get(component_name, {})
        return {
            variant_type: list(variants.keys())
            for variant_type, variants in component_variants.items()
        }

    def get_default_variants(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Get default variant definitions for common components."""
        return {
            "button": {
                "color": {
                    "primary": {"bg": "primary", "c": "white"},
                    "secondary": {"bg": "gray.6", "c": "white"},
                    "success": {"bg": "green.6", "c": "white"},
                    "warning": {"bg": "yellow.6", "c": "black"},
                    "error": {"bg": "red.6", "c": "white"},
                },
                "style": {
                    "filled": {"bd": "none"},
                    "outline": {
                        "bd": "1px solid primary",
                        "bg": "transparent",
                        "c": "primary",
                    },
                    "light": {"bg": "primary.1", "c": "primary.9"},
                    "subtle": {"bg": "gray.1", "c": "gray.9"},
                    "transparent": {"bg": "transparent", "c": "gray.9"},
                },
                "size": {
                    "xs": {"py": "xs", "px": "sm", "fz": "xs"},
                    "sm": {"py": "sm", "px": "md", "fz": "sm"},
                    "md": {"py": "md", "px": "lg", "fz": "md"},
                    "lg": {"py": "lg", "px": "xl", "fz": "lg"},
                    "xl": {"py": "xl", "px": "xxl", "fz": "xl"},
                },
            },
            "input": {
                "style": {
                    "default": {"bd": "1px solid gray.3"},
                    "filled": {"bg": "gray.0", "bd": "1px solid transparent"},
                    "unstyled": {"bd": "none", "bg": "transparent"},
                },
                "size": {
                    "xs": {"py": "xs", "px": "sm", "fz": "xs"},
                    "sm": {"py": "sm", "px": "md", "fz": "sm"},
                    "md": {"py": "md", "px": "lg", "fz": "md"},
                    "lg": {"py": "lg", "px": "xl", "fz": "lg"},
                    "xl": {"py": "xl", "px": "xxl", "fz": "xl"},
                },
            },
        }

    def load_default_variants(self) -> None:
        """Load default variant definitions."""
        default_variants = self.get_default_variants()

        for component_name, variant_types in default_variants.items():
            for variant_type_str, variants in variant_types.items():
                variant_type = VariantType(variant_type_str)
                for variant_name, styles in variants.items():
                    self.register_variant(
                        component_name, variant_type, variant_name, styles
                    )
