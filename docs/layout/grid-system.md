# Grid System Documentation

## Overview

The Polygon UI Grid System provides a powerful, responsive layout framework inspired by CSS Grid and modern web frameworks like Mantine. It consists of three main components:

- **Grid**: Advanced grid container with responsive columns, gutters, and alignment
- **SimpleGrid**: Simplified grid for equal-sized columns with responsive behavior
- **Col**: Column component for precise control within Grid layouts

## Grid Component

### Basic Usage

```python
from polygon_ui.layout.components import Grid, Col

# Basic 12-column grid
grid = Grid(columns=12)
grid.add_child(Col(span=4), content="Column 1")
grid.add_child(Col(span=4), content="Column 2")
grid.add_child(Col(span=4), content="Column 3")
```

### Responsive Columns

```python
# Responsive column configuration
grid = Grid(columns={
    "base": 1,    # Mobile: 1 column
    "sm": 2,      # Small screens: 2 columns
    "md": 3,      # Medium screens: 3 columns
    "lg": 4,      # Large screens: 4 columns
    "xl": 6       # Extra large: 6 columns
})
```

### Gutters and Spacing

```python
# Theme-based gutter
grid = Grid(columns=12, gutter="lg")  # Uses theme spacing

# Custom pixel gutter
grid = Grid(columns=12, gutter=24)   # 24px gutters

# Responsive gutters
grid = Grid(columns=12, gutter={
    "base": "sm",
    "md": "md",
    "lg": "lg"
})
```

### Alignment and Justification

```python
# Horizontal alignment
grid = Grid(
    columns=12,
    justify="start",   # start, center, end, space-between, space-around, space-evenly
)

# Vertical alignment
grid = Grid(
    columns=12,
    align="start"      # start, center, end, stretch
)
```

## SimpleGrid Component

### Basic Usage

```python
from polygon_ui.layout.components import SimpleGrid

# Equal columns with responsive breakpoints
grid = SimpleGrid(cols={
    "base": 1,    # Mobile: 1 column
    "sm": 2,      # Small: 2 columns
    "md": 3,      # Medium: 3 columns
    "lg": 4       # Large: 4 columns
})

# Add children - they automatically flow into equal columns
for i in range(8):
    grid.add_child(QLabel(f"Item {i+1}"))
```

### Spacing

```python
# Theme-based spacing
grid = SimpleGrid(cols=3, spacing="md")

# Custom pixel spacing
grid = SimpleGrid(cols=3, spacing=16)
```

## Col Component

### Span and Offset

```python
from polygon_ui.layout.components import Col

# Column spanning (out of 12 by default)
col = Col(span=6)        # Takes half the width
col = Col(span={"md": 6, "lg": 4})  # Responsive span

# Column offset for positioning
col = Col(span=6, offset=3)  # 6 columns wide, offset by 3
```

### Ordering and Visibility

```python
# Visual reordering
col = Col(span=4, order=2)  # Appears third visually

# Responsive visibility
col = Col(
    span=4,
    visible={"base": False, "md": True}  # Hidden on mobile, visible on larger screens
)
```

### Convenience Methods

```python
col = Col()

# Quick width presets
col.half_width()      # 12 on mobile, 6 on md+
col.third_width()     # 12 on mobile, 4 on md+
col.quarter_width()   # 12 on mobile, 3 on md+

# Quick positioning
col.offset_center()   # Center horizontally
col.offset_right()    # Align to right
col.offset_left()     # Align to left
```

## Best Practices

### 1. Mobile-First Design

Always start with mobile layouts and enhance for larger screens:

```python
# ✅ Good - mobile first
grid = Grid(columns={
    "base": 1,
    "sm": 2,
    "md": 3
})

# ❌ Avoid - desktop first without mobile consideration
grid = Grid(columns=4)  # Always 4 columns, even on mobile
```

### 2. Use Semantic Breakpoints

```python
# ✅ Good - meaningful breakpoints
cols = {
    "base": 1,    # Mobile portrait
    "sm": 2,      # Mobile landscape / small tablet
    "md": 3,      # Tablet
    "lg": 4,      # Desktop
    "xl": 6       # Large desktop
}
```

### 3. Consistent Spacing

