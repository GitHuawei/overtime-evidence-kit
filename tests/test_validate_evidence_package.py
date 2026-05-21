import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_evidence_package import validate_package  # noqa: E402


def load_mock_package():
    with (ROOT / "examples" / "mock-evidence-package" / "package.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


class ValidateEvidencePackageTest(unittest.TestCase):
    def test_valid_mock_package_passes(self):
        result = validate_package(load_mock_package())
        self.assertEqual(result.errors, [])

    def test_missing_event_field_fails_schema_validation(self):
        data = load_mock_package()
        del data["events"][0]["workDate"]
        result = validate_package(data)
        self.assertIn("$.events[0] missing required field: workDate", result.errors)

    def test_invalid_event_type_fails_schema_validation(self):
        data = load_mock_package()
        data["events"][0]["eventType"] = "mock_invalid_type"
        result = validate_package(data)
        self.assertIn(
            "$.events[0].eventType must be one of: weekday_overtime, release_night, rest_day_task",
            result.errors,
        )

    def test_wrong_duration_type_fails_schema_validation(self):
        data = load_mock_package()
        data["events"][0]["durationMinutes"] = "150"
        result = validate_package(data)
        self.assertIn("$.events[0].durationMinutes must be integer", result.errors)

    def test_unknown_event_reference_fails(self):
        data = load_mock_package()
        data["evidenceItems"][0]["eventId"] = "evt-mock-missing"
        result = validate_package(data)
        self.assertIn(
            "$.evidenceItems[0].eventId references unknown eventId: evt-mock-missing",
            result.errors,
        )

    def test_quick_locator_must_be_source_quote_substring(self):
        data = load_mock_package()
        data["evidenceItems"][0]["quickLocator"] = "missing locator"
        result = validate_package(data)
        self.assertIn(
            "$.evidenceItems[0].quickLocator is not a substring of sourceQuote",
            result.errors,
        )

    def test_git_message_id_must_use_mock_prefix(self):
        data = load_mock_package()
        git_item = copy.deepcopy(data["evidenceItems"][2])
        git_item["messageId"] = "not-mock-commit"
        data["evidenceItems"][2] = git_item
        result = validate_package(data)
        self.assertIn("$.evidenceItems[2].messageId must start with mock-", result.errors)

    def test_start_time_must_be_earlier_than_end_time(self):
        data = load_mock_package()
        data["events"][0]["startTime"] = "2026-02-03T22:00:00+08:00"
        data["events"][0]["endTime"] = "2026-02-03T21:30:00+08:00"
        result = validate_package(data)
        self.assertIn("$.events[0].startTime must be earlier than endTime", result.errors)

    def test_duration_minutes_must_match_time_range(self):
        data = load_mock_package()
        data["events"][0]["durationMinutes"] = 149
        result = validate_package(data)
        self.assertIn("$.events[0].durationMinutes must equal 150", result.errors)

    def test_each_event_must_have_evidence_coverage(self):
        data = load_mock_package()
        data["evidenceItems"] = [
            item
            for item in data["evidenceItems"]
            if item["eventId"] != "evt-mock-release-001"
        ]
        result = validate_package(data)
        self.assertIn(
            "$.events[1].eventId has no evidence coverage: evt-mock-release-001",
            result.errors,
        )

    def test_strong_event_requires_multiple_source_types(self):
        data = load_mock_package()
        data["evidenceItems"] = [
            item
            for item in data["evidenceItems"]
            if item["eventId"] != "evt-mock-weekday-001" or item["sourceType"] != "git"
        ]
        result = validate_package(data)
        self.assertIn(
            "$.events[0].evidenceStrength strong requires at least "
            "2 evidence items from 2 source types",
            result.errors,
        )

    def test_schema_files_must_be_available(self):
        data = load_mock_package()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_package(data, schema_dir=Path(temp_dir))
        self.assertTrue(any(error.startswith("schema load failed:") for error in result.errors))


if __name__ == "__main__":
    unittest.main()
