from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AcceptedDocument:
    path: Path
    index: int | None
    slug: str | None
    heading: str | None
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
