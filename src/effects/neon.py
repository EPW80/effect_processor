"""Neon glow effect implementation.

This module provides the neon glow effect that creates vibrant,
saturated colors with a glowing appearance.
"""

from __future__ import annotations

import cv2
import numpy as np

from .base import BaseEffect


class NeonGlowEffect(BaseEffect):
    """Neon glow effect that enhances saturation and adds glowing highlights.

    This effect increases color saturation and brightness, then applies
    a Gaussian blur overlay to create a "glowing" neon aesthetic.
    """

    @property
    def name(self) -> str:
        """Return the effect name."""
        return "neon"

    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply neon glow effect.

        Args:
            image: Input image as numpy array (BGR format).

        Returns:
            Image with enhanced saturation and glow effect.
        """
        self._log_apply()

        # Increase saturation and brightness
        result = image.copy().astype(np.float32)

        # Convert to HSV for easier manipulation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        # Increase saturation (vaporwave colors)
        saturation_boost = 1.0 + self.config.NEON_SATURATION_BOOST * self.intensity
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_boost, 0, 255)

        # Increase value/brightness
        brightness_boost = 1.0 + self.config.NEON_BRIGHTNESS_BOOST * self.intensity
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_boost, 0, 255)

        # Convert back to BGR
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)  # type: ignore[assignment]

        # Add glow effect using Gaussian blur
        kernel_size = self.config.NEON_GLOW_KERNEL_SIZE
        glow = cv2.GaussianBlur(
            result,
            (kernel_size, kernel_size),
            0,
        )
        glow_weight = self.config.NEON_GLOW_BASE_WEIGHT * self.intensity
        result = cv2.addWeighted(  # type: ignore[assignment]
            result, self.config.NEON_ORIGINAL_WEIGHT, glow, glow_weight, 0
        )

        return np.clip(result, 0, 255).astype(np.uint8)
