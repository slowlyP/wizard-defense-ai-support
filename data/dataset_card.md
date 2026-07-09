# 데이터셋 카드

데이터셋 이름: Wizard Defense Inquiries (v0.2.0-dataset-v1)

요약 목적:
이 데이터셋은 Unity 게임 "Random Wizard Defense"를 위한 플레이어 문의(지원 티켓) 샘플을 합성한 것으로, 의도 분류(intent classification) 및 검색 기반 응답(grounded response) 시스템의 개발과 평가에 사용됩니다.

버전: v0.2.0-dataset-v1

데이터 출처:
- 게임 디자인 문서를 기반으로 합성된 문의(실사용자 데이터 포함하지 않음). 샘플 문장은 게임 맥락을 반영하여 작성되었습니다.

라벨 스키마:
- `category`: `gameplay_guide`, `wizard_acquisition`, `wizard_growth`, `tower_progress`, `skill_combat`, `bug_report`, `feedback_balance`
- `subcategory`: 각 카테고리에 대한 상세 영어 키워드(예: `placement`, `acquisition_guide`, `resonance` 등)
- `urgency`: `low` / `medium` / `high`
- `needs_human`: `true` / `false`

카테고리 분포:
- 총 샘플 수: 100
- `gameplay_guide`: 16
- `wizard_acquisition`: 18
- `wizard_growth`: 15
- `tower_progress`: 12
- `skill_combat`: 14
- `bug_report`: 14
- `feedback_balance`: 11

제한 사항(Limitations):
- 합성 데이터이므로 실제 사용자 표현의 다양성이 제한될 수 있습니다.
- 문화적/언어적 표현 패턴이 한정되어 있으며, 실제 티켓에서는 더 다양한 방언·약어·오타가 나타날 수 있습니다.
- 현재 버전은 한국어 문의 중심이며 다른 언어는 포함되어 있지 않습니다.
- v0.6.0 baseline comparison 결과, dataset v1에는 일부 라벨 경계가 애매한 샘플이 포함되어 있음이 확인되었습니다.
- 특히 `bug_report` vs feature category, `feedback_balance` vs `skill_combat`/`tower_progress`, `wizard_growth` vs `wizard_acquisition`, `gameplay_guide` vs `wizard_growth`/`skill_combat` 경계에서 혼동이 발생했습니다.
- 이 모호성은 dataset v1의 알려진 한계로 기록하며, 현재 CSV row는 변경하지 않습니다.

프라이버시 고지:
- 이 데이터셋은 실사용자 PII(개인식별정보)를 포함하지 않으며, 모두 합성된 예시로 구성되어 있습니다.

향후 개선 계획:
- 실제 플레이어 로그(익명화 및 적법한 동의 후)를 추가하여 다양성을 높임.
- 더 많은 엣지케이스(복합 문의, 멀티턴 대화) 샘플 추가.
- 추가 메타데이터(플랫폼, 클라이언트 버전, 재현 단계 등) 포함.
- dataset v2에서는 v0.7.0 data quality review의 라벨 경계 규칙을 적용하여 모호한 샘플을 재검토합니다.
- dataset v2에서는 기능 단어와 오류 표현이 함께 있는 `bug_report`, 기능 단어와 평가 표현이 함께 있는 `feedback_balance`, `얻`/`획득`/`보상` 표현이 섞인 성장·획득 경계 샘플을 보강합니다.

## Dataset v2 (v0.8.0-dataset-v2)

데이터셋 파일:
- `data/raw/wizard_defense_inquiries_v2.csv`

생성 배경:
- dataset v2는 `v0.6.0-baseline-comparison`과 `v0.7.0-data-quality-review` 이후 생성한 개선 버전입니다.
- 기존 v1 파일인 `data/raw/wizard_defense_inquiries_raw.csv`는 비교 기준으로 보존하며 덮어쓰지 않습니다.
- v2는 라벨 경계가 약했던 category와 ambiguous case를 보강하기 위한 별도 파일입니다.

라벨 스키마:
- v1과 동일한 컬럼을 사용합니다: `id`, `text`, `category`, `subcategory`, `urgency`, `needs_human`
- category label set은 변경하지 않았습니다: `gameplay_guide`, `wizard_acquisition`, `wizard_growth`, `tower_progress`, `skill_combat`, `bug_report`, `feedback_balance`

카테고리 분포:
- 총 샘플 수: 150
- `gameplay_guide`: 20
- `wizard_acquisition`: 20
- `wizard_growth`: 20
- `tower_progress`: 20
- `skill_combat`: 20
- `bug_report`: 25
- `feedback_balance`: 25

v2 목표 개선 사항:
- `bug_report`에 기능 단어가 포함된 오류 사례를 늘렸습니다. 예: 레조넌스 실패, 소환 UI 멈춤, 보상 중복, 층 선택 오류, 스킬 효과 미적용.
- `feedback_balance`에 기능 단어가 포함된 평가 사례를 늘렸습니다. 예: 소환 비용, 전설 등장 확률, 스킬 조합 독주, 타워 보상 효율, 성장 비용.
- `wizard_growth`와 `wizard_acquisition`을 구분하기 위한 최소 쌍을 보강했습니다. 예: 경험치/성장 재료 획득 vs 신규 마법사 소환/등장 확률 안내.
- `gameplay_guide`와 `wizard_growth`, `gameplay_guide`와 `skill_combat`의 경계 사례를 보강했습니다. 예: 시스템 개념 설명과 성장 수치 질문, 조합 추천과 스킬 계산 질문.
- Random Wizard Defense Unity repository에서 확인 가능한 마법사 소환, 배치, 속성, 합성, 전설 마법사, 아케인 연구, 타워 층, 적 이동, 상태 이상, UI/사운드 범위에 맞춰 작성했습니다.

v2 제한 사항:
- 여전히 합성 데이터이며 실제 플레이어 로그는 포함하지 않습니다.
- v2는 dataset 생성 단계이며, 아직 rule-based 또는 TF-IDF 평가를 수행하지 않았습니다.
- 모델 평가 결과는 추후 별도 실험으로 기록해야 합니다.
