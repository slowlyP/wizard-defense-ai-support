# Wizard Defense AI Support

설명:
이 저장소는 Unity 게임 "Random Wizard Defense"를 위한 AI 지원 시스템의 초기 구조입니다. 이 프로젝트는 인턴십용 포트폴리오로 활용하기 적합하도록 의도 분류, 문서 검색, 근거 기반 응답 설계를 중심으로 한 스캐폴딩을 제공합니다.

프로젝트 목표:
- 플레이어 문의를 자동 분류하고 관련 게임 문서에서 근거를 찾아 응답을 생성할 수 있는 시스템을 구축하는 것.
- 데이터셋 설계, 라벨링 가이드, 문서 기반 검색 파이프라인 설계 등 AI 엔지니어링 역량을 보여주기 위한 자료 제공.

구성 요약:
- `frontend/`: 사용자 채팅 UI와 대시보드를 위한 공간(초기에는 README만 포함).
- `backend/`: 분류기·검색·응답 파이프라인을 둘 예정(초기에는 README만 포함).
- `data/`: 원시 및 처리된 데이터, 라벨링 가이드, 데이터셋 카드 포함.
- `knowledge/`: 게임플레이 가이드, 마법사 획득·성장 가이드, 스킬 문서 등 근거 문서.
- `experiments/`: 실험 로그와 에러 분석 템플릿.
- `docs/`: 아키텍처 다이어그램 및 포트폴리오 요약.

데이터셋 버전:
- v1 dataset은 `data/raw/wizard_defense_inquiries_raw.csv`에 보존되어 있습니다.
- v2 dataset은 v0.7.0 data quality review 이후 생성한 `data/raw/wizard_defense_inquiries_v2.csv`이며, 150개 문의와 개선된 라벨 경계 사례를 포함합니다.

평가 결과:
- dataset v2 baseline 평가는 `backend/scripts/evaluate_v2_baselines.py`로 실행하며, 결과는 `experiments/*_v2.csv`와 `experiments/v2_baseline_evaluation_summary.md`에 분리 저장됩니다.
- v0.11.0에서는 improved rule classifier를 사용한 로컬 support router prototype을 추가했으며, `backend/scripts/run_support_router_demo.py`로 demo CSV와 summary를 생성할 수 있습니다.
- v0.12.0에서는 support router output을 한국어 response draft template으로 변환하는 로컬 prototype을 추가했습니다.

빠른 시작:
1. `.env.example`를 `.env`로 복사하고 필요한 값을 채우세요.
2. 먼저 데이터셋과 라벨링 가이드를 검토한 뒤 백엔드/프론트엔드 작업을 진행하세요.

향후 작업 추천:
- 소규모 백엔드 스켈레톤(FastAPI)으로 분류 및 검색 엔드포인트 제작.
- `data/`의 샘플을 이용한 벤치마크용 간단한 파이프라인 구성.
- 포트폴리오 문서 작성 및 데모 시나리오 정리.

주의: 프로젝트의 Codex 작업 워크플로우 및 핸드오프 문서는 `docs/codex_workflow.md`에 있고, 필수 작업 체크리스트는 `docs/codex_task_checklist.md`에 있습니다. Codex(또는 자동화 에이전트)는 두 문서를 먼저 읽고 체크리스트를 준수해야 합니다.

# wizard-defense-ai-support
AI support system for Random Wizard Defense player inquiries
