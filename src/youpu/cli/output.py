from __future__ import annotations

import json
import sys
from dataclasses import asdict

from youpu.app.results import CommandResult


def render_text(result: CommandResult, *, stderr: bool = False) -> None:
    target = sys.stderr if stderr else sys.stdout
    print(result.summary, file=target)

    for diag in result.diagnostics:
        prefix = diag.level.upper()
        parts = [f"{prefix}: {diag.message}"]
        if diag.path:
            parts.append(f"path={diag.path}")
        if diag.code:
            parts.append(f"code={diag.code}")
        print(" | ".join(parts), file=target)


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
    stderr: bool = False,
) -> None:
    if output_format == "json":
        target = sys.stderr if stderr else sys.stdout
        print(render_json(result), file=target)
        return

    render_text(result, stderr=stderr)
