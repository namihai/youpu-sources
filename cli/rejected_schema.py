from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cli.schema_config import SchemaConfigError
from cli.schema_config import get_schema_path
from cli.schema_config import load_schema_document


@dataclass(frozen=True)
class RejectedColumn:
    name: str
    required: bool
    example: str


def _schema_error(repo_root: Path, message: str, code: str) -> SchemaConfigError:
    return SchemaConfigError(
        path=get_schema_path(repo_root, "rejected"),
        message=message,
        code=code,
    )


def get_rejected_columns(repo_root: Path) -> list[RejectedColumn]:
    raw = load_schema_document(str(get_schema_path(repo_root, "rejected")))
    if not isinstance(raw, dict):
        raise _schema_error(repo_root, "rejected schema must be a mapping", "rejected_schema_invalid")

    columns = raw.get("columns")
    if not isinstance(columns, list) or not columns:
        raise _schema_error(repo_root, "rejected schema must define a non-empty `columns` list", "rejected_schema_invalid")

    parsed: list[RejectedColumn] = []
    seen_names: set[str] = set()
    for index, item in enumerate(columns, start=1):
        if not isinstance(item, dict):
            raise _schema_error(
                repo_root,
                f"rejected schema column #{index} must be a mapping",
                "rejected_schema_invalid",
            )

        name = item.get("name")
        required = item.get("required")
        example = item.get("example")

        if not isinstance(name, str) or not name:
            raise _schema_error(repo_root, f"rejected schema column #{index} is missing a valid `name`", "rejected_schema_invalid")
        if name in seen_names:
            raise _schema_error(repo_root, f"rejected schema column `{name}` is duplicated", "rejected_schema_invalid")
        if not isinstance(required, bool):
            raise _schema_error(
                repo_root,
                f"rejected schema column `{name}` must define boolean `required`",
                "rejected_schema_invalid",
            )
        if not isinstance(example, str) or not example:
            raise _schema_error(
                repo_root,
                f"rejected schema column `{name}` must define non-empty `example`",
                "rejected_schema_invalid",
            )

        seen_names.add(name)
        parsed.append(
            RejectedColumn(
                name=name,
                required=required,
                example=example,
            )
        )

    return parsed


def get_rejected_template_path(repo_root: Path) -> Path:
    raw = load_schema_document(str(get_schema_path(repo_root, "rejected")))
    if not isinstance(raw, dict):
        raise _schema_error(repo_root, "rejected schema must be a mapping", "rejected_schema_invalid")
    template = raw.get("template")
    if not isinstance(template, dict):
        raise _schema_error(repo_root, "rejected schema must define `template.path`", "rejected_schema_invalid")
    path = template.get("path")
    if not isinstance(path, str) or not path:
        raise _schema_error(repo_root, "rejected schema must define non-empty `template.path`", "rejected_schema_invalid")
    return repo_root / path


def get_rejected_column_names(repo_root: Path) -> list[str]:
    return [column.name for column in get_rejected_columns(repo_root)]


def get_rejected_required_columns(repo_root: Path) -> list[str]:
    return [column.name for column in get_rejected_columns(repo_root) if column.required]
