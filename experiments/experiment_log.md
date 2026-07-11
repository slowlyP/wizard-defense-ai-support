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

## EXP-011 Router Test Suite (v0.13.0-router-test-suite)

- Date: 2026-07-09
- Goal: support router와 response template prototype의 안전하고 일관된 output을 보장하는 local regression test suite를 추가
- Config: `unittest`, tests `backend/tests/test_support_router.py`, `backend/tests/test_response_templates.py`, `backend/tests/test_router_template_integration.py`, optional runner `backend/scripts/run_local_tests.py`
- Output: `experiments/router_test_summary.md`
- Results: `python -m unittest discover backend/tests` 기준 13개 테스트가 통과했습니다.
- Coverage: category별 `suggested_response_type`, `needs_human=true` 처리, `bug_triage`와 `balance_feedback_ack`의 안전 문구 제한, router -> template integration output field를 확인합니다.
- Notes: dataset v1, dataset v2, 기존 baseline CSV, router/template demo CSV, category label, support router behavior, response template behavior, frontend, Unity game files는 변경하지 않았습니다. 외부 API와 LLM API를 사용하지 않았습니다.

## EXP-012 FastAPI Local Prototype (v0.14.0-fastapi-local-prototype)

- 날짜: 2026-07-10
- 목적: 기존 support router와 response template generator를 local FastAPI endpoint로 연결하고 portfolio에서 재현 가능한 preview flow를 제공
- 구성: API `backend/app/api.py`, schema `backend/app/api_schemas.py`, in-process smoke test `backend/scripts/run_api_smoke_test.py`, unittest `backend/tests/test_api_local.py`
- 출력: `experiments/api_local_smoke_test_outputs.csv`, `experiments/api_local_summary.md`
- 결과: `GET /health`와 `POST /support/preview`를 구현하고 7개 category 대표 한국어 문의를 local in-process client로 검증했습니다. Bug 및 balance 사례는 기존 router 정책에 따라 `needs_human=true`를 유지합니다.
- 참고: support router와 response template behavior, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았습니다. 외부 API, LLM API, 실제 helpdesk integration을 사용하지 않습니다.

## EXP-013 API Contract Documentation (v0.15.0-api-contract-docs)

- 날짜: 2026-07-10
- 목적: FastAPI local prototype의 endpoint, request/response schema, enum value, error behavior, 안전 제한사항과 재현 가능한 사용 방법을 문서화
- 구성: Contract `docs/api_contract.md`, usage guide `docs/local_api_usage.md`, summary `experiments/api_contract_summary.md`
- 결과: `GET /health`와 `POST /support/preview`의 실제 구현 기준 계약, PowerShell 호출 예시, HTTP 422 입력 오류, local 실행 및 troubleshooting 절차를 한국어로 정리했습니다.
- 참고: API, router, response template, test behavior와 dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았습니다. 외부 API와 LLM API를 사용하지 않았습니다.

## EXP-014 Batch Support Preview (v0.16.0-batch-support-preview)

- 날짜: 2026-07-10
- 목적: 여러 한국어 플레이어 문의를 CSV에서 읽어 기존 support router와 response template flow로 처리하는 local batch preview 제공
- 구성: Script `backend/scripts/run_batch_support_preview.py`, unittest `backend/tests/test_batch_support_preview.py`, 기본 입력 `data/raw/wizard_defense_inquiries_v2.csv`
- 출력: `experiments/batch_support_preview_outputs.csv`, `experiments/batch_support_preview_summary.md`
- 결과: Dataset v2의 150개 row를 처리했고 `needs_human=true` 57개를 기록했습니다. Predicted category 7종과 response type 7종의 분포를 console과 summary에 기록했습니다.
- 참고: 빈 문자열과 whitespace-only `text` row는 안전하게 건너뜁니다. API, router, response template behavior, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았으며 외부 API와 LLM API를 사용하지 않았습니다.

## EXP-015 Batch Support Analysis Report (v0.17.0-batch-analysis-report)

