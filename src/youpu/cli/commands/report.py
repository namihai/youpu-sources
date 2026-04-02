from __future__ import annotations

import argparse
from pathlib import Path

from youpu.app.report import build_repository_report
from youpu.app.results import CommandResult
from youpu.cli.argparse_utils import CliArgumentParser
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.domain.diagnostics import Diagnostic


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu report", add_help=False)


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="report",
                summary="Report failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message="invalid arguments",
                        code="usage_error",
                    )
                ],
            ),
            EXIT_USAGE_ERROR,
        )

    report = build_repository_report(repo_root)

    return (
        CommandResult(
            ok=True,
            command="report",
            summary=report.summary,
            diagnostics=[],
            data=report.data,
        ),
        EXIT_OK,
    )
