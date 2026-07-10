"""Generate deterministic local reports from a batch support preview CSV."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_PATH = ROOT / "experiments" / "batch_support_preview_outputs.csv"
DEFAULT_REPORT_PATH = ROOT / "experiments" / "batch_support_analysis_report.md"
DEFAULT_CATEGORY_SUMMARY_PATH = ROOT / "experiments" / "batch_support_category_summary.csv"
DEFAULT_MISMATCH_PATH = ROOT / "experiments" / "batch_support_mismatch_samples.csv"

CATEGORY_SUMMARY_COLUMNS = ["expected_category", "total", "correct", "mismatch", "accuracy"]
MISMATCH_COLUMNS = [
    "id",
    "text",
    "expected_category",
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
    "routing_reason",
]
REQUIRED_INPUT_COLUMNS = {
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
}


@dataclass
class AnalysisResult:
    total_rows: int
    comparable_rows: int
    match_count: int
    mismatch_count: int
    accuracy: Optional[float]
    needs_human_counts: Counter
    predicted_category_counts: Counter
    expected_category_counts: Counter
    urgency_counts: Counter
    response_type_counts: Counter
    category_summary: List[Dict[str, str]]

    @property
    def needs_human_count(self) -> int:
        return self.needs_human_counts["true"]

    @property
    def needs_human_ratio(self) -> float:
        return self.needs_human_count / self.total_rows if self.total_rows else 0.0


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _validate_paths(
    input_path: Path,
    report_path: Path,
    category_summary_path: Path,
    mismatch_path: Path,
) -> None:
    output_pairs = [
        (report_path, DEFAULT_REPORT_PATH),
        (category_summary_path, DEFAULT_CATEGORY_SUMMARY_PATH),
        (mismatch_path, DEFAULT_MISMATCH_PATH),
    ]
    resolved_outputs = [path.resolve() for path, _ in output_pairs]
    if len(set(resolved_outputs)) != len(resolved_outputs):
        raise ValueError("analysis output paths must be different")
    if input_path.resolve() in resolved_outputs:
        raise ValueError("input path must not be used as an output path")

    experiments_path = (ROOT / "experiments").resolve()
    for output_path, allowed_path in output_pairs:
        resolved_output = output_path.resolve()
        if resolved_output.parent == experiments_path and resolved_output != allowed_path.resolve():
            raise ValueError(f"output inside experiments must use {allowed_path.name}")


def _read_rows(input_path: Path) -> List[Dict[str, str]]:
    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_INPUT_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"input CSV is missing required columns: {', '.join(missing)}")
        return list(reader)


def _build_category_summary(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    comparable_rows = [row for row in rows if (row.get("expected_category") or "").strip()]
    summary = []
    for category in sorted({row["expected_category"].strip() for row in comparable_rows}):
        category_rows = [row for row in comparable_rows if row["expected_category"].strip() == category]
        correct = sum(row.get("predicted_category", "").strip() == category for row in category_rows)
        total = len(category_rows)
        summary.append(
            {
                "expected_category": category,
                "total": str(total),
                "correct": str(correct),
                "mismatch": str(total - correct),
                "accuracy": f"{correct / total:.4f}",
            }
        )
    return summary


def _write_csv(path: Path, columns: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows({column: row.get(column, "") for column in columns} for row in rows)


def _count_lines(counts: Counter) -> str:
    if not counts:
        return "- 해당 데이터가 없습니다."
    return "\n".join(f"- `{name}`: {count}개" for name, count in sorted(counts.items()))


def _escape_markdown(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _category_table(summary: List[Dict[str, str]]) -> str:
    if not summary:
        return "비어 있지 않은 `expected_category`가 없어 category별 accuracy를 계산하지 않았습니다."
    lines = [
        "| expected_category | total | correct | mismatch | accuracy |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(
            f"| `{_escape_markdown(row['expected_category'])}` | {row['total']} | "
            f"{row['correct']} | {row['mismatch']} | {float(row['accuracy']):.2%} |"
        )
    return "\n".join(lines)


def _mismatch_table(rows: List[Dict[str, str]]) -> str:
    if not rows:
        return "선택된 mismatch sample이 없습니다."
    lines = [
        "| id | text | expected_category | predicted_category |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {_escape_markdown(row.get('id', ''))} | {_escape_markdown(row.get('text', ''))} | "
            f"`{_escape_markdown(row.get('expected_category', ''))}` | "
            f"`{_escape_markdown(row.get('predicted_category', ''))}` |"
        )
    return "\n".join(lines)


def _write_report(
    path: Path,
    input_path: Path,
    result: AnalysisResult,
    mismatch_samples: List[Dict[str, str]],
) -> None:
    accuracy_text = f"{result.accuracy:.2%}" if result.accuracy is not None else "계산하지 않음"
    content = f"""# Batch Support 분석 보고서 (v0.17.0-batch-analysis-report)

## 1. 목적

기존 batch support preview output을 집계해 분류 성능, 사람 검토 비율, urgency와 response type 분포, 대표 mismatch를 portfolio에서 검토할 수 있도록 정리합니다.

## 2. 입력 파일

- `{_display_path(input_path)}`
- 입력 CSV는 읽기 전용으로 사용하며 수정하거나 덮어쓰지 않습니다.

## 3. 전체 요약

- 전체 row: {result.total_rows}개
- Expected category 비교 가능 row: {result.comparable_rows}개
- Match: {result.match_count}개
- Mismatch: {result.mismatch_count}개
- Accuracy: {accuracy_text}
- `needs_human=true`: {result.needs_human_count}개 ({result.needs_human_ratio:.2%})
- Predicted category 종류: {len(result.predicted_category_counts)}개
- Suggested response type 종류: {len(result.response_type_counts)}개

