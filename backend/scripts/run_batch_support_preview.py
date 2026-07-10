"""Process a local inquiry CSV through the deterministic support preview flow."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.response_templates import generate_response_template  # noqa: E402
from backend.app.support_router import route_inquiry  # noqa: E402


DEFAULT_INPUT_PATH = ROOT / "data" / "raw" / "wizard_defense_inquiries_v2.csv"
DEFAULT_OUTPUT_PATH = ROOT / "experiments" / "batch_support_preview_outputs.csv"
OUTPUT_COLUMNS = [
    "id",
    "text",
    "expected_category",
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
    "routing_reason",
    "response_draft",
    "internal_note",
]
EXPECTED_CATEGORY_COLUMNS = ("expected_category", "label", "category")


@dataclass
class BatchResult:
    processed_count: int
    skipped_count: int
    needs_human_count: int
    category_counts: Counter
    response_type_counts: Counter


def _expected_category_column(fieldnames: List[str]) -> Optional[str]:
    return next((name for name in EXPECTED_CATEGORY_COLUMNS if name in fieldnames), None)


def _validate_paths(input_path: Path, output_path: Path) -> None:
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input path and output path must be different")

    # Inside experiments/, this tool may overwrite only its dedicated output.
    experiments_path = (ROOT / "experiments").resolve()
    resolved_output = output_path.resolve()
    if resolved_output.parent == experiments_path and resolved_output != DEFAULT_OUTPUT_PATH.resolve():
        raise ValueError("output inside experiments must use batch_support_preview_outputs.csv")


def process_csv(input_path: Path, output_path: Path, limit: Optional[int] = None) -> BatchResult:
    """Process valid text rows and skip empty or whitespace-only inquiry rows."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    if limit is not None and limit < 0:
        raise ValueError("limit must be zero or greater")
    _validate_paths(input_path, output_path)

    output_rows: List[Dict[str, str]] = []
    skipped_count = 0

    with input_path.open("r", newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames or []
        if "text" not in fieldnames:
            raise ValueError("input CSV must include a text column")

        expected_column = _expected_category_column(fieldnames)
        has_id = "id" in fieldnames

        for source_index, source_row in enumerate(reader, start=1):
            text = (source_row.get("text") or "").strip()
            if not text:
                skipped_count += 1
                continue
            if limit is not None and len(output_rows) >= limit:
                break

            route = route_inquiry(text)
            template = generate_response_template(route)
            output_rows.append(
                {
                    "id": source_row.get("id", "") if has_id else str(source_index),
                    "text": text,
                    "expected_category": source_row.get(expected_column, "") if expected_column else "",
                    "predicted_category": route["predicted_category"],
                    "urgency": route["urgency"],
                    "needs_human": str(route["needs_human"]).lower(),
                    "suggested_response_type": route["suggested_response_type"],
                    "routing_reason": route["routing_reason"],
                    "response_draft": template["response_draft"],
                    "internal_note": template["internal_note"],
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)

    return BatchResult(
        processed_count=len(output_rows),
        skipped_count=skipped_count,
        needs_human_count=sum(row["needs_human"] == "true" for row in output_rows),
        category_counts=Counter(row["predicted_category"] for row in output_rows),
        response_type_counts=Counter(row["suggested_response_type"] for row in output_rows),
    )


def _format_counts(counts: Counter) -> str:
    return ", ".join(f"{name}={count}" for name, count in sorted(counts.items())) or "none"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local CSV batch support preview.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = process_csv(args.input, args.output, args.limit)
    print("Batch Support Preview")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Processed rows: {result.processed_count}")
    print(f"Skipped empty rows: {result.skipped_count}")
    print(f"Needs human: {result.needs_human_count}")
    print(f"Category counts: {_format_counts(result.category_counts)}")
    print(f"Response type counts: {_format_counts(result.response_type_counts)}")


if __name__ == "__main__":
    main()
