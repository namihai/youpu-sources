from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from uuid import uuid4

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.schema import get_accepted_field_order
from youpu.domain.schema import load_schema_rules
from youpu.domain.urls import normalize_url
from youpu.infra.accepted_store import serialize_simple_yaml_mapping
from youpu.infra.rejected_store import parse_rejected_csv
from youpu.infra.rejected_store import write_rejected_csv
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_rejected_csv_path
from youpu.infra.repo_layout import get_staging_layout
from youpu.app.staging import RejectedImportRow
from youpu.app.staging import StagingAnalysis
from youpu.app.staging import build_staging_analysis
from youpu.app.staging import has_staging_candidates

SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")
ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


def build_analysis(repo_root: Path) -> StagingAnalysis:
    return build_staging_analysis(repo_root)


def serialize_accepted(doc: AcceptedDocument, repo_root: Path) -> str:
    normalized_fields = dict(doc.yaml_fields)
    normalized_fields["title"] = doc.yaml_fields.get("title", "").strip() or "标题"
    normalized_fields["canonical_url"] = normalize_url(doc.yaml_fields["canonical_url"].strip())
    yaml_lines = serialize_simple_yaml_mapping(normalized_fields, get_accepted_field_order(repo_root)).splitlines()
    body = doc.body.rstrip()
    parts = ["---", *yaml_lines, "---"]
    if body:
        parts.extend(["", body])
    return "\n".join(parts) + "\n"


def merge_ingest(repo_root: Path, analysis: StagingAnalysis) -> dict[str, int | str]:
    accepted_dir = get_accepted_dir(repo_root)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    next_index = next_accepted_index(accepted_dir)
    imported_accepted = 0
    imported_rejected = 0
    temp_paths: list[Path] = []
    replace_pairs: list[tuple[Path, Path]] = []
    delete_targets: list[Path] = []
    backup_paths: list[tuple[Path, Path]] = []
    applied_targets: list[Path] = []

    ready_accepted_targets: list[tuple[AcceptedDocument, Path]] = []
    for doc in analysis.accepted_ready:
        target = target_accepted_path(repo_root, doc, next_index)
        next_index += 1
        ready_accepted_targets.append((doc, target))

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

    columns = load_schema_rules(repo_root).rejected_column_names
    try:
        for doc, target in ready_accepted_targets:
            temp_path = _temp_path_for(target)
            temp_path.write_text(serialize_accepted(doc, repo_root), encoding="utf-8")
            temp_paths.append(temp_path)
            replace_pairs.append((temp_path, target))
            delete_targets.append(doc.path)
            imported_accepted += 1

        if analysis.rejected_ready:
            temp_path = _temp_path_for(rejected_csv)
            write_rejected_csv(temp_path, columns, existing_rows)
            temp_paths.append(temp_path)
            replace_pairs.append((temp_path, rejected_csv))

        for source_path, rows in rows_by_file.items():
            remaining = [row for row in rows if (row.source_path, row.row_number) not in ready_row_keys]
            if not remaining:
                delete_targets.append(source_path)
                continue
            temp_path = _temp_path_for(source_path)
            write_rejected_csv(temp_path, columns, [(row.url, row.title, row.reason) for row in remaining])
            temp_paths.append(temp_path)
            replace_pairs.append((temp_path, source_path))

        for temp_path, target_path in replace_pairs:
            backup_path = _backup_path_for(target_path)
            if target_path.exists():
                target_path.replace(backup_path)
                backup_paths.append((target_path, backup_path))
            temp_path.replace(target_path)
            applied_targets.append(target_path)

        for path in delete_targets:
            backup_path = _backup_path_for(path)
            if path.exists():
                path.replace(backup_path)
                backup_paths.append((path, backup_path))
                applied_targets.append(path)
    finally:
        if any(path.exists() for path in temp_paths):
            for target_path in reversed(applied_targets):
                if target_path.exists():
                    target_path.unlink()
            for target_path, backup_path in reversed(backup_paths):
                if backup_path.exists():
                    backup_path.replace(target_path)
            for temp_path in temp_paths:
                if temp_path.exists():
                    temp_path.unlink()
        else:
            for _, backup_path in backup_paths:
                if backup_path.exists():
                    backup_path.unlink()

    return {"imported_accepted": imported_accepted, "imported_rejected": imported_rejected, "staging_root": "staging"}


def build_summary(analysis: StagingAnalysis, repo_root: Path) -> str:
    layout = get_staging_layout(repo_root)
    return "\n".join([
        "Ingest completed",
        f"staging root: {layout.root.relative_to(repo_root)}",
        f"accepted candidates ready: {len(analysis.accepted_ready)}",
        f"rejected candidates ready: {len(analysis.rejected_ready)}",
    ])
def slugify(text: str) -> str:
    lowered = text.strip().lower()
    slug = SLUG_CLEAN_RE.sub("-", lowered).strip("-")
    return slug or "imported"


def next_accepted_index(accepted_dir: Path) -> int:
    max_index = 0
    for path in accepted_dir.glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def target_accepted_path(repo_root: Path, doc: AcceptedDocument, index: int) -> Path:
    source_slug = slugify(doc.path.stem)
    return get_accepted_dir(repo_root) / f"SRC-{index:04d}-{source_slug}.md"


def _temp_path_for(path: Path) -> Path:
    return path.with_name(f".{path.name}.{uuid4().hex}.tmp")


def _backup_path_for(path: Path) -> Path:
    return path.with_name(f".{path.name}.{uuid4().hex}.bak")
