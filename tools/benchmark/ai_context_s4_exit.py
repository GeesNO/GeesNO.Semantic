"""Repository-internal deterministic S4 AI Context exit benchmark.

This is non-normative milestone tooling tied to one synthetic recipe. It is not
a public Projection API, Profile evaluator or D7 conformance-result producer.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "tools" / "validation"
RUNNER = ROOT / "conformance" / "runner"
sys.path.insert(0, str(VALIDATION))
sys.path.insert(0, str(RUNNER))

import ai_context_acceptance as acceptance  # noqa: E402
from fixture_runner import validate_bytes  # noqa: E402
from schema_validation import load_schema  # noqa: E402


BENCHMARK_ROOT = ROOT / "benchmarks" / "ai-context" / "v0.1"
RECIPE_PATH = BENCHMARK_ROOT / "recipe.json"
EXPECTED_DIR = BENCHMARK_ROOT / "expected"
EXPECTED_COMPLETE_PATH = EXPECTED_DIR / "complete-narrow.projection.json"
EXPECTED_BOUNDED_PATH = EXPECTED_DIR / "bounded-partial.projection.json"
EXPECTED_REPORT_PATH = BENCHMARK_ROOT / "expected-report.json"

FOUNDATION_PATH = ROOT / "PROJECT_FOUNDATION.md"
S2_SCHEMA_PATH = ROOT / "schema" / "v0.1" / "geesno-semantic.schema.json"
I2_SCHEMA_PATH = (
    ROOT
    / "profiles"
    / "ai-context"
    / "schema"
    / "v0.1"
    / "ai-context.schema.json"
)
PROFILE_PATH = ROOT / "profiles" / "ai-context" / "v0.1" / "profile.json"

BINDING = {
    "family": "https://geesno.com/binding/ai-context-json",
    "version": "0.1.0",
}
PROFILE_EDITION = {
    "profile_family": "https://geesno.com/profile/ai-context",
    "profile_version": "0.1.0",
}
COLLECTIONS = ("entities", "sources", "bindings", "assertions", "tombstones")
MEASUREMENT_SERIALIZATION = {
    "id": "s4-benchmark-json-measurement",
    "version": "0.1",
    "encoding": "UTF-8",
    "ensure_ascii": False,
    "sort_keys": True,
    "separators": [",", ":"],
    "trailing_newline": True,
}
EXPECTED_ROOT_KEYS = {
    "benchmark",
    "generator_recipe",
    "source",
    "materiality",
    "complete_narrow_projection",
    "bounded_partial_projection",
    "measurement_serialization",
    "thresholds",
}


class BenchmarkError(RuntimeError):
    """Raised when generated benchmark evidence violates its fixed recipe."""


@dataclass(frozen=True)
class BenchmarkRun:
    recipe: dict[str, Any]
    source: dict[str, Any]
    complete_projection: dict[str, Any]
    bounded_projection: dict[str, Any]
    report: dict[str, Any]
    source_bytes: bytes
    complete_bytes: bytes
    bounded_bytes: bytes
    report_bytes: bytes


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise BenchmarkError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path) -> str:
    return _sha256(path.read_bytes())


def measurement_text(value: Any) -> str:
    """Serialize only for deterministic benchmark measurement."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ) + "\n"


def measurement_bytes(value: Any) -> bytes:
    return measurement_text(value).encode("utf-8")


def load_recipe() -> dict[str, Any]:
    recipe = json.loads(RECIPE_PATH.read_text(encoding="utf-8"))
    validate_recipe(recipe)
    return recipe


