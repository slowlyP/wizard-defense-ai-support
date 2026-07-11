# RAG Retrieval Baseline Prototype 요약

## 1. 목적

`v0.28.0-rag-retrieval-baseline-prototype`은 향후 RAG/LLM 비교에 사용할 작은 bilingual local retrieval baseline을 구현한다. 검색 단계 자체의 relevance, ordering과 safety routing을 생성 모델 없이 검증하는 것이 목적이다.

## 2. 문제 배경

기존 support knowledge는 topic별 deterministic response에 강하지만, RAG 계획을 실제로 평가하려면 structured chunk를 독립적으로 검색하는 기준이 필요했다. Embedding이나 LLM을 먼저 도입하면 검색 오류와 생성 오류를 분리하기 어렵기 때문에 단순하고 설명 가능한 local scoring부터 구현했다.

## 3. 현재 시스템 설명

현재 시스템은 LLM chatbot이 아니다. Rule-based classifier + topic detection + response templates에 deterministic retrieval baseline을 더한 support preview tool이다. 외부 LLM API, embedding, vector DB와 generative response generation을 사용하지 않는다.

## 4. 추가한 retrieval 구조

`rag_knowledge_base.py`는 immutable bilingual chunk를 보관한다. `rag_retriever.py`는 입력을 정규화한 뒤 phrase keyword, title/topic/content token을 정수 점수로 계산한다. 점수 내림차순, 요청 언어 우선, chunk ID 오름차순으로 정렬해 같은 입력에 항상 같은 결과를 반환한다. Positive score가 없는 unrelated query는 빈 결과를 반환한다.

## 5. Knowledge chunk metadata 설계

각 chunk는 `id`, `topic`, `language`, `source_type`, `safety_level`, `requires_human_review`, `title`, `content`를 포함한다. Retrieval용 `keywords`도 함께 두되 demo CSV에는 player/support 검토에 필요한 metadata와 score를 기록한다. Sensitive safety chunk에는 refund, compensation, restoration, guaranteed fix와 patch date를 약속하지 않는 내용만 넣었다.

## 6. Korean/English retrieval examples

- “마법사의 종류가 뭐야?” → `wizard_elements.ko.v1`
- “전설 마법사는 누구 있어?” → `legendary_wizards.ko.v1`
- “아르덴은 어떤 마법사야?” → `arden.ko.v1`
- “레조넌스가 뭐야?” → `resonance.ko.v1`
- “환불받고 싶어” → `refund_request.ko.v1`, human review
- “What wizard types are available?” → `wizard_elements.en.v1`
- “How does fusion work?” → `fusion.en.v1`
- “I paid but did not receive the item.” → `payment_issue.en.v1`, human review

전체 17개 bilingual example의 최대 3개 ranked 결과는 `rag_retrieval_baseline_demo_outputs.csv`에 저장했다.

## 7. `/support/preview` 연동 여부

기존 endpoint와 8개 response field는 유지한다. Player-facing `response_draft`는 기존 deterministic support knowledge/template가 계속 담당한다. Retrieval 결과의 chunk ID와 safety review 표시는 `internal_note`에 추가한다. Retrieved chunk가 `requires_human_review=true`이면 기존 router 결과를 낮추지 않고 `needs_human=true`로만 강화한다. `language`를 생략한 `{"text": "..."}` 요청은 계속 한국어 기본값으로 동작한다.

## 8. 검증 결과

- Focused retrieval/API integration unittest: 14 tests passed
- 전체 backend unittest: 72 tests passed
- API smoke: 7/7 passed, historical output CSV는 실행 직후 원래 byte로 복원
- 요청된 Python module compile: passed
- `npm install`: up to date, 새 dependency 없음
- `npm run build`: Vite production build passed
- `git diff --check`: passed
- Protected dataset/이전 experiment CSV와 Unity repository: 이 작업으로 인한 변경 없음
- Secret/IP scan: 추가 `.pem`, AWS key pattern, private key block, 실제 public IPv4 없음
- Demo: 17 examples 생성 성공
- Deterministic ordering, `top_k`, unrelated query empty result, bilingual wizard/legendary/refund 검색을 자동 검증한다.

## 9. 변경하지 않은 항목

API response field name과 endpoint path, `api_schemas.py`, `support_router.py`, dataset v1/v2, 이전 experiment CSV와 frontend UI는 변경하지 않았다. Unity repository도 read-only reference로만 확인했다. 외부 API/LLM, authentication, database, Steamworks, account/payment/helpdesk integration을 구현하지 않았다.

## 10. 한계

Substring/token scoring은 한국어 형태 변화, 오타, 동의어와 긴 복합 문의에 제한이 있다. In-code chunk는 작은 baseline에 적합하지만 문서 갱신과 규모 확장에는 별도 ingestion/versioning 설계가 필요하다. Retrieval score는 확률이나 사실 보증이 아니며 player-facing answer generation 품질을 측정하지 않는다.

## 11. 다음 작업 제안

- Optional LLM adapter는 별도 승인 후 retrieval context만 사용하는 비활성 기본 구성으로 검토
- Versioned retrieval evaluation set과 relevance metric 추가
- Prompt grounding 및 citation 일치 평가
- Prompt injection, over-promise와 PII guardrail 평가
- 현재 deterministic search와 future vector search의 offline 비교
