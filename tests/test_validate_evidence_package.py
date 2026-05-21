import copy
import json
import sys
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

    def test_missing_event_field_fails(self):
        data = load_mock_package()
        del data["events"][0]["workDate"]
        result = validate_package(data)
        self.assertIn("events[0] missing required field: workDate", result.errors)

    def test_unknown_event_reference_fails(self):
        data = load_mock_package()
        data["evidenceItems"][0]["eventId"] = "evt-mock-missing"
        result = validate_package(data)
        self.assertIn(
            "evidenceItems[0] references unknown eventId: evt-mock-missing",
            result.errors,
        )

    def test_quick_locator_must_be_source_quote_substring(self):
        data = load_mock_package()
        data["evidenceItems"][0]["quickLocator"] = "不存在的定位文本"
        result = validate_package(data)
        self.assertIn(
            "evidenceItems[0] quickLocator is not a substring of sourceQuote",
            result.errors,
        )

    def test_git_message_id_must_use_mock_prefix(self):
        data = load_mock_package()
        git_item = copy.deepcopy(data["evidenceItems"][2])
        git_item["messageId"] = "not-mock-commit"
        data["evidenceItems"][2] = git_item
        result = validate_package(data)
        self.assertIn("evidenceItems[2] git messageId must start with mock-", result.errors)


if __name__ == "__main__":
    unittest.main()
