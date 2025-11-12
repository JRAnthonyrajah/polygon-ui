
> Dash Mantine Components v2.4.0 Documentation for Styles Overview
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Styles Overview
This guide will help you understand how to apply styles to Dash Mantine components.
Category: Styling

### Component specific props
Most of the components provide props that allow you to customize their styles. For example, `Button` component has
`color`, `variant`, `size` and `radius` props that control its appearance:


### Style props

[Style props](/style-props) work similar to component specific props, but with several differences:

- Style props are not component specific, they can be used with any component.
- Style props always control a single CSS property. For example, `c` prop controls CSS `color` property, while `color` prop controls a set of properties: `color`, `background-color` and `border-color`.
- Style props are set in style attribute. It is not possible to override them with CSS without using `!important`.

[Style props](/style-props) are useful when you need to change a single CSS property without creating a separate file for styles. Some of the most common use cases are:


- Changing text color and font-size

```python

dmc.Card([
    dmc.Text("Card title", c="blue.8", fz="lg"),
    dmc.Text("Card description", c="dimmed", fz="sm")
])
```

- Applying margins to inputs inside a form:

```python
dmc.Paper([
    dmc.TextInput(label="First name"),
    dmc.TextInput(label="Last name", mt="md"),
    dmc.TextInput(label="Email", mt="md")
])
```

- Adding padding to various elements:

```python
dmc.Paper("My custom card", p="xl")
```

Note that style props were never intended to be used as a primary way of styling components. In most cases, it is better
to limit the number of style props used per component to 3-4. If you find yourself using more than 4 style props,
consider creating a separate CSS file with styles – it will be easier to maintain and will be more performant.


### style prop

You can use the `style` prop to define inline styles, just like in other dash components:
```python
dmc.Card(style={"backgroundColor": "blue", "color": "white"})
```

### className prop
You can define CSS classes in a `.css` file in the `/assets` folder. These can then be referenced using the `className` prop, just like in other dash components:

```python
dmc.Card(className="card-style")
```

.css file:
```css
.card-style {
    background-color: blue;
    color: white;
}
```

### Styles API

Note that the `style` and the `className` props will apply style to the root of the component.  Many DMC components contain
multiple elements, for example the `TextInput` includes `label`, `description`, `error` props.

Use the `classNames` or `styles` props to target the nested elements.  See more information in the [StylesAPI](/styles-api) section.

- `styles` prop: Used to apply inline styles directly to specific inner elements of a Mantine component.
- `classNames`prop: Used to apply custom CSS class names to specific inner elements of a Mantine component

### theme prop in MantineProvider

DMC includes a great default theme that supports light and dark mode. Use the `theme` prop to change the global styles.

For those of you familiar with Dash Bootstrap Components, this is similar to setting the theme using a Bootstrap
stylesheet. However, in DMC, instead of linking to a  CSS file, you can directly define the theme using a Python
dictionary, which makes it easy to customize the theme. For example, you can  override colors, fonts, spacing,
and even component-specific styles globally.

For more information see the [Theme Object](/theme-object) section.


###  Theme Tokens

A theme token is a named value from the global theme, like a color, spacing unit, or font family. In DMC, these tokens
can be used in any styles with the Mantine [CSS variables](/css-variables):

For example:

 - In a `.css` file in `/assets`:

```css
.root {
  background: var(--mantine-color-red-5); /* red[5] from theme.colors */
  margin-top: var(--mantine-spacing-md);  /* md from theme.spacing */
}
```

-  In style props:
```python
dcc.Box(bg="red.5", mt="xl")
# Shorthand for: var(--mantine-color-red-5), var(--mantine-spacing-xl)
```

- In the `style` prop:
```python
dcc.Box(style={"backgroundColor": "var(--mantine-color-red-5)"})

```
---


> Dash Mantine Components v2.4.0 Documentation for Styles API
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Styles API
With Styles API you can overwrite styles of inner elements in Mantine components with classNames or styles props.
Category: Styling

### Styles API Overview

DMC supports `style` and `className` props for styling the root element, just like other Dash libraries.
However, many DMC components have nested elements.  For example the `TextInput` includes `label`, `description`,
`error` props.

The Styles API is a set of props and techniques that allows you to customize the style of any element inside a Mantine
component - inline using the  `classNames` or `styles` props, or using the [Theme Object](/theme-object).


### Styles API Selectors

Each component has its own set of selectors based on its structure. These are documented in the Styles API section of each component’s page.


#### Example: `dmc.Button` Selectors

| Name    | Static selector         | Description                      |
| :------ | :---------------------- | :------------------------------- |
| root    | .mantine-Button-root    | Root element                     |
| loader  | .mantine-Button-loader  | Loader shown when `loading=True` |
| section | .mantine-Button-section | Left and right icon sections     |
| inner   | .mantine-Button-inner   | Container for label and content  |
| label   | .mantine-Button-label   | The button’s text                |


You can use these selectors in multiple ways:

#### 1) With `classNames` or `styles` props

```python
# Using classNames
dmc.Button(
    "Styled with classNames",
    classNames={
        "root": "my-root-class",
        "label": "my-label-class",
        "inner": "my-inner-class",
    }
)

# Using inline styles
dmc.Button(
    "Styled with styles prop",
    styles={
        "root": {"backgroundColor": "red"},
        "label": {"color": "blue"},
        "inner": {"fontSize": 20},
    }
)
```

#### 2) In the `theme` prop in  `MantineProvider`

```python
theme = {
    "components": {
        "Button": {
            "classNames": {
                "root": "my-root-class",
                "label": "my-label-class",
                "inner": "my-inner-class",
            },
            "styles": {
                "root": {"backgroundColor": "red"},
                "label": {"color": "blue"},
                "inner": {"fontSize": 20},
            }
        }
    }
}

app.layout = dmc.MantineProvider(
    theme=theme,
    children=dmc.Button("Themed Button")
)
```

#### 3) In a `.css` file using static selectors

```css
.mantine-Button-root {
    background-color: red;
}

.mantine-Button-label {
    color: blue;
}

.mantine-Button-inner {
    font-size: 20px;
}
```

### classNames Prop

The `classNames` prop is used to apply custom CSS class names to specific inner elements of a Mantine component. It
accepts a dictionary  with element names as keys and classes as values. This approach is preferred for larger-scale styling and
maintainability.


### Styles Prop

