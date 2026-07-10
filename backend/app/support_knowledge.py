"""Deterministic support knowledge for player question coverage.

The support preview is a rule-based baseline. This module does not call LLM APIs,
external APIs, account systems, payment systems, or helpdesk integrations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class KnowledgeMatch:
    subtopic: str
    response_ko: str
    response_en: str
    note_ko: str
    note_en: str
    needs_human_review: bool = False


ELEMENTS = "Fire, Water, Wind, Stone, Lightning"
LEGENDARY_NAMES = "Arden, Orphel, Lumiel, Novarin"


def _has_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _safe_review(subtopic: str, ko_intro: str, en_intro: str) -> KnowledgeMatch:
    return KnowledgeMatch(
        subtopic=subtopic,
        response_ko=(
            ko_intro
            + " 발생 상황, 시점, 빌드, 스크린샷을 함께 남겨 주세요. "
            + "이 preview는 환불, 보상, 복구, 해결 시점을 약속하지 않고 사람이 검토할 수 있도록 정리합니다."
        ),
        response_en=(
            en_intro
            + " Please include the situation, time, build, and screenshot for review. "
            + "This preview does not promise refunds, compensation, restoration, certain fixes, or patch dates."
        ),
        note_ko="손실/결제/환불성 문의이므로 보상, 복구, 환불을 약속하지 않는 human review tone을 사용합니다.",
        note_en="Loss/payment/refund inquiry: use human review wording without promising compensation, restoration, or refund.",
        needs_human_review=True,
    )


def detect_support_knowledge(text: str) -> KnowledgeMatch | None:
    """Return a deterministic knowledge match for a player inquiry."""
    normalized = text.strip()

    if _has_any(normalized, [
        "refund", "payment", "paid", "did not receive", "reward", "lost", "compensation", "restore", "restoration",
        "보상", "결제", "환불", "복구", "미지급", "사라", "잃어", "?섎텋", "寃곗젣", "蹂댁긽", "紐?諛쏆", "?щ씪", "?ㅼ뼱",
    ]):
        if _has_any(normalized, ["resonance", "material", "materials", "공명", "재료", "?덉“", "?щ즺"]):
            return _safe_review(
                "reward_loss_safe_reply",
                "공명/resonance 재료가 사라진 것처럼 보인다면 자동 확정 답변보다 human review로 다루는 것이 안전합니다.",
                "If resonance or growth materials appear to be lost, this should be handled as a human review case rather than an automatic final answer.",
            )
        if _has_any(normalized, ["refund", "payment", "paid", "결제", "환불", "寃곗젣", "?섎텋"]):
            return _safe_review(
                "payment_refund_safe_reply",
                "결제, 환불, 아이템 미지급 문의는 자동으로 환불이나 지급을 약속하지 않고 human review로 접수해야 합니다.",
                "Payment, refund, or missing item inquiries should be handled by human review without promising a refund or item grant.",
            )
        return _safe_review(
            "bug_report_safe_reply",
            "보상 또는 진행 손실 가능성이 있는 문의는 자동 확정 답변보다 human review로 다루는 것이 안전합니다.",
            "Reward or progression loss reports should be handled by human review rather than an automatic final answer.",
        )

    if _has_any(normalized, ["fullscreen", "resolution", "screen", "ui", "전체화면", "해상도", "화면", "?꾩껜", "?붾㈃", "?댁긽", "源⑥ 졇", "源⑥졇"]):
        return KnowledgeMatch(
            subtopic="fullscreen_resolution",
            response_ko=(
                "전체화면, 해상도, UI 표시 문제가 있으면 먼저 windowed/fullscreen 전환, 해상도 재선택, "
                "Steam demo 또는 Windows build 재실행을 확인해 주세요. 계속 재현되면 PC 해상도, fullscreen/windowed 상태, "
                "스크린샷과 재현 순서를 함께 보내 주시면 검토에 도움이 됩니다."
            ),
            response_en=(
                "For fullscreen, resolution, or UI layout issues, first try switching between windowed and fullscreen mode, "
                "reselecting the resolution, and restarting the Steam demo or Windows build. If it continues, include PC resolution, "
                "fullscreen/windowed state, a screenshot, and reproduction steps."
            ),
            note_ko="화면 표시 문제는 PC 해상도와 fullscreen/windowed 상태를 함께 확인하도록 안내합니다.",
            note_en="Display issue: request PC resolution plus fullscreen/windowed state.",
            needs_human_review=True,
        )

    if _has_any(normalized, ["pc", "mouse", "drag", "place", "placement", "control", "steam demo", "마우스", "드래그", "배치", "조작", "留덉슦", "?쒕옒", "諛곗튂", "議곗옉"]):
        return KnowledgeMatch(
            subtopic="pc_controls",
            response_ko=(
                "PC / Steam demo 기준으로 마법사는 mouse click 후 drag placement 방식으로 중앙 전장 영역 안에서 배치합니다. "
                "Unity WizardDragController.cs 기준으로 한 번에 하나의 wizard만 드래그하고, 지정된 이동 가능 범위 안에서 위치가 제한됩니다."
            ),
            response_en=(
                "In the PC / Steam demo context, wizards are placed with mouse-based drag placement inside the central battlefield area. "
                "Based on WizardDragController.cs, one wizard is dragged at a time and movement is clamped to the allowed placement range."
            ),
            note_ko="Unity WizardDragController.cs에서 mouse input, drag placement, 이동 범위 제한을 확인했습니다.",
            note_en="Confirmed mouse input, drag placement, and clamped movement from Unity WizardDragController.cs.",
        )

    if _has_any(normalized, ["boss", "보스", "floor", "tower", "unlock", "next floor", "층", "타워", "해금", "蹂댁뒪", "痢", "?ㅼ쓬"]):
        if _has_any(normalized, ["boss", "보스", "蹂댁뒪"]):
            return KnowledgeMatch(
                subtopic="boss_schedule",
                response_ko=(
                    "보스 층이나 등장 시점은 현재 build의 tower/floor 진행 상태와 연결해 확인해야 합니다. "
                    "이 preview에서는 정확한 live release 일정이나 보스 등장 층을 확정하지 않고, 진행 중인 floor와 완료 상태를 함께 확인하도록 안내합니다."
                ),
                response_en=(
                    "Boss timing should be checked against the tower/floor progress in the current build. "
                    "This preview does not guarantee exact live release behavior or a fixed boss-floor schedule; check the current floor and completion state."
                ),
                note_ko="Tower 관련 문의는 확정 일정이나 미검증 보스 층을 약속하지 않습니다.",
                note_en="Tower/boss reply avoids promising exact schedules or unverified boss floors.",
            )
        return KnowledgeMatch(
            subtopic="tower_floors",
            response_ko=(
                "타워 floor 진행은 현재 선택한 floor, 완료 상태, unlock 조건에 따라 달라질 수 있습니다. "
                "다음 층이 열리지 않으면 현재 floor 완료 여부와 build 내 안내를 먼저 확인해 주세요."
            ),
            response_en=(
                "Tower floor progression depends on the selected floor, completion state, and unlock conditions in the current build. "
                "If the next floor is not unlocked, first check whether the current floor is completed and review the in-game guidance."
            ),
            note_ko="TowerFloor/TowerProgress 계열 구현이 있어 floor 진행 안내는 일반 조건 중심으로 제공합니다.",
            note_en="TowerFloor/TowerProgress scripts exist; keep floor guidance general and condition-based.",
        )

    if _has_any(normalized, ["fusion", "combine", "combination", "합성", "조합", "?듯빀", "議고빀", "⑹튂", "fire and water", "遺덉씠", "遺", "臾"]):
        asks_fire_water = _has_any(normalized, ["fire and water", "fire + water", "遺덉씠", "遺", "臾"])
        ko_example = "Fire + Water는 지원되는 fusion pair 중 하나이며 mist/안개 계열 fusion 예시로 안내할 수 있습니다." if asks_fire_water else "지원되는 pair는 서로 다른 element 조합을 기준으로 처리됩니다."
        en_example = "Fire + Water is one supported fusion pair and can be described as a mist-style fusion example." if asks_fire_water else "Supported pairs are handled as different-element combinations."
        return KnowledgeMatch(
            subtopic="fusion_examples" if asks_fire_water else "fusion",
            response_ko=(
                "Fusion은 서로 다른 두 element wizard를 선택해 조합을 시도하는 deterministic gameplay system입니다. "
                "같은 wizard 또는 같은 element끼리는 조합하지 않으며, 등록된 pair가 있을 때 fusion wizard가 생성됩니다. " + ko_example
            ),
            response_en=(
                "Fusion is a deterministic gameplay system where two different element wizards are selected and combined. "
                "The same wizard or the same element cannot be fused, and a fusion wizard is created only when the pair is registered. " + en_example
            ),
            note_ko="Unity WizardFusionManager.cs에서 서로 다른 element pair와 prefab 기반 fusion 처리를 확인했습니다.",
            note_en="Confirmed different-element pair fusion and prefab lookup from Unity WizardFusionManager.cs.",
        )

    if _has_any(normalized, ["resonance", "공명", "성장", "강화", "?덉“", "怨듬챸"]):
        return KnowledgeMatch(
            subtopic="resonance",
            response_ko=(
                "공명/resonance는 마법사 성장 또는 강화 계열로 안내하는 것이 안전합니다. "
                "신규 마법사 획득과는 구분되는 성장 시스템이며, 정확한 수치나 보상 결과는 현재 build의 안내를 기준으로 확인해야 합니다."
            ),
            response_en=(
                "Resonance is best described as a wizard growth or enhancement system. "
                "It is separate from acquiring a new wizard, and exact values or reward outcomes should be checked in the current build."
            ),
            note_ko="공명은 성장 계열 안내로 처리하고 수치/보상 확정 약속은 피합니다.",
            note_en="Treat resonance as growth guidance and avoid promising exact values or rewards.",
        )

    if _has_any(normalized, ["arden", "아르덴", "?꾨Ⅴ"]):
        return KnowledgeMatch(
            subtopic="arden",
            response_ko="Arden은 Fire 계열 전설 마법사이며 explosive fire damage dealer로 안내할 수 있습니다.",
            response_en="Arden is a Fire legendary wizard and can be described as an explosive fire damage dealer.",
            note_ko="Unity LegendaryWizard.cs에서 Arden -> Fire 매핑을 확인했습니다.",
            note_en="Confirmed Arden -> Fire mapping from Unity LegendaryWizard.cs.",
        )

    if _has_any(normalized, ["orphel", "오르펠", "?ㅻⅤ"]):
        return KnowledgeMatch(
            subtopic="orphel",
            response_ko="Orphel은 Water 계열 전설 마법사이며 freeze/control type으로 안내할 수 있습니다.",
            response_en="Orphel is a Water legendary wizard and can be described as a freeze/control type.",
            note_ko="Unity LegendaryWizard.cs와 Orphel freeze skill 파일을 기준으로 freeze/control 톤으로 안내합니다.",
            note_en="Use freeze/control wording based on LegendaryWizard.cs and Orphel freeze skill files.",
        )

    if _has_any(normalized, ["lumiel", "루미엘", "猷⑤"]):
        return KnowledgeMatch(
            subtopic="lumiel",
            response_ko="Lumiel은 Wind 계열 전설 마법사이며 support and blessing type입니다. 문서화되지 않은 치유량이나 회복 효과는 확정하지 않습니다.",
            response_en="Lumiel is a Wind legendary wizard and a support and blessing type. This preview does not promise undocumented healing or guaranteed recovery effects.",
            note_ko="Lumiel blessing 파일은 확인했지만 미문서화 치유 보장은 하지 않습니다.",
            note_en="Lumiel blessing files exist, but avoid promising undocumented healing.",
        )

    if _has_any(normalized, ["novarin", "노바린", "?몃컮"]):
        return KnowledgeMatch(
            subtopic="novarin",
            response_ko="Novarin은 Lightning 계열 전설 마법사이며 special lightning type으로 안내할 수 있습니다.",
            response_en="Novarin is a Lightning legendary wizard and can be described as a special lightning type.",
            note_ko="Unity LegendaryWizard.cs에서 Novarin -> Lightning 매핑을 확인했습니다.",
            note_en="Confirmed Novarin -> Lightning mapping from Unity LegendaryWizard.cs.",
        )

    if _has_any(normalized, ["legendary", "전설", "?꾩꽕"]):
        return KnowledgeMatch(
            subtopic="legendary_wizards",
            response_ko=(
                "전설 마법사는 Arden, Orphel, Lumiel, Novarin으로 정리할 수 있습니다. "
                "Arden은 Fire 계열 explosive fire damage dealer, Orphel은 Water 계열 freeze/control type, "
                "Lumiel은 Wind 계열 support and blessing type, Novarin은 Lightning 계열 special lightning type입니다."
            ),
            response_en=(
                "The legendary wizards are Arden, Orphel, Lumiel, and Novarin. "
                "Arden is an explosive Fire damage dealer, Orphel is a freeze/control type, "
                "Lumiel is a support and blessing type, and Novarin is a special Lightning type."
            ),
            note_ko="Unity LegendaryWizard.cs에서 Arden, Orphel, Lumiel, Novarin enum과 원소 매핑을 확인했습니다.",
            note_en="Confirmed from Unity LegendaryWizard.cs: Arden, Orphel, Lumiel, and Novarin with element mapping.",
        )

    if _has_any(normalized, ["element", "elements", "wizard type", "wizard types", "how many wizard", "what wizard", "fire wizard", "lightning wizard", "속성", "종류", "마법사", "?띿꽦", "留덈쾿", "醫낅쪟", "萸먮춴"]):
        return KnowledgeMatch(
            subtopic="wizard_elements",
            response_ko=(
                f"기본 wizard element/type은 {ELEMENTS} 다섯 가지입니다. "
                "Unity WizardElement.cs 기준으로 Fire, Water, Wind, Stone, Lightning enum과 element별 wizard sprite 적용이 확인됩니다."
            ),
            response_en=(
                f"The basic wizard element/types are {ELEMENTS}. "
                "Based on Unity WizardElement.cs, the game defines Fire, Water, Wind, Stone, and Lightning and applies a wizard sprite per element."
            ),
            note_ko="Unity WizardElement.cs의 WizardElementType enum을 근거로 답변합니다.",
            note_en="Answer is based on the WizardElementType enum in Unity WizardElement.cs.",
        )

    return None


def build_knowledge_response(text: str, language: str = "ko") -> dict[str, object] | None:
    """Build a deterministic response override for detected support knowledge."""
    match = detect_support_knowledge(text)
    if match is None:
        return None
    selected_language = "en" if language == "en" else "ko"
    if selected_language == "en":
        return {
            "subtopic": match.subtopic,
            "response_draft": match.response_en,
            "internal_note": f"Knowledge topic: {match.subtopic}. {match.note_en}",
            "needs_human_review": match.needs_human_review,
        }
    return {
        "subtopic": match.subtopic,
        "response_draft": match.response_ko,
        "internal_note": f"Knowledge topic: {match.subtopic}. {match.note_ko}",
        "needs_human_review": match.needs_human_review,
    }