"""
Scanlines effect implementation
"""

import numpy as np
from .base import BaseEffect


class ScanlinesEffect(BaseEffect):
    """Scanlines effect that creates retro CRT monitor-style horizontal lines."""

    @property
    def name(self) -> str:
        return "scanlines"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply retro scanlines effect."""
        self._log("Applying scanlines...")

        result = image.copy()
        height, _ = result.shape[:2]

        # Create scanlines every few pixels based on intensity
        scanline_spacing = max(
            self.config.SCANLINES_MIN_SPACING,
            int(self.config.SCANLINES_BASE_SPACING / self.intensity),
        )

        for y in range(0, height, scanline_spacing):
            # Darken every nth line
            if y < height:
                result[y, :] = (result[y, :] * self.config.SCANLINES_DARKNESS).astype(
                    np.uint8
                )

        return result
