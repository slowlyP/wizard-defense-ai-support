import unittest

from backend.app.rag_retriever import retrieve_support_chunks


class RagRetrieverTests(unittest.TestCase):
    def assertTopTopic(self, text, topic, language="ko"):
        results = retrieve_support_chunks(text, language)
        self.assertTrue(results)
        self.assertEqual(results[0].chunk.topic, topic)
        return results

    def test_korean_wizard_types(self):
        self.assertTopTopic("마법사의 종류가 뭐야?", "wizard_elements")

    def test_korean_legendary_wizards(self):
        self.assertTopTopic("전설 마법사는 누구 있어?", "legendary_wizards")

    def test_korean_arden(self):
        self.assertTopTopic("아르덴은 어떤 마법사야?", "arden")

    def test_korean_resonance(self):
        self.assertTopTopic("레조넌스가 뭐야?", "resonance")

    def test_korean_refund_requires_human_review(self):
        results = self.assertTopTopic("환불받고 싶어", "refund_request")
        self.assertTrue(results[0].chunk.requires_human_review)

    def test_english_wizard_types(self):
        self.assertTopTopic("What wizard types are available?", "wizard_elements", "en")

    def test_english_legendary_wizards(self):
        self.assertTopTopic("Who are the legendary wizards?", "legendary_wizards", "en")

    def test_english_refund_requires_human_review(self):
        results = self.assertTopTopic("I want a refund.", "refund_request", "en")
        self.assertTrue(results[0].chunk.requires_human_review)

    def test_top_k_limit(self):
        self.assertEqual(len(retrieve_support_chunks("wizard legendary fire", "en", top_k=2)), 2)

    def test_ordering_is_deterministic(self):
        first = retrieve_support_chunks("How does fusion work?", "en")
        second = retrieve_support_chunks("How does fusion work?", "en")
        self.assertEqual(first, second)

    def test_unrelated_query_returns_empty_without_crashing(self):
        self.assertEqual(retrieve_support_chunks("quasar nebula sandwich", "en"), [])


if __name__ == "__main__":
    unittest.main()

