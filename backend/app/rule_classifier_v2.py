"""
Improved rule-based classifier for dataset v2 experiments.

This module keeps the original rule classifier untouched. It adds transparent
priority rules based on the refined label boundary policy from data/labeling_guide.md.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from .schemas import InquiryResult


CATEGORY_LABELS = {
    "gameplay_guide",
    "wizard_acquisition",
    "wizard_growth",
    "tower_progress",
    "skill_combat",
    "bug_report",
    "feedback_balance",
}


BUG_HARD_SIGNALS = [
    "생성되지",
    "나오지 않",
    "나오지 않았",
    "진행이 안",
    "인식하지 못",
    "강제 종료",
    "크래시",
    "사라졌",
    "사라졌어요",
    "사라져서",
    "중복 지급",
    "두 번 지급",
    "적용되지",
    "발동했는데",
    "계속 움직",
    "경로를 벗어나",
    "줄고 새",
    "골드만 줄",
    "소모되었는데",
    "아무 일도",
    "멈",
    "깨져",
    "끊",
    "눌리지",
    "겹쳐",
    "허공",
    "바뀌지",
    "변하지",
    "다른 층",
    "화면 없이",
    "밖으로 튕",
    "프레임 드랍",
    "발생합니다",
    "이상합니다",
    "생긴 것처럼",
    "끝났는데",
    "계속 피해",
    "확인할 수 없습니다",
]

BUG_CONTEXT_TERMS = [
    "오류",
    "버그",
    "문제",
    "이상",
    "확인 부탁",
    "재현",
]

BALANCE_SIGNALS = [
    "너무",
    "지나치",
    "낮",
    "강한",
    "강력",
    "강하게",
    "약",
    "효율",
    "밸런스",
    "조정",
    "개선",
    "과도",
    "불리",
    "부담",
    "단조",
    "아쉽",
    "체감되지",
    "메타",
    "다양성",
    "가치",
    "위험도에 비해",
    "비해",
    "느낍",
    "요구량보다",
    "확률이 낮",
    "비용 대비",
    "성능 차이",
]

GROWTH_CONTEXT = [
    "성장",
    "레벨업",
    "레벨",
    "경험치",
    "성장 재료",
    "성장 보너스",
    "공격력 보너스",
    "레벨 보너스",
    "연구",
    "아케인",
    "레조넌스",
    "루미엘 축복",
    "재능",
    "성장 수치",
]

ACQUISITION_CONTEXT = [
    "소환",
    "획득",
    "얻",
    "뽑기",
    "등장 확률",
    "확률",
    "전설 마법사 등장",
    "시작 마법사",
    "새 마법사",
    "속성",
    "랜덤",
    "생성",
]

GUIDE_REQUESTS = [
    "추천",
    "팁",
    "운영",
    "전략",
    "흐름",
    "언제",
    "상황",
    "빌드",
    "어느 위치",
    "도움",
    "어떻게 섞",
    "준비",
    "기준",
    "설명해 주세요",
    "쉽게 설명",
    "괜찮나요",
]

SKILL_FORMULA_CONTEXT = [
    "스킬",
    "쿨타임",
    "피해",
    "데미지",
    "공식",
    "판정",
    "대상",
    "타격",
    "발동 조건",
    "상태 이상",
    "빙결",
    "화상",
    "둔화",
    "연쇄",
    "체인",
    "버프",
    "범위",
    "팝업",
    "투사체",
    "가장 가까운",
    "우선 공격",
]

TOWER_CONTEXT = [
    "타워",
    "층",
    "라운드",
    "보스",
    "잠금",
    "클리어",
    "진행",
    "선택",
    "보상",
    "스크롤",
    "층별",
]

GAMEPLAY_CONTEXT = [
    "배치",
    "위치",
    "경로",
    "초반",
    "초보자",
    "운영",
    "빌드",
    "조합",
    "덱",
    "상성",
    "전투 상황",
    "막히",
    "버티",
]

SUBCATEGORY_HINTS = {
    "bug_report": [
        ("crash", ["강제 종료", "크래시"]),
        ("ui_freeze", ["멈", "진행이 안"]),
        ("reward_issue", ["보상", "중복", "두 번"]),
        ("skill_effect_fail", ["스킬", "발동", "적용되지", "움직"]),
        ("visual_glitch", ["깨져", "겹쳐", "허공", "이펙트"]),
        ("input_issue", ["입력", "인식", "눌리지"]),
    ],
    "feedback_balance": [
        ("economy", ["골드", "비용", "보상", "경제"]),
        ("skill_balance", ["스킬", "빙결", "화상", "체인"]),
        ("difficulty_curve", ["난이도", "적 체력", "보스"]),
        ("meta_diversity", ["메타", "다양성", "조합"]),
        ("growth_pace", ["성장", "레벨업", "요구량"]),
    ],
    "wizard_growth": [
        ("arcane_research", ["연구", "아케인"]),
        ("leveling", ["레벨업", "경험치", "레벨"]),
        ("resonance", ["레조넌스"]),
        ("growth_bonus", ["보너스", "축복", "공격력"]),
    ],
    "wizard_acquisition": [
        ("legendary_acquisition", ["전설", "등장"]),
        ("summon_cost", ["골드", "비용"]),
        ("spawn_position", ["생성", "소환 포인트", "겹치"]),
        ("random_element", ["속성", "랜덤"]),
    ],
    "gameplay_guide": [
        ("placement", ["배치", "위치", "언덕"]),
        ("team_composition", ["조합", "덱", "빌드"]),
        ("beginner_guide", ["초보", "처음", "초반"]),
        ("strategy", ["전략", "운영", "팁", "추천"]),
    ],
    "skill_combat": [
        ("damage_formula", ["피해", "데미지", "공식", "계산"]),
        ("cooldown_display", ["쿨타임"]),
        ("targeting_rules", ["대상", "우선", "연쇄", "체인"]),
        ("status_effect", ["빙결", "화상", "둔화", "상태 이상"]),
    ],
    "tower_progress": [
        ("floor_selection", ["층", "선택"]),
        ("unlock_conditions", ["잠금", "조건"]),
        ("reward_rules", ["보상"]),
        ("boss_progress", ["보스"]),
    ],
}

SCORE_KEYWORDS = {
    "gameplay_guide": GAMEPLAY_CONTEXT + GUIDE_REQUESTS,
    "wizard_acquisition": ACQUISITION_CONTEXT,
    "wizard_growth": GROWTH_CONTEXT,
    "tower_progress": TOWER_CONTEXT,
    "skill_combat": SKILL_FORMULA_CONTEXT,
    "bug_report": BUG_HARD_SIGNALS + BUG_CONTEXT_TERMS,
    "feedback_balance": BALANCE_SIGNALS,
}


def _matches(text: str, keywords: List[str]) -> List[str]:
    return [keyword for keyword in keywords if keyword in text]


def _has_any(text: str, keywords: List[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _pick_subcategory(category: str, text: str, matched_keywords: List[str]) -> str:
    for subcategory, keywords in SUBCATEGORY_HINTS.get(category, []):
        if _has_any(text, keywords):
            return subcategory
    return matched_keywords[0] if matched_keywords else "unknown"


def _result(
    category: str,
    subcategory: str,
    matched_keywords: List[str],
    confidence: float,
) -> Dict:
    urgency = "low"
    needs_human = False
    if category == "bug_report":
        urgency = "high" if _has_any(" ".join(matched_keywords), ["강제 종료", "사라", "소모", "골드만"]) else "medium"
        needs_human = True
    elif category == "feedback_balance":
        urgency = "medium"
        needs_human = True

    return InquiryResult(
        category=category,
        subcategory=subcategory,
        urgency=urgency,
        needs_human=needs_human,
        confidence=round(confidence, 3),
        matched_keywords=matched_keywords,
    ).__dict__


def classify_inquiry_v2(text: str) -> Dict:
    if not isinstance(text, str) or not text.strip():
        return _result("gameplay_guide", "unknown", [], 0.0)

    normalized = text.strip().lower()

    # Clear failures override feature words, following the v2 label policy.
    is_normal_info_question = (
        "정상인가요" in normalized
        or "정상인지" in normalized
        or "얼마나 오래" in normalized
    )
    bug_matches = [] if is_normal_info_question else _matches(normalized, BUG_HARD_SIGNALS)
    if bug_matches:
        subcategory = _pick_subcategory("bug_report", normalized, bug_matches)
        return _result("bug_report", subcategory, bug_matches, 0.9)

    # Balance/economy complaints override feature categories unless there is a hard bug.
    balance_matches = _matches(normalized, BALANCE_SIGNALS)
    if balance_matches:
        if _has_any(normalized, ["어떻게 섞", "무엇을 먼저", "추천", "빌드"]):
            guide_balance_matches = _matches(normalized, GUIDE_REQUESTS + GAMEPLAY_CONTEXT)
            subcategory = _pick_subcategory("gameplay_guide", normalized, guide_balance_matches)
            return _result("gameplay_guide", subcategory, guide_balance_matches, 0.8)
        subcategory = _pick_subcategory("feedback_balance", normalized, balance_matches)
        return _result("feedback_balance", subcategory, balance_matches, 0.85)

    growth_matches = _matches(normalized, GROWTH_CONTEXT)
    acquisition_matches = _matches(normalized, ACQUISITION_CONTEXT)
    guide_matches = _matches(normalized, GUIDE_REQUESTS + GAMEPLAY_CONTEXT)
    skill_matches = _matches(normalized, SKILL_FORMULA_CONTEXT)
    tower_matches = _matches(normalized, TOWER_CONTEXT)

    # Explicit growth-stat phrasing should beat guide/combat/acquisition wording.
    if growth_matches and _has_any(normalized, ["성장 단계", "성장 수치", "레벨 보너스", "경험치 획득량", "레조넌스로 전설 마법사를 만드는"]):
        subcategory = _pick_subcategory("wizard_growth", normalized, growth_matches)
        return _result("wizard_growth", subcategory, growth_matches, 0.82)

    # Strong guide/advice requests stay guide before floor or feature nouns hijack them.
    if guide_matches and _has_any(normalized, ["빌드", "추천", "어떻게 섞", "무엇을 먼저", "어느 위치"]):
        if not _has_any(normalized, ["계산", "공식", "판정", "피해", "데미지", "쿨타임", "대상", "발동 조건", "가이드가 아니라"]):
            subcategory = _pick_subcategory("gameplay_guide", normalized, guide_matches)
            return _result("gameplay_guide", subcategory, guide_matches, 0.8)

    # Process questions about floors should stay tower_progress before generic guide wording.
    if tower_matches and _has_any(normalized, ["층", "층별", "클리어", "잠금", "보스", "선택한 층"]):
        subcategory = _pick_subcategory("tower_progress", normalized, tower_matches)
        return _result("tower_progress", subcategory, tower_matches, 0.78)

    # Acquisition info questions with summon/rarity/probability wording stay acquisition.
    if acquisition_matches and _has_any(normalized, ["소환", "등급", "확률", "전설 마법사"]):
        subcategory = _pick_subcategory("wizard_acquisition", normalized, acquisition_matches)
        return _result("wizard_acquisition", subcategory, acquisition_matches, 0.78)

    # Skill formula/targeting should beat growth when both skill and bonus words appear.
    if skill_matches and _has_any(normalized, ["계산", "공식", "판정", "피해", "데미지", "쿨타임", "대상", "연쇄", "체인", "빙결", "화상", "둔화", "버프", "팝업", "투사체", "가장 가까운", "우선 공격"]):
        subcategory = _pick_subcategory("skill_combat", normalized, skill_matches)
        return _result("skill_combat", subcategory, skill_matches, 0.78)

    # Strategy and guide requests with system words stay gameplay when they ask for advice.
    if guide_matches and _has_any(normalized, ["추천", "팁", "운영", "전략", "상황", "준비", "기준", "흐름", "어떻게 섞", "빌드", "어느 위치", "도움", "가이드"]):
        if not _has_any(normalized, ["계산", "공식", "판정", "피해", "데미지", "쿨타임", "대상", "발동 조건"]):
            subcategory = _pick_subcategory("gameplay_guide", normalized, guide_matches)
            return _result("gameplay_guide", subcategory, guide_matches, 0.78)

    # Growth materials/experience are separated from new wizard acquisition.
    if growth_matches and (_has_any(normalized, ["경험치", "성장 재료", "레벨업", "보너스", "연구", "아케인"]) or len(growth_matches) >= len(acquisition_matches)):
        subcategory = _pick_subcategory("wizard_growth", normalized, growth_matches)
        return _result("wizard_growth", subcategory, growth_matches, 0.78)

    if acquisition_matches:
        subcategory = _pick_subcategory("wizard_acquisition", normalized, acquisition_matches)
        return _result("wizard_acquisition", subcategory, acquisition_matches, 0.72)

    if tower_matches:
        subcategory = _pick_subcategory("tower_progress", normalized, tower_matches)
        return _result("tower_progress", subcategory, tower_matches, 0.72)

    if skill_matches:
        subcategory = _pick_subcategory("skill_combat", normalized, skill_matches)
        return _result("skill_combat", subcategory, skill_matches, 0.68)

    if guide_matches:
        subcategory = _pick_subcategory("gameplay_guide", normalized, guide_matches)
        return _result("gameplay_guide", subcategory, guide_matches, 0.65)

    scores: List[Tuple[str, int, List[str]]] = []
    for category, keywords in SCORE_KEYWORDS.items():
        matched = _matches(normalized, keywords)
        scores.append((category, len(matched), matched))

    best_category, best_score, best_matches = max(scores, key=lambda item: item[1])
    if best_score == 0:
        return _result("gameplay_guide", "unknown", [], 0.05)

    subcategory = _pick_subcategory(best_category, normalized, best_matches)
    confidence = min(0.95, 0.25 + 0.12 * len(best_matches))
    return _result(best_category, subcategory, best_matches, confidence)


def classify_inquiry(text: str) -> Dict:
    return classify_inquiry_v2(text)
