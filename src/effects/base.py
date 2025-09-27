"""
Base class for all vaporwave effects
"""

from abc import ABC, abstractmethod
import numpy as np

try:
    from ..config import get_effect_config
except ImportError:
    from config import get_effect_config


class BaseEffect(ABC):
    """Abstract base class for all vaporwave effects."""

    def __init__(self, intensity: float = 1.0, verbose: bool = True):
        """
        Initialize the effect.

        Args:
            intensity: Effect intensity multiplier (0.1 to 5.0)
            verbose: Whether to print effect application messages
        """
        self.intensity = max(0.1, min(5.0, intensity))
        self.verbose = verbose
        self.config = get_effect_config()

    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the effect to an image.

        Args:
            image: Input image as numpy array

        Returns:
            Processed image as numpy array
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the effect."""
        pass

    def _log(self, message: str) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
