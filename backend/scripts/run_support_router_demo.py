from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.support_router import route_inquiry  # noqa: E402


OUTPUT_PATH = ROOT / "experiments" / "support_router_demo_outputs.csv"
SUMMARY_PATH = ROOT / "experiments" / "support_router_summary.md"


DEMO_EXAMPLES = [
    {"id": "demo_001", "text": "처음 시작하면 마법사를 어디에 배치하는 게 가장 안전한가요?"},
    {"id": "demo_002", "text": "불 마법사와 물 마법사를 같이 쓸 때 어떤 조합이 좋은가요?"},
    {"id": "demo_003", "text": "전설 마법사는 어떤 방식으로 획득하나요?"},
    {"id": "demo_004", "text": "소환 티켓을 쓰면 등급 확률이 어떻게 적용되나요?"},
    {"id": "demo_005", "text": "마법사 레벨업에 필요한 경험치는 어디서 얻나요?"},
    {"id": "demo_006", "text": "레조넌스로 전설 마법사를 만드는 방법을 알려주세요."},
    {"id": "demo_007", "text": "다음 층은 어떤 조건에서 열리나요?"},
    {"id": "demo_008", "text": "보스가 있는 층에서는 어떤 준비를 먼저 해야 하나요?"},
    {"id": "demo_009", "text": "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요."},
    {"id": "demo_010", "text": "스킬 피해량 계산식과 쿨타임 기준이 궁금합니다."},
    {"id": "demo_011", "text": "레조넌스 재료가 사라지고 전설 마법사가 생성되지 않았어요."},
    {"id": "demo_012", "text": "층 보상을 받았는데 골드만 사라지고 보상이 표시되지 않습니다."},
    {"id": "demo_013", "text": "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다."},
    {"id": "demo_014", "text": "특정 스킬 조합이 지나치게 강해서 다른 조합을 쓸 이유가 없습니다."},
    {"id": "demo_015", "text": "초보자용 성장 가이드를 추천해 주세요."},
    {"id": "demo_016", "text": "성장 단계가 오르면 어떤 보너스를 받나요?"},
    {"id": "demo_017", "text": "번개 마법사와 불 마법사 조합이 효과적인 상황을 알려주세요."},
    {"id": "demo_018", "text": "번개 스킬이 설명과 다르게 가까운 적을 우선 공격하지 않는 것 같습니다."},
    {"id": "demo_019", "text": "타워 업그레이드 비용 대비 보상 효율이 낮은 것 같습니다."},
    {"id": "demo_020", "text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다."},
]


CSV_COLUMNS = [
    "id",
    "text",
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
    "routing_reason",
]


