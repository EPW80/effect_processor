#!/usr/bin/env python3
"""
Test script for video and GIF processing functionality
"""
import sys
import os

# Add src directory to path for importing vaporwave_processor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from vaporwave_processor import VaporwaveProcessor  # noqa: E402


def test_video_processing():
    """Test video processing with a sample video."""
    print("🎬 Testing Video Processing")
    print("=" * 40)

    processor = VaporwaveProcessor(intensity=1.0)

    # Test with a hypothetical input video
    input_video = "test_input.mp4"
    output_video = "output/test_output.mp4"

    if os.path.exists(input_video):
        print(f"Processing video: {input_video}")
        success = processor.process_media(
            input_video,
            output_video,
            effects=["chromatic", "neon", "scanlines"],
        )

        if success:
            print("✅ Video processing completed successfully!")
        else:
            print("❌ Video processing failed!")
    else:
        print(f"⚠️  Test video {input_video} not found. " f"Skipping video test.")


def test_gif_processing():
    """Test GIF processing with a sample GIF."""
    print("\n🎞️  Testing GIF Processing")
    print("=" * 40)

    processor = VaporwaveProcessor(intensity=1.2)

    # Test with a hypothetical input GIF
    input_gif = "test_input.gif"
    output_gif = "output/test_output.gif"

    if os.path.exists(input_gif):
        print(f"Processing GIF: {input_gif}")
        success = processor.process_media(
            input_gif, output_gif, effects=["holographic", "vhs", "chromatic"]
        )

        if success:
            print("✅ GIF processing completed successfully!")
        else:
            print("❌ GIF processing failed!")
    else:
        print(f"⚠️  Test GIF {input_gif} not found. Skipping GIF test.")


def create_sample_video():
    """Create a simple test video using OpenCV."""
    print("\n📹 Creating sample test video...")

    try:
        import cv2
        import numpy as np

        # Create a simple test video
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("test_input.mp4", fourcc, 10.0, (640, 480))

        for i in range(50):  # 5 seconds at 10 FPS
            # Create a frame with moving colored rectangle
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

            # Add some colored shapes that move
            x = int(50 + i * 10)
            y = int(100 + 50 * np.sin(i * 0.2))

            cv2.rectangle(frame, (x, y), (x + 100, y + 100), (255, 100, 150), -1)
            cv2.circle(frame, (300, 200), 50, (100, 255, 100), -1)
            cv2.putText(
                frame,
                f"Frame {i}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            out.write(frame)

        out.release()
        print("✅ Sample video 'test_input.mp4' created successfully!")
        return True

    except Exception as e:
        print(f"❌ Failed to create sample video: {e}")
        return False


def main():
    """Main test function."""
    print("🌈 Vaporwave Video/GIF Processing Test")
    print("=" * 50)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Create sample video if it doesn't exist
    if not os.path.exists("test_input.mp4"):
        create_sample_video()

    # Run tests
    test_video_processing()
    test_gif_processing()

    print("\n🎉 Testing complete!")
    print("\nTo test with your own files:")
    print("1. Place a video file as 'test_input.mp4'")
    print("2. Place a GIF file as 'test_input.gif'")
    print("3. Run this script again")


if __name__ == "__main__":
    main()
