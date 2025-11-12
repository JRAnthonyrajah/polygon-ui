from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .colors import Colors


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def linearize_rgb(rgb: Tuple[float, float, float]) -> List[float]:
    """Convert sRGB to linear RGB."""
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]


def relative_luminance(hex_color: str) -> float:
    """Calculate relative luminance of a color."""
    rgb = [c / 255.0 for c in hex_to_rgb(hex_color)]
    linear_rgb = linearize_rgb(rgb)
    return 0.2126 * linear_rgb[0] + 0.7152 * linear_rgb[1] + 0.0722 * linear_rgb[2]


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two colors per WCAG."""
    l1 = relative_luminance(color1)
    l2 = relative_luminance(color2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


class DesignTokenValidator:
    """Validator for design tokens ensuring WCAG AA compliance."""

    MIN_CONTRAST_NORMAL = 4.5
    MIN_CONTRAST_LARGE = 3.0

    def __init__(self, colors_instance: "Colors"):
        self.colors = colors_instance

    def validate_color_contrasts(self) -> List[str]:
        """Validate contrast ratios for common color combinations.

        Checks:
        - Each shade as text on white background
        - Each shade as text on black background
        - Typical foreground/background pairs within color families
        """
        issues = []

        # Standard backgrounds
        white = "#ffffff"
        black = "#000000"

        for name, color_shades in self.colors._colors.items():
            # Check each shade on white (light mode)
            for i, shade in enumerate(color_shades.shades):
                ratio = contrast_ratio(shade, white)
                if ratio < self.MIN_CONTRAST_NORMAL:
                    issues.append(
                        f"Low contrast for {name} shade {i+1} ({shade}) on white: {ratio:.2f}:1"
                    )

            # Check each shade on black (dark mode)
            for i, shade in enumerate(color_shades.shades):
                ratio = contrast_ratio(
                    black, shade
                )  # black text on shade bg, or vice versa?
                # Typically, for dark shades, check light text on dark bg
                # But for simplicity, check shade as bg with black text if light, but better to check typical
                # Assuming shades[0] light to shades[9] dark
                # For light shades (0-4), check black text on shade bg
                if i < 5:
                    ratio_bg = contrast_ratio(black, shade)
                    if ratio_bg < self.MIN_CONTRAST_NORMAL:
                        issues.append(
                            f"Low contrast black text on {name} light shade {i+1} ({shade}): {ratio_bg:.2f}:1"
                        )
                # For dark shades (5-9), check white text on shade bg
                else:
                    ratio_bg = contrast_ratio(white, shade)
                    if ratio_bg < self.MIN_CONTRAST_NORMAL:
                        issues.append(
                            f"Low contrast white text on {name} dark shade {i+1} ({shade}): {ratio_bg:.2f}:1"
                        )

            # Check intra-family contrast, e.g., adjacent shades for borders etc.
            for i in range(len(color_shades.shades) - 1):
                ratio_adj = contrast_ratio(
                    color_shades.shades[i], color_shades.shades[i + 1]
                )
                if ratio_adj < self.MIN_CONTRAST_LARGE:  # Large for subtle differences
                    issues.append(
                        f"Low adjacent contrast in {name} shades {i+1}-{i+2}: {ratio_adj:.2f}:1"
                    )

        # Check semantic pairs, e.g., primary color on backgrounds
        primary = self.colors._colors["blue"].shades[5]  # 500 shade typical primary
        for bg_name in ["gray", "red", "green"]:
            bg_shade = self.colors._colors[bg_name].shades[1]  # light bg
            ratio = contrast_ratio(primary, bg_shade)
            if ratio < self.MIN_CONTRAST_NORMAL:
                issues.append(
                    f"Primary blue on {bg_name} light bg low contrast: {ratio:.2f}:1"
                )

        return issues

    def validate(self) -> bool:
        """Run full validation and raise if issues found."""
        issues = self.validate_color_contrasts()
        if issues:
            raise ValueError(
                f"WCAG AA compliance issues in design tokens:\n" + "\n".join(issues)
            )
        return True


# Example usage: After creating Colors instance
# colors_obj = colors.Colors()
# validator = DesignTokenValidator(colors_obj)
# validator.validate()
