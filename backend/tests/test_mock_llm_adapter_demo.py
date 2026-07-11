import unittest

from backend.scripts.run_mock_llm_adapter_demo import EXAMPLES, build_demo_rows


class MockLLMAdapterDemoTests(unittest.TestCase):
    def test_demo_rows_cover_all_examples_and_are_deterministic(self):
        first = build_demo_rows()
        second = build_demo_rows()
        self.assertEqual(first, second)
        self.assertEqual(len(first), len(EXAMPLES))

    def test_sensitive_demo_rows_are_safe(self):
        rows = build_demo_rows()
        sensitive = [row for row in rows if row["id"].endswith(("refund", "payment"))]
        self.assertEqual(len(sensitive), 4)
        for row in sensitive:
            self.assertEqual(row["needs_human"], "true")
            self.assertIn("review" if row["language"] == "en" else "검토", row["final_safe_draft"])


if __name__ == "__main__":
    unittest.main()

