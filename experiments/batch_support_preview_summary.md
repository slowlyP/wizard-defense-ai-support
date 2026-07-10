# Batch Support Preview 요약 (v0.16.0-batch-support-preview)

## 1. 목적

여러 한국어 플레이어 문의를 local CSV에서 읽어 기존 support router와 response template generator에 순서대로 전달하고, 검토 가능한 deterministic batch preview 결과를 하나의 신규 CSV로 저장합니다.

## 2. 입력 데이터

- 기본 입력: `data/raw/wizard_defense_inquiries_v2.csv`
- 입력 text: `text` column
- 식별자: `id` column이 있으면 원래 값을 보존하고, 없으면 source row 기준 sequential id를 사용합니다.
- 기대 category: `expected_category`, `label`, `category` 순서로 존재하는 column을 찾아 `expected_category`로 보존합니다.
- 빈 문자열 또는 whitespace-only `text` row는 처리하지 않고 건너뜁니다. Console의 `Skipped empty rows`에서 그 수를 확인할 수 있습니다.
- `--limit`은 빈 row를 제외하고 output에 기록할 최대 유효 row 수입니다.

## 3. 출력 파일

- 기본 출력: `experiments/batch_support_preview_outputs.csv`
- 기본 실행 결과: 150개 row 처리, 빈 row 0개 건너뜀, `needs_human=true` 57개
- 기존 experiment CSV는 읽거나 덮어쓰지 않습니다.

## 4. 출력 CSV columns

- `id`
- `text`
- `expected_category`
- `predicted_category`
- `urgency`
- `needs_human`
- `suggested_response_type`
- `routing_reason`
- `response_draft`
- `internal_note`

## 5. 처리 흐름

1. UTF-8 CSV를 읽고 `text` column 존재 여부를 확인합니다.
2. 빈 문자열과 whitespace-only row를 건너뜁니다.
3. `route_inquiry(text)`로 category, urgency, human review 여부, response type, routing reason을 생성합니다.
4. `generate_response_template(route)`로 response draft와 internal note를 생성합니다.
5. 입력 식별자와 기대 category를 함께 신규 batch output CSV에 기록합니다.
6. 처리 수, human review 수, category 분포, response type 분포를 console에 출력합니다.

## 6. 검증 결과

- 기본 dataset v2의 150개 row를 모두 처리했습니다.
- `needs_human=true`는 57개입니다.
- Predicted category 분포는 `bug_report` 25개, `feedback_balance` 24개, `gameplay_guide` 18개, `skill_combat` 19개, `tower_progress` 21개, `wizard_acquisition` 21개, `wizard_growth` 22개입니다.
- Response type 분포는 `acquisition_answer` 21개, `balance_feedback_ack` 24개, `bug_triage` 30개, `growth_answer` 22개, `guide_answer` 17개, `skill_combat_answer` 19개, `tower_progress_answer` 17개입니다.
- Category 수와 response type 수가 일대일로 같지 않을 수 있습니다. 기존 router가 feature category에서 오류 신호를 감지하면 `bug_triage`로 올리는 정책을 그대로 적용하기 때문입니다.
- Temporary CSV 기반 unittest에서 output 생성, column, row count, 기대 category 보존, bug/balance human review, 빈 row 건너뛰기, sequential id를 확인했습니다.

## 7. 안전 제한사항

- 외부 API와 LLM API를 호출하지 않습니다.
- 실제 API key가 필요하지 않습니다.
- Gmail, Slack, Discord, 실제 helpdesk와 연동하지 않습니다.
- 환불, 보상, 복구, guaranteed fix, patch date를 약속하지 않는 기존 response template을 그대로 사용합니다.
- dataset v1과 dataset v2를 수정하지 않습니다.

## 8. 한계

- Rule-based classifier 결과가 잘못되면 batch preview에도 그대로 반영됩니다.
- 빈 text row는 결과 CSV에 error row로 남지 않고 건너뛰므로 source별 누락 여부는 skipped count와 입력 검토로 확인해야 합니다.
- 대용량 streaming이나 병렬 처리를 위한 production batch system이 아닙니다.
- Output은 실제 고객에게 발송되는 답변이 아니라 portfolio용 local preview입니다.

## 9. 다음 작업 제안

- 별도 승인을 받은 뒤 mismatch 분석용 aggregate report를 설계합니다.
- 운영 도입 전에는 input schema validation과 row별 error report 정책을 확장합니다.
- 대용량 입력이 필요해질 경우 memory usage와 streaming write 방식을 검토합니다.
