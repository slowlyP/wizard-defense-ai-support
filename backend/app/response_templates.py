"""
Safe Korean response draft templates for support router results.

This module is a local prototype only. It does not call external APIs and does
not generate final customer-service decisions such as refunds or compensation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class ResponseDraft:
    response_draft: str
    internal_note: str


BASE_TEMPLATES = {
    "guide_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 플레이 방법과 운영 팁에 가까운 문의로 확인됩니다. "
        "PC 환경에서는 마우스로 마법사를 선택해 중앙 전장 안에서 드래그 배치하고, 적 이동 경로에 공격이 자주 닿도록 위치를 조정해 보세요. "
        "초반에는 안정적인 조합을 구성한 뒤 층과 적 구성에 맞춰 배치를 바꾸는 것이 좋습니다."
    ),
    "acquisition_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 마법사 획득, 소환, 등급 또는 등장 확률 안내에 가까운 문의로 확인됩니다. "
        "마법사 획득 결과는 현재 Steam demo 또는 Windows build에 적용된 소환 규칙에 따라 달라질 수 있습니다. "
        "정확한 등급과 확률 조건은 실행 중인 build의 게임 내 안내를 확인해 주세요."
    ),
    "growth_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 마법사 성장, 레벨업, 경험치, 성장 재료 또는 레조넌스 관련 문의로 확인됩니다. "
        "보유한 마법사의 성장 재료, 경험치, 단계 조건은 현재 PC build의 게임 내 안내를 기준으로 확인해 주세요. "
        "레조넌스와 성장 보너스는 신규 획득과 구분되는 성장 시스템입니다."
    ),
    "tower_progress_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 층 진행, 잠금 해제, 보스, 층 보상 또는 타워 진행 조건에 가까운 문의로 확인됩니다. "
        "다음 floor/stage 진행 여부는 현재 Steam demo 또는 Windows build의 진행 상태와 해금 조건에 따라 달라질 수 있습니다. "
        "보스 층이나 보상 조건을 확인할 때는 현재 도전 중인 층과 완료 상태를 함께 확인해 주세요."
    ),
    "skill_combat_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 스킬 효과, 쿨타임, 피해 계산, 타격 판정 또는 전투 상호작용 관련 문의로 확인됩니다. "
        "스킬 결과는 대상, 범위, 발동 조건, 상태 효과와 현재 PC build에 따라 달라질 수 있습니다. "
        "기대와 다르게 보이면 사용한 마법사, 대상 적, floor/stage와 전투 상황을 함께 확인해 주세요."
    ),
    "bug_triage": (
        "제보해 주셔서 감사합니다. 이 내용은 실제 동작 오류나 진행 문제 가능성이 있어 검토가 필요한 문의로 확인됩니다. "
        "확인을 위해 재현 순서, floor/stage, 마법사 조합, 오류 화면과 사용한 Windows/Steam demo build를 알려주세요. "
        "화면 표시 문제라면 PC 해상도와 fullscreen/windowed 상태도 함께 남겨 주시면 검토에 도움이 됩니다."
    ),
    "balance_feedback_ack": (
        "의견을 보내주셔서 감사합니다. 이 내용은 밸런스, 비용, 확률, 효율 또는 특정 조합의 강약에 대한 피드백으로 확인됩니다. "
        "보내주신 내용은 Steam demo와 PC playtest의 밸런스 검토 참고 자료로 정리할 수 있습니다. "
        "다만 조정 여부나 적용 시점은 확정해서 안내드리기 어렵습니다."
    ),
}


TYPE_NOTES = {
    "guide_answer": "자동 안내 가능: PC 마우스 플레이와 운영 팁 중심의 문의입니다.",
    "acquisition_answer": "자동 안내 가능: 현재 PC build의 마법사 획득 규칙 문의입니다.",
    "growth_answer": "자동 안내 가능: PC build의 성장, 경험치, 레조넌스 안내 문의입니다.",
    "tower_progress_answer": "자동 안내 가능: PC build의 floor/stage 진행 조건 문의입니다.",
    "skill_combat_answer": "자동 안내 가능: PC build의 스킬/전투 규칙 안내 문의입니다.",
    "bug_triage": "사람 검토 필요: Windows/Steam demo 재현 정보 확인이 필요합니다.",
    "balance_feedback_ack": "사람 검토 필요: Steam demo/PC playtest 밸런스 참고 의견입니다.",
}


def _human_review_suffix(urgency: str) -> str:
    if urgency == "high":
        return (
            " 현재 문의는 우선 확인이 필요한 사례로 분류되었으므로, 재현 단계와 발생 시점을 최대한 구체적으로 남겨 주시면 검토에 도움이 됩니다."
        )
    return " 이 문의는 담당 검토가 필요할 수 있으며, 확인 과정에서 추가 정보 요청이 있을 수 있습니다."


def generate_response_template(route: Dict) -> Dict:
    """Create a safe Korean response draft from support router output fields."""
    response_type = route.get("suggested_response_type", "guide_answer")
    urgency = route.get("urgency", "low")
    needs_human = bool(route.get("needs_human", False))
    category = route.get("predicted_category", "unknown")
    routing_reason = route.get("routing_reason", "")

    draft = BASE_TEMPLATES.get(response_type, BASE_TEMPLATES["guide_answer"])
    note = TYPE_NOTES.get(response_type, TYPE_NOTES["guide_answer"])

    if needs_human:
        draft = f"{draft}{_human_review_suffix(urgency)}"
        note = f"{note} Router reason: {routing_reason}"
    else:
        note = f"{note} predicted_category={category}, urgency={urgency}."

    if urgency == "high" and "재현" not in draft:
        draft = (
            f"{draft} 문제 확인을 위해 재현 순서, 발생한 층, 사용한 마법사, 발생 시점을 함께 알려주세요."
        )

    return asdict(ResponseDraft(response_draft=draft, internal_note=note))
