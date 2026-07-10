# Batch Support 분석 보고서 (v0.17.0-batch-analysis-report)

## 1. 목적

기존 batch support preview output을 집계해 분류 성능, 사람 검토 비율, urgency와 response type 분포, 대표 mismatch를 portfolio에서 검토할 수 있도록 정리합니다.

## 2. 입력 파일

- `experiments\batch_support_preview_outputs.csv`
- 입력 CSV는 읽기 전용으로 사용하며 수정하거나 덮어쓰지 않습니다.

## 3. 전체 요약

- 전체 row: 150개
- Expected category 비교 가능 row: 150개
- Match: 141개
- Mismatch: 9개
- Accuracy: 94.00%
- `needs_human=true`: 57개 (38.00%)
- Predicted category 종류: 7개
- Suggested response type 종류: 7개

## 4. Predicted category 분포

- `bug_report`: 25개
- `feedback_balance`: 24개
- `gameplay_guide`: 18개
- `skill_combat`: 19개
- `tower_progress`: 21개
- `wizard_acquisition`: 21개
- `wizard_growth`: 22개

## 5. Expected category 분포

- `bug_report`: 25개
- `feedback_balance`: 25개
- `gameplay_guide`: 20개
- `skill_combat`: 20개
- `tower_progress`: 20개
- `wizard_acquisition`: 20개
- `wizard_growth`: 20개

## 6. Expected vs predicted 결과

- 비교 가능 row: 150개
- 일치: 141개
- 불일치: 9개
- Accuracy: 94.00%

## 7. Category별 accuracy

| expected_category | total | correct | mismatch | accuracy |
| --- | ---: | ---: | ---: | ---: |
| `bug_report` | 25 | 25 | 0 | 100.00% |
| `feedback_balance` | 25 | 24 | 1 | 96.00% |
| `gameplay_guide` | 20 | 16 | 4 | 80.00% |
| `skill_combat` | 20 | 18 | 2 | 90.00% |
| `tower_progress` | 20 | 19 | 1 | 95.00% |
| `wizard_acquisition` | 20 | 19 | 1 | 95.00% |
| `wizard_growth` | 20 | 20 | 0 | 100.00% |

## 8. needs_human 분석

- `false`: 93개
- `true`: 57개

- `needs_human=true` 비율: 38.00%

## 9. Urgency 분포

- `high`: 11개
- `low`: 93개
- `medium`: 46개

## 10. Suggested response type 분포

- `acquisition_answer`: 21개
- `balance_feedback_ack`: 24개
- `bug_triage`: 30개
- `growth_answer`: 22개
- `guide_answer`: 17개
- `skill_combat_answer`: 19개
- `tower_progress_answer`: 17개

## 11. Mismatch sample 요약

- 전체 mismatch: 9개
- Report에 표시한 sample: 9개
- 전체 선택 sample은 `experiments/batch_support_mismatch_samples.csv`에서 확인할 수 있습니다.

| id | text | expected_category | predicted_category |
| --- | --- | --- | --- |
| 9 | 적이 몰려올 때 소환을 먼저 해야 하나요 아니면 연구를 먼저 해야 하나요? | `gameplay_guide` | `wizard_acquisition` |
| 14 | 라운드가 빨라질 때 어떤 기준으로 마법사를 추가 소환해야 하나요? | `gameplay_guide` | `wizard_acquisition` |
| 15 | 보스가 나오는 층에서는 어떤 조합을 준비하는 게 좋나요? | `gameplay_guide` | `tower_progress` |
| 16 | 공격 범위가 겹치는 마법사들을 한곳에 모아도 괜찮나요? | `gameplay_guide` | `skill_combat` |
| 34 | 골드를 써서 마법사를 추가하는 것과 연구하는 것 중 어떤 차이가 있나요? | `wizard_acquisition` | `wizard_growth` |
| 71 | 층별 추천 전투력 같은 기준이 있나요? | `tower_progress` | `gameplay_guide` |
| 84 | 루미엘 축복은 다른 마법사의 공격에도 영향을 주나요? | `skill_combat` | `wizard_growth` |
| 93 | 상태 이상 효과가 보스에게도 똑같이 적용되나요? | `skill_combat` | `tower_progress` |
| 138 | 전설 마법사 없이 진행하는 빌드가 너무 불리한 것 같습니다. | `feedback_balance` | `gameplay_guide` |

## 12. 해석

- Accuracy는 비어 있지 않은 `expected_category`가 있는 row만 기준으로 계산합니다.
- Category별 accuracy는 어떤 expected label에서 rule-based 경계가 약한지 비교하는 지표입니다.
- `needs_human`과 `suggested_response_type`은 category prediction뿐 아니라 기존 router의 오류 신호와 검토 정책도 반영합니다.
- 이 결과는 현재 고정 dataset과 rule에 대한 재현 가능한 local 분석이며 production 성능을 의미하지 않습니다.

## 13. 안전 제한사항

- 외부 API와 LLM API를 호출하지 않습니다.
- 실제 API key, helpdesk, Gmail, Slack, Discord integration을 사용하지 않습니다.
- 입력 batch preview CSV와 dataset을 수정하지 않습니다.

## 14. 한계

- 동일한 dataset v2를 기반으로 만든 batch preview를 분석하므로 독립 holdout 평가가 아닙니다.
- Keyword와 priority rule의 오분류 원인을 자동으로 확정하지 않습니다.
- Accuracy는 category 일치만 측정하며 response draft 품질이나 실제 운영 만족도를 평가하지 않습니다.

## 15. 다음 작업 제안

- 별도 승인 후 mismatch pattern을 category pair 기준으로 세분화합니다.
- 독립 holdout sample이 준비되면 같은 report contract로 재평가합니다.
- 운영 적용 전에는 human-review workload와 response safety를 별도 지표로 정의합니다.
