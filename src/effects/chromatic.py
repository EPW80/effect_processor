"""Chromatic aberration effect implementation.

This module provides the chromatic aberration effect that simulates
the color fringing seen in old camera lenses.
"""

from __future__ import annotations

import numpy as np

from .base import BaseEffect


class ChromaticAberrationEffect(BaseEffect):
    """Chromatic aberration effect that creates RGB color separation.

    This effect shifts the red and blue color channels in opposite directions,
    creating the distinctive "color fringing" associated with cheap optics.
    """

    @property
    def name(self) -> str:
        """Return the effect name."""
        return "chromatic"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply chromatic aberration effect.

        Args:
            image: Input image as numpy array (BGR format).

        Returns:
            Image with RGB channels shifted to create color separation.
        """
        self._log_apply()

        # Get image dimensions
        _, width = image.shape[:2]

        # Calculate shift amount based on intensity and config
        shift = int(self.config.CHROMATIC_SHIFT_BASE * self.intensity)

        # Create shifted versions for each color channel
        result = image.copy()

        # Red channel - shift right
        if shift < width:
            result[:, shift:, 2] = image[:, :-shift, 2]
            result[:, :shift, 2] = image[:, -shift:, 2]

        # Blue channel - shift left
        if shift < width:
            result[:, :-shift, 0] = image[:, shift:, 0]
            result[:, -shift:, 0] = image[:, :shift, 0]

        return result
