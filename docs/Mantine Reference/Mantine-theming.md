
> Dash Mantine Components v2.4.0 Documentation for MantineProvider
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## MantineProvider
Use MantineProvider component to manage themes in your app globally.
Category: Theming

Wrap your `app.layout` with a single `MantineProvider` to enable theming and styling features across your app. There should only be one `MantineProvider` in your app.

The `MantineProvider`:

1. Sets the global theme, including colors, spacing, and fonts.
2. Handles light and dark mode toggling.
3. Provides Mantine CSS variables according to the selected theme.

### Usage

Your app must be wrapped inside a MantineProvider, and it must be used only once.

```python
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
    theme = {...},
    children={...}
)
```

### theme object

See the [Theme Object](/theme-object) section to learn how to customize the default Mantine theme`.


### Custom Colors

See the [Colors](/colors) section to learn how to customize the theme colors.

### Light and Dark Color Schemes
Mantine supports both light and dark color schemes.  The default color scheme is "light".
When the `MantineProvider` is added to your app, it automatically sets the `data-mantine-color-scheme` attribute at the
top level of the app. This attribute controls whether the app uses light or dark mode. All components in the app
reference this attribute to decide which colors to apply.

You can change the color scheme with the `forceColorScheme` prop.

In the [Theme Switch Componets](/theme-switch) section, learn how to add a component to allow users to select either light or dark mode.

```python
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
    forceColorScheme="dark",
    theme = {...},
    children={...}
)
```


### Keyword Arguments


#### MantineProvider

- children (a list of or a singular dash component, string or number; optional):
    Your application.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- classNamesPrefix (string; optional):
    A prefix for components static classes (for example
    {selector}-Text-root), `mantine` by default.

- colorSchemeManager (dict; optional):
    Used to retrieve/set color scheme value in external storage, by
    default uses `window.localStorage`.

    `colorSchemeManager` is a dict with keys:

- cssVariablesResolver (dict; optional):
    Function to generate CSS variables based on theme object.

    `cssVariablesResolver` is a dict with keys:

- cssVariablesSelector (string; optional):
    CSS selector to which CSS variables should be added, `:root` by
    default.

- deduplicateCssVariables (boolean; optional):
    Determines whether CSS variables should be deduplicated: if CSS
    variable has the same value as in default theme, it is not added
    in the runtime. @,default,`True`.

- defaultColorScheme (a value equal to: 'auto', 'dark', 'light'; optional):
    Default color scheme value used when `colorSchemeManager` cannot
    retrieve value from external storage, `light` by default.

- env (a value equal to: 'default', 'test'; optional):
    Environment at which the provider is used, `'test'` environment
    disables all transitions and portals.

- forceColorScheme (a value equal to: 'dark', 'light'; optional):
    Forces color scheme value, if set, MantineProvider ignores
    `colorSchemeManager` and `defaultColorScheme`.

- stylesTransform (dict; optional):
    An object to transform `styles` and `sx` props into css classes,
    can be used with CSS-in-JS libraries.

    `stylesTransform` is a dict with keys:

- theme (dict; optional):
    Theme override object.

    `theme` is a dict with keys:

- withCssVariables (boolean; optional):
    Determines whether theme CSS variables should be added to given
    `cssVariablesSelector` @,default,`True`.

- withGlobalClasses (boolean; optional):
    Determines whether global classes should be added with `<style />`
    tag. Global classes are required for `hiddenFrom`/`visibleFrom`
    and `lightHidden`/`darkHidden` props to work. @,default,`True`.

- withStaticClasses (boolean; optional):
    Determines whether components should have static classes, for
    example, `mantine-Button-root`. @,default,`True`.

> Dash Mantine Components v2.4.0 Documentation for Theme Object
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com


---
## Theme Object
Mantine theme is an object where your application's colors, fonts, spacing, border-radius and other design tokens are stored.
Category: Theming

### Theme overview

Mantine’s  [default theme](/theme-object#default-theme) makes Dash apps look great in both light and dark modes. If you’re new to Dash Mantine Components,
start with the default theme. You can customize the theme globally by editing the `theme` prop in the `MantineProvider`.

The `theme` object is a dictionary where you can set things like colors, border radius, spacing, fonts, and breakpoints.
Mantine will merge your custom theme with the defaults, so you just need to provide what you want to change.

This example demonstrates how changing the `theme` updates the entire app’s appearance. Here, we change:
- Primary accent color
- Border radius
- Card shadow style
- Color scheme (light/dark)

Try it live: [DMC Theme Builder on Pycafe](https://py.cafe/app/dash.mantine.components/dash-mantine-theme-builder)

---

---


### Usage


```python
import dash_mantine_components as dmc

