# Dash Mantine Components - Complete Technical Reference

## Table of Contents

1. [Overview](#overview)
2. [Installation & Quick Start](#installation--quick-start)
3. [Component Categories](#component-categories)
   - [Forms & Inputs](#forms--inputs)
   - [Layout Components](#layout-components)
   - [Data Display](#data-display-components)
   - [Feedback & Overlays](#feedback--overlays)
   - [Charts & Visualization](#charts--visualization)
   - [Advanced Components](#advanced-components)
   - [Utility Components](#utility-components)
4. [Advanced Features](#advanced-features)
   - [Functions as Props](#functions-as-props)
   - [Rich Text Editor](#rich-text-editor)
   - [Performance Optimization](#performance-optimization)
5. [Migration Guide](#migration-guide)
6. [Styling & Theming](#styling--theming)
7. [Integration Examples](#integration-examples)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

---

## Overview

**Dash Mantine Components** is an extensive (90+) Dash components library based on [Mantine](https://mantine.dev/) React Components Library. It simplifies creating high-quality dashboards with well-designed components out of the box.

**Key Features:**
- **90+ Components**: Comprehensive component library covering all UI needs
- **Modern Design**: Based on Mantine's React component library with consistent styling
- **Full Theming**: Light/dark mode support with customizable themes
- **Accessibility**: Built-in accessibility features
- **Dash Integration**: Seamless integration with Plotly Dash callbacks
- **Performance**: Async loading and bundle optimization

**Request Flow:** `Client → Semantic Proxy (4001) → LiteLLM (4000) → AI Providers`

## Installation & Quick Start

### Installation

```bash
pip install dash-mantine-components
```

### Basic Setup

```python
import dash
from dash import Dash, Input, Output, callback, html
import dash_mantine_components as dmc

app = Dash()

app.layout = dmc.MantineProvider([
    dmc.DatePickerInput(
        id="date-picker",
        label="Start Date",
        description="You can also provide a description",
        minDate='2022-08-05',
        value=None,
        w=200
    ),
    dmc.Space(h=10),
    dmc.Text(id="selected-date"),
])

@callback(Output("selected-date", "children"), Input("date-picker", "value"))
def update_output(d):
    prefix = "You have selected: "
    if d:
        return prefix + d
    else:
        return no_update

if __name__ == "__main__":
    app.run_server(debug=True)
```

---

## Component Categories

## Forms & Input Components

### TextInput

**Complete Prop List:**
- `id` (string, required): Unique ID for Dash callbacks
- `value` (string | number): Current input value
- `type` (string, default='text'): Input type ('text', 'email', 'url', 'password', 'search', 'tel', 'number')
- `placeholder` (string): Placeholder text
- `label` (string): Label above input
- `description` (string): Helper text below input
- `error` (bool): Show error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `size` (string): Component size ('xs', 'sm', 'md', 'lg', 'xl')
- `radius` (string | number): Border radius
- `maxLength` (number): Maximum character count
- `readOnly` (bool): Read-only mode
- `leftSection` (Dash component): Element before input
- `rightSection` (Dash component): Element after input
- `inputContainer` (dict): Container props
- `styles` (dict): Style overrides
- `className` (string): CSS classes
- `debounce` (bool | number | 'true'): Debounce input
- `__component` (string): Internal component identifier

**Basic Example:**
```python
dmc.TextInput(
    id="email-input",
    placeholder="Enter your email",
    label="Email Address",
    required=True,
    error=False,
    rightSection=dmc.ActionIcon(dmc.IconX(), onClick=clear_email)
)
```

### Advanced Patterns:**

**Dynamic Validation:**
```python
@callback([Output("email", "error"), Output("email", "description")], Input("email", "value"))
def validate_email(value):
    if value and "@" not re.match(r'^[\w\.-]+@[\w\.-]+\.[\w\.]{2,}$', value):
        return True, "Please enter a valid email"
    return False, ""
```

**Auto-complete Integration:**
```python
@callback(Output("suggestions", "data"), Input("search", "value"))
def get_suggestions(value):
    return [
        {"label": f"Match: {value}", "value": value},
        {"label": f"Similar: {value}", "value": f"{value}2"}
    ]
```

**Custom Styling:**
```python
# Using style props
dmc.TextInput(
    style={"borderColor": "#e74c3c"},
    sx={(theme) => ({
        "&:hover": {
            borderColor: theme.colors.blue[6]
        }
    })
)
```

### PasswordInput

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (string): Current password
- `placeholder` (string): Placeholder text
- `label` (string): Input label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `size` (string): Component size
- `radius` (string | number): Border radius
- `toggleTabIndex` (number): Tab index for visibility toggle
- `inputContainer` (dict): Container props
- `styles` (dict): Style overrides

**Example:**
```python
dmc.PasswordInput(
    id="password",
    placeholder="Enter password",
    label="Password",
    required=True,
    visibilityToggle=True,
    toggleTabIndex=0
)
```

### NumberInput

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (number | string): Current value
- `placeholder` (string): Placeholder text
- `label` (string): Input label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `min` (number): Minimum value
- `max` (number): Maximum value
- `step` (number): Increment step
- `precision` (number): Decimal places
- `decimalSeparator` (string): Decimal separator
- `hideControls` (bool): Hide increment/decrement buttons
- `styles` (dict): Style overrides

**Example:**
```python
dmc.NumberInput(
    id="age",
    label="Age",
    min=0,
    max=120,
    step=1,
    precision=0,
    hideControls=False
)
```

### Select

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (string | number | list): Selected value(s)
- `data` (list of dicts): Options with label/value
- `placeholder` (string): Placeholder text
- `label` (string): Input label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `searchable` (bool): Enable search functionality
- `clearable` (bool): Show clear button
- `nothingFound` (string): Text when no options found
- `maxDropdownHeight` (number): Maximum dropdown height
- `filter` (function): Custom filter function
- `limit` (number): Limit searchable options
- `creatable` (bool): Allow creating new options
- `getCreateLabel` (string): Create label text
- `withCheckIcon` (bool): Show check icons
- `styles` (dict): Style overrides

**Example:**
```python
options = [
    {"label": "Red", "value": "red"},
    {"label": "Blue", "value": "blue"},
    {"label": "Green", "value": "green"}
]

dmc.Select(
    id="color-select",
    data=options,
    value="red",
    placeholder="Choose color",
    searchable=True,
    clearable=True
)
```

### MultiSelect

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (list): Selected values
- `data` (list of dicts): Options with label/value
- `placeholder` (string): Placeholder text
- `label` (string): Input label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `searchable` (bool): Enable search
- `clearable` (bool): Show clear all button
- `nothingFound` (string): No results text
- `maxDropdownHeight` (number): Maximum dropdown height
- `filter` (function): Custom filter function
- `limit` (number): Limit searchable options
- `creatable` (bool): Allow creating new options
- `getCreateLabel` (string): Create label text
- `maxSelectedValues` (number): Maximum selections
- `styles` (dict): Style overrides

**Example:**
```python
dmc.MultiSelect(
    id="tags-select",
    data=options,
    value=["red", "blue"],
    placeholder="Select multiple colors",
    searchable=True,
    maxSelectedValues=3
)
```

### Slider

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (number | list): Single value or range [min, max]
- `min` (number): Minimum value
- `max` (number): Maximum value
- `step` (number): Step increment
- `marks` (list | bool): Show marks or custom marks list
- `label` (string | function): Label or formatting function
- `labelAlwaysOn` (bool): Always show label
- `showLabelOnHover` (bool): Show label only on hover
- `color` (string): Color scheme
- `size` (string): Component size
- `thumbSize` (number): Thumb size in pixels
- `trackWidth` (number): Track width
- `radius` (string | number): Border radius
- `styles` (dict): Style overrides
- `container` (dict): Container props
- `sx` (dict): Advanced styling

**Range Slider Example:**
```python
dmc.Slider(
    id="price-range",
    value=[100, 500],
    min=0,
    max=1000,
    step=10,
    marks=[
        {"value": 0, "label": "$0"},
        {"value": 500, "label": "$500"},
        {"value": 1000, "label": "$1000"}
    ],
    label="Price Range"
)

# Custom label function
dmc.Slider(
    id="confidence-slider",
    value=75,
    label=lambda v: f"{v}% confidence"
)
```

### Switch

**Complete Prop List:**
- `id` (string, required): Component ID
- `checked` (bool): Switch state
- `label` (string): Switch label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable switch
- `size` (string): Component size
- `radius` (string | number): Border radius
- `color` (string): Color when on
- `offLabel` (string): Off text
- `onLabel` (string): On text
- `thumbIcon` (Dash component): Custom thumb icon
- `styles` (dict): Style overrides
- `sx` (dict): Advanced styling

**Example:**
```python
dmc.Switch(
    id="notifications",
    checked=False,
    label="Enable notifications"
)

# Switch group
dmc.Switch(
    id="feature-toggle",
    label="Dark mode",
    color="dark"
)
```

### Checkbox

**Complete Prop List:**
- `id` (string, required): Component ID
- `checked` (bool): Checkbox state
- `label` (string): Checkbox label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable checkbox
- `required` (bool): Show required indicator
- `indeterminate` (bool): Indeterminate state
- `color` (string): Color when checked
- `size` (string): Component size
- `radius` (string | number): Border radius
- `icon` (Dash component): Custom checkbox icon
- `styles` (dict): Style overrides
- `sx` (dict): Advanced styling

**Checkbox Group Example:**
```python
dmc.Checkbox.Group(
    id="preferences",
    value=[],
    label="Select preferences",
    children=[
        dmc.Checkbox(value="email", label="Email notifications"),
        dmc.Checkbox(value="sms", label="SMS notifications")
    ]
)
```

### DateInput / DatePickerInput

**DatePickerInput Props:**
- `id` (string, required): Component ID
- `value` (string | date): Selected date (ISO string or date object)
- `placeholder` (string): Placeholder text
- `label` (string): Input label
- `description` (string): Helper text
- `error` (bool): Error state
- `disabled` (bool): Disable input
- `required` (bool): Show required indicator
- `minDate` (string | date): Minimum selectable date
- `maxDate` (string | date): Maximum selectable date
- `clearable` (bool): Show clear button
- `dropdownType` (string): 'modal' or 'popover'
- `styles` (dict): Style overrides

**Basic Example:**
```python
from datetime import date

dmc.DatePickerInput(
    id="date-picker",
    value=date(2024, 1, 15),
    label="Select Date",
    placeholder="Pick a date",
    minDate=date(2023, 1, 1),
    clearable=True
)
```

### RichTextEditor

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (string): Editor content (HTML)
- `placeholder` (string): Placeholder text
- `editable` (bool): Enable/disable editing
- `focus` (bool): Auto-focus editor
- `toolbar` (list): Toolbar configuration
- `styles` (dict): Style overrides

**Basic Example:**
```python
dmc.RichTextEditor(
    id="editor",
    placeholder="Start typing...",
    value="<p>Hello <strong>world</strong></p>",
    editable=True,
    toolbar=[
        'bold', 'italic', 'underline',
        'h1', 'h2', 'h3',
        'bulletList', 'numberedList',
        'link', 'image', 'table'
    ]
)
```

**Client-Side Access:**
```javascript
// In assets/custom.js
function getEditorContent(editorId) {
    const editor = dash_mantine_components.getEditor(editorId);
    if (editor) {
        return editor.getHTML();
    }
    return "";
}
```

**Migration Notes:**
- v2.3.0+ uses Tiptap v3
- Code highlighting enabled with CodeBlockLowlight
- `focus` and `editable` props added in v2.4.0

---

## Layout Components

### Container

**Complete Prop List:**
- `fluid` (bool, default=False): Full width without max-width
- `size` (string | number | tuple): Container size or responsive breakpoints
- `px` (string | number): Horizontal padding
- `py` (string | number): Vertical padding
- `children` (Dash component): Content to wrap
- `styles` (dict): Style overrides

**Responsive Example:**
```python
# Fixed width container
dmc.Container(
    size="md",  # 75% max-width
    px="xl",
    children=[...]
)

# Responsive container
dmc.Container(
    size={"base": "sm", "md": 50, "lg": 70, "xl": 90},
    children=[...]
)

# Fluid container
dmc.Container(
    fluid=True,
    children=[...]
)
```

### Grid and Col

**Grid Props:**
- `gutter` (string | number): Spacing between columns
- `justify` (string): Horizontal alignment
- `align` (string): Vertical alignment
- `cols` (number | tuple): Columns per row

**Col Props:**
- `span` (number | tuple): Column width (1-12)
- `offset` (number | tuple): Column offset
- `children` (Dash component): Column content

**Basic Grid Example:**
```python
dmc.Grid(
    gutter="lg",
    children=[
        dmc.Col(span=12, md=6, children="Left Column"),
        dmc.Col(span=12, md=6, children="Right Column")
    ]
)
```

**Responsive Grid:**
```python
dmc.Grid(
    children=[
        dmc.Col(span=12, xs=12, md=6, lg=4, children="Mobile 12, Desktop 4"),
        dmc.Col(span=12, xs=6, md=6, lg=6, children="Mobile 6, Desktop 6")
    ]
)
```

### SimpleGrid

**Props:**
- `cols` (number): Number of columns
- `spacing` (string | number): Item spacing
- `breakpoints` (dict): Responsive column counts

**Example:**
```python
dmc.SimpleGrid(
    cols=3,
    spacing="md",
    breakpoints={
        "xs": 1,
        "sm": 2,
        "lg": 4
    },
    children=[
        dmc.Card("Item 1"),
        dmc.Card("Item 2"),
        dmc.Card("Item 3")
    ]
)
```

### Stack

**Props:**
- `gap` (string | number): Spacing between items
- `direction` (string): 'row' or 'column'
- `align` (string): Cross-axis alignment
- `justify` (string): Main-axis alignment
- `children` (list): Stacked items

**Vertical Stack:**
```python
dmc.Stack(
    gap="md",
    direction="column",
    children=[
        dmc.TextInput(label="Field 1"),
        dmc.TextInput(label="Field 2"),
        dmc.Button("Submit")
    ]
)
```

**Horizontal Stack:**
```python
dmc.Stack(
    gap="sm",
    direction="row",
    justify="space-between",
    children=[
        dmc.Button("Cancel"),
        dmc.Button("Submit", color="blue")
    ]
)
```

### Flex

**Props:**
- `direction` (string): Main axis direction
- `wrap` (bool): Flex wrap behavior
- `gap` (string | number): Spacing
- `justify` (string): Main-axis alignment
- `align` (string): Cross-axis alignment
- `children` (list): Flex items

**Example:**
```python
dmc.Flex(
    gap="lg",
    justify="space-between",
    align="center",
    children=[
        dmc.Text("Left"),
        dmc.Button("Center"),
        dmc.Text("Right")
    ]
)
```

### Center

**Props:**
- `inline` (bool): Inline centering
- `horizontal` (string | number | tuple): Horizontal spacing
- `vertical` (string | number | tuple): Vertical spacing
- `children` (Dash component): Content to center

**Example:**
```python
dmc.Center(
    inline=True,
    children=dmc.Button("Centered Button")
)

dmc.Center(
    h=300,
    children=[
        dmc.Title("Centered Title"),
        dmc.Button("Centered Button")
    ]
)
```

### Box

**Props:**
- `p`, `px`, `py`, `m`, `mx`, `my`, `mt`, `mb`, `ml`, `mr` (string | number): Spacing utilities
- `component` (string): HTML tag
- `children` (Dash component): Content
- `sx` (dict | function): Emotion styles
- `styles` (dict): Style overrides

**Utility Examples:**
```python
# Using spacing utilities
dmc.Box(p="md")  # Padding all sides
dmc.Box(px="xl")  # Horizontal padding only
dmc.Box(my="lg")  # Margin

# Custom HTML tag
dmc.Box(
    component="section",
    p="lg",
    children=[...content...]
)
```

**Advanced Styling:**
```python
dmc.Box(
    sx={(theme) => ({
        backgroundColor: theme.colors.blue[0],
        borderRadius: theme.radius.md
    })},
    children=[...content...]
)
```

### Paper

**Props:**
- `shadow` (string): Shadow level
- `p`, `px`, `py` (string | number): Padding
- `radius` (string | number): Border radius
- `withBorder` (bool): Add border
- `children` (Dash component): Content

**Example:**
```python
dmc.Paper(
    shadow="md",
    p="lg",
    radius="md",
    withBorder=True,
    children=[
        dmc.Title("Card Title", order=3),
        dmc.Text("Card content here")
    ]
)
```

### Card

**Props:**
- `shadow` (string): Shadow level
- `p`, `px`, `py` (string | number): Padding
- `radius` (string | number): Border radius
- `withBorder` (bool): Add border
- `children` (CardSection | Dash component): Content sections
- `styles` (dict): Style overrides

**Card with Sections:**
```python
dmc.Card(
    shadow="sm",
    children=[
        dmc.CardSection(
            dmc.Title("Header", order=3),
            inheritPadding=False,
            p="md"
        ),
        dmc.CardSection(
            dmc.Text("Main content"),
            inheritPadding=False,
            p="md"
        ),
        dmc.CardSection(
            dmc.Button("Action", variant="outline"),
            inheritPadding=False,
            p="md"
        )
    ]
)
```

---

## Data Display Components

### Table

**Complete Prop List:**
- `data` (list of dicts): Table data
- `columns` (list of dicts): Column definitions
- `striped` (bool): Striped rows
- `highlightOnHover` (bool): Hover highlighting
- `withBorder` (bool): Table border
- `withColumnBorders` (bool): Column borders
- `horizontalSpacing` (string): Cell horizontal spacing
- `verticalSpacing` (string): Cell vertical spacing
- `styles` (dict): Style overrides

**Basic Example:**
```python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'CCities', 'Tokyo'],
    'Salary': [75000, 82000, 65000]
})

dmc.Table(
    striped=True,
    highlightOnHover=True,
    withBorder=True,
    data=df.to_dict('records'),
    columns=[
        {'name': 'Name', 'accessor': 'Name'},
        {'name': 'Age', 'accessor': 'Age'},
        {'name': 'City', 'accessor': 'City'},
        {'name': 'Salary', 'accessor': 'Salary',
         'format': '${value:,.2f}'}
    ]
)
```

**Dynamic Table with Pagination:**
```python
@callback(
    Output("table", "data"),
    Input("page", "value"),
    [State("table", "data")],
    prevent_initial_call=True
)
def update_table_data(page, stored_data):
    start = (page - 1) * 50
    return stored_data[start:start + 50]

app.layout = dmc.Container([
    dmc.Table(id="data-table"),
    dmc.Pagination(id="pagination", total=10),
    dcc.Store(id="table-data", data=large_dataset)
])
```

### Text

**Complete Prop List:**
- `children` (string | Dash component): Text content
- `size` (string | number): Font size
- `weight` (number | string): Font weight
- `color` (string): Text color
- `align` (string): Text alignment
- `lineClamp` (number): Limit lines
- `underline` (bool): Underline text
- `transform` (string): Text transformation
- `gradient` (bool): Gradient text
- `variant` (string): Text variant
- `styles` (dict): Style overrides
- `sx` (dict): Advanced styling

**Examples:**
```python
# Basic text
dmc.Text("Hello World")

# With styling
dmc.Text(
    size="xl",
    weight=700,
    color="blue",
    align="center"
)

# With advanced features
dmc.Text(
    lineClamp=3,
    underline=True,
    gradient={from: "blue", to: "cyan"},
    transform="uppercase",
    sx={(theme) => ({
        color: theme.fn.primaryColor
    })
)
```

### Title

**Complete Prop List:**
- `children` (string): Title text
- `order` (number): Heading level (1-6)
- `size` (string | number): Title size
- `weight` (number | string): Font weight
- `color` (string): Title color
- `align` (string): Text alignment
- `styles` (dict): Style overrides

**Examples:**
```python
dmc.Title("Main Title", order=1)
dmc.Title("Section Title", order=3)
dmc.Title("Subsection Title", order=4)
dmc.Title("Large", order=1, size="h1")
dmc.Title("Medium", order=2, size="h2")
dmc.Title("Small", order=4, size="h6")
```

### Code and CodeHighlight

**Code Component (Inline):**
- `children` (string): Code text
- `color` (string): Code color
- `block` (bool): Block display
- `copyable` (bool): Enable copy functionality
- `styles` (dict): Style overrides

**CodeHighlight Component:**
- `children` (string): Code to highlight
- `language` (string): Programming language
- `theme` (dict): Highlight theme
- `withCopyButton` (bool): Add copy button
- `copyTooltip` (string): Copy button tooltip
- `styles` (dict): Style overrides

**Examples:**
```python
# Inline code
dmc.Code("console.log('Hello World')", color="red"))

# Code block
dmc.CodeHighlight(
    language="python",
    children="def hello_world():\n    print('Hello World')\n",
    withCopyButton=True
)
```

### Badge

**Complete Prop List:**
- `children` (string): Badge text
- `color` (string): Color scheme
- `variant` (string): 'light', 'filled', 'outline', 'dot', 'white'
- `size` (string): Badge size
- `leftSection`, `rightSection` (Dash component): Side sections
- `fullWidth` (bool): Full width badge
- `styles` (dict): Style overrides

**Examples:**
```python
dmc.Badge("New", color="green", variant="filled")
dmc.Badge("42", color="blue", leftSection=dmc.IconUser())
dmc.Badge("Status", variant="outline")
```

### Avatar

**Complete Prop List:**
- `src` (string): Image URL
- `alt` (string): Alt text
- `size` (string | number): Avatar size
- `color` (string): Background color for initials
- `radius` (string | number): Border radius
- `children` (string): Initials fallback
- `styles` (dict): Style overrides

**Examples:**
```python
# Image avatar
dmc.Avatar(
    src="https://example.com/avatar.jpg",
    alt="User Avatar",
    size="lg",
    radius="xl"
)

# Initials avatar
dmc.Avatar("JD", color="indigo", size="md")

# Avatar group
dmc.AvatarGroup(
    spacing="sm",
    total=5,
    children=[
        dmc.Avatar(src="user1.jpg", alt="User 1"),
        dmc.Avatar("AB", color="blue"),
        dmc.Avatar("CD", color="red")
    ]
)
```

### Progress

**Complete Prop List:**
- `value` (number | string): Progress value (0-100)
- `size` (string): Progress bar size
- `color` (string): Progress color
- `radius` (string | number): Border radius
- `showValue` (bool): Show percentage
- `label` (string): Custom label
- `labelPosition` (string): Label position
- `striped` (bool): Striped progress bar
- `animated` (bool): Animation
- `styles` (dict): Style overrides

**Examples:**
```python
dmc.Progress(
    value=75,
    size="md",
    color="green",
    showValue=True,
    label="Upload Progress"
)

# Circular progress
dmc.RingProgress(
    value=85,
    size=120,
    thickness=12,
    color="blue",
    showValue=True
)

# Striped progress
dmc.Progress(
    value=60,
    striped=True,
    color="orange"
)
```

### RingProgress

**Complete Prop List:**
- `value` (number): Progress value (0-100)
- `size` (number): Diameter in pixels
- `thickness` (number): Ring thickness
- `color` (string): Ring color
- `showValue` (bool): Show center value
- `label` (Dash component): Center content
- `styles` (dict): Style overrides

**Example:**
```python
dmc.RingProgress(
    value=85,
    size=120,
    thickness=8,
    color="blue",
    showValue=True
)
```

---

## Feedback & Overlay Components

### Modal

**Complete Prop List:**
- `id` (string): Component ID
- `opened` (bool): Modal visibility
- `onClose` (function): Close callback
- `title` (string): Modal title
- `size` (string): Modal size
- `centered` (bool): Center modal
- `overlayProps` (dict): Overlay styling
- `contentProps` (dict): Content area styling
- `closeOnClickOutside` (bool): Click outside to close
- `closeOnEscape` (bool): Escape key to close
- `withCloseButton` (bool): Show close button
- `transitionProps` (dict): Transition settings
- `zIndex` (number): Z-index
- `styles` (dict): Style overrides

**Basic Modal:**
```python
dmc.Modal(
    opened=True,
    title="Confirmation",
    size="md",
    centered=True,
    children=[
        dmc.Text("Are you sure?"),
        dmc.Group(
            position="right",
            mt="md",
            children=[
                dmc.Button("Cancel", variant="outline"),
                dmc.Button("Confirm", color="red")
            ]
        )
    ]
)
```

**Controlled Modal:**
```python
@callback(Output("modal", "opened"), Input("open-modal", "n_clicks"))
def open_modal(n_clicks):
    return True

@callback(
    Output("modal", "opened"),
    Input("close-modal", "n_clicks"),
    [State("modal", "opened")]
)
def close_modal(n_clicks, modal_opened):
    if n_clicks > 0 and modal_opened:
        return False
    return modal_opened
```

### Drawer

**Complete Prop List:**
- `id` (string): Component ID
- `opened` (bool): Drawer visibility
- `onClose` (function): Close callback
- `title` (string): Drawer title
- `position` (string): Position (left, right, top, bottom)
- `size` (string | number): Drawer size
- `overlayProps` (dict): Overlay styling
- `contentProps` (dict): Content area styling
- `closeOnClickOutside` (bool): Click outside to close
- `closeOnEscape` (bool): Escape key to close
- `withCloseButton` (bool): Show close button
- `styles` (dict): Style overrides

**Position Examples:**
```python
# Left drawer
dmc.Drawer(
    opened=True,
    position="left",
    title="Navigation",
    children=[...nav_links...]
)

# Right drawer
dmc.Drawer(
    opened=True,
    position="right",
    size="400",
    title="Details Panel",
    children=[...form_fields...]
)

# Top/bottom drawer
dmc.Drawer(
    position="bottom",
    size="md",
    title="Quick Actions",
    children=[...quick_actions...]
)
```

### Alert

**Complete Prop List:**
- `children` (string | Dash component): Alert content
- `title` (string): Alert title
- `color` (string): Alert color ('red', 'green', 'blue', 'yellow', 'orange')
- `variant` (string): Alert variant
- `icon` (Dash component): Alert icon
- `withCloseButton` (bool): Show close button
- `hide` (bool): Hide alert
- `autoClose` (number): Auto-close timeout
- `styles` (dict): Style overrides

**Color Examples:**
```python
dmc.Alert("Success message", color="green", title="Success!")
dmc.Alert("Warning message", color="yellow", title="Warning", icon=dmc.IconWarning())
dmc.Alert("Error message", color="red", title="Error", icon=dmc.IconX())
```

**Dismissible Alert:**
```python
@callback(
    Output("alert", "hidden"),
    Input("close-alert", "n_clicks")
)
def close_alert(n_clicks):
    return True

dmc.Alert(
    id="alert",
    hidden=False,
    title="Information",
    color="blue",
    children="Message content",
    withCloseButton=True,
    onClose=lambda: close_alert
)
```

### Notification

**Complete Prop List:**
- `id` (string): Unique identifier
- `title` (string): Notification title
- `message` (message): Notification message
- `color` (string): Notification color
- `autoClose` (number): Auto-close timeout
- `disallowClose` (bool): Disable manual close
- `loading` (bool): Show loading state
- `onClose` (function): Close callback
- `styles` (dict): Style overrides

**Example:**
```python
# Simple notification
dmc.Notification(
    title="Success",
    message="Operation completed successfully",
    color="green",
    autoClose=3000
)

# Advanced usage with NotificationContainer
app.layout = dmc.NotificationContainer()

# Show notification via callback
def show_notification():
    return dmc.Notification(
        title="Data Updated",
        message="Changes saved successfully",
        color="green"
    )
```

### Tooltip

**Complete Prop List:**
- `children` (string | Dash component): Trigger element
- `label` (string | Dash component): Tooltip content
- `position` (string): Tooltip position
- `withArrow` (bool): Show arrow
- `opened` (bool): Controlled visibility
- `delay` (number): Open delay (ms)
- `closeDelay` (number): Close delay (ms)
- `wrap` (bool): Wrap behavior)
- `inline` (bool): Inline tooltip
- `styles` (dict): Style overrides
- `events` (dict): Event handlers

**Basic Usage:**
```python
dmc.Tooltip(
    label="Click to copy",
    children=dmc.Button("Hover me")
)

# Controlled tooltip
dmc.Tooltip(
    label="Dynamic tooltip",
    children=dmc.Button("Dynamic"),
    opened=tooltip_open
)
```

**Position Examples:**
```python
dmc.Tooltip(
    position="bottom",
    position="end",
    withArrow=True
)

# With custom styling
dmc.Tooltip(
    styles={"root": {"backgroundColor": "black", "color": "white"}}
)
```

### Popover

**Complete Prop List:**
- `id` (string): Component ID
- `opened` (bool): Popover visibility
- `target` (string | Dash component): Target element
- `position` (string): Popover position
- `width` (number): Popover width
- `height` (number): Popover height
- `shadow` (string): Shadow level
- `withArrow` (bool): Show arrow
- `offset` (number): Popover offset
- `styles` (dict): Style overrides
- `zIndex` (number): Z-index

**Example:**
```python
dmc.Popover(
    width=300,
    position="bottom",
    withArrow=True,
    children=[
        dmc.PopoverTarget(
            dmc.Button("Click me")
        ),
        dmc.PopoverDropdown(dmc.Text("Dropdown content"))
    ]
)
```

### LoadingOverlay

**Complete Prop List:**
- `visible` (bool): Overlay visibility
- `loaderProps` (dict): Loader component props
- `overlayProps` (dict): Overlay styling
- `zIndex` (number): Z-index
- `styles` (dict): Style overrides
- `transitionProps` (dict): Transition settings

**Example:**
```python
dmc.LoadingOverlay(
    visible=True,
    loaderProps={"color": "blue"},
    overlayProps={"blur": 2}
)

# With custom content
dmc.LoadingOverlay(
    visible=loading,
    children=[dmc.Text("Loading...")],
    overlayProps={"blur": 4}
)
```

### Skeleton

**Complete Prop List:**
- `visible` (bool): Skeleton visibility
- `height` (string | number): Skeleton height
- `width` (string | number): Skeleton width
- `circle` (bool): Circular skeleton
- `animate` (bool): Animation
- `styles` (dict): Style overrides

**Examples:**
```python
# Text skeleton
dmc.Skeleton(
    height=20,
    width="100%",
    animate=True
)

# Image skeleton
dmc.Skeleton(
    height=40,
    width=40,
    circle=True
)

# Card skeleton
dmc.Paper(
    p="lg",
    children=[
        dmc.Skeleton(height=200)
    ]
)
```

---

## Charts & Visualization

### Chart Integration Overview

DMC integrates with **Recharts** for data visualization. All chart components use `ResponsiveContainer` by default and include proper callbacks.

### Chart Components

#### LineChart

**Complete Prop List:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides
- **Child Components**:
  - `LineChart.XAxis`
  - `LineChart.YAxis`
  - `LineChart.CartesianGrid`
  - `LineChart.Line`
  - `LineChart.Tooltip`
  - `LineChart.Legend`

**Example:**
```python
data = [
    {"month": "Jan", "sales": 1000, "profit": 200},
    {"month": "Feb", "sales": 1200, "profit": 300},
    {"month": "Mar", "sales": 900, "profit": 150}
]

dmc.LineChart(
    height=300,
    data=data,
    children=[
        dmc.LineChart.XAxis(dataKey="month"),
        dmc.LineChart.YAxis(),
        dmc.LineChart.CartesianGrid(),
        dmc.LineChart.Line(
            type="monotone",
            dataKey="sales",
            stroke="#8884d8"
        ),
        dmc.LineChart.Tooltip(),
        dmc.LineChart.Legend()
    ]
)
```

#### BarChart

**Complete Prop List:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides
- **Child Components**:
  - `BarChart.XAxis`
  - `BarChart.YAxis`
  - `BarChart.CartesianGrid`
  - `BarChart.Bar`
  - `BarChart.Tooltip`
  - `BarChart.Legend`

**Example:**
```python
dmc.BarChart(
    height=300,
    data=data,
    children=[
        dmc.BarChart.XAxis(dataKey="month"),
        dmc.BarChart.YAxis(),
        dmc.BarChart.CartesianGrid(),
        dmc.BarChart.Bar(
            dataKey="sales",
            fill="#82ca9d"
        ),
        dmc.BarChart.Tooltip(),
        dmc.BarChart.Legend()
    ]
)
```

#### AreaChart

**Complete Prop List:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (_number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides
- **Child Components**:
  - `AreaChart.XAxis`
  - `AreaChart.YAxis`
  - `AreaChart.CartesianGrid`
  - `AreaChart.Area`
  - `AreaChart.Tooltip`
  - `AreaChart.Legend`

**Example:**
```python
dmc.AreaChart(
    height=300,
    data=data,
    children=[
        dmc.AreaChart.XAxis(dataKey="month"),
        dmc.AreaChart.YAxis(),
        dmc.AreaChart.CartesianGrid(),
        dmc.AreaChart.Area(
            type="monotone",
            dataKey="sales",
            stroke="#8884d8",
            fill="#8884d8",
            fillOpacity=0.3
        ),
        dmc.AreaChart.Tooltip(),
        dmc.AreaChart.Legend()
    ]
)
```

#### PieChart

**Complete Prop List:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides
- **Child Components**:
  - `PieChart.Label` (optional): Label configuration
  - `PieChart.Pie`: Main pie configuration
  - `PieChart.Cell`: Cell configuration
  - `PieChart.Tooltip`: Tooltip configuration
  - `PieChart.Legend`: Legend configuration

**Example:**
```python
data = [
    {"name": "Category A", "value": 400},
    {"name": "Category B", "value": 300},
    {"name": "Category C", "value": 300}
]

dmc.PieChart(
    height=300,
    data=data,
    children=[
        dmc.PieChart.Label(position="outside"),
        dmc.PieChart.Pie(
            dataKey="value",
            nameKey="name",
            cx="50%",
            cy="50%",
            outerRadius=80,
            fill="#8884d8"
        ),
        dmc.PieChart.Cell(),
        dmc.PieChart.Tooltip(),
        dmc.PieChart.Legend()
    ]
)
```

#### ScatterChart

**Complete Prop List:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides
- **Child Components**:
  - `ScatterChart.XAxis`
  - `ScatterChart.YAxis`
  - `ScatterChart.ZAxis` (optional): Z-axis for 3D scatter
  - `ScatterChart.CartesianGrid`
  - `ScatterChart.Scatter`
  - `ScatterChart.Tooltip`
  - `ScatterChart.Legend`

**Example:**
```python
data = [
    {"x": 100, "y": 200, "z": 10},
    {"x": 120, "y": 150, "z": 20},
    {"x": 170, "y": 300, "z": 30}
]

dmc.ScatterChart(
    height=400,
    width=600,
    data=data,
    children=[
        dmc.ScatterChart.XAxis(dataKey="x"),
        dmc.ScatterChart.YAxis(dataKey="y"),
        dmc.ScatterChart.ZAxis(dataKey="z"),
        dmc.ScatterChart.CartesianGrid(),
        dmc.ScatterChart.Scatter(
            name="Data Points",
            dataKey="y",
            cx="50%",
            cy="50%",
            fill="#8884d8"
        )
    ]
)
```

### Composite Chart

**Use Multiple Chart Types:**
```python
# Combining chart types
dmc.CompositeChart(
    height=400,
    data=data,
    children=[
        dmc.AreaChart(
            name="Revenue",
            dataKey="month"
        ),
        dmc.BarChart(
            name="Profit",
            dataKey="month"
        )
    ]
)
```

### Chart Data Format

**Standard Format:**
```python
data = [
    {"month": "Jan", "sales": 1000, "profit": 200},
    {"month": "Feb", "sales": 1200, "profit": 300}
]
```

**Advanced Data Formatting:**
```python
# Using value formatter
dmc.LineChart(
    valueFormatter={(value) => f"${value:,.2f}"},
    dataKey="amount"
)

# Using tooltip props for detailed tooltips
dmc.BarChart(
    tooltipProps={
        "value": (value, payload) => f"{payload:,2f}"
    }
)
```

### Chart Styling

**Color Customization:**
```python
dmc.LineChart(
    data=data,
    children=[
        dmc.LineChart.Line(
            stroke="#8884d8"
        )
    ],
    styles={
        "root": {
            "&:hover": {
                "filter": "brightness(120%)"
            }
        }
    }
)
```

**Dark Mode Support:**
```python
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=[...chart...]
)
```

**Integration Patterns:**
```python
# Real-time chart updates
@callback(
    Output("chart", "data"),
    Input("refresh", "n_clicks")
)
def update_chart(refresh_n_clicks):
    return get_latest_data()
```

# Interactive charts
dmc.LineChart(
    height=300,
    children=[
        dmc.LineChart.Line(
            dataKey="sales",
            onClick=handle_click
        )
    ]
)

def handle_click(click_data):
    # Process chart click data
    return click_data
```

---

## Advanced Components

### Accordion

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (string | list): Opened panel(s)
- `multiple` (bool): Allow multiple panels open
- `chevronPosition` (string): Chevron position
- `variant` (string): Component variant
- `styles` (dict): Style overrides

**Example:**
```python
dmc.Accordion(
    value="panel-1",
    multiple=False,
    chevronPosition="right",
    children=[
        dmc.AccordionItem(
            value="panel-1",
            icon=dmc.IconChartBar(),
            label="Panel 1",
            children=[
                dmc.Text("Panel 1 content")
            ]
        ),
        dmc.AccordionItem(
            value="panel-2",
            label="Panel 2",
            children=[
                dmc.Text("Panel 2 content")
            ]
        )
    ]
)
```

### Carousel

**Complete Prop List:**
- `id` (string, required): Component ID
- `children` (list): Slide elements
- `loop` (bool): Loop slides
- `align` (string): Slide alignment
- `dragFree` (bool): Free dragging
- `draggable` (bool): Enable dragging
- `slideSize` (string): Slide size
- `orientation` (string): Orientation
- `height` (number): Carousel height
- `emblaOptions` (dict): Embla carousel options
- `styles` (dict): Style overrides

**Example:**
```python
dmc.Carousel(
    loop=True,
    align="center",
    height=200,
    children=[
        dmc.Image(src="slide1.jpg"),
        dmc.Image(src="slide2.jpg"),
        dmc.Image(src="slide3.jpg")
    ]
)

# Advanced carousel with controls
dmc.Carousel(
    loop=True,
    controls=["prev", "next"],
    styles={"control": {"margin": 10}}
)
```

### Tabs

**Complete Prop List:**
- `id` (string, required): Component ID
- `value` (string | number): Active tab
- `orientation` (string): Tab orientation
- `variant` (string): Tab variant
- `placement` (string): Tab placement
- `allowDeactivation` (bool): Allow deactivation
- `styles` (dict): Style overrides

**Example:**
```python
dmc.Tabs(
    value="tab1",
    children=[
        dmc.TabsList([
            dmc.Tab(value="tab1", label="Overview"),
            dmc.Tab(value="tab2", label="Details"),
            dmc.Tab(value="tab3", label="Settings")
        ]),
        dmc.TabsPanel(
            value="tab1",
            children=dmc.Text("Overview content")
        ),
        dmc.TabsPanel(
            value="tab2",
            children=dmc.Text("Details content")
        )
    ]
)
```

### Timeline

**Complete Prop List:**
- `id` (string, required): Component ID
- `active` (string | bool): Active timeline item
- `bulletSize` (string | number): Bullet size
- `lineWidth` (number): Line thickness
- `color` (string): Timeline color
- `align` (string): Timeline alignment
- `styles` (dict): Style overrides

**Example:**
```python
dmc.Timeline(
    active="item-2",
    bulletSize="lg",
    color="blue",
    align="center",
    children=[
        dmc.TimelineItem(
            id="item-1",
            title="Event 1",
            bullet=dmc.IconCalendar(),
            children=[
                dmc.Text("Event 1 details")
            ]
        ),
        dmc.TimelineItem(
            id="item-2",
            title="Event 2",
            bullet=dmc.IconCheckCircle(),
            children=[
                dmc.Text("Event 2 details")
            ]
        )
    ]
)
```

### Stepper

**Complete Prop List:**
- `id` (string, required): Component ID
- `active` (number): Active step
- `orientation` (string): Stepper orientation
- `color` (string): Step color
- `size` (string): Step size
- `iconPosition` (string): Icon position
- **allowNext** (bool): Allow next step
- **allowPrevious** (bool): Allow previous step
- **allowStepSelect** (bool): Allow step selection
- **styles` (dict): Style overrides

**Example:**
```python
dmc.Stepper(
    active=1,
    orientation="horizontal",
    color="blue",
    iconPosition="right",
    children=[
        dmc.StepperStep(
            label="First Step",
            description="Step 1 details"
        ),
        dmc.StepperStep(
            label="Second Step",
            description="Step 2 details"
        ),
        dmc.StepperStep(
            label="Completed",
            description="All steps completed"
        ),
        dmc.Stepper.Completed(
            description="✓ All done!"
        )
    ]
)
```

### ScrollArea

**Complete Prop List:**
- `id` (string, required): Component ID
- `scrollbars` (list): Scrollbar configuration
- `offset` (number): Scroll position offset
- `autoscroll` (bool): Auto-scroll
- `onScrollPositionChange` (function): Scroll callback
- `styles` (dict): Style overrides

**Example:**
```python
dmc.ScrollArea
    h={200},
    autoscroll=True,
    scrollbarProps={{
        "type": "always"
    }},
    onScrollPositionChange=lambda pos: print(f"Scrolled to {pos}")
)

# With scrollbars
dmc.ScrollArea
    h={300}
    scrollbars=["y", "x"],  # Y and X axes scrollbars
    styles={"root": {"height": 300}}
)
```

---

## Utility Components

### MantineContainer
**Overview**: Responsive wrapper component that provides consistent max-width and centering for layout sections.

**Props**:
- `fluid` (bool, default=False): Remove max-width constraint for full-width layouts.
- `size` (str | int, default="md"): Maximum width ("xs", "sm", "md", "lg", "xl", or custom px value).
- `px` (str | int, optional): Horizontal padding.
- `py` (str | int, optional): Vertical padding.
- `style` (dict, optional): Additional inline styles.
- `className` (str, optional): Custom CSS classes.

**Examples**:
```python
# Fixed width container
dmc.MantineContainer(
    size="lg",
    children=[
        dmc.Text("Content with maximum width of 960px")
    ]
)

# Full-width fluid container
dmc.MantineContainer(
    fluid=True,
    px="xl",
    children=[
        dmc.Text("Full-width content with horizontal padding")
    ]
)

# Responsive design
dmc.MantineContainer(
    size="md",
    px={"base": "md", "sm": "lg", "xl": "xl"},
    children=[...]
)
```

**Integration Patterns**:
- Page layouts: Wrap main content areas for consistent width.
- Form sections: Group related form elements.
- Dashboard panels: Create consistent card layouts.

### MantineLoader
**Overview**: Loading spinner components with multiple variants and customizable appearances.

**Props**:
- `variant` (str, default="oval"): Loader style ("oval", "dots", "bars", "rotate").
- `size` (str | int, default="md"): Loader size ("xs", "sm", "md", "lg", "xl", or custom px).
- `color` (str, optional): Custom color from theme.
- `speed` (int, default=1): Animation speed multiplier.
- `className` (str, optional): Custom CSS classes.

**Examples**:
```python
# Basic loader
dmc.MantineLoader()

# Custom variant and size
dmc.MantineLoader(
    variant="dots",
    size="xl",
    color="blue"
)

# Inline with content
dmc.Group([
    dmc.MantineLoader(size="sm"),
    dmc.Text("Loading...")
])

# Full-page loading overlay
dmc.LoadingOverlay(
    visible=True,
    loaderProps={"variant": "bars", "size": "xl"}
)
```

**Integration Patterns**:
- Data loading: Show during API calls or data processing.
- Form submissions: Display while forms are being submitted.
- Button states: Use `loading` prop in buttons for automatic loader.

### MantineScrollArea
**Overview**: Customizable scrollable areas with styled scrollbars and scroll position tracking.

**Props**:
- `viewportSize` (int, optional): Fixed height/width for viewport.
- `onScrollPositionChange` (callable, optional): Callback for scroll position changes.
- `scrollbars` (str, default="xy"): Which scrollbars to show ("x", "y", "xy", "none").
- `type` (str, default="auto"): Scroll behavior ("auto", "always", "scroll", "never").
- `offsetScrollbars` (bool, default=False): Offset scrollbars from edge.
- `hideScrollbar` (bool, default=False): Hide scrollbars but maintain functionality.
- `style` (dict, optional): Custom styles.

**Examples**:
```python
# Basic scrollable area
dmc.MantineScrollArea(
    h=300,
    children=[
        dmc.Text("Long content that will scroll...")
    ]
)

# With scroll position tracking
@app.callback(
    Output("scroll-position", "children"),
    Input("scroll-area", "scrollPositionChange")
)
def handle_scroll(scroll_data):
    return f"Scrolled to: {scroll_data}"

# Virtual scrolling for large lists
def render_virtual_list(items, item_height=40):
    return dmc.MantineScrollArea(
        h=400,
        children=[
            dmc.Box(
                h=item_height * len(items),
                children=[
                    # Render only visible items
                ]
            )
        ]
    )
```

**Performance Considerations**:
- Large lists (>100 items): Implement virtual scrolling to maintain performance.
- Scroll events: Debounce scroll position callbacks to avoid excessive updates.
- Memory: Clear scroll listeners on component unmount.

**Integration Patterns**:
- Data tables: Enable scrolling for large datasets.
- Chat interfaces: Auto-scroll to latest messages.
- Image galleries: Horizontal scrolling for thumbnail lists.

### MantineThemeIcon
**Overview**: Icon buttons with themed backgrounds and hover states for consistent icon actions.

**Props**:
- `size` (str | int, default="md"): Icon size ("xs", "sm", "md", "lg", "xl").
- `color` (str, default="gray"): Theme color for background.
- `variant` (str, default="filled"): Style variant ("filled", "light", "outline", "subtle", "transparent", "white").
- `radius` (str | int, default="sm"): Border radius.
- `children` (component, required): Icon component (e.g., `dmc.icontabler.X`).

**Examples**:
```python
# Basic themed icon
dmc.MantineThemeIcon(
    size="lg",
    color="blue",
    children=dmc.icontabler.settings
)

# Action buttons in tables
def render_table_actions():
    return dmc.Group([
        dmc.MantineThemeIcon(
            size="sm",
            color="green",
            variant="outline",
            children=dmc.icontabler.edit
        ),
        dmc.MantineThemeIcon(
            size="sm",
            color="red",
            variant="outline",
            children=dmc.icontabler.trash
        )
    ])

# Floating action button
dmc.MantineThemeIcon(
    size="xl",
    color="blue",
    style={"position": "fixed", "bottom": 20, "right": 20},
    children=dmc.icontabler.plus
)
```

**Integration Patterns**:
- Table actions: Edit/delete/view buttons in data tables.
- Navigation: Menu toggles, back buttons, navigation helpers.
- Quick actions: Add, save, export, refresh operations.

### MantineVisitorKey
**Overview**: Accessibility component for keyboard navigation and event handling in web applications.

**Props**:
- `onKeyDown` (callable, optional): Keyboard event handler.
- `keyBindings` (dict, optional): Predefined key shortcuts.
- `preventDefault` (bool, default=False): Prevent default browser behavior.
- `stopPropagation` (bool, default=False): Stop event propagation.

**Examples**:
```python
# Keyboard shortcuts
dmc.VisitorKey(
    keyBindings={
        "Enter": lambda: print("Submit action"),
        "Escape": lambda: print("Cancel action"),
        "Ctrl+S": lambda: print("Save action")
    },
    children=[
        dmc.TextInput(
            placeholder="Press Enter to submit, Escape to cancel"
        )
    ]
)

# Custom keyboard handling
@app.callback(
    Input("search-input", "n_keydown")
)
def handle_keyboard(key_code):
    if key_code == "Enter":
        return perform_search()
    elif key_code == "ArrowDown":
        return focus_next_result()
```

**Integration Patterns**:
- Form navigation: Tab between fields with custom keys.
- Data grids: Arrow key navigation for table cells.
- Modal dialogs: Escape key to close, Enter to confirm.

### MantineFocusTrap
**Overview**: Accessibility component that traps focus within a specific region, essential for modals and overlays.

**Props**:
- `active` (bool, default=True): Enable/disable focus trap.
- `initialFocus` (str | int, optional): Element selector or index for initial focus.
- `restoreFocus` (bool, default=True): Restore focus to previous element on unmount.
- `onEscape` (callable, optional): Handler for Escape key.

**Examples**:
```python
# Modal with focus trap
dmc.Modal(
    opened=True,
    children=[
        dmc.FocusTrap(
            active=True,
            initialFocus="input-name",
            children=[
                dmc.TextInput(id="input-name", label="Name"),
                dmc.TextInput(id="input-email", label="Email"),
                dmc.Button("Submit")
            ]
        )
    ]
)

# Custom focus management
dmc.FocusTrap(
    active=modal_open,
    onEscape=lambda: set_modal_open(False),
    children=[modal_content]
)
```

**Integration Patterns**:
- Modals: Ensure focus stays within modal dialog.
- Sidebars: Trap focus in navigation drawers.
- Forms: Keep focus within multi-step forms.

### Space, Divider, Group (Enhanced)

#### Enhanced Space Component
**Complete Prop List:**
- `h` (str | int): Height spacing
- `w` (str | int): Width spacing
- `direction` (str): "row" or "column"
- `gap` (str | int): Gap between items
- `style` (dict): Custom styles

**Advanced Spacing:**
```python
# Responsive spacing
dmc.Space(h={"base": "sm", "md": "md", "lg": "lg"})

# Complex layouts
dmc.Group(
    direction="column",
    gap="xl",
    children=[
        dmc.Text("Section 1"),
        dmc.Space(h="md"),
        dmc.Text("Section 2")
    ]
)
```

#### Enhanced Divider
**Complete Prop List:**
- `orientation` (str): "horizontal" or "vertical"
- `size` (str | int): Line thickness ("xs", "sm", "md", "lg", "xl")
- `color` (str): Theme color
- `label` (str): Optional label text
- `labelPosition` (str): "left", "center", "right"
- `variant` (str): "solid" or "dashed"
- `style` (dict): Custom styles

**Advanced Examples:**
```python
# Section dividers with labels
dmc.Divider(
    label="Configuration",
    labelPosition="center",
    size="md",
    color="blue",
    mt="xl",
    mb="md"
)

# Vertical dividers
dmc.Group([
    dmc.Text("Left content"),
    dmc.Divider(orientation="vertical", size="sm"),
    dmc.Text("Right content")
])
```

#### Enhanced Group
**Complete Prop List:**
- `gap` (str | int | dict): Spacing between items
- `justify` (str): "flex-start", "center", "flex-end", "space-between", "space-around"
- `align` (str): "flex-start", "center", "flex-end", "stretch"
- `wrap` (str): "nowrap", "wrap", "wrap-reverse"
- `direction` (str): "row", "column", "row-reverse", "column-reverse"
- `grow` (bool): Allow items to grow to fill space

**Advanced Layout Examples:**
```python
# Responsive grid
dmc.Group(
    grow=True,
    gap="md",
    children=[
        dmc.Button("Button 1", flex=1),
        dmc.Button("Button 2", flex=1),
        dmc.Button("Button 3", flex=1)
    ]
)

# Complex alignment
dmc.Group(
    justify="space-between",
    align="center",
    children=[
        dmc.Text("Left aligned"),
        dmc.Group(gap="sm", children=[
            dmc.Button("Cancel", variant="outline"),
            dmc.Button("Submit")
        ])
    ]
)
```

---

# Advanced Features

## Functions as Props (v2.0+)

### Overview

Functions as Props allows safe execution of JavaScript functions in Dash applications, enabling dynamic formatting, custom rendering, and complex interactions.

### How It Works

1. **Define Functions**: Create JavaScript functions in `/assets/custom.js`
2. **Reference by Name**: Use `{"function": "functionName"}` in Python
3. **Pass Options**: Use `{"options": {"key": "value"}}` for parameters
4. **Return Components**: Can return React components

### Basic Usage**

**JavaScript Functions:**
```javascript
// assets/custom.js
var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.formatCurrency = function(value, options) {
    const currency = options.currency || 'USD';
    return `${currency} ${value.toFixed(2)}`;
};

dmcfuncs.isWeekday = function(dateStr) {
    const date = dayjs(dateStr, "YYYY-MM-DD");
    const day = date.day();
    return day !== 5;  // Exclude Fridays
};
```

**Python Integration:**
```python
# Function reference
dmc.Slider(
    label={"function": "formatCurrency", "options": {"unit": "USD"}},
    value=25
)

# Direct function call
dmc.Button(
    label={"function": "formatPercent", "options": {"format": "percentage"}}
)
)
```

### Supported Component Props

**Forms & Inputs:**
- **Slider/RangeSlider**: `label`, `scale`
- **Select/MultiSelect/TagsInput**: `renderOption`, `filter`
- **Date Components**: `disabledDates`

**Charts:**
- **All Charts**: `valueFormatter`, `tooltipProps`

**Advanced Components:**
- **Tree**: `renderNode`
- **RichTextEditor**: `getEditor(id)`

### AI-Assisted Function Generation

**Template for AI:**
```
Write a JavaScript function for Dash Mantine Components named `formatUsd`. Assign it to `dmcfuncs.formatUsd`. Include the global header. In Python version:
def format_usd(value, options):
    return f"${options.unit} ${value:.2f}"
```

**Example AI Prompt:**
> Create a JavaScript function for Dash Mantine Components named `formatUsd` that formats currency values. Include global header and support percentage formatting.
> In Python:
> def format_usd(value, options):
>     return f"${options.unit} ${value:.2f}"

**Result:**
```javascript
var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.formatUsd = function(value, options) {
    const currency = options.currency || 'USD';
    return `${currency} ${value.toFixed(2)}`;
};
```

### Best Practices

1. **Performance**: Cache expensive computations
2. **Type Safety**: Use TypeScript JSDoc comments
3. **Error Handling**: Always validate function existence before use
4. **React Components**: Use `React.createElement()` for complex JSX

### Client-Side Access

**Get Editor Instance:**
```javascript
const editor = dash_mantine_components.getEditor("editor-id");
if (editor) {
    return editor.getHTML();
}
```

**External Library Integration:**
```python
app = Dash(
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/dayjs@1.10.8/dayjs.min.js"
    ]
)

# In JavaScript:
const dayjs = require('dayjs');
```

---

# Rich Text Editor Details

### Complete Prop List:

**Core Editor Props:**
- `id` (string, required): Component ID
- `value` (string): Editor content (HTML)
- `placeholder` (string): Placeholder text
- `editable` (bool): Enable/disable editing
- `focus` (bool): Auto-focus editor
- `toolbar` (list): Toolbar configuration
- `styles` (dict): Style overrides

**Toolbar Configuration:**
```python
# Basic toolbar
toolbar = [
    'bold', 'italic', 'underline',
    'h1', 'h2', 'h3',
    'bulletList', 'numberedList',
    'link', 'image',
    'table'
]

# Advanced toolbar with custom controls
toolbar = [
    'bold', 'italic', 'underline',
    {'type': 'separator'},
    {'color': 'red', 'label': 'Delete', 'action': 'delete'},
    {
        'function': 'clearFormat',
        'options': {"format": "titleize"}
    }
]
```

**Examples:**

**Basic Editor:**
```python
dmc.RichTextEditor(
    id="editor",
    value="<p>Initial content</p>",
    placeholder="Start typing...",
    editable=True,
    toolbar=[
        'bold', 'italic', 'underline',
        'h1', 'h2', 'h3',
        'link', 'image'
    ]
)
```

**Server-Side Integration:**
```python
@callback(Output("content", "children"), Input("editor", "value"))
def update_editor(html_content(html_content):
    return html.Div(dmc.P(html_content, dangerously_setInnerHTML=True))

# Client-side editor access
# assets/editor-client.js
function update_editor():
    editor = dash_mantine_components.getEditor("editor")
    if editor:
        editor.commands.setContent("<p>Updated</p>")
```

### Migration Notes

- **v2.3.0+**: Now uses Tiptap 3
- **Code Highlighting**: Top 10 languages bundled by default
- **Focus Control**: New `focus` prop for cursor management
- **Text Style API**: Enhanced text formatting options

---

# Charts & Visualization

## Chart Integration

DMC integrates with **Recharts** for data visualization. All charts include:

- **Responsive Design**: Automatic screen size adaptation
- **Interactive Features**: Hover effects, click events, highlighting
- **Custom Styling**: Theme integration
- **Performance**: Virtualization support

### Chart Components

#### LineChart

**Props:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- `styles` (dict): Style overrides

**Child Components:**
- `LineChart.XAxis`: X-axis configuration
- `LineChart.YAxis`: Y-axis configuration
- `LineChart.CartesianGrid`: Grid lines
- `LineChart.Line`: Line configuration
- `LineChart.Tooltip`: Tooltip configuration
- `LineChart.Legend`: Legend

**Example:**
```python
data = [
    {"month": "Jan", "sales": 1000, "profit": 200},
    {"month": "Feb", "sales": 1200, "profit": 300}
]

dmc.LineChart(
    height=300,
    data=data,
    children=[
        dmc.LineChart.XAxis(dataKey="month"),
        dmc.LineChart.YAxis(),
        dmc.LineChart.CartesianGrid(),
        dmc.LineChart.Line(
            type="monotone",
            dataKey="sales",
            stroke="#8884d8"
        ),
        dmc.LineChart.Tooltip(),
        dmc.LineChart.Legend()
    ]
)
```

#### BarChart

**Props:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (string): Chart width
- `margin` (dict): Chart margins
- **Child Components**:
  - `BarChart.XAxis`: X-axis configuration
  - `BarChart.YAxis`: Y-axis configuration
  - `BarChart.CartesianGrid`: Grid lines
  - `BarChart.Bar`: Bar configuration
  - `BarChart.Tooltip`: Tooltip configuration
  - `BarChart.Legend`: Legend

**Example:**
```python
dmc.BarChart(
    height=300,
    data=data,
    children=[
        dmc.BarChart.XAxis(dataKey="month"),
        dmc.BarChart.YAxis(),
        dmc.BarChart.CartesianGrid(),
        dmc.BarChart.Bar(
            dataKey="sales",
            fill="#82ca9d"
        ),
        dmc.BarChart.Tooltip(),
        dmc.BarChart.Legend()
    ]
)
```

#### AreaChart

**Props:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- **Child Components**:
  - `AreaChart.XAxis`: X-axis configuration
  - `AreaChart.YAxis`: Y-axis configuration
  - `AreaChart.CartesianGrid`: Grid lines
  - `AreaChart.Area`: Area configuration
  - `AreaChart.Tooltip`: Tooltip configuration
  - `AreaChart.Legend`: Legend

**Example:**
```python
dmc.AreaChart(
    height=300,
    data=data,
    children=[
        dmc.AreaChart.XAxis(dataKey="month"),
        dmc.AreaChart.YAxis(),
        dmc.AreaChart.CartesianGrid(),
        dmc.AreaChart.Area(
            type="monotone",
            dataKey="sales",
            stroke="#8884d8",
            fill="#8884d8",
            fillOpacity=0.3
        ),
        dmc.AreaChart.Tooltip(),
        dmc.AreaChart.Legend()
    ]
)
```

#### PieChart

**Props:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- **Child Components:**
  - `PieChart.Label`: Label configuration
  - `PieChart.Pie`: Pie configuration
  - `PieChart.Cell`: Cell configuration
  - `PieChart.Tooltip`: Tooltip configuration
  - `PieChart.Legend`: Legend

**Example:**
```python
data = [
    {"name": "Category A", "value": 400, "color": "#f5f2f"},
    {"name": "Category B", "value": 300, "color": "#4299e0"},
    {"name": "Category C", "value": 300, "color": "#228be6f"}
]

dmc.PieChart(
    height=300,
    data=data,
    children=[
        dmc.PieChart.Label(position="outside"),
        dmc.PieChart.Pie(
            dataKey="value",
            nameKey="name",
            cx="50%",
            cy="50%",
            outerRadius=80,
            fill="#82ca9d"
        ),
        dmc.PieChart.Cell(),
        dmc.PieChart.Tooltip(),
        dmc.PieChart.Legend()
    ]
)
```

#### ScatterChart

**Props:**
- `id` (string, required): Component ID
- `data` (list of dicts): Chart data
- `height` (number): Chart height
- `width` (number): Chart width
- `margin` (dict): Chart margins
- **Child Components**:
  - `ScatterChart.XAxis`: X-axis configuration
  - `ScatterChart.YAxis`: Y-axis configuration
  - `ScatterChart.ZAxis` (optional): Z-axis configuration
  - `ScatterChart.CartesianGrid`: Grid lines
  - `ScatterChart.Scatter`: Scatter configuration
  - `ScatterChart.Tooltip`: Tooltip configuration
  - `ScatterChart.Legend`: Legend

**Example:**
```python
data = [
    {"x": 100, "y": 200, "z": 10},
    {"x": 120, "y": 150, "z": 20}
]

dmc.ScatterChart(
    height=400,
    width=600,
    data=data,
    children=[
        dmc.ScatterChart.XAxis(dataKey="x"),
        dmc.ScatterChart.YAxis(dataKey="y"),
        dmc.ScatterChart.ZAxis(dataKey="z"),
        dmc.ScatterChart.CartesianGrid(),
        dmc.ScatterChart.Scatter(
            name="Data Points",
            dataKey="y"
        ),
        dmc.ScatterChart.Tooltip()
    ]
)
```

### Composite Chart

**Multiple Chart Types:**
```python
# Combining line and bar
dmc.CompositeChart(
    height=400,
    data=revenue_profit_data,
    children=[
        dmc.AreaChart(
            name="Revenue",
            dataKey="month"
        ),
        dmc.BarChart(
            name="Profit",
            dataKey="month"
        )
    ]
)

# Line + Scatter
dmc.CompositeChart(
    height=400,
    data=combined_data,
    children=[
        dmc.LineChart(
            name="Users Over Time",
            dataKey="timestamp"
        ),
        dmc.ScatterChart(
            name="User Activity",
            dataKey="user_activity"
        )
    ]
)
```

### Chart Advanced Features

#### Function Props in Charts

```python
# Custom value formatter for charts
dmc.LineChart(
    valueFormatter={(value) => f"${value:,.2f}"},
    dataKey="amount"
)

# Dynamic tooltip content
dmc.BarChart(
    tooltipProps={
        "value": (value, payload) => `f"Payload.currency}${value:,.2f}`
    }
)

# Custom bar colors
dmc.BarChart(
    getBarColor={(value, index) => {
        colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "gray"]
        return colors[index % len(colors)]
    }
)
```

#### Interactive Charts

**Hover Events:**
```python
@callback(
    Output("chart-data", "data"),
    Input("chart", "hoverData")
)
def update_hover_data(hover_data):
    # Add hover effect
    for item in hover_data:
        item['hover'] = True
    return hover_data

@callback(
    Output("chart", "clickData"),
    Input("chart", "clickData")
)
def handle_chart_click(click_data):
    # Handle chart interactions
    return click_data
```

---

## Configuration

### Environment Setup

**Required Dependencies:**
- Python 3.8+
- Dash >= 2.0
- Node.js (for custom builds, optional)

**Basic Setup:**
```python
import dash
from dash import Dash, dcc, callback, Input, Output
import dash_mantine_components as dmc

app = Dash()

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[...your app content...]
)

# Custom functions setup
def setup_custom_functions():
    # Create assets/custom.js with function definitions
    # Return to use with dmc functions as props
    pass "options" parameter from Python
    # Supports React.createElement for components
```

### External Scripts
```python
app = Dash(
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dayjs@1.10.8/dayjs.min.js",
        "https://cdn.jsdelivr.net/npm/mdi-material/5.0.0/mdi.js"
    ]
)
```

### CSS Variables
```css
/* Custom CSS overrides */
.mantine-TextInput-input {
    border-color: #ddd;
    background-color: var(--mantine-color-blue-0);
}
```

---

# Integration Examples

### Complete Dashboard Example

**Responsive Dashboard Layout:**
```python
app.layout = dmc.MantineProvider([
    dmc.AppShell(
        navbar=dmc.AppShellNavbar(
            height=60,
            children=[
                dmc.Group(
                    position="apart",
                    children=[
                        dmc.Button("Dashboard", variant="subtle"),
                        dmc.Button("Reports"),
                        dmc.Button("Settings")
                    ]
                )
            ]
        ),
        dmc.AppShellMain([
            dmc.Container(
                size="lg",
                children=[
                    dmc.Grid(
                        gutter="lg",
                        children=[
                            dmc.Col(span=12, md=6),
                            dmc.Col(span=12, md=6),
                            dmc.Col(span=12, md=6)
                        ]
                    )
                )
            ]
        )
    ])
```

### Form with Validation

**Comprehensive Form Example:**
```python
@callback(
    [Output("submit-btn", "n_clicks"), Input("submit-btn", "n_clicks")],
    [Output("form-alert", "hidden"), Output("form-alert", "children")],
    [Input("email-input", "value"), Input("password-input", "value")],
    [Input("country-select", "value")],
    [Input("birth-date", "value")],
    [State("form-state", "data")],
    prevent_initial_call=True
)
def validate_form(submit_n_clicks, email, password, country, birthdate, form_data):
    errors = []

    # Email validation
    if email and "@" not re.match(r'^[\w\.-]+@[\w\.-]+\.[\w\.]{2,}$', email):
        errors.append("Invalid email format")

    # Password requirements
    if not password or len(password) < 8:
        errors.append("Password must be at least 8 characters")

    # Country validation
    if not country:
        errors.append("Country is required")

    # Date validation
    if birthdate:
        errors.append("Date is required")

    return len(errors) > 0

# Usage
app.layout = dmc.Container([
    dmc.TextInput(id="email-input"),
    dmc.PasswordInput(id="password-input"),
    dmc.Select(id="country-select"),
    dmc.DatePickerInput(id="birth-date"),
    dmc.Button("Submit", id="submit-btn", n_clicks=0),
    dmc.Alert(id="form-alert", hidden=True)
])
```

### Real-time Data Integration

**WebSocket Example:**
```python
import websocket
import json

# WebSocket connection
ws = websocket.WebSocket()

# App with real-time updates
@callback(
    Output("live-chart", "data"),
    Input("ws", "n_messages")
)
def update_chart(n_messages):
    if n_messages:
        try:
            messages = json.loads(n_messages[-1])
            return messages[-1]["chart_data"]
        except:
            return n_messages
    return []

@app.callback(
    Output("table-data", "data"),
    Input("refresh", "n_clicks")
)
def refresh_table(refresh_n_clicks):
    return get_updated_data()
```

### File Upload Integration

**Drag & Drop File Components:**
```python
from dash import dcc

app.layout = dmc.Container([
    dcc.Upload(
        id="file-upload",
        children="Upload JSON",
        multiple=True,
        accept=".json,.csv",
        completed=False
    ),
    html.Div(id="upload-status")
])

@callback(
    Output("file-upload", "completed"),
    Input("file-upload", "contents"),
    prevent_initial_call=True
)
def handle_upload(contents):
    try:
        # Process uploaded files
        return "Upload complete!"
    except:
        return "Upload failed"
```

---

# Best Practices Summary

1. **Performance**: Use lazy loading and memoization
2. **Accessibility**: Always include proper labels and ARIA attributes
3. **Error Handling**: Validate input before processing
4. **State Management**: Use dcc.Store for complex state
5. **Theme Consistency**: Centralize theme configuration

---

# API Reference

## Component Quick Reference

### Forms & Input Components

#### TextInput
- **Key Props**: `id`, `value`, `placeholder`, `label`, `description`
- **Styling**: `styles`, `sx`, `className`
- **Events**: `onChange`, `n_blur`, `n_submit`
- **Validation**: `error`, `required`
- **Integration**: Dash callbacks with Input/Output

#### Select
- **Key Props**: `id`, `value`, `data`, `searchable`
- **Data Format**: List of `{'label': 'Display', 'value': 'val'}`
- **Features**: `creatable`, `searchable`, `maxDropdownHeight`
- **Styling**: `variant`, `color`, `size`
- **Advanced**: `getCreateLabel`, `onCreate`

#### DatePickerInput
- **Key Props**: `id`, `value`, `placeholder`, `minDate`, `maxDate`
- **Data Format**: ISO string or date object
- **Features**: `clearable`, `dropdownType`
- **Integration**: `onChange` callbacks

#### Slider
- **Key Props**: `id`, `value`, `min`, `max`, `step`, `marks`
- **Features**: `label`, `labelAlwaysOn`, `showLabelOnHover`
- **Customization**: `getBarColor`, `valueFormatter`

#### RichTextEditor
- **Key Props**: `id`, `value`, `editable`, `focus`
- **Features**: `toolbar`, `toolbar`, `sx`
- **Integration**: `getEditor(id)` for client-side access

---

## Layout Components

#### Container
- **Key Props**: `fluid`, `size`, `px`, `py`
- **Responsiveness**: `size` parameter with breakpoints
- **Integration**: Wrap entire app for consistent spacing

#### Grid System
- **Grid + Col**: Flexible 12-column layout system
- **SimpleGrid**: Equal-width columns
- **Responsive**: Breakpoint-based sizing

#### Flex
- **Properties**: `direction`, `wrap`, `gap`, `align`, `justify`

#### Box
- **Utilities**: `p`, `px`, `py`, `m` shortcuts
- **Advanced**: `sx` prop for Emotion styling

---

## Data Display Components

#### Text & Typography
- **Text**: Basic text with full styling control
- **Title**: Semantic headings (h1-h6)
- **Code**: Inline and block code highlighting
- **Badge**: Status indicators and tags
- **Avatar**: User profiles with fallbacks

#### Table
- **Features**: Sorting, filtering, highlighting
- **Performance**: Virtual scrolling for large datasets
- **Integration**: Pandas DataFrame integration
- **Accessibility**: Semantic table structure

#### Progress Indicators
- **Progress**: Linear progress bar
- **RingProgress**: Circular progress indicator
- **Badge**: Status and category indicators

---

## Feedback & Overlays

#### Modal Management
- **Stacked Modals**: `ModalStack` and `DrawerStack`
- **Z-index Management**: Proper layering and focus trapping
- **User Experience**: Controlled vs automatic closing

#### Alert System
- **Notification Types**: Success, error, warning, info
- **Auto-dismissal**: Time-based or manual dismiss
- **Container Integration**: `NotificationContainer` system

#### Loading States
- **Skeleton**: Content placeholders
- **LoadingOverlay**: Full overlay with blur effects
- **Progress**: Visual feedback for long operations

#### Hover Effects
- **Tooltip**: Context-sensitive information
- **Popover**: Click or hover dropdowns
- **Popovers**: Rich dropdown content

---

## Charts & Visualization

These components leverage Mantine's charting capabilities (built on Recharts under the hood) for interactive, responsive visualizations. They support theming, tooltips, legends, and animations. All charts inherit common props like `data`, `height`, `width`, and `theme`.

### MantineChart (Generic Chart Wrapper)
**Overview**: A flexible wrapper for various chart types, allowing dynamic switching between chart modes (e.g., line, bar) via props. Ideal for dashboards needing multi-view charts.

**Props**:
- `data` (list of dicts, required): Chart data array, e.g., `[{'name': 'A', 'value': 10}, ...]`.
- `type` (str, default="line"): Chart type ("line", "bar", "area", "scatter", "pie", "radar", "bubble").
- `height` (int | str, default=300): Chart height in px or "auto".
- `width` (int | str, default="100%"): Chart width.
- `colors` (list[str] | str, default="theme"): Color palette or theme-based.
- `showTooltip` (bool, default=True): Enable/disable tooltips.
- `showLegend` (bool, default=True): Show/hide legend.
- `margin` (dict, default={"top": 5, "right": 30, "left": 20, "bottom": 5}): Chart margins.
- `animate` (bool, default=True): Enable animations.
- `className` (str, optional): Additional CSS classes.
- `style` (dict, optional): Inline styles.
- `id` (str, optional): Dash component ID for callbacks.
- `loading` (bool, default=False): Show loading overlay.

**Examples**:
```python
import dash
import dash_mantine_components as dmc
from dash import html

data = [{'name': 'Jan', 'value': 400}, {'name': 'Feb', 'value': 300}]

app = dash.Dash(__name__)

app.layout = html.Div([
    dmc.MantineChart(
        id="dynamic-chart",
        type="bar",  # Can be updated via callback
        data=data,
        height=400,
        colors=["#ff6384", "#36a2eb"]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
```
- **Callback Example**: Update `type` prop via dropdown to switch views.

**Advanced Usage**:
- Dynamic typing: Use Dash callbacks to change `type` based on user input (e.g., toggle between "line" and "bar").
- Custom axes: Extend with `xAxis` and `yAxis` props (dicts for labels, ticks, etc.) for domain-specific formatting (e.g., dates on x-axis).
- Responsiveness: Set `width="100%"` and wrap in `dmc.Container` for fluid layouts.

**Integration Patterns**:
- With `dmc.DataTable`: Sync chart data with table filters.
- With `dmc.Modal`: Embed charts in modals for detailed views.
- Dash Ecosystem: Use with `dash_bootstrap_components` for responsive grids.

**Performance Considerations**:
- For large datasets (>1000 points), disable `animate` and use `head_limit` in data preprocessing to subsample.
- Virtual rendering: Charts auto-handle via Recharts; avoid re-renders by memoizing data in callbacks.
- Memory: Clear tooltips on unmount to prevent leaks.

**Styling & Theming**:
- Inherit from Mantine theme: `colors` prop uses `theme.colors`.
- Custom CSS: Target `.recharts-wrapper` for overrides, e.g., `tooltip { background: var(--mantine-color-blue-0); }`.
- Dark mode: Auto-adapts via `dmc.MantineProvider`.

### MantineScatterChart
**Overview**: Scatter plot for bivariate data visualization, supporting bubble sizing and color mapping. Useful for correlations, clusters, or geospatial data.

**Props** (extends MantineChart):
- `xAxisKey` (str, required): Key for x-axis data.
- `yAxisKey` (str, required): Key for y-axis data.
- `sizeKey` (str, optional): Key for bubble size (for bubble variant).
- `colorKey` (str, optional): Key for color mapping.
- `pointSize` (int | list[int], default=4): Point radius.
- `opacity` (float, 0-1, default=0.8): Point opacity.
- `shape` (str, default="circle"): Point shape ("circle", "square", "triangle").

**Examples**:
```python
data = [
    {'x': 1, 'y': 2, 'size': 10, 'color': 'red'},
    {'x': 3, 'y': 5, 'size': 20, 'color': 'blue'}
]

dmc.MantineScatterChart(
    data=data,
    xAxisKey="x",
    yAxisKey="y",
    sizeKey="size",
    height=400,
    colors="category10"  # D3 palette
)
```

**Advanced Usage**:
- Bubble charts: Set `sizeKey` for variable sizing; scale with `pointSize=[min, max]`.
- Quadrants: Use `margin` to add quadrant lines via overlays.
- Zooming: Integrate with `dmc.ActionIcon` for pan/zoom controls (custom callback).

**Integration Patterns**:
- With `dmc.Slider`: Filter data by x/y ranges.
- Pandas Integration: Convert DataFrame to list of dicts via `df.to_dict('records')`.
- Clustering: Pair with ML libs (e.g., scikit-learn) for dynamic point coloring.

**Performance Considerations**:
- Limit to <5000 points; use WebGL via Recharts extensions for larger sets.
- Debounce data updates in callbacks to avoid jittery renders.

**Styling & Theming**:
- Custom shapes: Override via `style` with SVG paths.
- Tooltips: Customize with `showTooltip` formatter for units (e.g., "x: {value} km").

### MantineLineChart
**Overview**: Line chart for time-series or sequential data, with support for multiple lines, smoothing, and markers.

**Props** (extends MantineChart):
- `dataKey` (str, required): Key for y-values.
- `xAxisKey` (str, required): Key for x-axis (e.g., dates).
- `strokeWidth` (int, default=2): Line thickness.
- `smooth` (bool, default=False): Enable curve smoothing.
- `showMarkers` (bool, default=True): Display data points.
- `dot` (bool | dict, default=True): Customize markers (size, fill).

**Examples**:
```python
data = [{'date': '2023-01', 'sales': 400}, {'date': '2023-02', 'sales': 300}]

dmc.MantineLineChart(
    type="line",
    data=data,
    dataKey="sales",
    xAxisKey="date",
    smooth=True,
    height=300
)
```

**Advanced Usage**:
- Multi-line: Use array of datasets with `data=[line1, line2]` and shared x-axis.
- Area fill: Combine with `MantineAreaChart` for stacked lines.
- Forecasting: Append predicted data with dashed lines (`strokeDasharray="5 5"`).

**Integration Patterns**:
- With `dmc.DatePicker`: Update x-axis range dynamically.
- Time-series: Use with Plotly for hybrid charts (DMC for overview, Plotly for drill-down).

**Performance Considerations**:
- For real-time data (e.g., streaming), use `animate=False` and partial updates.
- Smoothing on large data: Disable for >1000 points to reduce CPU.

**Styling & Theming**:
- Line styles: `stroke` prop for colors, `strokeLinecap="round"` for ends.
- Grid: Customize `xAxis`/`yAxis` ticks with theme fonts.

### MantineAreaChart
**Overview**: Area chart for cumulative or filled line data, great for stacked areas or trend volumes.

**Props** (extends MantineLineChart):
- `baseLine` (int | float, default=0): Y-value for area base.
- `stacked` (bool, default=False): Stack multiple areas.
- `fillOpacity` (float, 0-1, default=0.6): Area fill transparency.

**Examples**:
```python
dmc.MantineAreaChart(
    data=data,
    dataKey="sales",
    xAxisKey="date",
    stacked=True,
    fillOpacity=0.7,
    colors={0: "blue", 1: "green"}  # For multi-area
)
```

**Advanced Usage**:
- Stacked series: Provide `data` as list of series; auto-stacks.
- Gradient fills: Use `fill` prop with linear gradients via CSS vars.

**Integration Patterns**:
- With `dmc.Tabs`: Switch between stacked/normal views.
- Dashboard: Embed in `dmc.Grid` with metrics cards.

**Performance Considerations**:
- Stacking computation: Pre-compute cumulative sums client-side for large stacks.
- Opacity: Lower for overlaps to maintain readability.

**Styling & Theming**:
- Fill patterns: Custom SVG defs for hatched fills.
- Theme integration: `fill` uses `theme.fn.linearGradient`.

### MantineBarChart
**Overview**: Bar chart for categorical comparisons, supporting horizontal/vertical orientations and grouping.

**Props** (extends MantineChart):
- `dataKey` (str, required): Key for bar heights.
- `barSize` (int, default=32): Bar width/height.
- `layout` (str, default="vertical"): "vertical" or "horizontal".
- `groupMode` (str, default="grouped"): "grouped" or "stacked".
- `maxBarSize` (int, optional): Cap bar size for consistency.

**Examples**:
```python
dmc.MantineBarChart(
    type="bar",
    data=data,
    dataKey="value",
    layout="horizontal",
    barSize=40,
    height=300
)
```

**Advanced Usage**:
- Grouped bars: Multiple `dataKey` for side-by-side bars.
- Negative values: Auto-handles with mirrored bars.

**Integration Patterns**:
- With `dmc.SegmentedControl`: Toggle layout/grouping.
- Export: Integrate with `dmc.Button` for PNG/SVG download via html2canvas.

**Performance Considerations**:
- Wide categories (>50): Use horizontal layout and pagination.
- Animations: Disable for batched updates.

**Styling & Theming**:
- Bar labels: Add via `label` prop with custom renderers.
- Gaps: Control with `barCategoryGap` (0-50%).

### MantinePieChart
**Overview**: Pie/donut chart for proportional data, with customizable slices and labels.

**Props** (extends MantineChart):
- `dataKey` (str, required): Value key for slice sizes.
- `nameKey` (str, required): Label key for slices.
- `innerRadius` (int, default=0): For donut (e.g., 60 for 60% radius).
- `padAngle` (float, default=0): Slice separation.
- `cornerRadius` (int, default=3): Rounded corners.
- `cx`/`cy` (str | int, default="50%"): Center position.

**Examples**:
```python
data = [{'name': 'A', 'value': 40}, {'name': 'B', 'value': 60}]

dmc.MantinePieChart(
    data=data,
    dataKey="value",
    nameKey="name",
    innerRadius=40,
    height=300
)
```

**Advanced Usage**:
- Animated slices: Use `animate` with callbacks for dynamic data.
- Legends: Sync external `dmc.List` with slice clicks.

**Integration Patterns**:
- With `dmc.Tooltip`: Enhance slice hover details.
- Nested pies: Use multiple components for sub-categories.

**Performance Considerations**:
- Few slices (<20) recommended; aggregate small ones into "Other".
- SVG-based: Efficient for static data.

**Styling & Theming**:
- Slice patterns: Custom `fill` with patterns (e.g., stripes).
- Labels: Position with `labelLine` props.

### MantineRadarChart
**Overview**: Radar/spider chart for multi-attribute comparisons (e.g., skills, metrics).

**Props** (extends MantineChart):
- `dataKey` (str, required): Value key.
- `nameKey` (str, required): Category key.
- `angleAxisKey` (str, required): Angular axis (categories).
- `gridLevel` (int, default=5): Number of radial levels.
- `shape` (str, default="circle"): "circle" or "polygon".
- `connectNulls` (bool, default=False): Fill gaps in data.

**Examples**:
```python
data = [{'subject': 'Math', 'score': 80}, {'subject': 'Science', 'score': 90}]

dmc.MantineRadarChart(
    data=data,
    dataKey="score",
    nameKey="subject",
    angleAxisKey="subject",
    height=400
)
```

**Advanced Usage**:
- Multi-polygons: Overlay multiple datasets for comparisons.
- Custom scales: Normalize data to 0-100 via preprocessing.

**Integration Patterns**:
- With `dmc.Card`: Embed in cards for KPI radars.
- Comparisons: Side-by-side with `dmc.SimpleGrid`.

**Performance Considerations**:
- Limit axes (<10) to avoid clutter; use for 3-8 metrics.
- Vector rendering: Scales well, but test on mobile.

**Styling & Theming**:
- Polygon fill: `fillOpacity` for transparency in overlays.
- Axes: Customize ticks with theme colors.

### MantineBubbleChart
**Overview**: Bubble variant of scatter, emphasizing volume via size/color. For 3D-like data viz.

**Props** (extends MantineScatterChart):
- All scatter props, plus `zAxisKey` (str, optional): For color/size mapping.

**Examples**:
Similar to scatter, with `sizeKey` and `colorKey` for bubbles.

**Advanced Usage**:
- Volume encoding: Map sales volume to size, profit to color.
- Clustering: Highlight groups with stroke borders.

**Integration Patterns**:
- With filters: Use `dmc.MultiSelect` for dimension selection.
- Maps: Overlay on `dmc.Map` for geo-bubbles.

**Performance Considerations**:
- <2000 bubbles; use opacity for density.
- Pre-filter data server-side.

**Styling & Theming**:
- Bubble gradients: `fill` with radial gradients.

---

## Advanced Components

### MantineRichTextEditor
**Overview**: WYSIWYG editor with toolbar, supporting Markdown output, uploads, and custom controls. Built on Quill.js with Mantine styling.

**Props**:
- `value` (str, default=""): Editor content (HTML or Markdown).
- `onChange` (callable, optional): Callback for content changes.
- `id` (str, optional): Dash ID.
- `placeholder` (str, default="Start typing..."): Placeholder text.
- `readonly` (bool, default=False): Read-only mode.
- `autosaveInterval` (int, optional): Auto-save frequency (ms).
- `toolbar` (bool | list[str], default=True): Show/hide toolbar; specify controls (e.g., ["bold", "italic", "link"]).
- `uploadMaxFileSize` (int, default=5*1024*1024): Max upload size (bytes).
- `onImageUpload` (callable, optional): Custom image handler (e.g., for S3).
- `labels` (dict, optional): Customize toolbar labels (e.g., {"bold": "Bold"}).
- `style` (dict, optional): Inline styles for editor/toolbar.
- `classNames` (dict, optional): Custom classes (e.g., {"root": "my-editor"}).
- `theme` (str, default="light"): "light" or "dark".
- `height` (int | str, default=200): Editor height.

**Examples**:
```python
from dash import Output, Input, callback
import dash_mantine_components as dmc

@callback(Output("editor-content", "children"), Input("rich-editor", "value"))
def update_content(value):
    return html.Div(value)  # Render as HTML

app.layout = html.Div([
    dmc.MantineRichTextEditor(
        id="rich-editor",
        value="<p>Hello, world!</p>",
        height=300,
        toolbar=[["bold", "italic"], ["link"], ["ul", "ol"], ["blockquote"]]
    ),
    html.Div(id="editor-content")
])
```

**Advanced Usage**:
- Markdown support: Set `value` as Markdown; use `dangerouslySetInnerHTML` for output.
- Custom controls: Extend toolbar with plugins (e.g., embed YouTube via custom blot).
- Collaborative editing: Integrate with Yjs for real-time (requires custom setup).
- Autosave: Use `autosaveInterval=30000` with Dash storage callbacks.

**Integration Patterns**:
- With `dmc.Modal`: Full-screen editor for long-form content.
- Forms: Embed in `dmc.Group` with validation via `required=True`.
- Dash: Store content in dcc.Store; parse Markdown with `markdown` lib.

**Performance Considerations**:
- Large docs (>10k chars): Use lazy loading and debounce `onChange`.
- Images: Limit uploads; compress client-side with Canvas API.
- Undo/redo: Built-in, but clear history on unmount for memory.

**Styling & Theming**:
- Quill overrides: Target `.ql-editor` for font/line-height.
- Theme: Auto-syncs with Mantine; custom via `theme.overrides.Quill`.
- Dark mode: Handles automatically; adjust contrast for tooltips.

### MantineCodeHighlight
**Overview**: Syntax-highlighted code blocks with copy functionality. Built on Prism.js with multiple language support.

**Props**:
- `code` (str, required): Source code to display.
- `language` (str, default="js"): Programming language for syntax highlighting.
- `copy` (bool, default=True): Show copy button.
- `showLineNumbers` (bool, default=False): Display line numbers.
- `theme` (str, optional): Code theme (e.g., "dark", "light").
- `style` (dict, optional): Inline styles.
- `className` (str, optional): CSS classes.

**Examples**:
```python
dmc.MantineCodeHighlight(
    code="def hello():\n    print('Hello, World!')",
    language="python",
    showLineNumbers=True,
    copy=True
)
```

**Advanced Usage**:
- Multi-language: Use with `dmc.Tabs` for language switching.
- Custom themes: Override Prism CSS variables.
- Integration: With `dmc.Accordion` for collapsible code sections.

**Supported Languages**: Python, JavaScript, TypeScript, Java, C++, CSS, HTML, SQL, Bash, JSON, XML, and 50+ more via Prism.js.

### MantineNotifications
**Overview**: System for toast notifications with positioning, auto-close, and rich content support.

**Usage**:
```python
# Show notification (typically in callback)
dmc.showNotification({
    "title": "Success",
    "message": "Data saved successfully!",
    "color": "green",
    "autoClose": 5000
})

# Error notification
dmc.showNotification({
    "title": "Error",
    "message": "Failed to save data",
    "color": "red",
    "autoClose": False
})
```

**Notification Props**:
- `title` (str): Notification title.
- `message` (str): Notification message.
- `color` (str): Color theme (e.g., "blue", "green", "red").
- `autoClose` (int | bool): Auto-close delay in ms, false for manual close.
- `icon` (str): Custom icon (Mantine icon name).
- `loading` (bool): Show loading state.
- `withCloseButton` (bool): Show close button.

**Integration Patterns**:
- Form validation: Show success/error notifications in callbacks.
- Long operations: Loading notifications during async tasks.
- User feedback: Confirm actions with brief notifications.

### MantineModals
**Overview**: Stackable modal system with transitions, focus management, and customization options.

**Basic Modal**:
```python
dmc.Modal(
    opened=modal_open,
    onClose=lambda: setattr(modal, 'opened', False),
    title="Modal Title",
    children=[
        dmc.Text("Modal content goes here"),
        dmc.Button("Close", onClick=lambda: setattr(modal, 'opened', False))
    ]
)
```

**Advanced Features**:
- **Nested Modals**: Support for multiple modal layers with proper z-index management.
- **Custom Sizes**: `size` prop for responsive dimensions ("sm", "md", "lg", "xl", or custom).
- **Transitions**: Built-in slide, fade, and scale transitions.
- **Focus Trap**: Automatic focus management for accessibility.

**Modal Props**:
- `opened` (bool, required): Controls modal visibility.
- `onClose` (callable, required): Close handler.
- `title` (str): Modal title.
- `size` (str | int): Modal size.
- `centered` (bool): Center modal vertically.
- `overlayProps` (dict): Overlay customization.
- `transitionProps` (dict): Transition configuration.

**Integration Patterns**:
- Confirm dialogs: Delete confirmations, form warnings.
- Forms: Complex data entry in dedicated modal.
- Media viewers: Image galleries, video players.

### MantinePopover
**Overview**: Hover or click-activated popover with rich content support and positioning options.

**Basic Usage**:
```python
dmc.Popover(
    width=300,
    position="bottom",
    withArrow=True,
    target=dmc.Button("Click me"),
    dropdown=dmc.Text("Popover content")
)
```

**Popover Props**:
- `position` (str): Position relative to target ("bottom", "top", "left", "right").
- `withArrow` (bool): Show arrow pointing to target.
- `width` (int | str): Popover width.
- `offset` (int): Distance from target in px.
- `opened` (bool): Controlled open state.
- `onClose` (callable): Close handler.
- `target` (component): Element that triggers popover.

**Advanced Features**:
- **Controlled Mode**: Manual state management via `opened` prop.
- **Hover Activation**: Automatic show/hide on hover.
- **Click Activation**: Toggle on click, close on outside click.
- **Nested Popovers**: Support for hierarchical information display.

**Integration Patterns**:
- Tooltips: Enhanced tooltips with rich content.
- Actions: Context menus, quick actions.
- Forms: Mini-forms within popovers.

### MantineDrawer
**Overview**: Slide-out panels from screen edges with responsive behavior and content lazy loading.

**Basic Usage**:
```python
dmc.Drawer(
    opened=drawer_open,
    onClose=lambda: setattr(drawer, 'opened', False),
    title="Navigation",
    position="left",
    size=300,
    children=[
        dmc.NavLink("Home", href="/"),
        dmc.NavLink("Settings", href="/settings"),
        dmc.NavLink("Profile", href="/profile")
    ]
)
```

**Drawer Props**:
- `opened` (bool, required): Controls drawer visibility.
- `onClose` (callable, required): Close handler.
- `position` (str, default="right"): Slide direction ("left", "right", "top", "bottom").
- `size` (int | str, default="100%"): Drawer size.
- `overlayProps` (dict): Overlay customization.
- `transitionProps` (dict): Transition configuration.

**Advanced Features**:
- **Responsive Design**: Automatic adaptation to screen size.
- **Lazy Loading**: Content loads only when drawer opens.
- **Touch Support**: Swipe gestures for mobile devices.

**Integration Patterns**:
- Navigation: Mobile navigation menus.
- Settings: App settings and preferences.
- Filters: Advanced filter panels.

---

## Advanced Features

### Functions as Props (v2.0+)

#### Function Declaration

**JavaScript:**
```javascript
var dmcfuncs = window.dashMantineFunctions = {};

dmcfuncs.formatCurrency = function(value, options) {
    const currency = options.currency || 'USD';
    return `${currency} ${value:.2f}`;
};

dmcfuncs.isWeekday = function(dateStr) {
    const date = dayjs(dateStr, "YYYY-MM-DD");
    return date.day() !== 5;
};
```

**Python Usage:**
```python
dmc.Button(
    label={"function": "formatCurrency", "options": {"unit": "USD"}},
    value=25
)
```

#### Supported Components & Props

| Component | Supported Props |
|-------------|---------------|
|-------------|
| Button | `label`, `scale` |
|-------------|
| Slider | `label`, `scale` |
|-------------|
| Select | `renderOption`, `filter` |
|-------------|
| MultiSelect | `renderOption`, `filter` |
|-------------|
| Date Components | `disabledDates` |
|-------------|
| Charts | `valueFormatter`, `tooltipProps` |

#### Advanced Usage

**React Components:**
```javascript
// Returning custom components
dmc.Badge(
    React.createElement(
        dmc.Badge,
        {"color": "red", "variant": "filled"},
        children: "New"
    )
)

// Custom tooltip with rich content
dmc.Tooltip(
    label="Rich tooltip",
    children=[
        dmc.Text("Click for details")
    ]
)
```

**Performance Considerations:**
- Cache expensive calculations in functions
- Use `lru_cache` for frequently called functions
- Test function return types carefully
- Avoid inline functions for simple formatting

---

### Rich Text Editor

#### Complete Editor Setup

**Core Features:**
- **Tiptap 3 Integration**: Latest rich text editing capabilities
- **Code Highlighting**: Built-in syntax highlighting
- **Client-Side Access**: `getEditor(id)` function
- **Focus Control**: `focus` and `editable` props
- **Auto-Save**: Debounced saving support
- **Custom Toolbar**: Customizable toolbar controls

**Basic Usage:**
```python
dmc.RichTextEditor(
    id="editor",
    value="<p>Hello <strong>Hello</strong></p>",
    placeholder="Start typing...",
    editable=True,
    toolbar=[
        "bold", "italic", "underline",
        "h1", "h2", "h3",
        "link", "image",
        "code"
    ]
)
```

**Advanced Configuration:**
```python
dmc.RichTextEditor(
    plugins=[
        "history", "bold", "italic", "link", "table"
    ],
    stickyHeader=True,
    stickyFooter=True,
    characters="all",
    spellcheckSpelling=true
    placeholder="Start typing...",
    styles={{
        "content": {
            backgroundColor: "#f8f8fa"
        }
    }
)
```

#### Client-Side Functions

**Access Editor State:**
```javascript
// In assets/custom.js
const editor = dash_mantine_components.getEditor('editor-id');
if (editor) {
    const html = editor.getHTML();
    console.log('Current editor content:', html);
}
```

**Enhanced Function Support:**
```python
# Use with external libraries
app = Dash(
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/prismjs@2.0.2/prism.min.js"]
)

# In JavaScript
import {prismjs} from "prismjs";
import {h} from "prismjs";

dmc.Prism(
    language="python",
    children="print('Hello <mark>Hello</mark>')
)
)
```

#### Custom Controls

**Toolbar Extensions:**
```python
# Custom toolbar with save/load functionality
toolbar = [
    [
        'save', 'load', 'download',
        'clear'
    ],
    ["separator"],
    ["bold", "italic", "underline"],
    ["separator"],
    ["h1", "h2", "h3"],
    ["separator"],
    ["link", "image"]
]
]

# Dynamic toolbar via callback
@callback(
    Output("editor-toolbar", "children"),
    Input("add-control", "n_clicks")
)
def update_toolbar(add_control, n_clicks):
    if add_control in add_control:
        toolbar.append('save')
    elif n_clicks > 0 and clear_control in add_control:
        toolbar.remove('clear')
    return toolbar
```

---

## Styling and Theming

### Complete Theme Configuration

**Core Properties:**
```python
theme = {
    "colorScheme": "light",  # "dark", "auto"
    "primaryColor": "blue",
    "fontFamily": "Inter, sans-serif",
    "headings": {
        "fontFamily": "Inter, sans-serif",
        "sizes": {
            "h1": {"fontSize": 34, "fontWeight": 700},
            "h2": {"fontSize": 26, "fontWeight": 600},
            # ... other heading styles
        }
    },
        "colors": {
            "dark": ["#1c1c1d", "#a8a7b7"], # 10 shades
            "gray": ["#C1C2C5", "#A8AAB7"], # 10 shades
            "red": ["#fff5f5", "#fccdd2"], # 10 shades
        },
        "grape": ["#f0fff4", "#c8f9fa"], # 10 shades
        "indigo": ["#e8eaf6", "#d6bc3d"]  # 10 shades
        "blue": ["#E3F2FD", "#BBDEFB"]      # 10 shades
    },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px"
        },
        "radius": {
            "xs": "2px",
            "sm": "4px",
            "md": "8px",
            "lg": "12px",
            "xl": "16px"
        }
    },
    "components": {
        "Button": {
            "styles": {
                "root": {
                    "fontWeight": 600,
                    "textTransform": "uppercase"
                }
            },
            "TextInput": {
                "styles": {
                    "input": {
                        "borderColor": "var(--mantine-color-blue-6)"
                    }
                }
            }
        }
    }
}
```

### Dark Mode Implementation

#### Auto Theme Detection
```python
# Auto system theme detection
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "auto"}
)

# Manual theme toggle
@callback(
    Output("theme-provider", "theme"),
    Input("theme-toggle", "value")
)
def toggle_theme(is_dark):
    return {
        "colorScheme": "dark" if is_dark else "light"
    }
```

#### Custom Color Schemes
```python
# Custom color palette
theme = {
    "colors": {
        "brand": ["#fffef5", "#f8fafc", "#fee2d5"], # Light theme colors
        "accent": ["#f0f4a", "#d6bcd6"], # Accent colors
        "complementary": ["#e3f2fd", "#cfe3f0"] # Complementary colors
    },
    "primary": "indigo",
    "secondary": "teal"
    }
}
```

### Component Style Overrides

**Global Style Overrides:**
```python
dmc.MantineProvider(
    theme={
        "components": {
            "Button": {
                "styles": {
                    "root": {
                        "fontWeight": 600,
                        "textTransform": "uppercase"
                    }
                }
            }
        }
    }
    },
    children=[...]
)
```

**Individual Component Styling:**
```python
# Using style props
dmc.Button(
    style={"color": "#428af0"},
    sx={(theme) => ({
        "&:hover": {"color": "var(--mantine-color-blue-6)"}
    })
)

# Using sx for advanced styling
dmc.Button(
    sx={(theme) => ({
        "&:hover": {"backgroundColor": theme.fn.colors.blue[0]}
    })
)
```

### CSS Integration

**Global Variables:**
```css
:root {
    --mantine-color-blue-6: #428af0;
    --mantine-color-dark-6: #1c1c1e;
}
```

**Component CSS Classes:**
```css
.custom-text-input {
    border-color: var(--mantine-color-blue-6);
}
.mantine-focus {
    outline: none !important;  /* Remove focus outline */
}
.mantine-focus:focus {
    border-color: var(--mantine-color-blue-4);
}
```

---

## Performance Optimization

### Virtualization Techniques

**Large Dataset Handling:**
```python
# For datasets with 1000+ rows
@callback(
    Output("table-data", "data"),
    Input("page", "value"),
    [State("table-data", "data")],
    prevent_initial_call=True
)
def paginate_table(page, stored_data):
    start = (page - 1) * 100
    return stored_data[start:start + 100]
```

**Lazy Component Loading:**
```python
# Async loading for heavy components
import dash

@callback(
    Output("heavy-component", "children"),
    Input("load-btn", "n_clicks"),
    Input("heavy-component", "n_clicks")
)
def load_heavy_component(n_clicks):
    if n_clicks > 0:
        return dmc.HeavyComponent()
    return None
```

### Memory Management

**State Store for Complex Forms:**
```python
# Use dcc.Store for form data state
dcc.Store(id="form-state", data={
    "username": "",
    "password": "",
    "preferences": []
}, clear_data=False)
```

### Bundle Optimization

**External Scripts:**
```python
app = Dash(
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dayjs@1.10.8/dayjs.min.js",
    "https://cdn.jsdelivr.net/npm/mdi-material/5.0.0/mdi.js"
    ]
)
```

### Debouncing

**User Input Debouncing:**
```python
from dash_extensions.javascript import debounce

@app.callback(
    Output("filtered-data", "children"),
    Input("search-input", "value"),
    debounce=300
)
def filter_data(search):
    return [item for item in all_items if search.lower() in item["name"].lower()]

# Input debouncing
dmc.TextInput(
    debounce=True,
    debounce=500,  # 500ms
    id="debounced-input"
)
```

---

## Complete Integration Examples

### Real-world Dashboard Example

```python
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc

# Sales Dashboard Example
def create_sales_dashboard():
    sales_df = pd.DataFrame({
        "month": ["Jan", "Feb", "Mar"],
        "product": ["A", "B", "C"],
        "region": ["North", "South", "East", "West"],
        "sales": [1000, 1200, 900, 650]
    })

    return dmc.MantineProvider([
        dmc.Container(size="lg", px="md", children=[
            dmc.Title("Sales Dashboard", order=1),
            dmc.Grid(gutter="lg", children=[
                dmc.Col(span=4, children=[
                    dmc.Card(
                        shadow="sm",
                        children=[
                            dmc.Text("North Sales"),
                            dmc.Text("$50,000")
                        ]
                    ),
                    dmc.Card(
                        shadow="sm",
                        children=[
                            dmc.Text("Europe Sales"),
                            dmc.Text("$80,000")
                        ]
                    ),
                    dmc.Col(span=4, children=[
                        dmc.Card(
                        shadow="sm",
                        children=[
                            dmc.Text("$70,000")
                        ]
                    )
                ]
            )
        ]),
        dmc.Grid(gutter="md", children=[
            dmc.Col(span=12, children=[
                dmc.Card(
                    shadow="md",
                    children=[dmc.Text("Monthly Summary")]),
                dmc.Card(
                    shadow="md",
                    children=[dmc.Text("Details View")])
                ),
                dmc.Col(span=12, children=[
                    dmc.Card(
                        shadow="md",
                        children=[dmc.Text("Export Options")],
                        children=[
                            dmc.Button("Export", variant="outline")
                        ]
                    )
                )
            ])
        ])
    ])

# Complex Callback Pattern
@callback(
    Output("chart-data", "data"),
    Input("refresh-btn", "n_clicks"),
    Input("region-filter", "value")
)
)
def refresh_chart(region_filter, refresh_n_clicks):
    if refresh_n_clicks > 0:
        return get_sales_data(region)
    else:
        return get_sales_data()
```

### Navigation Example

**Navigation with Accordion and Tabs:**
```python
dmc.NavigationNavigation(
    dmc.Navbar(
        dmc.NavLink("Dashboard", href="/dashboard"),
        dmc.NavLink("Reports", href="/reports", target="_blank"),
        dmc.NavLink("Settings", href="/settings")
    ),
    dmc.Tabs([
        dmc.TabsList([
            dmc.Tab(value="overview", label="Overview", icon="home"),
            dmc.Tab(value="analytics", label="Analytics", icon="analytics-chart"),
            dmc.Tab(value="reports", label="Reports", icon="analytics-chart")
        ])
    ])
```

### File Upload Example

```python
import dash
from dash import dcc

app.layout = html.Div([
    dcc.Upload(
        id="file-upload",
        accept=".json,.csv",
        multiple=True,
        showlabel=False,
        text="Upload JSON/CSV"
    ),
    html.Div(id="upload-status")
])

@callback(
    Output("upload-status", "children"),
    Input("file-upload", "contents"),
    prevent_initial_call=True
)
def handle_upload(contents):
    try:
        # Process files here
        files = [json.loads(f) for f in contents if f.strip() for f in contents]
        return "Upload complete!"
    except:
        return "Upload failed!"
```

### Data Integration

**Dashboard with Multiple Data Sources:**
```python
# Database query callback
@app.callback(
    Output("table-data", "data"),
    Input("date-range", "start_date"),
    Input("region-filter", "value")
)
)
def load_dashboard(start_date, region):
    # Load data based on filters
    if region and start_date:
        start_date = date
    return get_sales_data(start_date, region)
    return get_all_data()  # Return all if no filters

# API integration
@callback(
    Output("api-data", "data"),
    Input("api-refresh", "n_clicks")
)
def fetch_api_data():
    # Fetch from API
    return requests.get("https://api.example.com/data").json")
```

### Real-time Updates

**WebSocket Integration:**
```python
# App with WebSocket connection
@callback(
    Output("live-table", "children"),
    Input("ws-message", "n_messages")
)
def update_live_data(n_messages):
    try:
        messages = [json.loads(msg) for msg in n_messages]
        return messages[-1]
    except:
        return n_messages

# Periodic updates
dcc.Interval(
    id="timer",
    interval=5000,  # 5 seconds
    n_intervals=0,
    interval=1000,  # 1 second
)
    components=[dmc.Text(id="live-table", children="Live Updates")],
    dcc.Store(id="live-data", data=[])
)
)
```

---

## Additional Guides, Tutorials, & Best Practices

### Guides & Tutorials

#### Theming Guide
**Overview**: Customize global theme with `MantineProvider` for consistent branding and user experience.

**Basic Theme Setup**:
```python
import dash_mantine_components as dmc

theme = {
    "colorScheme": "light",
    "primaryColor": "blue",
    "fontFamily": "Inter, sans-serif",
    "headings": {
        "fontFamily": "Inter, sans-serif",
        "sizes": {
            "h1": {"fontSize": "2.5rem", "fontWeight": 700},
            "h2": {"fontSize": "2rem", "fontWeight": 600},
        }
    },
    "colors": {
        "brand": "#0066FF",
        "brandHover": "#0052CC",
    },
    "spacing": {
        "xs": "4px",
        "sm": "8px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
    }
}

app.layout = dmc.MantineProvider(
    theme=theme,
    children=[
        # Your app content
    ]
)
```

**Advanced Customization**:
```python
# Dark mode toggle
theme = {
    "colorScheme": "dark" if is_dark_mode else "light",
    "primaryColor": "blue",
    "components": {
        "Button": {
            "styles": {
                "root": {
                    "borderRadius": "8px",
                    "textTransform": "none"
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
}

# Dynamic theme updates
@app.callback(
    Output("app-container", "theme"),
    Input("theme-toggle", "checked")
)
def update_theme(is_dark):
    return {
        "colorScheme": "dark" if is_dark else "light",
        "primaryColor": "blue"
    }
```

**Theme Integration Patterns**:
- **Brand Integration**: Match company colors and typography
- **User Preferences**: Store theme choice in local storage or user profile
- **Accessibility**: Respect system color scheme preferences
- **Component Overrides**: Customize specific component styles globally

#### Performance Optimization Tutorial

**Benchmark Testing Setup**:
```python
import time
import psutil
from functools import wraps

def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss

        result = func(*args, **kwargs)

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss

        print(f"{func.__name__}: {end_time - start_time:.3f}s, "
              f"Memory: {(end_memory - start_memory) / 1024 / 1024:.1f}MB")

        return result
    return wrapper

# Usage with large datasets
@measure_performance
def render_large_dataset(data):
    return dmc.DataTable(
        data=data,
        columns=[{"name": i, "id": i} for i in data[0].keys()],
        pagination=True,
        pageSize=50
    )
```

**Optimization Techniques**:

1. **Virtual Scrolling**:
```python
def render_virtualized_list(items):
    return dmc.ScrollArea(
        h=400,
        children=[
            dmc.Box(
                h=len(items) * 40,  # Total height
                children=[
                    # Render only visible items
                ]
            )
        ]
    )
```

2. **Memoization**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param1, param2):
    # Heavy computation
    return result

# Use in callbacks
@app.callback(Output("result", "children"), Input("input", "value"))
def compute(value):
    return expensive_calculation(value, additional_param)
```

3. **Lazy Loading**:
```python
import dash

app.layout = html.Div([
    dcc.Loading(
        id="loading",
        children=[
            html.Div(id="content")
        ],
        type="circle"
    )
])

@app.callback(
    Output("content", "children"),
    Input("trigger", "n_clicks")
)
def load_heavy_content(n_clicks):
    if n_clicks:
        # Load expensive components only when needed
        return dmc.Grid([
            dmc.Col(dmc.Text("Heavy content"), span=6)
        ])
    return "Click to load content"
```

**Performance Monitoring**:
```python
# Add performance monitoring to production
@app.callback(
    Output("performance-metrics", "children"),
    Input("page-load", "timestamp")
)
def track_performance(load_time):
    metrics = {
        "load_time": load_time,
        "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,
        "render_time": None  # Measure in component
    }
    return html.Pre(json.dumps(metrics, indent=2))
```

#### Accessibility (a11y) Guide

**Screen Reader Testing**:
```python
# Accessible form setup
dmc.Group([
    dmc.TextInput(
        id="search",
        label="Search products",
        description="Type to search for products",
        aria_label="Product search input",
        autoComplete="off"
    ),
    dmc.Button(
        "Search",
        aria_label="Submit search query"
    )
])
```

**Keyboard Navigation**:
```python
dmc.VisitorKey(
    keyBindings={
        "Enter": lambda: perform_search(),
        "Escape": lambda: clear_search(),
        "ArrowDown": lambda: focus_next_result(),
        "ArrowUp": lambda: focus_previous_result()
    },
    children=[
        dmc.TextInput(id="search-input", placeholder="Press Enter to search"),
        dmc.List(id="search-results", children=[])
    ]
)
```

**Focus Management**:
```python
# Modal with proper focus trap
dmc.Modal(
    opened=True,
    children=[
        dmc.FocusTrap(
            active=True,
            initialFocus="first-input",
            children=[
                dmc.TextInput(id="first-input", label="First Name"),
                dmc.TextInput(id="second-input", label="Last Name"),
                dmc.Button("Submit")
            ]
        )
    ]
)
```

**ARIA Labeling**:
```python
dmc.DataTable(
    data=table_data,
    columns=[
        {"name": "Product", "id": "product", "aria_label": "Product name"},
        {"name": "Price", "id": "price", "aria_label": "Product price"}
    ],
    aria_label="Product inventory table"
)
```

#### Internationalization (i18n) Tutorial

**Multi-language Setup**:
```python
import json

# Translation dictionaries
translations = {
    "en": {
        "welcome": "Welcome",
        "submit": "Submit",
        "cancel": "Cancel",
        "loading": "Loading..."
    },
    "es": {
        "welcome": "Bienvenido",
        "submit": "Enviar",
        "cancel": "Cancelar",
        "loading": "Cargando..."
    },
    "fr": {
        "welcome": "Bienvenue",
        "submit": "Soumettre",
        "cancel": "Annuler",
        "loading": "Chargement..."
    }
}

# Language context
app.layout = html.Div([
    dcc.Store(id="language-store", data="en"),
    dmc.Group([
        dmc.Button(
            "English",
            onClick=lambda: set_language("en")
        ),
        dmc.Button(
            "Español",
            onClick=lambda: set_language("es")
        ),
        dmc.Button(
            "Français",
            onClick=lambda: set_language("fr")
        )
    ]),
    html.Div(id="localized-content")
])

@app.callback(
    Output("localized-content", "children"),
    Input("language-store", "data")
)
def render_localized_content(lang):
    t = translations[lang]
    return dmc.Container([
        dmc.Title(t["welcome"]),
        dmc.Group([
            dmc.Button(t["submit"]),
            dmc.Button(t["cancel"], variant="outline")
        ])
    ])
```

**Date/Number Formatting**:
```python
import locale

def format_number(value, language="en"):
    try:
        locale.setlocale(locale.LC_ALL, f"{language}_{language.upper()}.UTF-8")
        return locale.format_string("%d", value, grouping=True)
    except:
        return f"{value:,}"

def format_date(date, language="en"):
    if language == "es":
        return date.strftime("%d/%m/%Y")
    elif language == "fr":
        return date.strftime("%d/%m/%Y")
    else:
        return date.strftime("%m/%d/%Y")
```

### Advanced Usage Patterns

#### State Management Patterns
**Complex Form State**:
```python
import dash
from dash import dcc, html, Input, Output, State

app.layout = html.Div([
    dcc.Store(id="form-state", data={}),
    dcc.Store(id="validation-state", data={}),

    dmc.Form([
        dmc.TextInput(
            id="name",
            label="Name",
            error=False  # Will be updated dynamically
        ),
        dmc.TextInput(
            id="email",
            label="Email",
            error=False
        ),
        dmc.NumberInput(
            id="age",
            label="Age",
            min=18,
            max=120
        ),
        dmc.Group([
            dmc.Button("Submit", id="submit-btn"),
            dmc.Button("Reset", id="reset-btn", variant="outline")
        ])
    ]),

    html.Div(id="form-errors")
])

@app.callback(
    [Output("name", "error"),
     Output("email", "error"),
     Output("age", "error"),
     Output("form-errors", "children")],
    [Input("name", "value"),
     Input("email", "value"),
     Input("age", "value")]
)
def validate_form(name, email, age):
    errors = []
    name_error = False
    email_error = False
    age_error = False

    if not name or len(name.strip()) < 2:
        name_error = "Name must be at least 2 characters"
        errors.append("Name must be at least 2 characters")

    if not email or "@" not in email:
        email_error = "Valid email required"
        errors.append("Valid email required")

    if not age or age < 18:
        age_error = "Must be 18 or older"
        errors.append("Must be 18 or older")

    error_display = dmc.Alert(
        "Please fix the following errors:\n" + "\n".join(f"- {e}" for e in errors),
        color="red",
        children=[]
    ) if errors else None

    return name_error, email_error, age_error, error_display
```

**Multi-step Forms**:
```python
app.layout = html.Div([
    dcc.Store(id="wizard-data", data={}),
    dcc.Store(id="wizard-step", data=1),

    dmc.Stepper(
        id="form-wizard",
        active=1,
        children=[
            dmc.Stepper.Step(
                label="Personal Info",
                description="Basic information"
            ),
            dmc.Stepper.Step(
                label="Preferences",
                description="Your preferences"
            ),
            dmc.Stepper.Step(
                label="Review",
                description="Review and submit"
            )
        ]
    ),

    html.Div(id="step-content"),

    dmc.Group([
        dmc.Button("Previous", id="prev-btn", disabled=True),
        dmc.Button("Next", id="next-btn"),
        dmc.Button("Submit", id="submit-btn", style={"display": "none"})
    ])
])

@app.callback(
    [Output("step-content", "children"),
     Output("prev-btn", "disabled"),
     Output("next-btn", "style"),
     Output("submit-btn", "style")],
    Input("wizard-step", "data")
)
def render_wizard_step(step):
    if step == 1:
        return [
            dmc.Form([
                dmc.TextInput(id="first-name", label="First Name"),
                dmc.TextInput(id="last-name", label="Last Name"),
                dmc.NumberInput(id="age", label="Age")
            ])
        ], True, {}, {"display": "none"}
    elif step == 2:
        return [
            dmc.Form([
                dmc.Select(id="theme", label="Theme", data=[
                    {"value": "light", "label": "Light"},
                    {"value": "dark", "label": "Dark"}
                ]),
                dmc.Checkbox(id="notifications", label="Enable notifications")
            ])
        ], False, {}, {"display": "none"}
    else:
        return [
            dmc.Alert("Review your information before submitting", color="blue"),
            # Show summary of all data
        ], False, {"display": "none"}, {}
```

#### Custom Hooks and Functions
**Reusable Data Fetching**:
```python
# assets/custom.js
window.dashMantineFunctions = window.dashMantineFunctions || {};

dashMantineFunctions.fetchUserData = async function(userId, options) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        return null;
    }
};

dashMantineFunctions.formatCurrency = function(amount, options) {
    const currency = options.currency || 'USD';
    const locale = options.locale || 'en-US';

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount);
};

# Python usage
dmc.DataTable(
    data=user_data,
    columns=[
        {
            "name": "Salary",
            "id": "salary",
            "format": {"function": "formatCurrency", "options": {"currency": "USD"}}
        }
    ]
)
```

**Error Boundaries**:
```python
# assets/error-boundary.js
class DMLErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('DMC Error Boundary caught an error:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return dmc.Alert(
                "Something went wrong. Please refresh the page.",
                color="red",
                title="Error",
                children=[
                    dmc.Button("Refresh", onClick={() => window.location.reload()})
                ]
            );
        }

        return this.props.children;
    }
}

// Register the error boundary
window.DMLErrorBoundary = DMLErrorBoundary;
```

#### Testing Strategies
**Component Testing**:
```python
import pytest
from dash.testing.composite import DashComposite
import dash_mantine_components as dmc

def test_button_rendering(dash_duo):
    app = dash.Dash(__name__)

    app.layout = dmc.Button(
        "Test Button",
        id="test-button",
        color="blue"
    )

    dash_duo.start_server(app)

    # Check if button is rendered
    button = dash_duo.find_element("#test-button")
    assert button.text == "Test Button"

    # Test click interaction
    button.click()

    # Check for any state changes
    dash_duo.wait_for_text_to_equal("#test-button", "Test Button")

def test_form_validation(dash_duo):
    app = dash.Dash(__name__)

    app.layout = dmc.Form([
        dmc.TextInput(
            id="email-input",
            label="Email",
            required=True
        ),
        html.Div(id="error-message")
    ])

    @app.callback(
        Output("error-message", "children"),
        Input("email-input", "value")
    )
    def validate_email(email):
        if email and "@" not in email:
            return dmc.Text("Invalid email format", color="red")
        return ""

    dash_duo.start_server(app)

    # Find email input
    email_input = dash_duo.find_element("#email-input")

    # Test invalid email
    email_input.send_keys("invalid-email")
    dash_duo.wait_for_text_to_equal("#error-message", "Invalid email format")

    # Test valid email
    email_input.clear()
    email_input.send_keys("test@example.com")
    dash_duo.wait_for_text_to_equal("#error-message", "")
```

### Integration Examples

#### With Plotly Dash
**Hybrid Dashboard**:
```python
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc

app.layout = dmc.Container([
    dmc.Title("Analytics Dashboard"),

    dmc.Grid([
        dmc.Col([
            dmc.Card([
                dmc.Text("Revenue Trend"),
                dcc.Graph(id="revenue-chart")
            ])
        ], span=8),

        dmc.Col([
            dmc.Card([
                dmc.Text("Key Metrics"),
                dmc.Stack([
                    dmc.Text(id="total-revenue"),
                    dmc.Text(id="growth-rate"),
                    dmc.Text(id="active-users")
                ])
            ])
        ], span=4)
    ]),

    dmt.Select(
        id="time-range",
        label="Time Range",
        data=[
            {"value": "7d", "label": "Last 7 days"},
            {"value": "30d", "label": "Last 30 days"},
            {"value": "90d", "label": "Last 90 days"}
        ],
        value="30d"
    )
])

@app.callback(
    [Output("revenue-chart", "figure"),
     Output("total-revenue", "children"),
     Output("growth-rate", "children"),
     Output("active-users", "children")],
    Input("time-range", "value")
)
def update_dashboard(time_range):
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30 if time_range == "30d" else 90)
    revenue = np.random.randint(1000, 5000, size=len(dates))

    # Create Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=revenue, mode='lines+markers'))
    fig.update_layout(title="Revenue Trend", xaxis_title="Date", yaxis_title="Revenue ($)")

    # Calculate metrics
    total_revenue = sum(revenue)
    growth_rate = ((revenue[-1] - revenue[0]) / revenue[0]) * 100
    active_users = np.random.randint(100, 1000)

    return (
        fig,
        dmc.Text(f"Total Revenue: ${total_revenue:,.0f}", size="lg", weight="bold"),
        dmc.Text(f"Growth Rate: {growth_rate:.1f}%",
                 color="green" if growth_rate > 0 else "red"),
        dmc.Text(f"Active Users: {active_users:,}")
    )
```

#### With Backend APIs
**Real-time Data Integration**:
```python
import requests
import dash
from dash import dcc, html, Input, Output, Interval
import dash_mantine_components as dmc

API_BASE_URL = "https://api.example.com"

def fetch_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API Error: {e}")
        return None

app.layout = dmc.Container([
    dmc.Title("Live API Dashboard"),

    dmc.Grid([
        dmc.Col([
            dmc.Card([
                dmc.Group([
                    dmc.Loader(),
                    dmc.Text("Live Data", id="live-status")
                ]),
                html.Div(id="api-data")
            ])
        ], span=6),

        dmc.Col([
            dmc.Card([
                dmc.Text("API Health"),
                dmc.Progress(
                    id="api-health",
                    value=0,
                    color="green"
                )
            ])
        ], span=6)
    ]),

    Interval(
        id="update-interval",
        interval=5000,  # Update every 5 seconds
        n_intervals=0
    )
])

@app.callback(
    [Output("live-status", "children"),
     Output("api-data", "children"),
     Output("api-health", "value")],
    Input("update-interval", "n_intervals")
)
def update_live_data(n):
    # Fetch live data from API
    data = fetch_api_data("live-stats")

    if data:
        status = "Connected"
        health = 100

        # Format data for display
        content = dmc.Stack([
            dmc.Text(f"Users Online: {data.get('users_online', 0)}"),
            dmc.Text(f"Server Load: {data.get('server_load', 0)}%"),
            dmc.Text(f"Response Time: {data.get('response_time', 0)}ms"),
            dmc.Text(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        ])
    else:
        status = "Connection Error"
        health = 0
        content = dmc.Alert(
            "Failed to fetch data from API",
            color="red",
            children=[]
        )

    return status, content, health
```

---

## Best Practices Summary

### Performance
- Use `dcc.Loading` for async operations
- Implement virtualization for large datasets
- Cache expensive computations
- Use debouncing for frequent inputs
- Optimize bundle size with selective imports
- Monitor memory usage and render times
- Implement lazy loading for heavy components

### Accessibility
- Always include `label` for form inputs
- Use semantic HTML elements
- Test with screen readers
- Implement proper ARIA labels
- Provide keyboard navigation
- Use focus traps in modals and overlays
- Maintain proper color contrast ratios

### Error Handling
- Comprehensive validation in callbacks
- User-friendly error messages
- Graceful degradation
- Implement error boundaries
- Log errors appropriately (not sensitive data)
- Provide recovery mechanisms

### Security
- Sanitize all user inputs
- Use HTTPS for external resources
- Never log sensitive data in production
- Implement proper authentication/authorization
- Validate API responses
- Use Content Security Policy headers

### Development
- Use version control (pin dependencies)
- Implement comprehensive testing (unit, integration, e2e)
- Use TypeScript for type safety
- Document all custom functions
- Follow consistent naming conventions
- Implement proper state management
- Use environment variables for configuration

### Deployment
- Containerize applications with Docker
- Use reverse proxy (nginx) for production
- Implement proper logging and monitoring
- Set up health checks
- Use CDN for static assets
- Implement proper backup strategies

### Support Resources
- **Documentation**: https://www.dash-mantine-components.com
- **GitHub**: https://github.com/snehilvj/dash-mantine-components
- **Discord**: https://discord.gg/KuJkh4Pyq5
- **Forum**: https://community.plotly.com/
- **Mantine Docs**: https://mantine.dev/
- **Dash Docs**: https://dash.plotly.com/

---

*This documentation is compiled from the official Dash Mantine Components GitHub repository, PyPI package information, and comprehensive documentation extraction. For the most up-to-date information, visit https://www.dash-mantine-components.com.*
