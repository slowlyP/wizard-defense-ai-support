# Security and Access Control Plan

버전: v0.25.0-security-and-access-control-plan
대상: EC2 production-style React + FastAPI 고객지원 미리보기 보안 계획

## 1. 목적

이 문서는 현재 EC2 production-style 배포를 더 production-ready한 방향으로 발전시키기 전에 검토해야 할 보안, 접근 제어, API 보호, secret 관리 기준을 정리한다.

이번 단계는 계획 문서화이며 HTTPS, 인증, 데이터베이스, Steamworks, 실제 고객지원 시스템 연동을 구현하지 않는다. 실제 public IP, AWS 계정 ID, `.pem` 경로, private key, AWS credential은 기록하지 않고 `EC2_PUBLIC_IP` placeholder만 사용한다.

## 2. 현재 배포 구조의 보안 상태

현재 구조에서 이미 적용된 보안상 개선은 다음과 같다.

- Nginx가 port `80`에서 public entry point 역할을 한다.
- React production build는 Nginx static root에서 제공된다.
- FastAPI는 public interface가 아니라 `127.0.0.1:8000`에서 systemd service로 실행된다.
- Nginx가 `/support/preview`, `/health`, `/docs`, `/openapi.json`을 내부 FastAPI로 reverse proxy한다.
- public inbound `5173`과 `8000`은 닫힌 상태가 정상이다.
- SSH `22`는 `My IP`로 제한하는 것이 기본 정책이다.
- frontend는 production build에서 same-origin `/support/preview`를 호출해 기존 `5173 -> 8000` CORS split을 피한다.

## 3. 아직 미구현된 보안 항목

현재 구조에는 다음 항목이 아직 없다.

- HTTPS
- domain
- authentication
- authorization
- database
- persistent support ticket storage
- Steamworks integration
- real user account
- payment/account recovery/helpdesk integration
- centralized security monitoring
- rate limiting

이 항목들은 실제 public production service로 전환하기 전에 별도 작업으로 검토해야 한다.

## 4. HTTPS 적용 계획

HTTPS는 domain 연결 이후 certificate을 적용하는 방식으로 검토한다.

권장 방향:

- domain을 EC2 또는 load balancer endpoint에 연결한다.
- certificate 발급 방식을 결정한다.
- Nginx에 TLS 설정을 추가한다.
- HTTP port 80 요청을 HTTPS로 redirect한다.
- mixed content가 발생하지 않도록 frontend API path는 same-origin relative path를 유지한다.
- certificate 갱신 절차와 실패 시 알림 방식을 운영 문서에 추가한다.

주의:

- HTTPS 적용 전까지 browser에는 안전하지 않은 HTTP 경고가 표시될 수 있다.
- HTTPS 적용 후에도 `/support/preview` endpoint path와 response field는 변경하지 않는다.

## 5. 접근 제어 계획

운영 모드는 크게 두 가지로 나눠 검토한다.

### Public demo mode

- 포트폴리오 데모로 공개 가능한 범위만 제공한다.
- 입력에는 계정, 결제, 개인정보를 넣지 말라는 안내를 유지한다.
- `/support/preview`는 abuse 가능성을 고려해 rate limiting을 검토한다.
- `/docs`와 `/openapi.json` 공개 여부를 별도로 결정한다.

### Admin/internal mode

- 운영자 또는 평가자에게만 접근을 허용하는 모드다.
- IP allowlist, basic auth, reverse proxy auth, application auth 중 하나를 검토할 수 있다.
- future auth options는 실제 계정 체계가 필요할 때 별도 설계한다.

미래 인증 후보:

- Nginx basic auth for temporary internal review
- Application-level login
- OAuth/OIDC provider integration
- Admin-only route protection

이번 단계에서는 인증을 구현하지 않는다.

## 6. API 보호 계획

`/support/preview`는 사용자 입력을 받는 endpoint이므로 abuse prevention을 검토해야 한다.

검토 항목:

- request size limit
- request rate limit
- timeout 설정
- JSON parse error handling
- CORS policy 유지
- 입력값에 계정/결제/개인정보를 넣지 않도록 frontend 안내 유지
- `/health` 공개 범위 결정
- `/docs`와 `/openapi.json` 공개 범위 결정

현재 CORS 정책은 local development용 allowlist를 유지하고, production browser flow는 same-origin Nginx proxy로 처리한다. wildcard CORS를 열지 않는 방향을 유지한다.

## 7. Security group policy

현재 권장 정책은 다음과 같다.

- Keep `22` from `My IP`
- Keep `80` for controlled test range or public demo range
- Keep `5173` closed
- Keep `8000` closed

HTTPS를 적용하면 추가로 `443` inbound rule이 필요할 수 있다. 그 경우에도 `5173`과 `8000`은 public inbound로 열지 않는다.

## 8. Secret management policy

현재 서비스는 외부 API key나 database secret 없이 동작한다.

기본 정책:

- `.pem` file을 repository에 commit하지 않는다.
- private key 내용을 문서, issue, commit, screenshot에 포함하지 않는다.
- AWS credential을 repository에 commit하지 않는다.
- API key가 필요한 기능을 추가할 경우 environment variable 또는 managed secret store를 검토한다.
- `.env`와 `.env.local`은 commit하지 않는다.
- reusable docs에는 실제 public IP 대신 `EC2_PUBLIC_IP` placeholder를 사용한다.

## 9. Operational risk

운영 중 주요 위험은 다음과 같다.

- EC2 stop/start 후 public IP가 바뀔 수 있다.
- systemd service가 failed 상태가 될 수 있다.
- Nginx 설정 오류로 502 또는 static serving 실패가 발생할 수 있다.
- HTTPS가 없으므로 browser에 보안 경고가 표시될 수 있다.
- `/docs` 공개가 API 탐색 경로를 제공할 수 있다.
- rate limit이 없으면 `/support/preview`가 반복 호출될 수 있다.
- 로그에 사용자 입력이 남을 경우 개인정보 리스크가 생길 수 있다.

## 10. Recommended next steps

권장 다음 단계는 다음과 같다.

1. Domain과 HTTPS 적용 절차를 별도 문서로 설계한다.
2. `/docs`와 `/openapi.json` 공개 범위를 결정한다.
3. public demo mode와 internal review mode를 구분한다.
4. rate limiting 또는 request size limit 적용 여부를 검토한다.
5. 개인정보 입력 방지 문구와 logging policy를 점검한다.
6. secret scan을 release checklist에 고정한다.
7. Security group least privilege 기준을 release마다 확인한다.

## 11. Limitations

이번 문서는 보안 계획이며 구현이 아니다.

- HTTPS를 구현하지 않았다.
- authentication을 구현하지 않았다.
- authorization을 구현하지 않았다.
- database를 추가하지 않았다.
- persistent support ticket storage를 추가하지 않았다.
- Steamworks integration을 추가하지 않았다.
- 실제 계정, 결제, 계정 복구, helpdesk 연동을 추가하지 않았다.
- 외부 API 또는 LLM API를 호출하지 않았다.