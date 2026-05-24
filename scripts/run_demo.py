#!/usr/bin/env python3
"""Run the complete mock demo pipeline into a disposable output directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_mock_package import (  # noqa: E402
    DEFAULT_EVENTS,
    DEFAULT_GIT_LOG,
    DEFAULT_MESSAGES,
    build_package,
)
from render_evidence_index import CSV_FIELDS, write_index_file  # noqa: E402
from render_mock_report import render_report  # noqa: E402
from validate_evidence_package import validate_package  # noqa: E402


DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "demo"
PACKAGE_FILE = "package.json"
REPORT_FILE = "mock-report.md"
INDEX_FILE = "mock-evidence-index.csv"


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def prepare_output_dir(output_dir: Path, clean: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not clean:
        return
    for name in (PACKAGE_FILE, REPORT_FILE, INDEX_FILE):
        path = output_dir / name
        if path.exists():
            path.unlink()


def run_demo(output_dir: Path = DEFAULT_OUTPUT_DIR, clean: bool = True) -> dict[str, Any]:
    prepare_output_dir(output_dir, clean=clean)

    package = build_package(
        DEFAULT_MESSAGES,
        DEFAULT_GIT_LOG,
        DEFAULT_EVENTS,
        "2026-02-01",
        "2026-02-28",
        "技术岗位劳动者",
        "pkg-mock-2026-02",
    )
    validation = validate_package(package)
    if not validation.ok:
        raise ValueError("demo package validation failed: " + "; ".join(validation.errors))

    package_path = output_dir / PACKAGE_FILE
    report_path = output_dir / REPORT_FILE
    index_path = output_dir / INDEX_FILE

    write_text(package_path, json.dumps(package, ensure_ascii=False, indent=2) + "\n")
    write_text(report_path, render_report(package))
    write_index_file(index_path, package)

    events = [item for item in package.get("events", []) if isinstance(item, dict)]
    evidence_items = [
        item for item in package.get("evidenceItems", []) if isinstance(item, dict)
    ]
    return {
        "outputDir": output_dir,
        "packagePath": package_path,
        "reportPath": report_path,
        "indexPath": index_path,
        "eventCount": len(events),
        "evidenceCount": len(evidence_items),
        "csvHeader": ",".join(CSV_FIELDS),
    }


def format_summary(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Mock demo complete.",
            f"- Output directory: {summary['outputDir']}",
            f"- Evaluated package: {summary['packagePath']}",
            f"- Markdown report: {summary['reportPath']}",
            f"- Evidence index CSV: {summary['indexPath']}",
            f"- Included events: {summary['eventCount']}",
            f"- Evidence items: {summary['evidenceCount']}",
            "- Boundary: mock-only data; no real evidence was read.",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the complete mock evidence demo pipeline."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated demo files. Defaults to outputs/demo/.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove previously generated demo files before writing.",
    )
    args = parser.parse_args(argv)

    try:
        summary = run_demo(args.output_dir, clean=not args.no_clean)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
