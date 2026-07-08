# TF-IDF Evaluation Summary

## v0.5.0 TF-IDF Baseline

개요:
이 문서는 `data/raw/wizard_defense_inquiries_raw.csv` 전체 데이터셋을 대상으로 TF-IDF 기반 category classifier를 평가한 v0.5.0 baseline 결과를 기록합니다. 이번 실험은 rule-based classifier를 대체하지 않고, 이후 모델 개선과 비교할 수 있는 간단한 machine learning baseline을 만들기 위한 평가입니다.

실행 명령:

```powershell
python backend/scripts/evaluate_tfidf_classifier.py
```

Dependency:
- `scikit-learn`

설치 명령:

```powershell
pip install -r requirements.txt
```

평가 설정:
- Input: `text`
- Target: `category`
- Feature: `TfidfVectorizer`
- Classifier: `LogisticRegression`
- Evaluation: `StratifiedKFold(n_splits=5, random_state=42)`
- Output CSV: `experiments/tfidf_predictions.csv`

## 전체 결과

- Total samples: 100
- Overall accuracy: 58.00%
- Mismatched examples: 42

## Category별 결과

| category | precision | recall | F1 | support |
| --- | ---: | ---: | ---: | ---: |
| `bug_report` | 0.3750 | 0.2143 | 0.2727 | 14 |
| `feedback_balance` | 0.5556 | 0.4545 | 0.5000 | 11 |
| `gameplay_guide` | 0.5833 | 0.4375 | 0.5000 | 16 |
| `skill_combat` | 0.6316 | 0.8571 | 0.7273 | 14 |
| `tower_progress` | 0.5000 | 0.5833 | 0.5385 | 12 |
| `wizard_acquisition` | 0.6522 | 0.8333 | 0.7317 | 18 |
| `wizard_growth` | 0.6000 | 0.6000 | 0.6000 | 15 |

## Confusion-style Summary

행은 expected category, 열은 predicted category입니다.

| expected \ predicted | `bug_report` | `feedback_balance` | `gameplay_guide` | `skill_combat` | `tower_progress` | `wizard_acquisition` | `wizard_growth` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bug_report` | 3 | 1 | 1 | 3 | 3 | 1 | 2 |
| `feedback_balance` | 1 | 5 | 0 | 2 | 2 | 1 | 0 |
| `gameplay_guide` | 2 | 0 | 7 | 0 | 0 | 4 | 3 |
| `skill_combat` | 0 | 0 | 0 | 12 | 1 | 0 | 1 |
| `tower_progress` | 1 | 2 | 1 | 0 | 7 | 1 | 0 |
| `wizard_acquisition` | 1 | 0 | 1 | 1 | 0 | 15 | 0 |
| `wizard_growth` | 0 | 1 | 2 | 1 | 1 | 1 | 9 |

## Rule-based Baseline과 비교

- Rule-based v0.4.0 accuracy: 60.00%
- TF-IDF v0.5.0 accuracy: 58.00%
- TF-IDF는 `skill_combat`, `feedback_balance`, `wizard_growth`에서 rule-based보다 더 균형 잡힌 결과를 보였지만, `gameplay_guide` recall이 낮아 전체 accuracy는 약간 낮았습니다.
- 데이터셋 크기가 100개로 작기 때문에 cross-validation 결과는 baseline 비교용으로만 해석해야 합니다.

## 해석

TF-IDF baseline은 키워드 규칙 없이도 `skill_combat`, `wizard_acquisition`, `wizard_growth`의 표현 패턴을 어느 정도 학습했습니다. 다만 한국어 문의 문장이 짧고 category 간 공통 단어가 많아 `gameplay_guide`와 `wizard_acquisition`, `bug_report`와 전투/탑 진행 category가 자주 섞였습니다.

이번 결과는 rule-based classifier를 제거하거나 대체하기 위한 근거가 아니라, 이후 TF-IDF feature 조정, 데이터 증강, 또는 LLM 기반 접근을 비교하기 위한 기준점입니다.
