"""
Evaluate rule-based and TF-IDF baselines on dataset v2.

Run from repository root:
python backend/scripts/evaluate_v2_baselines.py
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Dict, Iterable, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from backend.app.rule_classifier import classify_inquiry


DATASET_PATH = REPO_ROOT / "data" / "raw" / "wizard_defense_inquiries_v2.csv"
RULE_OUTPUT_PATH = REPO_ROOT / "experiments" / "rule_classifier_predictions_v2.csv"
TFIDF_OUTPUT_PATH = REPO_ROOT / "experiments" / "tfidf_predictions_v2.csv"
COMPARISON_OUTPUT_PATH = REPO_ROOT / "experiments" / "baseline_comparison_v2.csv"
SUMMARY_OUTPUT_PATH = REPO_ROOT / "experiments" / "v2_baseline_evaluation_summary.md"

RANDOM_STATE = 42
N_SPLITS = 5


RULE_PREDICTION_FIELDS = [
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

TFIDF_PREDICTION_FIELDS = [
    "id",
    "text",
    "expected_category",
    "predicted_category",
    "correct",
]

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


def load_dataset(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def format_accuracy(correct: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{(correct / total) * 100:.2f}%"


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def get_comparison_type(rule_correct: bool, tfidf_correct: bool) -> str:
    if rule_correct and tfidf_correct:
        return "both_correct"
    if not rule_correct and not tfidf_correct:
        return "both_wrong"
    if rule_correct:
        return "rule_only_correct"
    return "tfidf_only_correct"


def build_tfidf_pipeline() -> Pipeline:
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


def evaluate_rule_based(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    predictions = []

    for row in rows:
        result = classify_inquiry(row.get("text", ""))
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


def evaluate_tfidf(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    texts = [row["text"] for row in rows]
    expected = [row["category"] for row in rows]

    min_category_count = min(Counter(expected).values())
    n_splits = min(N_SPLITS, min_category_count)
    if n_splits < 2:
        raise SystemExit("At least two samples per category are required for StratifiedKFold.")

    pipeline = build_tfidf_pipeline()
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    predicted = list(cross_val_predict(pipeline, texts, expected, cv=cv))

    predictions = []
    for row, predicted_category in zip(rows, predicted):
        expected_category = row["category"]
        predictions.append(
            {
                "id": row["id"],
                "text": row["text"],
                "expected_category": expected_category,
                "predicted_category": predicted_category,
                "correct": str(expected_category == predicted_category).lower(),
            }
        )

    return predictions


def save_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def compare_predictions(
    rule_predictions: List[Dict[str, str]],
    tfidf_predictions: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    tfidf_by_id = {row["id"]: row for row in tfidf_predictions}
    comparison_rows = []

    for rule_row in rule_predictions:
        row_id = rule_row["id"]
        tfidf_row = tfidf_by_id[row_id]

        rule_correct = parse_bool(rule_row["correct"])
        tfidf_correct = parse_bool(tfidf_row["correct"])

        comparison_rows.append(
            {
                "id": row_id,
                "text": rule_row["text"],
                "expected_category": rule_row["expected_category"],
                "rule_predicted_category": rule_row["predicted_category"],
                "tfidf_predicted_category": tfidf_row["predicted_category"],
                "rule_correct": rule_row["correct"],
                "tfidf_correct": tfidf_row["correct"],
                "comparison_type": get_comparison_type(rule_correct, tfidf_correct),
            }
        )

    return comparison_rows


def summarize_comparison(comparison_rows: List[Dict[str, str]]) -> Dict:
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


def make_category_table(summary: Dict) -> str:
    lines = [
        "| category | total | rule-based correct | rule-based accuracy | TF-IDF correct | TF-IDF accuracy | both correct | both wrong | rule-only correct | TF-IDF-only correct |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for category in sorted(summary["category_stats"]):
        stats = summary["category_stats"][category]
        total = stats["total"]
        lines.append(
            f"| `{category}` | {total} | {stats['rule_correct']} | "
            f"{format_accuracy(stats['rule_correct'], total)} | "
            f"{stats['tfidf_correct']} | {format_accuracy(stats['tfidf_correct'], total)} | "
            f"{stats['both_correct']} | {stats['both_wrong']} | "
            f"{stats['rule_only_correct']} | {stats['tfidf_only_correct']} |"
        )
    return "\n".join(lines)


def write_summary(path: Path, summary: Dict) -> None:
    total = summary["total"]
    rule_correct = summary["rule_correct"]
    tfidf_correct = summary["tfidf_correct"]
    rule_accuracy = format_accuracy(rule_correct, total)
    tfidf_accuracy = format_accuracy(tfidf_correct, total)
    rule_delta = (rule_correct / total) - 0.60 if total else 0.0
    tfidf_delta = (tfidf_correct / total) - 0.58 if total else 0.0

    content = f"""# V2 Baseline Evaluation Summary (v0.9.0-v2-baseline-evaluation)

