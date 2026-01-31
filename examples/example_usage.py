#!/usr/bin/env python3
"""
Example usage of the Vaporwave Processor
"""

import sys
from pathlib import Path

# Add parent directory to path to import src package
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vaporwave_processor import VaporwaveProcessor


def main():
    print("🌈 Vaporwave Processor Demo")
    print("=" * 30)

    # Get base directory
    base_dir = Path(__file__).parent.parent
    input_image = base_dir / "assets" / "samples" / "test_input.jpg"
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Check if input exists
    if not input_image.exists():
        print(f"❌ Error: Test input image not found at {input_image}")
        print("Please ensure test_input.jpg exists in assets/samples/")
        return

    # Initialize processor with different intensities
    processor_subtle = VaporwaveProcessor(intensity=0.5)
    processor_normal = VaporwaveProcessor(intensity=1.0)
    processor_intense = VaporwaveProcessor(intensity=2.0)

    # Example 1: Process an image with specific effects
    print("1. Processing with normal intensity (chromatic, holographic, neon)...")
    processor_normal.process_media(
        str(input_image),
        str(output_dir / "example_normal.jpg"),
        effects=["chromatic", "holographic", "neon"],
    )

    # Example 2: Process with intense effects
    print("\n2. Processing with intense effects (all effects)...")
    processor_intense.process_media(
        str(input_image), str(output_dir / "example_intense.jpg")
    )

    # Example 3: Process with subtle effects
    print("\n3. Processing with subtle effects (scanlines, vhs)...")
    processor_subtle.process_media(
        str(input_image),
        str(output_dir / "example_subtle.jpg"),
        effects=["scanlines", "vhs"],
    )

    print("\n✅ All examples completed!")
    print("Check the output/ directory for results.")


if __name__ == "__main__":
    main()
