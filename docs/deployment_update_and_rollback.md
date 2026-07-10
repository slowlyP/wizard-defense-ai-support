# Deployment Update and Rollback

버전: v0.24.0-production-operations-runbook
대상: EC2 production-style 배포 업데이트와 rollback 절차

## 1. 목적

이 문서는 `wizard-defense-ai-support` EC2 production-style 배포에서 새 tag를 적용하거나 문제가 생겼을 때 이전 tag로 rollback하는 절차를 정리한다.

실제 public IP, AWS 계정 ID, SSH 개인키 경로, private key, AWS credential은 기록하지 않는다. 외부 접속 예시는 `EC2_PUBLIC_IP` placeholder를 사용한다.

## 2. 업데이트 전 체크리스트

- 현재 작업 트리가 깨끗한지 확인한다.
- 배포하려는 tag가 GitHub에 push되어 있는지 확인한다.
- 이전 정상 tag를 기록한다.
- backend unittest와 API smoke test가 통과하는지 확인한다.
- frontend production build가 통과하는지 확인한다.
- 기존 `experiments/*.csv`가 의도치 않게 변경되지 않았는지 확인한다.
- public inbound `5173`, `8000`을 다시 열지 않는다.

## 3. 현재 버전 확인

```bash
cd /home/ubuntu/wizard-defense-ai-support
git status --short
git --no-pager log --oneline --decorate -n 10
git tag --points-at HEAD
git tag --sort=-creatordate | head
sudo systemctl status wizard-defense-support-api
sudo systemctl status nginx
```

현재 정상 tag와 배포 예정 tag를 운영 기록에 남긴다.

## 4. 새 tag 배포 절차

```bash
cd /home/ubuntu/wizard-defense-ai-support
git status --short
git fetch --tags
git checkout <TAG>
```

backend 검증:

```bash
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
python -m py_compile backend/app/api.py
python -m py_compile backend/app/api_schemas.py
python -m py_compile backend/app/response_templates.py
```

frontend build와 static file 배포:

```bash
cd frontend
npm install
VITE_API_BASE_URL= npm run build
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo chown -R www-data:www-data /var/www/wizard-defense-support
cd ..
```

service 반영:

```bash
sudo systemctl restart wizard-defense-support-api
sudo systemctl status wizard-defense-support-api
sudo nginx -t
sudo systemctl reload nginx
```

## 5. 업데이트 후 smoke verification

```bash
curl http://127.0.0.1/health
curl -X POST http://127.0.0.1/support/preview \
  -H "Content-Type: application/json" \
  -d '{"text":"업데이트 후 확인 문의입니다.","language":"ko"}'
curl -I http://127.0.0.1
curl -I http://127.0.0.1/docs
```

browser에서 확인한다.

- `http://EC2_PUBLIC_IP` 접속
- Korean / English toggle
- inquiry submission
- CORS error 없음
- `/docs` 접근

## 6. rollback 기준

다음 상황이면 rollback을 검토한다.

- FastAPI service가 start/restart 후 failed 상태가 된다.
- `/health`가 실패한다.
- `/support/preview`가 500 또는 502를 반환한다.
- React 화면이 열리지 않는다.
- frontend bundle이 localhost API를 바라본다.
- 주요 browser flow에서 CORS error가 발생한다.
- 새 tag에서 기존 endpoint path 또는 response field 호환성이 깨진다.

## 7. rollback 절차

이전 정상 tag로 checkout한다.

```bash
cd /home/ubuntu/wizard-defense-ai-support
git status --short
git checkout <PREVIOUS_TAG>
```

검증과 재배포:

```bash
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
cd frontend
npm install
VITE_API_BASE_URL= npm run build
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo chown -R www-data:www-data /var/www/wizard-defense-support
cd ..
sudo systemctl restart wizard-defense-support-api
sudo nginx -t
sudo systemctl reload nginx
```

## 8. rollback 후 확인

```bash
sudo systemctl status wizard-defense-support-api
sudo systemctl status nginx
curl http://127.0.0.1/health
curl -X POST http://127.0.0.1/support/preview \
  -H "Content-Type: application/json" \
  -d '{"text":"롤백 후 확인 문의입니다.","language":"ko"}'
curl -I http://127.0.0.1
```

browser에서 `http://EC2_PUBLIC_IP`를 열고 화면, 언어 toggle, inquiry submission을 확인한다.

## 9. 주의사항

- update 전 `git status --short`가 깨끗해야 한다.
- production server에서 직접 임시 수정했다면 반드시 별도 문서로 기록하고 repository에 반영할지 결정한다.
- smoke test는 `experiments/api_local_smoke_test_outputs.csv`를 다시 쓸 수 있으므로, 운영 검증 후 의도치 않은 CSV 변경이 commit에 포함되지 않게 확인한다.
- generated secret, SSH key, AWS credential, 실제 public IP를 commit하지 않는다.
- `/support/preview`, `/health`, `/docs`, `/openapi.json` endpoint path는 배포 절차에서 바꾸지 않는다.
- public inbound `5173`, `8000`을 rollback 중 임시로 열지 않는다.