# Dash Mantine Components - Comprehensive Documentation

## Overview

**Dash Mantine Components** is an extensive (90+) Dash components library based on [Mantine](https://mantine.dev/) React Components Library. It makes it easier to create high-quality dashboards with well-designed components out of the box.

- **Current Version**: 2.4.0 (released November 6, 2025)
- **License**: MIT
- **Author**: Snehil Vij <snehilvj@outlook.com>
- **Repository**: https://github.com/snehilvj/dash-mantine-components
- **Documentation**: https://www.dash-mantine-components.com
- **PyPI**: https://pypi.org/project/dash-mantine-components/

## Installation

```bash
pip install dash-mantine-components
```

## Quick Start Example

```python
import dash
from dash import Dash, Input, Output, callback, html, no_update
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

## Key Features

### Core Capabilities

- **90+ Components**: Extensive component library covering most UI needs
- **Modern Design**: Based on Mantine's React component library with consistent styling
- **Theming Support**: Full light/dark mode support with customizable themes
- **Accessibility**: Built-in accessibility features
- **Dash Integration**: Seamless integration with Plotly Dash callbacks and patterns

### Performance & Features

- **Async Loading**: Charts and code highlight components loaded asynchronously to reduce bundle size
- **Functions as Props**: Support for JavaScript functions in component props (v2.0+)
- **Container Queries**: Support for responsive container-based layouts
- **Rich Text Editing**: Advanced rich text editor with Tiptap integration
- **Data Visualization**: Comprehensive chart components with Recharts integration

## Component Categories

### 1. Forms & Inputs

#### Text Inputs
- **TextInput**: Basic text input field
- **PasswordInput**: Password input with visibility toggle
- **NumberInput**: Numeric input with validation
- **JsonInput**: JSON formatted input with validation
- **TextArea**: Multi-line text input with auto-resize
- **RichTextEditor**: Advanced rich text editor with Tiptap

#### Selection Components
- **Select**: Dropdown selection with search
- **MultiSelect**: Multiple selection with search
- **Autocomplete**: Autocomplete with custom filtering
- **TagsInput**: Tag-based input system
- **Checkbox**: Single checkbox
- **CheckboxGroup**: Group of checkboxes
- **Radio**: Radio button
- **RadioGroup**: Group of radio buttons
- **Switch**: Toggle switch
- **Chip**: Selectable chip
- **ChipGroup**: Group of chips

#### Date & Time
- **DatePickerInput**: Date selection with calendar
- **DateRangePicker**: Date range selection
- **TimeInput**: Time selection
- **TimePicker**: Enhanced time picker
- **DateTimePicker**: Combined date and time selection
- **MonthPickerInput**: Month selection
- **YearPickerInput**: Year selection
- **MiniCalendar**: Compact calendar view

### 2. Layout & Structure

#### Container Components
- **Container**: Responsive container with fluid layout
- **Grid**: Grid system with breakpoints
- **SimpleGrid**: Simplified grid layout
- **Flex**: Flexible box layout
- **Stack**: Vertical/horizontal stacking
- **Center**: Center content alignment
- **Group**: Group components with spacing

#### Navigation & Structure
- **AppShell**: Application shell with header, sidebar, navbar
- **Header**: Application header
- **Navbar**: Navigation sidebar
- **Aside**: Additional sidebar
- **Footer**: Application footer
- **Affix**: Fixed positioning
- **Space**: Spacer component

### 3. Data Display

#### Information Display
- **Text**: Text display with variants
- **Title**: Title with different sizes
- **Heading**: Heading component
- **Badge**: Badge/label component
- **Avatar**: User avatar
- **AvatarGroup**: Multiple avatars
- **Kbd**: Keyboard key display
- **Code**: Inline code display
- **Blockquote**: Quote display
- **Image**: Image display
- **BackgroundImage**: Background image

#### Lists & Tables
- **List**: Unordered/ordered lists
- **ListItem**: List item component
- **Table**: Data table
- **TableScrollContainer**: Scrollable table container

#### Progress & Indicators
- **Progress**: Progress bar
- **RingProgress**: Circular progress
- **SemiCircleProgress**: Semi-circular progress
- **Skeleton**: Loading skeleton
- **LoadingOverlay**: Loading overlay

### 4. Charts & Visualization

#### Chart Components (using Recharts)
- **LineChart**: Line-based data visualization
- **AreaChart**: Area-based charts
- **BarChart**: Bar charts
- **PieChart**: Pie charts
- **DonutChart**: Donut charts
- **ScatterChart**: Scatter plots
- **RadarChart**: Radar/spider charts
- **CompositeChart**: Combined chart types
- **BubbleChart**: Bubble charts

#### Chart Features
- **Multiple Axes**: Support for left, right Y-axes
- **Animations**: Chart animations
- **Interactive Features**: Hover effects, click callbacks
- **Custom Styling**: Colors, gradients, and themes
- **Value Formatting**: Custom value formatters
- **Tooltips**: Interactive tooltips

### 5. Feedback & Interaction

#### Overlays & Modals
- **Modal**: Modal dialogs
- **ModalStack**: Stacked modals with managed state
- **Drawer**: Slide-out panels
- **DrawerStack**: Stacked drawers
- **Popover**: Popover tooltips
- **Tooltip**: Tooltips with positioning
- **FloatingTooltip**: Floating tooltips
- **HoverCard**: Hover-activated cards

#### Notifications & Alerts
- **NotificationContainer**: Modern notification system
- **Notification**: Individual notifications
- **Alert**: Alert boxes
- **ActionIcon**: Icon buttons
- **Button**: Enhanced buttons
- **ButtonGroup**: Button groups

#### Navigation & Interaction
- **Carousel**: Image/content carousel
- **Tabs**: Tabbed content
- **Accordion**: Collapsible sections
- **Stepper**: Step-by-step navigation
- **Timeline**: Timeline display
- **Tree**: Hierarchical tree structure
- **Pagination**: Page navigation

### 6. Advanced Components

#### Code & Syntax
- **CodeHighlight**: Syntax highlighting
- **CodeHighlightTabs**: Tabbed code display
- **InlineCodeHighlight**: Inline code highlighting

#### Media & Content
- **Spoiler**: Expandable content
- **Highlight**: Text highlighting
- **Mark**: Text marking
- **MediaQuery**: Responsive design utilities

#### Utilities
- **NotificationContainer**: Advanced notification management
- **DirectionProvider**: RTL text direction support
- **CopyButton**: Ready-to-use copy functionality
- **CustomCopyButton**: Advanced copy functionality

## Advanced Features

### Functions as Props (v2.0+)

Components can now accept JavaScript functions via a sophisticated system that allows safe execution of custom JavaScript in Dash applications.

#### How Function Props Work

In JavaScript libraries like Mantine, some component props accept functions for dynamic formatting, custom rendering, or behavior control. Dash Mantine Components enables this through named function references:

```python
# Define in assets/custom.js
var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};

