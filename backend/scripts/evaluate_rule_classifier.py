"""
Rule-based classifier evaluation script.

Run from repository root:
python backend/scripts/evaluate_rule_classifier.py
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


from backend.app.rule_classifier import classify_inquiry


DATASET_PATH = REPO_ROOT / "data" / "raw" / "wizard_defense_inquiries_raw.csv"
OUTPUT_PATH = REPO_ROOT / "experiments" / "rule_classifier_predictions.csv"


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


def load_dataset(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def format_accuracy(correct: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{(correct / total) * 100:.2f}%"


def evaluate(rows: Iterable[Dict[str, str]]) -> Dict:
    predictions = []
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    total = 0
    correct = 0

    for row in rows:
        result = classify_inquiry(row.get("text", ""))
        expected_category = row.get("category", "")
        predicted_category = result.get("category", "")
        is_correct = expected_category == predicted_category

        total += 1
        if is_correct:
            correct += 1

        category_stats[expected_category]["total"] += 1
        if is_correct:
            category_stats[expected_category]["correct"] += 1

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

    mismatches = [prediction for prediction in predictions if prediction["correct"] != "true"]
    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total else 0.0,
        "category_stats": dict(category_stats),
        "predictions": predictions,
        "mismatches": mismatches,
    }


def save_predictions(path: Path, predictions: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=PREDICTION_FIELDS)
        writer.writeheader()
        writer.writerows(predictions)


def print_results(results: Dict) -> None:
    total = results["total"]
    correct = results["correct"]

    print("Rule-based Classifier Evaluation")
    print("=" * 40)
    print(f"Total samples: {total}")
    print(f"Correct samples: {correct}")
    print(f"Accuracy: {format_accuracy(correct, total)}")
    print()

    print("Per-category results")
    print("-" * 40)
    for category in sorted(results["category_stats"]):
        stats = results["category_stats"][category]
        category_total = stats["total"]
        category_correct = stats["correct"]
        print(
            f"{category}: total={category_total}, "
            f"correct={category_correct}, "
            f"accuracy={format_accuracy(category_correct, category_total)}"
        )
    print()

    mismatches = results["mismatches"]
    print(f"Mismatched examples: {len(mismatches)}")
    print("-" * 40)
    for mismatch in mismatches[:20]:
        print(
            f"[{mismatch['id']}] expected={mismatch['expected_category']} "
            f"predicted={mismatch['predicted_category']} "
            f"confidence={mismatch['confidence']}"
        )
        print(f"text: {mismatch['text']}")
        print(f"matched_keywords: {mismatch['matched_keywords']}")
        print()

    if len(mismatches) > 20:
        print(f"... {len(mismatches) - 20} more mismatches omitted from console output.")


def main() -> None:
    rows = load_dataset(DATASET_PATH)
    results = evaluate(rows)
    save_predictions(OUTPUT_PATH, results["predictions"])
    print_results(results)
    print(f"Saved predictions: {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
