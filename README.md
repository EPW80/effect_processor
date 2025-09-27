# Vaporwave Processor

A Python library for applying vaporwave holographic 3D effects to images and videos.

## Features

- Apply retro vaporwave effects to images
- Create holographic 3D visual effects
- Process videos with aesthetic filters
- Easy-to-use API for custom effect chains
- Graphical user interface for easy operation
- Command-line interface for batch processing

### Available Effects
- **Chromatic Aberration**: RGB color separation effect ✅
- **Holographic**: 3D hologram-style visual distortion ✅  
- **Neon Glow**: Bright neon lighting effects ✅
- **Scanlines**: Retro CRT monitor scanlines ✅
- **VHS**: Vintage video tape distortion effects ✅

*All effects are fully implemented and working!*

## Installation

```bash
pip install vaporwave-processor
```

For GUI support, ensure tkinter is installed:
```bash
sudo apt install python3-tk  # On Ubuntu/Debian
```

## Usage

### Command Line
```bash
# Basic usage
vaporwave input.jpg output.jpg

# With custom intensity
vaporwave input.jpg output.jpg 1.5
```

### GUI Application
```bash
# Launch the graphical interface
vaporwave-gui

# Or run directly
python gui_app.py

# Or use the launcher script
./launch_gui.sh
```

### Python API
```python
from vaporwave_processor import VaporwaveProcessor

# Initialize the processor
processor = VaporwaveProcessor(intensity=1.5)

# Apply effects to an image
processor.process_media("input.jpg", "output.jpg", effects=['chromatic', 'neon'])
```

## Examples

### Sample Outputs

**Normal Intensity Effect:**
[Normal Intensity](output/example_normal.jpg)

**Intense Effect:**
[Intense Effect](output/example_intense.jpg)

**Animated GIF Processing:**
[Animated Output](output/test_output.gif)

## Requirements

- Python 3.9+
- OpenCV
- NumPy
- Pillow
- SciPy
- scikit-image

## License

MIT License
