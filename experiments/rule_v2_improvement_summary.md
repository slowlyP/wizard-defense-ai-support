# Rule V2 Improvement Summary (v0.10.0-rule-v2-improvement)

## 목적

이 문서는 `data/raw/wizard_defense_inquiries_v2.csv` 기준으로 original rule-based classifier와 별도 improved rule-based classifier를 비교한 실험 결과를 기록합니다. 원본 rule classifier는 재현 가능하도록 유지했고, 개선 규칙은 `backend/app/rule_classifier_v2.py`에 별도 구현했습니다.

## 사용한 dataset

- Dataset: `data/raw/wizard_defense_inquiries_v2.csv`
- Total samples: 150
- Original rule prediction: `experiments/rule_classifier_predictions_v2.csv`
- Improved rule prediction: `experiments/rule_v2_improved_predictions.csv`
- TF-IDF prediction: `experiments/tfidf_predictions_v2.csv`
- Comparison output: `experiments/rule_v2_improvement_comparison.csv`
- Evaluation script: `backend/scripts/evaluate_rule_v2_improvement.py`

## 전체 결과

- Original rule-based correct: 67 / 150
- Original rule-based accuracy: 44.67%
- Improved rule-based correct: 141 / 150
- Improved rule-based accuracy: 94.00%
- TF-IDF correct: 109 / 150
- TF-IDF accuracy: 72.67%
- Improved rule gain/loss: +49.33%p
- Improved gain rows: 75
- Improved loss rows: 1

## category별 original vs improved 비교표

| category | total | original correct | original accuracy | improved correct | improved accuracy | TF-IDF correct | TF-IDF accuracy | gain | loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bug_report` | 25 | 5 | 20.00% | 25 | 100.00% | 16 | 64.00% | 20 | 0 |
| `feedback_balance` | 25 | 4 | 16.00% | 24 | 96.00% | 21 | 84.00% | 20 | 0 |
| `gameplay_guide` | 20 | 12 | 60.00% | 16 | 80.00% | 6 | 30.00% | 4 | 0 |
| `skill_combat` | 20 | 11 | 55.00% | 18 | 90.00% | 17 | 85.00% | 7 | 0 |
| `tower_progress` | 20 | 13 | 65.00% | 19 | 95.00% | 19 | 95.00% | 7 | 1 |
| `wizard_acquisition` | 20 | 17 | 85.00% | 19 | 95.00% | 17 | 85.00% | 2 | 0 |
| `wizard_growth` | 20 | 5 | 25.00% | 20 | 100.00% | 13 | 65.00% | 15 | 0 |

## improved rule이 좋아진 category

- `bug_report`: +20 correct
- `feedback_balance`: +20 correct
- `gameplay_guide`: +4 correct
- `skill_combat`: +7 correct
- `tower_progress`: +6 correct
- `wizard_acquisition`: +2 correct
- `wizard_growth`: +15 correct

## 아직 약한 category

- improved rule 기준 60% 미만 category가 없습니다.

## TF-IDF와의 차이

- TF-IDF accuracy는 72.67%이고 improved rule accuracy는 94.00%입니다.
- TF-IDF 대비 improved rule gap은 +21.33%p입니다.
- Improved rule은 의도 경계가 명확한 키워드와 우선순위를 설명하기 쉽지만, TF-IDF는 v2의 다양한 표현을 더 넓게 포착했습니다.
- v2에서는 improved rule이 TF-IDF보다 높은 accuracy를 기록했지만, 규칙이 dataset v2의 표현 분포에 강하게 맞춰져 있을 수 있으므로 다음 평가에서는 일반화 가능성을 별도로 확인해야 합니다.

## 다음 작업 제안

- `rule_v2_improvement_comparison.csv`에서 `improved_loss` row를 확인해 과도한 priority rule을 줄입니다.
- `bug_report`와 `feedback_balance`는 더 세밀한 hard failure signal과 complaint signal을 분리합니다.
- `gameplay_guide`와 `skill_combat` 경계는 전략 요청과 계산/판정 요청을 더 명확히 나누는 규칙을 추가 검토합니다.
- 다음 실험에서는 rule 개선과 TF-IDF feature engineering을 같은 v2 dataset에서 비교합니다.
