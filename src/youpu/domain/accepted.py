from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ACCEPTED_FIELD_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


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
            if char == quote:
                quote = None
            continue

        if char in {"'", '"'}:
            quote = char
            token_started = True
            current.append(char)
            continue

        if char == ",":
            item = _parse_inline_array_item("".join(current))
            items.append(item)
            current = []
            token_started = False
            continue

        if not token_started and char.isspace():
            continue

        token_started = True
        current.append(char)

    if quote is not None:
        raise ValueError("must use balanced quotes inside inline array")

    items.append(_parse_inline_array_item("".join(current)))
    return items


def _parse_inline_array_item(raw: str) -> str:
    item = raw.strip()
    if not item:
        raise ValueError("inline array items must not be empty")
    if item.startswith('"') and item.endswith('"'):
        import json

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


@dataclass(frozen=True)
class AcceptedDocument:
    path: Path
    index: int | None
    slug: str | None
    yaml_fields: dict[str, str]
    body: str


@dataclass(frozen=True)
class AcceptedField:
    name: str
    field_type: str
    required: bool
    example: str

    @property
    def is_array(self) -> bool:
        return self.field_type == "inline_array"
