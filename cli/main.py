from __future__ import annotations

import argparse

from cli.commands import check_merge as check_merge_command
from cli.commands import check_pr as check_pr_command
from cli.commands import ingest as ingest_command
from cli.commands import report as report_command
from cli.commands import validate_imports as validate_imports_command
from cli.commands import validate_repo as validate_repo_command
from cli.errors import CliError
from cli.errors import EXIT_OK
from cli.errors import EXIT_RUNTIME_ERROR
from cli.errors import RuntimeCliError
from cli.errors import UsageError
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.output import emit_result
from cli.repo import resolve_repo_root

COMMAND_HANDLERS = {
    "validate-repo": validate_repo_command.run,
    "validate-imports": validate_imports_command.run,
    "check-pr": check_pr_command.run,
    "check-merge": check_merge_command.run,
    "ingest": ingest_command.run,
    "report": report_command.run,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="youpu",
        description="Unified CLI entrypoint for the youpu-sources repository.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colorized output.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root path. Default: auto-detect from current directory.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run.",
    )
    parser.add_argument(
        "command_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to the selected command.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    raw_args = list([] if argv is None else argv)
    if argv is None:
        import sys
        raw_args = list(sys.argv[1:])
    parser = build_parser()
    args = parser.parse_args(raw_args)

    try:
        repo_root = resolve_repo_root(args.root)
    except FileNotFoundError as exc:
        err = RuntimeCliError(str(exc))
        emit_result(
            CommandResult(
                ok=False,
                command="bootstrap",
                summary=f"youpu: {err}",
                diagnostics=[Diagnostic(level="error", message=str(err), code="runtime_error")],
            ),
            output_format=args.format,
            no_color=args.no_color,
            stderr=True,
        )
        return err.exit_code

    if not args.command:
        parser.print_help()
        return EXIT_OK

    if args.command not in COMMAND_HANDLERS:
        err = UsageError(f"unknown command: {args.command}")
        emit_result(
            CommandResult(
                ok=False,
                command=args.command,
                summary=f"youpu: {err}",
                diagnostics=[Diagnostic(level="error", message=str(err), code="usage_error")],
            ),
            output_format=args.format,
            no_color=args.no_color,
            stderr=True,
        )
        return err.exit_code

    try:
        result, exit_code = COMMAND_HANDLERS[args.command](args.command_args, repo_root)
    except CliError as exc:
        emit_result(
            CommandResult(
                ok=False,
                command=args.command,
                summary=f"youpu: {exc}",
                diagnostics=[Diagnostic(level="error", message=str(exc), code="runtime_error")],
            ),
            output_format=args.format,
            no_color=args.no_color,
            stderr=True,
        )
        return exc.exit_code
    except Exception as exc:
        emit_result(
            CommandResult(
                ok=False,
                command=args.command,
                summary=f"youpu: {exc}",
                diagnostics=[Diagnostic(level="error", message=str(exc), code="runtime_error")],
            ),
            output_format=args.format,
            no_color=args.no_color,
            stderr=True,
        )
        return EXIT_RUNTIME_ERROR
    emit_result(
        result,
        output_format=args.format,
        no_color=args.no_color,
        stderr=not result.ok,
    )
    return exit_code
