# Security Group Cleanup Verification

버전: v0.23.0-production-deployment-verification
대상: EC2 production-style 배포 이후 inbound port 정리 검증

## 1. 목적

이 문서는 React + FastAPI 고객지원 미리보기 도구를 Nginx reverse proxy 기반 production-style 구조로 전환한 뒤, EC2 Security Group inbound rule이 의도대로 정리되었는지 검증한 결과를 기록한다.

실제 public IP, AWS 계정 ID, `.pem` 경로, private key, AWS credential은 기록하지 않는다. 검증 문서에서는 `EC2_PUBLIC_IP` placeholder만 사용한다.

## 2. 기존 개발용 포트

초기 browser 검증과 local development에서는 다음 port가 사용되었다.

- `5173`: Vite React dev server
- `8000`: FastAPI direct access

이 구조는 개발 중에는 편리하지만 browser 기준으로 `5173 -> 8000` cross-origin 호출이 발생할 수 있고, production-style 배포에서는 direct public exposure를 줄이는 편이 안전하다.

## 3. production-style 이후 유지 포트

production-style 검증 이후 유지해야 하는 inbound rule은 다음과 같다.

- `22`: SSH, Source는 `My IP`
- `80`: HTTP, Source는 `My IP` 또는 통제된 test range

public demo로 공개할 경우 `80`의 Source 범위는 별도 보안 검토 후 결정해야 한다. 관리용 SSH `22`는 계속 `My IP`로 제한하는 것이 기본이다.

## 4. 제거된 인바운드 규칙

검증 이후 다음 inbound rule은 제거된 상태로 확인되었다.

- `5173`: Vite dev server public access 제거
- `8000`: FastAPI direct public access 제거

FastAPI는 계속 `127.0.0.1:8000`에서 실행되지만, public inbound `8000`은 필요하지 않다. 외부 browser는 Nginx port 80을 통해서만 접근한다.

## 5. 포트 확인 방법

사용자 local PowerShell에서 다음 방식으로 port 접근 여부를 확인했다.

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
Test-NetConnection EC2_PUBLIC_IP -Port 5173
Test-NetConnection EC2_PUBLIC_IP -Port 8000
```

EC2 내부에서는 다음 방식으로 service 상태와 내부 binding을 확인할 수 있다.

```bash
sudo systemctl status nginx
sudo systemctl status wizard-defense-support-api
ss -ltnp | grep 8000
curl http://127.0.0.1/health
```

## 6. 정상 기준

정상 기준은 다음과 같다.

- `80`: `TcpTestSucceeded True`
- `5173`: `TcpTestSucceeded False`
- `8000`: `TcpTestSucceeded False`

사용자가 제공한 실제 확인 결과도 위 기준과 일치했다.

## 7. 주의사항

- `22`를 제거하면 SSH 접속이 불가능해질 수 있다.
- `22`의 Source를 너무 넓게 열면 관리 포트 노출 위험이 커진다.
- `80`을 닫으면 browser에서 React UI에 접근할 수 없다.
- public production으로 전환한다면 `80` Source 범위를 어떻게 열지 별도 검토해야 한다.
- HTTPS를 추가하면 `443` inbound rule이 필요할 수 있다.
- `5173`과 `8000`은 개발 편의를 위한 port이며 production-style public access에는 필요하지 않다.
- 실제 public IP, `.pem` file, AWS credential, private key는 repository 문서나 commit에 포함하지 않는다.

## 8. 다음 보안 작업

- HTTPS 구성
- domain 연결
- authentication 또는 제한된 access control 검토
- Nginx/systemd logging 점검
- least privilege security group 재검토
- `/docs`와 `/openapi.json` 공개 범위 검토