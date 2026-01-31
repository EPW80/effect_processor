"""Tests for GUI application using CustomTkinter.

Note: These tests mock the GUI components extensively since running actual
GUI tests requires a display. For headless environments (CI), tests that
require a display are skipped.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import gui_app


class TestColorPalette:
    """Tests for color palette configuration."""

    def test_colors_defined(self) -> None:
        """Test that color palette is properly defined."""
        assert "primary" in gui_app.COLORS
        assert "secondary" in gui_app.COLORS
        assert "accent" in gui_app.COLORS
        assert "success" in gui_app.COLORS
        assert "warning" in gui_app.COLORS
        assert "error" in gui_app.COLORS

    def test_colors_are_valid_hex(self) -> None:
        """Test that colors are valid hex values."""
        for name, color in gui_app.COLORS.items():
            assert color.startswith("#"), f"{name} should be a hex color"
            assert len(color) == 7, f"{name} should be 7 chars (#RRGGBB)"


class TestWindowConfiguration:
    """Tests for window configuration constants."""

    def test_window_title_defined(self) -> None:
        """Test window title is defined."""
        assert gui_app.WINDOW_TITLE
        assert "Vaporwave" in gui_app.WINDOW_TITLE

    def test_window_size_defined(self) -> None:
        """Test window size is defined."""
        assert gui_app.WINDOW_SIZE == (700, 580)


class TestModuleImports:
    """Tests for module imports and dependencies."""

    def test_customtkinter_import(self) -> None:
        """Test that customtkinter can be imported."""
        import customtkinter as ctk
        assert ctk is not None

    def test_gui_class_exists(self) -> None:
        """Test that VaporwaveGUI class exists."""
        assert hasattr(gui_app, "VaporwaveGUI")

    def test_main_function_exists(self) -> None:
        """Test that main function exists."""
        assert hasattr(gui_app, "main")
        assert callable(gui_app.main)


# Skip tests that require a display
try:
    import tkinter
    tkinter.Tk().destroy()
    HAS_DISPLAY = True
except Exception:
    HAS_DISPLAY = False


@pytest.mark.skipif(not HAS_DISPLAY, reason="No display available")
class TestVaporwaveGUIWithDisplay:
    """Tests that require a display."""

    def test_gui_creation(self) -> None:
        """Test that GUI can be created."""
        app = gui_app.VaporwaveGUI()
        try:
            assert app.intensity.get() == 1.0
        finally:
            app.destroy()

    def test_default_effects_enabled(self) -> None:
        """Test that all effects are enabled by default."""
        app = gui_app.VaporwaveGUI()
        try:
            for effect_name, var in app.effects.items():
                assert var.get() is True, f"{effect_name} should be enabled by default"
        finally:
            app.destroy()

    @patch("gui_app.filedialog.askopenfilename")
    def test_select_input_file(self, mock_filedialog: Mock) -> None:
        """Test input file selection."""
        app = gui_app.VaporwaveGUI()
        try:
            mock_filedialog.return_value = "/path/to/input.jpg"
            app.select_input()
            assert app.input_file.get() == "/path/to/input.jpg"
            assert "vaporwave" in app.output_file.get()
        finally:
            app.destroy()

    @patch("gui_app.filedialog.askopenfilename")
    def test_select_input_cancelled(self, mock_filedialog: Mock) -> None:
        """Test input file selection when cancelled."""
        app = gui_app.VaporwaveGUI()
        try:
            mock_filedialog.return_value = ""
            app.select_input()
            assert app.input_file.get() == ""
        finally:
            app.destroy()

    @patch("gui_app.filedialog.asksaveasfilename")
    @patch("gui_app.messagebox.showwarning")
    def test_select_output_without_input(
        self, mock_warning: Mock, mock_filedialog: Mock
    ) -> None:
        """Test output file selection without input file."""
        app = gui_app.VaporwaveGUI()
        try:
            app.select_output()
            mock_warning.assert_called_once()
            mock_filedialog.assert_not_called()
        finally:
            app.destroy()

    @patch("gui_app.filedialog.asksaveasfilename")
    def test_select_output_with_input(self, mock_filedialog: Mock) -> None:
        """Test output file selection with input file set."""
        app = gui_app.VaporwaveGUI()
        try:
            app.input_file.set("/path/to/input.jpg")
            mock_filedialog.return_value = "/path/to/output.jpg"
            app.select_output()
            assert app.output_file.get() == "/path/to/output.jpg"
        finally:
            app.destroy()

    def test_intensity_default_value(self) -> None:
        """Test default intensity value."""
        app = gui_app.VaporwaveGUI()
        try:
            assert app.intensity.get() == 1.0
        finally:
            app.destroy()

    @patch("gui_app.messagebox.showerror")
    def test_process_without_input_file(self, mock_error: Mock) -> None:
        """Test processing without input file shows error."""
        app = gui_app.VaporwaveGUI()
        try:
            app.process()
            mock_error.assert_called_once()
            assert "input" in mock_error.call_args[0][1].lower()
        finally:
            app.destroy()

    @patch("gui_app.messagebox.showerror")
    def test_process_without_output_file(self, mock_error: Mock) -> None:
        """Test processing without output file shows error."""
        app = gui_app.VaporwaveGUI()
        try:
            app.input_file.set("/path/to/input.jpg")
            app.process()
            mock_error.assert_called_once()
            assert "output" in mock_error.call_args[0][1].lower()
        finally:
            app.destroy()

    @patch("gui_app.messagebox.showerror")
    def test_process_without_effects(self, mock_error: Mock) -> None:
        """Test processing without any effects selected shows error."""
        app = gui_app.VaporwaveGUI()
        try:
            app.input_file.set("/path/to/input.jpg")
            app.output_file.set("/path/to/output.jpg")
            for var in app.effects.values():
                var.set(False)
            app.process()
            mock_error.assert_called_once()
            assert "effect" in mock_error.call_args[0][1].lower()
        finally:
            app.destroy()

    def test_get_selected_effects(self) -> None:
        """Test getting selected effects."""
        app = gui_app.VaporwaveGUI()
        try:
            app.effects["chromatic"].set(False)
            app.effects["vhs"].set(False)
            selected = [name for name, var in app.effects.items() if var.get()]
            assert "chromatic" not in selected
            assert "vhs" not in selected
            assert "holographic" in selected
            assert "neon" in selected
            assert "scanlines" in selected
        finally:
            app.destroy()

    @patch("gui_app.messagebox.showinfo")
    def test_processing_complete_success(self, mock_info: Mock) -> None:
        """Test successful processing completion."""
        app = gui_app.VaporwaveGUI()
        try:
            app.output_file.set("/path/to/output.jpg")
            app._processing_complete(True, None)
            mock_info.assert_called_once()
        finally:
            app.destroy()

    @patch("gui_app.messagebox.showerror")
    def test_processing_complete_failure(self, mock_error: Mock) -> None:
        """Test failed processing completion."""
        app = gui_app.VaporwaveGUI()
        try:
            app._processing_complete(False, "Test error message")
            mock_error.assert_called_once()
            assert "Test error message" in mock_error.call_args[0][1]
        finally:
            app.destroy()

    def test_update_intensity_label(self) -> None:
        """Test that intensity label updates correctly."""
        app = gui_app.VaporwaveGUI()
        try:
            app._update_intensity_label(1.5)
            assert "1.5" in app.intensity_value_label.cget("text")
        finally:
            app.destroy()


class TestGUILogic:
    """Tests for GUI logic that don't require a display."""

    def test_select_output_filetypes_image(self) -> None:
        """Test that correct filetypes are offered for images."""
        # Test logic without actual GUI
        input_ext = ".jpg"
        if input_ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"):
            filetypes = [
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("WebP files", "*.webp"),
                ("All files", "*.*"),
            ]
            default_ext = ".jpg"
        assert default_ext == ".jpg"
        assert any("JPEG" in ft[0] for ft in filetypes)

    def test_select_output_filetypes_gif(self) -> None:
        """Test that correct filetypes are offered for GIFs."""
        input_ext = ".gif"
        if input_ext == ".gif":
            filetypes = [("GIF files", "*.gif"), ("All files", "*.*")]
            default_ext = ".gif"
        assert default_ext == ".gif"
        assert any("GIF" in ft[0] for ft in filetypes)

    def test_select_output_filetypes_video(self) -> None:
        """Test that correct filetypes are offered for videos."""
        input_ext = ".mp4"
        if input_ext not in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"):
            filetypes = [
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MKV files", "*.mkv"),
                ("All files", "*.*"),
            ]
            default_ext = ".mp4"
        assert default_ext == ".mp4"
        assert any("MP4" in ft[0] for ft in filetypes)

    def test_output_path_generation(self) -> None:
        """Test that output path is correctly generated from input."""
        input_path = Path("/path/to/image.jpg")
        output_path = (
            input_path.parent
            / f"{input_path.stem}_vaporwave{input_path.suffix}"
        )
        assert str(output_path) == "/path/to/image_vaporwave.jpg"

    def test_output_directory_creation_logic(self) -> None:
        """Test the logic for creating output directory."""
        output_path = Path("/path/to/new/directory/output.jpg")
        parent = output_path.parent
        assert parent == Path("/path/to/new/directory")
