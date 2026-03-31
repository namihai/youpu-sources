from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit


REQUIRED_ROOT_ENTRIES = (
    "accepted",
    "rejected",
    "docs",
    "templates",
    "cli",
    "README.md",
)

ACCEPTED_NAME_RE = re.compile(r"^SRC-(\d{4})-([a-z0-9-]+)\.md$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
TRACKING_PARAM_PREFIXES = ("utm_",)
TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "dclid",
    "mc_cid",
    "mc_eid",
    "igshid",
}


@dataclass(frozen=True)
class AcceptedDocument:
    path: Path
    index: int | None
    slug: str | None
    heading: str | None
    yaml_fields: dict[str, str]
    body: str


@dataclass(frozen=True)
class RejectedRow:
    row_number: int
    url: str
    title: str
    reason: str


@dataclass(frozen=True)
class RejectedCsv:
    path: Path
    columns: list[str]
    rows: list[RejectedRow]


@dataclass(frozen=True)
class ImportsLayout:
    root: Path
    accepted: Path
    rejected: Path
    reports: Path


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


def parse_accepted_document(path: str | Path) -> AcceptedDocument:
    doc_path = Path(path)
    text = doc_path.read_text(encoding="utf-8")

    name_match = ACCEPTED_NAME_RE.match(doc_path.name)
    index = int(name_match.group(1)) if name_match else None
    slug = name_match.group(2) if name_match else None

    title_match = TITLE_RE.search(text)
    heading = title_match.group(1).strip() if title_match else None

    yaml_match = YAML_BLOCK_RE.search(text)
    yaml_fields = parse_simple_yaml_block(text)
    body = text[yaml_match.end():].lstrip() if yaml_match else ""

    return AcceptedDocument(
        path=doc_path,
        index=index,
        slug=slug,
        heading=heading,
        yaml_fields=yaml_fields,
        body=body,
    )


def parse_rejected_csv(path: str | Path) -> RejectedCsv:
    csv_path = Path(path)

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = list(reader.fieldnames or [])
        rows: list[RejectedRow] = []

        for row_number, row in enumerate(reader, start=2):
            rows.append(
                RejectedRow(
                    row_number=row_number,
                    url=(row.get("url") or "").strip(),
                    title=(row.get("title") or "").strip(),
                    reason=(row.get("reason") or "").strip(),
                )
            )

    return RejectedCsv(
        path=csv_path,
        columns=columns,
        rows=rows,
    )


def normalize_url(url: str) -> str:
    raw = url.strip()
    if not raw:
        raise ValueError("url is empty")

    split = urlsplit(raw)
    if not split.scheme or not split.netloc:
        raise ValueError(f"invalid absolute url: {url}")

    scheme = split.scheme.lower()
    hostname = (split.hostname or "").lower()
    port = split.port

    if port is None:
        netloc = hostname
    elif (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = hostname
    else:
        netloc = f"{hostname}:{port}"

    filtered_query: list[tuple[str, str]] = []
    for key, value in parse_qsl(split.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith(TRACKING_PARAM_PREFIXES):
            continue
        if lowered in TRACKING_PARAMS:
            continue
        if not key:
            continue
        filtered_query.append((key, value))

    query = urlencode(filtered_query, doseq=True)

    return urlunsplit((scheme, netloc, split.path, query, ""))


def is_repo_root(path: Path) -> bool:
    return all((path / entry).exists() for entry in REQUIRED_ROOT_ENTRIES)


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start)
    current = current.resolve()

    for candidate in (current, *current.parents):
        if is_repo_root(candidate):
            return candidate

    raise FileNotFoundError(
        f"Could not find repository root from: {current}"
    )


def resolve_repo_root(root: str | None) -> Path:
    if root:
        candidate = Path(root).resolve()
        if not is_repo_root(candidate):
            raise FileNotFoundError(
                f"Provided --root is not a valid repository root: {candidate}"
            )
        return candidate

    return find_repo_root()


def get_imports_layout(repo_root: Path) -> ImportsLayout:
    imports_root = repo_root / "imports"
    return ImportsLayout(
        root=imports_root,
        accepted=imports_root / "accepted",
        rejected=imports_root / "rejected",
        reports=imports_root / "reports",
    )


def ensure_imports_layout(repo_root: Path) -> ImportsLayout:
    layout = get_imports_layout(repo_root)
    for path in (layout.root, layout.accepted, layout.rejected, layout.reports):
        path.mkdir(parents=True, exist_ok=True)
    return layout
