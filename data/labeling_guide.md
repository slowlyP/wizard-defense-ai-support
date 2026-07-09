# 레이블링 가이드

이 문서는 `Wizard Defense AI Support`의 문의 데이터에 대한 레이블링 규칙을 한국어로 설명합니다. 모든 라벨(카테고리, 서브카테고리, 긴급도, 사람 검토 필요 여부)은 아래 기준에 따라 일관되게 적용해야 합니다.

1) 카테고리 정의
- `gameplay_guide`: 플레이어가 게임 플레이 방법, 배치, 전략, 상성 등 게임 플레이 자체에 대해 묻는 질문.
- `wizard_acquisition`: 마법사 랜덤 획득, 뽑기, 티켓, 등급, 중복 획득, 획득 확률 관련 문의.
- `wizard_growth`: 마법사 성장, 레벨업, 재능(타렌트), 레조넌스(Resonance) 시스템 등 성장 관련 문의.
- `tower_progress`: 타워(또는 던전) 층 진행, 보상, 보스, 층 관련 진척도 및 잠금 해제 문의.
- `skill_combat`: 스킬 사용, 쿨타임, 상호작용, 데미지 계산 등 전투·스킬 관련 문의.
- `bug_report`: 게임 이상 동작, 크래시, 저장 손실, UI 오류 등 명백한 버그 리포트.
- `feedback_balance`: 밸런스, 경험치/드랍율/업그레이드 비용 등 시스템 전반의 밸런스 의견 또는 개선 제안.

2) 서브카테고리 예시
- `placement`, `path_rules`, `strategy`, `elemental_synergy`, `mechanics`, `beginner_guide` 등은 `gameplay_guide`의 서브카테고리 예시입니다.
- `acquisition_guide`, `random_draw`, `draw_ticket`, `duplicate_acquisition`, `acquisition_probability` 등은 `wizard_acquisition`의 서브카테고리 예시입니다.
- `resonance`, `leveling`, `talent`, `level_cap` 등은 `wizard_growth`의 서브카테고리 예시입니다.
- `floor_difficulty`, `unlock_conditions`, `boss_tactics`, `reward_bug` 등은 `tower_progress`의 서브카테고리 예시입니다.
- `cooldown_display`, `skill_synergy`, `damage_formula`, `hitbox_issue` 등은 `skill_combat`의 서브카테고리 예시입니다.
- `crash`, `save_loss`, `visual_glitch`, `input_issue` 등은 `bug_report`의 서브카테고리 예시입니다.
- `overpowered`, `economy`, `drop_rate`, `meta_diversity` 등은 `feedback_balance`의 서브카테고리 예시입니다.

3) 긴급도(urgency) 규칙
- `high`: 게임을 진행할 수 없게 하는 문제(크래시, 저장 손실, 플레이 중지 버그), 또는 다수의 유저에게 큰 피해를 주는 문제.
- `medium`: 게임 경험을 어렵게 하거나 혼란을 주는 문제(UI 미노출, 보상 미지급, 밸런스 이슈로 인한 불만 등).
- `low`: 정보 문의, 가이드 요청, 소소한 오타/문서 개선 요청 등 즉시 조치가 필요하지 않은 항목.

4) `needs_human` (사람 검토 필요 여부) 규칙
- `true`: 문제 재현이 필요하거나 보상/환불/데이터 복구 등 사람이 개입해야 하는 경우(예: 저장 손실, 보상 중복, 크래시 재현 요청, 치팅/악용 의심, 민감한 경제 보상 이슈).
- `false`: 단순 정보 제공이나 자동 응답으로 처리 가능한 문의(게임플레이 팁, 일반 가이드, 마법사 획득 방법 등).

