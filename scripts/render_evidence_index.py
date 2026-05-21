#!/usr/bin/env python3
"""Render a CSV evidence index from a mock evidence package."""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path
from typing import Any


CSV_FIELDS = [
    "evidenceId",
    "eventId",
    "eventType",
    "workDate",
    "sourceType",
    "sourceFileName",
    "sourceRowNum",
    "messageId",
    "quickLocator",
    "redactionLevel",
]


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("package root must be a JSON object")
    return data


def evidence_sort_key(item: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(item.get("eventId", "")),
        str(item.get("timestamp", "")),
        str(item.get("evidenceId", "")),
    )


def render_index(data: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    events_by_id = {
        event.get("eventId"): event
        for event in data.get("events", [])
        if isinstance(event, dict)
    }
    evidence_items = [
        item for item in data.get("evidenceItems", []) if isinstance(item, dict)
    ]
    for item in sorted(evidence_items, key=evidence_sort_key):
        event = events_by_id.get(item.get("eventId"), {})
        row = {field: item.get(field, "") for field in CSV_FIELDS}
        if isinstance(event, dict):
            row["eventType"] = event.get("eventType", "")
            row["workDate"] = event.get("workDate", "")
        writer.writerow(row)
    return output.getvalue()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: render_evidence_index.py <package.json>", file=sys.stderr)
        return 2
    try:
        data = load_package(Path(argv[1]))
        print(render_index(data), end="")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
