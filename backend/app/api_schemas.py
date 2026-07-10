"""Pydantic schemas for the local support preview API."""

from typing import Literal

from pydantic import BaseModel, Field


class SupportPreviewRequest(BaseModel):
    """One player inquiry submitted for a deterministic local preview."""

    text: str = Field(..., min_length=1, description="Player inquiry text")
    language: Literal["ko", "en"] = Field(
        default="ko",
        description="Response draft language",
    )


class SupportPreviewResponse(BaseModel):
    """Combined support router and response template output."""

    text: str
    predicted_category: str
    urgency: str
    needs_human: bool
    suggested_response_type: str
    routing_reason: str
    response_draft: str
    internal_note: str
