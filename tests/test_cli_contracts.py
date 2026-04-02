from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path

from tests.support import create_repo_skeleton
from youpu.cli.main import main


class CliContractsTests(unittest.TestCase):
    def test_check_pr_json_output_uses_stable_payload_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(["--format", "json", "--root", str(repo_root), "check-pr"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout.getvalue(), "")
        payload = json.loads(stderr.getvalue())
        self.assertEqual(payload["ok"], False)
        self.assertEqual(payload["command"], "check-pr")
        self.assertIn("diagnostics", payload)
        self.assertIn("data", payload)
        self.assertEqual(payload["data"]["validate_command"], "validate-repo")
        self.assertEqual(payload["data"]["schema_command"], "validate-schema")
        self.assertEqual(payload["data"]["staging_command"], "validate-imports")

    def test_check_merge_reports_pending_staging_in_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            staging_doc = repo_root / "staging" / "accepted" / "sample.md"
            staging_doc.write_text(
                """# Sample

```yaml
title: "Sample"
subtitle: "Subtitle"
canonical_url: "https://example.com/path"
domain: "领域"
content_type: "内容类型"
data_form: "文本"
data_type: "元数据"
region: "CN"
source_type: "机构"
source_org: "Org"
permissions: "公开"
tags: [tag-a]
use_cases: [case-a]
```
""",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = main(["--format", "json", "--root", str(repo_root), "check-merge"])

        self.assertEqual(exit_code, 1)
        payload = json.loads(stderr.getvalue())
        self.assertEqual(payload["command"], "check-merge")
        self.assertEqual(payload["data"]["pending_staging"], True)
        self.assertGreaterEqual(payload["data"]["staging_issues"], 0)
        self.assertTrue(any(item["code"] == "merge_pending_staging" for item in payload["diagnostics"]))

    def test_unknown_command_returns_usage_error_payload(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["unknown-command"])

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("usage_error", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
