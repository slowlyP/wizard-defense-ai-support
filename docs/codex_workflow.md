# Codex 작업 워크플로우 및 핸드오프 문서

이 문서는 Codex(자동화 에이전트)가 이후 작업을 시작하기 전에 반드시 먼저 읽어야 하는 프로젝트 규칙과 현재 상태, 체크리스트 및 다음 작업 순서를 요약합니다.

1. 프로젝트 개요
- Project name: Wizard Defense AI Support
- Related game repository: random-wizard-defense
- Goal: Random Wizard Defense 게임의 플레이어 문의를 자동 분류하고, 게임 가이드 문서를 검색하여 근거 기반 답변을 생성하는 AI 포트폴리오 프로젝트

2. 문서화 규칙
- 모든 문서 내용은 한국어로 작성해야 합니다.
- 다음 파일/문서는 한국어로 유지됩니다: README, labeling guide, dataset card, experiment log, error analysis, architecture, portfolio summary, knowledge documents.
- 파일명, 폴더명, CSV 컬럼명, 카테고리 라벨, 서브카테고리 라벨, 코드 식별자는 영어로 유지합니다.
- 다음 라벨은 번역하거나 변경하지 않습니다: gameplay_guide, wizard_growth, equipment_inventory, tower_progress, skill_combat, bug_report, feedback_balance.

3. Codex 작업 전 체크리스트
- 현재 브랜치를 확인한다.
- `docs/codex_workflow.md`를 먼저 읽는다.
- 요청 범위를 벗어난 작업을 하지 않는다.
- 외부 API를 호출하지 않는다 unless explicitly requested.
- `.env` 또는 실제 API 키를 생성하거나 커밋하지 않는다.
- 항상 `.env.example`만 참조하고, 실제 키는 커밋하지 않는다.
- 모든 문서는 한국어로 작성한다(예외: 파일/코드 식별자는 영어).
- 코드, 파일명, 라벨명은 영어 규칙을 유지한다.
- 작업 후 변경된 파일 목록과 요약을 문서화해서 보고한다.
- 다음 단계 제안은 가능하나, 사용자 승인 없이 구현하지 않는다.

4. 데이터셋 규칙
- Main dataset path: `data/raw/wizard_defense_inquiries_raw.csv`
- Columns: `id,text,category,subcategory,urgency,needs_human`
- Dataset version: `v0.2.0-dataset-v1`
- 이 데이터셋은 사용자의 게임 디자인을 기반으로 합성된 한국어 플레이어 문의를 포함합니다.
- 실제 사용자 데이터나 개인 식별 정보(PII)를 포함하면 안 됩니다.
- 현재 목표 크기: 100 rows
- Categories (라벨):
  - gameplay_guide
  - wizard_growth
  - equipment_inventory
  - tower_progress
  - skill_combat
  - bug_report
  - feedback_balance

5. 현재까지 완료한 작업
- GitHub repository 생성: `wizard-defense-ai-support`
- 초기 레포 구조 생성(프론트엔드/백엔드/데이터/문서 등)
- 문서 한국어 작성 규칙 수립
- 데이터셋 v1 생성: `data/raw/wizard_defense_inquiries_raw.csv` (100개 한국어 샘플)
- `data/labeling_guide.md` 업데이트(한국어)
- `data/dataset_card.md` 업데이트(한국어, 버전 표기)
- `README.md` 업데이트(한국어)
- `docs/portfolio_summary.md` 업데이트(한국어)
- `knowledge/` 문서 및 관련 문서들을 한국어로 변환
- `docs/architecture.md`, `experiments/` 문서들을 한국어로 변환

6. 다음 작업 순서 (우선순위 순)
1) 데이터셋 품질 검증 (중복, 필드 유효성, 라벨 일관성)
2) dataset v1 커밋
3) `feature/inquiry-dataset-v1` 브랜치 병합 -> `main`
4) 태그 생성: `v0.2.0-dataset-v1`
5) 규칙 기반 분류기(rule-based classifier) 구현 (초안)
6) TF-IDF 기반 베이스라인 실험 구성
7) FastAPI 백엔드 스켈레톤 구현
8) React 프론트엔드 스켈레톤 구현
9) 이후: LLM 기반 프롬프트 실험 추가(사용자 승인 후)

7. Codex에게 요청할 때 사용해야 하는 기본 문장(템플릿)

"Before making changes, read docs/codex_workflow.md and follow the project rules and checklist.
Task:
[작업 내용]
Scope:
[수정할 파일/폴더]
Do not:
[하지 말아야 할 것]
Completion criteria:
[완료 기준]"

8. 하지 말아야 할 것 (요약)
- 요청받지 않은 경우 백엔드/프론트엔드를 구현하지 않는다.
- 요청받지 않은 경우 인제스트(ingestion) 스크립트를 생성하지 않는다.
- 외부 API를 호출하지 않는다.
- 실제 API 키를 추가하거나 커밋하지 않는다.
- 라벨을 임의로 변경하지 않는다.
- 사용자 승인 없이 전체 프로젝트 구조를 재작성하지 않는다.
- 무관한 기능을 생성하지 않는다.

부록: 변경 보고 규칙
- 작업 완료 후 다음 정보를 포함한 요약을 작성한다:
  - 변경된 파일 목록
  - 간단한 변경 내용 설명
  - 후속 권장 작업(최대 3개)

이 문서는 모든 Codex 작업의 진입점입니다. Codex는 이 규칙을 준수해야 하며, 위 체크리스트를 확인한 후에만 변경을 수행하세요.
