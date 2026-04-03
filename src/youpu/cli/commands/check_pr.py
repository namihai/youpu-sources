from __future__ import annotations

from pathlib import Path

from youpu.app.checks import run_pr_check
from youpu.app.results import CommandResult
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import sub_check_data
from youpu.cli.commands.common import usage_error_result


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu check-pr"):
        return usage_error_result("check-pr", "PR check failed")

    report = run_pr_check(repo_root)
    ok = report.ok
    return (
        CommandResult(
            ok=ok,
            command="check-pr",
            summary="PR check passed" if ok else "PR check failed",
            diagnostics=report.diagnostics,
            data={
                **sub_check_data(
                    "validate", report.repo.ok,
                    command="validate-repo",
                    summary_passed="Repository validation passed",
                    summary_failed="Repository validation failed",
                ),
                **sub_check_data(
                    "schema", report.schema.ok,
                    command="validate-schema",
                    summary_passed="Schema validation passed",
                    summary_failed="Schema validation failed",
                ),
                **sub_check_data(
                    "staging", report.imports.ok,
                    command="validate-imports",
                    summary_passed="Staging validation passed",
                    summary_failed="Staging validation failed",
                ),
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
