from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.diagnostics import Diagnostic
from youpu.domain.rules import schema_error_diagnostic
from youpu.domain.rules import validate_accepted_document
from youpu.domain.schema import SchemaRules
from youpu.domain.schema import load_schema_rules
from youpu.infra.accepted_store import parse_accepted_document
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_staging_accepted_paths
from youpu.infra.repo_layout import get_staging_layout
from youpu.infra.repo_layout import validate_staging_accepted_filename
from youpu.infra.schema_store import SchemaConfigError


@dataclass(frozen=True)
class StagingAnalysis:
    diagnostics: list[Diagnostic]
    accepted_docs: list[AcceptedDocument]
    accepted_ready: list[AcceptedDocument]


def build_staging_analysis(repo_root: Path) -> StagingAnalysis:
    diagnostics: list[Diagnostic] = []
    accepted_docs: list[AcceptedDocument] = []
    accepted_error_paths: set[str] = set()
    accepted_seen_urls: dict[str, list[str]] = defaultdict(list)
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
        )

    accepted_urls, accepted_index_diags = accepted_url_index(repo_root, rules=rules)
    diagnostics.extend(accepted_index_diags)
    layout = get_staging_layout(repo_root)

    if layout.root.exists():
        for path in sorted(layout.root.iterdir()):
            if path.name.startswith("."):
                continue
            if path.is_file() and path.suffix == ".md":
                continue
            diagnostics.append(Diagnostic(level="error", message="staging root only accepts markdown files", path=str(path.relative_to(repo_root)), code="staging_unexpected_file"))

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

    for normalized_url, paths in sorted(accepted_seen_urls.items()):
        if len(paths) >= 2:
            for rel_path in paths:
                diagnostics.append(Diagnostic(level="error", message=f"duplicate canonical_url inside staging: {normalized_url}", path=rel_path, code="staging_accepted_duplicate_canonical_url"))
                accepted_error_paths.add(rel_path)

    return StagingAnalysis(
        diagnostics=diagnostics,
        accepted_docs=accepted_docs,
        accepted_ready=[doc for doc in accepted_docs if str(doc.path.relative_to(repo_root)) not in accepted_error_paths],
    )


def has_staging_candidates(analysis: StagingAnalysis) -> bool:
    return bool(analysis.accepted_docs)


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
