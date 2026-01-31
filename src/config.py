"""Configuration management for Vaporwave Processor.

This module provides configuration classes and utilities for managing
effect parameters, processing settings, and loading configurations from
TOML files or environment variables.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, TypeVar

# Use tomllib for Python 3.11+, fallback to tomli for older versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib  # type: ignore[import-not-found]
    except ImportError:
        tomllib = None  # type: ignore[assignment]

from .logging_config import get_logger

logger = get_logger(__name__)

# Environment variable prefix for configuration
ENV_PREFIX = "VAPORWAVE_"

# Default configuration file name
CONFIG_FILENAME = "vaporwave.toml"

T = TypeVar("T")


def _get_env_value(key: str, default: T, type_hint: type[T]) -> T:
    """Get a configuration value from environment variables.

    Args:
        key: The configuration key (will be prefixed with ENV_PREFIX).
        default: The default value if not set.
        type_hint: The expected type for conversion.

    Returns:
        The value from environment or the default.
    """
    env_key = f"{ENV_PREFIX}{key.upper()}"
    env_value = os.environ.get(env_key)

    if env_value is None:
        return default

    try:
        if type_hint is bool:
            return env_value.lower() in ("true", "1", "yes")  # type: ignore[return-value]
        elif type_hint is int:
            return int(env_value)  # type: ignore[return-value]
        elif type_hint is float:
            return float(env_value)  # type: ignore[return-value]
        elif type_hint is str:
            return env_value  # type: ignore[return-value]
        else:
            return default
    except (ValueError, TypeError):
        logger.warning(
            "Invalid environment value for %s: %s, using default",
            env_key,
            env_value,
        )
        return default


@dataclass
class EffectConfig:
    """Configuration for individual effects.

    These parameters control the intensity and behavior of each visual effect.
    Values can be overridden via environment variables with the VAPORWAVE_ prefix.

    Example:
        Set VAPORWAVE_CHROMATIC_SHIFT_BASE=10 to double the chromatic shift.
    """

    # Chromatic Aberration
    CHROMATIC_SHIFT_BASE: int = 5

    # Holographic Effect
    HOLOGRAPHIC_WAVE_X_FREQ: float = 0.02
    HOLOGRAPHIC_WAVE_Y_FREQ: float = 0.01
    HOLOGRAPHIC_WAVE_AMPLITUDE: float = 30
    HOLOGRAPHIC_HUE_FREQ: float = 0.005
    HOLOGRAPHIC_RGB_PHASE_SHIFT_G: float = 2.09
    HOLOGRAPHIC_RGB_PHASE_SHIFT_B: float = 4.19

    # Neon Glow
    NEON_SATURATION_BOOST: float = 0.5
    NEON_BRIGHTNESS_BOOST: float = 0.3
    NEON_GLOW_KERNEL_SIZE: int = 21
    NEON_ORIGINAL_WEIGHT: float = 0.7
    NEON_GLOW_BASE_WEIGHT: float = 0.3

    # Scanlines
    SCANLINES_BASE_SPACING: int = 4
    SCANLINES_MIN_SPACING: int = 2
    SCANLINES_DARKNESS: float = 0.7

    # VHS Effect
    VHS_DISTORTION_BASE: int = 20
    VHS_DISTORTION_PROBABILITY_BASE: float = 0.1
    VHS_NOISE_BASE: float = 10
    VHS_GREEN_SHIFT_BASE: int = 2
    VHS_CONTRAST_REDUCTION: float = 0.9
    VHS_BRIGHTNESS_OFFSET: float = 25

    def __post_init__(self) -> None:
        """Load values from environment variables after initialization."""
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Override values from environment variables."""
        for f in fields(self):
            env_value = _get_env_value(f.name, getattr(self, f.name), f.type)
            setattr(self, f.name, env_value)


