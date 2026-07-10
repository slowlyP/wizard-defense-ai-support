# Production Deployment Verification

버전: v0.23.0-production-deployment-verification
대상: React + FastAPI 고객지원 미리보기 도구의 EC2 production-style 배포 검증

## 1. 목적

이 문서는 v0.22.0에서 정리한 Nginx, systemd, React production build 기반 배포 hardening 절차를 실제 EC2 환경에 적용한 뒤 검증한 결과를 기록한다.

실제 public IP, AWS 계정 ID, `.pem` 경로, private key, AWS credential은 문서에 기록하지 않는다. 재사용 가능한 문서에서는 항상 `EC2_PUBLIC_IP` placeholder를 사용한다.

## 2. 검증 배경

이전 개발 검증에서는 React Vite dev server가 `5173` 포트에서 실행되고 FastAPI가 `8000` 포트에서 실행되어 browser 기준 cross-origin 요청이 발생했다. 이 구조에서는 `/support/preview` 호출 시 CORS preflight 문제가 생길 수 있었다.

v0.22.0에서는 production-style 구조로 다음 방향을 문서화했다.

- Nginx가 port 80에서 React production build를 제공한다.
- FastAPI는 public port가 아니라 EC2 내부 `127.0.0.1:8000`에서 systemd service로 실행한다.
- Nginx가 `/support/preview`, `/health`, `/docs`, `/openapi.json`을 FastAPI로 reverse proxy한다.
- React frontend는 production build에서 same-origin 상대 경로로 API를 호출한다.

v0.23.0에서는 사용자가 이 구조를 실제 EC2에 적용한 뒤 확인한 결과를 문서화한다.

## 3. 적용된 production-style 구조

검증된 구조는 다음과 같다.

- Public browser entry: `http://EC2_PUBLIC_IP`
- Static frontend serving: Nginx port 80
- React build output: `frontend/dist`를 Nginx static web root로 복사
- FastAPI runtime: systemd service
- FastAPI bind address: `127.0.0.1:8000`
- Reverse proxy: Nginx가 public HTTP 요청을 내부 FastAPI로 전달
- Direct public dev ports: `5173`, `8000` inbound rule 제거

## 4. 최종 접속 구조

브라우저와 외부 검증자는 다음 구조로 접근한다.

```text
http://EC2_PUBLIC_IP
http://EC2_PUBLIC_IP/support/preview
http://EC2_PUBLIC_IP/health
http://EC2_PUBLIC_IP/docs
```

`/support/preview`는 browser에서 직접 URL로 여는 페이지가 아니라 React UI가 inquiry 제출 시 호출하는 API path다. `/health`와 `/docs`는 Nginx reverse proxy를 통해 FastAPI 응답을 확인하는 검증 path로 사용했다.

## 5. Nginx 역할

Nginx는 production-style 배포에서 public entry point 역할을 한다.

- port 80에서 React production build를 serving한다.
- `/support/preview` 요청을 `127.0.0.1:8000/support/preview`로 proxy한다.
- `/health` 요청을 `127.0.0.1:8000/health`로 proxy한다.
- `/docs` 요청을 `127.0.0.1:8000/docs`로 proxy한다.
- `/openapi.json` 요청을 `127.0.0.1:8000/openapi.json`으로 proxy한다.
- browser가 보는 origin을 port 80 하나로 통일해 CORS preflight 문제를 피한다.

검증 결과 Nginx service는 active/running 상태였고, `nginx -t`는 syntax ok 및 test successful 결과를 반환했다.

## 6. systemd FastAPI 역할

systemd는 FastAPI backend를 장기 실행 service로 관리한다.

- FastAPI service는 active/running 상태로 확인되었다.
- FastAPI는 `127.0.0.1:8000`에 bind되어 public network에 직접 노출되지 않았다.
- Nginx reverse proxy만 FastAPI에 접근하는 구조로 검증되었다.

이 구조에서는 SSH terminal을 닫아도 backend process가 종료되지 않으며, service restart/status/log 확인을 systemd 명령으로 수행할 수 있다.

## 7. React production build 역할

React frontend는 Vite production build 결과물을 Nginx static root에서 제공한다.

검증된 역할은 다음과 같다.

