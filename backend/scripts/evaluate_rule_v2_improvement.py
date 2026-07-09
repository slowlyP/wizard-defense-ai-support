"""
Evaluate the improved rule-based classifier on dataset v2.

Run from repository root:
python backend/scripts/evaluate_rule_v2_improvement.py
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
import sys
from typing import Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from backend.app.rule_classifier_v2 import classify_inquiry_v2


DATASET_PATH = REPO_ROOT / "data" / "raw" / "wizard_defense_inquiries_v2.csv"
ORIGINAL_RULE_PATH = REPO_ROOT / "experiments" / "rule_classifier_predictions_v2.csv"
TFIDF_PATH = REPO_ROOT / "experiments" / "tfidf_predictions_v2.csv"
IMPROVED_OUTPUT_PATH = REPO_ROOT / "experiments" / "rule_v2_improved_predictions.csv"
COMPARISON_OUTPUT_PATH = REPO_ROOT / "experiments" / "rule_v2_improvement_comparison.csv"
SUMMARY_OUTPUT_PATH = REPO_ROOT / "experiments" / "rule_v2_improvement_summary.md"


PREDICTION_FIELDS = [
    "id",
    "text",
    "expected_category",
    "predicted_category",
    "expected_subcategory",
    "predicted_subcategory",
    "correct",
    "confidence",
    "matched_keywords",
]

COMPARISON_FIELDS = [
    "id",
    "text",
    "expected_category",
    "original_rule_predicted_category",
    "improved_rule_predicted_category",
    "tfidf_predicted_category",
    "original_rule_correct",
    "improved_rule_correct",
    "tfidf_correct",
    "comparison_type",
]


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def save_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def format_accuracy(correct: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{(correct / total) * 100:.2f}%"


def format_delta(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%p"


def evaluate_improved(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    predictions = []
    for row in rows:
        result = classify_inquiry_v2(row.get("text", ""))
        expected_category = row.get("category", "")
        predicted_category = result.get("category", "")
        is_correct = expected_category == predicted_category

        predictions.append(
            {
                "id": row.get("id", ""),
                "text": row.get("text", ""),
                "expected_category": expected_category,
                "predicted_category": predicted_category,
                "expected_subcategory": row.get("subcategory", ""),
                "predicted_subcategory": result.get("subcategory", ""),
                "correct": str(is_correct).lower(),
                "confidence": result.get("confidence", ""),
                "matched_keywords": "|".join(result.get("matched_keywords", [])),
            }
        )
    return predictions


def get_comparison_type(original_correct: bool, improved_correct: bool, tfidf_correct: bool) -> str:
    if improved_correct and not original_correct:
        return "improved_gain"
    if original_correct and not improved_correct:
        return "improved_loss"
    if improved_correct and tfidf_correct:
        return "improved_and_tfidf_correct"
    if improved_correct:
        return "improved_only_correct"
    if tfidf_correct:
        return "tfidf_only_correct"
    return "all_wrong"


def compare_predictions(
    original_rows: List[Dict[str, str]],
    improved_rows: List[Dict[str, str]],
    tfidf_rows: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    original_by_id = {row["id"]: row for row in original_rows}
    tfidf_by_id = {row["id"]: row for row in tfidf_rows}
    comparison_rows = []

    for improved_row in improved_rows:
        row_id = improved_row["id"]
        original_row = original_by_id[row_id]
        tfidf_row = tfidf_by_id[row_id]
        original_correct = parse_bool(original_row["correct"])
        improved_correct = parse_bool(improved_row["correct"])
        tfidf_correct = parse_bool(tfidf_row["correct"])

        comparison_rows.append(
            {
                "id": row_id,
                "text": improved_row["text"],
                "expected_category": improved_row["expected_category"],
                "original_rule_predicted_category": original_row["predicted_category"],
                "improved_rule_predicted_category": improved_row["predicted_category"],
                "tfidf_predicted_category": tfidf_row["predicted_category"],
                "original_rule_correct": original_row["correct"],
                "improved_rule_correct": improved_row["correct"],
                "tfidf_correct": tfidf_row["correct"],
                "comparison_type": get_comparison_type(
                    original_correct,
                    improved_correct,
                    tfidf_correct,
                ),
            }
        )

    return comparison_rows


def summarize(comparison_rows: List[Dict[str, str]]) -> Dict:
    summary = {
        "total": len(comparison_rows),
        "original_correct": 0,
        "improved_correct": 0,
        "tfidf_correct": 0,
        "improved_gain": 0,
        "improved_loss": 0,
        "category_stats": defaultdict(
            lambda: {
                "total": 0,
                "original_correct": 0,
                "improved_correct": 0,
                "tfidf_correct": 0,
                "improved_gain": 0,
                "improved_loss": 0,
            }
        ),
    }

    for row in comparison_rows:
        category = row["expected_category"]
        original_correct = parse_bool(row["original_rule_correct"])
        improved_correct = parse_bool(row["improved_rule_correct"])
        tfidf_correct = parse_bool(row["tfidf_correct"])

        summary["original_correct"] += int(original_correct)
        summary["improved_correct"] += int(improved_correct)
        summary["tfidf_correct"] += int(tfidf_correct)
        if improved_correct and not original_correct:
            summary["improved_gain"] += 1
        if original_correct and not improved_correct:
            summary["improved_loss"] += 1

        category_stats = summary["category_stats"][category]
        category_stats["total"] += 1
        category_stats["original_correct"] += int(original_correct)
        category_stats["improved_correct"] += int(improved_correct)
        category_stats["tfidf_correct"] += int(tfidf_correct)
        if improved_correct and not original_correct:
            category_stats["improved_gain"] += 1
        if original_correct and not improved_correct:
            category_stats["improved_loss"] += 1

    summary["category_stats"] = dict(summary["category_stats"])
    return summary


def make_category_table(summary: Dict) -> str:
    lines = [
        "| category | total | original correct | original accuracy | improved correct | improved accuracy | TF-IDF correct | TF-IDF accuracy | gain | loss |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for category in sorted(summary["category_stats"]):
        stats = summary["category_stats"][category]
        total = stats["total"]
        lines.append(
            f"| `{category}` | {total} | {stats['original_correct']} | "
            f"{format_accuracy(stats['original_correct'], total)} | "
            f"{stats['improved_correct']} | {format_accuracy(stats['improved_correct'], total)} | "
            f"{stats['tfidf_correct']} | {format_accuracy(stats['tfidf_correct'], total)} | "
            f"{stats['improved_gain']} | {stats['improved_loss']} |"
        )
    return "\n".join(lines)


def write_summary(path: Path, summary: Dict) -> None:
    total = summary["total"]
    original_correct = summary["original_correct"]
    improved_correct = summary["improved_correct"]
    tfidf_correct = summary["tfidf_correct"]
    original_accuracy = original_correct / total if total else 0.0
    improved_accuracy = improved_correct / total if total else 0.0
    tfidf_accuracy = tfidf_correct / total if total else 0.0
    gain_points = (improved_accuracy - original_accuracy) * 100
    tfidf_gap = (tfidf_accuracy - improved_accuracy) * 100

    improved_categories = []
    weak_categories = []
    for category, stats in sorted(summary["category_stats"].items()):
        delta = stats["improved_correct"] - stats["original_correct"]
        if delta > 0:
            improved_categories.append(f"- `{category}`: +{delta} correct")
        if stats["improved_correct"] / stats["total"] < 0.6:
            weak_categories.append(
                f"- `{category}`: {stats['improved_correct']}/{stats['total']} correct, "
                f"{format_accuracy(stats['improved_correct'], stats['total'])}"
            )

    content = f"""# Rule V2 Improvement Summary (v0.10.0-rule-v2-improvement)

