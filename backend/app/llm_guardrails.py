"""Deterministic output guardrails for mock and future adapter drafts."""

from __future__ import annotations

import re
from dataclasses import dataclass


FORBIDDEN_PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "refund_promise": (
        re.compile(r"환불(?:해|을)[^.!?]{0,20}(?:드리|보장|확정)"),
        re.compile(r"\b(?:we will|will|guarantee(?:d)?)\s+(?:a\s+)?refund\b", re.IGNORECASE),
        re.compile(r"\brefund (?:is )?guaranteed\b", re.IGNORECASE),
    ),
    "compensation_promise": (
        re.compile(r"보상(?:해|을)[^.!?]{0,20}(?:드리|지급|보장|확정)"),
        re.compile(r"\b(?:we will|will|guarantee(?:d)?)\s+(?:provide\s+)?compensation\b", re.IGNORECASE),
    ),
    "restoration_promise": (
        re.compile(r"복구[^.!?]{0,24}(?:드리|드립|보장|확정)"),
        re.compile(r"\b(?:we will|will|guarantee(?:d)?)\s+restore\b", re.IGNORECASE),
        re.compile(r"\brestoration (?:is )?guaranteed\b", re.IGNORECASE),
    ),
    "guaranteed_fix": (
        re.compile(r"(?:반드시|확실히)[^.!?]{0,20}(?:수정|해결)"),
        re.compile(r"\bguaranteed fix\b|\bwill definitely (?:fix|resolve)\b", re.IGNORECASE),
    ),
    "patch_date_promise": (
        re.compile(r"(?:패치|patch)[^.!?]{0,24}(?:날짜|일정|적용일)[^.!?]{0,12}(?:확정|보장)"),
        re.compile(r"\b(?:confirmed|guaranteed) patch date\b|\bpatch date (?:is )?confirmed\b", re.IGNORECASE),
    ),
}


@dataclass(frozen=True)
class GuardrailResult:
    is_safe: bool
    violations: tuple[str, ...]
    sanitized_draft: str


def _safe_fallback(language: str) -> str:
    if language == "en":
        return (
            "This inquiry requires human review. Please provide only the necessary situation, time, build, and screenshot through an approved support process. "
            "No refund, compensation, restoration, guaranteed fix, or patch date is promised."
        )
    return (
        "이 문의는 사람 검토가 필요합니다. 승인된 지원 절차에 필요한 발생 상황, 시각, build와 screenshot만 남겨 주세요. "
        "환불, 보상, 복구, guaranteed fix 또는 patch date를 약속하지 않습니다."
    )


def apply_llm_guardrails(draft: str, language: str = "ko", sensitive: bool = False) -> GuardrailResult:
    """Detect forbidden promises and return a fixed safe fallback when needed."""
    violations = tuple(
        name
        for name, patterns in FORBIDDEN_PATTERNS.items()
        if any(pattern.search(draft) for pattern in patterns)
    )
    selected_language = "en" if language == "en" else "ko"
    sanitized = _safe_fallback(selected_language) if violations or sensitive else draft.strip()
    return GuardrailResult(
        is_safe=not violations,
        violations=violations,
        sanitized_draft=sanitized,
    )
