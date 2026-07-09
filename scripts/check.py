#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(__file__).resolve().parent / "checker.json"
FIELD_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DATA_FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")
TRACKING_PARAM_PREFIXES = ("utm_",)
TRACKING_PARAMS = {"fbclid", "gclid", "dclid", "mc_cid", "mc_eid", "igshid"}


@dataclass(frozen=True)
class FieldRule:
    name: str
    field_type: str
    required: bool
    choices: tuple[str, ...]
    unique: bool


@dataclass(frozen=True)
class Config:
    data_dir: str
    min_body_chars: int
    fields: tuple[FieldRule, ...]


@dataclass(frozen=True)
class Diagnostic:
    level: str
    message: str
    path: str | None = None
    code: str | None = None

    def render(self) -> str:
        parts = [f"{self.level.upper()}: {self.message}"]
        if self.path:
            parts.append(f"path={self.path}")
        if self.code:
            parts.append(f"code={self.code}")
        return " | ".join(parts)


@dataclass(frozen=True)
class CheckResult:
    diagnostics: list[Diagnostic]
    file_count: int


class CheckError(ValueError):
    def __init__(self, message: str, *, code: str, path: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.path = path


def main() -> int:
    try:
        config = load_config(CONFIG_PATH)
    except CheckError as exc:
        diagnostic = Diagnostic(level="error", message=str(exc), path=exc.path, code=exc.code)
        print_report([diagnostic], file_count=0)
        return 1

    result = check_repo(config)
    errors = [item for item in result.diagnostics if item.level == "error"]
    print_report(errors, file_count=result.file_count)
    if errors:
        return 1

    return 0


def print_report(errors: list[Diagnostic], *, file_count: int) -> None:
    if not errors:
        print("Status: PASS")
        print(f"Files checked: {file_count}")
        return

    print("Status: FAIL")
    print(f"Files checked: {file_count}")
    print(f"Failures: {len(errors)}")
    print()
    print(f"{'Code':<24} File")
    print(f"{'-' * 24} {'-' * 40}")
    for error in errors:
        print(f"{error.code or 'unknown':<24} {error.path or '-'}")


def load_config(path: Path) -> Config:
    rel_path = str(path.relative_to(REPO_ROOT))
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CheckError("missing checker.json", path=rel_path, code="config_missing") from exc
    except json.JSONDecodeError as exc:
        raise CheckError(f"invalid checker.json: {exc.msg}", path=rel_path, code="config_invalid") from exc

    if not isinstance(raw, dict):
        raise CheckError("checker.json must be an object", path=rel_path, code="config_invalid")

    data_dir = raw.get("data_dir")
    if not isinstance(data_dir, str) or not data_dir:
        raise CheckError("checker.json must define non-empty data_dir", path=rel_path, code="config_invalid")
    if data_dir.startswith("/") or ".." in Path(data_dir).parts:
        raise CheckError("data_dir must be a relative path inside the repository", path=rel_path, code="config_invalid")

    min_body_chars = raw.get("min_body_chars", 0)
    if not isinstance(min_body_chars, int) or min_body_chars < 0:
        raise CheckError("checker.json must define non-negative integer min_body_chars when present", path=rel_path, code="config_invalid")

    fields_raw = raw.get("fields")
    if not isinstance(fields_raw, list) or not fields_raw:
        raise CheckError("checker.json must define a non-empty fields list", path=rel_path, code="config_invalid")

    fields: list[FieldRule] = []
    seen_names: set[str] = set()
    for index, item in enumerate(fields_raw, start=1):
        if not isinstance(item, dict):
            raise CheckError(f"field #{index} must be an object", path=rel_path, code="config_invalid")

        name = item.get("name")
        field_type = item.get("type")
        required = item.get("required")
        unique = item.get("unique", False)
        choices_raw = item.get("choices", [])

        if not isinstance(name, str) or not FIELD_NAME_RE.match(name):
            raise CheckError(f"field #{index} has invalid name", path=rel_path, code="config_invalid")
        if name in seen_names:
            raise CheckError(f"field {name!r} is duplicated", path=rel_path, code="config_invalid")
        if field_type not in {"string", "url", "enum", "inline_array"}:
            raise CheckError(f"field {name!r} has unsupported type {field_type!r}", path=rel_path, code="config_invalid")
        if not isinstance(required, bool):
            raise CheckError(f"field {name!r} must define boolean required", path=rel_path, code="config_invalid")
        if not isinstance(unique, bool):
            raise CheckError(f"field {name!r} must define boolean unique when present", path=rel_path, code="config_invalid")
        if field_type == "enum":
            if not isinstance(choices_raw, list) or not choices_raw:
                raise CheckError(f"field {name!r} must define non-empty choices", path=rel_path, code="config_invalid")
            if not all(isinstance(choice, str) and choice for choice in choices_raw):
                raise CheckError(f"field {name!r} choices must be non-empty strings", path=rel_path, code="config_invalid")
            if len(set(choices_raw)) != len(choices_raw):
                raise CheckError(f"field {name!r} choices must not contain duplicates", path=rel_path, code="config_invalid")
            choices = tuple(choices_raw)
        else:
            if choices_raw:
                raise CheckError(f"field {name!r} can only define choices when type is enum", path=rel_path, code="config_invalid")
            choices = ()

        seen_names.add(name)
        fields.append(FieldRule(name=name, field_type=field_type, required=required, choices=choices, unique=unique))

    return Config(data_dir=data_dir, min_body_chars=min_body_chars, fields=tuple(fields))


def check_repo(config: Config) -> CheckResult:
    diagnostics: list[Diagnostic] = []
    data_root = REPO_ROOT / config.data_dir
    if not data_root.exists():
        return CheckResult(
            diagnostics=[Diagnostic(level="error", message="data directory is missing", path=config.data_dir, code="data_missing")],
            file_count=0,
        )
    if not data_root.is_dir():
        return CheckResult(
            diagnostics=[Diagnostic(level="error", message="data path must be a directory", path=config.data_dir, code="data_not_directory")],
            file_count=0,
        )

    allowed_fields = {field.name for field in config.fields}
    unique_values: dict[str, dict[str, list[str]]] = {
        field.name: {} for field in config.fields if field.unique
    }
    title_values: dict[str, list[str]] = {}
    file_count = 0

    for path in sorted(data_root.iterdir()):
        rel_path = str(path.relative_to(REPO_ROOT))
        if path.name.startswith("."):
            continue
        if not path.is_file() or path.suffix != ".md":
            diagnostics.append(Diagnostic(level="error", message="data directory only accepts markdown files", path=rel_path, code="data_unexpected_file"))
            continue
        file_count += 1
        if not DATA_FILENAME_RE.match(path.name):
            diagnostics.append(Diagnostic(level="error", message="filename must use lowercase letters, numbers, and hyphens", path=rel_path, code="invalid_filename"))

        try:
            fields, body = parse_document(path)
        except CheckError as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=rel_path, code=exc.code))
            continue

        diagnostics.extend(validate_fields(fields, config.fields, allowed_fields, rel_path))
        body_chars = count_text_chars(body)
        if body_chars < config.min_body_chars:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"markdown body must contain at least {config.min_body_chars} non-whitespace character(s); found {body_chars}",
                    path=rel_path,
                    code="body_too_short",
                )
            )

        title = fields.get("title", "").strip()
        if title:
            title_values.setdefault(title, []).append(rel_path)

        for field in config.fields:
            if not field.unique:
                continue
            value = fields.get(field.name, "").strip()
            if not value:
                continue
            if field.field_type == "url":
                try:
                    value = normalize_url(value)
                except ValueError:
                    pass
            unique_values[field.name].setdefault(value, []).append(rel_path)

    for field_name, values in sorted(unique_values.items()):
        for value, paths in sorted(values.items()):
            if len(paths) > 1:
                code = "duplicate_source" if field_name == "canonical_url" else "duplicate_unique_field"
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"duplicate unique field {field_name!r}: {value}",
                        path=", ".join(paths),
                        code=code,
                    )
                )

    for title, paths in sorted(title_values.items()):
        if len(paths) > 1:
            diagnostics.append(Diagnostic(level="warning", message=f"duplicate title: {title}", path=", ".join(paths), code="duplicate_title"))

    return CheckResult(diagnostics=diagnostics, file_count=file_count)


