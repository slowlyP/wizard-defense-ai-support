# Experiment Log

개요:
실험 구성, 하이퍼파라미터, 결과 요약 및 재현 가능한 실행 절차를 기록하는 템플릿입니다. 모델 학습/평가 시에는 실험별로 이 파일 또는 별도 마크다운을 생성해 상세 기록을 남기세요.

예시 항목 형식:
- 날짜: YYYY-MM-DD
- 목적: 실험의 짧은 설명
- 설정: 사용한 데이터셋, 모델, 주요 파라미터
- 결과: 주요 지표(예: accuracy, recall, MRR) 및 관찰 내용

## EXP-001 Rule-based Classifier (v0.3.0-rule-baseline)

- Date: 2026-07-08
- Goal: 키워드 기반 룰 분류기 초기 후보 구현 및 간단한 테스트
- Config: Python script `backend/app/rule_classifier.py`, dataset `data/raw/wizard_defense_inquiries_raw.csv`
- Results: 기본 키워드 규칙으로 샘플 테스트 통과(7/7 사례 출력)
- Notes: 2026-07-08 로컬 테스트에서 발견된 `freeze_or_crash`, `equip_failure`, `floor_selection_issue`, `skill_targeting` 오분류를 보정했습니다. 버그 키워드는 높은 긴급도와 사람 검토 필요로 처리하고, 장비/층/스킬 실패 패턴은 중간 긴급도와 사람 검토 필요로 처리합니다. 향후 전체 데이터셋 기준 정밀도/재현율 검증이 필요합니다.


