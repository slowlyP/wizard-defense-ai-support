# Data Quality Review (v0.7.0-data-quality-review)

## 목적

이 문서는 `v0.6.0-baseline-comparison` 결과를 바탕으로 dataset v1의 라벨 경계와 데이터 품질 문제를 정리하기 위한 검토 문서입니다. 이번 단계의 목표는 dataset v2를 만들기 전에 어떤 category가 약하고, 어떤 문의 유형에서 라벨 정책이 흔들리는지 명확히 기록하는 것입니다.

이번 작업에서는 `data/raw/wizard_defense_inquiries_raw.csv`의 row, category label, classifier logic을 변경하지 않습니다. 이 문서는 분석과 정책 정리만 수행하며, dataset v2 생성은 다음 작업으로 분리합니다.

## 사용한 기준선 결과

- Dataset: `data/raw/wizard_defense_inquiries_raw.csv`
- Baseline comparison: `experiments/baseline_comparison.csv`
- Baseline summary: `experiments/baseline_comparison_summary.md`
- Rule-based accuracy: 60.00% (60/100)
- TF-IDF accuracy: 58.00% (58/100)
- Both correct: 40
- Both wrong: 22
- Rule-only correct: 20
- TF-IDF-only correct: 18

두 baseline의 전체 정확도 차이는 2.00%p로 작지만, 한쪽만 맞춘 샘플이 38개입니다. 따라서 단순히 더 높은 baseline을 선택하기보다 라벨 경계와 샘플 구성을 정리하는 것이 dataset v2의 우선 과제입니다.

## category별 문제 요약

| category | 주요 관찰 | v2 검토 우선도 |
|---|---|---|
| `bug_report` | 두 baseline 모두 3/14 correct로 낮고, both wrong 8개가 발생했습니다. 그래픽 깨짐, 프레임 드랍, 사운드 끊김, 보상 중복처럼 명확한 장애 표현이 기능 단어에 묻힙니다. | 높음 |
| `feedback_balance` | rule-based 1/11, TF-IDF 5/11로 차이가 큽니다. 비용, 확률, 스킬 조합, 성장 비용처럼 기능 단어가 강한 밸런스 의견이 다른 category로 이동합니다. | 높음 |
| `wizard_growth` | rule-based 8/15, TF-IDF 9/15입니다. `얻`, `획득`, `보상`, `경험치` 표현 때문에 `wizard_acquisition` 또는 `tower_progress`와 혼동됩니다. | 중간 |
| `gameplay_guide` boundary | rule-based는 강하지만 TF-IDF는 7/16 correct로 낮습니다. 레조넌스, 조합, 전설 마법사 같은 시스템 단어가 포함된 설명 요청이 `wizard_growth` 또는 `skill_combat`으로 이동합니다. | 중간 |

## 공통 오분류 패턴

- `bug_report` vs feature category: 오류 문장에 소환, 레조넌스, 경로, 튜토리얼, 보상, 스킬 같은 기능 단어가 들어가면 기능 category로 분류되기 쉽습니다.
- `feedback_balance` vs feature category: 밸런스 의견에 타워, 전설 마법사, 스킬, 성장 비용 같은 기능 단어가 들어가면 `tower_progress`, `wizard_acquisition`, `skill_combat`, `wizard_growth`로 이동합니다.
- `wizard_growth` vs `wizard_acquisition`: 성장 재화나 경험치를 "얻는다"는 표현이 신규 마법사 획득과 같은 표면 단어를 공유합니다.
- `gameplay_guide` vs `wizard_growth`: 시스템 설명 요청에서 레조넌스, 전설 마법사, 성장 경로 같은 단어가 나오면 일반 가이드가 성장 문의로 이동합니다.
- `gameplay_guide` vs `skill_combat`: 조합이 "효과적인 상황", "추천 덱", "배치 전략"처럼 플레이 조언이면 guide에 가깝지만, 스킬 효과나 데미지 계산을 묻는 경우는 combat에 가깝습니다.

## 라벨 정책 개선안

### `bug_report` vs feature category

- 실제 동작이 기대와 다르거나 진행이 막히는 경우는 기능 단어가 포함되어도 `bug_report`로 라벨링합니다.
- `생성되지 않아요`, `멈춤`, `진행이 안 됨`, `중복 지급`, `소모되었는데 아무 일 없음`, `깨져 보임`, `끊김`, `강제 종료`, `입력 불가`는 `bug_report` 의도 신호로 봅니다.
- 단순히 "어떻게 하나요", "작동 방식이 궁금합니다", "설명해 주세요"처럼 정보 요청이면 feature category를 유지합니다.
- 보상, 재료, 저장 데이터 손실이 포함되면 `needs_human=true` 후보로 표시합니다.

예시:
- "레조넌스 작동 후 전설 마법사가 생성되지 않아요." -> `bug_report`
- "레조넌스로 전설 마법사를 만드는 방법을 알려주세요." -> `wizard_growth`

### `feedback_balance` vs `skill_combat`

- 스킬의 강함, 약함, 지나친 효율, 특정 조합 독주, 밸런스 패치 요청은 `feedback_balance`로 라벨링합니다.
- 스킬 사용법, 쿨타임, 대상 판정, 데미지 공식, 스킬 간 상호작용 설명 요청은 `skill_combat`으로 라벨링합니다.
- "설명과 다르게 작동", "안 맞음", "발동하지 않음"처럼 실제 동작 오류가 있으면 `bug_report` 또는 `skill_combat` 경계 사례로 검토합니다.

예시:
- "특정 스킬 조합이 지나치게 강력해요. 밸런스 패치 필요합니다." -> `feedback_balance`
- "스킬 데미지 계산법 알려주세요." -> `skill_combat`

