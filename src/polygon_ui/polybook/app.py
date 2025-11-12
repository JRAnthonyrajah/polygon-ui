"""
PolyBook main application - component development workshop.
"""

import sys
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QListWidget,
    QStackedWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QScrollArea,
    QFrame,
    QCheckBox,
    QSpinBox,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from ..core.provider import PolygonProvider
from ..theme.theme import Theme, ColorScheme
from .component_registry import ComponentRegistry, ComponentInfo
from .story import StoryManager, Story


class PolyBookMainWindow(QMainWindow):
    """Main window for PolyBook application."""

    def __init__(self):
        super().__init__()
        self.polygon_provider = None
        self.component_registry = ComponentRegistry()
        self.story_manager = StoryManager()
        self.current_component = None
        self.current_story = None

        self.init_ui()
        self.init_theme()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("PolyBook - Polygon UI Component Workshop")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Component list
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Center panel - Component preview
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)

        # Right panel - Props and documentation
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Set splitter sizes
        splitter.setSizes([250, 500, 450])

    def create_left_panel(self) -> QWidget:
        """Create the left panel with component list."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Add spacing and margins
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        self.components_header = QLabel("Components")
        # Theme-aware styling will be applied in apply_theme_styling
        self.components_header.setProperty("class", "header")
        self.components_header.setStyleSheet(
            """
            QLabel[class="header"] {
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0px;
                border-bottom: 2px solid #e1e5e9;
                margin-bottom: 8px;
            }
        """
        )
        layout.addWidget(self.components_header)

        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search components...")
        self.search_box.setStyleSheet(
            """
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                outline: none;
            }
        """
        )
        self.search_box.textChanged.connect(self.on_search_components)
        layout.addWidget(self.search_box)

        # Component list
        self.component_list = QListWidget()
        self.component_list.setStyleSheet(
            """
            QListWidget {
                border: 1px solid #e1e5e9;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 12px 16px;
                margin: 2px 0px;
                border-radius: 6px;
                font-size: 14px;
            }
        """
        )
        self.component_list.itemClicked.connect(self.on_component_selected)
        layout.addWidget(self.component_list)

        # Theme controls
        theme_group = QGroupBox("Theme")
        theme_group.setProperty("class", "group-box")
        theme_group.setStyleSheet(
            """
            QGroupBox[class="group-box"] {
                font-size: 14px;
                font-weight: 600;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 8px;
            }
        """
        )
        theme_layout = QVBoxLayout(theme_group)

        # Color scheme toggle
        self.theme_toggle = QPushButton("Toggle Dark/Light")
        self.theme_toggle.setStyleSheet(
            """
            QPushButton {
                padding: 10px 16px;
                border: 2px solid #228be6;
                border-radius: 6px;
                background-color: #228be6;
                color: #ffffff;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1c7ed6;
                border-color: #1c7ed6;
            }
            QPushButton:pressed {
                background-color: #1971c2;
                border-color: #1971c2;
            }
        """
        )
        self.theme_toggle.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_toggle)

        # Primary color selector
        primary_color_layout = QHBoxLayout()
        primary_color_layout.setContentsMargins(0, 8, 0, 0)

        primary_label = QLabel("Primary:")
        primary_label.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                padding-right: 8px;
            }
        """
        )
        primary_color_layout.addWidget(primary_label)

        self.primary_color_combo = QComboBox()
        self.primary_color_combo.setStyleSheet(
            """
            QComboBox {
                padding: 6px 10px;
                border: 2px solid #e1e5e9;
                border-radius: 6px;
                font-size: 13px;
            }
            QComboBox:focus {
                outline: none;
            }
        """
        )
        self.primary_color_combo.addItems(["blue", "red", "green", "yellow", "purple"])
        self.primary_color_combo.currentTextChanged.connect(self.change_primary_color)
        primary_color_layout.addWidget(self.primary_color_combo)
        theme_layout.addLayout(primary_color_layout)

        layout.addWidget(theme_group)

        return panel

    def create_center_panel(self) -> QWidget:
        """Create the center panel with component preview."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Header with component name and story selector
        header_layout = QHBoxLayout()
        self.component_title = QLabel("Select a component")
        # Theme-aware styling will be applied in apply_theme_styling
        self.component_title.setProperty("class", "component-title")
        self.component_title.setStyleSheet(
            """
            QLabel[class="component-title"] {
                font-size: 18px;
                font-weight: 600;
                padding: 0px;
            }
        """
        )
        header_layout.addWidget(self.component_title)

        header_layout.addStretch()

        # Story selector
        story_label = QLabel("Story:")
        story_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                padding-right: 8px;
            }
        """
        )
        header_layout.addWidget(story_label)

        self.story_combo = QComboBox()
        self.story_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #e1e5e9;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:focus {
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid currentColor;
                margin-right: 5px;
            }
        """
        )
        self.story_combo.currentTextChanged.connect(self.on_story_changed)
        header_layout.addWidget(self.story_combo)

        layout.addLayout(header_layout)

        # Component preview area
        preview_group = QGroupBox("Preview")
        preview_group.setProperty("class", "group-box")
        preview_group.setStyleSheet(
            """
            QGroupBox[class="group-box"] {
                font-size: 14px;
                font-weight: 600;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 8px;
            }
        """
        )
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(16, 24, 16, 16)

        self.preview_area = QWidget()
        self.preview_area.setMinimumHeight(400)
        self.preview_area.setStyleSheet(
            """
            QWidget {
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                margin: 8px 0px;
            }
        """
        )
        preview_layout.addWidget(self.preview_area)

        layout.addWidget(preview_group)

        return panel

    def create_right_panel(self) -> QWidget:
        """Create the right panel with props editor and documentation."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Props editor
        props_group = QGroupBox("Props")
        # Theme-aware styling will be applied in apply_theme_styling
        props_group.setProperty("class", "group-box")
        props_group.setStyleSheet(
            """
            QGroupBox[class="group-box"] {
                font-size: 14px;
                font-weight: 600;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                margin-top: 0px;
                padding-top: 8px;
            }
        """
        )
        props_layout = QVBoxLayout(props_group)

        self.props_editor = QWidget()
        self.props_editor_layout = QVBoxLayout(self.props_editor)
        self.props_editor_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.props_editor)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)
        props_layout.addWidget(scroll_area)

        layout.addWidget(props_group)

        # Documentation
        docs_group = QGroupBox("Documentation")
        docs_group.setProperty("class", "group-box")
        docs_group.setStyleSheet(
            """
            QGroupBox[class="group-box"] {
                font-size: 14px;
                font-weight: 600;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                margin-top: 0px;
                padding-top: 8px;
            }
        """
        )
        docs_layout = QVBoxLayout(docs_group)

        self.docs_text = QTextEdit()
        self.docs_text.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #e1e5e9;
                border-radius: 6px;
                font-size: 13px;
                padding: 12px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                outline: none;
            }
        """
        )
        self.docs_text.setReadOnly(True)
        self.docs_text.setMaximumHeight(200)
        docs_layout.addWidget(self.docs_text)

        layout.addWidget(docs_group)

        # Generated code
        code_group = QGroupBox("Generated Code")
        code_group.setProperty("class", "group-box")
        code_group.setStyleSheet(
            """
            QGroupBox[class="group-box"] {
                font-size: 14px;
                font-weight: 600;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                margin-top: 0px;
                padding-top: 8px;
            }
        """
        )
        code_layout = QVBoxLayout(code_group)

        self.code_text = QTextEdit()
        self.code_text.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #e1e5e9;
                border-radius: 6px;
                background-color: #2d3748;
                color: #e2e8f0;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 16px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                outline: none;
            }
        """
        )
        self.code_text.setReadOnly(True)
        code_layout.addWidget(self.code_text)

        layout.addWidget(code_group)

        return panel

    def init_theme(self):
        """Initialize the theme system."""
        # Create theme
        theme = Theme(color_scheme=ColorScheme.LIGHT)

        # Create and initialize PolygonProvider
        self.polygon_provider = PolygonProvider(theme)

        # Apply theme to main window
        self.apply_theme_styling()

        # Add some example components for testing
        self.add_example_components()

        # Populate component list
        self.populate_component_list()

    def apply_theme_styling(self):
        """Apply theme-aware styling to the main window."""
        if not self.polygon_provider:
            return

        theme = self.polygon_provider.theme
        is_dark = theme.color_scheme == ColorScheme.DARK

        # Theme colors
        text_color = theme.get_color("gray", 9 if not is_dark else 0)
        border_color = theme.get_color("gray", 3 if not is_dark else 6)
        bg_color = theme.get_color("gray", 0 if is_dark else 1)
        panel_bg = theme.get_color("gray", 1 if not is_dark else 2)

        # Apply colors directly to specific labels to override any hardcoded styles
        if hasattr(self, "component_title"):
            # Use explicit high-contrast colors based on theme
            if is_dark:
                title_color = "#ffffff"  # White text for dark theme
            else:
                title_color = "#212529"  # Dark text for light theme

            self.component_title.setStyleSheet(
                f"""
                QLabel {{
                    font-size: 18px;
                    font-weight: 600;
                    padding: 0px;
                    color: {title_color} !important;
                    background-color: transparent !important;
                }}
                """
            )

        # Apply theme color to Components header label with forceful styling
        if hasattr(self, "components_header"):
            # Use explicit high-contrast colors based on theme
            if is_dark:
                label_color = "#ffffff"  # White text for dark theme
                border_col = "#495057"  # Lighter border for dark theme
            else:
                label_color = "#212529"  # Dark text for light theme
                border_col = "#dee2e6"  # Standard border for light theme

            self.components_header.setStyleSheet(
                f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: 600;
                    padding: 8px 0px;
                    border-bottom: 2px solid {border_col};
                    margin-bottom: 8px;
                    color: {label_color} !important;
                    background-color: transparent !important;
                }}
                """
            )

        # Set comprehensive theme styling
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {bg_color};
            }}

            QWidget {{
                background-color: transparent;
                color: {text_color};
            }}

            /* Group boxes */
            QGroupBox[class="group-box"] {{
                color: {text_color};
                border-color: {border_color};
                background-color: {panel_bg};
            }}

            QGroupBox[class="group-box"]::title {{
                color: {text_color};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}

            /* Component list */
            QListWidget {{
                background-color: {panel_bg};
                border-color: {border_color};
            }}

            QListWidget::item {{
                color: {text_color};
                background-color: {panel_bg};
            }}

            QListWidget::item:hover {{
                background-color: {theme.get_primary_color()}20;
            }}

            QListWidget::item:selected {{
                background-color: {theme.get_primary_color()};
                color: white;
            }}

            /* Line edits */
            QLineEdit {{
                background-color: {panel_bg};
                color: {text_color};
                border-color: {border_color};
            }}

            /* Combo boxes */
            QComboBox {{
                background-color: {panel_bg};
                color: {text_color};
                border-color: {border_color};
            }}

            QComboBox::drop-down {{
                background-color: {panel_bg};
                border: none;
            }}

            QComboBox::down-arrow {{
                border-top-color: {text_color};
            }}

            /* Text areas */
            QTextEdit {{
                background-color: {panel_bg};
                color: {text_color};
                border-color: {border_color};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {theme.get_primary_color()};
                color: white;
                border-color: {theme.get_primary_color()};
            }}

            QPushButton:hover {{
                background-color: {theme.colors.get_color(theme.primary_color, 7 if not is_dark else 5)};
                border-color: {theme.colors.get_color(theme.primary_color, 7 if not is_dark else 5)};
            }}

            QPushButton:pressed {{
                background-color: {theme.colors.get_color(theme.primary_color, 8 if not is_dark else 4)};
                border-color: {theme.colors.get_color(theme.primary_color, 8 if not is_dark else 4)};
            }}
        """
        )

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.polygon_provider:
            self.polygon_provider.toggle_color_scheme()
            self.apply_theme_styling()  # Reapply theme-aware styling

    def change_primary_color(self, color: str):
        """Change the primary color."""
        if self.polygon_provider:
            self.polygon_provider.update_theme(primary_color=color)
            self.apply_theme_styling()  # Reapply theme-aware styling

    def add_example_components(self):
        """Add some example components to the registry."""
        # This will be expanded as we create real components
        # For now, we'll add placeholder entries

        # Button component example
        self.component_registry.register_component(
            name="Button",
            component_class=None,  # Will be replaced with real button class
            description="A clickable button component",
            category="Input",
            default_props={"text": "Click me", "variant": "filled", "size": "md"},
            examples=[
                {"text": "Primary Button", "variant": "primary", "size": "md"},
                {"text": "Small Outline", "variant": "outline", "size": "sm"},
                {"text": "Large Filled", "variant": "filled", "size": "lg"},
            ],
        )

        # Input component example
        self.component_registry.register_component(
            name="Input",
            component_class=None,  # Will be replaced with real input class
            description="Text input component",
            category="Input",
            default_props={"placeholder": "Enter text...", "size": "md"},
            examples=[
                {"placeholder": "Name", "size": "sm"},
                {"placeholder": "Email address", "size": "md"},
                {"placeholder": "Search...", "size": "lg"},
            ],
        )

    def populate_component_list(self):
        """Populate the component list with registered components."""
        self.component_list.clear()

        components = self.component_registry.list_components()
        for component_name in sorted(components):
            self.component_list.addItem(component_name)

    def on_search_components(self, text: str):
        """Handle component search."""
        if not text:
            self.populate_component_list()
            return

        self.component_list.clear()
        results = self.component_registry.search_components(text)

        for component_info in results:
            self.component_list.addItem(component_info.name)

    def on_component_selected(self, item):
        """Handle component selection."""
        component_name = item.text()
        try:
            component_info = self.component_registry.get_component(component_name)
            self.current_component = component_info

            # Update UI
            self.component_title.setText(component_info.name)

            # Load stories
            self.story_manager.create_default_stories(component_name, component_info)
            self.populate_stories(component_name)

            # Update documentation
            self.update_documentation(component_info)

            # Create props editor
            self.create_props_editor(component_info)

            # Show first story
            stories = self.story_manager.list_stories(component_name)
            if stories:
                self.show_story(component_name, stories[0].name)

        except ValueError as e:
            print(f"Error selecting component: {e}")

    def populate_stories(self, component_name: str):
        """Populate the story combo box."""
        self.story_combo.clear()

        stories = self.story_manager.list_stories(component_name)
        for story in stories:
            self.story_combo.addItem(story.name)

    def on_story_changed(self, story_name: str):
        """Handle story selection change."""
        if self.current_component and story_name:
            self.show_story(self.current_component.name, story_name)

    def show_story(self, component_name: str, story_name: str):
        """Show a specific story."""
        if not self.current_component:
            return

        story = self.story_manager.get_story(component_name, story_name)
        if not story:
            return

        self.current_story = story

        # Update props editor with story props
        self.update_props_editor(story.props)

        # Render component (placeholder for now)
        self.render_component_placeholder(story)

        # Update generated code
        self.update_generated_code(component_name, story.props)

    def update_documentation(self, component_info: ComponentInfo):
        """Update the documentation panel."""
        doc_text = f"""
## {component_info.name}

**Category:** {component_info.category}

{component_info.description}

### Default Props
{self.format_dict(component_info.default_props)}

### Examples
{component_info.name} has {len(component_info.examples)} example configurations.
        """.strip()

        self.docs_text.setPlainText(doc_text)

    def create_props_editor(self, component_info: ComponentInfo):
        """Create props editor for the component."""
        # Clear existing props editor
        for i in reversed(range(self.props_editor_layout.count())):
            child = self.props_editor_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # Add props based on component_info
        if component_info.name == "Button":
            self.add_text_prop("text", "Click me")
            self.add_combo_prop(
                "variant", ["filled", "outline", "light", "subtle"], "filled"
            )
            self.add_combo_prop("size", ["xs", "sm", "md", "lg", "xl"], "md")
        elif component_info.name == "Input":
            self.add_text_prop("placeholder", "Enter text...")
            self.add_combo_prop("size", ["xs", "sm", "md", "lg", "xl"], "md")

    def update_props_editor(self, props: Dict[str, Any]):
        """Update props editor with current story props."""
        # This would update the prop values in the editor
        # Implementation depends on the specific widgets created
        pass

    def add_text_prop(self, name: str, default_value: str):
        """Add a text property editor."""
        layout = QHBoxLayout()

        label = QLabel(f"{name}:")
        line_edit = QLineEdit(default_value)
        line_edit.setObjectName(f"prop_{name}")

        layout.addWidget(label)
        layout.addWidget(line_edit)

        self.props_editor_layout.addLayout(layout)

    def add_combo_prop(self, name: str, options: list, default_value: str):
        """Add a combo property editor."""
        layout = QHBoxLayout()

        label = QLabel(f"{name}:")
        combo = QComboBox()
        combo.addItems(options)
        combo.setCurrentText(default_value)
        combo.setObjectName(f"prop_{name}")

        layout.addWidget(label)
        layout.addWidget(combo)

        self.props_editor_layout.addLayout(layout)

    def render_component_placeholder(self, story: Story):
        """Render a placeholder for the component."""
        # Clear preview area
        for i in reversed(self.preview_area.layout().count()):
            child = self.preview_area.layout().itemAt(i).widget()
            if child:
                child.setParent(None)

        # Create placeholder widget
        props_text = self.format_dict(story.props) if story.props else "No custom props"
        placeholder = QLabel(
            f"🧩 {self.current_component.name}\n\n📋 Configuration:\n{props_text}\n\n📱 Component will render here"
        )
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 32px 16px;
                font-size: 14px;
                line-height: 1.6;
            }
        """
        )

        self.preview_area.layout().addWidget(placeholder)

    def update_generated_code(self, component_name: str, props: Dict[str, Any]):
        """Update the generated code panel."""
        code = f"""
