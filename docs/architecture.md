# Architecture

시스템 아키텍처 개요:

- Ingest(데이터 수집/정리): `knowledge/` 및 `data/raw/`의 문서를 파싱하여 `data/processed/`에 정형화된 형식으로 저장합니다.
- Indexing(색인 생성): 문서 임베딩을 생성하고 검색 엔진(예: 벡터 DB)에 인덱스를 생성합니다.
- Backend(백엔드): 의도 분류기와 검색/응답 생성 파이프라인을 제공하는 API 계층입니다.
- Frontend(프론트엔드): 플레이어 문의를 전송하고 응답을 표시하는 간단한 UI입니다.

설계 원칙:
- 검색 결과는 재현 가능하도록 설계하고, 응답에는 항상 `knowledge/` 문서의 근거(citation)를 포함하도록 합니다.

