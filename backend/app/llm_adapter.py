"""Provider-neutral interface and deterministic local mock implementation.

No class in this module calls a network, external API, or real language model.
The mock validates adapter boundaries and can later be replaced behind the same
interface only after a separately approved provider-integration task.
"""

from __future__ import annotations

from typing import Protocol

from .llm_prompt_builder import MockPrompt


class LLMAdapter(Protocol):
    name: str

    def generate_draft(self, prompt: MockPrompt) -> str:
        """Return a draft for a previously sanitized prompt."""


class MockLLMAdapter:
    """Local deterministic adapter; it is not an actual LLM integration."""

    name = "local_deterministic_mock"

    def generate_draft(self, prompt: MockPrompt) -> str:
        if prompt.needs_human_review:
            if prompt.language == "en":
                return (
                    "This inquiry requires human review. Please provide the situation, time, build, and a screenshot through an approved support process. "
                    "This local mock does not promise a refund, compensation, restoration, a certain resolution, or a patch date."
                )
            return (
                "이 문의는 사람 검토가 필요합니다. 승인된 지원 절차에 발생 상황, 시각, build와 screenshot을 남겨 주세요. "
                "이 local mock은 민감 요청의 자동 처리나 해결 일정을 확정하지 않습니다."
            )

        if prompt.context:
            evidence = prompt.context[0]
            if prompt.language == "en":
                return f"Based on the retrieved local support context: {evidence}"
            return f"검색된 로컬 지원 근거를 기준으로 안내합니다: {evidence}"

        if prompt.language == "en":
            return "The local mock has no verified retrieval context. Please use the deterministic template response."
        return "로컬 mock에서 확인된 검색 근거가 없습니다. 기존 deterministic template 응답을 사용해 주세요."
