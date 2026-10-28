"""S2 reference conformance runner for deterministic Layers 0 through 3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fixture_runner import SCHEMA_PATH, run_suite, validate_bytes
from schema_validation import load_schema


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="optional SemanticDocument files to validate")
    args = parser.parse_args()

    if args.paths:
        schema = load_schema(SCHEMA_PATH)
        status = 0
        for path in args.paths:
            outcome = validate_bytes(path.read_bytes(), schema)
            print(json.dumps({"path": str(path), **outcome}, ensure_ascii=False, sort_keys=True))
            if outcome["result"] != "valid":
                status = 1
        return status

    valid, invalid, expected, errors = run_suite()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    defs_count = len(load_schema(SCHEMA_PATH)["$defs"])
    print(
        "S2 conformance baseline OK: "
        f"Draft 2020-12 schema ({defs_count} $defs); "
        f"{valid} valid, {invalid} invalid, {expected} expected fixtures; "
        "Layers 0-3 matched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
