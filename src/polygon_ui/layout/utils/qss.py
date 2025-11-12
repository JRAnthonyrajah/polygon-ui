"""
Layout QSS generation utilities for Polygon UI layout components.
Enhanced for responsive support using Qt property selectors.
"""

from typing import Dict, Any, Optional


def generate_flex_qss(
    direction: str = "column",
    justify: str = "start",
    align: str = "stretch",
    gap: Optional[str] = None,
    theme_spacing: Optional[Dict[str, int]] = None,
    breakpoint: Optional[str] = None,
) -> str:
    """
    Generate QSS for flexbox-like layout styling using Qt properties.
    Sets styles for container and children based on flex properties.
    Alignment and justification should be handled primarily by QBoxLayout,
    QSS provides supplementary styling.
    """
    if theme_spacing is None:
        theme_spacing = {}

    qss_parts = []

    # Build selector
    base_selector = "QWidget"
    if breakpoint:
        base_selector += f'[breakpoint="{breakpoint}"]'
    container_sel = f'{base_selector}[cssClass="layout-container"]'
    child_sel = f'{base_selector}[cssClass="layout-child"]'

    # Container base styles
    container_rules = "box-sizing: border-box;"
    qss_parts.append(f"{container_sel} {{ {container_rules} }}")

    # Child gap margins
    if gap:
        gap_px = theme_spacing.get(gap, 8)
        half_gap = gap_px // 2
        if direction == "row":
            margin_rules = f"margin-left: {half_gap}px; margin-right: {half_gap}px;"
        else:
            margin_rules = f"margin-top: {half_gap}px; margin-bottom: {half_gap}px;"
        child_rules = f"box-sizing: border-box; {margin_rules}"
        qss_parts.append(f"{child_sel} {{ {child_rules} }}")

    # Supplementary alignment for content
    justify_map = {
        "start": "left",
        "center": "center",
        "end": "right",
        "space-between": "justify",
        "space-around": "justify",
    }
    align_map = {
        "start": "top",
        "center": "middle",
        "end": "bottom",
        "stretch": "",  # handled by layout
    }
    if justify in justify_map:
        align_h = justify_map[justify]
        qss_parts.append(f"{container_sel} {{ text-align: {align_h}; }}")
    if align in align_map and align_map[align]:
        align_v = align_map[align]
        qss_parts.append(f"{container_sel} {{ vertical-align: {align_v}; }}")

    return "\n".join(qss_parts)


def generate_grid_qss(
    columns: int = 12,
    gutter: Optional[str] = None,
    theme_spacing: Optional[Dict[str, int]] = None,
    breakpoint: Optional[str] = None,
) -> str:
    """
    Generate QSS for grid layout styling using calculated widths.
    Note: Last cell margin-right should be set to 0 in code for perfect gutters.
    """
    if theme_spacing is None:
        theme_spacing = {}

    qss_parts = []

    base_selector = "QWidget"
    if breakpoint:
        base_selector += f'[breakpoint="{breakpoint}"]'
    container_sel = f'{base_selector}[cssClass="grid-container"]'
    cell_sel = f'{base_selector}[cssClass="grid-cell"]'

    # Container
    container_rules = "box-sizing: border-box;"
    qss_parts.append(f"{container_sel} {{ {container_rules} }}")

    # Cell width and margins
    if gutter:
        gutter_px = theme_spacing.get(gutter, 8)
        total_gutter_width = (columns - 1) * gutter_px
        width = f"calc((100% - {total_gutter_width}px) / {columns})"
        margin_right = f"{gutter_px}px"
    else:
        width = f"{100 / columns}%"
        margin_right = "0"
    cell_rules = (
        f"width: {width}; box-sizing: border-box; margin-right: {margin_right};"
    )
    qss_parts.append(f"{cell_sel} {{ {cell_rules} }}")

    return "\n".join(qss_parts)


def generate_responsive_qss(breakpoints: Dict[str, Dict[str, Any]]) -> str:
    """
    Generate comprehensive QSS for responsive layouts across breakpoints.
    Each breakpoint generates its own QSS rules using property selectors.
    In component code: widget.setProperty("breakpoint", current_breakpoint)
    """
    all_qss_parts = []
    for bp_name, props in breakpoints.items():
        theme_spacing = props.pop("theme_spacing", None)
        layout_type = props.pop("type", "flex")
        if layout_type == "flex":
            # Pass relevant props
            flex_props = {}
            if "direction" in props:
                flex_props["direction"] = props["direction"]
            if "justify" in props:
                flex_props["justify"] = props["justify"]
            if "align" in props:
                flex_props["align"] = props["align"]
            if "gap" in props:
                flex_props["gap"] = props["gap"]
            qss = generate_flex_qss(
                breakpoint=bp_name, theme_spacing=theme_spacing, **flex_props
            )
        elif layout_type == "grid":
            grid_props = {}
            if "columns" in props:
                grid_props["columns"] = props["columns"]
            if "gutter" in props:
                grid_props["gutter"] = props["gutter"]
            qss = generate_grid_qss(
                breakpoint=bp_name, theme_spacing=theme_spacing, **grid_props
            )
        else:
            qss = f"/* Unsupported layout type '{layout_type}' for breakpoint '{bp_name}' */"
        all_qss_parts.append(qss)
    return "\n\n".join(all_qss_parts) + "\n/* End of responsive QSS */\n"
