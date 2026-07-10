# Incident Troubleshooting Checklist

버전: v0.24.0-production-operations-runbook
대상: EC2 production-style React + FastAPI preview 장애 대응

## 1. 목적

이 문서는 운영 중 장애가 발생했을 때 빠르게 원인을 좁히고 임시 복구 또는 근본 조치를 기록하기 위한 checklist다.

실제 public IP, AWS 계정 ID, SSH 개인키 경로, private key, AWS credential은 기록하지 않는다. 외부 접속 예시는 `EC2_PUBLIC_IP` placeholder를 사용한다.

## 2. 역할 상황별 빠른 분기

- 브라우저 화면이 열리지 않음: Nginx, port 80, static files 확인
- 분석 버튼 실패: `/support/preview`, FastAPI service, Nginx proxy 확인
- `/health` 실패: FastAPI service와 Nginx proxy 확인
- `/docs` 실패: Nginx `/docs` proxy와 FastAPI docs 확인
- 502 Bad Gateway: FastAPI service down 또는 proxy target 문제 확인
- CORS error: frontend build API base와 same-origin 여부 확인
- SSH 실패: security group `22`, instance 상태, local network 확인

## 3. 브라우저 화면이 열리지 않을 때

확인:

```bash
sudo systemctl status nginx
sudo nginx -t
curl -I http://127.0.0.1
ls -la /var/www/wizard-defense-support
sudo tail -n 100 /var/log/nginx/error.log
```

외부 확인:

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
```

조치:

- Nginx가 꺼져 있으면 start/restart한다.
- static root에 `index.html`이 없으면 frontend를 rebuild 후 copy한다.
- port 80이 막혀 있으면 security group을 확인한다.

## 4. 문의 분석 버튼이 실패할 때

확인:

```bash
curl http://127.0.0.1/health
curl -X POST http://127.0.0.1/support/preview \
  -H "Content-Type: application/json" \
  -d '{"text":"버튼 실패 확인 문의입니다.","language":"ko"}'
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
sudo tail -n 100 /var/log/nginx/error.log
```

조치:

- FastAPI service가 failed면 restart한다.
- API response가 422면 request JSON 형식을 확인한다.
- browser console에서 localhost API를 호출하는지 확인한다.

## 5. `/health`가 실패할 때

확인:

```bash
sudo systemctl status wizard-defense-support-api
curl http://127.0.0.1:8000/health
curl http://127.0.0.1/health
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
```

판단:

- `127.0.0.1:8000/health`는 성공하고 `127.0.0.1/health`만 실패하면 Nginx proxy 문제다.
- 둘 다 실패하면 FastAPI service 문제다.

## 6. `/docs`가 실패할 때

확인:

```bash
curl -I http://127.0.0.1/docs
curl -I http://127.0.0.1:8000/docs
sudo nginx -t
sudo tail -n 100 /var/log/nginx/error.log
```

조치:

- FastAPI docs는 열리지만 Nginx path가 실패하면 Nginx location 설정을 확인한다.
- production 공개 범위를 제한하려는 의도인지 운영 기록을 확인한다.

## 7. 502 Bad Gateway

확인:

```bash
sudo systemctl status wizard-defense-support-api
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
ss -ltnp | grep 8000
curl http://127.0.0.1:8000/health
sudo tail -n 100 /var/log/nginx/error.log
```

조치:

```bash
sudo systemctl restart wizard-defense-support-api
sudo systemctl status wizard-defense-support-api
curl http://127.0.0.1/health
```

service가 반복적으로 실패하면 최근 배포 tag로 rollback을 검토한다.

## 8. CORS error

production-style 구조에서는 browser가 같은 origin의 `/support/preview`를 호출해야 한다.

확인:

- browser developer tools에서 request URL이 `http://EC2_PUBLIC_IP/support/preview`인지 확인한다.
- request URL이 `http://127.0.0.1:8000` 또는 `localhost`이면 frontend build API base가 잘못된 것이다.

