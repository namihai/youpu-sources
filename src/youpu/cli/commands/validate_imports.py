from __future__ import annotations

from pathlib import Path

from youpu.app.checks import ImportsCheck
from youpu.app.checks import run_imports_check
from youpu.app.results import CommandResult
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import usage_error_result
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.infra.repo_layout import StagingLayout
from youpu.infra.repo_layout import get_staging_layout


def build_summary(report: ImportsCheck, layout: StagingLayout, repo_root: Path, *, ok: bool) -> str:
    header = "Staging validation passed" if ok else "Staging validation failed"
    return "\n".join(
        [
            header,
            f"staging root: {layout.root.relative_to(repo_root)}",
            f"accepted candidates ready: {report.accepted_ready}",
            f"rejected candidates ready: {report.rejected_ready}",
            f"issues: {len(report.diagnostics)}",
        ]
    )


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu validate-imports"):
        return usage_error_result("validate-imports", "Staging validation failed")

    report = run_imports_check(repo_root)
    ok = report.ok
    layout = get_staging_layout(repo_root)
    return (
        CommandResult(
            ok=ok,
            command="validate-imports",
            summary=build_summary(report, layout, repo_root, ok=ok),
            diagnostics=report.diagnostics,
            data={
                "staging_root": str(layout.root.relative_to(repo_root)),
                "accepted_ready": report.accepted_ready,
                "rejected_ready": report.rejected_ready,
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
