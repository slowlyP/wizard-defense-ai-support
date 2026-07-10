# AWS EC2 배포 문서화 요약 (v0.18.0-aws-ec2-deployment-docs)

## 1. 목적

FastAPI support preview prototype을 AWS EC2에 수동 배포하고 browser에서 확인한 절차를 portfolio에서 재현할 수 있도록 문서화합니다. 이번 작업은 실제 infrastructure 변경이나 application code 변경 없이 기존 검증 결과를 정리합니다.

## 2. 배포 환경

- Cloud: `AWS EC2`
- AMI: `Ubuntu Server 24.04 LTS`
- Instance type: `t3.micro`
- Security group: `SSH 22` from `My IP`, `Custom TCP 8000` from `My IP`
- Application tag: `v0.17.0-batch-analysis-report`
- Process: `python -m uvicorn backend.app.api:app --host 0.0.0.0 --port 8000`
- Access: 실제 IP를 기록하지 않고 `EC2_PUBLIC_IP` placeholder 사용

## 3. 실행한 주요 명령

```bash
git clone https://github.com/slowlyP/wizard-defense-ai-support.git
cd wizard-defense-ai-support
git checkout v0.17.0-batch-analysis-report
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
python -m uvicorn backend.app.api:app --host 0.0.0.0 --port 8000
```

## 4. Browser 검증 결과

- `/health`에서 `{"status":"ok"}` response를 확인했습니다.
- `/docs`에서 Swagger UI가 표시되는 것을 확인했습니다.
- Swagger UI의 `POST /support/preview`에서 한국어 문의를 실행했습니다.
- `레조넌스 했는데 재료만 사라졌어요`는 `bug_report`, `high`, `needs_human=true`, `bug_triage`로 확인되었습니다.
- JSON object 두 개를 붙여 넣을 때 발생하는 HTTP 422 JSON decode error와 올바른 single-object request 형식을 확인했습니다.
- Browser의 automatic `/favicon.ico` 404는 API endpoint 장애가 아님을 확인했습니다.

## 5. 확인된 endpoint

- `GET /health`
- `GET /docs`
- `POST /support/preview`

## 6. 보안 및 비용 관리

- SSH와 API port source를 `My IP`로 제한합니다.
- 실제 public IP, AWS account ID, credential, private key, `.pem` file을 repository에 기록하지 않습니다.
- 검증 후 instance를 `stop` 또는 `terminate`하고 불필요한 `8000` inbound rule을 닫습니다.
- Production 공개 전에는 authentication, HTTPS, reverse proxy가 필요합니다.

## 7. 제한사항

- 임시 수동 배포이며 CI/CD가 없습니다.
- HTTPS와 domain이 없습니다.
- `systemd`, `nginx`, `gunicorn`을 구성하지 않았습니다.
- Authentication, automatic restart, monitoring, centralized logging이 없습니다.
- Production customer support system이 아닙니다.

## 8. 다음 작업 제안

- 별도 승인 후 `systemd` 기반 process 관리 방식을 설계합니다.
- HTTPS와 reverse proxy 도입 요구사항을 검토합니다.
- 비용과 공개 범위를 통제하는 deployment checklist를 별도 운영 문서로 확장합니다.
