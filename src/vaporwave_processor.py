"""
Vaporwave Processor - A library for applying vaporwave holographic 3D effects
"""

import cv2
import numpy as np
import imageio
from tqdm import tqdm
from typing import List, Optional, Dict

try:
    from .config import get_processing_config
    from .effects import (
        BaseEffect,
        ChromaticAberrationEffect,
        HolographicEffect,
        NeonGlowEffect,
        ScanlinesEffect,
        VHSEffect,
    )
except ImportError:
    # Fallback for direct execution
    from config import get_processing_config
    from effects import (
        BaseEffect,
        ChromaticAberrationEffect,
        HolographicEffect,
        NeonGlowEffect,
        ScanlinesEffect,
        VHSEffect,
    )


class VaporwaveProcessor:
    """
    Main class for applying vaporwave effects to images and videos.
    """

    def __init__(self, intensity: float = 1.0, verbose: bool = True):
        """
        Initialize the VaporwaveProcessor.

        Args:
            intensity: Effect intensity multiplier (0.1 to 5.0)
            verbose: Whether to print effect application messages
        """
        self.config = get_processing_config()
        self.intensity = max(
            self.config.MIN_INTENSITY, min(self.config.MAX_INTENSITY, intensity)
        )
        self.verbose = verbose

        # Initialize effect instances
        self.effects: Dict[str, BaseEffect] = {
            "chromatic": ChromaticAberrationEffect(self.intensity, verbose),
            "holographic": HolographicEffect(self.intensity, verbose),
            "neon": NeonGlowEffect(self.intensity, verbose),
            "scanlines": ScanlinesEffect(self.intensity, verbose),
            "vhs": VHSEffect(self.intensity, verbose),
        }

    def process_media(
        self,
        input_path: str,
        output_path: str,
        effects: Optional[List[str]] = None,
    ) -> bool:
        """
        Process media file with vaporwave effects.

        Args:
            input_path: Path to input media file
            output_path: Path to save processed media
            effects: List of effects to apply. If None, applies all effects.
                    Available: 'chromatic', 'holographic', 'neon',
                    'scanlines', 'vhs'

        Returns:
            True if processing successful, False otherwise
        """
        if effects is None:
            effects = ["chromatic", "holographic", "neon", "scanlines", "vhs"]

        try:
            # Determine file type and process accordingly
            if input_path.lower().endswith(self.config.VIDEO_FORMATS):
                return self._process_video(input_path, output_path, effects)
            elif input_path.lower().endswith(self.config.GIF_FORMATS):
                return self._process_gif(input_path, output_path, effects)
            else:
                return self._process_image(input_path, output_path, effects)
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False

    def _process_image(
        self, input_path: str, output_path: str, effects: List[str]
    ) -> bool:
        """Process a single image file."""
        # Load image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Could not load image: {input_path}")
            return False

        # Apply effects
        processed = self._apply_effects(image, effects)

        # Save result
        cv2.imwrite(output_path, processed)
        print(f"Processed image saved: {output_path}")
        return True

    def _process_video(
        self, input_path: str, output_path: str, effects: List[str]
    ) -> bool:
        """Process a video file."""
        print(f"Processing video: {input_path} -> {output_path}")
        print(f"Effects: {', '.join(effects)}")
        print(f"Intensity: {self.intensity}")

        try:
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                print(f"Error: Could not open video file {input_path}")
                return False

            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            print(f"Video info: {width}x{height}, {fps} FPS, " f"{total_frames} frames")

            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*self.config.VIDEO_CODEC)
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            if not out.isOpened():
                print(f"Error: Could not create output video file " f"{output_path}")
                cap.release()
                return False

            # Process frames with progress bar
            frame_count = 0
            # Create a non-verbose processor for frame processing
            frame_processor = VaporwaveProcessor(self.intensity, verbose=False)
            with tqdm(total=total_frames, desc="Processing frames") as pbar:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Apply effects to frame
                    processed_frame = frame_processor._apply_effects(frame, effects)

                    # Write frame to output video
                    out.write(processed_frame)

                    frame_count += 1
                    pbar.update(1)

            # Release everything
            cap.release()
            out.release()

            print(f"Video processing complete! Processed {frame_count} " f"frames")
            print(f"Output saved: {output_path}")
            return True

        except Exception as e:
            print(f"Error processing video: {e}")
            return False

    def _process_gif(
        self, input_path: str, output_path: str, effects: List[str]
    ) -> bool:
        """Process a GIF file using streaming to reduce memory usage."""
        print(f"Processing GIF: {input_path} -> {output_path}")
        print(f"Effects: {', '.join(effects)}")
        print(f"Intensity: {self.intensity}")

        try:
            # Read GIF using imageio
            gif_reader = imageio.get_reader(input_path)

            # Get total number of frames and metadata
            total_frames = len(gif_reader)
            print(f"GIF info: {total_frames} frames")

            # Get original GIF duration info
            try:
                duration = gif_reader.get_meta_data().get(
                    "duration", self.config.GIF_DEFAULT_DURATION
                )
            except Exception:
                duration = self.config.GIF_DEFAULT_DURATION

            # Process and write frames in chunks to reduce memory usage
            chunk_size = min(self.config.GIF_CHUNK_SIZE, total_frames)
            frame_processor = VaporwaveProcessor(self.intensity, verbose=False)

            # Initialize writer with first frame to get dimensions
            first_frame = gif_reader.get_data(0)
            if first_frame.shape[2] == 4:  # RGBA
                first_frame = first_frame[:, :, :3]

            # Convert and process first frame
            frame_bgr = cv2.cvtColor(first_frame, cv2.COLOR_RGB2BGR)
            processed_frame = frame_processor._apply_effects(frame_bgr, effects)
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
                        processed_frame = frame_processor._apply_effects(
                            frame_bgr, effects
                        )

                        # Convert back to RGB for imageio
                        processed_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                        chunk_frames.append(processed_rgb)
                        pbar.update(1)

                    # Add chunk to all frames
                    all_frames.extend(chunk_frames)

                    # Optional: Clear chunk from memory
                    del chunk_frames

            # Save processed GIF
            imageio.mimsave(output_path, all_frames, duration=duration)

            gif_reader.close()

            print(f"GIF processing complete! Processed {len(all_frames)} frames")
            print(f"Output saved: {output_path}")
            return True

        except Exception as e:
            print(f"Error processing GIF: {e}")
            return False

    def _apply_effects(self, image: np.ndarray, effects: List[str]) -> np.ndarray:
        """Apply specified effects to an image using modular effect system."""
        result = image.copy()

        for effect_name in effects:
            if effect_name in self.effects:
                result = self.effects[effect_name].apply(result)
            else:
                print(f"Warning: Unknown effect '{effect_name}' ignored")

        return result

    def get_available_effects(self) -> List[str]:
        """Get list of available effect names."""
        return list(self.effects.keys())

    def add_custom_effect(self, name: str, effect: BaseEffect) -> None:
        """Add a custom effect to the processor."""
        self.effects[name] = effect


def main():
    """Example main function for console script entry point."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: vaporwave <input_file> <output_file> [intensity]")
        print("Example: vaporwave input.jpg output.jpg 1.5")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    intensity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    processor = VaporwaveProcessor(intensity=intensity)
    success = processor.process_media(input_file, output_file)

    if success:
        print("Processing completed successfully!")
    else:
        print("Processing failed!")


if __name__ == "__main__":
    main()
