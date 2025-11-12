
> Dash Mantine Components v2.4.0 Documentation for Layout Overview
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Layout Overview
This guide gives an overview of layout components available in Dash Mantine components.
Category: Layout

### SimpleGrid
Use [SimpleGrid](/components/simplegrid) if you need columns with equal size. The `cols`, `spacing` and `verticalSpacing` props accepts dictionaries to set responsive values based on viewport width.


### Grid
Use [Grid](/components/grid) if you need columns with different sizes.   You can also set spans, spacing, offsets, and ordering and more.


### Group
Use [Group](/components/group) if you want to put items next to each other horizontally.

### Stack
Use [Stack](/components/stack) if you want to put items next to each other vertically


### Flex
Use [Flex](/components/flex) if you want to create both horizontal and vertical flexbox layouts. It's more flexible than `Group` and `Stack` but requires more configuration.


### AspectRatio
Use [AspectRatio](/components/aspectratio) to ensure that content always maintains a specific width-to-height ratio,
no matter the screen size.  Great for images and videos.


### Center
Use [Center](/compnents/center) component to center content vertically and horizontally.
This example centers an icon with a link with the `inline` prop:


### Container
Use [Container](/components/container) to center content horizontally and add horizontal padding from theme. Good for limiting width and centering content on large screens.


###  Box
[Box](/components/box) is like an `html.Div` but also includes Mantine style props.


### Paper

Use [Paper](/components/paper) to group content visually like a card.  It includes props for background, padding, shadow, borders, and rounded corners.


### AppShell

The [AppShell](/components/appshell) component is a layout component designed to create responsive and consistent app layouts.
It includes:
- `AppShell` - root component, it is required to wrap all other components, used to configure layout properties
- `AppShellHeader` - section rendered at the top of the page
- `AppShellNavbar` - section rendered on the left side of the page
- `AppShellAside` - section rendered on the right side of the page
- `AppShellFooter` - section rendered at the bottom of the page
- `AppShellMain` - main section rendered at the center of the page, has static position, all other sections are offset by its padding
- `AppShellSection` - utility component that can be used to render group of content inside `AppShellNavbar` and `AppShellAside`

This DMC documentation app is built using `AppShell` components.

See the [AppShell](/components/appshell) docs for more info and examples:

---


> Dash Mantine Components v2.4.0 Documentation for AppShell
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## AppShell
Responsive shell for your application with header, navbar, aside and footer.
Category: Layout

### Examples

Since `AppShell` components have fixed position, it is not possible to include live demos on this page.


Please see the code in the [dmc-docs GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell).  Or run the app and edit the code on **[PyCafe](https://py.cafe/dash.mantine.components)**.


1. Basic AppShell with Header and Navbar
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/basic_appshell.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/basic-appshell-collapsible-navbar)

```python
"""
Basic Appshell with header and  navbar that collapses on mobile.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

2. Responsive Width and Height
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/responsive_sizes.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/appshell-responsive-width-height)

```python
"""
Responsive width and height

App shell with responsive navbar width and height
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={
        "height": {"base": 60, "md": 70, "lg": 80},
    },
    navbar={
        "width": {"base": 200, "md": 300, "lg": 400},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

3. Mobile-Only Navbar
   - Buttons in the header are displayed in the navbar on mobile.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/mobile_navbar.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/responsive-mobile-navbar-demo)

```python
"""
Mobile only navbar

Navbar is only visible on mobile, links that are rendered in the header
on desktop are hidden on mobile in header and rendered in navbar instead.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"
buttons = [
    dmc.Button("Home", variant="subtle", color="gray"),
    dmc.Button("Blog", variant="subtle", color="gray"),
    dmc.Button("Contacts", variant="subtle", color="gray"),
    dmc.Button("Support", variant="subtle", color="gray"),
]

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Burger(
                                id="burger",
                                size="sm",
                                hiddenFrom="sm",
                                opened=False,
                            ),
                            dmc.Image(src=logo, h=40, flex=0),
                            dmc.Title("Demo App", c="blue"),
                        ]
                    ),
                    dmc.Group(
                        children=buttons,
                        ml="xl",
                        gap=0,
                        visibleFrom="sm",
                    ),
                ],
                justify="space-between",
                style={"flex": 1},
                h="100%",
                px="md",
            ),
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=buttons,
            py="md",
            px=4,
        ),
        dmc.AppShellMain(
            "Navbar is only visible on mobile, links that are rendered in the header on desktop are hidden on mobile in header and rendered in navbar instead."
        ),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"desktop": True, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened, "desktop": True}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

4. Collapsible Navbar on Desktop and Mobile
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/responsive_sizes.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/Collapsible-navbar-on-both-desktop-and-moble)

```python
"""
Responsive width and height

App shell with responsive navbar width and height
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={
        "height": {"base": 60, "md": 70, "lg": 80},
    },
    navbar={
        "width": {"base": 200, "md": 300, "lg": 400},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

5. Full AppShell Layout
   - Includes all elements: navbar, header, aside, and footer.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/full_layout.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/AppShell-with-all-elements)

```python
"""
AppShell with all elements

Navbar, header, aside and footer used together
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain(
            "Aside is hidden on md breakpoint and cannot be opened when it is collapsed"
        ),
        dmc.AppShellAside("Aside", p="md"),
        dmc.AppShellFooter("Footer", p="md"),
    ],
    header={"height": 60},
    footer={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "md",
        "collapsed": {"desktop": False, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

6. Scrollable Navbar with 60 Links
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/navbar_scroll.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/Appshell-with-scrollable-navbar)

```python
"""
Scrollable Navbar with 60 links
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback


app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=dmc.ScrollArea(
                [
                    "60 links in a scrollable section",
                    *[
                        dmc.Skeleton(height=28, mt="sm", animate=False)
                        for _ in range(60)
                    ],
                ]
            ),
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

7. Alternate AppShell Layout
   - Navbar and aside are rendered on top of the header and footer.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/alt_layout.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/dash-alt-layout-appshell)

