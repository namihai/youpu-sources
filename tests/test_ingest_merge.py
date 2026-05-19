from __future__ import annotations

import tempfile
import unittest
import os
from unittest.mock import patch
from pathlib import Path

from youpu.app.ingest import build_analysis
from youpu.app.ingest import merge_ingest
from youpu.infra.accepted_store import parse_accepted_document
from tests.support import create_repo_skeleton


class IngestMergeTests(unittest.TestCase):
    def test_merge_ingest_moves_ready_items_into_data_area(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            accepted_path = repo_root / "staging" / "sample.md"
            accepted_path.write_text(
                """---
title: "Sample Title"
summary: "A sample text dataset source."
canonical_url: "https://example.com/dataset?utm_source=x&id=1"
publisher: "Example Org"
modality: "text"
access_level: "request"
---

## Notes

Body text.
""",
                encoding="utf-8",
            )
            analysis = build_analysis(repo_root)
            self.assertEqual(analysis.diagnostics, [])

            result = merge_ingest(repo_root, analysis)

            accepted_files = list((repo_root / "data").glob("*.md"))
            self.assertEqual(result["imported_accepted"], 1)
            self.assertEqual(len(accepted_files), 1)
            self.assertFalse(accepted_path.exists())

            accepted_doc = parse_accepted_document(accepted_files[0])

        self.assertEqual(accepted_doc.yaml_fields["canonical_url"], "https://example.com/dataset?id=1")
        self.assertEqual(accepted_doc.yaml_fields["summary"], "A sample text dataset source.")
        self.assertEqual(accepted_doc.yaml_fields["publisher"], "Example Org")

    def test_invalid_staging_filename_is_not_slugified_or_imported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            accepted_path = repo_root / "staging" / "Sample Dataset.md"
            accepted_path.write_text(
                """---
title: "Sample Title"
summary: "A sample text dataset source."
canonical_url: "https://example.com/dataset"
publisher: "Example Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )

            analysis = build_analysis(repo_root)
            result = merge_ingest(repo_root, analysis)

            accepted_files = list((repo_root / "data").glob("*.md"))
            self.assertTrue(any(item.code == "staging_accepted_invalid_filename" for item in analysis.diagnostics))
            self.assertEqual(analysis.accepted_ready, [])
            self.assertEqual(result["imported_accepted"], 0)
            self.assertEqual(accepted_files, [])
            self.assertTrue(accepted_path.exists())

    def test_merge_ingest_keeps_sources_when_accepted_write_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            accepted_path = repo_root / "staging" / "sample.md"
            accepted_path.write_text(
                """---
title: "Sample Title"
summary: "A sample text dataset source."
canonical_url: "https://example.com/dataset"
publisher: "Example Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )

            analysis = build_analysis(repo_root)
            self.assertEqual(analysis.diagnostics, [])

            with patch("youpu.app.ingest.serialize_accepted", side_effect=OSError("simulated write failure")):
                with self.assertRaisesRegex(OSError, "simulated write failure"):
                    merge_ingest(repo_root, analysis)

            accepted_files = list((repo_root / "data").glob("*.md"))
            temp_files = list(repo_root.rglob("*.tmp"))
            self.assertEqual(accepted_files, [])
            self.assertTrue(accepted_path.exists())
            self.assertEqual(temp_files, [])

    def test_merge_ingest_uses_base_ref_for_next_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))

            from subprocess import run

            run(["git", "init", "-b", "main"], cwd=repo_root, check=True)
            run(["git", "config", "user.name", "Test User"], cwd=repo_root, check=True)
            run(["git", "config", "user.email", "test@example.com"], cwd=repo_root, check=True)
            run(["git", "add", "."], cwd=repo_root, check=True)
            run(["git", "commit", "-m", "initial"], cwd=repo_root, check=True)
            run(["git", "branch", "feature"], cwd=repo_root, check=True)

            (repo_root / "data" / "SRC-0007-existing.md").write_text(
                """---
title: "Existing"
summary: "Existing sample text dataset source."
canonical_url: "https://example.com/existing"
publisher: "Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )
            run(["git", "add", "."], cwd=repo_root, check=True)
            run(["git", "commit", "-m", "main accepted"], cwd=repo_root, check=True)
            run(["git", "checkout", "feature"], cwd=repo_root, check=True)

            accepted_path = repo_root / "staging" / "sample.md"
            accepted_path.write_text(
                """---
title: "Sample Title"
summary: "A sample text dataset source."
canonical_url: "https://example.com/dataset"
publisher: "Example Org"
modality: "text"
access_level: "open"
---
""",
                encoding="utf-8",
            )

            analysis = build_analysis(repo_root)
            self.assertEqual(analysis.diagnostics, [])

            original_env = os.environ.get("YOUPU_ACCEPTED_BASE_REF")
            os.environ["YOUPU_ACCEPTED_BASE_REF"] = "main"
            try:
                merge_ingest(repo_root, analysis)
            finally:
                if original_env is None:
                    os.environ.pop("YOUPU_ACCEPTED_BASE_REF", None)
                else:
                    os.environ["YOUPU_ACCEPTED_BASE_REF"] = original_env

            accepted_files = sorted(path.name for path in (repo_root / "data").glob("*.md"))

        self.assertEqual(accepted_files, ["SRC-0008-sample.md"])


if __name__ == "__main__":
    unittest.main()
