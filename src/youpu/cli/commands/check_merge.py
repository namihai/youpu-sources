from __future__ import annotations

from pathlib import Path

from youpu.app.checks import run_merge_check
from youpu.app.results import CommandResult
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import usage_error_result


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu check-merge"):
        return usage_error_result("check-merge", "Merge check failed")

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
