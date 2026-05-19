from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class FlowCase:
    case_id: str
    title: str
    kind: str
    summary: str
    expected_pr_check: str
    expected_merge_check: str
    expected_ingest: str
    must_finalize: bool
    expected_post_ingest_merge: str = "skip"
    accepted_examples: int = 0
    mutations: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)
    expected_codes: tuple[str, ...] = ()


HIGH_VALUE_CASE_IDS: tuple[str, ...] = (
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T12",
)


CASES: tuple[FlowCase, ...] = (
    FlowCase(
        case_id="T01",
        title="empty-data-empty-staging",
        kind="data-baseline",
        summary="`data` 为空，`staging` 为空。",
        expected_pr_check="pass",
        expected_merge_check="pass",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
    ),
    FlowCase(
        case_id="T02",
        title="nonempty-data-empty-staging",
        kind="data-baseline",
        summary="`data` 非空，`staging` 为空。",
        expected_pr_check="pass",
        expected_merge_check="pass",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=1,
    ),
    FlowCase(
        case_id="T03",
        title="empty-data-valid-staging-accepted",
        kind="staging-happy-path",
        summary="`data` 为空，`staging` 有合法样例。",
        expected_pr_check="pass",
        expected_merge_check="fail",
        expected_ingest="pass",
        expected_post_ingest_merge="pass",
        must_finalize=True,
        accepted_examples=1,
    ),
    FlowCase(
        case_id="T04",
        title="nonempty-data-valid-staging-accepted",
        kind="staging-happy-path",
        summary="`data` 非空，`staging` 有合法样例。",
        expected_pr_check="pass",
        expected_merge_check="fail",
        expected_ingest="pass",
        expected_post_ingest_merge="pass",
        must_finalize=True,
        accepted_examples=2,
    ),
    FlowCase(
        case_id="T05",
        title="staging-accepted-conflicts-with-data-accepted",
        kind="staging-conflict",
        summary="staging accepted 与正式 accepted 冲突。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=1,
        mutations=("duplicate_into_data_accepted",),
        expected_codes=("staging_accepted_conflict_accepted",),
    ),
    FlowCase(
        case_id="T06",
        title="staging-accepted-duplicate-canonical-url",
        kind="staging-invalid",
        summary="staging accepted 内部 canonical_url 重复。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=2,
        mutations=("duplicate_canonical_url_in_staging",),
        expected_codes=("staging_accepted_duplicate_canonical_url",),
    ),
    FlowCase(
        case_id="T07",
        title="staging-unexpected-file",
        kind="staging-invalid",
        summary="staging 中存在不支持的文件。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        mutations=("create_unexpected_staging_file",),
        expected_codes=("staging_unexpected_file",),
    ),
    FlowCase(
        case_id="T08",
        title="staging-accepted-invalid-filename",
        kind="staging-invalid",
        summary="staging accepted 文件名非法，包括中文文件名。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=1,
        mutations=("invalid_staging_accepted_filename",),
        expected_codes=("staging_accepted_invalid_filename",),
    ),
    FlowCase(
        case_id="T09",
        title="staging-accepted-invalid-content",
        kind="staging-invalid",
        summary="staging accepted 内容结构非法。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=1,
        mutations=("invalid_staging_accepted_content",),
        expected_codes=("staging_accepted_invalid_canonical_url",),
    ),
    FlowCase(
        case_id="T10",
        title="invalid-data-accepted",
        kind="data-invalid",
        summary="正式 accepted 文件非法。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        accepted_examples=1,
        mutations=("remove_required_summary_field",),
        expected_codes=("accepted_missing_field",),
    ),
    FlowCase(
        case_id="T11",
        title="data-unexpected-file",
        kind="data-invalid",
        summary="正式区存在非 Markdown 文件。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        mutations=("create_data_unexpected_file",),
        expected_codes=("data_unexpected_file",),
    ),
    FlowCase(
        case_id="T12",
        title="staging-unexpected-directory",
        kind="staging-invalid",
        summary="staging 中存在子目录。",
        expected_pr_check="fail",
        expected_merge_check="fail",
        expected_ingest="skip",
        expected_post_ingest_merge="skip",
        must_finalize=False,
        mutations=("create_staging_unexpected_dir",),
        expected_codes=("staging_unexpected_file",),
    ),
    FlowCase(
        case_id="T13",
        title="pending-staging-boundary",
        kind="boundary",
        summary="push 后 pr-check 通过，但 merge-check 因 pending staging 失败。",
        expected_pr_check="pass",
        expected_merge_check="fail",
        expected_ingest="pass",
        expected_post_ingest_merge="pass",
        must_finalize=True,
        accepted_examples=1,
        expected_codes=("merge_pending_staging",),
    ),
    FlowCase(
        case_id="T14",
        title="post-ingest-merge-check-passes",
        kind="boundary",
        summary="ingest 成功后再次 merge-check 通过。",
        expected_pr_check="pass",
        expected_merge_check="fail",
        expected_ingest="pass",
        expected_post_ingest_merge="pass",
        must_finalize=True,
        accepted_examples=1,
    ),
)


def list_cases(*, high_value_only: bool = False) -> list[FlowCase]:
    if not high_value_only:
        return list(CASES)
    return [case for case in CASES if case.case_id in HIGH_VALUE_CASE_IDS]
