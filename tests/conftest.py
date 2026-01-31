"""
Shared pytest fixtures for vaporwave processor tests.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest


@pytest.fixture
def sample_image() -> np.ndarray:
    """Create a sample test image."""
    # Create a 100x100 RGB image with gradient
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    for i in range(100):
        for j in range(100):
            image[i, j] = [i * 2, j * 2, (i + j)]
    return image


@pytest.fixture
def solid_color_image() -> np.ndarray:
    """Create a solid color test image."""
    return np.full((100, 100, 3), [128, 64, 200], dtype=np.uint8)


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_image_file(temp_dir: Path, sample_image: np.ndarray) -> Path:
    """Create a sample image file on disk."""
    file_path = temp_dir / "test_image.jpg"
    cv2.imwrite(str(file_path), sample_image)
    return file_path


@pytest.fixture
def sample_video_file(temp_dir: Path) -> Path:
    """Create a sample video file for testing."""
    file_path = temp_dir / "test_video.mp4"

    # Create a simple test video with 10 frames
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(file_path), fourcc, 10.0, (100, 100))

    for i in range(10):
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        # Create a moving rectangle
        x = i * 10
        cv2.rectangle(frame, (x, 20), (x + 20, 40), (255, 100, 150), -1)
        out.write(frame)

    out.release()
    return file_path


@pytest.fixture
def sample_gif_frames() -> list[np.ndarray]:
    """Create sample frames for GIF testing."""
    frames = []
    for i in range(5):
        frame = np.zeros((50, 50, 3), dtype=np.uint8)
        # Create different colored frames
        frame[:, :] = [i * 50, (5 - i) * 50, 100]
        frames.append(frame)
    return frames


@pytest.fixture
def sample_gif_file(temp_dir: Path, sample_gif_frames: list[np.ndarray]) -> Path:
    """Create a sample GIF file for testing."""
    import imageio

    file_path = temp_dir / "test.gif"
    # Convert BGR to RGB for imageio
    rgb_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in sample_gif_frames]
    imageio.mimsave(str(file_path), rgb_frames, duration=0.1)
    return file_path


@pytest.fixture
def intensity_values() -> list[float]:
    """Common intensity values for testing."""
    return [0.5, 1.0, 1.5, 2.0]


@pytest.fixture
def all_effects() -> list[str]:
    """List of all available effects."""
    return ["chromatic", "holographic", "neon", "scanlines", "vhs"]
