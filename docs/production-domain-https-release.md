# Production Domain and HTTPS Release

## Overview

This document records the production domain and HTTPS setup for the Wizard Defense AI Support Preview portfolio project.

The production preview service is available at:

```text
https://support.slowlyp.dev
```

The deployment uses a React frontend served by Nginx and a FastAPI backend running behind an internal reverse proxy.

## Production URL

| Item | Value |
|---|---|
| Production site | `https://support.slowlyp.dev` |
| Health check | `https://support.slowlyp.dev/health` |
| API docs | `https://support.slowlyp.dev/docs` |

## Deployment Architecture

```text
User Browser
    ↓ HTTPS
support.slowlyp.dev
    ↓
Nginx
    ├─ Serves React production frontend
    └─ Proxies API requests to FastAPI
            ↓
        127.0.0.1:8000
```

The backend service is not exposed directly to the public internet.

## Security Group Policy

The production security group follows this access policy:

| Port | Purpose | Source |
|---|---|---|
| 22 | SSH administration | Administrator IP only |
| 80 | HTTP / Let's Encrypt validation / redirect | Public |
| 443 | HTTPS production access | Public |

The following development ports must remain closed in production:

```text
8000
5173
```

## HTTPS Setup Result

HTTPS was enabled using Certbot with the Nginx plugin.

```bash
sudo certbot --nginx -d support.slowlyp.dev
```

Certbot successfully issued and deployed the certificate for the production domain.

## Production Verification Checklist

Use the following checklist after deployment or infrastructure changes.

### DNS

```powershell
nslookup support.slowlyp.dev
```

Expected result:

```text
support.slowlyp.dev resolves to the production EC2 address
```

### Public ports

```powershell
Test-NetConnection support.slowlyp.dev -Port 80
Test-NetConnection support.slowlyp.dev -Port 443
```

Expected result:

```text
Port 80  -> True
Port 443 -> True
```

### EC2 service status

```bash
sudo systemctl status nginx --no-pager
sudo systemctl status wizard-defense-support-api --no-pager
```

Expected result:

```text
nginx active/running
wizard-defense-support-api active/running
```

### Local server checks on EC2

```bash
curl -i http://127.0.0.1
curl -i http://127.0.0.1/health
```

Expected result:

```text
Frontend HTML is returned
Health check returns {"status":"ok"}
```

### Public HTTPS checks

```text
https://support.slowlyp.dev
https://support.slowlyp.dev/health
https://support.slowlyp.dev/docs
```

Expected result:

```text
React frontend opens successfully
Health check returns {"status":"ok"}
FastAPI Swagger docs open successfully
```

## Certificate Renewal Check

Certbot installed a scheduled renewal task. Renewal can be tested with:

```bash
sudo certbot renew --dry-run
```

Expected result:

```text
The simulated renewal succeeds without errors
```

## Production Notes

- Do not commit EC2 public IP addresses to the repository.
- Do not commit private keys, `.pem` files, credentials, or AWS account details.
- Keep FastAPI bound to `127.0.0.1:8000`.
- Keep Nginx as the only public entry point.
- Keep development ports closed in production.
- Use the production domain for portfolio demonstrations.
