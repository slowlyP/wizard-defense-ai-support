# Support Knowledge Base Seed

## 1. 목적

향후 RAG 지식 후보를 작은 검토 단위로 정리한다. 이 문서는 계획용 seed이며 현재 RAG가 구현되었거나 아래 내용이 자동 검색된다고 주장하지 않는다.

## 2. Future RAG seed knowledge 안내

각 항목은 Unity read-only reference와 현재 `support_knowledge.py`에 반영된 범위를 출발점으로 한다. 실제 ingestion 전 source version, 승인자, 최신 build 검토, 언어 pair와 safety metadata가 필요하다. 수치, 확률, live balance와 schedule은 별도 승인 없이는 넣지 않는다.

## 3. Wizard elements

- Fire / 불
- Water / 물
- Wind / 바람
- Stone / 돌
- Lightning / 번개

기본 원소/type은 위 다섯 가지로 안내한다. 개별 효과의 정확한 수치나 최종 balance는 현재 build의 승인 문서 없이는 확정하지 않는다.

## 4. Legendary wizards

- 아르덴 / Arden — Fire 계열, explosive damage dealer 안내
- 오르펠 / Orphel — Water 계열, freeze/control type 안내
- 루미엘 / Lumiel — Wind 계열, support/blessing type 안내
- 노바린 / Novarin — Lightning 계열, special lightning type 안내

치유량, 획득 확률, 최종 능력치처럼 문서화되지 않은 효과는 보장하지 않는다.

## 5. Fusion 예시

- 불 + 물 → 안개
- 안개 + 나무 → 숲
- 번개 + 바람 → 폭풍
- 돌 + 불 → 용암

현재 deterministic support knowledge에서 검증된 핵심 규칙은 서로 다른 element의 등록된 pair를 조합한다는 점과 Fire + Water의 mist/안개 예시다. 나머지 조합명은 future seed 후보이므로 authoritative 문서와 현재 build에서 별도 검증되기 전에는 확정 답변에 사용하지 않는다.

## 6. Resonance 지원 안내

공명/resonance는 신규 마법사 획득과 구분되는 성장·강화 계열로 설명한다. 정확한 수치와 보상 결과는 현재 build의 승인 문서를 확인한다. 재료가 사라졌다는 문의는 자동 복구·보상을 약속하지 않고 발생 시각, 단계, build 정보를 받아 human review로 보낸다.

## 7. Tower/floor 안내

층 선택과 다음 층 진행은 현재 tower/floor 진행 상태 및 완료 조건을 확인하도록 안내한다. 정확한 boss 층, live schedule, 미출시 층과 해금 날짜를 추측하거나 약속하지 않는다.

## 8. PC/Steam demo controls 안내

PC/Steam demo 맥락에서 마법사는 중앙 전장 내 허용 범위에서 mouse drag 방식으로 배치하며 한 번에 하나를 드래그한다. 플랫폼이나 build별 차이가 있으면 현재 demo guide를 우선하고 미검증 단축키는 만들지 않는다.

## 9. Fullscreen/resolution troubleshooting 안내

Windowed/fullscreen 전환, resolution 재선택, Steam demo 또는 Windows build 재실행을 먼저 확인한다. 계속 재현되면 PC resolution, fullscreen/windowed 상태, build, screenshot과 재현 단계를 요청한다. Guaranteed fix나 patch date는 말하지 않는다.

## 10. Reward/payment/refund safe review 안내

보상·재화 손실은 자동 지급 또는 restoration을 확정하지 않는다. 결제·환불은 가능 여부를 약속하지 않고 플랫폼, 발생 시각과 안전한 주문 식별 절차를 안내한 뒤 human review로 전환한다. 카드번호, 비밀번호 같은 민감정보를 채팅이나 prompt에 요청하지 않는다.

## 11. 금지 문구

- “무조건 환불해 드립니다.”
- “보상 아이템을 반드시 지급합니다.”
- “계정이나 진행을 확실히 복구합니다.”
- “다음 패치에서 반드시 수정됩니다.”
- “패치 날짜는 확정입니다.”

## 12. 한계

이 seed는 운영 FAQ, 결제 정책 또는 live game database가 아니다. Account recovery, Steamworks, payment/refund 처리와 helpdesk integration을 수행하지 않는다. 특히 fusion 후보와 미문서화 효과는 승인 전 검색 대상에서 제외해야 한다.
