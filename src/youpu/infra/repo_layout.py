from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

STAGING_ACCEPTED_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")


@dataclass(frozen=True)
class StagingLayout:
    root: Path
    accepted_dir: Path
    rejected_dir: Path
    rejected_csv: Path


def get_data_root(repo_root: Path) -> Path:
    return repo_root / "data"


def get_accepted_dir(repo_root: Path) -> Path:
    return get_data_root(repo_root) / "accepted"


def get_rejected_csv_path(repo_root: Path) -> Path:
    return get_data_root(repo_root) / "rejected.csv"


def get_staging_layout(repo_root: Path) -> StagingLayout:
    staging_root = repo_root / "staging"
    rejected_dir = staging_root / "rejected"
    return StagingLayout(
        root=staging_root,
        accepted_dir=staging_root / "accepted",
        rejected_dir=rejected_dir,
        rejected_csv=rejected_dir / "rows.csv",
    )


def get_staging_accepted_paths(repo_root: Path) -> list[Path]:
    accepted_dir = get_staging_layout(repo_root).accepted_dir
    if not accepted_dir.exists():
        return []
    return sorted(path for path in accepted_dir.glob("*.md") if path.is_file())


def validate_staging_accepted_filename(path: str | Path) -> str | None:
    candidate = Path(path)
    name = candidate.name
    if name.startswith("SRC-"):
        return "staging markdown must not use the final `SRC-####-slug.md` naming"
    if not STAGING_ACCEPTED_NAME_RE.match(name):
        return "staging markdown filename must use lowercase letters, digits, and hyphens"
    return None
