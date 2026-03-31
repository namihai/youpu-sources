from __future__ import annotations

import argparse
import re
from pathlib import Path

from cli.commands import duplicates as duplicates_command
from cli.commands import validate as validate_command
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import parse_rejected_csv

ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(prog="youpu report", add_help=False)


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
    except SystemExit:
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

    validate_result, _ = validate_command.run([], repo_root)
    duplicates_result, _ = duplicates_command.run([], repo_root)
    cross_conflicts = sum(1 for item in duplicates_result.diagnostics if item.code == "cross_duplicate_url")

    summary = "\n".join(
        [
            "Repository summary",
            f"accepted files: {accepted_count}",
            f"rejected rows: {rejected_count}",
            f"latest accepted id: {latest_id or 'none'}",
            f"validation: {'passed' if validate_result.ok else 'failed'}",
            f"duplicates: {'none' if duplicates_result.ok else 'found'}",
            f"cross-conflicts: {cross_conflicts}",
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
                "duplicates_ok": duplicates_result.ok,
                "cross_conflicts": cross_conflicts,
            },
        ),
        EXIT_OK,
    )
