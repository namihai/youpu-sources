from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from youpu.domain.diagnostics import Diagnostic


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    command: str
    summary: str
    diagnostics: list[Diagnostic] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)
