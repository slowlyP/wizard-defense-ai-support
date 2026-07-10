# FastAPI Local Prototype Summary (v0.14.0-fastapi-local-prototype)

## 목적

기존 support router와 response template generator를 작은 local FastAPI app으로 연결해 문의 입력부터 라우팅, 안전한 응답 초안 생성까지 한 번에 확인할 수 있도록 구성했습니다.

## API 구성

- `GET /health`: local app 상태를 `{"status": "ok"}`로 반환합니다.
- `POST /support/preview`: `text`를 입력받아 router field와 response template field를 함께 반환합니다.
- 입력의 앞뒤 공백은 제거하며, 빈 문자열과 공백만 있는 문자열은 HTTP 422로 거부합니다.
- 기존 `backend/app/support_router.py`와 `backend/app/response_templates.py`를 그대로 사용하므로 결과는 deterministic합니다.

## Smoke test 범위

`backend/scripts/run_api_smoke_test.py`는 network port를 열지 않고 FastAPI in-process client를 사용합니다. 다음 7개 category의 한국어 대표 사례를 각각 확인합니다.

- `gameplay_guide`
- `wizard_acquisition`
- `wizard_growth`
- `tower_progress`
- `skill_combat`
- `bug_report`
- `feedback_balance`

결과는 `experiments/api_local_smoke_test_outputs.csv`에 저장합니다. CSV에는 입력 text, category, urgency, human review 여부, response type, routing reason, response draft, internal note가 포함됩니다.

## 안전성과 제한사항

- 외부 API와 LLM API를 호출하지 않습니다.
- Gmail, Slack, Discord, 외부 helpdesk와 연결하지 않습니다.
- API key나 실제 운영 credential을 사용하지 않습니다.
- `bug_report`와 `feedback_balance`의 human review 정책은 기존 support router 결과를 그대로 따릅니다.
- response draft는 portfolio용 local 초안이며 실제 고객 지원 결정이 아닙니다.

## 실행 방법

```powershell
python -m uvicorn backend.app.api:app --reload
python backend/scripts/run_api_smoke_test.py
python -m unittest discover backend/tests
```