def route_demo_examples() -> List[Dict]:
    rows = []
    for example in DEMO_EXAMPLES:
        route = route_inquiry(example["text"])
        rows.append(
            {
                "id": example["id"],
                "text": example["text"],
                "predicted_category": route["predicted_category"],
                "urgency": route["urgency"],
                "needs_human": str(route["needs_human"]).lower(),
                "suggested_response_type": route["suggested_response_type"],
                "routing_reason": route["routing_reason"],
            }
        )
    return rows


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, rows: List[Dict]) -> None:
    category_counts = Counter(row["predicted_category"] for row in rows)
    urgency_counts = Counter(row["urgency"] for row in rows)
    human_count = sum(1 for row in rows if row["needs_human"] == "true")
    response_counts = Counter(row["suggested_response_type"] for row in rows)

    category_lines = "\n".join(
        f"- `{category}`: {count}건" for category, count in sorted(category_counts.items())
    )
    urgency_lines = "\n".join(
        f"- `{urgency}`: {count}건" for urgency, count in sorted(urgency_counts.items())
    )
    response_lines = "\n".join(
        f"- `{response_type}`: {count}건"
        for response_type, count in sorted(response_counts.items())
    )

    content = f"""# Support Router Summary (v0.11.0-support-router-prototype)

## 목적

이 문서는 improved rule classifier를 기반으로 한국어 플레이어 문의를 지원 라우팅 정보로 변환하는 로컬 prototype 결과를 기록합니다. 이번 단계에서는 web server, FastAPI, 외부 API, Gmail, Slack, Discord 연동을 구현하지 않고 로컬 Python script와 CSV output만 생성합니다.

## 사용한 classifier

- Classifier: `backend/app/rule_classifier_v2.py`
- Router: `backend/app/support_router.py`
- Demo script: `backend/scripts/run_support_router_demo.py`
- Demo output: `experiments/support_router_demo_outputs.csv`
- Demo examples: {len(rows)}건

## router output fields

- `predicted_category`: improved rule classifier가 예측한 category입니다.
- `urgency`: 지원 처리 우선순위이며 `low`, `medium`, `high` 중 하나입니다.
- `needs_human`: 자동 응답만으로 충분한지, 사람 검토가 필요한지 나타냅니다.
- `routing_reason`: 라우팅 판단 근거를 짧은 한국어 문장으로 설명합니다.
- `suggested_response_type`: 응답 템플릿 또는 처리 흐름을 고르기 위한 내부 타입입니다.

## category별 routing policy

- `gameplay_guide`: 배치, 조합, 초반 운영, 전략 문의는 `guide_answer`로 라우팅하고 기본 `urgency=low`, `needs_human=false`로 처리합니다.
- `wizard_acquisition`: 소환, 획득, 등급, 등장 확률 안내 문의는 `acquisition_answer`로 라우팅합니다.
- `wizard_growth`: 레벨업, 경험치, 성장 재료, 레조넌스 문의는 `growth_answer`로 라우팅합니다.
- `tower_progress`: 층 진행, 잠금 해제, 보스, 층 보상 문의는 `tower_progress_answer`로 라우팅합니다.
- `skill_combat`: 스킬 효과, 쿨타임, 피해 계산, 타격 판정 문의는 `skill_combat_answer`로 라우팅합니다.
- `bug_report`: 진행 불가, 크래시, 보상/재화 손실, UI 이상은 `bug_triage`로 라우팅하고 `needs_human=true`로 처리합니다.
- `feedback_balance`: 비용, 확률, 효율, 강함/약함, 조정 요청은 `balance_feedback_ack`로 라우팅하고 `urgency=medium`, `needs_human=true`로 처리합니다.

## demo 결과 요약

Category 분포:
{category_lines}

Urgency 분포:
{urgency_lines}

Suggested response type 분포:
{response_lines}

- 사람 검토 필요: {human_count} / {len(rows)}건
- 자동 응답 가능: {len(rows) - human_count} / {len(rows)}건

## 사람 검토가 필요한 케이스 기준

- 게임 진행 불가, 크래시, 멈춤, 저장/보상/재화 손실 가능성이 있으면 `bug_report`로 라우팅하고 사람 검토가 필요합니다.
- 기능 단어가 포함되어도 실제 동작 실패나 설명과 실제 효과 차이를 말하면 사람 검토 대상입니다.
- 밸런스, 비용, 확률, 효율, 강함/약함에 대한 조정 요청은 정책 판단이 필요하므로 사람 검토 대상으로 둡니다.
- 분류는 되었지만 문의가 보상 복구, 공지 누락, 버그 여부 확인처럼 운영 판단을 요구하면 `needs_human=true`로 올립니다.

## 한계

- 이 prototype은 rule 기반이며 실제 ticket history나 운영자 처리 결과를 학습하지 않았습니다.
- `routing_reason`은 설명 가능한 데모용 문장이고, 실제 고객 응답 문구는 아닙니다.
- improved rule classifier가 dataset v2 표현 분포에 맞춰져 있을 수 있어 holdout sample에서 별도 검증이 필요합니다.
- 외부 helpdesk, email, chat system과 연결하지 않았으므로 실제 ticket assignment 기능은 없습니다.

## 다음 작업 제안

- `suggested_response_type`별 한국어 응답 템플릿 초안을 작성합니다.
- `needs_human=true` 케이스를 운영 queue 기준으로 더 세분화합니다.
- FastAPI 구현 전 router 입출력 schema와 단위 테스트를 추가합니다.
"""
    path.write_text(content, encoding="utf-8-sig")


def main() -> None:
    rows = route_demo_examples()
    write_csv(OUTPUT_PATH, rows)
    write_summary(SUMMARY_PATH, rows)

    print("Support Router Demo")
    print("=" * 40)
    print(f"Demo rows: {len(rows)}")
    print(f"Needs human: {sum(1 for row in rows if row['needs_human'] == 'true')}")
    print(f"Saved demo output: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Saved summary: {SUMMARY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
