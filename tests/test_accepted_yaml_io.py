from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from youpu.app.ingest import serialize_accepted
from youpu.domain.accepted import AcceptedDocument
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.accepted_store import parse_simple_yaml_block


class AcceptedYamlIoTests(unittest.TestCase):
    def test_parse_simple_yaml_block_supports_quoted_scalars(self) -> None:
        text = """---
title: "Title: Example"
summary: "Quoted \\\"value\\\""
publisher: "Org: Example"
---
"""

        fields = parse_simple_yaml_block(text)

        self.assertEqual(fields["title"], "Title: Example")
        self.assertEqual(fields["summary"], 'Quoted "value"')
        self.assertEqual(fields["publisher"], "Org: Example")

    def test_parse_simple_yaml_block_rejects_invalid_lines(self) -> None:
        text = """---
title = invalid
---
"""

        with self.assertRaisesRegex(ValueError, "expected `key: value`"):
            parse_simple_yaml_block(text)

    def test_serialize_accepted_round_trips_special_characters(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        doc = AcceptedDocument(
            path=repo_root / "staging/accepted/example.md",
            index=None,
            slug=None,
            yaml_fields={
                "title": "Title: Example",
                "summary": 'Quoted "value"',
                "canonical_url": "https://EXAMPLE.com/path?utm_source=x&id=1",
                "publisher": "Org: Example",
                "modality": "multimodal",
                "access_level": "request",
                "tags": "[tag-a, tag-b]",
            },
            body="## Notes\n\nBody text.\n",
        )

        rendered = serialize_accepted(doc, repo_root)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SRC-0001-example.md"
            path.write_text(rendered, encoding="utf-8")
            parsed = parse_accepted_document(path)

        self.assertEqual(parsed.yaml_fields["summary"], 'Quoted "value"')
        self.assertEqual(parsed.yaml_fields["publisher"], "Org: Example")
        self.assertEqual(parsed.yaml_fields["modality"], "multimodal")
        self.assertEqual(parsed.yaml_fields["access_level"], "request")
        self.assertEqual(parsed.yaml_fields["tags"], "[tag-a, tag-b]")
        self.assertEqual(parsed.yaml_fields["canonical_url"], "https://example.com/path?id=1")
        self.assertEqual(parsed.body, "## Notes\n\nBody text.\n")

    def test_parse_accepted_document_preserves_leading_indentation_in_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SRC-0001-example.md"
            path.write_text(
                """---
title: "Title"
canonical_url: "https://example.com"
---
    code block
""",
                encoding="utf-8",
            )

            parsed = parse_accepted_document(path)

        self.assertEqual(parsed.body, "    code block\n")


if __name__ == "__main__":
    unittest.main()