```python
"""
Alt Layout
Navbar and Aside are rendered on top on Header and Footer

"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            p="md",
            children=[
                dmc.Group(
                    [
                        dmc.Burger(
                            id="navbar-burger", size="sm", hiddenFrom="sm", opened=False
                        ),
                        dmc.Text("Navbar"),
                    ]
                ),
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
        ),
        dmc.AppShellMain(
            "Alt layout – Navbar and Aside are rendered on top of Header and Footer"
        ),
        dmc.AppShellAside("Aside", p="md"),
        dmc.AppShellFooter("Footer", p="md"),
    ],
    layout="alt",
    header={"height": 60},
    footer={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "md",
        "collapsed": {"desktop": False, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

8. AppShell with Theme Switch Component
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/appshell_with_theme_switch.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/dash-mantine-theme-toggle-app)

```python
"""
Basic Appshell with header and  navbar that collapses on mobile.  Also includes a theme switch.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, Input, Output, State, callback, clientside_callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Burger(
                                id="burger",
                                size="sm",
                                hiddenFrom="sm",
                                opened=False,
                            ),
                            dmc.Image(src=logo, h=40, flex=0),
                            dmc.Title("Demo App", c="blue"),
                        ]
                    ),
                    theme_toggle,
                ],
                justify="space-between",
                style={"flex": 1},
                h="100%",
                px="md",
            ),
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)

if __name__ == "__main__":
    app.run(debug=True)
```

### Basic usage

AppShell is a layout component. It can be used to implement a common Header - Navbar - Footer - Aside layout pattern.
All AppShell components have `position: fixed` style - they are not scrolled with the page.

The documentation app that you are viewing uses AppShell with Header, Aside, and Navbar.

This is the code for the first example above for the basic app shell with header and navbar.  The navbar collapses on mobile.

```python

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)

```

### AppShell components

* `AppShell` - root component, it is required to wrap all other components, used to configure layout properties
* `AppShellHeader` - section rendered at the top of the page
* `AppShellNavbar` - section rendered on the left side of the page
* `AppShellAside` - section rendered on the right side of the page
* `AppShellFooter` - section rendered at the bottom of the page
* `AppShellMain` - main section rendered at the center of the page, has static position, all other sections are offset by its padding
* `AppShellSection` - utility component that can be used to render group of content inside `AppShellNavbar` and `AppShellAside`

### AppShell Configuration
`AppShell` component accepts, `header`, `footer`, `navbar` and `aside` props to configure corresponding sections. It is
required to set these props if you want to use corresponding components. For example, if you want to use `AppShellHeader`
component, you need to set `header` prop on the `AppShell` component.

### header and footer properties

`header` and `footer` configuration dictionaries are the same and have the following properties:

- `height`: Height of the section: number, string or dict  with breakpoints as keys and height as value
- `collapsed`: boolean; If section is collapsed it is hidden from the viewport and is not offset in `AppShellMain`
- `offset`: boolean; Determines whether the section should be offset by the `AppShellMain`. For example, it is useful if you want to hide header based on the scroll position.

### navbar and aside properties

`navbar` and `aside` configuration dictionaries are the same as well and have the following properties:

- `width`: Width of the section: number, string or dict with breakpoints as keys and width as value
- `breakpoint`: Breakpoint at which section should switch to mobile mode. In mobile mode the section always has
100% width and its collapsed state is controlled by the `collapsed.mobile` instead of `collapsed.desktop`
- `collapsed`: Determines whether the section should be collapsed.  Example:  {"desktop": False; "mobile": True };

### layout prop
`layout` prop controls how `AppShellHeader` / `AppShellFooter` and `AppShellNavbar` / `AppShellAside` are positioned
relative to each other. It accepts `alt` and `default` values:

- `alt` – `AppShellNavbar`/`AppShellAside` height is equal to viewport height, `AppShellHeader`/`AppShellFooter` width
is equal to viewport width less the `AppShellNavbar` and `AppShellAside` width.  See example #7 above.

- `default` – `AppShellNavbar`/`AppShellAside` height is equal to viewport height - `AppShellHeader`/ `AppShellFooter`
height, `AppShellHeader`/`AppShellFooter` width is equal to viewport width

### height prop
`height` property in `header` and `footer` configuration dicts works the following way:

- If you pass a number, the value will be converted to rem and used as height at all viewport sizes.
- To change height based on viewport width, use dict with breakpoints as keys and height as values. It works the same way as `style` props.

Examples:
```python
# Height is a number, it will be converted to rem  and used as height at all viewport sizes
dmc.AppShell(
    children=[
        dmc.AppShellHeader("Header")
        # ...
     ],
    header={"height": 48}
)
```

```python

# Height is an dict with breakpoints:
# - height is 48 when viewport width is < theme.breakpoints.sm
# - height is 60 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - height is 76 when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
    children=[
       dmc.AppShellHeader("Header")
    ],
    header={"height": {"base": 48, "sm": 60, "lg": 76}}
)
```

### Width configuration
`width` property in `navbar` and `aside`  configuration dictionaries works the following way:

- If you pass a number, the value will be converted to rem and used as width when the viewport is larger than breakpoint.
- To change `width` based on viewport width, use dict with breakpoints as keys and width as values. It works the same way as `style` props. Note that width is always 100% when the viewport is smaller than breakpoint.

Examples

```python
# Width is a number, it will be converted to rem and used as width when viewport is larger than theme.breakpoints.sm
dmc.AppShell(
    children=[
        dmc.AppShellNavbar("Navbar")
        # ...
     ],
    navbar={"width": 48, "breakpoint": "sm"}
)
```

```python

# Width is an object with breakpoints:
# - width is 100% when viewport width is < theme.breakpoints.sm
# - width is 200 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - width is 300 when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
    children=[
        dmc.AppShellNavbar("Navbar")
        # ...
     ],
    navbar={"width": {"sm": 200, "lg": 300 }, "breakpoint": 'sm' }
)
```

### padding prop
`padding` prop controls the padding of the `AppShellMain` component. It is important to use it instead of setting padding
on the `AppShellMain` directly because padding of the `AppShellMain` is also used to offset `AppShellHeader`, `AppShellNavbar`, `AppShellAside` and `AppShellFooter` components.

`padding` prop works the same way as `style` props and accepts numbers, strings and dicts with breakpoints as keys and padding as values. You can reference theme.spacing values or use any valid CSS values.

```python
# Padding is always theme.spacing.md
dmc.AppShell(
   # content
   padding="md"
)
```


```python

# Padding is:
# - 10 when viewport width is < theme.breakpoints.sm
# - 15 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - theme.spacing.xl when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
   # content
   padding={"base": 10, "sm": 15, "lg": "xl" }
)
```
### Collapsed navbar/aside configuration
`navbar` and `aside` props have `collapsed` property. The property accepts an dict { mobile: boolean; desktop: boolean } which
allows to configure collapsed state depending on the viewport width.

See example #4 above: Collapsible Navbar on Desktop and Mobile

### withBorder prop
`withBorder` prop is available on `AppShell` and associated sections: `AppShellHeader`, `AppShellNavbar`, `AppShellAside`
and `AppShellFooter`. By default, `withBorder` prop is True – all components have a border on the side that is adjacent
to the `AppShellMain` component. For example, `AppShellHeader` is located at the top of the page – it has a border on the
bottom side, `AppShellNavbar` is located on the left side of the page – it has a border on the right side.

To remove the border from all components, set `withBorder=False` on the `AppShell`:

```python
dmc.AppShell(withBorder=False)
```

To remove the border from a specific component, set `withBorder=False` on that component:

```python
dmc.AppShell(
   children=[
      dmc.AppShellHeader(withBorder=False)
   ]
)
```



### zIndex prop

`zIndex` prop is available on AppShell and associated sections: `AppShellHeader`, `AppShellNavbar`, `AppShellAside` and `AppShellFooter`.

By default, all sections z-index is 200.

To change z-index of all sections, set `zIndex` prop on the AppShell:

```python
import dash_mantine_components as dmc

dmc.AppShell(
    zIndex=100,
    children=[
        # content
    ]
)
```

To change z-index of individual sections, set `zIndex` prop on each of them:

```python
import dash_mantine_components as dmc

dmc.AppShell(
    children=[
        dmc.AppShellHeader("Header", zIndex=2000),
        dmc.AppShellNavbar("Navbar", zIndex=2000),
    ]
)
```

### Control transitions
Set `transitionDuration` and `transitionTimingFunction` props on the `AppShell` to control transitions:

```python
dmc.AppShell(
   transitionDuration=500,
   transitionTimingFunction="ease"   ,
)
```

### disabled prop
Set `disabled` prop on the `AppShell` to prevent all sections except `AppShellMain` from rendering. It is useful when
you want to hide the shell on some pages of your application.

```python
dmc.AppShell(disabled=True)
```


### Usage in docs

```python
import dash_mantine_components as dmc

dmc.AppShell(
    [
        dmc.AppShellHeader("Header", px=25),
        dmc.AppShellNavbar("Navbar"),
        dmc.AppShellAside("Aside", withBorder=False),
        dmc.AppShellMain(children=[...]),
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "xl",
        "collapsed": {"desktop": False, "mobile": True},
    },
)
```


### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### AppShell Selectors

| Selector | Static selector            | Description                       |
|----------|-----------------------------|-----------------------------------|
| root     | .mantine-AppShell-root      | Root element (AppShell component) |
| navbar   | .mantine-AppShell-navbar    | AppShell.Navbar root element      |
| header   | .mantine-AppShell-header    | AppShell.Header root element      |
| main     | .mantine-AppShell-main      | AppShell.Main root element        |
| aside    | .mantine-AppShell-aside     | AppShell.Aside root element       |
| footer   | .mantine-AppShell-footer    | AppShell.Footer root element      |
| section  | .mantine-AppShell-section   | AppShell.Section root element     |

#### AppShell CSS Variables

| Selector | Variable                                 | Description                                   |
|----------|------------------------------------------|-----------------------------------------------|
| root     | --app-shell-transition-duration          | Controls transition duration of all children  |
|          | --app-shell-transition-timing-function   | Controls transition timing function of all children |

#### AppShell Data Attributes

| Selector         | Attribute         | Condition                    | Value                                |
|------------------|-------------------|------------------------------|--------------------------------------|
| root             | data-resizing     | User is resizing the window  | –                                    |
| root             | data-layout       | –                            | Value of the `layout` prop           |
| root             | data-disabled     | `disabled` prop is set       | –                                    |
| navbar, header, aside, footer | data-with-border | `withBorder` prop is set either on the AppShell or on the associated component | – |
| section          | data-grow         | `grow` prop is set on the AppShell.Section | – |


### Keyword Arguments
### AppShell
- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- aside (dict; optional):
    AppShell.Aside configuration, controls width, breakpoints and
    collapsed state. Required if you use AppShell.Aside component.

    `aside` is a dict with keys:

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- disabled (boolean; optional):
    If set, Navbar, Aside, Header and Footer components be hidden.

- footer (dict; optional):
    AppShell.Footer configuration, controls height, offset and
    collapsed state. Required if you use AppShell.Footer component.

    `footer` is a dict with keys:

- header (dict; optional):
    AppShell.Header configuration, controls height, offset and
    collapsed state. Required if you use AppShell.Header component.

    `header` is a dict with keys:

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- layout (a value equal to: 'default', 'alt'; optional):
    Determines how Navbar/Aside are arranged relative to
    Header/Footer, `default` by default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- navbar (dict; optional):
    AppShell.Navbar configuration, controls width, breakpoints and
    collapsed state. Required if you use AppShell.Navbar component.

    `navbar` is a dict with keys:

- offsetScrollbars (boolean; optional):
    Determines whether Header and Footer components should include
    styles to offset scrollbars. Based on `react-remove-scroll`.
    `True` by default.

- padding (number; optional):
    Controls padding of the main section, `0` by default. !important!:
    use `padding` prop instead of `p`.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- transitionDuration (number; optional):
    Duration of all transitions in ms, `200` by default.

- transitionTimingFunction (optional):
    Timing function of all transitions, `ease` by default.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether associated components should have a border,
    `True` by default.

- zIndex (string | number; optional):
    `z-index` of all associated elements, `200` by default.
#### Navbar

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Header

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Aside

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Footer

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Section

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- grow (boolean; optional):
    Determines whether the section should take all available space,
    `False` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

---

> Dash Mantine Components v2.4.0 Documentation for AppShell
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## AppShell
Responsive shell for your application with header, navbar, aside and footer.
Category: Layout

### Examples

Since `AppShell` components have fixed position, it is not possible to include live demos on this page.


Please see the code in the [dmc-docs GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell).  Or run the app and edit the code on **[PyCafe](https://py.cafe/dash.mantine.components)**.


1. Basic AppShell with Header and Navbar
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/basic_appshell.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/basic-appshell-collapsible-navbar)

```python
"""
Basic Appshell with header and  navbar that collapses on mobile.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