def validate_recipe(recipe: dict[str, Any]) -> None:
    _require(isinstance(recipe, dict), "recipe root must be an object")
    _require(set(recipe) == EXPECTED_ROOT_KEYS, "recipe root members differ")
    _require(
        recipe["benchmark"] == {"id": "s4-ai-context-exit", "version": "0.1"},
        "unsupported benchmark identity",
    )
    _require(
        recipe["generator_recipe"]
        == {"id": "s4-ai-context-benchmark", "version": "0.1"},
        "unsupported generator recipe identity",
    )
    _require(
        recipe["measurement_serialization"] == MEASUREMENT_SERIALIZATION,
        "measurement serialization differs from the supported deterministic form",
    )
    _require(
        recipe["thresholds"]
        == {
            "source_minimum_addressable_records": 10000,
            "bounded_record_ratio_percent_max": 10,
            "bounded_byte_ratio_percent_max": 25,
        },
        "S4 benchmark thresholds changed",
    )

    source = recipe["source"]
    for member in ("entity_count", "assertion_count", "source_count", "binding_count"):
        _require(
            isinstance(source.get(member), int) and source[member] > 0,
            f"source.{member} must be a positive integer",
        )
    _require(
        source["assertion_count"] == source["entity_count"],
        "this fixed recipe requires one Assertion per Entity",
    )
    _require(
        source["binding_count"] == source["source_count"],
        "this fixed recipe requires one Binding per Source",
    )
    top_level_total = sum(
        source[member]
        for member in ("entity_count", "assertion_count", "source_count", "binding_count")
    )
    _require(
        top_level_total >= recipe["thresholds"]["source_minimum_addressable_records"],
        "recipe source does not meet the top-level addressable-record minimum",
    )

    materiality = recipe["materiality"]
    material_entities = materiality["material_entity_indices"]
    material_trace = materiality["material_source_binding_entity_indices"]
    _require(
        material_entities == sorted(set(material_entities)),
        "material Entity indices must be sorted and unique",
    )
    _require(
        material_trace == sorted(set(material_trace)),
        "material Source/Binding indices must be sorted and unique",
    )
    _require(
        set(material_trace).issubset(material_entities),
        "material Source/Binding indices must also be material Entity indices",
    )
    _require(
        all(0 <= index < source["entity_count"] for index in material_entities),
        "material Entity index is outside the source",
    )
    _require(
        all(0 <= index < source["source_count"] for index in material_trace),
        "material Source/Binding index is outside its category",
    )

    narrow = recipe["complete_narrow_projection"]
    narrow_entities = narrow["entity_indices"]
    narrow_trace = narrow["material_source_binding_entity_indices"]
    _require(narrow_entities == [0], "the fixed narrow scope must use Entity 0")
    _require(narrow_trace == [0], "the fixed narrow scope must carry traceability 0")

    bounded = recipe["bounded_partial_projection"]
    scope_count = bounded["scope_entity_count"]
    carried_count = bounded["carried_entity_count"]
    omission_index = bounded["omission_entity_index"]
    bounded_trace = bounded["material_source_binding_entity_indices"]
    _require(
        0 < carried_count < scope_count <= source["entity_count"],
        "bounded carried/scope counts are inconsistent",
    )
    _require(
        carried_count <= omission_index < scope_count,
        "omission target must be known, in scope and outside carried content",
    )
    _require(
        omission_index in material_entities,
        "bounded omission target must be material under this recipe",
    )
    _require(
        bounded_trace == material_trace,
        "bounded Projection must carry the recipe's material Source/Binding cases",
    )
    _require(
        all(index < carried_count for index in bounded_trace),
        "bounded traceability index lies outside carried Entities",
    )


def _record_id(category: str, index: int) -> str:
    prefixes = {
        "entity": "10000000",
        "assertion": "20000000",
        "source": "30000000",
        "binding": "40000000",
        "provenance": "50000000",
        "confidence": "60000000",
        "review": "70000000",
    }
    return f"urn:uuid:{prefixes[category]}-0000-4000-8000-{index:012x}"


def _reference(category: str, index: int) -> dict[str, str]:
    return {"target": _record_id(category, index), "location": "in-document"}


def build_synthetic_source(recipe: dict[str, Any]) -> dict[str, Any]:
    """Build the one fixed synthetic source described by recipe.json."""

    source_recipe = recipe["source"]
    material_entities = set(recipe["materiality"]["material_entity_indices"])
    material_trace = set(
        recipe["materiality"]["material_source_binding_entity_indices"]
    )

    entities: list[dict[str, Any]] = []
    for index in range(source_recipe["entity_count"]):
        entity: dict[str, Any] = {
            "id": _record_id("entity", index),
            "kind": "concept",
        }
        if index in material_entities:
            provenance: dict[str, Any] = {
                "id": _record_id("provenance", index),
                "kind": "bench:synthetic-observation",
                "details": f"Material synthetic observation {index:04d}",
            }
            if index in material_trace:
                provenance["sources"] = [_reference("source", index)]
            entity.update(
                {
                    "provenance": [provenance],
                    "confidence": [
                        {
                            "id": _record_id("confidence", index),
                            "score": {
                                "kind": "decimal",
                                "coefficient": "97",
                                "exponent": "-2",
                            },
                            "method": "bench:deterministic-score",
                        }
                    ],
                    "reviews": [
                        {
                            "id": _record_id("review", index),
                            "disposition": "bench:reviewed",
                            "details": "Synthetic review evidence",
                        }
                    ],
                    "validity": {
                        "kind": "bench:measurement-window",
                        "from": {"kind": "date", "value": "2026-01-01"},
                        "until": {"kind": "date", "value": "2026-12-31"},
                    },
                }
            )
        entities.append(entity)

    sources = [
        {
            "id": _record_id("source", index),
            "locations": [
                {
                    "kind": "bench:source-slot",
                    "value": f"synthetic-source-{index:04d}",
                }
            ],
            "revision": {"kind": "bench:recipe-revision", "value": "r1"},
        }
        for index in range(source_recipe["source_count"])
    ]
    bindings = [
        {
            "id": _record_id("binding", index),
            "entity": _reference("entity", index),
            "source": _reference("source", index),
            "locator": {
                "kind": "bench:source-index",
                "value": f"slot-{index:04d}",
            },
            "method": "bench:deterministic-correlation",
        }
        for index in range(source_recipe["binding_count"])
    ]
    assertions = [
        {
            "id": _record_id("assertion", index),
            "kind": "property",
            "subject": _reference("entity", index),
            "property": "bench:label",
            "value": f"Synthetic semantic record {index:04d}",
        }
        for index in range(source_recipe["assertion_count"])
    ]

    return {
        "spec_version": "0.1.0",
        "id": source_recipe["semantic_document_id"],
        "scope": {"completeness": "partial"},
        "namespaces": {"bench": "https://example.invalid/benchmark/terms/"},
        "entities": entities,
        "sources": sources,
        "bindings": bindings,
        "assertions": assertions,
    }


