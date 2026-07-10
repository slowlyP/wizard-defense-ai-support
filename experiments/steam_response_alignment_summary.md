# Steam 지원 응답 정렬 요약 (v0.19.0-steam-support-response-alignment)

## 1. 목적

기존 deterministic response template을 Random Wizard Defense의 PC / Steam release 방향과 한국어 fantasy tower defense 지원 문맥에 맞게 조정한 결과를 기록합니다.

## 2. 변경 이유

기존 template은 일반 게임 안내에는 적합했지만 mouse-based PC play, Windows build, Steam demo 확인 정보를 명시하지 않았습니다. Mobile-first로 오해될 수 있는 문맥을 피하고 현재 release 방향에 맞는 정보를 요청하도록 wording을 갱신했습니다.

## 3. Steam / PC 방향 반영 내용

- `gameplay_guide`에서 mouse drag placement와 PC play를 안내합니다.
- Bug triage에서 Windows/Steam demo build, PC resolution, fullscreen/windowed 상태를 확인합니다.
- Tower와 system 안내에서 Steam demo 또는 Windows build 조건을 기준으로 설명합니다.
- Balance feedback을 Steam demo/PC playtest 검토 자료로 안내합니다.
- Steamworks 연동이나 release 완료를 단정하지 않고 demo/build context만 사용합니다.

## 4. Category별 response wording 변화

- `gameplay_guide`: PC mouse selection과 drag placement 중심으로 변경했습니다.
- `wizard_acquisition`: Steam demo/Windows build의 acquisition rule 확인을 안내합니다.
- `wizard_growth`: PC build의 growth, experience, resonance 안내로 정리했습니다.
- `tower_progress`: Floor/stage progression과 build별 unlock context를 반영했습니다.
- `skill_combat`: PC build, wizard, target, floor/stage 전투 context를 확인합니다.
- `bug_report`: Reproduction step, floor/stage, wizard composition, error screen, Windows/Steam demo build와 resolution을 요청합니다.
- `feedback_balance`: Steam demo/PC playtest balance review로 접수하되 change나 patch date를 약속하지 않습니다.

## 5. 검증 결과

- Demo example: 7건
- 사람 검토 필요: 2건
- 자동 응답 가능: 5건

Category 분포:
- `bug_report`: 1건
- `feedback_balance`: 1건
- `gameplay_guide`: 1건
- `skill_combat`: 1건
- `tower_progress`: 1건
- `wizard_acquisition`: 1건
- `wizard_growth`: 1건

Response type 분포:
- `acquisition_answer`: 1건
- `balance_feedback_ack`: 1건
- `bug_triage`: 1건
- `growth_answer`: 1건
- `guide_answer`: 1건
- `skill_combat_answer`: 1건
- `tower_progress_answer`: 1건

Urgency 분포:
- `high`: 1건
- `low`: 5건
- `medium`: 1건

- Unittest에서 output field, PC/Steam phrase, safety wording, router integration을 확인했습니다.

## 6. 변경하지 않은 항목

- Support router category, urgency, `needs_human`, `suggested_response_type` behavior
- FastAPI endpoint path와 response field
- Dataset v1/v2와 기존 experiment CSV
- Unity game repository file

## 7. 한계

- 고정 template이므로 개별 PC hardware와 build-specific 원인을 자동 진단하지 않습니다.
- Steamworks integration이나 Steam release 완료 상태를 의미하지 않습니다.
- Response draft는 실제 customer support policy가 아닌 portfolio preview입니다.

## 8. 다음 작업 제안

- 별도 승인 후 Windows build bug intake field를 structured schema로 설계합니다.
- Steam demo playtest에서 확인된 support phrase를 검토해 template을 보완합니다.
- 실제 release 전에는 platform support policy와 privacy 기준을 별도로 정의합니다.
