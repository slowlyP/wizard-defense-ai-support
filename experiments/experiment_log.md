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

## EXP-007 V2 Baseline Evaluation (v0.9.0-v2-baseline-evaluation)

- Date: 2026-07-09
- Goal: dataset v2 기준으로 기존 rule-based classifier와 TF-IDF + LogisticRegression baseline을 평가하고 v1 baseline과 비교할 기준을 생성
- Config: Dataset `data/raw/wizard_defense_inquiries_v2.csv`, script `backend/scripts/evaluate_v2_baselines.py`, `TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))`, `LogisticRegression(class_weight="balanced", random_state=42)`, `StratifiedKFold(n_splits=5, random_state=42)`
- Output: `experiments/rule_classifier_predictions_v2.csv`, `experiments/tfidf_predictions_v2.csv`, `experiments/baseline_comparison_v2.csv`, `experiments/v2_baseline_evaluation_summary.md`
- Results: 150개 샘플 기준 rule-based 67/150 correct, accuracy 44.67%; TF-IDF 109/150 correct, accuracy 72.67%
- Comparison results: both correct 51개, both wrong 25개, rule-only correct 16개, TF-IDF-only correct 58개
- Category results: `wizard_acquisition`은 두 baseline 모두 85.00%로 안정적이었고, TF-IDF는 `tower_progress` 95.00%, `skill_combat` 85.00%, `feedback_balance` 84.00%를 기록했습니다. Rule-based는 `bug_report` 20.00%, `feedback_balance` 16.00%, `wizard_growth` 25.00%에서 약했습니다.
- Notes: dataset v1과 dataset v2는 변경하지 않았습니다. 기존 v1 evaluation output은 덮어쓰지 않고 `_v2` output으로 분리했습니다. classifier behavior, backend scripts(신규 v2 평가 스크립트 제외), frontend, Unity game files는 변경하지 않았습니다.

## EXP-008 Rule v2 Improvement (v0.10.0-rule-v2-improvement)

- Date: 2026-07-09
- Goal: dataset v2 기준으로 기존 rule-based classifier의 약한 category를 보강한 별도 improved rule classifier를 평가
- Config: Dataset `data/raw/wizard_defense_inquiries_v2.csv`, improved classifier `backend/app/rule_classifier_v2.py`, script `backend/scripts/evaluate_rule_v2_improvement.py`, original rule prediction `experiments/rule_classifier_predictions_v2.csv`, TF-IDF prediction `experiments/tfidf_predictions_v2.csv`
- Output: `experiments/rule_v2_improved_predictions.csv`, `experiments/rule_v2_improvement_comparison.csv`, `experiments/rule_v2_improvement_summary.md`
- Results: 150개 샘플 기준 original rule-based 67/150 correct, accuracy 44.67%; improved rule-based 141/150 correct, accuracy 94.00%; TF-IDF 109/150 correct, accuracy 72.67%
- Improvement results: improved gains 75개, improved losses 1개입니다.
- Category results: `bug_report` 25/25, `feedback_balance` 24/25, `wizard_growth` 20/20으로 v2 baseline의 약한 category가 크게 개선되었습니다. `gameplay_guide`는 16/20, `skill_combat`은 18/20, `tower_progress`는 19/20, `wizard_acquisition`은 19/20입니다.
- Notes: 기존 `backend/app/rule_classifier.py`와 v1/v2 baseline output은 변경하지 않았습니다. dataset v1, dataset v2, category label, classifier baseline CSV, frontend, Unity game files는 변경하지 않았습니다. improved rule은 refined label policy에 맞춘 투명한 keyword, pattern, priority rule 실험이며, 다음 단계에서는 일반화 가능성을 별도로 검증해야 합니다.

## EXP-009 Support Router Prototype (v0.11.0-support-router-prototype)

- Date: 2026-07-09
- Goal: improved rule classifier 결과를 바탕으로 한국어 플레이어 문의를 지원 라우팅 필드로 변환하는 로컬 prototype을 생성
- Config: Router `backend/app/support_router.py`, classifier `backend/app/rule_classifier_v2.py`, demo script `backend/scripts/run_support_router_demo.py`
- Output: `experiments/support_router_demo_outputs.csv`, `experiments/support_router_summary.md`
- Results: curated demo 20건을 실행했고, `needs_human=true` 7건, 자동 응답 가능 13건으로 라우팅했습니다.
- Policy: `bug_report`는 `bug_triage`, `feedback_balance`는 `balance_feedback_ack`, 나머지 feature category는 각 guide/answer type으로 연결합니다. 기능 category로 예측되어도 미지급, 표시 오류, 생성 실패 같은 실패 신호가 있으면 `bug_triage`와 사람 검토로 올립니다.
- Notes: dataset v1, dataset v2, 기존 baseline CSV, 기존 rule improvement CSV, category label, improved rule classifier behavior, frontend, Unity game files는 변경하지 않았습니다. 이번 단계에서는 web server, FastAPI, 외부 API, helpdesk 연동을 구현하지 않았습니다.

## EXP-010 Response Template Prototype (v0.12.0-response-template-prototype)

- Date: 2026-07-09
- Goal: support router output을 안전한 한국어 response draft template으로 변환하는 로컬 prototype을 생성
- Config: Router `backend/app/support_router.py`, template module `backend/app/response_templates.py`, demo script `backend/scripts/run_response_template_demo.py`
- Output: `experiments/response_template_demo_outputs.csv`, `experiments/response_template_summary.md`
- Results: curated demo 20건을 실행했고, `needs_human=true` 7건, 자동 응답 가능 13건으로 response draft를 생성했습니다.
- Template types: `guide_answer`, `acquisition_answer`, `growth_answer`, `tower_progress_answer`, `skill_combat_answer`, `bug_triage`, `balance_feedback_ack`
- Safety policy: 환불, 보상, 재화 복구, 정확한 patch date, guaranteed fix를 약속하지 않습니다. `needs_human=true`는 검토 또는 추가 정보 요청 문구를 포함하고, `urgency=high`는 재현 정보와 상황 정보를 더 구체적으로 요청합니다.
- Notes: dataset v1, dataset v2, 기존 baseline CSV, 기존 rule improvement CSV, 기존 support router output, category label, support router behavior, frontend, Unity game files는 변경하지 않았습니다. 이번 단계에서는 web server, FastAPI, 외부 API, LLM API, helpdesk 연동을 구현하지 않았습니다.
