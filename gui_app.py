"""Modern GUI for the Vaporwave Processor using CustomTkinter.

This module provides a modern, dark-themed graphical user interface for
applying vaporwave effects to images, videos, and GIFs.
"""

from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.effects import EffectName
from src.exceptions import ProcessingError
from src.logging_config import configure_logging, get_logger
from src.vaporwave_processor import VaporwaveProcessor

# Configure logging for GUI
configure_logging(level="INFO")
logger = get_logger(__name__)

# Window configuration
WINDOW_TITLE = "✨ Vaporwave Effect Processor"
WINDOW_SIZE = (700, 580)

# Theme configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Vaporwave color palette
COLORS = {
    "primary": "#FF00FF",       # Magenta
    "secondary": "#00FFFF",     # Cyan
    "accent": "#FF6AD5",        # Pink
    "success": "#00FF9F",       # Neon green
    "warning": "#FFB347",       # Orange
    "error": "#FF6B6B",         # Red
    "bg_dark": "#1A1A2E",       # Dark purple
    "bg_medium": "#16213E",     # Medium purple
}


class VaporwaveGUI(ctk.CTk):
    """Modern GUI class for the Vaporwave Effect Processor.

    This class creates a CustomTkinter-based user interface with a
    vaporwave aesthetic for selecting files, choosing effects, and
    processing media.

    Attributes:
        input_file: StringVar holding the input file path.
        output_file: StringVar holding the output file path.
        intensity: DoubleVar for the effect intensity slider.
        effects: Dictionary of effect name to BooleanVar for checkboxes.
    """

    def __init__(self) -> None:
        """Initialize the GUI."""
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.minsize(600, 500)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variables
        self.input_file = ctk.StringVar()
        self.output_file = ctk.StringVar()
        self.intensity = ctk.DoubleVar(value=1.0)

        # Initialize effect checkboxes from EffectName enum
        self.effects: dict[str, ctk.BooleanVar] = {
            effect.value: ctk.BooleanVar(value=True) for effect in EffectName
        }

        self.progress_bar: ctk.CTkProgressBar
        self.status_label: ctk.CTkLabel
        self.intensity_value_label: ctk.CTkLabel
        self.process_button: ctk.CTkButton

        self._setup_ui()
        logger.debug("GUI initialized")

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main container frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)

        # Title label
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌴 VAPORWAVE PROCESSOR 🌴",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["primary"],
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # === File Selection Section ===
        self._create_file_section(main_frame, start_row=1)

        # === Effects Section ===
        self._create_effects_section(main_frame, start_row=3)

        # === Intensity Section ===
        self._create_intensity_section(main_frame, start_row=4)

        # === Process Button ===
        self.process_button = ctk.CTkButton(
            main_frame,
            text="⚡ PROCESS MEDIA ⚡",
            command=self.process,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["accent"],
            height=50,
            corner_radius=10,
        )
        self.process_button.grid(
            row=5, column=0, columnspan=3, pady=25, padx=50, sticky="ew"
        )

        # === Progress Section ===
        self._create_progress_section(main_frame, start_row=6)

    def _create_file_section(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """Create the file selection section."""
        # Input file
        input_label = ctk.CTkLabel(
            parent, text="📁 Input File:", font=ctk.CTkFont(size=14)
        )
        input_label.grid(row=start_row, column=0, padx=10, pady=10, sticky="w")

        input_entry = ctk.CTkEntry(
            parent,
            textvariable=self.input_file,
            placeholder_text="Select an image, video, or GIF...",
            width=350,
        )
        input_entry.grid(row=start_row, column=1, padx=10, pady=10, sticky="ew")

        input_button = ctk.CTkButton(
            parent,
            text="Browse",
            command=self.select_input,
            width=100,
            fg_color=COLORS["secondary"],
            hover_color="#00CCCC",
            text_color="black",
        )
        input_button.grid(row=start_row, column=2, padx=10, pady=10)

        # Output file
        output_label = ctk.CTkLabel(
            parent, text="💾 Output File:", font=ctk.CTkFont(size=14)
        )
        output_label.grid(row=start_row + 1, column=0, padx=10, pady=10, sticky="w")

        output_entry = ctk.CTkEntry(
            parent,
            textvariable=self.output_file,
            placeholder_text="Output will be saved here...",
            width=350,
        )
        output_entry.grid(row=start_row + 1, column=1, padx=10, pady=10, sticky="ew")

        output_button = ctk.CTkButton(
            parent,
            text="Save As",
            command=self.select_output,
            width=100,
            fg_color=COLORS["secondary"],
            hover_color="#00CCCC",
            text_color="black",
        )
        output_button.grid(row=start_row + 1, column=2, padx=10, pady=10)

    def _create_effects_section(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """Create the effects selection section."""
        effects_label = ctk.CTkLabel(
            parent, text="🎨 Effects:", font=ctk.CTkFont(size=14)
        )
        effects_label.grid(row=start_row, column=0, padx=10, pady=15, sticky="nw")

        # Effects container frame
        effects_frame = ctk.CTkFrame(parent, fg_color="transparent")
        effects_frame.grid(
            row=start_row, column=1, columnspan=2, padx=10, pady=10, sticky="w"
        )

        # Effect icons
        effect_icons = {
            "chromatic": "🌈",
            "holographic": "💿",
            "neon": "💡",
            "scanlines": "📺",
            "vhs": "📼",
        }

        for i, (name, var) in enumerate(self.effects.items()):
            icon = effect_icons.get(name, "✨")
            checkbox = ctk.CTkCheckBox(
                effects_frame,
                text=f"{icon} {name.title()}",
                variable=var,
                font=ctk.CTkFont(size=13),
                fg_color=COLORS["primary"],
                hover_color=COLORS["accent"],
                border_color=COLORS["secondary"],
            )
            checkbox.grid(row=i // 3, column=i % 3, padx=15, pady=8, sticky="w")

    def _create_intensity_section(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """Create the intensity slider section."""
        intensity_label = ctk.CTkLabel(
            parent, text="⚙️ Intensity:", font=ctk.CTkFont(size=14)
        )
        intensity_label.grid(row=start_row, column=0, padx=10, pady=15, sticky="w")

        # Slider container
        slider_frame = ctk.CTkFrame(parent, fg_color="transparent")
        slider_frame.grid(
            row=start_row, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        slider_frame.grid_columnconfigure(0, weight=1)

        # Intensity slider
        intensity_slider = ctk.CTkSlider(
            slider_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=15,
            variable=self.intensity,
            command=self._update_intensity_label,
            progress_color=COLORS["primary"],
            button_color=COLORS["secondary"],
            button_hover_color=COLORS["accent"],
        )
        intensity_slider.grid(row=0, column=0, padx=(0, 15), sticky="ew")

        # Intensity value display
        self.intensity_value_label = ctk.CTkLabel(
            slider_frame,
            text="1.0x",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["secondary"],
            width=50,
        )
        self.intensity_value_label.grid(row=0, column=1)

    def _create_progress_section(self, parent: ctk.CTkFrame, start_row: int) -> None:
        """Create the progress bar and status section."""
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            parent,
            mode="indeterminate",
            progress_color=COLORS["primary"],
        )
        self.progress_bar.grid(
            row=start_row, column=0, columnspan=3, padx=20, pady=10, sticky="ew"
        )
        self.progress_bar.set(0)

        # Status label
        self.status_label = ctk.CTkLabel(
            parent,
            text="✅ Ready to process files",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["success"],
        )
        self.status_label.grid(row=start_row + 1, column=0, columnspan=3, pady=10)

    def _update_intensity_label(self, value: float) -> None:
        """Update the intensity value display."""
        self.intensity_value_label.configure(text=f"{value:.1f}x")

    def select_input(self) -> None:
        """Open a file dialog to select the input file."""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All Media", "*.jpg *.jpeg *.png *.gif *.mp4 *.avi *.mov *.mkv *.webp"),
                ("Images", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                ("GIFs", "*.gif"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            input_path = Path(filename)
            self.input_file.set(str(input_path))
            logger.debug("Selected input file: %s", input_path)

            # Auto-suggest output filename
            output_path = (
                input_path.parent / f"{input_path.stem}_vaporwave{input_path.suffix}"
            )
            self.output_file.set(str(output_path))

    def select_output(self) -> None:
        """Open a file dialog to select the output file location."""
        if not self.input_file.get():
            messagebox.showwarning("Warning", "Please select an input file first")
            return

        input_path = Path(self.input_file.get())
        input_ext = input_path.suffix.lower()

        if input_ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"):
            filetypes = [
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("WebP files", "*.webp"),
                ("All files", "*.*"),
            ]
            default_ext = ".jpg"
        elif input_ext == ".gif":
            filetypes = [("GIF files", "*.gif"), ("All files", "*.*")]
            default_ext = ".gif"
        else:  # video files
            filetypes = [
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MKV files", "*.mkv"),
                ("All files", "*.*"),
            ]
            default_ext = ".mp4"

        filename = filedialog.asksaveasfilename(
            title="Save Output As",
            filetypes=filetypes,
            defaultextension=default_ext,
        )
        if filename:
            self.output_file.set(filename)

    def process(self) -> None:
        """Validate inputs and start the processing thread."""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return

        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return

        # Get selected effects
        selected_effects = [name for name, var in self.effects.items() if var.get()]

        if not selected_effects:
            messagebox.showerror("Error", "Please select at least one effect")
            return

        # Check if input file exists
        input_path = Path(self.input_file.get())
        if not input_path.exists():
            messagebox.showerror("Error", "Input file does not exist")
            return

        # Create output directory if needed
        output_path = Path(self.output_file.get())
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Starting processing: %s -> %s with effects %s",
            input_path,
            output_path,
            selected_effects,
        )

        # Update UI for processing state
        self.progress_bar.start()
        self.status_label.configure(
            text="⏳ Processing... Please wait", text_color=COLORS["warning"]
        )
        self.process_button.configure(state="disabled")

        # Start processing in thread
        thread = threading.Thread(target=self._process_thread, args=(selected_effects,))
        thread.daemon = True
        thread.start()

    def _process_thread(self, effects: list[str]) -> None:
        """Run the processing in a background thread.

        Args:
            effects: List of effect names to apply.
        """
        try:
            processor = VaporwaveProcessor(intensity=self.intensity.get())
            success = processor.process_media(
                self.input_file.get(), self.output_file.get(), effects=effects
            )
            self.after(0, self._processing_complete, success, None)
        except ProcessingError as e:
            logger.error("Processing error: %s", e)
            self.after(0, self._processing_complete, False, str(e))
        except Exception as e:
            logger.exception("Unexpected error during processing")
            self.after(0, self._processing_complete, False, str(e))

    def _processing_complete(self, success: bool, error: str | None = None) -> None:
        """Handle processing completion in the main thread.

        Args:
            success: Whether processing was successful.
            error: Error message if processing failed.
        """
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.process_button.configure(state="normal")

        if success:
            logger.info("Processing completed successfully")
            self.status_label.configure(
                text="✅ Processing completed successfully!",
                text_color=COLORS["success"],
            )
            messagebox.showinfo(
                "Success",
                f"🎉 Processing complete!\n\nOutput saved to:\n{self.output_file.get()}",
            )
        else:
            logger.error("Processing failed: %s", error)
            self.status_label.configure(
                text="❌ Processing failed", text_color=COLORS["error"]
            )
            messagebox.showerror("Error", f"Processing failed:\n{error}")


def main() -> None:
    """Launch the GUI application."""
    logger.info("Starting Vaporwave Effect Processor GUI (CustomTkinter)")

    app = VaporwaveGUI()
    logger.debug("Entering main event loop")
    app.mainloop()
    logger.info("GUI closed")


if __name__ == "__main__":
    main()
