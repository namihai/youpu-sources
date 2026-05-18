#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from tests.flow.cases import HIGH_VALUE_CASE_IDS
from tests.flow.cases import FlowCase
from tests.flow.cases import list_cases
from tests.support import create_repo_skeleton
from youpu.cli.main import main as youpu_main

SOURCE_EXAMPLES_DIR = REPO_ROOT / "tests" / "source-examples"
GENERATED_DIR = REPO_ROOT / "tests" / "flow" / "generated"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and run local flow-test plans."
    )
    parser.add_argument("--list", action="store_true", help="List available flow-test cases.")
    parser.add_argument("--plan", action="store_true", help="Print a JSON execution plan.")
    parser.add_argument("--run", action="store_true", help="Run selected local flow-test cases.")
    parser.add_argument(
        "--high-value-only",
        action="store_true",
        help="Restrict output to the current high-value local cases.",
    )
    parser.add_argument(
        "--case",
        dest="case_ids",
        action="append",
        default=[],
        help="Filter by case id. May be repeated.",
    )
    return parser


def select_case_objects(case_ids: list[str], *, high_value_only: bool) -> list[FlowCase]:
    normalized = {item.strip().upper() for item in case_ids if item.strip()}
    cases = list_cases(high_value_only=high_value_only)
    if normalized:
        cases = [case for case in cases if case.case_id in normalized]
    return cases


def render_list(selected: list[FlowCase]) -> str:
    lines: list[str] = []
    for case in selected:
        lines.append(
            f"{case.case_id}: {case.title} | "
            f"pr={case.expected_pr_check} merge={case.expected_merge_check} "
            f"ingest={case.expected_ingest}"
        )
    return "\n".join(lines)


def build_plan(selected: list[FlowCase]) -> dict[str, object]:
    return {
        "case_count": len(selected),
        "selected_case_ids": [case.case_id for case in selected],
        "high_value_case_ids": list(HIGH_VALUE_CASE_IDS),
        "source_examples_dir": str(SOURCE_EXAMPLES_DIR.relative_to(REPO_ROOT)),
        "results_dir": str(GENERATED_DIR.relative_to(REPO_ROOT)),
        "cases": [asdict(case) for case in selected],
    }


def read_example(name: str) -> str:
    return (SOURCE_EXAMPLES_DIR / name).read_text(encoding="utf-8")


def accepted_fixture(name: str, *, title: str | None = None, canonical_url: str | None = None, summary: str | None = None) -> str:
    content = read_example(name)
    if title is not None:
        content = replace_yaml_scalar(content, "title", title)
    if canonical_url is not None:
        content = replace_yaml_scalar(content, "canonical_url", canonical_url)
    if summary is not None:
        content = replace_yaml_scalar(content, "summary", summary)
    return content


def replace_yaml_scalar(content: str, key: str, value: str) -> str:
    prefix = f"{key}: "
    lines = content.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f'{prefix}"{value}"'
            replaced = True
            break
    if not replaced:
        raise ValueError(f"missing yaml field: {key}")
    return "\n".join(lines) + "\n"


def remove_yaml_field(content: str, key: str) -> str:
    prefix = f"{key}: "
    lines = [line for line in content.splitlines() if not line.startswith(prefix)]
    return "\n".join(lines) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_data_accepted(repo_root: Path, filename: str, content: str) -> None:
    write_text(repo_root / "data" / "accepted" / filename, content)


def write_staging_accepted(repo_root: Path, filename: str, content: str) -> None:
    write_text(repo_root / "staging" / "accepted" / filename, content)


def write_rejected_csv(repo_root: Path, *, rows: list[tuple[str, str, str]], staging: bool) -> None:
    target = (
        repo_root / "staging" / "rejected" / "rows.csv"
        if staging
        else repo_root / "data" / "rejected.csv"
    )
    body = ["url,title,reason"]
    body.extend(",".join(row) for row in rows)
    write_text(target, "\n".join(body) + "\n")


def command_payload(repo_root: Path, command: str) -> tuple[int, dict[str, object]]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = youpu_main(["--format", "json", "--root", str(repo_root), command])
    raw = stdout.getvalue() if stdout.getvalue().strip() else stderr.getvalue()
    payload = json.loads(raw) if raw.strip() else {}
    return exit_code, payload


def codes_from_payload(payload: dict[str, object]) -> list[str]:
    diagnostics = payload.get("diagnostics", [])
    if not isinstance(diagnostics, list):
        return []
    return [
        str(item.get("code"))
        for item in diagnostics
        if isinstance(item, dict) and item.get("code")
    ]


