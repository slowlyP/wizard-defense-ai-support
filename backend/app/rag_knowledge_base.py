"""Small local knowledge base for deterministic retrieval experiments.

This module contains reviewed support snippets only. It does not use an LLM,
embeddings, a vector database, external APIs, or private player data.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    topic: str
    language: str
    source_type: str
    safety_level: str
    requires_human_review: bool
    title: str
    content: str
    keywords: tuple[str, ...]


def _chunk(
    topic: str,
    language: str,
    title: str,
    content: str,
    keywords: tuple[str, ...],
    *,
    source_type: str = "game_guide",
    safety_level: str = "normal",
    requires_human_review: bool = False,
) -> KnowledgeChunk:
    return KnowledgeChunk(
        id=f"{topic}.{language}.v1",
        topic=topic,
        language=language,
        source_type=source_type,
        safety_level=safety_level,
        requires_human_review=requires_human_review,
        title=title,
        content=content,
        keywords=keywords,
    )


RAG_KNOWLEDGE_CHUNKS: tuple[KnowledgeChunk, ...] = (
    _chunk("wizard_elements", "ko", "마법사 원소", "기본 마법사 원소는 Fire/불, Water/물, Wind/바람, Stone/돌, Lightning/번개 다섯 가지입니다.", ("마법사 종류", "마법사 원소", "종류", "속성", "fire", "water", "wind", "stone", "lightning")),
    _chunk("wizard_elements", "en", "Wizard elements", "The five basic wizard elements are Fire, Water, Wind, Stone, and Lightning.", ("wizard types", "wizard elements", "elements", "fire", "water", "wind", "stone", "lightning")),
    _chunk("legendary_wizards", "ko", "전설 마법사", "전설 마법사는 Arden/아르덴, Orphel/오르펠, Lumiel/루미엘, Novarin/노바린입니다.", ("전설 마법사", "전설", "아르덴", "오르펠", "루미엘", "노바린")),
    _chunk("legendary_wizards", "en", "Legendary wizards", "The legendary wizards are Arden, Orphel, Lumiel, and Novarin.", ("legendary wizards", "legendary wizard", "legendary", "arden", "orphel", "lumiel", "novarin")),
    _chunk("arden", "ko", "아르덴", "Arden/아르덴은 Fire 계열 전설 마법사이며 폭발형 화염 damage dealer로 안내할 수 있습니다.", ("arden", "아르덴", "불 전설", "화염 전설")),
    _chunk("arden", "en", "Arden", "Arden is a Fire legendary wizard and an explosive fire damage dealer.", ("arden", "fire legendary", "explosive fire")),
    _chunk("orphel", "ko", "오르펠", "Orphel/오르펠은 Water 계열 전설 마법사이며 freeze/control type입니다.", ("orphel", "오르펠", "물 전설", "빙결")),
    _chunk("orphel", "en", "Orphel", "Orphel is a Water legendary wizard with freeze and control abilities.", ("orphel", "water legendary", "freeze", "control")),
    _chunk("lumiel", "ko", "루미엘", "Lumiel/루미엘은 Wind 계열 전설 마법사이며 support/blessing type입니다. 문서화되지 않은 회복 효과는 보장하지 않습니다.", ("lumiel", "루미엘", "바람 전설", "축복")),
    _chunk("lumiel", "en", "Lumiel", "Lumiel is a Wind legendary wizard and a support and blessing type. Undocumented healing is not guaranteed.", ("lumiel", "wind legendary", "support", "blessing")),
    _chunk("novarin", "ko", "노바린", "Novarin/노바린은 Lightning 계열 전설 마법사이며 special lightning type입니다.", ("novarin", "노바린", "번개 전설")),
    _chunk("novarin", "en", "Novarin", "Novarin is a Lightning legendary wizard and a special lightning type.", ("novarin", "lightning legendary", "special lightning")),
    _chunk("fusion", "ko", "마법사 Fusion", "Fusion은 서로 다른 원소의 서로 다른 마법사 두 명을 등록된 조합으로 합치는 시스템입니다. Fire + Water는 안개 계열 예시입니다.", ("fusion", "퓨전", "합성", "조합", "합치", "불 물", "fire water")),
    _chunk("fusion", "en", "Wizard fusion", "Fusion combines two different wizards of different elements when their pair is registered. Fire + Water is a mist-style example.", ("fusion", "combine", "combination", "fire water", "mist")),
    _chunk("resonance", "ko", "공명과 성장", "공명/resonance는 신규 획득과 구분되는 마법사 성장·강화 계열입니다. 정확한 수치와 보상은 현재 build 안내를 확인해야 합니다.", ("공명", "레조넌스", "resonance", "성장", "강화")),
    _chunk("resonance", "en", "Resonance and growth", "Resonance is a wizard growth and enhancement system separate from acquiring a new wizard. Check the current build for exact values.", ("resonance", "growth", "enhancement", "materials")),
    _chunk("tower_floors", "ko", "타워 층 진행", "타워 floor 진행은 현재 선택한 층, 완료 상태와 unlock 조건에 따라 달라집니다.", ("타워", "층", "다음 층", "해금", "floor", "tower")),
    _chunk("tower_floors", "en", "Tower floors", "Tower progression depends on the selected floor, completion state, and unlock conditions in the current build.", ("tower", "floor", "next floor", "unlock")),
    _chunk("boss", "ko", "보스 진행", "보스 층과 등장 시점은 현재 build의 tower/floor 진행 상태로 확인합니다. 미검증 일정이나 층을 확정하지 않습니다.", ("보스", "boss", "보스 층", "등장 시점")),
    _chunk("boss", "en", "Boss progression", "Check boss timing against tower and floor progression in the current build. Do not guarantee unverified schedules or boss floors.", ("boss", "boss floor", "boss timing", "schedule")),
    _chunk("pc_controls", "ko", "PC 배치 조작", "PC/Steam demo에서는 마우스로 한 번에 하나의 마법사를 드래그해 중앙 전장의 허용 범위 안에 배치합니다.", ("pc", "마우스", "드래그", "배치", "조작", "steam demo")),
    _chunk("pc_controls", "en", "PC placement controls", "On PC and in the Steam demo, drag one wizard at a time with the mouse inside the allowed central battlefield area.", ("pc controls", "place wizards", "mouse", "drag", "placement", "steam demo")),
    _chunk("fullscreen_resolution", "ko", "전체화면과 해상도", "UI 표시 문제는 windowed/fullscreen 전환, 해상도 재선택과 build 재실행을 확인하고 재현 정보와 screenshot을 남깁니다.", ("전체화면", "해상도", "화면", "ui", "fullscreen", "resolution"), requires_human_review=True),
    _chunk("fullscreen_resolution", "en", "Fullscreen and resolution", "For UI display issues, switch windowed/fullscreen mode, reselect the resolution, restart the build, and provide reproduction details and a screenshot.", ("fullscreen", "resolution", "screen", "ui", "broken ui"), requires_human_review=True),
    _chunk("reward_loss", "ko", "보상 또는 재화 손실", "보상이나 재화 손실은 자동 지급·보상·복구를 약속하지 않고 발생 시각, build와 screenshot을 받아 human review로 보냅니다.", ("보상", "미지급", "못 받", "재화", "사라", "손실"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("reward_loss", "en", "Reward or currency loss", "Do not promise grants, compensation, or restoration for missing rewards. Collect the time, build, and screenshot for human review.", ("reward", "did not receive", "missing reward", "lost", "currency"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("payment_issue", "ko", "결제 문제", "결제 또는 아이템 미지급은 환불·지급을 약속하지 않고 민감 결제정보를 요청하지 않으며 human review로 보냅니다.", ("결제", "구매", "아이템 미지급", "돈", "지급되지"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("payment_issue", "en", "Payment issue", "Do not promise a refund or item grant for payment issues and do not request sensitive payment data. Route the case to human review.", ("payment", "paid", "purchase", "did not receive the item", "missing item"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("refund_request", "ko", "환불 요청", "환불 가능 여부를 확정하거나 약속하지 않습니다. 플랫폼 정책 확인과 human review가 필요합니다.", ("환불", "refund", "돈 돌려", "취소"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("refund_request", "en", "Refund request", "Do not promise or guarantee a refund. The platform policy must be checked and the request requires human review.", ("refund", "want a refund", "money back", "cancel purchase"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("bug_report", "ko", "버그 신고", "버그 신고에는 재현 순서, floor/stage, 마법사 조합, build와 screenshot을 요청하며 수정이나 patch date를 보장하지 않습니다.", ("버그", "오류", "작동하지", "깨져", "재현", "튕김"), source_type="troubleshooting", requires_human_review=True),
    _chunk("bug_report", "en", "Bug report", "Request reproduction steps, floor or stage, wizard composition, build, and screenshot. Do not guarantee a fix or patch date.", ("bug", "error", "not working", "broken", "crash", "reproduce"), source_type="troubleshooting", requires_human_review=True),
    _chunk("safety_policy", "ko", "고객지원 안전 정책", "환불, 보상, 복구, guaranteed fix 또는 patch date를 약속하지 않습니다. 민감 사례는 human review로 전환합니다.", ("안전 정책", "약속", "human review", "사람 검토", "환불", "보상", "복구"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
    _chunk("safety_policy", "en", "Support safety policy", "Never promise refunds, compensation, restoration, guaranteed fixes, or patch dates. Route sensitive cases to human review.", ("safety policy", "human review", "promise", "refund", "compensation", "restoration"), source_type="safety_policy", safety_level="sensitive", requires_human_review=True),
)
