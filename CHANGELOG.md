# Changelog

All notable changes to the Vaporwave Processor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-30

### Added

- **Modern CustomTkinter GUI**: Complete rewrite of the graphical interface
  - Modern dark theme with vaporwave-inspired color palette (magenta, cyan, pink)
  - Improved visual design with emoji icons and larger fonts
  - Smoother slider controls and rounded button corners
  - Better responsive layout with proper grid configuration

### Changed

- **GUI Framework**: Migrated from Tkinter to CustomTkinter for modern look and feel
  - Replaced `tk.Tk` with `ctk.CTk` as base window class
  - Updated all widgets to CustomTkinter equivalents (CTkButton, CTkEntry, etc.)
  - Status messages now use color-coded feedback (green/orange/red)

### Dependencies

- Added `customtkinter>=5.2.0` as new dependency

## [1.1.0] - 2026-01-30

### Added

- **Logging Infrastructure**: Centralized logging system with configurable log levels
  - New `src/logging_config.py` module with `get_logger()` and `configure_logging()` functions
  - Support for console and file logging with customizable formats
  - Runtime log level adjustment via `set_log_level()`

- **Custom Exception Hierarchy**: Structured exception handling for better error management
  - `VaporwaveError`: Base exception class with details support
  - `ProcessingError`: For media processing failures with input/output path context
  - `EffectError`: For effect-specific failures
  - `UnsupportedFormatError`: For unsupported file format errors
  - `OutputWriteError`: For file writing failures

- **Effect Name Enum**: Type-safe effect names via `EffectName` StrEnum
  - `EffectName.CHROMATIC`, `EffectName.HOLOGRAPHIC`, etc.
  - `EFFECT_REGISTRY` for effect class lookup
  - `get_effect_class()` helper function

- **Enhanced Configuration Management**:
  - TOML configuration file support (`vaporwave.toml`)
  - Environment variable overrides with `VAPORWAVE_` prefix
  - `load_config_from_file()` and `reset_config()` functions
  - Auto-discovery of config files in current directory and home

- **Documentation Files**:
  - `CHANGELOG.md` for version history
  - `CONTRIBUTING.md` for contribution guidelines

### Changed

- **VaporwaveProcessor Class**:
  - Now uses `pathlib.Path` for all file operations
  - Constructor accepts `log_level` parameter instead of `verbose` boolean
  - Uses proper exception raising instead of returning boolean success flags
  - Proper resource cleanup with `try/finally` blocks for video/GIF processing

- **Effect Classes**:
  - Removed `verbose` parameter from constructors
  - Now use centralized logging via `logger.info()` instead of `print()`
  - Added `_log_apply()` method in base class for consistent logging

- **GUI Application**:
  - Uses `pathlib.Path` for file path handling
  - Integrated with logging system
  - Effect checkboxes now dynamically generated from `EffectName` enum
  - Better error handling with specific exception types

- **Configuration**:
  - Singleton pattern for config instances (thread-safer)
  - Added `IMAGE_FORMATS` tuple to `ProcessingConfig`
  - Type annotations improved with `tuple[str, ...]`

### Fixed

- Removed try/except import fallbacks that caused import issues
- Fixed potential resource leaks in video/GIF processing
- Proper context managers for file operations

### Developer Experience

- Added `tomli` as optional dependency for Python < 3.11
- Updated `pyproject.toml` with proper metadata and URLs
- Added `Typing :: Typed` classifier

## [1.0.0] - 2026-01-15

### Added

- Initial release
- Five vaporwave effects: chromatic aberration, holographic, neon glow, scanlines, VHS
- Support for images (JPG, PNG, BMP, TIFF, WebP)
- Support for videos (MP4, AVI, MOV, MKV, WMV)
- Support for animated GIFs
- Tkinter-based GUI application
- Command-line interface
- Configurable effect intensity (0.1 - 5.0)
- Progress bars for video/GIF processing
- Chunked GIF processing for memory efficiency

[Unreleased]: https://github.com/EPW80/effect_processor/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/EPW80/effect_processor/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/EPW80/effect_processor/releases/tag/v1.0.0