2. Responsive Width and Height
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/responsive_sizes.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/appshell-responsive-width-height)

```python
"""
Responsive width and height

App shell with responsive navbar width and height
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={
        "height": {"base": 60, "md": 70, "lg": 80},
    },
    navbar={
        "width": {"base": 200, "md": 300, "lg": 400},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

3. Mobile-Only Navbar
   - Buttons in the header are displayed in the navbar on mobile.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/mobile_navbar.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/responsive-mobile-navbar-demo)

```python
"""
Mobile only navbar

Navbar is only visible on mobile, links that are rendered in the header
on desktop are hidden on mobile in header and rendered in navbar instead.
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"
buttons = [
    dmc.Button("Home", variant="subtle", color="gray"),
    dmc.Button("Blog", variant="subtle", color="gray"),
    dmc.Button("Contacts", variant="subtle", color="gray"),
    dmc.Button("Support", variant="subtle", color="gray"),
]

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Burger(
                                id="burger",
                                size="sm",
                                hiddenFrom="sm",
                                opened=False,
                            ),
                            dmc.Image(src=logo, h=40, flex=0),
                            dmc.Title("Demo App", c="blue"),
                        ]
                    ),
                    dmc.Group(
                        children=buttons,
                        ml="xl",
                        gap=0,
                        visibleFrom="sm",
                    ),
                ],
                justify="space-between",
                style={"flex": 1},
                h="100%",
                px="md",
            ),
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=buttons,
            py="md",
            px=4,
        ),
        dmc.AppShellMain(
            "Navbar is only visible on mobile, links that are rendered in the header on desktop are hidden on mobile in header and rendered in navbar instead."
        ),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"desktop": True, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened, "desktop": True}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

4. Collapsible Navbar on Desktop and Mobile
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/responsive_sizes.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/Collapsible-navbar-on-both-desktop-and-moble)

```python
"""
Responsive width and height

App shell with responsive navbar width and height
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={
        "height": {"base": 60, "md": 70, "lg": 80},
    },
    navbar={
        "width": {"base": 200, "md": 300, "lg": 400},
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

5. Full AppShell Layout
   - Includes all elements: navbar, header, aside, and footer.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/full_layout.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/AppShell-with-all-elements)

```python
"""
AppShell with all elements

Navbar, header, aside and footer used together
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id="burger",
                        size="sm",
                        hiddenFrom="sm",
                        opened=False,
                    ),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain(
            "Aside is hidden on md breakpoint and cannot be opened when it is collapsed"
        ),
        dmc.AppShellAside("Aside", p="md"),
        dmc.AppShellFooter("Footer", p="md"),
    ],
    header={"height": 60},
    footer={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "md",
        "collapsed": {"desktop": False, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

6. Scrollable Navbar with 60 Links
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/navbar_scroll.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/Appshell-with-scrollable-navbar)

```python
"""
Scrollable Navbar with 60 links
"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback


app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=dmc.ScrollArea(
                [
                    "60 links in a scrollable section",
                    *[
                        dmc.Skeleton(height=28, mt="sm", animate=False)
                        for _ in range(60)
                    ],
                ]
            ),
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

7. Alternate AppShell Layout
   - Navbar and aside are rendered on top of the header and footer.
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/alt_layout.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/dash-alt-layout-appshell)

```python
"""
Alt Layout
Navbar and Aside are rendered on top on Header and Footer

"""

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40, flex=0),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            p="md",
            children=[
                dmc.Group(
                    [
                        dmc.Burger(
                            id="navbar-burger", size="sm", hiddenFrom="sm", opened=False
                        ),
                        dmc.Text("Navbar"),
                    ]
                ),
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
        ),
        dmc.AppShellMain(
            "Alt layout – Navbar and Aside are rendered on top of Header and Footer"
        ),
        dmc.AppShellAside("Aside", p="md"),
        dmc.AppShellFooter("Footer", p="md"),
    ],
    layout="alt",
    header={"height": 60},
    footer={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "md",
        "collapsed": {"desktop": False, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)
```

8. AppShell with Theme Switch Component
   - [View Code on GitHub](https://github.com/snehilvj/dmc-docs/tree/main/help_center/appshell/appshell_with_theme_switch.py)
   - [Live Demo on PyCafe](https://py.cafe/dash.mantine.components/dash-mantine-theme-toggle-app)

```python
"""
Basic Appshell with header and  navbar that collapses on mobile.  Also includes a theme switch.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, Input, Output, State, callback, clientside_callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Burger(
                                id="burger",
                                size="sm",
                                hiddenFrom="sm",
                                opened=False,
                            ),
                            dmc.Image(src=logo, h=40, flex=0),
                            dmc.Title("Demo App", c="blue"),
                        ]
                    ),
                    theme_toggle,
                ],
                justify="space-between",
                style={"flex": 1},
                h="100%",
                px="md",
            ),
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)

if __name__ == "__main__":
    app.run(debug=True)
```

### Basic usage

AppShell is a layout component. It can be used to implement a common Header - Navbar - Footer - Aside layout pattern.
All AppShell components have `position: fixed` style - they are not scrolled with the page.

The documentation app that you are viewing uses AppShell with Header, Aside, and Navbar.

This is the code for the first example above for the basic app shell with header and navbar.  The navbar collapses on mobile.

```python

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback

app = Dash()

logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Image(src=logo, h=40),
                    dmc.Title("Demo App", c="blue"),
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                "Navbar",
                *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
            ],
            p="md",
        ),
        dmc.AppShellMain("Main"),
    ],
    header={"height": 60},
    padding="md",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)


app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


