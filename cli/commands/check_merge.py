from __future__ import annotations

import argparse
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.commands import ingest as ingest_command
from cli.commands import validate_repo as validate_repo_command
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import get_imports_layout


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

    validate_result, validate_exit = validate_repo_command.run([], repo_root)
    diagnostics = list(validate_result.diagnostics)

    layout = get_imports_layout(repo_root)
    accepted_files = sorted(layout.accepted.glob("*.md"))
    rejected_files = sorted(layout.rejected.glob("*.csv"))
    if accepted_files or rejected_files:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="imports directory still contains pending files; run `youpu ingest` first",
                path=str(layout.root.relative_to(repo_root)),
                code="merge_pending_imports",
                details={
                    "accepted_files": [str(path.relative_to(repo_root)) for path in accepted_files],
                    "rejected_files": [str(path.relative_to(repo_root)) for path in rejected_files],
                },
            )
        )

    analysis = ingest_command.build_analysis(repo_root)
    diagnostics.extend(analysis.diagnostics)
    ok = not any(diag.level == "error" for diag in diagnostics)
    return (
        CommandResult(
            ok=ok,
            command="check-merge",
            summary="Merge check passed" if ok else "Merge check failed",
            diagnostics=diagnostics,
            data={
                "validate_ok": validate_result.ok,
                "validate_exit_code": validate_exit,
                "pending_imports": bool(accepted_files or rejected_files),
                "imports_issues": len(analysis.diagnostics),
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
