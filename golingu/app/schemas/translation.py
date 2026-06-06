"""
GoLingu - Pydantic Schemas
Request/response models with validation.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Translation Schemas
# ---------------------------------------------------------------------------

class TranslationRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The text to translate.",
        examples=["Hello World"],
    )
    targetLanguage: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="BCP-47 language code for the target language (e.g. 'bn', 'es', 'fr').",
        examples=["bn"],
    )
    sourceLanguage: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=10,
        description="BCP-47 language code for the source language. Auto-detected when omitted.",
        examples=["en"],
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must contain at least one non-whitespace character")
        return v.strip()

    @field_validator("targetLanguage", "sourceLanguage", mode="before")
    @classmethod
    def language_code_lowercase(cls, v: Optional[str]) -> Optional[str]:
        return v.strip().lower() if v else v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Hello World",
                    "targetLanguage": "bn",
                }
            ]
        }
    }


class TranslationResponse(BaseModel):
    translatedText: str = Field(
        ...,
        description="The translated text.",
        examples=["হ্যালো ওয়ার্ল্ড"],
    )
    sourceLanguage: Optional[str] = Field(
        default=None,
        description="Detected or provided source language code.",
    )
    targetLanguage: str = Field(
        ...,
        description="The target language code used.",
    )
    characterCount: int = Field(
        ...,
        description="Number of characters in the original text.",
    )


# ---------------------------------------------------------------------------
# Health Schemas
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    version: str = Field(..., examples=["1.0.0"])
    service: str = Field(..., examples=["GoLingu Translation API"])


# ---------------------------------------------------------------------------
# Error Schemas
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")
    detail: Optional[str] = Field(default=None, description="Additional context.")


class ErrorResponse(BaseModel):
    error: ErrorDetail
