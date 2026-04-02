from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from cli.accepted_schema import get_accepted_field_order
from cli.argparse_utils import CliArgumentParser
from cli.content_rules import load_schema_rules
from cli.content_rules import schema_error_diagnostic
from cli.content_rules import validate_accepted_document
from cli.content_rules import validate_rejected_values
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.errors import EXIT_VALIDATION_FAILED
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import AcceptedDocument
from cli.repo import get_accepted_dir
from cli.repo import get_rejected_csv_path
from cli.repo import get_staging_accepted_paths
from cli.repo import get_staging_layout
from cli.repo import normalize_url
from cli.repo import parse_accepted_document
from cli.repo import parse_rejected_csv
from cli.repo import serialize_simple_yaml_mapping
from cli.repo import validate_staging_accepted_filename
from cli.schema_config import SchemaConfigError

SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")
ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


@dataclass(frozen=True)
class RejectedImportRow:
    source_path: Path
    row_number: int
    url: str
    title: str
    reason: str


@dataclass(frozen=True)
class IngestAnalysis:
    diagnostics: list[Diagnostic]
    accepted_docs: list[AcceptedDocument]
    accepted_ready: list[AcceptedDocument]
    rejected_rows: list[RejectedImportRow]
    rejected_ready: list[RejectedImportRow]


def has_staging_candidates(analysis: IngestAnalysis) -> bool:
    return bool(analysis.accepted_docs or analysis.rejected_rows)


def build_parser() -> argparse.ArgumentParser:
    return CliArgumentParser(prog="youpu ingest", add_help=False)


def accepted_url_index(repo_root: Path) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception:
            continue
        raw = doc.yaml_fields.get("canonical_url", "").strip()
        if not raw:
            continue
        try:
            normalized = normalize_url(raw)
        except ValueError:
            continue
        index[normalized].append(str(path.relative_to(repo_root)))
    return index


def rejected_url_index(repo_root: Path) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    csv_path = get_rejected_csv_path(repo_root)
    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception:
        return index

    for row in rejected.rows:
        if not row.url:
            continue
        try:
            normalized = normalize_url(row.url)
        except ValueError:
            continue
        index[normalized].append(f"{csv_path.relative_to(repo_root)}:{row.row_number}")
    return index


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    slug = SLUG_CLEAN_RE.sub("-", lowered).strip("-")
    return slug or "imported"