if __name__ == "__main__":
    app.run(debug=True)

```

### AppShell components

* `AppShell` - root component, it is required to wrap all other components, used to configure layout properties
* `AppShellHeader` - section rendered at the top of the page
* `AppShellNavbar` - section rendered on the left side of the page
* `AppShellAside` - section rendered on the right side of the page
* `AppShellFooter` - section rendered at the bottom of the page
* `AppShellMain` - main section rendered at the center of the page, has static position, all other sections are offset by its padding
* `AppShellSection` - utility component that can be used to render group of content inside `AppShellNavbar` and `AppShellAside`

### AppShell Configuration
`AppShell` component accepts, `header`, `footer`, `navbar` and `aside` props to configure corresponding sections. It is
required to set these props if you want to use corresponding components. For example, if you want to use `AppShellHeader`
component, you need to set `header` prop on the `AppShell` component.

### header and footer properties

`header` and `footer` configuration dictionaries are the same and have the following properties:

- `height`: Height of the section: number, string or dict  with breakpoints as keys and height as value
- `collapsed`: boolean; If section is collapsed it is hidden from the viewport and is not offset in `AppShellMain`
- `offset`: boolean; Determines whether the section should be offset by the `AppShellMain`. For example, it is useful if you want to hide header based on the scroll position.

### navbar and aside properties

`navbar` and `aside` configuration dictionaries are the same as well and have the following properties:

- `width`: Width of the section: number, string or dict with breakpoints as keys and width as value
- `breakpoint`: Breakpoint at which section should switch to mobile mode. In mobile mode the section always has
100% width and its collapsed state is controlled by the `collapsed.mobile` instead of `collapsed.desktop`
- `collapsed`: Determines whether the section should be collapsed.  Example:  {"desktop": False; "mobile": True };

### layout prop
`layout` prop controls how `AppShellHeader` / `AppShellFooter` and `AppShellNavbar` / `AppShellAside` are positioned
relative to each other. It accepts `alt` and `default` values:

- `alt` – `AppShellNavbar`/`AppShellAside` height is equal to viewport height, `AppShellHeader`/`AppShellFooter` width
is equal to viewport width less the `AppShellNavbar` and `AppShellAside` width.  See example #7 above.

- `default` – `AppShellNavbar`/`AppShellAside` height is equal to viewport height - `AppShellHeader`/ `AppShellFooter`
height, `AppShellHeader`/`AppShellFooter` width is equal to viewport width

### height prop
`height` property in `header` and `footer` configuration dicts works the following way:

- If you pass a number, the value will be converted to rem and used as height at all viewport sizes.
- To change height based on viewport width, use dict with breakpoints as keys and height as values. It works the same way as `style` props.

Examples:
```python
# Height is a number, it will be converted to rem  and used as height at all viewport sizes
dmc.AppShell(
    children=[
        dmc.AppShellHeader("Header")
        # ...
     ],
    header={"height": 48}
)
```

```python

# Height is an dict with breakpoints:
# - height is 48 when viewport width is < theme.breakpoints.sm
# - height is 60 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - height is 76 when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
    children=[
       dmc.AppShellHeader("Header")
    ],
    header={"height": {"base": 48, "sm": 60, "lg": 76}}
)
```

### Width configuration
`width` property in `navbar` and `aside`  configuration dictionaries works the following way:

- If you pass a number, the value will be converted to rem and used as width when the viewport is larger than breakpoint.
- To change `width` based on viewport width, use dict with breakpoints as keys and width as values. It works the same way as `style` props. Note that width is always 100% when the viewport is smaller than breakpoint.

Examples

```python
# Width is a number, it will be converted to rem and used as width when viewport is larger than theme.breakpoints.sm
dmc.AppShell(
    children=[
        dmc.AppShellNavbar("Navbar")
        # ...
     ],
    navbar={"width": 48, "breakpoint": "sm"}
)
```

```python

# Width is an object with breakpoints:
# - width is 100% when viewport width is < theme.breakpoints.sm
# - width is 200 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - width is 300 when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
    children=[
        dmc.AppShellNavbar("Navbar")
        # ...
     ],
    navbar={"width": {"sm": 200, "lg": 300 }, "breakpoint": 'sm' }
)
```

### padding prop
`padding` prop controls the padding of the `AppShellMain` component. It is important to use it instead of setting padding
on the `AppShellMain` directly because padding of the `AppShellMain` is also used to offset `AppShellHeader`, `AppShellNavbar`, `AppShellAside` and `AppShellFooter` components.

`padding` prop works the same way as `style` props and accepts numbers, strings and dicts with breakpoints as keys and padding as values. You can reference theme.spacing values or use any valid CSS values.

```python
# Padding is always theme.spacing.md
dmc.AppShell(
   # content
   padding="md"
)
```


```python

# Padding is:
# - 10 when viewport width is < theme.breakpoints.sm
# - 15 when viewport width is >= theme.breakpoints.sm and < theme.breakpoints.lg
# - theme.spacing.xl when viewport width is >= theme.breakpoints.lg
dmc.AppShell(
   # content
   padding={"base": 10, "sm": 15, "lg": "xl" }
)
```
### Collapsed navbar/aside configuration
`navbar` and `aside` props have `collapsed` property. The property accepts an dict { mobile: boolean; desktop: boolean } which
allows to configure collapsed state depending on the viewport width.

See example #4 above: Collapsible Navbar on Desktop and Mobile

### withBorder prop
`withBorder` prop is available on `AppShell` and associated sections: `AppShellHeader`, `AppShellNavbar`, `AppShellAside`
and `AppShellFooter`. By default, `withBorder` prop is True – all components have a border on the side that is adjacent
to the `AppShellMain` component. For example, `AppShellHeader` is located at the top of the page – it has a border on the
bottom side, `AppShellNavbar` is located on the left side of the page – it has a border on the right side.

To remove the border from all components, set `withBorder=False` on the `AppShell`:

```python
dmc.AppShell(withBorder=False)
```

To remove the border from a specific component, set `withBorder=False` on that component:

```python
dmc.AppShell(
   children=[
      dmc.AppShellHeader(withBorder=False)
   ]
)
```



### zIndex prop

`zIndex` prop is available on AppShell and associated sections: `AppShellHeader`, `AppShellNavbar`, `AppShellAside` and `AppShellFooter`.

By default, all sections z-index is 200.

To change z-index of all sections, set `zIndex` prop on the AppShell:

```python
import dash_mantine_components as dmc

dmc.AppShell(
    zIndex=100,
    children=[
        # content
    ]
)
```

To change z-index of individual sections, set `zIndex` prop on each of them:

```python
import dash_mantine_components as dmc

dmc.AppShell(
    children=[
        dmc.AppShellHeader("Header", zIndex=2000),
        dmc.AppShellNavbar("Navbar", zIndex=2000),
    ]
)
```

### Control transitions
Set `transitionDuration` and `transitionTimingFunction` props on the `AppShell` to control transitions:

```python
dmc.AppShell(
   transitionDuration=500,
   transitionTimingFunction="ease"   ,
)
```

### disabled prop
Set `disabled` prop on the `AppShell` to prevent all sections except `AppShellMain` from rendering. It is useful when
you want to hide the shell on some pages of your application.

```python
dmc.AppShell(disabled=True)
```


### Usage in docs

```python
import dash_mantine_components as dmc