The `styles` prop is used to apply inline styles directly to specific inner elements of a Mantine component. It accepts
an dictionary where keys correspond to the names of the inner elements (as defined in the component's Styles API documentation)
and values are style objects. Inline styles have higher specificity than classes, meaning they will override styles
defined by classes unless `!important` is explicitly used in the class definition.

You cannot use pseudo-classes (for example, `:hover`, `:first-of-type`) and media queries inside the `styles` prop.


> styles prop usage
>
> Some examples and demos in the documentation use the `styles` prop for convenience, but it is not recommended to use the `styles` prop as the primary means of styling components, as the `classNames` prop is more flexible and has better performance.

### Avoid dynamic class names

When inspecting elements in the browser, you may see generated class names like `m_77c9d27d`. These are internal to Mantine and can change between versions. Don’t target these in your CSS.

Instead, use:

* the `styles` or `classNames` props
* static class selectors like `.mantine-Button-root`



### Global vs. Specific Styling

You can combine global styling (via `theme` or static CSS) with component-specific overrides using `styles` or `classNames`.

For example:

* A default red background can be applied globally using `.mantine-Button-root`
* A specific button can override this with its own `className` or `styles`

Note: For components rendered in a portal — such as `Popover`, `Tooltip`, or `Modal` — static selectors often won’t work because parts of the DOM are rendered outside the main tree. In these cases, use `classNames` or `styles`, or set `withinPortal=False` if appropriate.


### Component Classes

Mantine uses hashed class names (e.g., `m_77c9d27d`) for internal styling. These class names may change between versions or builds, so you should never rely on them directly.

**Do not do this:**

```css
/* This is fragile and will likely break */
.m_77c9d27d {
  background: blue;
}
```

**Instead, do this:**

```css
/* Use static selectors */
.mantine-Button-root {
  background: blue;
}
```

Or:

```python
# Use the Styles API
dmc.Button(
    "Styled Button",
    classNames={"root": "my-custom-button"}
)
```



### Data Attributes

Many Mantine components use `data-*` attributes to reflect state or props. These can be useful for styling in CSS, especially when using features like loading states, icons, or layout modifiers.

You’ll find a list of data attributes for each component in its Styles API docs.

Example (`dmc.Button`):

| Selector  | Attribute                | Set When…            | Example value     |
| --------- | ------------------------ | -------------------- | ----------------- |
| `root`    | `data-disabled`          | `disabled=True`      | –                 |
| `root`    | `data-loading`           | `loading=True`       | –                 |
| `root`    | `data-block`             | `fullWidth=True`     | –                 |
| `root`    | `data-with-left-section` | `leftSection` is set | –                 |
| `section` | `data-position`          | Always               | `left` or `right` |

Example CSS targeting data attributes:

```css
/* Style disabled buttons */
.dmc-data-attributes-demo[data-disabled="true"] {
    color: red;
    cursor: not-allowed;
}

/* Style buttons while loading */
.dmc-data-attributes-demo[data-loading="true"] {
    background-color: darkgray;
}

/* Style left icon section */
.dmc-data-attributes-demo .mantine-Button-section[data-position="left"] {
    color: var(--mantine-color-yellow-filled);
}
```

```python
import dash_mantine_components as dmc
from dash import html

component = dmc.Group(
    [
        dmc.Button("Default Button"),
        dmc.Button("Disabled Button", disabled=True, className="dmc-data-attributes-demo"),
        dmc.Button("Loading Button", loading=True, className="dmc-data-attributes-demo"),
        dmc.Button("Button with Left Section", leftSection=html.Div("left"), className="dmc-data-attributes-demo"),
    ],
    gap="sm"
)
```
### attributes prop

Use `attributes` prop to pass attributes to inner elements of all components that support Styles API. For example,
it can be used to add data attributes for testing purposes:


```python
import dash_mantine_components as dmc


component = dmc.Button(
    "Button with attributes",
    attributes={
        "root": { "data-test-id": "root" },
        "label": { "data-test-id": "label" },
        "inner": { "data-test-id": "inner" },
      },
)
```
### More Examples

Here are a few component-specific examples. Refer to each component’s Styles API section for the full list of selectors and attributes.

#### Button

```python
import dash_mantine_components as dmc
from dash_iconify import DashIconify

component = dmc.Button(
    "Settings",
    leftSection=DashIconify(icon="ic:baseline-settings-input-composite"),
    styles={"root": {"fontWeight": 400}, "section": {"width": 100}},
)
```
#### Badge

```python
import dash_mantine_components as dmc

component = dmc.Badge(
    "Badge 1",
    variant="dot",
    styles={
        "root": {"borderWidth": 1, "height": 30, "padding": 10},
        "inner": {"fontWeight": 500},
    },
)
```
#### TextInput

```python
import dash_mantine_components as dmc

component = dmc.TextInput(
    label="TextInput with custom styles",
    placeholder="TextInput with custom styles",
    description="Description below the input",
    w=300,
    styles={
        "input": {"borderColor": dmc.DEFAULT_THEME["colors"]["violet"][4]},
        "label": {
            "color": "blue",
            "backgroundColor": dmc.DEFAULT_THEME["colors"]["yellow"][1],
        },
    },
)
```
### Styles with Callbacks

```python
from dash import  html, callback, Output, Input, State
import dash_mantine_components as dmc

component = html.Div([
    dmc.TextInput(
        id="styles-input",
        label="Required Input",
        required=True,
    ),
    dmc.Button("Submit", id="styles-submit-btn")
])

@callback(
    Output("styles-input", "styles"),
    Input("styles-submit-btn", "n_clicks"),
    State("styles-input", "value"),
    prevent_initial_call=True
)
def update_styles(n_clicks, value):
    if not value:
        return {
            "input": {"borderColor": "red"},
            "label": {"color": "red"}
        }
    return {
        "input": {"borderColor": "green"},
        "label": {"color": "green"}
    }
```
### Slider

See the [Styling the Slider](/components/slider#styling-the-slider) section for a detailed example including:

* Dynamic theming with `light-dark`
* Custom styling for tracks, marks, and thumbs
* Attribute-based styling using `[data-filled]`


### Tabs

For another advanced example, see the [Styling the Tabs](/components/tabs#styling-the-tabs) section.


### DatePickerInput

Components that use portals (like `Popover`, `Modal`, and `Tooltip`) often render outside the DOM tree. To style their internal parts:

* Use `classNames` or `styles` props
* Or set `withinPortal=False` if supported

```python
import dash_mantine_components as dmc

component = dmc.Stack([
    dmc.DatePickerInput(
        label="Default Calendar style"
    ),
    dmc.DatePickerInput(
        label="Calendar without red weekend days",
        styles={"day": {"color": "var(--mantine-color-text)"}},
    )
])
```

---


> Dash Mantine Components v2.4.0 Documentation for Style Props
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Style Props
With style props you can add responsive styles to any Mantine component that supports these props.
Category: Styling

### Supported props

Style props add styles to the root element, if you want to style nested elements use [Styles API](/styles-api) instead.

```python
dmc.Box(mx="auto", maw=400, c="blue.6", bg="#fff")
```

:border: false

### Theme values
Some style props can reference values from theme, for example `mt` will use `theme.spacing` value if you set `xs`, `sm`, `md`, `lg`, `xl`:

```python

# margin-top: theme.spacing.xs
dmc.Box(mt="xs")

# margin-top: theme.spacing.md * -1
dmc.Box(mt="-md")

# margin-top: auto
dmc.Box(mt="auto")

# margin-top: 1rem
dmc.Box(mt=16)

# margin-top: 5rem
dmc.Box(mt="5rem")


```

In `c`, `bd` and `bg` props you can reference colors from `theme.colors`:

```python

# Color: theme.colors.blue[theme.primaryShade]
dmc.Box(c="blue")

# Background: theme.colors.orange[1]
dmc.Box(bg="orange.1")

# Border: 1px solid theme.colors.red[6]
dmc.Box(bd="1px solid red.6")

# Color: if colorScheme is dark `var(--mantine-color-dark-2)`, if colorScheme is light `var(--mantine-color-gray-6)`
dmc.Box(c="dimmed")

# Color: if colorScheme is dark `var(--mantine-color-white)`, if colorScheme is light `var(--mantine-color-black)`
dmc.Box(c="bright")

# Background: #EDFEFF
dmc.Box(bg="#EDFEFF")

# Background: rgba(0, 34, 45, 0.6)
dmc.Box(bg="rgba(0, 34, 45, 0.6)")

```




### Responsive styles

You can pass a dictionary to style props to add responsive styles with style props.
Note that responsive style props are less performant than regular style props, it is not recommended using them in large amounts.

```python
import dash_mantine_components as dmc

component = dmc.Box(
    "Box with responsive style props",
    w={"base": 200, "sm": 400, "lg": 500},
    py={"base": "xs", "sm": "md", "lg": "xl"},
    bg={"base": "blue.7", "sm": "red.7", "lg": "green.7"},
    c="#fff",
    ta="center",
    mx="auto",
)
```
Responsive values are calculated the following way:

- `base` value is used when none of the breakpoint values are provided
- `xs`, `sm`, `md`, `lg`, `xl` values are used when the viewport width is larger that the value of corresponding breakpoint specified in `dmc.DEFAULT_THEME`.

```python
import dash_mantine_components as dmc

dmc.Box(w={ "base": 320, "sm": 480, "lg": 640 })
```

In this case the element will have the following styles:

```css
/* Base styles added to element and then get overwritten with responsive values */
.element {
  width: 20rem;
}

/* 48em is theme.breakpoints.sm by default */
@media (min-width: 48em) {
  .element {
    width: 30rem;
  }
}

/* 75em is theme.breakpoints.lg by default */
@media (min-width: 75em) {
  .element {
    width: 40rem;
  }
}
```

Note that underlying Mantine transforms `px` to `rem`, but for most part you can ignore this.

---


> Dash Mantine Components v2.4.0 Documentation for CSS Variables
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## CSS Variables
How to use CSS variables with Dash Mantine Components.
Category: Styling

MantineProvider exposes all Mantine CSS variables based on the given theme. You can use these variables in CSS files,
style prop or any other styles. See the full list of variables at the bottom of the page.

### Typography variables

#### Font family
The following CSS variables are used to assign font families to all Mantine components:


| Variable                        | Default value           | Description                                              |
|:--------------------------------|:------------------------|:---------------------------------------------------------|
| `mantine-font-family`           | system sans-serif fonts | Controls font-family property of most Mantine components |
| `mantine-font-family-monospace` | system monospace fonts  | Controls font-family property of code blocks             |
| `mantine-font-family-headings`  | system sans-serif fonts | Controls font-family property of headings                |


You can control these variables in the [theme](/theme-object). Note that if `theme.headings.fontFamily` is not set,
`--mantine-font-family-headings` value will be the same as `--mantine-font-family`


```python
theme = {
    # Controls --mantine-font-family
    "fontFamily": "Arial, sans-serif",

    # Controls --mantine-font-family-monospace
    "fontFamilyMonospace": "Courier New, monospace",

    "headings": {
        # Controls --mantine-font-family-headings
        "fontFamily": "Georgia, serif",
    },
}
dmc.MantineProvider(theme=theme, children=[])
```

If you want to use system fonts as a fallback for custom fonts, you can reference `dmc.DEFAULT_THEME` value instead of defining it manually:

```python
import dash_mantine_components as dmc

theme = {
    "fontFamily": f"Roboto, {dmc.DEFAULT_THEME['fontFamily']}"
}
```
You can reference font family variables in your CSS:

```css

.text {
  font-family: var(--mantine-font-family);
}

.code {
  font-family: var(--mantine-font-family-monospace);
}

.heading {
  font-family: var(--mantine-font-family-headings);
}

```

And in `ff` style prop:

- `ff="text"` will use `--mantine-font-family` variable
- `ff="monospace"` will use `--mantine-font-family-monospace` variable
- `ff="heading"` will use `--mantine-font-family-headings` variable


```python
dmc.Text(
    "This text uses --mantine-font-family-monospace variable",
    ff="monospace"
)
```


#### Font size

Font size variables are used in most Mantine components to control text size. The variable that is chosen depends on
the component and its size prop.

| Variable                        | Default value   |
|:--------------------------------|:----------------|
| --mantine-font-size-xs          | 0.75rem (12px)  |
| --mantine-font-size-sm          | 0.875rem (14px) |
| --mantine-font-size-md          | 1rem (16px)     |
| --mantine-font-size-lg          | 1.125rem (18px) |
| --mantine-font-size-xl          | 1.25rem (20px)  |

You can reference font size variables in CSS:

```css
.demo {
  font-size: var(--mantine-font-size-md);
}
```

And in `fz` style prop:
```python
dmc.Text(
    "This text uses --mantine-font-size-xl variable",
    fz="xl"
)
```

To define custom font sizes, can use `theme.fontSizes` property:

```python
theme = {
    'fontSizes': {
    'xs': '0.5rem',
    'sm': '0.75rem',
    'md': '1rem',
    'lg': '1.25rem',
    'xl': '1.5rem',
  },
}
dmc.MantineProvider(theme=theme, children=[])
```


Note that `theme.fontSizes` dict is merged with the dmc.DEFAULT_THEME – it is not required to define all values, only those that you want to change.

```python
theme = {
    'fontSizes': {'xs': '0.5rem'}
}
```

You can add any number of additional font sizes to the `theme.fontSizes` object. These values will be defined as
CSS variables in `--mantine-font-size-{size}` format:


```python
theme = {
    'fontSizes': {
        'xxs': '0.125rem',
        'xxl': '2rem',
    }
}
```

After defining `theme.fontSizes`, you can reference these variables in your CSS:

```css
.demo {
  font-size: var(--mantine-font-size-xxs);
}
```

> Case conversion
>
>Case conversion (camelCase to kebab-case) is not automatically applied to custom font sizes. If you define `theme.fontSizes`
with camelCase keys, you need to reference them in camelCase format. For example, if you define `{ customSize: '1rem' }`, you need to reference it as `--mantine-font-size-customSize`.


#### Line height

Line height variables are used in the Text component. In other components, line-height is either calculated based on font size or set to `--mantine-line-height`, which is an alias for `--mantine-line-height-md`.

| Variable                      | Default value  |
|:------------------------------|:---------------|
| --mantine-line-height         | 1.55           |
| --mantine-line-height-xs      | 1.4            |
| --mantine-line-height-sm      | 1.45           |
| --mantine-line-height-md      | 1.55           |
| --mantine-line-height-lg      | 1.6            |
| --mantine-line-height-xl      | 1.65           |

You can reference line height variables in your CSS:

```css
.demo {
  line-height: var(--mantine-line-height-md);
}
```

```python
dmc.Text("This text uses --mantine-line-height-xl variable", lh="xl")
```

To define custom line heights, you can use theme.lineHeights property:

```python
theme = {
    'lineHeights': {
    'xs': '1.2',
    'sm': '1.3',
    'md': '1.4',
    'lg': '1.5',
    'xl': '1.6',
  },
}
```


#### Headings

`theme.headings` controls `font-size`, `line-height`, `font-weight`, and `text-wrap` CSS properties of headings in `Title` and `TypographyStylesProvider` components.

| Variable                        | Default value   |
|:--------------------------------|:----------------|
| **General variables**           |                 |
| --mantine-heading-font-weight   | 700             |
| --mantine-heading-text-wrap     | wrap            |
| **h1 heading**                  |                 |
| --mantine-h1-font-size          | 2.125rem (34px) |
| --mantine-h1-line-height        | 1.3             |
| --mantine-h1-font-weight        | 700             |
| **h2 heading**                  |                 |
| --mantine-h2-font-size          | 1.625rem (26px) |
| --mantine-h2-line-height        | 1.35            |
| --mantine-h2-font-weight        | 700             |
| **h3 heading**                  |                 |
| --mantine-h3-font-size          | 1.375rem (22px) |
| --mantine-h3-line-height        | 1.4             |
| --mantine-h3-font-weight        | 700             |
| **h4 heading**                  |                 |
| --mantine-h4-font-size          | 1.125rem (18px) |
| --mantine-h4-line-height        | 1.45            |
| --mantine-h4-font-weight        | 700             |
| **h5 heading**                  |                 |
| --mantine-h5-font-size          | 1rem (16px)     |
| --mantine-h5-line-height        | 1.5             |
| --mantine-h5-font-weight        | 700             |
| **h6 heading**                  |                 |
| --mantine-h6-font-size          | 0.875rem (14px) |
| --mantine-h6-line-height        | 1.5             |
| --mantine-h6-font-weight        | 700             |

These variables are used in the `Title` component. The `order` prop controls which heading level to use. For example, `order={3}` Title will use:

- `--mantine-h3-font-size`
- `--mantine-h3-line-height`
- `--mantine-h3-font-weight`


```python
import dash_mantine_components as dmc
from dash import html

component = html.Div(
    [
        dmc.Title(f"This is h1 title", order=1),
        dmc.Title(f"This is h2 title", order=2),
        dmc.Title(f"This is h3 title", order=3),
        dmc.Title(f"This is h4 title", order=4),
        dmc.Title(f"This is h5 title", order=5),
        dmc.Title(f"This is h6 title", order=6),
    ]
)
```
You can reference heading variables in your CSS:


```css
.h1 {
  font-size: var(--mantine-h1-font-size);
  line-height: var(--mantine-h1-line-height);
  font-weight: var(--mantine-h1-font-weight);
}
```
And in fz and lh style props:

```python
dmc.Text("This text uses --mantine-h1-* variables",  fz="h1", lh="h1")
```

To change heading styles, can use `theme.headings` property:

```python
theme = {
    "headings": {
        "sizes": {
            "h1": {
                "fontSize": "2rem",
                "lineHeight": "1.5",
                "fontWeight": "500",
            },
            "h2": {
                "fontSize": "1.5rem",
                "lineHeight": "1.6",
                "fontWeight": "500",
            },
        },
        # ...
    },
}
```

`theme.headings` dict is deeply merged with the default theme – it is not required to define all values, only those that you want to change.


```python
theme = {
    "headings": {
        "sizes": {
            "h1": {
                "fontSize": "2rem",
            },
        },
    },
}
```


#### Font smoothing

Font smoothing variables control `-webkit-font-smoothing` and `moz-osx-font-smoothing` CSS properties. These variables are used to make text look better on screens with high pixel density.

Font smoothing variables are controlled by the `theme.fontSmoothing` theme property, which is `True` by default. If `theme.fontSmoothing` is `False`, both variables will be set to `unset`.

| Variable                        | Default value  |
|:--------------------------------|:---------------|
| --mantine-webkit-font-smoothing | antialiased    |
| --mantine-moz-font-smoothing    | grayscale      |

If you need to override font smoothing values, the best way is to disable `theme.fontSmoothing` and set global styles on the `body` element:

```python
# Disable font smoothing in your theme
theme = {
  "fontSmoothing": False,
}
```

Add global styles to your project with desired font smoothing values
```css
body {
  -webkit-font-smoothing: subpixel-antialiased;
  -moz-osx-font-smoothing: auto;
}
```


### Colors variables

Colors variables are controlled by `theme.colors` and `theme.primaryColor`. Each color defined in the `theme.colors` object is required to have 10 shades. Theme colors can be referenced by their name and shade index, for example, `--mantine-color-red-6`.

You can define new colors on the theme object or override existing colors:

```python
theme = {
    "colors": {
        "demo": [
            "#FF0000",
            "#FF3333",
            "#FF6666",
            "#FF9999",
            "#FFCCCC",
            "#FFEEEE",
            "#FFFAFA",
            "#FFF5F5",
            "#FFF0F0",
            "#FFEBEB",
        ],
    },
}
```

The code above will define the following CSS variables:

| Variable                      | Default value  |
|:------------------------------|:---------------|
| --mantine-color-demo-0        | #FF0000        |
| --mantine-color-demo-1        | #FF3333        |
| --mantine-color-demo-2        | #FF6666        |
| --mantine-color-demo-3        | #FF9999        |
| --mantine-color-demo-4        | #FFCCCC        |
| --mantine-color-demo-5        | #FFEEEE        |
| --mantine-color-demo-6        | #FFFAFA        |
| --mantine-color-demo-7        | #FFF5F5        |
| --mantine-color-demo-8        | #FFF0F0        |
| --mantine-color-demo-9        | #FFEBEB        |

#### Variant colors

Some Mantine components like `Button` or `Badge` have the `variant` prop that in combination with the `color` prop controls the component text, background, and border colors. For each variant and color, Mantine defines a set of CSS variables that control these colors. For example, for the default blue color the following CSS variables are defined:

| Variable                                         | Default value                 |
|:-------------------------------------------------|:------------------------------|
| **Filled variant**                               |                               |
| --mantine-color-blue-filled                      | var(--mantine-color-blue-6)   |
| --mantine-color-blue-filled-hover                | var(--mantine-color-blue-7)   |
| **Light variant**                                |                               |
| --mantine-color-blue-light                       | rgba(34, 139, 230, 0.1)       |
| --mantine-color-blue-light-hover                 | rgba(34, 139, 230, 0.12)      |
| --mantine-color-blue-light-color                 | var(--mantine-color-blue-6)   |
| **Outline variant**                              |                               |
| --mantine-color-blue-outline                     | var(--mantine-color-blue-6)   |
| --mantine-color-blue-outline-hover               | rgba(34, 139, 230, 0.05)      |


For example, if you use Button component the following way:


```python
import dash_mantine_components as dmc

component = dmc.Button("Pink filled button", color="pink", variant="filled")
```
The component will have the following styles:

- Background color will be `var(--mantine-color-pink-filled)`
- Background color on hover will be `var(--mantine-color-pink-filled-hover)`
- Text color will be `var(--mantine-color-white)`
- Border color will be `transparent`

Note that the variables above are not static; they are generated based on the values of `theme.colors` and `theme.primaryShade`. Additionally, their values are different for dark and light color schemes.

#### Variant Colors Variables

Variant colors variables are used in all components that support the `color` prop, for example, `Button`, `Badge`, `Avatar`, and `Pagination`. The color values used by these components are determined by `cssVariablesResolver` and `variantColorResolver`.

#### Primary Color Variables

Primary color variables are defined by `theme.primaryColor` (which must be a key of `theme.colors`). The following CSS variables are defined for the primary color:

| Variable                                      | Default value                                      |
|:----------------------------------------------|:---------------------------------------------------|
| --mantine-primary-color-{shade}               | `var(--mantine-color-{primaryColor}-{shade})`      |
| --mantine-primary-color-filled                | `var(--mantine-color-{primaryColor}-filled)`       |
| --mantine-primary-color-filled-hover          | `var(--mantine-color-{primaryColor}-filled-hover)` |
| --mantine-primary-color-light                 | `var(--mantine-color-{primaryColor}-light)`        |
| --mantine-primary-color-light-hover           | `var(--mantine-color-{primaryColor}-light-hover)`  |
| --mantine-primary-color-light-color           | `var(--mantine-color-{primaryColor}-light-color)`  |

You can reference primary color variables in CSS:

```css
.demo {
  color: var(--mantine-primary-color-0);
  background-color: var(--mantine-primary-color-filled);
}
```

#### Other Color Variables

The following colors are used in various Mantine components. Note that default values are provided for the light color scheme; dark color scheme values are different.

| Variable                          | Description                                             | Default Value                    |
|-----------------------------------|---------------------------------------------------------|----------------------------------|
| --mantine-color-white             | Value of `theme.white`                                  | #fff                             |
| --mantine-color-black             | Value of `theme.black`                                  | #000                             |
| --mantine-color-text              | Color used for text in the body element                 | var(--mantine-color-black)       |
| --mantine-color-body              | Body background color                                   | var(--mantine-color-white)       |
| --mantine-color-error             | Color used for error messages and states                | var(--mantine-color-red-6)       |
| --mantine-color-placeholder       | Color used for input placeholders                       | var(--mantine-color-gray-5)      |
| --mantine-color-dimmed            | Color used for dimmed text                              | var(--mantine-color-gray-6)      |
| --mantine-color-bright            | Color used for bright text                              | var(--mantine-color-black)       |
| --mantine-color-anchor            | Color used for links                                    | var(--mantine-primary-color-6)   |
| --mantine-color-default           | Background color of default variant                     | var(--mantine-color-white)       |
| --mantine-color-default-hover     | Background color of default variant on hover            | var(--mantine-color-gray-0)      |
| --mantine-color-default-color     | Text color of default variant                           | var(--mantine-color-black)       |
| --mantine-color-default-border    | Border color of default variant                         | var(--mantine-color-gray-4)      |


### Spacing variables

`theme.spacing` values are used in most Mantine components to control paddings, margins, and other spacing-related properties. The following CSS variables are defined based on `theme.spacing`:

| Variable               | Default value   |
|------------------------|-----------------|
| --mantine-spacing-xs   | 0.625rem (10px) |
| --mantine-spacing-sm   | 0.75rem (12px)  |
| --mantine-spacing-md   | 1rem (16px)     |
| --mantine-spacing-lg   | 1.25rem (20px)  |
| --mantine-spacing-xl   | 2rem (32px)     |

To define custom spacing values, use the `theme.spacing` property:

```python
theme = {
    "spacing": {
        "xs": "0.5rem",
        "sm": "0.75rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
    },
}
```

### Border radius variables

Mantine components that support the `radius` prop use border radius variables to control border radius. The following CSS variables are defined based on `theme.radius`:

| Variable                 | Default value  |
|--------------------------|----------------|
| --mantine-radius-xs      | 0.125rem (2px) |
| --mantine-radius-sm      | 0.25rem (4px)  |
| --mantine-radius-md      | 0.5rem (8px)   |
| --mantine-radius-lg      | 1rem (16px)    |
| --mantine-radius-xl      | 2rem (32px)    |

Additionally, `--mantine-radius-default` variable is defined based on `theme.defaultRadius` value. If the `radius` prop on components is not set explicitly, `--mantine-radius-default` is used instead.

To define custom border radius values, use the `theme.radius` and `theme.defaultRadius` properties:

```python
theme = {
    "defaultRadius": "sm",
    "radius": {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "2rem",
        "xl": "3rem",
    },
}
```


### Shadow variables

Shadow variables are used in all Mantine components that support the `shadow` prop. The following CSS variables are defined based on `theme.shadows`:

| Variable              | Default value                                                                                          |
|-----------------------|--------------------------------------------------------------------------------------------------------|
| --mantine-shadow-xs   | 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1)                                            |
| --mantine-shadow-sm   | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 10px 15px -5px, rgba(0, 0, 0, 0.04) 0 7px 7px -5px |
| --mantine-shadow-md   | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 20px 25px -5px, rgba(0, 0, 0, 0.04) 0 10px 10px -5px|
| --mantine-shadow-lg   | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 28px 23px -7px, rgba(0, 0, 0, 0.04) 0 12px 12px -7px|
| --mantine-shadow-xl   | 0 1px 3px rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 36px 28px -7px, rgba(0, 0, 0, 0.04) 0 17px 17px -7px|

To define custom shadow values, use the `theme.shadows` property:

```python
theme = {
    "shadows": {
        "xs": "0 1px 2px rgba(0, 0, 0, 0.1)",
        "sm": "0 1px 3px rgba(0, 0, 0, 0.1)",
        "md": "0 2px 4px rgba(0, 0, 0, 0.1)",
        "lg": "0 4px 8px rgba(0, 0, 0, 0.1)",
        "xl": "0 8px 16px rgba(0, 0, 0, 0.1)",
    },
}
```

### z-index variables

z-index variables are defined in `@mantine/core/styles.css`. Unlike other variables, z-index variables are not controlled by the theme and are not exposed in the theme object.

| Variable                  | Default value |
|---------------------------|---------------|
| --mantine-z-index-app     | 100           |
| --mantine-z-index-modal   | 200           |
| --mantine-z-index-popover | 300           |
| --mantine-z-index-overlay | 400           |
| --mantine-z-index-max     | 9999          |

You can reference z-index variables in CSS:

```css
/* Display content above the modal */
.my-content {
  z-index: calc(var(--mantine-z-index-modal) + 1);
}
```

And in components by referencing the CSS variable:

```python
import dash_mantine_components as dmc

dmc.Modal(
    zIndex="var(--mantine-z-index-max)",
    opened=True,
    children="Modal content"
)
```

### CSS Variables list

#### CSS variables not depending on color scheme
#### Light color scheme only variables
#### Dark color scheme only variables


### CSS Variables Not Depending on Color Scheme

| Variable | Value |
|----------|-------|
| --mantine-scale | 1 |
| --mantine-cursor-type | default |
| --mantine-color-scheme | light dark |
| --mantine-webkit-font-smoothing | antialiased |
| --mantine-moz-font-smoothing | grayscale |
| --mantine-color-white | #fff |
| --mantine-color-black | #000 |
| --mantine-line-height | 1.55 |
| --mantine-font-family | -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji |
| --mantine-font-family-monospace | ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace |
| --mantine-font-family-headings | -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji |
| --mantine-heading-font-weight | 700 |
| --mantine-heading-text-wrap | wrap |
| --mantine-radius-default | 0.25rem |
| --mantine-primary-color-filled | var(--mantine-color-blue-filled) |
| --mantine-primary-color-filled-hover | var(--mantine-color-blue-filled-hover) |
| --mantine-primary-color-light | var(--mantine-color-blue-light) |
| --mantine-primary-color-light-hover | var(--mantine-color-blue-light-hover) |
| --mantine-primary-color-light-color | var(--mantine-color-blue-light-color) |
| --mantine-breakpoint-xs | 36em |
| --mantine-breakpoint-sm | 48em |
| --mantine-breakpoint-md | 62em |
| --mantine-breakpoint-lg | 75em |
| --mantine-breakpoint-xl | 88em |
| --mantine-spacing-xs | 0.625rem |
| --mantine-spacing-sm | 0.75rem |
| --mantine-spacing-md | 1rem |
| --mantine-spacing-lg | 1.25rem |
| --mantine-spacing-xl | 2rem |
| --mantine-font-size-xs | 0.75rem |
| --mantine-font-size-sm | 0.875rem |
| --mantine-font-size-md | 1rem |
| --mantine-font-size-lg | 1.125rem |
| --mantine-font-size-xl | 1.25rem |
| --mantine-line-height-xs | 1.4 |
| --mantine-line-height-sm | 1.45 |
| --mantine-line-height-md | 1.55 |
| --mantine-line-height-lg | 1.6 |
| --mantine-line-height-xl | 1.65 |
| --mantine-shadow-xs | 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.05), 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.1) |
| --mantine-shadow-sm | 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 0.625rem 0.9375rem -0.3125rem, rgba(0, 0, 0, 0.04) 0 0.4375rem 0.4375rem -0.3125rem |
| --mantine-shadow-md | 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 1.25rem 1.5625rem -0.3125rem, rgba(0, 0, 0, 0.04) 0 0.625rem 0.625rem -0.3125rem |
| --mantine-shadow-lg | 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 1.75rem 1.4375rem -0.4375rem, rgba(0, 0, 0, 0.04) 0 0.75rem 0.75rem -0.4375rem |
| --mantine-shadow-xl | 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.05) 0 2.25rem 1.75rem -0.4375rem, rgba(0, 0, 0, 0.04) 0 1.0625rem 1.0625rem -0.4375rem |
| --mantine-radius-xs | 0.125rem |
| --mantine-radius-sm | 0.25rem |
| --mantine-radius-md | 0.5rem |
| --mantine-radius-lg | 1rem |
| --mantine-radius-xl | 2rem |

