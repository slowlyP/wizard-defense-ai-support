# LLM/RAG 준비 계획 요약

## 1. 목적

`v0.27.0-llm-rag-readiness-plan`에서 현재 deterministic baseline을 미래 LLM/RAG 후보와 안전하게 비교·확장하기 위한 문서 기준을 마련했다.

## 2. 문제 배경

기존 도구는 넓어진 player question coverage와 안전 template를 제공하지만, 문서가 증가할수록 keyword/template 유지보수와 근거 제시가 어려워질 수 있다. 반대로 LLM을 바로 연결하면 환각, 과도한 약속, 개인정보, injection, 비용과 latency 기준이 없는 상태가 된다.

## 3. 현재 시스템 설명

현재 시스템은 LLM chatbot이 아니다. 외부 LLM API를 사용하지 않는 rule-based deterministic baseline이며, inquiry classifier + topic detection + response templates로 support response preview를 만든다. RAG와 generative AI 응답 생성도 구현되어 있지 않다.

## 4. 추가한 문서

- `docs/llm_rag_readiness_plan.md`
- `docs/rag_knowledge_base_design.md`
- `docs/prompt_and_guardrail_design.md`
- `docs/llm_rag_evaluation_plan.md`
- `docs/baseline_vs_llm_rag_comparison.md`
- `docs/support_knowledge_base_seed.md`
- 본 summary

## 5. Future LLM/RAG architecture 요약

User inquiry → deterministic classifier/topic detector → approved knowledge retrieval → optional LLM draft generator → guardrail filter → human review flag → response preview 흐름을 제안했다. 장애나 low confidence에는 현재 baseline으로 fallback한다.

## 6. RAG knowledge base 설계 요약

승인된 support topic, FAQ, game/demo guide, troubleshooting 및 safety/privacy policy만 후보로 삼는다. Topic, language, source type, safety level, human review metadata를 필수로 하고 secret, raw PII와 미검증 balance는 제외한다.

## 7. Prompt 및 guardrail 설계 요약

System/developer/user/retrieved context를 분리하고 retrieved text를 비신뢰 data로 취급한다. 환불·보상·복구·fix·patch date 약속을 금지하며 결제·계정·손실 사례는 human review로 전환한다.

## 8. 평가 계획 요약

Current rule-based, future retrieval-only, future LLM/RAG를 동일 dataset에서 category, coverage, usefulness, safety, hallucination, human review, bilingual consistency, latency와 cost로 비교한다. Safety violation false negative를 우선 관리한다.

## 9. Baseline vs LLM/RAG 비교 요약

Baseline은 재현성, 낮은 비용과 명시적 안전 통제가 강점이다. Future LLM/RAG는 지식 범위와 자연스러운 표현을 보강할 가능성이 있지만 환각과 운영 위험이 크다. Deterministic routing/safety + retrieval grounding + optional LLM drafting + human review의 hybrid 구성을 권장한다.

## 10. 변경하지 않은 항목

API endpoint와 field, backend/router/template/knowledge behavior, frontend, dataset v1/v2, 기존 experiment CSV, Unity repository를 변경하지 않았다. 외부 API/LLM, API key, dependency, authentication, database, Steamworks, payment/account/helpdesk integration을 추가하지 않았다.

## 11. 검증 결과

- `python -m unittest discover backend/tests`: 58 tests passed
- `python backend/scripts/run_api_smoke_test.py`: 7/7 preview cases passed (생성 CSV는 검증 후 기존 내용으로 복원)
- Python compile: `api.py`, `api_schemas.py`, `response_templates.py`, `support_knowledge.py` passed
- `npm install`: up to date, 새 dependency 없음
- `npm run build`: Vite production build passed
- `git diff --check`: passed
- 보호 대상 backend/frontend/dataset/기존 experiment CSV: content diff 없음
- Secret/IP scan: 추가 `.pem`, AWS access key pattern, private key block, 실제 public IPv4 literal 없음
- Unity repository: 이 작업 전후 모두 기존 `Assets/Scenes/MainBattleScene.unity` 수정 상태만 표시되며 이 작업에서 파일을 변경하지 않음

## 12. 한계

실제 retrieval, embedding, vector store, LLM adapter나 production control은 구현·평가하지 않았다. Seed 지식은 ingestion 전 source 승인과 최신성 검토가 필요하다.

## 13. 다음 작업 제안

승인 후 Phase 1 knowledge cleanup과 별도 versioned retrieval 평가셋을 먼저 수행한다. 그 결과를 baseline과 비교한 뒤에만 retrieval prototype 및 선택적 LLM adapter를 별도 작업으로 제안한다.