dmc.MantineProvider(
    theme={
        # add your colors
        "colors": {
             # add your colors
            "deepBlue": ["#E9EDFC", "#C1CCF6", "#99ABF0" "..."], # 10 colors
            # or replace default theme color
            "blue": ["#E9EDFC", "#C1CCF6", "#99ABF0" "..."],   # 10 colors
        },
        "shadows": {
            # other shadows (xs, sm, lg) will be merged from default theme
            "md": "1px 1px 3px rgba(0,0,0,.25)",
            "xl": "5px 5px 3px rgba(0,0,0,.25)",
        },
        "headings": {
            "fontFamily": "Roboto, sans-serif",
            "sizes": {
                "h1": {"fontSize": '30px'},
            },
        },
    },
    children=[
        # your app layout here
    ],
)
```


### Theme properties
You can find a complete list of all theme properties in the theme object in the references section at the bottom of the
page. In the next section, we’ll focus on a few key properties to explain them in more detail.

#### Colors

See more information and examples in [Colors](/colors) section

- `colors` adds colors or over-rides named theme colors
- `primaryColor` sets the app's primary (default) accent color
- `primaryShade` sets the app's primary shade in either light or dark mode

#### Typography

See more information and examples in [Typography](/typography) section

- `fontFamily` – controls font-family in all components except `Title`, `Code` and `Kbd`
- `fontFamilyMonospace` – controls font-family of components that require monospace font: `Code`, `Kbd` and `CodeHighlight`
- `headings.fontFamily` – controls font-family of h1-h6 tags in `Title`, fallbacks to `theme.fontFamily` if not defined
- `fontSizes` - defines the font-size from `xs` to `xl`
- `lineHeights` -defines `line-height` values for `Text` component, most other components use `theme.lineHeights.md` by default

#### Breakpoints

See more information and examples in [Responsive Styles](/responsive-styles) section

#### autoContrast
`autoContrast` controls whether text color should be changed based on the given color prop in the following components:

* `ActionIcon` with `variant='filled'` only
* `Alert` with `variant='filled'` only
* `Avatar` with `variant='filled'` only
* `Badge` with `variant='filled'` only
* `Button` with `variant='filled'` only
* `Chip` with `variant='filled'` only
* `NavLink` with `variant='filled'` only
* `ThemeIcon` with `variant='filled'` only
* `Checkbox` with `variant='filled'` only
* `Radio` with `variant='filled'` only
* `Tabs` with `variant='filled'` only
* `SegmentedControl`
* `Stepper`
* `Pagination`
* `Progress`
* `Indicator`
* `Timeline`
* `Spotlight`
* All dates components that are based on Calendar component

`autoContrast` checks whether the given color luminosity is above or below the `luminanceThreshold` value and changes text color to either `theme.white` or `theme.black` accordingly.

`autoContrast` can be set globally on the theme level or individually for each component via `autoContrast` prop, except for dates components which only support global theme setting.


```python
import dash_mantine_components as dmc

component = dmc.Box([
    dmc.Code("autoContrast=True"),
    dmc.Group(
        [
            dmc.Button("Lime.4 button", color="lime.4", autoContrast=True),
            dmc.Button("Blue.2 button", color="blue.2", autoContrast=True),
            dmc.Button("Orange.3 button", color="orange.3", autoContrast=True),
        ],
        mt="xs",
        mb="lg"
    ),
    dmc.Code("autoContrast=False"),
    dmc.Group(
        [
            dmc.Button("Lime.4 button", color="lime.4"),
            dmc.Button("Blue.2 button", color="blue.2"),
            dmc.Button("Orange.3 button", color="orange.3"),
        ],
        mt="xs"
    )
])
```
#### luminanceThreshold

`luminanceThreshold` controls which luminance value is used to determine if text color should be light or dark. It is
used only if `theme.autoContrast` is set to `True`. Default value is 0.3.

See a live demo of `luminanceThreshold` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#luminancethreshold)

```python
dmc.MantineProvider(
    dmc.Group([
        dmc.Button("button", color=f"blue.{i}") for i in range(10)
    ]),
    theme={
        "luminanceThreshold": .45,
        "autoContrast": True
    }
)
```

#### focusRing
`theme.focusRing` controls focus ring styles, it supports the following values:

- 'auto' (default and recommended) – focus ring is visible only when the user navigates with keyboard, this is the default browser behavior for native interactive elements
- 'always' – focus ring is visible when user navigates with keyboard and mouse, for example, the focus ring will be visible when user clicks on a button
- 'never' – focus ring is always hidden, it is not recommended – users who navigate with keyboard will not have visual indication of the current focused element


See a live demo of `focusRing` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#focusring)

#### focusClassName

`theme.focusClassName` is a CSS class that is added to elements that have focus styles, for example, `Button` or
`ActionIcon`. It can be used to customize focus ring styles of all interactive components except inputs. Note that when
`theme.focusClassName` is set, `theme.focusRing` is ignored.

See a live demo of `focusClassName` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#focusclassname)

```python
dmc.MantineProvider(
    dmc.Button("click button to see focus ring", m="lg"),
    theme={"focusClassName": "focus"}
)
```
Define the class in the `.css` file in `/assets` folder
```css

