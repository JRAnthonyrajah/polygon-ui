def apply_widget_styles(self):
        """Apply theme-aware styles to specific widgets."""
        if not self.polygon_provider:
            return
        theme = self.polygon_provider.theme
        is_dark = theme.color_scheme == ColorScheme.DARK
        text_color = theme.get_color("gray", 9 if not is_dark else 0)
        border_color = theme.get_color("gray", 3 if not is_dark else 6)
        panel_bg = theme.get_color("gray", 0 if is_dark else 1)
        code_bg = theme.get_color("gray", 8 if not is_dark else 1)
        code_color = theme.get_color("gray", 1 if not is_dark else 8)

        # Components header
        self.components_header.setStyleSheet(
            f\"\"\"
            QLabel[class="header"] {{
                font-size: 16px;
                font-weight: 600;
                padding: 8px 0px;
                border-bottom: 2px solid {border_color};
                margin-bottom: 8px;
                color: {text_color};
                background-color: transparent;
            }}
            \"\"\"
        )

        # Search box
        self.search_box.setStyleSheet(
            f\"\"\"
            QLineEdit {{
                padding: 10px 12px;
                border: 2px solid {border_color};
                border-radius: 8px;
                font-size: 14px;
                background-color: {panel_bg};
                color: {text_color};
            }}
            QLineEdit:focus {{
                outline: none;
                border-color: {theme.get_primary_color()};
            }}
            \"\"\"
        )

        # Component list
        self.component_list.setStyleSheet(
            f\"\"\"
            QListWidget {{
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 4px;
                background-color: {panel_bg};
                color: {text_color};
            }}
            QListWidget::item {{
                padding: 12px 16px;
                margin: 2px 0px;
                border-radius: 6px;
                font-size: 14px;
                color: {text_color};
            }}
            QListWidget::item:hover {{
                background-color: {theme.get_primary_color(6)}20;
            }}
            \"\"\"
        )

        # Primary color combo
        self.primary_color_combo.setStyleSheet(
            f\"\"\"
            QComboBox {{
                padding: 6px 10px;
                border: 2px solid {border_color};
                border-radius: 6px;
                font-size: 13px;
                background-color: {panel_bg};
                color: {text_color};
            }}
            QComboBox:focus {{
                outline: none;
                border-color: {theme.get_primary_color()};
            }}
            \"\"\"
        )

        # Story combo
        self.story_combo.setStyleSheet(
            f\"\"\"
            QComboBox {{
                padding: 8px 12px;
                border: 2px solid {border_color};
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
                background-color: {panel_bg};
                color: {text_color};
            }}
            QComboBox:focus {{
                outline: none;
                border-color: {theme.get_primary_color()};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
                background-color: {panel_bg};
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {text_color};
                margin-right: 5px;
            }}
            \"\"\"
        )

        # Preview area
        self.preview_area.setStyleSheet(
            f\"\"\"
            QWidget {{
                border: 2px dashed {border_color};
                border-radius: 8px;
                margin: 8px 0px;
                background-color: {panel_bg};
            }}
            \"\"\"
        )

        # Docs text
        self.docs_text.setStyleSheet(
            f\"\"\"
            QTextEdit {{
                border: 1px solid {border_color};
                border-radius: 6px;
                font-size: 13px;
                padding: 12px;
                line-height: 1.5;
                background-color: {panel_bg};
                color: {text_color};
            }}
            QTextEdit:focus {{
                outline: none;
                border-color: {theme.get_primary_color()};
            }}
            \"\"\"
        )

        # Code text
        self.code_text.setStyleSheet(
            f\"\"\"
            QTextEdit {{
                border: 1px solid {border_color};
                border-radius: 6px;
                background-color: {code_bg};
                color: {code_color};
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 16px;
                line-height: 1.4;
            }}
            QTextEdit:focus {{
                outline: none;
                border-color: {theme.get_primary_color()};
            }}
            \"\"\"
        )

        # Theme toggle (specific hover/pressed shades)
        primary = theme.get_primary_color()
        primary_hover = theme.colors.get_color(theme.primary_color, 7 if not is_dark else 5)
        primary_pressed = theme.colors.get_color(theme.primary_color, 8 if not is_dark else 4)
        self.theme_toggle.setStyleSheet(
            f\"\"\"
            QPushButton[class="primary"] {{
                padding: 10px 16px;
                border: 2px solid {primary};
                border-radius: 6px;
                background-color: {primary};
                color: {theme.get_color('white', 0)};
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton[class="primary"]:hover {{
                background-color: {primary_hover};
                border-color: {primary_hover};
            }}
            QPushButton[class="primary"]:pressed {{
                background-color: {primary_pressed};
                border-color: {primary_pressed};
            }}
            \"\"\"
        )
