import json
import tempfile
import unittest
from pathlib import Path

from scripts import run_demo
from scripts.render_evidence_index import CSV_FIELDS
from scripts.validate_evidence_package import validate_package


class RunDemoTests(unittest.TestCase):
    def run_demo_in_temp(self):
        temp_dir = tempfile.TemporaryDirectory()
        output_dir = Path(temp_dir.name) / "demo"
        summary = run_demo.run_demo(output_dir)
        self.addCleanup(temp_dir.cleanup)
        return output_dir, summary

    def test_demo_writes_expected_files(self):
        output_dir, summary = self.run_demo_in_temp()

        self.assertEqual(output_dir, summary["outputDir"])
        self.assertTrue((output_dir / "package.json").is_file())
        self.assertTrue((output_dir / "mock-report.md").is_file())
        self.assertTrue((output_dir / "mock-evidence-index.csv").is_file())

    def test_generated_package_validates_and_has_rule_fields(self):
        output_dir, _summary = self.run_demo_in_temp()
        package = json.loads((output_dir / "package.json").read_text(encoding="utf-8"))
        result = validate_package(package)

        self.assertTrue(result.ok, result.errors)
        for event in package["events"]:
            self.assertIn("evidenceStrength", event)
            self.assertIn("qualityGate", event)
            self.assertIn("riskFlags", event)
            self.assertIn("reviewAction", event)

    def test_report_contains_mock_only_notice(self):
        output_dir, _summary = self.run_demo_in_temp()
        report = (output_dir / "mock-report.md").read_text(encoding="utf-8")

        self.assertIn("mock-only 提醒", report)
        self.assertIn("不提供法律意见", report)
        self.assertIn("## 摘要", report)
        self.assertIn("## 事件概览", report)
        self.assertIn("## 边界说明", report)
        self.assertNotIn("sourceQuote", report)

    def test_csv_header_is_stable(self):
        output_dir, _summary = self.run_demo_in_temp()
        first_line = (
            output_dir / "mock-evidence-index.csv"
        ).read_text(encoding="utf-8").splitlines()[0]

        self.assertEqual(first_line, ",".join(CSV_FIELDS))

    def test_demo_output_has_no_consecutive_question_mark_corruption(self):
        output_dir, _summary = self.run_demo_in_temp()

        for path in output_dir.iterdir():
            if path.suffix in {".json", ".md", ".csv"}:
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("?" * 3, text)


if __name__ == "__main__":
    unittest.main()
