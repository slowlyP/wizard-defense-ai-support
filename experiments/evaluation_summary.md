# Evaluation Summary

## v0.4.0 Rule-based Classifier Evaluation

개요:
이 문서는 `data/raw/wizard_defense_inquiries_raw.csv` 전체 데이터셋을 기존 `classify_inquiry(text)` 함수로 평가한 v0.4.0 baseline 결과를 기록합니다. 이번 평가는 모델 학습이나 classifier logic 변경 없이, 현재 rule-based classifier의 category 예측 결과를 dataset label과 비교했습니다.

실행 명령:

```powershell
python backend/scripts/evaluate_rule_classifier.py
```

평가 산출물:
- Console summary: 전체 정확도, category별 정확도, 오분류 예시
- Prediction CSV: `experiments/rule_classifier_predictions.csv`

## 전체 결과

- Total samples: 100
- Correct samples: 60
- Accuracy: 60.00%
- Mismatched examples: 40

## Category별 결과

| category | total | correct | accuracy |
| --- | ---: | ---: | ---: |
| `bug_report` | 14 | 3 | 21.43% |
| `feedback_balance` | 11 | 1 | 9.09% |
| `gameplay_guide` | 16 | 13 | 81.25% |
| `skill_combat` | 14 | 10 | 71.43% |
| `tower_progress` | 12 | 9 | 75.00% |
| `wizard_acquisition` | 18 | 16 | 88.89% |
| `wizard_growth` | 15 | 8 | 53.33% |

## 해석

`wizard_acquisition`, `gameplay_guide`, `tower_progress`, `skill_combat`는 baseline 단계에서 상대적으로 높은 정확도를 보였습니다. 반면 `bug_report`와 `feedback_balance`는 문맥보다 단일 키워드 우선순위에 크게 영향을 받아 낮은 정확도를 보였습니다.

주요 실패 패턴:
- `bug_report` 문의가 명확한 오류 표현 없이 배치, 성장, 획득 단어를 포함하면 다른 category로 분류됩니다.
- `feedback_balance` 문의가 확률, 보상, 골드처럼 다른 category와 공유되는 단어를 포함하면 의도 구분이 어렵습니다.
- `wizard_growth` 문의에서 `얻`, `획득`, `경로`, `초보자` 같은 단어가 `wizard_acquisition` 또는 `gameplay_guide`로 끌어갑니다.
- 버그 표현이 포함된 기능 문의는 기능 category보다 `bug_report`로 우선 분류되는 경향이 있습니다.

## 결론

이번 결과는 v0.4.0 evaluation baseline으로 기록합니다. 현재 rule-based classifier는 포트폴리오용 초기 baseline으로는 동작하지만, category 간 공유 키워드와 오류 문맥 처리에서 개선 여지가 큽니다. 다음 단계에서는 classifier logic을 바로 교체하기보다 오분류 유형을 기준으로 rule priority, negative keywords, category별 문맥 키워드 보강 후보를 정리하는 것이 적절합니다.
