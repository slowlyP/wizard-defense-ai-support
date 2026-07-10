import csv
import importlib
import tempfile
import unittest
from pathlib import Path

from backend.scripts.analyze_batch_support_preview import (
    CATEGORY_SUMMARY_COLUMNS,
    MISMATCH_COLUMNS,
    analyze_csv,
)


class BatchSupportAnalysisTests(unittest.TestCase):
    def _write_input(self, path):
        fieldnames = [
            "id",
            "text",
            "expected_category",
            "predicted_category",
            "urgency",
            "needs_human",
            "suggested_response_type",
            "routing_reason",
        ]
        rows = [
            {
                "id": "1",
                "text": "초반 배치를 알려주세요.",
                "expected_category": "gameplay_guide",
                "predicted_category": "gameplay_guide",
                "urgency": "low",
                "needs_human": "false",
                "suggested_response_type": "guide_answer",
                "routing_reason": "guide",
            },
            {
                "id": "2",
                "text": "배치 버튼이 작동하지 않아요.",
                "expected_category": "gameplay_guide",
                "predicted_category": "bug_report",
                "urgency": "medium",
                "needs_human": "true",
                "suggested_response_type": "bug_triage",
                "routing_reason": "bug",
            },
            {
                "id": "3",
                "text": "게임이 멈췄어요.",
                "expected_category": "bug_report",
                "predicted_category": "bug_report",
                "urgency": "high",
                "needs_human": "true",
                "suggested_response_type": "bug_triage",
                "routing_reason": "bug",
            },
            {
                "id": "4",
                "text": "확률이 너무 낮아요.",
                "expected_category": "feedback_balance",
                "predicted_category": "wizard_acquisition",
                "urgency": "medium",
                "needs_human": "true",
                "suggested_response_type": "acquisition_answer",
                "routing_reason": "acquisition",
            },
        ]
        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _read_csv(self, path):
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))

    def test_analysis_script_module_can_be_imported(self):
        module = importlib.import_module("backend.scripts.analyze_batch_support_preview")
        self.assertTrue(callable(module.analyze_csv))

    def test_temporary_preview_is_analyzed_with_correct_metrics_and_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "input.csv"
            report_path = root / "report.md"
            category_path = root / "category.csv"
            mismatch_path = root / "mismatch.csv"
            self._write_input(input_path)

            result = analyze_csv(input_path, report_path, category_path, mismatch_path, mismatch_limit=1)
            category_rows = self._read_csv(category_path)
            mismatch_rows = self._read_csv(mismatch_path)

            self.assertTrue(report_path.exists())
            self.assertTrue(category_path.exists())
            self.assertTrue(mismatch_path.exists())
            self.assertEqual(result.total_rows, 4)
            self.assertEqual(result.match_count, 2)
            self.assertEqual(result.mismatch_count, 2)
            self.assertAlmostEqual(result.accuracy, 0.5)
            self.assertEqual(result.needs_human_counts["true"], 3)
            self.assertEqual(result.needs_human_counts["false"], 1)
            self.assertEqual(list(category_rows[0]), CATEGORY_SUMMARY_COLUMNS)
            self.assertEqual(list(mismatch_rows[0]), MISMATCH_COLUMNS)
            self.assertEqual(len(mismatch_rows), 1)

            gameplay = next(
                row for row in category_rows if row["expected_category"] == "gameplay_guide"
            )
            self.assertEqual(gameplay["total"], "2")
            self.assertEqual(gameplay["correct"], "1")
            self.assertEqual(gameplay["mismatch"], "1")
            self.assertEqual(gameplay["accuracy"], "0.5000")

    def test_zero_mismatch_limit_writes_header_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "input.csv"
            report_path = root / "report.md"
            category_path = root / "category.csv"
            mismatch_path = root / "mismatch.csv"
            self._write_input(input_path)

            result = analyze_csv(input_path, report_path, category_path, mismatch_path, mismatch_limit=0)

            self.assertEqual(result.mismatch_count, 2)
            self.assertEqual(self._read_csv(mismatch_path), [])


if __name__ == "__main__":
    unittest.main()