- 날짜: 2026-07-10
- 목적: 기존 batch support preview output을 읽기 전용으로 분석해 portfolio용 category accuracy, human-review, urgency, response type, mismatch report 생성
- 구성: Script `backend/scripts/analyze_batch_support_preview.py`, unittest `backend/tests/test_batch_support_analysis.py`, input `experiments/batch_support_preview_outputs.csv`
- 출력: `experiments/batch_support_analysis_report.md`, `experiments/batch_support_category_summary.csv`, `experiments/batch_support_mismatch_samples.csv`, `experiments/batch_support_analysis_summary.md`
- 결과: 150개 중 141개 category가 일치해 accuracy 94.00%를 기록했고 mismatch 9개, `needs_human=true` 57개와 7개 predicted category 및 7개 response type 분포를 확인했습니다.
- 참고: Accuracy는 비어 있지 않은 `expected_category` row만 대상으로 계산합니다. API, router, response template, batch preview behavior, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았고 외부 API와 LLM API를 사용하지 않았습니다.

## EXP-016 AWS EC2 Deployment Documentation (v0.18.0-aws-ec2-deployment-docs)

- 날짜: 2026-07-10
- 목적: FastAPI support preview prototype의 AWS EC2 수동 배포와 browser verification 절차를 portfolio용 한국어 문서로 정리
- 구성: Deployment guide `docs/aws_ec2_deployment.md`, browser verification `docs/aws_ec2_browser_verification.md`, summary `experiments/aws_ec2_deployment_summary.md`
- 결과: `Ubuntu Server 24.04 LTS`, `t3.micro`, `My IP` 제한 Security group에서 repository clone, venv, test, Uvicorn 실행과 `GET /health`, `GET /docs`, `POST /support/preview` 검증 절차를 기록했습니다.
- 참고: 실제 EC2 public IP, AWS account ID, credential, secret, private key, `.pem` file은 기록하지 않았습니다. API, router, response template, dataset, 기존 experiment output, Unity game files는 변경하지 않았고 외부 API와 LLM API를 호출하지 않았습니다.

## EXP-017 Steam Support Response Alignment (v0.19.0-steam-support-response-alignment)

- 날짜: 2026-07-10
- 목적: 한국어 support response template을 PC mouse play, Windows build, Steam demo 방향과 fantasy tower defense 문맥에 맞게 정렬
- 구성: Template `backend/app/response_templates.py`, demo `backend/scripts/run_response_template_demo.py`, tests `backend/tests/test_response_templates.py`, `backend/tests/test_router_template_integration.py`
- 출력: `experiments/steam_response_template_demo_outputs.csv`, `experiments/steam_response_alignment_summary.md`
- 결과: 7개 category별 response를 생성했고 `gameplay_guide`의 mouse drag 안내, bug triage의 Windows/Steam demo build와 PC resolution 확인, balance feedback의 Steam demo/PC playtest 검토 문구를 반영했습니다.
- 참고: Router category/urgency/`needs_human` behavior와 FastAPI endpoint/field contract는 변경하지 않았습니다. Dataset v1/v2, 기존 experiment CSV, Unity game files를 변경하지 않았고 외부 API와 LLM API를 사용하지 않았습니다.

## EXP-018 React Support Preview Frontend (v0.20.0-react-support-preview-frontend)

- 날짜: 2026-07-10
- 목적: FastAPI Swagger `/docs`를 대신하는 한국어 user-facing support preview browser UI 제공
- 구성: Vite + React, entry `frontend/src/main.jsx`, UI `frontend/src/App.jsx`, style `frontend/src/styles.css`, API `POST /support/preview`
- 결과: Korean inquiry form, 4개 example chip, loading/error state, Korean-labeled result card와 original enum display를 구현했습니다. CSS-only dark purple/navy, gold, rune, magic book, tower motif를 적용했습니다.
- Backend 변경: Vite local dev를 위해 `backend/app/api.py`에 `http://localhost:5173`, `http://127.0.0.1:5173`만 허용하는 minimal CORS middleware를 추가했습니다. Endpoint와 response schema는 변경하지 않았습니다.
- 참고: Router, response template, API schema, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았습니다. 외부 API, LLM API, Steamworks, authentication, payment, account recovery, helpdesk integration을 추가하지 않았습니다.

## EXP-019 Frontend I18n Language Toggle (v0.21.0-frontend-i18n-language-toggle)

- 날짜: 2026-07-10
- 목적: React support preview UI와 deterministic response draft/internal note에 Korean/English 선택 기능 제공
- 구성: Frontend copy dictionary와 `localStorage`, optional API request field `language`, Korean/English response template
- API 호환성: `POST /support/preview`와 response field 8개를 유지하며 `language` 생략 시 `ko`를 적용합니다. Allowed value는 `ko`, `en`입니다.
- 결과: Title, form, example, loading/error, result label, enum friendly label, portfolio note를 선택 언어로 전환하고 English bug/balance safety response를 추가했습니다.
- 참고: Support router category/urgency/`needs_human` behavior, dataset v1/v2, 기존 experiment CSV, Unity game files를 변경하지 않았습니다. 외부 translation API, LLM API, Steamworks, account/payment/ticket integration을 사용하지 않았습니다.

