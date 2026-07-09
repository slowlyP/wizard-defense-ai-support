# Error Analysis

개요:
분류 및 검색 파이프라인에서 발생하는 주요 실패 유형을 체계적으로 기록하고 개선 방안을 추적하기 위한 템플릿입니다.


섹션 예시:
- 잘못 분류된 의도(Misclassified intents) — 오분류 샘플과 원인 분석
- 검색 불일치(Retrieval mismatches) — 잘못된 문서 반환(오탐/미탐) 사례
- 모델 할루시네이션 및 근거 결여(Model hallucinations) — 근거 없는 응답과 교정 방안

## Rule-based Classifier Error Analysis (v0.3.0-rule-baseline)

작성 지침(한국어):
- 각 오분류 샘플에 대해 원본 텍스트, 예측 라벨, 기대 라벨, 매칭된 키워드, 개선 방안을 기록합니다.
- 자주 누락되는 표현(예: 은유적 표현, 줄임말, 오타)은 키워드 사전에 추가합니다.
- 버그 리포트 관련 샘플은 `needs_human=true`로 표시되어야 하며, 사람 검토 후 처리 절차를 문서화합니다.

템플릿 예시:
- Sample: "문의 텍스트"
- Predicted: `category` / `subcategory` / urgency / needs_human
- Expected: `category` / `subcategory`
- Matched keywords: [...]
- Root cause: (예: 키워드 누락, 중의성 등)
- Fix: (예: 키워드 추가, 규칙 우선순위 변경, 후처리 규칙)

### 2026-07-08 로컬 테스트 보정 기록
- Sample: "게임을 켜면 화면이 멈춰요."
- Predicted: `gameplay_guide` / `unknown` / low / false
- Expected: `bug_report` / `freeze_or_crash` / high / true
- Root cause: `멈춰` 표현이 버그 키워드에 없어서 fallback 분류가 적용됨
- Fix: `멈춰`, `멈춤`, `멈춥니다`, `튕김`, `튕겨`, `먹통`, `진행이 안` 등 버그 키워드를 확장하고 버그 매칭 시 `needs_human=true`로 처리

- Sample: "마법사는 어떻게 획득하나요?"
- Expected: `wizard_acquisition` / `acquisition_guide` / low / false
- Fix: 현재 게임에 없는 이전 지원 카테고리를 제거하고, 마법사 획득·뽑기·티켓·등급·중복 획득 문의를 `wizard_acquisition`으로 분류

- Sample: "1층으로 가려고 했는데 다시 6층으로 돌아가요."
- Expected: `tower_progress` / `floor_selection_issue` / medium / true
- Fix: 층 이동 문맥에서 `다시`, `돌아가`가 함께 매칭되면 `floor_selection_issue`로 처리

- Sample: "번개 빔 스킬이 몬스터한테 안 맞는 것 같아요."
- Expected: `skill_combat` / `skill_targeting` / medium / true
- Fix: 스킬/전투 문맥에서 `안 맞` 같은 실패 패턴이 매칭되면 `skill_targeting`으로 처리

## Rule-based Classifier Error Analysis (v0.4.0-evaluation-baseline)

평가 기준:
- Dataset: `data/raw/wizard_defense_inquiries_raw.csv`
- Script: `backend/scripts/evaluate_rule_classifier.py`
- Output: `experiments/rule_classifier_predictions.csv`
- Total samples: 100
- Correct samples: 60
- Accuracy: 60.00%
- Mismatched examples: 40

Category별 결과:
- `bug_report`: 3/14 correct, 21.43%
- `feedback_balance`: 1/11 correct, 9.09%
- `gameplay_guide`: 13/16 correct, 81.25%
- `skill_combat`: 10/14 correct, 71.43%
- `tower_progress`: 9/12 correct, 75.00%
- `wizard_acquisition`: 16/18 correct, 88.89%
- `wizard_growth`: 8/15 correct, 53.33%

