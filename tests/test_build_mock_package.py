import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_mock_package import DEFAULT_EVENTS, DEFAULT_GIT_LOG, DEFAULT_MESSAGES, build_package  # noqa: E402
from validate_evidence_package import validate_package  # noqa: E402


class BuildMockPackageTest(unittest.TestCase):
    def test_builder_outputs_valid_package_shape(self):
        package = build_package(
            DEFAULT_MESSAGES,
            DEFAULT_GIT_LOG,
            DEFAULT_EVENTS,
            "2026-02-01",
            "2026-02-28",
            "技术岗位劳动者",
            "pkg-mock-2026-02",
        )
        self.assertEqual(len(package["events"]), 4)
        self.assertEqual(len(package["evidenceItems"]), 11)
        self.assertEqual(len(package["excludedCandidates"]), 3)
        self.assertEqual(validate_package(package).errors, [])

    def test_builder_quick_locators_are_source_quote_substrings(self):
        package = build_package(
            DEFAULT_MESSAGES,
            DEFAULT_GIT_LOG,
            DEFAULT_EVENTS,
            "2026-02-01",
            "2026-02-28",
            "技术岗位劳动者",
            "pkg-mock-2026-02",
        )
        for item in package["evidenceItems"]:
            self.assertIn(item["quickLocator"], item["sourceQuote"])

    def test_builder_cli_outputs_json(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_mock_package.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["packageId"], "pkg-mock-2026-02")

    def test_builder_rejects_non_mock_commit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            git_path = Path(temp_dir) / "git-log.json"
            git_path.write_text(
                json.dumps(
                    [
                        {
                            "commit": "not-mock-commit",
                            "authorRole": "员工-A",
                            "timestamp": "2026-02-03T20:45:00+08:00",
                            "repository": "mock-order-service",
                            "summary": "mock summary",
                            "changedFiles": ["src/mock_file.py"],
                            "eventId": "evt-mock-weekday-001",
                            "evidenceId": "evd-mock-git-x",
                            "includeInPackage": True,
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_mock_package.py",
                    "--git-log",
                    str(git_path),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("commit must start with mock-", result.stderr)

    def test_builder_missing_input_file_fails(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/build_mock_package.py",
                "--messages",
                "examples/mock-wechat-export/missing.jsonl",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