- Vite dev server 없이 `http://EC2_PUBLIC_IP`에서 React UI가 열렸다.
- `:5173` 포트 없이 browser 접근이 가능했다.
- frontend inquiry submission은 same-origin `/support/preview` 요청으로 동작했다.
- Korean / English language toggle이 browser에서 동작했다.
- Korean response와 English response 흐름이 browser에서 확인되었다.

## 8. 브라우저 검증 항목

사용자가 browser에서 확인한 항목은 다음과 같다.

- React 화면이 `http://EC2_PUBLIC_IP`에서 열린다.
- `:5173` 없이 port 80만으로 화면에 접근할 수 있다.
- 한국어 / English toggle이 동작한다.
- Korean inquiry submission이 정상 response를 표시한다.
- English inquiry submission이 정상 response를 표시한다.
- 이전 `5173 -> 8000` 구조에서 보이던 CORS preflight error가 발생하지 않는다.
- `/docs`가 Nginx reverse proxy를 통해 접근된다.

## 9. 서버 내부 검증 명령

EC2 내부에서 확인한 명령과 결과는 다음과 같다.

```bash
python -m unittest discover backend/tests
# 35 tests OK

python backend/scripts/run_api_smoke_test.py
# Preview cases: 7/7 passed

npm run build
# React production build success

systemctl status wizard-defense-support-api
# active/running

ss -ltnp | grep 8000
# FastAPI listens on 127.0.0.1:8000

systemctl status nginx
# active/running

sudo nginx -t
# syntax is ok
# test is successful

curl http://127.0.0.1/health
# {"status":"ok"}

curl -X POST http://127.0.0.1/support/preview \
  -H "Content-Type: application/json" \
  -d '{"text":"테스트 문의입니다.","language":"ko"}'
# 200 JSON response

curl -I http://127.0.0.1
# 200 OK

curl -I http://127.0.0.1/docs
# 200 OK
```

## 10. 로컬 포트 검증 명령

사용자 local PowerShell에서 EC2 public endpoint의 port 상태를 확인했다.

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
# TcpTestSucceeded: True

Test-NetConnection EC2_PUBLIC_IP -Port 5173
# TcpTestSucceeded: False

Test-NetConnection EC2_PUBLIC_IP -Port 8000
# TcpTestSucceeded: False
```

이 결과는 browser 접근에 필요한 port 80만 열려 있고, 개발용 Vite port 5173과 direct API port 8000은 public inbound에서 제거되었음을 의미한다.

## 11. 결과 요약

- Production-style EC2 접속은 `http://EC2_PUBLIC_IP` 기준으로 동작한다.
- Nginx가 React production build를 port 80에서 제공한다.
- FastAPI는 systemd service로 `127.0.0.1:8000`에서 실행된다.
- `/support/preview`, `/health`, `/docs`, `/openapi.json` reverse proxy 구조가 검증되었다.
- React UI는 `:5173` 없이 browser에서 열린다.
- Korean / English language toggle이 동작한다.
- Inquiry submission이 CORS preflight error 없이 동작한다.
- Public inbound `5173`, `8000`은 닫힌 상태로 확인되었다.
- API endpoint path, response field name, support router behavior, response template behavior는 변경하지 않았다.

## 12. 한계

이번 검증은 production-style 배포 구조 검증이며 다음 항목은 포함하지 않는다.

- HTTPS 없음
- domain 연결 없음
- authentication 없음
- database 없음
- real support ticket storage 없음
- Steamworks integration 없음
- payment/account recovery/helpdesk integration 없음
- centralized logging/monitoring 없음

## 13. 다음 작업 제안

- HTTPS와 domain 연결을 별도 단계에서 검토한다.
- `/docs` 공개 범위를 production 공개 수준에 맞게 제한할지 검토한다.
- 인증 또는 제한된 access control을 도입할지 검토한다.
- Nginx access/error log와 systemd journal 기반 운영 로그 확인 절차를 정리한다.
- Security group least privilege 정책을 public demo 여부에 맞게 다시 점검한다.
## v0.24.0 운영 문서 연결

v0.24.0에서는 검증된 EC2 production-style 구조를 운영하기 위한 runbook을 추가했다. 일상 상태 확인, 재배포, rollback, 장애 대응은 `docs/production_operations_runbook.md`, `docs/deployment_update_and_rollback.md`, `docs/incident_troubleshooting_checklist.md`를 기준으로 수행한다.