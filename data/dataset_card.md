# Dataset Card

Short description:
Small support dataset for "Random Wizard Defense" combining player tickets, FAQs, and crafted examples for classification and retrieval.

언어: 영어 (primary), 일부 한글 예시 포함 가능

Purpose: Training and evaluating intent classification and retrieval grounding for support responses.

Composition:
- `raw/` contains original text dumps and transcripts.
- `processed/` contains cleaned, split, and labeled examples used for model training.

Recommended splits:
- Train: 80%
- Dev: 10%
- Test: 10%

Privacy & Safety:
- Ensure no real player PII is included. Use synthetic or anonymized tickets.
