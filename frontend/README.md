# React 고객지원 미리보기

## 목적

FastAPI의 `POST /support/preview`를 한국어 browser UI에서 사용하는 Vite + React frontend입니다. PC / Steam 방향의 문의 응답 초안을 fantasy tower defense 분위기의 desktop 화면에서 확인합니다.

이 화면은 portfolio preview이며 실제 고객지원, Steam login, 인증, 결제, 계정 복구 또는 support ticket 접수 기능이 아닙니다.

## 사전 조건

- Repository root: `C:\UnityProjects\wizard-defense-ai-support`
- Node.js와 npm
- Python dependency 설치 완료

## Frontend dependency 설치

```powershell
Set-Location frontend
npm install
```

PowerShell execution policy로 `npm.ps1` 실행이 막히면 다음처럼 `npm.cmd`를 사용합니다.

```powershell
npm.cmd install
```

## Backend 실행

Repository root의 별도 terminal에서 실행합니다.

```powershell
python -m uvicorn backend.app.api:app --reload
```

Backend 기본 주소는 `http://127.0.0.1:8000`입니다.

## Frontend dev server 실행

`frontend` directory에서 실행합니다.

```powershell
npm run dev
```

PowerShell 환경에 따라 다음 command를 사용할 수 있습니다.

```powershell
npm.cmd run dev
```

Browser에서 `http://127.0.0.1:5173`을 엽니다.

## Environment variable

기본 API 주소를 바꾸려면 `frontend/.env.local`을 생성합니다.

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

값이 없으면 `http://127.0.0.1:8000`을 사용합니다. `.env.local`은 commit하지 않습니다.

## Production build 확인

```powershell
npm run build
```

Build 결과는 `frontend/dist/`에 생성되며 repository에는 commit하지 않습니다.

## Backend 연결 오류 해결

화면에 backend 연결 오류가 표시되면 다음을 확인합니다.

1. Backend terminal에서 Uvicorn이 실행 중인지 확인합니다.
2. `http://127.0.0.1:8000/health`가 `{"status":"ok"}`를 반환하는지 확인합니다.
3. `VITE_API_BASE_URL`에 endpoint path가 아닌 base URL만 입력했는지 확인합니다.
4. Environment variable을 변경한 뒤 Vite dev server를 다시 시작합니다.
5. Frontend origin이 `http://localhost:5173` 또는 `http://127.0.0.1:5173`인지 확인합니다.

## API 개발 문서

`http://127.0.0.1:8000/docs`는 개발자용 Swagger API 문서로 계속 사용할 수 있습니다. 일반 사용자의 주요 browser 경험은 이 React frontend입니다.
