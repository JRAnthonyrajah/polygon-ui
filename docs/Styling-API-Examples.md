# Polygon UI Styling API Examples

This document demonstrates how to use the comprehensive styling system that matches Mantine's capabilities for Qt/PySide applications.

## Overview

The Polygon UI styling system provides:

- **Style Props**: Mantine-style shorthand properties (`c`, `bg`, `w`, `h`, `m`, `p`, etc.)
- **Styles API**: Component-specific styling with `classNames`, `styles`, and `attributes`
- **Theme Integration**: Deep theme integration with CSS variables
- **Responsive Design**: Dictionary-based responsive breakpoints
- **CSS Variable System**: Comprehensive CSS variable generation
- **Qt Native Styling**: QSS generation for Qt applications

## Style Props Examples

### Basic Usage

```python
from polygon_ui.styles import StyleProps
from polygon_ui.theme import Theme

# Create a theme
theme = Theme()

# Create style props with theme integration
props = StyleProps(
    {
        "c": "blue.6",           # Color -> CSS: color: var(--mantine-color-blue-6)
        "bg": "gray.0",          # Background -> CSS: background-color: var(--mantine-color-gray-0)
        "p": "md",             # Padding -> CSS: padding: var(--mantine-spacing-md)
        "m": "xl",             # Margin -> CSS: margin: var(--mantine-spacing-xl)
        "w": 300,              # Width -> CSS: width: 300px
        "h": 200,              # Height -> CSS: height: 200px
        "br": "lg",             # Border radius -> CSS: border-radius: var(--mantine-radius-lg)
        "fw": 600,             # Font weight -> CSS: font-weight: 600
        "ta": "center",          # Text align -> CSS: text-align: center
    },
    theme=theme
)

# Convert to CSS dictionary
css_dict = props.to_css_dict()
# Returns: {
#   'color': 'var(--mantine-color-blue-6)',
#   'background-color': 'var(--mantine-color-gray-0)',
#   'padding': 'var(--mantine-spacing-md)',
#   'margin': 'var(--mantine-spacing-xl)',
#   'width': '300px',
#   'height': '200px',
#   'border-radius': 'var(--mantine-radius-lg)',
#   'font-weight': '600',
#   'text-align': 'center'
# }

# Generate QSS for Qt
qss_string = props.to_qss_string()
# Returns formatted QSS string
```

### Responsive Styling

```python
from polygon_ui.styles import StyleProps

# Responsive style props using dictionary syntax
props = StyleProps({
    "w": {"base": 300, "sm": 400, "lg": 600},
    "p": {"base": "md", "sm": "lg", "xl": "2xl"},
    "c": {"base": "dark", "sm": "primary", "lg": "accent"}
}, theme=theme)

# Get media queries for breakpoints
media_queries = props.get_media_queries()
# Returns:
# {
#     "sm": "@media (min-width: 48em) {\n    width: 400px;\n    padding: var(--mantine-spacing-lg);\n    color: var(--mantine-color-primary-6);\n  }",
#     "lg": "@media (min-width: 75em) {\n    width: 600px;\n    padding: var(--mantine-spacing-xl);\n    color: var(--mantine-color-accent-6);\n  }"
# }
```

### Advanced Shorthand Properties

