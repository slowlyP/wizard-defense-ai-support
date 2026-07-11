import unittest

from backend.app.llm_prompt_builder import build_mock_llm_prompt
from backend.app.rag_retriever import retrieve_support_chunks
from backend.app.support_router import route_inquiry


class LLMPromptBuilderTests(unittest.TestCase):
    def test_prompt_includes_retrieved_chunk_ids_and_titles(self):
        text = "What wizard types are available?"
        prompt = build_mock_llm_prompt(text, "en", route_inquiry(text), retrieve_support_chunks(text, "en"))
        self.assertIn("wizard_elements.en.v1", prompt.prompt_text)
        self.assertIn("Wizard elements", prompt.prompt_text)

    def test_prompt_redacts_secrets_private_keys_and_email(self):
        private_key = "-----BEGIN PRIVATE KEY----- secret material -----END PRIVATE KEY-----"
        text = f"AKIA1234567890ABCDEF {private_key} player@example.com"
        prompt = build_mock_llm_prompt(text, "en", route_inquiry(text), [])
        for forbidden in ["AKIA1234567890ABCDEF", "secret material", "player@example.com"]:
            self.assertNotIn(forbidden, prompt.prompt_text)
        self.assertIn("[REDACTED]", prompt.prompt_text)


if __name__ == "__main__":
    unittest.main()