def validate_fields(
    fields: dict[str, str],
    rules: tuple[FieldRule, ...],
    allowed_fields: set[str],
    rel_path: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for key in sorted(fields):
        if key not in allowed_fields:
            diagnostics.append(Diagnostic(level="error", message=f"unknown meta field {key!r}", path=rel_path, code="unknown_field"))

    for rule in rules:
        value = fields.get(rule.name, "").strip()
        if rule.required and not value:
            diagnostics.append(Diagnostic(level="error", message=f"missing required field {rule.name!r}", path=rel_path, code="missing_required_field"))
            continue
        if not value:
            continue

        if rule.field_type == "url":
            try:
                normalize_url(value)
            except ValueError as exc:
                diagnostics.append(Diagnostic(level="error", message=f"field {rule.name!r} {exc}", path=rel_path, code="invalid_url"))
        elif rule.field_type == "enum" and value not in rule.choices:
            choices = ", ".join(rule.choices)
            diagnostics.append(Diagnostic(level="error", message=f"field {rule.name!r} must be one of: {choices}", path=rel_path, code="invalid_enum"))
        elif rule.field_type == "inline_array":
            try:
                parse_inline_array(value)
            except ValueError as exc:
                diagnostics.append(Diagnostic(level="error", message=f"field {rule.name!r} {exc}", path=rel_path, code="invalid_inline_array"))

    return diagnostics


def parse_document(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise CheckError("markdown file must start with front matter delimited by ---", code="front_matter_missing")

    block_lines: list[str] = []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :])
            return parse_simple_yaml_block(block_lines), body
        block_lines.append(line)

    raise CheckError("missing closing --- for front matter", code="front_matter_unclosed")