주요 오분류 패턴:
- `bug_report` -> `gameplay_guide`: 오류 표현이 약하고 배치, 클릭, 화면 같은 일반 플레이 단서가 먼저 잡히는 경우가 있습니다.
- `wizard_growth` -> `gameplay_guide`: 성장 문의에 `경로`, `초보자`, 짧은 단어 `성`이 포함되면 gameplay 쪽으로 끌리는 경우가 있습니다.
- `wizard_growth` -> `wizard_acquisition`: 성장 문의에서 `얻`, `획득`이 경험치나 보상 문맥으로 쓰여도 획득 category가 우선됩니다.
- `feedback_balance` -> 다른 category: 확률, 보상, 골드, 강함/약함 같은 balance 단서가 다른 기능 단서와 충돌합니다.
- 기능 문의 -> `bug_report`: `멈춰`, `버그`, `안 돼요` 같은 오류 단어가 포함되면 기능 category보다 bug_report가 우선됩니다.

대표 오분류 예시:
- Sample: "적들이 몰려올 때 어느 타워부터 업그레이드해야 할까요?"
- Predicted: `tower_progress`
- Expected: `gameplay_guide`
- Matched keywords: [`타워`]
- Root cause: `타워` 단어가 층 진행 문맥이 아닌 전략 문맥에서도 사용됩니다.
- Fix 후보: `업그레이드`, `전략`, `어느` 같은 가이드 문맥과 함께 나타날 때 `gameplay_guide` 우선순위를 검토합니다.

- Sample: "마법사 레벨업에 필요한 경험치는 어떻게 얻나요?"
- Predicted: `wizard_acquisition`
- Expected: `wizard_growth`
- Matched keywords: [`얻`]
- Root cause: `얻` 단어가 획득과 성장 재화 문맥을 모두 가리킵니다.
- Fix 후보: `레벨업`, `경험치`, `성장`이 함께 있으면 `wizard_growth`를 우선하는 규칙을 검토합니다.

- Sample: "그래픽이 깨져 보이는 현상이 자주 발생합니다."
- Predicted: `gameplay_guide`
- Expected: `bug_report`
- Matched keywords: []
- Root cause: 버그 category에 그래픽 깨짐, 표시 오류, 발생 같은 표현이 부족해 fallback이 적용됩니다.
- Fix 후보: 표시/그래픽 오류 관련 bug keyword를 추가할지 검토합니다.

- Sample: "마법사 획득 연출이 끝나지 않고 화면이 멈춰요."
- Predicted: `bug_report`
- Expected: `wizard_acquisition`
- Matched keywords: [`멈춰`]
- Root cause: 기능 문맥과 오류 문맥이 함께 있을 때 현재 classifier는 bug_report를 우선합니다.
- Fix 후보: dataset label 정책상 기능 category를 유지할지, 오류가 있으면 bug_report로 재라벨링할지 별도 검토가 필요합니다.

다음 개선 후보:
- 공유 키워드(`얻`, `확률`, `보상`, `타워`, `전설`)의 category별 문맥 규칙을 분리합니다.
- `bug_report`는 기능 단어와 함께 나오는 오류 표현을 별도 subcategory로 추적합니다.
- `feedback_balance`는 `너무`, `약한`, `강한`, `불공평`, `조정` 같은 평가 표현을 더 강하게 반영합니다.
- 다음 단계인 TF-IDF baseline 전에 rule-based baseline의 한계를 그대로 보존해 비교 기준으로 사용합니다.

## TF-IDF Baseline Error Analysis (v0.5.0-tfidf-baseline)

평가 기준:
- Dataset: `data/raw/wizard_defense_inquiries_raw.csv`
- Script: `backend/scripts/evaluate_tfidf_classifier.py`
- Output: `experiments/tfidf_predictions.csv`
- Method: `TfidfVectorizer` + `LogisticRegression`
- Evaluation: `StratifiedKFold(n_splits=5, random_state=42)`
- Total samples: 100
- Accuracy: 58.00%
- Mismatched examples: 42