def setup_case(case: FlowCase, repo_root: Path) -> None:
    example_a = "ancient-chinese-ocr-shared-task.md"
    example_b = "chinese-calligraphy-dataset-19-authors.md"
    example_c = "dunhuang-institute-digital-resources.md"

    if case.case_id == "T01":
        return

    if case.case_id == "T02":
        write_data_accepted(
            repo_root,
            "SRC-0001-ocr-shared-task.md",
            accepted_fixture(example_a),
        )
        return

    if case.case_id == "T03":
        write_staging_accepted(
            repo_root,
            "ancient-chinese-ocr-shared-task.md",
            accepted_fixture(example_a),
        )
        return

    if case.case_id == "T04":
        write_rejected_csv(
            repo_root,
            staging=True,
            rows=[("https://example.com/rejected-one", "Rejected One", "not fit")],
        )
        return

    if case.case_id == "T05":
        write_data_accepted(
            repo_root,
            "SRC-0001-ocr-shared-task.md",
            accepted_fixture(example_a),
        )
        write_staging_accepted(
            repo_root,
            "chinese-calligraphy-dataset-19-authors.md",
            accepted_fixture(example_b),
        )
        write_rejected_csv(
            repo_root,
            staging=True,
            rows=[("https://example.com/rejected-two", "Rejected Two", "out of scope")],
        )
        return

    if case.case_id == "T06":
        content = accepted_fixture(example_a)
        write_data_accepted(repo_root, "SRC-0001-ocr-shared-task.md", content)
        write_staging_accepted(repo_root, "ancient-chinese-ocr-shared-task.md", content)
        return

    if case.case_id == "T07":
        staging_content = accepted_fixture(example_a)
        write_staging_accepted(repo_root, "ancient-chinese-ocr-shared-task.md", staging_content)
        write_rejected_csv(
            repo_root,
            staging=False,
            rows=[("https://evahan.nlpeer.com", "Rejected OCR", "already rejected")],
        )
        return

    if case.case_id == "T08":
        row = ("https://example.com/rejected-dupe", "Rejected Dupe", "duplicate")
        write_rejected_csv(repo_root, staging=False, rows=[row])
        write_rejected_csv(repo_root, staging=True, rows=[row])
        return

    if case.case_id == "T09":
        write_data_accepted(
            repo_root,
            "SRC-0001-ocr-shared-task.md",
            accepted_fixture(example_a),
        )
        write_rejected_csv(
            repo_root,
            staging=True,
            rows=[("https://evahan.nlpeer.com", "Rejected OCR", "conflict with accepted")],
        )
        return

    if case.case_id == "T10":
        first = accepted_fixture(example_a)
        second = accepted_fixture(example_b, canonical_url="https://evahan.nlpeer.com")
        write_staging_accepted(repo_root, "ancient-chinese-ocr-shared-task.md", first)
        write_staging_accepted(repo_root, "duplicate-url.md", second)
        return

    if case.case_id == "T11":
        write_rejected_csv(
            repo_root,
            staging=True,
            rows=[
                ("https://example.com/rejected-dup", "Rejected Dup A", "duplicate"),
                ("https://example.com/rejected-dup", "Rejected Dup B", "duplicate"),
            ],
        )
        return

    if case.case_id == "T12":
        write_text(repo_root / "staging" / "tmp.txt", "unexpected\n")
        return

    if case.case_id == "T13":
        write_staging_accepted(
            repo_root,
            "敦煌壁画数据集.md",
            accepted_fixture(example_a),
        )
        return

    if case.case_id == "T14":
        invalid = accepted_fixture(example_a, canonical_url="not-a-url")
        write_staging_accepted(repo_root, "ancient-chinese-ocr-shared-task.md", invalid)
        return

    if case.case_id == "T15":
        write_text(
            repo_root / "staging" / "rejected" / "rows.csv",
            "bad,header\nhttps://example.com/rejected-three,Rejected Three\n",
        )
        return

    if case.case_id == "T16":
        invalid = remove_yaml_field(accepted_fixture(example_a), "summary")
        write_data_accepted(repo_root, "SRC-0001-invalid.md", invalid)
        return

    if case.case_id == "T17":
        write_rejected_csv(
            repo_root,
            staging=False,
            rows=[
                ("https://example.com/rejected-dupe", "Rejected A", "duplicate"),
                ("https://example.com/rejected-dupe", "Rejected B", "duplicate"),
            ],
        )
        return

    if case.case_id == "T18":
        accepted = accepted_fixture(example_a)
        write_data_accepted(repo_root, "SRC-0001-ocr-shared-task.md", accepted)
        write_rejected_csv(
            repo_root,
            staging=False,
            rows=[("https://evahan.nlpeer.com", "Same URL", "conflict")],
        )
        return

    if case.case_id == "T19":
        write_staging_accepted(
            repo_root,
            "dunhuang-institute-digital-resources.md",
            accepted_fixture(example_c),
        )
        return

    if case.case_id == "T20":
        write_staging_accepted(
            repo_root,
            "dunhuang-institute-digital-resources.md",
            accepted_fixture(example_c),
        )
        write_rejected_csv(
            repo_root,
            staging=True,
            rows=[("https://example.com/rejected-finalize", "Rejected Finalize", "not fit")],
        )
        return

    raise ValueError(f"unsupported case id: {case.case_id}")


