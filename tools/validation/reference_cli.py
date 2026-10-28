"""Minimal repository/reference CLI for integrated conformance validation.

The CLI observes and reports existing conformance checks. It is not a public
SDK API and is not a semantic authority, repair tool, or normative artifact
grammar.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, TextIO


ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "tools" / "validation"
S2_RUNNER = ROOT / "conformance" / "runner"
for path in (VALIDATION, S2_RUNNER):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from integrated_conformance import IntegratedRun, run_integrated_suite  # noqa: E402
from fixture_runner import SCHEMA_PATH, validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


def format_run(run: IntegratedRun) -> str:
    lines = []
    for result in run.results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"[{status}] {result.name}: {result.summary}")
    overall = "PASS" if run.passed else "FAIL"
    lines.append(
        f"Integrated conformance suite: {overall} ({len(run.results)} components)."
    )
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run offline GeesNO.Semantic repository conformance checks."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser(
        "validate-repository",
        help="run the deterministic integrated repository suite",
    )
    document = subcommands.add_parser(
        "validate-document",
        help="validate one SemanticDocument through the existing S2 Layers 0-3",
    )
    document.add_argument("path", type=Path, help="SemanticDocument path")
    return parser


def _validate_document(path: Path, output: TextIO) -> int:
    try:
        data = path.read_bytes()
        schema = load_schema(SCHEMA_PATH)
    except (OSError, ValueError) as error:
        print(f"ERROR: cannot read or configure validation for {path}: {error}", file=output)
        return 2

    outcome = validate_bytes(data, schema)
    if outcome["result"] == "valid":
        print(f"SemanticDocument VALID: {path} (S2 Layers 0-3).", file=output)
        return 0

    details = ", ".join(
        f"{key}={outcome[key]}" for key in ("result", "layer", "category")
        if key in outcome
    )
    print(f"SemanticDocument INVALID: {path} ({details}).", file=output)
    return 1


def main(
    argv: list[str] | None = None,
    *,
    runner: Callable[[], IntegratedRun] | None = None,
    output: TextIO | None = None,
) -> int:
    args = _parser().parse_args(argv)
    stream = output or sys.stdout
    if args.command == "validate-document":
        return _validate_document(args.path, stream)

    try:
        run = (runner or run_integrated_suite)()
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=stream)
        return 2

    print(format_run(run), file=stream)
    return 0 if run.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
