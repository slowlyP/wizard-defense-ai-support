# React 고객지원 미리보기 요약 (v0.20.0-react-support-preview-frontend)

## 1. 목적

FastAPI Swagger `/docs`를 일반 사용자 화면으로 사용하지 않고, Random Wizard Defense의 한국어 player support preview를 위한 별도 React browser UI를 제공합니다.

## 2. 추가한 화면

- 문의 입력 textarea와 `문의 분석하기` button
- 4개 한국어 example inquiry chip
- Loading과 backend connection error 상태
- Category, urgency, human review, response type 결과 card
- Routing reason, response draft, internal note card
- Portfolio preview 제한사항 안내

## 3. API 연동 방식

- Endpoint: `POST /support/preview`
- Default base URL: `http://127.0.0.1:8000`
- Optional environment variable: `VITE_API_BASE_URL`
- Local CORS allowlist: `http://localhost:5173`, `http://127.0.0.1:5173`
- Existing endpoint path와 response field는 변경하지 않았습니다.

## 4. 한국어 UI 구성

- Page title, subtitle, form, loading, error, result label, 안내 문구를 한국어로 구성했습니다.
- `needs_human=true`는 `필요`, `false`는 `불필요`로 표시합니다.
- Category, urgency, response type은 한국어 설명과 original enum value를 함께 표시합니다.
- `/docs`는 developer API documentation으로 유지합니다.

## 5. 디자인 방향

- Dark purple/navy desktop background
- Gold accent와 soft purple glow
- Card-based result layout
- CSS-only rune, magic book, wizard tower motif
- External image와 font를 사용하지 않음
- 1920×1080 PC browser를 중심으로 구성하고 좁은 화면에서도 layout이 무너지지 않도록 responsive rule을 추가

## 6. 실행 방법

```powershell
python -m uvicorn backend.app.api:app --reload
Set-Location frontend
npm install
npm run dev
```

PowerShell execution policy가 `npm.ps1`을 차단하면 `npm.cmd install`, `npm.cmd run dev`를 사용합니다.

## 7. 검증 결과

- Backend unittest 27개와 API smoke 7개가 통과했습니다.
- Local CORS preflight와 실제 `POST /support/preview` request에서 `http://127.0.0.1:5173` allow origin을 확인했습니다.
- `npm install`은 vulnerability 0건으로 완료되었고 `npm run build`에서 29개 module을 production bundle로 생성했습니다.
- Local backend와 frontend를 함께 실행해 각각 HTTP 200을 확인했고 example 문의가 `bug_report`, `high`, `needs_human=true`, `bug_triage`로 반환되는 것을 확인했습니다.
- 이번 실행 환경에는 사용할 수 있는 in-app browser instance가 없어 click과 screenshot 기반 자동 검증은 수행하지 못했습니다. UI interaction은 local browser에서 수동 확인이 필요합니다.
- `git diff --check`와 protected-file hash로 범위 밖 변경 여부를 확인했습니다.

## 8. 변경하지 않은 항목

- Support router category behavior
- Response template logic
- API request/response field
- Dataset v1/v2
- 기존 experiment CSV
- Unity game repository file
- 실제 Steamworks, authentication, payment, account recovery, helpdesk integration

## 9. 한계

- Local development용 frontend이며 production hosting 설정은 포함하지 않습니다.
- Authentication, history storage, ticket submission이 없습니다.
- Backend process가 중단되면 result를 생성할 수 없습니다.
- Automated frontend component test는 포함하지 않습니다.

## 10. 다음 작업 제안

- 별도 승인 후 frontend component test와 accessibility audit을 추가합니다.
- Production deployment가 필요해지면 frontend hosting과 API base URL 전략을 설계합니다.
- 실제 playtest를 바탕으로 Korean label과 result hierarchy를 개선합니다.
