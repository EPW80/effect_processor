"""Custom exception hierarchy for the vaporwave processor.

This module defines specific exceptions for different error scenarios,
enabling better error handling and more informative error messages.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class VaporwaveError(Exception):
    """Base exception for all vaporwave processor errors.

    All custom exceptions inherit from this class, allowing callers
    to catch all package-specific errors with a single except clause.
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error description.
            details: Optional dictionary with additional context.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            detail_str = ", ".join(f"{k}={v!r}" for k, v in self.details.items())
            return f"{self.message} ({detail_str})"
        return self.message


class ConfigurationError(VaporwaveError):
    """Raised when there is a configuration-related error.

    Examples:
        - Invalid configuration values
        - Missing required configuration
        - Configuration file parsing errors
    """

    pass


class ProcessingError(VaporwaveError):
    """Raised when media processing fails.

    This exception is used for errors during image, video, or GIF processing
    that are not related to specific effects.
    """

    def __init__(
        self,
        message: str,
        input_path: Path | str | None = None,
        output_path: Path | str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the processing error.

        Args:
            message: Human-readable error description.
            input_path: The input file that was being processed.
            output_path: The intended output file path.
            details: Optional dictionary with additional context.
        """
        details = details or {}
        if input_path:
            details["input_path"] = str(input_path)
        if output_path:
            details["output_path"] = str(output_path)
        super().__init__(message, details)
        self.input_path = Path(input_path) if input_path else None
        self.output_path = Path(output_path) if output_path else None


class EffectError(VaporwaveError):
    """Raised when an effect application fails.

    This exception is specific to errors occurring within effect processing,
    such as invalid parameters or effect-specific failures.
    """

    def __init__(
        self,
        message: str,
        effect_name: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the effect error.

        Args:
            message: Human-readable error description.
            effect_name: The name of the effect that failed.
            details: Optional dictionary with additional context.
        """
        details = details or {}
        if effect_name:
            details["effect"] = effect_name
        super().__init__(message, details)
        self.effect_name = effect_name


class UnsupportedFormatError(ProcessingError):
    """Raised when the input file format is not supported.

    This is a specific type of processing error for format-related issues.
    """

    def __init__(
        self,
        file_path: Path | str,
        detected_format: str | None = None,
        supported_formats: list[str] | None = None,
    ) -> None:
        """Initialize the unsupported format error.

        Args:
            file_path: Path to the unsupported file.
            detected_format: The format that was detected (if known).
            supported_formats: List of formats that are supported.
        """
        details: dict[str, Any] = {}
        if detected_format:
            details["detected_format"] = detected_format
        if supported_formats:
            details["supported_formats"] = supported_formats

        message = f"Unsupported file format: {file_path}"
        super().__init__(message, input_path=file_path, details=details)
        self.detected_format = detected_format
        self.supported_formats = supported_formats or []


class FileNotFoundError(ProcessingError):
    """Raised when an input file does not exist.

    Note: This shadows the built-in FileNotFoundError intentionally
    to provide more context about the processing operation.
    """

    def __init__(self, file_path: Path | str) -> None:
        """Initialize the file not found error.

        Args:
            file_path: Path to the missing file.
        """
        message = f"Input file not found: {file_path}"
        super().__init__(message, input_path=file_path)


class OutputWriteError(ProcessingError):
    """Raised when writing output fails.

    This can occur due to permission issues, disk space, or invalid paths.
    """

    def __init__(
        self,
        output_path: Path | str,
        reason: str | None = None,
    ) -> None:
        """Initialize the output write error.

        Args:
            output_path: Path where writing failed.
            reason: Optional reason for the failure.
        """
        message = f"Failed to write output: {output_path}"
        details = {"reason": reason} if reason else None
        super().__init__(message, output_path=output_path, details=details)
        self.reason = reason
