#!/usr/bin/env python3
"""Render a human-readable markdown report from a mock evidence package."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

from display_labels import (
    evidence_strength_label,
    event_type_label,
    quality_gate_label,
    risk_flag_label,
    source_type_label,
)


MOCK_ONLY_NOTICE = (
    "\u006d\u006f\u0063\u006b-\u006f\u006e\u006c\u0079 \u63d0\u9192\uff1a"
    "\u672c\u62a5\u544a\u7531\u5b8c\u5168\u865a\u6784\u7684\u6837\u4f8b\u6570\u636e\u751f\u6210\uff0c"
    "\u53ea\u7528\u4e8e\u7ed3\u6784\u6f14\u793a\u548c\u672c\u5730\u9a8c\u8bc1\uff0c"
    "\u4e0d\u63d0\u4f9b\u6cd5\u5f8b\u610f\u89c1\u3002"
)
NONE_TEXT = "\u65e0"


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


def list_text(
    values: Any, labeler: Callable[[object], str] | None = None
) -> str:
    if isinstance(values, list) and values:
        render = labeler or (lambda value: str(value))
        return ", ".join(render(value) for value in values)
    return NONE_TEXT


def distribution_text(
    events: list[dict[str, Any]],
    field: str,
    labeler: Callable[[object], str] | None = None,
) -> str:
    counter = Counter(str(event.get(field, "")) for event in events if event.get(field))
    if not counter:
        return NONE_TEXT
    render = labeler or (lambda value: str(value))
    return ", ".join(f"{render(key)}: {counter[key]}" for key in sorted(counter))


def linked_evidence_preview(
    event_id: str, evidence_by_event: dict[str, list[dict[str, Any]]]
) -> str:
    items = sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key)
    if not items:
        return NONE_TEXT
    preview = [
        f"{item.get('evidenceId', '')} ({source_type_label(item.get('sourceType', ''))})"
        for item in items[:3]
    ]
    if len(items) > 3:
        preview.append(f"+{len(items) - 3} \u9879")
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
        f"# Mock \u52a0\u73ed\u8bc1\u636e\u62a5\u544a\uff1a{data.get('packageId', '')}",
        "",
        f"> {MOCK_ONLY_NOTICE}",
        "",
        "## \u6458\u8981",
        "",
        f"- \u671f\u95f4\uff1a{data.get('periodStart', '')} \u81f3 {data.get('periodEnd', '')}",
        f"- \u4e3b\u4f53\u89d2\u8272\uff1a{data.get('subjectRole', '')}",
        f"- \u7eb3\u5165\u4e8b\u4ef6\u6570\uff1a{len(events)}",
        f"- \u8bc1\u636e\u9879\u6570\uff1a{evidence_count}",
        f"- \u6392\u9664\u5019\u9009\u6570\uff1a{len(excluded_candidates)}",
        f"- \u8d28\u91cf\u95e8\uff1a{distribution_text(sorted_events, 'qualityGate', quality_gate_label)}",
        f"- \u8bc1\u636e\u5f3a\u5ea6\uff1a{distribution_text(sorted_events, 'evidenceStrength', evidence_strength_label)}",
        "",
        "## \u4e8b\u4ef6\u6982\u89c8",
        "",
        "| \u4e8b\u4ef6ID | \u7c7b\u578b | \u65e5\u671f | \u65f6\u957f | \u5f3a\u5ea6 | \u8d28\u91cf\u95e8 | \u98ce\u9669 |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]

    for event in sorted_events:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(event.get("eventId", "")),
                    event_type_label(event.get("eventType", "")),
                    str(event.get("workDate", "")),
                    f"{event.get('durationMinutes', '')} \u5206\u949f",
                    evidence_strength_label(event.get("evidenceStrength", "")),
                    quality_gate_label(event.get("qualityGate", "")),
                    list_text(event.get("riskFlags", []), risk_flag_label),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## \u8bc1\u636e\u7d22\u5f15\u9884\u89c8",
            "",
            "| \u4e8b\u4ef6ID | \u5173\u8054\u8bc1\u636e |",
            "| --- | --- |",
        ]
    )
    for event in sorted_events:
        event_id = str(event.get("eventId", ""))
        lines.append(f"| {event_id} | {linked_evidence_preview(event_id, evidence_by_event)} |")

    lines.extend(["", "## \u7eb3\u5165\u4e8b\u4ef6", ""])

    for event in sorted_events:
        event_id = str(event.get("eventId", ""))
        risk_flags_text = list_text(event.get("riskFlags", []), risk_flag_label)

        lines.extend(
            [
                f"### {event_id}",
                "",
                f"- \u7c7b\u578b\uff1a{event_type_label(event.get('eventType', ''))}",
                f"- \u65e5\u671f\uff1a{event.get('workDate', '')}",
                f"- \u65f6\u95f4\uff1a{event.get('startTime', '')} \u81f3 {event.get('endTime', '')}",
                f"- \u65f6\u957f\u5206\u949f\uff1a{event.get('durationMinutes', '')}",
                f"- \u8bc1\u636e\u5f3a\u5ea6\uff1a{evidence_strength_label(event.get('evidenceStrength', ''))}",
                f"- \u8d28\u91cf\u95e8\uff1a{quality_gate_label(event.get('qualityGate', ''))}",
                f"- \u98ce\u9669\u6807\u8bb0\uff1a{risk_flags_text}",
                f"- \u590d\u6838\u52a8\u4f5c\uff1a{event.get('reviewAction', '')}",
                f"- \u6458\u8981\uff1a{event.get('workSummary', '')}",
                "- \u8bc1\u636e\uff1a",
            ]
        )
        for item in sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key):
            lines.append(
                f"  - {item.get('evidenceId', '')}: "
                f"{source_type_label(item.get('sourceType', ''))}, "
                f"{item.get('sourceFileName', '')}:{item.get('sourceRowNum', '')}, "
                f"\u5feb\u901f\u5b9a\u4f4d `{item.get('quickLocator', '')}`"
            )
        lines.append("")

    if excluded_candidates:
        lines.extend(["## \u6392\u9664\u5019\u9009", ""])
        for candidate in excluded_candidates:
            lines.append(f"- {candidate.get('candidateId', '')}: {candidate.get('reason', '')}")
        lines.append("")

    lines.extend(["## \u590d\u6838\u63d0\u793a", ""])
    if needs_review:
        lines.append("\u4ee5\u4e0b mock events \u5728\u590d\u7528\u524d\u9700\u8981\u4eba\u5de5\u590d\u6838\uff1a")
        lines.append("")
        for event in needs_review:
            event_id = event.get("eventId", "")
            reasons = []
            if event.get("qualityGate") != "pass":
                reasons.append(f"\u8d28\u91cf\u95e8={quality_gate_label(event.get('qualityGate', ''))}")
            risk_text = list_text(event.get("riskFlags", []), risk_flag_label)
            if risk_text != NONE_TEXT:
                reasons.append(f"\u98ce\u9669={risk_text}")
            lines.append(f"- {event_id}: {', '.join(reasons)}")
    else:
        lines.append("\u5f53\u524d\u6ca1\u6709\u8d85\u51fa\u5e38\u89c4\u590d\u6838\u8303\u56f4\u7684 mock events\u3002")
    lines.extend(
        [
            "",
            "\u672c\u62a5\u544a\u53ea\u7528\u4e8e\u7ed3\u6784\u9884\u89c8\uff0c\u4e0d\u662f\u6cd5\u5f8b\u610f\u89c1\u3002",
            "",
            "## \u8fb9\u754c\u8bf4\u660e",
            "",
            "- \u4ec5\u4f7f\u7528 mock-only \u6570\u636e\u3002",
            "- \u4e0d\u5305\u542b\u5b8c\u6574\u804a\u5929\u539f\u6587\u3001\u5f55\u97f3\u8f6c\u5199\u3001\u6e90\u7801\u3001\u79c1\u6709\u4ea4\u4ed8\u6d41\u7a0b\u6216\u6cd5\u5f8b\u7ed3\u8bba\u3002",
            "- \u4e0d\u8981\u5728\u672c\u4ed3\u5e93\u3001issue\u3001PR \u6216 discussion \u4e2d\u63d0\u4ea4\u771f\u5b9e\u6848\u4ef6\u6750\u6599\u3002",
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