Use theme spacing values for consistency:

```python
# ✅ Good - theme-based spacing
grid = Grid(columns=12, gutter="md")

# ❌ Avoid - arbitrary pixel values
grid = Grid(columns=12, gutter=27)
```

### 4. Accessibility Considerations

```python
# Maintain logical order for screen readers
col = Col(span=4, order=0)  # Keep order=0 for logical flow

# Use appropriate column spans for content
wide_content = Col(span={"base": 12, "md": 8})  # Give content room to breathe
```

### 5. Performance Optimization

```python
# For large grids, consider SimpleGrid for better performance
large_grid = SimpleGrid(cols=4)  # More efficient than complex Grid + Col

# Use responsive spans to avoid unnecessary complexity
simple = Col(span=6)  # Better than responsive when not needed
```

## Migration from QGridLayout

### Before (QGridLayout)

```python
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel

widget = QWidget()
layout = QGridLayout(widget)

# Add widgets with row, column, colspan, rowspan
layout.addWidget(QLabel("A"), 0, 0, 1, 2)  # Row 0, Col 0, 1 row, 2 cols
layout.addWidget(QLabel("B"), 0, 2, 1, 1)  # Row 0, Col 2, 1 row, 1 col
layout.addWidget(QLabel("C"), 1, 0, 1, 3)  # Row 1, Col 0, 1 row, 3 cols

# Set spacing
layout.setHorizontalSpacing(16)
layout.setVerticalSpacing(8)
```

### After (Polygon UI Grid)

```python
from polygon_ui.layout.components import Grid, Col

grid = Grid(columns=3, gutter="md")

# More semantic and responsive
grid.add_child(Col(span=2), QLabel("A"))
grid.add_child(Col(span=1), QLabel("B"))
grid.add_child(Col(span=3), QLabel("C"))

# Responsive capabilities not possible with QGridLayout
responsive_grid = Grid(columns={
    "base": 1,
    "sm": 2,
    "md": 3
})
```

### Key Differences

| Feature | QGridLayout | Polygon UI Grid |
|---------|-------------|-----------------|
| Responsive Design | Manual | Built-in |
| Theme Integration | None | Full |
| Mobile-First | No | Yes |
| Semantic API | Low-level | High-level |
| Auto-fit | No | Yes |
| Performance | Good | Excellent |

## Advanced Patterns

### Nested Grids

```python
outer_grid = Grid(columns=12, gutter="md")

# First column contains nested grid
nested_grid = Grid(columns=6, gutter="sm")
nested_grid.add_child(Col(span=3), QLabel("Nested 1"))
nested_grid.add_child(Col(span=3), QLabel("Nested 2"))

outer_grid.add_child(Col(span=6), nested_grid)
outer_grid.add_child(Col(span=6), QLabel("Main content"))
```

### Auto-fit Layouts

```python
# Grid that automatically fits content
auto_grid = Grid(columns="auto")  # Automatically determines column count
auto_grid.add_child(Col(span="auto"), content)  # Auto-sizing columns
```

### Complex Responsive Layouts

```python
# Card grid that adapts from 1 to 4 columns
card_grid = Grid(columns={
    "base": 1,
    "sm": 2,
    "md": 2,
    "lg": 3,
    "xl": 4
}, gutter="lg")

# Cards that are full-width on mobile, half on tablet, quarter on desktop
for card_data in cards:
    card = Col(span={
        "base": 12,
        "sm": 6,
        "md": 6,
        "lg": 4,
        "xl": 3
    })
    card.add_child(create_card_widget(card_data))
    card_grid.add_child(card)
```

## Performance Considerations

- **SimpleGrid vs Grid**: Use SimpleGrid for equal columns (better performance)
- **Responsive Complexity**: Keep responsive logic simple when possible
- **Large Grids**: Grid components are optimized for 100+ children
- **Resize Events**: Responsive updates are debounced for smooth performance

## Conclusion

The Polygon UI Grid System provides a modern, responsive alternative to Qt's native layout system. With mobile-first design, theme integration, and comprehensive responsive capabilities, it enables the creation of complex, adaptive layouts with clean, semantic code.

For specific API details, see the individual component documentation and type hints.
