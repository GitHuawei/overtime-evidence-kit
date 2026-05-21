#!/usr/bin/env python3
"""Evaluate mock evidence package quality fields."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rules_engine import evaluate_package


def load_package(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("package root must be a JSON object")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a mock evidence package.")
    parser.add_argument("package", help="Path to package.json")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args(argv)

    try:
        data = load_package(Path(args.package))
        evaluated = evaluate_package(data)
        indent = 2 if args.pretty else None
        print(json.dumps(evaluated, ensure_ascii=False, indent=indent))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
