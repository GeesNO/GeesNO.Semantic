# AI Context JSON Schemas 0.1

This directory contains the Draft 2020-12 JSON Schemas for the
AI Context JSON and AI Context Assessment JSON bindings, edition `0.1.0`.

The schemas validate supported representations. They do not originate,
extend or override the semantic contracts defined by the applicable
binding specifications.

## AI Context Profile and Projection Schema

The dispatch schema for `ai-context-json/0.1.0` is:

- [`v0.1/ai-context.schema.json`](v0.1/ai-context.schema.json)

It accepts exactly two root artifact roles:

- `profile_requirement_artifact`
- `projection_artifact`

Binding-defined objects are closed, exact binding and Profile constants
are enforced, and the eight supported requirement kinds use
kind-selected bodies.

Profile-defined values remain inert data and cannot introduce new
binding operators or executable behavior.

The schema implements the structural constraints and conditionals
defined by the normative
[AI Context JSON Binding specification](../../../spec/ai-context-json-binding.md).

These include:

- root artifact dispatch;
- exact binding and Profile versions;
- closed binding-defined member sets;
- requirement-body dispatch;
- non-empty optional descriptor groups;
- truncation requiring `projection_completeness: "partial"`.

Structural schema validation does not by itself:

- assess Profile applicability or exact Vocabulary meaning;
- compare decimal cardinality bounds;
- resolve requirement or descriptor references;
- prove source-state consistency;
- establish accurate reference-availability coverage;
- assess material-context or completeness claims.

These concerns remain governed by the normative binding and Profile
specifications and their applicable deterministic validation rules.

## AI Context Assessment Result Schema

The structural schema for `ai-context-assessment-json/0.1.0` is:

- [`v0.1/ai-context-assessment.schema.json`](v0.1/ai-context-assessment.schema.json)

It validates the singular root role:

- `conformance_result_artifact`

The schema defines structural acceptance of supported assessment-result
representations. It does not constitute a result fixture corpus,
requirement evaluator, aggregation engine or diagnostic engine.

Schema validation does not independently:

- resolve binding-local references;
- compare scope tokens;
- prove package or coupling contents;
- enforce Profile-defined context cardinality;
- derive requirement-level or aggregate outcomes.

The corresponding deterministic integrity and semantic-validation
responsibilities remain separate from structural JSON validation.

The normative authority is the
[AI Context Assessment JSON Binding specification](../../../spec/ai-context-assessment-json-binding.md).

## Offline Schema References

The schemas intentionally do not declare a public `$id`.

The absence of `$id` must not be interpreted as assigning a repository
path or retrieval URL as the normative schema identity.

References to the supported GeesNO.Semantic Core records use the
relative offline schema resource:

```text
../../../../schema/v0.1/geesno-semantic.schema.json
```

Repository-local tests supply that resource through a local
`referencing.Registry`.

Schema validation does not require network access, a remote resolver
or runtime dereferencing of semantic identifiers.

## Temporal Validation

Assessment timestamps follow the applicable layered temporal
validation model.

The JSON Schema enforces:

- canonical UTC `Z` spelling;
- hour, minute and second ranges;
- the prohibition of trailing fractional zeros.

Gregorian calendar validity is checked separately by the existing
deterministic Core temporal validator.

It is not redefined by a JSON Schema regular expression or a `format`
annotation.

```text
structural timestamp validity
!= complete Gregorian calendar validity
```

## Conformance and Test Coverage

Repository-local tests under:

- [`tools/validation/tests/`](../../../tools/validation/tests/)

provide non-normative schema validation checks.

The exact AI Context Profile artifact is available at:

- [`../v0.1/profile.json`](../v0.1/profile.json)

Assessment-result fixtures are maintained separately under:

- [`../assessment-conformance/v0.1/`](../assessment-conformance/v0.1/README.md)

The Profile and Projection acceptance corpus is distinct from the
assessment-result corpus.

The complete assessment corpus includes serialized valid and invalid
result artifacts as well as non-serialized semantic scenarios:

- [AI Context assessment corpus catalogue](../../../conformance/ai-context-assessment-corpus.md)

The catalogue documents 58 fixed cases and their expectations.
Applicable contracts, fixtures and deterministic tests determine
actual conformance.

## Architectural Boundary

```text
JSON Schema validity
!= complete semantic conformance

JSON Schema
!= semantic authority

Profile declaration
!= proof of Profile conformance
```

No general Profile composition schema is defined here.

The schemas are representation-specific validation artifacts. They do
not establish runtime execution, network requirements, a central
registry, a resolver, certification or endorsement.

For the applicable public architectural and conformance boundaries,
see:

- [ARCHITECTURE.md](../../../ARCHITECTURE.md)
- [Conformance Guide](../../../docs/conformance-guide.md)