5) 애매한 경우 처리
- 메시지가 버그 리포트와 게임플레이 질문을 동시에 포함하면 우선 `bug_report`로 표시합니다(버그가 사용자 경험에 중대한 영향을 미칠 가능성이 높음).
- 라벨이 분명하지 않거나 둘 이상의 카테고리에 해당하는 경우 `needs_human=true`로 표시하고 검토자에게 전달합니다.
- v0.6.0 baseline comparison에서 `bug_report`, `feedback_balance`, `wizard_growth`, `gameplay_guide` 경계 샘플의 혼동이 확인되었습니다. dataset v2를 만들기 전까지 기존 dataset row는 변경하지 않되, 아래 경계 규칙을 신규 라벨링과 재검토 기준으로 사용합니다.

6) 라벨 경계 규칙

### `bug_report` vs feature category
- 실제 동작이 기대와 다르거나 진행이 막히는 경우는 기능 단어가 포함되어도 `bug_report`로 라벨링합니다.
- `생성되지 않아요`, `멈춤`, `진행이 안 됨`, `중복 지급`, `소모되었는데 아무 일 없음`, `깨져 보임`, `끊김`, `강제 종료`, `입력 불가`는 `bug_report` 의도 신호로 봅니다.
- 단순히 "어떻게 하나요", "작동 방식이 궁금합니다", "설명해 주세요"처럼 정보 요청이면 해당 feature category를 유지합니다.
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
- "초보자용 성장 가이드를 추천해 주세요." -> `gameplay_guide`
- "성장 단계가 오르면 어떤 보너스를 받나요?" -> `wizard_growth`

### `gameplay_guide` vs `skill_combat`
- 조합이 좋은 상황, 추천 덱, 배치 우선순위, 전투 운영 팁은 `gameplay_guide`입니다.
- 스킬 쿨타임, 데미지 계산, 타격 판정, 스킬 발동 조건, 상태 이상 효과는 `skill_combat`입니다.
- "효과적인 상황"처럼 전략 조언을 묻는 문장은 스킬 단어가 있어도 `gameplay_guide`에 가깝습니다.

예시:
- "번개 마법사와 불 마법사 조합이 효과적인 상황을 알려주세요." -> `gameplay_guide`
- "번개 스킬이 어떤 대상에게 연쇄되는지 알려주세요." -> `skill_combat`

7) 예시 (올바른 라벨링 vs 잘못된 라벨링)
- 예시 A
	- 텍스트: "레조넌스 시도했는데 재료만 사라지고 아무 일도 안 일어났어요. 보상 돌려줄 수 있나요?"
	- 올바른 라벨: `bug_report`, 서브카테고리 `resonance_fail`, `urgency=high`, `needs_human=true` (재료 손실 및 보상 문제는 사람 개입 필요)
	- 잘못된 라벨: `wizard_growth` 또는 `feedback_balance` (문제가 명백히 버그임)

- 예시 B
	- 텍스트: "초반에 어떤 마법사가 효율이 좋나요? 추천해 주세요."
	- 올바른 라벨: `gameplay_guide`, 서브카테고리 `beginner_guide`, `urgency=low`, `needs_human=false`
	- 잘못된 라벨: `feedback_balance` 또는 `bug_report`

- 예시 C
	- 텍스트: "업데이트 후 스킬 설명과 실제 효과가 달라졌어요. 공지에 안 나왔습니다."
	- 올바른 라벨: `bug_report`(또는 `feedback_balance`의 경계 사례), 서브카테고리 `patch_effects`, `urgency=medium`, `needs_human=true` (밸런스 변경으로 인한 혼란·정책적 판단 필요)

8) 라벨링 워크플로
- 각 샘플은 1차 라벨러가 라벨을 적용한 뒤 2차 검토자와 교차 검증합니다.
- 분쟁 표본은 별도의 리뷰 풀로 보내고 최종 라벨을 결정합니다.

9) 메타데이터
- `id`: 샘플 고유 ID
- `text`: 플레이어 문의 원문(한국어)
- `category`: 위 정의된 영어 키워드
- `subcategory`: 영어 키워드 (가능한 한 상세하게)
- `urgency`: `low`/`medium`/`high`
- `needs_human`: `true`/`false`

