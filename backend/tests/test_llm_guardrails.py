import unittest

from backend.app.llm_guardrails import apply_llm_guardrails


class LLMGuardrailTests(unittest.TestCase):
    def assertViolation(self, draft, violation, language="ko"):
        result = apply_llm_guardrails(draft, language)
        self.assertFalse(result.is_safe)
        self.assertIn(violation, result.violations)
        self.assertNotEqual(result.sanitized_draft, draft)

    def test_refund_promise(self):
        self.assertViolation("환불해 드리겠습니다.", "refund_promise")

    def test_compensation_promise(self):
        self.assertViolation("보상을 지급해 드립니다.", "compensation_promise")

    def test_restoration_promise(self):
        self.assertViolation("진행을 복구해 드립니다.", "restoration_promise")

    def test_guaranteed_fix(self):
        self.assertViolation("We provide a guaranteed fix.", "guaranteed_fix", "en")

    def test_patch_date_promise(self):
        self.assertViolation("The patch date is confirmed.", "patch_date_promise", "en")

    def test_sensitive_draft_forces_human_review_wording(self):
        result = apply_llm_guardrails("Thank you for the inquiry.", "en", sensitive=True)
        self.assertTrue(result.is_safe)
        self.assertIn("human review", result.sanitized_draft)
        self.assertIn("No refund", result.sanitized_draft)


if __name__ == "__main__":
    unittest.main()

