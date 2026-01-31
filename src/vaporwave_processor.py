"""Vaporwave Processor - A library for applying vaporwave holographic 3D effects.

This module provides the main VaporwaveProcessor class for applying various
retro-style visual effects to images, videos, and GIFs.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import cv2
import imageio
import numpy as np
from tqdm import tqdm

from .config import get_processing_config
from .effects import (
    BaseEffect,
    EffectName,
    get_effect_class,
)
from .exceptions import (
    ProcessingError,
    UnsupportedFormatError,
)
from .logging_config import configure_logging, get_logger

if TYPE_CHECKING:
    from .config import ProcessingConfig

# Module-level logger
logger = get_logger(__name__)


class VaporwaveProcessor:
    """Main class for applying vaporwave effects to images and videos.

    This processor supports images, videos, and GIFs, applying various
    retro-style effects like chromatic aberration, VHS distortion, and more.

    Attributes:
        intensity: The effect intensity multiplier (0.1 to 5.0).
        effects: Dictionary mapping effect names to effect instances.
        config: The processing configuration.

    Example:
        >>> processor = VaporwaveProcessor(intensity=1.5)
        >>> processor.process_media("input.jpg", "output.jpg")
        >>> processor.process_media("video.mp4", "output.mp4", effects=["neon", "vhs"])
    """

    def __init__(
        self,
        intensity: float = 1.0,
        verbose: bool = False,
        log_level: str = "INFO",
    ) -> None:
        """Initialize the VaporwaveProcessor.

        Args:
            intensity: Effect intensity multiplier (0.1 to 5.0).
            verbose: If True, enables DEBUG level logging.
            log_level: The log level to use (DEBUG, INFO, WARNING, ERROR).
        """
        # Configure logging based on verbosity
        if verbose:
            configure_logging(level="DEBUG", verbose=True)
        else:
            configure_logging(level=log_level)  # type: ignore[arg-type]

        self.config: ProcessingConfig = get_processing_config()
        self.intensity = max(
            self.config.MIN_INTENSITY, min(self.config.MAX_INTENSITY, intensity)
        )

        # Initialize effect instances using the registry
        self.effects: dict[str, BaseEffect] = {
            name.value: get_effect_class(name)(self.intensity) for name in EffectName
        }

        logger.debug(
            "Initialized VaporwaveProcessor with intensity=%.2f, effects=%s",
            self.intensity,
            list(self.effects.keys()),
        )

    def process_media(
        self,
        input_path: str | Path,
        output_path: str | Path,
        effects: list[str | EffectName] | None = None,
    ) -> bool:
        """Process media file with vaporwave effects.

        Args:
            input_path: Path to input media file.
            output_path: Path to save processed media.
            effects: List of effects to apply. If None, applies all effects.
                    Available: 'chromatic', 'holographic', 'neon',
                    'scanlines', 'vhs'

        Returns:
            True if processing successful, False otherwise.

        Raises:
            ProcessingError: If the file cannot be processed.
            UnsupportedFormatError: If the file format is not supported.
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        if effects is None:
            effects = EffectName.all()
        else:
            # Normalize to strings
            effects = [str(e) for e in effects]

        logger.info("Processing %s -> %s", input_path, output_path)
        logger.info("Effects: %s, Intensity: %.2f", effects, self.intensity)

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine file type and process accordingly
            suffix = input_path.suffix.lower()
            if suffix in self.config.VIDEO_FORMATS:
                return self._process_video(input_path, output_path, effects)
            elif suffix in self.config.GIF_FORMATS:
                return self._process_gif(input_path, output_path, effects)
            elif suffix in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"):
                return self._process_image(input_path, output_path, effects)
            else:
                raise UnsupportedFormatError(
                    input_path,
                    detected_format=suffix,
                    supported_formats=[".jpg", ".png", ".mp4", ".gif"],
                )
        except (ProcessingError, UnsupportedFormatError):
            raise
        except Exception as e:
            logger.exception("Unexpected error processing %s", input_path)
            raise ProcessingError(
                f"Failed to process media: {e}",
                input_path=input_path,
                output_path=output_path,
            ) from e

    def _process_image(
        self, input_path: Path, output_path: Path, effects: list[str]
    ) -> bool:
        """Process a single image file.

        Args:
            input_path: Path to the input image.
            output_path: Path to save the processed image.
            effects: List of effect names to apply.

        Returns:
            True if processing successful.

        Raises:
            ProcessingError: If the image cannot be loaded or saved.
        """
        # Load image
        image = cv2.imread(str(input_path))
        if image is None:
            raise ProcessingError(
                f"Could not load image: {input_path}",
                input_path=input_path,
            )

        logger.debug(
            "Loaded image: %s (%dx%d)", input_path, image.shape[1], image.shape[0]
        )

        # Apply effects
        processed = self._apply_effects(image, effects)

        # Save result
        success = cv2.imwrite(str(output_path), processed)
        if not success:
            raise ProcessingError(
                f"Could not save image: {output_path}",
                input_path=input_path,
                output_path=output_path,
            )

        logger.info("Processed image saved: %s", output_path)
        return True

    def _process_video(
        self, input_path: Path, output_path: Path, effects: list[str]
    ) -> bool:
        """Process a video file.

        Args:
            input_path: Path to the input video.
            output_path: Path to save the processed video.
            effects: List of effect names to apply.

        Returns:
            True if processing successful.

        Raises:
            ProcessingError: If the video cannot be opened or written.
        """
        logger.info("Processing video: %s -> %s", input_path, output_path)

        # Open input video
        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            raise ProcessingError(
                f"Could not open video file: {input_path}",
                input_path=input_path,
            )

        try:
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            logger.info(
                "Video info: %dx%d, %d FPS, %d frames", width, height, fps, total_frames
            )

            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*self.config.VIDEO_CODEC)  # type: ignore[attr-defined]
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

            if not out.isOpened():
                raise ProcessingError(
                    f"Could not create output video: {output_path}",
                    input_path=input_path,
                    output_path=output_path,
                )

            try:
                # Process frames with progress bar
                frame_count = 0
                with tqdm(total=total_frames, desc="Processing frames") as pbar:
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # Apply effects to frame
                        processed_frame = self._apply_effects(frame, effects)

                        # Write frame to output video
                        out.write(processed_frame)

                        frame_count += 1
                        pbar.update(1)

                logger.info(
                    "Video processing complete! Processed %d frames", frame_count
                )
                logger.info("Output saved: %s", output_path)
                return True

            finally:
                out.release()

        finally:
            cap.release()

    def _process_gif(
        self, input_path: Path, output_path: Path, effects: list[str]
    ) -> bool:
        """Process a GIF file using streaming to reduce memory usage.

        Args:
            input_path: Path to the input GIF.
            output_path: Path to save the processed GIF.
            effects: List of effect names to apply.

        Returns:
            True if processing successful.

        Raises:
            ProcessingError: If the GIF cannot be read or written.
        """
        logger.info("Processing GIF: %s -> %s", input_path, output_path)

        try:
            # Read GIF using imageio
            gif_reader = imageio.get_reader(str(input_path))
        except Exception as e:
            raise ProcessingError(
                f"Could not open GIF file: {input_path}",
                input_path=input_path,
            ) from e

        try:
            # Get total number of frames and metadata
            total_frames = len(gif_reader)
            logger.info("GIF info: %d frames", total_frames)

            # Get original GIF duration info
            try:
                duration = gif_reader.get_meta_data().get(
                    "duration", self.config.GIF_DEFAULT_DURATION
                )
            except Exception:
                duration = self.config.GIF_DEFAULT_DURATION

            # Process and write frames in chunks to reduce memory usage
            chunk_size = min(self.config.GIF_CHUNK_SIZE, total_frames)

            # Initialize writer with first frame to get dimensions
            first_frame = gif_reader.get_data(0)
            if first_frame.shape[2] == 4:  # RGBA
                first_frame = first_frame[:, :, :3]  # type: ignore[assignment]

            # Convert and process first frame
            frame_bgr = cv2.cvtColor(first_frame, cv2.COLOR_RGB2BGR)
            processed_frame = self._apply_effects(frame_bgr, effects)
            first_processed_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

            # Start with the first frame
            all_frames = [first_processed_rgb]

            with tqdm(total=total_frames, desc="Processing GIF frames") as pbar:
                pbar.update(1)  # First frame already processed

                # Process remaining frames in chunks
                for chunk_start in range(1, total_frames, chunk_size):
                    chunk_end = min(chunk_start + chunk_size, total_frames)
                    chunk_frames = []

                    # Process chunk
                    for frame_idx in range(chunk_start, chunk_end):
                        frame = gif_reader.get_data(frame_idx)

                        # Convert PIL/imageio frame to OpenCV format (BGR)
                        if frame.shape[2] == 4:  # RGBA
                            frame_rgb = frame[:, :, :3]
                        else:
                            frame_rgb = frame

                        # Convert RGB to BGR for OpenCV
                        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

                        # Apply effects
                        processed_frame = self._apply_effects(frame_bgr, effects)

                        # Convert back to RGB for imageio
                        processed_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                        chunk_frames.append(processed_rgb)
                        pbar.update(1)

                    # Add chunk to all frames
                    all_frames.extend(chunk_frames)

                    # Clear chunk from memory
                    del chunk_frames

            # Save processed GIF
            imageio.mimsave(str(output_path), all_frames, duration=duration)  # type: ignore[arg-type]

            logger.info("GIF processing complete! Processed %d frames", len(all_frames))
            logger.info("Output saved: %s", output_path)
            return True

        finally:
            gif_reader.close()

    def _apply_effects(self, image: np.ndarray, effects: list[str]) -> np.ndarray:
        """Apply specified effects to an image using modular effect system.

        Args:
            image: Input image as numpy array (BGR format).
            effects: List of effect names to apply.

        Returns:
            Processed image with all effects applied.
        """
        result = image.copy()

        for effect_name in effects:
            if effect_name in self.effects:
                try:
                    result = self.effects[effect_name].apply(result)
                except Exception as e:
                    logger.warning(
                        "Effect '%s' failed: %s - skipping",
                        effect_name,
                        e,
                    )
            else:
                logger.warning("Unknown effect '%s' ignored", effect_name)

        return result

    def get_available_effects(self) -> list[str]:
        """Get list of available effect names.

        Returns:
            List of effect name strings.
        """
        return list(self.effects.keys())

    def add_custom_effect(self, name: str, effect: BaseEffect) -> None:
        """Add a custom effect to the processor.

        Args:
            name: The name to register the effect under.
            effect: An instance of a BaseEffect subclass.
        """
        self.effects[name] = effect
        logger.debug("Added custom effect: %s", name)


def main() -> None:
    """CLI entry point for vaporwave processing.

    Usage:
        vaporwave <input_file> <output_file> [intensity]

    Example:
        vaporwave input.jpg output.jpg 1.5
    """
    import sys

    if len(sys.argv) < 3:
        print("Usage: vaporwave <input_file> <output_file> [intensity]")
        print("Example: vaporwave input.jpg output.jpg 1.5")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    intensity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    # Validate input file exists
    if not input_file.exists():
        logger.error("Input file not found: %s", input_file)
        sys.exit(1)

    processor = VaporwaveProcessor(intensity=intensity, verbose=True)

    try:
        success = processor.process_media(input_file, output_file)
        if success:
            logger.info("Processing completed successfully!")
        else:
            logger.error("Processing failed!")
            sys.exit(1)
    except ProcessingError as e:
        logger.error("Processing error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
