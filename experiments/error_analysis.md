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
