"""Repository-local S5 I4 assessment-result corpus checks.

This module validates only the approved serialized result corpus and the
binding-local integrity cases assigned to I4. It is not an evaluator,
aggregation engine, diagnostic engine, public CLI, SDK or runtime contract.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
S2_RUNNER = ROOT / "conformance" / "runner"
if str(S2_RUNNER) not in sys.path:
    sys.path.insert(0, str(S2_RUNNER))

from semantic_validation import SemanticChecker, SemanticValidationError  # noqa: E402


CORPUS = ROOT / "profiles" / "ai-context" / "assessment-conformance" / "v0.1"
INVENTORY_PATH = ROOT / "spec" / "s5-assessment-corpus-inventory.md"
SCHEMA_PATH = (
    ROOT
    / "profiles"
    / "ai-context"
    / "schema"
    / "v0.1"
    / "ai-context-assessment.schema.json"
)
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
S2_REFERENCE = "../../../../schema/v0.1/geesno-semantic.schema.json"

VALID_FIXTURES = (
    "v01-minimal-stable-conformant.json",
    "v02-stable-violation-diagnostic.json",
    "v03-profile-subject-unsupported.json",
    "v04-semantic-document-unavailable.json",
    "v05-not-applicable-neutral.json",
    "v06-package-local-subject.json",
    "v07-coupled-subject.json",
    "v08-stable-profile-artifact-locator.json",
    "v09-package-local-profile-artifact-locator.json",
    "v10-coupled-profile-artifact-locator.json",
    "v11-diagnostic-taxonomy-and-typed-references.json",
    "v12-enumeration-blocked-context-metadata.json",
)

LAYER_A_INVALID_FIXTURES = (
    "i01-wrong-assessment-binding-family.json",
    "i02-wrong-assessment-binding-version.json",
    "i03-wrong-result-artifact-kind.json",
    "i04-missing-required-root-member.json",
    "i05-plural-aggregate-root-members.json",
    "i06-subject-branch-slot-missing.json",
    "i07-requirement-reference-branches-contradict.json",
    "i08-invalid-overall-outcome-token.json",
    "i09-invalid-requirement-outcome-token.json",
    "i10-unknown-diagnostic-code.json",
    "i11-diagnostic-code-category-mismatch.json",
    "i12-invalid-diagnostic-severity.json",
    "i13-malformed-local-reference-token.json",
    "i14-local-reference-without-root-scope.json",
    "i15-locator-requirement-without-profile-artifact-context.json",
    "i16-null-context-value.json",
    "i17-extra-assessment-context-grammar.json",
    "i18-extra-assessor-metadata-grammar.json",
)

TEMPORAL_INVALID_FIXTURES = (
    "i19-invalid-gregorian-assessment-timestamp.json",
)

LAYER_B_INVALID_FIXTURES = (
    "i20-dangling-diagnostic-cross-reference.json",
    "i21-duplicate-requirement-occurrence.json",
    "i22-ambiguous-local-reference-declaration.json",
)


@dataclass(frozen=True)
class CorpusRun:
    valid_passed: int
    layer_a_rejected: int
    temporal_rejected: int
    layer_b_rejected: int
    errors: tuple[str, ...]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    s2_schema = _load_json(S2_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    registry = Registry().with_resource(
        S2_REFERENCE,
        Resource.from_contents(s2_schema),
    )
    return Draft202012Validator(schema, registry=registry)


def layer_a_errors(artifact: Any) -> list[str]:
    """Return deterministic I2 JSON Schema errors."""

    return [
        f"/{'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in sorted(
            _validator().iter_errors(artifact),
            key=lambda item: (
                tuple(str(part) for part in item.absolute_path),
                item.message,
            ),
        )
    ]


def temporal_errors(artifact: Any) -> list[str]:
    """Reuse the accepted S2 Layer 3 Gregorian date-time check."""

    if not isinstance(artifact, dict):
        return []
    metadata = artifact.get("assessor_metadata")
    if not isinstance(metadata, dict):
        return []
    timestamp = metadata.get("assessment_timestamp")
    if not isinstance(timestamp, str):
        return []
    try:
        SemanticChecker({}).check_temporal("date_time", timestamp)
    except SemanticValidationError as error:
        return [str(error)]
    return []


def _local_key(value: Any) -> tuple[str, str] | None:
    if not isinstance(value, dict):
        return None
    scope_ref = value.get("scope_ref")
    local_ref = value.get("local_ref")
    if isinstance(scope_ref, str) and isinstance(local_ref, str):
        return scope_ref, local_ref
    return None


def _walk_local_references(value: Any) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        key = _local_key(value)
        if key is not None and set(value) == {"scope_ref", "local_ref"}:
            yield key
        for child in value.values():
            yield from _walk_local_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_local_references(child)


def layer_b_errors(artifact: Any) -> list[str]:
    """Check only I4-owned binding-local integrity rules from approved I1."""

    if not isinstance(artifact, dict):
        return []

    errors: list[str] = []
    root_scope = artifact.get("reference_scope")
    expected_scope = root_scope.get("scope_ref") if isinstance(root_scope, dict) else None
    for scope_ref, local_ref in _walk_local_references(artifact):
        if isinstance(expected_scope, str) and scope_ref != expected_scope:
            errors.append(
                f"local reference {local_ref!r} uses scope {scope_ref!r}, "
                f"expected {expected_scope!r}"
            )

    result_declarations: dict[tuple[str, str], int] = {}
    diagnostic_declarations: dict[tuple[str, str], int] = {}
    occurrence_keys: dict[tuple[str, str], int] = {}

    requirement_results = artifact.get("requirement_results", [])
    if isinstance(requirement_results, list):
        for result in requirement_results:
            if not isinstance(result, dict):
                continue
            result_key = _local_key(result.get("requirement_result_ref"))
            if result_key is not None:
                result_declarations[result_key] = result_declarations.get(result_key, 0) + 1

            requirement_ref = result.get("requirement_ref")
            if isinstance(requirement_ref, dict):
                strategy = requirement_ref.get("reference_strategy")
                if strategy == "stable_requirement_reference":
                    token = requirement_ref.get("requirement_id")
                elif strategy == "locator_occurrence_reference":
                    token = requirement_ref.get("requirement_locator")
                else:
                    token = None
                if isinstance(strategy, str) and isinstance(token, str):
                    occurrence_key = strategy, token
                    occurrence_keys[occurrence_key] = occurrence_keys.get(occurrence_key, 0) + 1

    diagnostics = artifact.get("diagnostics", [])
    if isinstance(diagnostics, list):
        for diagnostic in diagnostics:
            if not isinstance(diagnostic, dict):
                continue
            diagnostic_key = _local_key(diagnostic.get("diagnostic_ref"))
            if diagnostic_key is not None:
                diagnostic_declarations[diagnostic_key] = (
                    diagnostic_declarations.get(diagnostic_key, 0) + 1
                )

    for key, count in sorted({**result_declarations, **diagnostic_declarations}.items()):
        total = result_declarations.get(key, 0) + diagnostic_declarations.get(key, 0)
        if total > 1:
            errors.append(
                f"local occurrence reference {key[0]}:{key[1]} is declared {total} times"
            )

    for occurrence_key, count in sorted(occurrence_keys.items()):
        if count > 1:
            errors.append(
                "requirement occurrence "
                f"{occurrence_key[0]}:{occurrence_key[1]} is reported {count} times"
            )

    if isinstance(requirement_results, list):
        for result in requirement_results:
            if not isinstance(result, dict):
                continue
            for diagnostic_ref in result.get("diagnostic_refs", []):
                key = _local_key(diagnostic_ref)
                if key is not None and diagnostic_declarations.get(key, 0) != 1:
                    errors.append(
                        f"diagnostic reference {key[0]}:{key[1]} does not resolve exactly once"
                    )

    if isinstance(diagnostics, list):
        for diagnostic in diagnostics:
            if not isinstance(diagnostic, dict):
                continue
            key = _local_key(diagnostic.get("requirement_result_ref"))
            if key is not None and result_declarations.get(key, 0) != 1:
                errors.append(
                    f"requirement-result reference {key[0]}:{key[1]} does not resolve exactly once"
                )
            for related in diagnostic.get("related_refs", []):
                if not isinstance(related, dict):
                    continue
                kind = related.get("related_ref_kind")
                member = {
                    "requirement_result": "requirement_result_ref",
                    "diagnostic": "diagnostic_ref",
                }.get(kind)
                if member is None:
                    continue
                related_key = _local_key(related.get(member))
                declarations = (
                    result_declarations
                    if kind == "requirement_result"
                    else diagnostic_declarations
                )
                if related_key is not None and declarations.get(related_key, 0) != 1:
                    errors.append(
                        f"related {kind} reference "
                        f"{related_key[0]}:{related_key[1]} does not resolve exactly once"
                    )

    return sorted(set(errors))


def corpus_inventory_errors() -> list[str]:
    errors: list[str] = []
    approved_rows = tuple(
        (case_id, stable_name)
        for case_id, stable_name in re.findall(
            r"^\| `([VI][0-9]{2})` \| `([^`]+)` \|",
            INVENTORY_PATH.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
    )
    approved_names = tuple(
        f"{case_id.casefold()}-{stable_name}.json"
        for case_id, stable_name in approved_rows
    )
    implemented_names = (
        VALID_FIXTURES
        + LAYER_A_INVALID_FIXTURES
        + TEMPORAL_INVALID_FIXTURES
        + LAYER_B_INVALID_FIXTURES
    )
    if approved_names != implemented_names:
        errors.append(
            "assessment fixture names do not match approved I3 IDs/stable names: "
            f"expected {approved_names}, implemented {implemented_names}"
        )

    expected = {
        "valid": set(VALID_FIXTURES),
        "invalid": set(
            LAYER_A_INVALID_FIXTURES
            + TEMPORAL_INVALID_FIXTURES
            + LAYER_B_INVALID_FIXTURES
        ),
    }
    for directory, names in expected.items():
        actual = {
            path.name
            for path in (CORPUS / directory).glob("*.json")
            if path.is_file()
        }
        if actual != names:
            errors.append(
                f"assessment {directory} corpus inventory differs: "
                f"expected {sorted(names)}, found {sorted(actual)}"
            )
    return errors


def run_corpus() -> CorpusRun:
    errors = corpus_inventory_errors()
    valid_passed = 0
    layer_a_rejected = 0
    temporal_rejected = 0
    layer_b_rejected = 0

    for name in VALID_FIXTURES:
        artifact = _load_json(CORPUS / "valid" / name)
        validation_errors = layer_a_errors(artifact)
        calendar_errors = [] if validation_errors else temporal_errors(artifact)
        integrity_errors = (
            [] if validation_errors or calendar_errors else layer_b_errors(artifact)
        )
        if validation_errors or calendar_errors or integrity_errors:
            errors.append(
                f"valid fixture {name} failed: "
                f"{validation_errors + calendar_errors + integrity_errors}"
            )
        else:
            valid_passed += 1

    for name in LAYER_A_INVALID_FIXTURES:
        artifact = _load_json(CORPUS / "invalid" / name)
        if layer_a_errors(artifact):
            layer_a_rejected += 1
        else:
            errors.append(f"Layer A invalid fixture {name} passed I2 schema")

    for name in TEMPORAL_INVALID_FIXTURES:
        artifact = _load_json(CORPUS / "invalid" / name)
        structural = layer_a_errors(artifact)
        if structural:
            errors.append(f"temporal fixture {name} failed at Layer A: {structural}")
        elif temporal_errors(artifact):
            temporal_rejected += 1
        else:
            errors.append(f"temporal fixture {name} passed S2 Layer 3")

    for name in LAYER_B_INVALID_FIXTURES:
        artifact = _load_json(CORPUS / "invalid" / name)
        structural = layer_a_errors(artifact)
        calendar = [] if structural else temporal_errors(artifact)
        if structural or calendar:
            errors.append(
                f"Layer B fixture {name} failed earlier: {structural + calendar}"
            )
        elif layer_b_errors(artifact):
            layer_b_rejected += 1
        else:
            errors.append(f"Layer B invalid fixture {name} passed integrity checks")

    return CorpusRun(
        valid_passed=valid_passed,
        layer_a_rejected=layer_a_rejected,
        temporal_rejected=temporal_rejected,
        layer_b_rejected=layer_b_rejected,
        errors=tuple(errors),
    )
