#!/usr/bin/env python3
"""Build a mock evidence package from mock source inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from rules_engine import evaluate_package


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MESSAGES = ROOT / "examples" / "mock-wechat-export" / "messages.jsonl"
DEFAULT_GIT_LOG = ROOT / "examples" / "mock-git-log" / "git-log.json"
DEFAULT_EVENTS = ROOT / "examples" / "mock-event-drafts" / "events.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number} must contain a JSON object")
            rows.append(row)
    return rows


def build_chat_evidence(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for row in messages:
        if row.get("includeInPackage") is not True:
            continue
        event_id = row.get("eventId")
        evidence_id = row.get("evidenceId")
        if not event_id or not evidence_id:
            continue
        items.append(
            {
                "evidenceId": evidence_id,
                "eventId": event_id,
                "sourceType": row.get("sourceType", "wechat"),
                "sourceFileName": "mock-wechat-export/messages.jsonl",
                "sourceRowNum": row.get("sourceRowNum"),
                "messageId": row.get("messageId"),
                "timestamp": row.get("timestamp"),
                "senderRole": row.get("senderRole"),
                "sourceQuote": row.get("content"),
                "quickLocator": row.get("quickLocator"),
                "redactionLevel": "mock",
                "evidenceRole": row.get("evidenceRole", "work_process"),
            }
        )
    return items


def build_git_evidence(git_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for index, row in enumerate(git_rows, start=1):
        if row.get("includeInPackage") is not True:
            continue
        commit = row.get("commit")
        if not isinstance(commit, str) or not commit.startswith("mock-"):
            raise ValueError(f"git-log[{index}] commit must start with mock-")
        items.append(
            {
                "evidenceId": row.get("evidenceId"),
                "eventId": row.get("eventId"),
                "sourceType": "git",
                "sourceFileName": "mock-git-log/git-log.json",
                "sourceRowNum": index,
                "messageId": commit,
                "timestamp": row.get("timestamp"),
                "senderRole": row.get("authorRole"),
                "sourceQuote": f"{commit} {row.get('summary', '')}",
                "quickLocator": row.get("quickLocator", commit),
                "redactionLevel": "mock",
                "evidenceRole": row.get("evidenceRole", "git_output"),
            }
        )
    return items


def build_excluded_candidates(messages: list[dict[str, Any]]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in messages:
        candidate_id = row.get("candidateId")
        reason = row.get("excludeReason")
        if row.get("includeInPackage") is False and candidate_id and reason:
            if candidate_id in seen:
                continue
            seen.add(candidate_id)
            candidates.append({"candidateId": str(candidate_id), "reason": str(reason)})
    return candidates


def build_package(
    messages_path: Path,
    git_log_path: Path,
    events_path: Path,
    period_start: str,
    period_end: str,
    subject_role: str,
    package_id: str,
) -> dict[str, Any]:
    messages = load_jsonl(messages_path)
    git_rows = load_json(git_log_path)
    events = load_json(events_path)
    if not isinstance(git_rows, list):
        raise ValueError("git log must be a JSON array")
    if not isinstance(events, list):
        raise ValueError("events draft must be a JSON array")

    package = {
        "packageId": package_id,
        "periodStart": period_start,
        "periodEnd": period_end,
        "subjectRole": subject_role,
        "inputSources": [
            "mock-wechat-export/messages.jsonl",
            "mock-git-log/git-log.json",
            "mock-event-drafts/events.json",
        ],
        "events": events,
        "evidenceItems": build_chat_evidence(messages) + build_git_evidence(git_rows),
        "excludedCandidates": build_excluded_candidates(messages),
        "validationReports": [],
        "publicOutputs": {
            "summaryMarkdown": "mock-report.md",
            "evidenceIndexCsv": "mock-evidence-index.csv",
        },
    }
    return evaluate_package(package)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a mock evidence package.")
    parser.add_argument("--messages", type=Path, default=DEFAULT_MESSAGES)
    parser.add_argument("--git-log", type=Path, default=DEFAULT_GIT_LOG)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--period-start", default="2026-02-01")
    parser.add_argument("--period-end", default="2026-02-28")
    parser.add_argument("--subject-role", default="技术岗位劳动者")
    parser.add_argument("--package-id", default="pkg-mock-2026-02")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    try:
        package = build_package(
            args.messages,
            args.git_log,
            args.events,
            args.period_start,
            args.period_end,
            args.subject_role,
            args.package_id,
        )
        print(json.dumps(package, ensure_ascii=False, indent=2 if args.pretty else None))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
