from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from youpu.app.staging import build_staging_analysis
from youpu.domain.diagnostics import Diagnostic
from youpu.domain.rules import schema_error_diagnostic
from youpu.domain.rules import validate_accepted_document
from youpu.domain.schema import SchemaRules
from youpu.domain.schema import get_accepted_field_order
from youpu.domain.schema import get_accepted_template_path
from youpu.domain.schema import load_schema_rules
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.accepted_store import parse_simple_yaml_block
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_data_root
from youpu.infra.repo_layout import get_staging_accepted_paths
from youpu.infra.repo_layout import get_staging_layout
from youpu.infra.schema_store import SchemaConfigError
from youpu.infra.schema_store import get_schema_path


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
    schema_path = get_schema_path(repo_root, "accepted")
    if not schema_path.exists():
        diagnostics.append(Diagnostic(level="error", message="schema file is missing", path=str(schema_path.relative_to(repo_root)), code="schema_missing"))
        return SchemaCheck(diagnostics=diagnostics)

    diagnostics.extend(_validate_accepted_schema(repo_root))
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

    diagnostics.extend(_validate_data_root(repo_root))
    diagnostics.extend(_validate_repo_accepted(repo_root, rules))
    diagnostics.extend(_validate_accepted_duplicates(repo_root, rules))
    return RepoCheck(diagnostics=diagnostics)


def _validate_data_root(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    data_root = get_data_root(repo_root)
    if not data_root.exists():
        return diagnostics
    for path in sorted(data_root.iterdir()):
        if path.name.startswith("."):
            continue
        if path.is_file() and path.suffix == ".md":
            continue
        diagnostics.append(Diagnostic(level="error", message="data root only accepts markdown files", path=str(path.relative_to(repo_root)), code="data_unexpected_file"))
    return diagnostics


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


def _validate_accepted_duplicates(repo_root: Path, rules: SchemaRules) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_index: dict[int, list[str]] = defaultdict(list)
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
        if doc.index is not None:
            by_index[doc.index].append(str(path.relative_to(repo_root)))
        title = doc.yaml_fields.get("title", "").strip()
        if title:
            by_title[title].append(str(path.relative_to(repo_root)))
        if not normalized:
            continue
        by_canonical_url[normalized].append(str(path.relative_to(repo_root)))
    for index, paths in sorted(by_index.items()):
        if len(paths) >= 2:
            diagnostics.append(Diagnostic(level="error", message=f"duplicate accepted index: SRC-{index:04d}", path=", ".join(paths), code="accepted_duplicate_index", details={"index": index, "paths": paths}))
    for canonical_url, paths in sorted(by_canonical_url.items()):
        if len(paths) >= 2:
            diagnostics.append(Diagnostic(level="error", message=f"duplicate canonical_url: {canonical_url}", path=", ".join(paths), code="accepted_duplicate_canonical_url", details={"canonical_url": canonical_url, "paths": paths}))
    for title, paths in sorted(by_title.items()):
        if len(paths) >= 2:
            diagnostics.append(Diagnostic(level="warning", message=f"duplicate title: {title}", path=", ".join(paths), code="accepted_duplicate_title", details={"title": title, "paths": paths}))
    return diagnostics


def run_imports_check(repo_root: Path) -> ImportsCheck:
    analysis = build_staging_analysis(repo_root)
    diagnostics = list(analysis.diagnostics)
    return ImportsCheck(
        diagnostics=diagnostics,
        accepted_ready=len(analysis.accepted_ready),
        has_candidates=bool(analysis.accepted_docs),
    )


def run_pr_check(repo_root: Path) -> PrCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root) if schema.ok else RepoCheck(diagnostics=[])
    imports = run_imports_check(repo_root) if schema.ok else ImportsCheck(diagnostics=[], accepted_ready=0, has_candidates=False)
    diagnostics = [*schema.diagnostics, *repo.diagnostics, *imports.diagnostics]
    return PrCheck(diagnostics=diagnostics, schema=schema, repo=repo, imports=imports)


def run_merge_check(repo_root: Path) -> MergeCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root) if schema.ok else RepoCheck(diagnostics=[])
    diagnostics = [*schema.diagnostics, *repo.diagnostics]
    layout = get_staging_layout(repo_root)
    accepted_files = get_staging_accepted_paths(repo_root)
    pending_staging = bool(accepted_files)
    if pending_staging:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="staging directory still contains pending files; run `youpu ingest` first",
                path=str(layout.root.relative_to(repo_root)),
                code="merge_pending_staging",
                details={
                    "accepted_files": [str(path.relative_to(repo_root)) for path in accepted_files],
                },
            )
        )
    imports = run_imports_check(repo_root) if schema.ok else ImportsCheck(diagnostics=[], accepted_ready=0, has_candidates=False)
    diagnostics.extend(imports.diagnostics)
    return MergeCheck(diagnostics=diagnostics, schema=schema, repo=repo, pending_staging=pending_staging, staging_issues=len(imports.diagnostics))
