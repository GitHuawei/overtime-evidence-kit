import csv
import io
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from render_evidence_index import CSV_FIELDS, render_index  # noqa: E402
from render_mock_report import MOCK_ONLY_NOTICE, render_report  # noqa: E402


def load_mock_package():
    with (ROOT / "examples" / "mock-evidence-package" / "package.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return json.load(handle)


class RenderOutputsTest(unittest.TestCase):
    def test_report_contains_preview_summary(self):
        data = load_mock_package()
        report = render_report(data)
        self.assertIsInstance(report, str)
        self.assertIn("pkg-mock-2026-02", report)
        self.assertIn(MOCK_ONLY_NOTICE, report)
        self.assertIn("## 排除候选", report)
        self.assertIn("## 摘要", report)
        self.assertIn("## 事件概览", report)
        self.assertIn("## 复核提示", report)
        self.assertIn("## 边界说明", report)
        self.assertIn("- 质量门：", report)
        self.assertIn("- 证据强度：", report)
        self.assertIn("工作日加班", report)
        self.assertIn("发布夜处理", report)
        self.assertIn("休息日任务", report)
        self.assertIn("通过", report)
        self.assertIn("需复核", report)
        self.assertIn("证据来源单一", report)
        self.assertIn("需要人工复核", report)
        self.assertIn("单聊", report)
        self.assertIn("群聊", report)
        self.assertIn("Git 记录", report)

    def test_report_contains_all_event_ids(self):
        data = load_mock_package()
        report = render_report(data)
        for event in data["events"]:
            self.assertIn(event["eventId"], report)

    def test_report_does_not_emit_sensitive_patterns(self):
        report = render_report(load_mock_package())
        self.assertIsNone(re.search(r"(?<!\d)1[3-9]\d{9}(?!\d)", report))
        self.assertIsNone(re.search(r"\b\d{17}[\dXx]\b", report))

    def test_report_does_not_emit_full_source_quotes(self):
        data = load_mock_package()
        report = render_report(data)
        for item in data["evidenceItems"]:
            self.assertNotIn(item["sourceQuote"], report)
        self.assertIn("快速定位", report)

    def test_evidence_index_header_and_row_count(self):
        data = load_mock_package()
        csv_text = render_index(data)
        rows = list(csv.DictReader(io.StringIO(csv_text)))
        self.assertEqual(csv_text.splitlines()[0], ",".join(CSV_FIELDS))
        self.assertEqual(len(rows), len(data["evidenceItems"]))
        self.assertIn("事件类型", rows[0])
        self.assertIn("日期", rows[0])
        self.assertIn("工作日加班", csv_text)
        self.assertIn("发布夜处理", csv_text)
        self.assertIn("休息日任务", csv_text)
        self.assertIn("单聊", csv_text)
        self.assertIn("群聊", csv_text)
        self.assertIn("Git 记录", csv_text)

    def test_evidence_index_can_be_read_as_csv(self):
        data = load_mock_package()
        rows = list(csv.DictReader(io.StringIO(render_index(data))))
        self.assertEqual(set(rows[0].keys()), set(CSV_FIELDS))
        self.assertTrue(all(row["脱敏级别"] == "mock" for row in rows))

    def test_renderers_match_committed_samples(self):
        data = load_mock_package()
        expected_report = (ROOT / "examples" / "mock-evidence-package" / "mock-report.md").read_text(
            encoding="utf-8"
        )
        expected_index = (
            ROOT / "examples" / "mock-evidence-package" / "mock-evidence-index.csv"
        ).read_text(encoding="utf-8")
        self.assertEqual(render_report(data), expected_report)
        self.assertEqual(render_index(data), expected_index)


if __name__ == "__main__":
    unittest.main()