/* Use `&:focus` when you want focus ring to be visible when control is clicked */
.focus {
  &:focus {
    outline: 2px solid var(--mantine-color-red-filled);
    outline-offset: 3px;
  }
}
```


#### activeClassName
`theme.activeClassName` is a CSS class that is added to elements that have active styles, for example, `Button` or
`ActionIcon`. It can be used to customize active styles of all interactive components.

To disable active styles for all components, set `theme.activeClassName` to an empty string.


See a live demo of `activeClassName` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#activeclassname)

#### defaultRadius

`theme.defaultRadius` controls the default border-radius property in most components, for example, `Button` or `TextInput`.
You can set to either one of the values from `theme.radius` or a number/string to use exact value. Note that numbers are
treated as pixels, but converted to rem. For example, `{'defaultRadius': 4}` will be converted to 0.25rem. You can learn
more about rem conversion in the [rem units guide](https://mantine.dev/styles/rem/).


See a live demo of `defaultRadius` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#defaultradius)

```python

dmc.MantineProvider(
    dmc.Box([
        dmc.Button("Button", m="sm"),
        dmc.TextInput(m="sm", label="TextInput with defaultRadius", placeholder="TextInput with default radius")
    ]),
    theme={"defaultRadius": "xl"},
)
```

#### cursorType
`theme.cursorType` controls the default cursor type for interactive elements, that do not have cursor: pointer styles
by default. For example, `Checkbox`.


See a live demo of `cursorType` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#cursortype)


```python
dmc.MantineProvider(
    dmc.Checkbox(label="Pointer cursor", mt="md"),
    theme={"cursorType": 'pointer'},
)
```

#### defaultGradient
`theme.defaultGradient` controls the default gradient configuration for components that support `variant='gradient'`
(Button, ActionIcon, Badge, etc.).


See a live demo of `defaultGradient` in the [Mantine Docs](https://mantine.dev/theming/theme-object/#defaultgradient)

```python
dmc.MantineProvider(
    dmc.Button("Button with custom default gradient", variant="gradient"),
    theme={
        "defaultGradient": {
            "from": 'orange',
            "to": 'red',
            "deg": 45,
          },
    }
)
```
#### components defaultProps

Default props

You can define default props for every Mantine component by setting `theme.components`. These props will be used by
default by all components of your application unless they are overridden by component props.

See a live demo of `defaultProps` in the [Mantine Docs](https://mantine.dev/theming/default-props/)


```python
dmc.MantineProvider(
    dmc.Group(
        [
            dmc.Button("Default button"),
            dmc.Button("Button with props", color="red", variant="filled"),
        ]
    ),
    theme={
        "components": {
            "Button": {
                "defaultProps": {
                    "color": "cyan",
                    "variant": "outline",
                },
            },
        },
    }
)
```

#### components custom variants

See how to add custom variants to `ActionIcon` and `Button` in the theme object, making these variants available globally
across your app. Detailed examples are provided in their respective documentation sections.  Also, see examples live:

- [Live Demo: Button Variants on PyCafe](https://py.cafe/dash.mantine.components/button-custom-variants-demo-0)
- [Live Demo: ActionIcon Variants on PyCafe](https://py.cafe/dash.mantine.components/actionicon-custom-variants-demo)

#### components custom sizes

See and example of adding custom sizes in the  [Checkbox](/components/checkbox) section.  Also see a live dome on PyCafe:

- [Live Demo: Checkbox Sizes PyCafe](https://py.cafe/dash.mantine.components/checkbox-custom-sizes-demo)

#### other

`theme.other` is an object that can be used to store any other properties that you want to access with the theme objects.

```python
dmc.MantineProvider(
    # your app layout,
    theme={
        "other": {
            "charcoal": "#333333",
            "primaryHeadingSize": 45,
            "fontWeights": {
                "bold": 700,
                "extraBold": 900,
            },
        },
    }
)
```


### Usage in DMC docs

MantineProvider is used to customize theme for these docs as well. The theming is more or less inline with below.

```python
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
     forceColorScheme="light",
     theme={
         "primaryColor": "indigo",
         "fontFamily": "'Inter', sans-serif",
         "components": {
             "Button": {"defaultProps": {"fw": 400}},
             "Alert": {"styles": {"title": {"fontWeight": 500}}},
             "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
             "Badge": {"styles": {"root": {"fontWeight": 500}}},
             "Progress": {"styles": {"label": {"fontWeight": 500}}},
             "RingProgress": {"styles": {"label": {"fontWeight": 500}}},
             "CodeHighlightTabs": {"styles": {"file": {"padding": 12}}},
             "Table": {
                 "defaultProps": {
                     "highlightOnHover": True,
                     "withTableBorder": True,
                     "verticalSpacing": "sm",
                     "horizontalSpacing": "md",
                 }
             },
         },
     },
     children=[
         # content
     ],
 )
