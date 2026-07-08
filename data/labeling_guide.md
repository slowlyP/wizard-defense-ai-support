# 레이블링 가이드

이 문서는 `Wizard Defense AI Support`의 문의 데이터에 대한 레이블링 규칙을 한국어로 설명합니다. 모든 라벨(카테고리, 서브카테고리, 긴급도, 사람 검토 필요 여부)은 아래 기준에 따라 일관되게 적용해야 합니다.

1) 카테고리 정의
- `gameplay_guide`: 플레이어가 게임 플레이 방법, 배치, 전략, 상성 등 게임 플레이 자체에 대해 묻는 질문.
- `wizard_growth`: 마법사 성장, 레벨업, 재능(타렌트), 레조넌스(Resonance) 시스템 등 성장 관련 문의.
- `equipment_inventory`: 장비 획득, 장착, 인벤토리, 장비 강화/분해 관련 문의.
- `tower_progress`: 타워(또는 던전) 층 진행, 보상, 보스, 층 관련 진척도 및 잠금 해제 문의.
- `skill_combat`: 스킬 사용, 쿨타임, 상호작용, 데미지 계산 등 전투·스킬 관련 문의.
- `bug_report`: 게임 이상 동작, 크래시, 저장 손실, UI 오류 등 명백한 버그 리포트.
- `feedback_balance`: 밸런스, 경험치/드랍율/업그레이드 비용 등 시스템 전반의 밸런스 의견 또는 개선 제안.

2) 서브카테고리 예시
- `placement`, `path_rules`, `strategy`, `elemental_synergy`, `mechanics`, `beginner_guide` 등은 `gameplay_guide`의 서브카테고리 예시입니다.
- `resonance`, `leveling`, `talent`, `level_cap` 등은 `wizard_growth`의 서브카테고리 예시입니다.
- `equip_slots`, `item_stats`, `upgrade_costs`, `filter_bug` 등은 `equipment_inventory`의 서브카테고리 예시입니다.
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
- `false`: 단순 정보 제공이나 자동 응답으로 처리 가능한 문의(게임플레이 팁, 일반 가이드, 장비 사용법 등).

5) 애매한 경우 처리
- 메시지가 버그 리포트와 게임플레이 질문을 동시에 포함하면 우선 `bug_report`로 표시합니다(버그가 사용자 경험에 중대한 영향을 미칠 가능성이 높음).
- 라벨이 분명하지 않거나 둘 이상의 카테고리에 해당하는 경우 `needs_human=true`로 표시하고 검토자에게 전달합니다.

6) 예시 (올바른 라벨링 vs 잘못된 라벨링)
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

7) 라벨링 워크플로
- 각 샘플은 1차 라벨러가 라벨을 적용한 뒤 2차 검토자와 교차 검증합니다.
- 분쟁 표본은 별도의 리뷰 풀로 보내고 최종 라벨을 결정합니다.

8) 메타데이터
- `id`: 샘플 고유 ID
- `text`: 플레이어 문의 원문(한국어)
- `category`: 위 정의된 영어 키워드
- `subcategory`: 영어 키워드 (가능한 한 상세하게)
- `urgency`: `low`/`medium`/`high`
- `needs_human`: `true`/`false`

