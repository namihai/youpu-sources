from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from youpu.domain.diagnostics import Diagnostic
from youpu.domain.rules import schema_error_diagnostic
from youpu.domain.rules import validate_accepted_document
from youpu.domain.rules import validate_rejected_values
from youpu.domain.schema import SchemaRules
from youpu.domain.schema import get_accepted_field_order
from youpu.domain.schema import get_accepted_template_path
from youpu.domain.schema import get_rejected_column_names
from youpu.domain.schema import get_rejected_template_path
from youpu.domain.schema import load_schema_rules
from youpu.domain.urls import normalize_url
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.accepted_store import parse_simple_yaml_block
from youpu.infra.rejected_store import parse_rejected_csv
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_rejected_csv_path
from youpu.infra.repo_layout import get_staging_accepted_paths
from youpu.infra.repo_layout import get_staging_layout
from youpu.infra.schema_store import SchemaConfigError
from youpu.infra.schema_store import get_schema_path
from youpu.app.staging import build_staging_analysis


@dataclass(frozen=True)
class SchemaCheck:
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class RepoCheck:
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class ImportsCheck:
    diagnostics: list[Diagnostic]
    accepted_ready: int
    rejected_ready: int
    has_candidates: bool

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class PrCheck:
    diagnostics: list[Diagnostic]
    schema: SchemaCheck
    repo: RepoCheck
    imports: ImportsCheck

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class MergeCheck:
    diagnostics: list[Diagnostic]
    schema: SchemaCheck
    repo: RepoCheck
    pending_staging: bool
    staging_issues: int

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


def run_schema_check(repo_root: Path) -> SchemaCheck:
    diagnostics: list[Diagnostic] = []
    for schema_name in ("accepted", "rejected"):
        schema_path = get_schema_path(repo_root, schema_name)
        if not schema_path.exists():
            diagnostics.append(Diagnostic(level="error", message="schema file is missing", path=str(schema_path.relative_to(repo_root)), code="schema_missing"))
    if diagnostics:
        return SchemaCheck(diagnostics=diagnostics)

    diagnostics.extend(_validate_accepted_schema(repo_root))
    diagnostics.extend(_validate_rejected_schema(repo_root))
    return SchemaCheck(diagnostics=diagnostics)


def _validate_accepted_schema(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        field_order = get_accepted_field_order(repo_root)
        template_path = get_accepted_template_path(repo_root)
    except SchemaConfigError as exc:
        return [schema_error_diagnostic(exc, repo_root)]

    if not template_path.exists():
        return [Diagnostic(level="error", message="accepted template file is missing", path=str(template_path.relative_to(repo_root)), code="accepted_template_missing")]
    try:
        template_fields = parse_simple_yaml_block(template_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [Diagnostic(level="error", message=str(exc), path=str(template_path.relative_to(repo_root)), code="accepted_template_parse_error")]

    template_order = list(template_fields.keys())
    if template_order != field_order:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="accepted template YAML fields do not match accepted schema order",
                path=str(template_path.relative_to(repo_root)),
                code="accepted_template_field_order_mismatch",
                details={"expected": field_order, "actual": template_order},
            )
        )
    return diagnostics


def _validate_rejected_schema(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        column_names = get_rejected_column_names(repo_root)
        template_path = get_rejected_template_path(repo_root)
    except SchemaConfigError as exc:
        return [schema_error_diagnostic(exc, repo_root)]

    if not template_path.exists():
        return [Diagnostic(level="error", message="rejected template file is missing", path=str(template_path.relative_to(repo_root)), code="rejected_template_missing")]

    with template_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [Diagnostic(level="error", message="rejected template must include a header row", path=str(template_path.relative_to(repo_root)), code="rejected_template_missing_header")]

    header = rows[0]
    if header != column_names:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="rejected template header does not match rejected schema order",
                path=str(template_path.relative_to(repo_root)),
                code="rejected_template_header_mismatch",
                details={"expected": column_names, "actual": header},
            )
        )
    if len(rows) > 1 and len(rows[1]) != len(column_names):
        diagnostics.append(Diagnostic(level="error", message="rejected template example row must match rejected schema column count", path=str(template_path.relative_to(repo_root)), code="rejected_template_example_mismatch"))
    return diagnostics


def run_repo_check(repo_root: Path) -> RepoCheck:
    diagnostics: list[Diagnostic] = []
    try:
        rules = load_schema_rules(repo_root)
    except SchemaConfigError:
        return RepoCheck(
            diagnostics=[
                Diagnostic(
                    level="error",
                    message="schema validation must pass before repository content validation",
                    code="repo_schema_prerequisite_failed",
                )
            ]
        )

    diagnostics.extend(_validate_repo_accepted(repo_root, rules))
    diagnostics.extend(_validate_accepted_duplicates(repo_root, rules))
    diagnostics.extend(_validate_repo_rejected(repo_root, rules))
    diagnostics.extend(_validate_rejected_duplicates(repo_root, rules))
    diagnostics.extend(_validate_cross(repo_root, rules))
    return RepoCheck(diagnostics=diagnostics)


