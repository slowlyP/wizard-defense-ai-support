import unittest

from backend.app.support_router import route_inquiry


class SupportRouterTests(unittest.TestCase):
    def assert_route(self, text, expected_category, expected_response_type):
        route = route_inquiry(text)
        self.assertEqual(route["predicted_category"], expected_category)
        self.assertEqual(route["suggested_response_type"], expected_response_type)
        self.assertIn(route["urgency"], {"low", "medium", "high"})
        self.assertIsInstance(route["needs_human"], bool)
        self.assertTrue(route["routing_reason"])
        return route

    def test_bug_report_sets_needs_human_true(self):
        route = self.assert_route(
            "레조넌스 시도했는데 재료만 사라지고 아무 일도 안 일어났어요.",
            "bug_report",
            "bug_triage",
        )
        self.assertTrue(route["needs_human"])

    def test_feedback_balance_routes_to_ack(self):
        route = self.assert_route(
            "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다.",
            "feedback_balance",
            "balance_feedback_ack",
        )
        self.assertTrue(route["needs_human"])
        self.assertEqual(route["urgency"], "medium")

    def test_guide_question_routes_to_guide_answer(self):
        self.assert_route(
            "처음 시작하면 마법사를 어디에 배치하는 게 가장 안전한가요?",
            "gameplay_guide",
            "guide_answer",
        )

    def test_acquisition_question_routes_to_acquisition_answer(self):
        self.assert_route(
            "전설 마법사는 어떤 방식으로 획득하나요?",
            "wizard_acquisition",
            "acquisition_answer",
        )

    def test_growth_question_routes_to_growth_answer(self):
        self.assert_route(
            "마법사 레벨업에 필요한 경험치는 어디서 얻나요?",
            "wizard_growth",
            "growth_answer",
        )

    def test_skill_question_routes_to_skill_combat_answer(self):
        self.assert_route(
            "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요.",
            "skill_combat",
            "skill_combat_answer",
        )

    def test_tower_progress_question_routes_to_tower_progress_answer(self):
        self.assert_route(
            "다음 층은 어떤 조건에서 열리나요?",
            "tower_progress",
            "tower_progress_answer",
        )


if __name__ == "__main__":
    unittest.main()
