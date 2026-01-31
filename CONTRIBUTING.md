# Contributing to Vaporwave Processor

Thank you for your interest in contributing to the Vaporwave Processor! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Adding New Effects](#adding-new-effects)

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/effect_processor.git
   cd effect_processor
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/EPW80/effect_processor.git
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv recommended)

### Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Verify Installation

```bash
# Run tests
pytest

# Run linting
ruff check src tests

# Run type checking
mypy src
```

## Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes, following the [coding standards](#coding-standards)

3. Add or update tests as needed

4. Run tests and linting locally before committing

5. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add: new holographic shimmer effect variant"
   git commit -m "Fix: handle alpha channel in PNG processing"
   ```

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use `ruff` for linting and formatting
- Maximum line length: 88 characters
- Use double quotes for strings

### Type Hints

All code must include type hints:

```python
def process_image(
    self,
    input_path: Path,
    output_path: Path,
    effects: list[str],
) -> bool:
    """Process an image with the specified effects."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def apply(self, image: np.ndarray) -> np.ndarray:
    """Apply the effect to an image.

    Args:
        image: Input image as numpy array (BGR format, uint8).

    Returns:
        Processed image as numpy array (BGR format, uint8).

    Raises:
        EffectError: If the effect cannot be applied.
    """
    ...
```

### Logging

Use the centralized logging system instead of `print()`:

```python
from src.logging_config import get_logger

logger = get_logger(__name__)

logger.debug("Detailed debugging info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred: %s", error)
```

### Exception Handling

Use specific exceptions from `src.exceptions`:

```python
from src.exceptions import ProcessingError, EffectError

# Instead of:
# return False

# Do:
raise ProcessingError(
    "Failed to load image",
    input_path=input_path,
    details={"reason": "file corrupted"},
)
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_effects.py

# Run specific test
pytest tests/test_effects.py::test_chromatic_aberration

# Skip slow tests
pytest -m "not slow"
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use fixtures from `conftest.py`
- Aim for high coverage of new code

Example test:

```python
import pytest
import numpy as np
from src.effects import ChromaticAberrationEffect

def test_chromatic_aberration_applies_shift(sample_image):
    """Test that chromatic aberration shifts color channels."""
    effect = ChromaticAberrationEffect(intensity=1.0)
    result = effect.apply(sample_image)

    # Result should be different from input
    assert not np.array_equal(result, sample_image)
    # Result should have same shape
    assert result.shape == sample_image.shape
```

## Submitting Changes

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (for visual changes)

4. Wait for review and address any feedback

## Adding New Effects

To add a new effect:

1. Create a new file in `src/effects/`:
   ```python
   # src/effects/glitch.py
   """Glitch effect implementation."""

   from __future__ import annotations

   import numpy as np

   from .base import BaseEffect


   class GlitchEffect(BaseEffect):
       """Glitch effect that creates digital corruption artifacts."""

       @property
       def name(self) -> str:
           return "glitch"

       def apply(self, image: np.ndarray) -> np.ndarray:
           self._log_apply()
           # Your effect implementation here
           return result
   ```

2. Add to `src/effects/__init__.py`:
   ```python
   from .glitch import GlitchEffect

   class EffectName(StrEnum):
       # ... existing effects
       GLITCH = "glitch"

   EFFECT_REGISTRY: dict[EffectName | str, type[BaseEffect]] = {
       # ... existing effects
       EffectName.GLITCH: GlitchEffect,
   }

   __all__ = [
       # ... existing exports
       "GlitchEffect",
   ]
   ```

3. Add configuration parameters to `src/config.py` if needed

4. Add tests in `tests/test_effects.py`

5. Update documentation in `README.md`

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Help with contributions

Thank you for contributing! 🌊✨
