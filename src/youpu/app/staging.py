from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.diagnostics import Diagnostic
from youpu.domain.rules import schema_error_diagnostic
from youpu.domain.rules import validate_accepted_document
from youpu.domain.rules import validate_rejected_values
from youpu.domain.schema import SchemaRules
from youpu.domain.schema import load_schema_rules
from youpu.domain.urls import normalize_url
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.rejected_store import parse_rejected_csv
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_rejected_csv_path
from youpu.infra.repo_layout import get_staging_accepted_paths
from youpu.infra.repo_layout import get_staging_layout
from youpu.infra.repo_layout import validate_staging_accepted_filename
from youpu.infra.schema_store import SchemaConfigError


@dataclass(frozen=True)
class RejectedImportRow:
    source_path: Path
    row_number: int
    url: str
    title: str
    reason: str


@dataclass(frozen=True)
class StagingAnalysis:
    diagnostics: list[Diagnostic]
    accepted_docs: list[AcceptedDocument]
    accepted_ready: list[AcceptedDocument]
    rejected_rows: list[RejectedImportRow]
    rejected_ready: list[RejectedImportRow]


def build_staging_analysis(repo_root: Path) -> StagingAnalysis:
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
        return StagingAnalysis(
            diagnostics=[
                Diagnostic(
                    level="error",
                    message="schema validation must pass before validating staging content",
                    code="staging_schema_prerequisite_failed",
                    details={"cause": schema_error_diagnostic(exc, repo_root).code},
                )
            ],
            accepted_docs=[],
            accepted_ready=[],
            rejected_rows=[],
            rejected_ready=[],
        )

    accepted_urls, accepted_index_diags = accepted_url_index(repo_root, rules=rules)
    rejected_urls, rejected_index_diags = rejected_url_index(repo_root, rules=rules)
    diagnostics.extend(accepted_index_diags)
    diagnostics.extend(rejected_index_diags)
    layout = get_staging_layout(repo_root)

    if layout.root.exists():
        for path in sorted(layout.root.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path == layout.accepted_dir or path == layout.rejected_dir:
                continue
            diagnostics.append(Diagnostic(level="error", message="staging root only accepts `accepted/` and `rejected/`", path=str(path.relative_to(repo_root)), code="staging_unexpected_file"))

    if layout.accepted_dir.exists():
        for path in sorted(layout.accepted_dir.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path.is_file() and path.suffix == ".md":
                continue
            diagnostics.append(Diagnostic(level="error", message="staging/accepted only accepts markdown files", path=str(path.relative_to(repo_root)), code="staging_unexpected_file"))

    if layout.rejected_dir.exists():
        for path in sorted(layout.rejected_dir.iterdir()):
            if path.name == ".gitkeep":
                continue
            if path == layout.rejected_csv:
                continue
            diagnostics.append(Diagnostic(level="error", message="staging/rejected only accepts `rows.csv`", path=str(path.relative_to(repo_root)), code="staging_unexpected_file"))

    for path in get_staging_accepted_paths(repo_root):
        rel_path = str(path.relative_to(repo_root))
        filename_error = validate_staging_accepted_filename(path)
        if filename_error:
            diagnostics.append(Diagnostic(level="error", message=filename_error, path=rel_path, code="staging_accepted_invalid_filename"))
            accepted_error_paths.add(rel_path)
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=rel_path, code="staging_accepted_parse_error"))
            accepted_error_paths.add(rel_path)
            continue
        accepted_docs.append(doc)
        doc_diagnostics, normalized_url = validate_accepted_document(doc, rel_path=rel_path, rules=rules, code_prefix="staging_accepted")
        diagnostics.extend(doc_diagnostics)
        if doc_diagnostics:
            accepted_error_paths.add(rel_path)
        if normalized_url:
            accepted_seen_urls[normalized_url].append(rel_path)
            if normalized_url in accepted_urls:
                diagnostics.append(Diagnostic(level="error", message=f"canonical_url already exists in accepted: {normalized_url}", path=rel_path, code="staging_accepted_conflict_accepted", details={"matches": accepted_urls[normalized_url]}))
                accepted_error_paths.add(rel_path)
            if normalized_url in rejected_urls:
                diagnostics.append(Diagnostic(level="error", message=f"canonical_url already exists in rejected: {normalized_url}", path=rel_path, code="staging_accepted_conflict_rejected", details={"matches": rejected_urls[normalized_url]}))
                accepted_error_paths.add(rel_path)

    for normalized_url, paths in sorted(accepted_seen_urls.items()):
        if len(paths) >= 2:
            for rel_path in paths:
                diagnostics.append(Diagnostic(level="error", message=f"duplicate canonical_url inside staging: {normalized_url}", path=rel_path, code="staging_accepted_duplicate_canonical_url"))
                accepted_error_paths.add(rel_path)

    rejected_files = [layout.rejected_csv] if layout.rejected_csv.exists() else []
    for path in rejected_files:
        rel_csv_path = str(path.relative_to(repo_root))
        try:
            rejected = parse_rejected_csv(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=rel_csv_path, code="staging_rejected_parse_error"))
            continue
        if rejected.columns != rules.rejected_column_names:
            diagnostics.append(Diagnostic(level="error", message=f"invalid header, expected {','.join(rules.rejected_column_names)}", path=rel_csv_path, code="staging_rejected_invalid_header"))
            continue
        for issue in rejected.structural_issues:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"row has {issue.actual_width} columns, expected {issue.expected_width}",
                    path=f"{rel_csv_path}:{issue.row_number}",
                    code="staging_rejected_invalid_row_shape",
                )
            )
            rejected_error_paths.add(f"{rel_csv_path}:{issue.row_number}")
        for row in rejected.rows:
            row_path = f"{rel_csv_path}:{row.row_number}"
            rejected_rows.append(RejectedImportRow(source_path=path, row_number=row.row_number, url=row.url, title=row.title, reason=row.reason))
            if any(issue.row_number == row.row_number for issue in rejected.structural_issues):
                continue
            row_diagnostics, normalized_url = validate_rejected_values(url=row.url, title=row.title, reason=row.reason, path=row_path, code_prefix="staging_rejected")
            diagnostics.extend(row_diagnostics)
            if row_diagnostics:
                rejected_error_paths.add(row_path)
            if normalized_url is None:
                continue
            if normalized_url in accepted_urls:
                diagnostics.append(Diagnostic(level="error", message=f"url already exists in accepted: {normalized_url}", path=row_path, code="staging_rejected_conflict_accepted", details={"matches": accepted_urls[normalized_url]}))
                rejected_error_paths.add(row_path)
            if normalized_url in rejected_urls:
                diagnostics.append(Diagnostic(level="error", message=f"url already exists in rejected: {normalized_url}", path=row_path, code="staging_rejected_conflict_rejected", details={"matches": rejected_urls[normalized_url]}))
                rejected_error_paths.add(row_path)
            rejected_seen_urls[normalized_url].append(row_path)

    for normalized_url, paths in sorted(rejected_seen_urls.items()):
        if len(paths) >= 2:
            for row_path in paths:
                diagnostics.append(Diagnostic(level="error", message=f"duplicate url inside {layout.rejected_csv.relative_to(repo_root)}: {normalized_url}", path=row_path, code="staging_rejected_duplicate_url"))
                rejected_error_paths.add(row_path)

    return StagingAnalysis(
        diagnostics=diagnostics,
        accepted_docs=accepted_docs,
        accepted_ready=[doc for doc in accepted_docs if str(doc.path.relative_to(repo_root)) not in accepted_error_paths],
        rejected_rows=rejected_rows,
        rejected_ready=[row for row in rejected_rows if f"{row.source_path.relative_to(repo_root)}:{row.row_number}" not in rejected_error_paths],
    )