```python
from polygon_ui.styles import StyleProps

# Comprehensive styling with all available shorthands
props = StyleProps({
    # Colors
    "c": "blue.6",           # color
    "bg": "gray.0",          # background-color
    "bc": "blue.2",          # border-color
    "opc": 0.8,             # opacity

    # Sizing
    "w": "100%",            # width
    "h": "auto",            # height
    "mi": "200px",           # min-width
    "ma": "800px",           # max-width
    "mih": "100px",          # min-height
    "mah": "400px",          # max-height

    # Spacing - margins
    "m": "lg",              # margin (all sides)
    "mt": "md",              # margin-top
    "mb": "sm",              # margin-bottom
    "ml": "xl",              # margin-left
    "mr": "md",              # margin-right
    "mx": "auto",            # margin-left & margin-right
    "my": "sm",              # margin-top & margin-bottom

    # Spacing - padding
    "p": "lg",               # padding (all sides)
    "pt": "md",              # padding-top
    "pb": "sm",              # padding-bottom
    "pl": "xl",              # padding-left
    "pr": "lg",              # padding-right
    "px": "md",              # padding-left & padding-right
    "py": "sm",              # padding-top & padding-bottom

    # Borders
    "bd": "1px solid",        # border
    "bdw": "2px",           # border-width
    "bds": "solid",          # border-style

    # Border radius
    "br": "md",              # border-radius
    "btlr": "lg",           # border-top-left-radius
    "btrr": "md",           # border-top-right-radius

    # Typography
    "fz": "lg",              # font-size
    "fw": "bold",            # font-weight
    "ff": "heading",         # font-family
    "lh": "1.5",             # line-height
    "ls": "0.02em",          # letter-spacing
    "tt": "uppercase",       # text-transform
    "ta": "center",          # text-align
    "td": "underline",       # text-decoration

    # Display and layout
    "d": "flex",             # display
    "fxd": "column",         # flex-direction
    "jc": "center",          # justify-content
    "ai": "center",          # align-items
    "gap": "md",             # gap
    "pos": "relative",       # position
    "z": "100",              # z-index
    "ov": "hidden",          # overflow

    # Effects
    "sh": "lg",              # box-shadow
    "tsh": "md",             # text-shadow
    "curs": "pointer",        # cursor

    # Transform
    "tf": "scale(1.05)",     # transform
    "trs": "all 0.2s ease",    # transition
}, theme=theme)
```

## Styles API Examples

### Basic Styles API Usage

```python
from polygon_ui.styles import StylesAPI
from polygon_ui.theme import Theme

# Create a theme
theme = Theme()

# Create StylesAPI for a Button component
button_styles = StylesAPI(
    component_name="Button",
    theme=theme
)

# Register CSS selectors for component elements
button_styles.register_selector("root", ".mantine-Button-root")
button_styles.register_selector("label", ".mantine-Button-label")
button_styles.register_selector("inner", ".mantine-Button-inner")

# Set styles for different elements
button_styles.set_style("root", {
    "display": "inline-flex",
    "alignItems": "center",
    "cursor": "pointer",
    "border": "1px solid var(--mantine-color-default-border)"
})

button_styles.set_style("label", {
    "color": "var(--mantine-color-white)",
    "fontWeight": "500"
})

# Set CSS class names
button_styles.set_class_name("root", "my-custom-button")
button_styles.set_class_name("label", "button-text")

# Set custom attributes
button_styles.set_attribute("root", "data-testid", "submit-button")
button_styles.set_data_attribute("root", "loading", "true")

# Generate QSS
qss = button_styles.to_qss_string()
```

### Component Configuration Override

```python
# Override component styles in theme
from polygon_ui.theme.theme_utils import ThemeOverride

override = ThemeOverride(
    components={
        "Button": {
            "styles": {
                "root": {
                    "borderRadius": "var(--mantine-radius-xl)",
                    "padding": "12px 24px"
                },
                "label": {
                    "fontSize": "var(--mantine-font-size-lg)"
                }
            },
            "defaultProps": {
                "size": "lg",
                "radius": "lg"
            }
        }
    }
)

# Apply override to theme
from polygon_ui.theme.theme_utils import ThemeMerger
custom_theme = ThemeMerger.apply_override(theme, override)
```

### Theme Integration

```python
from polygon_ui.styles import StylesAPI
from polygon_ui.theme import Theme

# Create StylesAPI with theme
styles_api = StylesAPI(
    styles={
        "root": {
            "backgroundColor": "primary",  # Will be resolved to theme.primary_color
            "padding": "md",             # Will be resolved to theme spacing
            "borderRadius": "lg"         # Will be resolved to theme radius
        }
    },
    theme=theme
)

# Resolve theme variables
resolved_styles = styles_api.resolve_theme_variables({
    "backgroundColor": "primary",
    "padding": "md",
    "borderRadius": "lg",
    "color": "text"
})

# Returns:
# {
#     "backgroundColor": "var(--mantine-primary-color-6)",
#     "padding": "var(--mantine-spacing-md)",
#     "borderRadius": "var(--mantine-radius-lg)",
#     "color": "var(--mantine-color-text)"
# }
```

## Theme Customization Examples

### Creating Custom Themes

