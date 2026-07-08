"""
간단한 키워드 기반 룰 분류기

설명: 이 모듈은 한국어 문의 텍스트를 받아 사전 정의된 키워드 규칙으로 카테고리, 서브카테고리, 긴급도, 사람 검토 필요 여부, 신뢰도, 매칭된 키워드를 반환합니다.
"""
from typing import List, Dict
from .schemas import InquiryResult


# 카테고리별 키워드 사전 (간단한 예시)
KEYWORDS = {
    "gameplay_guide": [
        "길", "경로", "배치", "타일", "성", "라운드", "초반", "초보자", "배치 규칙",
    ],
    "wizard_acquisition": [
        "획득", "얻", "뽑기", "뽑", "소환", "티켓", "뽑기권", "등급", "등장 확률",
        "확률", "중복", "같은 마법사", "보유", "목록",
    ],
    "wizard_growth": [
        "전설", "레조넌스", "합쳐", "합성", "성장", "레벨업", "재능", "타렌트",
    ],
    "tower_progress": [
        "층", "타워", "언락", "잠금", "스테이지", "보스", "몬스터", "스폰",
    ],
    "skill_combat": [
        "스킬", "쿨다운", "사거리", "범위", "데미지", "투사체", "타겟", "연계", "번개", "빔",
    ],
    "bug_report": [
        "크래시", "멈추", "멈춰", "멈춤", "멈춥니다", "프리징", "튕김", "튕겨",
        "오류", "버그", "안 돼요", "안됩니다", "먹통", "진행이 안", "저장", "사라졌", "입력 인식",
    ],
    "feedback_balance": [
        "너무", "강한", "약한", "밸런스", "확률", "골드", "보상", "과도", "밸런스 조정",
    ],
}


ISSUE_PATTERNS = [
    "안 맞", "안 들어가", "돌아가", "다시", "안 움직", "공격을 안",
]

SUBCATEGORY_RULES = {
    "bug_report": [
        ("freeze_or_crash", ["멈추", "멈춰", "멈춤", "멈춥니다", "프리징", "튕김", "튕겨", "먹통"]),
    ],
    "wizard_acquisition": [
        ("draw_ticket", ["티켓", "뽑기권"]),
        ("duplicate_acquisition", ["중복", "같은 마법사", "또 뽑"]),
        ("acquisition_probability", ["확률", "등장 확률"]),
        ("rarity_draw", ["전설", "등급"]),
        ("acquisition_guide", ["획득", "얻", "뽑기", "뽑", "소환"]),
    ],
    "tower_progress": [
        ("floor_selection_issue", ["층", "다시", "돌아가"]),
    ],
    "skill_combat": [
        ("skill_targeting", ["안 맞", "타겟", "몬스터", "공격을 안", "빔", "스킬"]),
    ],
}


def _score_text(text: str, keywords: List[str]) -> tuple[int, List[str]]:
    """주어진 텍스트에서 키워드 매칭 수와 매칭 키워드 목록 반환"""
    matches = []
    lowered = text.lower()
    for kw in keywords:
        if kw in lowered:
            matches.append(kw)
    return len(matches), matches


def _pick_subcategory(category: str, text: str, matches: List[str]) -> str:
    """카테고리별 의미 있는 서브카테고리를 우선 반환합니다."""
    lowered = text.lower()
    for subcategory, keywords in SUBCATEGORY_RULES.get(category, []):
        if any(keyword in lowered for keyword in keywords):
            return subcategory
    return matches[0] if matches else "unknown"


def classify_inquiry(text: str) -> Dict:
    """텍스트를 분류하고 결과를 반환합니다.

    반환 형식:
    {
        "category": str,
        "subcategory": str,
        "urgency": str,
        "needs_human": bool,
        "confidence": float,
        "matched_keywords": List[str]
    }
    """
    if not isinstance(text, str) or not text.strip():
        return InquiryResult(
            category="feedback_balance",
            subcategory="unknown",
            urgency="low",
            needs_human=False,
            confidence=0.0,
            matched_keywords=[],
        ).__dict__

    scores = {}
    matches = {}
    # 점수 계산
    for cat, kws in KEYWORDS.items():
        count, matched = _score_text(text, kws)
        scores[cat] = count
        matches[cat] = matched

    issue_count, issue_matches = _score_text(text, ISSUE_PATTERNS)
    bug_count, bug_matches = _score_text(text, KEYWORDS["bug_report"])
    acquisition_count, acquisition_matches = _score_text(text, KEYWORDS["wizard_acquisition"])

    # 최고 점수 카테고리 선택
    best_cat = max(scores.items(), key=lambda x: x[1])[0]
    best_score = scores[best_cat]
    best_matches = matches[best_cat]

    # 획득/뽑기 단서가 있으면 성장 문의와 구분해 마법사 획득으로 우선 분류합니다.
    if acquisition_count > 0:
        best_cat = "wizard_acquisition"
        best_score = max(best_score, acquisition_count)
        best_matches = acquisition_matches

    # 버그 키워드는 사람 검토가 필요한 오류로 우선 분류합니다.
    if bug_count > 0:
        best_cat = "bug_report"
        best_score = max(best_score, bug_count)
        best_matches = bug_matches

    # 긴급도 및 사람 검토 규칙
    needs_human = False
    urgency = "low"
    if bug_count > 0:
        needs_human = True
        urgency = "high"

    if issue_count > 0 and best_cat in {"wizard_acquisition", "tower_progress", "skill_combat"}:
        needs_human = True
        urgency = "medium"
        best_matches = list(dict.fromkeys(best_matches + issue_matches))

    # 피드백/밸런스 언급이면 사람 검토 권장
    fb_terms = KEYWORDS["feedback_balance"]
    fb_count, fb_matches = _score_text(text, fb_terms)
    if fb_count > 0 and not needs_human:
        needs_human = True
        urgency = "medium"

    # 신뢰도 계산: 매칭 수가 늘수록 높아지는 간단한 휴리스틱
    confidence = min(0.95, 0.2 + (len(best_matches) * 0.15))

    # 매칭 키워드 집계
    matched_keywords = best_matches

    # 예외: 어떤 키워드도 매칭되지 않으면 낮은 신뢰도로 추측
    if best_score == 0:
        # 선호: gameplay_guide 또는 feedback_balance
        fallback = "gameplay_guide"
        return InquiryResult(
            category=fallback,
            subcategory="unknown",
            urgency="low",
            needs_human=False,
            confidence=0.05,
            matched_keywords=[],
        ).__dict__

    subcategory = _pick_subcategory(best_cat, text, matched_keywords)

    result = InquiryResult(
        category=best_cat,
        subcategory=subcategory,
        urgency=urgency,
        needs_human=needs_human,
        confidence=round(confidence, 3),
        matched_keywords=matched_keywords,
    )

    return result.__dict__


if __name__ == "__main__":
    # 간단한 로컬 테스트
    samples = [
        "마법사는 길 위에 설치할 수 없나요?",
        "전설 마법사 두 명이 나오면 합쳐지나요?",
        "특수 뽑기권은 어디에 사용하나요?",
        "1층으로 가려고 했는데 다시 6층으로 돌아가요.",
        "번개 비 스킬이 몬스터한테 안 맞는 것 같아요.",
        "게임을 켜면 화면이 멈춰요.",
        "번개 마법사가 너무 약한 것 같아요.",
    ]
    for s in samples:
        print(s, "->", classify_inquiry(s))
