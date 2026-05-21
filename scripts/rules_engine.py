#!/usr/bin/env python3
"""Mock-only rules engine for evidence package quality fields."""

from __future__ import annotations

import copy
import json
import re
from datetime import datetime
from typing import Any


PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_RE = re.compile(r"\b\d{17}[\dXx]\b")
REAL_COMMIT_RE = re.compile(r"(?<!mock-)(?<!schema-)\b[0-9a-fA-F]{7,40}\b")


def source_type_set(evidence_items: list[dict[str, Any]]) -> set[str]:
    return {
        str(item.get("sourceType", ""))
        for item in evidence_items
        if isinstance(item.get("sourceType"), str) and item.get("sourceType")
    }


def has_task_source(evidence_items: list[dict[str, Any]]) -> bool:
    task_roles = {"task_source", "release_coordination"}
    return any(item.get("evidenceRole") in task_roles for item in evidence_items)


def has_result_evidence(evidence_items: list[dict[str, Any]]) -> bool:
    result_roles = {"work_result", "git_output"}
    return any(item.get("evidenceRole") in result_roles for item in evidence_items)


def contains_sensitive_pattern(value: Any) -> bool:
    serialized = json.dumps(value, ensure_ascii=False)
    phone_cleaned = PHONE_RE.sub("", serialized)
    return bool(
        PHONE_RE.search(serialized)
        or ID_CARD_RE.search(serialized)
        or REAL_COMMIT_RE.search(phone_cleaned)
    )


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def event_has_valid_time_range(event: dict[str, Any]) -> bool:
    start = parse_datetime(event.get("startTime"))
    end = parse_datetime(event.get("endTime"))
    return start is not None and end is not None and start < end


def evaluate_event(event: dict[str, Any], evidence_items: list[dict[str, Any]]) -> dict[str, Any]:
    risk_flags: list[str] = []
    sources = source_type_set(evidence_items)
    task_source = has_task_source(evidence_items)
    result_evidence = has_result_evidence(evidence_items)

    if not event_has_valid_time_range(event):
        risk_flags.append("missing_end_time")
    if len(sources) == 1:
        risk_flags.append("single_source_only")
    if not result_evidence:
        risk_flags.append("weak_result_evidence")
    if event.get("eventType") == "rest_day_task":
        risk_flags.append("manual_review_required")
    if contains_sensitive_pattern({"event": event, "evidenceItems": evidence_items}):
        risk_flags.append("sensitive_content_present")

    if len(evidence_items) >= 2 and len(sources) >= 2 and task_source and result_evidence:
        evidence_strength = "strong"
    elif len(evidence_items) >= 2 and (task_source or result_evidence):
        evidence_strength = "medium"
    else:
        evidence_strength = "weak"

    high_risk_flags = {"missing_end_time", "sensitive_content_present"}
    review_flags = {"single_source_only", "weak_result_evidence", "manual_review_required"}
    if evidence_strength == "weak" or any(flag in risk_flags for flag in high_risk_flags):
        quality_gate = "blocked"
    elif evidence_strength == "medium" or any(flag in risk_flags for flag in review_flags):
        quality_gate = "needs_review"
    else:
        quality_gate = "pass"

    unique_risk_flags = list(dict.fromkeys(risk_flags))
    return {
        "evidenceStrength": evidence_strength,
        "qualityGate": quality_gate,
        "riskFlags": unique_risk_flags,
        "reviewAction": build_review_action(event, unique_risk_flags, evidence_strength),
    }


def build_review_action(
    event: dict[str, Any], risk_flags: list[str], evidence_strength: str
) -> str:
    if "sensitive_content_present" in risk_flags:
        return "移除或泛化敏感内容后再公开。"
    if "missing_end_time" in risk_flags:
        return "补充 mock 起止时间并重新运行规则评价。"
    if "manual_review_required" in risk_flags:
        return "人工确认休息日任务来源和处理结果是否足够。"
    if "single_source_only" in risk_flags:
        return "补充另一类 mock 来源，例如 Git、群聊或系统截图索引。"
    if "weak_result_evidence" in risk_flags:
        return "补充处理结果或产出确认记录。"
    if evidence_strength == "strong":
        return "复核 mock 时间线与多来源证据是否一致。"
    return f"人工复核 {event.get('eventId', 'mock event')} 的证据链是否完整。"


def evaluate_package(package: dict[str, Any]) -> dict[str, Any]:
    evaluated = copy.deepcopy(package)
    evidence_by_event: dict[str, list[dict[str, Any]]] = {}
    for item in evaluated.get("evidenceItems", []):
        if isinstance(item, dict) and isinstance(item.get("eventId"), str):
            evidence_by_event.setdefault(item["eventId"], []).append(item)

    for event in evaluated.get("events", []):
        if not isinstance(event, dict):
            continue
        event_id = event.get("eventId")
        linked_evidence = evidence_by_event.get(event_id, [])
        event.update(evaluate_event(event, linked_evidence))
    return evaluated
