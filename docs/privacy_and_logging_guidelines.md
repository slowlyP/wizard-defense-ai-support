# Privacy and Logging Guidelines

버전: v0.25.0-security-and-access-control-plan
대상: EC2 production-style 고객지원 미리보기 개인정보와 로그 기준

## 1. 목적

이 문서는 React + FastAPI 고객지원 미리보기 서비스에서 사용자 입력, 로그, 개인정보 노출 위험을 어떻게 다룰지 정리한다.

현재 서비스는 실제 고객지원 시스템이 아니라 portfolio preview다. 실제 public IP, AWS 계정 ID, `.pem` 경로, private key, AWS credential은 기록하지 않는다.

## 2. 현재 서비스의 데이터 처리 범위

현재 서비스의 범위는 다음과 같다.

- support preview only
- no database
- no real ticket storage
- no account integration
- no Steam login
- no payment handling
- no account recovery
- no external helpdesk integration
- no LLM API call

`/support/preview`는 입력 text를 받아 local rule/router/template flow로 preview response를 생성한다.

## 3. 사용자 입력 처리 주의사항

사용자 입력에는 다음 정보를 넣지 않도록 안내해야 한다.

- 실명
- 이메일
- 전화번호
- 주소
- 계정 ID
- 비밀번호
- 결제 정보
- 주문/영수증 정보
- 인증 코드
- private token
- 민감한 개인 사정

현재 frontend의 privacy 안내는 계속 유지되어야 한다.

## 4. 개인정보 입력 방지 안내

UI와 문서에는 다음 취지를 유지한다.

- 이 화면은 portfolio support preview다.
- 실제 고객지원, 계정 복구, 결제 문의 접수 시스템이 아니다.
- 게임 계정이나 결제 정보는 입력하지 않는다.
- 실제 문의 접수가 필요한 경우 별도 공식 채널이 필요하다.

## 5. 로그에 남을 수 있는 정보

현재 구조에서 로그에 남을 수 있는 정보는 다음과 같다.

- client IP 또는 reverse proxy 관련 정보
- request path
- HTTP status code
- user agent
- request time
- FastAPI error stack trace
- systemd service start/stop/restart 기록
- Nginx proxy error 기록

애플리케이션 구현 방식에 따라 request body가 로그에 남을 수도 있으므로, 운영 중에는 request body logging을 피하는 것을 기본 정책으로 한다.

## 6. 로그에 남기면 안 되는 정보

다음 정보는 로그에 남기지 않는 방향으로 설계한다.

- password
- payment information
- account recovery information
- email verification code
- private token
- SSH key path
- private key content
- AWS credential
- real public IP를 재사용 가능한 문서에 고정 기록한 내용
- 사용자가 입력한 민감한 개인정보 원문

장애 분석을 위해 입력 예시가 필요하면 실제 사용자 입력이 아닌 synthetic example을 사용한다.

## 7. Nginx access/error log 주의사항

Nginx access log는 기본적으로 request path와 client 정보가 남을 수 있다.

주의사항:

- query string에 민감한 정보를 넣지 않는다.
- `/support/preview`는 POST body를 사용하므로 URL에는 문의 내용이 들어가지 않게 유지한다.
- error log를 공유할 때 실제 IP와 민감한 header가 포함되지 않았는지 확인한다.
- log file을 외부에 공유할 경우 필요한 부분만 발췌하고 masking한다.

## 8. FastAPI systemd journal log 주의사항

FastAPI journal에는 service error와 stack trace가 남을 수 있다.

정책:

- request body 전체를 info log로 남기지 않는다.
- 예외 발생 시에도 사용자 입력 원문을 그대로 출력하지 않는 방향을 검토한다.
- debugging용 임시 로그를 추가했다면 운영 반영 전 제거한다.
- `journalctl` output을 문서화할 때 secret, IP, 사용자 입력을 masking한다.

## 9. 향후 실제 고객지원 시스템 전환 시 필요한 항목

실제 고객지원 시스템으로 전환하려면 다음이 필요하다.

- retention policy
- data deletion policy
- access audit
- privacy notice
- user consent wording
- data classification policy
- admin access control
- encrypted storage
- backup and restore policy
- incident response policy

이 항목들은 현재 portfolio preview 범위를 넘어선다.

## 10. Limitations

현재 서비스는 개인정보 처리 시스템으로 설계되지 않았다.

- database가 없다.
- ticket persistence가 없다.
- auth가 없다.
- user account가 없다.
- audit log가 없다.
- retention/deletion workflow가 없다.
- privacy notice는 운영 수준 문서가 아니라 preview 안내 수준이다.