from __future__ import annotations

import argparse

from cli.commands import inspect_url as inspect_url_command
from cli.commands import ingest as ingest_command
from cli.commands import report as report_command
from cli.commands import submit as submit_command
from cli.commands import validate as validate_command
from cli.errors import EXIT_OK
from cli.errors import RuntimeCliError
from cli.errors import UsageError
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.output import emit_result
from cli.repo import resolve_repo_root

PLANNED_COMMANDS = [
    "validate",
    "ingest",
    "submit",
    "inspect-url",
    "report",
]


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
        "--quiet",
        action="store_true",
        help="Only output final result.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Output additional details.",
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

    if args.command not in PLANNED_COMMANDS:
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

    if args.command == "validate":
        result, exit_code = validate_command.run(args.command_args, repo_root)
        emit_result(
            result,
            output_format=args.format,
            no_color=args.no_color,
            stderr=not result.ok,
        )
        return exit_code

    if args.command == "ingest":
        result, exit_code = ingest_command.run(args.command_args, repo_root)
        emit_result(
            result,
            output_format=args.format,
            no_color=args.no_color,
            stderr=not result.ok,
        )
        return exit_code

    if args.command == "inspect-url":
        result, exit_code = inspect_url_command.run(args.command_args, repo_root)
        emit_result(
            result,
            output_format=args.format,
            no_color=args.no_color,
            stderr=not result.ok,
        )
        return exit_code

    if args.command == "report":
        result, exit_code = report_command.run(args.command_args, repo_root)
        emit_result(
            result,
            output_format=args.format,
            no_color=args.no_color,
            stderr=not result.ok,
        )
        return exit_code

    if args.command == "submit":
        result, exit_code = submit_command.run(args.command_args, repo_root)
        emit_result(
            result,
            output_format=args.format,
            no_color=args.no_color,
            stderr=not result.ok,
        )
        return exit_code

    suffix = f" {' '.join(args.command_args)}" if args.command_args else ""
    err = UsageError(
        f"command not implemented yet: {args.command}{suffix} (repo: {repo_root})"
    )
    emit_result(
        CommandResult(
            ok=False,
            command=args.command,
            summary=f"youpu: {err}",
            diagnostics=[Diagnostic(level="error", message=str(err), code="not_implemented")],
            data={"repo_root": str(repo_root)},
        ),
        output_format=args.format,
        no_color=args.no_color,
        stderr=True,
    )
    return err.exit_code
