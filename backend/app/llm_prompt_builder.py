"""Deterministic prompt-like input builder for the local mock adapter.

The builder does not send prompts anywhere. It redacts common secret and
private-data patterns before assembling a stable structure for local tests.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, Sequence

from .rag_retriever import RetrievalResult


REDACTION_PATTERNS = (
    re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.DOTALL | re.IGNORECASE),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b(?:card|account|order)[ _-]?(?:number|id)\s*[:=]\s*[^\s,;]+", re.IGNORECASE),
)


def redact_prompt_text(value: str) -> str:
    """Replace secret/private-data-looking text before local prompt assembly."""
    redacted = value
    for pattern in REDACTION_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return " ".join(redacted.split())


@dataclass(frozen=True)
class MockPrompt:
    language: str
    inquiry: str
    route_category: str
    needs_human_review: bool
    chunk_ids: tuple[str, ...]
    chunk_titles: tuple[str, ...]
    context: tuple[str, ...]
    prompt_text: str


def build_mock_llm_prompt(
    inquiry: str,
    language: str,
    route: Mapping[str, object],
    retrieved_chunks: Sequence[RetrievalResult],
) -> MockPrompt:
    """Build deterministic bilingual input for ``MockLLMAdapter`` only."""
    selected_language = "en" if language == "en" else "ko"
    chunk_ids = tuple(result.chunk.id for result in retrieved_chunks)
    chunk_titles = tuple(redact_prompt_text(result.chunk.title) for result in retrieved_chunks)
    context = tuple(redact_prompt_text(result.chunk.content) for result in retrieved_chunks)
    needs_review = bool(route.get("needs_human", False)) or any(
        result.chunk.requires_human_review for result in retrieved_chunks
    )
    safe_inquiry = redact_prompt_text(inquiry)
    category = str(route.get("predicted_category", "unknown"))
    context_lines = "\n".join(
        f"- [{chunk_id}] {title}: {content}"
        for chunk_id, title, content in zip(chunk_ids, chunk_titles, context)
    ) or "- [no_context]"
    if selected_language == "en":
        prompt_text = (
            "LOCAL MOCK PROMPT — NO EXTERNAL LLM CALL\n"
            f"Language: en\nCategory: {category}\nHuman review: {str(needs_review).lower()}\n"
            f"Inquiry: {safe_inquiry}\nRetrieved context:\n{context_lines}\n"
            "Constraint: Use only context; never promise refunds, compensation, restoration, fixes, or patch dates."
        )
    else:
        prompt_text = (
            "로컬 MOCK PROMPT — 외부 LLM 호출 없음\n"
            f"언어: ko\n카테고리: {category}\n사람 검토: {str(needs_review).lower()}\n"
            f"문의: {safe_inquiry}\n검색 근거:\n{context_lines}\n"
            "제약: 근거만 사용하고 환불, 보상, 복구, 수정 또는 패치 날짜를 약속하지 않는다."
        )
    return MockPrompt(
        language=selected_language,
        inquiry=safe_inquiry,
        route_category=category,
        needs_human_review=needs_review,
        chunk_ids=chunk_ids,
        chunk_titles=chunk_titles,
        context=context,
        prompt_text=prompt_text,
    )