```python
from polygon_ui.theme import Theme, ColorScheme
from polygon_ui.theme.colors import Colors
from polygon_ui.theme.spacing import Spacing

# Create custom colors
custom_colors = Colors()
custom_colors.add_custom_color("brand", [
    "#f0f9ff",  # 0
    "#d0ebff",  # 1
    "#a5d8ff",  # 2
    "#74c0fc",  # 3
    "#4dabf7",  # 4
    "#339af0",  # 5
    "#228be6",  # 6
    "#1c7ed6",  # 7
    "#1971c2",  # 8
    "#1864ab",  # 9
])

# Create custom theme
custom_theme = Theme(
    color_scheme=ColorScheme.LIGHT,
    primary_color="brand",
    colors=custom_colors,
    spacing=Spacing(),
    radius={"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24},
    shadows={
        "custom": "0 4px 6px -1px rgba(33, 154, 230, 0.3)"
    },
    breakpoints={"sm": 576, "md": 768, "lg": 1024, "xl": 1280}
)
)
```

### Theme Merging and Inheritance

```python
from polygon_ui.theme.theme_utils import ThemeMerger, ThemeOverride

# Base theme
base_theme = Theme()

# Customizations
customizations = {
    "colors": {
        "accent": ["#f0f9ff", "#d0ebff", "#a5d8ff", "#74c0fc"]
    },
    "spacing": {"xs": 2, "sm": 4, "lg": 24},
    "fontFamily": "Inter, system-ui, sans-serif",
    "components": {
        "Button": {
            "styles": {
                "root": {"fontWeight": 500}
            }
        }
    }
}

# Create inherited theme
inherited_theme = ThemeMerger.create_inherited_theme(
    base_theme=base_theme,
    customizations=customizations
)
```

### Theme Validation

```python
from polygon_ui.theme.theme_utils import ThemeValidator

# Validate theme
errors = ThemeValidator.validate_theme(custom_theme)
if errors:
    print("Theme validation errors:")
    for error in errors:
        print(f"  - {error}")

# Get theme completeness analysis
analysis = ThemeValidator.get_theme_completeness(custom_theme)
print(f"Theme score: {analysis['score']}/{analysis['max_score']}")
print(f"Missing colors: {analysis['missing_colors']}")
print(f"Missing components: {analysis['missing_components']}")

# Get recommendations
print("Recommendations:")
for rec in analysis['recommendations']:
    print(f"  - {rec}")
```

## CSS Variable System Examples

### Generating CSS Variables

```python
from polygon_ui.styles.css_variables import CSSVariableGenerator
from polygon_ui.theme import Theme

# Create theme and generator
theme = Theme()
generator = CSSVariableGenerator(theme)

# Generate all variables
variables = generator.generate_all_variables()

# Generate specific color scheme variables
light_variables = generator.generate_all_variables(ColorScheme.LIGHT)
dark_variables = generator.get_theme.variables(ColorScheme.DARK)

# Generate CSS string
css_string = generator.generate_css_string()

# Get variables by pattern
color_variables = generator.get_variable_by_pattern("--mantine-color-blue")
spacing_variables = generator.get_variable_by_pattern("--mantine-spacing-")
```

### CSS Generation Options

```python
from polygon_ui.styles.theme_css import ThemeCSSGenerator, CSSGenerationOptions

# Create generator with options
options = CSSGenerationOptions(
    include_comments=True,
    minify=False,
    include_media_queries=True,
    include_vendor_prefixes=True,
    optimize_variables=True,
    pretty_print=True
)

generator = ThemeCSSGenerator(theme, options)

# Generate complete theme CSS
theme_css = generator.generate_theme_css()

# Generate component-specific CSS
button_css = generator.generate_component_css("Button")

# Generate QSS for Qt
qss = generator.generate_qss()
```

### CSS Optimization

```python
from polygon_ui.styles.theme_css import CSSOptimizer

# Optimize CSS for production
optimized_css = CSSOptimizer.compress_css(theme_css)

# Extract critical CSS for above-the-fold content
critical_selectors = [".hero", ".navigation", ".call-to-action"]
critical_css = CSSOptimizer.extract_critical_css(theme_css, critical_selectors)

# Optimize with used variables
used_variables = generator.get_used_variables()
optimized_css = CSSOptimizer.optimize_css(theme_css, used_variables)
```

## Complete Usage Examples

### Creating a Styled Component

