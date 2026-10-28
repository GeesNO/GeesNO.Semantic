"""Layer 0: safe, loss-aware JSON parsing for the S2 reference runner."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RawNumber:
    """An accepted JSON number token retained without host-number coercion."""

    token: str


@dataclass(frozen=True, slots=True)
class ResourceLimits:
    max_bytes: int = 16 * 1024 * 1024
    max_depth: int = 128
    max_container_items: int = 100_000
    max_string_chars: int = 1_000_000
    max_number_chars: int = 100_000


class RawInputError(ValueError):
    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category


class ResourceRefusal(RuntimeError):
    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category


def _raw_number(token: str, limits: ResourceLimits) -> RawNumber:
    if len(token) > limits.max_number_chars:
        raise ResourceRefusal("numeric-token-limit", "JSON number token exceeds the configured limit")
    return RawNumber(token)


def _reject_constant(token: str) -> None:
    raise RawInputError("json-syntax", f"non-JSON numeric literal {token!r}")


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise RawInputError("duplicate-member", "duplicate decoded object member name")
        result[name] = value
    return result


def _check_scalar_string(value: str) -> None:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise RawInputError("unicode-scalar", "lone or malformed surrogate content")


def _inspect(value: Any, limits: ResourceLimits, depth: int = 0) -> None:
    if depth > limits.max_depth:
        raise ResourceRefusal("nesting-limit", "JSON nesting exceeds the configured limit")
    if isinstance(value, str):
        if len(value) > limits.max_string_chars:
            raise ResourceRefusal("string-limit", "JSON string exceeds the configured limit")
        _check_scalar_string(value)
    elif isinstance(value, RawNumber):
        return
    elif isinstance(value, list):
        if len(value) > limits.max_container_items:
            raise ResourceRefusal("container-limit", "JSON array exceeds the configured limit")
        for item in value:
            _inspect(item, limits, depth + 1)
    elif isinstance(value, dict):
        if len(value) > limits.max_container_items:
            raise ResourceRefusal("container-limit", "JSON object exceeds the configured limit")
        for name, item in value.items():
            _inspect(name, limits, depth + 1)
            _inspect(item, limits, depth + 1)


def parse_bytes(data: bytes, limits: ResourceLimits | None = None) -> dict[str, Any]:
    limits = limits or ResourceLimits()
    if len(data) > limits.max_bytes:
        raise ResourceRefusal("byte-limit", "input exceeds the configured byte limit")
    if data.startswith(b"\xef\xbb\xbf"):
        raise RawInputError("utf8-bom", "UTF-8 BOM is not admitted")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise RawInputError("invalid-utf8", "input is not strict UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_int=lambda token: _raw_number(token, limits),
            parse_float=lambda token: _raw_number(token, limits),
            parse_constant=_reject_constant,
        )
    except ResourceRefusal:
        raise
    except RawInputError:
        raise
    except (json.JSONDecodeError, UnicodeError) as error:
        raise RawInputError("json-syntax", "input is not one complete JSON text") from error
    except RecursionError as error:
        raise ResourceRefusal("nesting-limit", "parser recursion limit reached") from error
    if not isinstance(value, dict):
        raise RawInputError("non-object-root", "SemanticDocument root must be an object")
    _inspect(value, limits)
    return value


def parse_path(path: Path, limits: ResourceLimits | None = None) -> dict[str, Any]:
    return parse_bytes(path.read_bytes(), limits)


def dump_preserving_numbers(value: Any) -> str:
    """Serialize a parsed data model while re-emitting every raw number token."""

    if isinstance(value, RawNumber):
        return value.token
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(dump_preserving_numbers(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{dump_preserving_numbers(name)}:{dump_preserving_numbers(item)}"
            for name, item in value.items()
        ) + "}"
    raise TypeError(f"unsupported parsed JSON node: {type(value).__name__}")
