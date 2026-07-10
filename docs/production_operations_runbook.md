# Production Operations Runbook

버전: v0.24.0-production-operations-runbook
대상: EC2 production-style React + FastAPI 고객지원 미리보기 운영

## 1. 목적

이 문서는 EC2에 배포된 Wizard Defense AI Support preview 서비스를 운영, 상태 확인, 재시작, 업데이트, 장애 대응, 비용 관리할 때 사용하는 운영 runbook이다.

이 문서는 실제 public IP, AWS 계정 ID, SSH 개인키 경로, private key, AWS credential을 기록하지 않는다. 모든 외부 접속 예시는 `EC2_PUBLIC_IP` placeholder를 사용한다.

## 2. 운영 대상 구조 요약

현재 production-style 구조는 다음과 같다.

- Nginx: public HTTP port `80`에서 browser entry point 역할
- React production build: Nginx static root에서 제공
- FastAPI: systemd service로 실행
- FastAPI bind: `127.0.0.1:8000`
- Same-origin API path: browser는 `/support/preview`를 호출하고 Nginx가 내부 FastAPI로 reverse proxy
- Proxy path: `/support/preview`, `/health`, `/docs`, `/openapi.json`
- Public 개발 port: `5173`, `8000`은 security group inbound에서 닫힌 상태가 정상

## 3. 자주 보는 상태 확인 명령

EC2 SSH 접속 후 다음 명령으로 기본 상태를 확인한다.

```bash
sudo systemctl status wizard-defense-support-api
sudo systemctl status nginx
sudo nginx -t
curl http://127.0.0.1/health
```

`/support/preview` smoke 확인은 다음처럼 한다.

```bash
curl -X POST http://127.0.0.1/support/preview \
  -H "Content-Type: application/json" \
  -d '{"text":"테스트 문의입니다.","language":"ko"}'
```

외부 browser 기준으로는 다음 URL을 확인한다.

```text
http://EC2_PUBLIC_IP
http://EC2_PUBLIC_IP/health
http://EC2_PUBLIC_IP/docs
```

## 4. 서비스 시작/중지/재시작

FastAPI systemd service:

```bash
sudo systemctl start wizard-defense-support-api
sudo systemctl stop wizard-defense-support-api
sudo systemctl restart wizard-defense-support-api
sudo systemctl status wizard-defense-support-api
```

Nginx:

```bash
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl status nginx
```

Nginx 설정을 바꾼 뒤에는 reload 전에 반드시 syntax test를 실행한다.

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 5. 로그 확인

FastAPI service 로그:

```bash
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
sudo journalctl -u wizard-defense-support-api -f
```

Nginx access/error log:

```bash
sudo tail -n 100 /var/log/nginx/access.log
sudo tail -n 100 /var/log/nginx/error.log
sudo tail -f /var/log/nginx/error.log
```

장애 상황에서는 먼저 시간대와 요청 path를 기록한 뒤, Nginx error log와 FastAPI journal을 함께 본다.

## 6. React frontend 새로 배포 절차

frontend만 바꿨을 때의 절차다.

```bash
cd /home/ubuntu/wizard-defense-ai-support
cd frontend
npm install
VITE_API_BASE_URL= npm run build
sudo mkdir -p /var/www/wizard-defense-support
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo chown -R www-data:www-data /var/www/wizard-defense-support
sudo nginx -t
sudo systemctl reload nginx
```

확인:

```bash
curl -I http://127.0.0.1
curl http://127.0.0.1/health
```

browser에서는 hard refresh 후 `http://EC2_PUBLIC_IP`를 확인한다.

## 7. Backend code update 절차

backend code가 바뀐 경우에는 테스트를 먼저 통과시킨 뒤 service를 재시작한다.

```bash
cd /home/ubuntu/wizard-defense-ai-support
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
python -m py_compile backend/app/api.py
python -m py_compile backend/app/api_schemas.py
python -m py_compile backend/app/response_templates.py
sudo systemctl restart wizard-defense-support-api
sudo systemctl status wizard-defense-support-api
curl http://127.0.0.1/health
```

API path, response field, support router behavior, response template behavior를 바꾸는 작업은 별도 버전 작업으로 분리하고 문서화한다.

## 8. 새 tag 배포 절차

새 tag를 배포할 때는 작업 트리가 깨끗한지 먼저 확인한다.

```bash
cd /home/ubuntu/wizard-defense-ai-support
git status --short
git fetch --tags
git tag --sort=-creatordate | head
git checkout <TAG>
```

검증과 배포:

```bash
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
cd frontend
npm install
VITE_API_BASE_URL= npm run build
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
cd ..
sudo systemctl restart wizard-defense-support-api
sudo nginx -t
sudo systemctl reload nginx
curl http://127.0.0.1/health
```

## 9. 보안 그룹 점검

정상 운영 기준:

- `22`: SSH, Source는 `My IP`
- `80`: HTTP, Source는 `My IP` 또는 통제된 test range
- `5173`: 닫힘
- `8000`: 닫힘

local PowerShell 확인 예시:

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
Test-NetConnection EC2_PUBLIC_IP -Port 5173
Test-NetConnection EC2_PUBLIC_IP -Port 8000
```

정상 기준은 `80 true`, `5173 false`, `8000 false`다.

## 10. EC2 stop/start 후 확인 항목

EC2를 stop/start하면 public IP가 바뀔 수 있다. 문서에는 실제 IP를 기록하지 말고 필요한 곳에서만 `EC2_PUBLIC_IP`를 새 값으로 해석한다.

확인 순서:

```bash
sudo systemctl status nginx
sudo systemctl status wizard-defense-support-api
curl http://127.0.0.1/health
curl -I http://127.0.0.1
```

외부에서는 다음을 확인한다.

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
```

browser에서 `http://EC2_PUBLIC_IP`가 열리는지 확인한다.

## 11. 비용 관리 주의사항

- 데모가 끝났고 계속 운영할 필요가 없으면 EC2 stop을 검토한다.
- 더 이상 필요 없는 instance, volume, snapshot, Elastic IP가 남아 있는지 AWS console에서 확인한다.
- public demo가 아니라면 port 80 Source 범위를 제한한다.
- 장기간 운영할 경우 로그 크기와 disk 사용량을 주기적으로 확인한다.

```bash
df -h
sudo du -sh /var/log/nginx
sudo journalctl --disk-usage
```

## 12. 운영 한계

현재 구조의 한계는 다음과 같다.

- HTTPS 없음
- domain 없음
- auth 없음
- database 없음
- persistent support ticket storage 없음
- Steamworks integration 없음
- payment/account recovery/helpdesk integration 없음
- centralized monitoring 없음

## 13. 다음 작업 제안

- HTTPS와 domain 연결
- `/docs`와 `/openapi.json` 공개 범위 제한
- 인증 또는 제한된 access control 검토
- Nginx/systemd 로그 회전과 monitoring 정리
- 배포 전후 checklist 자동화
- 백업 또는 rollback tag 정책 명문화

## v0.25.0 보안 계획 연결

v0.25.0에서는 production-ready에 가까운 운영을 위해 보안과 접근 제어 계획 문서를 추가했다. HTTPS, 접근 제어, API 노출, 개인정보와 로그 기준은 `docs/security_and_access_control_plan.md`, `docs/privacy_and_logging_guidelines.md`, `docs/production_security_checklist.md`를 기준으로 검토한다.
