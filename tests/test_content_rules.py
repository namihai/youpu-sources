from __future__ import annotations

import unittest
from pathlib import Path

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.rules import validate_accepted_document
from youpu.domain.rules import validate_rejected_values
from youpu.domain.schema import SchemaRules


class ContentRulesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rules = SchemaRules(
            accepted_required_fields=["title", "canonical_url", "tags"],
            accepted_allowed_fields={"title", "canonical_url", "tags"},
            accepted_array_fields=["tags"],
            rejected_column_names=["url", "title", "reason"],
        )

    def test_validate_accepted_document_reports_schema_errors(self) -> None:
        doc = AcceptedDocument(
            path=Path("example.md"),
            index=1,
            slug="example",
            heading=None,
            yaml_fields={
                "title": "Example",
                "canonical_url": "not-a-url",
                "tags": "tag-a, tag-b",
                "extra": "value",
            },
            body="body",
        )

        diagnostics, normalized_url = validate_accepted_document(
            doc,
            rel_path="data/accepted/example.md",
            rules=self.rules,
            code_prefix="accepted",
        )

        self.assertIsNone(normalized_url)
        self.assertEqual(
            [item.code for item in diagnostics],
            [
                "accepted_missing_h1",
                "accepted_unknown_field",
                "accepted_invalid_array",
                "accepted_invalid_canonical_url",
            ],
        )

    def test_validate_accepted_document_returns_normalized_url_when_valid(self) -> None:
        doc = AcceptedDocument(
            path=Path("example.md"),
            index=1,
            slug="example",
            heading="Example",
            yaml_fields={
                "title": "Example",
                "canonical_url": "https://EXAMPLE.com/path?utm_source=x&id=1",
                "tags": "[tag-a]",
            },
            body="body",
        )

        diagnostics, normalized_url = validate_accepted_document(
            doc,
            rel_path="staging/accepted/example.md",
            rules=self.rules,
            code_prefix="staging_accepted",
        )

        self.assertEqual(diagnostics, [])
        self.assertEqual(normalized_url, "https://example.com/path?id=1")

    def test_validate_rejected_values_reports_missing_and_invalid_fields(self) -> None:
        diagnostics, normalized_url = validate_rejected_values(
            url="bad-url",
            title="",
            reason="",
            path="data/rejected.csv:2",
            code_prefix="rejected",
        )

        self.assertIsNone(normalized_url)
        self.assertEqual(
            [item.code for item in diagnostics],
            [
                "rejected_invalid_url",
                "rejected_missing_title",
                "rejected_missing_reason",
            ],
        )

    def test_validate_accepted_document_rejects_malformed_inline_array(self) -> None:
        doc = AcceptedDocument(
            path=Path("example.md"),
            index=1,
            slug="example",
            heading="Example",
            yaml_fields={
                "title": "Example",
                "canonical_url": "https://example.com/path",
                "tags": "[tag-a,,tag-b]",
            },
            body="body",
        )

        diagnostics, normalized_url = validate_accepted_document(
            doc,
            rel_path="staging/accepted/example.md",
            rules=self.rules,
            code_prefix="staging_accepted",
        )

        self.assertEqual(normalized_url, "https://example.com/path")
        self.assertEqual([item.code for item in diagnostics], ["staging_accepted_invalid_array"])


if __name__ == "__main__":
    unittest.main()