## 목적

이 문서는 `data/raw/wizard_defense_inquiries_v2.csv` 기준으로 original rule-based classifier와 별도 improved rule-based classifier를 비교한 실험 결과를 기록합니다. 원본 rule classifier는 재현 가능하도록 유지했고, 개선 규칙은 `backend/app/rule_classifier_v2.py`에 별도 구현했습니다.

## 사용한 dataset

- Dataset: `data/raw/wizard_defense_inquiries_v2.csv`
- Total samples: {total}
- Original rule prediction: `experiments/rule_classifier_predictions_v2.csv`
- Improved rule prediction: `experiments/rule_v2_improved_predictions.csv`
- TF-IDF prediction: `experiments/tfidf_predictions_v2.csv`
- Comparison output: `experiments/rule_v2_improvement_comparison.csv`
- Evaluation script: `backend/scripts/evaluate_rule_v2_improvement.py`

## 전체 결과

- Original rule-based correct: {original_correct} / {total}
- Original rule-based accuracy: {format_accuracy(original_correct, total)}
- Improved rule-based correct: {improved_correct} / {total}
- Improved rule-based accuracy: {format_accuracy(improved_correct, total)}
- TF-IDF correct: {tfidf_correct} / {total}
- TF-IDF accuracy: {format_accuracy(tfidf_correct, total)}
- Improved rule gain/loss: {format_delta(gain_points)}
- Improved gain rows: {summary['improved_gain']}
- Improved loss rows: {summary['improved_loss']}

