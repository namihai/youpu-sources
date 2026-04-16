from __future__ import annotations

import csv
from pathlib import Path

from youpu.domain.rejected import RejectedCsv
from youpu.domain.rejected import RejectedRow
from youpu.domain.rejected import RejectedRowStructureIssue


def parse_rejected_csv(path: str | Path, allow_missing: bool = False) -> RejectedCsv:
    csv_path = Path(path)
    if allow_missing and not csv_path.exists():
        return RejectedCsv(path=csv_path, columns=[], rows=[], structural_issues=[])

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            columns = next(reader)
        except StopIteration:
            columns = []
        rows: list[RejectedRow] = []
        structural_issues: list[RejectedRowStructureIssue] = []
        header_positions = {name: index for index, name in enumerate(columns)}
        expected_width = len(columns)

        for row_number, row in enumerate(reader, start=2):
            if len(row) != expected_width:
                structural_issues.append(
                    RejectedRowStructureIssue(
                        row_number=row_number,
                        actual_width=len(row),
                        expected_width=expected_width,
                    )
                )

            def get_value(name: str) -> str:
                index = header_positions.get(name)
                if index is None or index >= len(row):
                    return ""
                return row[index].strip()

            rows.append(
                RejectedRow(
                    row_number=row_number,
                    url=get_value("url"),
                    title=get_value("title"),
                    reason=get_value("reason"),
                )
            )
    return RejectedCsv(path=csv_path, columns=columns, rows=rows, structural_issues=structural_issues)


def write_rejected_csv(csv_path: Path, columns: list[str], rows: list[tuple[str, str, str]]) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)
