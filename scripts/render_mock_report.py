#!/usr/bin/env python3
"""Render a human-readable markdown report from a mock evidence package."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_report(data: dict[str, Any]) -> str:
    evidence_by_event: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in data.get("evidenceItems", []):
        evidence_by_event[item.get("eventId", "")].append(item)

    lines = [
        f"# Mock Evidence Report: {data.get('packageId', '')}",
        "",
        f"- Period: {data.get('periodStart', '')} to {data.get('periodEnd', '')}",
        f"- Subject role: {data.get('subjectRole', '')}",
        "",
        "## Events",
        "",
    ]

    for event in data.get("events", []):
        event_id = event.get("eventId", "")
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
                f"- Summary: {event.get('workSummary', '')}",
                "- Evidence:",
            ]
        )
        for item in evidence_by_event.get(event_id, []):
            lines.append(
                f"  - {item.get('evidenceId', '')}: {item.get('sourceType', '')}, "
                f"{item.get('sourceFileName', '')}, locator `{item.get('quickLocator', '')}`"
            )
        lines.append("")

    if data.get("excludedCandidates"):
        lines.extend(["## Excluded Candidates", ""])
        for candidate in data["excludedCandidates"]:
            lines.append(f"- {candidate.get('candidateId', '')}: {candidate.get('reason', '')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: render_mock_report.py <package.json>", file=sys.stderr)
        return 2
    data = load_package(Path(argv[1]))
    print(render_report(data), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

