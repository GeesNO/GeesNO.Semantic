"""Exact AI Context Profile 0.1 Projection construction and local inspection.

This non-normative SDK surface materializes caller-selected S2 records. It does
not select, expand, retrieve, resolve, rank, or infer semantic content.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from copy import deepcopy
from types import MappingProxyType
from typing import Any

from tools.validation import ai_context_acceptance as _s4_acceptance
from tools.validation import ai_context_requirement_assessment as _s5_assessment
from tools.validation import ai_context_result_construction as _s5_results

from ._s2 import ResourceLimits, dump_preserving_numbers, parse_bytes
from .assertions import Assertion, assertion_view
from .document import SemanticDocument
from .entities import Concept, Representation, entity_view
from .lifecycle import Revision, Tombstone
from .sources import Binding, Source


AI_CONTEXT_PROJECTION_BINDING = MappingProxyType(
    {
        "family": "https://geesno.com/binding/ai-context-json",
        "version": "0.1.0",
    }
)
AI_CONTEXT_PROFILE_EDITION = MappingProxyType(
    {
        "profile_family": "https://geesno.com/profile/ai-context",
        "profile_version": "0.1.0",
    }
)

ExactAssessmentContext = _s5_assessment.ExactAssessmentContext
MaterialContextFact = _s5_assessment.MaterialContextFact
RequirementAssessment = _s5_assessment.RequirementAssessment
RequirementAssessmentRun = _s5_assessment.RequirementAssessmentRun
DiagnosticInput = _s5_results.DiagnosticInput

_MISSING = object()
_SELECTABLE_COLLECTIONS = (
    "entities",
    "sources",
    "bindings",
    "assertions",
    "tombstones",
)


class Projection(Mapping[str, Any]):
    """A thin live view over one D6 Projection artifact backing mapping."""

    __slots__ = ("_backing_artifact",)

    def __init__(self, backing_artifact: dict[str, Any]) -> None:
        if not isinstance(backing_artifact, dict):
            raise TypeError("backing_artifact must be a parsed JSON object")
        self._backing_artifact = backing_artifact

    @property
    def backing_artifact(self) -> dict[str, Any]:
        """Return this Projection's independent loss-aware backing artifact."""

        return self._backing_artifact

    @property
    def carried_content(self) -> Mapping[str, Any]:
        value = self._backing_artifact.get("carried_content", {})
        if not isinstance(value, dict):
            raise TypeError("carried_content must be a JSON object before inspection")
        return value

    @property
    def namespaces(self) -> Mapping[str, str]:
        value = self._backing_artifact.get("namespaces", {})
        if not isinstance(value, dict):
            raise TypeError("namespaces must be a JSON object before inspection")
        return value.copy()

    @property
    def entities(self) -> tuple[Concept | Representation, ...]:
        return tuple(entity_view(record) for record in self._records("entities"))

    @property
    def sources(self) -> tuple[Source, ...]:
        return tuple(Source(record) for record in self._records("sources"))

    @property
    def bindings(self) -> tuple[Binding, ...]:
        return tuple(Binding(record) for record in self._records("bindings"))

    @property
    def assertions(self) -> tuple[Assertion, ...]:
        return tuple(assertion_view(record) for record in self._records("assertions"))

    @property
    def tombstones(self) -> tuple[Tombstone, ...]:
        return tuple(Tombstone(record) for record in self._records("tombstones"))

    @property
    def revision(self) -> Revision | None:
        record = self.carried_content.get("revision")
        if record is None:
            return None
        if not isinstance(record, dict):
            raise TypeError("carried_content.revision must be a JSON object")
        return Revision(record)

    def get_record(
        self,
        identifier: str,
        *,
        category: str | None = None,
    ) -> Concept | Representation | Source | Binding | Assertion | Tombstone | Revision | None:
        """Return one exactly identified carried record without source fallback."""

        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string")
        categories = (*_SELECTABLE_COLLECTIONS, "revision")
        if category is not None and category not in categories:
            raise ValueError(f"unsupported carried record category: {category!r}")
        selected = (category,) if category is not None else categories
        for candidate in selected:
            if candidate == "revision":
                revision = self.revision
                if revision is not None and revision.identifier == identifier:
                    return revision
                continue
            for record in self._records(candidate):
                if record.get("id") == identifier:
                    return _record_view(candidate, record)
        return None

    def find_assertions(
        self,
        *,
        subject_target: str | None = None,
        kind: str | None = None,
        term: str | None = None,
    ) -> tuple[Assertion, ...]:
        """Filter carried Assertions by exact local token comparisons only."""

        for value, name in (
            (subject_target, "subject_target"),
            (kind, "kind"),
            (term, "term"),
        ):
            if value is not None and not isinstance(value, str):
                raise TypeError(f"{name} must be a string or None")

        matches: list[Assertion] = []
        for assertion in self.assertions:
            record = assertion.backing_record
            subject = record.get("subject")
            if subject_target is not None and (
                not isinstance(subject, dict)
                or subject.get("target") != subject_target
            ):
                continue
            if kind is not None and record.get("kind") != kind:
                continue
            if term is not None and term not in (
                record.get("type"),
                record.get("property"),
                record.get("predicate"),
            ):
                continue
            matches.append(assertion)
        return tuple(matches)

    def _records(self, category: str) -> list[dict[str, Any]]:
        records = self.carried_content.get(category, [])
        if not isinstance(records, list):
            raise TypeError(f"carried_content.{category} must be a JSON array")
        if not all(isinstance(record, dict) for record in records):
            raise TypeError(f"carried_content.{category} records must be JSON objects")
        return records

    def __getitem__(self, key: str) -> Any:
        return self._backing_artifact[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._backing_artifact)

    def __len__(self) -> int:
        return len(self._backing_artifact)


