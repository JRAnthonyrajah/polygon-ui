"""
Component factory for Polygon UI components.
"""

from typing import Type, Dict, Any, Optional
from ..theme.theme import Theme


class ComponentFactory:
    """
    Factory class for creating and managing Polygon UI components.
    """

    def __init__(self):
        self._component_classes: Dict[str, Type] = {}
        self._component_configs: Dict[str, Dict[str, Any]] = {}

    def register_component(
        self, name: str, component_class: Type, config: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a component class with the factory.

        Args:
            name: Component name
            component_class: Component class
            config: Component configuration
        """
        self._component_classes[name] = component_class
        if config:
            self._component_configs[name] = config

    def create_component(
        self, name: str, parent: Optional[Any] = None, **kwargs
    ) -> Any:
        """
        Create a component instance.

        Args:
            name: Component name
            parent: Parent widget
            **kwargs: Component properties

        Returns:
            Component instance
        """
        if name not in self._component_classes:
            raise ValueError(f"Component '{name}' not registered")

        component_class = self._component_classes[name]
        config = self._component_configs.get(name, {})

        # Merge config with kwargs
        merged_props = {**config, **kwargs}

        return component_class(parent=parent, **merged_props)

    def list_components(self) -> list[str]:
        """List all registered component names."""
        return list(self._component_classes.keys())

    def get_component_class(self, name: str) -> Optional[Type]:
        """Get component class by name."""
        return self._component_classes.get(name)

    def get_component_config(self, name: str) -> Dict[str, Any]:
        """Get component configuration."""
        return self._component_configs.get(name, {})

    def unregister_component(self, name: str) -> None:
        """Unregister a component."""
        self._component_classes.pop(name, None)
        self._component_configs.pop(name, None)
