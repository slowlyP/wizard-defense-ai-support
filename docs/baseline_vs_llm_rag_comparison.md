# Deterministic Baseline과 Future LLM/RAG 비교

## 1. 목적

현재 구현된 규칙 기반 지원 미리보기와 미래 LLM/RAG 후보의 역할, 장점과 위험을 구분하고 권장 hybrid 구조를 설명한다.

## 2. 현재 deterministic baseline의 강점

동일 입력에 재현 가능한 결과를 제공하고 동작 이유를 추적하기 쉽다. 외부 모델 비용이나 network dependency가 없고 금지 약속 및 human review 규칙을 코드와 template로 고정할 수 있다. 기존 API 계약과 한국어/영어 preview가 이미 회귀 테스트된다.

## 3. 현재 deterministic baseline의 한계

표현 변화와 긴 맥락에 취약하고 등록된 topic 밖에서는 일반적인 답이 될 수 있다. 문서가 늘면 keyword와 template 유지보수가 복잡해지며, 근거 citation과 자연스러운 multi-turn 설명은 제한적이다.

## 4. Future LLM/RAG의 강점

승인된 문서를 검색해 더 넓은 질문 표현을 다루고, 근거를 바탕으로 자연스러운 한국어/영어 초안을 만들 가능성이 있다. 문서 단위 갱신과 citation을 설계하면 template만으로 다루기 어려운 설명을 보강할 수 있다.

## 5. Future LLM/RAG의 위험

환각, prompt injection, 근거 오인용, 개인정보 누출, 민감 문의 과도한 약속, 비용·latency·provider 장애가 발생할 수 있다. 문서가 오래되거나 검색이 실패하면 자연스럽지만 틀린 답을 만들 위험도 있다.

## 6. 비교표

| 항목 | Current deterministic baseline | Future retrieval-only | Future LLM/RAG |
|---|---|---|---|
| 현재 구현 | 구현됨 | 미구현 | 미구현 |
| 재현성 | 높음 | 높음 | 설정에 따라 변동 |
| 자연스러운 표현 | 제한적 | template 수준 | 높아질 가능성 |
| 근거 범위 | 등록 rule/topic | 검색 문서 | 검색 문서 + 생성 |
| 환각 위험 | 낮음 | 낮음~중간 | 중간~높음 |
| 비용/latency | 낮음 | index에 따라 증가 | API/model에 따라 증가 |
| 안전 통제 | 명시적 rule | filter + rule | 다층 guardrail 필요 |
| 장애 fallback | 자체 동작 | baseline | retrieval/baseline 필요 |

## 7. 두 방식이 모두 유용한 이유

Baseline은 안전 정책과 측정 가능한 하한을 제공한다. Retrieval/LLM은 표현과 지식 범위를 넓힐 후보이다. LLM이 항상 baseline을 대체하는 것이 아니라, 신뢰 가능한 경우에만 초안 품질을 보강하고 실패 시 baseline으로 돌아가는 구조가 운영상 유용하다.

## 8. 권장 hybrid architecture

- Deterministic routing and safety guardrails로 category, topic, 민감도와 금지 약속을 통제한다.
- Retrieval로 승인된 grounded context를 제공한다.
- LLM은 선택적으로 자연스러운 draft generation만 담당한다.
- 결제, 환불, 보상, 복구, 개인정보와 낮은 confidence 사례는 human review로 보낸다.

## 9. Portfolio 설명 문구

> Wizard Defense AI Support는 현재 외부 LLM API를 사용하지 않는 rule-based AI support preview tool입니다. 규칙 기반 분류, topic detection, response template로 재현 가능한 deterministic baseline을 구축했으며, v0.27.0에서는 이 baseline을 향후 retrieval-only 및 선택적 LLM/RAG 후보와 안전하게 비교하기 위한 지식 베이스, prompt/guardrail, 평가 계획을 문서화했습니다.

“현재 LLM/RAG chatbot을 구현했다”거나 “generative AI가 자동 처리한다”는 표현은 사용하지 않는다.

## 10. 한계

비교는 계획 수준이며 future 후보의 성능을 입증하지 않는다. 실제 모델, provider, vector store와 운영 비용은 선정되지 않았다. Human review도 실제 계정·결제 처리 권한이나 helpdesk 연동을 뜻하지 않는다.
