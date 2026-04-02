from __future__ import annotations

import argparse
from pathlib import Path

from youpu.app.checks import run_schema_check
from youpu.app.results import CommandResult
from youpu.cli.argparse_utils import CliArgumentParser
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu validate-schema", add_help=False)


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="validate-schema",
                summary="Schema validation failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    report = run_schema_check(repo_root)
    ok = report.ok
    return (
        CommandResult(
            ok=ok,
            command="validate-schema",
            summary="Schema validation passed" if ok else "Schema validation failed",
            diagnostics=report.diagnostics,
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
