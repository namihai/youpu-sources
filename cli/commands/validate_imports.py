from __future__ import annotations

import argparse
from pathlib import Path

from cli.commands import ingest as ingest_command
from cli.argparse_utils import CliArgumentParser
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import get_imports_layout


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu validate-imports", add_help=False)


def build_summary(analysis: ingest_command.IngestAnalysis, repo_root: Path, *, ok: bool) -> str:
    header = "Staging validation passed" if ok else "Staging validation failed"
    layout = get_imports_layout(repo_root)
    return "\n".join(
        [
            header,
            f"staging root: {layout.root.relative_to(repo_root)}",
            f"accepted candidates ready: {len(analysis.accepted_ready)}",
            f"rejected candidates ready: {len(analysis.rejected_ready)}",
            f"issues: {len(analysis.diagnostics)}",
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

    analysis = ingest_command.build_analysis(repo_root)
    ok = not any(diag.level == "error" for diag in analysis.diagnostics)
    layout = get_imports_layout(repo_root)
    return (
        CommandResult(
            ok=ok,
            command="validate-imports",
            summary=build_summary(analysis, repo_root, ok=ok),
            diagnostics=analysis.diagnostics,
            data={
                "imports_root": str(layout.root.relative_to(repo_root)),
                "accepted_ready": len(analysis.accepted_ready),
                "rejected_ready": len(analysis.rejected_ready),
            },
        ),
        EXIT_OK if ok else EXIT_VALIDATION_FAILED,
    )
