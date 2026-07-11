# Portfolio README Showcase 요약

## 1. 목적

`v0.30.0-portfolio-readme-showcase`에서 recruiter/interviewer가 1분 안에 프로젝트의 구현 범위, 안전 경계, 기술 stack과 future LLM/RAG 방향을 이해하도록 repository entry point를 재구성했다.

## 2. 문제 배경

기존 README는 milestone이 누적되어 최신 구현과 초기 scaffolding 설명이 섞여 있었다. 중요한 기능은 존재했지만 현재 시스템이 실제 LLM/RAG chatbot인지, 무엇이 구현·미구현인지, 배포가 어떤 구조인지 빠르게 파악하기 어려웠다.

## 3. README 개선 내용

- One-line summary와 1분 portfolio overview를 최상단에 배치
- Implemented/not implemented table로 범위를 즉시 구분
- Default API flow와 demo-only mock adapter flow를 분리한 architecture 추가
- Core features, tech stack, API, frontend, deployment를 짧은 section으로 정리
- v0.1.0~v0.30.0 milestone을 phase별 compact table로 압축
- Demo artifact, 86 tests, smoke 7/7과 frontend build 결과를 표시
- 면접에서 사용할 한국어 설명 문장, limitations와 next steps 추가

## 4. 포트폴리오 설명 강화 내용

단순 기능 목록보다 “왜 rule-based baseline을 먼저 만들었는가”, “retrieval과 mock adapter를 어떻게 future architecture와 분리했는가”, “민감 문의를 왜 human review로 보내는가”를 설명하도록 구성했다. EC2 배포와 operations/security 문서도 end-to-end engineering evidence로 연결했다.

## 5. 현재 구현 범위와 미구현 범위 정리

구현 범위는 classifier, topic knowledge, deterministic template, local retrieval, demo-only mock adapter, guardrail, FastAPI/React, bilingual mode와 production-style deployment verification이다. 외부 LLM provider, embedding/vector DB, HTTPS/domain/auth/database/ticket/Steamworks/account/payment/helpdesk integration은 미구현으로 명확히 표시했다.

## 6. 검증 결과

- 전체 backend unittest: 86 tests passed
- API smoke: 7/7 passed, historical output CSV는 실행 직후 원래 byte로 복원
- 요청된 Python module compile: passed
- Mock adapter demo: 14 examples 실행 성공, 기존 CSV는 실행 직후 원래 byte로 복원
- `npm install`: up to date, package 변경 없음
- `npm run build`: Vite production build passed
- `git diff --check`: passed
- Source/API/dataset/기존 CSV와 Unity repository: 이 작업으로 인한 변경 없음
- Secret/IP scan: 추가 `.pem`, AWS/provider key pattern, private key block, 실제 public IPv4 없음

## 7. 변경하지 않은 항목

Backend/frontend source, endpoint path, API request/response schema, Korean/English behavior, dataset v1/v2, 기존 experiment CSV, requirements/package files와 Unity repository를 변경하지 않았다. 외부 API, LLM dependency, key 또는 credential을 추가하지 않았다.

## 8. 한계

README는 기술적 결과를 요약하지만 code review, live demo와 experiment detail을 대체하지 않는다. Screenshot asset은 이번 version에서 추가하지 않았다. Test count와 deployment 상태는 문서화된 최신 검증 시점 기준이다.

## 9. 다음 작업 제안

- Portfolio screenshot과 짧은 demo GIF 추가
- Retrieval evaluation 결과를 시각화한 chart 추가
- Interview용 2~3분 walkthrough와 repository navigation guide 보강
