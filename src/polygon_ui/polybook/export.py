"""Component export functionality for PolyBook.

Allows exporting components as code snippets, themes, or configurations.
"""

from typing import Dict, Any
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QMimeData, QUrl

from .app import PolyBookApp
from .registry import ComponentRegistry


class Exporter:
    """
    Handles exporting components from PolyBook.
    """

    @staticmethod
    def export_code_snippet(
        component_name: str, props: Dict[str, Any], theme: Dict[str, Any]
    ) -> str:
        """
        Generate and export Python code snippet for a component.

        Args:
            component_name (str): Name of the component.
            props (Dict): Component properties.
            theme (Dict): Current theme configuration.

        Returns:
            str: Generated code as string.
        """
        # Example generation (extend for full components)
        code = f"""from polygon_ui import {component_name}

# Props: {props}
# Theme: {theme}

component = {component_name}("Example", **{props})
"""
        return code

    @staticmethod
    def export_theme_config(theme: Dict[str, Any]) -> str:
        """
        Export current theme as JSON/TOML config.

        Args:
            theme (Dict): Theme dictionary.

        Returns:
            str: Theme config string.
        """
        import json

        return json.dumps(theme, indent=2)

    @staticmethod
    def save_to_file(app: PolyBookApp, content: str, file_type: str = "py") -> bool:
        """
        Save content to file via dialog.

        Args:
            app (PolyBookApp): PolyBook instance.
            content (str): Content to save.
            file_type (str): File extension (py, json, toml).

        Returns:
            bool: Success status.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            app,
            "Export File",
            f"export.{file_type}",
            f"{file_type.upper()} Files (*.{file_type})",
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(content)
                QMessageBox.information(
                    app, "Export Success", f"Exported to {file_path}"
                )
                return True
            except Exception as e:
                QMessageBox.warning(app, "Export Failed", str(e))
        return False

    @staticmethod
    def copy_to_clipboard(app: PolyBookApp, content: str):
        """
        Copy content to system clipboard.
        """
        clipboard = app.clipboard()
        mime_data = QMimeData()
        mime_data.setText(content)
        clipboard.setMimeData(mime_data)
        QMessageBox.information(app, "Copied", "Content copied to clipboard!")