#### Primary Color Shades (0-9)
| Variable | Value |
|----------|-------|
| --mantine-primary-color-0 | var(--mantine-color-blue-0) |
| --mantine-primary-color-1 | var(--mantine-color-blue-1) |
| --mantine-primary-color-2 | var(--mantine-color-blue-2) |
| --mantine-primary-color-3 | var(--mantine-color-blue-3) |
| --mantine-primary-color-4 | var(--mantine-color-blue-4) |
| --mantine-primary-color-5 | var(--mantine-color-blue-5) |
| --mantine-primary-color-6 | var(--mantine-color-blue-6) |
| --mantine-primary-color-7 | var(--mantine-color-blue-7) |
| --mantine-primary-color-8 | var(--mantine-color-blue-8) |
| --mantine-primary-color-9 | var(--mantine-color-blue-9) |

#### Color Palette - Dark
| Variable | Value |
|----------|-------|
| --mantine-color-dark-0 | #C9C9C9 |
| --mantine-color-dark-1 | #b8b8b8 |
| --mantine-color-dark-2 | #828282 |
| --mantine-color-dark-3 | #696969 |
| --mantine-color-dark-4 | #424242 |
| --mantine-color-dark-5 | #3b3b3b |
| --mantine-color-dark-6 | #2e2e2e |
| --mantine-color-dark-7 | #242424 |
| --mantine-color-dark-8 | #1f1f1f |
| --mantine-color-dark-9 | #141414 |

