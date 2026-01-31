"""Centralized logging configuration for the vaporwave processor.

This module provides a unified logging setup with configurable log levels,
formatters, and handlers for both console and file output.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Literal

# Package-level logger name
LOGGER_NAME = "vaporwave_processor"

# Log format strings
CONSOLE_FORMAT = "%(levelname)s: %(message)s"
DETAILED_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
FILE_FORMAT = (
    "%(asctime)s | %(name)s | %(levelname)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance for the given module name.

    Args:
        name: The module name. If None, returns the root package logger.
              For submodules, use __name__ to get a properly namespaced logger.

    Returns:
        A configured Logger instance.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    if name is None:
        return logging.getLogger(LOGGER_NAME)

    # Ensure child loggers are properly namespaced under the package
    if not name.startswith(LOGGER_NAME) and name != LOGGER_NAME:
        # For external modules or short names, prefix with package name
        if "." not in name:
            name = f"{LOGGER_NAME}.{name}"

    return logging.getLogger(name)


def configure_logging(
    level: LogLevel = "INFO",
    log_file: Path | str | None = None,
    verbose: bool = False,
) -> logging.Logger:
    """Configure the package logging with console and optional file output.

    Args:
        level: The minimum log level to capture. Defaults to INFO.
        log_file: Optional path to a log file. If provided, logs will also
                  be written to this file with detailed formatting.
        verbose: If True, sets level to DEBUG and uses detailed console format.

    Returns:
        The configured root package logger.

    Example:
        >>> configure_logging(level="DEBUG", log_file="processing.log")
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug message will appear")
    """
    # Get or create the root package logger
    logger = logging.getLogger(LOGGER_NAME)

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Set effective level
    effective_level = "DEBUG" if verbose else level
    logger.setLevel(getattr(logging, effective_level))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = DETAILED_FORMAT if verbose else CONSOLE_FORMAT
    console_handler.setFormatter(logging.Formatter(console_format))
    console_handler.setLevel(getattr(logging, effective_level))
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file is not None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
        file_handler.setLevel(logging.DEBUG)  # Capture all levels to file
        logger.addHandler(file_handler)

    # Prevent propagation to root logger to avoid duplicate messages
    logger.propagate = False

    return logger


def set_log_level(level: LogLevel) -> None:
    """Update the log level for the package logger at runtime.

    Args:
        level: The new log level to set.

    Example:
        >>> set_log_level("DEBUG")  # Enable debug output
        >>> set_log_level("WARNING")  # Reduce verbosity
    """
    logger = logging.getLogger(LOGGER_NAME)
    numeric_level = getattr(logging, level)
    logger.setLevel(numeric_level)

    # Update all handlers too
    for handler in logger.handlers:
        handler.setLevel(numeric_level)


# Initialize with default configuration on import
_default_logger = configure_logging()