dmcfuncs.formatTemp = function(value, options) {
    const unit = options.unit || 'C';
    return `${value}°${unit}`;
};

# Use in component
dmc.Slider(
    label={"function": "formatTemp", "options": {"unit": "F"}},
    value=25
)
```

#### Supported Function Props

**Core Components (v2.0+):**
- **Slider/RangeSlider**: `label`, `scale`
- **Select/MultiSelect/TagsInput**: `renderOption`, `filter`
- **Date Components**: `disabledDates`
- **Bar Charts**: `getBarColor`, `valueFormatter`, `tooltipProps`
- **All Charts**: `valueFormatter`, `tooltipProps`

**Additional Support (v2.1.0+):**
- **AutoComplete**: `renderOption`, `filter`
- **Date Components**: `getYearControlProps`, `getMonthControlProps`, `getDayProps`, `renderDay`
- **Tree**: `renderNode`

**Chart Enhancements (v2.4.0+):**
- **AreaChart, BarChart, BubbleChart, CompositeChart, LineChart, ScatterChart**: `xAxisProps`, `yAxisProps`, `gridProps`, `rightYAxisProps`
- **BubbleChart**: `zAxisProps`

#### Advanced Function Usage

**Returning Components:**
Functions can return React components using `React.createElement()`:

```javascript
var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};
var dmc = window.dash_mantine_components;

