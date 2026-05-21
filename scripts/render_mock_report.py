#!/usr/bin/env python3
"""Render a human-readable markdown report from a mock evidence package."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
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

    lines = [
        f"# Mock Evidence Report: {data.get('packageId', '')}",
        "",
        f"> {MOCK_ONLY_NOTICE}",
        "",
        "## Package Summary",
        "",
        f"- Period: {data.get('periodStart', '')} to {data.get('periodEnd', '')}",
        f"- Subject role: {data.get('subjectRole', '')}",
        f"- Included events: {len(events)}",
        f"- Evidence items: {len(evidence_items) if isinstance(evidence_items, list) else 0}",
        f"- Excluded candidates: {len(excluded_candidates)}",
        "",
        "## Events",
        "",
    ]

    for event in sorted(events, key=event_sort_key):
        event_id = str(event.get("eventId", ""))
        risk_flags = event.get("riskFlags", [])
        if isinstance(risk_flags, list) and risk_flags:
            risk_flags_text = ", ".join(str(flag) for flag in risk_flags)
        else:
            risk_flags_text = "none"

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
                f"locator `{item.get('quickLocator', '')}`"
            )
        lines.append("")

    if excluded_candidates:
        lines.extend(["## Excluded Candidates", ""])
        for candidate in excluded_candidates:
            lines.append(f"- {candidate.get('candidateId', '')}: {candidate.get('reason', '')}")
        lines.append("")

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
