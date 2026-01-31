# Vaporwave Processor Test Suite

This directory contains comprehensive tests for the Vaporwave Processor library.

## Test Structure

```
tests/
├── conftest.py           # Shared pytest fixtures
├── test_effects.py       # Unit tests for individual effects
├── test_processor.py     # Integration tests for processor pipeline
├── test_config.py        # Tests for configuration management
└── test_gui.py          # Tests for GUI application
```

## Running Tests

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html --cov-report=term
```

### Run Specific Test Files

```bash
# Run only effect tests
pytest tests/test_effects.py

# Run only processor tests
pytest tests/test_processor.py

# Run only GUI tests
pytest tests/test_gui.py

# Run only config tests
pytest tests/test_config.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_effects.py::TestChromaticAberrationEffect

# Run a specific test function
pytest tests/test_effects.py::TestChromaticAberrationEffect::test_apply_basic

# Run tests matching a pattern
pytest -k "chromatic"
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Output Capture Disabled

```bash
pytest -s
```

## Test Categories

### Unit Tests (test_effects.py)

Tests individual effect implementations:
- ChromaticAberrationEffect
- HolographicEffect
- NeonGlowEffect
- ScanlinesEffect
- VHSEffect

Each effect is tested for:
- Proper initialization
- Intensity clamping
- Basic application
- Output shape preservation
- Effect-specific behavior

### Integration Tests (test_processor.py)

Tests the complete processor pipeline:
- Image processing
- Video processing
- GIF processing
- Effect combinations
- Error handling
- Intensity variations

### Configuration Tests (test_config.py)

Tests configuration management:
- Default values
- Configuration updates
- Singleton behavior
- Error handling

### GUI Tests (test_gui.py)

Tests the GUI application:
- Widget initialization
- File selection
- Effect toggling
- Processing workflow
- Error handling

## Fixtures

Common fixtures are defined in `conftest.py`:

- `sample_image`: 100x100 gradient image
- `solid_color_image`: Solid color test image
- `sample_image_file`: Image file on disk
- `sample_video_file`: 10-frame test video
- `sample_gif_file`: 5-frame test GIF
- `temp_dir`: Temporary directory for test files
- `intensity_values`: Common intensity test values
- `all_effects`: List of all available effects

## Writing New Tests

When adding new effects or features:

1. Add unit tests in `test_effects.py` for new effects
2. Add integration tests in `test_processor.py` for new processing features
3. Add GUI tests in `test_gui.py` for new UI components
4. Add shared fixtures to `conftest.py` if reusable

### Example Test

```python
def test_new_feature(sample_image: np.ndarray) -> None:
    """Test description."""
    # Arrange
    processor = VaporwaveProcessor(intensity=1.0)

    # Act
    result = processor.some_new_method(sample_image)

    # Assert
    assert result.shape == sample_image.shape
    assert not np.array_equal(result, sample_image)
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. The test suite:

- Uses temporary files and directories
- Cleans up after itself
- Runs deterministically
- Provides clear failure messages
- Supports parallel execution

## Coverage Goals

- Overall coverage: >85%
- Core processor: >90%
- Individual effects: >85%
- Configuration: >90%
- GUI: >70% (GUI testing has inherent limitations)
