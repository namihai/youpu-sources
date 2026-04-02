from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli.commands.ingest import serialize_accepted
from cli.repo import AcceptedDocument
from cli.repo import parse_accepted_document
from cli.repo import parse_simple_yaml_block


class AcceptedYamlIoTests(unittest.TestCase):
    def test_parse_simple_yaml_block_supports_quoted_scalars(self) -> None:
        text = """# Example

```yaml
title: "Title: Example"
subtitle: "Quoted \\\"value\\\""
tags: [tag-a, tag-b]
```
"""

        fields = parse_simple_yaml_block(text)

        self.assertEqual(fields["title"], "Title: Example")
        self.assertEqual(fields["subtitle"], 'Quoted "value"')
        self.assertEqual(fields["tags"], "[tag-a, tag-b]")

    def test_parse_simple_yaml_block_rejects_invalid_lines(self) -> None:
        text = """# Example

```yaml
title = invalid
```
"""

        with self.assertRaisesRegex(ValueError, "expected `key: value`"):
            parse_simple_yaml_block(text)

    def test_serialize_accepted_round_trips_special_characters(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        doc = AcceptedDocument(
            path=repo_root / "staging/accepted/example.md",
            index=None,
            slug=None,
            heading="Title: Example",
            yaml_fields={
                "title": "Title: Example",
                "subtitle": 'Quoted "value"',
                "canonical_url": "https://EXAMPLE.com/path?utm_source=x&id=1",
                "domain": "文化:艺术",
                "content_type": "目录",
                "data_form": "文本",
                "data_type": "元数据",
                "region": "CN",
                "source_type": "机构",
                "source_org": "Org",
                "permissions": "restricted: review",
                "tags": "[tag-a, tag-b]",
                "use_cases": "[case-a]",
            },
            body="## Notes\n\nBody text.\n",
        )

        rendered = serialize_accepted(doc, repo_root)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SRC-0001-example.md"
            path.write_text(rendered, encoding="utf-8")
            parsed = parse_accepted_document(path)

        self.assertEqual(parsed.heading, "Title: Example")
        self.assertEqual(parsed.yaml_fields["subtitle"], 'Quoted "value"')
        self.assertEqual(parsed.yaml_fields["domain"], "文化:艺术")
        self.assertEqual(parsed.yaml_fields["permissions"], "restricted: review")
        self.assertEqual(parsed.yaml_fields["canonical_url"], "https://example.com/path?id=1")
        self.assertEqual(parsed.body, "## Notes\n\nBody text.\n")


if __name__ == "__main__":
    unittest.main()