#### Color Palette - Gray
| Variable | Value |
|----------|-------|
| --mantine-color-gray-0 | #f8f9fa |
| --mantine-color-gray-1 | #f1f3f5 |
| --mantine-color-gray-2 | #e9ecef |
| --mantine-color-gray-3 | #dee2e6 |
| --mantine-color-gray-4 | #ced4da |
| --mantine-color-gray-5 | #adb5bd |
| --mantine-color-gray-6 | #868e96 |
| --mantine-color-gray-7 | #495057 |
| --mantine-color-gray-8 | #343a40 |
| --mantine-color-gray-9 | #212529 |

#### Color Palette - Red
| Variable | Value |
|----------|-------|
| --mantine-color-red-0 | #fff5f5 |
| --mantine-color-red-1 | #ffe3e3 |
| --mantine-color-red-2 | #ffc9c9 |
| --mantine-color-red-3 | #ffa8a8 |
| --mantine-color-red-4 | #ff8787 |
| --mantine-color-red-5 | #ff6b6b |
| --mantine-color-red-6 | #fa5252 |
| --mantine-color-red-7 | #f03e3e |
| --mantine-color-red-8 | #e03131 |
| --mantine-color-red-9 | #c92a2a |

#### Color Palette - Pink
| Variable | Value |
|----------|-------|
| --mantine-color-pink-0 | #fff0f6 |
| --mantine-color-pink-1 | #ffdeeb |
| --mantine-color-pink-2 | #fcc2d7 |
| --mantine-color-pink-3 | #faa2c1 |
| --mantine-color-pink-4 | #f783ac |
| --mantine-color-pink-5 | #f06595 |
| --mantine-color-pink-6 | #e64980 |
| --mantine-color-pink-7 | #d6336c |
| --mantine-color-pink-8 | #c2255c |
| --mantine-color-pink-9 | #a61e4d |

