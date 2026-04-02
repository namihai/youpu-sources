from __future__ import annotations

from pathlib import Path

REQUIRED_ROOT_ENTRIES = (
    "data",
    "staging",
    "schemas",
    "docs",
    "templates",
    "src",
    "README.md",
)


def is_repo_root(path: Path) -> bool:
    return all((path / entry).exists() for entry in REQUIRED_ROOT_ENTRIES)


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start)
    current = current.resolve()
    for candidate in (current, *current.parents):
        if is_repo_root(candidate):
            return candidate
    raise FileNotFoundError(f"Could not find repository root from: {current}")


def resolve_repo_root(root: str | None) -> Path:
    if root:
        candidate = Path(root).resolve()
        if not is_repo_root(candidate):
            raise FileNotFoundError(f"Provided --root is not a valid repository root: {candidate}")
        return candidate
    return find_repo_root()
