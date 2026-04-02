from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cli import schema_validation
from cli import validation
from cli.commands import ingest as ingest_command
from cli.output import Diagnostic
from cli.repo import get_staging_accepted_paths
from cli.repo import get_staging_layout


@dataclass(frozen=True)
class SchemaCheck:
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class RepoCheck:
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class ImportsCheck:
    diagnostics: list[Diagnostic]
    accepted_ready: int
    rejected_ready: int
    has_candidates: bool

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class PrCheck:
    diagnostics: list[Diagnostic]
    schema: SchemaCheck
    repo: RepoCheck
    imports: ImportsCheck

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


@dataclass(frozen=True)
class MergeCheck:
    diagnostics: list[Diagnostic]
    schema: SchemaCheck
    repo: RepoCheck
    pending_staging: bool
    staging_issues: int

    @property
    def ok(self) -> bool:
        return not any(diag.level == "error" for diag in self.diagnostics)


def run_schema_check(repo_root: Path) -> SchemaCheck:
    return SchemaCheck(diagnostics=schema_validation.validate_schema(repo_root))


def run_repo_check(repo_root: Path) -> RepoCheck:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(validation.validate_accepted(repo_root))
    diagnostics.extend(validation.validate_accepted_duplicates(repo_root))
    diagnostics.extend(validation.validate_rejected(repo_root))
    diagnostics.extend(validation.validate_rejected_duplicates(repo_root))
    diagnostics.extend(validation.validate_cross(repo_root))
    return RepoCheck(diagnostics=diagnostics)


def run_imports_check(repo_root: Path) -> ImportsCheck:
    analysis = ingest_command.build_analysis(repo_root)
    return ImportsCheck(
        diagnostics=analysis.diagnostics,
        accepted_ready=len(analysis.accepted_ready),
        rejected_ready=len(analysis.rejected_ready),
        has_candidates=ingest_command.has_staging_candidates(analysis),
    )


def run_pr_check(repo_root: Path) -> PrCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root)
    imports = run_imports_check(repo_root)
    diagnostics = [*schema.diagnostics, *repo.diagnostics, *imports.diagnostics]
    if imports.ok and not imports.has_candidates:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="no staging candidates found",
                code="staging_empty",
            )
        )
    return PrCheck(
        diagnostics=diagnostics,
        schema=schema,
        repo=repo,
        imports=imports,
    )


def run_merge_check(repo_root: Path) -> MergeCheck:
    schema = run_schema_check(repo_root)
    repo = run_repo_check(repo_root)
    diagnostics = [*schema.diagnostics, *repo.diagnostics]

    layout = get_staging_layout(repo_root)
    accepted_files = get_staging_accepted_paths(repo_root)
    rejected_files = [layout.rejected_csv] if layout.rejected_csv.exists() else []
    pending_staging = bool(accepted_files or rejected_files)
    if pending_staging:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="staging directory still contains pending files; run `youpu ingest` first",
                path=str(layout.root.relative_to(repo_root)),
                code="merge_pending_staging",
                details={
                    "accepted_files": [str(path.relative_to(repo_root)) for path in accepted_files],
                    "rejected_files": [str(path.relative_to(repo_root)) for path in rejected_files],
                },
            )
        )

    imports = run_imports_check(repo_root)
    diagnostics.extend(imports.diagnostics)
    return MergeCheck(
        diagnostics=diagnostics,
        schema=schema,
        repo=repo,
        pending_staging=pending_staging,
        staging_issues=len(imports.diagnostics),
    )