```

### Default theme

Default theme is available as `dmc.DEFAULT_THEME`. It includes all theme properties with default values.
When you pass theme override to MantineProvider, it will be deeply merged with the default theme.

### Theme Object Reference

| **Name**               | **Description**                                                                                                                                                                | **Type**                         |
|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------|
| `focusRing`            | Controls focus ring styles. Options: `auto` (default, shows when navigating with keyboard), `always` (shows for keyboard and mouse), `never` (always hidden, not recommended). | 'auto' or 'always' or 'never'    |
| `scale`                | rem units scale, adjust if customizing `<html />` font-size. Default: `1` (16px font-size).                                                                                    | `number`                         |
| `fontSmoothing`        | Determines whether `font-smoothing` is applied to the body. Default: `true`.                                                                                                   | `boolean`                        |
| `white`                | Base white color. Example: `#ffffff`.                                                                                                                                          | `string`                         |
| `black`                | Base black color. Example: `#000000`.                                                                                                                                          | `string`                         |
| `colors`               | Object of colors, where each key is a color name, and each value is an array of at least 10 shades. Example: `colors.blue = ['#f0f8ff', '#add8e6', ...]`.                      | `object`                         |
| `primaryShade`         | Determines which shade of `colors.primary` is used. Options: `{light: 6, dark: 8}` (default) or a single number (e.g., `6` for both modes).                                    | `number or object`               |
| `primaryColor`         | Key of `theme.colors`. Determines the default primary color. Default: `blue`.                                                                                                  | `string`                         |
| `variantColorResolver` | Function to resolve colors for variants like `Button` and `ActionIcon`. Can be used for deep customization.                                                                    | `function`                       |
| `autoContrast`         | If `true`, adjusts text color for better contrast based on the background color. Default: `false`.                                                                             | `boolean`                        |
| `luminanceThreshold`   | Threshold for determining whether text should be light or dark when `autoContrast` is enabled. Default: `0.3`.                                                                 | `number`                         |
| `fontFamily`           | Font-family used in all components. Example: `'Arial, sans-serif'`.                                                                                                            | `string`                         |
| `fontFamilyMonospace`  | Monospace font-family used in code components. Example: `'Courier, monospace'`.                                                                                                | `string`                         |
| `headings`             | Controls heading styles. Includes `fontFamily`, `fontWeight`, `textWrap` (e.g., `'wrap'`, `'nowrap'`) and sizes for `h1` to `h6` (e.g., `{'fontSize': 32, 'lineHeight': 1.4}`). | `object`                         |
| `radius`               | Object defining border-radius values. Example: `{sm: 4, md: 8, lg: 16}`.                                                                                                       | `object`                         |
| `defaultRadius`        | Default border-radius used by most components. Example: `md`.                                                                                                                  | `string`                         |
| `spacing`              | Object defining spacing values (e.g., margins, padding). Example: `{xs: 4, sm: 8, md: 16, lg: 24}`.                                                                            | `object`                         |
| `fontSizes`            | Object defining font-size values. Example: `{xs: 12, sm: 14, md: 16, lg: 20}`.                                                                                                 | `object`                         |
| `lineHeights`          | Object defining line-height values. Example: `{xs: 1.2, sm: 1.4, md: 1.6}`.                                                                                                    | `object`                         |
| `breakpoints`          | Object defining responsive breakpoints (in em). Example: `{xs: 30, sm: 48, md: 64}` (for 480px, 768px, and 1024px respectively).                                               | `object`                         |
| `shadows`              | Object defining box-shadow values. Example: `{sm: '0px 1px 3px rgba(0, 0, 0, 0.2)', md: '0px 4px 6px rgba(0, 0, 0, 0.1)'}`.                                                    | `object`                         |
| `respectReducedMotion` | If `true`, respects OS reduce-motion settings. Default: `false`.                                                                                                               | `boolean`                        |
| `cursorType`           | Determines cursor style for interactive elements. Options: `'default'` or `'pointer'`. Default: `'default'`.                                                                   | `'default' or 'pointer'`         |
| `defaultGradient`      | Default gradient configuration. Example: `{'from': '#6a11cb', 'to': '#2575fc', 'deg': 45}`.                                                                                    | `object`                         |
| `activeClassName`      | CSS class applied to elements with active styles (e.g., `Button`).                                                                                                             | `string`                         |
| `focusClassName`       | CSS class applied to elements with focus styles (overrides `focusRing`).                                                                                                       | `string`                         |
| `components`           | Customizations for individual components (e.g., default props for `Button`).                                                                                                   | `object`                         |
| `other`                | User-defined custom properties for additional flexibility.                                                                                                                     | `object`                         |

