# Batch Support 분석 요약 (v0.17.0-batch-analysis-report)

## 1. 목적

기존 batch support preview 결과를 변경하지 않고 읽어 category 정확도, human-review workload, urgency, response type, mismatch를 portfolio용 분석 자료로 정리합니다.

## 2. 입력

- `experiments/batch_support_preview_outputs.csv`
- 150개 row와 `expected_category`, `predicted_category`, `needs_human`, `urgency`, `suggested_response_type`을 분석했습니다.
- 입력 CSV는 읽기 전용으로 사용했으며 수정하거나 덮어쓰지 않았습니다.

## 3. 생성한 출력

- `experiments/batch_support_analysis_report.md`: 전체 분석과 분포, category별 accuracy, mismatch 해석을 포함합니다.
- `experiments/batch_support_category_summary.csv`: expected category별 total, correct, mismatch, accuracy를 기록합니다.
- `experiments/batch_support_mismatch_samples.csv`: 최대 sample 수 제한을 적용한 mismatch 상세를 기록합니다.
- `experiments/batch_support_analysis_summary.md`: 실행 목적과 핵심 결과를 요약합니다.

## 4. 핵심 분석 결과

- 전체 row: 150개
- Expected category 비교 가능 row: 150개
- Match: 141개
- Mismatch: 9개
- Accuracy: 94.00%
- `needs_human=true`: 57개, 38.00%
- Urgency: `high` 11개, `medium` 46개, `low` 93개
- Predicted category: 7종
- Suggested response type: 7종
- Category별 accuracy는 `bug_report`와 `wizard_growth` 100.00%, `feedback_balance` 96.00%, `tower_progress`와 `wizard_acquisition` 95.00%, `skill_combat` 90.00%, `gameplay_guide` 80.00%입니다.

## 5. 검증 결과

- Controlled temporary CSV로 전체 accuracy와 category별 accuracy 계산을 검증했습니다.
- `needs_human=true/false` count를 검증했습니다.
- Markdown report와 두 CSV output 생성을 검증했습니다.
- Category summary와 mismatch CSV의 required column을 검증했습니다.
- `mismatch_limit=1`과 `mismatch_limit=0` 동작을 검증했습니다.
- 전체 test suite, `py_compile`, `git diff --check`, deterministic output 검증을 수행했습니다.

## 6. 변경하지 않은 항목

- FastAPI와 schema behavior
- Support router와 response template behavior
- Batch support preview script와 test
- `experiments/batch_support_preview_outputs.csv`
- Dataset v1과 dataset v2
- 기존 experiment CSV
- Unity game repository file

## 7. 한계

- Dataset v2 기반 batch preview를 다시 분석하므로 independent holdout 평가가 아닙니다.
- Category accuracy만 계산하며 response draft의 자연스러움이나 실제 고객 만족도를 평가하지 않습니다.
- Mismatch의 근본 원인은 자동 확정하지 않고 검토용 sample만 제공합니다.

## 8. 다음 작업 제안

- 별도 승인 후 expected-predicted category pair별 confusion summary를 설계합니다.
- 독립 holdout inquiry가 준비되면 동일한 report format으로 비교합니다.
- 실제 운영 전에는 human-review workload와 response safety 지표를 별도로 정의합니다.
