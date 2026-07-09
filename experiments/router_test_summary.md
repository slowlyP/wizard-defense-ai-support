# Router Test Summary (v0.13.0-router-test-suite)

## 목적

이 문서는 support router와 response template prototype의 회귀 테스트 구성을 기록합니다. 목표는 라우팅 결과와 안전한 응답 초안 생성 규칙이 이후 변경에서도 일관되게 유지되는지 확인하는 것입니다.

## 테스트 대상

- Router module: `backend/app/support_router.py`
- Response template module: `backend/app/response_templates.py`
- Router tests: `backend/tests/test_support_router.py`
- Response template tests: `backend/tests/test_response_templates.py`
- Integration tests: `backend/tests/test_router_template_integration.py`
- Optional local runner: `backend/scripts/run_local_tests.py`

## 테스트 범위

- `bug_report` 문의가 `needs_human=true`와 `bug_triage`로 라우팅되는지 확인합니다.
- `feedback_balance` 문의가 `balance_feedback_ack`로 라우팅되는지 확인합니다.
- `gameplay_guide`, `wizard_acquisition`, `wizard_growth`, `skill_combat`, `tower_progress` 문의가 각각 기대한 `suggested_response_type`으로 라우팅되는지 확인합니다.
- 모든 `suggested_response_type`이 한국어 `response_draft`와 `internal_note`를 생성하는지 확인합니다.
- inquiry text -> support router -> response template generator 통합 흐름에서 필수 output field가 모두 존재하는지 확인합니다.

## 주요 테스트 케이스

- "레조넌스 시도했는데 재료만 사라지고 아무 일도 안 일어났어요." -> `bug_report`, `bug_triage`, `needs_human=true`
- "전설 마법사 등장 확률이 너무 낮아서 조정이 필요합니다." -> `feedback_balance`, `balance_feedback_ack`
- "처음 시작하면 마법사를 어디에 배치하는 게 가장 안전한가요?" -> `gameplay_guide`, `guide_answer`
- "전설 마법사는 어떤 방식으로 획득하나요?" -> `wizard_acquisition`, `acquisition_answer`
- "마법사 레벨업에 필요한 경험치는 어디서 얻나요?" -> `wizard_growth`, `growth_answer`
- "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요." -> `skill_combat`, `skill_combat_answer`
- "다음 층은 어떤 조건에서 열리나요?" -> `tower_progress`, `tower_progress_answer`

## 안전 응답 검증 기준

- `bug_triage` 응답은 환불, 보상, 복구, guaranteed fix를 약속하지 않아야 합니다.
- `balance_feedback_ack` 응답은 patch date, 확정 적용, guaranteed change를 약속하지 않아야 합니다.
- `needs_human=true`인 경우 응답 초안에는 검토, 추가 정보, 확인 중 하나에 해당하는 안내가 포함되어야 합니다.
- 테스트는 외부 API, LLM API, Unity game file, dataset CSV를 읽거나 수정하지 않습니다.

## 실행 방법

리포지토리 루트에서 다음 명령을 실행합니다.

```powershell
python -m unittest discover backend/tests
```

선택적으로 다음 wrapper script를 사용할 수 있습니다.

```powershell
python backend/scripts/run_local_tests.py
```

## 한계

- 현재 테스트는 고정된 대표 문장 기반 회귀 테스트이며, 전체 dataset v2를 재평가하지 않습니다.
- rule-based classifier의 세부 keyword coverage를 전부 검증하지 않습니다.
- response draft의 자연스러움이나 실제 운영 정책 적합성은 자동으로 판단하지 않습니다.

## 다음 작업 제안

- FastAPI 구현 전 router와 template generator의 request/response schema 테스트를 추가합니다.
- 안전 문구 금지어 목록을 별도 fixture로 분리해 유지보수성을 높입니다.
- 신규 dataset 또는 holdout sample이 생기면 smoke test 케이스를 추가합니다.