#### Color Palette - Grape
| Variable | Value |
|----------|-------|
| --mantine-color-grape-0 | #f8f0fc |
| --mantine-color-grape-1 | #f3d9fa |
| --mantine-color-grape-2 | #eebefa |
| --mantine-color-grape-3 | #e599f7 |
| --mantine-color-grape-4 | #da77f2 |
| --mantine-color-grape-5 | #cc5de8 |
| --mantine-color-grape-6 | #be4bdb |
| --mantine-color-grape-7 | #ae3ec9 |
| --mantine-color-grape-8 | #9c36b5 |
| --mantine-color-grape-9 | #862e9c |

#### Color Palette - Violet
| Variable | Value |
|----------|-------|
| --mantine-color-violet-0 | #f3f0ff |
| --mantine-color-violet-1 | #e5dbff |
| --mantine-color-violet-2 | #d0bfff |
| --mantine-color-violet-3 | #b197fc |
| --mantine-color-violet-4 | #9775fa |
| --mantine-color-violet-5 | #845ef7 |
| --mantine-color-violet-6 | #7950f2 |
| --mantine-color-violet-7 | #7048e8 |
| --mantine-color-violet-8 | #6741d9 |
| --mantine-color-violet-9 | #5f3dc4 |

#### Color Palette - Indigo
| Variable | Value |
|----------|-------|
| --mantine-color-indigo-0 | #edf2ff |
| --mantine-color-indigo-1 | #dbe4ff |
| --mantine-color-indigo-2 | #bac8ff |
| --mantine-color-indigo-3 | #91a7ff |
| --mantine-color-indigo-4 | #748ffc |
| --mantine-color-indigo-5 | #5c7cfa |
| --mantine-color-indigo-6 | #4c6ef5 |
| --mantine-color-indigo-7 | #4263eb |
| --mantine-color-indigo-8 | #3b5bdb |
| --mantine-color-indigo-9 | #364fc7 |

#### Color Palette - Blue
| Variable | Value |
|----------|-------|
| --mantine-color-blue-0 | #e7f5ff |
| --mantine-color-blue-1 | #d0ebff |
| --mantine-color-blue-2 | #a5d8ff |
| --mantine-color-blue-3 | #74c0fc |
| --mantine-color-blue-4 | #4dabf7 |
| --mantine-color-blue-5 | #339af0 |
| --mantine-color-blue-6 | #228be6 |
| --mantine-color-blue-7 | #1c7ed6 |
| --mantine-color-blue-8 | #1971c2 |
| --mantine-color-blue-9 | #1864ab |

#### Color Palette - Cyan
| Variable | Value |
|----------|-------|
| --mantine-color-cyan-0 | #e3fafc |
| --mantine-color-cyan-1 | #c5f6fa |
| --mantine-color-cyan-2 | #99e9f2 |
| --mantine-color-cyan-3 | #66d9e8 |
| --mantine-color-cyan-4 | #3bc9db |
| --mantine-color-cyan-5 | #22b8cf |
| --mantine-color-cyan-6 | #15aabf |
| --mantine-color-cyan-7 | #1098ad |
| --mantine-color-cyan-8 | #0c8599 |
| --mantine-color-cyan-9 | #0b7285 |

#### Color Palette - Teal
| Variable | Value |
|----------|-------|
| --mantine-color-teal-0 | #e6fcf5 |
| --mantine-color-teal-1 | #c3fae8 |
| --mantine-color-teal-2 | #96f2d7 |
| --mantine-color-teal-3 | #63e6be |
| --mantine-color-teal-4 | #38d9a9 |
| --mantine-color-teal-5 | #20c997 |
| --mantine-color-teal-6 | #12b886 |
| --mantine-color-teal-7 | #0ca678 |
| --mantine-color-teal-8 | #099268 |
| --mantine-color-teal-9 | #087f5b |

#### Color Palette - Green
| Variable | Value |
|----------|-------|
| --mantine-color-green-0 | #ebfbee |
| --mantine-color-green-1 | #d3f9d8 |
| --mantine-color-green-2 | #b2f2bb |
| --mantine-color-green-3 | #8ce99a |
| --mantine-color-green-4 | #69db7c |
| --mantine-color-green-5 | #51cf66 |
| --mantine-color-green-6 | #40c057 |
| --mantine-color-green-7 | #37b24d |
| --mantine-color-green-8 | #2f9e44 |
| --mantine-color-green-9 | #2b8a3e |

#### Color Palette - Lime
| Variable | Value |
|----------|-------|
| --mantine-color-lime-0 | #f4fce3 |
| --mantine-color-lime-1 | #e9fac8 |
| --mantine-color-lime-2 | #d8f5a2 |
| --mantine-color-lime-3 | #c0eb75 |
| --mantine-color-lime-4 | #a9e34b |
| --mantine-color-lime-5 | #94d82d |
| --mantine-color-lime-6 | #82c91e |
| --mantine-color-lime-7 | #74b816 |
| --mantine-color-lime-8 | #66a80f |
| --mantine-color-lime-9 | #5c940d |

#### Color Palette - Yellow
| Variable | Value |
|----------|-------|
| --mantine-color-yellow-0 | #fff9db |
| --mantine-color-yellow-1 | #fff3bf |
| --mantine-color-yellow-2 | #ffec99 |
| --mantine-color-yellow-3 | #ffe066 |
| --mantine-color-yellow-4 | #ffd43b |
| --mantine-color-yellow-5 | #fcc419 |
| --mantine-color-yellow-6 | #fab005 |
| --mantine-color-yellow-7 | #f59f00 |
| --mantine-color-yellow-8 | #f08c00 |
| --mantine-color-yellow-9 | #e67700 |
#
### Color Palette - Orange
| Variable | Value |
|----------|-------|
| --mantine-color-orange-0 | #fff4e6 |
| --mantine-color-orange-1 | #ffe8cc |
| --mantine-color-orange-2 | #ffd8a8 |
| --mantine-color-orange-3 | #ffc078 |
| --mantine-color-orange-4 | #ffa94d |
| --mantine-color-orange-5 | #ff922b |
| --mantine-color-orange-6 | #fd7e14 |
| --mantine-color-orange-7 | #f76707 |
| --mantine-color-orange-8 | #e8590c |
| --mantine-color-orange-9 | #d9480f |

