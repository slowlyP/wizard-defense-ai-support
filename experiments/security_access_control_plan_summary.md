# Security Access Control Plan Summary

버전: v0.25.0-security-and-access-control-plan

## 1. 목적

이 문서는 EC2 production-style 배포를 더 production-ready한 방향으로 발전시키기 전에 필요한 보안, 접근 제어, 개인정보, logging 계획을 문서화한 작업을 요약한다.

## 2. 추가한 문서

- `docs/security_and_access_control_plan.md`
- `docs/privacy_and_logging_guidelines.md`
- `docs/production_security_checklist.md`

## 3. 보안 계획 요약

보안 계획 문서는 현재 적용된 구조와 아직 남은 보안 항목을 구분했다.

- Nginx port 80 public entry point
- FastAPI `127.0.0.1:8000` private bind
- public `5173`/`8000` closed
- SSH `22` limited to My IP
- HTTPS/domain/auth/database/ticket storage/Steamworks는 미구현 상태로 기록
- wildcard CORS를 열지 않고 same-origin proxy를 유지하는 방향 기록

## 4. 접근 제어 계획 요약

접근 제어는 public demo mode와 admin/internal mode로 나눠 검토하도록 정리했다.

- public demo mode: 포트폴리오 preview 범위만 공개
- admin/internal mode: IP allowlist, basic auth, application auth 등 future option 검토
- `/docs`와 `/openapi.json` 공개 범위 별도 결정
- `/support/preview` abuse prevention과 rate limiting 검토

## 5. 개인정보/로그 정책 요약

privacy/logging 문서는 다음 기준을 정리했다.

- 현재 서비스는 support preview only이며 database와 real ticket storage가 없다.
- 계정, 결제, 개인정보 입력을 금지하는 안내를 유지한다.
- request body 전체를 log로 남기지 않는 방향을 기본 정책으로 둔다.
- Nginx access/error log와 FastAPI journal 공유 시 masking을 전제로 한다.
- 실제 고객지원 시스템 전환 전 retention, deletion, access audit, privacy notice가 필요하다.

## 6. 검증 결과

이 작업에서 실행한 검증 계획은 다음과 같다.

- `python -m unittest discover backend/tests`
- `python backend/scripts/run_api_smoke_test.py`
- `python -m py_compile backend/app/api.py`
- `python -m py_compile backend/app/api_schemas.py`
- `python -m py_compile backend/app/response_templates.py`
- `npm install`
- `npm run build`
- `git diff --check`

검증 결과는 작업 완료 보고에 기록한다.

## 7. 변경하지 않은 항목

- API endpoint path
- API response field name
- support router behavior
- response template behavior
- dataset v1
- dataset v2
- previous experiment CSV files
- Unity game repository files
- HTTPS implementation
- authentication implementation
- database implementation
- external API 또는 LLM API 연동
- AWS credential, private key, 실제 public IP

## 8. 한계

이번 작업은 계획 문서화이며 구현이 아니다.

- HTTPS를 적용하지 않았다.
- authentication을 구현하지 않았다.
- authorization을 구현하지 않았다.
- rate limiting을 구현하지 않았다.
- database 또는 persistent storage를 추가하지 않았다.
- Steamworks 또는 real helpdesk integration을 추가하지 않았다.

## 9. 다음 작업 제안

- HTTPS와 domain 적용 절차 문서화
- `/docs`와 `/openapi.json` 공개 범위 결정
- rate limiting과 request size limit 구현 가능성 검토
- public demo mode와 internal review mode 분리
- 개인정보 안내와 logging masking 기준 점검