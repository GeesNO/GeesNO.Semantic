# AI Context Assessment Result Conformance 0.1

This directory contains deterministic conformance fixtures for the
`ai-context-assessment-json` binding, edition `0.1.0`.

The assessment-result corpus is separate from the AI Context Profile and
Projection acceptance corpus. It verifies supported assessment-result
representation and binding-local integrity without creating semantic truth.

```text
fixture filename
!= normative identity

fixture expectation
!= evaluator-derived semantic truth

repository-local checker output
!= conformance_result_artifact
```

The JSON fixtures contain only supported binding grammar.

The technical corpus catalogue documents all 58 assessment cases,
their fixed expectations and their coverage boundaries:

- [AI Context assessment corpus catalogue](../../../../conformance/ai-context-assessment-corpus.md)

The materialized fixtures and deterministic Python tests provide
executable coverage; the catalogue is the human-readable reference.

## Valid Assessment Result Artifacts

The following twelve JSON fixtures are expected to pass structural
assessment-result binding validation.

| ID | Fixture | Expected result |
| --- | --- | --- |
| `V01` | `valid/v01-minimal-stable-conformant.json` | Pass structural binding validation. |
| `V02` | `valid/v02-stable-violation-diagnostic.json` | Pass structural binding validation. |
| `V03` | `valid/v03-profile-subject-unsupported.json` | Pass structural binding validation. |
| `V04` | `valid/v04-semantic-document-unavailable.json` | Pass structural binding validation. |
| `V05` | `valid/v05-not-applicable-neutral.json` | Pass structural binding validation. |
| `V06` | `valid/v06-package-local-subject.json` | Pass structural binding validation. |
| `V07` | `valid/v07-coupled-subject.json` | Pass structural binding validation. |
| `V08` | `valid/v08-stable-profile-artifact-locator.json` | Pass structural binding validation. |
| `V09` | `valid/v09-package-local-profile-artifact-locator.json` | Pass structural binding validation. |
| `V10` | `valid/v10-coupled-profile-artifact-locator.json` | Pass structural binding validation. |
| `V11` | `valid/v11-diagnostic-taxonomy-and-typed-references.json` | Pass structural binding validation; representation coverage only. |
| `V12` | `valid/v12-enumeration-blocked-context-metadata.json` | Pass structural validation and applicable temporal validation. |

Structural validity does not by itself establish complete semantic
conformance.

## Invalid Assessment Result Artifacts

The following twenty-two JSON fixtures are expected to be rejected at
their respective validation boundaries.

| IDs | Fixtures | First rejecting validation boundary |
| --- | --- | --- |
| `I01-I18` | `invalid/i01-*.json` through `invalid/i18-*.json` | Structural JSON binding validation. |
| `I19` | `invalid/i19-invalid-gregorian-assessment-timestamp.json` | Gregorian temporal validation after structural acceptance. |
| `I20` | `invalid/i20-dangling-diagnostic-cross-reference.json` | Binding-local reference integrity. |
| `I21` | `invalid/i21-duplicate-requirement-occurrence.json` | Binding-local duplicate occurrence integrity. |
| `I22` | `invalid/i22-ambiguous-local-reference-declaration.json` | Binding-local declaration integrity. |

The repository-local validation component is:

- [`tools/validation/ai_context_assessment_corpus.py`](../../../../tools/validation/ai_context_assessment_corpus.py)

It checks the exact fixture inventory, structural schema outcomes,
applicable Gregorian temporal validity and the binding-local integrity
rules exercised by `I20-I22`.

The checker does not require network access, a registry, a resolver,
a model provider or hidden execution state.

## Requirement-Assessment Scenarios

The assessment corpus also includes twenty-four requirement-assessment
scenarios, identified as `S01-S24`.

These scenarios are not serialized into invented Profile artifacts.
They are exercised by repository-local tests against established
AI Context Profile artifacts and explicit non-serialized micro-scenarios.

The scenarios cover two distinct concerns:

- Requirement-level assessment against an exact Profile edition.
- Aggregation and construction of assessment-result artifacts.

These responsibilities remain separate from structural JSON binding
validation.

The scenarios do not imply a general assessment runtime, public CLI,
network service or required SDK.

## Conformance Boundary

Assessment-result conformance must distinguish structural validity,
binding-local integrity and requirement-level evaluation.

```text
schema-valid
!= complete conformance

fixture expectation
!= semantic authority

assessment result
!= semantic truth

assessment result
!= execution authorization
```

Assessment-result artifacts report the outcome of an assessment under
the applicable contract. They do not create Review, permission or
execution authority.

The normative contract is defined by:

- [AI Context Assessment JSON Binding](../../../../spec/ai-context-assessment-json-binding.md)
- [AI Context Profile](../../../../spec/ai-context-profile.md)
- [AI Context JSON Binding](../../../../spec/ai-context-json-binding.md)

For the broader public conformance model, see:

- [Conformance Guide](../../../../docs/conformance-guide.md)

The corpus is deterministic and usable offline. The reference
implementation is non-normative.
