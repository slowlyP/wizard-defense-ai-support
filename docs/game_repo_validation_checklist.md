# 게임 레포 검증 체크리스트

## 1. 목적
이 문서는 AI 지원 프로젝트의 데이터셋, 라벨, `knowledge` 문서, 분류기, 백엔드, 프론트 데모가 실제 Random Wizard Defense Unity 프로젝트와 일치하는지 검증하기 위한 기준 문서입니다. Codex는 게임 레포의 실제 구현 상태와 계획 상태를 확인한 뒤 AI 지원 범위가 게임 내용과 어긋나지 않는지 점검해야 합니다.

## 2. 게임 레포 확인 위치
- Local path: `C:\UnityProjects\Wizard Random Defense`
- GitHub repository: `https://github.com/slowlyP/random-wizard-defense`

## 3. 검증 대상
Codex는 게임 레포를 다음 AI 지원 프로젝트 파일과 비교해야 합니다.

- `data/raw/wizard_defense_inquiries_raw.csv`
- `data/labeling_guide.md`
- `data/dataset_card.md`
- `knowledge/*.md`
- `backend/app/rule_classifier.py`
- `backend/scripts/test_rule_classifier.py`
- `experiments/*.md`
- `README.md`
- `docs/portfolio_summary.md`

## 4. Unity 게임 레포에서 확인해야 할 항목
- [ ] `Assets/Scripts` 안의 주요 C# 스크립트 확인
- [ ] 마법사 배치 시스템 존재 여부 확인
- [ ] 랜덤 마법사 획득 시스템 존재 여부 확인
- [ ] 전설 마법사 공명 또는 관련 계획 존재 여부 확인
- [ ] 탑 층 진행 시스템 존재 여부 확인
- [ ] 몬스터 이동 / 스폰 시스템 존재 여부 확인
- [ ] 스킬 / 전투 시스템 존재 여부 확인
- [ ] AI 지원 문서에 게임 레포에서 확인되지 않은 시스템이 현재 기능처럼 남아 있는지 확인
- [ ] 구현 완료 기능과 계획 중인 기능 구분

## 5. 지원 카테고리 검증 규칙
Codex는 각 AI category가 실제 게임 기능 또는 명확한 계획과 연결되는지 확인해야 합니다.

- `gameplay_guide`: 실제 기본 플레이/배치/라운드 규칙과 연결되는가?
- `wizard_acquisition`: 실제 랜덤 마법사 획득/뽑기/등급 시스템 또는 명확한 계획과 연결되는가?
- `wizard_growth`: 실제 강화/공명/성장/시너지 시스템 또는 명확한 계획과 연결되는가?
- `tower_progress`: 실제 탑 층/라운드/해금 시스템과 연결되는가?
- `skill_combat`: 실제 스킬/공격/전투 시스템과 연결되는가?
- `bug_report`: 실제 게임 기능에서 발생 가능한 오류 유형인가?
- `feedback_balance`: 실제 게임 밸런스 요소와 연결되는가?

## 6. 금지 규칙
- 실제 게임에 없는 기능을 현재 구현 기능처럼 문서화하지 않는다.
- 게임에 없는 시스템으로 문의 데이터를 만들지 않는다.
- 계획 단계 기능은 반드시 `planned` 또는 계획 중으로 표시한다.
- 게임 레포에서 확인되지 않은 시스템은 현재 지원 category로 사용하지 않는다.
- 실제 구현 여부를 확인하지 못한 기능은 current feature로 쓰지 않는다.
- 게임 레포를 확인하지 못한 경우 추측으로 수정하지 않는다.

## 7. 검증 결과 기록 형식
아래 형식을 사용해 게임 레포 검증 결과를 기록합니다.

```markdown
## Game Repo Validation Result

- Date:
- AI branch:
- Game repo path:
- Checked game files:
- Confirmed existing features:
- Confirmed planned features:
- Unsupported AI assumptions found:
- Corrected items:
- Remaining uncertainty:
- Next action:
```

## 8. Codex 작업 전 추가 체크리스트
- [ ] 게임 레포 경로를 확인했는가?
- [ ] 게임 레포를 실제로 열람했는가?
- [ ] AI 작업이 실제 게임 기능과 연결되는가?
- [ ] 현재 구현 기능과 계획 기능을 구분했는가?
- [ ] 없는 기능을 문의 카테고리로 만들지 않았는가?
- [ ] 데이터셋 라벨이 게임 기능과 일치하는가?
- [ ] `knowledge` 문서가 게임 기능과 일치하는가?
- [ ] `rule classifier` 키워드가 실제 지원 카테고리와 일치하는가?
