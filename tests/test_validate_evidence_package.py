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

    def test_mock_package_contains_preview_month_shape(self):
        data = load_mock_package()
        self.assertEqual(len(data["events"]), 4)
        self.assertEqual(len(data["excludedCandidates"]), 3)
        covered_event_ids = {item["eventId"] for item in data["evidenceItems"]}
        self.assertEqual({event["eventId"] for event in data["events"]}, covered_event_ids)

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

    def test_phone_like_value_does_not_trigger_commit_hash_error(self):
        data = load_mock_package()
        placeholder_phone = "139" + "0000" + "0000"
        data["subjectRole"] = f"mock role with placeholder phone {placeholder_phone}"
        result = validate_package(data)
        self.assertIn("package contains a phone-number-like value", result.errors)
        self.assertNotIn("package contains a real-commit-like hash", result.errors)

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

    def test_period_start_must_not_be_after_period_end(self):
        data = load_mock_package()
        data["periodStart"] = "2026-03-01"
        data["periodEnd"] = "2026-02-01"
        result = validate_package(data)
        self.assertIn(
            "$.periodStart must be earlier than or equal to periodEnd",
            result.errors,
        )

    def test_event_work_date_must_be_within_period(self):
        data = load_mock_package()
        data["events"][0]["workDate"] = "2026-03-01"
        result = validate_package(data)
        self.assertIn("$.events[0].workDate must be within package period", result.errors)

    def test_unknown_risk_flag_fails(self):
        data = load_mock_package()
        data["events"][0]["riskFlags"] = ["mock_unknown_risk"]
        result = validate_package(data)
        self.assertIn(
            "$.events[0].riskFlags[0] is not an allowed risk flag: mock_unknown_risk",
            result.errors,
        )

    def test_empty_excluded_reason_fails(self):
        data = load_mock_package()
        data["excludedCandidates"][0]["reason"] = "  "
        result = validate_package(data)
        self.assertIn(
            "$.excludedCandidates[0].reason must explain why the candidate is excluded",
            result.errors,
        )

    def test_far_evidence_timestamp_warns(self):
        data = load_mock_package()
        data["evidenceItems"][0]["timestamp"] = "2026-02-10T19:12:00+08:00"
        result = validate_package(data)
        self.assertEqual(result.errors, [])
        self.assertIn(
            "$.evidenceItems[0].timestamp is far from linked event time range",
            result.warnings,
        )

    def test_jsonl_source_row_num_must_match_message_id(self):
        data = load_mock_package()
        data["evidenceItems"][0]["messageId"] = "mock-msg-mismatch"
        result = validate_package(data)
        self.assertIn(
            "$.evidenceItems[0].sourceRowNum does not match source messageId",
            result.errors,
        )

    def test_each_event_must_have_evidence_coverage(self):
        data = load_mock_package()
        data["evidenceItems"] = [
            item
            for item in data["evidenceItems"]
            if item["eventId"] != "evt-mock-release-001"
        ]
        result = validate_package(data)
        self.assertIn(
            "$.events[2].eventId has no evidence coverage: evt-mock-release-001",
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
