from __future__ import annotations

import json
import sys
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from rich.console import Console


@dataclass(frozen=True)
class Diagnostic:
    level: str
    message: str
    path: str | None = None
    code: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CommandResult:
    ok: bool
    command: str
    summary: str
    diagnostics: list[Diagnostic] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)


def render_text(result: CommandResult, *, no_color: bool = False, stderr: bool = False) -> None:
    console = Console(stderr=stderr, no_color=no_color)
    status_style = "green" if result.ok else "red"
    console.print(result.summary, style=status_style)

    for diag in result.diagnostics:
        prefix = diag.level.upper()
        parts = [f"{prefix}: {diag.message}"]
        if diag.path:
            parts.append(f"path={diag.path}")
        if diag.code:
            parts.append(f"code={diag.code}")
        console.print(" | ".join(parts))


def render_json(result: CommandResult) -> str:
    payload = {
        "ok": result.ok,
        "command": result.command,
        "summary": result.summary,
        "diagnostics": [asdict(item) for item in result.diagnostics],
        "data": result.data,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def emit_result(
    result: CommandResult,
    *,
    output_format: str = "text",
    no_color: bool = False,
    stderr: bool = False,
) -> None:
    if output_format == "json":
        target = sys.stderr if stderr else sys.stdout
        print(render_json(result), file=target)
        return

    render_text(result, no_color=no_color, stderr=stderr)
