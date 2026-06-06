"""
GoLingu - Gemini Service
Low-level async wrapper around the Google Gemini API.
"""

import asyncio
from typing import Optional

import google.generativeai as genai
from google.api_core.exceptions import (
    GoogleAPICallError,
    InvalidArgument,
    PermissionDenied,
    ResourceExhausted,
)

from app.core.config import settings
from app.core.exceptions import (
    GeminiAuthError,
    GeminiRateLimitError,
    GeminiServiceError,
)
from app.core.logging import get_logger

logger = get_logger("services.gemini")


class GeminiService:
    """
    Async wrapper around Google Generative AI SDK.
    Handles authentication, retries, and error normalisation.
    """

    def __init__(self) -> None:
        self._model_name = settings.GEMINI_MODEL
        self._max_tokens = settings.GEMINI_MAX_TOKENS
        self._temperature = settings.GEMINI_TEMPERATURE
        self._model: Optional[genai.GenerativeModel] = None
        self._initialized = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Configure the Gemini client. Must be called once at startup."""
        if self._initialized:
            return

        if not settings.GEMINI_API_KEY:
            raise GeminiAuthError(
                "GEMINI_API_KEY environment variable is not set.",
            )

        genai.configure(api_key=settings.GEMINI_API_KEY)

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=self._max_tokens,
            temperature=self._temperature,
        )

        self._model = genai.GenerativeModel(
            model_name=self._model_name,
            generation_config=generation_config,
        )

        self._initialized = True
        logger.info(f"GeminiService initialised | model={self._model_name}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the text response.

        Args:
            prompt: The fully-formed prompt string.

        Returns:
            The model's text response.

        Raises:
            GeminiAuthError: On authentication failures.
            GeminiRateLimitError: When quota is exceeded.
            GeminiServiceError: On any other Gemini error.
        """
        if not self._initialized or self._model is None:
            raise GeminiServiceError("GeminiService has not been initialised.")

        logger.debug(f"Sending prompt to Gemini | chars={len(prompt)}")

        try:
            # Run the synchronous SDK call in a thread pool to avoid
            # blocking the event loop.
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._model.generate_content(prompt),
            )
            text = self._extract_text(response)
            logger.debug(f"Received response from Gemini | chars={len(text)}")
            return text

        except PermissionDenied as exc:
            logger.error(f"Gemini auth error: {exc}")
            raise GeminiAuthError(
                "Gemini API key is invalid or lacks permission.",
                detail=str(exc),
            ) from exc

        except ResourceExhausted as exc:
            logger.warning(f"Gemini rate limit hit: {exc}")
            raise GeminiRateLimitError(
                "Gemini API quota exceeded. Please retry later.",
                detail=str(exc),
            ) from exc

        except InvalidArgument as exc:
            logger.error(f"Gemini invalid argument: {exc}")
            raise GeminiServiceError(
                "Invalid request sent to Gemini API.",
                detail=str(exc),
            ) from exc

        except GoogleAPICallError as exc:
            logger.error(f"Gemini API error: {exc}")
            raise GeminiServiceError(
                "An error occurred while communicating with Gemini API.",
                detail=str(exc),
            ) from exc

        except Exception as exc:
            logger.exception(f"Unexpected Gemini error: {exc}")
            raise GeminiServiceError(
                "An unexpected error occurred in GeminiService.",
                detail=str(exc),
            ) from exc

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_text(response: genai.types.GenerateContentResponse) -> str:
        """Safely extract text from a Gemini response object."""
        try:
            text = response.text
            if not text:
                raise GeminiServiceError("Gemini returned an empty response.")
            return text.strip()
        except (AttributeError, ValueError) as exc:
            # response.text raises ValueError when the response is blocked
            candidate = response.candidates[0] if response.candidates else None
            finish_reason = getattr(
                getattr(candidate, "finish_reason", None), "name", "UNKNOWN"
            )
            raise GeminiServiceError(
                f"Gemini response was blocked or empty. finish_reason={finish_reason}",
                detail=str(exc),
            ) from exc


# Module-level singleton — shared across requests
gemini_service = GeminiService()