조치:

```bash
cd /home/ubuntu/wizard-defense-ai-support/frontend
VITE_API_BASE_URL= npm run build
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo systemctl reload nginx
```

## 9. systemd service failed

확인:

```bash
sudo systemctl status wizard-defense-support-api
sudo journalctl -u wizard-defense-support-api -n 200 --no-pager
cat /etc/systemd/system/wizard-defense-support-api.service
```

주요 원인:

- venv path 불일치
- working directory 불일치
- Python dependency 누락
- import error
- port 충돌

조치 후:

```bash
sudo systemctl daemon-reload
sudo systemctl restart wizard-defense-support-api
sudo systemctl status wizard-defense-support-api
```

## 10. Nginx config failure

확인:

```bash
sudo nginx -t
sudo tail -n 100 /var/log/nginx/error.log
```

조치:

- 최근 수정한 site config를 확인한다.
- syntax test가 통과하기 전에는 reload하지 않는다.
- 이전 정상 config로 되돌린 뒤 `sudo nginx -t`를 다시 실행한다.

## 11. frontend build가 localhost를 바라볼 때

증상:

- browser가 `127.0.0.1:8000` 또는 `localhost:8000`으로 API를 호출한다.
- 운영 browser에서 API 연결 실패 또는 CORS error가 난다.

조치:

```bash
cd /home/ubuntu/wizard-defense-ai-support/frontend
VITE_API_BASE_URL= npm run build
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo systemctl reload nginx
```

browser cache를 hard refresh한다.

## 12. port 80 blocked

확인:

```powershell
Test-NetConnection EC2_PUBLIC_IP -Port 80
```

EC2 내부 확인:

```bash
sudo systemctl status nginx
sudo ss -ltnp | grep ':80'
```

조치:

- Nginx가 port 80을 listen하는지 확인한다.
- Security group inbound `80` Source를 확인한다.
- instance가 running 상태인지 확인한다.

## 13. SSH 접속 실패

확인:

- EC2 instance가 running인지 확인한다.
- Security group inbound `22` Source가 현재 local public IP와 일치하는지 확인한다.
- SSH user가 `ubuntu`인지 확인한다.
- SSH 개인키 파일 권한과 위치를 local에서 확인한다.

주의: SSH 개인키 경로와 내용은 repository 문서에 기록하지 않는다.

## 14. 디스크 용량 부족

확인:

```bash
df -h
sudo du -sh /var/log/nginx
sudo journalctl --disk-usage
```

조치:

- 오래된 build artifact와 불필요한 cache를 정리한다.
- log rotation 상태를 확인한다.
- 원인이 반복되면 volume 크기와 monitoring을 별도 작업으로 검토한다.

## 15. 로그 수집 명령

장애 기록에 남길 기본 로그:

```bash
date
hostname
sudo systemctl status wizard-defense-support-api --no-pager
sudo systemctl status nginx --no-pager
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
sudo tail -n 100 /var/log/nginx/error.log
sudo tail -n 50 /var/log/nginx/access.log
curl -i http://127.0.0.1/health
```

## 16. 임시 복구 순서

1. Nginx syntax 확인: `sudo nginx -t`
2. FastAPI service 확인: `sudo systemctl status wizard-defense-support-api`
3. FastAPI restart: `sudo systemctl restart wizard-defense-support-api`
4. Nginx reload: `sudo systemctl reload nginx`
5. `/health` 확인
6. `/support/preview` 확인
7. browser 확인
8. 실패하면 이전 정상 tag rollback 검토

## 17. 근본 조치 기록 방식

장애가 끝난 뒤 다음을 기록한다.

- 발생 시간
- 사용자 증상
- 영향 범위
- 확인한 명령과 결과
- 임시 복구 조치
- 근본 원인 추정
- 재발 방지 작업
- 관련 tag 또는 commit
- 실제 IP, key, credential은 기록하지 않고 placeholder를 사용