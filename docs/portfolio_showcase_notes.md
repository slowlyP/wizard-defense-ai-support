# Portfolio Showcase Notes

## 1. 목적

Recruiter와 interviewer가 프로젝트의 구현 범위, 기술적 의사결정과 향후 확장 방향을 빠르게 이해하도록 README의 표현 기준과 면접 설명 포인트를 정리한다.

## 2. 포트폴리오에서 강조할 점

- Dataset과 label boundary부터 classifier, API, UI, deployment, operations까지 단계별로 만든 end-to-end 과정
- LLM을 바로 도입하지 않고 measurable deterministic baseline을 먼저 만든 판단
- 실제 게임 repository를 read-only reference로 검증한 knowledge coverage
- Reward/payment/refund 문의를 human review로 보내는 safety-first routing
- 구현 결과를 unittest, smoke test, CSV experiment와 versioned summary로 남긴 재현성
- EC2/Nginx/systemd 적용뿐 아니라 rollback, incident, privacy/security 계획까지 문서화한 운영 관점

## 3. 면접에서 설명할 핵심 문장

> “처음에는 rule-based classifier와 template으로 재현 가능한 baseline을 만들고 dataset v2에서 개선 결과를 측정했습니다.”

> “질문 coverage를 넓힌 뒤 local structured chunk와 keyword/topic scoring으로 retrieval baseline을 만들었습니다. 아직 embedding이나 vector DB를 쓰지는 않습니다.”

> “Future LLM integration은 실제 provider 대신 deterministic mock adapter로 interface와 prompt/guardrail 흐름부터 검증했습니다.”

> “민감 문의는 자동 답변 권한을 주지 않고 human review로 올리며, 환불·보상·복구·수정 일정 약속을 guardrail로 제한했습니다.”

## 4. 현재 시스템을 LLM 프로젝트로 과장하지 않는 표현

사용할 표현:

- Rule-based AI support preview tool
- Deterministic support assistant
- Deterministic retrieval baseline
- Optional local mock LLM adapter prototype
- Future LLM/RAG-ready architecture

사용하지 않을 표현:

- 실제 LLM chatbot
- Production RAG chatbot
- OpenAI/Claude-powered assistant
- Fully automated customer support
- Production-ready support system

## 5. LLM/RAG 관련성을 설명하는 정확한 표현

현재는 외부 LLM API, embedding과 vector DB를 사용하지 않는다. 대신 classifier/template baseline, structured knowledge retrieval, provider-neutral adapter interface, prompt redaction과 guardrail을 분리해 향후 LLM/RAG 후보를 비교할 architecture를 준비했다. `MockLLMAdapter`는 생성 품질을 증명하는 모델이 아니라 integration boundary를 검증하는 deterministic test double이다.

## 6. 기술적으로 보여줄 수 있는 부분

### Classifier

Rule priority와 keyword를 설명할 수 있고 dataset v1/v2 및 TF-IDF baseline과 비교한 실험 결과가 있다. Category뿐 아니라 urgency, response type과 human review routing으로 이어진다.

### Retrieval baseline

Bilingual chunk metadata, deterministic scoring, `top_k`, stable tie-break와 sensitive safety metadata를 코드와 CSV로 보여줄 수 있다. Unrelated query가 context를 만들어 내지 않는 fallback도 테스트한다.

### Mock adapter

Provider-neutral protocol, sanitized prompt object, deterministic output과 demo-only 분리를 보여준다. 실제 provider dependency나 key는 없다.

### Guardrail

Forbidden promise concept, prompt redaction, sensitive fallback과 human review 정책을 unit test로 검증한다. Regex 한계도 명시한다.

### Deployment

Nginx port 80, React static build, same-origin reverse proxy, FastAPI `127.0.0.1:8000`, systemd 구조와 Security Group의 public `5173`/`8000` 제거를 설명할 수 있다.

### Operations docs

Health check, update, rollback, incident troubleshooting, secret/privacy/access-control 계획으로 “배포했다”를 넘어 운영 시 고려사항을 보여준다.

## 7. 주의해서 말해야 할 부분

- EC2 verification은 production-style 구조 검증이지 production-ready 인증이 아니다.
- Human review flag는 실제 ticket 생성이나 담당자 배정을 의미하지 않는다.
- Retrieval score는 relevance 확률이나 정답 보장이 아니다.
- Mock adapter는 real model의 hallucination, cost, latency를 평가하지 않는다.
- Game guide는 현재 확인된 build/reference 범위이며 live service balance를 보장하지 않는다.
- 실제 사용자 데이터, payment 처리, account recovery 또는 Steamworks integration은 없다.

## 8. 다음 포트폴리오 보강 작업

1. React 화면, 민감 문의 결과, architecture와 deployment verification screenshot 추가
2. Retrieval relevance evaluation set과 baseline/vector candidate 비교 chart 추가
3. 면접용 2~3분 demo script와 핵심 code walkthrough 경로 정리

