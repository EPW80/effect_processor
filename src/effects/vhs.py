"""VHS distortion effect implementation.

This module provides the VHS effect that simulates the visual artifacts
and degradation of analog video tape recordings.
"""

from __future__ import annotations

import numpy as np

from .base import BaseEffect


class VHSEffect(BaseEffect):
    """VHS effect that creates vintage video tape distortion and artifacts.

    This effect adds horizontal line distortion, noise, color bleeding,
    and contrast reduction to simulate VHS tape degradation.
    """

    @property
    def name(self) -> str:
        """Return the effect name."""
        return "vhs"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply VHS distortion effect.

        Args:
            image: Input image as numpy array (BGR format).

        Returns:
            Image with VHS-style distortion and noise.
        """
        self._log_apply()

        result = image.copy().astype(np.float32)
        height, width = result.shape[:2]

        # Add horizontal distortion lines
        distortion_intensity = int(self.config.VHS_DISTORTION_BASE * self.intensity)
        distortion_probability = (
            self.config.VHS_DISTORTION_PROBABILITY_BASE * self.intensity
        )

        for y in range(height):
            # Random chance for distortion
            if np.random.random() < distortion_probability:
                # Horizontal shift for this line
                shift = np.random.randint(-distortion_intensity, distortion_intensity)

                if shift > 0 and shift < width:
                    # Shift line right
                    result[y, shift:] = result[y, :-shift]
                    result[y, :shift] = result[y, -shift:]
                elif shift < 0 and abs(shift) < width:
                    # Shift line left
                    shift = abs(shift)
                    result[y, :-shift] = result[y, shift:]
                    result[y, -shift:] = result[y, :shift]

        # Add noise
        noise_intensity = self.config.VHS_NOISE_BASE * self.intensity
        noise = np.random.normal(0, noise_intensity, result.shape)
        result = result + noise

        # Add color shift (VHS color bleeding)
        if width > 2:
            # Slight green channel shift
            green_shift = int(self.config.VHS_GREEN_SHIFT_BASE * self.intensity)
            if green_shift > 0 and green_shift < width:
                result[:, green_shift:, 1] = result[:, :-green_shift, 1]

        # Reduce contrast slightly (VHS degradation)
        result = (
            result * self.config.VHS_CONTRAST_REDUCTION
            + self.config.VHS_BRIGHTNESS_OFFSET
        )

        return np.clip(result, 0, 255).astype(np.uint8)