#### Heading Sizes
| Variable | Value |
|----------|-------|
| --mantine-h1-font-size | 2.125rem |
| --mantine-h1-line-height | 1.3 |
| --mantine-h1-font-weight | 700 |
| --mantine-h2-font-size | 1.625rem |
| --mantine-h2-line-height | 1.35 |
| --mantine-h2-font-weight | 700 |
| --mantine-h3-font-size | 1.375rem |
| --mantine-h3-line-height | 1.4 |
| --mantine-h3-font-weight | 700 |
| --mantine-h4-font-size | 1.125rem |
| --mantine-h4-line-height | 1.45 |
| --mantine-h4-font-weight | 700 |
| --mantine-h5-font-size | 1rem |
| --mantine-h5-line-height | 1.5 |
| --mantine-h5-font-weight | 700 |
| --mantine-h6-font-size | 0.875rem |
| --mantine-h6-line-height | 1.5 |
| --mantine-h6-font-weight | 700 |

### Light Color Scheme Only Variables

| Variable | Value |
|----------|-------|
| --mantine-primary-color-contrast | var(--mantine-color-white) |
| --mantine-color-bright | var(--mantine-color-black) |
| --mantine-color-text | #000 |
| --mantine-color-body | #fff |
| --mantine-color-error | var(--mantine-color-red-6) |
| --mantine-color-placeholder | var(--mantine-color-gray-5) |
| --mantine-color-anchor | var(--mantine-color-blue-6) |
| --mantine-color-default | var(--mantine-color-white) |
| --mantine-color-default-hover | var(--mantine-color-gray-0) |
| --mantine-color-default-color | var(--mantine-color-black) |
| --mantine-color-default-border | var(--mantine-color-gray-4) |
| --mantine-color-dimmed | var(--mantine-color-gray-6) |
| --mantine-color-disabled | var(--mantine-color-gray-2) |
| --mantine-color-disabled-color | var(--mantine-color-gray-5) |
| --mantine-color-disabled-border | var(--mantine-color-gray-3) |
| --mantine-color-dark-text | var(--mantine-color-dark-filled) |
| --mantine-color-dark-filled | var(--mantine-color-dark-6) |
| --mantine-color-dark-filled-hover | var(--mantine-color-dark-7) |
| --mantine-color-dark-light | rgba(46, 46, 46, 0.1) |
| --mantine-color-dark-light-hover | rgba(46, 46, 46, 0.12) |
| --mantine-color-dark-light-color | var(--mantine-color-dark-6) |
| --mantine-color-dark-outline | var(--mantine-color-dark-6) |
| --mantine-color-dark-outline-hover | rgba(46, 46, 46, 0.05) |
| --mantine-color-gray-text | var(--mantine-color-gray-filled) |
| --mantine-color-gray-filled | var(--mantine-color-gray-6) |
| --mantine-color-gray-filled-hover | var(--mantine-color-gray-7) |
| --mantine-color-gray-light | rgba(134, 142, 150, 0.1) |
| --mantine-color-gray-light-hover | rgba(134, 142, 150, 0.12) |
| --mantine-color-gray-light-color | var(--mantine-color-gray-6) |
| --mantine-color-gray-outline | var(--mantine-color-gray-6) |
| --mantine-color-gray-outline-hover | rgba(134, 142, 150, 0.05) |
| --mantine-color-red-text | var(--mantine-color-red-filled) |
| --mantine-color-red-filled | var(--mantine-color-red-6) |
| --mantine-color-red-filled-hover | var(--mantine-color-red-7) |
| --mantine-color-red-light | rgba(250, 82, 82, 0.1) |
| --mantine-color-red-light-hover | rgba(250, 82, 82, 0.12) |
| --mantine-color-red-light-color | var(--mantine-color-red-6) |
| --mantine-color-red-outline | var(--mantine-color-red-6) |
| --mantine-color-red-outline-hover | rgba(250, 82, 82, 0.05) |
| --mantine-color-pink-text | var(--mantine-color-pink-filled) |
| --mantine-color-pink-filled | var(--mantine-color-pink-6) |
| --mantine-color-pink-filled-hover | var(--mantine-color-pink-7) |
| --mantine-color-pink-light | rgba(230, 73, 128, 0.1) |
| --mantine-color-pink-light-hover | rgba(230, 73, 128, 0.12) |
| --mantine-color-pink-light-color | var(--mantine-color-pink-6) |
| --mantine-color-pink-outline | var(--mantine-color-pink-6) |
| --mantine-color-pink-outline-hover | rgba(230, 73, 128, 0.05) |
| --mantine-color-grape-text | var(--mantine-color-grape-filled) |
| --mantine-color-grape-filled | var(--mantine-color-grape-6) |
| --mantine-color-grape-filled-hover | var(--mantine-color-grape-7) |
| --mantine-color-grape-light | rgba(190, 75, 219, 0.1) |
| --mantine-color-grape-light-hover | rgba(190, 75, 219, 0.12) |
| --mantine-color-grape-light-color | var(--mantine-color-grape-6) |
| --mantine-color-grape-outline | var(--mantine-color-grape-6) |
| --mantine-color-grape-outline-hover | rgba(190, 75, 219, 0.05) |
| --mantine-color-violet-text | var(--mantine-color-violet-filled) |
| --mantine-color-violet-filled | var(--mantine-color-violet-6) |
| --mantine-color-violet-filled-hover | var(--mantine-color-violet-7) |
| --mantine-color-violet-light | rgba(121, 80, 242, 0.1) |
| --mantine-color-violet-light-hover | rgba(121, 80, 242, 0.12) |
| --mantine-color-violet-light-color | var(--mantine-color-violet-6) |
| --mantine-color-violet-outline | var(--mantine-color-violet-6) |
| --mantine-color-violet-outline-hover | rgba(121, 80, 242, 0.05) |
| --mantine-color-indigo-text | var(--mantine-color-indigo-filled) |
| --mantine-color-indigo-filled | var(--mantine-color-indigo-6) |
| --mantine-color-indigo-filled-hover | var(--mantine-color-indigo-7) |
| --mantine-color-indigo-light | rgba(76, 110, 245, 0.1) |
| --mantine-color-indigo-light-hover | rgba(76, 110, 245, 0.12) |
| --mantine-color-indigo-light-color | var(--mantine-color-indigo-6) |
| --mantine-color-indigo-outline | var(--mantine-color-indigo-6) |
| --mantine-color-indigo-outline-hover | rgba(76, 110, 245, 0.05) |
| --mantine-color-blue-text | var(--mantine-color-blue-filled) |
| --mantine-color-blue-filled | var(--mantine-color-blue-6) |
| --mantine-color-blue-filled-hover | var(--mantine-color-blue-7) |
| --mantine-color-blue-light | rgba(34, 139, 230, 0.1) |
| --mantine-color-blue-light-hover | rgba(34, 139, 230, 0.12) |
| --mantine-color-blue-light-color | var(--mantine-color-blue-6) |
| --mantine-color-blue-outline | var(--mantine-color-blue-6) |
| --mantine-color-blue-outline-hover | rgba(34, 139, 230, 0.05) |
| --mantine-color-cyan-text | var(--mantine-color-cyan-filled) |
| --mantine-color-cyan-filled | var(--mantine-color-cyan-6) |
| --mantine-color-cyan-filled-hover | var(--mantine-color-cyan-7) |
| --mantine-color-cyan-light | rgba(21, 170, 191, 0.1) |
| --mantine-color-cyan-light-hover | rgba(21, 170, 191, 0.12) |
| --mantine-color-cyan-light-color | var(--mantine-color-cyan-6) |
| --mantine-color-cyan-outline | var(--mantine-color-cyan-6) |
| --mantine-color-cyan-outline-hover | rgba(21, 170, 191, 0.05) |
| --mantine-color-teal-text | var(--mantine-color-teal-filled) |
| --mantine-color-teal-filled | var(--mantine-color-teal-6) |
| --mantine-color-teal-filled-hover | var(--mantine-color-teal-7) |
| --mantine-color-teal-light | rgba(18, 184, 134, 0.1) |
| --mantine-color-teal-light-hover | rgba(18, 184, 134, 0.12) |
| --mantine-color-teal-light-color | var(--mantine-color-teal-6) |
| --mantine-color-teal-outline | var(--mantine-color-teal-6) |
| --mantine-color-teal-outline-hover | rgba(18, 184, 134, 0.05) |
| --mantine-color-green-text | var(--mantine-color-green-filled) |
| --mantine-color-green-filled | var(--mantine-color-green-6) |
| --mantine-color-green-filled-hover | var(--mantine-color-green-7) |
| --mantine-color-green-light | rgba(64, 192, 87, 0.1) |
| --mantine-color-green-light-hover | rgba(64, 192, 87, 0.12) |
| --mantine-color-green-light-color | var(--mantine-color-green-6) |
| --mantine-color-green-outline | var(--mantine-color-green-6) |
| --mantine-color-green-outline-hover | rgba(64, 192, 87, 0.05) |
| --mantine-color-lime-text | var(--mantine-color-lime-filled) |
| --mantine-color-lime-filled | var(--mantine-color-lime-6) |
| --mantine-color-lime-filled-hover | var(--mantine-color-lime-7) |
| --mantine-color-lime-light | rgba(130, 201, 30, 0.1) |
| --mantine-color-lime-light-hover | rgba(130, 201, 30, 0.12) |
| --mantine-color-lime-light-color | var(--mantine-color-lime-6) |
| --mantine-color-lime-outline | var(--mantine-color-lime-6) |
| --mantine-color-lime-outline-hover | rgba(130, 201, 30, 0.05) |
| --mantine-color-yellow-text | var(--mantine-color-yellow-filled) |
| --mantine-color-yellow-filled | var(--mantine-color-yellow-6) |
| --mantine-color-yellow-filled-hover | var(--mantine-color-yellow-7) |
| --mantine-color-yellow-light | rgba(250, 176, 5, 0.1) |
| --mantine-color-yellow-light-hover | rgba(250, 176, 5, 0.12) |
| --mantine-color-yellow-light-color | var(--mantine-color-yellow-6) |
| --mantine-color-yellow-outline | var(--mantine-color-yellow-6) |
| --mantine-color-yellow-outline-hover | rgba(250, 176, 5, 0.05) |
| --mantine-color-orange-text | var(--mantine-color-orange-filled) |
| --mantine-color-orange-filled | var(--mantine-color-orange-6) |
| --mantine-color-orange-filled-hover | var(--mantine-color-orange-7) |
| --mantine-color-orange-light | rgba(253, 126, 20, 0.1) |
| --mantine-color-orange-light-hover | rgba(253, 126, 20, 0.12) |
| --mantine-color-orange-light-color | var(--mantine-color-orange-6) |
| --mantine-color-orange-outline | var(--mantine-color-orange-6) |
| --mantine-color-orange-outline-hover | rgba(253, 126, 20, 0.05) |

