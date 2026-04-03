from __future__ import annotations

from pathlib import Path

from youpu.app.ingest import build_analysis
from youpu.app.ingest import build_summary
from youpu.app.ingest import has_staging_candidates
from youpu.app.ingest import merge_ingest
from youpu.app.results import CommandResult
from youpu.cli.commands.common import parse_no_args
from youpu.cli.commands.common import usage_error_result
from youpu.cli.errors import EXIT_OK
from youpu.cli.errors import EXIT_VALIDATION_FAILED
from youpu.domain.diagnostics import Diagnostic
from youpu.infra.repo_layout import get_staging_layout


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    if not parse_no_args(command_args, prog="youpu ingest"):
        return usage_error_result("ingest", "Ingest operation failed")

    layout = get_staging_layout(repo_root)
    analysis = build_analysis(repo_root)
    if analysis.diagnostics:
        return (
            CommandResult(
                ok=False,
                command="ingest",
                summary="Ingest operation failed",
                diagnostics=analysis.diagnostics,
                data={
                    "staging_root": str(layout.root.relative_to(repo_root)),
                    "accepted_ready": len(analysis.accepted_ready),
                    "rejected_ready": len(analysis.rejected_ready),
                },
            ),
            EXIT_VALIDATION_FAILED,
        )

    if not has_staging_candidates(analysis):
        return (
            CommandResult(
                ok=False,
                command="ingest",
                summary="Ingest operation failed",
                diagnostics=[Diagnostic(level="error", message="no staging candidates found", code="staging_empty")],
                data={
                    "staging_root": str(layout.root.relative_to(repo_root)),
                    "accepted_ready": len(analysis.accepted_ready),
                    "rejected_ready": len(analysis.rejected_ready),
                },
            ),
            EXIT_VALIDATION_FAILED,
        )

    try:
        merge_data = merge_ingest(repo_root, analysis)
    except OSError as exc:
        return (
            CommandResult(
                ok=False,
                command="ingest",
                summary="Ingest operation failed",
                diagnostics=[Diagnostic(level="error", message=str(exc), code="ingest_io_error")],
                data={
                    "staging_root": str(layout.root.relative_to(repo_root)),
                    "accepted_ready": len(analysis.accepted_ready),
                    "rejected_ready": len(analysis.rejected_ready),
                },
            ),
            EXIT_VALIDATION_FAILED,
        )
    return (
        CommandResult(
            ok=True,
            command="ingest",
            summary=build_summary(analysis, repo_root),
            diagnostics=[],
            data={
                **merge_data,
                "accepted_ready": len(analysis.accepted_ready),
                "rejected_ready": len(analysis.rejected_ready),
            },
        ),
        EXIT_OK,
    )
