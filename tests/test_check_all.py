import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckAllTest(unittest.TestCase):
    def test_check_all_script_exists(self):
        self.assertTrue((ROOT / "scripts" / "check_all.py").is_file())

    def test_check_all_runs_successfully_from_repo_root(self):
        if os.environ.get("OVERTIME_CHECK_ALL_RUNNING") == "1":
            self.skipTest("avoid recursive check_all invocation")
        result = subprocess.run(
            [sys.executable, "scripts/check_all.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK: all checks passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
