# AWS EC2 Browser 검증 가이드

## 1. 목적

이 문서는 EC2에서 실행한 FastAPI support preview prototype을 browser와 Swagger UI로 확인한 절차를 기록합니다. 실제 public IP 대신 항상 `EC2_PUBLIC_IP` placeholder를 사용합니다.

## 2. 사전 조건

- EC2에서 Uvicorn이 `0.0.0.0:8000`으로 실행 중이어야 합니다.
- Security group의 `Custom TCP 8000` source가 검증자의 `My IP`로 설정되어 있어야 합니다.
- Browser를 실행하는 computer의 public IP가 Security group source와 일치해야 합니다.

## 3. Browser 확인 URL

```text
http://EC2_PUBLIC_IP:8000/health
http://EC2_PUBLIC_IP:8000/docs
```

`EC2_PUBLIC_IP`만 현재 EC2 public IPv4 address로 바꿉니다. 실제 IP를 repository, screenshot 설명, reusable document에 고정하지 않습니다.

## 4. `GET /health` 확인

Browser에서 다음 URL을 엽니다.

```text
http://EC2_PUBLIC_IP:8000/health
```

Expected response는 다음과 같습니다.

```json
{"status":"ok"}
```

이 response가 표시되면 EC2 network path, Security group, Uvicorn process, FastAPI app의 기본 응답을 함께 확인한 것입니다.

## 5. Swagger UI 확인

다음 URL을 엽니다.

```text
http://EC2_PUBLIC_IP:8000/docs
```

Swagger UI에서 다음 순서로 실행합니다.

1. `POST /support/preview`를 펼칩니다.
2. `Try it out`을 선택합니다.
3. `Request body`에 JSON object 하나를 입력합니다.
4. `Execute`를 선택합니다.
5. HTTP status와 response body를 확인합니다.

## 6. 테스트 request

```json
{
  "text": "레조넌스 했는데 재료만 사라졌어요"
}
```

## 7. 검증된 response 요약

사용자가 수행한 browser 검증에서 주요 routing field는 다음과 같이 확인되었습니다.

- `predicted_category`: `bug_report`
- `urgency`: `high`
- `needs_human`: `true`
- `suggested_response_type`: `bug_triage`

재료 손실 신호가 포함되어 기존 router가 high-priority bug triage와 사람 검토 대상으로 처리합니다.

## 8. Response fields

성공 response에는 다음 field가 포함됩니다.

- `text`
- `predicted_category`
- `urgency`
- `needs_human`
- `suggested_response_type`
- `routing_reason`
- `response_draft`
- `internal_note`

각 field의 상세 계약은 [로컬 API 계약 문서](api_contract.md)를 기준으로 합니다.

## 9. HTTP 422 JSON error

`Request body`에 JSON object를 두 개 연속으로 붙여 넣으면 하나의 유효한 JSON document가 아니므로 JSON decode error와 HTTP 422가 발생합니다.

잘못된 예시는 다음과 같습니다.

```text
{"text":"첫 번째 문의"}{"text":"두 번째 문의"}
```

`Request body`에는 다음처럼 JSON object 하나만 입력해야 합니다.

```json
{
  "text": "첫 번째 문의"
}
```

여러 문의를 처리할 때는 JSON object를 이어 붙이지 말고 local batch support preview script를 사용합니다.

## 10. `favicon.ico` 404

Browser가 page icon을 찾기 위해 `/favicon.ico`를 자동으로 request할 수 있습니다. App에 favicon route나 static file이 없으면 404 log가 표시될 수 있지만 `/health`, `/docs`, `/support/preview` 동작 문제는 아닙니다.

## 11. 접속 문제 확인 순서

1. SSH terminal에서 Uvicorn process가 계속 실행 중인지 확인합니다.
2. 실행 command가 `--host 0.0.0.0 --port 8000`인지 확인합니다.
3. Security group에서 `Custom TCP 8000` source가 현재 `My IP`인지 확인합니다.
4. URL에 `https`가 아니라 현재 prototype 기준 `http`를 사용했는지 확인합니다.
5. EC2 instance가 `running` 상태이고 public IPv4 address가 변경되지 않았는지 확인합니다.

## 12. 보안 주의사항

- 실제 public IP를 문서에 고정하지 않고 `EC2_PUBLIC_IP` placeholder를 사용합니다.
- `8000` port를 `0.0.0.0/0`에 공개하지 않고 검증자의 `My IP`로 제한합니다.
- 운영 공개 전에는 authentication, HTTPS, reverse proxy가 필요합니다.
- Swagger UI는 endpoint 실행 기능을 제공하므로 production에서는 공개 범위를 별도로 통제해야 합니다.
- API key, AWS credential, private key, `.pem` file을 request나 문서에 포함하지 않습니다.
