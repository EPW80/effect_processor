#!/usr/bin/env python3
"""
Example usage of the Vaporwave Processor
"""
import sys

sys.path.append("../src")
from vaporwave_processor import VaporwaveProcessor


def main():
    print("🌈 Vaporwave Processor Demo")
    print("=" * 30)

    # Initialize processor with different intensities
    processor_subtle = VaporwaveProcessor(intensity=0.5)
    processor_normal = VaporwaveProcessor(intensity=1.0)
    processor_intense = VaporwaveProcessor(intensity=2.0)

    # Example 1: Process an image with specific effects
    print("1. Processing with normal intensity (chromatic, holographic, neon)...")
    processor_normal.process_media(
        "../assets/samples/test_input.jpg",
        "../output/example_normal.jpg",
        effects=["chromatic", "holographic", "neon"],
    )

    # Example 2: Process with intense effects
    print("\n2. Processing with intense effects (all effects)...")
    processor_intense.process_media(
        "../assets/samples/test_input.jpg", "../output/example_intense.jpg"
    )

    # Example 3: Process with subtle effects
    print("\n3. Processing with subtle effects (scanlines, vhs)...")
    processor_subtle.process_media(
        "../assets/samples/test_input.jpg",
        "../output/example_subtle.jpg",
        effects=["scanlines", "vhs"],
    )

    print("\n✅ All examples completed!")
    print("Check the output/ directory for results.")


if __name__ == "__main__":
    main()
