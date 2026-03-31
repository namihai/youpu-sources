from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from tools.youpu.errors import EXIT_OK
from tools.youpu.errors import EXIT_USAGE_ERROR
from tools.youpu.errors import EXIT_VALIDATION_FAILED
from tools.youpu.output import CommandResult
from tools.youpu.output import Diagnostic
from tools.youpu.repo import parse_accepted_document
from tools.youpu.repo import parse_rejected_csv
from tools.youpu.repo import normalize_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="youpu duplicates", add_help=False)
    parser.add_argument(
        "--scope",
        choices=("accepted", "rejected", "cross", "all"),
        default="all",
    )
    return parser


def find_accepted_duplicates(repo_root: Path) -> list[Diagnostic]:
    accepted_dir = repo_root / "accepted"
    diagnostics: list[Diagnostic] = []
    by_canonical_url: dict[str, list[str]] = defaultdict(list)
    by_title: dict[str, list[str]] = defaultdict(list)

    for path in sorted(accepted_dir.glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"could not parse accepted document: {exc}",
                    path=str(path.relative_to(repo_root)),
                    code="accepted_parse_error",
                )
            )
            continue

        title = doc.yaml_fields.get("title", "").strip()
        if title:
            by_title[title].append(str(path.relative_to(repo_root)))

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if canonical_url:
            try:
                normalized = normalize_url(canonical_url)
            except ValueError as exc:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=str(exc),
                        path=str(path.relative_to(repo_root)),
                        code="accepted_invalid_canonical_url",
                    )
                )
            else:
                by_canonical_url[normalized].append(str(path.relative_to(repo_root)))

    for canonical_url, paths in sorted(by_canonical_url.items()):
        if len(paths) < 2:
            continue
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"duplicate canonical_url: {canonical_url}",
                path=", ".join(paths),
                code="accepted_duplicate_canonical_url",
                details={"canonical_url": canonical_url, "paths": paths},
            )
        )

    for title, paths in sorted(by_title.items()):
        if len(paths) < 2:
            continue
        diagnostics.append(
            Diagnostic(
                level="warning",
                message=f"duplicate title: {title}",
                path=", ".join(paths),
                code="accepted_duplicate_title",
                details={"title": title, "paths": paths},
            )
        )

    return diagnostics


def find_rejected_duplicates(repo_root: Path) -> list[Diagnostic]:
    csv_path = repo_root / "rejected" / "rejected.csv"
    diagnostics: list[Diagnostic] = []

    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception as exc:
        return [
            Diagnostic(
                level="error",
                message=f"could not parse rejected csv: {exc}",
                path=str(csv_path.relative_to(repo_root)),
                code="rejected_parse_error",
            )
        ]

    by_url: dict[str, list[int]] = defaultdict(list)
    for row in rejected.rows:
        if not row.url:
            continue
        try:
            normalized = normalize_url(row.url)
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=str(exc),
                    path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                    code="rejected_invalid_url",
                )
            )
            continue
        by_url[normalized].append(row.row_number)

    for url, rows in sorted(by_url.items()):
        if len(rows) < 2:
            continue
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"duplicate rejected url: {url}",
                path=", ".join(f"{csv_path.relative_to(repo_root)}:{row}" for row in rows),
                code="rejected_duplicate_url",
                details={"url": url, "rows": rows},
            )
        )

    return diagnostics


def find_cross_duplicates(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    accepted_urls: dict[str, list[str]] = defaultdict(list)
    rejected_urls: dict[str, list[int]] = defaultdict(list)

    accepted_dir = repo_root / "accepted"
    for path in sorted(accepted_dir.glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"could not parse accepted document: {exc}",
                    path=str(path.relative_to(repo_root)),
                    code="accepted_parse_error",
                )
            )
            continue

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if not canonical_url:
            continue

        try:
            normalized = normalize_url(canonical_url)
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=str(exc),
                    path=str(path.relative_to(repo_root)),
                    code="accepted_invalid_canonical_url",
                )
            )
            continue

        accepted_urls[normalized].append(str(path.relative_to(repo_root)))

    csv_path = repo_root / "rejected" / "rejected.csv"
    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception as exc:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"could not parse rejected csv: {exc}",
                path=str(csv_path.relative_to(repo_root)),
                code="rejected_parse_error",
            )
        )
        return diagnostics

    for row in rejected.rows:
        if not row.url:
            continue

        try:
            normalized = normalize_url(row.url)
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=str(exc),
                    path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                    code="rejected_invalid_url",
                )
            )
            continue

        rejected_urls[normalized].append(row.row_number)

    for url in sorted(set(accepted_urls) & set(rejected_urls)):
        accepted_paths = accepted_urls[url]
        rejected_rows = rejected_urls[url]
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"url exists in both accepted and rejected: {url}",
                path=", ".join(
                    accepted_paths
                    + [f"{csv_path.relative_to(repo_root)}:{row}" for row in rejected_rows]
                ),
                code="cross_duplicate_url",
                details={
                    "url": url,
                    "accepted_paths": accepted_paths,
                    "rejected_rows": rejected_rows,
                },
            )
        )

    return diagnostics


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        args = parser.parse_args(command_args)
    except SystemExit:
        return (
            CommandResult(
                ok=False,
                command="duplicates",
                summary="Duplicates check failed",
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

    diagnostics: list[Diagnostic] = []
    if args.scope in {"accepted", "all"}:
        diagnostics.extend(find_accepted_duplicates(repo_root))
    if args.scope in {"rejected", "all"}:
        diagnostics.extend(find_rejected_duplicates(repo_root))
    if args.scope in {"cross", "all"}:
        diagnostics.extend(find_cross_duplicates(repo_root))

    ok = not diagnostics
    result = CommandResult(
        ok=ok,
        command="duplicates",
        summary="No duplicates found" if ok else "Duplicates found",
        diagnostics=diagnostics,
        data={"scope": args.scope},
    )
    return result, (EXIT_OK if ok else EXIT_VALIDATION_FAILED)
