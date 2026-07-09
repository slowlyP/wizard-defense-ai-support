# Baseline Comparison Summary (v0.6.0-baseline-comparison)

## 전체 비교 결과

- Dataset: `data/raw/wizard_defense_inquiries_raw.csv`
- Rule-based prediction: `experiments/rule_classifier_predictions.csv`
- TF-IDF prediction: `experiments/tfidf_predictions.csv`
- Comparison output: `experiments/baseline_comparison.csv`
- Total samples: 100
- Rule-based correct: 60 / 100, accuracy 60.00%
- TF-IDF correct: 58 / 100, accuracy 58.00%
- Both correct: 40
- Both wrong: 22
- Rule-only correct: 20
- TF-IDF-only correct: 18

전체 accuracy는 rule-based가 TF-IDF보다 2.00%p 높습니다. 다만 40개 샘플만 두 방식이 동시에 맞췄고, 38개 샘플은 한쪽만 맞췄기 때문에 두 baseline은 서로 다른 강점과 약점을 보입니다. 이 결과는 v0.6.0 포트폴리오 baseline으로 보존하고, 다음 단계의 데이터 확장 또는 feature engineering 실험에서 비교 기준으로 사용합니다.

## category별 비교

| category | total | rule-based correct | rule-based accuracy | TF-IDF correct | TF-IDF accuracy | both correct | both wrong | rule-only correct | TF-IDF-only correct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bug_report` | 14 | 3 | 21.43% | 3 | 21.43% | 0 | 8 | 3 | 3 |
| `feedback_balance` | 11 | 1 | 9.09% | 5 | 45.45% | 1 | 6 | 0 | 4 |
| `gameplay_guide` | 16 | 13 | 81.25% | 7 | 43.75% | 6 | 2 | 7 | 1 |
| `skill_combat` | 14 | 10 | 71.43% | 12 | 85.71% | 8 | 0 | 2 | 4 |
| `tower_progress` | 12 | 9 | 75.00% | 7 | 58.33% | 5 | 1 | 4 | 2 |
| `wizard_acquisition` | 18 | 16 | 88.89% | 15 | 83.33% | 14 | 1 | 2 | 1 |
| `wizard_growth` | 15 | 8 | 53.33% | 9 | 60.00% | 6 | 4 | 2 | 3 |

## rule-based가 강한 영역

- `gameplay_guide`: rule-based는 13/16으로 TF-IDF의 7/16보다 높습니다. 배치, 경로, 초반 라운드처럼 명확한 키워드가 있는 일반 가이드 문의에서 강합니다.
- `tower_progress`: rule-based는 9/12로 TF-IDF의 7/12보다 높습니다. 층, 라운드, 타워 진행 관련 단서가 직접 등장할 때 안정적입니다.
- `wizard_acquisition`: 두 방식 모두 강하지만 rule-based가 16/18로 가장 높습니다. 소환, 획득, 뽑기 같은 직접 표현이 있는 문의에 유리합니다.
- rule-only correct는 총 20개이며, 그중 `gameplay_guide` 7개와 `tower_progress` 4개가 큰 비중을 차지합니다.

## TF-IDF가 강한 영역

- `skill_combat`: TF-IDF는 12/14로 rule-based의 10/14보다 높습니다. 스킬, 공격, 대상, 전투 표현이 다양하게 나타나는 문의에서 char n-gram feature가 도움이 된 것으로 보입니다.
- `feedback_balance`: TF-IDF는 5/11로 rule-based의 1/11보다 높습니다. rule-based가 기능 키워드에 끌리는 반면, TF-IDF는 일부 밸런스 표현을 더 잘 포착했습니다.
- `wizard_growth`: TF-IDF는 9/15로 rule-based의 8/15보다 약간 높습니다. 성장, 레벨업, 경험치 문맥의 변형 표현을 일부 더 잘 처리했습니다.
- TF-IDF-only correct는 총 18개이며, `feedback_balance` 4개와 `skill_combat` 4개가 가장 큰 비중을 차지합니다.

## 둘 다 틀리는 공통 오분류 유형

- 오류 표현이 약한 `bug_report`: `그래픽이 깨져 보이는 현상`, `프레임 드랍`, `사운드 재생 문제`처럼 명시적인 버그 키워드가 약하거나 기능 단어가 함께 있으면 두 방식 모두 기능 category로 이동하는 경우가 많습니다.
- 밸런스 의도와 기능 단서의 충돌: `타워 업그레이드 비용`, `전설 마법사 등장 확률`, `특정 스킬 조합`처럼 밸런스 평가가 있어도 타워, 마법사, 스킬 단서가 강하면 다른 category로 분류됩니다.
- 성장과 획득의 경계 혼동: `경험치를 어떻게 얻나요`, `퀘스트로 얻는 보상`, `경험치 획득량`처럼 `얻`, `획득`, `보상` 표현이 성장 의도와 획득 의도를 동시에 가리킵니다.
- gameplay와 성장/스킬 조합 문의의 경계 혼동: `레조넌스 시스템 설명`, `마법사 조합이 효과적인 상황`처럼 설명 요청이지만 내부 기능 단어가 강하면 `wizard_growth` 또는 `skill_combat`으로 이동합니다.
- 기능 category로 라벨링된 UI 중단 사례: `뽑기 진행 중 UI가 멈추고 진행이 안 됩니다`는 현재 expected category가 `wizard_acquisition`이지만 두 방식 모두 `bug_report`로 예측했습니다. label policy 검토가 필요한 경계 사례입니다.

## 다음 개선 방향

- category label은 유지한 상태에서 `baseline_comparison.csv`를 기준으로 rule-only correct와 TF-IDF-only correct 샘플을 분리해 다음 실험 후보를 정의합니다.
- `bug_report`는 기능 단어와 오류 표현이 함께 등장하는 문장을 별도 패턴으로 추적합니다.
- `feedback_balance`는 `너무`, `낮아`, `과도`, `효율`, `밸런스`, `패치`, `체감` 같은 평가 표현을 기능 단서와 분리해 분석합니다.
- `wizard_growth`와 `wizard_acquisition`은 `얻`, `획득`, `보상`이 성장 재화 문맥인지 신규 마법사 획득 문맥인지 구분하는 예시를 추가로 수집합니다.
- 다음 단계에서는 아직 data v2를 구현하지 않고, 이 v0.6.0 비교 결과를 포트폴리오 baseline 문서로 먼저 고정합니다.
