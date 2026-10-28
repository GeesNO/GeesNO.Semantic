"""Layered validation orchestration and deterministic fixture execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

if __package__:
    from .raw_parse import RawInputError, ResourceRefusal, parse_bytes
    from .schema_validation import (
        SchemaValidationError,
        load_schema,
        validate as schema_validate,
    )
    from .semantic_validation import (
        SemanticValidationError,
        validate as semantic_validate,
    )
    from .version_dispatch import UnsupportedVersion, dispatch
else:  # Preserve direct script/path-based runner use.
    from raw_parse import RawInputError, ResourceRefusal, parse_bytes
    from schema_validation import (
        SchemaValidationError,
        load_schema,
        validate as schema_validate,
    )
    from semantic_validation import (
        SemanticValidationError,
        validate as semantic_validate,
    )
    from version_dispatch import UnsupportedVersion, dispatch


ROOT = Path(__file__).resolve().parents[2]
CONFORMANCE = ROOT / "conformance"
SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
FIXTURE_SUFFIXES = {".json", ".raw"}


def validate_bytes(data: bytes, schema: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        document = parse_bytes(data)
    except ResourceRefusal as error:
        return {"result": "resource-refusal", "layer": 0, "category": error.category}
    except RawInputError as error:
        return {"result": "invalid", "layer": 0, "category": error.category}

    try:
        dispatch(document)
    except UnsupportedVersion as error:
        return {"result": "unsupported-version", "layer": 1, "category": error.category}
    except ValueError as error:
        return {"result": "invalid", "layer": 1, "category": getattr(error, "category", "version")}

    try:
        schema_validate(document, schema or load_schema(SCHEMA_PATH))
    except SchemaValidationError as error:
        return {"result": "invalid", "layer": 2, "category": error.category}

    try:
        semantic_validate(document)
    except ResourceRefusal as error:
        return {"result": "resource-refusal", "layer": 3, "category": error.category}
    except SemanticValidationError as error:
        return {"result": "invalid", "layer": 3, "category": error.category}
    return {"result": "valid"}


def fixture_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.iterdir() if path.is_file() and path.suffix in FIXTURE_SUFFIXES)


def run_suite() -> tuple[int, int, int, list[str]]:
    schema = load_schema(SCHEMA_PATH)
    fixtures = fixture_files(CONFORMANCE / "valid") + fixture_files(CONFORMANCE / "invalid")
    expected_files = sorted((CONFORMANCE / "expected").glob("*.json"))
    errors: list[str] = []
    seen_expected: set[Path] = set()
    for fixture in fixtures:
        expected_path = CONFORMANCE / "expected" / f"{fixture.stem}.json"
        seen_expected.add(expected_path)
        if not expected_path.is_file():
            errors.append(f"missing expected outcome for {fixture.relative_to(ROOT)}")
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        actual = validate_bytes(fixture.read_bytes(), schema)
        mismatches = {key: (value, actual.get(key)) for key, value in expected.items() if actual.get(key) != value}
        if mismatches:
            errors.append(f"{fixture.relative_to(ROOT)}: expected {expected}, got {actual}")
    for expected_path in expected_files:
        if expected_path not in seen_expected:
            errors.append(f"orphan expected outcome {expected_path.relative_to(ROOT)}")
    valid_count = len(fixture_files(CONFORMANCE / "valid"))
    invalid_count = len(fixture_files(CONFORMANCE / "invalid"))
    return valid_count, invalid_count, len(expected_files), errors
