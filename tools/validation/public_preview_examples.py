"""Validate the explicit S7 P5 learning-example inventory with S2 Layers 0-3."""

from __future__ import annotations

import socket
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples" / "cross-domain" / "public-preview"
RUNNER = ROOT / "conformance" / "runner"
if str(RUNNER) not in sys.path:
    sys.path.insert(0, str(RUNNER))

from fixture_runner import SCHEMA_PATH, validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


EXAMPLE_NAMES = (
    "minimal",
    "engineering",
    "tabular",
    "document",
    "software",
    "product",
    "scientific",
)
EXAMPLE_FILES = {"README.md", "example.json"}
README_MARKERS = (
    "NON-NORMATIVE LEARNING EXAMPLE",
    "project-authored, synthetic and",
    "## What This Represents",
    "## What To Notice",
    "## Core Concepts",
    "## Domain Meaning",
    "## Validate",
    "## Boundaries",
    "planned for Public Preview release candidate `0.1.0-preview.1`",
)


def validate_inventory() -> tuple[tuple[str, int], tuple[str, ...]]:
    errors: list[str] = []
    results: list[tuple[str, int]] = []
    if not EXAMPLES.is_dir():
        return (), (f"missing P5 example collection: {EXAMPLES.relative_to(ROOT)}",)
    expected_directories = set(EXAMPLE_NAMES)
    actual_directories = {path.name for path in EXAMPLES.iterdir() if path.is_dir()}
    if actual_directories != expected_directories:
        errors.append(
            "example directories differ from the explicit P5 inventory: "
            f"expected {sorted(expected_directories)}, got {sorted(actual_directories)}"
        )

    schema = load_schema(SCHEMA_PATH)
    with (
        patch.object(socket, "socket", side_effect=AssertionError("network access")),
        patch.object(
            socket,
            "create_connection",
            side_effect=AssertionError("network access"),
        ),
        patch.object(
            socket,
            "getaddrinfo",
            side_effect=AssertionError("name resolution"),
        ),
    ):
        for name in EXAMPLE_NAMES:
            directory = EXAMPLES / name
            if not directory.is_dir():
                errors.append(f"missing example directory: {directory.relative_to(ROOT)}")
                continue
            actual_files = {path.name for path in directory.iterdir() if path.is_file()}
            if actual_files != EXAMPLE_FILES:
                errors.append(
                    f"{directory.relative_to(ROOT)} files differ from the P5 manifest: "
                    f"expected {sorted(EXAMPLE_FILES)}, got {sorted(actual_files)}"
                )
                continue
            readme = (directory / "README.md").read_text(encoding="utf-8")
            for marker in README_MARKERS:
                if marker not in readme:
                    errors.append(f"{name} README is missing marker: {marker}")
            document_path = directory / "example.json"
            outcome = validate_bytes(document_path.read_bytes(), schema)
            if outcome != {"result": "valid"}:
                errors.append(f"{name} failed S2 Layers 0-3: {outcome}")
            results.append((name, document_path.stat().st_size))

    return tuple(results), tuple(errors)


def main() -> int:
    results, errors = validate_inventory()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    for name, size in results:
        print(f"[PASS] {name}: S2 Layers 0-3; {size} bytes")
    print(f"S7 P5 learning examples: PASS ({len(results)} Core documents, offline).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
