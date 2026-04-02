from __future__ import annotations

from pathlib import Path

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.accepted import parse_inline_array
from youpu.domain.diagnostics import Diagnostic
from youpu.domain.schema import SchemaRules
from youpu.domain.urls import normalize_url
from youpu.infra.schema_store import SchemaConfigError


def schema_error_diagnostic(exc: SchemaConfigError, repo_root: Path) -> Diagnostic:
    return Diagnostic(
        level="error",
        message=str(exc),
        path=str(exc.path.relative_to(repo_root)),
        code=exc.code,
    )


def validate_accepted_document(
    doc: AcceptedDocument,
    *,
    rel_path: str,
    rules: SchemaRules,
    code_prefix: str,
) -> tuple[list[Diagnostic], str | None]:
    diagnostics: list[Diagnostic] = []
    normalized_url: str | None = None

    if not doc.heading:
        diagnostics.append(Diagnostic(level="error", message="missing H1 title", path=rel_path, code=f"{code_prefix}_missing_h1"))
    elif doc.yaml_fields.get("title", "").strip() and doc.heading != doc.yaml_fields.get("title", "").strip():
        diagnostics.append(Diagnostic(level="error", message="H1 title does not match YAML `title`", path=rel_path, code=f"{code_prefix}_title_mismatch"))

    for key in rules.accepted_required_fields:
        if not doc.yaml_fields.get(key, "").strip():
            diagnostics.append(Diagnostic(level="error", message=f"missing required field `{key}`", path=rel_path, code=f"{code_prefix}_missing_field", details={"field": key}))

    for key in sorted(doc.yaml_fields):
        if key not in rules.accepted_allowed_fields:
            diagnostics.append(Diagnostic(level="error", message=f"field `{key}` is not part of the accepted schema", path=rel_path, code=f"{code_prefix}_unknown_field", details={"field": key}))

    for key in rules.accepted_array_fields:
        value = doc.yaml_fields.get(key, "").strip()
        if not value:
            continue
        try:
            parse_inline_array(value)
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=f"field `{key}` {exc}",
                    path=rel_path,
                    code=f"{code_prefix}_invalid_array",
                    details={"field": key},
                )
            )

    canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
    if canonical_url:
        try:
            normalized_url = normalize_url(canonical_url)
        except ValueError as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=rel_path, code=f"{code_prefix}_invalid_canonical_url"))

    return diagnostics, normalized_url


def validate_rejected_values(
    *,
    url: str,
    title: str,
    reason: str,
    path: str,
    code_prefix: str,
) -> tuple[list[Diagnostic], str | None]:
    diagnostics: list[Diagnostic] = []
    normalized_url: str | None = None

    if not url:
        diagnostics.append(Diagnostic(level="error", message="missing `url`", path=path, code=f"{code_prefix}_missing_url"))
    else:
        try:
            normalized_url = normalize_url(url)
        except ValueError as exc:
            diagnostics.append(Diagnostic(level="error", message=str(exc), path=path, code=f"{code_prefix}_invalid_url"))

    if not title:
        diagnostics.append(Diagnostic(level="error", message="missing `title`", path=path, code=f"{code_prefix}_missing_title"))
    if not reason:
        diagnostics.append(Diagnostic(level="error", message="missing `reason`", path=path, code=f"{code_prefix}_missing_reason"))

    return diagnostics, normalized_url
