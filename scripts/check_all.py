#!/usr/bin/env python3
"""Run all local checks for the release candidate."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".idea",
}
IGNORED_PREFIXES = {
    ("docs", "plans"),
}
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".csv", ".py", ".yml", ".yaml"}
RELEASE_REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "LICENSE",
    "docs/demo.md",
    "docs/open-source-boundary.md",
    "docs/public-launch.md",
    "docs/public-outputs.md",
    "docs/release-checklist.md",
    "docs/repository-settings.md",
    "docs/roadmap.md",
    ".github/workflows/ci.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/privacy_boundary.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
]
RELEASE_REQUIRED_PHRASES = {
    "README.md": [
        "Release Candidate",
        "mock-only",
        "不处理真实案件材料",
        "不提供法律意见",
        "快速开始",
        "质量门",
        "python scripts/run_demo.py",
        "outputs/demo/",
    ],
    "CHANGELOG.md": [
        "v0.1.0 - planned",
        "fictional mock evidence package",
        "mock-only",
        "Known limitations",
        "不处理真实案件材料",
    ],
    "CONTRIBUTING.md": [
        "mock-only",
        "不提交真实微信聊天",
        "不提交真实 Git commit",
        "python scripts/check_all.py",
    ],
    "SECURITY.md": [
        "不要公开提交敏感信息",
        "fictional mock data",
        "不提供法律意见",
    ],
    "docs/open-source-boundary.md": [
        "strict mock-only boundary",
        "Never commit or request",
        "does not provide legal advice",
    ],
    "docs/demo.md": [
        "mock-only",
        "python scripts/run_demo.py",
        "outputs/demo/",
        "不读取用户真实文件",
    ],
    "docs/public-launch.md": [
        "v0.1.0 Release Candidate",
        "mock-only",
        "未创建 GitHub Release 或 tag",
        "不提供法律意见",
        "post-launch monitoring checklist",
    ],
    "docs/release-checklist.md": [
        "受控公开",
        "docs/plans/",
        "不要创建 GitHub Release 或 tag",
        "Known limitations",
    ],
    "docs/repository-settings.md": [
        "GitHub repository settings",
        "建议 topics",
        "不要创建 GitHub Release 或 tag",
        "不加入法律结论",
    ],
    ".github/ISSUE_TEMPLATE/bug_report.md": [
        "Mock-only Confirmation",
        "real WeChat chats",
        "real Git data",
        "Do not paste real evidence",
    ],
    ".github/ISSUE_TEMPLATE/feature_request.md": [
        "Mock-only Confirmation",
        "real WeChat chats",
        "legal outcome guarantee",
    ],
    ".github/ISSUE_TEMPLATE/privacy_boundary.md": [
        "Mock-only Confirmation",
        "no real evidence",
        "fictional mock data only",
    ],
    ".github/PULL_REQUEST_TEMPLATE.md": [
        "Mock-only and Privacy Checklist",
        "real WeChat chats",
        "real Git commits",
        "legal outcomes",
    ],
}
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_CARD_RE = re.compile(r"\b\d{17}[\dXx]\b")
REAL_COMMIT_RE = re.compile(r"(?<!mock-)(?<!schema-)\b[0-9a-fA-F]{7,40}\b")
TEXT_CORRUPTION_PATTERNS = [
    ("\ufffd replacement character", re.compile("\ufffd")),
    ("consecutive question marks", re.compile(r"\?{3,}")),
    (
        "mojibake cjk marker",
        re.compile(
            "|".join(
                [
                    "\ufffd" * 4,
                    "\u0531\u0580" + "\ufffd" * 2,
                    "\ufffd" * 4 + "\u03f5\u0373",
                    "\u02be\ufffd\ufffd",
                    "\ufffd\u0377\ufffd",
                    "\ufffd\u6fbe\ufffd",
                ]
            )
        ),
    ),
]


def iter_files(*suffixes: str) -> list[Path]:
    suffix_set = set(suffixes)
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(relative_parts[: len(prefix)] == prefix for prefix in IGNORED_PREFIXES):
            continue
        if not suffix_set or path.suffix in suffix_set:
            files.append(path)
    return sorted(files)


def run_subprocess(command: list[str], name: str, env: dict[str, str] | None = None) -> bool:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=env,
    )
    if result.returncode == 0:
        print(f"PASS {name}")
        return True

    print(f"FAIL {name}")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return False


def run_to_file(command: list[str], output_path: Path, name: str) -> bool:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"FAIL {name}")
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return False
    output_path.write_text(result.stdout, encoding="utf-8")
    print(f"PASS {name}")
    return True


def check_utf8_files() -> bool:
    for path in iter_files(*TEXT_SUFFIXES):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            print("FAIL utf8 files")
            print(f"{path.relative_to(ROOT)}: {exc}")
            return False
        corruption = find_text_corruption(text)
        if corruption:
            print("FAIL utf8 files")
            print(f"{path.relative_to(ROOT)}: {corruption}")
            return False
    print("PASS utf8 files")
    return True


def find_text_corruption(text: str) -> str | None:
    for label, pattern in TEXT_CORRUPTION_PATTERNS:
        if pattern.search(text):
            return f"contains {label}"
    return None


def check_json_files() -> bool:
    for path in iter_files(".json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print("FAIL json files")
            print(f"{path.relative_to(ROOT)}: {exc}")
            return False
    print("PASS json files")
    return True


def check_jsonl_files() -> bool:
    for path in iter_files(".jsonl"):
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if line.strip():
                        json.loads(line)
        except Exception as exc:
            print("FAIL jsonl files")
            print(f"{path.relative_to(ROOT)}:{line_number}: {exc}")
            return False
    print("PASS jsonl files")
    return True


def scan_sensitive_patterns() -> bool:
    failures: list[str] = []
    forbidden_path = re.compile(r"history-analysis[\\/].*outputs")
    forbidden_keywords = [
        "real" + "-case-secret",
        "actual" + "-client-material",
    ]
    for path in iter_files(*TEXT_SUFFIXES):
        text = path.read_text(encoding="utf-8")
        phone_cleaned = PHONE_RE.sub("", text)
        if PHONE_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)}: phone-number-like value")
        if ID_CARD_RE.search(text):
            failures.append(f"{path.relative_to(ROOT)}: id-card-like value")
        if REAL_COMMIT_RE.search(phone_cleaned):
            failures.append(f"{path.relative_to(ROOT)}: real-commit-like hash")
        if forbidden_path.search(text):
            failures.append(f"{path.relative_to(ROOT)}: forbidden output path")
        for keyword in forbidden_keywords:
            if keyword in text:
                failures.append(f"{path.relative_to(ROOT)}: forbidden keyword {keyword}")

    if failures:
        print("FAIL sensitive scan")
        print("\n".join(failures))
        return False
    print("PASS sensitive scan")
    return True


def check_build_evaluate_pipeline() -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        built_package = temp_root / "built-package.json"
        evaluated_package = temp_root / "evaluated-package.json"
        if not run_to_file(
            [sys.executable, "scripts/build_mock_package.py"],
            built_package,
            "build mock package",
        ):
            return False
        if not run_to_file(
            [sys.executable, "scripts/evaluate_mock_package.py", str(built_package)],
            evaluated_package,
            "evaluate mock package",
        ):
            return False
        pipeline_checks = [
            (
                [
                    sys.executable,
                    "scripts/validate_evidence_package.py",
                    str(evaluated_package),
                ],
                "built package validation",
            ),
            (
                [
                    sys.executable,
                    "scripts/render_mock_report.py",
                    str(evaluated_package),
                ],
                "render built mock report",
            ),
            (
                [
                    sys.executable,
                    "scripts/render_evidence_index.py",
                    str(evaluated_package),
                ],
                "render built evidence index",
            ),
        ]
        for command, name in pipeline_checks:
            if not run_subprocess(command, name):
                return False
    return True


def check_committed_outputs() -> bool:
    samples = [
        (
            [
                sys.executable,
                "scripts/render_mock_report.py",
                "examples/mock-evidence-package/package.json",
            ],
            ROOT / "examples" / "mock-evidence-package" / "mock-report.md",
            "committed mock report",
        ),
        (
            [
                sys.executable,
                "scripts/render_evidence_index.py",
                "examples/mock-evidence-package/package.json",
            ],
            ROOT / "examples" / "mock-evidence-package" / "mock-evidence-index.csv",
            "committed evidence index",
        ),
    ]
    for command, expected_path, name in samples:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"FAIL {name}")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            return False
        expected = expected_path.read_text(encoding="utf-8")
        if result.stdout != expected:
            print(f"FAIL {name}")
            print(f"{expected_path.relative_to(ROOT)} is out of date; regenerate sample output")
            return False
        print(f"PASS {name}")
    return True


def check_demo_run() -> bool:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "demo-output"
        result = subprocess.run(
            [
                sys.executable,
                "scripts/run_demo.py",
                "--output-dir",
                str(output_dir),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print("FAIL demo run")
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            return False

        expected_files = [
            output_dir / "package.json",
            output_dir / "mock-report.md",
            output_dir / "mock-evidence-index.csv",
        ]
        for path in expected_files:
            if not path.is_file():
                print("FAIL demo run")
                print(f"{path.name} was not generated")
                return False
            corruption = find_text_corruption(path.read_text(encoding="utf-8"))
            if corruption:
                print("FAIL demo run")
                print(f"{path.name}: {corruption}")
                return False

        package = json.loads((output_dir / "package.json").read_text(encoding="utf-8"))
        if not run_subprocess(
            [
                sys.executable,
                "scripts/validate_evidence_package.py",
                str(output_dir / "package.json"),
            ],
            "demo package validation",
        ):
            return False
        report = (output_dir / "mock-report.md").read_text(encoding="utf-8")
        index_header = (output_dir / "mock-evidence-index.csv").read_text(
            encoding="utf-8"
        ).splitlines()[0]
        expected_header = "证据ID,事件ID,事件类型,日期,来源类型,来源文件,来源行号,消息ID,快速定位,脱敏级别"
        if (
            "mock-only 提醒" not in report
            or "## 摘要" not in report
            or "## 事件概览" not in report
            or "## 复核提示" not in report
            or "## 边界说明" not in report
            or "工作日加班" not in report
            or "发布夜处理" not in report
            or "休息日任务" not in report
            or "需复核" not in report
            or "证据来源单一" not in report
            or "单聊" not in report
            or "群聊" not in report
            or "Git 记录" not in report
            or "sourceQuote" in report
            or index_header != expected_header
            or "工作日加班" not in (output_dir / "mock-evidence-index.csv").read_text(
                encoding="utf-8"
            )
            or "群聊" not in (output_dir / "mock-evidence-index.csv").read_text(
                encoding="utf-8"
            )
        ):
            print("FAIL demo run")
            print("demo public output localization check failed")
            return False
        if not package.get("events"):
            print("FAIL demo run")
            print("demo package has no events")
            return False
        print("PASS demo run")
        return True


def check_release_readiness_files() -> bool:
    failures: list[str] = []
    for relative_path in RELEASE_REQUIRED_FILES:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path}: missing required release file")

    for relative_path, phrases in RELEASE_REQUIRED_PHRASES.items():
        path = ROOT / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                failures.append(f"{relative_path}: missing required phrase {phrase!r}")

    if failures:
        print("FAIL release readiness files")
        print("\n".join(failures))
        return False
    print("PASS release readiness files")
    return True


def main() -> int:
    checks = [
        check_utf8_files,
        check_json_files,
        check_jsonl_files,
        check_build_evaluate_pipeline,
        lambda: run_subprocess(
            [
                sys.executable,
                "scripts/validate_evidence_package.py",
                "examples/mock-evidence-package/package.json",
            ],
            "evidence package validation",
        ),
        lambda: run_subprocess(
            [
                sys.executable,
                "scripts/render_mock_report.py",
                "examples/mock-evidence-package/package.json",
            ],
            "render mock report",
        ),
        lambda: run_subprocess(
            [
                sys.executable,
                "scripts/render_evidence_index.py",
                "examples/mock-evidence-package/package.json",
            ],
            "render evidence index",
        ),
        check_committed_outputs,
        check_demo_run,
        check_release_readiness_files,
        lambda: run_subprocess(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_*.py",
            ],
            "unit tests",
            env={**os.environ, "OVERTIME_CHECK_ALL_RUNNING": "1"},
        ),
        scan_sensitive_patterns,
    ]

    for check in checks:
        if not check():
            return 1
    print("OK: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