## EXP-020 Production Deployment Hardening (v0.22.0-production-deployment-hardening)

Purpose: Prepare a production-style EC2 deployment path for the React + FastAPI support preview tool.

Changes:

- Added same-origin frontend API base handling for production builds with `VITE_API_BASE_URL=`.
- Added Nginx static hosting and reverse proxy example config.
- Added systemd FastAPI service example.
- Added production hardening documentation and deployment troubleshooting notes.

Validation plan:

- `python -m unittest discover backend/tests`
- `python backend/scripts/run_api_smoke_test.py`
- `python -m py_compile backend/app/api.py`
- `python -m py_compile backend/app/api_schemas.py`
- `python -m py_compile backend/app/response_templates.py`
- `npm install`
- `npm run build`
- `git diff --check`

Notes:

- No Unity repository files are modified.
- No support router behavior, response template behavior, endpoint path, response field name, or dataset file is intentionally changed.
- No HTTPS, domain, auth, real data, Steamworks, payment, account recovery, or external helpdesk integration is added.

## EXP-021 Production Deployment Verification (v0.23.0-production-deployment-verification)

- 날짜: 2026-07-10
- 목적: v0.22.0 production deployment hardening 절차를 실제 EC2에 적용한 뒤 Nginx, systemd, React production build, Security Group cleanup 결과를 문서화
- 구성: `docs/production_deployment_verification.md`, `docs/security_group_cleanup_verification.md`, `experiments/production_deployment_verification_summary.md`
- 검증 결과: Nginx는 port 80에서 React production build를 serving했고, FastAPI는 systemd service로 `127.0.0.1:8000`에서 active/running 상태였습니다. `/support/preview`, `/health`, `/docs`, `/openapi.json` reverse proxy 구조가 확인되었습니다.
- Browser 결과: `http://EC2_PUBLIC_IP`에서 React UI가 `:5173` 없이 열렸고, Korean / English toggle과 inquiry submission이 동작했습니다. 이전 `5173 -> 8000` CORS preflight issue는 발생하지 않았습니다.
- Security Group 결과: local PowerShell port verification 기준 `80`은 true, `5173`과 `8000`은 false로 확인되어 개발용 public port가 제거되었습니다.
- 참고: 실제 EC2 public IP, AWS account ID, `.pem` path, private key, AWS credential은 기록하지 않았습니다. API endpoint path, response field name, support router behavior, response template behavior, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았습니다.
## EXP-022 Production Operations Runbook (v0.24.0-production-operations-runbook)

- 날짜: 2026-07-10
- 목적: v0.23.0에서 검증된 EC2 production-style 배포를 운영자가 상태 확인, 업데이트, rollback, 장애 대응할 수 있도록 한국어 운영 runbook으로 정리
- 구성: `docs/production_operations_runbook.md`, `docs/deployment_update_and_rollback.md`, `docs/incident_troubleshooting_checklist.md`, `experiments/production_operations_runbook_summary.md`
- 결과: Nginx port 80, React production build, FastAPI systemd service, `127.0.0.1:8000`, same-origin `/support/preview` 구조를 기준으로 운영 명령, 로그 확인, 재배포, rollback, 장애 checklist를 추가했습니다.
- 참고: API endpoint path, response field name, support router behavior, response template behavior, dataset v1/v2, 기존 experiment CSV, Unity game files는 변경하지 않았습니다. 실제 EC2 public IP, AWS account ID, SSH 개인키 경로, private key, AWS credential은 기록하지 않았습니다.

## EXP-023 Security and Access Control Plan (v0.25.0-security-and-access-control-plan)

