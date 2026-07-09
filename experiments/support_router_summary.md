# Support Router Summary (v0.11.0-support-router-prototype)

## 목적

이 문서는 improved rule classifier를 기반으로 한국어 플레이어 문의를 지원 라우팅 정보로 변환하는 로컬 prototype 결과를 기록합니다. 이번 단계에서는 web server, FastAPI, 외부 API, Gmail, Slack, Discord 연동을 구현하지 않고 로컬 Python script와 CSV output만 생성합니다.

## 사용한 classifier

- Classifier: `backend/app/rule_classifier_v2.py`
- Router: `backend/app/support_router.py`
- Demo script: `backend/scripts/run_support_router_demo.py`
- Demo output: `experiments/support_router_demo_outputs.csv`
- Demo examples: 20건

## router output fields

- `predicted_category`: improved rule classifier가 예측한 category입니다.
- `urgency`: 지원 처리 우선순위이며 `low`, `medium`, `high` 중 하나입니다.
- `needs_human`: 자동 응답만으로 충분한지, 사람 검토가 필요한지 나타냅니다.
- `routing_reason`: 라우팅 판단 근거를 짧은 한국어 문장으로 설명합니다.
- `suggested_response_type`: 응답 템플릿 또는 처리 흐름을 고르기 위한 내부 타입입니다.

## category별 routing policy

- `gameplay_guide`: 배치, 조합, 초반 운영, 전략 문의는 `guide_answer`로 라우팅하고 기본 `urgency=low`, `needs_human=false`로 처리합니다.
- `wizard_acquisition`: 소환, 획득, 등급, 등장 확률 안내 문의는 `acquisition_answer`로 라우팅합니다.
- `wizard_growth`: 레벨업, 경험치, 성장 재료, 레조넌스 문의는 `growth_answer`로 라우팅합니다.
- `tower_progress`: 층 진행, 잠금 해제, 보스, 층 보상 문의는 `tower_progress_answer`로 라우팅합니다.
- `skill_combat`: 스킬 효과, 쿨타임, 피해 계산, 타격 판정 문의는 `skill_combat_answer`로 라우팅합니다.
- `bug_report`: 진행 불가, 크래시, 보상/재화 손실, UI 이상은 `bug_triage`로 라우팅하고 `needs_human=true`로 처리합니다.
- `feedback_balance`: 비용, 확률, 효율, 강함/약함, 조정 요청은 `balance_feedback_ack`로 라우팅하고 `urgency=medium`, `needs_human=true`로 처리합니다.

## demo 결과 요약

Category 분포:
- `bug_report`: 2건
- `feedback_balance`: 3건
- `gameplay_guide`: 4건
- `skill_combat`: 3건
- `tower_progress`: 3건
- `wizard_acquisition`: 2건
- `wizard_growth`: 3건

Urgency 분포:
- `high`: 2건
- `low`: 13건
- `medium`: 5건

Suggested response type 분포:
- `acquisition_answer`: 2건
- `balance_feedback_ack`: 3건
- `bug_triage`: 3건
- `growth_answer`: 3건
- `guide_answer`: 4건
- `skill_combat_answer`: 3건
- `tower_progress_answer`: 2건

- 사람 검토 필요: 7 / 20건
- 자동 응답 가능: 13 / 20건

## 사람 검토가 필요한 케이스 기준

- 게임 진행 불가, 크래시, 멈춤, 저장/보상/재화 손실 가능성이 있으면 `bug_report`로 라우팅하고 사람 검토가 필요합니다.
- 기능 단어가 포함되어도 실제 동작 실패나 설명과 실제 효과 차이를 말하면 사람 검토 대상입니다.
- 밸런스, 비용, 확률, 효율, 강함/약함에 대한 조정 요청은 정책 판단이 필요하므로 사람 검토 대상으로 둡니다.
- 분류는 되었지만 문의가 보상 복구, 공지 누락, 버그 여부 확인처럼 운영 판단을 요구하면 `needs_human=true`로 올립니다.

## 한계

- 이 prototype은 rule 기반이며 실제 ticket history나 운영자 처리 결과를 학습하지 않았습니다.
- `routing_reason`은 설명 가능한 데모용 문장이고, 실제 고객 응답 문구는 아닙니다.
- improved rule classifier가 dataset v2 표현 분포에 맞춰져 있을 수 있어 holdout sample에서 별도 검증이 필요합니다.
- 외부 helpdesk, email, chat system과 연결하지 않았으므로 실제 ticket assignment 기능은 없습니다.

## 다음 작업 제안

- `suggested_response_type`별 한국어 응답 템플릿 초안을 작성합니다.
- `needs_human=true` 케이스를 운영 queue 기준으로 더 세분화합니다.
- FastAPI 구현 전 router 입출력 schema와 단위 테스트를 추가합니다.
