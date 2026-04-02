from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from youpu.app.ingest import build_analysis
from youpu.app.ingest import merge_ingest
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.rejected_store import parse_rejected_csv
from tests.support import create_repo_skeleton


class IngestMergeTests(unittest.TestCase):
    def test_merge_ingest_moves_ready_items_into_data_area(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = create_repo_skeleton(Path(tmp))
            accepted_path = repo_root / "staging" / "accepted" / "sample.md"
            accepted_path.write_text(
                """# Sample Title

```yaml
title: "Sample Title"
subtitle: "Subtitle: value"
canonical_url: "https://example.com/dataset?utm_source=x&id=1"
domain: "领域"
content_type: "内容类型"
data_form: "文本"
data_type: "元数据"
region: "CN"
source_type: "机构"
source_org: "Example Org"
permissions: "internal: review"
tags: [tag-a, tag-b]
use_cases: [case-a]
```

## Notes

Body text.
""",
                encoding="utf-8",
            )
            rejected_path = repo_root / "staging" / "rejected" / "rows.csv"
            rejected_path.write_text(
                "url,title,reason\nhttps://example.com/rejected?utm_source=x,Rejected,not fit\n",
                encoding="utf-8",
            )

            analysis = build_analysis(repo_root)
            self.assertEqual(analysis.diagnostics, [])

            result = merge_ingest(repo_root, analysis)

            accepted_files = list((repo_root / "data" / "accepted").glob("*.md"))
            self.assertEqual(result["imported_accepted"], 1)
            self.assertEqual(result["imported_rejected"], 1)
            self.assertEqual(len(accepted_files), 1)
            self.assertFalse(accepted_path.exists())
            self.assertFalse(rejected_path.exists())

            accepted_doc = parse_accepted_document(accepted_files[0])
            rejected_csv = parse_rejected_csv(repo_root / "data" / "rejected.csv")

        self.assertEqual(accepted_doc.yaml_fields["canonical_url"], "https://example.com/dataset?id=1")
        self.assertEqual(accepted_doc.yaml_fields["subtitle"], "Subtitle: value")
        self.assertEqual(rejected_csv.rows[0].url, "https://example.com/rejected")


if __name__ == "__main__":
    unittest.main()
