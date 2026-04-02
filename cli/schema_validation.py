from __future__ import annotations

import csv
from pathlib import Path

from cli.accepted_schema import get_accepted_field_order
from cli.accepted_schema import get_accepted_template_path
from cli.output import Diagnostic
from cli.rejected_schema import get_rejected_column_names
from cli.rejected_schema import get_rejected_template_path
from cli.repo import parse_simple_yaml_block
from cli.schema_config import SchemaConfigError
from cli.schema_config import get_schema_path


def validate_accepted_schema(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        field_order = get_accepted_field_order(repo_root)
        template_path = get_accepted_template_path(repo_root)
    except SchemaConfigError as exc:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=str(exc),
                path=str(exc.path.relative_to(repo_root)),
                code=exc.code,
            )
        )
        return diagnostics

    if not template_path.exists():
        diagnostics.append(
            Diagnostic(
                level="error",
                message="accepted template file is missing",
                path=str(template_path.relative_to(repo_root)),
                code="accepted_template_missing",
            )
        )
        return diagnostics

    try:
        template_fields = parse_simple_yaml_block(template_path.read_text(encoding="utf-8"))
    except Exception as exc:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=str(exc),
                path=str(template_path.relative_to(repo_root)),
                code="accepted_template_parse_error",
            )
        )
        return diagnostics

    template_order = list(template_fields.keys())
    if template_order != field_order:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="accepted template YAML fields do not match accepted schema order",
                path=str(template_path.relative_to(repo_root)),
                code="accepted_template_field_order_mismatch",
                details={
                    "expected": field_order,
                    "actual": template_order,
                },
            )
        )

    return diagnostics


def validate_rejected_schema(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        column_names = get_rejected_column_names(repo_root)
        template_path = get_rejected_template_path(repo_root)
    except SchemaConfigError as exc:
        diagnostics.append(
            Diagnostic(
                level="error",
                message=str(exc),
                path=str(exc.path.relative_to(repo_root)),
                code=exc.code,
            )
        )
        return diagnostics

    if not template_path.exists():
        diagnostics.append(
            Diagnostic(
                level="error",
                message="rejected template file is missing",
                path=str(template_path.relative_to(repo_root)),
                code="rejected_template_missing",
            )
        )
        return diagnostics

    with template_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="rejected template must include a header row",
                path=str(template_path.relative_to(repo_root)),
                code="rejected_template_missing_header",
            )
        )
        return diagnostics

    header = rows[0]
    if header != column_names:
        diagnostics.append(
            Diagnostic(
                level="error",
                message="rejected template header does not match rejected schema order",
                path=str(template_path.relative_to(repo_root)),
                code="rejected_template_header_mismatch",
                details={
                    "expected": column_names,
                    "actual": header,
                },
            )
        )

    if len(rows) > 1 and len(rows[1]) != len(column_names):
        diagnostics.append(
            Diagnostic(
                level="error",
                message="rejected template example row must match rejected schema column count",
                path=str(template_path.relative_to(repo_root)),
                code="rejected_template_example_mismatch",
            )
        )

    return diagnostics


def validate_schema(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for schema_name in ("accepted", "rejected"):
        schema_path = get_schema_path(repo_root, schema_name)
        if not schema_path.exists():
            diagnostics.append(
                Diagnostic(
                    level="error",
                    message="schema config file is missing",
                    path=str(schema_path.relative_to(repo_root)),
                    code="schema_missing",
                )
            )
    if diagnostics:
        return diagnostics

    diagnostics.extend(validate_accepted_schema(repo_root))
    diagnostics.extend(validate_rejected_schema(repo_root))
    return diagnostics
