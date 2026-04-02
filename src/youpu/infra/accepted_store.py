from __future__ import annotations

import json
import re
from pathlib import Path

from youpu.domain.accepted import AcceptedDocument

ACCEPTED_NAME_RE = re.compile(r"^SRC-(\d{4})-([a-z0-9-]+)\.md$")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def extract_simple_yaml_block(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    start_line: int | None = None
    offset = 0

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") and stripped[3:].strip() == "yaml":
            offset += len(line)
            start_line = index + 1
            break
        offset += len(line)

    if start_line is None:
        raise ValueError("missing ```yaml fenced block")

    block_lines: list[str] = []
    for line in lines[start_line:]:
        stripped = line.strip()
        if stripped == "```":
            return "".join(block_lines), offset + sum(len(item) for item in block_lines) + len(line)
        block_lines.append(line)

    raise ValueError("missing closing ``` for yaml fenced block")


def parse_simple_yaml_scalar(raw_value: str, *, line_number: int) -> str:
    value = raw_value.strip()
    if value.startswith("[") and value.endswith("]"):
        return value
    if value.startswith('"') and value.endswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid quoted YAML string at line {line_number}: {exc.msg}") from exc
        if not isinstance(parsed, str):
            raise ValueError(f"yaml value at line {line_number} must decode to a string")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_simple_yaml_block(text: str) -> dict[str, str]:
    block, _ = extract_simple_yaml_block(text)
    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(block.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid yaml line {line_number}: expected `key: value`")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
            raise ValueError(f"invalid yaml key at line {line_number}: {key!r}")
        if key in fields:
            raise ValueError(f"duplicate yaml key at line {line_number}: {key}")
        fields[key] = parse_simple_yaml_scalar(value, line_number=line_number)
    return fields


def render_simple_yaml_value(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        return stripped
    return json.dumps(value, ensure_ascii=False)


def serialize_simple_yaml_mapping(fields: dict[str, str], field_order: list[str]) -> str:
    return "\n".join(f"{key}: {render_simple_yaml_value(fields.get(key, ''))}" for key in field_order)


def parse_accepted_document(path: str | Path) -> AcceptedDocument:
    doc_path = Path(path)
    text = doc_path.read_text(encoding="utf-8")

    name_match = ACCEPTED_NAME_RE.match(doc_path.name)
    index = int(name_match.group(1)) if name_match else None
    slug = name_match.group(2) if name_match else None

    title_match = TITLE_RE.search(text)
    heading = title_match.group(1).strip() if title_match else None
    _, yaml_block_end = extract_simple_yaml_block(text)
    yaml_fields = parse_simple_yaml_block(text)
    body = text[yaml_block_end:].lstrip()

    return AcceptedDocument(
        path=doc_path,
        index=index,
        slug=slug,
        heading=heading,
        yaml_fields=yaml_fields,
        body=body,
    )