def _validate_repo_accepted(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        rel_path = str(path.relative_to(repo_root))
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=rel_path, code="accepted_parse_error"))
            continue

        if doc.index is None or doc.slug is None:
            diagnostics.append(Diagnostic(level="error", message="invalid filename, expected SRC-####-slug.md", path=rel_path, code="accepted_invalid_filename"))

        doc_diagnostics, _ = validate_accepted_document(doc, rel_path=rel_path, rules=rules, code_prefix="accepted")
        diagnostics.extend(doc_diagnostics)
    return diagnostics


def _validate_repo_rejected(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    csv_path = get_rejected_csv_path(repo_root)

    if not csv_path.exists():
        return diagnostics

    try:
        rejected = parse_rejected_csv(csv_path, allow_missing=True)
    except Exception as exc:
        return [Diagnostic(level="error", message=str(exc), path=str(csv_path.relative_to(repo_root)), code="rejected_parse_error")]

    if rejected.columns != rules.rejected_column_names:
        diagnostics.append(Diagnostic(level="error", message=f"invalid header, expected {','.join(rules.rejected_column_names)}", path=str(csv_path.relative_to(repo_root)), code="rejected_invalid_header"))
        return diagnostics

    for issue in rejected.structural_issues:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"row has {issue.actual_width} columns, expected {issue.expected_width}",
                path=f"{csv_path.relative_to(repo_root)}:{issue.row_number}",
                code="rejected_invalid_row_shape",
            )
        )
    for row in rejected.rows:
        if any(issue.row_number == row.row_number for issue in rejected.structural_issues):
            continue
        row_diags, _ = validate_rejected_values(url=row.url, title=row.title, reason=row.reason, path=f"{csv_path.relative_to(repo_root)}:{row.row_number}", code_prefix="rejected")
        diagnostics.extend(row_diags)
    return diagnostics


def _validate_cross(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    accepted_urls: dict[str, list[str]] = defaultdict(list)
    rejected_urls: dict[str, list[int]] = defaultdict(list)

    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="warning", message=f"cross-file checks skipped for unreadable accepted file: {exc}", path=str(path.relative_to(repo_root)), code="cross_partial_due_to_parse_error"))
            continue
        doc_diagnostics, normalized = validate_accepted_document(doc, rel_path=str(path.relative_to(repo_root)), rules=rules, code_prefix="accepted")
        if doc_diagnostics:
            diagnostics.append(Diagnostic(level="warning", message="cross-file checks skipped for invalid accepted file", path=str(path.relative_to(repo_root)), code="cross_partial_due_to_parse_error"))
            continue
        if not normalized:
            continue
        accepted_urls[normalized].append(str(path.relative_to(repo_root)))

    csv_path = get_rejected_csv_path(repo_root)
    try:
        rejected = parse_rejected_csv(csv_path, allow_missing=True)
    except Exception as exc:
        diagnostics.append(Diagnostic(level="warning", message=f"cross-file checks skipped for unreadable rejected CSV: {exc}", path=str(csv_path.relative_to(repo_root)), code="cross_partial_due_to_parse_error"))
        return diagnostics
    if rejected.columns and rejected.columns != rules.rejected_column_names:
        diagnostics.append(Diagnostic(level="warning", message="cross-file checks skipped because rejected CSV header is invalid", path=str(csv_path.relative_to(repo_root)), code="cross_partial_due_to_parse_error"))
        return diagnostics
    if rejected.structural_issues:
        for issue in rejected.structural_issues:
            diagnostics.append(Diagnostic(level="warning", message="cross-file checks skipped for structurally invalid rejected row", path=f"{csv_path.relative_to(repo_root)}:{issue.row_number}", code="cross_partial_due_to_parse_error"))
        return diagnostics
    for row in rejected.rows:
        if not row.url:
            continue
        try:
            normalized = normalize_url(row.url)
        except ValueError:
            continue
        rejected_urls[normalized].append(row.row_number)

    for url in sorted(set(accepted_urls) & set(rejected_urls)):
        accepted_paths = accepted_urls[url]
        rejected_rows = rejected_urls[url]
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"canonical_url exists in both accepted and rejected: {url}",
                path=", ".join(accepted_paths + [f"{csv_path.relative_to(repo_root)}:{row}" for row in rejected_rows]),
                code="cross_url_conflict",
                details={"url": url, "accepted_paths": accepted_paths, "rejected_rows": rejected_rows},
            )
        )
    return diagnostics


