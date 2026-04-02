from __future__ import annotations

import json
import re
from pathlib import Path

from youpu.domain.accepted import ACCEPTED_FIELD_NAME_RE
from youpu.domain.accepted import AcceptedDocument

ACCEPTED_NAME_RE = re.compile(r"^SRC-(\d{4})-([a-z0-9-]+)\.md$")

def extract_front_matter(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    if not lines:
        raise ValueError("missing YAML front matter")
    if lines[0].strip() != "---":
        raise ValueError("accepted documents must start with YAML front matter delimited by ---")

    offset = len(lines[0])
    block_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            return "".join(block_lines), offset + sum(len(item) for item in block_lines) + len(line)
        block_lines.append(line)

    raise ValueError("missing closing --- for YAML front matter")


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
    block, _ = extract_front_matter(text)
    fields: dict[str, str] = {}
    for line_number, raw_line in enumerate(block.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid yaml line {line_number}: expected `key: value`")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if not ACCEPTED_FIELD_NAME_RE.match(key):
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

    _, yaml_block_end = extract_front_matter(text)
    yaml_fields = parse_simple_yaml_block(text)
    body = text[yaml_block_end:].lstrip()

    return AcceptedDocument(
        path=doc_path,
        index=index,
        slug=slug,
        yaml_fields=yaml_fields,
        body=body,
    )