def evaluate_case(case: FlowCase, repo_root: Path) -> dict[str, object]:
    check_pr_exit, check_pr_payload = command_payload(repo_root, "check-pr")
    check_merge_exit, check_merge_payload = command_payload(repo_root, "check-merge")

    result: dict[str, object] = {
        "case_id": case.case_id,
        "title": case.title,
        "repo_root": str(repo_root),
        "expected": {
            "pr_check": case.expected_pr_check,
            "merge_check": case.expected_merge_check,
            "ingest": case.expected_ingest,
            "post_ingest_merge": case.expected_post_ingest_merge,
            "codes": list(case.expected_codes),
        },
        "actual": {
            "pr_check_exit_code": check_pr_exit,
            "pr_check_ok": bool(check_pr_payload.get("ok")),
            "pr_check_codes": codes_from_payload(check_pr_payload),
            "merge_check_exit_code": check_merge_exit,
            "merge_check_ok": bool(check_merge_payload.get("ok")),
            "merge_check_codes": codes_from_payload(check_merge_payload),
        },
    }

    if case.expected_ingest != "skip":
        ingest_exit, ingest_payload = command_payload(repo_root, "ingest")
        post_merge_exit, post_merge_payload = command_payload(repo_root, "check-merge")
        result["actual"].update(
            {
                "ingest_exit_code": ingest_exit,
                "ingest_ok": bool(ingest_payload.get("ok")),
                "ingest_codes": codes_from_payload(ingest_payload),
                "post_ingest_merge_exit_code": post_merge_exit,
                "post_ingest_merge_ok": bool(post_merge_payload.get("ok")),
                "post_ingest_merge_codes": codes_from_payload(post_merge_payload),
            }
        )
    else:
        result["actual"].update(
            {
                "ingest_exit_code": None,
                "ingest_ok": None,
                "ingest_codes": [],
                "post_ingest_merge_exit_code": None,
                "post_ingest_merge_ok": None,
                "post_ingest_merge_codes": [],
            }
        )

    result["passed"] = case_passed(case, result["actual"])
    return result


def case_passed(case: FlowCase, actual: dict[str, object]) -> bool:
    expected_pr_ok = case.expected_pr_check == "pass"
    expected_merge_ok = case.expected_merge_check == "pass"
    expected_ingest_ok = case.expected_ingest == "pass"
    expected_post_ingest_merge_ok = case.expected_post_ingest_merge == "pass"

    if bool(actual["pr_check_ok"]) != expected_pr_ok:
        return False
    if bool(actual["merge_check_ok"]) != expected_merge_ok:
        return False
    if case.expected_ingest != "skip" and bool(actual["ingest_ok"]) != expected_ingest_ok:
        return False
    if case.expected_post_ingest_merge != "skip" and bool(actual["post_ingest_merge_ok"]) != expected_post_ingest_merge_ok:
        return False

    if case.expected_codes:
        combined_codes = (
            set(actual["pr_check_codes"])
            | set(actual["merge_check_codes"])
            | set(actual["ingest_codes"])
            | set(actual["post_ingest_merge_codes"])
        )
        if not set(case.expected_codes).issubset(combined_codes):
            return False

    return True


def results_markdown(results: list[dict[str, object]]) -> str:
    lines = [
        "# Flow Test Results",
        "",
        "| Case | Passed | PR | Merge | Ingest | Post-Ingest Merge | Codes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in results:
        actual = item["actual"]
        codes = sorted(
            set(actual["pr_check_codes"])
            | set(actual["merge_check_codes"])
            | set(actual["ingest_codes"])
            | set(actual["post_ingest_merge_codes"])
        )
        lines.append(
            "| "
            + f"{item['case_id']} | "
            + ("yes" if item["passed"] else "no")
            + f" | {actual['pr_check_ok']} | {actual['merge_check_ok']} | {actual['ingest_ok']} | {actual['post_ingest_merge_ok']} | "
            + ", ".join(codes)
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def run_cases(selected: list[FlowCase]) -> dict[str, object]:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    for case in selected:
        case_root = GENERATED_DIR / case.case_id.lower()
        if case_root.exists():
            shutil.rmtree(case_root)
        create_repo_skeleton(case_root)
        setup_case(case, case_root)
        results.append(evaluate_case(case, case_root))

    summary = {
        "case_count": len(results),
        "passed_count": sum(1 for item in results if item["passed"]),
        "failed_case_ids": [item["case_id"] for item in results if not item["passed"]],
        "results": results,
    }
    (GENERATED_DIR / "results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (GENERATED_DIR / "results.md").write_text(
        results_markdown(results),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.list and not args.plan and not args.run:
        parser.error("one of --list, --plan, or --run is required")

    selected = select_case_objects(args.case_ids, high_value_only=args.high_value_only)
    if args.list:
        print(render_list(selected))
    if args.plan:
        print(json.dumps(build_plan(selected), ensure_ascii=False, indent=2))
    if args.run:
        summary = run_cases(selected)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if not summary["failed_case_ids"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
