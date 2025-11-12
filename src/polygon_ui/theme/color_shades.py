"""Color shades utility for managing color palettes."""

from typing import List


class ColorShades:
    """Represents a collection of 10 color shades from lightest to darkest."""

    def __init__(self, shades: List[str]) -> None:
        """Initialize color shades with validation.

        Args:
            shades: List of 10 hex color codes from lightest to darkest

        Raises:
            ValueError: If shades are not valid hex colors or wrong count
        """
        if len(shades) != 10:
            raise ValueError(
                f"ColorShades must have exactly 10 shades, got {len(shades)}"
            )

        validated_shades = []
        for i, shade in enumerate(shades):
            if not (
                isinstance(shade, str) and len(shade) == 7 and shade.startswith("#")
            ):
                raise ValueError(f"Invalid hex shade at index {i}: {shade}")
            validated_shades.append(shade)

        self.shades = validated_shades

    def __getitem__(self, index: int) -> str:
        """Get shade by index."""
        return self.shades[index]

    def __len__(self) -> int:
        """Get number of shades."""
        return len(self.shades)

    def __iter__(self):
        """Iterate over shades."""
        return iter(self.shades)

    def __repr__(self) -> str:
        """String representation."""
        return f"ColorShades({self.shades})"
