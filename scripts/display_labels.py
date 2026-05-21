"""Display labels for public human-facing mock outputs."""

from __future__ import annotations


EVENT_TYPE_LABELS = {
    "weekday_overtime": "\u5de5\u4f5c\u65e5\u52a0\u73ed",
    "release_night": "\u53d1\u5e03\u591c\u5904\u7406",
    "rest_day_task": "\u4f11\u606f\u65e5\u4efb\u52a1",
}
QUALITY_GATE_LABELS = {
    "pass": "\u901a\u8fc7",
    "needs_review": "\u9700\u590d\u6838",
}
RISK_FLAG_LABELS = {
    "single_source_only": "\u8bc1\u636e\u6765\u6e90\u5355\u4e00",
    "manual_review_required": "\u9700\u8981\u4eba\u5de5\u590d\u6838",
}
SOURCE_TYPE_LABELS = {
    "wechat": "\u5355\u804a",
    "group_chat": "\u7fa4\u804a",
    "git": "Git \u8bb0\u5f55",
}
EVIDENCE_STRENGTH_LABELS = {
    "strong": "\u5f3a",
    "medium": "\u4e2d",
    "weak": "\u5f31",
}


def display_label(mapping: dict[str, str], value: object) -> str:
    text = "" if value is None else str(value)
    return mapping.get(text, text)


def event_type_label(value: object) -> str:
    return display_label(EVENT_TYPE_LABELS, value)


def quality_gate_label(value: object) -> str:
    return display_label(QUALITY_GATE_LABELS, value)


def risk_flag_label(value: object) -> str:
    return display_label(RISK_FLAG_LABELS, value)


def source_type_label(value: object) -> str:
    return display_label(SOURCE_TYPE_LABELS, value)


def evidence_strength_label(value: object) -> str:
    return display_label(EVIDENCE_STRENGTH_LABELS, value)
