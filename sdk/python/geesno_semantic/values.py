"""Small constructors for the accepted S2 value and descriptor shapes."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any


def string_value(value: str) -> str:
    """Return the native S2 string branch without normalization."""

    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return value


def boolean_value(value: bool) -> bool:
    """Return the native S2 boolean branch without coercion."""

    if not isinstance(value, bool):
        raise TypeError("value must be a boolean")
    return value


def integer_value(value: str, *, source_lexical: str | None = None) -> dict[str, Any]:
    """Construct an exact integer record from caller-supplied lexical fields."""

    record: dict[str, Any] = {"kind": "integer", "value": _string(value, "value")}
    _add_source_lexical(record, source_lexical)
    return record


def decimal_value(
    *,
    coefficient: str,
    exponent: str,
    source_lexical: str | None = None,
) -> dict[str, Any]:
    """Construct an exact decimal tuple without float conversion."""

    record: dict[str, Any] = {
        "kind": "decimal",
        "coefficient": _string(coefficient, "coefficient"),
        "exponent": _string(exponent, "exponent"),
    }
    _add_source_lexical(record, source_lexical)
    return record


def date_value(value: str, *, source_lexical: str | None = None) -> dict[str, Any]:
    """Construct the S2 date branch from an explicit canonical candidate."""

    record: dict[str, Any] = {"kind": "date", "value": _string(value, "value")}
    _add_source_lexical(record, source_lexical)
    return record


def date_time_value(
    value: str,
    *,
    source_lexical: str | None = None,
) -> dict[str, Any]:
    """Construct the S2 date-time branch without timezone inference."""

    record: dict[str, Any] = {
        "kind": "date_time",
        "value": _string(value, "value"),
    }
    _add_source_lexical(record, source_lexical)
    return record


def reference_value(value: Mapping[str, Any]) -> dict[str, Any]:
    """Wrap one explicit reference as the S2 semantic-reference value."""

    return {"kind": "reference", "reference": _mapping(value, "value")}


def quantity_value(*, magnitude: Mapping[str, Any], unit: str) -> dict[str, Any]:
    """Construct a quantity whose magnitude and unit are both explicit."""

    return {
        "kind": "quantity",
        "magnitude": _mapping(magnitude, "magnitude"),
        "unit": _string(unit, "unit"),
    }


def list_value(items: Sequence[Any]) -> dict[str, Any]:
    """Construct an ordered, duplicate-preserving S2 list value."""

    return {"kind": "list", "items": _sequence(items, "items")}


def set_value(items: Sequence[Any]) -> dict[str, Any]:
    """Construct an S2 set value without sorting or deduplicating it."""

    return {"kind": "set", "items": _sequence(items, "items")}


def structured_value(
    *,
    datatype: str,
    members: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct an explicitly typed S2 structured value."""

    return {
        "kind": "structured",
        "datatype": _string(datatype, "datatype"),
        "members": _mapping(members, "members"),
    }


def condition(value: str) -> dict[str, str]:
    """Construct an explicit S2 value-condition candidate."""

    return {"kind": "condition", "value": _string(value, "value")}


def descriptor(*, kind: str, value: Any) -> dict[str, Any]:
    """Construct the qualified descriptor used by Sources and Bindings."""

    return {"kind": _string(kind, "kind"), "value": deepcopy(value)}


def fingerprint(*, algorithm: str, value: str) -> dict[str, str]:
    """Construct one Source fingerprint descriptor without interpreting it."""

    return {
        "algorithm": _string(algorithm, "algorithm"),
        "value": _string(value, "value"),
    }


def _add_source_lexical(record: dict[str, Any], source_lexical: str | None) -> None:
    if source_lexical is not None:
        record["source_lexical"] = _string(source_lexical, "source_lexical")


def _string(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _mapping(value: Mapping[str, Any], name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return deepcopy(dict(value))


def _sequence(value: Sequence[Any], name: str) -> list[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence")
    return deepcopy(list(value))


__all__ = [
    "boolean_value",
    "condition",
    "date_time_value",
    "date_value",
    "decimal_value",
    "descriptor",
    "fingerprint",
    "integer_value",
    "list_value",
    "quantity_value",
    "reference_value",
    "set_value",
    "string_value",
    "structured_value",
]
