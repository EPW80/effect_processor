"""
Tests for configuration management.
"""

from __future__ import annotations

import pytest

from src.config import (
    EffectConfig,
    ProcessingConfig,
    get_effect_config,
    get_processing_config,
    update_config,
)


class TestEffectConfig:
    """Tests for EffectConfig dataclass."""

    def test_default_values(self) -> None:
        """Test that default configuration values are set."""
        config = EffectConfig()

        # Chromatic Aberration
        assert config.CHROMATIC_SHIFT_BASE == 5

        # Holographic
        assert config.HOLOGRAPHIC_WAVE_X_FREQ == 0.02
        assert config.HOLOGRAPHIC_WAVE_Y_FREQ == 0.01

        # Neon
        assert config.NEON_SATURATION_BOOST == 0.5

        # Scanlines
        assert config.SCANLINES_BASE_SPACING == 4

        # VHS
        assert config.VHS_DISTORTION_BASE == 20

    def test_config_is_dataclass(self) -> None:
        """Test that EffectConfig is a dataclass."""
        config = EffectConfig()
        assert hasattr(config, "__dataclass_fields__")


class TestProcessingConfig:
    """Tests for ProcessingConfig dataclass."""

    def test_default_values(self) -> None:
        """Test that default processing configuration values are set."""
        config = ProcessingConfig()

        assert config.MIN_INTENSITY == 0.1
        assert config.MAX_INTENSITY == 5.0
        assert config.DEFAULT_INTENSITY == 1.0
        assert config.GIF_CHUNK_SIZE == 10
        assert config.VIDEO_CODEC == "mp4v"

    def test_supported_formats(self) -> None:
        """Test that supported formats are defined."""
        config = ProcessingConfig()

        assert ".mp4" in config.VIDEO_FORMATS
        assert ".avi" in config.VIDEO_FORMATS
        assert ".gif" in config.GIF_FORMATS

    def test_config_is_dataclass(self) -> None:
        """Test that ProcessingConfig is a dataclass."""
        config = ProcessingConfig()
        assert hasattr(config, "__dataclass_fields__")


class TestConfigGetters:
    """Tests for configuration getter functions."""

    def test_get_effect_config(self) -> None:
        """Test getting effect configuration."""
        config = get_effect_config()
        assert isinstance(config, EffectConfig)

    def test_get_processing_config(self) -> None:
        """Test getting processing configuration."""
        config = get_processing_config()
        assert isinstance(config, ProcessingConfig)

    def test_config_singleton_behavior(self) -> None:
        """Test that config getters return the same instance."""
        config1 = get_effect_config()
        config2 = get_effect_config()
        assert config1 is config2

        proc_config1 = get_processing_config()
        proc_config2 = get_processing_config()
        assert proc_config1 is proc_config2


class TestConfigUpdate:
    """Tests for configuration update functionality."""

    def test_update_effect_config(self) -> None:
        """Test updating effect configuration."""
        original_value = get_effect_config().CHROMATIC_SHIFT_BASE

        try:
            update_config({"CHROMATIC_SHIFT_BASE": 10})
            config = get_effect_config()
            assert config.CHROMATIC_SHIFT_BASE == 10
        finally:
            # Restore original value
            update_config({"CHROMATIC_SHIFT_BASE": original_value})

    def test_update_processing_config(self) -> None:
        """Test updating processing configuration."""
        original_value = get_processing_config().GIF_CHUNK_SIZE

        try:
            update_config({"GIF_CHUNK_SIZE": 20})
            config = get_processing_config()
            assert config.GIF_CHUNK_SIZE == 20
        finally:
            # Restore original value
            update_config({"GIF_CHUNK_SIZE": original_value})

    def test_update_multiple_values(self) -> None:
        """Test updating multiple configuration values."""
        original_chromatic = get_effect_config().CHROMATIC_SHIFT_BASE
        original_chunk_size = get_processing_config().GIF_CHUNK_SIZE

        try:
            update_config({"CHROMATIC_SHIFT_BASE": 7, "GIF_CHUNK_SIZE": 15})
            assert get_effect_config().CHROMATIC_SHIFT_BASE == 7
            assert get_processing_config().GIF_CHUNK_SIZE == 15
        finally:
            # Restore original values
            update_config(
                {
                    "CHROMATIC_SHIFT_BASE": original_chromatic,
                    "GIF_CHUNK_SIZE": original_chunk_size,
                }
            )

    def test_update_unknown_key_raises_error(self) -> None:
        """Test that updating unknown key raises ValueError."""
        with pytest.raises(ValueError, match="Unknown configuration key"):
            update_config({"UNKNOWN_KEY": 100})
