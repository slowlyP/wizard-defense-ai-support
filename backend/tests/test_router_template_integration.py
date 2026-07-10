import unittest

from backend.app.response_templates import generate_response_template
from backend.app.support_router import route_inquiry


class RouterTemplateIntegrationTests(unittest.TestCase):
    def test_inquiry_routes_and_generates_template_output(self):
        route = route_inquiry("층 선택 버튼을 눌렀는데 다른 층으로 이동합니다.")
        template = generate_response_template(route)

        output = {
            "predicted_category": route["predicted_category"],
            "urgency": route["urgency"],
            "needs_human": route["needs_human"],
            "suggested_response_type": route["suggested_response_type"],
            "routing_reason": route["routing_reason"],
            "response_draft": template["response_draft"],
            "internal_note": template["internal_note"],
        }

        for key in [
            "predicted_category",
            "urgency",
            "needs_human",
            "suggested_response_type",
            "routing_reason",
            "response_draft",
            "internal_note",
        ]:
            with self.subTest(key=key):
                self.assertIn(key, output)

        self.assertEqual(output["predicted_category"], "bug_report")
        self.assertTrue(output["needs_human"])
        self.assertEqual(output["suggested_response_type"], "bug_triage")
        self.assertRegex(output["response_draft"], r"[가-힣]")

    def test_automatic_guide_flow_stays_automatic(self):
        route = route_inquiry("초반에 어떤 마법사를 먼저 배치하면 좋나요?")
        template = generate_response_template(route)

        self.assertEqual(route["suggested_response_type"], "guide_answer")
        self.assertFalse(route["needs_human"])
        self.assertIn("response_draft", template)
        self.assertIn("internal_note", template)
        self.assertRegex(template["response_draft"], r"PC|마우스")

    def test_bug_flow_requests_windows_or_steam_context(self):
        route = route_inquiry("게임이 전투 중 멈춰서 진행이 안 됩니다.")
        template = generate_response_template(route)

        self.assertEqual(route["predicted_category"], "bug_report")
        self.assertTrue(route["needs_human"])
        self.assertEqual(route["suggested_response_type"], "bug_triage")
        self.assertRegex(template["response_draft"], r"Windows|Steam demo|PC")

    def test_router_result_can_generate_english_without_changing_route(self):
        route = route_inquiry("게임이 전투 중 멈춰서 진행이 안 됩니다.")
        category_before = route["predicted_category"]
        urgency_before = route["urgency"]
        needs_human_before = route["needs_human"]

        template = generate_response_template(route, language="en")

        self.assertEqual(route["predicted_category"], category_before)
        self.assertEqual(route["urgency"], urgency_before)
        self.assertEqual(route["needs_human"], needs_human_before)
        self.assertNotRegex(template["response_draft"], r"[가-힣]")
        self.assertNotRegex(template["internal_note"], r"[가-힣]")


if __name__ == "__main__":
    unittest.main()
