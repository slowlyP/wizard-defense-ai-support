# V2 Baseline Evaluation Summary (v0.9.0-v2-baseline-evaluation)

## 목적

이 문서는 `data/raw/wizard_defense_inquiries_v2.csv`에 대해 기존 rule-based classifier와 TF-IDF + LogisticRegression baseline을 평가한 결과를 기록합니다. dataset v2는 v0.7.0 data quality review 이후 라벨 경계와 약한 category를 보강하기 위해 생성되었으며, 이번 평가는 v2가 baseline 성능과 오분류 구조에 어떤 변화를 주었는지 확인하기 위한 기준선입니다.

## 사용한 dataset

- Dataset: `data/raw/wizard_defense_inquiries_v2.csv`
- Total samples: 150
- Rule-based output: `experiments/rule_classifier_predictions_v2.csv`
- TF-IDF output: `experiments/tfidf_predictions_v2.csv`
- Comparison output: `experiments/baseline_comparison_v2.csv`
- Evaluation script: `backend/scripts/evaluate_v2_baselines.py`

## 전체 비교 결과

- Rule-based correct: 67 / 150
- Rule-based accuracy: 44.67%
- TF-IDF correct: 109 / 150
- TF-IDF accuracy: 72.67%
- Both correct: 51
- Both wrong: 25
- Rule-only correct: 16
- TF-IDF-only correct: 58

## category별 비교표

| category | total | rule-based correct | rule-based accuracy | TF-IDF correct | TF-IDF accuracy | both correct | both wrong | rule-only correct | TF-IDF-only correct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bug_report` | 25 | 5 | 20.00% | 16 | 64.00% | 3 | 7 | 2 | 13 |
| `feedback_balance` | 25 | 4 | 16.00% | 21 | 84.00% | 4 | 4 | 0 | 17 |
| `gameplay_guide` | 20 | 12 | 60.00% | 6 | 30.00% | 3 | 5 | 9 | 3 |
| `skill_combat` | 20 | 11 | 55.00% | 17 | 85.00% | 10 | 2 | 1 | 7 |
| `tower_progress` | 20 | 13 | 65.00% | 19 | 95.00% | 12 | 0 | 1 | 7 |
| `wizard_acquisition` | 20 | 17 | 85.00% | 17 | 85.00% | 15 | 1 | 2 | 2 |
| `wizard_growth` | 20 | 5 | 25.00% | 13 | 65.00% | 4 | 6 | 1 | 9 |

## v1 대비 해석

- v1 baseline은 100 samples 기준 rule-based 60.00%, TF-IDF 58.00%, both correct 40, both wrong 22였습니다.
- v2 baseline은 150 samples 기준 rule-based 44.67%, TF-IDF 72.67%, both correct 51, both wrong 25입니다.
- Rule-based accuracy 변화: -15.33%
- TF-IDF accuracy 변화: 14.67%
- v2는 더 많은 `bug_report`와 `feedback_balance` 경계 사례를 포함하므로, 단순 정확도만으로 v1보다 쉬운 dataset이라고 해석하면 안 됩니다. v2 평가는 보강된 ambiguous case에서 두 baseline이 어떤 약점을 유지하는지 확인하는 목적이 더 큽니다.

## v2에서 개선된 점

- `bug_report`와 `feedback_balance` 샘플 수를 늘려 v1에서 약했던 category를 더 안정적으로 관찰할 수 있게 되었습니다.
- 기능 단어가 포함된 오류 문의와 평가 문의를 분리해 라벨 정책 검증에 더 적합한 샘플을 포함했습니다.
- `wizard_growth` vs `wizard_acquisition`, `gameplay_guide` vs `wizard_growth`, `gameplay_guide` vs `skill_combat` 경계 사례가 늘어났습니다.
- v1 evaluation output을 덮어쓰지 않고 `_v2` output으로 분리해 비교 가능성을 보존했습니다.

## 아직 남은 약점

- Rule-based classifier는 기존 keyword rule을 그대로 사용하므로 v2에서 새로 보강된 표현을 충분히 반영하지 못할 수 있습니다.
- TF-IDF baseline은 char n-gram 기반이므로 기능 단어와 의도 단어가 함께 있는 문장에서 핵심 의도를 안정적으로 분리하기 어렵습니다.
- `bug_report`와 `feedback_balance`는 feature word가 함께 등장할 때 여전히 다른 category와 충돌할 가능성이 큽니다.
- 이번 평가는 baseline evaluation이며 classifier logic 개선은 포함하지 않았습니다.

## 다음 작업 제안

- `baseline_comparison_v2.csv`에서 both wrong과 model-only correct 샘플을 분리해 v2 error analysis를 확장합니다.
- rule-based classifier는 v2 결과를 참고해 keyword 우선순위와 경계 규칙 개선 후보를 별도 실험으로 검토합니다.
- TF-IDF baseline은 feature engineering 또는 더 큰 train/evaluation split 전략을 별도 실험으로 검토합니다.
- dataset v2 기준 검색/응답 pipeline 평가를 진행하기 전, classifier baseline의 실패 유형을 먼저 문서화합니다.