def next_accepted_index(accepted_dir: Path) -> int:
    max_index = 0
    for path in accepted_dir.glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if not match:
            continue
        max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def build_analysis(repo_root: Path) -> IngestAnalysis:
    diagnostics: list[Diagnostic] = []
    accepted_docs: list[AcceptedDocument] = []
    rejected_rows: list[RejectedImportRow] = []
    accepted_error_paths: set[str] = set()
    rejected_error_paths: set[str] = set()
    accepted_seen_urls: dict[str, list[str]] = defaultdict(list)
    rejected_seen_urls: dict[str, list[str]] = defaultdict(list)
    try:
        rules = load_schema_rules(repo_root)
    except SchemaConfigError as exc:
        diagnostics.append(schema_error_diagnostic(exc, repo_root))
        return IngestAnalysis(
            diagnostics=diagnostics,
            accepted_docs=[],
            accepted_ready=[],
            rejected_rows=[],
            rejected_ready=[],
        )
    accepted_urls = accepted_url_index(repo_root)
    rejected_urls = rejected_url_index(repo_root)
    layout = get_staging_layout(repo_root)

    if layout.root.exists():
        for path in sorted(layout.root.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path == layout.accepted_dir or path == layout.rejected_dir:
                continue
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="staging root only accepts `accepted/` and `rejected/`",
                    path=str(path.relative_to(repo_root)),
                    code="staging_unexpected_file",
                )
            )

    if layout.accepted_dir.exists():
        for path in sorted(layout.accepted_dir.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path.is_file() and path.suffix == ".md":
                continue
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="staging/accepted only accepts markdown files",
                    path=str(path.relative_to(repo_root)),
                    code="staging_unexpected_file",
                )
            )

    if layout.rejected_dir.exists():
        for path in sorted(layout.rejected_dir.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path == layout.rejected_csv:
                continue
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="staging/rejected only accepts `rows.csv`",
                    path=str(path.relative_to(repo_root)),
                    code="staging_unexpected_file",
                )
            )

    for path in get_staging_accepted_paths(repo_root):
        rel_path = str(path.relative_to(repo_root))
        filename_error = validate_staging_accepted_filename(path)
        if filename_error:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=filename_error,
                    path=rel_path,
                    code="staging_accepted_invalid_filename",
                )
            )
            accepted_error_paths.add(rel_path)
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(level="error", message=str(exc), path=rel_path, code="staging_accepted_parse_error")
            )
            accepted_error_paths.add(rel_path)
            continue

        accepted_docs.append(doc)

        doc_diagnostics, normalized_url = validate_accepted_document(
            doc,
            rel_path=rel_path,
            rules=rules,
            code_prefix="staging_accepted",
        )
        diagnostics.extend(doc_diagnostics)
        if doc_diagnostics:
            accepted_error_paths.add(rel_path)
        if normalized_url:
            accepted_seen_urls[normalized_url].append(rel_path)
            if normalized_url in accepted_urls:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"canonical_url already exists in accepted: {normalized_url}",
                        path=rel_path,
                        code="staging_accepted_conflict_accepted",
                        details={"matches": accepted_urls[normalized_url]},
                    )
                )
                accepted_error_paths.add(rel_path)
            if normalized_url in rejected_urls:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"canonical_url already exists in rejected: {normalized_url}",
                        path=rel_path,
                        code="staging_accepted_conflict_rejected",
                        details={"matches": rejected_urls[normalized_url]},
                    )
                )
                accepted_error_paths.add(rel_path)

    for normalized_url, paths in sorted(accepted_seen_urls.items()):
        if len(paths) < 2:
            continue
        for rel_path in paths:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"duplicate canonical_url inside staging: {normalized_url}",
                    path=rel_path,
                    code="staging_accepted_duplicate_canonical_url",
                )
            )
            accepted_error_paths.add(rel_path)

    rejected_files = [layout.rejected_csv] if layout.rejected_csv.exists() else []
    for path in rejected_files:
        rel_csv_path = str(path.relative_to(repo_root))
        try:
            rejected = parse_rejected_csv(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(level="error", message=str(exc), path=rel_csv_path, code="staging_rejected_parse_error")
            )
            continue

        if rejected.columns != rules.rejected_column_names:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"invalid header, expected {','.join(rules.rejected_column_names)}",
                    path=rel_csv_path,
                    code="staging_rejected_invalid_header",
                )
            )
            continue

        for row in rejected.rows:
            row_path = f"{rel_csv_path}:{row.row_number}"
            rejected_rows.append(
                RejectedImportRow(
                    source_path=path,
                    row_number=row.row_number,
                    url=row.url,
                    title=row.title,
                    reason=row.reason,
                )
            )

            row_diagnostics, normalized_url = validate_rejected_values(
                url=row.url,
                title=row.title,
                reason=row.reason,
                path=row_path,
                code_prefix="staging_rejected",
            )
            diagnostics.extend(row_diagnostics)
            if row_diagnostics:
                rejected_error_paths.add(row_path)
            if normalized_url is None:
                continue

            if normalized_url in accepted_urls:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"url already exists in accepted: {normalized_url}",
                        path=row_path,
                        code="staging_rejected_conflict_accepted",
                        details={"matches": accepted_urls[normalized_url]},
                    )
                )
                rejected_error_paths.add(row_path)
            if normalized_url in rejected_urls:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"url already exists in rejected: {normalized_url}",
                        path=row_path,
                        code="staging_rejected_conflict_rejected",
                        details={"matches": rejected_urls[normalized_url]},
                    )
                )
                rejected_error_paths.add(row_path)

            rejected_seen_urls[normalized_url].append(row_path)

    for normalized_url, paths in sorted(rejected_seen_urls.items()):
        if len(paths) < 2:
            continue
        for row_path in paths:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"duplicate url inside {layout.rejected_csv.relative_to(repo_root)}: {normalized_url}",
                    path=row_path,
                    code="staging_rejected_duplicate_url",
                )
            )
            rejected_error_paths.add(row_path)

    accepted_ready = [
        doc for doc in accepted_docs if str(doc.path.relative_to(repo_root)) not in accepted_error_paths
    ]
    rejected_ready = [
        row
        for row in rejected_rows
        if f"{row.source_path.relative_to(repo_root)}:{row.row_number}" not in rejected_error_paths
    ]
    return IngestAnalysis(
        diagnostics=diagnostics,
        accepted_docs=accepted_docs,
        accepted_ready=accepted_ready,
        rejected_rows=rejected_rows,
        rejected_ready=rejected_ready,
    )


