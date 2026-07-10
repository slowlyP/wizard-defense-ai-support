# LLM/RAG 준비 계획

## 1. 목적

현재 Wizard Random Defense 고객지원 미리보기 도구를 유지하면서, 향후 근거 기반 LLM/RAG 흐름으로 확장하기 위한 경계, 단계, 위험과 검증 기준을 정의한다. 이 문서는 `v0.27.0-llm-rag-readiness-plan`의 계획 문서이며 실제 LLM 연동 구현서가 아니다.

## 2. 현재 시스템의 위치

현재 구현은 rule-based deterministic support assistant이다. 규칙 기반 문의 분류기, topic detector, 응답 템플릿으로 같은 입력에 재현 가능한 초안을 만든다. 외부 LLM API를 사용하지 않으며 RAG도 구현하지 않았다. 따라서 현재 제품은 LLM 챗봇이나 RAG 챗봇이 아니라, future LLM/RAG baseline으로 사용할 수 있는 규칙 기반 AI support preview tool이다.

## 3. 왜 바로 LLM을 붙이지 않고 baseline을 먼저 만드는가

결정론적 baseline은 분류 정확도, 안전 문구, human review 전환, 지연 시간과 실패 사례를 고정된 기준으로 남긴다. 이 기준이 있어야 retrieval-only 및 LLM/RAG 후보가 실제로 유용성은 높이고 안전성은 유지했는지 비교할 수 있다. 또한 지식 출처와 금지 약속을 먼저 정리하면 환각과 운영 위험을 줄일 수 있다.

## 4. 향후 LLM/RAG 목표

- 검증된 문서에서 관련 근거를 검색하고 답변에 사용한다.
- 한국어/영어 문의에 자연스럽고 일관된 초안을 만든다.
- 환불, 결제, 보상, 복구 등 민감 문의를 자동 확정하지 않고 human review로 보낸다.
- 검색 근거가 부족하거나 모델을 사용할 수 없으면 deterministic fallback을 제공한다.
- baseline 대비 품질, 안전성, latency와 cost를 측정한다.

## 5. 제안 아키텍처

```text
user inquiry
  -> rule-based classifier
  -> topic detector
  -> knowledge retrieval
  -> LLM draft generator (선택적 future component)
  -> guardrail filter
  -> human review flag
  -> response preview
```

분류기와 topic detector는 검색 범위를 좁히고 안전 우선순위를 결정한다. Knowledge retrieval은 승인된 chunk만 제공한다. 선택적 LLM adapter는 근거 안에서 초안을 만들며, guardrail filter가 금지 약속과 개인정보 노출을 검사한다. 민감하거나 근거가 약한 결과는 human review flag를 유지한 채 preview로만 표시한다.

## 6. 현재 baseline과 향후 영역의 분리

현재 구현 영역은 문의 분류, topic detection, response template, `needs_human`, 한국어/영어 deterministic draft, 기존 `/health` 및 `/support/preview` 계약이다. 향후 영역은 문서 ingestion, retrieval index, embedding/vector store, LLM adapter, prompt 실행, citation, 모델 비용 관리이다. 향후 영역은 이 버전에서 설치·호출·구현하지 않는다.

## 7. 향후 구현 단계

1. Phase 1: knowledge base cleanup — 출처, 소유자, 언어, 안전 등급, 최신성 및 승인 상태를 정리한다.
2. Phase 2: retrieval prototype — 외부 LLM 없이 고정 평가셋으로 검색 품질과 근거 표시를 검증한다.
3. Phase 3: optional LLM adapter — 승인 후 provider-neutral adapter와 비활성 기본 설정을 설계한다.
4. Phase 4: guardrail evaluation — injection, 환각, 과도한 약속, 개인정보 누출과 fallback을 평가한다.
5. Phase 5: EC2 deployment hardening for LLM mode — secret manager, egress 제한, timeout, rate limit, cost/latency 관측과 장애 격리를 검증한다.

## 8. 위험

- Hallucination: 검색 문서에 없는 게임 규칙이나 상태를 만들어 낼 수 있다.
- Refund/compensation over-promise: 환불·보상·복구를 권한 없이 확정할 수 있다.
- Personal data leakage: 문의나 로그의 개인정보가 prompt 또는 출력에 남을 수 있다.
- Prompt injection: 사용자가 시스템 규칙 무시나 비공개 정보 출력을 유도할 수 있다.
- API cost: 비정상 반복 요청과 긴 context가 비용을 증가시킬 수 있다.
- Latency: retrieval 및 모델 호출로 preview 응답이 느려질 수 있다.

## 9. Guardrail 전략

입력 길이와 형식을 제한하고 개인정보를 최소화한다. 검색 대상은 승인된 출처 allowlist로 제한하며 retrieved text를 지시가 아닌 참고 데이터로 취급한다. 출력은 금지 약속, 근거 없는 수치·일정, secret/PII 패턴을 검사한다. 결제, 환불, 계정, 보상, 아이템 손실은 항상 human review 후보로 유지한다. 근거 부족, 검사 실패, timeout 또는 adapter 장애 시 현재 deterministic response로 fallback한다.

## 10. No-secret 정책

API key, AWS credential, private key, `.pem` 경로·내용, AWS account ID, 실제 EC2 public IP를 코드·문서·prompt·로그·지식 베이스에 저장하지 않는다. 예시 주소는 `EC2_PUBLIC_IP`만 사용한다. 향후 secret은 저장소 밖의 승인된 secret 관리 수단으로 주입하고 로그에서 마스킹한다.

## 11. 한계

이 계획은 모델, provider, vector store를 선정하지 않는다. 실제 계정·결제·Steamworks·helpdesk 데이터에 접근하지 않으며, 현재 게임 build의 미문서화 밸런스나 운영 정책을 보장하지 않는다. 문서화만으로 production 안전성을 증명할 수 없다.

## 12. 다음 단계

Phase 1 승인 후 seed 문서를 출처별 작은 chunk로 분리하고, 문서 소유자와 갱신 절차를 정한다. 이어서 LLM을 사용하지 않는 retrieval prototype과 offline 평가셋을 먼저 만들고, 결과가 baseline보다 나은 경우에만 선택적 LLM adapter 검토를 제안한다.