### Dark Color Scheme Only Variables

| Variable | Value |
|----------|-------|
| --mantine-primary-color-contrast | var(--mantine-color-white) |
| --mantine-color-bright | var(--mantine-color-white) |
| --mantine-color-text | var(--mantine-color-dark-0) |
| --mantine-color-body | var(--mantine-color-dark-7) |
| --mantine-color-error | var(--mantine-color-red-8) |
| --mantine-color-placeholder | var(--mantine-color-dark-3) |
| --mantine-color-anchor | var(--mantine-color-blue-4) |
| --mantine-color-default | var(--mantine-color-dark-6) |
| --mantine-color-default-hover | var(--mantine-color-dark-5) |
| --mantine-color-default-color | var(--mantine-color-white) |
| --mantine-color-default-border | var(--mantine-color-dark-4) |
| --mantine-color-dimmed | var(--mantine-color-dark-2) |
| --mantine-color-disabled | var(--mantine-color-dark-6) |
| --mantine-color-disabled-color | var(--mantine-color-dark-3) |
| --mantine-color-disabled-border | var(--mantine-color-dark-4) |
| --mantine-color-dark-text | var(--mantine-color-dark-4) |
| --mantine-color-dark-filled | var(--mantine-color-dark-8) |
| --mantine-color-dark-filled-hover | var(--mantine-color-dark-9) |
| --mantine-color-dark-light | rgba(46, 46, 46, 0.15) |
| --mantine-color-dark-light-hover | rgba(46, 46, 46, 0.2) |
| --mantine-color-dark-light-color | var(--mantine-color-dark-3) |
| --mantine-color-dark-outline | var(--mantine-color-dark-4) |
| --mantine-color-dark-outline-hover | rgba(66, 66, 66, 0.05) |
| --mantine-color-gray-text | var(--mantine-color-gray-4) |
| --mantine-color-gray-filled | var(--mantine-color-gray-8) |
| --mantine-color-gray-filled-hover | var(--mantine-color-gray-9) |
| --mantine-color-gray-light | rgba(134, 142, 150, 0.15) |
| --mantine-color-gray-light-hover | rgba(134, 142, 150, 0.2) |
| --mantine-color-gray-light-color | var(--mantine-color-gray-3) |
| --mantine-color-gray-outline | var(--mantine-color-gray-4) |
| --mantine-color-gray-outline-hover | rgba(206, 212, 218, 0.05) |
| --mantine-color-red-text | var(--mantine-color-red-4) |
| --mantine-color-red-filled | var(--mantine-color-red-8) |
| --mantine-color-red-filled-hover | var(--mantine-color-red-9) |
| --mantine-color-red-light | rgba(250, 82, 82, 0.15) |
| --mantine-color-red-light-hover | rgba(250, 82, 82, 0.2) |
| --mantine-color-red-light-color | var(--mantine-color-red-3) |
| --mantine-color-red-outline | var(--mantine-color-red-4) |
| --mantine-color-red-outline-hover | rgba(255, 135, 135, 0.05) |
| --mantine-color-pink-text | var(--mantine-color-pink-4) |
| --mantine-color-pink-filled | var(--mantine-color-pink-8) |
| --mantine-color-pink-filled-hover | var(--mantine-color-pink-9) |
| --mantine-color-pink-light | rgba(230, 73, 128, 0.15) |
| --mantine-color-pink-light-hover | rgba(230, 73, 128, 0.2) |
| --mantine-color-pink-light-color | var(--mantine-color-pink-3) |
| --mantine-color-pink-outline | var(--mantine-color-pink-4) |
| --mantine-color-pink-outline-hover | rgba(247, 131, 172, 0.05) |
| --mantine-color-grape-text | var(--mantine-color-grape-4) |
| --mantine-color-grape-filled | var(--mantine-color-grape-8) |
| --mantine-color-grape-filled-hover | var(--mantine-color-grape-9) |
| --mantine-color-grape-light | rgba(190, 75, 219, 0.15) |
| --mantine-color-grape-light-hover | rgba(190, 75, 219, 0.2) |
| --mantine-color-grape-light-color | var(--mantine-color-grape-3) |
| --mantine-color-grape-outline | var(--mantine-color-grape-4) |
| --mantine-color-grape-outline-hover | rgba(218, 119, 242, 0.05) |
| --mantine-color-violet-text | var(--mantine-color-violet-4) |
| --mantine-color-violet-filled | var(--mantine-color-violet-8) |
| --mantine-color-violet-filled-hover | var(--mantine-color-violet-9) |
| --mantine-color-violet-light | rgba(121, 80, 242, 0.15) |
| --mantine-color-violet-light-hover | rgba(121, 80, 242, 0.2) |
| --mantine-color-violet-light-color | var(--mantine-color-violet-3) |
| --mantine-color-violet-outline | var(--mantine-color-violet-4) |
| --mantine-color-violet-outline-hover | rgba(151, 117, 250, 0.05) |
| --mantine-color-indigo-text | var(--mantine-color-indigo-4) |
| --mantine-color-indigo-filled | var(--mantine-color-indigo-8) |
| --mantine-color-indigo-filled-hover | var(--mantine-color-indigo-9) |
| --mantine-color-indigo-light | rgba(76, 110, 245, 0.15) |
| --mantine-color-indigo-light-hover | rgba(76, 110, 245, 0.2) |
| --mantine-color-indigo-light-color | var(--mantine-color-indigo-3) |
| --mantine-color-indigo-outline | var(--mantine-color-indigo-4) |
| --mantine-color-indigo-outline-hover | rgba(116, 143, 252, 0.05) |
| --mantine-color-blue-text | var(--mantine-color-blue-4) |
| --mantine-color-blue-filled | var(--mantine-color-blue-8) |
| --mantine-color-blue-filled-hover | var(--mantine-color-blue-9) |
| --mantine-color-blue-light | rgba(34, 139, 230, 0.15) |
| --mantine-color-blue-light-hover | rgba(34, 139, 230, 0.2) |
| --mantine-color-blue-light-color | var(--mantine-color-blue-3) |
| --mantine-color-blue-outline | var(--mantine-color-blue-4) |
| --mantine-color-blue-outline-hover | rgba(77, 171, 247, 0.05) |
| --mantine-color-cyan-text | var(--mantine-color-cyan-4) |
| --mantine-color-cyan-filled | var(--mantine-color-cyan-8) |
| --mantine-color-cyan-filled-hover | var(--mantine-color-cyan-9) |
| --mantine-color-cyan-light | rgba(21, 170, 191, 0.15) |
| --mantine-color-cyan-light-hover | rgba(21, 170, 191, 0.2) |
| --mantine-color-cyan-light-color | var(--mantine-color-cyan-3) |
| --mantine-color-cyan-outline | var(--mantine-color-cyan-4) |
| --mantine-color-cyan-outline-hover | rgba(59, 201, 219, 0.05) |
| --mantine-color-teal-text | var(--mantine-color-teal-4) |
| --mantine-color-teal-filled | var(--mantine-color-teal-8) |
| --mantine-color-teal-filled-hover | var(--mantine-color-teal-9) |
| --mantine-color-teal-light | rgba(18, 184, 134, 0.15) |
| --mantine-color-teal-light-hover | rgba(18, 184, 134, 0.2) |
| --mantine-color-teal-light-color | var(--mantine-color-teal-3) |
| --mantine-color-teal-outline | var(--mantine-color-teal-4) |
| --mantine-color-teal-outline-hover | rgba(56, 217, 169, 0.05) |
| --mantine-color-green-text | var(--mantine-color-green-4) |
| --mantine-color-green-filled | var(--mantine-color-green-8) |
| --mantine-color-green-filled-hover | var(--mantine-color-green-9) |
| --mantine-color-green-light | rgba(64, 192, 87, 0.15) |
| --mantine-color-green-light-hover | rgba(64, 192, 87, 0.2) |
| --mantine-color-green-light-color | var(--mantine-color-green-3) |
| --mantine-color-green-outline | var(--mantine-color-green-4) |
| --mantine-color-green-outline-hover | rgba(105, 219, 124, 0.05) |
| --mantine-color-lime-text | var(--mantine-color-lime-4) |
| --mantine-color-lime-filled | var(--mantine-color-lime-8) |
| --mantine-color-lime-filled-hover | var(--mantine-color-lime-9) |
| --mantine-color-lime-light | rgba(130, 201, 30, 0.15) |
| --mantine-color-lime-light-hover | rgba(130, 201, 30, 0.2) |
| --mantine-color-lime-light-color | var(--mantine-color-lime-3) |
| --mantine-color-lime-outline | var(--mantine-color-lime-4) |
| --mantine-color-lime-outline-hover | rgba(169, 227, 75, 0.05) |
| --mantine-color-yellow-text | var(--mantine-color-yellow-4) |
| --mantine-color-yellow-filled | var(--mantine-color-yellow-8) |
| --mantine-color-yellow-filled-hover | var(--mantine-color-yellow-9) |
| --mantine-color-yellow-light | rgba(250, 176, 5, 0.15) |
| --mantine-color-yellow-light-hover | rgba(250, 176, 5, 0.2) |
| --mantine-color-yellow-light-color | var(--mantine-color-yellow-3) |
| --mantine-color-yellow-outline | var(--mantine-color-yellow-4) |
| --mantine-color-yellow-outline-hover | rgba(255, 212, 59, 0.05) |
| --mantine-color-orange-text | var(--mantine-color-orange-4) |
| --mantine-color-orange-filled | var(--mantine-color-orange-8) |
| --mantine-color-orange-filled-hover | var(--mantine-color-orange-9) |
| --mantine-color-orange-light | rgba(253, 126, 20, 0.15) |
| --mantine-color-orange-light-hover | rgba(253, 126, 20, 0.2) |
| --mantine-color-orange-light-color | var(--mantine-color-orange-3) |
| --mantine-color-orange-outline | var(--mantine-color-orange-4) |
| --mantine-color-orange-outline-hover | rgba(255, 169, 77, 0.05) |

