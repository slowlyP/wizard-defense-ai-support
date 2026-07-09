"""
Compare rule-based and TF-IDF baseline prediction outputs.

Run from repository root:
python backend/scripts/compare_baselines.py
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[2]
RULE_PREDICTIONS_PATH = REPO_ROOT / "experiments" / "rule_classifier_predictions.csv"
TFIDF_PREDICTIONS_PATH = REPO_ROOT / "experiments" / "tfidf_predictions.csv"
OUTPUT_PATH = REPO_ROOT / "experiments" / "baseline_comparison.csv"


COMPARISON_FIELDS = [
    "id",
    "text",
    "expected_category",
    "rule_predicted_category",
    "tfidf_predicted_category",
    "rule_correct",
    "tfidf_correct",
    "comparison_type",
]


def load_predictions(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def index_by_id(rows: Iterable[Dict[str, str]], source_name: str) -> Dict[str, Dict[str, str]]:
    indexed: Dict[str, Dict[str, str]] = {}

    for row in rows:
        row_id = row.get("id", "")
        if not row_id:
            raise ValueError(f"{source_name} contains a row without id.")
        if row_id in indexed:
            raise ValueError(f"{source_name} contains duplicate id: {row_id}")
        indexed[row_id] = row

    return indexed


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def format_accuracy(correct: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{(correct / total) * 100:.2f}%"


def get_comparison_type(rule_correct: bool, tfidf_correct: bool) -> str:
    if rule_correct and tfidf_correct:
        return "both_correct"
    if not rule_correct and not tfidf_correct:
        return "both_wrong"
    if rule_correct:
        return "rule_only_correct"
    return "tfidf_only_correct"


def compare_predictions(
    rule_rows: List[Dict[str, str]],
    tfidf_rows: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rule_by_id = index_by_id(rule_rows, "rule_classifier_predictions.csv")
    tfidf_by_id = index_by_id(tfidf_rows, "tfidf_predictions.csv")

    rule_ids = set(rule_by_id)
    tfidf_ids = set(tfidf_by_id)
    if rule_ids != tfidf_ids:
        missing_from_rule = sorted(tfidf_ids - rule_ids, key=int)
        missing_from_tfidf = sorted(rule_ids - tfidf_ids, key=int)
        raise ValueError(
            "Prediction ids do not match. "
            f"missing_from_rule={missing_from_rule}, "
            f"missing_from_tfidf={missing_from_tfidf}"
        )

    comparison_rows: List[Dict[str, str]] = []
    for row_id in sorted(rule_ids, key=int):
        rule_row = rule_by_id[row_id]
        tfidf_row = tfidf_by_id[row_id]

        expected_category = rule_row.get("expected_category", "")
        if expected_category != tfidf_row.get("expected_category", ""):
            raise ValueError(f"Expected category mismatch for id={row_id}.")

        text = rule_row.get("text", "")
        if text != tfidf_row.get("text", ""):
            raise ValueError(f"Text mismatch for id={row_id}.")

        rule_correct = parse_bool(rule_row.get("correct", "false"))
        tfidf_correct = parse_bool(tfidf_row.get("correct", "false"))

        comparison_rows.append(
            {
                "id": row_id,
                "text": text,
                "expected_category": expected_category,
                "rule_predicted_category": rule_row.get("predicted_category", ""),
                "tfidf_predicted_category": tfidf_row.get("predicted_category", ""),
                "rule_correct": str(rule_correct).lower(),
                "tfidf_correct": str(tfidf_correct).lower(),
                "comparison_type": get_comparison_type(rule_correct, tfidf_correct),
            }
        )

    return comparison_rows


def summarize(comparison_rows: List[Dict[str, str]]) -> Dict:
    summary = {
        "total": len(comparison_rows),
        "rule_correct": 0,
        "tfidf_correct": 0,
        "both_correct": 0,
        "both_wrong": 0,
        "rule_only_correct": 0,
        "tfidf_only_correct": 0,
        "category_stats": defaultdict(
            lambda: {
                "total": 0,
                "rule_correct": 0,
                "tfidf_correct": 0,
                "both_correct": 0,
                "both_wrong": 0,
                "rule_only_correct": 0,
                "tfidf_only_correct": 0,
            }
        ),
    }

    for row in comparison_rows:
        category = row["expected_category"]
        comparison_type = row["comparison_type"]
        rule_correct = parse_bool(row["rule_correct"])
        tfidf_correct = parse_bool(row["tfidf_correct"])

        summary["rule_correct"] += int(rule_correct)
        summary["tfidf_correct"] += int(tfidf_correct)
        summary[comparison_type] += 1

        category_stats = summary["category_stats"][category]
        category_stats["total"] += 1
        category_stats["rule_correct"] += int(rule_correct)
        category_stats["tfidf_correct"] += int(tfidf_correct)
        category_stats[comparison_type] += 1

    summary["category_stats"] = dict(summary["category_stats"])
    return summary


def save_comparison(path: Path, comparison_rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=COMPARISON_FIELDS)
        writer.writeheader()
        writer.writerows(comparison_rows)


def print_results(summary: Dict) -> None:
    total = summary["total"]
    rule_correct = summary["rule_correct"]
    tfidf_correct = summary["tfidf_correct"]

    print("Baseline Comparison")
    print("=" * 40)
    print(f"Total samples: {total}")
    print(
        f"Rule-based correct: {rule_correct} "
        f"({format_accuracy(rule_correct, total)})"
    )
    print(
        f"TF-IDF correct: {tfidf_correct} "
        f"({format_accuracy(tfidf_correct, total)})"
    )
    print(f"Both correct: {summary['both_correct']}")
    print(f"Both wrong: {summary['both_wrong']}")
    print(f"Rule-only correct: {summary['rule_only_correct']}")
    print(f"TF-IDF-only correct: {summary['tfidf_only_correct']}")
    print()

    print("Per-category comparison summary")
    print("-" * 40)
    for category in sorted(summary["category_stats"]):
        stats = summary["category_stats"][category]
        category_total = stats["total"]
        print(
            f"{category}: total={category_total}, "
            f"rule_correct={stats['rule_correct']} "
            f"({format_accuracy(stats['rule_correct'], category_total)}), "
            f"tfidf_correct={stats['tfidf_correct']} "
            f"({format_accuracy(stats['tfidf_correct'], category_total)}), "
            f"both_correct={stats['both_correct']}, "
            f"both_wrong={stats['both_wrong']}, "
            f"rule_only_correct={stats['rule_only_correct']}, "
            f"tfidf_only_correct={stats['tfidf_only_correct']}"
        )


def main() -> None:
    rule_rows = load_predictions(RULE_PREDICTIONS_PATH)
    tfidf_rows = load_predictions(TFIDF_PREDICTIONS_PATH)
    comparison_rows = compare_predictions(rule_rows, tfidf_rows)
    summary = summarize(comparison_rows)

    save_comparison(OUTPUT_PATH, comparison_rows)
    print_results(summary)
    print(f"Saved comparison: {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
