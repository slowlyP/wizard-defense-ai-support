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