def create_projection(
    source: SemanticDocument,
    *,
    selection_context: Mapping[str, Any],
    projection_scope: Mapping[str, Any],
    projection_completeness: str,
    carried_content_selection: Mapping[str, Sequence[str]],
    reference_availability: Sequence[Mapping[str, Any]],
    source_state_descriptor: Any = _MISSING,
    include_source_scope: bool = False,
    include_revision: bool = False,
    include_history: bool = False,
    namespaces: Mapping[str, str] | None = None,
    projection_artifact_id: str | None = None,
    boundedness: Sequence[Mapping[str, Any]] | None = None,
    truncation: Mapping[str, Any] | None = None,
    omissions: Sequence[Mapping[str, Any]] | None = None,
    projection_continuations: Sequence[Mapping[str, Any]] | None = None,
    dependency_continuations: Sequence[Mapping[str, Any]] | None = None,
    material_context: Sequence[Mapping[str, Any]] | None = None,
    profile_artifact_reference: str | None = None,
    artifact_metadata: Mapping[str, Any] | None = None,
) -> Projection:
    """Copy an explicit caller selection into one exact D6 Projection.

    This builder deliberately makes no validity or conformance claim. It never
    expands related records, creates omissions, probes references, or chooses
    Projection completeness.
    """

    if not isinstance(source, SemanticDocument):
        raise TypeError("source must be a SemanticDocument")
    if not isinstance(selection_context, Mapping):
        raise TypeError("selection_context must be a mapping")
    if not isinstance(projection_scope, Mapping):
        raise TypeError("projection_scope must be a mapping")
    if not isinstance(projection_completeness, str):
        raise TypeError("projection_completeness must be a string")
    if not isinstance(carried_content_selection, Mapping):
        raise TypeError("carried_content_selection must be a mapping")
    if not isinstance(include_source_scope, bool):
        raise TypeError("include_source_scope must be a bool")
    if not isinstance(include_revision, bool):
        raise TypeError("include_revision must be a bool")
    if not isinstance(include_history, bool):
        raise TypeError("include_history must be a bool")

    unknown_categories = sorted(
        set(carried_content_selection) - set(_SELECTABLE_COLLECTIONS)
    )
    if unknown_categories:
        raise ValueError(f"unsupported carried content categories: {unknown_categories}")

    source_tree = source.backing_tree
    source_state: dict[str, Any] = {
        "semantic_document_id": deepcopy(source_tree["id"]),
    }
    if include_source_scope:
        source_state["source_scope"] = deepcopy(source_tree["scope"])

    revision = source.revision
    if revision is not None:
        source_state["semantic_revision_id"] = deepcopy(revision.identifier)
        if source_state_descriptor is not _MISSING:
            source_state["source_state_descriptor"] = deepcopy(
                source_state_descriptor
            )
    elif source_state_descriptor is _MISSING:
        raise ValueError(
            "source_state_descriptor is required when the source has no current Revision"
        )
    else:
        source_state["source_state_descriptor"] = deepcopy(source_state_descriptor)

    carried_content: dict[str, Any] = {}
    for category in _SELECTABLE_COLLECTIONS:
        selected_ids = carried_content_selection.get(category, ())
        if isinstance(selected_ids, (str, bytes)) or not isinstance(
            selected_ids, Sequence
        ):
            raise TypeError(f"{category} selection must be a sequence of IDs")
        if not all(isinstance(identifier, str) for identifier in selected_ids):
            raise TypeError(f"{category} selection IDs must be strings")
        if len(selected_ids) != len(set(selected_ids)):
            raise ValueError(f"{category} selection contains duplicate IDs")
        if not selected_ids:
            continue
        selected = set(selected_ids)
        source_records = source_tree.get(category, [])
        if not isinstance(source_records, list):
            raise TypeError(f"source {category} must be a JSON array")
        available = {
            record.get("id")
            for record in source_records
            if isinstance(record, dict) and isinstance(record.get("id"), str)
        }
        missing = sorted(selected - available)
        if missing:
            raise ValueError(f"unknown source {category} IDs: {missing}")
        carried_content[category] = [
            deepcopy(record)
            for record in source_records
            if isinstance(record, dict) and record.get("id") in selected
        ]

    if include_revision:
        if revision is None:
            raise ValueError("include_revision requires a current source Revision")
        carried_content["revision"] = deepcopy(revision.backing_record)
    if include_history:
        if "history" not in source_tree:
            raise ValueError("include_history requires explicit source history")
        carried_content["history"] = deepcopy(source_tree["history"])

    artifact: dict[str, Any] = {
        "artifact_kind": "projection_artifact",
        "binding": dict(AI_CONTEXT_PROJECTION_BINDING),
        "profile_edition": dict(AI_CONTEXT_PROFILE_EDITION),
        "source_state": source_state,
        "selection_context": deepcopy(dict(selection_context)),
        "projection_scope": deepcopy(dict(projection_scope)),
        "projection_completeness": projection_completeness,
        "carried_content": carried_content,
        "reference_availability": _copy_mapping_sequence(
            reference_availability, "reference_availability"
        ),
    }
    if namespaces is not None:
        if not isinstance(namespaces, Mapping):
            raise TypeError("namespaces must be a mapping")
        source_namespaces = source.namespaces
        for prefix, expansion in namespaces.items():
            if source_namespaces.get(prefix) != expansion:
                raise ValueError(
                    f"namespace {prefix!r} does not match the source declaration"
                )
        artifact["namespaces"] = deepcopy(dict(namespaces))
    if projection_artifact_id is not None:
        artifact["projection_artifact_id"] = projection_artifact_id

    optional_sequences = (
        ("boundedness", boundedness),
        ("omissions", omissions),
        ("projection_continuations", projection_continuations),
        ("dependency_continuations", dependency_continuations),
        ("material_context", material_context),
    )
    for member, value in optional_sequences:
        if value is not None:
            artifact[member] = _copy_mapping_sequence(value, member)
    if truncation is not None:
        artifact["truncation"] = _copy_mapping(truncation, "truncation")
    if profile_artifact_reference is not None:
        artifact["profile_artifact_reference"] = profile_artifact_reference
    if artifact_metadata is not None:
        artifact["artifact_metadata"] = _copy_mapping(
            artifact_metadata, "artifact_metadata"
        )
    return Projection(artifact)


