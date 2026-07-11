# Optional Mock LLM Adapter Prototype 요약

## 1. 목적

Retrieval 이후 optional draft adapter와 guardrail을 연결하는 architecture를 외부 LLM/API 없이 재현 가능한 local demo로 검증했다.

## 2. 문제 배경

v0.28.0 retrieval baseline은 relevant chunk와 safety metadata를 제공하지만 future generation boundary는 구현되지 않았다. 실제 provider를 바로 연결하면 prompt 구성, secret 처리, unsafe output과 fallback 문제를 provider behavior와 분리하기 어렵다. 먼저 deterministic mock을 두어 interface와 검증 기준을 고정했다.

## 3. 현재 구현 설명

현재 구현은 실제 LLM API가 아니다. `MockLLMAdapter`라는 이름의 local deterministic formatter이며 network, model SDK, API key를 사용하지 않는다. Default `/support/preview`는 기존 template flow를 그대로 사용하고 mock adapter는 demo/test에서만 명시적으로 호출된다.

## 4. 추가한 모듈

- `backend/app/llm_adapter.py`: provider-neutral protocol과 `MockLLMAdapter`
- `backend/app/llm_prompt_builder.py`: bilingual prompt-like structure와 redaction
- `backend/app/llm_guardrails.py`: forbidden promise 검사와 safe fallback
- `backend/scripts/run_mock_llm_adapter_demo.py`: template/retrieval/mock/guardrail 비교 CSV 생성
- 관련 prompt, guardrail, adapter, demo tests

## 5. Prompt builder 요약

Inquiry, language, route category, `needs_human`, ranked chunk ID/title/content를 stable text로 조합한다. Private-key block, AWS access-key-looking string, email과 account/order/card identifier를 `[REDACTED]`로 치환한다. Prompt는 로컬 mock input이며 외부로 전송되지 않는다.

## 6. Guardrail 요약

Refund, compensation, restoration, guaranteed fix 및 patch date promise를 concept별 violation으로 기록한다. 위반 또는 sensitive metadata가 있으면 fixed human-review fallback을 반환한다. Payment/refund demo는 자동 처리나 해결을 약속하지 않으며 필요한 상황·시각·build·screenshot만 승인된 절차로 요청한다.

## 7. Demo output 요약

`experiments/mock_llm_adapter_demo_outputs.csv`에는 한국어 7개, 영어 7개 총 14개 example이 있다. Wizard types, legendary, fusion, resonance, PC controls, refund와 payment를 포함한다. 각 row는 route, retrieved chunk IDs, template draft, mock draft, guardrail result와 final safe draft를 비교한다. 최종 demo generation에서 14개 mock draft 모두 guardrail violation이 없었고 sensitive 4개 row는 `needs_human=true`와 human-review final draft를 유지했다.

## 8. 검증 결과

- Focused prompt/guardrail/mock/demo tests: 14 tests passed
- Demo script: 14 rows 생성 성공
- 전체 backend unittest: 86 tests passed
- API smoke: 7/7 passed, historical CSV는 실행 직후 원래 byte로 복원
- 요청된 Python module compile: passed
- `npm install`: up to date, 새 dependency 없음
- `npm run build`: Vite production build passed
- `git diff --check`: passed
- Dataset/기존 CSV/package/requirements와 Unity repository: 이 작업으로 인한 변경 없음
- Secret/IP scan: 추가 `.pem`, AWS/provider key pattern, private key block, 실제 public IPv4 없음

## 9. 변경하지 않은 항목

`/support/preview` implementation과 request/response schema, endpoint path, frontend, dataset v1/v2, 기존 experiment CSV, requirements/package files와 Unity repository를 변경하지 않았다. 외부 LLM/RAG/vector/embedding dependency, authentication, database, Steamworks, account/payment/helpdesk integration을 추가하지 않았다.

## 10. 한계

Mock adapter는 실제 model의 언어 품질, hallucination, prompt injection, latency, cost 또는 provider outage를 모사하지 않는다. Regex guardrail과 baseline redaction은 완전한 safety/compliance control이 아니다. Demo는 architecture proof이지 external LLM integration이 아니다.

## 11. 다음 작업 제안

- Versioned retrieval/prompt grounding evaluation
- Multilingual guardrail adversarial set과 false-positive/false-negative 분석
- 별도 승인 시 provider failure fallback, cost/latency budget 및 저장소 밖 key handling 설계