Category별 결과:
- `bug_report`: precision 0.3750, recall 0.2143, F1 0.2727
- `feedback_balance`: precision 0.5556, recall 0.4545, F1 0.5000
- `gameplay_guide`: precision 0.5833, recall 0.4375, F1 0.5000
- `skill_combat`: precision 0.6316, recall 0.8571, F1 0.7273
- `tower_progress`: precision 0.5000, recall 0.5833, F1 0.5385
- `wizard_acquisition`: precision 0.6522, recall 0.8333, F1 0.7317
- `wizard_growth`: precision 0.6000, recall 0.6000, F1 0.6000

주요 오분류 패턴:
- `gameplay_guide` -> `wizard_acquisition`: 마법사, 속성, 배치 문맥이 함께 있는 일반 가이드 문의가 획득 category로 이동했습니다.
- `gameplay_guide` -> `wizard_growth`: 전설 마법사, 레조넌스, 조합 같은 단어가 가이드 문맥보다 성장 문맥으로 강하게 반영되었습니다.
- `bug_report` -> `skill_combat` 또는 `tower_progress`: 오류 문의가 스킬, 몬스터, 층 같은 기능 단어와 함께 나타나면 기능 category로 분류되었습니다.
- `feedback_balance` -> `skill_combat` 또는 `tower_progress`: 밸런스 문의에 스킬, 층, 스폰 같은 기능 단어가 포함되면 balance 의도가 약해졌습니다.

대표 오분류 예시:
- Sample: "경로 타일에 마법사를 놓을 수 없다고 표시되는데 정확히 어디에 놓아야 하나요?"
- Predicted: `wizard_acquisition`
- Expected: `gameplay_guide`
- Root cause: `마법사`와 배치 표현이 짧은 문장 안에서 획득/보유 계열 표현과 충분히 분리되지 않았습니다.
- Fix 후보: 한국어 형태소 분석 없이 char n-gram만 쓰는 baseline의 한계로 기록하고, category별 데이터 확충 또는 feature 조정을 검토합니다.

- Sample: "전략적으로 바람 마법사를 어떤 위치에 두는 게 좋나요?"
- Predicted: `wizard_acquisition`
- Expected: `gameplay_guide`
- Root cause: 위치/전략 가이드보다 마법사 표현이 더 넓은 획득 category와 연결되었습니다.
- Fix 후보: `위치`, `두는`, `전략`이 포함된 gameplay 예시를 늘립니다.

- Sample: "스킬 레벨업 시 데미지 증가량 계산법 알려주세요."
- Predicted: `wizard_growth`
- Expected: `skill_combat`
- Root cause: `레벨업` 표현이 성장 category와 강하게 연결되었습니다.
- Fix 후보: 스킬 성장/스킬 피해 계산 문의의 label policy를 명확히 하고, `skill_combat` 학습 예시를 늘립니다.

비교 메모:
- TF-IDF v0.5.0 accuracy는 58.00%로 rule-based v0.4.0 accuracy 60.00%보다 낮습니다.
- TF-IDF는 `feedback_balance`와 `wizard_growth`에서 rule-based보다 개선 가능성을 보였지만, `gameplay_guide`와 `bug_report` recall이 낮았습니다.
- 이 결과는 rule-based classifier를 제거하기 위한 근거가 아니라, 다음 실험에서 feature engineering 또는 데이터 확충 효과를 비교하기 위한 baseline입니다.

## Baseline Comparison Findings (v0.6.0-baseline-comparison)

평가 기준:
- Dataset: `data/raw/wizard_defense_inquiries_raw.csv`
- Rule-based prediction: `experiments/rule_classifier_predictions.csv`
- TF-IDF prediction: `experiments/tfidf_predictions.csv`
- Script: `backend/scripts/compare_baselines.py`
- Output: `experiments/baseline_comparison.csv`
- Summary: `experiments/baseline_comparison_summary.md`
- Total samples: 100
- Rule-based accuracy: 60.00% (60/100)
- TF-IDF accuracy: 58.00% (58/100)
- Both correct: 40
- Both wrong: 22
- Rule-only correct: 20
- TF-IDF-only correct: 18

