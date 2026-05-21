import unittest

from scripts.display_labels import (
    evidence_strength_label,
    event_type_label,
    quality_gate_label,
    risk_flag_label,
    source_type_label,
)


class DisplayLabelsTest(unittest.TestCase):
    def test_known_event_type_labels(self):
        self.assertEqual(event_type_label("weekday_overtime"), "工作日加班")
        self.assertEqual(event_type_label("release_night"), "发布夜处理")
        self.assertEqual(event_type_label("rest_day_task"), "休息日任务")

    def test_known_quality_and_risk_labels(self):
        self.assertEqual(quality_gate_label("pass"), "通过")
        self.assertEqual(quality_gate_label("needs_review"), "需复核")
        self.assertEqual(risk_flag_label("single_source_only"), "证据来源单一")
        self.assertEqual(risk_flag_label("manual_review_required"), "需要人工复核")

    def test_known_source_and_strength_labels(self):
        self.assertEqual(source_type_label("wechat"), "单聊")
        self.assertEqual(source_type_label("group_chat"), "群聊")
        self.assertEqual(source_type_label("git"), "Git 记录")
        self.assertEqual(evidence_strength_label("strong"), "强")
        self.assertEqual(evidence_strength_label("medium"), "中")
        self.assertEqual(evidence_strength_label("weak"), "弱")

    def test_unknown_values_fall_back_to_original_text(self):
        self.assertEqual(event_type_label("custom_type"), "custom_type")
        self.assertEqual(quality_gate_label("custom_gate"), "custom_gate")
        self.assertEqual(risk_flag_label("custom_risk"), "custom_risk")
        self.assertEqual(source_type_label("custom_source"), "custom_source")
        self.assertEqual(evidence_strength_label("custom_strength"), "custom_strength")


if __name__ == "__main__":
    unittest.main()
