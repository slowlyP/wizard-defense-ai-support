"""Local-only FastAPI prototype for support routing and response previews."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .api_schemas import SupportPreviewRequest, SupportPreviewResponse
from .response_templates import generate_response_template
from .support_router import route_inquiry


app = FastAPI(
    title="Wizard Defense AI Support Local API",
    version="0.14.0",
    description="외부 서비스 없이 실행되는 로컬 support preview prototype입니다.",
)

# Local Vite origins only; production deployment should define its own allowlist.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return a small readiness response for local smoke checks."""
    return {"status": "ok"}


@app.post("/support/preview", response_model=SupportPreviewResponse)
def support_preview(payload: SupportPreviewRequest) -> SupportPreviewResponse:
    """Route an inquiry and build its deterministic response draft."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="text must not be blank")

    # Existing modules remain the single source of routing and template behavior.
    route = route_inquiry(text)
    template = generate_response_template(route)
    return SupportPreviewResponse(text=text, **route, **template)
