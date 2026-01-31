"""Scanlines effect implementation.

This module provides the scanlines effect that simulates the horizontal
lines visible on CRT monitors and old televisions.
"""

from __future__ import annotations

import numpy as np

from .base import BaseEffect


class ScanlinesEffect(BaseEffect):
    """Scanlines effect that creates retro CRT monitor-style horizontal lines.

    This effect darkens alternating horizontal lines to simulate the
    appearance of a CRT monitor or old television screen.
    """

    @property
    def name(self) -> str:
        """Return the effect name."""
        return "scanlines"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply retro scanlines effect.

        Args:
            image: Input image as numpy array (BGR format).

        Returns:
            Image with horizontal scanlines overlay.
        """
        self._log_apply()

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
