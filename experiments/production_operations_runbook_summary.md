# Production Operations Runbook Summary

버전: v0.24.0-production-operations-runbook

## 1. 목적

이 문서는 EC2 production-style 배포가 검증된 이후 운영자가 서비스를 상태 확인, 업데이트, 재시작, rollback, 장애 대응할 수 있도록 운영 runbook을 추가한 작업을 요약한다.

## 2. 추가한 문서

- `docs/production_operations_runbook.md`
- `docs/deployment_update_and_rollback.md`
- `docs/incident_troubleshooting_checklist.md`

## 3. 운영 절차 요약

운영 runbook은 다음 항목을 정리했다.

- Nginx port 80 상태 확인
- FastAPI systemd service 상태 확인
- `/health`와 `/support/preview` smoke 확인
- React production build 재배포
- Nginx reload 전 syntax test
- FastAPI journal과 Nginx access/error log 확인
- EC2 stop/start 이후 확인 항목
- 비용 관리와 disk/log 사용량 확인

## 4. 업데이트/롤백 절차 요약

배포 업데이트 문서는 다음 흐름을 정리했다.

- 현재 tag와 service 상태 확인
- `git fetch --tags` 후 새 tag checkout
- backend unittest, API smoke test, py_compile 실행
- frontend `npm install`과 production build 실행
- `frontend/dist`를 `/var/www/wizard-defense-support`로 복사
- FastAPI service restart와 Nginx reload
- 문제 발생 시 이전 정상 tag로 rollback

## 5. 장애 대응 절차 요약

장애 checklist는 다음 상황을 빠르게 분기하도록 구성했다.

- 브라우저 화면이 열리지 않음
- 분석 버튼 실패
- `/health` 실패
- `/docs` 실패
- 502 Bad Gateway
- CORS error
- systemd service failed
- Nginx config failure
- frontend build가 localhost를 바라보는 경우
- port 80 blocked
- SSH 접속 실패
- 디스크 용량 부족

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
- external API 또는 LLM API 연동
- AWS credential, private key, 실제 public IP

## 8. 한계

이번 작업은 운영 문서화이며 다음 기능을 구현하지 않았다.

- HTTPS
- domain
- auth
- database
- persistent support ticket storage
- Steamworks integration
- centralized monitoring
- automated deployment pipeline

## 9. 다음 작업 제안

- HTTPS와 domain 연결 절차 문서화
- `/docs` 공개 범위 제한 검토
- 운영 로그 rotation과 monitoring 절차 추가
- 배포 checklist 자동화 또는 GitHub Actions 검토
- 인증 또는 제한된 access control 도입 검토