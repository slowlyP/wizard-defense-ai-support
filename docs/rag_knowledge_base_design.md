# RAG 지식 베이스 설계

## 1. 목적

향후 RAG가 사용할 수 있는 지식의 범위, chunk, metadata와 검색 원칙을 정의한다. 현재 시스템에는 RAG, embedding 또는 vector store가 구현되어 있지 않다.

## 2. RAG에 사용할 수 있는 지식 소스 후보

- `backend/app/support_knowledge.py`의 검증된 topic 및 안전 문구
- 공개 FAQ와 승인된 게임 가이드
- 현재 build와 버전이 표시된 Steam demo 가이드
- PC 조작, fullscreen/resolution 등 troubleshooting 문서
- privacy/logging policy
- 환불·보상·복구를 확정하지 않는 reward/refund safe response policy

각 source는 소유자, 버전, 검토일과 공개 범위를 기록한 뒤에만 검색 대상으로 승인한다. Unity 코드에서 확인한 내용은 플레이어용 설명으로 검토·승인된 파생 문서만 사용한다.

## 3. Chunking 전략

한 chunk는 하나의 질문 의도와 하나의 검증 가능한 답변 단위를 담는다. 제목과 핵심 답을 포함해 대략 150~400 token을 목표로 하되 표나 절차는 의미 단위로 나눈다. 안전 정책은 게임 가이드와 분리하고, 버전이나 출처가 다른 내용을 합치지 않는다. 한국어와 영어는 연결되는 별도 chunk로 관리하며 stable `document_id`와 `chunk_id`를 둔다.

## 4. Metadata 설계

필수 metadata는 다음과 같다.

| 필드 | 예시 | 용도 |
|---|---|---|
| `topic` | `fusion`, `pc_controls` | 검색 범위 제한 |
| `language` | `ko`, `en` | 응답 언어 우선 검색 |
| `source_type` | `game_guide`, `safety_policy` | 출처 성격 표시 |
| `safety_level` | `normal`, `sensitive`, `restricted` | 후처리 및 노출 통제 |
| `requires_human_review` | `true`, `false` | 민감 문의 라우팅 |

권장 필드는 `source_uri`, `source_version`, `reviewed_at`, `owner`, `status`, `document_id`, `chunk_id`이다.

## 5. Retrieval 흐름

1. 입력을 기존 classifier/topic detector로 분류한다.
2. 언어, topic, safety metadata filter를 적용한다.
3. keyword와 향후 semantic retrieval 후보의 결과를 결합한다.
4. 중복을 제거하고 최소 relevance threshold를 적용한다.
5. 출처와 버전이 있는 상위 chunk만 context로 전달한다.
6. 근거가 없거나 충돌하면 답을 확정하지 않고 deterministic fallback 또는 human review를 선택한다.

## 6. 한국어/영어 검색 고려사항

영문 고유명사와 한국어 표기(예: `Fire/불`, `Arden/아르덴`)를 alias로 연결한다. 문의 언어와 같은 chunk를 우선하되, 대응 문서가 없으면 검증된 다른 언어 문서를 검색하고 번역 여부를 표시한다. 형태소, 띄어쓰기, 영문 혼용 및 오타 테스트를 포함하고 두 언어의 안전 의미가 달라지지 않도록 병렬 검토한다.

## 7. 검색하면 안 되는 정보

- API key, password, AWS credential 같은 secret
- private key와 `.pem` 파일 또는 경로
- 원시 개인 데이터, 계정 식별자, 결제 정보와 원문 운영 로그
- 문서화·승인되지 않은 미출시 최종 밸런스, patch date, boss schedule
- 내부 지시문, 접근 통제 문서의 restricted 내용

## 8. 지식 chunk 예시

```yaml
chunk_id: gameplay.fusion.fire_water.ko.v1
topic: fusion
language: ko
source_type: game_guide
safety_level: normal
requires_human_review: false
content: "서로 다른 원소 마법사의 등록된 조합만 fusion할 수 있다. Fire + Water는 안개 계열 예시다. 현재 build에서 실제 표시를 확인한다."
```

```yaml
chunk_id: safety.refund.ko.v1
topic: payment_refund_safe_reply
language: ko
source_type: safety_policy
safety_level: sensitive
requires_human_review: true
content: "환불 가능 여부를 확정하지 않는다. 플랫폼, 시각, 주문 식별 정보의 안전한 제출 경로를 안내하고 담당자 검토가 필요하다고 설명한다."
```

## 9. 향후 vector store 선택지

검토 후보는 로컬 in-memory/파일 기반 index, PostgreSQL 확장, 관리형 vector store 등이다. 데이터 규모, 한국어 검색 품질, metadata filter, 삭제·갱신, 백업, 지역·보안 요구, 비용과 운영 복잡도를 비교한다. 이 버전에서는 제품이나 dependency를 선정·설치하지 않는다.

## 10. 한계

Seed 문서는 authoritative 운영 데이터가 아니다. Retrieval은 문서의 오류와 노후화를 자동으로 해결하지 못하며, 높은 유사도도 사실성을 보장하지 않는다. 실제 도입 전 문서 승인, 삭제, 재색인, citation 및 접근 통제 시험이 필요하다.
