"""Write a new deterministic retrieval demo without touching older outputs."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.rag_retriever import retrieve_support_chunks


OUTPUT_PATH = ROOT / "experiments" / "rag_retrieval_baseline_demo_outputs.csv"
EXAMPLES = (
    ("ko_wizard_types", "ko", "마법사의 종류가 뭐야?"),
    ("ko_legendary", "ko", "전설 마법사는 누구 있어?"),
    ("ko_arden", "ko", "아르덴은 어떤 마법사야?"),
    ("ko_fusion", "ko", "불이랑 물을 합치면 뭐가 돼?"),
    ("ko_resonance", "ko", "레조넌스가 뭐야?"),
    ("ko_pc", "ko", "PC에서 마법사를 어떻게 배치해?"),
    ("ko_fullscreen", "ko", "전체화면에서 UI가 이상해"),
    ("ko_reward", "ko", "보상을 못 받았어"),
    ("ko_refund", "ko", "환불받고 싶어"),
    ("ko_payment", "ko", "결제했는데 아이템이 안 들어왔어"),
    ("en_wizard_types", "en", "What wizard types are available?"),
    ("en_legendary", "en", "Who are the legendary wizards?"),
    ("en_resonance", "en", "What is resonance?"),
    ("en_fusion", "en", "How does fusion work?"),
    ("en_pc", "en", "How do I place wizards on PC?"),
    ("en_refund", "en", "I want a refund."),
    ("en_payment", "en", "I paid but did not receive the item."),
)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=("id", "language", "text", "rank", "chunk_id", "topic", "score", "safety_level", "requires_human_review", "title", "content"))
        writer.writeheader()
        for example_id, language, text in EXAMPLES:
            for rank, result in enumerate(retrieve_support_chunks(text, language, top_k=3), start=1):
                writer.writerow({
                    "id": example_id, "language": language, "text": text, "rank": rank,
                    "chunk_id": result.chunk.id, "topic": result.chunk.topic, "score": result.score,
                    "safety_level": result.chunk.safety_level,
                    "requires_human_review": str(result.chunk.requires_human_review).lower(),
                    "title": result.chunk.title, "content": result.chunk.content,
                })
    print(f"Saved {len(EXAMPLES)} retrieval examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
