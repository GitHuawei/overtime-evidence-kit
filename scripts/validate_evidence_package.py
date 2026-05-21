#!/usr/bin/env python3
"""Validate a mock overtime evidence package."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_DIR = ROOT / "schema"
DEFAULT_SOURCE_ROOT = ROOT / "examples"

ALLOWED_RISK_FLAGS = {
    "missing_end_time",
    "single_source_only",
    "unclear_task_owner",
    "sensitive_content_present",
    "needs_legal_review",
    "weak_result_evidence",
    "manual_review_required",
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


def load_schemas(schema_dir: Path = DEFAULT_SCHEMA_DIR) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name in (
        "overtime-event.schema.json",
        "evidence-item.schema.json",
        "evidence-package.schema.json",
    ):
        schema_path = schema_dir / name
        with schema_path.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        if not isinstance(schema, dict):
            raise ValueError(f"{schema_path} must contain a JSON object")
        schemas[name] = schema
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            schemas[schema_id] = schema
    return schemas


def validate_package(
    data: dict[str, Any],
    schema_dir: Path = DEFAULT_SCHEMA_DIR,
    source_root: Path = DEFAULT_SOURCE_ROOT,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        schemas = load_schemas(schema_dir)
    except Exception as exc:
        return ValidationResult(errors=[f"schema load failed: {exc}"], warnings=warnings)

    validate_json_schema(
        data,
        schemas["evidence-package.schema.json"],
        schemas,
        "$",
        errors,
    )
    validate_references_and_locators(data, errors)
    validate_package_period(data, errors)
    validate_event_timing(data, errors)
    validate_risk_flags(data, errors)
    validate_excluded_candidates(data, errors)
    validate_event_evidence_coverage(data, errors)
    validate_evidence_timestamps(data, warnings)
    validate_source_row_alignment(data, source_root, errors)
    validate_mock_only(data, errors, warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def validate_json_schema(
    value: Any,
    schema: dict[str, Any],
    schemas: dict[str, dict[str, Any]],
    path: str,
    errors: list[str],
) -> None:
    ref = schema.get("$ref")
    if isinstance(ref, str):
        validate_json_schema(value, resolve_ref(ref, schemas), schemas, path, errors)
        return

    expected_type = schema.get("type")
    if expected_type and not matches_type(value, expected_type):
        errors.append(f"{path} must be {expected_type}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} must be one of: {', '.join(map(str, schema['enum']))}")

    if expected_type == "object" and isinstance(value, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path} missing required field: {field}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in properties:
                    errors.append(f"{path}.{field} is not allowed")

        for field, field_schema in properties.items():
            if field in value:
                validate_json_schema(
                    value[field],
                    field_schema,
                    schemas,
                    f"{path}.{field}",
                    errors,
                )

    if expected_type == "array" and isinstance(value, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(value) < min_items:
            errors.append(f"{path} must contain at least {min_items} item(s)")

        if schema.get("uniqueItems") is True:
            seen: set[str] = set()
            for item in value:
                serialized = json.dumps(item, ensure_ascii=False, sort_keys=True)
                if serialized in seen:
                    errors.append(f"{path} must contain unique items")
                    break
                seen.add(serialized)

        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_json_schema(
                    item,
                    item_schema,
                    schemas,
                    f"{path}[{index}]",
                    errors,
                )

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path} must contain at least {min_length} character(s)")

        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            errors.append(f"{path} does not match pattern: {pattern}")

        fmt = schema.get("format")
        if fmt == "date" and not is_valid_date(value):
            errors.append(f"{path} must be a valid date")
        if fmt == "date-time" and parse_datetime(value) is None:
            errors.append(f"{path} must be a valid date-time")

    minimum = schema.get("minimum")
    if isinstance(minimum, (int, float)) and isinstance(value, (int, float)):
        if value < minimum:
            errors.append(f"{path} must be greater than or equal to {minimum}")


def resolve_ref(ref: str, schemas: dict[str, dict[str, Any]]) -> dict[str, Any]:
    schema_name = ref.removeprefix("./")
    if schema_name in schemas:
        return schemas[schema_name]
    if ref in schemas:
        return schemas[ref]
    raise ValueError(f"unresolved schema reference: {ref}")


def matches_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    return True


def is_valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def parse_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_references_and_locators(data: dict[str, Any], errors: list[str]) -> None:
    events = data.get("events", [])
    evidence_items = data.get("evidenceItems", [])
    if not isinstance(events, list) or not isinstance(evidence_items, list):
        return

    event_ids = {
        event.get("eventId")
        for event in events
        if isinstance(event, dict) and isinstance(event.get("eventId"), str)
    }

    for index, evidence in enumerate(evidence_items):
        if not isinstance(evidence, dict):
            continue

        event_id = evidence.get("eventId")
        if event_id not in event_ids:
            errors.append(f"$.evidenceItems[{index}].eventId references unknown eventId: {event_id}")

        source_quote = evidence.get("sourceQuote")
        quick_locator = evidence.get("quickLocator")
        if isinstance(source_quote, str) and isinstance(quick_locator, str):
            if quick_locator not in source_quote:
                errors.append(
                    f"$.evidenceItems[{index}].quickLocator is not a substring of sourceQuote"
                )

        if evidence.get("sourceType") == "git":
            message_id = str(evidence.get("messageId", ""))
            if not message_id.startswith("mock-"):
                errors.append(f"$.evidenceItems[{index}].messageId must start with mock-")


def validate_event_timing(data: dict[str, Any], errors: list[str]) -> None:
    events = data.get("events", [])
    if not isinstance(events, list):
        return

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue

        start = event.get("startTime")
        end = event.get("endTime")
        duration = event.get("durationMinutes")
        if not isinstance(start, str) or not isinstance(end, str):
            continue

        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)
        if start_dt is None or end_dt is None:
            continue

        if start_dt >= end_dt:
            errors.append(f"$.events[{index}].startTime must be earlier than endTime")
            continue

        if isinstance(duration, int):
            expected_minutes = int((end_dt - start_dt).total_seconds() // 60)
            if duration != expected_minutes:
                errors.append(
                    f"$.events[{index}].durationMinutes must equal {expected_minutes}"
                )


def validate_package_period(data: dict[str, Any], errors: list[str]) -> None:
    period_start = data.get("periodStart")
    period_end = data.get("periodEnd")
    if not isinstance(period_start, str) or not isinstance(period_end, str):
        return

    start_date = parse_date(period_start)
    end_date = parse_date(period_end)
    if start_date is None or end_date is None:
        return

    if start_date > end_date:
        errors.append("$.periodStart must be earlier than or equal to periodEnd")
        return

    events = data.get("events", [])
    if not isinstance(events, list):
        return
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        work_date = event.get("workDate")
        if not isinstance(work_date, str):
            continue
        parsed_work_date = parse_date(work_date)
        if parsed_work_date is None:
            continue
        if parsed_work_date < start_date or parsed_work_date > end_date:
            errors.append(f"$.events[{index}].workDate must be within package period")


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def validate_risk_flags(data: dict[str, Any], errors: list[str]) -> None:
    events = data.get("events", [])
    if not isinstance(events, list):
        return
    for event_index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        risk_flags = event.get("riskFlags", [])
        if not isinstance(risk_flags, list):
            continue
        for flag_index, flag in enumerate(risk_flags):
            if not isinstance(flag, str):
                continue
            if flag not in ALLOWED_RISK_FLAGS:
                errors.append(
                    f"$.events[{event_index}].riskFlags[{flag_index}] "
                    f"is not an allowed risk flag: {flag}"
                )


def validate_excluded_candidates(data: dict[str, Any], errors: list[str]) -> None:
    candidates = data.get("excludedCandidates", [])
    if not isinstance(candidates, list):
        return
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            continue
        reason = candidate.get("reason")
        if not isinstance(reason, str) or len(reason.strip()) < 6:
            errors.append(
                f"$.excludedCandidates[{index}].reason must explain why the candidate is excluded"
            )


def validate_event_evidence_coverage(data: dict[str, Any], errors: list[str]) -> None:
    events = data.get("events", [])
    evidence_items = data.get("evidenceItems", [])
    if not isinstance(events, list) or not isinstance(evidence_items, list):
        return

    evidence_by_event: dict[str, list[dict[str, Any]]] = {}
    for evidence in evidence_items:
        if not isinstance(evidence, dict):
            continue
        event_id = evidence.get("eventId")
        if isinstance(event_id, str):
            evidence_by_event.setdefault(event_id, []).append(evidence)

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        event_id = event.get("eventId")
        if not isinstance(event_id, str):
            continue

        covered_items = evidence_by_event.get(event_id, [])
        if not covered_items:
            errors.append(f"$.events[{index}].eventId has no evidence coverage: {event_id}")
            continue

        if event.get("evidenceStrength") == "strong":
            source_types = {
                item.get("sourceType")
                for item in covered_items
                if isinstance(item.get("sourceType"), str)
            }
            if len(covered_items) < 2 or len(source_types) < 2:
                errors.append(
                    f"$.events[{index}].evidenceStrength strong requires at least "
                    "2 evidence items from 2 source types"
                )


def validate_evidence_timestamps(data: dict[str, Any], warnings: list[str]) -> None:
    events = data.get("events", [])
    evidence_items = data.get("evidenceItems", [])
    if not isinstance(events, list) or not isinstance(evidence_items, list):
        return

    event_ranges: dict[str, tuple[datetime, datetime]] = {}
    for event in events:
        if not isinstance(event, dict):
            continue
        event_id = event.get("eventId")
        start = event.get("startTime")
        end = event.get("endTime")
        if not isinstance(event_id, str) or not isinstance(start, str) or not isinstance(end, str):
            continue
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)
        if start_dt is not None and end_dt is not None:
            event_ranges[event_id] = (start_dt, end_dt)

    for index, evidence in enumerate(evidence_items):
        if not isinstance(evidence, dict):
            continue
        event_id = evidence.get("eventId")
        timestamp = evidence.get("timestamp")
        if not isinstance(event_id, str) or not isinstance(timestamp, str):
            continue
        linked_range = event_ranges.get(event_id)
        evidence_dt = parse_datetime(timestamp)
        if linked_range is None or evidence_dt is None:
            continue
        lower_bound = linked_range[0] - timedelta(hours=24)
        upper_bound = linked_range[1] + timedelta(hours=24)
        if evidence_dt < lower_bound or evidence_dt > upper_bound:
            warnings.append(
                f"$.evidenceItems[{index}].timestamp is far from linked event time range"
            )


def validate_source_row_alignment(
    data: dict[str, Any], source_root: Path, errors: list[str]
) -> None:
    evidence_items = data.get("evidenceItems", [])
    if not isinstance(evidence_items, list):
        return

    jsonl_cache: dict[Path, list[dict[str, Any] | None]] = {}
    for index, evidence in enumerate(evidence_items):
        if not isinstance(evidence, dict):
            continue
        source_file_name = evidence.get("sourceFileName")
        source_row_num = evidence.get("sourceRowNum")
        message_id = evidence.get("messageId")
        if not isinstance(source_file_name, str) or not source_file_name.endswith(".jsonl"):
            continue
        if not isinstance(source_row_num, int) or not isinstance(message_id, str):
            continue

        source_path = source_root / source_file_name
        if source_path not in jsonl_cache:
            try:
                jsonl_cache[source_path] = load_jsonl(source_path)
            except Exception as exc:
                errors.append(f"$.evidenceItems[{index}].sourceFileName cannot be read: {exc}")
                continue

        rows = jsonl_cache[source_path]
        row_index = source_row_num - 1
        if row_index < 0 or row_index >= len(rows):
            errors.append(f"$.evidenceItems[{index}].sourceRowNum does not exist")
            continue

        row = rows[row_index]
        if not isinstance(row, dict) or row.get("messageId") != message_id:
            errors.append(
                f"$.evidenceItems[{index}].sourceRowNum does not match source messageId"
            )


def load_jsonl(path: Path) -> list[dict[str, Any] | None]:
    rows: list[dict[str, Any] | None] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                rows.append(None)
                continue
            value = json.loads(stripped)
            rows.append(value if isinstance(value, dict) else None)
    return rows


def validate_mock_only(
    data: dict[str, Any], errors: list[str], warnings: list[str]
) -> None:
    serialized = json.dumps(data, ensure_ascii=False)
    phone_cleaned = PHONE_RE.sub("", serialized)
    if PHONE_RE.search(serialized):
        errors.append("package contains a phone-number-like value")
    if ID_CARD_RE.search(serialized):
        errors.append("package contains an ID-card-like value")
    if REAL_COMMIT_RE.search(phone_cleaned):
        errors.append("package contains a real-commit-like hash")

    if "示例科技有限公司" in serialized:
        warnings.append("package uses generic company placeholder: 示例科技有限公司")


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
