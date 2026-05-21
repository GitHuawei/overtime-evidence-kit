import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rules_engine import evaluate_event, evaluate_package  # noqa: E402
from validate_evidence_package import validate_package  # noqa: E402


def load_mock_package():
    with (ROOT / "examples" / "mock-evidence-package" / "package.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


class RulesEngineTest(unittest.TestCase):
    def test_multisource_task_and_result_is_strong_pass(self):
        package = load_mock_package()
        event = package["events"][0]
        evidence = [item for item in package["evidenceItems"] if item["eventId"] == event["eventId"]]
        result = evaluate_event(event, evidence)
        self.assertEqual(result["evidenceStrength"], "strong")
        self.assertEqual(result["qualityGate"], "pass")

    def test_single_source_multiple_evidence_is_medium_needs_review(self):
        package = load_mock_package()
        event = package["events"][1]
        evidence = [item for item in package["evidenceItems"] if item["eventId"] == event["eventId"]]
        result = evaluate_event(event, evidence)
        self.assertEqual(result["evidenceStrength"], "medium")
        self.assertEqual(result["qualityGate"], "needs_review")
        self.assertIn("single_source_only", result["riskFlags"])

    def test_missing_result_evidence_sets_weak_result_flag(self):
        package = load_mock_package()
        event = package["events"][0]
        evidence = [
            item
            for item in package["evidenceItems"]
            if item["eventId"] == event["eventId"] and item["evidenceRole"] == "task_source"
        ]
        result = evaluate_event(event, evidence)
        self.assertIn("weak_result_evidence", result["riskFlags"])

    def test_rest_day_sets_manual_review_required(self):
        package = load_mock_package()
        event = package["events"][3]
        evidence = [item for item in package["evidenceItems"] if item["eventId"] == event["eventId"]]
        result = evaluate_event(event, evidence)
        self.assertIn("manual_review_required", result["riskFlags"])
        self.assertEqual(result["qualityGate"], "needs_review")

    def test_sensitive_pattern_blocks_event(self):
        package = load_mock_package()
        event = copy.deepcopy(package["events"][0])
        evidence = [item for item in package["evidenceItems"] if item["eventId"] == event["eventId"]]
        evidence[0] = copy.deepcopy(evidence[0])
        evidence[0]["sourceQuote"] = "mock sensitive " + "139" + "0000" + "0000"
        result = evaluate_event(event, evidence)
        self.assertIn("sensitive_content_present", result["riskFlags"])
        self.assertEqual(result["qualityGate"], "blocked")

    def test_weak_event_is_blocked_and_has_review_action(self):
        package = load_mock_package()
        event = package["events"][0]
        evidence = [copy.deepcopy(package["evidenceItems"][0])]
        evidence[0]["evidenceRole"] = "review_note"
        result = evaluate_event(event, evidence)
        self.assertEqual(result["evidenceStrength"], "weak")
        self.assertEqual(result["qualityGate"], "blocked")
        self.assertTrue(result["reviewAction"])

    def test_evaluate_package_output_validates(self):
        evaluated = evaluate_package(load_mock_package())
        self.assertEqual(validate_package(evaluated).errors, [])

    def test_evaluate_cli_outputs_valid_package(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/evaluate_mock_package.py",
                "examples/mock-evidence-package/package.json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(validate_package(data).errors, [])


if __name__ == "__main__":
    unittest.main()