## 목적

이 문서는 `data/raw/wizard_defense_inquiries_v2.csv`에 대해 기존 rule-based classifier와 TF-IDF + LogisticRegression baseline을 평가한 결과를 기록합니다. dataset v2는 v0.7.0 data quality review 이후 라벨 경계와 약한 category를 보강하기 위해 생성되었으며, 이번 평가는 v2가 baseline 성능과 오분류 구조에 어떤 변화를 주었는지 확인하기 위한 기준선입니다.

## 사용한 dataset

- Dataset: `data/raw/wizard_defense_inquiries_v2.csv`
- Total samples: {total}
- Rule-based output: `experiments/rule_classifier_predictions_v2.csv`
- TF-IDF output: `experiments/tfidf_predictions_v2.csv`
- Comparison output: `experiments/baseline_comparison_v2.csv`
- Evaluation script: `backend/scripts/evaluate_v2_baselines.py`

## 전체 비교 결과

- Rule-based correct: {rule_correct} / {total}
- Rule-based accuracy: {rule_accuracy}
- TF-IDF correct: {tfidf_correct} / {total}
- TF-IDF accuracy: {tfidf_accuracy}
- Both correct: {summary['both_correct']}
- Both wrong: {summary['both_wrong']}
- Rule-only correct: {summary['rule_only_correct']}
- TF-IDF-only correct: {summary['tfidf_only_correct']}

## category별 비교표

{make_category_table(summary)}

## v1 대비 해석

- v1 baseline은 100 samples 기준 rule-based 60.00%, TF-IDF 58.00%, both correct 40, both wrong 22였습니다.
- v2 baseline은 150 samples 기준 rule-based {rule_accuracy}, TF-IDF {tfidf_accuracy}, both correct {summary['both_correct']}, both wrong {summary['both_wrong']}입니다.
- Rule-based accuracy 변화: {format_percent(rule_delta)}
- TF-IDF accuracy 변화: {format_percent(tfidf_delta)}
- v2는 더 많은 `bug_report`와 `feedback_balance` 경계 사례를 포함하므로, 단순 정확도만으로 v1보다 쉬운 dataset이라고 해석하면 안 됩니다. v2 평가는 보강된 ambiguous case에서 두 baseline이 어떤 약점을 유지하는지 확인하는 목적이 더 큽니다.

## v2에서 개선된 점

- `bug_report`와 `feedback_balance` 샘플 수를 늘려 v1에서 약했던 category를 더 안정적으로 관찰할 수 있게 되었습니다.
- 기능 단어가 포함된 오류 문의와 평가 문의를 분리해 라벨 정책 검증에 더 적합한 샘플을 포함했습니다.
- `wizard_growth` vs `wizard_acquisition`, `gameplay_guide` vs `wizard_growth`, `gameplay_guide` vs `skill_combat` 경계 사례가 늘어났습니다.
- v1 evaluation output을 덮어쓰지 않고 `_v2` output으로 분리해 비교 가능성을 보존했습니다.

