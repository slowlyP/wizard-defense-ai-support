import unittest

from backend.app.response_templates import generate_response_template


ALL_RESPONSE_TYPES = [
    "guide_answer",
    "acquisition_answer",
    "growth_answer",
    "tower_progress_answer",
    "skill_combat_answer",
    "bug_triage",
    "balance_feedback_ack",
]


def make_route(response_type, needs_human=False, urgency="low"):
    return {
        "predicted_category": "bug_report" if response_type == "bug_triage" else "gameplay_guide",
        "urgency": urgency,
        "needs_human": needs_human,
        "suggested_response_type": response_type,
        "routing_reason": "테스트용 라우팅 사유입니다.",
    }


class ResponseTemplateTests(unittest.TestCase):
    def test_every_response_type_returns_korean_draft(self):
        for response_type in ALL_RESPONSE_TYPES:
            with self.subTest(response_type=response_type):
                result = generate_response_template(make_route(response_type))
                self.assertTrue(result["response_draft"])
                self.assertTrue(result["internal_note"])
                self.assertRegex(result["response_draft"], r"[가-힣]")

    def test_bug_triage_does_not_promise_compensation_or_guaranteed_fixes(self):
        result = generate_response_template(make_route("bug_triage", needs_human=True, urgency="high"))
        draft = result["response_draft"]
        forbidden_terms = ["환불해", "보상해", "복구해", "반드시 해결", "보장", "guaranteed fix"]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, draft)

    def test_balance_feedback_does_not_promise_patch_dates_or_changes(self):
        result = generate_response_template(
            make_route("balance_feedback_ack", needs_human=True, urgency="medium")
        )
        draft = result["response_draft"]
        forbidden_terms = ["패치 날짜", "적용 날짜", "반드시 조정", "확정 적용", "guaranteed"]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, draft)

    def test_needs_human_true_includes_review_or_additional_info_wording(self):
        for response_type in ["bug_triage", "balance_feedback_ack", "skill_combat_answer"]:
            with self.subTest(response_type=response_type):
                result = generate_response_template(
                    make_route(response_type, needs_human=True, urgency="medium")
                )
                self.assertRegex(result["response_draft"], r"검토|추가 정보|확인")
                self.assertIn("Router reason:", result["internal_note"])


if __name__ == "__main__":
    unittest.main()
