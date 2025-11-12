"""
Styles API for Polygon UI components.
"""

from typing import Dict, Any, Callable, Optional


class StylesAPI:
    """Styles API for component customization."""

    def __init__(self, styles: Dict[str, Any] = None):
        self.styles = styles or {}

    def set_style(self, selector: str, style: Dict[str, Any]) -> None:
        """Set style for a specific selector."""
        self.styles[selector] = style

    def get_style(self, selector: str) -> Optional[Dict[str, Any]]:
        """Get style for a specific selector."""
        return self.styles.get(selector)

    def apply_function(self, style_func: Callable) -> Dict[str, Any]:
        """Apply a function to generate styles."""
        return style_func()

    def to_dict(self) -> Dict[str, Any]:
        """Convert styles to dictionary."""
        return self.styles.copy()
