import unittest

from fastapi.testclient import TestClient

from backend.app.api import app
from backend.app.llm_adapter import MockLLMAdapter
from backend.app.llm_guardrails import apply_llm_guardrails
from backend.app.llm_prompt_builder import build_mock_llm_prompt
from backend.app.rag_retriever import retrieve_support_chunks
from backend.app.support_router import route_inquiry


EXPECTED_API_FIELDS = {
    "text", "predicted_category", "urgency", "needs_human", "suggested_response_type",
    "routing_reason", "response_draft", "internal_note",
}


class MockLLMAdapterTests(unittest.TestCase):
    def build_draft(self, text, language):
        route = route_inquiry(text)
        chunks = retrieve_support_chunks(text, language)
        prompt = build_mock_llm_prompt(text, language, route, chunks)
        return MockLLMAdapter().generate_draft(prompt)

    def test_deterministic_korean_draft(self):
        first = self.build_draft("마법사의 종류가 뭐야?", "ko")
        second = self.build_draft("마법사의 종류가 뭐야?", "ko")
        self.assertEqual(first, second)
        self.assertIn("Fire", first)

    def test_deterministic_english_draft(self):
        first = self.build_draft("Who are the legendary wizards?", "en")
        second = self.build_draft("Who are the legendary wizards?", "en")
        self.assertEqual(first, second)
        self.assertIn("Arden", first)

    def test_sensitive_refund_uses_safe_human_review(self):
        draft = self.build_draft("I want a refund", "en")
        result = apply_llm_guardrails(draft, "en", sensitive=True)
        self.assertIn("human review", result.sanitized_draft)
        self.assertNotIn("we will refund", result.sanitized_draft.lower())

    def test_existing_api_contract_and_text_only_caller(self):
        result = TestClient(app).post("/support/preview", json={"text": "마법사의 종류가 뭐야?"})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(set(result.json()), EXPECTED_API_FIELDS)


if __name__ == "__main__":
    unittest.main()

