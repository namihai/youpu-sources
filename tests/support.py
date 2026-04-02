from __future__ import annotations

from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def create_repo_skeleton(repo_root: Path) -> Path:
    (repo_root / "data" / "accepted").mkdir(parents=True)
    (repo_root / "staging" / "accepted").mkdir(parents=True)
    (repo_root / "staging" / "rejected").mkdir(parents=True)
    (repo_root / "schemas").mkdir(parents=True)
    (repo_root / "docs").mkdir(parents=True)
    (repo_root / "templates").mkdir(parents=True)
    (repo_root / "cli").mkdir(parents=True)
    (repo_root / "README.md").write_text("# temp repo\n", encoding="utf-8")

    for rel_path in (
        "schemas/accepted.json",
        "schemas/rejected.json",
        "templates/accepted.md",
        "templates/rejected.rows.csv",
    ):
        source = FIXTURE_ROOT / rel_path
        target = repo_root / rel_path
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    return repo_root
