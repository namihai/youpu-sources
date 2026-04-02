from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(frozen=True)
class Diagnostic:
    level: str
    message: str
    path: str | None = None
    code: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