def load_projection_bytes(
    data: bytes,
    *,
    limits: ResourceLimits | None = None,
) -> Projection:
    """Parse one Projection artifact without fetching or claiming conformance."""

    tree = parse_bytes(data, limits)
    if not isinstance(tree, dict):
        raise TypeError("Projection root must be a JSON object")
    return Projection(tree)


def load_projection_text(
    text: str,
    *,
    limits: ResourceLimits | None = None,
) -> Projection:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return load_projection_bytes(text.encode("utf-8"), limits=limits)


def dump_projection_text(projection: Projection) -> str:
    if not isinstance(projection, Projection):
        raise TypeError("projection must be a Projection")
    return dump_preserving_numbers(projection.backing_artifact)


def dump_projection_bytes(projection: Projection) -> bytes:
    return dump_projection_text(projection).encode("utf-8")


def projection_structural_errors(projection: Projection | Mapping[str, Any]) -> list[str]:
    """Delegate D6 structural validation to the frozen S4 implementation."""

    return _s4_acceptance.structural_errors(_projection_mapping(projection))


def projection_semantic_errors(
    projection: Projection | Mapping[str, Any],
    source: SemanticDocument | Mapping[str, Any],
    *,
    fixture_name: str = "",
) -> list[str]:
    """Delegate accepted Projection semantic checks to the S4 implementation."""

    return _s4_acceptance.semantic_errors(
        _projection_mapping(projection),
        _source_mapping(source),
        fixture_name=fixture_name,
    )