dmcfuncs.renderBadge = function({ option }) {
    return React.createElement(
        dmc.Badge,
        {
            color: option.value === "A" ? "red" : "blue",
            variant: "light",
            radius: "sm"
        },
        option.value
    );
};
```

**Using External Libraries:**
Include external JavaScript libraries and use them in your functions:

```python
app = Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js"])
```

```javascript
dmcfuncs.excludeDate = function(dateStr) {
    const date = dayjs(dateStr, "YYYY-MM-DD");
    return date.isValid() && date.day() !== 5;
}
```

#### AI-Assisted Function Generation

Most Dash users are more comfortable with Python than JavaScript. Use AI tools to generate JavaScript functions:

**Prompt Template:**
1. State the function name
2. Mention it's for Dash Mantine Components
3. Provide Python logic
4. Include the required global header
5. Specify React.createElement if returning components

**Example Prompt:**
> Write a JavaScript function for Dash Mantine Components named `formatUsd`. Assign it to `dmcfuncs.formatUsd`. Include the global header.
>
> Python version:
> ```python
> def formatUsd(value):
>     return f"${value:,.2f}"
> ```

#### Best Practices
- Always use the global header: `var dmcfuncs = window.dashMantineFunctions = window.dashMantineFunctions || {};`
- For React components, use `window.dash_mantine_components` as `dmc`
- Use `React.createElement()` instead of JSX
- Pass options as the second parameter to functions
- Test functions in browser console before integration

### Rich Text Editor Features

The RichTextEditor component includes:
- **Tiptap 3 Integration**: Latest rich text editing capabilities
- **Editor Access**: `dash_mantine_components.getEditor(id)` for client-side callbacks
- **Code Highlighting**: Built-in code block syntax highlighting
- **Focus Control**: Programmatic cursor management
- **Edit Mode**: Toggle between editable and read-only modes

### Styling & Theming

#### MantineProvider
Wrap your app with MantineProvider for consistent theming:

```python
app.layout = dmc.MantineProvider([
    # Your components here
], theme={"colorScheme": "dark"})
```

#### Style Props
All components support Mantine's style system:
- **Responsive**: Responsive spacing and sizing
- **Theme Integration**: Automatic theme color support
- **Custom Styles**: Override default styling
- **Container Queries**: Modern responsive approach

### Plotly Integration

Add Mantine-styled Plotly templates:

```python
import dash_mantine_components as dmc

# Add Mantine templates
dmc.add_figure_templates(set_default="mantine_light")
```

## Callback Patterns

### Common Callback Patterns

#### Input Components
```python
@callback(
    Output("output-text", "children"),
    Input("text-input", "value"),
    Input("number-input", "value"),
    State("select", "value")
)
def handle_input(text_value, number_value, select_value):
    return f"Input: {text_value}, Number: {number_value}, Select: {select_value}"
```

#### Chart Interactions
```python
@callback(
    Output("chart-details", "children"),
    Input("line-chart", "hoverData"),
    Input("bar-chart", "clickData")
)
def handle_chart_interactions(hover_data, click_data):
    if hover_data:
        return f"Hovering: {hover_data}"
    if click_data:
        return f"Clicked: {click_data}"
```

#### Modal Management
```python
@callback(
    Output("modal", "opened"),
    Output("modal-content", "children"),
    Input("open-modal-btn", "n_clicks"),
    prevent_initial_call=True
)
def manage_modal(n_clicks):
    if n_clicks:
        return True, "Modal content"
    return False, ""
