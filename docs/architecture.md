# Architecture

시스템 아키텍처 개요 (Korean):

- Ingest: `knowledge/` 및 `data/raw/`를 파싱하여 `data/processed/`로 정리합니다.
- Indexing: 임베딩을 생성하고 검색 인덱스를 빌드합니다.
- Backend: 분류기 및 검색 엔드포인트, 그리고 응답 생성 파이프라인을 제공합니다.
- Frontend: 플레이어 문의를 보내고 결과를 표시하는 간단한 UI.

Notes:
- Keep retrieval deterministic and provide citation links to `knowledge/` files for grounded answers.
