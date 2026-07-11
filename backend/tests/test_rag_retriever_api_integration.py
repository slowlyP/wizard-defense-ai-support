import unittest

from fastapi.testclient import TestClient

from backend.app.api import app


REQUIRED_FIELDS = {
    "text", "predicted_category", "urgency", "needs_human",
    "suggested_response_type", "routing_reason", "response_draft", "internal_note",
}


class RagRetrieverApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_existing_api_fields_remain_unchanged(self):
        response = self.client.post("/support/preview", json={"text": "What wizard types are available?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), REQUIRED_FIELDS)

    def test_internal_note_records_retrieval_context(self):
        response = self.client.post(
            "/support/preview",
            json={"text": "What wizard types are available?", "language": "en"},
        )
        self.assertIn("wizard_elements.en.v1", response.json()["internal_note"])

    def test_refund_stays_safe_and_requires_review(self):
        response = self.client.post(
            "/support/preview",
            json={"text": "I want a refund", "language": "en"},
        )
        result = response.json()
        self.assertTrue(result["needs_human"])
        self.assertIn("refund_request.en.v1", result["internal_note"])
        self.assertNotIn("we will refund", result["response_draft"].lower())


if __name__ == "__main__":
    unittest.main()

