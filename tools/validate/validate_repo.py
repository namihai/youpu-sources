#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ACCEPTED_DIR = ROOT / "accepted"
REJECTED_CSV = ROOT / "rejected" / "rejected.csv"

ACCEPTED_NAME_RE = re.compile(r"^SRC-\d{4}-[a-z0-9-]+\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

REQUIRED_NONEMPTY_FIELDS = [
    "title",
    "domain",
    "content_type",
    "data_form",
    "data_type",
    "region",
    "source_type",
    "source_org",
    "permissions",
    "tags",
    "use_cases",
]

REGION_PLACEHOLDERS = {
    "不明",
    "待确认",
    "不适用",
    "不明/待确认",
}

DISALLOWED_FIELDS = [
    "id",
    "subtitle",
    "period",
    "update_frequency",
    "created_by",
    "created_at",
    "updated_at",
]

REJECTED_COLUMNS = ["url", "title", "reason"]


def parse_simple_yaml_block(text: str) -> dict[str, str]:
    match = YAML_BLOCK_RE.search(text)
    if not match:
        raise ValueError("missing ```yaml fenced block")

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key_match = KEY_RE.match(line)
        if not key_match:
            continue
        key, value = key_match.groups()
        fields[key] = value.strip()
    return fields


def validate_accepted() -> list[str]:
    errors: list[str] = []
    if not ACCEPTED_DIR.exists():
        errors.append(f"missing directory: {ACCEPTED_DIR}")
        return errors

    for path in sorted(ACCEPTED_DIR.glob("*.md")):
        if not ACCEPTED_NAME_RE.match(path.name):
            errors.append(
                f"{path}: invalid filename, expected SRC-####-slug.md"
            )

        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"{path}: failed to read file: {exc}")
            continue

        try:
            fields = parse_simple_yaml_block(text)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue

        title_match = TITLE_RE.search(text)
        if not title_match:
            errors.append(f"{path}: missing H1 title")
        else:
            heading = title_match.group(1).strip()
            yaml_title = fields.get("title", "").strip()
            if yaml_title and heading != yaml_title:
                errors.append(f"{path}: H1 title does not match YAML `title`")

        for key in REQUIRED_NONEMPTY_FIELDS:
            value = fields.get(key, "").strip()
            if not value:
                errors.append(f"{path}: missing required field `{key}`")

        for key in DISALLOWED_FIELDS:
            if key in fields:
                errors.append(f"{path}: field `{key}` is no longer part of the accepted schema")

        for key in ("tags", "use_cases"):
            value = fields.get(key, "").strip()
            if value and not (value.startswith("[") and value.endswith("]")):
                errors.append(
                    f"{path}: field `{key}` must use inline array syntax like [a, b]"
                )

        region = fields.get("region", "").strip()
        if not region:
            errors.append(f"{path}: missing required field `region`")

    return errors


def validate_rejected() -> list[str]:
    errors: list[str] = []
    if not REJECTED_CSV.exists():
        errors.append(f"missing file: {REJECTED_CSV}")
        return errors

    try:
        with REJECTED_CSV.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != REJECTED_COLUMNS:
                errors.append(
                    f"{REJECTED_CSV}: invalid header, expected {','.join(REJECTED_COLUMNS)}"
                )
                return errors

            seen_urls: dict[str, int] = {}
            for index, row in enumerate(reader, start=2):
                url = (row.get("url") or "").strip()
                title = (row.get("title") or "").strip()
                reason = (row.get("reason") or "").strip()

                if not url:
                    errors.append(f"{REJECTED_CSV}:{index}: missing `url`")
                if not title:
                    errors.append(f"{REJECTED_CSV}:{index}: missing `title`")
                if not reason:
                    errors.append(f"{REJECTED_CSV}:{index}: missing `reason`")

                if url:
                    if url in seen_urls:
                        errors.append(
                            f"{REJECTED_CSV}:{index}: duplicate url, first seen on row {seen_urls[url]}"
                        )
                    else:
                        seen_urls[url] = index
    except Exception as exc:
        errors.append(f"{REJECTED_CSV}: failed to read file: {exc}")

    return errors


def main() -> int:
    errors = []
    errors.extend(validate_accepted())
    errors.extend(validate_rejected())

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
