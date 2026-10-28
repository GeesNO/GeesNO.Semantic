"""Repository-local S4 AI Context acceptance checks.

This module validates the finite I4 corpus. Its pass/fail strings are test
details, not a D7 result artifact or a public diagnostic contract.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "profiles" / "ai-context" / "conformance" / "v0.1"
SCHEMA_PATH = ROOT / "profiles" / "ai-context" / "schema" / "v0.1" / "ai-context.schema.json"
PROFILE_PATH = ROOT / "profiles" / "ai-context" / "v0.1" / "profile.json"
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
S2_REFERENCE = "../../../../schema/v0.1/geesno-semantic.schema.json"
SOURCE_PATH = CORPUS / "sources" / "source-context.json"

PROFILE_EDITION = {
    "profile_family": "https://geesno.com/profile/ai-context",
    "profile_version": "0.1.0",
}

VALID_FIXTURES = (
    "v01-complete-narrow.json",
    "v02-bounded-partial-truncation.json",
    "v03-bounded-unknown.json",
    "v04-material-context-carried.json",
    "v05-exact-external-reference.json",
    "v06-explicit-omission-partial.json",
    "v07-omission-dependency-continuation.json",
    "v08-projection-continuation.json",
    "v09-material-source.json",
    "v10-material-binding.json",
    "v11-external-reference-closure.json",
    "v12-unknown-extension-carried.json",
)

STRUCTURAL_INVALID_FIXTURES = (
    "i01-wrong-binding.json",
    "i02-unknown-grammar-member.json",
    "i03-missing-projection-group.json",
    "i07-truncation-without-partial.json",
)

SEMANTIC_INVALID_FIXTURES = (
    "i04-missing-namespace-context.json",
    "i05-identity-rewritten.json",
    "i06-reference-retargeted.json",
    "i08-omission-marked-complete.json",
    "i09-unknown-hides-known-partial.json",
    "i10-bound-misreported-as-truncation.json",
    "i11-projection-continuation-for-dependency.json",
    "i12-dependency-continuation-for-projection.json",
    "i13-material-carry-dropped.json",
    "i14-fabricated-reference-sufficiency.json",
    "i15-missing-material-source.json",
    "i16-missing-material-binding.json",
    "i17-locator-promoted-to-identity.json",
    "i18-unresolved-descriptor-reference.json",
    "i19-descriptor-reference-wrong-group.json",
    "i20-duplicate-descriptor-identity.json",
    "i21-reference-availability-inconsistent.json",
    "i22-unknown-extension-altered.json",
)

RECORD_COLLECTIONS = (
    "entities",
    "sources",
    "bindings",
    "assertions",
    "tombstones",
)
DESCRIPTOR_GROUPS = (
    "boundedness",
    "omissions",
    "projection_continuations",
    "dependency_continuations",
    "material_context",
    "reference_availability",
)
TERM_VALUE_MEMBERS = {
    "algorithm",
    "datatype",
    "disposition",
    "kind",
    "method",
    "predicate",
    "property",
    "reason",
    "type",
    "unit",
}
QUALIFIED_TERM = re.compile(r"^[A-Za-z][A-Za-z0-9._-]*:[A-Za-z0-9_][A-Za-z0-9._-]*$")

REQUIREMENT_STATES = {
    "material-context-carry": "carried",
    "material-context-reference": "exact_reference_sufficient",
    "material-context-omission": "omitted",
    "material-context-dependency": "dependency_continuation",
    "source-record-traceability": "carried",
    "binding-record-traceability": "carried",
}

# This expectation is external test context. It is not serialized Projection
# grammar and does not make continuation universally mandatory.
PROJECTION_CONTINUATION_REQUIRED = {
    "i12-dependency-continuation-for-projection.json",
}


@dataclass(frozen=True)
class CorpusRun:
    valid_passed: int
    structural_invalid_rejected: int
    semantic_invalid_rejected: int
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


def structural_errors(artifact: Any) -> list[str]:
    """Return deterministic schema errors for one D6 artifact."""

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


def _walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _requirement_references(artifact: dict[str, Any]) -> Iterable[str]:
    for value in _walk(artifact):
        if isinstance(value, dict) and "requirement_reference" in value:
            reference = value["requirement_reference"]
            if isinstance(reference, str):
                yield reference


def _descriptor_references(artifact: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for value in _walk(artifact):
        if (
            isinstance(value, dict)
            and set(value) == {"descriptor_group", "descriptor_id"}
        ):
            yield value


def _descriptor_index(
    artifact: dict[str, Any],
) -> tuple[dict[tuple[str, str], dict[str, Any]], list[str]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    identities: dict[str, str] = {}
    errors: list[str] = []
    for group in DESCRIPTOR_GROUPS:
        for descriptor in artifact.get(group, []):
            descriptor_id = descriptor.get("descriptor_id")
            if not isinstance(descriptor_id, str):
                continue
            if descriptor_id in identities:
                errors.append(
                    "descriptor_id "
                    f"{descriptor_id!r} is duplicated in {identities[descriptor_id]} and {group}"
                )
            else:
                identities[descriptor_id] = group
            index[(group, descriptor_id)] = descriptor
    return index, errors


def _id_index(document: dict[str, Any]) -> dict[str, tuple[dict[str, Any], str | None, str]]:
    index: dict[str, tuple[dict[str, Any], str | None, str]] = {}

    def visit(value: Any, host_id: str | None, collection: str) -> None:
        if isinstance(value, dict):
            own_id = value.get("id")
            next_host = host_id
            if isinstance(own_id, str):
                index[own_id] = (value, host_id, collection)
                next_host = own_id
            for child in value.values():
                visit(child, next_host, collection)
        elif isinstance(value, list):
            for child in value:
                visit(child, host_id, collection)

    for collection in RECORD_COLLECTIONS:
        for record in document.get(collection, []):
            visit(record, None, collection)
    revision = document.get("revision")
    if isinstance(revision, dict):
        visit(revision, None, "revision")
    return index


def _top_record_index(document: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for collection in RECORD_COLLECTIONS:
        for record in document.get(collection, []):
            record_id = record.get("id")
            if isinstance(record_id, str):
                index[(collection, record_id)] = record
    return index


def _references(value: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], str, str]]:
    found: list[tuple[tuple[str, ...], str, str]] = []
    if isinstance(value, dict):
        if (
            set(value) == {"target", "location"}
            and isinstance(value.get("target"), str)
            and isinstance(value.get("location"), str)
        ):
            found.append((path, value["target"], value["location"]))
        else:
            for key, child in value.items():
                found.extend(_references(child, path + (key,)))
    elif isinstance(value, list):
        for child in value:
            found.extend(_references(child, path + ("[]",)))
    return sorted(found)


def _compact_terms(value: Any, member: str | None = None) -> set[str]:
    terms: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if QUALIFIED_TERM.fullmatch(key):
                terms.add(key)
            terms.update(_compact_terms(child, key))
    elif isinstance(value, list):
        for child in value:
            terms.update(_compact_terms(child, member))
    elif (
        isinstance(value, str)
        and member in TERM_VALUE_MEMBERS
        and QUALIFIED_TERM.fullmatch(value)
    ):
        terms.add(value)
    return terms


def _carried_document(artifact: dict[str, Any]) -> dict[str, Any]:
    carried = dict(artifact.get("carried_content", {}))
    return carried


def _availability_by_target(
    artifact: dict[str, Any], errors: list[str]
) -> dict[str, dict[str, Any]]:
    by_target: dict[str, dict[str, Any]] = {}
    for descriptor in artifact.get("reference_availability", []):
        target = descriptor.get("reference_target")
        if not isinstance(target, str):
            continue
        if target in by_target:
            errors.append(f"reference availability is duplicated for {target}")
        else:
            by_target[target] = descriptor
    return by_target


def _scope_record_ids(artifact: dict[str, Any]) -> set[str] | None:
    scope = artifact.get("projection_scope", {})
    descriptor = scope.get("scope_descriptor")
    if scope.get("scope_kind") != "fixture-record-set" or not isinstance(descriptor, dict):
        return None
    record_ids = descriptor.get("record_ids")
    if not isinstance(record_ids, list) or not all(isinstance(item, str) for item in record_ids):
        return None
    return set(record_ids)


def semantic_errors(
    artifact: dict[str, Any],
    source: dict[str, Any],
    *,
    fixture_name: str = "",
) -> list[str]:
    """Check deterministic D2-D6 invariants used by the finite I4 corpus."""

    errors: list[str] = []
    profile = _load_json(PROFILE_PATH)
    requirement_ids = {
        item["requirement_id"]
        for item in profile.get("requirements", [])
        if isinstance(item, dict) and isinstance(item.get("requirement_id"), str)
    }

    if artifact.get("profile_edition") != PROFILE_EDITION:
        errors.append("Projection does not identify AI Context Profile edition 0.1.0 exactly")
    if artifact.get("source_state", {}).get("semantic_document_id") != source.get("id"):
        errors.append("Projection source_state does not identify its source SemanticDocument")

    for reference in _requirement_references(artifact):
        if reference not in requirement_ids:
            errors.append(f"unresolved same-edition requirement reference {reference!r}")

    descriptor_index, descriptor_errors = _descriptor_index(artifact)
    errors.extend(descriptor_errors)
    for reference in _descriptor_references(artifact):
        key = (reference["descriptor_group"], reference["descriptor_id"])
        if key not in descriptor_index:
            errors.append(
                "unresolved descriptor reference "
                f"{reference['descriptor_group']}:{reference['descriptor_id']}"
            )

    carried = _carried_document(artifact)
    source_top = _top_record_index(source)
    carried_top = _top_record_index(carried)
    source_ids = _id_index(source)
    carried_ids = _id_index(carried)

    for (collection, record_id), record in carried_top.items():
        source_record = source_top.get((collection, record_id))
        if source_record is None:
            errors.append(
                f"carried {collection} identity {record_id!r} is absent from that source category"
            )
            continue
        if record.get("kind") != source_record.get("kind"):
            errors.append(f"carried record kind changed for {record_id}")
        if _references(record) != _references(source_record):
            errors.append(f"carried references were omitted or retargeted for {record_id}")

    locator_values = {
        binding.get("locator", {}).get("value")
        for binding in source.get("bindings", [])
        if isinstance(binding.get("locator"), dict)
        and isinstance(binding["locator"].get("value"), str)
    }
    for record_id in carried_ids:
        if record_id in locator_values and record_id not in source_ids:
            errors.append(f"locator value {record_id!r} was promoted to semantic identity")

    source_namespaces = source.get("namespaces", {})
    projection_namespaces = artifact.get("namespaces", {})
    for term in sorted(_compact_terms(carried)):
        prefix = term.split(":", 1)[0]
        if prefix not in projection_namespaces:
            errors.append(f"compact carried term {term!r} has no Projection namespace mapping")
        elif projection_namespaces[prefix] != source_namespaces.get(prefix):
            errors.append(f"compact carried term {term!r} changes its absolute expansion")

    carried_reference_targets = {target for _, target, _ in _references(carried)}
    availability = _availability_by_target(artifact, errors)
    for target in sorted(carried_reference_targets):
        if target not in availability:
            errors.append(f"missing reference availability for carried target {target}")
    for target, descriptor in availability.items():
        state = descriptor.get("availability_state")
        target_is_carried = target in carried_ids
        if state == "carried" and not target_is_carried:
            errors.append(f"reference availability marks uncarried target {target} as carried")
        if state == "external" and target_is_carried:
            errors.append(f"reference availability marks carried target {target} as external")

    material_states: dict[str, set[str]] = {}
    for descriptor in artifact.get("material_context", []):
        target = descriptor.get("context_target")
        state = descriptor.get("preservation_state")
        requirement = descriptor.get("requirement_reference")
        if isinstance(target, str) and isinstance(state, str):
            material_states.setdefault(target, set()).add(state)
        expected_state = REQUIREMENT_STATES.get(requirement)
        if expected_state is not None and state != expected_state:
            errors.append(
                f"requirement {requirement!r} requires preservation_state {expected_state!r}"
            )

        if state == "carried":
            carried_reference = descriptor.get("carried_record_reference")
            if carried_reference not in carried_ids:
                errors.append(f"material carried record {carried_reference!r} is not carried")
            elif carried_reference not in source_ids:
                errors.append(f"material carried record {carried_reference!r} is absent from source")
            else:
                carried_node, carried_host, carried_collection = carried_ids[carried_reference]
                source_node, source_host, source_collection = source_ids[carried_reference]
                if (
                    carried_node != source_node
                    or carried_host != source_host
                    or carried_collection != source_collection
                ):
                    errors.append(
                        f"material carried record {carried_reference!r} changed body or host scope"
                    )
            if requirement == "source-record-traceability" and (
                carried_reference not in {
                    item.get("id") for item in carried.get("sources", [])
                }
            ):
                errors.append("material Source requirement is not satisfied by a carried Source")
            if requirement == "binding-record-traceability" and (
                carried_reference not in {
                    item.get("id") for item in carried.get("bindings", [])
                }
            ):
                errors.append("material Binding requirement is not satisfied by a carried Binding")

        if state == "exact_reference_sufficient" and isinstance(target, str):
            if target not in carried_reference_targets:
                errors.append(f"exact-reference sufficiency for {target} has no carried exact reference")
            if target in carried_ids:
                errors.append(f"exact-reference sufficiency for {target} is contradicted by carriage")
            if availability.get(target, {}).get("availability_state") not in {
                "external",
                "unassessed",
            }:
                errors.append(f"exact-reference sufficiency for {target} lacks consistent availability")

        if state == "omitted" and isinstance(target, str):
            omission_reference = descriptor.get("omission_reference", {})
            omission = descriptor_index.get(
                (
                    omission_reference.get("descriptor_group", ""),
                    omission_reference.get("descriptor_id", ""),
                )
            )
            if omission is not None and omission.get("omitted_target") != target:
                errors.append(f"omission reference for {target} identifies another target")

        if state == "dependency_continuation" and isinstance(target, str):
            dependency_reference = descriptor.get("dependency_continuation_reference", {})
            dependency = descriptor_index.get(
                (
                    dependency_reference.get("descriptor_group", ""),
                    dependency_reference.get("descriptor_id", ""),
                )
            )
            if dependency is not None and dependency.get("dependency_target") != target:
                errors.append(f"dependency continuation for {target} identifies another target")

    for target, states in material_states.items():
        if len(states) > 1 and states != {"omitted", "dependency_continuation"}:
            errors.append(f"material target {target} has incompatible preservation states")

    completeness = artifact.get("projection_completeness")
    omissions = artifact.get("omissions", [])
    if omissions and completeness != "partial":
        errors.append("known omission inside Projection scope requires partial completeness")
    for omission in omissions:
        omitted_target = omission.get("omitted_target")
        if omitted_target in carried_ids:
            errors.append(f"target {omitted_target} is both omitted and carried")

    scope_ids = _scope_record_ids(artifact)
    carried_top_ids = {record_id for _, record_id in carried_top}
    if scope_ids is not None:
        missing_scope_ids = scope_ids - carried_top_ids
        if completeness == "complete" and missing_scope_ids:
            errors.append("complete fixture Projection is missing declared in-scope records")
        if artifact.get("truncation") is not None and not missing_scope_ids:
            errors.append("truncation is declared although the explicit fixture scope is fully carried")

    for continuation in artifact.get("projection_continuations", []):
        if (
            "source_state_reference" in continuation
            and continuation["source_state_reference"] != artifact.get("source_state")
        ):
            errors.append("Projection continuation changes the root source state")
        if (
            "profile_edition_reference" in continuation
            and continuation["profile_edition_reference"] != artifact.get("profile_edition")
        ):
            errors.append("Projection continuation changes the root Profile edition")

    if (
        fixture_name in PROJECTION_CONTINUATION_REQUIRED
        and not artifact.get("projection_continuations")
    ):
        errors.append("explicit fixture context requires Projection continuation, not dependency continuation")

    return sorted(set(errors))


def corpus_inventory_errors() -> list[str]:
    errors: list[str] = []
    expected = {
        "valid": set(VALID_FIXTURES),
        "invalid": set(STRUCTURAL_INVALID_FIXTURES + SEMANTIC_INVALID_FIXTURES),
        "sources": {SOURCE_PATH.name},
    }
    for directory, names in expected.items():
        actual = {
            path.name
            for path in (CORPUS / directory).glob("*.json")
            if path.is_file()
        }
        if actual != names:
            errors.append(
                f"AI Context {directory} corpus inventory differs: "
                f"expected {sorted(names)}, found {sorted(actual)}"
            )
    return errors


def run_corpus() -> CorpusRun:
    errors = corpus_inventory_errors()
    source = _load_json(SOURCE_PATH)
    valid_passed = 0
    structural_rejected = 0
    semantic_rejected = 0

    for name in VALID_FIXTURES:
        artifact = _load_json(CORPUS / "valid" / name)
        structural = structural_errors(artifact)
        semantic = [] if structural else semantic_errors(
            artifact,
            source,
            fixture_name=name,
        )
        if structural or semantic:
            errors.append(f"valid fixture {name} failed: {structural + semantic}")
        else:
            valid_passed += 1

    for name in STRUCTURAL_INVALID_FIXTURES:
        artifact = _load_json(CORPUS / "invalid" / name)
        if structural_errors(artifact):
            structural_rejected += 1
        else:
            errors.append(f"structural-invalid fixture {name} passed schema validation")

    for name in SEMANTIC_INVALID_FIXTURES:
        artifact = _load_json(CORPUS / "invalid" / name)
        structural = structural_errors(artifact)
        if structural:
            errors.append(f"semantic-invalid fixture {name} failed structurally: {structural}")
            continue
        if semantic_errors(artifact, source, fixture_name=name):
            semantic_rejected += 1
        else:
            errors.append(f"semantic-invalid fixture {name} passed semantic validation")

    return CorpusRun(
        valid_passed=valid_passed,
        structural_invalid_rejected=structural_rejected,
        semantic_invalid_rejected=semantic_rejected,
        errors=tuple(errors),
    )
