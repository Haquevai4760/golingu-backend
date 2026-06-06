"""
GoLingu - Custom Exceptions
Domain-specific exceptions for clean error propagation.
"""

from typing import Any, Optional


class GoLinguBaseException(Exception):
    """Base exception for all GoLingu errors."""

    def __init__(self, message: str, detail: Optional[Any] = None) -> None:
        self.message = message
        self.detail = detail
        super().__init__(message)


class GeminiServiceError(GoLinguBaseException):
    """Raised when the Gemini API returns an unexpected error."""


class GeminiAuthError(GoLinguBaseException):
    """Raised when Gemini API authentication fails."""


class GeminiRateLimitError(GoLinguBaseException):
    """Raised when Gemini API rate limit is exceeded."""


class TranslationError(GoLinguBaseException):
    """Raised when a translation cannot be completed."""


class UnsupportedLanguageError(GoLinguBaseException):
    """Raised when the target language code is not supported."""


class InvalidRequestError(GoLinguBaseException):
    """Raised for malformed or logically invalid requests."""
