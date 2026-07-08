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

프라이버시 고지:
- 이 데이터셋은 실사용자 PII(개인식별정보)를 포함하지 않으며, 모두 합성된 예시로 구성되어 있습니다.

향후 개선 계획:
- 실제 플레이어 로그(익명화 및 적법한 동의 후)를 추가하여 다양성을 높임.
- 더 많은 엣지케이스(복합 문의, 멀티턴 대화) 샘플 추가.
- 추가 메타데이터(플랫폼, 클라이언트 버전, 재현 단계 등) 포함.
