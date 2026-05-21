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
    "\u8bc1\u636eID",
    "\u4e8b\u4ef6ID",
    "\u4e8b\u4ef6\u7c7b\u578b",
    "\u65e5\u671f",
    "\u6765\u6e90\u7c7b\u578b",
    "\u6765\u6e90\u6587\u4ef6",
    "\u6765\u6e90\u884c\u53f7",
    "\u6d88\u606fID",
    "\u5feb\u901f\u5b9a\u4f4d",
    "\u8131\u654f\u7ea7\u522b",
]
PACKAGE_FIELD_BY_CSV_FIELD = {
    "\u8bc1\u636eID": "evidenceId",
    "\u4e8b\u4ef6ID": "eventId",
    "\u4e8b\u4ef6\u7c7b\u578b": "eventType",
    "\u65e5\u671f": "workDate",
    "\u6765\u6e90\u7c7b\u578b": "sourceType",
    "\u6765\u6e90\u6587\u4ef6": "sourceFileName",
    "\u6765\u6e90\u884c\u53f7": "sourceRowNum",
    "\u6d88\u606fID": "messageId",
    "\u5feb\u901f\u5b9a\u4f4d": "quickLocator",
    "\u8131\u654f\u7ea7\u522b": "redactionLevel",
}
PACKAGE_FIELDS = [
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
        package_row = {field: item.get(field, "") for field in PACKAGE_FIELDS}
        if isinstance(event, dict):
            package_row["eventType"] = event.get("eventType", "")
            package_row["workDate"] = event.get("workDate", "")
        row = {
            csv_field: package_row.get(package_field, "")
            for csv_field, package_field in PACKAGE_FIELD_BY_CSV_FIELD.items()
        }
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
