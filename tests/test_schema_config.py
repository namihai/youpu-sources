from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from youpu.domain.schema import get_accepted_field_order
from youpu.infra.schema_store import SchemaConfigError
from youpu.infra.schema_store import get_schema_path
from youpu.infra.schema_store import load_schema_document


class SchemaConfigTests(unittest.TestCase):
    def test_get_schema_path_points_to_json(self) -> None:
        repo_root = Path("/tmp/example-repo")
        self.assertEqual(
            get_schema_path(repo_root, "accepted"),
            repo_root / "schemas" / "accepted.json",
        )

    def test_load_schema_document_reads_updated_content_without_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "accepted.json"
            path.write_text(json.dumps({"fields": [{"name": "title"}]}), encoding="utf-8")
            first = load_schema_document(path)

            path.write_text(json.dumps({"fields": [{"name": "subtitle"}]}), encoding="utf-8")
            second = load_schema_document(path)

        self.assertEqual(first, {"fields": [{"name": "title"}]})
        self.assertEqual(second, {"fields": [{"name": "subtitle"}]})

    def test_load_schema_document_reports_json_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "accepted.json"
            path.write_text('{"fields": [}', encoding="utf-8")

            with self.assertRaises(SchemaConfigError) as ctx:
                load_schema_document(path)

        self.assertEqual(ctx.exception.code, "schema_parse_error")
        self.assertEqual(ctx.exception.path, path)
        self.assertIn("invalid schema JSON", str(ctx.exception))

    def test_accepted_schema_uses_repo_json_file(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        field_order = get_accepted_field_order(repo_root)
        self.assertEqual(field_order[0], "title")
        self.assertEqual(field_order[-1], "use_cases")


if __name__ == "__main__":
    unittest.main()
