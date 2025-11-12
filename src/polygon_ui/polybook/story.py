"""
Story system for PolyBook - similar to Storybook stories.
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Story:
    """A story represents a component state or configuration."""

    name: str
    description: str = ""
    props: Dict[str, Any] = None
    template: Optional[str] = None
    code: Optional[str] = None

    def __post_init__(self):
        if self.props is None:
            self.props = {}


class StoryManager:
    """Manages stories for components in PolyBook."""

    def __init__(self):
        self._stories: Dict[
            str, Dict[str, Story]
        ] = {}  # component_name -> story_name -> Story

    def add_story(self, component_name: str, story: Story) -> None:
        """
        Add a story for a component.

        Args:
            component_name: Name of the component
            story: Story to add
        """
        if component_name not in self._stories:
            self._stories[component_name] = {}

        self._stories[component_name][story.name] = story

    def get_story(self, component_name: str, story_name: str) -> Optional[Story]:
        """Get a specific story."""
        return self._stories.get(component_name, {}).get(story_name)

    def list_stories(self, component_name: str) -> list[Story]:
        """List all stories for a component."""
        return list(self._stories.get(component_name, {}).values())

    def list_all_stories(self) -> Dict[str, list[Story]]:
        """List all stories grouped by component."""
        return {
            component_name: list(stories.values())
            for component_name, stories in self._stories.items()
        }

    def remove_story(self, component_name: str, story_name: str) -> None:
        """Remove a story."""
        if component_name in self._stories:
            self._stories[component_name].pop(story_name, None)

            # Remove component entry if no stories left
            if not self._stories[component_name]:
                del self._stories[component_name]

    def create_default_stories(self, component_name: str, component_info) -> None:
        """
        Create default stories for a component.

        Args:
            component_name: Name of the component
            component_info: Component information
        """
        # Default story
        default_story = Story(
            name="Default",
            description="Default state of the component",
            props=deepcopy(component_info.default_props),
        )
        self.add_story(component_name, default_story)

        # Example stories
        for i, example in enumerate(component_info.examples):
            example_story = Story(
                name=f"Example {i + 1}",
                description=f"Example {i + 1} from component definition",
                props=deepcopy(example),
            )
            self.add_story(component_name, example_story)

    def get_story_count(self, component_name: str) -> int:
        """Get the number of stories for a component."""
        return len(self._stories.get(component_name, {}))

    def get_total_stories(self) -> int:
        """Get total number of stories across all components."""
        return sum(len(stories) for stories in self._stories.values())

    def duplicate_story(
        self, component_name: str, story_name: str, new_story_name: str
    ) -> Optional[Story]:
        """Duplicate a story with a new name."""
        original_story = self.get_story(component_name, story_name)
        if not original_story:
            return None

        new_story = Story(
            name=new_story_name,
            description=f"Copy of {story_name}",
            props=deepcopy(original_story.props),
            template=original_story.template,
            code=original_story.code,
        )

        self.add_story(component_name, new_story)
        return new_story

    def update_story(
        self, component_name: str, story_name: str, **updates
    ) -> Optional[Story]:
        """Update a story with new values."""
        story = self.get_story(component_name, story_name)
        if not story:
            return None

        for key, value in updates.items():
            if hasattr(story, key):
                setattr(story, key, value)

        return story