## 4. Predicted category 분포

{_count_lines(result.predicted_category_counts)}

## 5. Expected category 분포

{_count_lines(result.expected_category_counts)}

## 6. Expected vs predicted 결과

- 비교 가능 row: {result.comparable_rows}개
- 일치: {result.match_count}개
- 불일치: {result.mismatch_count}개
- Accuracy: {accuracy_text}

## 7. Category별 accuracy

{_category_table(result.category_summary)}

## 8. needs_human 분석

{_count_lines(result.needs_human_counts)}

- `needs_human=true` 비율: {result.needs_human_ratio:.2%}

## 9. Urgency 분포

{_count_lines(result.urgency_counts)}

## 10. Suggested response type 분포

{_count_lines(result.response_type_counts)}

## 11. Mismatch sample 요약

- 전체 mismatch: {result.mismatch_count}개
- Report에 표시한 sample: {len(mismatch_samples)}개
- 전체 선택 sample은 `experiments/batch_support_mismatch_samples.csv`에서 확인할 수 있습니다.

{_mismatch_table(mismatch_samples)}

## 12. 해석

- Accuracy는 비어 있지 않은 `expected_category`가 있는 row만 기준으로 계산합니다.
- Category별 accuracy는 어떤 expected label에서 rule-based 경계가 약한지 비교하는 지표입니다.
- `needs_human`과 `suggested_response_type`은 category prediction뿐 아니라 기존 router의 오류 신호와 검토 정책도 반영합니다.
- 이 결과는 현재 고정 dataset과 rule에 대한 재현 가능한 local 분석이며 production 성능을 의미하지 않습니다.

## 13. 안전 제한사항

- 외부 API와 LLM API를 호출하지 않습니다.
- 실제 API key, helpdesk, Gmail, Slack, Discord integration을 사용하지 않습니다.
- 입력 batch preview CSV와 dataset을 수정하지 않습니다.

## 14. 한계

- 동일한 dataset v2를 기반으로 만든 batch preview를 분석하므로 독립 holdout 평가가 아닙니다.
- Keyword와 priority rule의 오분류 원인을 자동으로 확정하지 않습니다.
- Accuracy는 category 일치만 측정하며 response draft 품질이나 실제 운영 만족도를 평가하지 않습니다.

## 15. 다음 작업 제안

- 별도 승인 후 mismatch pattern을 category pair 기준으로 세분화합니다.
- 독립 holdout sample이 준비되면 같은 report contract로 재평가합니다.
- 운영 적용 전에는 human-review workload와 response safety를 별도 지표로 정의합니다.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig")


def analyze_csv(
    input_path: Path,
    report_path: Path,
    category_summary_path: Path,
    mismatch_path: Path,
    mismatch_limit: int = 20,
) -> AnalysisResult:
    """Analyze one batch preview CSV and write all requested report artifacts."""
    input_path = Path(input_path)
    report_path = Path(report_path)
    category_summary_path = Path(category_summary_path)
    mismatch_path = Path(mismatch_path)
    if mismatch_limit < 0:
        raise ValueError("mismatch limit must be zero or greater")
    _validate_paths(input_path, report_path, category_summary_path, mismatch_path)

    rows = _read_rows(input_path)
    expected_rows = [row for row in rows if (row.get("expected_category") or "").strip()]
    mismatches = [
        row
        for row in expected_rows
        if row.get("predicted_category", "").strip() != row["expected_category"].strip()
    ]
    mismatch_samples = mismatches[:mismatch_limit]
    match_count = len(expected_rows) - len(mismatches)
    category_summary = _build_category_summary(rows)

    needs_human_counts = Counter(
        "true" if (row.get("needs_human") or "").strip().lower() == "true" else "false"
        for row in rows
    )
    # Always expose both boolean values in the analysis contract.
    needs_human_counts["true"] += 0
    needs_human_counts["false"] += 0

    result = AnalysisResult(
        total_rows=len(rows),
        comparable_rows=len(expected_rows),
        match_count=match_count,
        mismatch_count=len(mismatches),
        accuracy=match_count / len(expected_rows) if expected_rows else None,
        needs_human_counts=needs_human_counts,
        predicted_category_counts=Counter(row.get("predicted_category", "").strip() for row in rows),
        expected_category_counts=Counter(row["expected_category"].strip() for row in expected_rows),
        urgency_counts=Counter(row.get("urgency", "").strip() for row in rows),
        response_type_counts=Counter(row.get("suggested_response_type", "").strip() for row in rows),
        category_summary=category_summary,
    )

    _write_csv(category_summary_path, CATEGORY_SUMMARY_COLUMNS, category_summary)
    _write_csv(mismatch_path, MISMATCH_COLUMNS, mismatch_samples)
    _write_report(report_path, input_path, result, mismatch_samples)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a local batch support preview CSV.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--category-summary-output", type=Path, default=DEFAULT_CATEGORY_SUMMARY_PATH)
    parser.add_argument("--mismatch-output", type=Path, default=DEFAULT_MISMATCH_PATH)
    parser.add_argument("--mismatch-limit", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = analyze_csv(
        args.input,
        args.report_output,
        args.category_summary_output,
        args.mismatch_output,
        args.mismatch_limit,
    )
    print("Batch Support Analysis")
    print(f"Input: {args.input}")
    print(f"Report: {args.report_output}")
    print(f"Total rows: {result.total_rows}")
    print(f"Needs human: {result.needs_human_count}")
    print(f"Mismatches: {result.mismatch_count}")
    print(f"Category count: {len(result.predicted_category_counts)}")
    print(f"Response type count: {len(result.response_type_counts)}")


if __name__ == "__main__":
    main()
