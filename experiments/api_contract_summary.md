# API 계약 문서화 요약 (v0.15.0-api-contract-docs)

## 1. 목적

FastAPI local prototype의 request, response, enum value, validation error, 안전 제한사항을 구현 코드와 일치하는 문서로 정리해 portfolio에서 API 설계 의도를 명확히 설명합니다.

## 2. 작성한 문서

- `docs/api_contract.md`: endpoint별 schema, field, enum, error behavior, 안전 제한사항을 정의합니다.
- `docs/local_api_usage.md`: dependency 설치, server 실행, smoke test, unittest, PowerShell 호출, troubleshooting 절차를 설명합니다.

## 3. API 계약 요약

`POST /support/preview`는 필수 `string` field인 `text`를 입력받습니다. 성공 시 입력 text와 router field 5개, response template field 2개를 포함한 8개 field를 반환합니다. 빈 입력, whitespace-only 입력, 누락 field, 잘못된 type은 HTTP 422로 처리합니다.

Category는 기존 7개 label, urgency는 `low`, `medium`, `high`, suggested response type은 기존 7개 template type만 문서화했습니다.

## 4. 문서화한 endpoint

- `GET /health`
- `POST /support/preview`

## 5. 검증 방법

- `python -m unittest discover backend/tests`
- `python backend/scripts/run_api_smoke_test.py`
- 구현 파일과 보호 대상 CSV의 `git diff` 확인
- 문서 파일 존재 여부와 UTF-8 내용 확인
- Unity game repository의 `git status --short` 확인

## 6. 변경하지 않은 항목

- FastAPI app과 Pydantic schema behavior
- support router와 response template behavior
- API smoke test script와 unittest
- dataset v1과 dataset v2
- 기존 experiment CSV output
- Unity game repository file

## 7. 한계

- 실제 network deployment, 인증, 권한, rate limiting 계약은 포함하지 않습니다.
- FastAPI와 Pydantic version에 따라 HTTP 422의 세부 `detail` 표현은 달라질 수 있습니다.
- response draft는 실제 고객 지원 답변이나 운영 결정을 대신하지 않습니다.

## 8. 다음 작업 제안

- API versioning과 backward compatibility 정책을 별도 문서로 정의합니다.
- production 전환이 승인될 경우 authentication, logging, monitoring 요구사항을 설계합니다.
- client prototype 작업 전에 contract example을 기준으로 UI field mapping을 검토합니다.
