from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptedField:
    name: str
    required: bool = True
    is_array: bool = False


ACCEPTED_FIELDS = [
    AcceptedField("title"),
    AcceptedField("subtitle"),
    AcceptedField("canonical_url"),
    AcceptedField("domain"),
    AcceptedField("content_type"),
    AcceptedField("data_form"),
    AcceptedField("data_type"),
    AcceptedField("region"),
    AcceptedField("source_type"),
    AcceptedField("source_org"),
    AcceptedField("permissions"),
    AcceptedField("tags", is_array=True),
    AcceptedField("use_cases", is_array=True),
]


ACCEPTED_FIELD_ORDER = [field.name for field in ACCEPTED_FIELDS]
ACCEPTED_REQUIRED_FIELDS = [field.name for field in ACCEPTED_FIELDS if field.required]
ACCEPTED_ARRAY_FIELDS = [field.name for field in ACCEPTED_FIELDS if field.is_array]
ACCEPTED_ALLOWED_FIELDS = {field.name for field in ACCEPTED_FIELDS}
