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

## EXP-004 Baseline Comparison (v0.6.0-baseline-comparison)

- Date: 2026-07-09
- Goal: 동일한 100-row inquiry dataset에서 rule-based baseline과 TF-IDF baseline의 예측 결과를 id 기준으로 비교
- Config: Python script `backend/scripts/compare_baselines.py`, rule prediction `experiments/rule_classifier_predictions.csv`, TF-IDF prediction `experiments/tfidf_predictions.csv`
- Output: `experiments/baseline_comparison.csv`, `experiments/baseline_comparison_summary.md`
- Results: 100개 샘플 기준 rule-based 60/100 correct, accuracy 60.00%; TF-IDF 58/100 correct, accuracy 58.00%
- Comparison results: both correct 40개, both wrong 22개, rule-only correct 20개, TF-IDF-only correct 18개
- Category results: `gameplay_guide`와 `tower_progress`, `wizard_acquisition`은 rule-based가 강했고, `skill_combat`, `feedback_balance`, `wizard_growth`는 TF-IDF가 더 강하거나 개선 가능성을 보였습니다. `bug_report`는 두 방식 모두 21.43%로 공통 취약 영역입니다.
- Notes: dataset label, category label, knowledge 문서, rule-based classifier logic, TF-IDF classifier logic은 변경하지 않았습니다. 이번 실험은 v0.6.0 포트폴리오 baseline comparison으로 기록하며, 다음 data v2 단계는 아직 구현하지 않았습니다.

## EXP-005 Data Quality Review (v0.7.0-data-quality-review)

- Date: 2026-07-09
- Goal: v0.6.0 baseline comparison 결과를 바탕으로 dataset v1의 라벨 경계 문제와 dataset v2 개선 방향을 문서화
- Config: Review sources `experiments/baseline_comparison.csv`, `experiments/baseline_comparison_summary.md`, `experiments/error_analysis.md`, `data/labeling_guide.md`, `data/dataset_card.md`
- Output: `experiments/data_quality_review.md`
- Results: `bug_report`, `feedback_balance`, `wizard_growth`, `gameplay_guide` 경계 사례를 dataset v2 우선 검토 대상으로 정리했습니다.
- Policy updates: `bug_report` vs feature category, `feedback_balance` vs `skill_combat`, `feedback_balance` vs `tower_progress`, `wizard_growth` vs `wizard_acquisition`, `gameplay_guide` vs `wizard_growth`, `gameplay_guide` vs `skill_combat` 경계 규칙을 `data/labeling_guide.md`에 추가했습니다.
- Notes: dataset CSV row, category label, classifier logic, backend scripts, frontend, Unity game files는 변경하지 않았습니다. 이번 실험은 분석과 문서화만 수행하며 dataset v2는 아직 구현하지 않았습니다.

## EXP-006 Dataset v2 Creation (v0.8.0-dataset-v2)

- Date: 2026-07-09
- Goal: v0.7.0 data quality review와 refined labeling policy를 반영해 개선된 150-row inquiry dataset v2를 생성
- Config: Source policy `experiments/data_quality_review.md`, `data/labeling_guide.md`, preserved v1 dataset `data/raw/wizard_defense_inquiries_raw.csv`, Unity validation reference `C:\UnityProjects\Wizard Random Defense`
- Output: `data/raw/wizard_defense_inquiries_v2.csv`
- Results: 총 150개 row를 생성했습니다. 분포는 `gameplay_guide` 20개, `wizard_acquisition` 20개, `wizard_growth` 20개, `tower_progress` 20개, `skill_combat` 20개, `bug_report` 25개, `feedback_balance` 25개입니다.
- Improvements: `bug_report`와 `feedback_balance`의 feature-word boundary case를 늘리고, `wizard_growth` vs `wizard_acquisition`, `gameplay_guide` vs `wizard_growth`, `gameplay_guide` vs `skill_combat` 경계 샘플을 보강했습니다.
- Validation: header 포함 151 lines, data rows 150개, invalid category 없음, empty required fields 없음, duplicated text 없음, unsupported system keyword 없음.
- Notes: v1 dataset은 변경하지 않았습니다. classifier code, backend scripts, frontend, prediction CSV, baseline comparison CSV, Unity game files는 변경하지 않았습니다. 모델 평가는 아직 수행하지 않았습니다.
