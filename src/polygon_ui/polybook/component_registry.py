"""
Component registry for PolyBook.
"""

from typing import Dict, Any, Type, Callable, List
from dataclasses import dataclass, field


@dataclass
class ComponentInfo:
    """Information about a registered component."""

    name: str
    component_class: Type
    description: str
    category: str
    tags: List[str] = field(default_factory=list)
    default_props: Dict[str, Any] = field(default_factory=dict)
    examples: List[Dict[str, Any]] = field(default_factory=list)


class ComponentRegistry:
    """Registry for components that can be displayed in PolyBook."""

    def __init__(self):
        self._components: Dict[str, ComponentInfo] = {}
        self._categories: Dict[str, List[str]] = {}

    def register_component(
        self,
        name: str,
        component_class: Type,
        description: str = "",
        category: str = "General",
        tags: List[str] = None,
        default_props: Dict[str, Any] = None,
        examples: List[Dict[str, Any]] = None,
    ) -> None:
        """
        Register a component for use in PolyBook.

        Args:
            name: Component name
            component_class: Component class
            description: Component description
            category: Component category
            tags: List of tags for search and filtering
            default_props: Default properties for the component
            examples: Example configurations
        """
        component_info = ComponentInfo(
            name=name,
            component_class=component_class,
            description=description,
            category=category,
            tags=tags or [],
            default_props=default_props or {},
            examples=examples or [],
        )

        self._components[name] = component_info

        # Update categories
        if category not in self._categories:
            self._categories[category] = []
        if name not in self._categories[category]:
            self._categories[category].append(name)

        # Update tags index if needed (for future search)
        if not hasattr(self, "_tags"):
            self._tags = {}
        for tag in tags or []:
            tag_lower = tag.lower()
            if tag_lower not in self._tags:
                self._tags[tag_lower] = []
            if name not in self._tags[tag_lower]:
                self._tags[tag_lower].append(name)

    def get_component(self, name: str) -> ComponentInfo:
        """Get component information by name."""
        if name not in self._components:
            raise ValueError(f"Component '{name}' not found")
        return self._components[name]

    def list_components(self) -> List[str]:
        """List all registered component names."""
        return list(self._components.keys())

    def list_categories(self) -> List[str]:
        """List all component categories."""
        return list(self._categories.keys())

    def get_components_by_category(self, category: str) -> List[ComponentInfo]:
        """Get all components in a specific category."""
        if category not in self._categories:
            return []

        return [
            self._components[name]
            for name in self._categories[category]
            if name in self._components
        ]

    def search_components(self, query: str) -> List[ComponentInfo]:
        """Search components by name, description, category, or tags."""
        query = query.lower()
        results = []

        for component_info in self._components.values():
            if (
                query in component_info.name.lower()
                or query in component_info.description.lower()
                or query in component_info.category.lower()
                or any(query in tag.lower() for tag in component_info.tags)
            ):
                results.append(component_info)

        return results

    def unregister_component(self, name: str) -> None:
        """Unregister a component."""
        if name in self._components:
            component_info = self._components[name]
            category = component_info.category

            del self._components[name]

            # Remove from category
            if category in self._categories and name in self._categories[category]:
                self._categories[category].remove(name)

                # Remove empty category
                if not self._categories[category]:
                    del self._categories[category]

    def get_component_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_components": len(self._components),
            "total_categories": len(self._categories),
            "components_by_category": {
                category: len(components)
                for category, components in self._categories.items()
            },
        }
