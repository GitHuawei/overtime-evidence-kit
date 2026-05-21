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
        self.assertIn("does not provide legal advice", readme)
        self.assertIn("v0.1.0 - planned", changelog)
        self.assertIn("mock-only boundaries", changelog)
        self.assertIn("Known limitations", changelog)
        self.assertIn("Real evidence handling is not included", changelog)

    def test_public_launch_docs_are_public_safe(self):
        public_launch = self.read("docs/public-launch.md")
        repository_settings = self.read("docs/repository-settings.md")

        self.assertIn("v0.1.0 Release Candidate", public_launch)
        self.assertIn("mock-only", public_launch)
        self.assertIn("no GitHub Release or tag", public_launch)
        self.assertIn("does not provide legal advice", public_launch)
        self.assertIn("Post-launch Monitoring Checklist", public_launch)

        self.assertIn("Mock-only toolkit", repository_settings)
        self.assertIn("Suggested topics", repository_settings)
        self.assertIn("Do not create a GitHub Release or tag", repository_settings)
        self.assertIn("No legal conclusions", repository_settings)

    def test_release_checklist_blocks_private_plans_and_release_actions(self):
        checklist = self.read("docs/release-checklist.md")

        self.assertIn("controlled public launch", checklist)
        self.assertIn("docs/plans/", checklist)
        self.assertIn("No GitHub Release or tag", checklist)
        self.assertIn("Known limitations", checklist)

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
