#!/usr/bin/env python3
"""Validate a mock overtime evidence package."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EVENT_REQUIRED = {
    "eventId",
    "workDate",
    "eventType",
    "startTime",
    "endTime",
    "durationMinutes",
    "multiplier",
    "claimAmount",
    "workSummary",
    "evidenceStrength",
    "qualityGate",
    "riskFlags",
    "reviewAction",
}

EVIDENCE_REQUIRED = {
    "evidenceId",
    "eventId",
    "sourceType",
    "sourceFileName",
    "sourceRowNum",
    "messageId",
    "timestamp",
    "senderRole",
    "sourceQuote",
    "quickLocator",
    "redactionLevel",
}

PACKAGE_REQUIRED = {
    "packageId",
    "periodStart",
    "periodEnd",
    "subjectRole",
    "inputSources",
    "events",
    "evidenceItems",
    "excludedCandidates",
    "validationReports",
    "publicOutputs",
}

REAL_COMMIT_RE = re.compile(r"(?<!mock-)\b[0-9a-f]{7,40}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_RE = re.compile(r"\b\d{17}[\dXx]\b")


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_package(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("package root must be a JSON object")
    return data


def missing_fields(obj: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if field not in obj)


def validate_package(data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    for field in missing_fields(data, PACKAGE_REQUIRED):
        errors.append(f"package missing required field: {field}")

    events = data.get("events", [])
    evidence_items = data.get("evidenceItems", [])
    if not isinstance(events, list):
        errors.append("events must be a list")
        events = []
    if not isinstance(evidence_items, list):
        errors.append("evidenceItems must be a list")
        evidence_items = []

    event_ids: set[str] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"events[{index}] must be an object")
            continue
        for field in missing_fields(event, EVENT_REQUIRED):
            errors.append(f"events[{index}] missing required field: {field}")
        event_id = event.get("eventId")
        if isinstance(event_id, str):
            event_ids.add(event_id)

    for index, evidence in enumerate(evidence_items):
        if not isinstance(evidence, dict):
            errors.append(f"evidenceItems[{index}] must be an object")
            continue
        for field in missing_fields(evidence, EVIDENCE_REQUIRED):
            errors.append(f"evidenceItems[{index}] missing required field: {field}")

        event_id = evidence.get("eventId")
        if event_id not in event_ids:
            errors.append(f"evidenceItems[{index}] references unknown eventId: {event_id}")

        source_quote = evidence.get("sourceQuote")
        quick_locator = evidence.get("quickLocator")
        if isinstance(source_quote, str) and isinstance(quick_locator, str):
            if quick_locator not in source_quote:
                errors.append(
                    f"evidenceItems[{index}] quickLocator is not a substring of sourceQuote"
                )

        if evidence.get("sourceType") == "git":
            message_id = str(evidence.get("messageId", ""))
            if not message_id.startswith("mock-"):
                errors.append(f"evidenceItems[{index}] git messageId must start with mock-")

    serialized = json.dumps(data, ensure_ascii=False)
    if PHONE_RE.search(serialized):
        errors.append("package contains a phone-number-like value")
    if ID_CARD_RE.search(serialized):
        errors.append("package contains an ID-card-like value")
    real_commit_matches = [
        value for value in REAL_COMMIT_RE.findall(serialized) if not value.startswith("mock")
    ]
    if real_commit_matches:
        errors.append("package contains a real-commit-like hash")

    if "示例科技有限公司" in serialized:
        warnings.append("package uses generic company placeholder: 示例科技有限公司")

    return ValidationResult(errors=errors, warnings=warnings)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_evidence_package.py <package.json>", file=sys.stderr)
        return 2

    package_path = Path(argv[1])
    try:
        data = load_package(package_path)
        result = validate_package(data)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    if result.ok:
        print(f"OK: {package_path} passed validation")
        return 0

    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
