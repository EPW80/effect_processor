# Vaporwave Processor

A Python library for applying vaporwave holographic 3D effects to images, videos, and GIFs.

## Features

- Apply retro vaporwave effects to images, videos, and GIFs
- Create holographic 3D visual effects
- Process videos (MP4, AVI, MOV) with aesthetic filters
- Process animated GIFs with vaporwave effects
- Easy-to-use API for custom effect chains
- Graphical user interface for easy operation
- Command-line interface for batch processing

### Available Effects
- **Chromatic Aberration**: RGB color separation effect ✅
- **Holographic**: 3D hologram-style visual distortion ✅  
- **Neon Glow**: Bright neon lighting effects ✅
- **Scanlines**: Retro CRT monitor scanlines ✅
- **VHS**: Vintage video tape distortion effects ✅

*All effects are fully implemented and working with images, videos, and GIFs!*

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/EPW80/effect_processor.git
cd effect_processor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

For GUI support, ensure tkinter is installed:
```bash
sudo apt install python3-tk  # On Ubuntu/Debian
```

## Usage

### GUI Application (Recommended)
```bash
# Launch the graphical interface
./launch_gui.sh

# Or run directly
python3 gui_app.py
```

### Python API
```python
from src.vaporwave_processor import VaporwaveProcessor

# Initialize the processor
processor = VaporwaveProcessor(intensity=1.5)

# Process an image
processor.process_media("input.jpg", "output.jpg", effects=['chromatic', 'neon'])

# Process a video
processor.process_media("input.mp4", "output.mp4", effects=['holographic', 'vhs'])

# Process a GIF
processor.process_media("input.gif", "output.gif", effects=['scanlines', 'chromatic'])
```

### Command Line Examples
```bash
# Process a video with all effects
python3 -c "
from src.vaporwave_processor import VaporwaveProcessor
processor = VaporwaveProcessor(intensity=1.2)
processor.process_media('input.mp4', 'output.mp4', effects=['chromatic', 'holographic', 'neon', 'scanlines', 'vhs'])
"
```

## Examples

### Sample Outputs

The following sample outputs demonstrate different effect intensities:

- **Normal Intensity**: [example_normal.jpg](output/example_normal.jpg)
- **Intense Effects**: [example_intense.jpg](output/example_intense.jpg)  
- **Subtle Effects**: [example_subtle.jpg](output/example_subtle.jpg)
- **Animated GIF**: [test_output.gif](output/test_output.gif)

## Supported Formats

### Input Formats
- **Images**: JPG, PNG, BMP, TIFF
- **Videos**: MP4, AVI, MOV, MKV, WMV
- **Animations**: GIF

### Output Formats
- **Images**: JPG, PNG
- **Videos**: MP4
- **Animations**: GIF

## Requirements

- Python 3.9+
- opencv-python>=4.9.0.80
- numpy>=1.26.0
- Pillow>=10.2.0
- imageio>=2.34.0
- imageio-ffmpeg>=0.4.9
- tqdm>=4.66.1
- scipy>=1.11.4
- scikit-image>=0.22.0

## Project Structure

```
effect_processor/
├── src/
│   ├── vaporwave_processor.py    # Main processor class
│   ├── config.py                 # Configuration settings
│   └── effects/                  # Individual effect modules
├── gui_app.py                    # GUI application
├── launch_gui.sh                 # GUI launcher script
├── examples/
│   └── example_usage.py          # Usage examples
├── output/                       # Generated output files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## License

MIT License