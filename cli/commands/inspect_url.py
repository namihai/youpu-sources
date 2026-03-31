from __future__ import annotations

import argparse
from pathlib import Path

from cli.argparse_utils import CliArgumentParser
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import normalize_url


def build_parser() -> argparse.ArgumentParser:
    parser = CliArgumentParser(prog="youpu inspect-url", add_help=False)
    parser.add_argument("url")
    return parser


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    del repo_root
    parser = build_parser()
    try:
        args = parser.parse_args(command_args)
    except (SystemExit, ValueError):
        return (
            CommandResult(
                ok=False,
                command="inspect-url",
                summary="Inspect URL failed",
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

    try:
        canonical_url = normalize_url(args.url)
    except ValueError as exc:
        return (
            CommandResult(
                ok=False,
                command="inspect-url",
                summary="Inspect URL failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message=str(exc),
                        code="usage_error",
                    )
                ],
            ),
            EXIT_USAGE_ERROR,
        )

    return (
        CommandResult(
            ok=True,
            command="inspect-url",
            summary=canonical_url,
            diagnostics=[],
            data={
                "input": args.url,
                "canonical_url": canonical_url,
            },
        ),
        EXIT_OK,
    )