def serialize_accepted(doc: AcceptedDocument, repo_root: Path) -> str:
    heading = doc.yaml_fields.get("title", "").strip() or doc.heading or "标题"
    normalized_fields = dict(doc.yaml_fields)
    normalized_fields["title"] = heading
    normalized_fields["canonical_url"] = normalize_url(doc.yaml_fields["canonical_url"].strip())
    yaml_lines = serialize_simple_yaml_mapping(normalized_fields, get_accepted_field_order(repo_root)).splitlines()
    body = doc.body.rstrip()
    parts = [
        f"# {heading}",
        "",
        "```yaml",
        *yaml_lines,
        "```",
    ]
    if body:
        parts.extend(["", body])
    return "\n".join(parts) + "\n"


def target_accepted_path(repo_root: Path, doc: AcceptedDocument, index: int) -> Path:
    source_slug = slugify(doc.path.stem)
    return get_accepted_dir(repo_root) / f"SRC-{index:04d}-{source_slug}.md"


def write_rejected_csv(repo_root: Path, csv_path: Path, rows: list[tuple[str, str, str]]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(load_schema_rules(repo_root).rejected_column_names)
        writer.writerows(rows)


def merge_ingest(repo_root: Path, analysis: IngestAnalysis) -> dict[str, int]:
    accepted_dir = get_accepted_dir(repo_root)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    next_index = next_accepted_index(accepted_dir)
    imported_accepted = 0
    imported_rejected = 0

    for doc in analysis.accepted_ready:
        target = target_accepted_path(repo_root, doc, next_index)
        next_index += 1
        target.write_text(serialize_accepted(doc, repo_root), encoding="utf-8")
        doc.path.unlink()
        imported_accepted += 1

    rejected_csv = get_rejected_csv_path(repo_root)
    rejected_csv.parent.mkdir(parents=True, exist_ok=True)
    existing_rows: list[tuple[str, str, str]] = []
    if rejected_csv.exists():
        parsed = parse_rejected_csv(rejected_csv)
        existing_rows = [(row.url, row.title, row.reason) for row in parsed.rows]

    ready_row_keys = {(row.source_path, row.row_number) for row in analysis.rejected_ready}
    rows_by_file: dict[Path, list[RejectedImportRow]] = defaultdict(list)
    for row in analysis.rejected_rows:
        rows_by_file[row.source_path].append(row)

    for row in analysis.rejected_ready:
        existing_rows.append((normalize_url(row.url), row.title.strip(), row.reason.strip()))
        imported_rejected += 1

    if analysis.rejected_ready:
        write_rejected_csv(repo_root, rejected_csv, existing_rows)

    for source_path, rows in rows_by_file.items():
        remaining = [row for row in rows if (row.source_path, row.row_number) not in ready_row_keys]
        if not remaining:
            source_path.unlink()
            continue
        write_rejected_csv(
            repo_root,
            source_path,
            [(row.url, row.title, row.reason) for row in remaining],
        )

    return {
        "imported_accepted": imported_accepted,
        "imported_rejected": imported_rejected,
        "staging_root": "staging",
    }


def build_summary(analysis: IngestAnalysis, repo_root: Path) -> str:
    layout = get_staging_layout(repo_root)
    return "\n".join(
        [
            "Ingest completed",
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
                command="ingest",
                summary="Ingest failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    layout = get_staging_layout(repo_root)
    analysis = build_analysis(repo_root)
    if analysis.diagnostics:
        return (
            CommandResult(
                ok=False,
                command="ingest",
                summary="Ingest failed",
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
                summary="Ingest failed",
                diagnostics=[
                    Diagnostic(
                        level="error",
                        message="no staging candidates found",
                        code="staging_empty",
                    )
                ],
                data={
                    "staging_root": str(layout.root.relative_to(repo_root)),
                    "accepted_ready": len(analysis.accepted_ready),
                    "rejected_ready": len(analysis.rejected_ready),
                },
            ),
            EXIT_VALIDATION_FAILED,
        )

    merge_data = merge_ingest(repo_root, analysis)
    summary = build_summary(analysis, repo_root)
    return (
        CommandResult(
            ok=True,
            command="ingest",
            summary=summary,
            diagnostics=[],
            data={
                **merge_data,
                "accepted_ready": len(analysis.accepted_ready),
                "rejected_ready": len(analysis.rejected_ready),
            },
        ),
        EXIT_OK,
    )