## category별 original vs improved 비교표

{make_category_table(summary)}

## improved rule이 좋아진 category

{chr(10).join(improved_categories) if improved_categories else "- 개선된 category가 없습니다."}

## 아직 약한 category

{chr(10).join(weak_categories) if weak_categories else "- improved rule 기준 60% 미만 category가 없습니다."}

## TF-IDF와의 차이

- TF-IDF accuracy는 {format_accuracy(tfidf_correct, total)}이고 improved rule accuracy는 {format_accuracy(improved_correct, total)}입니다.
- TF-IDF 대비 improved rule gap은 {format_delta(-tfidf_gap)}입니다.
- Improved rule은 의도 경계가 명확한 키워드와 우선순위를 설명하기 쉽지만, TF-IDF는 v2의 다양한 표현을 더 넓게 포착했습니다.
- v2에서는 improved rule이 TF-IDF보다 높은 accuracy를 기록했지만, 규칙이 dataset v2의 표현 분포에 강하게 맞춰져 있을 수 있으므로 다음 평가에서는 일반화 가능성을 별도로 확인해야 합니다.

## 다음 작업 제안

- `rule_v2_improvement_comparison.csv`에서 `improved_loss` row를 확인해 과도한 priority rule을 줄입니다.
- `bug_report`와 `feedback_balance`는 더 세밀한 hard failure signal과 complaint signal을 분리합니다.
- `gameplay_guide`와 `skill_combat` 경계는 전략 요청과 계산/판정 요청을 더 명확히 나누는 규칙을 추가 검토합니다.
- 다음 실험에서는 rule 개선과 TF-IDF feature engineering을 같은 v2 dataset에서 비교합니다.
"""
    path.write_text(content, encoding="utf-8")


def print_results(summary: Dict) -> None:
    total = summary["total"]
    print("Rule V2 Improvement Evaluation")
    print("=" * 40)
    print(f"Total samples: {total}")
    print(
        f"Original rule: {summary['original_correct']} "
        f"({format_accuracy(summary['original_correct'], total)})"
    )
    print(
        f"Improved rule: {summary['improved_correct']} "
        f"({format_accuracy(summary['improved_correct'], total)})"
    )
    print(
        f"TF-IDF: {summary['tfidf_correct']} "
        f"({format_accuracy(summary['tfidf_correct'], total)})"
    )
    print(f"Improved gains: {summary['improved_gain']}")
    print(f"Improved losses: {summary['improved_loss']}")
    print()
    print("Per-category comparison")
    print("-" * 40)
    for category in sorted(summary["category_stats"]):
        stats = summary["category_stats"][category]
        category_total = stats["total"]
        print(
            f"{category}: total={category_total}, "
            f"original={stats['original_correct']} "
            f"({format_accuracy(stats['original_correct'], category_total)}), "
            f"improved={stats['improved_correct']} "
            f"({format_accuracy(stats['improved_correct'], category_total)}), "
            f"tfidf={stats['tfidf_correct']} "
            f"({format_accuracy(stats['tfidf_correct'], category_total)}), "
            f"gain={stats['improved_gain']}, loss={stats['improved_loss']}"
        )


def main() -> None:
    dataset_rows = load_csv(DATASET_PATH)
    original_rows = load_csv(ORIGINAL_RULE_PATH)
    tfidf_rows = load_csv(TFIDF_PATH)

    improved_rows = evaluate_improved(dataset_rows)
    comparison_rows = compare_predictions(original_rows, improved_rows, tfidf_rows)
    summary = summarize(comparison_rows)

    save_csv(IMPROVED_OUTPUT_PATH, PREDICTION_FIELDS, improved_rows)
    save_csv(COMPARISON_OUTPUT_PATH, COMPARISON_FIELDS, comparison_rows)
    write_summary(SUMMARY_OUTPUT_PATH, summary)
    print_results(summary)
    print(f"Saved improved predictions: {IMPROVED_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Saved comparison: {COMPARISON_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Saved summary: {SUMMARY_OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
