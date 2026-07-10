# v0.26.0 Support Question Coverage Expansion 요약

## 1. 목적

Wizard Random Defense support preview가 더 많은 플레이어 질문에 deterministic rule-based 방식으로 구체적인 응답 초안을 제공하도록 question coverage를 확장했습니다.

## 2. 문제 배경

기존 `/support/preview`는 broad category 분류와 기본 response template에는 강했지만, 마법사 종류, 속성, 전설 마법사, fusion, resonance, PC 배치, 전체화면/해상도 같은 실제 플레이어 질문에는 답변이 다소 일반적으로 보일 수 있었습니다.

## 3. 현재 시스템 성격

현재 프로젝트는 외부 LLM API를 사용하지 않습니다. LLM chatbot 또는 generative AI chatbot이 아니라 rule-based inquiry classifier, topic detection, response template을 조합하는 deterministic support assistant입니다. 이번 버전은 향후 LLM/RAG 확장을 위한 baseline을 더 명확하게 만드는 작업입니다.

## 4. 추가 question coverage 범위

- wizard types / wizard elements
- legendary wizards
- Arden, Orphel, Lumiel, Novarin individual legendary wizard questions
- fusion guidance and Fire + Water mist-style example
- resonance and lost resonance material safe review
- tower floor and boss timing guidance
- PC mouse drag placement
- fullscreen/resolution/UI display troubleshooting
- reward loss, payment, refund safe human-review replies
- English equivalents for wizard, legendary, resonance, fusion, PC controls, refund questions

## 5. 추가 knowledge topic

- `wizard_elements`
- `legendary_wizards`
- `arden`
- `orphel`
- `lumiel`
- `novarin`
- `fusion`
- `fusion_examples`
- `resonance`
- `tower_floors`
- `boss_schedule`
- `pc_controls`
- `fullscreen_resolution`
- `bug_report_safe_reply`
- `reward_loss_safe_reply`
- `payment_refund_safe_reply`

## 6. 한국어/영어 응답 강화 내용

`language="ko"`는 한국어 support draft를, `language="en"`은 English support draft를 반환합니다. Response field name, endpoint path, invalid language behavior는 변경하지 않았습니다.

## 7. Example inquiry 확장 내용

React UI의 Korean/English example chips를 각각 6개로 확장했습니다. 예시는 wizard type, legendary wizard, resonance, fusion, PC placement, fullscreen/UI issue를 포함합니다.

## 8. 검증 결과

- 신규 support knowledge unit test 추가
- 신규 API integration test 추가
- `experiments/support_question_coverage_demo_outputs.csv` 20개 예시 생성
- 전체 backend unittest, smoke test, py_compile, frontend build로 검증합니다.

## 9. 변경하지 않은 항목

- 외부 API 호출 없음
- LLM API 호출 없음
- API key 추가 없음
- Steamworks, account, payment, refund, helpdesk integration 구현 없음
- authentication/database 구현 없음
- dataset v1/v2 변경 없음
- 기존 experiment CSV overwrite 없음
- Unity game repository 수정 없음
- API endpoint path와 response field name 변경 없음

## 10. 한계

이 버전은 deterministic baseline입니다. 실제 운영 고객지원, account recovery, payment/refund 처리, live game DB 조회, player inventory 확인, patch schedule 확정 기능은 포함하지 않습니다.

## 11. 다음 작업 제안

- LLM/RAG readiness plan
- knowledge document chunking
- prompt template design
- guardrail evaluation
- rule-based baseline vs LLM/RAG comparison