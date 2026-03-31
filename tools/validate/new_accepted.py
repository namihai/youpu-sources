#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ACCEPTED_DIR = ROOT / "accepted"
TEMPLATE_PATH = ROOT / "templates" / "accepted.md"
NAME_RE = re.compile(r"^SRC-(\d{4})-[a-z0-9-]+\.md$")


def slugify(text: str) -> str:
    slug = text.strip().lower()
    slug = slug.replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "source"


def next_index() -> int:
    max_index = 0
    if not ACCEPTED_DIR.exists():
        return 1
    for path in ACCEPTED_DIR.glob("*.md"):
        match = NAME_RE.match(path.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 tools/validate/new_accepted.py <slug>")
        return 1

    raw_slug = sys.argv[1]
    slug = slugify(raw_slug)
    number = next_index()
    filename = f"SRC-{number:04d}-{slug}.md"
    target = ACCEPTED_DIR / filename

    if not TEMPLATE_PATH.exists():
        print(f"Template not found: {TEMPLATE_PATH}")
        return 1

    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    content = content.replace("标题", raw_slug, 2)

    ACCEPTED_DIR.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
