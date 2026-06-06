"""
GoLingu - Translation Endpoints
POST /translate — translate text using Gemini.
"""

from fastapi import APIRouter, HTTPException, Request, status

from app.core.exceptions import (
    GeminiAuthError,
    GeminiRateLimitError,
    GeminiServiceError,
    TranslationError,
    UnsupportedLanguageError,
)
from app.core.logging import get_logger
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.gemini_service import gemini_service
from app.services.translation_service import TranslationService

logger = get_logger("api.translation")

router = APIRouter(prefix="/translate", tags=["Translation"])

# Per-endpoint service instance (stateless, safe to share)
_translation_service = TranslationService(gemini_service)


@router.post(
    "",
    response_model=TranslationResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate text",
    description=(
        "Translate a piece of text into the specified target language using "
        "Google Gemini. Source language is auto-detected when not provided."
    ),
    responses={
        400: {"description": "Bad request — unsupported language or empty text"},
        429: {"description": "Rate limit exceeded"},
        502: {"description": "Gemini API error"},
    },
)
async def translate(request: Request, body: TranslationRequest) -> TranslationResponse:
    """Translate text to the target language."""
    logger.info(
        f"POST /translate | "
        f"ip={request.client.host if request.client else 'unknown'} "
        f"target={body.targetLanguage} chars={len(body.text)}"
    )

    try:
        return await _translation_service.translate(body)

    except UnsupportedLanguageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "UNSUPPORTED_LANGUAGE", "message": exc.message, "detail": exc.detail},
        ) from exc

    except TranslationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "TRANSLATION_FAILED", "message": exc.message, "detail": exc.detail},
        ) from exc

    except GeminiAuthError as exc:
        logger.critical(f"Gemini auth failure: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": "GEMINI_AUTH_ERROR", "message": "AI service authentication failed."},
        ) from exc

    except GeminiRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"code": "RATE_LIMIT_EXCEEDED", "message": exc.message},
        ) from exc

    except GeminiServiceError as exc:
        logger.error(f"Gemini service error: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": "GEMINI_SERVICE_ERROR", "message": "AI service is unavailable. Please try again."},
        ) from exc

    except Exception as exc:
        logger.exception(f"Unhandled exception in /translate: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "INTERNAL_ERROR", "message": "An unexpected error occurred."},
        ) from exc