## 아직 남은 약점

- Rule-based classifier는 기존 keyword rule을 그대로 사용하므로 v2에서 새로 보강된 표현을 충분히 반영하지 못할 수 있습니다.
- TF-IDF baseline은 char n-gram 기반이므로 기능 단어와 의도 단어가 함께 있는 문장에서 핵심 의도를 안정적으로 분리하기 어렵습니다.
- `bug_report`와 `feedback_balance`는 feature word가 함께 등장할 때 여전히 다른 category와 충돌할 가능성이 큽니다.
- 이번 평가는 baseline evaluation이며 classifier logic 개선은 포함하지 않았습니다.

## 다음 작업 제안

- `baseline_comparison_v2.csv`에서 both wrong과 model-only correct 샘플을 분리해 v2 error analysis를 확장합니다.
- rule-based classifier는 v2 결과를 참고해 keyword 우선순위와 경계 규칙 개선 후보를 별도 실험으로 검토합니다.
- TF-IDF baseline은 feature engineering 또는 더 큰 train/evaluation split 전략을 별도 실험으로 검토합니다.
- dataset v2 기준 검색/응답 pipeline 평가를 진행하기 전, classifier baseline의 실패 유형을 먼저 문서화합니다.
"""
    path.write_text(content, encoding="utf-8")


def print_results(summary: Dict) -> None:
    total = summary["total"]
    rule_correct = summary["rule_correct"]
    tfidf_correct = summary["tfidf_correct"]

    print("Dataset v2 Baseline Evaluation")
    print("=" * 40)
    print(f"Total samples: {total}")
    print(f"Rule-based correct: {rule_correct} ({format_accuracy(rule_correct, total)})")
    print(f"TF-IDF correct: {tfidf_correct} ({format_accuracy(tfidf_correct, total)})")
    print(f"Both correct: {summary['both_correct']}")
    print(f"Both wrong: {summary['both_wrong']}")
    print(f"Rule-only correct: {summary['rule_only_correct']}")
    print(f"TF-IDF-only correct: {summary['tfidf_only_correct']}")
    print()
    print("Per-category comparison summary")
    print("-" * 40)
    for category in sorted(summary["category_stats"]):
        stats = summary["category_stats"][category]
        total_for_category = stats["total"]
        print(
            f"{category}: total={total_for_category}, "
            f"rule_correct={stats['rule_correct']} "
            f"({format_accuracy(stats['rule_correct'], total_for_category)}), "
            f"tfidf_correct={stats['tfidf_correct']} "
            f"({format_accuracy(stats['tfidf_correct'], total_for_category)}), "
            f"both_correct={stats['both_correct']}, "
            f"both_wrong={stats['both_wrong']}, "
            f"rule_only_correct={stats['rule_only_correct']}, "
            f"tfidf_only_correct={stats['tfidf_only_correct']}"
        )


def main() -> None:
    rows = load_dataset(DATASET_PATH)
    rule_predictions = evaluate_rule_based(rows)
    tfidf_predictions = evaluate_tfidf(rows)
    comparison_rows = compare_predictions(rule_predictions, tfidf_predictions)
    summary = summarize_comparison(comparison_rows)

    save_csv(RULE_OUTPUT_PATH, RULE_PREDICTION_FIELDS, rule_predictions)
    save_csv(TFIDF_OUTPUT_PATH, TFIDF_PREDICTION_FIELDS, tfidf_predictions)
    save_csv(COMPARISON_OUTPUT_PATH, COMPARISON_FIELDS, comparison_rows)
    write_summary(SUMMARY_OUTPUT_PATH, summary)
    print_results(summary)
    print(f"Saved rule predictions: {RULE_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Saved TF-IDF predictions: {TFIDF_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Saved comparison: {COMPARISON_OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Saved summary: {SUMMARY_OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
