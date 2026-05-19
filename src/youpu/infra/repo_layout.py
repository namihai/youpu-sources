from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

STAGING_ACCEPTED_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")


@dataclass(frozen=True)
class StagingLayout:
    root: Path


def get_data_root(repo_root: Path) -> Path:
    return repo_root / "data"


def get_accepted_dir(repo_root: Path) -> Path:
    return get_data_root(repo_root)


def get_staging_layout(repo_root: Path) -> StagingLayout:
    staging_root = repo_root / "staging"
    return StagingLayout(
        root=staging_root,
    )


def get_staging_accepted_paths(repo_root: Path) -> list[Path]:
    staging_root = get_staging_layout(repo_root).root
    if not staging_root.exists():
        return []
    return sorted(path for path in staging_root.glob("*.md") if path.is_file())


def validate_staging_accepted_filename(path: str | Path) -> str | None:
    candidate = Path(path)
    name = candidate.name
    if name.startswith("SRC-"):
        return "staging markdown must not use the final `SRC-####-slug.md` naming"
    if not STAGING_ACCEPTED_NAME_RE.match(name):
        return "staging markdown filename must be an English slug using lowercase ASCII letters, digits, and hyphens"
    return None
