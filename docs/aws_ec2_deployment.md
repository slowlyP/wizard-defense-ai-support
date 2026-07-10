# AWS EC2 수동 배포 가이드

## 1. 목적

이 문서는 Wizard Defense AI Support의 FastAPI support preview prototype을 AWS EC2에 수동으로 배포한 절차를 재현 가능한 형태로 정리합니다. Portfolio demonstration을 위한 임시 배포 기준이며 production 운영 절차가 아닙니다.

## 2. 배포 대상

- Repository: `https://github.com/slowlyP/wizard-defense-ai-support.git`
- 기준 tag: `v0.17.0-batch-analysis-report`
- FastAPI app: `backend.app.api:app`
- 확인 대상 endpoint:
  - `GET /health`
  - `GET /docs`
  - `POST /support/preview`

## 3. AWS EC2 구성 요약

| 항목 | 설정 |
| --- | --- |
| AMI | `Ubuntu Server 24.04 LTS` |
| Instance type | `t3.micro` |
| SSH user | `ubuntu` |
| API port | `8000` |
| 배포 방식 | SSH terminal에서 직접 실행하는 임시 수동 배포 |

## 4. Security group

배포 검증에 사용한 inbound rule은 다음과 같이 최소 범위로 설정합니다.

| Type | Port | Source | 목적 |
| --- | ---: | --- | --- |
| SSH | `22` | `My IP` | 관리자 SSH 접속 |
| Custom TCP | `8000` | `My IP` | Browser에서 FastAPI 확인 |

`0.0.0.0/0` 전체 공개는 사용하지 않습니다. 접속 위치의 public IP가 변경되면 `My IP` source를 현재 값으로 다시 제한합니다.

## 5. Key pair 주의사항

- AWS에서 내려받은 `.pem` file은 repository에 복사하거나 commit하지 않습니다.
- Private key를 메신저, issue, 문서, screenshot으로 공유하지 않습니다.
- Key file은 local의 안전한 위치에 보관하고 필요 최소 권한만 부여합니다.
- 실제 key name, AWS account ID, credential, secret은 reusable document에 기록하지 않습니다.
- Key가 노출되었다고 의심되면 해당 key pair 사용을 중단하고 instance 접근 구성을 교체합니다.

## 6. EC2 접속

PowerShell에서 key file이 있는 local directory를 기준으로 다음과 같이 접속합니다.

```powershell
ssh -i ".\wizard-defense-api-key.pem" ubuntu@EC2_PUBLIC_IP
```

`EC2_PUBLIC_IP`는 실행 시점의 실제 EC2 public IPv4 address로만 바꿉니다. 실제 IP는 repository 문서에 저장하지 않습니다.

## 7. 서버 초기 설정

EC2의 Ubuntu shell에서 package index를 갱신하고 필요한 package를 설치합니다.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip
```

설치 상태를 확인합니다.

```bash
git --version
python3 --version
```

## 8. GitHub repository clone

```bash
git clone https://github.com/slowlyP/wizard-defense-ai-support.git
cd wizard-defense-ai-support
git checkout v0.17.0-batch-analysis-report
git status --short
```

`git status --short`에 예상하지 않은 변경이 없는지 확인합니다.

## 9. Python venv 생성

```bash
python3 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
```

SSH session을 새로 열면 repository directory로 이동한 후 `source .venv/bin/activate`를 다시 실행합니다.

## 10. Requirements 설치

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

실제 API key나 `.env` file은 필요하지 않습니다.

## 11. Unittest 실행

```bash
python -m unittest discover backend/tests
```

Test가 `OK`로 종료되는지 확인합니다. 설치된 dependency 조합에 따라 TestClient deprecation warning이 표시될 수 있으나 test 성공 여부는 최종 result로 판단합니다.

## 12. API smoke test 실행

```bash
python backend/scripts/run_api_smoke_test.py
```

`GET /health`와 7개 category의 in-process `POST /support/preview`가 통과하는지 확인합니다. 이 과정은 외부 API나 LLM API를 호출하지 않습니다.

## 13. Uvicorn 실행

```bash
python -m uvicorn backend.app.api:app --host 0.0.0.0 --port 8000
```

`0.0.0.0` bind는 EC2 network interface에서 request를 받을 수 있게 합니다. 접근 범위는 Security group의 `Custom TCP 8000` source를 `My IP`로 제한해 통제합니다. 이 terminal을 닫으면 foreground process도 종료될 수 있습니다.

## 14. Browser 확인

Uvicorn을 실행한 상태에서 [AWS EC2 browser 검증 가이드](aws_ec2_browser_verification.md)에 따라 `/health`, `/docs`, `/support/preview`를 확인합니다.

## 15. 서버 종료 방법

Uvicorn이 실행 중인 SSH terminal에서 다음 keyboard input으로 종료합니다.

```text
Ctrl + C
```

종료 log를 확인한 뒤 더 이상 필요하지 않은 SSH session도 종료합니다.

## 16. 비용 방지 주의사항

- 검증이 끝나면 EC2 instance를 `stop`하거나 더 이상 필요하지 않으면 `terminate`합니다.
- 사용하지 않는 Security group inbound rule의 `8000` port를 닫습니다.
- `stop` 상태에서도 storage 등 일부 resource 비용이 발생할 수 있으므로 연결된 resource를 함께 확인합니다.
- 불필요한 Elastic IP, volume, snapshot 같은 resource가 남지 않았는지 AWS console에서 확인합니다.
- Key pair와 `.pem` file을 안전하게 관리하고 repository에 추가하지 않습니다.

## 17. 한계

- SSH terminal에서 직접 실행하는 임시 수동 배포입니다.
- HTTPS가 구성되어 있지 않습니다.
- Domain이 연결되어 있지 않습니다.
- `systemd`, `nginx`, `gunicorn`을 구성하지 않았습니다.
- Authentication과 authorization이 없습니다.
- 자동 restart, monitoring, centralized logging, backup, CI/CD가 없습니다.
- Public production customer support system으로 사용하면 안 됩니다.

## 18. v0.22.0 Production-style Deployment Hardening

The earlier EC2 notes are still useful for manual API checks and temporary browser verification. For production-style review, use the hardened Nginx + systemd path:

- Build React with `VITE_API_BASE_URL=`.
- Copy `frontend/dist` into `/var/www/wizard-defense-support`.
- Run FastAPI with systemd on `127.0.0.1:8000`.
- Serve static files and reverse proxy API paths through Nginx on port 80.
- Keep SSH on port 22 limited to My IP.
- Keep port 80 limited to My IP during review or to the intended public range for a public demo.
- Close ports 5173 and 8000 after the Nginx reverse proxy is verified.

See `docs/production_deployment_hardening.md`, `docs/nginx_systemd_deployment.md`, `deploy/nginx/wizard-defense-support.conf.example`, and `deploy/systemd/wizard-defense-support-api.service.example`.
