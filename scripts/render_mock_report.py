#!/usr/bin/env python3
"""Render a human-readable markdown report from a mock evidence package."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MOCK_ONLY_NOTICE = (
    "Mock-only notice: this report is generated from fictional sample data. "
    "It is for structure review and does not provide legal advice."
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
    return "none"


def distribution_text(events: list[dict[str, Any]], field: str) -> str:
    counter = Counter(str(event.get(field, "")) for event in events if event.get(field))
    if not counter:
        return "none"
    return ", ".join(f"{key}: {counter[key]}" for key in sorted(counter))


def linked_evidence_preview(
    event_id: str, evidence_by_event: dict[str, list[dict[str, Any]]]
) -> str:
    items = sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key)
    if not items:
        return "none"
    preview = [
        f"{item.get('evidenceId', '')} ({item.get('sourceType', '')})"
        for item in items[:3]
    ]
    if len(items) > 3:
        preview.append(f"+{len(items) - 3} more")
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
        f"# Mock Evidence Report: {data.get('packageId', '')}",
        "",
        f"> {MOCK_ONLY_NOTICE}",
        "",
        "## Summary",
        "",
        f"- Period: {data.get('periodStart', '')} to {data.get('periodEnd', '')}",
        f"- Subject role: {data.get('subjectRole', '')}",
        f"- Included events: {len(events)}",
        f"- Evidence items: {evidence_count}",
        f"- Excluded candidates: {len(excluded_candidates)}",
        f"- Quality gates: {distribution_text(sorted_events, 'qualityGate')}",
        f"- Evidence strength: {distribution_text(sorted_events, 'evidenceStrength')}",
        "",
        "## Event Overview",
        "",
        "| Event ID | Type | Work date | Duration | Strength | Gate | Risks |",
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
                    f"{event.get('durationMinutes', '')} min",
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
            "## Evidence Index Preview",
            "",
            "| Event ID | Linked evidence |",
            "| --- | --- |",
        ]
    )
    for event in sorted_events:
        event_id = str(event.get("eventId", ""))
        lines.append(f"| {event_id} | {linked_evidence_preview(event_id, evidence_by_event)} |")

    lines.extend(
        [
            "",
            "## Included Events",
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
                f"- Type: {event.get('eventType', '')}",
                f"- Work date: {event.get('workDate', '')}",
                f"- Time: {event.get('startTime', '')} to {event.get('endTime', '')}",
                f"- Duration minutes: {event.get('durationMinutes', '')}",
                f"- Evidence strength: {event.get('evidenceStrength', '')}",
                f"- Quality gate: {event.get('qualityGate', '')}",
                f"- Risk flags: {risk_flags_text}",
                f"- Review action: {event.get('reviewAction', '')}",
                f"- Summary: {event.get('workSummary', '')}",
                "- Evidence:",
            ]
        )
        for item in sorted(evidence_by_event.get(event_id, []), key=evidence_sort_key):
            lines.append(
                f"  - {item.get('evidenceId', '')}: {item.get('sourceType', '')}, "
                f"{item.get('sourceFileName', '')}:{item.get('sourceRowNum', '')}, "
                f"quickLocator `{item.get('quickLocator', '')}`"
            )
        lines.append("")

    if excluded_candidates:
        lines.extend(["## Excluded Candidates", ""])
        for candidate in excluded_candidates:
            lines.append(f"- {candidate.get('candidateId', '')}: {candidate.get('reason', '')}")
        lines.append("")

    lines.extend(["## Review Notes", ""])
    if needs_review:
        lines.append("The following mock events need human review before reuse:")
        lines.append("")
        for event in needs_review:
            event_id = event.get("eventId", "")
            reasons = []
            if event.get("qualityGate") != "pass":
                reasons.append(f"gate={event.get('qualityGate', '')}")
            risk_text = list_text(event.get("riskFlags", []))
            if risk_text != "none":
                reasons.append(f"risks={risk_text}")
            lines.append(f"- {event_id}: {', '.join(reasons)}")
    else:
        lines.append("No mock events are currently flagged beyond routine review.")
    lines.extend(
        [
            "",
            "This report is a structure preview only. It is not legal advice.",
            "",
            "## Boundaries",
            "",
            "- Uses mock-only data.",
            "- Does not include full source quotes, chat transcripts, recordings, source code, private delivery details, or legal conclusions.",
            "- Keep real case materials out of this repository, issues, pull requests, and discussions.",
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
