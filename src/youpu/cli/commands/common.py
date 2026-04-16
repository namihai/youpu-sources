from __future__ import annotations

import argparse
import io
import sys

from youpu.app.results import CommandResult
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic


def parse_no_args(command_args: list[str], *, prog: str) -> bool:
    parser = argparse.ArgumentParser(prog=prog, add_help=False)
    saved_stderr = sys.stderr
    try:
        sys.stderr = io.StringIO()
        parser.parse_args(command_args)
    except SystemExit:
        return False
    finally:
        sys.stderr = saved_stderr
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


def sub_check_data(prefix: str, ok: bool, *, command: str, summary_passed: str, summary_failed: str) -> dict[str, object]:
    return {
        f"{prefix}_ok": ok,
        f"{prefix}_exit_code": EXIT_OK if ok else EXIT_VALIDATION_FAILED,
        f"{prefix}_summary": summary_passed if ok else summary_failed,
        f"{prefix}_command": command,
    }
