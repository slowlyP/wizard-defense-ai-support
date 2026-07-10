# Production Deployment Verification Summary

버전: v0.23.0-production-deployment-verification

## 1. 목적

이 문서는 v0.22.0 production deployment hardening 절차를 실제 EC2에 적용한 뒤 검증한 결과를 요약한다. 목적은 React + FastAPI 고객지원 미리보기 도구가 Nginx, systemd, React production build, Security Group cleanup 구조에서 동작함을 기록하는 것이다.

## 2. 검증된 항목

- Nginx가 port 80에서 React production build를 serving한다.
- FastAPI가 systemd service로 active/running 상태다.
- FastAPI가 public interface가 아니라 `127.0.0.1:8000`에서 실행된다.
- Nginx가 `/support/preview`, `/health`, `/docs`, `/openapi.json`을 reverse proxy한다.
- `http://EC2_PUBLIC_IP`에서 React UI가 열린다.
- Korean / English language toggle이 browser에서 동작한다.
- Inquiry submission이 정상 JSON response를 받는다.
- `/docs` reverse proxy 접근이 가능하다.
- public inbound `5173`, `8000`은 제거되었다.

## 3. 실제 운영 형태 요약

최종 운영 형태는 다음과 같다.

- User browser -> `http://EC2_PUBLIC_IP`
- Nginx -> static frontend files
- React frontend -> same-origin `/support/preview`
- Nginx -> `127.0.0.1:8000/support/preview`
- systemd -> FastAPI process 관리

외부 사용자는 port 80만 사용하고, FastAPI direct port는 public inbound에서 닫힌 상태다.

## 4. 해결된 문제

해결된 주요 문제는 Vite dev server `5173`에서 FastAPI `8000`으로 직접 호출하던 구조의 CORS preflight issue다.

production-style 구조에서는 browser가 같은 origin의 `/support/preview`로 요청하고, Nginx가 내부 FastAPI로 전달한다. 따라서 frontend browser flow에서 이전 cross-origin preflight 문제가 재현되지 않았다.

## 5. 검증 결과

사용자가 제공한 실제 검증 결과는 다음과 같다.

- Repository checkout: `v0.22.0-production-deployment-hardening`
- Backend unittest: 35 tests OK
- API smoke test: 7/7 passed
- React production build: success
- FastAPI systemd service: active/running
- FastAPI bind: `127.0.0.1:8000`
- Nginx service: active/running
- `nginx -t`: syntax is ok / test is successful
- `curl http://127.0.0.1/health`: `{"status":"ok"}`
- `curl POST http://127.0.0.1/support/preview`: 200 JSON response
- `curl -I http://127.0.0.1`: 200 OK
- `curl -I http://127.0.0.1/docs`: 200 OK
- Browser verification: React UI opens through port 80 without `:5173`
- Language toggle: Korean / English works
- Inquiry submission: works without CORS preflight error
- Local port verification: 80 true, 5173 false, 8000 false

## 6. 변경하지 않은 항목

이번 검증 문서화에서는 다음 항목을 변경하지 않는다.

- API endpoint path
- API response field name
- support router behavior
- response template behavior
- dataset v1
- dataset v2
- previous experiment CSV files
- Unity game repository files
- external API 또는 LLM API 연동
- Steamworks, auth, payment, account recovery, real helpdesk integration

## 7. 한계

이번 결과는 production-style deployment verification이며, 완전한 public production system 검증은 아니다.

- HTTPS 없음
- domain 없음
- authentication 없음
- database 없음
- real support ticket storage 없음
- Steamworks integration 없음
- centralized logging/monitoring 없음

## 8. 다음 작업 제안

- HTTPS와 domain 연결 검토
- `/docs`와 `/openapi.json` 공개 범위 제한 검토
- 인증 또는 제한된 access control 도입 검토
- Nginx access/error log와 systemd journal 운영 로그 문서화
- Security Group least privilege 정책 재점검