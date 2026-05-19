from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from uuid import uuid4

from youpu.domain.accepted import AcceptedDocument
from youpu.domain.schema import get_accepted_field_order
from youpu.domain.urls import normalize_url
from youpu.infra.accepted_store import serialize_simple_yaml_mapping
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_staging_layout
from youpu.app.staging import StagingAnalysis
from youpu.app.staging import build_staging_analysis
from youpu.app.staging import has_staging_candidates

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
    next_index = next_accepted_index(repo_root, accepted_dir)
    imported_accepted = 0
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

    try:
        for doc, target in ready_accepted_targets:
            temp_path = _temp_path_for(target)
            temp_path.write_text(serialize_accepted(doc, repo_root), encoding="utf-8")
            temp_paths.append(temp_path)
            replace_pairs.append((temp_path, target))
            delete_targets.append(doc.path)
            imported_accepted += 1

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

    return {"imported_accepted": imported_accepted, "staging_root": "staging"}


def build_summary(analysis: StagingAnalysis, repo_root: Path) -> str:
    layout = get_staging_layout(repo_root)
    return "\n".join([
        "Ingest completed",
        f"staging root: {layout.root.relative_to(repo_root)}",
        f"accepted candidates ready: {len(analysis.accepted_ready)}",
    ])
def next_accepted_index(repo_root: Path, accepted_dir: Path) -> int:
    max_index = 0
    for path in accepted_dir.glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    base_ref = os.environ.get("YOUPU_ACCEPTED_BASE_REF", "").strip()
    if base_ref:
        max_index = max(max_index, max_accepted_index_at_ref(repo_root, base_ref))
    return max_index + 1


def max_accepted_index_at_ref(repo_root: Path, ref: str) -> int:
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "data"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise OSError(f"failed to inspect accepted data at git ref `{ref}`") from exc

    max_index = 0
    for raw_path in result.stdout.splitlines():
        match = ACCEPTED_FILENAME_RE.match(Path(raw_path).name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index


def target_accepted_path(repo_root: Path, doc: AcceptedDocument, index: int) -> Path:
    source_slug = doc.path.stem
    return get_accepted_dir(repo_root) / f"SRC-{index:04d}-{source_slug}.md"


def _temp_path_for(path: Path) -> Path:
    return path.with_name(f".{path.name}.{uuid4().hex}.tmp")


def _backup_path_for(path: Path) -> Path:
    return path.with_name(f".{path.name}.{uuid4().hex}.bak")
