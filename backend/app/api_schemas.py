"""Pydantic schemas for the local support preview API."""

from pydantic import BaseModel, Field


class SupportPreviewRequest(BaseModel):
    """One player inquiry submitted for a deterministic local preview."""

    text: str = Field(..., min_length=1, description="Korean player inquiry text")


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
