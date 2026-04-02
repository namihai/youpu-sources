from __future__ import annotations

import argparse
from pathlib import Path

from youpu.app.checks import run_pr_check
from youpu.app.results import CommandResult
from youpu.cli.argparse_utils import CliArgumentParser
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic


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

    report = run_pr_check(repo_root)
    ok = report.ok
    return (
        CommandResult(
            ok=ok,
            command="check-pr",
            summary="PR check passed" if ok else "PR check failed",
            diagnostics=report.diagnostics,
            data={
                "validate_ok": report.repo.ok,
                "validate_exit_code": EXIT_OK if report.repo.ok else EXIT_VALIDATION_FAILED,
                "validate_summary": "Repository validation passed" if report.repo.ok else "Repository validation failed",
                "validate_command": "validate-repo",
                "schema_ok": report.schema.ok,
                "schema_exit_code": EXIT_OK if report.schema.ok else EXIT_VALIDATION_FAILED,
                "schema_summary": "Schema validation passed" if report.schema.ok else "Schema validation failed",
                "schema_command": "validate-schema",
                "staging_ok": report.imports.ok,
                "staging_exit_code": EXIT_OK if report.imports.ok else EXIT_VALIDATION_FAILED,
                "staging_summary": "Staging validation passed" if report.imports.ok else "Staging validation failed",
                "staging_command": "validate-imports",
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