```python
from polygon_ui.core import PolygonComponent
from polygon_ui.styles import StyleProps, StylesAPI
from polygon_ui.theme import Theme

class StyledButton(PolygonComponent):
    def __init__(self, text="Button", **kwargs):
        super().__init__()
        self.text = text
        self.theme = Theme()
        self.style_props = StyleProps(theme=self.theme, **kwargs.get('style_props', {}))
        self.styles_api = StylesAPI(
            component_name="Button",
            theme=self.theme,
            styles=kwargs.get('styles', {}),
            classNames=kwargs.get('classNames', {}),
            attributes=kwargs.get('attributes', {})
        )

        # Register selectors
        self._setup_selectors()

        # Apply additional styling
        self._apply_styles(**kwargs)

    def _setup_selectors(self):
        """Setup CSS selectors for button elements."""
        self.styles_api.register_selector("root", ".mantine-Button-root")
        self.styles_api.register_selector("label", ".mantine-Button-label")
        self.styles_api.register_selector("inner", ".mantine-Button-inner")

    def _apply_styles(self, **kwargs):
        """Apply styling from kwargs."""
        # Update style props
        if 'style_props' in kwargs:
            self.style_props.update_props(kwargs['style_props'])

        # Update styles API
        if 'styles' in kwargs:
            for selector, styles in kwargs['styles'].items():
                self.styles_api.set_style(selector, styles)

        # Update class names
        if 'classNames' in kwargs:
            for selector, class_name in kwargs['classNames'].items():
                self.styles_api.set_class_name(selector, class_name)

        # Update attributes
        if 'attributes' in kwargs:
            for selector, attrs in kwargs['attributes'].items():
                for attr_name, attr_value in attrs.items():
                    self.styles_api.set_attribute(selector, attr_name, attr_value)

    def get_qss(self) -> str:
        """Get combined QSS for the component."""
        # Get style props QSS
        style_props_qss = self.style_props.to_qss_string()

        # Get Styles API QSS
        styles_api_qss = self.styles_api.to_qss_string()

        # Combine and return
        if style_props_qss and styles_api_qss:
            return f"{style_props_qss}\n\n{styles_api_qss}"
        elif style_props_qss:
            return style_props_qss
        elif styles_api_qss:
            return styles_api_qss
        else:
            return ""

    def render(self):
        """Render the button with current styling."""
        # This would integrate with Qt/PySide widget rendering
        pass
```

### Responsive Layout Example

```python
from polygon_ui.styles import StyleProps
from polygon_ui.theme import Theme

def create_responsive_layout():
    """Create a responsive layout using style props."""
    theme = Theme()

    # Container with responsive width and padding
    container = StyleProps({
        "w": {"base": "100%", "md": "800px", "lg": "1200px"},
        "p": {"base": "md", "md": "lg", "xl": "2xl"},
        "mx": "auto",
        "bg": "background"
    }, theme=theme)

    # Header with responsive font size and spacing
    header = StyleProps({
        "mb": {"base": "lg", "md": "2xl"},
        "fz": {"base": "2rem", "sm": "2.5rem", "lg": "3rem"},
        "fw": "bold",
        "c": "heading",
        "ta": "center"
    }, theme=theme)

    # Navigation with responsive display
    nav = StyleProps({
        "d": {"base": "block", "lg": "flex"},
        "jc": "space-between",
        "ai": "center",
        "p": "sm",
        "bg": "surface"
    }, theme=theme)

    # Content area with responsive columns
    content = StyleProps({
        "d": "flex",
        "fxd": {"base": "column", "md": "row"},
        "gap": "lg"
    }, theme=theme)

    # Sidebar that hides on mobile
    sidebar = StyleProps({
        "w": {"base": "100%", "md": "250px", "lg": "300px"},
        "hiddenFrom": "md",
        "bg": "surface"
    }, theme=theme)

    # Main content that adjusts width
    main = StyleProps({
        "flex": 1,
        "minHeight": "400px",
        "bg": "background"
    }, theme=theme)

    return {
        "container": container,
        "header": header,
        "nav": nav,
        "content": content,
        "sidebar": sidebar,
        "main": main
    }
```

## Summary

The Polygon UI styling system now provides comprehensive Mantine-like capabilities:

✅ **Complete Style Props**: All Mantine shorthand properties with theme integration
✅ **Advanced Styles API**: Component-specific styling with selectors, classes, and attributes
✅ **Deep Theme Integration**: CSS variables, responsive design, and component overrides
✅ **Qt Native Support**: QSS generation for Qt applications
✅ **Responsive Design**: Dictionary-based breakpoints and media queries
✅ **Production Ready**: CSS optimization, minification, and source map generation

This system provides a solid foundation for building Mantine-like UI components for Qt/PySide applications while maintaining Qt's native performance and integration capabilities.
