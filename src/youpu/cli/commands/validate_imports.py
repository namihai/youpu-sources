from __future__ import annotations

import argparse
from pathlib import Path

from youpu.app.checks import ImportsCheck
from youpu.app.checks import run_imports_check
from youpu.app.results import CommandResult
from youpu.cli.argparse_utils import CliArgumentParser
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_USAGE_ERROR
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic
from youpu.infra.repo_layout import get_staging_layout


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu validate-imports", add_help=False)


def build_summary(report: ImportsCheck, repo_root: Path, *, ok: bool) -> str:
    header = "Staging validation passed" if ok else "Staging validation failed"
    layout = get_staging_layout(repo_root)
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
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="validate-imports",
                summary="Staging validation failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    report = run_imports_check(repo_root)
    ok = report.ok
    layout = get_staging_layout(repo_root)
    return (
        CommandResult(
            ok=ok,
            command="validate-imports",
            summary=build_summary(report, repo_root, ok=ok),
            diagnostics=report.diagnostics,
            data={
                "staging_root": str(layout.root.relative_to(repo_root)),
                "accepted_ready": report.accepted_ready,
                "rejected_ready": report.rejected_ready,
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