Category별 비교 요약:
- `bug_report`: 두 방식 모두 3/14 correct, both wrong 8개로 가장 큰 공통 취약 영역입니다.
- `feedback_balance`: rule-based 1/11, TF-IDF 5/11로 TF-IDF가 더 강하지만 both wrong 6개가 남아 있습니다.
- `gameplay_guide`: rule-based 13/16, TF-IDF 7/16으로 rule-based가 명확히 강합니다.
- `skill_combat`: rule-based 10/14, TF-IDF 12/14로 TF-IDF가 가장 안정적입니다.
- `tower_progress`: rule-based 9/12, TF-IDF 7/12로 rule-based가 더 강합니다.
- `wizard_acquisition`: rule-based 16/18, TF-IDF 15/18로 두 방식 모두 강합니다.
- `wizard_growth`: rule-based 8/15, TF-IDF 9/15로 TF-IDF가 약간 앞섭니다.

공통 오분류 패턴:
- `bug_report` 문의에서 그래픽 깨짐, 프레임 드랍, 사운드 끊김처럼 오류 표현이 일반 기능 단서보다 약하게 잡힙니다.
- `feedback_balance` 문의에서 타워, 전설 마법사, 스킬 같은 기능 단어가 밸런스 평가 표현보다 강하게 작동합니다.
- `wizard_growth`와 `wizard_acquisition` 사이에서 `얻`, `획득`, `보상`, `경험치` 표현이 중의적으로 작동합니다.
- 설명 요청인 `gameplay_guide`가 레조넌스, 조합, 전설 마법사 같은 내부 시스템 단어 때문에 성장 또는 스킬 category로 이동합니다.
- 일부 기능 라벨 샘플은 오류 표현을 포함해 classifier 입장에서는 `bug_report`로 보이는 경계 사례가 있습니다.

개선 후보:
- 이번 단계에서는 dataset label, category label, classifier logic을 변경하지 않고 비교 결과만 baseline으로 고정합니다.
- 다음 실험에서는 rule-only correct와 TF-IDF-only correct 샘플을 분리해 rule 보강 후보와 feature engineering 후보를 따로 관리합니다.
- `bug_report`와 `feedback_balance`는 기능 단서보다 의도 단서를 우선 판단할 수 있는 별도 실험 대상으로 분리합니다.

## Data Quality Review Findings (v0.7.0-data-quality-review)

검토 기준:
- Source: `experiments/baseline_comparison.csv`
- Summary: `experiments/baseline_comparison_summary.md`
- Review document: `experiments/data_quality_review.md`
- Rule-based accuracy: 60.00%
- TF-IDF accuracy: 58.00%
- Both correct: 40
- Both wrong: 22
- Rule-only correct: 20
- TF-IDF-only correct: 18

약한 category:
- `bug_report`: 두 baseline 모두 3/14 correct이며, both wrong 8개가 발생했습니다. 오류 표현이 기능 단어보다 약하게 잡히는 것이 핵심 문제입니다.
- `feedback_balance`: rule-based 1/11, TF-IDF 5/11로 낮습니다. 비용, 확률, 스킬 조합, 성장 비용 같은 기능 단어와 밸런스 평가 표현이 충돌합니다.
- `wizard_growth`: `얻`, `획득`, `보상`, `경험치` 표현 때문에 `wizard_acquisition` 또는 `tower_progress`와 혼동됩니다.
- `gameplay_guide` boundary: 레조넌스, 조합, 전설 마법사 같은 시스템 단어가 포함된 설명 요청이 `wizard_growth` 또는 `skill_combat`으로 이동합니다.

