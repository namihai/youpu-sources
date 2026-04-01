from __future__ import annotations

import argparse
import re
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.commands import ingest as ingest_command
from cli.commands import validate_repo as validate_repo_command
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import get_import_accepted_paths
from cli.repo import get_imports_layout
from cli.repo import parse_rejected_csv

ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu report", add_help=False)


def latest_accepted_id(repo_root: Path) -> str | None:
    latest = 0
    for path in (repo_root / "accepted").glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if not match:
            continue
        latest = max(latest, int(match.group(1)))
    if latest == 0:
        return None
    return f"SRC-{latest:04d}"


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="report",
                summary="Report failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message="invalid arguments",
                        code="usage_error",
                    )
                ],
            ),
            EXIT_USAGE_ERROR,
        )

    accepted_count = len(list((repo_root / "accepted").glob("*.md")))
    rejected = parse_rejected_csv(repo_root / "rejected" / "rejected.csv")
    rejected_count = len(rejected.rows)
    latest_id = latest_accepted_id(repo_root)
    layout = get_imports_layout(repo_root)
    pending_accepted = len(get_import_accepted_paths(repo_root))
    pending_rejected = 1 if layout.rejected_csv.exists() else 0

    validate_result, _ = validate_repo_command.run([], repo_root)
    validation_diagnostics = validate_result.diagnostics
    duplicate_errors = [
        item
        for item in validation_diagnostics
        if item.code in {"accepted_duplicate_canonical_url", "accepted_duplicate_title", "rejected_duplicate_url"}
    ]
    cross_conflicts = sum(1 for item in validation_diagnostics if item.code == "cross_url_conflict")
    import_analysis = ingest_command.build_analysis(repo_root)
    import_issues = len(import_analysis.diagnostics)

    summary = "\n".join(
        [
            "Repository summary",
            f"accepted files: {accepted_count}",
            f"rejected rows: {rejected_count}",
            f"latest accepted id: {latest_id or 'none'}",
            f"validation: {'passed' if validate_result.ok else 'failed'}",
            f"duplicates: {'none' if not duplicate_errors else 'found'}",
            f"cross-conflicts: {cross_conflicts}",
            f"imports pending accepted: {pending_accepted}",
            f"imports pending rejected: {pending_rejected}",
            f"imports issues: {import_issues}",
        ]
    )

    return (
        CommandResult(
            ok=True,
            command="report",
            summary=summary,
            diagnostics=[],
            data={
                "accepted_files": accepted_count,
                "rejected_rows": rejected_count,
                "latest_accepted_id": latest_id,
                "validation_ok": validate_result.ok,
                "duplicates_ok": not duplicate_errors,
                "cross_conflicts": cross_conflicts,
                "imports_pending_accepted": pending_accepted,
                "imports_pending_rejected": pending_rejected,
                "imports_issues": import_issues,
            },
        ),
        EXIT_OK,
    )