```

### Advanced Callbacks

#### Client-Side Callbacks with Rich Text Editor
```javascript
// In assets/custom.js
window.dashMantineFunction = {
    getEditorContent: (editorId) => {
        const editor = dash_mantine_components.getEditor(editorId);
        return editor.getHTML();
    }
};
```

## Performance Optimizations

### Async Component Loading
Charts and code highlight components are loaded asynchronously:
- **Reduced Bundle Size**: Main bundle reduced from 2.68 MiB to 823 KiB
- **Faster Initial Load**: Improved page load times
- **On-Demand Loading**: Components load when needed

### Debouncing
Input components support debouncing for performance:
```python
dmc.TextInput(
    debounce=True,  # Update on blur or enter
    # or
    debounce=300,   # 300ms delay
)
```

### Notification System
Modern notification management:
```python
# In client-side callback
dash_mantine_components.appNotifications.api.show({
    'title': 'Success',
    'message': 'Operation completed',
    'color': 'green'
})
```

## Migration Guide

### Version Compatibility

| Dash Mantine Components | Release Date | Mantine Version | Required Dash Version |
|-------------------------|--------------|-----------------|-----------------------|
| **2.4.0**               | Nov 2025     | 8.3.6           | `dash>=2.0.0` |
| **2.3.0**               | Sep 2025     | 8.3.1           | `dash>=2.0.0` |
| **2.2.1**               | Aug 2025     | 8.2.7           | `dash>=2.0.0` |
| **2.2.0**               | Aug 2025     | 8.2.5           | `dash>=2.0.0` |
| **2.1.0**               | Jul 2025     | 8.1.2           | `dash>=2.0.0` |
| **2.0.0**               | Jun 2025     | 8.0.2           | `dash>=2.0.0` |
| **1.3.0**               | May 2025     | 7.17.7          | `dash>=2.0.0` |
| **1.2.0**               | Apr 2025     | 7.17.4          | `dash>=2.0.0` |
| **1.1.0**               | Mar 2025     | 7.17.2          | `dash>=2.0.0` |
| **1.0.0**               | Mar 2025     | 7.17.0          | `dash>=2.0.0` |
| **0.15.0**              | Nov 2024     | 7.14.1          | `dash>=2.0.0,<3.0.0`|
| **0.14.0**              | Apr 2024     | 7.0             | `dash>=2.0.0,<3.0.0` |

### Migrating from 1.2.0 to 2.x

DMC V2 is based on Mantine V8 with significant breaking changes:

#### Key Changes
- **Switch withThumbIndicator**: New default styling with thumb indicators
- **DatesProvider timezone**: Timezone option removed
- **DateTimePicker timeInputProps**: Replaced with `timePickerProps`
- **CodeHighlight**: Now includes only top 10 languages for bundle size reduction
- **Popover hideDetached**: New prop, enabled by default
- **Carousel changes**: Updated Embla carousel props structure
- **Image No longer has `flex:0`**: Default style removed
- **New DatePicker**: Standalone calendar component added
- **New NotificationContainer**: Replaces NotificationProvider system
- **Portal reuseTargetNode**: Now enabled by default for performance
- **Menu data-hovered attribute**: Removed, use `:hover` and `:focus` selectors

### Stylesheets Automatic Inclusion (DMC ≥ 1.2.0)

Stylesheets are now bundled automatically. For older versions:

```python
import dash_mantine_components as dmc
from dash import Dash

app = Dash(
    external_stylesheets=[
        dmc.styles.CAROUSEL,
        dmc.styles.CODE_HIGHLIGHT,
        dmc.styles.NOTIFICATIONS,
        # or just use dmc.styles.ALL
    ]
)
```

### Major Version Changes

#### Version 2.0 (Mantine 8)
- **Breaking Changes**: Updated to Mantine 8.0.2
- **Rich Text Editor**: Now uses Tiptap 3 with enhanced features
- **Notifications**: New NotificationContainer system
- **Functions as Props**: Enhanced JavaScript function support

#### Version 1.0 (Mantine 7)
- **React 18 Support**: Compatible with Dash 3
- **Component Updates**: Breaking changes from Mantine 6 to 7
- **Async Loading**: Improved performance

#### Version 0.14 (Mantine 7)
- **Breaking Changes**: Updated to Mantine v7
- **New Components**: Charts, carousel, nprogress
- **Style System**: New style prop system
- **Required MantineProvider**: Now mandatory for all apps

## Configuration

### Environment Setup
Ensure your Dash app has access to required assets:
```python
import dash
from dash import Dash

