from __future__ import annotations

import argparse
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic
from cli import validation


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu validate-repo", add_help=False)


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="validate-repo",
                summary="Repository validation failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    diagnostics: list[Diagnostic] = []
    diagnostics.extend(validation.validate_accepted(repo_root))
    diagnostics.extend(validation.validate_accepted_duplicates(repo_root))
    diagnostics.extend(validation.validate_rejected(repo_root))
    diagnostics.extend(validation.validate_rejected_duplicates(repo_root))
    diagnostics.extend(validation.validate_cross(repo_root))

    ok = not any(diag.level == "error" for diag in diagnostics)
    return (
        CommandResult(
            ok=ok,
            command="validate-repo",
            summary="Repository validation passed" if ok else "Repository validation failed",
            diagnostics=diagnostics,
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
