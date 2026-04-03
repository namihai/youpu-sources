from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.support import create_repo_skeleton
from youpu.app.checks import run_imports_check
from youpu.app.checks import run_merge_check


class AppChecksTests(unittest.TestCase):
    def test_run_imports_check_counts_ready_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            (repo_root / "staging" / "accepted" / "sample.md").write_text(
                """---
title: "Sample"
summary: "Sample text dataset source."
canonical_url: "https://example.com/path"
publisher: "Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )
            (repo_root / "staging" / "rejected" / "rows.csv").write_text(
                "url,title,reason\nhttps://example.com/rejected,Rejected,not fit\n",
                encoding="utf-8",
            )

            report = run_imports_check(repo_root)

        self.assertTrue(report.ok)
        self.assertEqual(report.accepted_ready, 1)
        self.assertEqual(report.rejected_ready, 1)
        self.assertTrue(report.has_candidates)

    def test_run_merge_check_flags_pending_staging(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            (repo_root / "staging" / "accepted" / "sample.md").write_text(
                """---
title: "Sample"
summary: "Sample text dataset source."
canonical_url: "https://example.com/path"
publisher: "Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )

            report = run_merge_check(repo_root)

        self.assertFalse(report.ok)
        self.assertTrue(report.pending_staging)
        self.assertTrue(any(item.code == "merge_pending_staging" for item in report.diagnostics))


if __name__ == "__main__":
    unittest.main()
