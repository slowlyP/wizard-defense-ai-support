from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.response_templates import generate_response_template  # noqa: E402
from backend.app.support_router import route_inquiry  # noqa: E402


OUTPUT_PATH = ROOT / "experiments" / "response_template_demo_outputs.csv"
SUMMARY_PATH = ROOT / "experiments" / "response_template_summary.md"


DEMO_EXAMPLES = [
    {"id": "template_demo_001", "text": "처음 시작하면 마법사를 어느 위치에 두는 게 좋나요?"},
    {"id": "template_demo_002", "text": "불 마법사와 번개 마법사를 같이 쓰는 조합이 좋은 상황을 알려주세요."},
    {"id": "template_demo_003", "text": "전설 마법사는 소환으로만 얻을 수 있나요?"},
    {"id": "template_demo_004", "text": "소환 티켓을 쓰면 등급 확률이 어떻게 적용되는지 궁금합니다."},
    {"id": "template_demo_005", "text": "마법사 레벨업에 필요한 경험치는 어디에서 얻나요?"},
    {"id": "template_demo_006", "text": "레조넌스 성장 보너스가 어떤 기준으로 적용되나요?"},
    {"id": "template_demo_007", "text": "다음 층 잠금 해제 조건을 알고 싶습니다."},
    {"id": "template_demo_008", "text": "보스 층을 준비할 때 어떤 마법사를 먼저 강화해야 하나요?"},
    {"id": "template_demo_009", "text": "번개 스킬이 어떤 적에게 연쇄되는지 설명해 주세요."},
    {"id": "template_demo_010", "text": "스킬 피해량 계산과 쿨타임 기준을 알고 싶습니다."},
    {"id": "template_demo_011", "text": "레조넌스 시도 후 재료가 사라지고 결과가 생성되지 않았어요."},
    {"id": "template_demo_012", "text": "층 보상을 받았는데 보상 화면이 표시되지 않고 골드만 사라졌습니다."},
    {"id": "template_demo_013", "text": "전설 마법사 등장 확률이 너무 낮아서 조정이 필요하다고 느낍니다."},
    {"id": "template_demo_014", "text": "특정 스킬 조합이 지나치게 강해서 다른 조합의 가치가 낮습니다."},
    {"id": "template_demo_015", "text": "초보자용 성장 가이드와 추천 빌드를 알려주세요."},
    {"id": "template_demo_016", "text": "성장 단계가 오르면 공격력 보너스가 얼마나 달라지나요?"},
    {"id": "template_demo_017", "text": "스킬 설명과 실제 효과가 다르게 보이는데 확인이 필요합니다."},
    {"id": "template_demo_018", "text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다."},
    {"id": "template_demo_019", "text": "타워 업그레이드 비용 대비 보상 효율이 낮은 것 같습니다."},
    {"id": "template_demo_020", "text": "게임이 전투 중 멈춰서 진행이 안 됩니다."},
]


CSV_COLUMNS = [
    "id",
    "text",
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
    "routing_reason",
    "response_draft",
    "internal_note",
]


def build_demo_rows() -> List[Dict]:
    rows = []
    for example in DEMO_EXAMPLES:
        route = route_inquiry(example["text"])
        template = generate_response_template(route)
        rows.append(
            {
                "id": example["id"],
                "text": example["text"],
                "predicted_category": route["predicted_category"],
                "urgency": route["urgency"],
                "needs_human": str(route["needs_human"]).lower(),
                "suggested_response_type": route["suggested_response_type"],
                "routing_reason": route["routing_reason"],
                "response_draft": template["response_draft"],
                "internal_note": template["internal_note"],
            }
        )
    return rows


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _count_lines(counter: Counter) -> str:
    return "\n".join(f"- `{key}`: {value}건" for key, value in sorted(counter.items()))


