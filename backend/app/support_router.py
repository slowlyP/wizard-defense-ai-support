"""
Local support routing prototype built on the improved rule classifier.

The router does not change classification behavior. It adds support-operation
fields that can be reviewed in a portfolio demo before any API server exists.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List

from .rule_classifier_v2 import classify_inquiry_v2


SUGGESTED_RESPONSE_TYPES = {
    "gameplay_guide": "guide_answer",
    "wizard_acquisition": "acquisition_answer",
    "wizard_growth": "growth_answer",
    "tower_progress": "tower_progress_answer",
    "skill_combat": "skill_combat_answer",
    "bug_report": "bug_triage",
    "feedback_balance": "balance_feedback_ack",
}


HIGH_RISK_BUG_SIGNALS = [
    "강제 종료",
    "크래시",
    "튕겨",
    "튕김",
    "저장",
    "사라졌",
    "사라지",
    "소모",
    "복구",
    "보상",
    "진행이 안",
    "멈춰",
    "멈춤",
]

MEDIUM_BUG_SIGNALS = [
    "깨져",
    "표시",
    "안 보여",
    "인식",
    "작동하지",
    "발동하지",
    "적용되지",
    "표시되지",
    "지급되지",
    "생성되지",
    "이상",
    "끊겨",
]

BALANCE_REVIEW_SIGNALS = [
    "너무",
    "지나치",
    "불공평",
    "조정",
    "밸런스",
    "효율",
    "비용 대비",
    "확률",
    "약한",
    "강한",
]

AMBIGUOUS_REVIEW_SIGNALS = [
    "설명과 다르게",
    "정상인가요",
    "버그인가요",
    "공지에",
    "보상 돌려",
]


@dataclass
class SupportRoute:
    predicted_category: str
    urgency: str
    needs_human: bool
    routing_reason: str
    suggested_response_type: str


def _has_any(text: str, keywords: List[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _bug_urgency(text: str) -> str:
    if _has_any(text, HIGH_RISK_BUG_SIGNALS):
        return "high"
    if _has_any(text, MEDIUM_BUG_SIGNALS):
        return "medium"
    return "medium"


def _category_reason(category: str) -> str:
    reasons = {
        "gameplay_guide": "플레이 방법, 배치, 조합, 운영 팁 문의로 판단해 guide 답변으로 라우팅합니다.",
        "wizard_acquisition": "마법사 소환, 획득, 등급, 등장 확률 문의로 판단해 획득 안내로 라우팅합니다.",
        "wizard_growth": "레벨업, 경험치, 성장 재료, 레조넌스 문의로 판단해 성장 안내로 라우팅합니다.",
        "tower_progress": "층 진행, 잠금 해제, 보스, 층 보상 문의로 판단해 타워 진행 안내로 라우팅합니다.",
        "skill_combat": "스킬 효과, 쿨타임, 피해 계산, 타격 판정 문의로 판단해 전투/스킬 안내로 라우팅합니다.",
        "bug_report": "실제 동작 실패나 손실 가능성이 있어 버그 재현 확인 절차로 라우팅합니다.",
        "feedback_balance": "강함/약함, 비용, 확률, 효율에 대한 평가로 판단해 밸런스 피드백 접수로 라우팅합니다.",
    }
    return reasons.get(category, "분류 신뢰도가 낮아 기본 가이드 답변으로 라우팅합니다.")


def route_inquiry(text: str) -> Dict:
    """Return support routing fields for one Korean player inquiry."""
    classifier_result = classify_inquiry_v2(text)
    category = classifier_result["category"]
    normalized = text.strip().lower() if isinstance(text, str) else ""

    urgency = classifier_result.get("urgency", "low")
    needs_human = bool(classifier_result.get("needs_human", False))
    reason = _category_reason(category)
    suggested_response_type = SUGGESTED_RESPONSE_TYPES.get(category, "guide_answer")

    # Operational override: bug reports with loss/progress signals need faster review.
    if category == "bug_report":
        urgency = _bug_urgency(normalized)
        needs_human = True
        if urgency == "high":
            reason = "진행 불가, 크래시, 보상/재화 손실 가능성이 있어 high 우선순위 버그 triage로 라우팅합니다."

    # Balance feedback is normally human-reviewed because it may affect tuning policy.
    elif category == "feedback_balance":
        urgency = "medium"
        needs_human = True
        if _has_any(normalized, BALANCE_REVIEW_SIGNALS):
            reason = "비용, 확률, 효율, 강약 평가가 포함되어 밸런스 검토 대상으로 라우팅합니다."

    # Feature-category predictions can still route to triage when failure signals appear.
    elif _has_any(normalized, HIGH_RISK_BUG_SIGNALS + MEDIUM_BUG_SIGNALS):
        urgency = _bug_urgency(normalized)
        needs_human = True
        suggested_response_type = "bug_triage"
        reason = "분류 category는 기능 문의이지만 실패, 미지급, 표시 오류 신호가 있어 버그 triage로 라우팅합니다."

    # Ambiguous feature questions can remain automated unless they hint at policy or mismatch.
    elif _has_any(normalized, AMBIGUOUS_REVIEW_SIGNALS):
        urgency = "medium"
        needs_human = True
        reason = "기능 설명과 실제 동작 차이를 언급해 사람 검토가 필요한 경계 사례로 라우팅합니다."

    route = SupportRoute(
        predicted_category=category,
        urgency=urgency,
        needs_human=needs_human,
        routing_reason=reason,
        suggested_response_type=suggested_response_type,
    )
    return asdict(route)