---

> Dash Mantine Components v2.4.0 Documentation for Colors
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Colors
How to use colors with Dash Mantine Components.
Category: Theming

Mantine uses [open-color](https://yeun.github.io/open-color/) in default theme with some additions. Each color has 10 shades.


### Colors in the default theme

Colors are stored in the [theme object](/theme-object) as an array of strings. Each color is indexed from `0` (lightest) to `9`
(darkest). The default theme is available as `dmc.DEFAULT_THEME`, which contains all theme properties with their default values.

For example, access a specific shade by using the color name and index: `dmc.DEFAULT_THEME['colors']['blue'][1]`
Colors with larger indices are darker.

```python
import dash_mantine_components as dmc
from dash import html

component = html.Div(
    " This is a blue element",
    style={
        "backgroundColor": dmc.DEFAULT_THEME["colors"]["blue"][1],
        "color": dmc.DEFAULT_THEME["colors"]["blue"][9],
        "padding": dmc.DEFAULT_THEME["spacing"]["lg"]
    }
)
```
When using the `color` or other style props like `c`, `bd` or `bg` prop, you can use just the color.index:

```python
import dash_mantine_components as dmc

component = dmc.Group([
    dmc.Button("Button", color="blue.3"),
    dmc.Button("Button", variant="light", color="blue.3"),
    dmc.Button("Button", variant="outline", color="blue.3")
])
```
### Colors as CSS Variables

Mantine also exposes colors as CSS variables. A complete list of Mantine CSS variables is available in the
[Mantine Docs](https://mantine.dev/styles/css-variables-list/).

If you define custom colors in the `theme` object (via the `MantineProvider` component), these will also be included as
CSS variables.

```python
import dash_mantine_components as dmc
from dash import html

component = html.Div(
    " This is a blue theme",
    style={
        "backgroundColor": "var(--mantine-color-blue-1)",
        "color": "var(--mantine-color-blue-9)",
        "padding": "var(--mantine-spacing-lg)",
    }
)
```

### Adding extra colors
You can add any number of extra colors to `theme.colors` object. This will allow you to use them in all components that
support color prop, for example `Button`, `Badge` and `Switch`.


```python
import dash_mantine_components as dmc

dmc.MantineProvider(
    theme={
        "colors": {
            "myColor": [
              "#F2FFB6",
              "#DCF97E",
              "#C3E35B",
              "#AAC944",
              "#98BC20",
              "#86AC09",
              "#78A000",
              "#668B00",
              "#547200",
              "#455D00",
            ]
        },
    },
    children=[dmc.Button("Custom Colors!", color="myColor")],
)
```
### Changing colors

You can override named theme colors as well, by providing your own list of 10 colors

```python

dmc.MantineProvider(
    theme={
        "colors": {
            "blue": [... ] # your 10 colors for "blue" theme color
        }
    }
)
```

> 10 shades per color
>
> Colors override must include at least 10 shades per color. Otherwise, you will get a TypeScript error and some
> variants will not have proper colors. If you only have one color value, you can either pick the remaining colors
> manually or use the [colors generator tool](https://mantine.dev/colors-generator/).
>
> You can add more than 10 shades per color: these values will not be used by Mantine components with the default
> colors resolver, but you can still reference them by index, for example, color="blue.11".



### Supported color formats
You can use the following color formats in theme.colors:

- HEX: #fff, #ffffff
- RGB: rgb(255, 255, 255), rgba(255, 255, 255, 0.5)
- HSL: hsl(0, 0%, 100%), hsla(0, 0%, 100%, 0.5)
- OKLCH: oklch(96.27% 0.0217 238.66), oklch(96.27% 0.0217 238.66 / 0.5)

### Changing Theme Object defaults

You can change the defaults for `primaryColor` and `primaryShade` in the [theme object](/theme-object) in the
`MantineProvider` component.

#### primaryColor

The value of `theme.primaryColor` must be defined as key of `theme.colors`, it is used:

- As a default value for most of the components that support color prop
- To set default focus ring outline color

You can customize the primary color by changing it from its default value of `blue` to another predefined theme color.

This example changed the default primary color to `green`:

```python
dmc.MantineProvider(
    theme={"primaryColor": "green"},
    children=[] # your layout here

)
```

> Note You cannot assign CSS color values to `defaultColor`  It must be a defined color in the `theme` object.



#### primaryShade

`theme.primaryShade` is a number from 0 to 9. It determines which shade will be used for the components that have color prop.

```python
dmc.MantineProvider(
    theme={"primaryShade": 3},
    children=dmc.Group([
        dmc.Button("Button",),
        dmc.Button("Button", variant="light"),
        dmc.Button("Button", variant="outline")
    ])

)
```

You can also customize primary shade for dark and light color schemes separately (This is the default):


```python
dmc.MantineProvider(
    theme={"primaryShade": { "light": 6, "dark": 8 }},
    children=[] # your layout here

)
```

### Color prop
Components that support changing their color have color prop. This prop supports the following values:

- Key of `theme.colors`, for example, `blue` or `green`
- Key of `theme.colors` with color index, for example, `blue.5` or `green.9`
- CSS color value, for example, #fff or rgba(0, 0, 0, 0.5)


```python
import dash_mantine_components as dmc

component= dmc.Box([
    dmc.Text("Filled variant", size="sm", mb=5, fw=500),
    dmc.Group([
        dmc.Button("Theme color", color="cyan"),
        dmc.Button("Hex color", color="#1D72FE")
    ]),

    dmc.Text("Light variant", size="sm", mb=5, mt="md", fw=500),
    dmc.Group([
        dmc.Button("Theme color", variant="light", color="cyan"),
        dmc.Button("Hex color", variant="light", color="#1D72FE")
    ]),

    dmc.Text("Outline variant", size="sm", mb=5, mt="md", fw=500),
    dmc.Group([
        dmc.Button("Theme color", variant="outline", color="cyan"),
        dmc.Button("Hex color", variant="outline", color="#1D72FE")
    ])
])
```
### Colors index reference
You can reference colors by index in `color` prop and style props, for example `c` prop:


```python
dmc.Text("Text with blue.5 color", c="blue.5")
dmc.Button("Button", color="blue.5")
```

### Difference between color and c props
`color` prop is used to control multiple CSS properties of the component. These properties can vary across different
components, but usually `color` prop controls `background`, `color` and `border-color` CSS properties. For example,
when you set `color='#C3FF36'` on `Button` component (with `variant='filled'`), it will set the following CSS properties:

- `background-color` to `#C3FF36`
- `background-color` when button is hovered to `#B0E631` (`#C3FF36` darkened by 10%)
- color to `var(--mantine-color-white)`
- `border-color` to `transparent`

`c` is a [style prop](/style-props) – it is responsible for setting a single CSS property `color` (color of the text).
You can combine both props to achieve better contrast between text and background. In the following example:

- `color` prop sets all background: #C3FF36 and color: `var(--mantine-color-white)`
- `c` prop overrides color styles to `color: var(--mantine-color-black)`


```python
import dash_mantine_components as dmc

component = dmc.Button("Button with color and c props",  color="#C3FF36", c="black")
```
### Colors in light and dark mode

#### Using light-dark() CSS Function
The [light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark) function allows defining different styles for light and dark color schemes.

```css
background-color: light-dark(white, black);
```

- The first argument applies in light mode.
- The second argument applies in dark mode.

Note that the light-dark() function is not supported in older browsers.

```python
import dash_mantine_components as dmc

component = dmc.Box([

    dmc.Text(
        "Click the theme switch in the header to see how the background changes in different modes:"
    ),
    # Using CSS color names
    dmc.Text(
        "light-dark(whitesmoke, gray)",
        style={"backgroundColor": "light-dark(whitesmoke, gray)"},
        p="lg",
        m="md"
    ),
    # Using Mantine CSS variables
    dmc.Text(
        "light-dark(var(--mantine-color-blue-1), var(--mantine-color-blue-9))",
        style={"backgroundColor": "light-dark(var(--mantine-color-blue-1), var(--mantine-color-blue-9))"},
        p="lg",
        m="md"
    )
])
```
#### CSS Class Names for Light/Dark Mode

Since light-dark() is not supported in older browsers, you can use class-based styling instead:

```python
import dash_mantine_components as dmc

component = dmc.Box([

    dmc.Text(
        "Click the theme switch in the header to see how the background changes in different modes"
    ),
    dmc.Text(
        "CSS class defined for light and dark scheme",
        className="light-dark-demo",
        p="lg",
        m="md"
    ),
])
```

```css
/* applied in light color-scheme */
.light-dark-demo {
    background-color: #ffec99
}

/* applied in dark color-scheme */
 [data-mantine-color-scheme='dark'] .light-dark-demo {
     background-color: #ff6b6b
}



/*
You can also use mantine colors

.light-dark-demo {
    background-color: var(--mantine-color-blue-1)
}

[data-mantine-color-scheme='dark'] .light-dark-demo {
     background-color:  var(--mantine-color-blue-1)
*/
```


#### CSS Variables for Light/Dark Mode

Defining CSS variables on the `:root` element allows global styling across your app, including the `body` element.

Here is an example using a CSS variable:

```python
import dash_mantine_components as dmc

component = dmc.Box([

    dmc.Text(
        "Click the theme switch in the header to see how the background changes in different modes:"
    ),
    dmc.Text(
        "CSS variable defined for light and dark scheme",
        style={"backgroundColor": "var(--my-light-dark-colors"},
        p="lg",
        m="md"
    ),
])
```

```css

:root {
  --my-light-dark-colors: aliceblue;
}

:root[data-mantine-color-scheme="dark"] {
  --my-light-dark-colors: blue;
}

/*
You can also use mantine colors

:root {
  --my-light-dark-colors: var(--mantine-color-blue-1);
}

:root[data-mantine-color-scheme="dark"] {
  --my-light-dark-colors: var(--mantine-color-blue-1);
}
*/


/*
The  --mantine-color-body CSS variable is used for body background and as background color
 of some components (Modal, Paper, etc.).  You can change it like this:

:root {
  --mantine-color-body: #f9f9f9;
}

:root[data-mantine-color-scheme="dark"] {
  --mantine-color-body: #333;
}


*/
```


### Default colors


```python
import dash_mantine_components as dmc

colors = dmc.DEFAULT_THEME["colors"]

component= dmc.SimpleGrid([
    dmc.Card([
        dmc.Box(h=100, w=100, bg=f"{c}.{i}" ),
        dmc.Text(f"{c} {i}", size="sm"),
        dmc.Text(f"{colors[c][i]}", size="sm", c="dimmed")
    ])  for c in list(colors) for i in range(10)
], cols={ "base": 5,  "lg": 10 }, spacing="xs")
```
### Default colors: CSS Variables list

For a list of all Mantine CSS variables that are generated from default theme, see the [CSS Variables](/css-variables/) section.

---


> Dash Mantine Components v2.4.0 Documentation for Typography
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Typography
How to set fonts, size and line height in the app theme
Category: Theming

### Change fonts

You can change fonts and other text styles for headings, code and all other components with the following theme properties:

- `theme.fontFamily` – controls font-family in all components except `Title`, `Code` and `Kbd`
- `theme.fontFamilyMonospace` – controls font-family of components that require monospace font: `Code`, `Kbd` and `CodeHighlight`
- `theme.headings.fontFamily` – controls font-family of h1-h6 tags in `Title`, fallbacks to `theme.fontFamily` if not defined

In this example, you can toggle between the default fonts and custom fonts specified in the `theme`.

```python
import dash_mantine_components as dmc
from dash import Dash, Input, Output


app = Dash()

component = dmc.Box([
    dmc.SegmentedControl(id="segment", data=["default", "custom-fonts"], value="default"),
    dmc.Box([
        dmc.Title("Greycliff CF title", order=3),
        dmc.Button("Verdana button"),
        dmc.Code("Monaco, Courier Code")
    ], bd=True, m="lg")
], m="lg")

theme= {
  "fontFamily": 'Verdana',
  "fontFamilyMonospace": 'Monaco, Courier, monospace',
  "headings": { "fontFamily": 'Greycliff CF' },
}

app.layout = dmc.MantineProvider(
    component,
    id="provider",
)

@app.callback(
    Output("provider", "theme"),
    Input("segment", "value")
)
def update_font_theme(val):
    if val == "default":
        return {}
    return theme


if __name__ == "__main__":
    app.run(debug=True)
```

### System fonts
By default, Mantine uses system fonts. It means that different devices will display components based on available font,
for example, macOS and iOS users will see San Francisco font, Windows users will see Segoe UI font, Android users will
see Roboto font and so on. This approach provides a familiar experience to the users and allows avoiding common problems
related to custom fonts loading (layout shift, invisible text, etc.), if you do not have strict requirements, it is
recommended to use system fonts for better performance.

Default values for theme properties:

- Default value for `theme.fontFamily` and `theme.headings.fontFamily` is `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji`
- Default value for `theme.fontFamilyMonospace` is `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, Courier New, monospace`


### Font Sizes

Default `theme.fontSizes` Values

| Key | Value      | Value in px |
|-----|------------|-------------|
| xs  | 0.75rem    | 12px        |
| sm  | 0.875rem   | 14px        |
| md  | 1rem       | 16px        |
| lg  | 1.125rem   | 18px        |
| xl  | 1.25rem    | 20px        |

You can customize the `fontSizes` defaults in the `theme`:
```python
theme = {
    "fontSizes" : {
        "xs": "0.75rem",            # customize font sizes here
        "sm": "0.875rem",
        "md": "1rem",
        "lg": "1.125rem",
        "xl": "1.25rem",
    }
}

dmc.MantineProvider(
    # your layout,
    theme=theme
)
```

### Line Heights

`theme.lineHeights` property defines line-height values for `Text` component, most other components use
`theme.lineHeights.md` by default:

 Default `theme.lineHeights` Values


| Key | Value  |
|-----|--------|
| xs  | 1.4    |
| sm  | 1.45   |
| md  | 1.55   |
| lg  | 1.6    |
| xl  | 1.65   |

You can customize the `lineHeights` defaults in the `theme`:

```python
theme = {
    "lineHeights" : {
        "xs": "1.4",            # customize line heights here
        "sm": "1.45",
        "md": "1.55",
        "lg": "1.6",
        "xl": "1.65",
    }
}

dmc.MantineProvider(
    # your layout,
    theme=theme
)

```

### h1-h6 styles
To customize headings styles in `Title` components set `theme.headings`:

```python
import dash_mantine_components as dmc

theme = {
    "headings": {
        # Properties for all headings
        "fontWeight": "400",
        "fontFamily": "Roboto",
        # Properties for individual headings
        "sizes": {
            "h1": {
                "fontWeight": "100",
                "fontSize": "36px",
                "lineHeight": "1.4",
            },
            "h2": {
                "fontSize": "30px",
                "lineHeight": "1.5",
            },
            # Additional heading levels
            "h6": {
                "fontWeight": "900",
            },
        },
    },
}

dmc.MantineProvider(
    # your app layout here,
    theme=theme,
)
```

With `theme.headings` you can customize `font-size`, `font-weight` and `line-height` per heading level. If you need
more control over styles, use `:is` selector with [Styles API](/styles-api) to target specific heading level:

You can find a complete minimal example in the [Help Center](https://github.com/snehilvj/dmc-docs/blob/main/help_center/theme/change_headings.py)

```python

theme = {
    "components": {
        "Title": {
            "classNames": {
                "root": "change-heading-demo",
            },
        },
    },
}

dmc.MantineProvider(
    theme=theme,
    children=[
        dmc.Title("Heading 1", order=1),
        dmc.Title("Heading 2", order=2),
        dmc.Title("Heading 3", order=3),
        dmc.Title("Heading 4", order=4),
        dmc.Title("Heading 5", order=5),
        dmc.Title("Heading 6", order=6),
    ],
)
```

In a `.css` file in `/assets` folder add:

```css

.change-heading-demo {
  &:is(h1) {
    font-family: GreycliffCF, sans-serif;
    font-weight: 900;
  }

  &:is(h5, h6) {
    color: var(--mantine-color-dimmed);
  }
}

```
