"""Repository-local Core/Profile/Extension/version integration checks.

These checks compose already-approved validators and frozen fixtures. They do
not define compatibility semantics, Profile behavior, or a normative result
format.
"""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "tools" / "validation"
S2_RUNNER = ROOT / "conformance" / "runner"
for path in (VALIDATION, S2_RUNNER):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ai_context_acceptance as s4_acceptance  # noqa: E402
import ai_context_assessment_corpus as s5_corpus  # noqa: E402
from fixture_runner import SCHEMA_PATH, validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


S2_VALID = ROOT / "conformance" / "valid"
S2_INVALID = ROOT / "conformance" / "invalid"
S4_CORPUS = ROOT / "profiles" / "ai-context" / "conformance" / "v0.1"
S5_CORPUS = (
    ROOT / "profiles" / "ai-context" / "assessment-conformance" / "v0.1"
)


@dataclass(frozen=True)
class BoundaryResult:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class BoundaryRun:
    results: tuple[BoundaryResult, ...]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _result(name: str, passed: bool, detail: str) -> BoundaryResult:
    return BoundaryResult(name=name, passed=passed, detail=detail)


def run_checks() -> BoundaryRun:
    """Exercise approved integration boundaries without modifying artifacts."""

    schema = load_schema(SCHEMA_PATH)
    source = _load_json(s4_acceptance.SOURCE_PATH)
    minimal = _load_json(S2_VALID / "minimal-document.json")
    opaque_extension = _load_json(S2_VALID / "unknown-extension-numbers.json")
    projection = _load_json(S4_CORPUS / "valid" / "v01-complete-narrow.json")
    extension_projection = _load_json(
        S4_CORPUS / "valid" / "v12-unknown-extension-carried.json"
    )
    assessment_result = _load_json(
        S5_CORPUS / "valid" / "v01-minimal-stable-conformant.json"
    )

    minimal_outcome = validate_bytes(
        (S2_VALID / "minimal-document.json").read_bytes(), schema
    )
    extension_outcome = validate_bytes(
        (S2_VALID / "unknown-extension-numbers.json").read_bytes(), schema
    )
    future_outcome = validate_bytes(
        (S2_INVALID / "version-future.json").read_bytes(), schema
    )

    extension_structural = s4_acceptance.structural_errors(extension_projection)
    extension_semantic = (
        []
        if extension_structural
        else s4_acceptance.semantic_errors(
            extension_projection,
            source,
            fixture_name="v12-unknown-extension-carried.json",
        )
    )

    newer_binding = copy.deepcopy(projection)
    newer_binding["binding"]["version"] = "0.1.1"

    newer_profile = copy.deepcopy(projection)
    newer_profile["profile_edition"]["profile_version"] = "0.1.1"
    newer_profile_structural = s4_acceptance.structural_errors(newer_profile)
    newer_profile_semantic = (
        []
        if newer_profile_structural
        else s4_acceptance.semantic_errors(newer_profile, source)
    )

    newer_assessment_binding = copy.deepcopy(assessment_result)
    newer_assessment_binding["binding"]["version"] = "0.1.1"

    results = (
        _result(
            "core-bare-valid",
            minimal_outcome == {"result": "valid"},
            f"S2 outcome={minimal_outcome}",
        ),
        _result(
            "core-not-profile",
            bool(s4_acceptance.structural_errors(minimal)),
            "bare S2 Core document is not a Projection artifact",
        ),
        _result(
            "core-unknown-extension-inert",
            extension_outcome == {"result": "valid"},
            f"S2 outcome={extension_outcome}",
        ),
        _result(
            "s4-extension-preservation",
            not extension_structural and not extension_semantic,
            "frozen unknown-Extension Projection passes S4 acceptance",
        ),
        _result(
            "s2-exact-version-boundary",
            future_outcome.get("result") == "unsupported-version",
            f"future-version outcome={future_outcome}",
        ),
        _result(
            "s4-exact-binding-version",
            bool(s4_acceptance.structural_errors(newer_binding)),
            "newer binding version is not substituted for 0.1.0",
        ),
        _result(
            "s4-exact-profile-edition",
            bool(newer_profile_structural or newer_profile_semantic),
            "newer Profile edition is not substituted for 0.1.0",
        ),
        _result(
            "s5-exact-assessment-binding-version",
            bool(s5_corpus.layer_a_errors(newer_assessment_binding)),
            "newer assessment binding is not substituted for 0.1.0",
        ),
    )
    return BoundaryRun(results=results)
