# Nginx + systemd Deployment Notes

Version: v0.22.0-production-deployment-hardening

## Files

- Nginx example: `deploy/nginx/wizard-defense-support.conf.example`
- systemd example: `deploy/systemd/wizard-defense-support-api.service.example`
- Full hardening guide: `docs/production_deployment_hardening.md`

## Deployment Flow

1. Prepare backend venv and dependencies under `/home/ubuntu/wizard-defense-ai-support`.
2. Install the systemd service example and start FastAPI on `127.0.0.1:8000`.
3. Build React with `VITE_API_BASE_URL=` so browser requests use same-origin relative paths.
4. Copy `frontend/dist` to `/var/www/wizard-defense-support`.
5. Install the Nginx site example, run `sudo nginx -t`, and reload Nginx.
6. Verify `http://EC2_PUBLIC_IP/`, `http://EC2_PUBLIC_IP/health`, and the support preview request.
7. Close direct dev ports 5173 and 8000 in the EC2 security group after reverse proxy verification.

## Reverse Proxy Paths

The Nginx example intentionally proxies only the current public API/documentation paths:

- `POST /support/preview`
- `GET /health`
- `GET /docs`
- `GET /openapi.json`

The FastAPI endpoint paths and response schema are unchanged.

## Placeholder Policy

The example files use placeholders only. Replace `EC2_PUBLIC_IP`, `/home/ubuntu/wizard-defense-ai-support`, and `ubuntu` for the actual server environment. Do not commit `.pem` files, AWS credentials, private keys, or real server-only secrets.
