from __future__ import annotations

from pathlib import Path

from youpu.app.checks import run_repo_check
from youpu.app.results import CommandResult
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import usage_error_result
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_VALIDATION_FAILED


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu validate-repo"):
        return usage_error_result("validate-repo", "Repository validation failed")

    report = run_repo_check(repo_root)
    ok = report.ok
    return (
        CommandResult(
            ok=ok,
            command="validate-repo",
            summary="Repository validation passed" if ok else "Repository validation failed",
            diagnostics=report.diagnostics,
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
