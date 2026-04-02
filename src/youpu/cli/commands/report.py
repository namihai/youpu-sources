from __future__ import annotations

from pathlib import Path

from youpu.app.report import build_repository_report
from youpu.app.results import CommandResult
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import usage_error_result
from youpu.cli.errors import EXIT_OK


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu report"):
        return usage_error_result("report", "Report failed")

    report = build_repository_report(repo_root)

    return (
        CommandResult(
            ok=True,
            command="report",
            summary=report.summary,
            diagnostics=report.diagnostics,
            data=report.data,
        ),
        EXIT_OK,
    )
