# Wizard Defense AI Support Preview

> Random Wizard Defense의 플레이어 문의를 분류하고, 로컬 지식과 안전 정책을 바탕으로 한국어/영어 지원 응답 초안을 보여주는 rule-based AI support preview tool입니다.

## 1분 포트폴리오 요약

이 프로젝트는 고객지원 문의를 `category`, `urgency`, `needs_human`으로 라우팅하고, 질문별 topic knowledge와 response template을 이용해 재현 가능한 답변 초안을 만드는 포트폴리오 프로젝트입니다.

처음부터 외부 LLM에 의존하지 않고 rule-based baseline을 구축한 뒤, common question coverage, deterministic retrieval, prompt/guardrail 경계와 optional mock adapter까지 단계적으로 확장했습니다. React UI와 FastAPI API를 연결했고, AWS EC2에서 Nginx + systemd production-style 구조도 검증·문서화했습니다.

> **중요:** 현재 구현은 실제 LLM chatbot이나 production RAG chatbot이 아닙니다. OpenAI, Claude 등 외부 LLM API를 호출하지 않으며 API key도 사용하지 않습니다. Retrieval은 embedding/vector DB가 아닌 local keyword/token/topic scoring이고, `MockLLMAdapter`는 demo-only deterministic formatter입니다.

## 현재 구현 상태

| 구현됨 | 아직 구현되지 않음 |
|---|---|
| Rule-based inquiry classifier와 7개 category | 실제 OpenAI/Claude/provider 연동 |
| `urgency`, `needs_human`, response type routing | Embedding 또는 vector DB 검색 |
| Deterministic topic detection와 support knowledge | Production RAG/LLM generation |
| 한국어/영어 response template | HTTPS, domain, authentication/authorization |
| Local deterministic retrieval baseline | Database, ticket storage, live player data |
| Demo-only `MockLLMAdapter`와 prompt builder | Steamworks, account recovery, payment/refund 처리 |
| Refund/compensation/restoration guardrail prototype | 실제 helpdesk 또는 자동 고객지원 처리 |
| FastAPI backend + React/Vite preview UI | Production-ready 운영 보장 |
| EC2/Nginx/systemd 배포 검증과 운영 문서 |  |

## Architecture

```text
User inquiry
  -> FastAPI POST /support/preview
  -> rule-based router
  -> support knowledge / topic detector
  -> deterministic local retrieval baseline
  -> response template
  -> preview response

Demo-only future architecture validation:
retrieved chunks
  -> prompt builder
  -> MockLLMAdapter (local, deterministic, no external call)
  -> guardrail check
  -> comparison CSV
```

`/support/preview`의 기본 경로는 deterministic template입니다. Mock adapter는 API에 연결되어 있지 않고 별도 demo/test에서만 명시적으로 실행됩니다.

## Core features

- 문의 분류: `gameplay_guide`, `wizard_acquisition`, `wizard_growth`, `tower_progress`, `skill_combat`, `bug_report`, `feedback_balance`
- 운영 routing: `urgency`, `needs_human`, `suggested_response_type`, `routing_reason`
- 답변 초안: gameplay, legendary wizard, fusion, resonance, tower/boss, PC controls, fullscreen/resolution 안내
- 안전 처리: reward loss, payment, refund 사례의 human-review 전환과 금지 약속 검사
- 한국어/영어: API request의 optional `language`로 response draft 언어 선택
- React preview UI: 문의 입력, 예시 chip, loading/error 상태, 분석 결과 card
- Retrieval baseline: bilingual structured chunks와 deterministic `top_k` ordering
- Mock adapter prototype: provider-neutral interface, prompt redaction, local deterministic draft
- Guardrail prototype: refund, compensation, restoration, guaranteed fix, patch date promise 검사

## Tech stack

| 영역 | 기술 |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Test | `unittest`, FastAPI `TestClient`, API smoke script |
| Baseline | Rule-based classifier, TF-IDF/LogisticRegression experiments |
| Retrieval | Pure Python keyword/token/topic scoring |
| Frontend | React, Vite, CSS |
| Deployment | AWS EC2, Nginx, systemd |
| Delivery | Git, GitHub tags/releases, versioned experiment artifacts |

## API example

### `POST /support/preview`

`language`를 생략하면 `ko`가 적용되므로 기존 `{"text": "..."}` caller도 동작합니다.

```json
{
  "text": "What wizard types are available?",
  "language": "en"
}
```

Response field는 다음 8개로 유지됩니다.

```text
text
predicted_category
urgency
needs_human
suggested_response_type
routing_reason
response_draft
internal_note
```

Local 실행:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.app.api:app --reload
```

자세한 계약과 호출 예시는 [API 계약](docs/api_contract.md), [로컬 API 사용법](docs/local_api_usage.md)을 참고하세요.

## Frontend overview

React UI는 문의를 입력하고 API의 category, urgency, human review, response type, routing reason, response draft와 internal note를 card 형태로 보여줍니다. 한국어/English toggle과 local/production same-origin API base 설정을 지원합니다.

```powershell
Set-Location frontend
npm install
npm run dev
```

개발 기본 주소는 frontend `http://127.0.0.1:5173`, backend `http://127.0.0.1:8000`입니다. 화면 설명은 [frontend README](frontend/README.md)를 참고하세요.

## Deployment overview

AWS EC2에서 다음 production-style 구조를 검증했습니다. 이는 production-ready 보장이 아니라 배포·운영 구조 검증입니다.

```text
Browser -> http://EC2_PUBLIC_IP (Nginx port 80)
        -> React production build
        -> same-origin /support/preview
        -> Nginx reverse proxy
        -> FastAPI systemd service on 127.0.0.1:8000
```

