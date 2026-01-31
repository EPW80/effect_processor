"""Vaporwave Processor Package.

A Python library for applying vaporwave holographic 3D effects
to images, videos, and GIFs.

Example:
    >>> from src import VaporwaveProcessor, EffectName
    >>> processor = VaporwaveProcessor(intensity=1.5)
    >>> processor.process_media("input.jpg", "output.jpg", effects=[EffectName.NEON])
"""

from .config import (
    EffectConfig,
    ProcessingConfig,
    get_effect_config,
    get_processing_config,
    load_config_from_file,
    reset_config,
    update_config,
)
from .effects import EffectName, get_effect_class
from .exceptions import (
    ConfigurationError,
    EffectError,
    OutputWriteError,
    ProcessingError,
    UnsupportedFormatError,
    VaporwaveError,
)
from .logging_config import configure_logging, get_logger, set_log_level
from .vaporwave_processor import VaporwaveProcessor

__version__ = "1.1.0"
__author__ = "Erik Williams"
__email__ = "erikwilliams@example.com"

__all__ = [
    # Main processor
    "VaporwaveProcessor",
    # Effects
    "EffectName",
    "get_effect_class",
    # Configuration
    "EffectConfig",
    "ProcessingConfig",
    "get_effect_config",
    "get_processing_config",
    "load_config_from_file",
    "reset_config",
    "update_config",
    # Exceptions
    "ConfigurationError",
    "EffectError",
    "OutputWriteError",
    "ProcessingError",
    "UnsupportedFormatError",
    "VaporwaveError",
    # Logging
    "configure_logging",
    "get_logger",
    "set_log_level",
]
