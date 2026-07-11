"""Generate a local mock-adapter comparison CSV without external calls."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.llm_adapter import MockLLMAdapter  # noqa: E402
from backend.app.llm_guardrails import apply_llm_guardrails  # noqa: E402
from backend.app.llm_prompt_builder import build_mock_llm_prompt  # noqa: E402
from backend.app.rag_retriever import retrieve_support_chunks  # noqa: E402
from backend.app.response_templates import generate_response_template  # noqa: E402
from backend.app.support_router import route_inquiry  # noqa: E402


OUTPUT_PATH = ROOT / "experiments" / "mock_llm_adapter_demo_outputs.csv"
EXAMPLES = (
    ("ko_wizard_types", "ko", "마법사의 종류가 뭐야?"),
    ("ko_legendary", "ko", "전설 마법사는 누구 있어?"),
    ("ko_fusion", "ko", "Fusion은 어떻게 해?"),
    ("ko_resonance", "ko", "레조넌스가 뭐야?"),
    ("ko_pc", "ko", "PC에서 마법사를 어떻게 배치해?"),
    ("ko_refund", "ko", "환불받고 싶어"),
    ("ko_payment", "ko", "결제했는데 아이템을 못 받았어"),
    ("en_wizard_types", "en", "What wizard types are available?"),
    ("en_legendary", "en", "Who are the legendary wizards?"),
    ("en_fusion", "en", "How does fusion work?"),
    ("en_resonance", "en", "What is resonance?"),
    ("en_pc", "en", "How do I place wizards on PC?"),
    ("en_refund", "en", "I want a refund."),
    ("en_payment", "en", "I paid but did not receive the item."),
)
FIELDS = (
    "id", "language", "text", "route_category", "needs_human", "retrieved_chunk_ids",
    "template_response_draft", "mock_llm_draft", "guardrail_is_safe", "guardrail_violations",
    "final_safe_draft",
)


def build_demo_rows() -> list[dict[str, object]]:
    adapter = MockLLMAdapter()
    rows: list[dict[str, object]] = []
    for example_id, language, text in EXAMPLES:
        route = route_inquiry(text)
        results = retrieve_support_chunks(text, language, top_k=3)
        sensitive = any(result.chunk.requires_human_review for result in results)
        if sensitive:
            route["needs_human"] = True
        template = generate_response_template({**route, "inquiry_text": text}, language)
        prompt = build_mock_llm_prompt(text, language, route, results)
        mock_draft = adapter.generate_draft(prompt)
        guardrail = apply_llm_guardrails(mock_draft, language, sensitive=sensitive)
        rows.append({
            "id": example_id,
            "language": language,
            "text": text,
            "route_category": route["predicted_category"],
            "needs_human": str(route["needs_human"]).lower(),
            "retrieved_chunk_ids": "|".join(result.chunk.id for result in results),
            "template_response_draft": template["response_draft"],
            "mock_llm_draft": mock_draft,
            "guardrail_is_safe": str(guardrail.is_safe).lower(),
            "guardrail_violations": "|".join(guardrail.violations),
            "final_safe_draft": guardrail.sanitized_draft,
        })
    return rows


def main() -> None:
    rows = build_demo_rows()
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} local mock adapter examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

