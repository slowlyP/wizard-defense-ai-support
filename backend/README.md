# Backend (플레이스홀더)

설명:
이 폴더는 분류기, 검색 인덱스 연동, 응답 생성 파이프라인을 제공하는 백엔드 구성요소를 포함할 예정입니다. 초기 단계에서는 구조와 예정된 컴포넌트를 문서로 정리합니다.

예정 구성 요소:
- `api/`: 채팅 및 관리용 REST 또는 FastAPI 엔드포인트
- `ingest/`: `knowledge/`와 `data/`를 파싱하여 색인(인덱스)을 생성하는 스크립트
- `models/`: 분류기 및 응답 생성기 래퍼(로컬 우선 구성)

TODO:
- 구현 시 가상환경 설정 및 `requirements.txt` 추가
- 간단한 실행 지침과 테스트 케이스 제공

간단한 테스트 실행 방법:
1. 리포지토리 루트에서 다음 명령으로 분류기 테스트를 실행합니다:

```powershell
python backend/scripts/test_rule_classifier.py
```

2. 출력은 한국어로 된 요약을 표시합니다. 이 스크립트는 v0.3.0-rule-baseline 후보의 룰 기반 분류기를 테스트합니다.

평가 실행 방법:
1. 리포지토리 루트에서 다음 명령으로 전체 데이터셋 평가를 실행합니다:

```powershell
python backend/scripts/evaluate_rule_classifier.py
```

2. 이 스크립트는 `data/raw/wizard_defense_inquiries_raw.csv`를 읽고 `classify_inquiry(text)` 결과를 dataset label과 비교합니다.
3. 콘솔에는 전체 정확도, category별 정확도, 오분류 예시가 출력됩니다.
4. 상세 예측 결과는 `experiments/rule_classifier_predictions.csv`에 저장됩니다.

TF-IDF baseline 평가 실행 방법:
1. 필요한 dependency를 설치합니다:

```powershell
pip install -r requirements.txt
```

2. 리포지토리 루트에서 다음 명령으로 TF-IDF baseline 평가를 실행합니다:

```powershell
python backend/scripts/evaluate_tfidf_classifier.py
```

3. 이 스크립트는 `data/raw/wizard_defense_inquiries_raw.csv`를 읽고 `text`를 입력, `category`를 target으로 사용합니다.
4. `TfidfVectorizer`와 `LogisticRegression`을 `StratifiedKFold`로 평가하며, 콘솔에 accuracy, category별 precision/recall/F1, confusion-style summary, 오분류 예시를 출력합니다.
5. 상세 예측 결과는 `experiments/tfidf_predictions.csv`에 저장됩니다.

Baseline comparison 실행 방법:
1. rule-based 평가와 TF-IDF 평가를 먼저 실행해 다음 파일이 존재하는지 확인합니다:

- `experiments/rule_classifier_predictions.csv`
- `experiments/tfidf_predictions.csv`

2. 리포지토리 루트에서 다음 명령으로 두 baseline 예측을 비교합니다:

```powershell
python backend/scripts/compare_baselines.py
```

3. 이 스크립트는 두 prediction CSV를 `id` 기준으로 비교하고, 전체 정확도, both correct, both wrong, rule-only correct, TF-IDF-only correct, category별 비교 결과를 콘솔에 출력합니다.
4. 상세 비교 결과는 `experiments/baseline_comparison.csv`에 저장됩니다.

Dataset v2 baseline 평가 실행 방법:
1. 리포지토리 루트에서 다음 명령으로 dataset v2 기준 rule-based와 TF-IDF baseline을 함께 평가합니다:

```powershell
python backend/scripts/evaluate_v2_baselines.py
```

2. 이 스크립트는 `data/raw/wizard_defense_inquiries_v2.csv`를 읽고 기존 rule-based classifier와 TF-IDF + `LogisticRegression` baseline을 평가합니다.
3. v1 평가 결과를 덮어쓰지 않고 다음 v2 전용 파일을 생성합니다:

- `experiments/rule_classifier_predictions_v2.csv`
- `experiments/tfidf_predictions_v2.csv`
- `experiments/baseline_comparison_v2.csv`
- `experiments/v2_baseline_evaluation_summary.md`

Rule v2 improvement 평가 실행 방법:
1. 리포지토리 루트에서 다음 명령으로 improved rule-based classifier를 dataset v2에서 평가합니다:

```powershell
python backend/scripts/evaluate_rule_v2_improvement.py
```

2. 이 스크립트는 기존 v2 baseline output을 덮어쓰지 않고 original rule-based, improved rule-based, TF-IDF 결과를 비교합니다.
3. 상세 결과는 다음 파일에 저장됩니다:

- `experiments/rule_v2_improved_predictions.csv`
- `experiments/rule_v2_improvement_comparison.csv`
- `experiments/rule_v2_improvement_summary.md`

Support router demo 실행 방법:
1. 리포지토리 루트에서 다음 명령으로 improved rule classifier 기반 support router prototype demo를 실행합니다:

```powershell
python backend/scripts/run_support_router_demo.py
```

2. 이 스크립트는 약 20개의 한국어 demo 문의를 `predicted_category`, `urgency`, `needs_human`, `routing_reason`, `suggested_response_type`으로 라우팅합니다.
3. 결과는 다음 파일에 저장됩니다:

- `experiments/support_router_demo_outputs.csv`
- `experiments/support_router_summary.md`
