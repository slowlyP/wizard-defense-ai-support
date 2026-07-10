import csv
import importlib
import tempfile
import unittest
from pathlib import Path

from backend.scripts.run_batch_support_preview import OUTPUT_COLUMNS, process_csv


class BatchSupportPreviewTests(unittest.TestCase):
    def _write_input(self, path, rows, fieldnames=("id", "text", "category")):
        with path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _read_output(self, path):
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            return list(csv.DictReader(file))

    def test_batch_script_module_can_be_imported(self):
        module = importlib.import_module("backend.scripts.run_batch_support_preview")
        self.assertTrue(callable(module.process_csv))

    def test_temporary_csv_is_processed_with_required_columns(self):
        rows = [
            {"id": "a", "text": "처음에는 마법사를 어디에 배치하나요?", "category": "gameplay_guide"},
            {"id": "b", "text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다.", "category": "bug_report"},
            {
                "id": "c",
                "text": "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다.",
                "category": "feedback_balance",
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.csv"
            output_path = Path(directory) / "output.csv"
            self._write_input(input_path, rows)

            result = process_csv(input_path, output_path)
            output_rows = self._read_output(output_path)

            self.assertTrue(output_path.exists())
            self.assertEqual(result.processed_count, len(rows))
            self.assertEqual(len(output_rows), len(rows))
            self.assertEqual(list(output_rows[0]), OUTPUT_COLUMNS)
            self.assertEqual(output_rows[0]["expected_category"], "gameplay_guide")

            by_category = {row["predicted_category"]: row for row in output_rows}
            self.assertEqual(by_category["bug_report"]["needs_human"], "true")
            self.assertEqual(by_category["feedback_balance"]["needs_human"], "true")

    def test_empty_and_whitespace_only_rows_are_skipped(self):
        rows = [
            {"id": "1", "text": "", "category": "gameplay_guide"},
            {"id": "2", "text": "   ", "category": "bug_report"},
            {"id": "3", "text": "다음 층은 언제 열리나요?", "category": "tower_progress"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.csv"
            output_path = Path(directory) / "output.csv"
            self._write_input(input_path, rows)

            result = process_csv(input_path, output_path)
            output_rows = self._read_output(output_path)

            self.assertEqual(result.processed_count, 1)
            self.assertEqual(result.skipped_count, 2)
            self.assertEqual(len(output_rows), 1)
            self.assertEqual(output_rows[0]["id"], "3")

    def test_missing_id_uses_sequential_ids_and_missing_label_stays_empty(self):
        rows = [{"text": "번개 스킬의 연쇄 대상을 알려주세요."}]
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.csv"
            output_path = Path(directory) / "output.csv"
            self._write_input(input_path, rows, fieldnames=("text",))

            process_csv(input_path, output_path)
            output_rows = self._read_output(output_path)

            self.assertEqual(output_rows[0]["id"], "1")
            self.assertEqual(output_rows[0]["expected_category"], "")


if __name__ == "__main__":
    unittest.main()
