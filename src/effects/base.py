"""Base class for all vaporwave effects.

This module defines the abstract base class that all effects must inherit from,
providing a consistent interface for effect application and configuration.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from ..config import get_effect_config
from ..logging_config import get_logger

# Module-level logger
logger = get_logger(__name__)


class BaseEffect(ABC):
    """Abstract base class for all vaporwave effects.

    All effect implementations must inherit from this class and implement
    the `apply` method and `name` property.

    Attributes:
        intensity: Effect intensity multiplier (clamped to 0.1-5.0 range).
        config: The global effect configuration instance.
    """

    def __init__(self, intensity: float = 1.0) -> None:
        """Initialize the effect.

        Args:
            intensity: Effect intensity multiplier (0.1 to 5.0).
                       Values outside this range are clamped.
        """
        self.intensity = max(0.1, min(5.0, intensity))
        self.config = get_effect_config()
        logger.debug("Initialized %s with intensity=%.2f", self.name, self.intensity)

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """Apply the effect to an image.

        Args:
            image: Input image as numpy array (BGR format, uint8).

        Returns:
            Processed image as numpy array (BGR format, uint8).
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the effect.

        Returns:
            A lowercase string identifier for the effect.
        """
        pass

    def _log_apply(self) -> None:
        """Log that this effect is being applied."""
        logger.info("Applying %s effect (intensity=%.2f)", self.name, self.intensity)
