"""
Style props system for Polygon UI components.
"""

from typing import Dict, Any, Union


class StyleProps:
    """Manages style props for components."""

    def __init__(self, props: Dict[str, Any] = None):
        self.props = props or {}

    def set_prop(self, name: str, value: Any) -> None:
        """Set a style prop."""
        self.props[name] = value

    def get_prop(self, name: str, default: Any = None) -> Any:
        """Get a style prop value."""
        return self.props.get(name, default)

    def update_props(self, props: Dict[str, Any]) -> None:
        """Update multiple style props."""
        self.props.update(props)

    def to_dict(self) -> Dict[str, Any]:
        """Convert style props to dictionary."""
        return self.props.copy()
