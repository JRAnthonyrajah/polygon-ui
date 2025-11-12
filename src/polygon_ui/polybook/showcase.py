"""
Showcase templates for common component patterns in PolyBook.
"""

from typing import Dict, Any, List
from dataclasses import dataclass

from polygon_ui import Button, Card, Stack, Text, Group, Form, Input, Select


@dataclass
class ShowcaseTemplate:
    """Pre-built template for component showcase."""

    name: str
    title: str
    description: str
    category: str
    components: List[str]
    props_overrides: Dict[str, Dict[str, Any]]
    layout: str  # 'stack', 'group', 'form', etc.
    example_code: str


class ShowcaseTemplates:
    """Manager for showcase templates."""

    def __init__(self):
        self.templates: Dict[str, ShowcaseTemplate] = {}
        self._init_templates()

    def _init_templates(self):
        """Initialize built-in templates."""

        # Button templates
        self.templates["basic_button"] = ShowcaseTemplate(
            name="basic_button",
            title="Basic Button Showcase",
            description="Simple buttons with variants and states.",
            category="Buttons",
            components=["Button"],
            props_overrides={
                "Button": {
                    "variants": ["filled", "light", "outline", "subtle", "gradient"],
                    "sizes": ["xs", "sm", "md", "lg", "xl"],
                    "disabled": [False, True],
                }
            },
            layout="group",
            example_code="""
Group([
    Button("Filled", variant="filled"),
    Button("Light", variant="light"),
    Button("Outline", variant="outline"),
    Button("Subtle", variant="subtle"),
])
""",
        )

        self.templates["button_states"] = ShowcaseTemplate(
            name="button_states",
            title="Button States",
            description="Interactive button states demonstration.",
            category="Buttons",
            components=["Button"],
            props_overrides={
                "Button": {
                    "loading": [False, True],
                    "disabled": [False, True],
                }
            },
            layout="stack",
            example_code="""
Stack([
    Button("Normal"),
    Button("Loading...", loading=True),
    Button("Disabled", disabled=True),
])
""",
        )

        # Form templates
        self.templates["simple_form"] = ShowcaseTemplate(
            name="simple_form",
            title="Simple Form Layout",
            description="Basic form with inputs and submit button.",
            category="Forms",
            components=["Form", "Input", "Button"],
            props_overrides={
                "Input": {"placeholder": ["Enter name", "Enter email"]},
                "Button": {"children": ["Submit"]},
            },
            layout="form",
            example_code="""
Form([
    Input(placeholder="Enter name"),
    Input(placeholder="Enter email"),
    Button("Submit"),
])
""",
        )

        self.templates["login_form"] = ShowcaseTemplate(
            name="login_form",
            title="Login Form",
            description="Complete login form with validation.",
            category="Forms",
            components=["Card", "Stack", "Input", "Button", "Text"],
            props_overrides={
                "Input": {"type": ["text", "password"]},
                "Button": {"variant": ["filled"]},
            },
            layout="card",
            example_code="""
Card([
    Text("Login", size="xl", weight="bold"),
    Stack([
        Input(placeholder="Username"),
        Input(placeholder="Password", type="password"),
        Button("Login", variant="filled"),
    ], spacing="md"),
])
""",
        )

        # Layout templates
        self.templates["stack_layout"] = ShowcaseTemplate(
            name="stack_layout",
            title="Stack Layout",
            description="Vertical/horizontal stacking of components.",
            category="Layouts",
            components=["Stack", "Button", "Card"],
            props_overrides={},
            layout="stack",
            example_code="""
Stack([
    Button("Top"),
    Card([Text("Middle content")]),
    Button("Bottom"),
], spacing="lg")
""",
        )

        self.templates["group_layout"] = ShowcaseTemplate(
            name="group_layout",
            title="Group Layout",
            description="Horizontal grouping of components.",
            category="Layouts",
            components=["Group", "Button"],
            props_overrides={},
            layout="group",
            example_code="""
Group([
    Button("Left"),
    Button("Middle"),
    Button("Right"),
], spacing="md")
""",
        )

        # Data display templates
        self.templates["data_card"] = ShowcaseTemplate(
            name="data_card",
            title="Data Display Card",
            description="Card for displaying structured data.",
            category="Data Display",
            components=["Card", "Text", "Stack"],
            props_overrides={},
            layout="card",
            example_code="""
Card([
    Text("User Profile", weight="bold"),
    Stack([
        Text("Name: John Doe"),
        Text("Email: john@example.com"),
        Text("Role: Admin"),
    ]),
])
""",
        )

        self.templates["stats_group"] = ShowcaseTemplate(
            name="stats_group",
            title="Statistics Group",
            description="Grouped stats cards.",
            category="Data Display",
            components=["Group", "Card", "Text"],
            props_overrides={},
            layout="group",
            example_code="""
Group([
    Card([Text("Users\\n1,234", weight="bold")]),
    Card([Text("Revenue\\n$12,345", weight="bold")]),
    Card([Text("Growth\\n+15%", weight="bold")]),
], spacing="xl")
""",
        )

    def get_template(self, name: str) -> ShowcaseTemplate:
        """Get a template by name."""
        if name in self.templates:
            return self.templates[name]
        raise ValueError(f"Template '{name}' not found")

    def list_templates(self, category: str = None) -> List[ShowcaseTemplate]:
        """List templates, optionally filtered by category."""
        if category:
            return [t for t in self.templates.values() if t.category == category]
        return list(self.templates.values())

    def render_template(self, template_name: str, provider) -> Any:
        """Render a template using the component renderer."""
        from .component_renderer import ComponentRenderer

        renderer = ComponentRenderer(provider)

        template = self.get_template(template_name)

        # For simplicity, render main layout with first variant
        if template.layout == "stack":
            from polygon_ui import Stack

            children = []
            for comp in template.components:
                props = template.props_overrides.get(comp, {})
                widget = renderer.render(comp, props)
                children.append(widget)
            return Stack(children=children)
        elif template.layout == "group":
            from polygon_ui import Group

            children = []
            for comp in template.components:
                props = template.props_overrides.get(comp, {})
                widget = renderer.render(comp, props)
                children.append(widget)
            return Group(children=children)
        # Add more layout renderers as needed
        else:
            raise NotImplementedError(f"Layout '{template.layout}' not implemented")
