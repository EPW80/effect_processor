"""
Holographic 3D effect implementation
"""

import numpy as np
from .base import BaseEffect


class HolographicEffect(BaseEffect):
    """Holographic 3D effect that creates rainbow interference patterns."""

    @property
    def name(self) -> str:
        return "holographic"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply holographic 3D effect using vectorized operations."""
        self._log("Applying holographic effect...")

        height, width = image.shape[:2]
        result = image.copy().astype(np.float32)

        # Create coordinate meshgrids for vectorized operations
        x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

        # Create wave pattern using vectorized operations
        wave = (
            np.sin(
                x_coords * self.config.HOLOGRAPHIC_WAVE_X_FREQ * self.intensity
                + y_coords * self.config.HOLOGRAPHIC_WAVE_Y_FREQ * self.intensity
            )
            * self.config.HOLOGRAPHIC_WAVE_AMPLITUDE
        )

        # Add rainbow colors based on position (vectorized)
        hue_shift = (
            (x_coords + y_coords) * self.config.HOLOGRAPHIC_HUE_FREQ * self.intensity
        )

        # Apply effects to all channels simultaneously using broadcasting
        result[:, :, 0] = np.clip(result[:, :, 0] + wave * np.cos(hue_shift), 0, 255)
        result[:, :, 1] = np.clip(
            result[:, :, 1]
            + wave * np.cos(hue_shift + self.config.HOLOGRAPHIC_RGB_PHASE_SHIFT_G),
            0,
            255,
        )
        result[:, :, 2] = np.clip(
            result[:, :, 2]
            + wave * np.cos(hue_shift + self.config.HOLOGRAPHIC_RGB_PHASE_SHIFT_B),
            0,
            255,
        )

        return result.astype(np.uint8)
