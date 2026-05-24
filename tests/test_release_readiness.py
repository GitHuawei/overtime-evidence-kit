import unittest
from pathlib import Path

from scripts import check_all


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_release_readiness_audit_passes(self):
        self.assertTrue(check_all.check_release_readiness_files())

    def test_readme_and_changelog_state_formal_release_boundary(self):
        readme = self.read("README.md")
        changelog = self.read("CHANGELOG.md")

        self.assertIn("v0.1.0 正式发布版", readme)
        self.assertIn("mock-only", readme)
        self.assertIn("可校验、可复核、可展示", readme)
        self.assertIn("Excel-friendly UTF-8 with BOM", readme)
        self.assertIn("docs/faq.md", readme)
        self.assertIn("docs/service-overview.md", readme)
        self.assertIn("不处理真实案件材料", readme)
        self.assertIn("不提供法律意见", readme)
        self.assertIn("python scripts/run_demo.py", readme)
        self.assertIn("outputs/demo/", readme)
        self.assertIn("v0.1.0 - 2026-05-24", changelog)
        self.assertIn("mock-only", changelog)
        self.assertIn("Launch-ready updates", changelog)
        self.assertIn("Excel-friendly UTF-8 with BOM", changelog)
        self.assertIn("Known limitations", changelog)
        self.assertIn("不处理真实案件材料", changelog)

    def test_public_launch_docs_are_public_safe(self):
        public_launch = self.read("docs/public-launch.md")
        repository_settings = self.read("docs/repository-settings.md")

        self.assertIn("v0.1.0", public_launch)
        self.assertIn("已发布", public_launch)
        self.assertIn("mock-only", public_launch)
        self.assertIn("不要创建新的 tag 或 release", public_launch)
        self.assertIn("不提供法律意见", public_launch)
        self.assertIn("post-launch monitoring checklist", public_launch)

        self.assertIn("GitHub repository settings", repository_settings)
        self.assertIn("建议 topics", repository_settings)
        self.assertIn("不要创建新的 GitHub Release 或 tag", repository_settings)
        self.assertIn("不加入法律结论", repository_settings)

    def test_release_checklist_blocks_private_plans_and_release_actions(self):
        checklist = self.read("docs/release-checklist.md")

        self.assertIn("v0.1.0", checklist)
        self.assertIn("docs/plans/", checklist)
        self.assertIn("docs/faq.md", checklist)
        self.assertIn("私有服务材料隔离", checklist)
        self.assertIn("不要创建新的 GitHub Release 或 tag", checklist)
        self.assertIn("Known limitations", checklist)

    def test_demo_doc_explains_chinese_run_path_and_boundaries(self):
        demo = self.read("docs/demo.md")

        self.assertIn("python scripts/run_demo.py", demo)
        self.assertIn("outputs/demo/", demo)
        self.assertIn("Excel-friendly UTF-8 with BOM", demo)
        self.assertIn("docs/service-overview.md", demo)
        self.assertIn("不读取用户真实文件", demo)
        self.assertIn("不要把真实案件材料脱敏后放进本仓库", demo)

    def test_formal_launch_docs_are_public_safe(self):
        faq = self.read("docs/faq.md")
        positioning = self.read("docs/positioning.md")
        service_overview = self.read("docs/service-overview.md")
        customer_safety = self.read("docs/customer-safety.md")
        business_boundary = self.read("docs/business-boundary.md")
        roadmap = self.read("docs/roadmap.md")

        self.assertIn("这个项目能处理我的真实微信聊天记录吗", faq)
        self.assertIn("不能", faq)
        self.assertIn("这个项目是不是法律意见", faq)
        self.assertIn("Excel-friendly UTF-8 with BOM", faq)

        self.assertIn("结构化方法", positioning)
        self.assertIn("可追踪", positioning)
        self.assertIn("可复核", positioning)

        self.assertIn("公开安全的服务咨询边界", service_overview)
        self.assertIn("GitHub 不接收真实材料", service_overview)
        self.assertIn("法律意见", service_overview)
        self.assertIn("真实服务流程", service_overview)

        self.assertIn("不要公开上传", customer_safety)
        self.assertIn("真实微信聊天", customer_safety)
        self.assertIn("GitHub issue", customer_safety)
        self.assertIn("本项目不提供法律意见", customer_safety)

        self.assertIn("Public Business Boundary", business_boundary)
        self.assertIn("不是价格表", business_boundary)
        self.assertIn("不在公开仓库说明", business_boundary)
        self.assertIn("不要在 GitHub issue", business_boundary)

        self.assertIn("当前公开版本：`v0.1.0`", roadmap)
        self.assertIn("v0.1.0 发布后校准", roadmap)
        self.assertIn("服务咨询相关方向", roadmap)
        self.assertIn("永久不纳入公开仓库范围", roadmap)

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
