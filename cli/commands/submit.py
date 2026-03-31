from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.commands import ingest as ingest_command
from cli.commands import validate as validate_command
from cli.errors import EXIT_OK
from cli.errors import EXIT_RUNTIME_ERROR
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import get_imports_layout


def build_parser() -> argparse.ArgumentParser:
    parser = CliArgumentParser(prog="youpu submit", add_help=False)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--message", default=None)
    parser.add_argument("--push", action="store_true")
    return parser


def pending_import_diagnostics(repo_root: Path) -> list[Diagnostic]:
    layout = get_imports_layout(repo_root)
    diagnostics: list[Diagnostic] = []

    accepted_files = sorted(layout.accepted.glob("*.md"))
    rejected_files = sorted(layout.rejected.glob("*.csv"))
    if accepted_files or rejected_files:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="imports directory still contains pending files; run `youpu ingest` first",
                path=str(layout.root.relative_to(repo_root)),
                code="submit_pending_imports",
                details={
                    "accepted_files": [str(path.relative_to(repo_root)) for path in accepted_files],
                    "rejected_files": [str(path.relative_to(repo_root)) for path in rejected_files],
                },
            )
        )

    analysis = ingest_command.build_analysis(repo_root)
    diagnostics.extend(analysis.diagnostics)
    return diagnostics


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        args = parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="submit",
                summary="Submit failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    if args.check_only and (args.message or args.push):
        return (
            CommandResult(
                ok=False,
                command="submit",
                summary="Submit failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message="--check-only cannot be combined with --message or --push",
                        code="usage_error",
                    )
                ],
            ),
            EXIT_USAGE_ERROR,
        )

    if not args.check_only and not args.message:
        return (
            CommandResult(
                ok=False,
                command="submit",
                summary="Submit failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message="--message is required unless --check-only is used",
                        code="usage_error",
                    )
                ],
            ),
            EXIT_USAGE_ERROR,
        )

    validate_result, _ = validate_command.run([], repo_root)
    diagnostics = list(validate_result.diagnostics)
    diagnostics.extend(pending_import_diagnostics(repo_root))
    ok = not diagnostics
    if args.check_only:
        return (
            CommandResult(
                ok=ok,
                command="submit",
                summary="Submit check passed" if ok else "Submit check failed",
                diagnostics=diagnostics,
                data={"check_only": True},
            ),
            EXIT_OK if ok else EXIT_VALIDATION_FAILED,
        )

    if not ok:
        return (
            CommandResult(
                ok=False,
                command="submit",
                summary="Submit failed",
                diagnostics=diagnostics,
                data={"check_only": False},
            ),
            EXIT_VALIDATION_FAILED,
        )

    try:
        subprocess.run(["git", "add", "-A"], cwd=repo_root, check=True, capture_output=True, text=True)
        staged_changes = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if staged_changes.returncode == 0:
            return (
                CommandResult(
                    ok=False,
                    command="submit",
                    summary="Submit failed",
                    diagnostics=[
                        Diagnostic(
                            level="error",
                            message="no staged changes to commit",
                            code="no_changes",
                        )
                    ],
                    data={"check_only": False},
                ),
                EXIT_USAGE_ERROR,
            )
        commit = subprocess.run(
            ["git", "commit", "-m", args.message],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        push_output = None
        if args.push:
            push = subprocess.run(
                ["git", "push"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            push_output = push.stdout.strip() or push.stderr.strip()
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        return (
            CommandResult(
                ok=False,
                command="submit",
                summary="Submit failed",
                diagnostics=[Diagnostic(level="error", message=message, code="git_command_failed")],
                data={"check_only": False},
            ),
            EXIT_RUNTIME_ERROR,
        )

    return (
        CommandResult(
            ok=True,
            command="submit",
            summary="Submit completed",
            diagnostics=[],
            data={
                "check_only": False,
                "message": args.message,
                "push": args.push,
                "commit_output": commit.stdout.strip() or commit.stderr.strip(),
                "push_output": push_output,
            },
        ),
        EXIT_OK,
    )
