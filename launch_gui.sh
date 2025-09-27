#!/bin/bash
# Simple launcher script for the Vaporwave GUI

echo "🌈 Starting Vaporwave Effect Processor GUI..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: tkinter not found. Please install it:"
    echo "   sudo apt install python3-tk"
    exit 1
fi

# Launch the GUI
echo "🚀 Launching GUI application..."
python3 gui_app.py

echo "👋 GUI application closed."