def assess_projection(
    projection: Projection | Mapping[str, Any],
    source: SemanticDocument | Mapping[str, Any],
    *,
    context: ExactAssessmentContext = ExactAssessmentContext(),
) -> RequirementAssessmentRun:
    """Delegate exact Profile 0.1.0 assessment to the approved S5 evaluator."""

    return _s5_assessment.assess_exact_profile_0_1(
        _s5_assessment.load_frozen_profile(),
        _projection_mapping(projection),
        _source_mapping(source),
        context,
    )


def construct_projection_result(
    run: RequirementAssessmentRun,
    **explicit_result_inputs: Any,
) -> dict[str, Any]:
    """Delegate D7 aggregation/result construction to the approved S5 helper."""

    return _s5_results.construct_conformance_result(
        run,
        **explicit_result_inputs,
    )


def _record_view(category: str, record: dict[str, Any]) -> Any:
    if category == "entities":
        return entity_view(record)
    if category == "sources":
        return Source(record)
    if category == "bindings":
        return Binding(record)
    if category == "assertions":
        return assertion_view(record)
    if category == "tombstones":
        return Tombstone(record)
    raise ValueError(f"unsupported carried record category: {category!r}")


def _projection_mapping(value: Projection | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, Projection):
        return value.backing_artifact
    if not isinstance(value, Mapping):
        raise TypeError("projection must be a Projection or mapping")
    return value


def _source_mapping(value: SemanticDocument | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, SemanticDocument):
        return value.backing_tree
    if not isinstance(value, Mapping):
        raise TypeError("source must be a SemanticDocument or mapping")
    return value


def _copy_mapping(value: Mapping[str, Any], name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return deepcopy(dict(value))


def _copy_mapping_sequence(
    value: Sequence[Mapping[str, Any]],
    name: str,
) -> list[dict[str, Any]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence of mappings")
    return [_copy_mapping(item, f"{name} item") for item in value]


__all__ = [
    "AI_CONTEXT_PROFILE_EDITION",
    "AI_CONTEXT_PROJECTION_BINDING",
    "DiagnosticInput",
    "ExactAssessmentContext",
    "MaterialContextFact",
    "Projection",
    "RequirementAssessment",
    "RequirementAssessmentRun",
    "assess_projection",
    "construct_projection_result",
    "create_projection",
    "dump_projection_bytes",
    "dump_projection_text",
    "load_projection_bytes",
    "load_projection_text",
    "projection_semantic_errors",
    "projection_structural_errors",
]
