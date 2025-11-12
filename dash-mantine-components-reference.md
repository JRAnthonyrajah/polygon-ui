# Dash Mantine Components - Comprehensive Reference Guide

> **Dash Mantine Components (DMC)** is a powerful component library for Plotly Dash that provides 100+ customizable components based on the React Mantine library. It offers consistent styling, theming, full light/dark mode support, and accessibility out of the box.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Core Concepts](#core-concepts)
3. [Basic Usage](#basic-usage)
4. [Component Categories](#component-categories)
5. [Key Components](#key-components)
6. [Styling & Theming](#styling--theming)
7. [Migration Guide](#migration-guide)
8. [Advanced Features](#advanced-features)
9. [Best Practices](#best-practices)
10. [Community & Support](#community--support)

---

## Installation & Setup

### Installation

```bash
# Using pip
pip install dash-mantine-components

# Using poetry
poetry add dash-mantine-components
```

### Requirements

| Component | Version Requirement |
|-----------|-------------------|
| Dash | `>=2.0.0` |
| React | `18.2.0` (for Dash 2.x) |
| Python | `>=3.8` |

### Basic Setup

```python
import dash
from dash import Dash
import dash_mantine_components as dmc

# Required for Dash 2.x
dash._dash_renderer._set_react_version("18.2.0")

app = Dash(__name__)

# Always wrap your layout with MantineProvider
app.layout = dmc.MantineProvider(
    dmc.Alert(
        "Welcome to Dash Mantine Components!",
        title="Hello!",
        color="violet",
    )
)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Core Concepts

### MantineProvider

The `MantineProvider` is **required** for all DMC applications. It handles:

- Global styles and themes
- Light/dark mode support
- Default props across the app
- Custom theme registration

```python
app.layout = dmc.MantineProvider(
    # Your app content here
    theme={
        "colorScheme": "light",  # or "dark"
        "primaryColor": "violet",
    }
)
```

### Component Philosophy

- **Accessibility First**: All components include ARIA attributes and keyboard navigation
- **Customizable**: Extensive theming and styling options
- **Type Safety**: Full TypeScript support in the underlying React components
- **Performance Optimized**: Efficient rendering and minimal re-renders
- **Responsive**: Built-in responsive design patterns

---

## Basic Usage

### Essential Components

#### Alert Component
```python
dmc.Alert(
    "This is an alert message",
    title="Important Notice",
    color="blue",
    variant="light"
)
```

#### Button Component
```python
dmc.Button(
    "Click me",
    color="violet",
    variant="filled",
    size="md",
    leftSection=dmc.Icon(icon="radix-icons:rocket")
)
```

#### Container and Layout
```python
dmc.Container(
    [
        dmc.Title("Welcome to DMC", order=1),
        dmc.Text("Build beautiful Dash apps with ease"),
    ],
    size="md",  # responsive container
    px="md"     # horizontal padding
)
```

---

## Component Categories

Based on the documentation analysis, DMC includes components in these categories:

### 1. **Layout & Structure**
- `Container`, `Grid`, `SimpleGrid`, `Group`, `Stack`
- `AppShell`, `Header`, `Navbar`, `Aside`, `Footer`
- `Divider`, `Space`

### 2. **Feedback & Overlays**
- `Modal`, `Drawer`, `Popover`, `Tooltip`
- `Alert`, `Notification`, `LoadingOverlay`
- `Affix`, `Progress`

### 3. **Forms & Input**
- `TextInput`, `NumberInput`, `Textarea`
- `Select`, `MultiSelect`, `TagsInput`
- `Checkbox`, `Radio`, `Switch`
- `DatePicker`, `DatePickerInput`, `DateTimePicker`

### 4. **Data Display**
- `Table`, `Card`, `Accordion`, `Tabs`
- `List`, `Badge`, `Avatar`, `Image`
- `CodeHighlight`, `RichTextEditor`

### 5. **Navigation**
- `Anchor`, `Button`, `ActionIcon`, `Breadcrumbs`
- `Pagination`, `Stepper`

### 6. **Charts & Visualization**
- Integration with `dash-ag-grid`
- Chart components (when using DMC Charts)

---

## Key Components

### Modal Component

The Modal component is perfect for dialogs and overlays:

```python
import dash
from dash import Input, Output, State, html
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = dmc.MantineProvider([
    dmc.Button("Open Modal", id="modal-button"),
    dmc.Modal(
        id="modal",
        title="Example Modal",
        size="md",  # sm, md, lg, xl
        centered=True,
        children=[
            dmc.Text("This is a modal dialog"),
            dmc.Group([
                dmc.Button("Cancel", variant="outline", id="cancel-btn"),
                dmc.Button("Save", id="save-btn"),
            ], mt="md")
        ]
    )
])

@app.callback(
    Output("modal", "opened"),
    Input("modal-button", "n_clicks"),
    State("modal", "opened"),
    prevent_initial_call=True
)
def toggle_modal(n_clicks, opened):
    return not opened

@app.callback(
    Output("modal", "opened", allow_duplicate=True),
    Input("cancel-btn", "n_clicks"),
    State("modal", "opened"),
    prevent_initial_call=True
)
def close_modal(n_clicks, opened):
    return False
```

#### Modal Stack for Multiple Modals

```python
dmc.ModalStack([
    dmc.ManagedModal(
        id="modal-1",
        title="First Modal",
        children=[dmc.Text("First modal content")]
    ),
    dmc.ManagedModal(
        id="modal-2",
        title="Second Modal",
        children=[dmc.Text("Second modal content")]
    )
])
```

### Table Component

Create responsive, styled tables:

```python
dmc.Table(
    [
        dmc.TableThead([
            dmc.TableTr([
                dmc.TableTh("Name"),
                dmc.TableTh("Email"),
                dmc.TableTh("Role")
            ])
        ]),
        dmc.TableTbody([
            dmc.TableTr([
                dmc.TableTd("John Doe"),
                dmc.TableTd("john@example.com"),
                dmc.TableTd(dmc.Badge("Admin", color="blue"))
            ]),
            dmc.TableTr([
                dmc.TableTd("Jane Smith"),
                dmc.TableTd("jane@example.com"),
                dmc.TableTd(dmc.Badge("User", color="gray"))
            ])
        ])
    ],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True
)
```

### Date and Time Components

#### DatePickerInput
```python
dmc.DatePickerInput(
    label="Select Date",
    placeholder="Pick a date",
    value="2024-01-01",
    clearable=True,
    minDate="2024-01-01",
    maxDate="2024-12-31"
)
```

#### DateTimePicker
```python
dmc.DateTimePicker(
    label="Select Date and Time",
    placeholder="Pick date and time",
    withSeconds=True,
    timePickerProps={
        "withDropdown": True,
        "minutesStep": 5
    }
)
```

---

## Styling & Theming

### Theme Configuration

```python
app.layout = dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
        "primaryColor": "violet",
        "fontFamily": "Inter, sans-serif",
        "components": {
            "Button": {
                "defaultProps": {
                    "variant": "filled",
                    "radius": "md"
                },
                "styles": {
                    "root": {
                        "fontWeight": 500
                    }
                }
            },
            "Card": {
                "defaultProps": {
                    "shadow": "sm",
                    "withBorder": True
                }
            }
        }
    },
    # Your app content
)
```

### Style Props

DMC components support intuitive style props:

```python
dmc.Container(
    # Margin & Padding
    m="xl",           # margin: var(--mantine-spacing-xl)
    mt="md",          # margin-top: var(--mantine-spacing-md)
    px="lg",          # padding-left & right

    # Sizing
    w="100%",         # width: 100%
    h=200,            # height: 200px
    miw=100,          # min-width: 100px
    mah="50vh",       # max-height: 50vh

    # Colors
    c="violet.6",     # color: var(--mantine-color-violet-6)
    bg="gray.0",      # background: var(--mantine-color-gray-0)

    # Typography
    fz="lg",          # font-size: var(--mantine-font-size-lg)
    fw=500,           # font-weight: 500
    lh=1.5,           # line-height: 1.5

    # Display
    display="flex",
    flex=1,

    # Position
    pos="relative",
    top=10,

    # Border
    bd="1px solid",
    borderColor="gray.3",
    borderRadius="md",

    # Responsive
    hiddenFrom="sm",  # hide on screens smaller than sm
    visibleFrom="lg", # show only on lg and larger
)
```

### CSS-in-JS with Styles API

```python
dmc.Button(
    "Custom Button",
    styles={
        "root": {
            "background": "linear-gradient(45deg, #7c3aed, #ec4899)",
            "border": "none",
            "&:hover": {
                "background": "linear-gradient(45deg, #6d28d9, #db2777)",
            }
        }
    }
)
```

---

## Migration Guide

### Version Compatibility

| DMC Version | Release Date | Mantine Version | Required Dash Version |
|-------------|--------------|-----------------|---------------------|
| **2.4.0** | Nov 2025 | 8.3.6 | `dash>=2.0.0` |
| **2.3.0** | Sep 2025 | 8.3.1 | `dash>=2.0.0` |
| **2.2.0** | Aug 2025 | 8.2.5 | `dash>=2.0.0` |
| **2.1.0** | Jul 2025 | 8.1.2 | `dash>=2.0.0` |
| **2.0.0** | Jun 2025 | 8.0.2 | `dash>=2.0.0` |
| **1.0.0** | Mar 2025 | 7.17.0 | `dash>=2.0.0` |

### Key Breaking Changes (1.x → 2.x)

#### 1. Switch Component
```python
# Old style (no indicator) - disable withThumbIndicator
dmc.MantineProvider(
    theme={
        "components": {
            "Switch": {
                "defaultProps": {
                    "withThumbIndicator": False,
                },
            },
        },
    }
)
```

#### 2. DateTimePicker Changes
```python
# ❌ 1.x - timeInputProps removed
dmc.DateTimePicker(timeInputProps={...})

# ✅ 2.x - use timePickerProps instead
dmc.DateTimePicker(timePickerProps={...})
```

#### 3. Carousel Updates
```python
# ❌ 1.x - embla options as props
dmc.Carousel(loop=True, dragFree=True)

# ✅ 2.x - use emblaOptions
dmc.Carousel({"loop": True, "dragFree": True})
```

#### 4. Notification System
```python
# ❌ 1.x - deprecated approach
dmc.NotificationProvider()
dmc.Notification(...)

# ✅ 2.x - new approach
dmc.NotificationContainer()
# Use notification.show() in callbacks
```

---

## Advanced Features

### Responsive Design

```python
dmc.Grid([
    dmc.GridCol(
        dmc.Text("Column 1"),
        span=4,  # 4 columns on all screens
    ),
    dmc.GridCol(
        dmc.Text("Column 2"),
        span={"base": 12, "sm": 6, "lg": 4},  # responsive
    ),
    dmc.GridCol(
        dmc.Text("Column 3"),
        span={"base": 12, "sm": 6, "lg": 4},
    ),
], gutter="lg")
```

### Compound Components

Many DMC components support compound patterns:

```python
dmc.AppShell([
    dmc.AppShellHeader(
        dmc.Group(dmc.Text("My App"), justify="space-between", px="md", h=60)
    ),
    dmc.AppShellNavbar(
        dmc.NavLink("Home", href="/"),
        width={"base": 200, "sm": 300},
        breakpoint="sm"
    ),
    dmc.AppShellMain(
        dmc.Container("Main content here")
    )
], padding="md")
```

### Client-Side Callbacks

```python
# In your JavaScript clientside callback
function showNotification() {
    dmc.showNotification({
        message: 'Success!',
        color: 'green',
        autoClose: 5000
    });
}
```

### Custom Components

```python
def CustomCard(title, content, **kwargs):
    return dmc.Card(
        [
            dmc.CardSection(
                dmc.Text(title, size="lg", fw=500, p="md")
            ),
            dmc.Box(content, p="md")
        ],
        withBorder=True,
        shadow="sm",
        **kwargs
    )
```

---

## Best Practices

### 1. **Always Use MantineProvider**
```python
# ✅ Good
app.layout = dmc.MantineProvider(your_layout)

# ❌ Bad - missing provider
app.layout = your_layout
```

### 2. **Use Semantic Components**
```python
# ✅ Good - semantic HTML structure
dmc.Container([
    dmc.Title("Page Title", order=1),
    dmc.Text("Page content..."),
])

# ❌ Avoid - generic divs
dmc.Box([dmc.Text("content")])
```

### 3. **Leverage Style Props**
```python
# ✅ Good - using style props
dmc.Button("Click", m="md", p="xs", radius="md")

# ❌ Avoid - inline styles when style props available
dmc.Button("Click", style={"margin": "var(--mantine-spacing-md)"})
```

### 4. **Responsive Design**
```python
# ✅ Good - responsive breakpoints
dmc.GridCol(span={"base": 12, "sm": 6, "lg": 4})

# ✅ Good - visibility props
dmc.Text("Desktop only", hiddenFrom="sm")
dmc.Text("Mobile only", visibleFrom="sm")
```

### 5. **Component Composition**
```python
# ✅ Good - reusable components
def DataTable(data):
    return dmc.Table([
        dmc.TableThead([
            dmc.TableTr([
                dmc.TableTh(col) for col in data[0].keys()
            ])
        ]),
        dmc.TableTbody([
            dmc.TableTr([
                dmc.TableTd(str(value)) for value in row.values()
            ]) for row in data
        ])
    ], striped=True, highlightOnHover=True)
```

### 6. **Performance Considerations**
```python
# ✅ Good - memoize expensive components
from functools import lru_cache

@lru_cache(maxsize=128)
def get_large_list_data():
    # expensive data loading
    return expensive_operation()

# ✅ Good - use loading states for slow operations
@app.callback(Output("output", "children"), Input("button", "n_clicks"))
def update_data(n_clicks):
    if n_clicks:
        return dmc.LoadingOverlay(visible=True, children="Loading...")
    # actual data loading
```

---

## Common Patterns & Solutions

### 1. **Form Handling**
```python
dmc.Container([
    dmc.TextInput(
        id="name-input",
        label="Name",
        required=True,
        error="Name is required" if not name else None
    ),
    dmc.NumberInput(
        id="age-input",
        label="Age",
        min=18,
        max=100
    ),
    dmc.Button("Submit", id="submit-btn")
])
```

### 2. **Data Tables with Actions**
```python
dmc.Table([
    dmc.TableThead([headers]),
    dmc.TableTbody([
        dmc.TableTr([
            dmc.TableTd(item[col]) for col in columns
        ] + [
            dmc.TableTd(
                dmc.Group([
                    dmc.ActionIcon(
                        icon="radix-icons:pencil-1",
                        onClick=f"edit_item('{item['id']}')"
                    ),
                    dmc.ActionIcon(
                        icon="radix-icons:trash-2",
                        color="red",
                        onClick=f"delete_item('{item['id']}')"
                    )
                ])
            )
        ]) for item in data
    ])
])
```

### 3. **Navigation Patterns**
```python
dmc.AppShell([
    dmc.AppShellHeader([
        dmc.Group([
            dmc.Text("My App", size="lg", fw=500),
            dmc.ThemeSwitch()
        ], justify="space-between", h="100%", px="md")
    ]),
    dmc.AppShellNavbar([
        dmc.NavLink("Dashboard", href="/", active=True),
        dmc.NavLink("Users", href="/users"),
        dmc.NavLink("Settings", href="/settings"),
    ], width=250),
    dmc.AppShellMain([
        dmc.Container(page_content)
    ])
])
```

---

## Community & Support

### Getting Help
- **Documentation**: https://dash-mantine-components.com
- **GitHub Issues**: https://github.com/snehilvj/dash-mantine-components/issues
- **Discord Community**: https://discord.gg/KuJkh4Pyq5
- **Dash Forum**: https://community.plotly.com/

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Resources
- **GitHub Repository**: https://github.com/snehilvj/dash-mantine-components
- **Examples**: https://github.com/snehilvj/dmc-docs
- **Mantine Docs**: https://mantine.dev/
- **Plotly Dash Docs**: https://dash.plotly.com/

---

## Quick Reference

### Common Props

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | Component ID for Dash callbacks |
| `className` | string | CSS class name |
| `style` | dict | Inline styles |
| `children` | list/nodes | Child components |
| `hiddenFrom` | string | Hide on screens smaller than breakpoint |
| `visibleFrom` | string | Show only on screens larger than breakpoint |

### Style Props Cheat Sheet

| Category | Props | Examples |
|----------|-------|----------|
| **Margin** | `m`, `mt`, `mr`, `mb`, `ml`, `mx`, `my` | `m="md"`, `mt=20` |
| **Padding** | `p`, `pt`, `pr`, `pb`, `pl`, `px`, `py` | `p="lg"`, `px=10` |
| **Size** | `w`, `h`, `minw`, `minh`, `maxw`, `maxh` | `w="100%"`, `h=200` |
| **Color** | `c`, `bg`, `color` | `c="violet.6"`, `bg="gray.0"` |
| **Typography** | `fz`, `fw`, `lh`, `fs` | `fz="lg"`, `fw=500` |
| **Border** | `bd`, `bdrs`, `bdc` | `bd="1px solid"`, `bdrs="md"` |

### Color Scale

DMC uses Mantine's color scale with values 0-9:
- `0` - Lightest shade (almost white)
- `6` - Base color (default)
- `9` - Darkest shade (almost black)

```python
# Examples
dmc.Button("Primary", color="blue.6")     # Base blue
dmc.Button("Light", color="blue.2")       # Light blue
dmc.Button("Dark", color="blue.8")        # Dark blue
```

---

## Conclusion

Dash Mantine Components provides a comprehensive suite of components for building beautiful, accessible, and responsive Dash applications. With its tight integration with Mantine's design system and extensive customization options, it's an excellent choice for production-ready Dash applications.

### Key Takeaways
1. **Always wrap your app in MantineProvider**
2. **Use semantic components for better accessibility**
3. **Leverage style props for consistent styling**
4. **Follow responsive design patterns**
5. **Use compound components for complex layouts**
6. **Utilize the extensive theming system**
7. **Stay updated with migration guides for major versions**

Happy coding with Dash Mantine Components! 🚀

---

*This reference guide was compiled from the official documentation repository and is intended for educational and reference purposes. For the most up-to-date information, please visit https://dash-mantine-components.com*