def write_summary(path: Path, rows: List[Dict]) -> None:
    response_counts = Counter(row["suggested_response_type"] for row in rows)
    category_counts = Counter(row["predicted_category"] for row in rows)
    urgency_counts = Counter(row["urgency"] for row in rows)
    human_count = sum(1 for row in rows if row["needs_human"] == "true")

    content = f"""# Response Template Summary (v0.12.0-response-template-prototype)

## 목적

이 문서는 support router output을 한국어 response draft template으로 변환하는 로컬 prototype 결과를 기록합니다. 이번 단계에서는 web server, FastAPI, 외부 API, LLM API, helpdesk 연동 없이 고정된 안전 템플릿만 사용합니다.

## 사용한 router

- Router: `backend/app/support_router.py`
- Template module: `backend/app/response_templates.py`
- Demo script: `backend/scripts/run_response_template_demo.py`
- Demo output: `experiments/response_template_demo_outputs.csv`
- Demo examples: {len(rows)}건

## 사용한 response template types

{_count_lines(response_counts)}

## template별 정책

- `guide_answer`: 배치, 조합, 초반 운영, 전략 문의에 일반적인 플레이 가이드를 제공합니다.
- `acquisition_answer`: 소환, 획득, 등급, 등장 확률 문의에 안전한 획득 안내를 제공합니다.
- `growth_answer`: 레벨업, 경험치, 성장 재료, 레조넌스 문의에 성장 시스템 안내를 제공합니다.
- `tower_progress_answer`: 층 진행, 잠금 해제, 보스, 보상 조건 문의에 타워 진행 안내를 제공합니다.
- `skill_combat_answer`: 스킬 효과, 쿨타임, 피해 계산, 판정 문의에 전투/스킬 안내를 제공합니다.
- `bug_triage`: 오류 가능성이 있는 문의에 재현 정보와 상황 정보를 요청하며, 보상이나 해결을 약속하지 않습니다.
- `balance_feedback_ack`: 밸런스 의견을 접수했다는 안전한 확인 문구를 제공하며, 조정 여부나 적용 시점을 약속하지 않습니다.

## demo 결과 요약

Category 분포:
{_count_lines(category_counts)}

Urgency 분포:
{_count_lines(urgency_counts)}

- 사람 검토 필요: {human_count} / {len(rows)}건
- 자동 응답 가능: {len(rows) - human_count} / {len(rows)}건

## needs_human=true 응답 처리 기준

- `bug_triage`는 재현 순서, 발생 시점, 사용한 마법사, 층 정보, 화면 상황 같은 확인 정보를 요청합니다.
- `balance_feedback_ack`는 검토 참고 자료로 정리할 수 있다고만 안내하고, 실제 조정 여부는 확정하지 않습니다.
- 기능 category로 분류되었더라도 router가 실패 신호를 감지한 경우에는 사람 검토 또는 추가 정보 요청 문구를 붙입니다.
- `urgency=high`인 경우에는 재현 단계와 상황 정보를 더 구체적으로 요청합니다.

## 자동 응답 가능 케이스 기준

- 단순 플레이 방법, 배치, 조합, 소환 안내, 성장 안내, 층 진행 조건, 스킬 규칙 설명은 자동 응답 초안으로 처리할 수 있습니다.
- 자동 응답 가능 케이스에서도 실제 수치, 확정 일정, 보상 판단은 포함하지 않습니다.

## 안전한 응답 제한사항

- 환불, 보상, 재화 복구를 약속하지 않습니다.
- 정확한 patch date 또는 guaranteed fix를 약속하지 않습니다.
- 운영자가 아직 확인하지 않은 원인을 단정하지 않습니다.
- 외부 API, LLM, 실제 ticket system과 연결하지 않습니다.
- response draft는 최종 고객 응답이 아니라 portfolio prototype용 초안입니다.

## 한계

- 고정 template 기반이므로 문의 세부 맥락에 맞춘 자연스러운 문장 변형은 제한적입니다.
- router와 improved rule classifier의 분류 결과에 의존하므로 분류 오류가 응답 초안에도 전파될 수 있습니다.
- 실제 고객 지원 정책, 보상 정책, 패치 계획과 연결되어 있지 않습니다.

## 다음 작업 제안

- response draft별 검수 checklist와 금지 표현 목록을 추가합니다.
- `needs_human=true` 케이스를 bug, balance, policy review queue로 더 세분화합니다.
- FastAPI 구현 전 template generator 단위 테스트를 추가합니다.
"""
    path.write_text(content, encoding="utf-8-sig")


def main() -> None:
    rows = build_demo_rows()
    write_csv(OUTPUT_PATH, rows)
    write_summary(SUMMARY_PATH, rows)

    print("Response Template Demo")
    print("=" * 40)
    print(f"Demo rows: {len(rows)}")
    print(f"Needs human: {sum(1 for row in rows if row['needs_human'] == 'true')}")
    print(f"Saved demo output: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Saved summary: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
