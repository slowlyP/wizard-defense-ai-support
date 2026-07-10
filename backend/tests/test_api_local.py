import unittest

from fastapi.testclient import TestClient

from backend.app.api import app


REQUIRED_FIELDS = {
    "text",
    "predicted_category",
    "urgency",
    "needs_human",
    "suggested_response_type",
    "routing_reason",
    "response_draft",
    "internal_note",
}


class LocalApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_returns_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_support_preview_returns_all_required_fields(self):
        response = self.client.post(
            "/support/preview",
            json={"text": "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요."},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), REQUIRED_FIELDS)

    def test_empty_or_blank_text_is_rejected(self):
        for text in ["", "   "]:
            with self.subTest(text=repr(text)):
                response = self.client.post("/support/preview", json={"text": text})
                self.assertEqual(response.status_code, 422)

    def test_bug_preview_requires_human_review(self):
        response = self.client.post(
            "/support/preview",
            json={"text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다."},
        )
        result = response.json()
        self.assertEqual(result["predicted_category"], "bug_report")
        self.assertTrue(result["needs_human"])
        self.assertEqual(result["suggested_response_type"], "bug_triage")

    def test_balance_preview_requires_human_review(self):
        response = self.client.post(
            "/support/preview",
            json={"text": "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다."},
        )
        result = response.json()
        self.assertEqual(result["predicted_category"], "feedback_balance")
        self.assertTrue(result["needs_human"])
        self.assertEqual(result["suggested_response_type"], "balance_feedback_ack")


if __name__ == "__main__":
    unittest.main()
