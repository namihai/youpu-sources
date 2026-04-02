from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RejectedRow:
    row_number: int
    url: str
    title: str
    reason: str


@dataclass(frozen=True)
class RejectedCsv:
    path: Path
    columns: list[str]
    rows: list[RejectedRow]


@dataclass(frozen=True)
class RejectedColumn:
    name: str
    required: bool
    example: str
