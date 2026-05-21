#!/usr/bin/env python3
"""Render a human-readable markdown report from a mock evidence package."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MOCK_ONLY_NOTICE = (
    "mock-only 提醒：本报告由完全虚构的样例数据生成，"
    "只用于结构演示和本地验证，不提供法律意见。"
)


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("package root must be a JSON object")
    return data


def event_sort_key(event: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(event.get("workDate", "")),
        str(event.get("startTime", "")),
        str(event.get("eventId", "")),
    )


def evidence_sort_key(item: dict[str, Any]) -> tuple[str, str]:
    return (str(item.get("timestamp", "")), str(item.get("evidenceId", "")))


def list_text(values: Any) -> str:
    if isinstance(values, list) and values:
        return ", ".join(str(value) for value in values)
    return "无"


def distribution_text(events: list[dict[str, Any]], field: str) -> str:
    counter = Counter(str(event.get(field, "")) for event in events if event.get(field))
    if not counter:
        return "无"
    return ", ".join(f"{key}: {counter[key]}" for key in sorted(counter))


def linked_evidence_preview(
    event_id: str, evidence_by_event: dict[str, list[dict[str, Any]]]
) -> str:
    items = sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key)
    if not items:
        return "无"
    preview = [
        f"{item.get('evidenceId', '')} ({item.get('sourceType', '')})"
        for item in items[:3]
    ]
    if len(items) > 3:
        preview.append(f"+{len(items) - 3} 项")
    return "; ".join(preview)


def render_report(data: dict[str, Any]) -> str:
    evidence_by_event: dict[str, list[dict[str, Any]]] = defaultdict(list)
    evidence_items = data.get("evidenceItems", [])
    if isinstance(evidence_items, list):
        for item in evidence_items:
            if isinstance(item, dict):
                evidence_by_event[str(item.get("eventId", ""))].append(item)

    events = [item for item in data.get("events", []) if isinstance(item, dict)]
    excluded_candidates = [
        item for item in data.get("excludedCandidates", []) if isinstance(item, dict)
    ]

    sorted_events = sorted(events, key=event_sort_key)
    evidence_count = len(evidence_items) if isinstance(evidence_items, list) else 0

    needs_review = [
        event
        for event in sorted_events
        if event.get("qualityGate") != "pass" or event.get("riskFlags")
    ]

    lines = [
        f"# Mock 加班证据报告：{data.get('packageId', '')}",
        "",
        f"> {MOCK_ONLY_NOTICE}",
        "",
        "## 摘要",
        "",
        f"- 期间：{data.get('periodStart', '')} 至 {data.get('periodEnd', '')}",
        f"- 主体角色：{data.get('subjectRole', '')}",
        f"- 纳入事件数：{len(events)}",
        f"- 证据项数：{evidence_count}",
        f"- 排除候选数：{len(excluded_candidates)}",
        f"- 质量门：{distribution_text(sorted_events, 'qualityGate')}",
        f"- 证据强度：{distribution_text(sorted_events, 'evidenceStrength')}",
        "",
        "## 事件概览",
        "",
        "| 事件ID | 类型 | 日期 | 时长 | 强度 | 质量门 | 风险 |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]

    for event in sorted_events:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(event.get("eventId", "")),
                    str(event.get("eventType", "")),
                    str(event.get("workDate", "")),
                    f"{event.get('durationMinutes', '')} 分钟",
                    str(event.get("evidenceStrength", "")),
                    str(event.get("qualityGate", "")),
                    list_text(event.get("riskFlags", [])),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 证据索引预览",
            "",
            "| 事件ID | 关联证据 |",
            "| --- | --- |",
        ]
    )
    for event in sorted_events:
        event_id = str(event.get("eventId", ""))
        lines.append(f"| {event_id} | {linked_evidence_preview(event_id, evidence_by_event)} |")

    lines.extend(
        [
            "",
            "## 纳入事件",
            "",
        ]
    )

    for event in sorted_events:
        event_id = str(event.get("eventId", ""))
        risk_flags_text = list_text(event.get("riskFlags", []))

        lines.extend(
            [
                f"### {event_id}",
                "",
                f"- 类型：{event.get('eventType', '')}",
                f"- 日期：{event.get('workDate', '')}",
                f"- 时间：{event.get('startTime', '')} 至 {event.get('endTime', '')}",
                f"- 时长分钟：{event.get('durationMinutes', '')}",
                f"- 证据强度：{event.get('evidenceStrength', '')}",
                f"- 质量门：{event.get('qualityGate', '')}",
                f"- 风险标记：{risk_flags_text}",
                f"- 复核动作：{event.get('reviewAction', '')}",
                f"- 摘要：{event.get('workSummary', '')}",
                "- 证据：",
            ]
        )
        for item in sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key):
            lines.append(
                f"  - {item.get('evidenceId', '')}: {item.get('sourceType', '')}, "
                f"{item.get('sourceFileName', '')}:{item.get('sourceRowNum', '')}, "
                f"快速定位 `{item.get('quickLocator', '')}`"
            )
        lines.append("")

    if excluded_candidates:
        lines.extend(["## 排除候选", ""])
        for candidate in excluded_candidates:
            lines.append(f"- {candidate.get('candidateId', '')}: {candidate.get('reason', '')}")
        lines.append("")

    lines.extend(["## 复核提示", ""])
    if needs_review:
        lines.append("以下 mock events 在复用前需要人工复核：")
        lines.append("")
        for event in needs_review:
            event_id = event.get("eventId", "")
            reasons = []
            if event.get("qualityGate") != "pass":
                reasons.append(f"gate={event.get('qualityGate', '')}")
            risk_text = list_text(event.get("riskFlags", []))
            if risk_text != "无":
                reasons.append(f"risks={risk_text}")
            lines.append(f"- {event_id}: {', '.join(reasons)}")
    else:
        lines.append("当前没有超出常规复核范围的 mock events。")
    lines.extend(
        [
            "",
            "本报告只用于结构预览，不是法律意见。",
            "",
            "## 边界说明",
            "",
            "- 仅使用 mock-only 数据。",
            "- 不包含完整聊天原文、录音转写、源码、私有交付流程或法律结论。",
            "- 不要在本仓库、issue、PR 或 discussion 中提交真实案件材料。",
            "",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: render_mock_report.py <package.json>", file=sys.stderr)
        return 2
    try:
        data = load_package(Path(argv[1]))
        print(render_report(data), end="")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
