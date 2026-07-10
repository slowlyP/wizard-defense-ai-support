# Frontend 다국어 선택 요약 (v0.21.0-frontend-i18n-language-toggle)

## 1. 목적

Random Wizard Defense support preview에서 사용자가 한국어와 English를 직접 선택하고, frontend UI와 deterministic response draft/internal note를 같은 언어로 확인할 수 있도록 합니다.

## 2. 변경 이유

기존 v0.20.0 frontend는 한국어만 제공했습니다. PC / Steam 방향의 portfolio demo에서 한국어 사용자 경험을 유지하면서 English support preview도 설명할 수 있도록 local i18n layer를 추가했습니다.

## 3. 언어 선택 UI 구성

- Page 상단에 `한국어`와 `English` toggle을 배치했습니다.
- Default는 `한국어`입니다.
- 선택값은 browser `localStorage`의 `wizard-support-language`에 저장합니다.
- Title, subtitle, form, example chip, loading/error, result label, enum friendly label, preview note를 선택 언어로 전환합니다.
- Original enum value는 두 언어 모두 그대로 표시합니다.
- `needs_human`은 한국어에서 `필요`/`불필요`, English에서 `Required`/`Not required`로 표시합니다.

## 4. API language field 설계

- Endpoint: `POST /support/preview`
- Optional request field: `language`
- Allowed value: `ko`, `en`
- Default: `ko`
- 기존 `{"text": "..."}` caller는 변경 없이 한국어 response를 받습니다.
- Response field name과 support router output은 변경하지 않았습니다.

## 5. 한국어/영어 응답 처리 방식

- `backend/app/response_templates.py`에 Korean/English 고정 template과 internal note를 별도로 정의했습니다.
- 외부 translation API와 LLM API를 사용하지 않습니다.
- English bug triage는 reproduction step, floor/stage, wizard composition, screenshot, Windows/Steam demo build, PC resolution, fullscreen/windowed state를 요청합니다.
- English balance response는 Steam demo/PC playtest review를 안내하지만 guaranteed change나 patch date를 약속하지 않습니다.
- Classifier는 기존 Korean keyword rule을 그대로 사용하므로 English inquiry classification coverage는 제한적입니다.

## 6. 검증 결과

- Language 생략, `ko`, `en`, invalid value를 포함한 backend unittest 35개가 통과했습니다.
- API smoke 7개가 통과했고 historical CSV는 원래 hash로 복원했습니다.
- Response field 유지와 Korean/English draft/note language를 확인했습니다.
- Korean/English 요청에서 category, urgency, `needs_human`, response type, routing reason이 동일함을 확인했습니다.
- English bug/balance safety wording을 검증했습니다.
- `npm install`과 Vite production build가 통과했고 29개 module을 bundle로 생성했습니다.
- Local frontend HTTP 200과 live English API response를 확인했습니다.
- 이번 실행 환경에는 사용할 수 있는 browser instance가 없어 language toggle click과 `localStorage` persistence의 browser automation은 수행하지 못했습니다. Local browser에서 최종 interaction을 수동 확인해야 합니다.

## 7. 변경하지 않은 항목

- `POST /support/preview` endpoint path
- Response field name 8개
- Support router category, urgency, `needs_human`, routing behavior
- Dataset v1/v2
- 기존 experiment CSV
- Unity game repository file
- Swagger `/docs`
- 실제 Steam login, account recovery, payment, ticket/helpdesk integration

## 8. 한계

- Support router classifier는 Korean-first rule set이므로 English free-text category accuracy를 별도로 보장하지 않습니다.
- Static UI/template dictionary 방식이며 locale file 분리나 pluralization library는 사용하지 않습니다.
- Browser language를 자동 감지하지 않고 저장된 user selection만 사용합니다.

## 9. 다음 작업 제안

- 별도 승인 후 English inquiry classifier evaluation dataset을 설계합니다.
- Frontend component test로 language persistence와 visible copy 전환을 자동화합니다.
- Locale가 늘어나면 translation dictionary를 별도 module로 분리합니다.
