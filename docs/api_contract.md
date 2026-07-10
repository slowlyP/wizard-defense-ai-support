# 로컬 API 계약 문서

## 1. 문서 목적

이 문서는 Wizard Defense AI Support의 local FastAPI prototype이 제공하는 request와 response 계약을 정의합니다. 문서의 기준 구현은 `backend/app/api.py`, `backend/app/api_schemas.py`, `backend/app/support_router.py`, `backend/app/response_templates.py`입니다.

## 2. API 개요

API는 상태 확인용 `GET /health`와 플레이어 문의 preview용 `POST /support/preview`를 제공합니다. 문의 preview는 기존 rule-based support router와 고정 response template을 순서대로 실행하며, 외부 서비스나 생성형 모델을 호출하지 않습니다.

## 3. API base URL

local 기본 주소는 다음과 같습니다.

```text
http://127.0.0.1:8000
```

## 4. `GET /health`

### 목적

local API process가 request에 응답할 수 있는지 간단히 확인합니다.

### Request

- Method: `GET`
- Path: `/health`
- Request body: 없음
- 필수 header: 없음

### Response schema

성공 시 HTTP 200과 JSON object를 반환합니다.

| Field | Type | 설명 |
| --- | --- | --- |
| `status` | `string` | 현재 구현에서는 `ok`를 반환합니다. |

### Example response

```json
{
  "status": "ok"
}
```

## 5. `POST /support/preview`

### 목적

한국어 플레이어 문의를 기존 support router로 분류하고, 라우팅 결과에 맞는 deterministic response draft와 internal note를 생성합니다.

### Request body schema

Content-Type은 `application/json`입니다.

| Field | Type | Required | 제약 | 설명 |
| --- | --- | --- | --- | --- |
| `text` | `string` | yes | 최소 1자이며 공백만으로 구성될 수 없음 | 분류하고 응답 초안을 만들 플레이어 문의입니다. |

### Response body schema

성공 시 HTTP 200과 다음 field를 포함한 JSON object를 반환합니다.

| Field | Type | 설명 |
| --- | --- | --- |
| `text` | `string` | 앞뒤 공백을 제거한 입력 문의입니다. |
| `predicted_category` | `string` | rule-based classifier가 선택한 category label입니다. |
| `urgency` | `string` | 라우팅 우선순위입니다. |
| `needs_human` | `boolean` | 사람 검토 필요 여부입니다. |
| `suggested_response_type` | `string` | response template 선택에 사용한 type입니다. |
| `routing_reason` | `string` | 해당 라우팅 결과를 선택한 이유입니다. |
| `response_draft` | `string` | 고정된 안전 template으로 생성한 한국어 응답 초안입니다. |
| `internal_note` | `string` | 자동 안내 여부 또는 사람 검토 사유를 담은 내부 참고입니다. |

### Example request

```json
{
  "text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다."
}
```

### Example response

```json
{
  "text": "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다.",
  "predicted_category": "bug_report",
  "urgency": "medium",
  "needs_human": true,
  "suggested_response_type": "bug_triage",
  "routing_reason": "실제 동작 실패나 손실 가능성이 있어 버그 재현 확인 절차로 라우팅합니다.",
  "response_draft": "제보해 주셔서 감사합니다. 이 내용은 실제 동작 오류나 진행 문제 가능성이 있어 검토가 필요한 문의로 확인됩니다. 확인을 위해 재현 순서, floor/stage, 마법사 조합, 오류 화면과 사용한 Windows/Steam demo build를 알려주세요. 화면 표시 문제라면 PC 해상도와 fullscreen/windowed 상태도 함께 남겨 주시면 검토에 도움이 됩니다. 이 문의는 담당 검토가 필요할 수 있으며, 확인 과정에서 추가 정보 요청이 있을 수 있습니다.",
  "internal_note": "사람 검토 필요: Windows/Steam demo 재현 정보 확인이 필요합니다. Router reason: 실제 동작 실패나 손실 가능성이 있어 버그 재현 확인 절차로 라우팅합니다."
}
```

### Empty text behavior

`text`가 빈 문자열이면 schema의 `min_length=1` 검증에 따라 HTTP 422를 반환합니다.

### Invalid input behavior

`text`가 공백만 포함하면 API가 앞뒤 공백을 제거한 뒤 HTTP 422와 `text must not be blank` detail을 반환합니다. 필수 field 누락, 잘못된 JSON type, 유효하지 않은 JSON body도 request validation 단계에서 HTTP 422로 처리됩니다.

## 6. Response field 설명

- `text`: 처리에 실제 사용한 정규화된 문의입니다. 현재 정규화는 앞뒤 공백 제거입니다.
- `predicted_category`: 문의의 주요 지원 category입니다.
- `urgency`: 자동 안내와 검토 우선순위를 나타내며 `low`, `medium`, `high` 중 하나입니다.
- `needs_human`: `true`이면 bug triage, balance review 또는 경계 사례 검토가 필요함을 뜻합니다.
- `suggested_response_type`: response draft 생성에 사용할 template type입니다.
- `routing_reason`: category, 오류 신호, balance 신호 등을 기준으로 작성된 라우팅 설명입니다.
- `response_draft`: 최종 고객 응답이 아닌 검토 가능한 한국어 초안입니다.
- `internal_note`: 자동 처리 가능 여부와 router 판단을 운영 검토용으로 요약합니다.

## 7. 허용된 category label

- `gameplay_guide`
- `wizard_acquisition`
- `wizard_growth`
- `tower_progress`
- `skill_combat`
- `bug_report`
- `feedback_balance`

## 8. 허용된 urgency 값

- `low`
- `medium`
- `high`

## 9. 허용된 suggested_response_type 값

- `guide_answer`
- `acquisition_answer`
- `growth_answer`
- `tower_progress_answer`
- `skill_combat_answer`
- `bug_triage`
- `balance_feedback_ack`

## 10. Error behavior

| 상황 | HTTP status | 현재 동작 |
| --- | --- | --- |
| `text`가 `""` | 422 | 최소 길이 validation error를 반환합니다. |
| `text`가 whitespace-only | 422 | `text must not be blank` detail을 반환합니다. |
| `text` field 누락 | 422 | required field validation error를 반환합니다. |
| `text`가 `number`, `boolean`, `object`, `array`, `null` 등 잘못된 type | 422 | string type validation error를 반환합니다. |
| JSON 형식 오류 | 422 | JSON decode 또는 request validation error를 반환합니다. |

Validation error의 세부 JSON 구조는 FastAPI와 Pydantic version에 따라 표현이 달라질 수 있으므로 client는 HTTP 422와 `detail` 존재 여부를 기준으로 처리하는 것이 안전합니다.

## 11. 안전 제한사항

- 환불을 약속하지 않습니다.
- 보상이나 재화 복구를 약속하지 않습니다.
- 문제 해결이나 fix를 보장하지 않습니다.
- patch date 또는 변경 적용 시점을 약속하지 않습니다.
- 외부 API를 호출하지 않습니다.
- LLM API를 호출하지 않습니다.
- 실제 helpdesk, Gmail, Slack, Discord와 연동하지 않습니다.

## 12. Portfolio 참고

이 API는 portfolio demonstration을 위한 local prototype입니다. 인증, 권한 관리, 영속 저장소, 운영 monitoring, rate limiting, 실제 고객 지원 정책 연동을 갖춘 production customer support system이 아닙니다.