def has_staging_candidates(analysis: StagingAnalysis) -> bool:
    return bool(analysis.accepted_docs or analysis.rejected_rows)


def accepted_url_index(repo_root: Path, *, rules: SchemaRules) -> tuple[dict[str, list[str]], list[Diagnostic]]:
    index: dict[str, list[str]] = defaultdict(list)
    diagnostics: list[Diagnostic] = []
    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        rel_path = str(path.relative_to(repo_root))
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="error", message=f"cannot validate staging conflicts because repository accepted data is unreadable: {exc}", path=rel_path, code="repo_accepted_conflict_index_failed"))
            continue
        doc_diagnostics, normalized = validate_accepted_document(doc, rel_path=rel_path, rules=rules, code_prefix="repo_accepted")
        if doc_diagnostics:
            diagnostics.append(Diagnostic(level="error", message="cannot validate staging conflicts because repository accepted data is invalid", path=rel_path, code="repo_accepted_conflict_index_failed"))
            continue
        raw = doc.yaml_fields.get("canonical_url", "").strip()
        if not raw:
            continue
        if normalized is None:
            diagnostics.append(Diagnostic(level="error", message="cannot validate staging conflicts because repository accepted URL is invalid", path=rel_path, code="repo_accepted_conflict_index_failed"))
            continue
        index[normalized].append(rel_path)
    return index, diagnostics


def rejected_url_index(repo_root: Path, *, rules: SchemaRules) -> tuple[dict[str, list[str]], list[Diagnostic]]:
    index: dict[str, list[str]] = defaultdict(list)
    diagnostics: list[Diagnostic] = []
    csv_path = get_rejected_csv_path(repo_root)
    try:
        rejected = parse_rejected_csv(csv_path, allow_missing=True)
    except Exception as exc:
        return index, [Diagnostic(level="error", message=f"cannot validate staging conflicts because repository rejected data is unreadable: {exc}", path=str(csv_path.relative_to(repo_root)), code="repo_rejected_conflict_index_failed")]
    rel_csv_path = str(csv_path.relative_to(repo_root))
    if rejected.columns and rejected.columns != rules.rejected_column_names:
        diagnostics.append(Diagnostic(level="error", message="cannot validate staging conflicts because repository rejected header is invalid", path=rel_csv_path, code="repo_rejected_conflict_index_failed"))
        return index, diagnostics
    if rejected.structural_issues:
        for issue in rejected.structural_issues:
            diagnostics.append(Diagnostic(level="error", message="cannot validate staging conflicts because repository rejected rows are structurally invalid", path=f"{rel_csv_path}:{issue.row_number}", code="repo_rejected_conflict_index_failed"))
        return index, diagnostics
    for row in rejected.rows:
        if not row.url:
            continue
        try:
            normalized = normalize_url(row.url)
        except ValueError:
            diagnostics.append(Diagnostic(level="error", message="cannot validate staging conflicts because repository rejected URL is invalid", path=f"{rel_csv_path}:{row.row_number}", code="repo_rejected_conflict_index_failed"))
            continue
        index[normalized].append(f"{csv_path.relative_to(repo_root)}:{row.row_number}")
    return index, diagnostics
