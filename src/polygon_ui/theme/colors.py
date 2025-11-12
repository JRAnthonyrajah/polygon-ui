    def validate(self) -> None:
        """Validate all colors in the palette."""
        for name, color in self._colors.items():
            # Check shades length and format (already in __post_init__, but revalidate)
            if len(color.shades) != 10:
                raise ValueError(f"Color '{name}' must have 10 shades")
            for i, shade in enumerate(color.shades):
                if not (isinstance(shade, str) and len(shade) == 7 and shade[0] == '#'):
                    raise ValueError(f"Invalid hex shade {i} for '{name}': {shade}")
        # Ensure no duplicate names
        if len(self._colors) != len(set(self._colors.keys())):
            raise ValueError("Duplicate color names detected")
