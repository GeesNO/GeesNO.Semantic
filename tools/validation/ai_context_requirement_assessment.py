"""Repository-local S5 I5 requirement assessment helpers.

This module evaluates requirement occurrences only. It deliberately does not
aggregate an overall outcome, emit diagnostics, or serialize a D7 result
artifact; those responsibilities remain assigned to S5 I6.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from . import ai_context_acceptance as s4_acceptance
except ImportError:  # Direct repository-script execution.
    import ai_context_acceptance as s4_acceptance


ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = ROOT / "profiles" / "ai-context" / "v0.1" / "profile.json"
S4_CORPUS = ROOT / "profiles" / "ai-context" / "conformance" / "v0.1"
SOURCE_PATH = S4_CORPUS / "sources" / "source-context.json"

PROFILE_EDITION = {
    "profile_family": "https://geesno.com/profile/ai-context",
    "profile_version": "0.1.0",
}

REQUIREMENT_IDS = (
    "projection-baseline",
    "projection-unknown",
    "material-context-carry",
    "material-context-reference",
    "material-context-omission",
    "material-context-dependency",
    "source-record-traceability",
    "binding-record-traceability",
    "external-reference-closure",
)

REQUIREMENT_OUTCOMES = frozenset(
    {"satisfied", "violated", "not_applicable", "unsupported", "unavailable"}
)
REQUIREMENT_MODES = frozenset({"required", "optional", "prohibited"})
SEMANTIC_SCENARIO_IDS = tuple(f"S{index:02d}" for index in range(1, 25))

MATERIAL_POLICY = {
    "material-context-carry": ("carry_required", "carried"),
    "material-context-reference": (
        "exact_reference_sufficient",
        "exact_reference_sufficient",
    ),
    "material-context-omission": ("explicit_omission_required", "omitted"),
    "material-context-dependency": (
        "dependency_continuation_required",
        "dependency_continuation",
    ),
}

RECORD_COLLECTIONS = (
    "entities",
    "sources",
    "bindings",
    "assertions",
    "tombstones",
)


@dataclass(frozen=True)
class MaterialContextFact:
    """One explicit applicability fact, independent of emitted descriptors."""

    condition: str
    context_target: Any


@dataclass(frozen=True)
class ExactAssessmentContext:
    """Explicit, deterministic context used by exact Profile 0.1 assessment."""

    material_context_facts: tuple[MaterialContextFact, ...] = ()
    material_source_ids: tuple[str, ...] = ()
    material_binding_ids: tuple[str, ...] = ()
    projection_scope_deterministic: bool | None = None


@dataclass(frozen=True)
class RequirementAssessment:
    requirement_id: str
    outcome: str

    def __post_init__(self) -> None:
        if self.outcome not in REQUIREMENT_OUTCOMES:
            raise ValueError(f"unsupported requirement outcome: {self.outcome}")


@dataclass(frozen=True)
class RequirementAssessmentRun:
    enumeration_available: bool
    results: tuple[RequirementAssessment, ...]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_frozen_profile() -> dict[str, Any]:
    return load_json(PROFILE_PATH)


def load_source() -> dict[str, Any]:
    return load_json(SOURCE_PATH)


def load_projection(directory: str, name: str) -> dict[str, Any]:
    return load_json(S4_CORPUS / directory / name)


def _is_exact_frozen_profile(profile: Mapping[str, Any]) -> bool:
    frozen = load_frozen_profile()
    candidate_header = dict(profile)
    frozen_header = dict(frozen)
    candidate_requirements = candidate_header.pop("requirements", None)
    frozen_requirements = frozen_header.pop("requirements")
    candidate_header.pop("artifact_metadata", None)
    frozen_header.pop("artifact_metadata", None)
    if candidate_header != frozen_header or not isinstance(
        candidate_requirements, list
    ):
        return False

    def by_id(requirements: Sequence[Any]) -> dict[str, Any]:
        return {
            requirement["requirement_id"]: requirement
            for requirement in requirements
            if isinstance(requirement, dict)
            and isinstance(requirement.get("requirement_id"), str)
        }

    candidate_by_id = by_id(candidate_requirements)
    frozen_by_id = by_id(frozen_requirements)
    return (
        len(candidate_requirements)
        == len(candidate_by_id)
        == len(frozen_requirements)
        and candidate_by_id == frozen_by_id
    )


def outcome_map(run: RequirementAssessmentRun) -> dict[str, str]:
    return {result.requirement_id: result.outcome for result in run.results}


def assess_requirement_mode(
    *,
    mode: str,
    applicable: bool,
    supported: bool = True,
    dependencies_available: bool = True,
    material_present: bool = True,
    condition_satisfied: bool = True,
) -> str:
    """Assess Accepted D5/D7 mode semantics without defining a Profile."""

    if mode not in REQUIREMENT_MODES:
        raise ValueError(f"unsupported requirement mode: {mode}")
    if not applicable:
        return "not_applicable"
    if not supported:
        return "unsupported"
    if not dependencies_available:
        return "unavailable"
    if mode == "prohibited":
        return "violated" if material_present else "satisfied"
    if mode == "optional" and not material_present:
        return "satisfied"
    return "satisfied" if condition_satisfied else "violated"


def resolve_subject_occurrence(
    reference: Mapping[str, Any],
    *,
    stable_artifacts: Mapping[str, Sequence[dict[str, Any]]] | None = None,
    local_occurrences: Mapping[tuple[str, str], Sequence[dict[str, Any]]] | None = None,
) -> dict[str, Any] | None:
    """Resolve one accepted D7 subject strategy without creating identity."""

    strategy = reference.get("reference_strategy")
    occurrences: Sequence[dict[str, Any]] = ()
    if strategy == "stable_artifact_identity":
        artifact_id = reference.get("artifact_id")
        if isinstance(artifact_id, str):
            occurrences = (stable_artifacts or {}).get(artifact_id, ())
    elif strategy == "assessment_local_artifact_reference":
        local = reference.get("local_reference", {})
        key = (local.get("scope_ref"), local.get("local_ref"))
        occurrences = (local_occurrences or {}).get(key, ())
    elif strategy == "coupled_subject":
        local = reference.get("coupled_occurrence_ref", {})
        key = (local.get("scope_ref"), local.get("local_ref"))
        occurrences = (local_occurrences or {}).get(key, ())
    else:
        raise ValueError(f"unsupported subject reference strategy: {strategy}")
    return occurrences[0] if len(occurrences) == 1 else None


def resolve_requirement_occurrence(
    profile: Mapping[str, Any] | None,
    reference: Mapping[str, Any],
    *,
    locator_occurrences: Mapping[str, Sequence[str]] | None = None,
) -> dict[str, Any] | None:
    """Resolve a requirement while keeping an occurrence locator non-identifying."""

    if profile is None:
        return None
    requirements = {
        requirement.get("requirement_id"): requirement
        for requirement in profile.get("requirements", [])
        if isinstance(requirement, dict)
        and isinstance(requirement.get("requirement_id"), str)
    }
    strategy = reference.get("reference_strategy")
    if strategy == "stable_requirement_reference":
        requirement_id = reference.get("requirement_id")
        return requirements.get(requirement_id)
    if strategy == "locator_occurrence_reference":
        locator = reference.get("requirement_locator")
        identities = (locator_occurrences or {}).get(locator, ())
        if len(identities) != 1:
            return None
        return requirements.get(identities[0])
    raise ValueError(f"unsupported requirement reference strategy: {strategy}")


def _walk_references(value: Any) -> set[str]:
    targets: set[str] = set()
    if isinstance(value, dict):
        if (
            set(value) == {"target", "location"}
            and isinstance(value.get("target"), str)
            and isinstance(value.get("location"), str)
        ):
            targets.add(value["target"])
        else:
            for child in value.values():
                targets.update(_walk_references(child))
    elif isinstance(value, list):
        for child in value:
            targets.update(_walk_references(child))
    return targets


def _record_index(document: Mapping[str, Any]) -> dict[str, tuple[Any, str | None, str]]:
    index: dict[str, tuple[Any, str | None, str]] = {}

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
    return index


def _descriptor_index(projection: Mapping[str, Any]) -> dict[tuple[str, str], Any]:
    index: dict[tuple[str, str], Any] = {}
    for group in (
        "boundedness",
        "omissions",
        "projection_continuations",
        "dependency_continuations",
        "material_context",
        "reference_availability",
    ):
        for descriptor in projection.get(group, []):
            descriptor_id = descriptor.get("descriptor_id")
            if isinstance(descriptor_id, str):
                index[(group, descriptor_id)] = descriptor
    return index


def _referenced_descriptor(
    reference: Any,
    group: str,
    index: Mapping[tuple[str, str], Any],
) -> Mapping[str, Any] | None:
    if not isinstance(reference, dict):
        return None
    if reference.get("descriptor_group") != group:
        return None
    descriptor = index.get((group, reference.get("descriptor_id")))
    return descriptor if isinstance(descriptor, dict) else None


def _projection_baseline_outcome(
    projection: Mapping[str, Any],
    source: Mapping[str, Any] | None,
    context: ExactAssessmentContext,
) -> str:
    if source is None:
        return "unavailable"
    if projection.get("source_state", {}).get("semantic_document_id") != source.get("id"):
        return "violated"
    completeness = projection.get("projection_completeness")
    if projection.get("truncation") is not None and completeness != "partial":
        return "violated"
    if projection.get("omissions") and completeness != "partial":
        return "violated"

    scope = projection.get("projection_scope", {})
    descriptor = scope.get("scope_descriptor")
    if context.projection_scope_deterministic is False:
        return "violated"
    if (
        context.projection_scope_deterministic is None
        and scope.get("scope_kind") != "fixture-record-set"
    ):
        return "unsupported"
    if scope.get("scope_kind") == "fixture-record-set" and isinstance(descriptor, dict):
        scope_ids = descriptor.get("record_ids")
        if isinstance(scope_ids, list) and completeness == "complete":
            carried_ids = set(_record_index(projection.get("carried_content", {})))
            if not set(scope_ids).issubset(carried_ids):
                return "violated"
    return "satisfied"


def _projection_unknown_outcome(projection: Mapping[str, Any]) -> str:
    if projection.get("projection_completeness") != "unknown":
        return "satisfied"
    if projection.get("truncation") is not None or projection.get("omissions"):
        return "violated"
    return "satisfied"


def _matching_material_descriptors(
    projection: Mapping[str, Any], requirement_id: str, target: Any
) -> list[Mapping[str, Any]]:
    return [
        descriptor
        for descriptor in projection.get("material_context", [])
        if descriptor.get("requirement_reference") == requirement_id
        and descriptor.get("context_target") == target
    ]


def _material_target_satisfied(
    requirement_id: str,
    target: Any,
    projection: Mapping[str, Any],
    source: Mapping[str, Any] | None,
) -> str:
    if not isinstance(target, str):
        return "unsupported"
    expected_state = MATERIAL_POLICY[requirement_id][1]
    descriptors = _matching_material_descriptors(projection, requirement_id, target)
    if len(descriptors) != 1:
        return "violated"
    descriptor = descriptors[0]
    if descriptor.get("preservation_state") != expected_state:
        return "violated"

    carried = projection.get("carried_content", {})
    carried_index = _record_index(carried)
    descriptor_index = _descriptor_index(projection)

    if expected_state == "carried":
        if source is None:
            return "unavailable"
        reference = descriptor.get("carried_record_reference")
        source_index = _record_index(source)
        if reference != target or reference not in carried_index or reference not in source_index:
            return "violated"
        return "satisfied" if carried_index[reference] == source_index[reference] else "violated"

    if expected_state == "exact_reference_sufficient":
        carried_targets = _walk_references(carried)
        availability = {
            item.get("reference_target"): item.get("availability_state")
            for item in projection.get("reference_availability", [])
        }
        if target not in carried_targets or target in carried_index:
            return "violated"
        return (
            "satisfied"
            if availability.get(target) in {"external", "unassessed"}
            else "violated"
        )

    if expected_state == "omitted":
        omission = _referenced_descriptor(
            descriptor.get("omission_reference"), "omissions", descriptor_index
        )
        if omission is None:
            return "violated"
        if "omitted_target" not in omission:
            return "unsupported"
        if omission.get("omitted_target") != target:
            return "violated"
        if projection.get("projection_completeness") != "partial":
            return "violated"
        return "violated" if target in carried_index else "satisfied"

    continuation = _referenced_descriptor(
        descriptor.get("dependency_continuation_reference"),
        "dependency_continuations",
        descriptor_index,
    )
    if continuation is None or continuation.get("dependency_target") != target:
        return "violated"
    return "satisfied"


def _material_requirement_outcome(
    requirement_id: str,
    projection: Mapping[str, Any],
    source: Mapping[str, Any] | None,
    context: ExactAssessmentContext,
) -> str:
    condition = MATERIAL_POLICY[requirement_id][0]
    targets = tuple(
        fact.context_target
        for fact in context.material_context_facts
        if fact.condition == condition
    )
    if not targets:
        return "not_applicable"
    outcomes = {
        _material_target_satisfied(requirement_id, target, projection, source)
        for target in targets
    }
    if "violated" in outcomes:
        return "violated"
    # A valid disposition outside this bounded assessor remains unsupported;
    # this is an implementation support boundary, not D7 overall aggregation.
    if "unsupported" in outcomes:
        return "unsupported"
    if "unavailable" in outcomes:
        return "unavailable"
    return "satisfied"


def _traceability_outcome(
    requirement_id: str,
    projection: Mapping[str, Any],
    source: Mapping[str, Any] | None,
    context: ExactAssessmentContext,
) -> str:
    if requirement_id == "source-record-traceability":
        targets = context.material_source_ids
        collection = "sources"
    else:
        targets = context.material_binding_ids
        collection = "bindings"
    if not targets:
        return "not_applicable"
    if source is None:
        return "unavailable"

    carried = projection.get("carried_content", {})
    source_records = {
        record.get("id"): record for record in source.get(collection, [])
    }
    carried_records = {
        record.get("id"): record for record in carried.get(collection, [])
    }
    for target in targets:
        descriptors = _matching_material_descriptors(projection, requirement_id, target)
        if len(descriptors) != 1:
            return "violated"
        descriptor = descriptors[0]
        if (
            descriptor.get("preservation_state") != "carried"
            or descriptor.get("carried_record_reference") != target
            or target not in source_records
            or carried_records.get(target) != source_records[target]
        ):
            return "violated"
    return "satisfied"


def _closure_outcome(projection: Mapping[str, Any]) -> str:
    carried = projection.get("carried_content", {})
    carried_index = _record_index(carried)
    targets = _walk_references(carried)
    availability: dict[str, str] = {}
    for descriptor in projection.get("reference_availability", []):
        target = descriptor.get("reference_target")
        state = descriptor.get("availability_state")
        if not isinstance(target, str) or target in availability:
            return "violated"
        availability[target] = state
    if not targets.issubset(availability):
        return "violated"
    for target, state in availability.items():
        if state == "carried" and target not in carried_index:
            return "violated"
        if state == "external" and target in carried_index:
            return "violated"
    return "satisfied"


def _validate_context(context: ExactAssessmentContext) -> None:
    known_conditions = {condition for condition, _ in MATERIAL_POLICY.values()}
    conditions_by_target: dict[str, set[str]] = {}
    for fact in context.material_context_facts:
        if fact.condition not in known_conditions:
            raise ValueError(f"unknown material-context condition: {fact.condition}")
        key = json.dumps(fact.context_target, sort_keys=True, separators=(",", ":"))
        conditions_by_target.setdefault(key, set()).add(fact.condition)

    allowed_pair = {"explicit_omission_required", "dependency_continuation_required"}
    for conditions in conditions_by_target.values():
        if len(conditions) > 1 and conditions != allowed_pair:
            raise ValueError("incompatible material-context applicability facts")


def assess_exact_profile_0_1(
    profile: Mapping[str, Any] | None,
    projection: Mapping[str, Any],
    source: Mapping[str, Any] | None,
    context: ExactAssessmentContext = ExactAssessmentContext(),
) -> RequirementAssessmentRun:
    """Assess the nine frozen requirements without aggregation or diagnostics."""

    if profile is None or not _is_exact_frozen_profile(profile):
        return RequirementAssessmentRun(False, ())
    if projection.get("profile_edition") != PROFILE_EDITION:
        raise ValueError("Projection does not declare exact AI Context Profile 0.1.0")
    structural = s4_acceptance.structural_errors(projection)
    if structural:
        raise ValueError("Projection must pass the frozen D6 structural schema")
    _validate_context(context)

    results: list[RequirementAssessment] = []
    for requirement in load_frozen_profile()["requirements"]:
        requirement_id = requirement["requirement_id"]
        if requirement_id == "projection-baseline":
            outcome = _projection_baseline_outcome(projection, source, context)
        elif requirement_id == "projection-unknown":
            outcome = _projection_unknown_outcome(projection)
        elif requirement_id in MATERIAL_POLICY:
            outcome = _material_requirement_outcome(
                requirement_id, projection, source, context
            )
        elif requirement_id in {
            "source-record-traceability",
            "binding-record-traceability",
        }:
            outcome = _traceability_outcome(
                requirement_id, projection, source, context
            )
        elif requirement_id == "external-reference-closure":
            outcome = _closure_outcome(projection)
        else:  # pragma: no cover - frozen artifact equality makes this unreachable
            outcome = "unsupported"
        results.append(RequirementAssessment(requirement_id, outcome))

    if tuple(result.requirement_id for result in results) != REQUIREMENT_IDS:
        raise ValueError("frozen Profile requirement inventory changed")
    return RequirementAssessmentRun(True, tuple(results))