- 날짜: 2026-07-10
- 목적: EC2 production-style 배포를 production-ready에 더 가깝게 다루기 전에 필요한 보안, 접근 제어, 개인정보, logging 계획을 한국어 문서로 정리
- 구성: `docs/security_and_access_control_plan.md`, `docs/privacy_and_logging_guidelines.md`, `docs/production_security_checklist.md`, `experiments/security_access_control_plan_summary.md`
- 결과: HTTPS/domain/auth/database/ticket storage/Steamworks 미구현 상태를 명확히 기록하고, public demo mode와 future admin/internal mode, `/support/preview` abuse prevention, `/docs` 공개 범위, secret management, privacy/logging checklist를 정리했습니다.
- 참고: HTTPS, authentication, authorization, database, user account, Steamworks, payment, account recovery, helpdesk integration은 구현하지 않았습니다. API endpoint path, response field name, support router behavior, response template behavior, dataset v1/v2, 기존 experiment CSV, Unity game files도 변경하지 않았습니다. 실제 EC2 public IP, AWS account ID, `.pem` path, private key, AWS credential은 기록하지 않았습니다.

## EXP-024 Support Question Coverage Expansion (v0.26.0-support-question-coverage-expansion)

- 날짜: 2026-07-11
- 목적: common player question에 대한 deterministic support response coverage를 확장하고, 현재 시스템이 외부 LLM API를 사용하지 않는 rule-based baseline임을 명확히 정리
- 구성: `backend/app/support_knowledge.py`, `backend/tests/test_support_knowledge.py`, `backend/tests/test_support_knowledge_api_integration.py`, `experiments/support_question_coverage_demo_outputs.csv`, `experiments/support_question_coverage_expansion_summary.md`
- 결과: wizard elements, legendary wizards, individual legendary wizard, fusion, resonance, tower, boss, PC controls, fullscreen/resolution, reward loss, payment/refund safe review 질문에 대한 한국어/영어 deterministic response draft를 보강했습니다.
- 참고: 외부 API, LLM API, API key, authentication, database, Steamworks, payment/refund/account/helpdesk integration은 추가하지 않았습니다. Dataset v1/v2와 기존 experiment CSV는 덮어쓰지 않았고 Unity game repository는 수정하지 않았습니다.

## EXP-025 LLM/RAG Readiness Plan (v0.27.0-llm-rag-readiness-plan)

- 날짜: 2026-07-11
- 목적: 외부 LLM API를 사용하지 않는 현재 rule-based deterministic baseline을 기준으로 future retrieval-only 및 optional LLM/RAG 확장 계획을 문서화
- 구성: `docs/llm_rag_readiness_plan.md`, `docs/rag_knowledge_base_design.md`, `docs/prompt_and_guardrail_design.md`, `docs/llm_rag_evaluation_plan.md`, `docs/baseline_vs_llm_rag_comparison.md`, `docs/support_knowledge_base_seed.md`, `experiments/llm_rag_readiness_plan_summary.md`
- 결과: proposed hybrid architecture, knowledge source/chunk/metadata, bilingual prompt, refund/compensation/PII/injection guardrail, deterministic fallback, baseline comparison metrics와 phased implementation plan을 정리했습니다.
- 참고: 이 실험은 planning/documentation only입니다. LLM/RAG, 외부 API, API key, embedding/vector DB dependency, authentication, database, Steamworks, payment/account/helpdesk integration을 구현하지 않았습니다. API 계약, backend/frontend 동작, dataset v1/v2, 기존 experiment CSV와 Unity game repository는 변경하지 않았습니다.

## EXP-026 RAG Retrieval Baseline Prototype (v0.28.0-rag-retrieval-baseline-prototype)

- 날짜: 2026-07-11
- 목적: 향후 RAG 평가를 위해 외부 LLM API, embedding, vector DB 없이 동작하는 bilingual deterministic retrieval baseline 구현
- 구성: `backend/app/rag_knowledge_base.py`, `backend/app/rag_retriever.py`, response-template/API integration, retrieval unittest, `backend/scripts/run_rag_retrieval_demo.py`
- 출력: `experiments/rag_retrieval_baseline_demo_outputs.csv`, `experiments/rag_retrieval_baseline_summary.md`
- 결과: wizard/legendary/fusion/resonance/tower/PC/display/safety topic의 local structured chunk를 token, keyword, topic 점수로 검색하고 stable `top_k` ordering을 제공합니다. Sensitive reward/payment/refund chunk는 `requires_human_review=true`로 기존 API routing을 강화합니다.
- 참고: 외부 API, LLM API, API key, embedding/vector DB 또는 새 dependency를 추가하지 않았습니다. 기존 endpoint와 response field, dataset v1/v2, 이전 experiment CSV와 Unity repository는 변경하지 않았습니다.