dmc.AppShell(
    [
        dmc.AppShellHeader("Header", px=25),
        dmc.AppShellNavbar("Navbar"),
        dmc.AppShellAside("Aside", withBorder=False),
        dmc.AppShellMain(children=[...]),
    ],
    header={"height": 70},
    padding="xl",
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    aside={
        "width": 300,
        "breakpoint": "xl",
        "collapsed": {"desktop": False, "mobile": True},
    },
)
```


### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### AppShell Selectors

| Selector | Static selector            | Description                       |
|----------|-----------------------------|-----------------------------------|
| root     | .mantine-AppShell-root      | Root element (AppShell component) |
| navbar   | .mantine-AppShell-navbar    | AppShell.Navbar root element      |
| header   | .mantine-AppShell-header    | AppShell.Header root element      |
| main     | .mantine-AppShell-main      | AppShell.Main root element        |
| aside    | .mantine-AppShell-aside     | AppShell.Aside root element       |
| footer   | .mantine-AppShell-footer    | AppShell.Footer root element      |
| section  | .mantine-AppShell-section   | AppShell.Section root element     |

#### AppShell CSS Variables

| Selector | Variable                                 | Description                                   |
|----------|------------------------------------------|-----------------------------------------------|
| root     | --app-shell-transition-duration          | Controls transition duration of all children  |
|          | --app-shell-transition-timing-function   | Controls transition timing function of all children |

#### AppShell Data Attributes

| Selector         | Attribute         | Condition                    | Value                                |
|------------------|-------------------|------------------------------|--------------------------------------|
| root             | data-resizing     | User is resizing the window  | –                                    |
| root             | data-layout       | –                            | Value of the `layout` prop           |
| root             | data-disabled     | `disabled` prop is set       | –                                    |
| navbar, header, aside, footer | data-with-border | `withBorder` prop is set either on the AppShell or on the associated component | – |
| section          | data-grow         | `grow` prop is set on the AppShell.Section | – |


### Keyword Arguments
### AppShell
- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- aside (dict; optional):
    AppShell.Aside configuration, controls width, breakpoints and
    collapsed state. Required if you use AppShell.Aside component.

    `aside` is a dict with keys:

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- disabled (boolean; optional):
    If set, Navbar, Aside, Header and Footer components be hidden.

- footer (dict; optional):
    AppShell.Footer configuration, controls height, offset and
    collapsed state. Required if you use AppShell.Footer component.

    `footer` is a dict with keys:

- header (dict; optional):
    AppShell.Header configuration, controls height, offset and
    collapsed state. Required if you use AppShell.Header component.

    `header` is a dict with keys:

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- layout (a value equal to: 'default', 'alt'; optional):
    Determines how Navbar/Aside are arranged relative to
    Header/Footer, `default` by default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- navbar (dict; optional):
    AppShell.Navbar configuration, controls width, breakpoints and
    collapsed state. Required if you use AppShell.Navbar component.

    `navbar` is a dict with keys:

- offsetScrollbars (boolean; optional):
    Determines whether Header and Footer components should include
    styles to offset scrollbars. Based on `react-remove-scroll`.
    `True` by default.

- padding (number; optional):
    Controls padding of the main section, `0` by default. !important!:
    use `padding` prop instead of `p`.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- transitionDuration (number; optional):
    Duration of all transitions in ms, `200` by default.

- transitionTimingFunction (optional):
    Timing function of all transitions, `ease` by default.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether associated components should have a border,
    `True` by default.

- zIndex (string | number; optional):
    `z-index` of all associated elements, `200` by default.
#### Navbar

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Header

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Aside

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Footer

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- withBorder (boolean; optional):
    Determines whether component should have a border, overrides
    `withBorder` prop on `AppShell` component.

- zIndex (string | number; optional):
    Component `z-index`, by default inherited from the `AppShell`.
#### Section

- children (a list of or a singular dash component, string or number; required):
    Content.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- grow (boolean; optional):
    Determines whether the section should take all available space,
    `False` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for AspectRatio
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## AspectRatio
Use the Aspect component to maintain responsive consistent width/height ratio.
Category: Layout

### Image

```python
import dash_mantine_components as dmc

component = dmc.AspectRatio(
    dmc.Image(
        src="https://www.nasa.gov/wp-content/uploads/2022/07/web_first_images_release.png",
        alt="Carina Nebula",
    ),
    ratio=4/3,
)
```
### Map embed

```python
import dash_mantine_components as dmc
from dash import html

component = dmc.AspectRatio(
    html.Iframe(
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3025.3063874233135!2d-74.04668908358428!3d40.68924937933441!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25090129c363d%3A0x40c6a5770d25022b!2sStatue%20of%20Liberty%20National%20Monument!5e0!3m2!1sen!2sru!4v1644262070010!5m2!1sen!2sru",
        title="Google map",
    ),
    ratio=16 / 9,
)
```
### Video embed

```python
import dash_mantine_components as dmc
from dash import html

component = dmc.AspectRatio(
    html.Iframe(
        src="https://www.youtube.com/embed/KsTKREWoVC4",
        title="YouTube video player",
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen",
    ),
    ratio=16 / 9,
)
```
### Inside flex container
By default, `AspectRatio` does not have fixed width and height, it will take as much space as possible in a regular
container. To make it work inside flex container, you need to set `width` or `flex` property.

```python
import dash_mantine_components as dmc
from dash import html

component = html.Div(
    dmc.AspectRatio(
        ratio=1,
        style={"flex": "0 0 100px"},
        children=[
            dmc.Image(
                src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/avatars/avatar-6.png",
                alt="Avatar",
            )
        ],
    ),
    style={"display": "flex"},
)
```
### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### AspectRatio Selectors

| Selector | Static selector                 | Description   |
|----------|----------------------------------|---------------|
| root     | .mantine-AspectRatio-root        | Root element  |

---

#### AspectRatio CSS Variables

| Selector | Variable      | Description     |
|----------|---------------|-----------------|
| root     | --ar-ratio    | Aspect ratio    |




### Keyword Arguments
#### AspectRatio

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- ratio (number; optional):
    Aspect ratio, e.g. `16 / 9`, `4 / 3`, `1920 / 1080`, `1` by
    default.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for Center
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Center
Use Center component to center content vertically and horizontally.
Category: Layout

### Simple Example

```python
import dash_mantine_components as dmc

component = dmc.Center(
    style={"height": 200, "width": "100%"},
    children=[
        dmc.Badge("Free", style={"marginRight": 5}),
        dmc.Anchor("Click now!", href="https://mantine.dev/"),
    ],
)
```
### Inline

To use `Center` with inline elements set `inline` prop. For example, you can center link icon and label:

```python
import dash_mantine_components as dmc
from dash_iconify import DashIconify

component = dmc.Box(
    dmc.Anchor(
        href="https://mantine.dev",
        target="_blank",
        children=dmc.Center(
            [
                DashIconify(
                    icon="tabler:arrow-left",  # Use the Tabler Arrow Left icon
                    width=12,
                    height=12,
                ),
                dmc.Box("Back to Mantine website", ml=5),
            ],
            inline=True,
        ),
    )
)
```
### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


| Name | Static selector    | Description  |
|------|--------------------|--------------|
| root | .mantine-Card-root | Root element |


### Keyword Arguments
#### Center

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- inline (boolean; optional):
    Determines whether `inline-flex` should be used instead of `flex`,
    `False` by default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for Container
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Container
Container is the most basic layout element, it centers content horizontally and adds horizontal padding from theme.
Category: Layout

### Simple Example

Container is the most basic layout element, it centers content horizontally and adds horizontal padding from Mantine's
theme.

Component accepts these props:

  * `size` – controls default max width
  * `fluid` – overwrites size prop and sets max width to 100%

```python
import dash_mantine_components as dmc
from dash import html

style = {
    "height": 100,
    "border": f"1px solid {dmc.DEFAULT_THEME['colors']['indigo'][4]}",
    "marginTop": 20,
    "marginBottom": 20,
}

component = html.Div(
    children=[
        dmc.Container("Default container", style=style),
        dmc.Container(
            "xs container with xs horizontal padding", size="xs", px="xs", style=style
        ),
        dmc.Container(
            "200px container with 0px horizontal padding", size=200, px=0, style=style
        ),
    ]
)
```
### Fluid
Set `fluid` prop to make container fluid, it will take 100% of available width, it is the same as setting `size="100%"`.

```python
import dash_mantine_components as dmc
from dash import html


component = dmc.Container(
    "Fluid container has 100% max-width",
    fluid=True,
    h=50,
    bg="var(--mantine-color-blue-light)"
)
```
### Grid strategy

Starting from 2.2.0, `Container` supports `strategy="grid"` prop which enables more features.

Differences from the default `strategy="block"`:

- Uses `display: grid` instead of `display: block`
- Does not include default inline padding
- Does not set `max-width` on the root element (uses grid template columns instead)

Features supported by `strategy="grid"`:

- Everything that is supported by `strategy="block"`
- Children with `data-breakout` attribute take the entire width of the container's parent element
- Children with `data-container` inside `data-breakout` have the same width as the main grid column

Example of using breakout feature:


```python
import dash_mantine_components as dmc
from dash import html


