from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cli.schema_config import SchemaConfigError
from cli.schema_config import get_schema_path
from cli.schema_config import load_schema_document


@dataclass(frozen=True)
class AcceptedField:
    name: str
    field_type: str
    required: bool
    example: str

    @property
    def is_array(self) -> bool:
        return self.field_type == "inline_array"


def _schema_error(repo_root: Path, message: str, code: str) -> SchemaConfigError:
    return SchemaConfigError(
        path=get_schema_path(repo_root, "accepted"),
        message=message,
        code=code,
    )


def get_accepted_fields(repo_root: Path) -> list[AcceptedField]:
    raw = load_schema_document(str(get_schema_path(repo_root, "accepted")))
    if not isinstance(raw, dict):
        raise _schema_error(repo_root, "accepted schema must be a mapping", "accepted_schema_invalid")

    fields = raw.get("fields")
    if not isinstance(fields, list) or not fields:
        raise _schema_error(repo_root, "accepted schema must define a non-empty `fields` list", "accepted_schema_invalid")

    parsed: list[AcceptedField] = []
    seen_names: set[str] = set()
    for index, item in enumerate(fields, start=1):
        if not isinstance(item, dict):
            raise _schema_error(
                repo_root,
                f"accepted schema field #{index} must be a mapping",
                "accepted_schema_invalid",
            )

        name = item.get("name")
        field_type = item.get("type")
        required = item.get("required")
        example = item.get("example")

        if not isinstance(name, str) or not name:
            raise _schema_error(repo_root, f"accepted schema field #{index} is missing a valid `name`", "accepted_schema_invalid")
        if name in seen_names:
            raise _schema_error(repo_root, f"accepted schema field `{name}` is duplicated", "accepted_schema_invalid")
        if field_type not in {"string", "url", "inline_array"}:
            raise _schema_error(
                repo_root,
                f"accepted schema field `{name}` has unsupported type `{field_type}`",
                "accepted_schema_invalid",
            )
        if not isinstance(required, bool):
            raise _schema_error(
                repo_root,
                f"accepted schema field `{name}` must define boolean `required`",
                "accepted_schema_invalid",
            )
        if not isinstance(example, str) or not example:
            raise _schema_error(
                repo_root,
                f"accepted schema field `{name}` must define non-empty `example`",
                "accepted_schema_invalid",
            )

        seen_names.add(name)
        parsed.append(
            AcceptedField(
                name=name,
                field_type=field_type,
                required=required,
                example=example,
            )
        )

    return parsed


def get_accepted_template_path(repo_root: Path) -> Path:
    raw = load_schema_document(str(get_schema_path(repo_root, "accepted")))
    if not isinstance(raw, dict):
        raise _schema_error(repo_root, "accepted schema must be a mapping", "accepted_schema_invalid")
    template = raw.get("template")
    if not isinstance(template, dict):
        raise _schema_error(repo_root, "accepted schema must define `template.path`", "accepted_schema_invalid")
    path = template.get("path")
    if not isinstance(path, str) or not path:
        raise _schema_error(repo_root, "accepted schema must define non-empty `template.path`", "accepted_schema_invalid")
    return repo_root / path


def get_accepted_field_order(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root)]


def get_accepted_required_fields(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root) if field.required]


def get_accepted_array_fields(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root) if field.is_array]


def get_accepted_allowed_fields(repo_root: Path) -> set[str]:
    return {field.name for field in get_accepted_fields(repo_root)}
