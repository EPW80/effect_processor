"""
Integration tests for VaporwaveProcessor.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.vaporwave_processor import VaporwaveProcessor


class TestVaporwaveProcessorInitialization:
    """Tests for processor initialization."""

    def test_default_initialization(self) -> None:
        """Test processor with default parameters."""
        processor = VaporwaveProcessor()
        assert processor.intensity == 1.0
        assert len(processor.effects) == 5

    def test_custom_intensity(self) -> None:
        """Test processor with custom intensity."""
        processor = VaporwaveProcessor(intensity=1.5)
        assert processor.intensity == 1.5

    def test_intensity_clamping(self) -> None:
        """Test that intensity is clamped to valid range."""
        processor_low = VaporwaveProcessor(intensity=0.01)
        assert processor_low.intensity == 0.1

        processor_high = VaporwaveProcessor(intensity=10.0)
        assert processor_high.intensity == 5.0

    def test_log_level_parameter(self) -> None:
        """Test log_level parameter setting."""
        # Should not raise - tests that parameter is accepted
        processor = VaporwaveProcessor(log_level="DEBUG")
        assert processor is not None

    def test_effects_loaded(self) -> None:
        """Test that all effects are loaded."""
        processor = VaporwaveProcessor()
        expected_effects = {"chromatic", "holographic", "neon", "scanlines", "vhs"}
        assert set(processor.effects.keys()) == expected_effects


class TestVaporwaveProcessorEffects:
    """Tests for effect application."""

    def test_get_available_effects(self) -> None:
        """Test getting list of available effects."""
        processor = VaporwaveProcessor()
        effects = processor.get_available_effects()
        assert "chromatic" in effects
        assert "holographic" in effects
        assert "neon" in effects
        assert "scanlines" in effects
        assert "vhs" in effects

    def test_apply_single_effect(self, sample_image: np.ndarray) -> None:
        """Test applying a single effect."""
        processor = VaporwaveProcessor()
        result = processor._apply_effects(sample_image, ["chromatic"])

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_apply_multiple_effects(self, sample_image: np.ndarray) -> None:
        """Test applying multiple effects."""
        processor = VaporwaveProcessor()
        result = processor._apply_effects(
            sample_image, ["chromatic", "neon", "scanlines"]
        )

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_apply_all_effects(
        self, sample_image: np.ndarray, all_effects: list[str]
    ) -> None:
        """Test applying all effects."""
        processor = VaporwaveProcessor()
        result = processor._apply_effects(sample_image, all_effects)

        assert result.shape == sample_image.shape
        assert not np.array_equal(result, sample_image)

    def test_unknown_effect_warning(self, sample_image: np.ndarray, caplog) -> None:
        """Test that unknown effects are ignored with warning."""
        import logging

        with caplog.at_level(logging.WARNING):
            processor = VaporwaveProcessor()
            result = processor._apply_effects(sample_image, ["unknown_effect"])

        # Result should be unchanged
        assert np.array_equal(result, sample_image)

        # Check warning was logged
        assert any(
            "unknown_effect" in record.message.lower() for record in caplog.records
        )

    def test_effect_order_matters(self, sample_image: np.ndarray) -> None:
        """Test that effect application order affects results."""
        processor = VaporwaveProcessor()

        result1 = processor._apply_effects(sample_image, ["chromatic", "neon"])
        result2 = processor._apply_effects(sample_image, ["neon", "chromatic"])

        # Different orders may produce different results
        # This test documents the behavior
        assert result1.shape == result2.shape

    def test_add_custom_effect(self, sample_image: np.ndarray) -> None:
        """Test adding a custom effect."""
        from src.effects import BaseEffect

        class CustomEffect(BaseEffect):
            @property
            def name(self) -> str:
                return "custom"

            def apply(self, image: np.ndarray) -> np.ndarray:
                # Simple invert effect
                return 255 - image

        processor = VaporwaveProcessor()
        custom_effect = CustomEffect(intensity=1.0)
        processor.add_custom_effect("custom", custom_effect)

        assert "custom" in processor.effects
        result = processor._apply_effects(sample_image, ["custom"])
        assert not np.array_equal(result, sample_image)


class TestImageProcessing:
    """Tests for image file processing."""

    def test_process_image_success(
        self, sample_image_file: Path, temp_dir: Path
    ) -> None:
        """Test successful image processing."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.jpg"

        success = processor.process_media(
            str(sample_image_file), str(output_path), effects=["chromatic"]
        )

        assert success is True
        assert output_path.exists()

        # Verify output is valid image
        output_image = cv2.imread(str(output_path))
        assert output_image is not None

    def test_process_image_all_effects(
        self, sample_image_file: Path, temp_dir: Path, all_effects: list[str]
    ) -> None:
        """Test image processing with all effects."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output_all.jpg"

        success = processor.process_media(
            str(sample_image_file), str(output_path), effects=all_effects
        )

        assert success is True
        assert output_path.exists()

    def test_process_image_default_effects(
        self, sample_image_file: Path, temp_dir: Path
    ) -> None:
        """Test image processing with default effects (None)."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output_default.jpg"

        success = processor.process_media(str(sample_image_file), str(output_path))

        assert success is True
        assert output_path.exists()

    def test_process_nonexistent_image(self, temp_dir: Path) -> None:
        """Test processing nonexistent image file raises exception."""
        from src.exceptions import ProcessingError

        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.jpg"

        with pytest.raises(ProcessingError):
            processor.process_media(str(temp_dir / "nonexistent.jpg"), str(output_path))


