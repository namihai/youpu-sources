from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from cli.commands.validate import DISALLOWED_FIELDS
from cli.commands.validate import REJECTED_COLUMNS
from cli.commands.validate import REQUIRED_NONEMPTY_FIELDS
from cli.errors import EXIT_OK
from cli.errors import EXIT_USAGE_ERROR
from cli.output import CommandResult
from cli.output import Diagnostic
from cli.repo import AcceptedDocument
from cli.repo import ImportsLayout
from cli.repo import ensure_imports_layout
from cli.repo import normalize_url
from cli.repo import parse_accepted_document
from cli.repo import parse_rejected_csv

SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")
ACCEPTED_FIELD_ORDER = [
    "title",
    "canonical_url",
    "domain",
    "content_type",
    "data_form",
    "data_type",
    "region",
    "source_type",
    "source_org",
    "permissions",
    "tags",
    "use_cases",
]
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="youpu ingest", add_help=False)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def accepted_url_index(repo_root: Path) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for path in sorted((repo_root / "accepted").glob("*.md")):
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
    csv_path = repo_root / "rejected" / "rejected.csv"
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
    accepted_urls = accepted_url_index(repo_root)
    rejected_urls = rejected_url_index(repo_root)
    layout = ensure_imports_layout(repo_root)

    for path in sorted(layout.accepted.glob("*.md")):
        rel_path = str(path.relative_to(repo_root))
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(level="error", message=str(exc), path=rel_path, code="import_accepted_parse_error")
            )
            accepted_error_paths.add(rel_path)
            continue

        accepted_docs.append(doc)

        if not doc.heading:
            diagnostics.append(
                Diagnostic(level="error", message="missing H1 title", path=rel_path, code="import_accepted_missing_h1")
            )
            accepted_error_paths.add(rel_path)
        elif doc.yaml_fields.get("title", "").strip() and doc.heading != doc.yaml_fields.get("title", "").strip():
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="H1 title does not match YAML `title`",
                    path=rel_path,
                    code="import_accepted_title_mismatch",
                )
            )
            accepted_error_paths.add(rel_path)

        for key in REQUIRED_NONEMPTY_FIELDS:
            value = doc.yaml_fields.get(key, "").strip()
            if not value:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"missing required field `{key}`",
                        path=rel_path,
                        code="import_accepted_missing_field",
                        details={"field": key},
                    )
                )
                accepted_error_paths.add(rel_path)

        for key in DISALLOWED_FIELDS:
            if key in doc.yaml_fields:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"field `{key}` is no longer part of the accepted schema",
                        path=rel_path,
                        code="import_accepted_disallowed_field",
                        details={"field": key},
                    )
                )
                accepted_error_paths.add(rel_path)

        for key in ("tags", "use_cases"):
            value = doc.yaml_fields.get(key, "").strip()
            if value and not (value.startswith("[") and value.endswith("]")):
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"field `{key}` must use inline array syntax like [a, b]",
                        path=rel_path,
                        code="import_accepted_invalid_array",
                        details={"field": key},
                    )
                )
                accepted_error_paths.add(rel_path)

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if canonical_url:
            try:
                normalized_url = normalize_url(canonical_url)
            except ValueError as exc:
                diagnostics.append(
                    Diagnostic(level="error", message=str(exc), path=rel_path, code="import_accepted_invalid_canonical_url")
                )
                accepted_error_paths.add(rel_path)
            else:
                accepted_seen_urls[normalized_url].append(rel_path)
                if normalized_url in accepted_urls:
                    diagnostics.append(
                        Diagnostic(
                            level="error",
                            message=f"canonical_url already exists in accepted: {normalized_url}",
                            path=rel_path,
                            code="import_accepted_conflict_accepted",
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
                            code="import_accepted_conflict_rejected",
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
                    message=f"duplicate canonical_url inside imports/accepted: {normalized_url}",
                    path=rel_path,
                    code="import_accepted_duplicate_canonical_url",
                )
            )
            accepted_error_paths.add(rel_path)

    for path in sorted(layout.rejected.glob("*.csv")):
        rel_csv_path = str(path.relative_to(repo_root))
        try:
            rejected = parse_rejected_csv(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(level="error", message=str(exc), path=rel_csv_path, code="import_rejected_parse_error")
            )
            continue

        if rejected.columns != REJECTED_COLUMNS:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"invalid header, expected {','.join(REJECTED_COLUMNS)}",
                    path=rel_csv_path,
                    code="import_rejected_invalid_header",
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

            if not row.url:
                diagnostics.append(Diagnostic(level="error", message="missing `url`", path=row_path, code="import_rejected_missing_url"))
                rejected_error_paths.add(row_path)
                continue

            try:
                normalized_url = normalize_url(row.url)
            except ValueError as exc:
                diagnostics.append(Diagnostic(level="error", message=str(exc), path=row_path, code="import_rejected_invalid_url"))
                rejected_error_paths.add(row_path)
                continue

            if not row.title:
                diagnostics.append(Diagnostic(level="error", message="missing `title`", path=row_path, code="import_rejected_missing_title"))
                rejected_error_paths.add(row_path)
            if not row.reason:
                diagnostics.append(Diagnostic(level="error", message="missing `reason`", path=row_path, code="import_rejected_missing_reason"))
                rejected_error_paths.add(row_path)
            if normalized_url in accepted_urls:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"url already exists in accepted: {normalized_url}",
                        path=row_path,
                        code="import_rejected_conflict_accepted",
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
                        code="import_rejected_conflict_rejected",
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
                    message=f"duplicate url inside imports/rejected: {normalized_url}",
                    path=row_path,
                    code="import_rejected_duplicate_url",
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