def _validate_accepted_duplicates(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_canonical_url: dict[str, list[str]] = defaultdict(list)
    by_title: dict[str, list[str]] = defaultdict(list)
    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(Diagnostic(level="warning", message=f"duplicate checks skipped for unreadable accepted file: {exc}", path=str(path.relative_to(repo_root)), code="accepted_duplicates_partial"))
            continue
        doc_diagnostics, normalized = validate_accepted_document(doc, rel_path=str(path.relative_to(repo_root)), rules=rules, code_prefix="accepted")
        if doc_diagnostics:
            diagnostics.append(Diagnostic(level="warning", message="duplicate checks skipped for invalid accepted file", path=str(path.relative_to(repo_root)), code="accepted_duplicates_partial"))
            continue
        title = doc.yaml_fields.get("title", "").strip()
        if title:
            by_title[title].append(str(path.relative_to(repo_root)))
        if not normalized:
            continue
        by_canonical_url[normalized].append(str(path.relative_to(repo_root)))
    for canonical_url, paths in sorted(by_canonical_url.items()):
        if len(paths) >= 2:
            diagnostics.append(Diagnostic(level="error", message=f"duplicate canonical_url: {canonical_url}", path=", ".join(paths), code="accepted_duplicate_canonical_url", details={"canonical_url": canonical_url, "paths": paths}))
    for title, paths in sorted(by_title.items()):
        if len(paths) >= 2:
            diagnostics.append(Diagnostic(level="warning", message=f"duplicate title: {title}", path=", ".join(paths), code="accepted_duplicate_title", details={"title": title, "paths": paths}))
    return diagnostics


def _validate_rejected_duplicates(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_url: dict[str, list[int]] = defaultdict(list)
    csv_path = get_rejected_csv_path(repo_root)
    try:
        rejected = parse_rejected_csv(csv_path, allow_missing=True)
    except Exception as exc:
        diagnostics.append(Diagnostic(level="warning", message=f"duplicate checks skipped for unreadable rejected CSV: {exc}", path=str(csv_path.relative_to(repo_root)), code="rejected_duplicates_partial"))
        return diagnostics
    if rejected.columns and rejected.columns != rules.rejected_column_names:
        diagnostics.append(Diagnostic(level="warning", message="duplicate checks skipped because rejected CSV header is invalid", path=str(csv_path.relative_to(repo_root)), code="rejected_duplicates_partial"))
        return diagnostics
    if rejected.structural_issues:
        for issue in rejected.structural_issues:
            diagnostics.append(Diagnostic(level="warning", message="duplicate checks skipped for structurally invalid rejected row", path=f"{csv_path.relative_to(repo_root)}:{issue.row_number}", code="rejected_duplicates_partial"))
        return diagnostics
    for row in rejected.rows:
        if not row.url:
            continue
        try:
            normalized = normalize_url(row.url)
        except ValueError:
            continue
        by_url[normalized].append(row.row_number)
    for url, rows in sorted(by_url.items()):
        if len(rows) >= 2:
            diagnostics.append(Diagnostic(level="error", message=f"duplicate rejected url: {url}", path=", ".join(f"{csv_path.relative_to(repo_root)}:{row}" for row in rows), code="rejected_duplicate_url", details={"url": url, "rows": rows}))
    return diagnostics


def run_imports_check(repo_root: Path) -> ImportsCheck:
    analysis = build_staging_analysis(repo_root)
    has_candidates = bool(analysis.accepted_docs or analysis.rejected_rows)
    diagnostics = list(analysis.diagnostics)
    return ImportsCheck(
        diagnostics=diagnostics,
        accepted_ready=len(analysis.accepted_ready),
        rejected_ready=len(analysis.rejected_ready),
        has_candidates=has_candidates,
    )


def run_pr_check(repo_root: Path) -> PrCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root) if schema.ok else RepoCheck(diagnostics=[])
    imports = run_imports_check(repo_root) if schema.ok else ImportsCheck(diagnostics=[], accepted_ready=0, rejected_ready=0, has_candidates=False)
    diagnostics = [*schema.diagnostics, *repo.diagnostics, *imports.diagnostics]
    return PrCheck(diagnostics=diagnostics, schema=schema, repo=repo, imports=imports)


def run_merge_check(repo_root: Path) -> MergeCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root) if schema.ok else RepoCheck(diagnostics=[])
    diagnostics = [*schema.diagnostics, *repo.diagnostics]
    layout = get_staging_layout(repo_root)
    accepted_files = get_staging_accepted_paths(repo_root)
    rejected_files = [layout.rejected_csv] if layout.rejected_csv.exists() else []
    pending_staging = bool(accepted_files or rejected_files)
    if pending_staging:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="staging directory still contains pending files; run `youpu ingest` first",
                path=str(layout.root.relative_to(repo_root)),
                code="merge_pending_staging",
                details={
                    "accepted_files": [str(path.relative_to(repo_root)) for path in accepted_files],
                    "rejected_files": [str(path.relative_to(repo_root)) for path in rejected_files],
                },
            )
        )
    imports = run_imports_check(repo_root) if schema.ok else ImportsCheck(diagnostics=[], accepted_ready=0, rejected_ready=0, has_candidates=False)
    diagnostics.extend(imports.diagnostics)
    return MergeCheck(diagnostics=diagnostics, schema=schema, repo=repo, pending_staging=pending_staging, staging_issues=len(imports.diagnostics))