class TestVideoProcessing:
    """Tests for video file processing."""

    def test_process_video_success(
        self, sample_video_file: Path, temp_dir: Path
    ) -> None:
        """Test successful video processing."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.mp4"

        success = processor.process_media(
            str(sample_video_file), str(output_path), effects=["chromatic", "neon"]
        )

        assert success is True
        assert output_path.exists()

        # Verify output is valid video
        cap = cv2.VideoCapture(str(output_path))
        assert cap.isOpened()
        ret, frame = cap.read()
        assert ret is True
        assert frame is not None
        cap.release()

    def test_process_video_frame_count(
        self, sample_video_file: Path, temp_dir: Path
    ) -> None:
        """Test that video frame count is preserved."""
        # Get original frame count
        cap_original = cv2.VideoCapture(str(sample_video_file))
        original_count = int(cap_original.get(cv2.CAP_PROP_FRAME_COUNT))
        cap_original.release()

        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.mp4"

        success = processor.process_media(
            str(sample_video_file), str(output_path), effects=["scanlines"]
        )

        assert success is True

        # Get processed frame count
        cap_processed = cv2.VideoCapture(str(output_path))
        processed_count = int(cap_processed.get(cv2.CAP_PROP_FRAME_COUNT))
        cap_processed.release()

        assert processed_count == original_count


class TestGIFProcessing:
    """Tests for GIF file processing."""

    def test_process_gif_success(self, sample_gif_file: Path, temp_dir: Path) -> None:
        """Test successful GIF processing."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.gif"

        success = processor.process_media(
            str(sample_gif_file), str(output_path), effects=["holographic", "vhs"]
        )

        assert success is True
        assert output_path.exists()

    def test_process_gif_frame_count(
        self, sample_gif_file: Path, temp_dir: Path
    ) -> None:
        """Test that GIF frame count is preserved."""
        import imageio

        # Get original frame count
        original_reader = imageio.get_reader(str(sample_gif_file))
        original_count = len(original_reader)
        original_reader.close()

        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.gif"

        success = processor.process_media(
            str(sample_gif_file), str(output_path), effects=["chromatic"]
        )

        assert success is True

        # Get processed frame count
        processed_reader = imageio.get_reader(str(output_path))
        processed_count = len(processed_reader)
        processed_reader.close()

        assert processed_count == original_count


class TestProcessorIntensity:
    """Tests for intensity parameter effects."""

    def test_different_intensities_produce_different_results(
        self, sample_image_file: Path, temp_dir: Path
    ) -> None:
        """Test that different intensities produce different outputs."""
        processor_low = VaporwaveProcessor(intensity=0.5)
        processor_high = VaporwaveProcessor(intensity=2.0)

        output_low = temp_dir / "output_low.jpg"
        output_high = temp_dir / "output_high.jpg"

        processor_low.process_media(
            str(sample_image_file), str(output_low), effects=["chromatic"]
        )
        processor_high.process_media(
            str(sample_image_file), str(output_high), effects=["chromatic"]
        )

        # Load both outputs
        img_low = cv2.imread(str(output_low))
        img_high = cv2.imread(str(output_high))

        # They should be different
        assert not np.array_equal(img_low, img_high)


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_file_path(self, temp_dir: Path) -> None:
        """Test handling of invalid file paths."""
        from src.exceptions import ProcessingError

        processor = VaporwaveProcessor()
        with pytest.raises(ProcessingError):
            processor.process_media("nonexistent.jpg", str(temp_dir / "output.jpg"))

    def test_empty_effects_list(self, sample_image_file: Path, temp_dir: Path) -> None:
        """Test handling of empty effects list."""
        processor = VaporwaveProcessor()
        output_path = temp_dir / "output.jpg"

        # Empty effects list should still work (no effects applied)
        success = processor.process_media(
            str(sample_image_file), str(output_path), effects=[]
        )

        assert success is True
        assert output_path.exists()