component = dmc.Container(
    [
        dmc.Box("Main Content", bg="var(--mantine-color-indigo-light)", h=50),
        html.Div(
            [
                "Breakout",
                html.Div(
                    "Container inside breakout",
                    style={
                        "backgroundColor": "var(--mantine-color-indigo-filled)",
                        "color": "white",
                        "height": 50,
                    },
                    **{"data-container": ""}
                ),
            ],
            style={
                "backgroundColor": "var(--mantine-color-indigo-light)",
                "marginTop": 16,
            },
            **{"data-breakout": ""}
        ),
    ],
    size=500,
    strategy="grid",
)
```
**Note — Adding custom HTML attributes to Dash components:**

* For `dash-html-components`, you can add custom attributes using Python’s `**` unpacking syntax:

  ```python
  html.Div(**{"data-breakout": ""})
  ```

* For DMC components that support the [Styles API](/styles-api), use the `attributes` prop to pass attributes to elements of the component:

  ```python
  dmc.Paper(attributes={"root": "data-breakout"})
  ```




### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### Container Selectors

| Selector | Static selector            | Description   |
|----------|-----------------------------|---------------|
| root     | .mantine-Container-root     | Root element  |


#### Container CSS Variables

| Selector | Variable          | Description               |
|----------|-------------------|---------------------------|
| root     | --container-size  | Controls container max-width |




### Keyword Arguments
#### Container

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- fluid (boolean; optional):
    Determines whether the container should take 100% of its parent
    width. If set, `size` prop is ignored. `False` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- size (number; optional):
    Sets `max-width` of the container, value is not responsive – it is
    the same for all screen sizes. Numbers are converted to rem.
    Ignored when `fluid` prop is set. `'md'` by default.

- strategy (a value equal to: 'block', 'grid'; optional):
    Centering strategy. Default value: 'block'.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for Flex
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Flex
Use the Flex component to compose elements in a flex container.
Category: Layout

### Introduction

### Supported Props

| Prop        | CSS Property     | Theme Key       |
|-------------|------------------|-----------------|
| gap         | gap              | theme.spacing   |
| rowGap      | rowGap           | theme.spacing   |
| columnGap   | columnGap        | theme.spacing   |
| align       | alignItems       | –               |
| justify     | justifyContent   | –               |
| wrap        | flexWrap         | –               |
| direction   | flexDirection    | –               |



### Responsive Props

Flex component props can have responsive values the same way as other style props:

```python
import dash_mantine_components as dmc

component = dmc.Flex(
    [
        dmc.Button("Button 1"),
        dmc.Button("Button 2"),
        dmc.Button("Button 3"),
    ],
    direction={"base": "column", "sm": "row"},
    gap={"base": "sm", "sm": "lg"},
    justify={"sm": "center"},
)
```
### Comparison: Group, Stack, and Flex

`Flex` component is an alternative to `Group` and `Stack`.
`Flex` is more flexible, it allows creating both horizontal and vertical flexbox layouts, but requires more configuration.

| Feature                    | Group | Stack | Flex |
|----------------------------|-------|-------|------|
| Direction                  | horizontal | vertical | both |
| Equal width children       | ✅     | ❌    | ❌   |
| flex-wrap support          | ✅     | ❌    | ✅   |
| Responsive flexbox props   | ❌     | ❌    | ✅   |




### Browser support
`Flex` uses flexbox gap to add spacing between children. In older browsers, `Flex` children may not have spacing.




### Styles API



This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.



| Name | Static selector    | Description  |
|:-----|:-------------------|:-------------|
| root | .mantine-Flex-root | Root element |


### Keyword Arguments
#### Flex

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (optional):
    `align-items` CSS property.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- columnGap (number; optional):
    `column-gap` CSS property.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- direction (optional):
    `flex-direction` CSS property.

- gap (number; optional):
    `gap` CSS property.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- justify (optional):
    `justify-content` CSS property.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- rowGap (number; optional):
    `row-gap` CSS property.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- wrap (optional):
    `flex-wrap` CSS property.
---

> Dash Mantine Components v2.4.0 Documentation for Grid
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Grid
Responsive 12 columns grid system
Category: Layout

### Usage

Use Grid component to create layouts with a flexbox grid system.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span=6),
        dmc.GridCol(dmc.Box("2", style=style), span=3),
        dmc.GridCol(dmc.Box("3", style=style), span=3),
    ],
    gutter="xl",
)
```
### Columns span
`The GridCol` `span` prop controls the ratio of column width to the total width of the row. By default, grid uses
12 columns layout, so `span` prop can be any number from 1 to 12.

Examples:
```python
dmc.GridCol(span=3)  # 3 / 12 = 25% of row width
dmc.GridCol(span=4)  # 4 / 12 = 33% of row width
dmc.GridCol(span=6)  # 6 / 12 = 50% of row width
dmc.GridCol(span=12) # 12 / 12 = 100% of row width
```
`span` prop also supports dictionary syntax to change column width based on viewport width, it accepts `xs`, `sm`, `md`,
`lg` and `xl` keys and values from 1 to 12. The syntax is the same as in `style` props.

In the following example `span={'base': 12, 'md': 6, 'lg': 3`}:

- `base` – 12 / 12 = 100% of row width when viewport width is less than `md` breakpoint
- `md` – 6 / 12 = 50% of row width when viewport width is between md and `lg` breakpoints
- `lg` – 3 / 12 = 25% of row width when viewport width is greater than `lg` breakpoint


```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span={"base": 12, "md": 6, "lg":3}),
        dmc.GridCol(dmc.Box("2", style=style), span={"base": 12, "md": 6, "lg":3}),
        dmc.GridCol(dmc.Box("3", style=style), span={"base": 12, "md": 6, "lg":3}),
        dmc.GridCol(dmc.Box("4", style=style), span={"base": 12, "md": 6, "lg":3}),
    ],
)
```
### Gutter

Set `gutter` prop to control spacing between columns. The prop works the same way as `style` props – you can reference
theme.spacing values with `xs`, `sm`, `md`, `lg` and `xl` strings and use dictionary syntax to change gutter based on
viewport width.  You can also set gutter to a number to set spacing in px.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span=4),
        dmc.GridCol(dmc.Box("2", style=style), span=4),
        dmc.GridCol(dmc.Box("3", style=style), span=4),
    ],
    gutter={ "base": 5, "xs": "md", "md": "xl", "xl": 50 },
)
```
### Grow

Set `grow` prop on Grid to force last row to take 100% of container width.

### Column Offset

Set `offset` prop on `GridCol` component to add gaps to the grid. `offset` prop supports the same syntax as span
prop: a number from 1 to 12 or a dictionary with `xs`, `sm`, `md`, `lg` and `xl` keys and values from 1 to 12.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span=3),
        dmc.GridCol(dmc.Box("2", style=style), span=3),
        dmc.GridCol(dmc.Box("3", style=style), span=3, offset=3),
    ],
    gutter="xl",
)
```
### Order
Set the `order` prop on `GridCol` component to change the order of columns. `order` prop supports the same syntax as
`span` prop: a number from 1 to 12 or a dictionary with `xs`, `sm`, `md`, `lg` and `xl` keys and values from 1 to 12.


```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("2", style=style), span=3, order={"base": 2, "sm": 1, "lg": 3}),
        dmc.GridCol(dmc.Box("3", style=style), span=3, order={"base": 3, "sm": 2, "lg": 2}),
        dmc.GridCol(dmc.Box("1", style=style), span=3, order={"base": 1, "sm": 3, "lg": 1}),
    ],
)
```
### Multiple rows

Once children columns span and offset sum exceeds `columns` prop (defaults to 12), columns are placed on next row.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span=4),
        dmc.GridCol(dmc.Box("2", style=style), span=4),
        dmc.GridCol(dmc.Box("3", style=style), span=4),
        dmc.GridCol(dmc.Box("4", style=style), span=4),
    ],
    gutter="xl",
)
```
### Justify and Align

Since grid is a flexbox container, you can control justify-content and align-items properties by using `justify` and
`align` props respectively. Note the minimum height set on column 2 and 3.

```python
import dash_mantine_components as dmc

dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1"), span=4),
        dmc.GridCol(dmc.Box("2", style={"minHeight":80}), span=4),
        dmc.GridCol(dmc.Box("3", style={"minHeight":120}), span=4),
    ],
    justify="center",
    align="stretch",

)
```

### Auto Sized Columns

All columns in a row with `span` or a `breakpoint` of `auto` will have equal size, growing as much as they can to fill the row.
In this example, the second column takes up 50% of the row while the other two columns automatically resize to fill the remaining space.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("span=auto", style=style), span="auto"),
        dmc.GridCol(dmc.Box("span=6", style=style), span=6),
        dmc.GridCol(dmc.Box("span=auto", style=style), span="auto"),
    ],
    gutter="xl",
)
```
### Fit Content

If you set `span` or a `breakpoint` to `content`, the column's size will automatically adjust to match the width of its content.

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("content width", style=style), span="content"),
        dmc.GridCol(dmc.Box("2", style=style), span=6),
    ],
    gutter="xl",
)
```
### Change columns count
By default, grids uses 12 columns layout, you can change it by setting `columns` prop on `Grid` component. Note that
in this case, columns span and offset will be calculated relative to this value.

In the following example, first column takes 50% with 12 span (12/24), second and third take 25% (6/24):


```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Grid(
    children=[
        dmc.GridCol(dmc.Box("1", style=style), span=12),
        dmc.GridCol(dmc.Box("2", style=style), span=6),
        dmc.GridCol(dmc.Box("3", style=style), span=6),
    ],
    columns=24
)
```
### Container queries
To use [container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries) instead
of media queries, set `type='container'`. With container queries, all responsive values are adjusted based on the
container width, not the viewport width.

Note that, when using container queries, it is also required to set `breakpoints` prop to the exact container width values.

To see how the grid changes, resize the root element of the demo with the resize handle located at the bottom right
corner of the demo:

```python
import dash_mantine_components as dmc

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.Box(
    # Wrapper div is added for demonstration purposes only,
    # it is not required in real projects
    dmc.Grid(
        children=[
            dmc.GridCol(dmc.Box("1", style=style), span={"base": 12, "md": 6, "lg": 3}),
            dmc.GridCol(dmc.Box("2", style=style), span={"base": 12, "md": 6, "lg": 3}),
            dmc.GridCol(dmc.Box("3", style=style), span={"base": 12, "md": 6, "lg": 3}),
            dmc.GridCol(dmc.Box("4", style=style), span={"base": 12, "md": 6, "lg": 3}),
        ],
        gutter="xl",
        type="container",
        breakpoints={
            "xs": "100px",
            "sm": "200px",
            "md": "300px",
            "lg": "400px",
            "xl": "500px",
        },
    ),
    style={"resize": 'horizontal', "overflow": 'hidden', "maxWidth": '100%', "margin": 24 },
)
```
### overflow: hidden
By default, `Grid` has `overflow: visible` style on the root element. In some cases you might want to change it to
`overflow: hidden` to prevent negative margins from overflowing the grid container. For example, if you use `Grid`
without parent container which has padding.

```python
dmc.Grid([
    dmc.GridCol("1", span=6),
    dmc.GridCol("2", span=6),
], overflow="hidden")
```


### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### Grid Selectors

| Selector   | Static selector            | Description                              |
|------------|-----------------------------|------------------------------------------|
| container  | .mantine-Grid-container     | Container element, only used with `type="container"` prop |
| root       | .mantine-Grid-root          | Root element                             |
| inner      | .mantine-Grid-inner         | Columns wrapper                          |
| col        | .mantine-Grid-col           | `Grid.Col` root element                  |

---

#### Grid CSS Variables

| Selector | Variable          | Description                      |
|----------|-------------------|----------------------------------|
| root     | --grid-overflow   | Controls `overflow` property     |
|          | --grid-align      | Controls `align-items` property  |
|          | --grid-justify    | Controls `justify-content` property |


### Keyword Arguments
#### Grid

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (optional):
    Sets `align-items`, `stretch` by default.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- breakpoints (dict; optional):
    Breakpoints values, only applicable when `type="container"` is
    set, ignored when `type` is not set or `type="media"` is set.

    `breakpoints` is a dict with keys:

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- columns (number; optional):
    Number of columns in each row, `12` by default.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- grow (boolean; optional):
    Determines whether columns in the last row should expand to fill
    all available space, `False` by default.

- gutter (number; optional):
    Gutter between columns, key of `theme.spacing` or any valid CSS
    value, `'md'` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- justify (optional):
    Sets `justify-content`, `flex-start` by default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- overflow (optional):
    Sets `overflow` CSS property on the root element, `'visible'` by
    default.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- type (a value equal to: 'media', 'container'; optional):
    Determines typeof of queries that are used for responsive styles,
    `'media'` by default.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
#### GridCol

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- offset (number; optional):
    Column offset on the left side – number of columns that should be
    left empty before this column.

- order (number; optional):
    Column order, can be used to reorder columns at different viewport
    sizes.

- span (number; optional):
    Column span, `12` by default.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for Group
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Group
Use Group component to place components in a horizontal flex container.
Category: Layout

### Usage

### preventGrowOverflow
`preventGrowOverflow` prop allows you to control how `Group` children should behave when there is not enough space to
fit them all on one line. By default, children are not allowed to take more space than (1 / children.length) * 100%
of parent width (`preventGrowOverflow` is set to True). To change this behavior, set `preventGrowOverflow` to False and
children will be allowed to grow and take as much space as they need.


```python
import dash_mantine_components as dmc

component = dmc.Box(
    style={"overflow": "hidden"},
    children=[
        dmc.Box(
            maw=500,
            p="md",
            mx="auto",
            bg="var(--mantine-color-blue-light)",
            children=[
                dmc.Text(
                    size="sm",
                    mb=5,
                    children=(
                        "preventGrowOverflow: true – each child width is always limited "
                        "to 33% of parent width (since there are 3 children)"
                    ),
                ),
                dmc.Group(
                    grow=True,
                    wrap="nowrap",
                    children=[
                        dmc.Button("First button", variant="default"),
                        dmc.Button("Second button with large content", variant="default"),
                        dmc.Button("Third button", variant="default"),
                    ],
                ),
                dmc.Text(
                    size="sm",
                    mb=5,
                    mt="md",
                    children=(
                        "preventGrowOverflow: false – children will grow based on their "
                        "content, they can take more than 33% of parent width"
                    ),
                ),
                dmc.Group(
                    grow=True,
                    preventGrowOverflow=False,
                    wrap="nowrap",
                    children=[
                        dmc.Button("First button", variant="default"),
                        dmc.Button("Second button with large content", variant="default"),
                        dmc.Button("Third button", variant="default"),
                    ],
                ),
            ],
        )
    ],
)
```
### Group children
`Group` works correctly only with components. Strings, or numbers may have incorrect styles if `grow` prop is set:

```python
# don't do this
dmc.Group([
    "Some text",
    dmc.Text("Some more text"),
    20,
], grow=True)
```

### Browser support
`Group` uses flexbox `gap` to add spacing between children. In older browsers, `Group` children may not have spacing.

### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### Group Selectors

| Selector | Static selector        | Description    |
|----------|-------------------------|----------------|
| root     | .mantine-Group-root     | Root element   |



#### Group CSS Variables

| Selector | Variable                 | Description                                                  |
|----------|--------------------------|--------------------------------------------------------------|
| root     | --group-align            | Controls `align-items` property                              |
|          | --group-justify          | Controls `justify-content` property                          |
|          | --group-gap              | Controls `gap` property                                      |
|          | --group-wrap             | Controls `flex-wrap` property                                |
|          | --group-child-width      | Controls max-width of child elements when `grow` and `preventGrowOverflow` are set |



#### Group Data Attributes

| Selector | Attribute   | Condition       |
|----------|-------------|-----------------|
| root     | data-grow   | `grow` prop is set |


### Keyword Arguments
#### Group

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (optional):
    Controls `align-items` CSS property, `'center'` by default.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- gap (number; optional):
    Key of `theme.spacing` or any valid CSS value for `gap`, numbers
    are converted to rem, `'md'` by default.

- grow (boolean; optional):
    Determines whether each child element should have `flex-grow: 1`
    style, `False` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- justify (optional):
    Controls `justify-content` CSS property, `'flex-start'` by
    default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- preventGrowOverflow (boolean; optional):
    Determines whether children should take only dedicated amount of
    space (`max-width` style is set based on the number of children),
    `True` by default.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- wrap (a value equal to: '-moz-initial', 'inherit', 'initial', 'revert', 'revert-layer', 'unset', 'nowrap', 'wrap', 'wrap-reverse'; optional):
    Controls `flex-wrap` CSS property, `'wrap'` by default.
---

> Dash Mantine Components v2.4.0 Documentation for SimpleGrid
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## SimpleGrid
Use SimpleGrid component to create a grid where each column takes equal width. You can use it to create responsive layouts.
Category: Layout

### Usage

`SimpleGrid` is a responsive grid system with equal-width columns. It uses CSS grid layout. If you need to set different
widths for columns, use `Grid` component instead.

### spacing and verticalSpacing props
`spacing` prop is used both for horizontal and vertical spacing if `verticalSpacing` is not set:

```python

