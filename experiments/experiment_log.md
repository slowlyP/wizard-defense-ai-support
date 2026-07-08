# Experiment Log

개요:
실험 구성, 하이퍼파라미터, 결과 요약 및 재현 가능한 실행 절차를 기록하는 템플릿입니다. 모델 학습/평가 시에는 실험별로 이 파일 또는 별도 마크다운을 생성해 상세 기록을 남기세요.

예시 항목 형식:
- 날짜: YYYY-MM-DD
- 목적: 실험의 짧은 설명
- 설정: 사용한 데이터셋, 모델, 주요 파라미터
- 결과: 주요 지표(예: accuracy, recall, MRR) 및 관찰 내용

## EXP-001 Rule-based Classifier (v0.3.0-rule-baseline)

- Date: 2026-07-08
- Goal: 키워드 기반 룰 분류기 초기 후보 구현 및 간단한 테스트
- Config: Python script `backend/app/rule_classifier.py`, dataset `data/raw/wizard_defense_inquiries_raw.csv`
- Results: 기본 키워드 규칙으로 샘플 테스트 통과(7/7 사례 출력)
- Notes: 2026-07-08 로컬 테스트에서 발견된 `freeze_or_crash`, `floor_selection_issue`, `skill_targeting` 오분류를 보정했습니다. 이후 현재 게임에 없는 이전 지원 카테고리를 제거하고 `wizard_acquisition`으로 전환했습니다. 마법사 획득, 뽑기권, 중복 획득 문의는 낮은 긴급도의 자동 응답 대상으로 처리합니다. 향후 전체 데이터셋 기준 정밀도/재현율 검증이 필요합니다.

## EXP-002 Rule-based Classifier Evaluation (v0.4.0-evaluation-baseline)

- Date: 2026-07-08
- Goal: 전체 dataset을 기존 rule-based classifier로 평가하여 v0.4.0 baseline을 기록
- Config: Python script `backend/scripts/evaluate_rule_classifier.py`, classifier `backend/app/rule_classifier.py`, dataset `data/raw/wizard_defense_inquiries_raw.csv`
- Output: `experiments/rule_classifier_predictions.csv`
- Results: 100개 샘플 중 60개 category 예측 일치, accuracy 60.00%
- Category results: `wizard_acquisition` 88.89%, `gameplay_guide` 81.25%, `tower_progress` 75.00%, `skill_combat` 71.43%, `wizard_growth` 53.33%, `bug_report` 21.43%, `feedback_balance` 9.09%
- Notes: classifier logic, dataset label, category label은 변경하지 않았습니다. 이번 실험은 TF-IDF 이전의 비교 기준으로 사용하며, 주요 오분류 원인은 공유 키워드와 오류 문맥 우선순위 충돌입니다.

## EXP-003 TF-IDF Baseline (v0.5.0-tfidf-baseline)

- Date: 2026-07-08
- Goal: 전체 dataset에 대해 TF-IDF + LogisticRegression baseline을 평가하고 rule-based baseline과 비교할 기준을 기록
- Config: Python script `backend/scripts/evaluate_tfidf_classifier.py`, dataset `data/raw/wizard_defense_inquiries_raw.csv`, `TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))`, `LogisticRegression(class_weight="balanced", random_state=42)`, `StratifiedKFold(n_splits=5, random_state=42)`
- Dependency: `scikit-learn`
- Output: `experiments/tfidf_predictions.csv`
- Results: 100개 샘플 기준 accuracy 58.00%, mismatched examples 42개
- Category results: `skill_combat` F1 0.7273, `wizard_acquisition` F1 0.7317, `wizard_growth` F1 0.6000, `tower_progress` F1 0.5385, `gameplay_guide` F1 0.5000, `feedback_balance` F1 0.5000, `bug_report` F1 0.2727
- Notes: dataset label, rule-based classifier logic, knowledge 문서는 변경하지 않았습니다. TF-IDF baseline은 rule-based v0.4.0 accuracy 60.00%보다 낮은 58.00%를 기록했으며, 이후 feature 조정 또는 데이터 확충 실험의 비교 기준으로 사용합니다.

