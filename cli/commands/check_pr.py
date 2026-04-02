from __future__ import annotations

import argparse
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.commands import validate_imports as validate_imports_command
from cli.commands import validate_repo as validate_repo_command
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu check-pr", add_help=False)


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="check-pr",
                summary="PR check failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    validate_result, validate_exit = validate_repo_command.run([], repo_root)
    staging_result, staging_exit = validate_imports_command.run([], repo_root)
    diagnostics = [*validate_result.diagnostics, *staging_result.diagnostics]
    ok = validate_result.ok and staging_result.ok
    return (
        CommandResult(
            ok=ok,
            command="check-pr",
            summary="PR check passed" if ok else "PR check failed",
            diagnostics=diagnostics,
            data={
                "validate_ok": validate_result.ok,
                "validate_exit_code": validate_exit,
                "validate_summary": validate_result.summary,
                "validate_command": validate_result.command,
                "staging_ok": staging_result.ok,
                "staging_exit_code": staging_exit,
                "staging_summary": staging_result.summary,
                "staging_command": staging_result.command,
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