def serialize_accepted(doc: AcceptedDocument) -> str:
    heading = doc.yaml_fields.get("title", "").strip() or doc.heading or "标题"
    normalized_fields = dict(doc.yaml_fields)
    normalized_fields["title"] = heading
    normalized_fields["canonical_url"] = normalize_url(doc.yaml_fields["canonical_url"].strip())
    yaml_lines = [f"{key}: {normalized_fields.get(key, '').strip()}" for key in ACCEPTED_FIELD_ORDER]
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
    return repo_root / "accepted" / f"SRC-{index:04d}-{source_slug}.md"


def write_rejected_csv(csv_path: Path, rows: list[tuple[str, str, str]]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(REJECTED_COLUMNS)
        writer.writerows(rows)


def merge_ingest(repo_root: Path, layout: ImportsLayout, analysis: IngestAnalysis) -> dict[str, int]:
    accepted_dir = repo_root / "accepted"
    next_index = next_accepted_index(accepted_dir)
    imported_accepted = 0
    imported_rejected = 0

    for doc in analysis.accepted_ready:
        target = target_accepted_path(repo_root, doc, next_index)
        next_index += 1
        target.write_text(serialize_accepted(doc), encoding="utf-8")
        doc.path.unlink()
        imported_accepted += 1

    rejected_csv = repo_root / "rejected" / "rejected.csv"
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
        write_rejected_csv(rejected_csv, existing_rows)

    for source_path, rows in rows_by_file.items():
        remaining = [row for row in rows if (row.source_path, row.row_number) not in ready_row_keys]
        if not remaining:
            source_path.unlink()
            continue
        write_rejected_csv(
            source_path,
            [(row.url, row.title, row.reason) for row in remaining],
        )

    return {
        "imported_accepted": imported_accepted,
        "imported_rejected": imported_rejected,
        "imports_root": str(layout.root.relative_to(repo_root)),
    }


def build_summary(repo_root: Path, layout: ImportsLayout, analysis: IngestAnalysis, *, dry_run: bool) -> str:
    header = "Ingest dry-run completed" if dry_run else "Ingest completed"
    return "\n".join(
        [
            header,
            f"imports root: {layout.root.relative_to(repo_root)}",
            f"accepted candidates ready: {len(analysis.accepted_ready)}",
            f"rejected candidates ready: {len(analysis.rejected_ready)}",
            f"issues: {len(analysis.diagnostics)}",
        ]
    )


def write_reports(
    repo_root: Path,
    layout: ImportsLayout,
    analysis: IngestAnalysis,
    *,
    dry_run: bool,
    merge_data: dict[str, int] | None = None,
) -> None:
    summary = build_summary(repo_root, layout, analysis, dry_run=dry_run)
    issues_md = layout.reports / "issues.md"
    summary_json = layout.reports / "summary.json"

    md_lines = [
        "# Ingest Report",
        "",
        f"- mode: {'dry-run' if dry_run else 'write'}",
        f"- imports root: {layout.root.relative_to(repo_root)}",
        f"- accepted ready: {len(analysis.accepted_ready)}",
        f"- rejected ready: {len(analysis.rejected_ready)}",
        f"- issues: {len(analysis.diagnostics)}",
    ]
    if merge_data is not None:
        md_lines.extend(
            [
                f"- imported accepted: {merge_data.get('imported_accepted', 0)}",
                f"- imported rejected: {merge_data.get('imported_rejected', 0)}",
            ]
        )

    if analysis.diagnostics:
        md_lines.extend(["", "## Issues", ""])
        for diag in analysis.diagnostics:
            line = f"- `{diag.path}`: {diag.message}" if diag.path else f"- {diag.message}"
            if diag.code:
                line = f"{line} (`{diag.code}`)"
            md_lines.append(line)
    else:
        md_lines.extend(["", "## Issues", "", "- none"])

    issues_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    payload = {
        "summary": summary,
        "dry_run": dry_run,
        "imports_root": str(layout.root.relative_to(repo_root)),
        "accepted_ready": len(analysis.accepted_ready),
        "rejected_ready": len(analysis.rejected_ready),
        "issues": len(analysis.diagnostics),
        "diagnostics": [
            {
                "level": diag.level,
                "message": diag.message,
                "path": diag.path,
                "code": diag.code,
                "details": diag.details,
            }
            for diag in analysis.diagnostics
        ],
    }
    if merge_data is not None:
        payload.update(merge_data)
    summary_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(command_args: list[str], repo_root: Path) -> tuple[CommandResult, int]:
    parser = build_parser()
    try:
        args = parser.parse_args(command_args)
    except SystemExit:
        return (
            CommandResult(
                ok=False,
                command="ingest",
                summary="Ingest failed",
                diagnostics=[Diagnostic(level="error", message="invalid arguments", code="usage_error")],
            ),
            EXIT_USAGE_ERROR,
        )

    layout = ensure_imports_layout(repo_root)
    analysis = build_analysis(repo_root)

    if args.dry_run:
        summary = build_summary(repo_root, layout, analysis, dry_run=True)
        write_reports(repo_root, layout, analysis, dry_run=True)
        return (
            CommandResult(
                ok=not analysis.diagnostics,
                command="ingest",
                summary=summary,
                diagnostics=analysis.diagnostics,
                data={
                    "imports_root": str(layout.root.relative_to(repo_root)),
                    "accepted_ready": len(analysis.accepted_ready),
                    "rejected_ready": len(analysis.rejected_ready),
                    "dry_run": True,
                },
            ),
            EXIT_OK if not analysis.diagnostics else EXIT_USAGE_ERROR,
        )

    merge_data = merge_ingest(repo_root, layout, analysis)
    summary = build_summary(repo_root, layout, analysis, dry_run=False)
    write_reports(repo_root, layout, analysis, dry_run=False, merge_data=merge_data)
    return (
        CommandResult(
            ok=not analysis.diagnostics,
            command="ingest",
            summary=summary,
            diagnostics=analysis.diagnostics,
            data={
                **merge_data,
                "accepted_ready": len(analysis.accepted_ready),
                "rejected_ready": len(analysis.rejected_ready),
                "dry_run": False,
            },
        ),
        EXIT_OK if not analysis.diagnostics else EXIT_USAGE_ERROR,
    )
