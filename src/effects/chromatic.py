"""
Chromatic aberration effect implementation
"""

import numpy as np
from .base import BaseEffect


class ChromaticAberrationEffect(BaseEffect):
    """Chromatic aberration effect that creates RGB color separation."""

    @property
    def name(self) -> str:
        return "chromatic"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply chromatic aberration effect."""
        self._log("Applying chromatic aberration...")

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
