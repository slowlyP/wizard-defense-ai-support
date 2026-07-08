"""
TF-IDF baseline classifier evaluation script.

Run from repository root:
python backend/scripts/evaluate_tfidf_classifier.py
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
import sys
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline


REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = REPO_ROOT / "data" / "raw" / "wizard_defense_inquiries_raw.csv"
OUTPUT_PATH = REPO_ROOT / "experiments" / "tfidf_predictions.csv"
RANDOM_STATE = 42
N_SPLITS = 5


PREDICTION_FIELDS = [
    "id",
    "text",
    "expected_category",
    "predicted_category",
    "correct",
]


def load_dataset(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(2, 4),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def format_accuracy(value: float) -> str:
    return f"{value * 100:.2f}%"


def save_predictions(path: Path, rows: List[Dict[str, str]], predictions: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=PREDICTION_FIELDS)
        writer.writeheader()
        for row, predicted_category in zip(rows, predictions):
            expected_category = row["category"]
            writer.writerow(
                {
                    "id": row["id"],
                    "text": row["text"],
                    "expected_category": expected_category,
                    "predicted_category": predicted_category,
                    "correct": str(expected_category == predicted_category).lower(),
                }
            )


def print_confusion_summary(labels: List[str], expected: List[str], predicted: List[str]) -> None:
    matrix = confusion_matrix(expected, predicted, labels=labels)
    print("Confusion-style summary")
    print("-" * 40)
    print("rows=expected, columns=predicted")
    print(",".join(["expected\\predicted"] + labels))
    for label, row in zip(labels, matrix):
        print(",".join([label] + [str(value) for value in row]))
    print()


def print_mismatches(rows: List[Dict[str, str]], predicted: List[str], limit: int = 20) -> None:
    mismatches = [
        (row, predicted_category)
        for row, predicted_category in zip(rows, predicted)
        if row["category"] != predicted_category
    ]

    print(f"Mismatched examples: {len(mismatches)}")
    print("-" * 40)
    for row, predicted_category in mismatches[:limit]:
        print(
            f"[{row['id']}] expected={row['category']} "
            f"predicted={predicted_category}"
        )
        print(f"text: {row['text']}")
        print()

    if len(mismatches) > limit:
        print(f"... {len(mismatches) - limit} more mismatches omitted from console output.")


def main() -> None:
    rows = load_dataset(DATASET_PATH)
    texts = [row["text"] for row in rows]
    expected = [row["category"] for row in rows]
    labels = sorted(Counter(expected))

    min_category_count = min(Counter(expected).values())
    n_splits = min(N_SPLITS, min_category_count)
    if n_splits < 2:
        raise SystemExit("At least two samples per category are required for StratifiedKFold.")

    pipeline = build_pipeline()
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    predicted = cross_val_predict(pipeline, texts, expected, cv=cv)
    predicted_list = list(predicted)

    accuracy = accuracy_score(expected, predicted_list)
    report = classification_report(
        expected,
        predicted_list,
        labels=labels,
        digits=4,
        zero_division=0,
    )

    save_predictions(OUTPUT_PATH, rows, predicted_list)

    print("TF-IDF Baseline Classifier Evaluation")
    print("=" * 40)
    print(f"Total samples: {len(rows)}")
    print(f"Evaluation method: StratifiedKFold(n_splits={n_splits}, random_state={RANDOM_STATE})")
    print(f"Overall accuracy: {format_accuracy(accuracy)}")
    print()
    print("Per-category precision / recall / F1")
    print("-" * 40)
    print(report)
    print_confusion_summary(labels, expected, predicted_list)
    print_mismatches(rows, predicted_list)
    print(f"Saved predictions: {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    main()
