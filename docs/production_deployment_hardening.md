# Production Deployment Hardening

Version: v0.22.0-production-deployment-hardening
Target: React + FastAPI support preview tool on EC2

## Architecture

The production-style EC2 layout uses Nginx as the public entry point on port 80 and keeps the FastAPI app bound to localhost.

- Browser: `http://EC2_PUBLIC_IP/`
- Nginx static root: `/var/www/wizard-defense-support`
- React build output source: `frontend/dist`
- FastAPI service: `127.0.0.1:8000`
- Public API paths proxied by Nginx: `/support/preview`, `/health`, `/docs`, `/openapi.json`

This keeps the browser on a single origin. The frontend is loaded from port 80 and API calls are sent to the same host and port through relative paths.

## Why This Fixes the 5173/8000 CORS Preflight Issue

The earlier browser verification used a Vite dev server on `:5173` calling FastAPI on `:8000`. That is a cross-origin request, so the browser may send a CORS preflight request.

The production-style layout avoids that split:

- React files are served by Nginx on port 80.
- The browser calls `/support/preview` on the same origin.
- Nginx forwards that request to FastAPI on `127.0.0.1:8000`.
- FastAPI can keep its local-development CORS allowlist instead of opening wildcard CORS.

## Frontend API Base

For local development, keep using the explicit backend URL:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

For production same-origin deployment, build with an empty API base so fetch calls use relative URLs:

```bash
VITE_API_BASE_URL= npm run build
```

If `VITE_API_BASE_URL` is not defined at all, the frontend still defaults to `http://127.0.0.1:8000` for local development convenience.

## React Production Build

```bash
cd /home/ubuntu/wizard-defense-ai-support/frontend
npm install
VITE_API_BASE_URL= npm run build
```

Copy the build output into the Nginx web root:

```bash
sudo mkdir -p /var/www/wizard-defense-support
sudo rsync -a --delete dist/ /var/www/wizard-defense-support/
sudo chown -R www-data:www-data /var/www/wizard-defense-support
```

## FastAPI Service

Use `deploy/systemd/wizard-defense-support-api.service.example` as a starting point.

```bash
sudo cp deploy/systemd/wizard-defense-support-api.service.example /etc/systemd/system/wizard-defense-support-api.service
sudo systemctl daemon-reload
sudo systemctl enable wizard-defense-support-api
sudo systemctl start wizard-defense-support-api
```

Service commands:

```bash
sudo systemctl status wizard-defense-support-api
sudo systemctl restart wizard-defense-support-api
sudo systemctl stop wizard-defense-support-api
sudo journalctl -u wizard-defense-support-api -n 100 --no-pager
```

## Nginx Site

Use `deploy/nginx/wizard-defense-support.conf.example` as a starting point.

```bash
sudo cp deploy/nginx/wizard-defense-support.conf.example /etc/nginx/sites-available/wizard-defense-support
sudo ln -s /etc/nginx/sites-available/wizard-defense-support /etc/nginx/sites-enabled/wizard-defense-support
sudo nginx -t
sudo systemctl reload nginx
```

The example serves static frontend files from `/var/www/wizard-defense-support` and reverse-proxies these paths:

- `/support/preview`
- `/health`
- `/docs`
- `/openapi.json`

## Security Group Cleanup

After Nginx reverse proxy verification:

- Keep port 22 limited to My IP.
- Keep port 80 limited to My IP during review, or to the intended public range for a public demo.
- Close port 5173 after the Vite dev server is no longer used.
- Close port 8000 after `/health` and `/support/preview` work through Nginx.

## Troubleshooting

502 Bad Gateway:
- Check `sudo systemctl status wizard-defense-support-api`.
- Check `sudo journalctl -u wizard-defense-support-api -n 100 --no-pager`.
- Confirm the service binds to `127.0.0.1:8000`.

CORS errors:
- Confirm the production build was created with `VITE_API_BASE_URL=`.
- Confirm the browser calls `/support/preview`, not `http://127.0.0.1:8000/support/preview`.
- Confirm the request is going to `http://EC2_PUBLIC_IP/support/preview`.

API not reachable:
- Check `curl http://127.0.0.1:8000/health` on EC2.
- Check `curl http://127.0.0.1/health` on EC2 after Nginx reload.
- Confirm the EC2 security group allows port 80 from the intended source.

Nginx test failure:
- Run `sudo nginx -t`.
- Check site file syntax and symlink paths.
- Confirm no duplicate `server_name` or conflicting default site blocks are active.

Frontend points to localhost from browser:
- Rebuild with `VITE_API_BASE_URL=`.
- Recopy `frontend/dist` into `/var/www/wizard-defense-support`.
- Hard-refresh the browser cache.

Service fails because venv path is wrong:
- Update `ExecStart` in the systemd unit to match the actual venv path.
- Run `sudo systemctl daemon-reload` after editing the unit.

## Limitations

This hardening pass does not add HTTPS, a custom domain, authentication, real customer data handling, Steamworks integration, payment features, account recovery, or an external helpdesk. It is a production-style portfolio deployment path for the existing local support preview API.

## v0.23.0 Verification Note

The production-style path documented here was later verified on EC2 and recorded in `docs/production_deployment_verification.md`. The verified access pattern uses `http://EC2_PUBLIC_IP` on port 80, keeps FastAPI on `127.0.0.1:8000`, and closes public inbound access to `5173` and `8000` after Nginx reverse proxy verification.