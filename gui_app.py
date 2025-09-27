"""Simple GUI for the Vaporwave Processor"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import os
from src.vaporwave_processor import VaporwaveProcessor


class VaporwaveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaporwave Effect Processor")
        self.root.geometry("600x500")

        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.intensity = tk.DoubleVar(value=1.0)
        self.effects = {
            "chromatic": tk.BooleanVar(value=True),
            "holographic": tk.BooleanVar(value=True),
            "scanlines": tk.BooleanVar(value=True),
            "neon": tk.BooleanVar(value=True),
            "vhs": tk.BooleanVar(value=True),
        }

        self.setup_ui()

    def setup_ui(self):
        # File selection
        tk.Label(self.root, text="Input File:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        tk.Entry(self.root, textvariable=self.input_file, width=40).grid(
            row=0, column=1, padx=10, pady=5
        )
        tk.Button(self.root, text="Browse", command=self.select_input).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Output file selection
        tk.Label(self.root, text="Output File:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        tk.Entry(self.root, textvariable=self.output_file, width=40).grid(
            row=1, column=1, padx=10, pady=5
        )
        tk.Button(self.root, text="Save As", command=self.select_output).grid(
            row=1, column=2, padx=10, pady=5
        )

        # Effects selection
        tk.Label(self.root, text="Effects:").grid(
            row=2, column=0, padx=10, pady=5, sticky="nw"
        )
        effects_frame = tk.Frame(self.root)
        effects_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")

        for i, (name, var) in enumerate(self.effects.items()):
            checkbutton = tk.Checkbutton(effects_frame, text=name.title(), variable=var)
            checkbutton.grid(row=i // 3, column=i % 3, padx=5, pady=2, sticky="w")

        # Intensity slider
        tk.Label(self.root, text="Intensity:").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        intensity_frame = tk.Frame(self.root)
        intensity_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Scale(
            intensity_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            variable=self.intensity,
            length=200,
        ).pack(side="left")
        self.intensity_label = tk.Label(intensity_frame, text="1.0")
        self.intensity_label.pack(side="left", padx=10)

        # Update intensity label
        self.intensity.trace("w", self.update_intensity_label)

        # Process button
        tk.Button(
            self.root,
            text="Process Image/Video",
            command=self.process,
            bg="#FF00FF",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
        ).grid(row=4, column=0, columnspan=3, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

        # Status label
        self.status_label = tk.Label(
            self.root, text="Ready to process files", fg="green", font=("Arial", 10)
        )
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)

    def update_intensity_label(self, *args):
        self.intensity_label.config(text=f"{self.intensity.get():.1f}")

    def select_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All Media", "*.jpg *.jpeg *.png *.gif *.mp4 *.avi *.mov"),
                ("Images", "*.jpg *.jpeg *.png"),
                ("Videos", "*.mp4 *.avi *.mov"),
                ("GIFs", "*.gif"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.input_file.set(filename)
            # Auto-suggest output filename
            name, ext = os.path.splitext(filename)
            output_name = f"{name}_vaporwave{ext}"
            self.output_file.set(output_name)

    def select_output(self):
        if not self.input_file.get():
            messagebox.showwarning("Warning", "Please select an input file first")
            return

        input_ext = os.path.splitext(self.input_file.get())[1].lower()

        if input_ext in [".jpg", ".jpeg", ".png"]:
            filetypes = [
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
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
                ("All files", "*.*"),
            ]
            default_ext = ".mp4"

        filename = filedialog.asksaveasfilename(
            title="Save Output As", filetypes=filetypes, defaultextension=default_ext
        )
        if filename:
            self.output_file.set(filename)

    def process(self):
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
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist")
            return

        # Create output directory if needed
        output_dir = os.path.dirname(self.output_file.get())
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Start processing in thread
        self.progress.start()
        self.status_label.config(text="Processing... Please wait", fg="orange")
        thread = threading.Thread(target=self.process_thread, args=(selected_effects,))
        thread.daemon = True
        thread.start()

    def process_thread(self, effects):
        try:
            processor = VaporwaveProcessor(intensity=self.intensity.get())
            success = processor.process_media(
                self.input_file.get(), self.output_file.get(), effects=effects
            )
            self.root.after(0, self.processing_complete, success, None)
        except Exception as e:
            self.root.after(0, self.processing_complete, False, str(e))

    def processing_complete(self, success, error=None):
        self.progress.stop()
        if success:
            self.status_label.config(
                text="Processing completed successfully!", fg="green"
            )
            messagebox.showinfo(
                "Success",
                f"Processing complete!\nOutput saved to:\n" f"{self.output_file.get()}",
            )
        else:
            self.status_label.config(text="Processing failed", fg="red")
            messagebox.showerror("Error", f"Processing failed: {error}")


def main():
    """Launch the GUI application"""
    root = tk.Tk()

    # Set application icon (optional)
    try:
        # You can add an icon file later
        # root.iconbitmap('icon.ico')
        pass
    except tk.TclError:
        pass

    # Center the window
    root.eval("tk::PlaceWindow . center")

    VaporwaveGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