from polygon_ui.components import {component_name}

# Create {component_name.lower()} with props
{component_name.lower()}_widget = {component_name}(
{self.format_props_for_code(props)}
)

# Add to layout
layout.addWidget({component_name.lower()}_widget)
        """.strip()

        self.code_text.setPlainText(code)

    def format_dict(self, d: Dict[str, Any]) -> str:
        """Format a dictionary for display."""
        if not d:
            return "None"

        lines = ["{"]
        for key, value in d.items():
            lines.append(f"  {key}: {repr(value)},")
        lines.append("}")
        return "\n".join(lines)

    def format_props_for_code(self, props: Dict[str, Any]) -> str:
        """Format props for code generation."""
        if not props:
            return ""

        lines = []
        for key, value in props.items():
            lines.append(f"    {key}={repr(value)},")
        return "\n".join(lines)

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        if self.polygon_provider:
            self.polygon_provider.toggle_color_scheme()

    def change_primary_color(self, color: str):
        """Change the primary color."""
        if self.polygon_provider:
            self.polygon_provider.update_theme(primary_color=color)


class PolyBookApp:
    """Main PolyBook application class."""

    def __init__(self):
        self.app = None
        self.window = None

    def run(self, args=None):
        """Run the PolyBook application."""
        if args is None:
            args = sys.argv

        # Create QApplication
        self.app = QApplication(args)
        self.app.setApplicationName("PolyBook")
        self.app.setApplicationVersion("0.1.0")

        # Create and show main window
        self.window = PolyBookMainWindow()
        self.window.show()

        # Run the application
        return self.app.exec()

    def get_component_registry(self) -> ComponentRegistry:
        """Get the component registry."""
        if self.window:
            return self.window.component_registry
        return ComponentRegistry()

    def get_story_manager(self) -> StoryManager:
        """Get the story manager."""
        if self.window:
            return self.window.story_manager
        return StoryManager()


def run_polybook():
    """Convenience function to run PolyBook."""
    app = PolyBookApp()
    return app.run()


if __name__ == "__main__":
    run_polybook()
