from .color_shades import ColorShades

class Colors:
    def __init__(self) -> None:
        self._colors = {
            # Gray
            'gray': ColorShades([
                '#f9fafb', '#f3f4f6', '#e5e7eb', '#d1d5db', '#9ca3af',
                '#6b7280', '#4b5563', '#374151', '#1f2937', '#111827'
            ]),
            # Red
            'red': ColorShades([
                '#fef2f2', '#fee2e2', '#fecaca', '#fca5a5', '#f87171',
                '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'
            ]),
            # Green
            'green': ColorShades([
                '#f0fdf4', '#dcfce7', '#bbf7d0', '#86efac', '#4ade80',
                '#22c55e', '#16a34a', '#15803d', '#166534', '#14532d'
            ]),
            # Blue
            'blue': ColorShades([
                '#eff6ff', '#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa',
                '#3b82f6', '#2563eb', '#1d4ed8', '#1e40af', '#1e3a8a'
            ]),
            # Yellow
            'yellow': ColorShades([
                '#fefce8', '#fef3c7', '#fde68a', '#fcd34d', '#fbbf24',
                '#f59e0b', '#d97706', '#b45309', '#92400e', '#78350f'
            ]),
            # Purple
            'purple': ColorShades([
                '#faf5ff', '#f3e8ff', '#e9d5ff', '#d8b4fe', '#c084fc',
                '#a855f7', '#9333ea', '#7e22ce', '#6b21a8', '#581c87'
            ]),
            # Orange
            'orange': ColorShades([
                '#fff7ed', '#ffedd5', '#fed7aa', '#fdba74', '#fb923c',
                '#f97316', '#ea580c', '#c2410c', '#9a3412', '#7c2d12'
            ]),
            # Pink
            'pink': ColorShades([
                '#fdf2f8', '#fce7f3', '#fbcfe8', '#f9a8d4', '#f472b6',
                '#ec4899', '#db2777', '#be185d', '#9d174d', '#831843'
            ]),
            # Indigo
            'indigo': ColorShades([
                '#eef2ff', '#e0e7ff', '#c7d2fe', '#a5b4fc', '#818cf8',
                '#6366f1', '#4f46e5', '#4338ca', '#3730a3', '#312e81'
            ]),
            # Teal
            'teal': ColorShades([
                '#f0fdfa', '#ccfbf1', '#99f6e4', '#5eead4', '#2dd4bf',
                '#14b8a6', '#0d9488', '#0f766e', '#115e59', '#134e4a'
            ]),
            # Cyan
            'cyan': ColorShades([
                '#ecfeff', '#cffafe', '#a5f3fc', '#67e8f9', '#22d3ee',
                '#06b6d4', '#0891b2', '#0e7490', '#155e75', '#164e63'
            ]),
            # Lime
            'lime': ColorShades([
                '#f7fee7', '#ecfccb', '#d9f99d', '#bef264', '#a3e635',
                '#84cc16', '#65a30d', '#4d7c0f', '#365314', '#1a531f'
            ]),
            # Amber
            'amber': ColorShades([
                '#fffbeb', '#fef3c7', '#fde68a', '#fcd34d', '#fbbf24',
                '#f59e0b', '#d97706', '#b45309', '#92400e', '#78350f'
            ]),
            # Rose
            'rose': ColorShades([
                '#fff1f2', '#ffe4e6', '#fecdd3', '#fda4af', '#fb7185',
                '#f43f5e', '#e11d48', '#be123c', '#9f1239', '#881337'
            ]),
        }
        self.validate()

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
