"""
테스트 스크립트: 규칙 기반 분류기를 리포지토리 루트에서 실행하고 결과를 한국어로 출력합니다.

루트에서 실행:
python backend/scripts/test_rule_classifier.py
"""
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from backend.app.rule_classifier import classify_inquiry


def pretty_print(result: dict):
    print("카테고리:", result.get("category"))
    print("서브카테고리:", result.get("subcategory"))
    print("긴급도:", result.get("urgency"))
    print("사람 검토 필요:", result.get("needs_human"))
    print("신뢰도:", result.get("confidence"))
    print("매칭 키워드:", result.get("matched_keywords"))
    print("-" * 40)


def run_tests():
    cases = [
        {
            "text": "마법사는 길 앞에 설치하면 되나요?",
            "expected": {"category": "gameplay_guide"},
        },
        {
            "text": "전설 마법사가 3명이 나오면 합쳐지나요?",
            "expected": {"category": "wizard_growth"},
        },
        {
            "text": "장비를 드래그했는데 계속 가방으로 돌아가요.",
            "expected": {
                "category": "equipment_inventory",
                "subcategory": "equip_failure",
                "urgency": "medium",
                "needs_human": True,
            },
        },
        {
            "text": "1층으로 가려고 했는데 다시 6층으로 돌아가요.",
            "expected": {
                "category": "tower_progress",
                "subcategory": "floor_selection_issue",
                "urgency": "medium",
                "needs_human": True,
            },
        },
        {
            "text": "번개 빔 스킬이 몬스터한테 안 맞는 것 같아요.",
            "expected": {
                "category": "skill_combat",
                "subcategory": "skill_targeting",
                "urgency": "medium",
                "needs_human": True,
            },
        },
        {
            "text": "게임을 켜면 화면이 멈춰요.",
            "expected": {
                "category": "bug_report",
                "subcategory": "freeze_or_crash",
                "urgency": "high",
                "needs_human": True,
            },
        },
        {
            "text": "번개 마법사가 너무 강한 것 같아요.",
            "expected": {"category": "feedback_balance", "urgency": "medium", "needs_human": True},
        },
    ]

    failed_cases = []
    for case in cases:
        print("문의:", case["text"])
        result = classify_inquiry(case["text"])
        pretty_print(result)
        failed_fields = [
            key
            for key, expected_value in case["expected"].items()
            if result.get(key) != expected_value
        ]
        if failed_fields:
            failed_cases.append((case["text"], failed_fields, result, case["expected"]))

    if failed_cases:
        print("실패한 테스트:")
        for text, fields, result, expected in failed_cases:
            print("문의:", text)
            print("불일치 필드:", fields)
            print("실제 결과:", result)
            print("기대 결과:", expected)
        raise SystemExit(1)

    print("모든 테스트가 통과했습니다.")


if __name__ == "__main__":
    run_tests()
