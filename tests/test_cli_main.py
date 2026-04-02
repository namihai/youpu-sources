from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import sys

from cli.main import main
from tests.support import create_repo_skeleton


class CliMainTests(unittest.TestCase):
    def test_report_command_writes_summary_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(["--root", str(repo_root), "report"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Repository summary", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_check_pr_without_candidates_fails_on_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(["--root", str(repo_root), "check-pr"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("staging_empty", stderr.getvalue())

    def test_module_entrypoint_matches_script_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            result = subprocess.run(
                [sys.executable, "-m", "cli.main", "--root", str(repo_root), "report"],
                check=False,
                capture_output=True,
                text=True,
                cwd=Path(__file__).resolve().parents[1],
            )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Repository summary", result.stdout)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
