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
        "마법사는 적 이동 경로를 고려해 공격이 자주 닿는 위치에 배치하고, 초반에는 안정적으로 버틸 수 있는 조합을 먼저 구성해 보세요. "
        "상황에 따라 속성 조합과 배치 위치를 바꾸면 더 안정적인 진행에 도움이 됩니다."
    ),
    "acquisition_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 마법사 획득, 소환, 등급 또는 등장 확률 안내에 가까운 문의로 확인됩니다. "
        "마법사 획득은 게임 내 소환과 획득 규칙에 따라 처리되며, 등급이나 등장 결과는 정해진 획득 방식에 따라 달라질 수 있습니다. "
        "정확한 수치나 조건은 현재 게임 내 안내와 관련 가이드 기준으로 확인하는 것이 좋습니다."
    ),
    "growth_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 마법사 성장, 레벨업, 경험치, 성장 재료 또는 레조넌스 관련 문의로 확인됩니다. "
        "이미 보유한 마법사를 강화하거나 성장시키는 경우에는 성장 재료, 경험치, 성장 단계 조건을 함께 확인해 주세요. "
        "레조넌스나 성장 보너스는 획득 문의와 구분되는 성장 시스템으로 안내하는 것이 적절합니다."
    ),
    "tower_progress_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 층 진행, 잠금 해제, 보스, 층 보상 또는 타워 진행 조건에 가까운 문의로 확인됩니다. "
        "다음 층 진행 여부는 현재 층 진행 상태와 조건 충족 여부에 따라 달라질 수 있습니다. "
        "보스 층이나 보상 조건이 궁금한 경우에는 현재 도전 중인 층과 진행 상황을 함께 확인해 주세요."
    ),
    "skill_combat_answer": (
        "문의해 주셔서 감사합니다. 이 내용은 스킬 효과, 쿨타임, 피해 계산, 타격 판정 또는 전투 상호작용 관련 문의로 확인됩니다. "
        "스킬은 대상, 범위, 발동 조건, 상태 효과에 따라 체감 결과가 달라질 수 있습니다. "
        "특정 스킬이 기대와 다르게 보이는 경우에는 사용한 마법사, 대상 적, 전투 상황을 함께 확인하는 것이 좋습니다."
    ),
    "bug_triage": (
        "제보해 주셔서 감사합니다. 이 내용은 실제 동작 오류나 진행 문제 가능성이 있어 검토가 필요한 문의로 확인됩니다. "
        "확인을 위해 발생한 상황, 재현 순서, 사용한 마법사나 층 정보, 오류가 발생한 화면을 가능한 범위에서 알려주세요. "
        "검토 후 원인 확인에 필요한 추가 정보가 있을 수 있습니다."
    ),
    "balance_feedback_ack": (
        "의견을 보내주셔서 감사합니다. 이 내용은 밸런스, 비용, 확률, 효율 또는 특정 조합의 강약에 대한 피드백으로 확인됩니다. "
        "보내주신 의견은 게임 밸런스 검토 참고 자료로 정리할 수 있습니다. "
        "다만 조정 여부나 적용 시점은 확정해서 안내드리기 어렵습니다."
    ),
}


TYPE_NOTES = {
    "guide_answer": "자동 안내 가능: 플레이 방법과 운영 팁 중심의 문의입니다.",
    "acquisition_answer": "자동 안내 가능: 마법사 획득 또는 소환 규칙 문의입니다.",
    "growth_answer": "자동 안내 가능: 성장, 경험치, 레조넌스 안내 문의입니다.",
    "tower_progress_answer": "자동 안내 가능: 층 진행과 보상 조건 안내 문의입니다.",
    "skill_combat_answer": "자동 안내 가능: 스킬/전투 규칙 안내 문의입니다.",
    "bug_triage": "사람 검토 필요: 오류 재현 정보와 상황 확인이 필요합니다.",
    "balance_feedback_ack": "사람 검토 필요: 밸런스 정책 판단에 참고할 피드백입니다.",
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