@dataclass
class ProcessingConfig:
    """Configuration for processing parameters.

    These parameters control file processing behavior, supported formats,
    and resource management settings.
    """

    # Intensity limits
    MIN_INTENSITY: float = 0.1
    MAX_INTENSITY: float = 5.0
    DEFAULT_INTENSITY: float = 1.0

    # GIF processing
    GIF_CHUNK_SIZE: int = 10
    GIF_DEFAULT_DURATION: float = 0.1

    # Video processing
    VIDEO_CODEC: str = "mp4v"

    # Supported formats (as tuples for immutability)
    VIDEO_FORMATS: tuple[str, ...] = (".mp4", ".avi", ".mov", ".mkv", ".wmv")
    GIF_FORMATS: tuple[str, ...] = (".gif",)
    IMAGE_FORMATS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

    def __post_init__(self) -> None:
        """Load values from environment variables after initialization."""
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Override values from environment variables."""
        for f in fields(self):
            # Skip tuple fields (formats) as they can't easily be set via env
            if f.type in (tuple, "tuple[str, ...]"):
                continue
            env_value = _get_env_value(f.name, getattr(self, f.name), f.type)
            setattr(self, f.name, env_value)


# Global configuration instances
_effect_config: EffectConfig | None = None
_processing_config: ProcessingConfig | None = None


def get_effect_config() -> EffectConfig:
    """Get the global effect configuration.

    Returns:
        The singleton EffectConfig instance.
    """
    global _effect_config
    if _effect_config is None:
        _effect_config = EffectConfig()
    return _effect_config


def get_processing_config() -> ProcessingConfig:
    """Get the global processing configuration.

    Returns:
        The singleton ProcessingConfig instance.
    """
    global _processing_config
    if _processing_config is None:
        _processing_config = ProcessingConfig()
    return _processing_config


def load_config_from_file(config_path: Path | str | None = None) -> bool:
    """Load configuration from a TOML file.

    Args:
        config_path: Path to the TOML config file. If None, searches for
                     'vaporwave.toml' in the current directory and user home.

    Returns:
        True if configuration was loaded, False otherwise.

    Example:
        >>> load_config_from_file("my_config.toml")
        >>> # Or auto-discover:
        >>> load_config_from_file()
    """
    global _effect_config, _processing_config

    if tomllib is None:
        logger.warning("TOML support not available. Install 'tomli' for Python < 3.11")
        return False

    # Find config file
    if config_path is None:
        search_paths = [
            Path.cwd() / CONFIG_FILENAME,
            Path.home() / f".{CONFIG_FILENAME}",
            Path.home() / ".config" / "vaporwave" / CONFIG_FILENAME,
        ]
        config_path = next((p for p in search_paths if p.exists()), None)
        if config_path is None:
            logger.debug("No configuration file found")
            return False
    else:
        config_path = Path(config_path)
        if not config_path.exists():
            logger.warning("Configuration file not found: %s", config_path)
            return False

    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)

        logger.info("Loading configuration from %s", config_path)

        # Update effect config
        if "effects" in config_data:
            update_config(config_data["effects"])

        # Update processing config
        if "processing" in config_data:
            update_config(config_data["processing"])

        return True

    except Exception as e:
        logger.error("Failed to load configuration from %s: %s", config_path, e)
        return False


def update_config(config_dict: dict[str, Any]) -> None:
    """Update configuration values from a dictionary.

    Args:
        config_dict: Dictionary of configuration key-value pairs.

    Raises:
        ValueError: If an unknown configuration key is provided.

    Example:
        >>> update_config({"CHROMATIC_SHIFT_BASE": 10, "MIN_INTENSITY": 0.5})
    """
    effect_config = get_effect_config()
    processing_config = get_processing_config()

    for key, value in config_dict.items():
        key_upper = key.upper()
        if hasattr(effect_config, key_upper):
            setattr(effect_config, key_upper, value)
            logger.debug("Updated effect config: %s = %s", key_upper, value)
        elif hasattr(processing_config, key_upper):
            setattr(processing_config, key_upper, value)
            logger.debug("Updated processing config: %s = %s", key_upper, value)
        else:
            raise ValueError(f"Unknown configuration key: {key}")


def reset_config() -> None:
    """Reset configuration to default values.

    This clears the singleton instances, causing them to be recreated
    with default values on next access.
    """
    global _effect_config, _processing_config
    _effect_config = None
    _processing_config = None
    logger.debug("Configuration reset to defaults")
