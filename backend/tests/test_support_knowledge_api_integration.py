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


class SupportKnowledgeApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def post_preview(self, text, language="ko"):
        response = self.client.post("/support/preview", json={"text": text, "language": language})
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_existing_response_fields_remain_unchanged(self):
        result = self.post_preview("What wizard types are available?", "en")
        self.assertEqual(set(result), REQUIRED_FIELDS)

    def test_english_wizard_types_api_response(self):
        result = self.post_preview("What wizard types are available?", "en")
        self.assertIn("Fire", result["response_draft"])
        self.assertIn("Lightning", result["response_draft"])

    def test_english_legendary_wizards_api_response(self):
        result = self.post_preview("What are legendary wizards?", "en")
        self.assertRegex(result["response_draft"], r"Arden|Orphel|Lumiel|Novarin")

    def test_english_resonance_api_response(self):
        result = self.post_preview("What is resonance?", "en")
        self.assertIn("Resonance", result["response_draft"])

    def test_english_refund_safe_api_response(self):
        result = self.post_preview("I want a refund", "en")
        draft = result["response_draft"].lower()
        self.assertIn("human review", draft)
        self.assertNotIn("we will refund", draft)
        self.assertNotIn("refund is guaranteed", draft)

    def test_invalid_language_behavior_remains_validation_error(self):
        response = self.client.post("/support/preview", json={"text": "What is resonance?", "language": "jp"})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()