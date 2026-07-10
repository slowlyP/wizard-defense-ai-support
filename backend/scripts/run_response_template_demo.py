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


OUTPUT_PATH = ROOT / "experiments" / "steam_response_template_demo_outputs.csv"
SUMMARY_PATH = ROOT / "experiments" / "steam_response_alignment_summary.md"

DEMO_EXAMPLES = [
    {"id": "steam_demo_001", "text": "PC에서 마우스로 마법사를 어디에 배치하면 좋나요?"},
    {"id": "steam_demo_002", "text": "전설 마법사는 어떤 방식으로 획득하나요?"},
    {"id": "steam_demo_003", "text": "마법사 레벨업에 필요한 경험치는 어디서 얻나요?"},
    {"id": "steam_demo_004", "text": "다음 층은 어떤 조건으로 열리나요?"},
    {"id": "steam_demo_005", "text": "번개 스킬은 어떤 적에게 연쇄되나요?"},
    {"id": "steam_demo_006", "text": "Windows 빌드에서 전투 중 멈춰서 진행이 안 됩니다."},
    {"id": "steam_demo_007", "text": "전설 마법사 확률이 너무 낮아 조정이 필요합니다."},
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
    human_count = sum(row["needs_human"] == "true" for row in rows)

    content = f"""# Steam 지원 응답 정렬 요약 (v0.19.0-steam-support-response-alignment)

## 1. 목적

기존 deterministic response template을 Random Wizard Defense의 PC / Steam release 방향과 한국어 fantasy tower defense 지원 문맥에 맞게 조정한 결과를 기록합니다.

## 2. 변경 이유

기존 template은 일반 게임 안내에는 적합했지만 mouse-based PC play, Windows build, Steam demo 확인 정보를 명시하지 않았습니다. Mobile-first로 오해될 수 있는 문맥을 피하고 현재 release 방향에 맞는 정보를 요청하도록 wording을 갱신했습니다.

## 3. Steam / PC 방향 반영 내용

- `gameplay_guide`에서 mouse drag placement와 PC play를 안내합니다.
- Bug triage에서 Windows/Steam demo build, PC resolution, fullscreen/windowed 상태를 확인합니다.
- Tower와 system 안내에서 Steam demo 또는 Windows build 조건을 기준으로 설명합니다.
- Balance feedback을 Steam demo/PC playtest 검토 자료로 안내합니다.
- Steamworks 연동이나 release 완료를 단정하지 않고 demo/build context만 사용합니다.

## 4. Category별 response wording 변화

- `gameplay_guide`: PC mouse selection과 drag placement 중심으로 변경했습니다.
- `wizard_acquisition`: Steam demo/Windows build의 acquisition rule 확인을 안내합니다.
- `wizard_growth`: PC build의 growth, experience, resonance 안내로 정리했습니다.
- `tower_progress`: Floor/stage progression과 build별 unlock context를 반영했습니다.
- `skill_combat`: PC build, wizard, target, floor/stage 전투 context를 확인합니다.
- `bug_report`: Reproduction step, floor/stage, wizard composition, error screen, Windows/Steam demo build와 resolution을 요청합니다.
- `feedback_balance`: Steam demo/PC playtest balance review로 접수하되 change나 patch date를 약속하지 않습니다.

## 5. 검증 결과

- Demo example: {len(rows)}건
- 사람 검토 필요: {human_count}건
- 자동 응답 가능: {len(rows) - human_count}건

Category 분포:
{_count_lines(category_counts)}

Response type 분포:
{_count_lines(response_counts)}

Urgency 분포:
{_count_lines(urgency_counts)}

- Unittest에서 output field, PC/Steam phrase, safety wording, router integration을 확인했습니다.

## 6. 변경하지 않은 항목

- Support router category, urgency, `needs_human`, `suggested_response_type` behavior
- FastAPI endpoint path와 response field
- Dataset v1/v2와 기존 experiment CSV
- Unity game repository file

## 7. 한계

- 고정 template이므로 개별 PC hardware와 build-specific 원인을 자동 진단하지 않습니다.
- Steamworks integration이나 Steam release 완료 상태를 의미하지 않습니다.
- Response draft는 실제 customer support policy가 아닌 portfolio preview입니다.

## 8. 다음 작업 제안

- 별도 승인 후 Windows build bug intake field를 structured schema로 설계합니다.
- Steam demo playtest에서 확인된 support phrase를 검토해 template을 보완합니다.
- 실제 release 전에는 platform support policy와 privacy 기준을 별도로 정의합니다.
"""
    path.write_text(content, encoding="utf-8-sig")


def main() -> None:
    rows = build_demo_rows()
    write_csv(OUTPUT_PATH, rows)
    write_summary(SUMMARY_PATH, rows)

    print("Steam Response Template Demo")
    print(f"Demo rows: {len(rows)}")
    print(f"Needs human: {sum(row['needs_human'] == 'true' for row in rows)}")
    print(f"Saved demo output: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Saved summary: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
