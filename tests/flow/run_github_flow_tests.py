#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tests.flow.cases import FlowCase
from tests.flow.cases import list_cases

GITHUB_CASE_IDS: tuple[str, ...] = (
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T19",
    "T20",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan GitHub flow-test runs without executing them."
    )
    parser.add_argument("--list", action="store_true", help="List GitHub flow-test cases.")
    parser.add_argument("--plan", action="store_true", help="Print a JSON plan for GitHub flow tests.")
    parser.add_argument("--check-auth", action="store_true", help="Check current gh authentication status.")
    parser.add_argument(
        "--issue-template",
        action="store_true",
        help="Print a Markdown issue template for recording a GitHub flow-test round.",
    )
    parser.add_argument(
        "--case",
        dest="case_ids",
        action="append",
        default=[],
        help="Filter by case id. May be repeated.",
    )
    return parser


def github_cases(case_ids: list[str]) -> list[FlowCase]:
    normalized = {item.strip().upper() for item in case_ids if item.strip()}
    selected = [case for case in list_cases() if case.case_id in GITHUB_CASE_IDS]
    if normalized:
        selected = [case for case in selected if case.case_id in normalized]
    return selected


def render_list(selected: list[FlowCase]) -> str:
    return "\n".join(
        f"{case.case_id}: {case.title} | kind={case.kind} finalize={case.must_finalize}"
        for case in selected
    )


def build_plan(selected: list[FlowCase]) -> dict[str, object]:
    return {
        "case_count": len(selected),
        "selected_case_ids": [case.case_id for case in selected],
        "github_case_ids": list(GITHUB_CASE_IDS),
        "repo": "namihai/youpu-sources",
        "branch_prefix": "flowtest/",
        "workflow_expectations": {
            "push": ["check-pr", "check-merge"],
            "comment": ["/finalize"],
        },
        "cases": [asdict(case) for case in selected],
    }


def check_auth() -> dict[str, object]:
    proc = subprocess.run(
        ["gh", "auth", "status"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def issue_template(selected: list[FlowCase]) -> str:
    lines = [
        "# 流程回归测试",
        "",
        "本 issue 用于记录一轮 GitHub 联调测试。",
        "",
        "## 范围",
        "",
        "- 仓库：`namihai/youpu-sources`",
        "- 目标流程：`check-pr` / `check-merge` / `/finalize`",
        "",
        "## 用例清单",
        "",
    ]
    for case in selected:
        lines.append(f"- [ ] {case.case_id} {case.summary}")
    lines.extend(
        [
            "",
            "## 记录字段",
            "",
            "- 分支名：",
            "- PR 链接：",
            "- `pr-check` 结果：",
            "- `check-merge` 结果：",
            "- `/finalize` 结果：",
            "- 关键错误码：",
            "- 是否符合预期：",
            "- 备注：",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not any((args.list, args.plan, args.check_auth, args.issue_template)):
        parser.error("one of --list, --plan, --check-auth, or --issue-template is required")

    selected = github_cases(args.case_ids)
    if args.list:
        print(render_list(selected))
    if args.plan:
        print(json.dumps(build_plan(selected), ensure_ascii=False, indent=2))
    if args.check_auth:
        print(json.dumps(check_auth(), ensure_ascii=False, indent=2))
    if args.issue_template:
        print(issue_template(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
