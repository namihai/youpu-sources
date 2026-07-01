from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from youpu.app.checks import run_imports_check
from youpu.app.checks import run_repo_check
from youpu.domain.diagnostics import Diagnostic
from youpu.infra.repo_layout import get_accepted_dir
from youpu.infra.repo_layout import get_staging_accepted_paths

ACCEPTED_FILENAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


@dataclass(frozen=True)
class RepositoryReport:
    summary: str
    diagnostics: list[Diagnostic]
    data: dict[str, object]


def latest_accepted_id(repo_root: Path) -> str | None:
    latest = 0
    for path in get_accepted_dir(repo_root).glob("*.md"):
        match = ACCEPTED_FILENAME_RE.match(path.name)
        if match:
            latest = max(latest, int(match.group(1)))
    return None if latest == 0 else f"SRC-{latest:04d}"


def build_repository_report(repo_root: Path) -> RepositoryReport:
    accepted_count = len(list(get_accepted_dir(repo_root).glob("*.md")))
    diagnostics: list[Diagnostic] = []
    latest_id = latest_accepted_id(repo_root)
    pending_accepted = len(get_staging_accepted_paths(repo_root))
    repo_check = run_repo_check(repo_root)
    duplicate_errors = [item for item in repo_check.diagnostics if item.code in {"accepted_duplicate_canonical_url", "accepted_duplicate_title"}]
    imports_check = run_imports_check(repo_root)
    diagnostics.extend(repo_check.diagnostics)
    diagnostics.extend(imports_check.diagnostics)

    summary = "\n".join([
        "Repository summary",
        f"raw accepted files: {accepted_count}",
        f"latest accepted id: {latest_id or 'none'}",
        f"validated repository health: {'passed' if repo_check.ok else 'failed'}",
        f"validated duplicates: {'none' if not duplicate_errors else 'found'}",
        f"staging pending accepted: {pending_accepted}",
        f"staging issues: {len(imports_check.diagnostics)}",
    ])

    return RepositoryReport(
        summary=summary,
        diagnostics=diagnostics,
        data={
            "raw_accepted_files": accepted_count,
            "latest_accepted_id": latest_id,
            "validation_ok": repo_check.ok,
            "duplicates_ok": not duplicate_errors,
            "staging_pending_accepted": pending_accepted,
            "staging_issues": len(imports_check.diagnostics),
            "health_diagnostics": len(diagnostics),
        },
    )