# `spacing` is used for both horizontal and vertical spacing
dmc.SimpleGrid(spacing="xl")

# `spacing` is used for horizontal spacing, `verticalSpacing` for vertical
dmc.SimpleGrid(spacing="xl", verticalSpacing="lg")
```

### Responsive Props

`cols`, `spacing` and `verticalSpacing` props support object notation for responsive values,
it works the same way as [style props](/style-props): the object may have `base`, `xs`, `sm`, `md`, `lg` and `xl` key,
and values from those keys will be applied according to current viewport width.

`cols` prop can be understood from the below example as:

- 1 column if viewport width is less than `sm` breakpoint
- 2 columns if viewport width is between `sm` and `lg` breakpoints
- 5 columns if viewport width is greater than `lg` breakpoint

Same logic applies to `spacing` and `verticalSpacing` props.

Resize browser to see breakpoints behavior.

```python
import dash_mantine_components as dmc
from dash import html

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = dmc.SimpleGrid(
    cols={"base": 1, "sm": 2, "lg": 5},
    spacing={"base": 10, "sm": "xl"},
    verticalSpacing={"base": "md", "sm": "xl"},
    children=[
        html.Div("1", style=style),
        html.Div("2", style=style),
        html.Div("3", style=style),
        html.Div("4", style=style),
        html.Div("5", style=style),
    ],
)
```
### Container queries
To use [container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries) instead
of media queries, set `type='container'`. With container queries, grid columns and spacing will be adjusted based on the
container width, not the viewport width.

Note that, when using container queries, `cols`, `spacing` and `verticalSpacing` props cannot reference `theme.breakpoints`
values in keys. It is required to use exact `px` or `em` values.

To see how the grid changes, resize the root element of the demo with the resize handle located at the bottom right
corner of the demo:


```python
import dash_mantine_components as dmc
from dash import html

style = {
    "border": f"1px solid var(--mantine-primary-color-filled)",
    "textAlign": "center",
}

component = html.Div(
    # Wrapper div is added for demonstration purposes only,
    # it is not required in real projects
    dmc.SimpleGrid(
        type="container",
        cols={"base": 1, "300px": 2, "500px": 5},
        spacing={"base": 10, "300px": "xl"},
        children=[
            html.Div("1", style=style),
            html.Div("2", style=style),
            html.Div("3", style=style),
            html.Div("4", style=style),
            html.Div("5", style=style),
        ],
        p="xs",
    ),
    style={"resize": "horizontal", "overflow": "hidden", "maxWidth": "100%"},
)
```
### Styles API



This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


| Name        | Static selector          | Description                                      |
|:------------|:-------------------------|:-------------------------------------------------|
| root        | .mantine-SimpleGrid-root | Root element                                     |


### Keyword Arguments
#### SimpleGrid

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- cols (number; optional):
    Number of columns, `1` by default.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- spacing (number; optional):
    Spacing between columns, `'md'` by default.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- type (a value equal to: 'media', 'container'; optional):
    Determines typeof of queries that are used for responsive styles,
    'media' by default.

- variant (string; optional):
    variant.

- verticalSpacing (number; optional):
    Spacing between rows, `'md'` by default.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---

> Dash Mantine Components v2.4.0 Documentation for Space
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Space
Use the Space component to add horizontal or vertical spacing from theme.
Category: Layout

### Simple Example

Space component can be customized with two props: `h` and `w`, shortcuts for height and width. These can take either
values from Mantine's theme i.e. xs, sm, md, lg, xl or number.

```python
import dash_mantine_components as dmc
from dash import html

component = html.Div(
    [
        dmc.Group([dmc.Badge("Badge 1"), dmc.Badge("Badge 2")]),
        dmc.Space(h="xl"),
        dmc.Group([dmc.Badge("Badge 1"), dmc.Space(w="lg"), dmc.Badge("Badge 2")]),
        dmc.Space(h=30),
        dmc.Group([dmc.Badge("Badge 1"), dmc.Space(w=45), dmc.Badge("Badge 2")]),
    ]
)
```
### Where to use

In most cases, you would want to use margin props instead of `Space` when working with Mantine components:

```python
import dash_mantine_components as dmc
from dash import html

html.Div([
    dmc.Text("First line"),
    dmc.Text("Second line", mt="md"),
])
```

But when you work with other components like `html` or `dcc`, you do not have access to Mantine's theme spacing,
and you may want to use dmc.Space component:

```python
import dash_mantine_components as dmc
from dash import html

html.Div([
    html.P("First line"),
    dmc.Space(h="md"),
    html.P("Second line"),
])
```


### Keyword Arguments
#### Space

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- className (string; optional):
    Class added to the root element, if applicable.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- tabIndex (number; optional):
    tab-index.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
---


> Dash Mantine Components v2.4.0 Documentation for Stack
> See complete docs at https://www.dash-mantine-components.com/assets/llms.txt
> All relative links in this file should be resolved against https://www.dash-mantine-components.com



## Stack
Use Stack component to compose elements and components in a vertical flex container
Category: Layout

### Usage

`Stack` is a vertical flex container. If you need a horizontal flex container, use `Group` component instead. If you
need to have full control over flex container properties, use `Flex` component.

Adjust stack styles with `align`, `justify`, and `spacing` props.

```python
import dash_mantine_components as dmc

component = dmc.Stack(
    [
        dmc.Button("1", variant="outline"),
        dmc.Button("2", variant="outline"),
        dmc.Button("3", variant="outline"),
    ],
    align="center",
    gap="xl",
)
```
### Interactive Demo

### Styles API


This component supports Styles API. With Styles API, you can customize styles of any inner element. See the Styling and Theming sections of these docs for more information.


#### Stack Selectors

| Selector | Static selector        | Description    |
|----------|-------------------------|----------------|
| root     | .mantine-Stack-root     | Root element   |



#### Stack CSS Variables

| Selector | Variable         | Description                     |
|----------|------------------|---------------------------------|
| root     | --stack-align    | Controls `align-items` property |
|          | --stack-justify  | Controls `justify-content` property |
|          | --stack-gap      | Controls `gap` property         |



### Keyword Arguments
#### Stack

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- align (optional):
    Controls `align-items` CSS property, `'stretch'` by default.

- aria-* (string; optional):
    Wild card aria attributes.

- attributes (boolean | number | string | dict | list; optional):
    Passes attributes to inner elements of a component.  See Styles
    API docs.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds custom CSS class names to inner elements of a component.  See
    Styles API docs.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- gap (number; optional):
    Key of `theme.spacing` or any valid CSS value to set `gap`
    property, numbers are converted to rem, `'md'` by default.

- hiddenFrom (optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- justify (optional):
    Controls `justify-content` CSS property, `'flex-start'` by
    default.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

- mod (string; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- styles (boolean | number | string | dict | list; optional):
    Adds inline styles directly to inner elements of a component.  See
    Styles API docs.

- tabIndex (number; optional):
    tab-index.

- variant (string; optional):
    variant.

- visibleFrom (optional):
    Breakpoint below which the component is hidden with `display:
    none`.
