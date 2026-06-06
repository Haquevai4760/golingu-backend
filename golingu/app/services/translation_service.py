"""
GoLingu - Translation Service
Orchestrates translation using GeminiService with prompt engineering.
"""

from typing import Optional

from app.core.exceptions import TranslationError, UnsupportedLanguageError
from app.core.logging import get_logger
from app.models.language import SUPPORTED_LANGUAGES, get_language, is_supported_language
from app.schemas.translation import TranslationRequest, TranslationResponse
from app.services.gemini_service import GeminiService

logger = get_logger("services.translation")


TRANSLATION_PROMPT_TEMPLATE = """\
You are GoLingu, a professional translation engine. Your sole task is to translate the given text accurately.

Rules:
- Output ONLY the translated text. No explanations, no notes, no alternatives, no quotation marks.
- Preserve the original tone, formatting, and punctuation as closely as the target language allows.
- If the source and target language are the same, return the text unchanged.
- Do not translate proper nouns unless they have a widely accepted equivalent in the target language.
- Source language: {source_language}
- Target language: {target_language_name} ({target_language_code})

Text to translate:
{text}
"""


class TranslationService:
    """
    High-level translation service.
    Validates input, builds prompts, and returns structured responses.
    """

    def __init__(self, gemini: GeminiService) -> None:
        self._gemini = gemini

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text to the specified target language.

        Args:
            request: Validated TranslationRequest.

        Returns:
            TranslationResponse with the translated text and metadata.

        Raises:
            UnsupportedLanguageError: If the language code is not supported.
            TranslationError: If translation fails for any reason.
        """
        self._validate_language(request.targetLanguage)
        if request.sourceLanguage:
            self._validate_language(request.sourceLanguage)

        target_lang = get_language(request.targetLanguage)
        source_lang_name = self._resolve_source_language(request.sourceLanguage)

        logger.info(
            f"Translating text | chars={len(request.text)} "
            f"src={request.sourceLanguage or 'auto'} "
            f"tgt={request.targetLanguage}"
        )

        prompt = TRANSLATION_PROMPT_TEMPLATE.format(
            source_language=source_lang_name,
            target_language_name=target_lang.name,
            target_language_code=target_lang.code,
            text=request.text,
        )

        try:
            translated = await self._gemini.generate(prompt)
        except Exception as exc:
            logger.error(f"Translation generation failed: {exc}")
            raise TranslationError(
                "Failed to generate translation.",
                detail=str(exc),
            ) from exc

        if not translated:
            raise TranslationError("Translation returned empty result.")

        logger.info(
            f"Translation complete | "
            f"input_chars={len(request.text)} output_chars={len(translated)}"
        )

        return TranslationResponse(
            translatedText=translated,
            sourceLanguage=request.sourceLanguage,
            targetLanguage=request.targetLanguage,
            characterCount=len(request.text),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_language(code: str) -> None:
        if not is_supported_language(code):
            supported = sorted(SUPPORTED_LANGUAGES.keys())
            raise UnsupportedLanguageError(
                f"Language code '{code}' is not supported.",
                detail=f"Supported codes: {', '.join(supported[:20])} … (and more)",
            )

    @staticmethod
    def _resolve_source_language(code: Optional[str]) -> str:
        if not code:
            return "auto-detect"
        lang = get_language(code)
        return f"{lang.name} ({lang.code})" if lang else code