- Public entry: Nginx port `80`
- Backend bind: `127.0.0.1:8000`
- Service management: systemd
- React build: Nginx static serving
- Security Group verification: public `5173`, `8000` closed
- 실제 public IP, AWS account ID, credential 또는 private key는 저장소에 기록하지 않음

검증과 운영 절차는 [배포 검증](docs/production_deployment_verification.md), [운영 runbook](docs/production_operations_runbook.md), [보안 계획](docs/security_and_access_control_plan.md)에 있습니다.

## Version history

| Phase | Version | 핵심 milestone |
|---|---|---|
| Project structure/data | v0.1.0–v0.2.0 | Repository scaffolding, Korean docs, dataset v1 |
| Baseline models | v0.3.0–v0.6.0 | Rule classifier, evaluation, TF-IDF, comparison |
| Data quality/baseline improvement | v0.7.0–v0.10.0 | Dataset review/v2, v2 evaluation, improved rule baseline |
| API/response templates | v0.11.0–v0.19.0 | Router, templates, tests, FastAPI, contract, batch analysis, Steam/PC alignment |
| Frontend/deployment | v0.20.0–v0.23.0 | React UI, bilingual mode, EC2 hardening and deployment verification |
| Operations/security | v0.24.0–v0.25.0 | Operations runbook, security/access/privacy plans |
| Knowledge/readiness | v0.26.0–v0.27.0 | Common question coverage, LLM/RAG readiness plan |
| Retrieval/mock architecture | v0.28.0–v0.29.0 | Deterministic retrieval, local mock adapter, prompt/guardrail prototype |
| Portfolio showcase | v0.30.0 | Recruiter-first README and portfolio positioning |

전체 실험 이력은 [experiment log](experiments/experiment_log.md)에서 확인할 수 있습니다.

## Demo and experiment outputs

| Artifact | 보여주는 내용 |
|---|---|
| `experiments/batch_support_preview_outputs.csv` | Dataset v2 batch routing/response output |
| `experiments/batch_support_analysis_report.md` | Category accuracy, mismatch, human-review 분석 |
| `experiments/support_question_coverage_demo_outputs.csv` | Common gameplay/support question coverage |
| `experiments/rag_retrieval_baseline_demo_outputs.csv` | Bilingual ranked retrieval chunks와 safety metadata |
| `experiments/mock_llm_adapter_demo_outputs.csv` | Template vs retrieval vs mock draft vs guardrail 비교 |

## Testing summary

- Backend regression: **86 tests passed**
- API smoke: **7/7 preview cases passed**
- Mock adapter demo: Korean 7 + English 7 examples
- Frontend: Vite production build passed
- Python compile, `git diff --check`, protected dataset/CSV 및 secret/IP scan 수행

```powershell
python -m unittest discover backend/tests
python backend/scripts/run_api_smoke_test.py
python backend/scripts/run_mock_llm_adapter_demo.py
Set-Location frontend
npm run build
```

## 면접에서 이렇게 설명할 수 있습니다

> “저는 LLM을 바로 붙이지 않고 먼저 rule-based baseline부터 만들었습니다. 문의 분류, 긴급도와 human review routing을 테스트 가능한 기준으로 고정한 뒤, 실제 게임 질문에 대한 deterministic knowledge coverage와 keyword/topic retrieval baseline을 구축했습니다.”

> “그다음 향후 LLM/RAG 확장을 위해 retrieval context, prompt redaction, provider-neutral mock adapter와 output guardrail 구조를 설계했습니다. 현재 mock adapter는 실제 LLM이 아니라 architecture 검증용 local formatter입니다.”

> “환불, 결제, 보상, 복구처럼 민감한 문의는 자동 확정하지 않고 `needs_human=true`로 보내며, 금지 약속 guardrail과 deterministic fallback으로 안전하게 처리하도록 설계했습니다.”

> “기능 구현뿐 아니라 React/FastAPI 연결, EC2의 Nginx·systemd 배포, rollback·incident·security 문서까지 포함해 개발과 운영 관점을 함께 보여주려고 했습니다.”

더 자세한 표현 가이드는 [portfolio showcase notes](docs/portfolio_showcase_notes.md)에 있습니다.

## Screenshot placeholder

추후 다음 이미지를 추가할 수 있습니다. 현재 README에는 실제 image asset을 새로 추가하지 않았습니다.

- React bilingual inquiry/response preview
- Sensitive refund inquiry의 human-review 결과
- Retrieval/mock adapter comparison artifact
- EC2 Nginx same-origin deployment 화면

## Limitations

- 실제 LLM provider 연동이 없으며 OpenAI/Claude-powered assistant가 아님
- Embedding/vector DB와 semantic search가 없음
- Retrieval은 작은 in-code knowledge base의 keyword/token/topic baseline
- Mock adapter는 model quality, hallucination, cost 또는 provider outage를 재현하지 않음
- HTTPS, domain, authentication, database, ticket storage가 아직 없음
- Steamworks, account recovery, payment/refund 처리와 live game DB 연동이 없음
- 실제 production 고객지원이나 fully automated support system이 아님

## Next steps

1. 별도 승인 후 real provider adapter readiness와 deterministic fallback 검토
2. 저장소 밖 environment variable/secret 관리 및 cost/latency monitoring 설계
3. Versioned retrieval evaluation과 optional vector search offline 비교
4. Portfolio UI/deployment screenshot 추가

## Repository guide

- `backend/`: classifier, router, knowledge, retrieval, mock adapter, API, tests
- `frontend/`: React/Vite support preview UI
- `data/`: versioned synthetic inquiry datasets와 labeling docs
- `experiments/`: reproducible outputs, evaluation reports, experiment log
- `docs/`: API, deployment, security, LLM/RAG readiness와 portfolio documentation
- `knowledge/`: gameplay/support source documents
