from __future__ import annotations

import argparse

from youpu.app.results import CommandResult
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.domain.diagnostics import Diagnostic


def parse_no_args(command_args: list[str], *, prog: str) -> bool:
    parser = argparse.ArgumentParser(prog=prog, add_help=False)
    try:
        parser.parse_args(command_args)
    except SystemExit:
        return False
    return True


def usage_error_result(command: str, summary: str, *, message: str = "invalid arguments") -> tuple[CommandResult, int]:
    return (
        CommandResult(
            ok=False,
            command=command,
            summary=summary,
            diagnostics=[Diagnostic(level="error", message=message, code="usage_error")],
        ),
        EXIT_USAGE_ERROR,
    )
