"""
Layout QSS generation utilities for Polygon UI layout components.
"""

from typing import Dict, Any, Optional


def generate_flex_qss(
    direction: str = "column",
    justify: str = "start",
    align: str = "stretch",
    gap: Optional[str] = None,
    theme_spacing: Dict[str, int] = None,
) -> str:
    """
    Generate QSS for flexbox-like layout styling.

    Note: Qt QSS doesn't support CSS flexbox directly. This utility generates
    equivalent visual styling using margins, padding, and alignment properties.

    Args:
        direction: Layout direction ("row" or "column")
        justify: Justify content ("start", "center", "end", "space-between", "space-around")
        align: Align items ("start", "center", "end", "stretch")
        gap: Gap spacing key from theme (e.g., "sm", "md")
        theme_spacing: Theme spacing values {key: pixels}

    Returns:
        QSS string for the layout container and children.
    """
    if theme_spacing is None:
        theme_spacing = {}

    qss_parts = []

    # Container styling
    if direction == "row":
        # For horizontal layout, use inline-block like behavior if needed
        qss_parts.append("QWidget.layout-container {")
        qss_parts.append("    /* Horizontal layout simulation */")
        qss_parts.append("}")
    else:
        qss_parts.append("QWidget.layout-container {")
        qss_parts.append("    /* Vertical layout simulation */")
        qss_parts.append("}")

    # Gap simulation via child margins (if not using Qt layout spacing)
    if gap:
        gap_px = theme_spacing.get(gap, 8)
        child_margin = f"{gap_px}px"
        qss_parts.append(f"QWidget.layout-child {{ margin: {child_margin}; }}")
        # Adjust for direction
        if direction == "row":
            qss_parts[-1] = qss_parts[-1].replace(
                "margin: ", "margin-left: "
            )  # simplistic
        else:
            qss_parts[-1] = qss_parts[-1].replace("margin: ", "margin-top: ")

    # Justify and align simulation (limited in QSS)
    justify_map = {
        "start": "left",  # or top
        "center": "center",
        "end": "right",  # or bottom
        "space-between": "justify",  # not direct
        "space-around": "justify",  # not direct
    }
    align_map = {
        "start": "top",
        "center": "center",
        "end": "bottom",
        "stretch": "stretch",
    }

    justify_qss = justify_map.get(justify, "left")
    align_qss = align_map.get(align, "stretch")

    qss_parts.append(
        f"QWidget.layout-container {{ text-align: {justify_qss}; vertical-align: {align_qss}; }}"
    )

    return "\n".join(qss_parts)


def generate_grid_qss(
    columns: int = 12,
    gutter: Optional[str] = None,
    theme_spacing: Dict[str, int] = None,
) -> str:
    """
    Generate QSS for grid layout styling.

    Args:
        columns: Number of columns
        gutter: Gutter spacing key from theme
        theme_spacing: Theme spacing values

    Returns:
        QSS string for grid container and cells.
    """
    if theme_spacing is None:
        theme_spacing = {}

    qss_parts = []

    # Container grid styling (Qt QSS limited for CSS Grid)
    qss_parts.append("QWidget.grid-container {")
    qss_parts.append(f"    /* {columns}-column grid simulation */")
    if gutter:
        gutter_px = theme_spacing.get(gutter, 8)
        qss_parts.append(f"    column-gap: {gutter_px}px;")
        qss_parts.append(f"    row-gap: {gutter_px}px;")
    qss_parts.append("}")

    # Cell styling
    cell_width = f"calc(100% / {columns})"
    qss_parts.append(f"QWidget.grid-cell {{ width: {cell_width}; }}")

    if gutter:
        gutter_px = theme_spacing.get(gutter, 8)
        qss_parts.append(
            f"QWidget.grid-cell {{ margin: {gutter_px / 2}px; }}"
        )  # half for shared gutters

    return "\n".join(qss_parts)


def generate_responsive_qss(breakpoints: Dict[str, Dict[str, Any]]) -> str:
    """
    Generate responsive QSS. Note: Qt QSS doesn't support media queries natively.
    This generates base QSS; responsive updates should be handled via runtime QSS regeneration.

    Args:
        breakpoints: Dict of breakpoint configs

    Returns:
        Base QSS string (responsive handled in code).
    """
    # For now, return base styles; full responsive QSS would require custom handling
    return "/* Responsive styles applied dynamically via code */"
