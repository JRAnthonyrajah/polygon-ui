    def validate(self) -> None:
        """Validate theme design tokens."""
        # Validate colors
        self.colors.validate()

        # Validate radius
        for size, value in self.radius.items():
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"Radius '{size}' must be non-negative int: {value}")

        # Validate shadows (basic string check)
        for size, shadow in self.shadows.items():
            if not isinstance(shadow, str) or 'rgba' not in shadow and 'rgb' not in shadow:
                raise ValueError(f"Shadow '{size}' must be valid CSS shadow: {shadow}")

        # Validate breakpoints
        for size, value in self.breakpoints.items():
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"Breakpoint '{size}' must be positive int: {value}")

        # Validate spacing and typography via their methods if available
        if hasattr(self.spacing, 'validate'):
            self.spacing.validate()
        if hasattr(self.typography, 'validate'):
            self.typography.validate()
