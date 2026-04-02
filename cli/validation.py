from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from cli.accepted_schema import ACCEPTED_ALLOWED_FIELDS
from cli.accepted_schema import ACCEPTED_ARRAY_FIELDS
from cli.accepted_schema import ACCEPTED_REQUIRED_FIELDS
from cli.output import Diagnostic
from cli.repo import get_accepted_dir
from cli.repo import get_rejected_csv_path
from cli.repo import normalize_url
from cli.repo import parse_accepted_document
from cli.repo import parse_rejected_csv

REJECTED_COLUMNS = ["url", "title", "reason"]


def validate_accepted(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    accepted_dir = get_accepted_dir(repo_root)

    for path in sorted(accepted_dir.glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception as exc:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message=str(exc),
                    path=str(path.relative_to(repo_root)),
                    code="accepted_parse_error",
                )
            )
            continue

        if doc.index is None or doc.slug is None:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="invalid filename, expected SRC-####-slug.md",
                    path=str(path.relative_to(repo_root)),
                    code="accepted_invalid_filename",
                )
            )

        if not doc.heading:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="missing H1 title",
                    path=str(path.relative_to(repo_root)),
                    code="accepted_missing_h1",
                )
            )
        elif doc.yaml_fields.get("title", "").strip() and doc.heading != doc.yaml_fields.get("title", "").strip():
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="H1 title does not match YAML `title`",
                    path=str(path.relative_to(repo_root)),
                    code="accepted_title_mismatch",
                )
            )

        for key in ACCEPTED_REQUIRED_FIELDS:
            value = doc.yaml_fields.get(key, "").strip()
            if not value:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"missing required field `{key}`",
                        path=str(path.relative_to(repo_root)),
                        code="accepted_missing_field",
                        details={"field": key},
                    )
                )

        for key in sorted(doc.yaml_fields):
            if key not in ACCEPTED_ALLOWED_FIELDS:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"field `{key}` is not part of the accepted schema",
                        path=str(path.relative_to(repo_root)),
                        code="accepted_unknown_field",
                        details={"field": key},
                    )
                )

        for key in ACCEPTED_ARRAY_FIELDS:
            value = doc.yaml_fields.get(key, "").strip()
            if value and not (value.startswith("[") and value.endswith("]")):
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=f"field `{key}` must use inline array syntax like [a, b]",
                        path=str(path.relative_to(repo_root)),
                        code="accepted_invalid_array",
                        details={"field": key},
                    )
                )

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if canonical_url:
            try:
                normalize_url(canonical_url)
            except ValueError as exc:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=str(exc),
                        path=str(path.relative_to(repo_root)),
                        code="accepted_invalid_canonical_url",
                    )
                )

    return diagnostics


def validate_rejected(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    csv_path = get_rejected_csv_path(repo_root)

    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception as exc:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=str(exc),
                path=str(csv_path.relative_to(repo_root)),
                code="rejected_parse_error",
            )
        )
        return diagnostics

    if rejected.columns != REJECTED_COLUMNS:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=f"invalid header, expected {','.join(REJECTED_COLUMNS)}",
                path=str(csv_path.relative_to(repo_root)),
                code="rejected_invalid_header",
            )
        )

    for row in rejected.rows:
        if not row.url:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="missing `url`",
                    path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                    code="rejected_missing_url",
                )
            )
        else:
            try:
                normalize_url(row.url)
            except ValueError as exc:
                diagnostics.append(
                    Diagnostic(
                        level="error",
                        message=str(exc),
                        path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                        code="rejected_invalid_url",
                    )
                )

        if not row.title:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="missing `title`",
                    path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                    code="rejected_missing_title",
                )
            )
        if not row.reason:
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="missing `reason`",
                    path=f"{csv_path.relative_to(repo_root)}:{row.row_number}",
                    code="rejected_missing_reason",
                )
            )

    return diagnostics


def validate_cross(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    accepted_urls: dict[str, list[str]] = defaultdict(list)
    rejected_urls: dict[str, list[int]] = defaultdict(list)

    accepted_dir = get_accepted_dir(repo_root)
    for path in sorted(accepted_dir.glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception:
            continue

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if not canonical_url:
            continue

        try:
            normalized = normalize_url(canonical_url)
        except ValueError:
            continue
        accepted_urls[normalized].append(str(path.relative_to(repo_root)))

    csv_path = get_rejected_csv_path(repo_root)
    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception:
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
                path=", ".join(
                    accepted_paths
                    + [f"{csv_path.relative_to(repo_root)}:{row}" for row in rejected_rows]
                ),
                code="cross_url_conflict",
                details={
                    "url": url,
                    "accepted_paths": accepted_paths,
                    "rejected_rows": rejected_rows,
                },
            )
        )

    return diagnostics


def validate_accepted_duplicates(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_canonical_url: dict[str, list[str]] = defaultdict(list)
    by_title: dict[str, list[str]] = defaultdict(list)

    for path in sorted(get_accepted_dir(repo_root).glob("*.md")):
        try:
            doc = parse_accepted_document(path)
        except Exception:
            continue

        title = doc.yaml_fields.get("title", "").strip()
        if title:
            by_title[title].append(str(path.relative_to(repo_root)))

        canonical_url = doc.yaml_fields.get("canonical_url", "").strip()
        if not canonical_url:
            continue
        try:
            normalized = normalize_url(canonical_url)
        except ValueError:
            continue
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


def validate_rejected_duplicates(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    by_url: dict[str, list[int]] = defaultdict(list)
    csv_path = get_rejected_csv_path(repo_root)

    try:
        rejected = parse_rejected_csv(csv_path)
    except Exception:
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
