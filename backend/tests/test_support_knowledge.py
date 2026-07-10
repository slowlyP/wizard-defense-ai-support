import unittest

from backend.app.response_templates import generate_response_template
from backend.app.support_knowledge import build_knowledge_response, detect_support_knowledge


def make_route(text, needs_human=False, urgency="low"):
    return {
        "predicted_category": "gameplay_guide",
        "urgency": urgency,
        "needs_human": needs_human,
        "suggested_response_type": "guide_answer",
        "routing_reason": "test route",
        "inquiry_text": text,
    }


class SupportKnowledgeTests(unittest.TestCase):
    def assertDraftContains(self, text, expected_terms, language="ko"):
        result = generate_response_template(make_route(text), language=language)
        draft = result["response_draft"]
        for term in expected_terms:
            with self.subTest(text=text, term=term):
                self.assertIn(term, draft)
        return draft

    def test_korean_wizard_kind_question_mentions_basic_elements(self):
        self.assertDraftContains("留덈쾿?ъ쓽 醫낅쪟媛 萸먯빞?", ["Fire", "Water", "Wind", "Stone", "Lightning"])

    def test_korean_wizard_variation_question_returns_useful_type_response(self):
        self.assertDraftContains("留덈쾿?щ뒗 萸먮춴 ?덉뼱?", ["wizard", "element", "Fire"])

    def test_korean_element_question_returns_elements(self):
        self.assertDraftContains("?띿꽦? 萸먭? ?덉뼱?", ["Fire", "Water", "Lightning"])

    def test_korean_legendary_question_mentions_legendary_names(self):
        self.assertDraftContains("?꾩꽕 留덈쾿?щ뒗 ?꾧뎄 ?덉뼱?", ["Arden", "Orphel", "Lumiel", "Novarin"])

    def test_arden_mentions_fire_explosive_damage_dealer(self):
        self.assertDraftContains("?꾨Ⅴ?댁? ?대뼡 留덈쾿?ъ빞?", ["Arden", "Fire", "explosive", "damage dealer"])

    def test_lumiel_mentions_support_blessing_without_overpromising_healing(self):
        draft = self.assertDraftContains("猷⑤??섏? ?먮윭??", ["Lumiel", "support", "blessing"])
        for forbidden in ["guaranteed healing", "healing is guaranteed", "회복 보장"]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, draft)

    def test_fusion_question_returns_guidance(self):
        self.assertDraftContains("?듯빀? ?대뼸寃???", ["Fusion", "element", "wizard"])

    def test_fire_water_fusion_mentions_mist(self):
        self.assertDraftContains("遺덉씠??臾??⑹튂硫?萸먭? ??", ["Fire + Water", "mist"])

    def test_resonance_question_returns_growth_response(self):
        self.assertDraftContains("?덉“?뚯뒪??萸먯빞?", ["resonance", "성장"])

    def test_lost_resonance_material_uses_safe_review_tone(self):
        draft = self.assertDraftContains("?덉“?뚯뒪 ?щ즺媛 ?щ씪議뚯뼱", ["human review", "약속하지"])
        for forbidden in ["환불해 드립니다", "보상해 드립니다", "복구해 드립니다", "guaranteed"]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, draft)

    def test_pc_placement_mentions_mouse_drag(self):
        self.assertDraftContains("PC?먯꽌??留덈쾿?щ? ?대뼸寃?諛곗튂??", ["mouse", "drag", "placement"])

    def test_fullscreen_issue_returns_resolution_guidance(self):
        self.assertDraftContains("?꾩껜?붾㈃?먯꽌 UI媛 ?댁긽??", ["fullscreen", "해상도", "스크린샷"])

    def test_english_wizard_types(self):
        self.assertDraftContains("What wizard types are available?", ["Fire", "Water", "Wind", "Stone", "Lightning"], language="en")

    def test_english_legendary_wizards(self):
        self.assertDraftContains("What are legendary wizards?", ["Arden", "Orphel", "Lumiel", "Novarin"], language="en")

    def test_english_resonance(self):
        self.assertDraftContains("What is resonance?", ["Resonance", "growth", "enhancement"], language="en")

    def test_english_refund_safe_review_tone(self):
        draft = self.assertDraftContains("I want a refund", ["human review", "does not promise", "refund"], language="en")
        for forbidden in ["we will refund", "refund is guaranteed", "will be restored", "guaranteed fix"]:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, draft.lower())

    def test_detected_subtopic_is_deterministic(self):
        first = build_knowledge_response("What are legendary wizards?", "en")
        second = build_knowledge_response("What are legendary wizards?", "en")
        self.assertEqual(first, second)
        self.assertEqual(detect_support_knowledge("What are legendary wizards?").subtopic, "legendary_wizards")


if __name__ == "__main__":
    unittest.main()