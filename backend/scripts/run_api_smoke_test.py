from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from backend.app.api import app  # noqa: E402


OUTPUT_PATH = ROOT / "experiments" / "api_local_smoke_test_outputs.csv"
EXAMPLES = [
    ("api_smoke_001", "처음 시작하면 마법사를 어디에 배치하는 게 가장 안전한가요?", "gameplay_guide"),
    ("api_smoke_002", "전설 마법사는 어떤 방식으로 획득하나요?", "wizard_acquisition"),
    ("api_smoke_003", "마법사 레벨업에 필요한 경험치는 어디서 얻나요?", "wizard_growth"),
    ("api_smoke_004", "다음 층은 어떤 조건에서 열리나요?", "tower_progress"),
    ("api_smoke_005", "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요.", "skill_combat"),
    ("api_smoke_006", "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다.", "bug_report"),
    ("api_smoke_007", "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다.", "feedback_balance"),
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


def run_smoke_test() -> List[Dict]:
    """Exercise the app in-process, assert key behavior, and return CSV rows."""
    client = TestClient(app)
    health_response = client.get("/health")
    health_response.raise_for_status()
    assert health_response.json() == {"status": "ok"}

    rows = []
    for example_id, text, expected_category in EXAMPLES:
        response = client.post("/support/preview", json={"text": text})
        response.raise_for_status()
        result = response.json()
        assert result["predicted_category"] == expected_category
        result["id"] = example_id
        result["needs_human"] = str(result["needs_human"]).lower()
        rows.append({column: result[column] for column in CSV_COLUMNS})
    return rows


def write_csv(rows: List[Dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = run_smoke_test()
    write_csv(rows)
    print("FastAPI Local Smoke Test")
    print(f"Health: ok")
    print(f"Preview cases: {len(rows)}/{len(EXAMPLES)} passed")
    print(f"Saved output: {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
