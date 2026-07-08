# Labeling Guide (레이블링 가이드)

목표: 게임 내 플레이어 문의를 일관되게 레이블링하기 위한 기준을 제공합니다.

Label taxonomy (예시):
- `bug_report` — 게임 내부 버그 및 크래시 보고.
- `gameplay_question` — 게임 메커니즘, 빌드, 레벨 관련 질문.
- `account_issue` — 계정, 결제, 접속 문제.
- `other` — 위 항목들에 해당하지 않는 일반 문의.

Annotation instructions:
1. Read the full user message and map to a single primary label.
2. If message contains both bug and gameplay question, prefer `bug_report`.
3. For ambiguous cases, mark `other` and flag for review.

Quality checks:
- Ensure >= 90% inter-annotator agreement on a 200-sample subset.
- Keep examples and edge-cases in `data/processed/README.md`.
