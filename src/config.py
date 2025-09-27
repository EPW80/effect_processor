"""
Configuration management for Vaporwave Processor
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EffectConfig:
    """Configuration for individual effects."""

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


@dataclass
class ProcessingConfig:
    """Configuration for processing parameters."""

    # Intensity limits
    MIN_INTENSITY: float = 0.1
    MAX_INTENSITY: float = 5.0
    DEFAULT_INTENSITY: float = 1.0

    # GIF processing
    GIF_CHUNK_SIZE: int = 10
    GIF_DEFAULT_DURATION: float = 0.1

    # Video processing
    VIDEO_CODEC: str = "mp4v"

    # Supported formats
    VIDEO_FORMATS: tuple = (".mp4", ".avi", ".mov", ".mkv", ".wmv")
    GIF_FORMATS: tuple = (".gif",)


# Global configuration instances
EFFECT_CONFIG = EffectConfig()
PROCESSING_CONFIG = ProcessingConfig()


def get_effect_config() -> EffectConfig:
    """Get the global effect configuration."""
    return EFFECT_CONFIG


def get_processing_config() -> ProcessingConfig:
    """Get the global processing configuration."""
    return PROCESSING_CONFIG


def update_config(config_dict: Dict[str, Any]) -> None:
    """Update configuration values from a dictionary."""
    global EFFECT_CONFIG, PROCESSING_CONFIG

    for key, value in config_dict.items():
        if hasattr(EFFECT_CONFIG, key):
            setattr(EFFECT_CONFIG, key, value)
        elif hasattr(PROCESSING_CONFIG, key):
            setattr(PROCESSING_CONFIG, key, value)
        else:
            raise ValueError(f"Unknown configuration key: {key}")