### `feedback_balance` vs `tower_progress`

- 층 진행, 잠금 해제, 보스 공략, 진행 보상 수령 조건을 묻는 경우는 `tower_progress`입니다.
- 타워 업그레이드 비용, 층 보상 효율, 진행 난이도, 경제 곡선에 대한 평가나 조정 요청은 `feedback_balance`입니다.
- "보상이 지급되지 않음", "층이 열리지 않음"처럼 실패 상태를 말하면 `bug_report` 후보로 검토합니다.

예시:
- "타워 업그레이드 비용 대비 효율이 낮은 것 같습니다." -> `feedback_balance`
- "다음 층은 어떤 조건에서 열리나요?" -> `tower_progress`

### `wizard_growth` vs `wizard_acquisition`

- 신규 마법사 획득, 소환, 뽑기, 티켓, 등급, 중복 획득, 등장 확률은 `wizard_acquisition`입니다.
- 이미 보유한 마법사의 레벨업, 경험치, 성장 보너스, 재능, 레조넌스, 성장 한계는 `wizard_growth`입니다.
- `얻다`, `획득`, `보상` 표현이 있어도 대상이 경험치, 성장 재료, 성장 보너스이면 `wizard_growth`로 라벨링합니다.
- 등장 확률이 낮다는 불만이 핵심이면 `feedback_balance`, 확률 안내가 핵심이면 `wizard_acquisition`입니다.

예시:
- "마법사 레벨업에 필요한 경험치는 어떻게 얻나요?" -> `wizard_growth`
- "전설 마법사 등장 확률이 어떻게 되나요?" -> `wizard_acquisition`
- "전설 마법사 등장 확률이 낮아 너무 운 요소가 큽니다." -> `feedback_balance`

### `gameplay_guide` vs `wizard_growth`

- 플레이 방법, 추천 빌드, 배치, 초반 전략, 시스템 개념을 쉽게 설명해 달라는 요청은 `gameplay_guide`입니다.
- 특정 성장 수치, 레벨업, 성장 보너스, 재능, 레조넌스 성장 비용이나 결과를 묻는 요청은 `wizard_growth`입니다.
- "성장 가이드 추천"처럼 가이드 요청과 성장 단어가 함께 있으면, 목적이 학습/추천이면 `gameplay_guide`, 수치/재화/단계 질문이면 `wizard_growth`로 구분합니다.

예시:
- "초보자용 성장 가이드를 추천해 주세요." -> `gameplay_guide` 후보로 재검토
- "성장 단계가 오르면 어떤 보너스를 받나요?" -> `wizard_growth`

### `gameplay_guide` vs `skill_combat`

- 조합이 좋은 상황, 추천 덱, 배치 우선순위, 전투 운영 팁은 `gameplay_guide`입니다.
- 스킬 쿨타임, 데미지 계산, 타격 판정, 스킬 발동 조건, 상태 이상 효과는 `skill_combat`입니다.
- "효과적인 상황"처럼 전략 조언을 묻는 문장은 스킬 단어가 있어도 `gameplay_guide`에 가깝습니다.

예시:
- "번개 마법사와 불 마법사 조합이 효과적인 상황을 알려주세요." -> `gameplay_guide`
- "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요." -> `skill_combat`

## dataset v2에서 추가해야 할 샘플 유형

- 기능 단어와 오류 표현이 함께 있는 `bug_report`: 레조넌스 실패, 소환 UI 멈춤, 보상 중복, 그래픽 깨짐, 프레임 드랍, 사운드 끊김, 입력 미인식.
- 기능 단어와 평가 표현이 함께 있는 `feedback_balance`: 타워 비용 효율, 스킬 조합 독주, 전설 등장 확률 불만, 성장 비용 과도, 골드 획득량 부족.
- `wizard_growth`와 `wizard_acquisition`을 구분하는 최소 쌍: "경험치를 얻는 방법" vs "마법사를 얻는 방법", "등장 확률 안내" vs "등장 확률 불만".
- `gameplay_guide`와 `wizard_growth`를 구분하는 시스템 설명 샘플: 레조넌스 개념 설명, 초보자 성장 루트 추천, 성장 수치 질문.
- `gameplay_guide`와 `skill_combat`을 구분하는 전투 조언 샘플: 조합 추천, 배치 전략, 스킬 데미지 공식, 스킬 판정 오류.

## dataset v2에서 수정해야 할 샘플 유형

- 현재 기능 category로 라벨링되어 있지만 오류 표현이 강한 샘플은 `bug_report` 후보로 재검토합니다.
- 현재 `wizard_growth`로 라벨링되어 있지만 목적이 "추천 가이드"인 샘플은 `gameplay_guide` 후보로 재검토합니다.
- 현재 `tower_progress` 또는 `wizard_acquisition`으로 보일 수 있으나 핵심이 비용, 효율, 확률 불만인 샘플은 `feedback_balance` 후보로 재검토합니다.
- `얻`, `획득`, `보상`처럼 여러 category에서 공유되는 단어가 포함된 샘플은 대상이 무엇인지 기준으로 label note를 추가합니다.
- 실제 게임 기능과 맞지 않거나 구현 여부가 불명확한 표현은 Unity repository 확인 후 유지, 수정, 제거 여부를 결정합니다.

## 다음 작업 제안

- `data/labeling_guide.md`의 경계 규칙을 기준으로 dataset v1의 ambiguous sample list를 별도로 작성합니다.
- dataset v2 작업에서는 먼저 라벨 정책 리뷰를 통과한 뒤 row 수정과 신규 샘플 추가를 진행합니다.
- dataset v2 생성 후 rule-based와 TF-IDF baseline을 같은 방식으로 재평가해 v0.7.0 문서와 비교합니다.
