"""
Unit tests for individual vaporwave effects.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.effects import (
    ChromaticAberrationEffect,
    HolographicEffect,
    NeonGlowEffect,
    ScanlinesEffect,
    VHSEffect,
)


class TestChromaticAberrationEffect:
    """Tests for chromatic aberration effect."""

    def test_initialization(self) -> None:
        """Test effect initialization."""
        effect = ChromaticAberrationEffect(intensity=1.0)
        assert effect.intensity == 1.0
        assert effect.name == "chromatic"

    def test_intensity_clamping(self) -> None:
        """Test that intensity is clamped to valid range."""
        effect_low = ChromaticAberrationEffect(intensity=0.01)
        assert effect_low.intensity == 0.1

        effect_high = ChromaticAberrationEffect(intensity=10.0)
        assert effect_high.intensity == 5.0

    def test_apply_basic(self, sample_image: np.ndarray) -> None:
        """Test basic application of chromatic aberration."""
        effect = ChromaticAberrationEffect(intensity=1.0)
        result = effect.apply(sample_image)

        # Result should have same shape
        assert result.shape == sample_image.shape

        # Result should be different from original
        assert not np.array_equal(result, sample_image)

        # Channels should be shifted
        # Red channel should differ from original
        assert not np.array_equal(result[:, :, 2], sample_image[:, :, 2])

    def test_apply_different_intensities(self, sample_image: np.ndarray) -> None:
        """Test that different intensities produce different results."""
        effect_low = ChromaticAberrationEffect(intensity=0.5)
        effect_high = ChromaticAberrationEffect(intensity=2.0)

        result_low = effect_low.apply(sample_image)
        result_high = effect_high.apply(sample_image)

        # Different intensities should produce different results
        assert not np.array_equal(result_low, result_high)

    def test_dtype_preservation(self, sample_image: np.ndarray) -> None:
        """Test that output dtype matches input."""
        effect = ChromaticAberrationEffect(intensity=1.0)
        result = effect.apply(sample_image)
        assert result.dtype == sample_image.dtype


class TestHolographicEffect:
    """Tests for holographic effect."""

    def test_initialization(self) -> None:
        """Test effect initialization."""
        effect = HolographicEffect(intensity=1.0)
        assert effect.intensity == 1.0
        assert effect.name == "holographic"

    def test_apply_basic(self, sample_image: np.ndarray) -> None:
        """Test basic application of holographic effect."""
        effect = HolographicEffect(intensity=1.0)
        result = effect.apply(sample_image)

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_apply_creates_rainbow_colors(self, solid_color_image: np.ndarray) -> None:
        """Test that holographic effect creates color variation."""
        effect = HolographicEffect(intensity=1.5)
        result = effect.apply(solid_color_image)

        # Should have more color variation than solid input
        original_variance = np.var(solid_color_image)
        result_variance = np.var(result)
        assert result_variance > original_variance


class TestNeonGlowEffect:
    """Tests for neon glow effect."""

    def test_initialization(self) -> None:
        """Test effect initialization."""
        effect = NeonGlowEffect(intensity=1.0)
        assert effect.intensity == 1.0
        assert effect.name == "neon"

    def test_apply_basic(self, sample_image: np.ndarray) -> None:
        """Test basic application of neon glow effect."""
        effect = NeonGlowEffect(intensity=1.0)
        result = effect.apply(sample_image)

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_brightness_increase(self, sample_image: np.ndarray) -> None:
        """Test that neon effect increases brightness."""
        effect = NeonGlowEffect(intensity=1.0)
        result = effect.apply(sample_image)

        # Average brightness should increase
        original_brightness = np.mean(sample_image)
        result_brightness = np.mean(result)
        assert result_brightness >= original_brightness


class TestScanlinesEffect:
    """Tests for scanlines effect."""

    def test_initialization(self) -> None:
        """Test effect initialization."""
        effect = ScanlinesEffect(intensity=1.0)
        assert effect.intensity == 1.0
        assert effect.name == "scanlines"

    def test_apply_basic(self, sample_image: np.ndarray) -> None:
        """Test basic application of scanlines effect."""
        effect = ScanlinesEffect(intensity=1.0)
        result = effect.apply(sample_image)

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_darkened_lines(self, sample_image: np.ndarray) -> None:
        """Test that scanlines create darker horizontal lines."""
        effect = ScanlinesEffect(intensity=1.0)
        result = effect.apply(sample_image)

        # Check that some rows are darker than others
        row_brightness = [np.mean(result[i, :]) for i in range(result.shape[0])]
        # Should have variation in row brightness
        assert np.std(row_brightness) > 0


class TestVHSEffect:
    """Tests for VHS effect."""

    def test_initialization(self) -> None:
        """Test effect initialization."""
        effect = VHSEffect(intensity=1.0)
        assert effect.intensity == 1.0
        assert effect.name == "vhs"

    def test_apply_basic(self, sample_image: np.ndarray) -> None:
        """Test basic application of VHS effect."""
        effect = VHSEffect(intensity=1.0)
        result = effect.apply(sample_image)

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_apply_adds_distortion(self, solid_color_image: np.ndarray) -> None:
        """Test that VHS effect adds visual distortion."""
        effect = VHSEffect(intensity=1.5)
        result = effect.apply(solid_color_image)

        # Result should be different from original due to distortion
        assert not np.array_equal(result, solid_color_image)


class TestEffectCommonBehavior:
    """Tests for common behavior across all effects."""

    @pytest.mark.parametrize(
        "effect_class",
        [
            ChromaticAberrationEffect,
            HolographicEffect,
            NeonGlowEffect,
            ScanlinesEffect,
            VHSEffect,
        ],
    )
    def test_all_effects_preserve_shape(
        self, effect_class: type, sample_image: np.ndarray
    ) -> None:
        """Test that all effects preserve image dimensions."""
        effect = effect_class(intensity=1.0)
        result = effect.apply(sample_image)
        assert result.shape == sample_image.shape

    @pytest.mark.parametrize(
        "effect_class",
        [
            ChromaticAberrationEffect,
            HolographicEffect,
            NeonGlowEffect,
            ScanlinesEffect,
            VHSEffect,
        ],
    )
    def test_all_effects_have_name(self, effect_class: type) -> None:
        """Test that all effects have a name property."""
        effect = effect_class(intensity=1.0)
        assert isinstance(effect.name, str)
        assert len(effect.name) > 0

    @pytest.mark.parametrize(
        "effect_class",
        [
            ChromaticAberrationEffect,
            HolographicEffect,
            NeonGlowEffect,
            ScanlinesEffect,
            VHSEffect,
        ],
    )
    def test_all_effects_accept_intensity(self, effect_class: type) -> None:
        """Test that all effects accept intensity parameter."""
        effect = effect_class(intensity=1.5)
        assert effect.intensity == 1.5
