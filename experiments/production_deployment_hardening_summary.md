# Production Deployment Hardening Summary

Version: v0.22.0-production-deployment-hardening

## Summary

This pass prepares a production-style EC2 deployment path for the React + FastAPI support preview tool without changing support routing behavior, response templates, dataset files, or Unity project files.

## Implemented

- Added same-origin production support in the frontend API base handling.
- Added Nginx example config for static React hosting and FastAPI reverse proxying.
- Added systemd example service for running FastAPI on localhost.
- Added production deployment hardening docs and Nginx/systemd notes.
- Documented security group cleanup after reverse proxy verification.

## Why It Matters

Serving React from Nginx on port 80 and proxying API requests to FastAPI on localhost removes the browser-side `5173 -> 8000` cross-origin split used during development. Production requests can use `/support/preview` from the same origin while direct public access to port 8000 can be closed.

## Out of Scope

No HTTPS, domain, authentication, real data handling, Steamworks integration, payment flow, account recovery, external helpdesk integration, LLM API calls, or Unity repository changes were added.
