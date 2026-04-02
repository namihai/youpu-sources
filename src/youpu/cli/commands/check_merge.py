from __future__ import annotations

import argparse
from pathlib import Path

from youpu.app.checks import run_merge_check
from youpu.app.results import CommandResult
from youpu.cli.argparse_utils import CliArgumentParser
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu check-merge", add_help=False)


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="check-merge",
                summary="Merge check failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    report = run_merge_check(repo_root)
    ok = report.ok
    return (
        CommandResult(
            ok=ok,
            command="check-merge",
            summary="Merge check passed" if ok else "Merge check failed",
            diagnostics=report.diagnostics,
            data={
                "validate_ok": report.repo.ok,
                "validate_exit_code": EXIT_OK if report.repo.ok else EXIT_VALIDATION_FAILED,
                "schema_ok": report.schema.ok,
                "schema_exit_code": EXIT_OK if report.schema.ok else EXIT_VALIDATION_FAILED,
                "pending_staging": report.pending_staging,
                "staging_issues": report.staging_issues,
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