app = Dash(
    __name__,
    assets_folder="assets",  # For custom JavaScript functions
    external_stylesheets=[]  # DMC stylesheets are bundled automatically
)
```

### Custom JavaScript
Create `assets/custom.js` for custom functions:
```javascript
window.dashMantineFunction = {
    customFormat: (value, options) => {
        // Custom formatting logic
        return formattedValue;
    }
};
```

## Development & Contributing

### Contributing Guidelines
1. **Issues**: Report bugs or request features via GitHub Issues
2. **Discord**: Join the community Discord for discussions
3. **Documentation**: Contribute to the dmc-docs repository
4. **PRs**: Pull requests are welcome and encouraged

### Resources
- **Discord**: https://discord.gg/KuJkh4Pyq5
- **Documentation**: https://www.dash-mantine-components.com
- **GitHub**: https://github.com/snehilvj/dash-mantine-components
- **Plotly Forum**: https://community.plotly.com/

### Development Setup
```bash
# Clone repository
git clone https://github.com/snehilvj/dash-mantine-components.git
cd dash-mantine-components

# Install dependencies
npm install
pip install -e .

# Build components
npm run build

# Run tests
npm test
```

## Best Practices

### Performance
- Use async loading benefits for charts
- Implement debouncing for frequent inputs
- Leverage client-side callbacks for simple interactions
- Use NotificationContainer for better notification management

### Accessibility
- Ensure proper ARIA labels on interactive elements
- Test keyboard navigation
- Validate color contrasts
- Use semantic HTML structure

### Styling
- Leverage Mantine's theme system
- Use responsive design patterns
- Maintain consistent spacing with built-in spacing props
- Use container queries for modern responsive design

## Troubleshooting

### Common Issues

#### Component Not Rendering
- Ensure dash-mantine-components is installed: `pip install dash-mantine-components`
- Check Dash version compatibility (DMC 1.0+ requires Dash 2.16+)

#### Callback Issues
- Use correct property names (refer to component documentation)
- Ensure proper callback pattern with Input/Output

#### Styling Problems
- Wrap app in MantineProvider for consistent theming
- Check that custom styles don't conflict with Mantine's CSS

#### Performance Issues
- Use debouncing for frequent updates
- Leverage async component loading
- Consider client-side callbacks for simple interactions

### Getting Help
- **Documentation**: https://www.dash-mantine-components.com
- **GitHub Issues**: https://github.com/snehilvj/dash-mantine-components/issues
- **Discord**: https://discord.gg/KuJkh4Pyq5
- **Plotly Forum**: https://community.plotly.com/

## Version History

### Recent Versions
- **2.4.0** (Nov 2025): CopyButton components, RichTextEditor enhancements
- **2.3.0** (Sep 2025): MiniCalendar, RTL support, Tiptap 3
- **2.2.0** (2025): RichTextEditor custom toolbar, container queries
- **2.1.0** (2025): Modal/Drawer stacks, advanced chart features
- **2.0.0** (2025): Mantine 8, functions as props, new notification system

### Historical Versions
- **1.0.0** (2024): Mantine 7, React 18 support
- **0.14.0** (2023): Mantine 7, new components
- **0.13.0** (2023): Mantine 6, TypeScript migration
- **0.11.0** (2023): Mantine 5, component overhaul
- **0.7.0** (2022): Mantine 4 updates

See [CHANGELOG.md](https://github.com/snehilvj/dash-mantine-components/blob/master/CHANGELOG.md) for complete version history.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/snehilvj/dash-mantine-components/blob/master/LICENSE) file for details.

## Acknowledgments

- **Mantine**: For the excellent React component library
- **Plotly Dash**: For the web application framework
- **Community**: For contributions, feedback, and support
- **Sponsors**: For supporting the project's continued development

---

*This documentation is compiled from the official Dash Mantine Components GitHub repository, PyPI package information, and project documentation. For the most up-to-date information, visit https://www.dash-mantine-components.com.*
