# Response Template Summary (v0.12.0-response-template-prototype)

## 목적

이 문서는 support router output을 한국어 response draft template으로 변환하는 로컬 prototype 결과를 기록합니다. 이번 단계에서는 web server, FastAPI, 외부 API, LLM API, helpdesk 연동 없이 고정된 안전 템플릿만 사용합니다.

## 사용한 router

- Router: `backend/app/support_router.py`
- Template module: `backend/app/response_templates.py`
- Demo script: `backend/scripts/run_response_template_demo.py`
- Demo output: `experiments/response_template_demo_outputs.csv`
- Demo examples: 20건

## 사용한 response template types

- `acquisition_answer`: 2건
- `balance_feedback_ack`: 3건
- `bug_triage`: 4건
- `growth_answer`: 2건
- `guide_answer`: 4건
- `skill_combat_answer`: 3건
- `tower_progress_answer`: 2건

## template별 정책

- `guide_answer`: 배치, 조합, 초반 운영, 전략 문의에 일반적인 플레이 가이드를 제공합니다.
- `acquisition_answer`: 소환, 획득, 등급, 등장 확률 문의에 안전한 획득 안내를 제공합니다.
- `growth_answer`: 레벨업, 경험치, 성장 재료, 레조넌스 문의에 성장 시스템 안내를 제공합니다.
- `tower_progress_answer`: 층 진행, 잠금 해제, 보스, 보상 조건 문의에 타워 진행 안내를 제공합니다.
- `skill_combat_answer`: 스킬 효과, 쿨타임, 피해 계산, 판정 문의에 전투/스킬 안내를 제공합니다.
- `bug_triage`: 오류 가능성이 있는 문의에 재현 정보와 상황 정보를 요청하며, 보상이나 해결을 약속하지 않습니다.
- `balance_feedback_ack`: 밸런스 의견을 접수했다는 안전한 확인 문구를 제공하며, 조정 여부나 적용 시점을 약속하지 않습니다.

## demo 결과 요약

Category 분포:
- `bug_report`: 4건
- `feedback_balance`: 3건
- `gameplay_guide`: 4건
- `skill_combat`: 3건
- `tower_progress`: 2건
- `wizard_acquisition`: 2건
- `wizard_growth`: 2건

Urgency 분포:
- `high`: 3건
- `low`: 13건
- `medium`: 4건

- 사람 검토 필요: 7 / 20건
- 자동 응답 가능: 13 / 20건

## needs_human=true 응답 처리 기준

- `bug_triage`는 재현 순서, 발생 시점, 사용한 마법사, 층 정보, 화면 상황 같은 확인 정보를 요청합니다.
- `balance_feedback_ack`는 검토 참고 자료로 정리할 수 있다고만 안내하고, 실제 조정 여부는 확정하지 않습니다.
- 기능 category로 분류되었더라도 router가 실패 신호를 감지한 경우에는 사람 검토 또는 추가 정보 요청 문구를 붙입니다.
- `urgency=high`인 경우에는 재현 단계와 상황 정보를 더 구체적으로 요청합니다.

## 자동 응답 가능 케이스 기준

- 단순 플레이 방법, 배치, 조합, 소환 안내, 성장 안내, 층 진행 조건, 스킬 규칙 설명은 자동 응답 초안으로 처리할 수 있습니다.
- 자동 응답 가능 케이스에서도 실제 수치, 확정 일정, 보상 판단은 포함하지 않습니다.

## 안전한 응답 제한사항

- 환불, 보상, 재화 복구를 약속하지 않습니다.
- 정확한 patch date 또는 guaranteed fix를 약속하지 않습니다.
- 운영자가 아직 확인하지 않은 원인을 단정하지 않습니다.
- 외부 API, LLM, 실제 ticket system과 연결하지 않습니다.
- response draft는 최종 고객 응답이 아니라 portfolio prototype용 초안입니다.

## 한계

- 고정 template 기반이므로 문의 세부 맥락에 맞춘 자연스러운 문장 변형은 제한적입니다.
- router와 improved rule classifier의 분류 결과에 의존하므로 분류 오류가 응답 초안에도 전파될 수 있습니다.
- 실제 고객 지원 정책, 보상 정책, 패치 계획과 연결되어 있지 않습니다.

## 다음 작업 제안

- response draft별 검수 checklist와 금지 표현 목록을 추가합니다.
- `needs_human=true` 케이스를 bug, balance, policy review queue로 더 세분화합니다.
- FastAPI 구현 전 template generator 단위 테스트를 추가합니다.