def _iter_references(value: Any) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        if (
            set(value) == {"target", "location"}
            and isinstance(value["target"], str)
            and isinstance(value["location"], str)
        ):
            yield value["target"], value["location"]
        else:
            for child in value.values():
                yield from _iter_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_references(child)


def _top_record_index(document: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    index: dict[str, tuple[str, dict[str, Any]]] = {}
    for collection in COLLECTIONS:
        for record in document.get(collection, []):
            record_id = record.get("id")
            if isinstance(record_id, str):
                index[record_id] = (collection, record)
    revision = document.get("revision")
    if isinstance(revision, dict) and isinstance(revision.get("id"), str):
        index[revision["id"]] = ("revision", revision)
    return index


def _carried_content(
    source: dict[str, Any],
    entity_indices: list[int],
    source_binding_indices: list[int],
) -> dict[str, Any]:
    return {
        "entities": [copy.deepcopy(source["entities"][index]) for index in entity_indices],
        "sources": [copy.deepcopy(source["sources"][index]) for index in source_binding_indices],
        "bindings": [copy.deepcopy(source["bindings"][index]) for index in source_binding_indices],
        "assertions": [
            copy.deepcopy(source["assertions"][index]) for index in entity_indices
        ],
    }


def _scope_record_ids(
    entity_indices: list[int], source_binding_indices: list[int]
) -> list[str]:
    return (
        [_record_id("entity", index) for index in entity_indices]
        + [_record_id("assertion", index) for index in entity_indices]
        + [_record_id("source", index) for index in source_binding_indices]
        + [_record_id("binding", index) for index in source_binding_indices]
    )


def _reference_availability(carried: dict[str, Any]) -> list[dict[str, Any]]:
    carried_ids = set(_top_record_index(carried))
    targets = sorted({target for target, _ in _iter_references(carried)})
    return [
        {
            "descriptor_id": f"availability-{position:04d}",
            "reference_target": target,
            "availability_state": "carried" if target in carried_ids else "external",
        }
        for position, target in enumerate(targets)
    ]


def _carried_material_context(
    entity_indices: list[int],
    source_binding_indices: list[int],
    material_entity_indices: set[int],
) -> list[dict[str, Any]]:
    descriptors: list[dict[str, Any]] = []
    for index in entity_indices:
        if index not in material_entity_indices:
            continue
        target = _record_id("entity", index)
        descriptors.append(
            {
                "descriptor_id": f"material-entity-{index:04d}",
                "context_target": target,
                "preservation_state": "carried",
                "carried_record_reference": target,
                "requirement_reference": "material-context-carry",
            }
        )
    for index in source_binding_indices:
        source_target = _record_id("source", index)
        binding_target = _record_id("binding", index)
        descriptors.extend(
            [
                {
                    "descriptor_id": f"material-source-{index:04d}",
                    "context_target": source_target,
                    "preservation_state": "carried",
                    "carried_record_reference": source_target,
                    "requirement_reference": "source-record-traceability",
                },
                {
                    "descriptor_id": f"material-binding-{index:04d}",
                    "context_target": binding_target,
                    "preservation_state": "carried",
                    "carried_record_reference": binding_target,
                    "requirement_reference": "binding-record-traceability",
                },
            ]
        )
    return descriptors


def _projection_base(
    recipe: dict[str, Any],
    scope_ids: list[str],
    carried: dict[str, Any],
    completeness: str,
    material_context: list[dict[str, Any]],
) -> dict[str, Any]:
    source_recipe = recipe["source"]
    return {
        "artifact_kind": "projection_artifact",
        "binding": copy.deepcopy(BINDING),
        "profile_edition": copy.deepcopy(PROFILE_EDITION),
        "source_state": {
            "semantic_document_id": source_recipe["semantic_document_id"],
            "source_state_descriptor": source_recipe["source_state_descriptor"],
        },
        "selection_context": {
            "selection_context_kind": "benchmark-record-set",
            "selection_descriptor": {"record_ids": copy.deepcopy(scope_ids)},
        },
        "projection_scope": {
            "scope_kind": "benchmark-record-set",
            "scope_descriptor": {"record_ids": copy.deepcopy(scope_ids)},
            "requirement_reference": "projection-baseline",
        },
        "projection_completeness": completeness,
        "carried_content": carried,
        "namespaces": {"bench": "https://example.invalid/benchmark/terms/"},
        "reference_availability": _reference_availability(carried),
        "material_context": material_context,
    }


def build_complete_projection(
    recipe: dict[str, Any], source: dict[str, Any]
) -> dict[str, Any]:
    projection_recipe = recipe["complete_narrow_projection"]
    entity_indices = projection_recipe["entity_indices"]
    trace_indices = projection_recipe["material_source_binding_entity_indices"]
    carried = _carried_content(source, entity_indices, trace_indices)
    scope_ids = _scope_record_ids(entity_indices, trace_indices)
    material = _carried_material_context(
        entity_indices,
        trace_indices,
        set(recipe["materiality"]["material_entity_indices"]),
    )
    return _projection_base(recipe, scope_ids, carried, "complete", material)


def build_bounded_projection(
    recipe: dict[str, Any], source: dict[str, Any]
) -> dict[str, Any]:
    projection_recipe = recipe["bounded_partial_projection"]
    scope_entities = list(range(projection_recipe["scope_entity_count"]))
    carried_entities = list(range(projection_recipe["carried_entity_count"]))
    trace_indices = projection_recipe["material_source_binding_entity_indices"]
    scope_ids = _scope_record_ids(scope_entities, trace_indices)
    carried = _carried_content(source, carried_entities, trace_indices)
    material = _carried_material_context(
        carried_entities,
        trace_indices,
        set(recipe["materiality"]["material_entity_indices"]),
    )
    omission_index = projection_recipe["omission_entity_index"]
    omitted_target = _record_id("entity", omission_index)
    omission_id = f"omitted-material-entity-{omission_index:04d}"
    material.append(
        {
            "descriptor_id": f"material-omission-entity-{omission_index:04d}",
            "context_target": omitted_target,
            "preservation_state": "omitted",
            "omission_reference": {
                "descriptor_group": "omissions",
                "descriptor_id": omission_id,
            },
            "requirement_reference": "material-context-omission",
        }
    )

    projection = _projection_base(recipe, scope_ids, carried, "partial", material)
    carried_count = len(_top_record_index(carried))
    remaining_count = len(scope_ids) - carried_count
    projection.update(
        {
            "boundedness": [
                {
                    "descriptor_id": "bounded-carried-records",
                    "bound_dimension": projection_recipe["bound_dimension"],
                    "bound_rule": projection_recipe["bound_rule"],
                    "limit_value": carried_count,
                    "bound_reached": True,
                }
            ],
            "truncation": {
                "truncation_established": True,
                "affected_scope": "declared-benchmark-record-set",
                "bound_reference": {
                    "descriptor_group": "boundedness",
                    "descriptor_id": "bounded-carried-records",
                },
                "requirement_reference": "projection-baseline",
            },
            "omissions": [
                {
                    "descriptor_id": omission_id,
                    "omitted_target": omitted_target,
                    "omission_category": "material-selected-record",
                    "requirement_reference": "material-context-omission",
                }
            ],
            "projection_continuations": [
                {
                    "descriptor_id": "remaining-benchmark-scope",
                    "continuation_scope": {
                        "remaining_record_count": remaining_count,
                        "first_uncarried_entity": _record_id(
                            "entity", projection_recipe["carried_entity_count"]
                        ),
                    },
                    "continuation_descriptor": projection_recipe[
                        "continuation_recipe"
                    ],
                    "source_state_reference": {
                        "semantic_document_id": recipe["source"][
                            "semantic_document_id"
                        ],
                        "source_state_descriptor": recipe["source"][
                            "source_state_descriptor"
                        ],
                    },
                    "profile_edition_reference": copy.deepcopy(PROFILE_EDITION),
                }
            ],
        }
    )
    return projection


def _record_counts(document: dict[str, Any]) -> dict[str, int]:
    return {
        collection: len(document.get(collection, []))
        for collection in COLLECTIONS
        if document.get(collection)
    }


def _nested_material_counts(document: dict[str, Any]) -> dict[str, int]:
    counts = {"provenance": 0, "confidence": 0, "reviews": 0}
    for collection in COLLECTIONS:
        for record in document.get(collection, []):
            counts["provenance"] += len(record.get("provenance", []))
            counts["confidence"] += len(record.get("confidence", []))
            counts["reviews"] += len(record.get("reviews", []))
    return counts


def _ratio(numerator: int, denominator: int) -> dict[str, Any]:
    getcontext().prec = 40
    decimal = Decimal(numerator) / Decimal(denominator)
    return {
        "numerator": numerator,
        "denominator": denominator,
        "decimal": f"{decimal:.12f}",
    }


def _identity_result(
    source: dict[str, Any],
    projection: dict[str, Any],
    expected_ids: set[str],
) -> dict[str, Any]:
    source_index = _top_record_index(source)
    carried_index = _top_record_index(projection["carried_content"])
    carried_ids = set(carried_index)
    matched = sum(
        1
        for record_id in carried_ids & set(source_index)
        if carried_index[record_id][0] == source_index[record_id][0]
    )
    rewritten = len(expected_ids - carried_ids)
    fabricated = len(carried_ids - set(source_index))
    category_changes = len(carried_ids & set(source_index)) - matched
    passed = (
        carried_ids == expected_ids
        and matched == len(carried_ids)
        and rewritten == 0
        and fabricated == 0
        and category_changes == 0
    )
    return {
        "result": "pass" if passed else "fail",
        "carried_id_count": len(carried_ids),
        "matched_exact_ids": matched,
        "rewritten_ids": rewritten,
        "fabricated_ids": fabricated,
        "category_changes": category_changes,
    }


def _reference_result(
    source: dict[str, Any], projection: dict[str, Any]
) -> dict[str, Any]:
    source_index = _top_record_index(source)
    carried_index = _top_record_index(projection["carried_content"])
    checked = 0
    retargeted = 0
    fabricated_targets = 0
    for record_id, (_, record) in carried_index.items():
        source_record = source_index.get(record_id, ("", {}))[1]
        carried_references = list(_iter_references(record))
        source_references = list(_iter_references(source_record))
        checked += len(carried_references)
        if Counter(carried_references) != Counter(source_references):
            difference = (
                Counter(carried_references) - Counter(source_references)
            ) + (Counter(source_references) - Counter(carried_references))
            retargeted += sum(difference.values()) or 1
        for target, location in carried_references:
            if location == "in-document" and target not in source_index:
                fabricated_targets += 1
    passed = retargeted == 0 and fabricated_targets == 0
    return {
        "result": "pass" if passed else "fail",
        "carried_exact_references_checked": checked,
        "retargeted_references": retargeted,
        "fabricated_carried_targets": fabricated_targets,
    }


def _provenance_result(
    recipe: dict[str, Any],
    source: dict[str, Any],
    projection: dict[str, Any],
) -> dict[str, Any]:
    material_indices = set(recipe["materiality"]["material_entity_indices"])
    carried_entities = {
        item["id"]: item for item in projection["carried_content"].get("entities", [])
    }
    required = [
        index
        for index in sorted(material_indices)
        if _record_id("entity", index) in carried_entities
    ]
    missing = 0
    altered = 0
    for index in required:
        source_entity = source["entities"][index]
        carried_entity = carried_entities[_record_id("entity", index)]
        if "provenance" not in carried_entity:
            missing += 1
        elif carried_entity["provenance"] != source_entity["provenance"]:
            altered += 1
    preserved = len(required) - missing - altered
    return {
        "result": "pass" if missing == 0 and altered == 0 else "fail",
        "required_material_provenance_cases": len(required),
        "preserved_material_provenance_cases": preserved,
        "missing": missing,
        "altered_or_widened": altered,
    }


def _traceability_result(
    source: dict[str, Any],
    projection: dict[str, Any],
    category: str,
    required_indices: list[int],
) -> dict[str, Any]:
    plural = "sources" if category == "source" else "bindings"
    source_records = {item["id"]: item for item in source[plural]}
    carried_records = {
        item["id"]: item for item in projection["carried_content"].get(plural, [])
    }
    required_ids = {_record_id(category, index) for index in required_indices}
    missing = len(required_ids - set(carried_records))
    retargeted = sum(
        1
        for record_id in required_ids & set(carried_records)
        if carried_records[record_id] != source_records[record_id]
    )
    preserved = len(required_ids) - missing - retargeted
    return {
        "result": "pass" if missing == 0 and retargeted == 0 else "fail",
        f"required_material_{plural}": len(required_ids),
        f"preserved_material_{plural}": preserved,
        "missing": missing,
        "retargeted": retargeted,
    }


def _scope_ids(projection: dict[str, Any]) -> list[str]:
    scope = projection.get("projection_scope", {})
    descriptor = scope.get("scope_descriptor", {})
    _require(
        scope.get("scope_kind") == "benchmark-record-set"
        and isinstance(descriptor, dict)
        and isinstance(descriptor.get("record_ids"), list)
        and all(isinstance(item, str) for item in descriptor["record_ids"]),
        "Projection does not use the fixed explicit benchmark-record-set scope",
    )
    return descriptor["record_ids"]


def _expected_carried_ids(
    entity_indices: list[int], source_binding_indices: list[int]
) -> set[str]:
    return set(_scope_record_ids(entity_indices, source_binding_indices))


def _material_descriptor_errors(
    recipe: dict[str, Any],
    projection: dict[str, Any],
    entity_indices: list[int],
    trace_indices: list[int],
    omitted_index: int | None = None,
) -> list[str]:
    descriptors = {
        (item.get("context_target"), item.get("requirement_reference")): item
        for item in projection.get("material_context", [])
    }
    errors: list[str] = []
    material_entities = set(recipe["materiality"]["material_entity_indices"])
    for index in entity_indices:
        if index not in material_entities:
            continue
        target = _record_id("entity", index)
        descriptor = descriptors.get((target, "material-context-carry"))
        if not descriptor or descriptor.get("carried_record_reference") != target:
            errors.append(f"material Entity {index} lacks exact carried context")
    for index in trace_indices:
        source_target = _record_id("source", index)
        binding_target = _record_id("binding", index)
        source_descriptor = descriptors.get(
            (source_target, "source-record-traceability")
        )
        binding_descriptor = descriptors.get(
            (binding_target, "binding-record-traceability")
        )
        if not source_descriptor or source_descriptor.get(
            "carried_record_reference"
        ) != source_target:
            errors.append(f"material Source {index} lacks exact carried context")
        if not binding_descriptor or binding_descriptor.get(
            "carried_record_reference"
        ) != binding_target:
            errors.append(f"material Binding {index} lacks exact carried context")
    if omitted_index is not None:
        omitted_target = _record_id("entity", omitted_index)
        descriptor = descriptors.get((omitted_target, "material-context-omission"))
        if not descriptor or descriptor.get("preservation_state") != "omitted":
            errors.append("known omitted material Entity lacks omission context")
    return errors


def benchmark_specific_errors(
    recipe: dict[str, Any],
    source: dict[str, Any],
    complete: dict[str, Any],
    bounded: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    source_ids = set(_top_record_index(source))

    narrow_recipe = recipe["complete_narrow_projection"]
    narrow_expected = _expected_carried_ids(
        narrow_recipe["entity_indices"],
        narrow_recipe["material_source_binding_entity_indices"],
    )
    narrow_scope = _scope_ids(complete)
    narrow_carried = set(_top_record_index(complete["carried_content"]))
    narrow_selected = complete["selection_context"].get("selection_descriptor", {}).get(
        "record_ids"
    )
    if set(narrow_scope) != narrow_expected or narrow_carried != narrow_expected:
        errors.append("complete narrow Projection does not carry its exact scope")
    if narrow_selected != narrow_scope:
        errors.append("complete narrow selection context differs from Projection scope")
    if not set(narrow_scope).issubset(source_ids):
        errors.append("complete narrow scope contains records absent from source")
    if complete.get("projection_completeness") != "complete":
        errors.append("complete narrow Projection is not complete")
    for member in ("boundedness", "truncation", "omissions", "projection_continuations"):
        if member in complete:
            errors.append(f"complete narrow Projection unexpectedly contains {member}")
    errors.extend(
        _material_descriptor_errors(
            recipe,
            complete,
            narrow_recipe["entity_indices"],
            narrow_recipe["material_source_binding_entity_indices"],
        )
    )

    bounded_recipe = recipe["bounded_partial_projection"]
    bounded_scope_entities = list(range(bounded_recipe["scope_entity_count"]))
    bounded_carried_entities = list(range(bounded_recipe["carried_entity_count"]))
    bounded_trace = bounded_recipe["material_source_binding_entity_indices"]
    bounded_expected = _expected_carried_ids(bounded_carried_entities, bounded_trace)
    bounded_expected_scope = _expected_carried_ids(bounded_scope_entities, bounded_trace)
    bounded_scope = _scope_ids(bounded)
    bounded_carried = set(_top_record_index(bounded["carried_content"]))
    bounded_selected = bounded["selection_context"].get("selection_descriptor", {}).get(
        "record_ids"
    )
    if set(bounded_scope) != bounded_expected_scope:
        errors.append("bounded Projection scope differs from recipe")
    if bounded_carried != bounded_expected:
        errors.append("bounded carried record set differs from recipe")
    if bounded_selected != bounded_scope:
        errors.append("bounded selection context differs from Projection scope")
    if not set(bounded_scope).issubset(source_ids):
        errors.append("bounded scope contains records absent from source")
    if bounded.get("projection_completeness") != "partial":
        errors.append("bounded Projection is not partial")
    if not bounded.get("boundedness") or not all(
        item.get("bound_reached") is True for item in bounded["boundedness"]
    ):
        errors.append("bounded Projection lacks a reached explicit bound")
    if bounded.get("truncation", {}).get("truncation_established") is not True:
        errors.append("bounded Projection lacks established truncation")
    if not bounded.get("omissions"):
        errors.append("bounded Projection lacks explicit omission")
    if not bounded.get("projection_continuations"):
        errors.append("bounded Projection lacks Projection continuation")
    omission_target = _record_id("entity", bounded_recipe["omission_entity_index"])
    if bounded.get("omissions", [{}])[0].get("omitted_target") != omission_target:
        errors.append("bounded omission target differs from recipe")
    if omission_target in bounded_carried or omission_target not in set(bounded_scope):
        errors.append("bounded omission target is not a missing in-scope record")
    if bounded["boundedness"][0].get("limit_value") != len(bounded_carried):
        errors.append("bounded limit value differs from carried record count")
    continuation = bounded.get("projection_continuations", [{}])[0]
    expected_remaining = len(bounded_scope) - len(bounded_carried)
    if continuation.get("continuation_scope", {}).get(
        "remaining_record_count"
    ) != expected_remaining:
        errors.append("Projection continuation remaining count differs from scope")
    if continuation.get("source_state_reference") != bounded.get("source_state"):
        errors.append("Projection continuation changes source state")
    if continuation.get("profile_edition_reference") != bounded.get("profile_edition"):
        errors.append("Projection continuation changes Profile edition")
    errors.extend(
        _material_descriptor_errors(
            recipe,
            bounded,
            bounded_carried_entities,
            bounded_trace,
            omitted_index=bounded_recipe["omission_entity_index"],
        )
    )

    return sorted(set(errors))


def _projection_report(
    recipe: dict[str, Any],
    source: dict[str, Any],
    projection: dict[str, Any],
    serialized: bytes,
    source_record_count: int,
    source_byte_count: int,
    expected_ids: set[str],
    trace_indices: list[int],
) -> dict[str, Any]:
    counts = _record_counts(projection["carried_content"])
    carried_total = sum(counts.values())
    text = serialized.decode("utf-8")
    return {
        "source_state": projection["source_state"],
        "selection_context": projection["selection_context"],
        "projection_scope": projection["projection_scope"],
        "projection_completeness": projection["projection_completeness"],
        "carried_record_counts_by_category": counts,
        "total_carried_semantic_records": carried_total,
        "additional_nested_id_bearing_context_by_category": _nested_material_counts(
            projection["carried_content"]
        ),
        "selected_record_count": len(_scope_ids(projection)),
        "descriptor_counts": {
            "omissions": len(projection.get("omissions", [])),
            "projection_continuations": len(
                projection.get("projection_continuations", [])
            ),
            "dependency_continuations": len(
                projection.get("dependency_continuations", [])
            ),
            "material_context": len(projection.get("material_context", [])),
            "reference_availability": len(
                projection.get("reference_availability", [])
            ),
        },
        "serialized_utf8_bytes": len(serialized),
        "serialized_unicode_characters": len(text),
        "sha256": _sha256(serialized),
        "source_record_ratio": _ratio(carried_total, source_record_count),
        "source_byte_ratio": _ratio(len(serialized), source_byte_count),
        "boundedness_present": bool(projection.get("boundedness")),
        "bound_reached_states": [
            item["bound_reached"] for item in projection.get("boundedness", [])
        ],
        "truncation_present": "truncation" in projection,
        "truncation_established": projection.get("truncation", {}).get(
            "truncation_established", False
        ),
        "identity_retention": _identity_result(source, projection, expected_ids),
        "reference_retention": _reference_result(source, projection),
        "material_provenance_retention": _provenance_result(
            recipe, source, projection
        ),
        "source_retention": _traceability_result(
            source, projection, "source", trace_indices
        ),
        "binding_retention": _traceability_result(
            source, projection, "binding", trace_indices
        ),
    }


def _all_retention_passed(report: dict[str, Any]) -> bool:
    return all(
        report[name]["result"] == "pass"
        for name in (
            "identity_retention",
            "reference_retention",
            "material_provenance_retention",
            "source_retention",
            "binding_retention",
        )
    )


def build_benchmark_run(
    recipe: dict[str, Any] | None = None,
    *,
    validate_source: bool = True,
) -> BenchmarkRun:
    recipe = copy.deepcopy(recipe) if recipe is not None else load_recipe()
    validate_recipe(recipe)
    source = build_synthetic_source(recipe)
    complete = build_complete_projection(recipe, source)
    bounded = build_bounded_projection(recipe, source)

    source_bytes = measurement_bytes(source)
    complete_bytes = measurement_bytes(complete)
    bounded_bytes = measurement_bytes(bounded)

    if validate_source:
        s2_result = validate_bytes(source_bytes, load_schema(S2_SCHEMA_PATH))
        _require(
            s2_result == {"result": "valid"},
            f"generated source is invalid: {s2_result}",
        )
    for name, projection in (("complete", complete), ("bounded", bounded)):
        structural = acceptance.structural_errors(projection)
        _require(not structural, f"{name} Projection failed I2: {structural}")
        semantic = acceptance.semantic_errors(projection, source)
        _require(not semantic, f"{name} Projection failed I4 checks: {semantic}")
    specific = benchmark_specific_errors(recipe, source, complete, bounded)
    _require(not specific, f"benchmark-specific checks failed: {specific}")

    source_counts = _record_counts(source)
    source_total = sum(source_counts.values())
    source_text = source_bytes.decode("utf-8")
    narrow_recipe = recipe["complete_narrow_projection"]
    bounded_recipe = recipe["bounded_partial_projection"]
    complete_expected_ids = _expected_carried_ids(
        narrow_recipe["entity_indices"],
        narrow_recipe["material_source_binding_entity_indices"],
    )
    bounded_expected_ids = _expected_carried_ids(
        list(range(bounded_recipe["carried_entity_count"])),
        bounded_recipe["material_source_binding_entity_indices"],
    )
    complete_report = _projection_report(
        recipe,
        source,
        complete,
        complete_bytes,
        source_total,
        len(source_bytes),
        complete_expected_ids,
        narrow_recipe["material_source_binding_entity_indices"],
    )
    bounded_report = _projection_report(
        recipe,
        source,
        bounded,
        bounded_bytes,
        source_total,
        len(source_bytes),
        bounded_expected_ids,
        bounded_recipe["material_source_binding_entity_indices"],
    )

    thresholds = recipe["thresholds"]
    source_minimum_passed = (
        source_total >= thresholds["source_minimum_addressable_records"]
    )
    record_ratio_passed = (
        bounded_report["total_carried_semantic_records"] * 100
        <= source_total * thresholds["bounded_record_ratio_percent_max"]
    )
    byte_ratio_passed = (
        len(bounded_bytes) * 100
        <= len(source_bytes) * thresholds["bounded_byte_ratio_percent_max"]
    )
    _require(source_minimum_passed, "source record threshold failed")
    _require(record_ratio_passed, "bounded record-ratio threshold failed")
    _require(byte_ratio_passed, "bounded byte-ratio threshold failed")
    _require(_all_retention_passed(complete_report), "complete retention checks failed")
    _require(_all_retention_passed(bounded_report), "bounded retention checks failed")

    source_nested_counts = _nested_material_counts(source)
    source_nested_total = sum(source_nested_counts.values())
    report = {
        "artifact_kind": "non_normative_s4_benchmark_evidence",
        "benchmark": recipe["benchmark"],
        "generator_recipe": {
            **recipe["generator_recipe"],
            "path": "benchmarks/ai-context/v0.1/recipe.json",
            "sha256": _file_sha256(RECIPE_PATH),
        },
        "profile_edition": copy.deepcopy(PROFILE_EDITION),
        "projection_binding_under_test": copy.deepcopy(BINDING),
        "measurement_serialization": copy.deepcopy(MEASUREMENT_SERIALIZATION),
        "normative_input_sha256": {
            "PROJECT_FOUNDATION.md": _file_sha256(FOUNDATION_PATH),
            "schema/v0.1/geesno-semantic.schema.json": _file_sha256(S2_SCHEMA_PATH),
            "profiles/ai-context/schema/v0.1/ai-context.schema.json": _file_sha256(
                I2_SCHEMA_PATH
            ),
            "profiles/ai-context/v0.1/profile.json": _file_sha256(PROFILE_PATH),
        },
        "source": {
            "semantic_document_id": source["id"],
            "source_state_descriptor": recipe["source"]["source_state_descriptor"],
            "benchmark_record_count_formula": "entities + assertions + sources + bindings",
            "record_counts_by_category": source_counts,
            "total_addressable_semantic_records": source_total,
            "additional_nested_id_bearing_context_by_category": source_nested_counts,
            "additional_nested_id_bearing_context_total": source_nested_total,
            "total_id_bearing_records_including_nested_context": (
                source_total + source_nested_total
            ),
            "benchmark_threshold_and_ratio_denominator": source_total,
            "serialized_utf8_bytes": len(source_bytes),
            "serialized_unicode_characters": len(source_text),
            "sha256": _sha256(source_bytes),
        },
        "complete_narrow_projection": complete_report,
        "bounded_partial_projection": bounded_report,
        "thresholds": {
            "source_minimum_addressable_records": thresholds[
                "source_minimum_addressable_records"
            ],
            "bounded_record_ratio_percent_max": thresholds[
                "bounded_record_ratio_percent_max"
            ],
            "bounded_byte_ratio_percent_max": thresholds[
                "bounded_byte_ratio_percent_max"
            ],
            "source_minimum_passed": source_minimum_passed,
            "bounded_record_ratio_passed": record_ratio_passed,
            "bounded_byte_ratio_passed": byte_ratio_passed,
            "evaluation": "integer cross-multiplication",
            "semantic_authority": False,
        },
        "dependencies": {
            "offline": True,
            "network_dependency": False,
            "model_provider_dependency": False,
            "tokenizer_dependency": False,
            "external_resolver_dependency": False,
            "automatic_dereference": False,
        },
    }
    report_bytes = measurement_bytes(report)
    return BenchmarkRun(
        recipe=recipe,
        source=source,
        complete_projection=complete,
        bounded_projection=bounded,
        report=report,
        source_bytes=source_bytes,
        complete_bytes=complete_bytes,
        bounded_bytes=bounded_bytes,
        report_bytes=report_bytes,
    )


def expected_mismatches(run: BenchmarkRun) -> list[str]:
    expected = (
        (EXPECTED_COMPLETE_PATH, run.complete_bytes),
        (EXPECTED_BOUNDED_PATH, run.bounded_bytes),
        (EXPECTED_REPORT_PATH, run.report_bytes),
    )
    mismatches: list[str] = []
    for path, actual in expected:
        if not path.is_file():
            mismatches.append(f"missing expected artifact {path.relative_to(ROOT)}")
        elif path.read_bytes() != actual:
            mismatches.append(f"expected artifact differs: {path.relative_to(ROOT)}")
    return mismatches


def write_expected(run: BenchmarkRun) -> None:
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)
    EXPECTED_COMPLETE_PATH.write_bytes(run.complete_bytes)
    EXPECTED_BOUNDED_PATH.write_bytes(run.bounded_bytes)
    EXPECTED_REPORT_PATH.write_bytes(run.report_bytes)


def _print_summary(run: BenchmarkRun) -> None:
    source = run.report["source"]
    complete = run.report["complete_narrow_projection"]
    bounded = run.report["bounded_partial_projection"]
    print(
        "S4 AI Context benchmark OK: "
        f"source={source['total_addressable_semantic_records']} records, "
        f"complete={complete['total_carried_semantic_records']} records, "
        f"bounded={bounded['total_carried_semantic_records']} records, "
        f"record_ratio={bounded['source_record_ratio']['decimal']}, "
        f"byte_ratio={bounded['source_byte_ratio']['decimal']}."
    )
    print(
        "Digests: "
        f"source={source['sha256']}, "
        f"complete={complete['sha256']}, "
        f"bounded={bounded['sha256']}."
    )
    print(
        "Offline deterministic milestone evidence only; no Profile conformance "
        "threshold, model, tokenizer, resolver or network dependency."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the repository-internal non-normative S4 AI Context benchmark."
    )
    parser.add_argument(
        "--write-expected",
        action="store_true",
        help="maintainer-only: replace checked benchmark evidence",
    )
    args = parser.parse_args(argv)
    try:
        run = build_benchmark_run()
        if args.write_expected:
            write_expected(run)
        else:
            mismatches = expected_mismatches(run)
            _require(not mismatches, "; ".join(mismatches))
        _print_summary(run)
    except (BenchmarkError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
