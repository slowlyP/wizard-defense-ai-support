# 로컬 API 사용 가이드

## 1. 문서 목적

이 문서는 Wizard Defense AI Support의 FastAPI prototype을 local 환경에서 설치, 실행, 호출, 검증하는 방법을 설명합니다.

## 2. 로컬 실행 전제

- Python environment가 준비되어 있어야 합니다.
- `requirements.txt`의 dependency를 설치해야 합니다.
- 모든 명령은 repository root인 `C:\UnityProjects\wizard-defense-ai-support`에서 실행합니다.
- virtual environment 사용을 권장합니다.

## 3. Dependency 설치

```powershell
python -m pip install -r requirements.txt
```

## 4. Local API server 실행

```powershell
python -m uvicorn backend.app.api:app --reload
```

기본 주소는 `http://127.0.0.1:8000`입니다. 실행 중인 terminal을 유지한 상태에서 별도 PowerShell terminal로 request를 보냅니다.

## 5. Smoke test 실행

```powershell
python backend/scripts/run_api_smoke_test.py
```

Smoke test는 network port를 열지 않는 in-process client로 `/health`와 7개 category의 `/support/preview`를 확인합니다. 결과는 `experiments/api_local_smoke_test_outputs.csv`에 저장됩니다.

## 6. Unittest 실행

```powershell
python -m unittest discover backend/tests
```

## 7. PowerShell 호출 예시

### `GET /health`

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health"
```

예상 결과의 `status` 값은 `ok`입니다.

### `POST /support/preview`

```powershell
$body = @{
    text = "층 선택 버튼을 눌렀는데 다른 층으로 이동합니다."
    language = "ko"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/support/preview" `
    -ContentType "application/json; charset=utf-8" `
    -Body $body
```

예상 response field는 다음과 같습니다.

- `text`
- `predicted_category`
- `urgency`
- `needs_human`
- `suggested_response_type`
- `routing_reason`
- `response_draft`
- `internal_note`

`language`는 optional이며 `ko` 또는 `en`을 사용합니다. 생략하면 `ko`가 적용됩니다. English response draft가 필요하면 다음처럼 보냅니다.

```powershell
$body = @{
    text = "게임이 전투 중 멈춰서 진행이 안 됩니다."
    language = "en"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://127.0.0.1:8000/support/preview" `
    -ContentType "application/json; charset=utf-8" `
    -Body $body
```

## 8. Troubleshooting

### Module import issue

`No module named 'backend'`와 같은 오류가 발생하면 현재 위치를 확인합니다.

```powershell
Get-Location
Set-Location "C:\UnityProjects\wizard-defense-ai-support"
```

Repository root에서 `python -m uvicorn backend.app.api:app --reload` 형식으로 실행해야 합니다.

### Missing dependency

`No module named 'fastapi'`, `No module named 'uvicorn'`, `No module named 'httpx'` 오류가 발생하면 현재 Python environment에 dependency를 다시 설치합니다.

```powershell
python -m pip install -r requirements.txt
```

### Port already in use

기본 port `8000`이 사용 중이면 다른 port로 실행합니다.

```powershell
python -m uvicorn backend.app.api:app --reload --port 8001
```

이 경우 request URL도 `http://127.0.0.1:8001`로 변경합니다.

### TestClient deprecation warning

설치된 FastAPI, Starlette, HTTP client version 조합에 따라 TestClient 관련 deprecation warning이 표시될 수 있습니다. 현재 test가 `OK`로 완료되고 smoke test가 7건 모두 통과하면 warning 자체는 실패가 아닙니다. Dependency 변경 전에는 호환 version과 test 결과를 함께 확인해야 합니다.

### Virtual environment 미활성화

설치했는데도 module을 찾지 못하면 `python`과 `pip`가 같은 environment를 사용하는지 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
python -m pip --version
```

필요하면 사용 중인 virtual environment를 활성화한 뒤 dependency 설치와 실행 명령을 다시 수행합니다.

## 9. 참고

- 이 API는 local에서만 실행하는 portfolio prototype입니다.
- 외부 service를 호출하지 않습니다.
- API key가 필요하지 않습니다.
- LLM API 또는 실제 helpdesk integration을 사용하지 않습니다.

## 10. React frontend 연동

React dev server는 `http://127.0.0.1:5173`에서 실행하며 `POST /support/preview`를 호출합니다. Backend는 local development를 위해 다음 origin만 CORS allowlist에 포함합니다.

- `http://localhost:5173`
- `http://127.0.0.1:5173`

실행 방법은 [React 고객지원 미리보기 문서](../frontend/README.md)를 확인합니다. `/docs`는 developer API documentation으로 유지되며 한국어 user-facing 경험은 React frontend가 담당합니다.