def count_text_chars(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def parse_simple_yaml_block(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines, start=2):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in raw_line:
            raise CheckError(f"invalid front matter line {line_number}: expected key: value", code="front_matter_invalid")
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        if not FIELD_NAME_RE.match(key):
            raise CheckError(f"invalid front matter key at line {line_number}: {key!r}", code="front_matter_invalid")
        if key in fields:
            raise CheckError(f"duplicate front matter key at line {line_number}: {key}", code="front_matter_duplicate_key")
        fields[key] = parse_simple_yaml_scalar(raw_value, line_number=line_number)
    return fields


def parse_simple_yaml_scalar(raw_value: str, *, line_number: int) -> str:
    value = raw_value.strip()
    if value.startswith("[") and value.endswith("]"):
        return value
    if value.startswith('"') and value.endswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise CheckError(f"invalid quoted string at line {line_number}: {exc.msg}", code="front_matter_invalid") from exc
        if not isinstance(parsed, str):
            raise CheckError(f"value at line {line_number} must decode to a string", code="front_matter_invalid")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_inline_array(value: str) -> list[str]:
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        raise ValueError("must use inline array syntax like [a, b]")

    inner = stripped[1:-1].strip()
    if not inner:
        return []

    items: list[str] = []
    current: list[str] = []
    quote: str | None = None
    token_started = False

    for char in inner:
        if quote is not None:
            current.append(char)
            if char == quote and not is_escaped_double_quote(current, quote):
                quote = None
            continue

        if char in {"'", '"'}:
            quote = char
            token_started = True
            current.append(char)
            continue

        if char == ",":
            items.append(parse_inline_array_item("".join(current)))
            current = []
            token_started = False
            continue

        if not token_started and char.isspace():
            continue

        token_started = True
        current.append(char)

    if quote is not None:
        raise ValueError("must use balanced quotes inside inline array")

    items.append(parse_inline_array_item("".join(current)))
    return items


def is_escaped_double_quote(current: list[str], quote: str) -> bool:
    if quote != '"':
        return False

    backslash_count = 0
    for char in reversed(current[:-1]):
        if char != "\\":
            break
        backslash_count += 1
    return backslash_count % 2 == 1


def parse_inline_array_item(raw: str) -> str:
    item = raw.strip()
    if not item:
        raise ValueError("inline array items must not be empty")
    if item.startswith('"') and item.endswith('"'):
        parsed = json.loads(item)
        if not isinstance(parsed, str) or not parsed:
            raise ValueError("inline array quoted items must decode to non-empty strings")
        return parsed
    if item.startswith("'") and item.endswith("'"):
        parsed = item[1:-1].replace("''", "'")
        if not parsed:
            raise ValueError("inline array quoted items must not be empty")
        return parsed
    if '"' in item or "'" in item or "[" in item or "]" in item:
        raise ValueError("inline array items must be comma-separated plain or quoted strings")
    return item


def normalize_url(url: str) -> str:
    raw = url.strip()
    if not raw:
        raise ValueError("is empty")

    split = urlsplit(raw)
    if not split.scheme or not split.netloc:
        raise ValueError(f"must be an absolute URL: {url}")

    scheme = split.scheme.lower()
    hostname = (split.hostname or "").lower()
    port = split.port

    host = f"[{hostname}]" if ":" in hostname else hostname
    userinfo = ""
    if split.username is not None:
        userinfo = split.username
        if split.password is not None:
            userinfo = f"{userinfo}:{split.password}"
        userinfo = f"{userinfo}@"

    if port is None or (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = f"{userinfo}{host}"
    else:
        netloc = f"{userinfo}{host}:{port}"

    filtered_query: list[tuple[str, str]] = []
    for key, value in parse_qsl(split.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith(TRACKING_PARAM_PREFIXES) or lowered in TRACKING_PARAMS or not key:
            continue
        filtered_query.append((key, value))

    return urlunsplit((scheme, netloc, split.path, urlencode(filtered_query, doseq=True), ""))


if __name__ == "__main__":
    raise SystemExit(main())
