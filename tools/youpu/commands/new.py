from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from tools.youpu.errors import EXIT_OK
from tools.youpu.errors import EXIT_REFUSED
from tools.youpu.errors import EXIT_USAGE_ERROR
from tools.youpu.output import CommandResult
from tools.youpu.output import Diagnostic
from tools.youpu.repo import normalize_url
from tools.youpu.repo import parse_accepted_document
from tools.youpu.repo import parse_rejected_csv

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="youpu new", add_help=False)
    subparsers = parser.add_subparsers(dest="target")

    accepted = subparsers.add_parser("accepted", add_help=False)
    accepted.add_argument("slug")
    accepted.add_argument("--title", default=None)
    accepted.add_argument("--url", default=None)
    accepted.add_argument("--dry-run", action="store_true")

    rejected = subparsers.add_parser("rejected", add_help=False)
    rejected.add_argument("--url", required=True)
    rejected.add_argument("--title", required=True)
    rejected.add_argument("--reason", required=True)
    rejected.add_argument("--dry-run", action="store_true")

    return parser


def next_accepted_index(accepted_dir: Path) -> int:
    max_index = 0
    for path in accepted_dir.glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if not match:
            continue
        max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def build_accepted_content(template_path: Path, *, title: str | None, url: str | None) -> str:
    text = template_path.read_text(encoding="utf-8")
    if title:
        text = text.replace("# 标题", f"# {title}", 1)
        text = text.replace("title: 标题", f"title: {title}", 1)
    if url:
        text = text.replace("canonical_url: https://example.com/dataset", f"canonical_url: {url}", 1)
    return text


def usage_result(summary: str, message: str) -> tuple[CommandResult, int]:
    return (
        CommandResult(
            ok=False,
            command="new",
            summary=summary,
            diagnostics=[
                Diagnostic(
                    level="error",
                    message=message,
                    code="usage_error",
                )
            ],
        ),
        EXIT_USAGE_ERROR,
    )


def refused_result(
    summary: str,
    message: str,
    *,
    path: str | None = None,
    code: str,
) -> tuple[CommandResult, int]:
    return (
        CommandResult(
            ok=False,
            command="new",
            summary=summary,
            diagnostics=[
                Diagnostic(
                    level="error",
                    message=message,
                    path=path,
                    code=code,
                )
            ],
        ),
        EXIT_REFUSED,
    )


def run_new_accepted(args: argparse.Namespace, repo_root: Path) -> tuple[CommandResult, int]:
    slug = args.slug.strip()
    if not slug or not SLUG_RE.fullmatch(slug):
        return usage_result("Create accepted failed", "slug must match [a-z0-9-]+")

    title = args.title.strip() if args.title is not None else None
    url = args.url.strip() if args.url is not None else None
    if args.title is not None and not title:
        return usage_result("Create accepted failed", "title must not be empty when provided")
    if args.url is not None and not url:
        return usage_result("Create accepted failed", "url must not be empty when provided")

    accepted_dir = repo_root / "accepted"
    template_path = repo_root / "templates" / "accepted.md"
    next_index = next_accepted_index(accepted_dir)
    output_path = accepted_dir / f"SRC-{next_index:04d}-{slug}.md"
    if output_path.exists():
        return refused_result(
            "Create accepted failed",
            f"target file already exists: {output_path.name}",
            path=str(output_path.relative_to(repo_root)),
            code="refused_existing_file",
        )

    if args.dry_run:
        return (
            CommandResult(
                ok=True,
                command="new",
                summary=f"Would create {output_path.relative_to(repo_root)}",
                diagnostics=[],
                data={
                    "target": str(output_path.relative_to(repo_root)),
                    "title": title if title is not None else "标题",
                    "canonical_url": url if url is not None else "https://example.com/dataset",
                    "dry_run": True,
                },
            ),
            EXIT_OK,
        )

    content = build_accepted_content(template_path, title=title, url=url)
    output_path.write_text(content, encoding="utf-8")

    doc = parse_accepted_document(output_path)
    return (
        CommandResult(
            ok=True,
            command="new",
            summary=f"Created {output_path.relative_to(repo_root)}",
            diagnostics=[],
            data={
                "target": str(output_path.relative_to(repo_root)),
                "title": doc.yaml_fields.get("title", ""),
                "canonical_url": doc.yaml_fields.get("canonical_url", ""),
            },
        ),
        EXIT_OK,
    )


def run_new_rejected(args: argparse.Namespace, repo_root: Path) -> tuple[CommandResult, int]:
    csv_path = repo_root / "rejected" / "rejected.csv"
    accepted_dir = repo_root / "accepted"
    raw_url = args.url.strip()
    title = args.title.strip()
    reason = args.reason.strip()

    if not raw_url:
        return usage_result("Add rejected failed", "url must not be empty")
    if not title:
        return usage_result("Add rejected failed", "title must not be empty")
    if not reason:
        return usage_result("Add rejected failed", "reason must not be empty")

    try:
        url = normalize_url(raw_url)
    except ValueError as exc:
        return usage_result("Add rejected failed", str(exc))

    for path in sorted(accepted_dir.glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception:
            continue
        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if not canonical_url:
            continue
        try:
            accepted_url = normalize_url(canonical_url)
        except ValueError:
            continue
        if accepted_url == url:
            return refused_result(
                "Add rejected failed",
                f"url already exists in accepted: {url}",
                path=str(path.relative_to(repo_root)),
                code="refused_accepted_conflict",
            )

    if csv_path.exists() and csv_path.stat().st_size > 0:
        try:
            rejected = parse_rejected_csv(csv_path)
        except Exception:
            rejected = None
        if rejected is not None:
            for row in rejected.rows:
                try:
                    existing_url = normalize_url(row.url)
                except ValueError:
                    existing_url = row.url
                if existing_url == url:
                    return refused_result(
                        "Add rejected failed",
                        f"url already exists in rejected.csv: {url}",
                        path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                        code="refused_duplicate_url",
                    )

    file_exists = csv_path.exists()
    needs_header = (not file_exists) or csv_path.stat().st_size == 0

    if args.dry_run:
        return (
            CommandResult(
                ok=True,
                command="new",
                summary=f"Would add rejected entry to {csv_path.relative_to(repo_root)}",
                diagnostics=[],
                data={
                    "target": str(csv_path.relative_to(repo_root)),
                    "url": url,
                    "title": title,
                    "reason": reason,
                    "dry_run": True,
                },
            ),
            EXIT_OK,
        )

    with csv_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if needs_header:
            writer.writerow(["url", "title", "reason"])
        writer.writerow([url, title, reason])

    return (
        CommandResult(
            ok=True,
            command="new",
            summary=f"Added rejected entry to {csv_path.relative_to(repo_root)}",
            diagnostics=[],
            data={
                "target": str(csv_path.relative_to(repo_root)),
                "url": url,
                "title": title,
                "reason": reason,
            },
        ),
        EXIT_OK,
    )


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        args = parser.parse_args(command_args)
    except SystemExit:
        return (
            CommandResult(
                ok=False,
                command="new",
                summary="Create command failed",
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

    if args.target == "accepted":
        return run_new_accepted(args, repo_root)

    if args.target == "rejected":
        return run_new_rejected(args, repo_root)

    return (
        CommandResult(
            ok=False,
            command="new",
            summary="Create command failed",
            diagnostics=[
                Diagnostic(
                    level="error",
                    message="missing target, expected `accepted` or `rejected`",
                    code="usage_error",
                )
            ],
        ),
        EXIT_USAGE_ERROR,
    )
