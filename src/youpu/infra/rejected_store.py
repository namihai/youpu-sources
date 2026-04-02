from __future__ import annotations

import csv
from pathlib import Path

from youpu.domain.rejected import RejectedCsv
from youpu.domain.rejected import RejectedRow


def parse_rejected_csv(path: str | Path, allow_missing: bool = False) -> RejectedCsv:
    csv_path = Path(path)
    if allow_missing and not csv_path.exists():
        return RejectedCsv(path=csv_path, columns=[], rows=[])

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
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
    return RejectedCsv(path=csv_path, columns=columns, rows=rows)


def write_rejected_csv(csv_path: Path, columns: list[str], rows: list[tuple[str, str, str]]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)
