from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SchemaConfigError(Exception):
    path: Path
    message: str
    code: str

    def __str__(self) -> str:
        return self.message


def get_schema_path(repo_root: Path, name: str) -> Path:
    return repo_root / "schemas" / f"{name}.json"


def load_schema_document(path_str: str) -> object:
    path = Path(path_str)
    if not path.exists():
        raise SchemaConfigError(
            path=path,
            message="schema file is missing",
            code="schema_missing",
        )

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SchemaConfigError(
            path=path,
            message=f"invalid schema JSON: {exc.msg} at line {exc.lineno} column {exc.colno}",
            code="schema_parse_error",
        ) from exc
