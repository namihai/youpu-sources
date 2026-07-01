from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from youpu.domain.accepted import ACCEPTED_FIELD_NAME_RE
from youpu.domain.accepted import AcceptedField
from youpu.infra.schema_store import SchemaConfigError
from youpu.infra.schema_store import get_schema_path
from youpu.infra.schema_store import load_schema_document


def _schema_error(repo_root: Path, name: str, message: str, code: str) -> SchemaConfigError:
    return SchemaConfigError(
        path=get_schema_path(repo_root, name),
        message=message,
        code=code,
    )


@dataclass(frozen=True)
class AcceptedSchemaConfig:
    fields: list[AcceptedField]
    template_path: Path


@dataclass(frozen=True)
class SchemaConfig:
    accepted: AcceptedSchemaConfig


def _parse_accepted_schema(repo_root: Path, raw: object) -> AcceptedSchemaConfig:
    if not isinstance(raw, dict):
        raise _schema_error(repo_root, "accepted", "accepted schema must be a mapping", "accepted_schema_invalid")

    fields = raw.get("fields")
    if not isinstance(fields, list) or not fields:
        raise _schema_error(repo_root, "accepted", "accepted schema must define a non-empty `fields` list", "accepted_schema_invalid")

    parsed: list[AcceptedField] = []
    seen_names: set[str] = set()
    for index, item in enumerate(fields, start=1):
        if not isinstance(item, dict):
            raise _schema_error(repo_root, "accepted", f"accepted schema field #{index} must be a mapping", "accepted_schema_invalid")

        name = item.get("name")
        field_type = item.get("type")
        required = item.get("required")
        example = item.get("example")
        choices_raw = item.get("choices")

        if not isinstance(name, str) or not name:
            raise _schema_error(repo_root, "accepted", f"accepted schema field #{index} is missing a valid `name`", "accepted_schema_invalid")
        if not ACCEPTED_FIELD_NAME_RE.match(name):
            raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` must use YAML-safe identifier syntax", "accepted_schema_invalid")
        if name in seen_names:
            raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` is duplicated", "accepted_schema_invalid")
        if field_type not in {"string", "url", "inline_array"}:
            raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` has unsupported type `{field_type}`", "accepted_schema_invalid")
        if not isinstance(required, bool):
            raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` must define boolean `required`", "accepted_schema_invalid")
        if not isinstance(example, str) or not example:
            raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` must define non-empty `example`", "accepted_schema_invalid")
        if choices_raw is not None:
            if field_type != "string":
                raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` can only use `choices` with type `string`", "accepted_schema_invalid")
            if not isinstance(choices_raw, list) or not choices_raw:
                raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` must define a non-empty `choices` list", "accepted_schema_invalid")
            if not all(isinstance(choice, str) and choice for choice in choices_raw):
                raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` choices must be non-empty strings", "accepted_schema_invalid")
            if len(set(choices_raw)) != len(choices_raw):
                raise _schema_error(repo_root, "accepted", f"accepted schema field `{name}` choices must not contain duplicates", "accepted_schema_invalid")
            choices: tuple[str, ...] | None = tuple(choices_raw)
        else:
            choices = None

        seen_names.add(name)
        parsed.append(AcceptedField(name=name, field_type=field_type, required=required, example=example, choices=choices))

    template = raw.get("template")
    if not isinstance(template, dict):
        raise _schema_error(repo_root, "accepted", "accepted schema must define `template.path`", "accepted_schema_invalid")
    path = template.get("path")
    if not isinstance(path, str) or not path:
        raise _schema_error(repo_root, "accepted", "accepted schema must define non-empty `template.path`", "accepted_schema_invalid")

    return AcceptedSchemaConfig(fields=parsed, template_path=repo_root / path)


def load_schema_config(repo_root: Path) -> SchemaConfig:
    return SchemaConfig(
        accepted=load_accepted_schema_config(repo_root),
    )


def get_accepted_fields(repo_root: Path) -> list[AcceptedField]:
    return load_accepted_schema_config(repo_root).fields


def get_accepted_field_order(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root)]


def get_accepted_required_fields(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root) if field.required]


def get_accepted_array_fields(repo_root: Path) -> list[str]:
    return [field.name for field in get_accepted_fields(repo_root) if field.is_array]


def get_accepted_allowed_fields(repo_root: Path) -> set[str]:
    return {field.name for field in get_accepted_fields(repo_root)}


def get_accepted_template_path(repo_root: Path) -> Path:
    return load_accepted_schema_config(repo_root).template_path


@dataclass(frozen=True)
class SchemaRules:
    accepted_required_fields: list[str]
    accepted_allowed_fields: set[str]
    accepted_array_fields: list[str]
    accepted_enum_fields: dict[str, tuple[str, ...]]


def load_schema_rules(repo_root: Path) -> SchemaRules:
    config = load_schema_config(repo_root)
    return SchemaRules(
        accepted_required_fields=[field.name for field in config.accepted.fields if field.required],
        accepted_allowed_fields={field.name for field in config.accepted.fields},
        accepted_array_fields=[field.name for field in config.accepted.fields if field.is_array],
        accepted_enum_fields={field.name: field.choices for field in config.accepted.fields if field.choices is not None},
    )


def load_accepted_schema_config(repo_root: Path) -> AcceptedSchemaConfig:
    accepted_raw = load_schema_document(get_schema_path(repo_root, "accepted"))
    return _parse_accepted_schema(repo_root, accepted_raw)
