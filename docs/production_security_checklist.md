# Production Security Checklist

버전: v0.25.0-security-and-access-control-plan
대상: EC2 production-style 배포 보안 점검

## 1. 목적

이 checklist는 배포 전후 보안 상태를 빠르게 확인하기 위한 문서다. 현재 단계에서는 보안 기능을 구현하지 않고, 확인해야 할 항목과 아직 남은 작업을 명확히 기록한다.

## 2. 배포 전 체크리스트

- [ ] 배포 tag가 확정되었다.
- [ ] `git status --short`가 깨끗하다.
- [ ] backend unittest가 통과한다.
- [ ] API smoke test가 통과한다.
- [ ] frontend production build가 통과한다.
- [ ] `git diff --check`가 통과한다.
- [ ] 기존 experiment CSV가 의도치 않게 변경되지 않았다.
- [ ] 실제 public IP, AWS credential, private key가 문서에 없다.

## 3. 보안 그룹 체크리스트

- [ ] SSH `22`는 `My IP`로 제한한다.
- [ ] HTTP `80`은 controlled test range 또는 public demo 정책에 맞게 제한한다.
- [ ] Vite dev server `5173`은 닫혀 있다.
- [ ] FastAPI direct port `8000`은 닫혀 있다.
- [ ] HTTPS 적용 전까지 `443`은 별도 계획 없이 열지 않는다.
- [ ] EC2 stop/start 후 Source IP와 public IP 변경 가능성을 확인한다.

## 4. Nginx 체크리스트

- [ ] `sudo nginx -t`가 통과한다.
- [ ] Nginx가 port `80`을 listen한다.
- [ ] React static root가 `/var/www/wizard-defense-support`로 맞다.
- [ ] `/support/preview` proxy가 `127.0.0.1:8000/support/preview`로 연결된다.
- [ ] `/health` proxy가 `127.0.0.1:8000/health`로 연결된다.
- [ ] `/docs`와 `/openapi.json` 공개 범위를 검토한다.
- [ ] error log에 secret이 남지 않는다.

## 5. FastAPI/systemd 체크리스트

- [ ] `wizard-defense-support-api` service가 active/running이다.
- [ ] FastAPI가 `127.0.0.1:8000`에 bind된다.
- [ ] public `0.0.0.0:8000` direct serving을 사용하지 않는다.
- [ ] `python -m unittest discover backend/tests`가 통과한다.
- [ ] `python backend/scripts/run_api_smoke_test.py`가 통과한다.
- [ ] service journal에 secret이나 민감한 사용자 입력이 남지 않는다.

## 6. frontend build 체크리스트

- [ ] production build는 `VITE_API_BASE_URL=` 기준으로 생성한다.
- [ ] browser가 `/support/preview` same-origin path를 호출한다.
- [ ] bundle이 `localhost:8000` 또는 `127.0.0.1:8000`을 public browser용 API로 바라보지 않는다.
- [ ] privacy 안내 문구가 유지된다.
- [ ] Korean / English toggle이 동작한다.

## 7. API endpoint exposure 체크리스트

- [ ] `/support/preview`는 필요한 request size와 rate limit 검토 대상으로 기록한다.
- [ ] `/health` 공개 범위를 검토한다.
- [ ] `/docs` 공개 여부를 검토한다.
- [ ] `/openapi.json` 공개 여부를 검토한다.
- [ ] endpoint path와 response field를 변경하지 않는다.
- [ ] wildcard CORS를 열지 않는다.

## 8. secret scan 체크리스트

- [ ] `.pem` file이 repository에 없다.
- [ ] AWS access key pattern이 없다.
- [ ] private key block이 없다.
- [ ] 실제 EC2 public IP가 reusable docs에 없다.
- [ ] docs는 `EC2_PUBLIC_IP` placeholder를 사용한다.
- [ ] `.env`와 `.env.local`이 commit되지 않는다.

## 9. logging/privacy 체크리스트

- [ ] request body 전체를 log로 남기지 않는다.
- [ ] 사용자가 계정/결제/개인정보를 입력하지 않도록 안내한다.
- [ ] Nginx access/error log 공유 시 IP와 민감 정보를 masking한다.
- [ ] FastAPI journal 공유 시 stack trace에 secret이 없는지 확인한다.
- [ ] 실제 고객지원 시스템 전환 전 retention/deletion policy를 설계한다.

## 10. release 후 수동 확인 항목

- [ ] `http://EC2_PUBLIC_IP`에서 React UI가 열린다.
- [ ] `/health`가 `{"status":"ok"}`를 반환한다.
- [ ] `/support/preview`가 200 JSON response를 반환한다.
- [ ] `/docs` 접근 정책이 의도와 일치한다.
- [ ] port `80`은 접근 가능하다.
- [ ] port `5173`은 접근 불가다.
- [ ] port `8000`은 접근 불가다.
- [ ] browser console에 CORS error가 없다.

## 11. 아직 남은 보안 작업

- HTTPS 적용
- domain 연결
- authentication 설계
- authorization 설계
- rate limiting 검토
- request size limit 검토
- `/docs`와 `/openapi.json` 공개 범위 제한 검토
- privacy notice 정리
- retention/deletion policy 설계
- monitoring과 alerting 검토