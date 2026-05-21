import unittest
from pathlib import Path

from scripts import check_all


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_release_readiness_audit_passes(self):
        self.assertTrue(check_all.check_release_readiness_files())

    def test_readme_and_changelog_state_release_candidate_boundary(self):
        readme = self.read("README.md")
        changelog = self.read("CHANGELOG.md")

        self.assertIn("v0.1.0 Release Candidate", readme)
        self.assertIn("mock-only", readme)
        self.assertIn("不处理真实案件材料", readme)
        self.assertIn("不提供法律意见", readme)
        self.assertIn("python scripts/run_demo.py", readme)
        self.assertIn("outputs/demo/", readme)
        self.assertIn("v0.1.0 - planned", changelog)
        self.assertIn("mock-only", changelog)
        self.assertIn("Known limitations", changelog)
        self.assertIn("不处理真实案件材料", changelog)

    def test_public_launch_docs_are_public_safe(self):
        public_launch = self.read("docs/public-launch.md")
        repository_settings = self.read("docs/repository-settings.md")

        self.assertIn("v0.1.0 Release Candidate", public_launch)
        self.assertIn("mock-only", public_launch)
        self.assertIn("未创建 GitHub Release 或 tag", public_launch)
        self.assertIn("不提供法律意见", public_launch)
        self.assertIn("post-launch monitoring checklist", public_launch)

        self.assertIn("GitHub repository settings", repository_settings)
        self.assertIn("建议 topics", repository_settings)
        self.assertIn("不要创建 GitHub Release 或 tag", repository_settings)
        self.assertIn("不加入法律结论", repository_settings)

    def test_release_checklist_blocks_private_plans_and_release_actions(self):
        checklist = self.read("docs/release-checklist.md")

        self.assertIn("受控公开", checklist)
        self.assertIn("docs/plans/", checklist)
        self.assertIn("不要创建 GitHub Release 或 tag", checklist)
        self.assertIn("Known limitations", checklist)

    def test_demo_doc_explains_chinese_run_path_and_boundaries(self):
        demo = self.read("docs/demo.md")

        self.assertIn("python scripts/run_demo.py", demo)
        self.assertIn("outputs/demo/", demo)
        self.assertIn("不读取用户真实文件", demo)
        self.assertIn("不要把真实案件材料脱敏后放进本仓库", demo)

    def test_issue_templates_warn_against_real_material(self):
        for relative_path in [
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/ISSUE_TEMPLATE/privacy_boundary.md",
        ]:
            with self.subTest(relative_path=relative_path):
                text = self.read(relative_path)
                self.assertIn("Mock-only Confirmation", text)
                self.assertIn("real WeChat", text)
                self.assertIn("real Git", text)
                self.assertIn("phone", text)

    def test_pull_request_template_has_privacy_checklist(self):
        text = self.read(".github/PULL_REQUEST_TEMPLATE.md")

        self.assertIn("Mock-only and Privacy Checklist", text)
        self.assertIn("real WeChat chats", text)
        self.assertIn("real Git commits", text)
        self.assertIn("legal outcomes", text)


if __name__ == "__main__":
    unittest.main()