라벨 정책 개선 요약:
- 실제 동작 실패, 진행 불가, 보상/재료 손실, UI 멈춤, 그래픽 깨짐, 사운드 끊김은 기능 단어가 있어도 `bug_report`로 검토합니다.
- 강함/약함, 비용 대비 효율, 확률 불만, 조정 요청, 밸런스 패치 요청은 관련 기능 단어가 있어도 `feedback_balance`로 검토합니다.
- 경험치, 성장 재료, 성장 보너스를 얻는 방법은 `wizard_growth`이고, 신규 마법사 소환/뽑기/등장 확률 안내는 `wizard_acquisition`입니다.
- 시스템 개념 설명, 추천 빌드, 배치 전략, 효과적인 조합 상황은 `gameplay_guide`이고, 데미지 공식, 쿨타임, 판정, 발동 조건은 `skill_combat`입니다.

주의 사항:
- 이번 단계에서는 dataset CSV row를 수정하지 않았습니다.
- category label, classifier logic, backend scripts, knowledge 문서는 변경하지 않았습니다.
- dataset v2에서는 이 정책을 기준으로 ambiguous sample list를 먼저 만든 뒤 row 수정과 신규 샘플 추가를 진행해야 합니다.

## V2 Baseline Evaluation Findings (v0.9.0-v2-baseline-evaluation)

평가 기준:
- Dataset: `data/raw/wizard_defense_inquiries_v2.csv`
- Script: `backend/scripts/evaluate_v2_baselines.py`
- Rule-based output: `experiments/rule_classifier_predictions_v2.csv`
- TF-IDF output: `experiments/tfidf_predictions_v2.csv`
- Comparison output: `experiments/baseline_comparison_v2.csv`
- Summary: `experiments/v2_baseline_evaluation_summary.md`
- Total samples: 150
- Rule-based accuracy: 44.67% (67/150)
- TF-IDF accuracy: 72.67% (109/150)
- Both correct: 51
- Both wrong: 25
- Rule-only correct: 16
- TF-IDF-only correct: 58

Category별 관찰:
- `bug_report`: rule-based 5/25, TF-IDF 16/25입니다. v2에서 기능 단어가 포함된 bug case가 늘어나면서 rule-based의 한계가 더 뚜렷해졌습니다.
- `feedback_balance`: rule-based 4/25, TF-IDF 21/25입니다. TF-IDF는 평가 표현을 비교적 잘 잡았지만, rule-based는 feature keyword에 끌리는 문제가 남았습니다.
- `gameplay_guide`: rule-based 12/20, TF-IDF 6/20입니다. v1과 마찬가지로 rule-based가 guide category에서는 더 강합니다.
- `skill_combat`: rule-based 11/20, TF-IDF 17/20입니다. 전투/스킬 표현이 다양해질수록 TF-IDF가 더 잘 일반화했습니다.
- `tower_progress`: rule-based 13/20, TF-IDF 19/20입니다. v2의 tower 표현은 TF-IDF baseline에 특히 유리했습니다.
- `wizard_acquisition`: 두 baseline 모두 17/20입니다. 소환, 전설 등장, 획득 안내 표현은 비교적 안정적입니다.
- `wizard_growth`: rule-based 5/20, TF-IDF 13/20입니다. 성장 표현이 다양해지면서 rule-based keyword coverage 부족이 나타났습니다.

v1 대비 해석:
- v1에서는 rule-based 60.00%, TF-IDF 58.00%였지만, v2에서는 rule-based 44.67%, TF-IDF 72.67%로 방향이 크게 달라졌습니다.
- v2는 `bug_report`와 `feedback_balance`의 feature-word boundary case를 의도적으로 늘렸기 때문에 rule-based keyword priority의 약점을 더 잘 드러냅니다.
- TF-IDF는 v2의 반복적이고 균형 잡힌 category별 표현에서 더 좋은 성능을 보였지만, `gameplay_guide`에서는 여전히 낮은 정확도를 보였습니다.

다음 분석 후보:
- `baseline_comparison_v2.csv`에서 both wrong 25개를 중심으로 세부 error analysis를 작성합니다.
- rule-only correct 16개와 TF-IDF-only correct 58개를 비교해 rule 보강 후보와 feature engineering 후보를 분리합니다.
- classifier logic 변경은 별도 실험으로 분리하고, 이번 결과는 v2 baseline으로 보존합니다.
