"""Repository-local S5 I6 aggregation and result construction.

This module consumes I5 requirement assessments and explicit diagnostic causes.
It implements only the accepted ADR-0030 aggregation and the human-approved I1
assessment binding. It is not a public API, CLI, SDK, runtime, resolver or
arbitrary-Profile evaluator.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

try:
    from . import ai_context_assessment_corpus as result_validation
    from . import ai_context_requirement_assessment as requirement_assessment
except ImportError:  # Direct repository-script execution.
    import ai_context_assessment_corpus as result_validation
    import ai_context_requirement_assessment as requirement_assessment


ASSESSMENT_BINDING = {
    "family": "https://geesno.com/binding/ai-context-assessment-json",
    "version": "0.1.0",
}
ARTIFACT_KIND = "conformance_result_artifact"
PROFILE_EDITION = dict(requirement_assessment.PROFILE_EDITION)
OVERALL_OUTCOMES = frozenset(
    {"conformant", "nonconformant", "indeterminate"}
)
DIAGNOSTIC_TAXONOMY = {
    "requirement_violated": "requirement_evaluation",
    "requirement_unsupported": "requirement_evaluation",
    "dependency_unavailable": "dependency_availability",
    "requirement_not_applicable": "requirement_evaluation",
    "invalid_binding_construct": "binding_structure",
    "unsupported_binding_construct": "binding_structure",
    "contradictory_projection_metadata": "binding_structure",
    "exact_vocabulary_unavailable": "dependency_availability",
    "profile_requirement_artifact_unavailable": "dependency_availability",
    "unresolved_requirement_reference": "requirement_reference",
    "missing_namespace_expansion_context": "binding_structure",
    "invalid_reference_availability_consistency": "binding_structure",
    "invalid_source_state_reference_preservation": "binding_structure",
    "structural_validation_failed": "binding_structure",
    "assessment_input_uninterpretable": "assessment_input",
}
DIAGNOSTIC_SEVERITIES = frozenset({"info", "warning", "error"})
UNAVAILABLE_DIAGNOSTIC_CODES = frozenset(
    {
        "dependency_unavailable",
        "exact_vocabulary_unavailable",
        "profile_requirement_artifact_unavailable",
    }
)
OUTCOME_DIAGNOSTIC_CODES = frozenset(
    {
        "requirement_violated",
        "requirement_unsupported",
        "requirement_not_applicable",
        *UNAVAILABLE_DIAGNOSTIC_CODES,
    }
)
ALLOWED_OUTCOME_DIAGNOSTICS = {
    "satisfied": frozenset(),
    "violated": frozenset({"requirement_violated"}),
    "not_applicable": frozenset({"requirement_not_applicable"}),
    "unsupported": frozenset({"requirement_unsupported"}),
    "unavailable": UNAVAILABLE_DIAGNOSTIC_CODES,
}
BLOCKER_DIAGNOSTIC_CODES = frozenset(DIAGNOSTIC_TAXONOMY) - {
    "requirement_violated",
    "requirement_unsupported",
    "requirement_not_applicable",
}


@dataclass(frozen=True)
class DiagnosticInput:
    """One explicit accepted diagnostic cause plus optional reporting data."""

    code: str
    diagnostic_ref: Mapping[str, Any] | None = None
    requirement_ref: Mapping[str, Any] | None = None
    requirement_result_ref: Mapping[str, Any] | None = None
    subject_ref: Mapping[str, Any] | None = None
    severity: str | None = None
    message: str | None = None
    locator: str | None = None
    related_refs: tuple[Mapping[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if self.code not in DIAGNOSTIC_TAXONOMY:
            raise ValueError(f"unsupported diagnostic code: {self.code}")
        if self.severity is not None and self.severity not in DIAGNOSTIC_SEVERITIES:
            raise ValueError(f"unsupported diagnostic severity: {self.severity}")


def aggregate_outcomes(
    outcomes: Sequence[str],
    *,
    decisive_structural_violation: bool = False,
    blockers: Sequence[DiagnosticInput] = (),
) -> str:
    """Apply D7 aggregation without deriving structural state from diagnostics."""

    invalid = sorted(set(outcomes) - requirement_assessment.REQUIREMENT_OUTCOMES)
    if invalid:
        raise ValueError(f"unsupported requirement outcomes: {invalid}")
    # The caller must establish this fact independently from diagnostic category.
    if not isinstance(decisive_structural_violation, bool):
        raise TypeError("decisive_structural_violation must be an explicit bool")
    if "violated" in outcomes or decisive_structural_violation:
        return "nonconformant"
    if "unsupported" in outcomes or "unavailable" in outcomes or blockers:
        return "indeterminate"
    return "conformant"


def _diagnostic_record(
    diagnostic: DiagnosticInput,
    *,
    default_requirement_ref: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if (
        diagnostic.requirement_ref is not None
        and default_requirement_ref is not None
        and diagnostic.requirement_ref != default_requirement_ref
    ):
        raise ValueError("diagnostic requirement_ref differs from its result")

    record: dict[str, Any] = {
        "diagnostic_code": diagnostic.code,
        "diagnostic_category": DIAGNOSTIC_TAXONOMY[diagnostic.code],
    }
    effective_requirement_ref = (
        diagnostic.requirement_ref
        if diagnostic.requirement_ref is not None
        else default_requirement_ref
    )
    optional_values = (
        ("diagnostic_ref", diagnostic.diagnostic_ref),
        ("requirement_ref", effective_requirement_ref),
        ("requirement_result_ref", diagnostic.requirement_result_ref),
        ("subject_ref", diagnostic.subject_ref),
        ("diagnostic_severity", diagnostic.severity),
        ("message", diagnostic.message),
        ("locator", diagnostic.locator),
    )
    for member, value in optional_values:
        if value is not None:
            record[member] = copy.deepcopy(value)
    if diagnostic.related_refs:
        record["related_refs"] = copy.deepcopy(list(diagnostic.related_refs))
    return record


def _required_diagnostics(
    outcome: str,
    supplied: Sequence[DiagnosticInput],
) -> tuple[DiagnosticInput, ...]:
    diagnostics = tuple(supplied)
    codes = {diagnostic.code for diagnostic in diagnostics}
    non_outcome_codes = codes - OUTCOME_DIAGNOSTIC_CODES
    if non_outcome_codes:
        raise ValueError(
            "structural diagnostics must be supplied as explicit blockers or "
            f"structural violations: {sorted(non_outcome_codes)}"
        )
    contradictory = (codes & OUTCOME_DIAGNOSTIC_CODES) - ALLOWED_OUTCOME_DIAGNOSTICS[
        outcome
    ]
    if contradictory:
        raise ValueError(
            f"diagnostic codes contradict {outcome}: {sorted(contradictory)}"
        )
    if outcome == "violated" and "requirement_violated" not in codes:
        diagnostics += (DiagnosticInput("requirement_violated"),)
    elif outcome == "unsupported" and "requirement_unsupported" not in codes:
        diagnostics += (DiagnosticInput("requirement_unsupported"),)
    elif outcome == "unavailable" and not (codes & UNAVAILABLE_DIAGNOSTIC_CODES):
        raise ValueError(
            "unavailable requires an explicit accepted availability diagnostic cause"
        )
    return diagnostics


def _validate_constructed_artifact(artifact: Mapping[str, Any]) -> None:
    errors = (
        result_validation.layer_a_errors(artifact)
        + result_validation.temporal_errors(artifact)
        + result_validation.layer_b_errors(artifact)
    )
    if errors:
        raise ValueError("constructed result is invalid: " + "; ".join(errors))


def construct_conformance_result(
    run: requirement_assessment.RequirementAssessmentRun,
    *,
    assessment_subject: Mapping[str, Any],
    requirement_references: Mapping[str, Mapping[str, Any]],
    requirement_diagnostics: Mapping[
        str, Sequence[DiagnosticInput]
    ] | None = None,
    blocker_diagnostics: Sequence[DiagnosticInput] = (),
    decisive_structural_violation: bool = False,
    requirement_result_references: Mapping[str, Mapping[str, Any]] | None = None,
    profile_edition: Mapping[str, Any] = PROFILE_EDITION,
    profile_requirement_artifact_reference: Mapping[str, Any] | None = None,
    assessment_result_id: str | None = None,
    assessment_context: Mapping[str, Any] | None = None,
    reference_scope: Mapping[str, Any] | None = None,
    assessor_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one valid exact-Profile 0.1 D7 result without inventing identity."""

    if dict(profile_edition) != PROFILE_EDITION:
        raise ValueError("I6 constructs results only for exact AI Context Profile 0.1.0")
    if not run.enumeration_available and run.results:
        raise ValueError("blocked enumeration cannot contain requirement results")

    requirement_diagnostics = requirement_diagnostics or {}
    requirement_result_references = requirement_result_references or {}
    result_ids = tuple(result.requirement_id for result in run.results)
    if len(result_ids) != len(set(result_ids)):
        raise ValueError("duplicate requirement occurrence result")

    expected_ids = set(requirement_assessment.REQUIREMENT_IDS)
    if run.enumeration_available:
        if set(result_ids) != expected_ids or len(result_ids) != len(expected_ids):
            raise ValueError("available exact Profile enumeration must contain nine results")
        if set(requirement_references) != expected_ids:
            raise ValueError("each exact Profile requirement needs one supplied reference")
    elif requirement_references:
        raise ValueError("blocked enumeration cannot fabricate requirement references")

    for supplied_name, supplied in (
        ("requirement diagnostics", requirement_diagnostics),
        ("requirement-result references", requirement_result_references),
    ):
        unknown = sorted(set(supplied) - set(result_ids))
        if unknown:
            raise ValueError(f"{supplied_name} target unknown results: {unknown}")

    all_blockers = tuple(blocker_diagnostics)
    invalid_blockers = sorted(
        diagnostic.code
        for diagnostic in all_blockers
        if diagnostic.code not in BLOCKER_DIAGNOSTIC_CODES
    )
    if invalid_blockers:
        raise ValueError(f"diagnostics are not assessment blockers: {invalid_blockers}")
    if not run.enumeration_available and not all_blockers:
        raise ValueError("blocked enumeration requires an explicit diagnostic")

    serialized_results: list[dict[str, Any]] = []
    serialized_diagnostics: list[dict[str, Any]] = []
    for result in run.results:
        requirement_ref = requirement_references[result.requirement_id]
        diagnostics = _required_diagnostics(
            result.outcome,
            requirement_diagnostics.get(result.requirement_id, ()),
        )
        result_record: dict[str, Any] = {
            "requirement_ref": copy.deepcopy(requirement_ref),
            "outcome": result.outcome,
        }
        result_ref = requirement_result_references.get(result.requirement_id)
        if result_ref is not None:
            result_record["requirement_result_ref"] = copy.deepcopy(result_ref)

        diagnostic_refs: list[Mapping[str, Any]] = []
        for diagnostic in diagnostics:
            if (
                diagnostic.requirement_result_ref is not None
                and diagnostic.requirement_result_ref != result_ref
            ):
                raise ValueError(
                    "diagnostic requirement_result_ref differs from its result"
                )
            serialized_diagnostics.append(
                _diagnostic_record(
                    diagnostic,
                    default_requirement_ref=requirement_ref,
                )
            )
            if diagnostic.diagnostic_ref is not None:
                diagnostic_refs.append(diagnostic.diagnostic_ref)
        if diagnostic_refs:
            result_record["diagnostic_refs"] = copy.deepcopy(diagnostic_refs)
        serialized_results.append(result_record)

    serialized_diagnostics.extend(
        _diagnostic_record(diagnostic) for diagnostic in all_blockers
    )
    overall_outcome = aggregate_outcomes(
        tuple(result.outcome for result in run.results),
        decisive_structural_violation=decisive_structural_violation,
        blockers=all_blockers,
    )

    artifact: dict[str, Any] = {
        "binding": copy.deepcopy(ASSESSMENT_BINDING),
        "artifact_kind": ARTIFACT_KIND,
        "profile_edition": copy.deepcopy(dict(profile_edition)),
        "assessment_subject": copy.deepcopy(dict(assessment_subject)),
        "overall_outcome": overall_outcome,
        "requirement_results": serialized_results,
    }
    optional_values = (
        ("assessment_result_id", assessment_result_id),
        (
            "profile_requirement_artifact_reference",
            profile_requirement_artifact_reference,
        ),
        ("assessment_context", assessment_context),
        ("reference_scope", reference_scope),
    )
    for member, value in optional_values:
        if value is not None:
            artifact[member] = copy.deepcopy(value)
    if serialized_diagnostics:
        artifact["diagnostics"] = serialized_diagnostics
    if assessor_metadata is not None:
        artifact["assessor_metadata"] = copy.deepcopy(assessor_metadata)

    _validate_constructed_artifact(artifact)
    return artifact