---

> Dash Mantine Components v2.4.0 Documentation for Responsive Styles
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Responsive Styles
Responsive styles let you adjust the appearance of individual components, including font size, visibility, spacing, and colors, based on screen size.
Category: Styling

Note:  If you are looking for how to structure app’s layout responsively, use components like
[Grid](/components/grid) and [Group](/components/group), [Stack](/components/stack) and others. Check out the [Layout Overview](/layout-overview) section
for tips on selecting the right layout components.

### Media Queries

Resize the browser window to see the color changing between blue and red.

```python
from dash import html

component = html.Div("Demo", className="media-query-demo")
```
```css

.media-query-demo  {
  background-color: var(--mantine-color-blue-filled);
  color: var(--mantine-color-white);
  padding: var(--mantine-spacing-md);
  text-align: center;

  @media (min-width: 48em) {
    background-color: var(--mantine-color-red-filled);
  }
}

```

When choosing between pixels (px) and rems (rem or em) for media queries, it's generally recommended to use rems because they
are relative to the user's font size, making your design more accessible and responsive to different browser zoom
levels; whereas pixels are absolute and won't adjust with font size changes.

Note that the rem unit is relative to the document's root element, while the em unit is relative to the immediate
parent of the targeted element. In Mantine, breakpoints are expected to be set in em units to align with its contextual
scaling approach.

### Configure breakpoints
`theme.breakpoints` are used in all responsive Mantine components. Breakpoints are expected to be set in `em` units. You
can configure these values in the [Theme Object](/theme-object) in the `MantineProvider`:

You can customize the `breakpoints` defaults in the `theme`:

```python
theme = {
    "breakpoints": {
        "xs": '30em',              # customize breakpoints here
        "sm": '48em',
        "md": '64em',
        "lg": '74em',
        "xl": '90em',
  },
}

dmc.MantineProvider(
    # your layout,
    theme=theme
)
```

### Default `theme.breakpoints` Values

| Breakpoint | Viewport width | Value in px |
|------------|----------------|-------------|
| xs         | 36em           | 576px       |
| sm         | 48em           | 768px       |
| md         | 62em           | 992px       |
| lg         | 75em           | 1200px      |
| xl         | 88em           | 1408px      |



### hiddenFrom and visibleFrom props
All Mantine components that have a root element support `hiddenFrom` and `visibleFrom` props. These props accept breakpoint
(`xs`, `sm`, `md`, `lg`, `xl`) and hide the component when viewport width is less than or greater than the specified breakpoint:


```python
import dash_mantine_components as dmc

component = dmc.Group(
    justify="center",
    children=[
        dmc.Button(
            "Hidden from sm",
            hiddenFrom="sm",
            color="orange"
        ),
        dmc.Button(
            "Visible from sm",
            visibleFrom="sm",
            color="cyan"
        ),
        dmc.Button(
            "Visible from md",
            visibleFrom="md",
            color="pink"
        )
    ]
)
```
### Hidden and visible from as classes
If you are building a component and want to use the same logic as in `hiddenFrom` and `visibleFrom` props but you do
not want to use Mantine components, you can use` mantine-hidden-from-{x}` and `mantine-visible-from-{x}` classes.

```python
html.Div("Hidden from md", className="mantine-hidden-from-md")
html.Div("visible from xl", className="mantine-visible-from-xl")

```

### Component size based on media query
Some components support `size` prop, which changes various aspects of component appearance. `size` prop is not
responsive – it is not possible to define different component sizes for different screen sizes.

### Container queries
Container queries enable you to apply styles to an element based on the size of the element's container. If, for
example, a container has less space available in the surrounding context, you can hide certain elements or use
smaller fonts. Container queries are supported in all modern browsers.

Note that CSS variables do not work in container queries and because of that rem scaling feature is not available.
If you rely on this feature, it is better to define breakpoints in px units.


```python
from dash import html
import dash_mantine_components as dmc

component = html.Div(
    className="container-query-demo-root",
    children=html.Div(
        "Resize parent element to see container query in action",
        className="container-query-demo-child"
    )
)
```
Add the following to a .css file in /assets

```css

.container-query-demo-root {
  min-width: 200px;
  max-width: 100%;
  min-height: 120px;
  container-type: inline-size;
  overflow: auto;
  resize: horizontal;
  border: solid;
  border-color: var(--mantine-color-default-border)
}

.container-query-demo-child {
  background-color: var(--mantine-color-dimmed);
  color: var(--mantine-color-white);
  padding: var(--mantine-spacing-md);

  @container (max-width: 500px) {
    background-color: var(--mantine-color-blue-filled);
  }

  @container (max-width: 300px) {
    background-color: var(--mantine-color-red-filled);
  }
}
```

### Responsive styles

You can pass a dictionary to style props to add responsive styles with [style props](/style-props).
Note that responsive style props are less performant than regular style props, it is not recommended using them in large amounts.

```python
import dash_mantine_components as dmc

component = dmc.Box(
    "Box with responsive style props",
    w={"base": 200, "sm": 400, "lg": 500},
    py={"base": "xs", "sm": "md", "lg": "xl"},
    bg={"base": "blue.7", "sm": "red.7", "lg": "green.7"},
    c="#fff",
    ta="center",
    mx="auto",
)
```
Responsive values are calculated the following way:

- `base` value is used when none of the breakpoint values are provided
- `xs`, `sm`, `md`, `lg`, `xl` values are used when the viewport width is larger that the value of corresponding breakpoint specified in `dmc.DEFAULT_THEME`.

```python
import dash_mantine_components as dmc

dmc.Box(w={ "base": 320, "sm": 480, "lg": 640 })
```

In this case the element will have the following styles:

```css
/* Base styles added to element and then get overwritten with responsive values */
.element {
  width: 20rem;
}

/* 48em is theme.breakpoints.sm by default */
@media (min-width: 48em) {
  .element {
    width: 30rem;
  }
}

/* 75em is theme.breakpoints.lg by default */
@media (min-width: 75em) {
  .element {
    width: 40rem;
  }
}
```

---


> Dash Mantine Components v2.4.0 Documentation for Right-to-left direction
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Right-to-left direction
All Mantine components support right-to-left direction out of the box. You can preview how components work with RTL direction by clicking direction control in the top right corner.
Category: Styling

### DirectionProvider

`DirectionProvider` component is used to set direction for all components inside it. It is required to wrap your
application with `DirectionProvider` if you are planning to either use RTL direction or change direction dynamically.

```python
app.layout=dmc.DirectionProvider(
    dmc.MantineProvider(
        # your layout
    ),
    direction="rtl",  # or "ltr"
    id="direction-provider"
)
```

The `direction` prop sets the `dir` attribute on the root element of your application, the `html` element.

### RTL direction toggle

You can change the text direction by updating the `direction` prop in a callback.

Here is a minimal example of a RTL direction toggle, similar to the one used in the DMC documentation:

```python

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

app = Dash()

layout = dmc.Stack([
    dmc.Group([
        dmc.Title("RTL Direction demo", order=3),
        dmc.ActionIcon(
            DashIconify(icon="tabler:text-direction-rtl", width=18),
            id="rtl-toggle",
            variant="outline",
        ),
    ], justify="space-between"),
    dmc.Slider(value=25, labelAlwaysOn=True, mt="xl"),
], m="lg")

app.layout = dmc.DirectionProvider(
    dmc.MantineProvider(layout),
    id="direction-provider",
    direction="ltr"
)

@callback(
    Output("rtl-toggle", "children"),
    Output("direction-provider", "direction"),
    Input("rtl-toggle", "n_clicks"),
    State("direction-provider", "direction")
)
def toggle_direction(n, d):
    if n is None:
        raise PreventUpdate

    new_dir = "ltr" if d == "rtl" else "rtl"
    return DashIconify(icon=f"tabler:text-direction-{d}", width=18), new_dir


if __name__ == "__main__":
    app.run(debug=True)

```
