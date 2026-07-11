# Optional Mock LLM Adapter 설계

## 1. 목적

`v0.29.0-optional-llm-adapter-prototype`은 retrieval 이후 draft generator와 guardrail을 연결하는 future LLM architecture를 외부 호출 없이 검증한다. 구현된 adapter는 실제 LLM이 아니라 로컬 deterministic mock이다.

## 2. 현재 시스템의 위치

현재 support preview는 rule-based deterministic baseline과 local deterministic retrieval baseline으로 동작한다. `/support/preview`는 기존 classifier, topic detection, response template 및 retrieval safety metadata를 사용한다. 외부 LLM API는 사용하지 않으며 실제 LLM chatbot이나 generative AI service가 아니다.

## 3. Optional mock LLM adapter를 먼저 만드는 이유

실제 provider를 연결하기 전에 route, retrieved context, prompt boundary, adapter interface, output guardrail과 fallback 책임을 분리할 수 있다. 고정 입력에서 재현 가능한 결과를 만들기 때문에 이후 provider 후보가 architecture와 safety contract를 지키는지 비교할 기준이 된다. API key, network failure와 비용 없이 guardrail test를 반복할 수도 있다.

## 4. Proposed architecture

```text
inquiry
  -> router
  -> topic detector
  -> retriever
  -> prompt builder
  -> MockLLMAdapter (demo-only, local deterministic)
  -> guardrail filter
  -> response preview comparison artifact
```

Production/default `/support/preview` 경로는 mock adapter를 호출하지 않는다. 별도 demo script가 template draft, retrieval context, mock draft와 final safe draft를 비교한다.

## 5. Adapter interface 설계

`LLMAdapter` protocol은 `name`과 `generate_draft(prompt)` 경계를 정의한다. `MockLLMAdapter`만 구현되어 있으며 첫 번째 verified context를 고정 문구로 조합한다. Context가 없으면 deterministic template fallback을 안내하고, sensitive prompt면 human review 문구를 반환한다. Network client, SDK 또는 provider configuration은 없다.

## 6. Prompt builder 설계

`build_mock_llm_prompt`는 user inquiry, language, route category, human review 상태, retrieved chunk ID/title/content를 stable order로 조합한다. 한국어/영어 constraint를 분리하고 context 밖 사실과 금지 약속을 만들지 않도록 명시한다. AWS access-key-looking pattern, private-key block, email, account/order/card identifier는 `[REDACTED]`로 바꾼다. 생성된 prompt는 로컬 object와 demo에만 사용되며 외부로 전송되지 않는다.

## 7. Guardrail filter 설계

`apply_llm_guardrails`는 refund, compensation, restoration, guaranteed fix와 patch date 약속 pattern을 분류한다. 위반이 있으면 `violations`를 남기고 고정 safe fallback으로 교체한다. Reward/payment/refund/account/recovery처럼 `requires_human_review`인 retrieval은 draft가 안전해 보여도 human-review fallback을 강제한다. 결과는 `is_safe`, `violations`, `sanitized_draft`로 반환한다.

## 8. Mock mode와 future real provider mode

| 항목 | 현재 mock mode | Future real provider mode |
|---|---|---|
| 실행 위치 | Local demo script | 별도 승인 후 adapter 뒤 |
| 생성 방식 | 고정 규칙과 retrieved context | Provider model candidate |
| Network/API key | 없음 | 저장소 밖 secret 주입 필요 |
| 비용/latency | 사실상 고정 | 측정 및 제한 필요 |
| 실패 fallback | Deterministic template | 동일 fallback 의무 |
| 현재 구현 여부 | 구현됨 | 미구현 |

## 9. No-secret / no-external-call 정책

API key, provider credential, AWS credential, private key, `.pem` 경로·내용, account ID, 실제 EC2 public IP와 raw private data를 prompt, code, CSV 또는 log에 넣지 않는다. 예시 주소가 필요하면 `EC2_PUBLIC_IP`만 사용한다. 현재 adapter에는 HTTP client와 외부 endpoint가 전혀 없다.

## 10. 한계

Mock output은 자연어 모델 품질, hallucination, token limit, provider latency나 cost를 재현하지 않는다. Regex guardrail은 표현 변형과 문맥 부정을 완전히 이해하지 못한다. Redaction은 최소 baseline이며 실제 PII detection이나 compliance control을 대신하지 않는다. Demo-only 통과는 production provider 승인이 아니다.

## 11. 다음 단계

- Optional real provider adapter: 별도 승인과 threat review 후에만 검토
- Environment variable key handling: 실제 key를 저장소 밖에서 주입하고 출력 마스킹
- Cost/latency monitoring: request budget, timeout, p50/p95 및 token 관측
- Provider failure fallback: timeout/error/circuit breaker 시 deterministic template 복귀
- Guardrail evaluation: multilingual adversarial set과 false-positive/false-negative 측정

