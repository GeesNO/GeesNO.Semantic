# AI Context Assessment JSON binding 0.1

**Binding edition:** `ai-context-assessment-json/0.1.0` (normative assessment-result JSON representation).

This document concretizes the assessment-result representation accepted by
ADR-0030 for:

```text
binding.family  = https://geesno.com/binding/ai-context-assessment-json
binding.version = 0.1.0
artifact_kind   = conformance_result_artifact
```

The binding family and binding version are separate values. The string
`https://geesno.com/binding/ai-context-assessment-json/0.1.0` is not the
binding identity defined here.

This specification defines the closed JSON member names, cardinalities, tagged
unions, tokens and representation constraints for assessment results. It does not
define JSON Schema, fixtures, an evaluator, aggregation code, a diagnostic
engine, a CLI, an SDK or runtime behavior.

The specification defines the accepted assessment-result binding grammar.
JSON Schema validates the structurally expressible part of that grammar;
it does not originate semantics or extend the binding.

The public architectural baseline is
[ARCHITECTURE.md](../ARCHITECTURE.md). Accepted ADRs and applicable normative
specifications remain authoritative in their respective scopes.

## Normative authority map

| Binding subject | Normative authority |
| --- | --- |
| Deterministic conformance and specification-before-schema authority | `ARCHITECTURE.md`; ADR-0028; ADR-0030 |
| Exact Profile identity and Profile/Core conformance separation | ADR-0024 |
| Projection and preservation semantics reported by assessment | ADR-0025 through ADR-0027 |
| Requirement modes, applicability, exact Vocabulary semantics, unsupported and unavailable | ADR-0028 |
| AI Context Profile requirement and Projection JSON binding conventions | ADR-0029 and `ai-context-json-binding.md` |
| Assessment artifact, outcomes, aggregation, references and diagnostics | ADR-0030 |
| Single-subject assessment and composite Profile exclusion | ADR-0031 |

Cardinalities and JSON shapes below are representational concretions inside the
accepted ADR-0030 member groups. They add no result state, identity kind, reference
strategy, diagnostic meaning or aggregation rule.

## Controlling distinctions

```text
conformance result
!= semantic truth
!= Review
!= permission
!= execution authorization

diagnostic
!= Assertion
!= Review
!= Confidence
!= Provenance

severity
!= conformance outcome

assessment result
!= assessed artifact mutation

Profile conformance
!= bare-core conformance

local reference
!= semantic identity

locator
!= semantic identity
!= requirement identity
```

One result artifact assesses exactly one subject against exactly one exact
Profile edition. Binding `0.1.0` defines no multi-subject result, multi-Profile
aggregate, composition result or result inheritance.

## Notation and general JSON rules

Cardinality notation is:

```text
[1]     exactly one, required
[0..1]  zero or one, optional
[0..*]  finite array, zero or more
[1..*]  finite non-empty array
```

The following rules apply throughout binding `0.1.0`:

1. Every binding-defined object is closed. Unknown members are invalid.
2. Member names and closed tokens are case-sensitive and compared exactly.
3. A required member has no default. Its absence is invalid.
4. An absent optional member makes no claim and supplies no implicit value.
5. JSON `null` never substitutes for absence or for a binding-defined value.
6. Optional arrays, when present, are non-empty. The required
   `requirement_results` array is expressly `[0..*]` and may be empty only under
   the enumeration-blocked rule below.
7. Array order creates no identity, priority, precedence, aggregation order,
   truth or execution order.
8. Duplicate JSON object member names are invalid under the accepted raw-input
   rules.
9. IRIs, locators and reference tokens are inert data and are never automatic
   dereference or execution instructions.
10. The binding defines no byte-canonical JSON form and no member ordering.
11. Binding `0.1.0` has no generic Extension member and does not reuse Core 0.1 JSON
    `extensions`.

An **absolute IRI string** reuses the accepted Core 0.1 JSON identifier lexical and exact
comparison rules. A **non-empty token** is a non-empty JSON string compared
exactly. A **non-empty text string** is a non-empty JSON string whose text is
reporting content rather than a closed token.

A **Profile-defined context value** is any finite non-null JSON value inside
the binding-defined `context_value` slot. It is inert data. Object members or
array items inside that value are value content, not binding operators or new
assessment grammar. The exact Profile edition owns the value's admissibility
and meaning. Nested JSON `null` may occur only as Profile-defined value content
when that exact Profile permits it; `context_value` itself is never `null`.

Unless a table expressly identifies an object, array, boolean, absolute IRI,
Profile-defined context value or canonical UTC date-time, every token or code
in its Value column is a non-empty JSON string.

## Root artifact grammar

The `conformance_result_artifact` root is closed and contains only these
members:

| Path/member | Cardinality | JSON type | Conditional rule | Authority/notes |
| --- | --- | --- | --- | --- |
| `binding` | `[1]` | closed object | none | Exact assessment binding family and version. |
| `artifact_kind` | `[1]` | string constant | none | Exactly `conformance_result_artifact`. |
| `assessment_result_id` | `[0..1]` | absolute IRI string | none | Identity of this result artifact only. |
| `profile_edition` | `[1]` | closed object | none | One exact AI Context Profile edition. |
| `profile_requirement_artifact_reference` | `[0..1]` | closed tagged union | Required for locator-only requirement references unless explicit package/coupling context unambiguously supplies the exact concrete Profile artifact. | Not Profile edition identity. |
| `assessment_subject` | `[1]` | closed tagged union | none | One subject role and one reference strategy. |
| `assessment_context` | `[0..1]` | closed object | Omit when there are no context entries. | Explicit Profile-defined assessment context only. |
| `reference_scope` | `[0..1]` | closed object | Required when any assessment-local `local_reference` occurs; may also identify the explicit package/coupling context used for locator-only Profile artifact context. | One declared finite local scope per result. |
| `overall_outcome` | `[1]` | closed string token | none | `conformant`, `nonconformant` or `indeterminate`. |
| `requirement_results` | `[0..*]`, member required | array of closed requirement-result objects | Empty only when reliable requirement enumeration was blocked; diagnostics must explain the blocker. | One item per exact Profile requirement occurrence, never per source member. |
| `diagnostics` | `[1..*]` when present | array of closed diagnostic objects | Required and non-empty when an empty `requirement_results` array needs to report the enumeration blocker. | No diagnostic is required for every requirement result. |
| `assessor_metadata` | `[0..1]` | closed non-empty object | Omit when no metadata member is supplied. | Reporting only; never aggregation input. |

Unknown root members are invalid binding structure. In particular, the root
does not admit `extensions`, `profile_editions`, `component_profiles`,
`merged_results`, `aggregate_result`, `composition_outcome`, execution data or
arbitrary metadata.

## Common scalar representations

| Scalar role | JSON representation | Constraints |
| --- | --- | --- |
| Result or accepted artifact identity | absolute IRI string | Exact comparison; no automatic dereference or derivation. |
| `scope_ref`, `local_ref` | non-empty token | Binding-local only; not global identity. |
| `requirement_id` | non-empty token | Stable only inside the exact Profile edition. |
| `requirement_locator` | non-empty opaque string | Binding/artifact-scoped occurrence locator; no universal syntax. |
| diagnostic `locator` | non-empty opaque string | Reporting locator interpreted only in its declared diagnostic/artifact context. |
| `context_key` | non-empty Profile-defined exact token | No expression, selector, query, function or prompt semantics. |
| `implementation_name` | non-empty text string | Reporting only. |
| `implementation_version` | non-empty opaque string | No ordering or compatibility inference. |
| `message` | non-empty text string | Human-readable, optional and non-authoritative. |
| `assessment_timestamp` | canonical UTC date-time string | Same lexical instant convention as the accepted Core 0.1 JSON date-time value: valid Gregorian `YYYY-MM-DDTHH:MM:SS[.fraction]Z`, with no trailing fractional zero. |

`assessment_timestamp` records a supplied assessment time only. It is not
current-time applicability, semantic truth, a reproducibility requirement or a
request to generate wall-clock state.

## Binding header

`binding [1]` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `family` | `[1]` | exact string `https://geesno.com/binding/ai-context-assessment-json` |
| `version` | `[1]` | exact string `0.1.0` |

No `latest`, `0.1`, range, alias, alternate family or inferred compatibility is
valid.

## Artifact kind and result identity

`artifact_kind [1]` is exactly `conformance_result_artifact`. AI Context Profile
requirement artifacts, Projection artifacts, SemanticDocuments, benchmark
evidence and composition/aggregate results do not use this artifact kind.

`assessment_result_id [0..1]`, when present, is an absolute IRI identifying
this result artifact. It is not subject identity, Profile identity, requirement
identity, Review identity, a content hash or an automatically derived value.

## Profile edition

profile_edition [1] reuses the AI Context JSON binding's closed representation:

| Member | Cardinality | Value |
| --- | --- | --- |
| `profile_family` | `[1]` | exact string `https://geesno.com/profile/ai-context` |
| `profile_version` | `[1]` | non-empty exact opaque version token other than `latest` |

The pair identifies one exact immutable Profile edition. Ranges, aliases,
`profile.family`, `profile.version`, `profile_uri`, `profile_editions` and
automatic substitution are invalid.

## Local reference and reference scope

`local_reference` is the only assessment-local reference primitive. It is a
closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `scope_ref` | `[1]` | non-empty local scope token |
| `local_ref` | `[1]` | non-empty occurrence token within that scope |

```text
local_reference
!= semantic identity
!= portable global reference

scope_ref
!= global namespace
```

`reference_scope [0..1]` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `scope_ref` | `[1]` | non-empty local scope token |
| `scope_kind` | `[1]` | `result_artifact_scope`, `assessment_package_scope` or `explicit_coupling_scope` |

When any `local_reference` occurs in the result, `reference_scope` is required
and every such `local_reference.scope_ref` must equal the declared root
`reference_scope.scope_ref`. A local reference must resolve exactly once to an
occurrence of the expected referent kind inside that finite scope.

`coupled_subject` or `coupled_profile_requirement_artifact` requires
`scope_kind = explicit_coupling_scope`. An assessment-local artifact reference
uses `assessment_package_scope` or `explicit_coupling_scope`. Result-local
requirement-result and diagnostic references may use
`result_artifact_scope`; when a package/coupling scope already governs the
result, they use that same single declared scope.

The scope is never inferred from a path, folder, URL or current process. The
object defines no ZIP, MIME, manifest, transport, registry, resolver or content
integrity mechanism.

## Artifact reference tagged unions

### Assessment subject

`assessment_subject [1]` is closed. `subject_role [1]` is exactly one of:

```text
profile_requirement_artifact
projection_artifact
semantic_document
```

It also contains exactly one reference-strategy branch:

| `reference_strategy` discriminator | Required value slot | Forbidden alternate slots | Scope/meaning |
| --- | --- | --- | --- |
| `stable_artifact_identity` | `artifact_id [1]` as absolute IRI | `local_reference`, `coupled_occurrence_ref` | Carries an already accepted stable identity for that subject artifact. |
| `assessment_local_artifact_reference` | `local_reference [1]` | `artifact_id`, `coupled_occurrence_ref` | Identifies one supplied subject occurrence in the declared package/coupling scope. |
| `coupled_subject` | `coupled_occurrence_ref [1]` as `local_reference` | `artifact_id`, `local_reference` | Identifies the explicitly coupled subject occurrence in an `explicit_coupling_scope`. |

`subject_role`, `reference_strategy` and the selected value slot are required.
No other member is allowed. A strategy without its slot, multiple slots or a
slot from another branch is invalid.

`artifact_id` transports stable identity already accepted for the subject type.
It does not create identity for an artifact that lacks one. A path, URL used as
location, digest, filename, locator or local token does not become
`artifact_id` merely by being placed in that slot.

### Profile requirement artifact reference

`profile_requirement_artifact_reference [0..1]` is closed and has exactly one
branch:

| `reference_strategy` discriminator | Required value slot | Forbidden alternate slots | Scope/meaning |
| --- | --- | --- | --- |
| `stable_artifact_identity` | `artifact_id [1]` as absolute IRI | `local_reference`, `coupled_occurrence_ref` | Carries an already accepted stable identity of the concrete Profile requirement artifact. |
| `assessment_local_artifact_reference` | `local_reference [1]` | `artifact_id`, `coupled_occurrence_ref` | Identifies the artifact occurrence in the declared package/coupling scope. |
| `coupled_profile_requirement_artifact` | `coupled_occurrence_ref [1]` as `local_reference` | `artifact_id`, `local_reference` | Identifies the explicitly coupled artifact occurrence in an `explicit_coupling_scope`. |

This member identifies a concrete artifact occurrence and never replaces
`profile_edition`.

If any `requirement_ref` uses `locator_occurrence_reference`, the exact concrete
Profile requirement artifact context must be unambiguous. The root member is
required unless an explicit package/coupling scope unambiguously couples
exactly one matching Profile requirement artifact. A bare locator plus
`profile_edition` is insufficient artifact context.

## Assessment context

`assessment_context [0..1]` is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `context_entries` | `[1..*]` | array of closed context-entry objects |

Each context entry is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `context_key` | `[1]` | non-empty Profile-defined exact token |
| `context_value` | `[1]` | finite non-null Profile-defined context value |

An empty assessment-context container is invalid and must be omitted. The
binding owns the two entry slots; the exact Profile edition owns each key's
meaning, admissible value shape and any key-level cardinality. Binding `0.1.0`
does not make context keys expressions, selectors, queries, functions, code,
prompts or evaluator plug-ins.

Duplicate `context_key` values are not universally prohibited by the binding,
because the exact Profile may define a repeatable key. They are invalid when
the exact Profile defines that key as singular or when the supplied entries do
not satisfy its deterministic context rule.

## Requirement result collection

`requirement_results` is a required finite JSON array with zero or more items.
Each item reports exactly one requirement occurrence from the exact Profile
edition. It never represents one failing source record, member or diagnostic.

The array may be empty only when reliable requirement enumeration was blocked,
for example by unavailable required Profile artifact context or uninterpretable
input. No requirement results may be fabricated. A non-empty `diagnostics`
array must explain the blocker using the accepted taxonomy. Empty results do
not create a new requirement outcome and do not by themselves choose the
overall outcome; the aggregation and structural rules of ADR-0030 remain controlling.

Each requirement-result object is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `requirement_ref` | `[1]` | closed requirement-reference tagged union |
| `outcome` | `[1]` | `satisfied`, `violated`, `not_applicable`, `unsupported` or `unavailable` |
| `diagnostic_refs` | `[1..*]` when present | array of `local_reference` objects resolving to diagnostics |
| `requirement_result_ref` | `[0..1]` | `local_reference` identifying this result occurrence |

`requirement_mode` is not assessment-result grammar. Mode authority remains in
the exact Profile requirement.

Requirement result order does not affect aggregation. Exactly one result may
represent a given requirement occurrence. Two results using the same stable
requirement reference, or the same locator in the same concrete Profile
artifact context, are a duplicate occurrence result and invalid.

`requirement_result_ref`, when present, declares an assessment-local occurrence
reference. It is not requirement identity, `requirement_id`, array position or
JSON Pointer identity and never replaces `requirement_ref`.

## Requirement reference tagged union

`requirement_ref` is a closed object with exactly one branch:

| `reference_strategy` discriminator | Required value slot | Forbidden alternate slot | Scope/meaning |
| --- | --- | --- | --- |
| `stable_requirement_reference` | `requirement_id [1]` as non-empty token | `requirement_locator` | Stable requirement identity scoped to the exact Profile edition. |
| `locator_occurrence_reference` | `requirement_locator [1]` as non-empty opaque string | `requirement_id` | Occurrence locator scoped to the exact concrete Profile requirement artifact. |

The selected discriminator and value slot are required. Plain strings are not
valid `requirement_ref` values.

`requirement_locator` has no universal path syntax. It may carry a JSON Pointer,
binding-specific path or another opaque local spelling only when the concrete
Profile artifact binding defines how to interpret that spelling. This binding
does not elevate any such spelling into universal requirement identity, a query
language or a navigation language.

Array index, processing order, file line, diagnostic path and JSON Pointer are
never universal requirement identity.

## Overall outcomes and aggregation

`overall_outcome [1]` is exactly one of:

```text
conformant
nonconformant
indeterminate
```

Requirement-level `outcome [1]` is exactly one of:

```text
satisfied
violated
not_applicable
unsupported
unavailable
```

No `warning`, `error`, `passed`, `failed`, `partial`, `unknown`, `skipped` or
`invalid_input` outcome exists.

The accepted interpretation remains:

1. A decisive applicable requirement or structural violation yields
   `nonconformant`, including when another requirement is `unsupported` or
   `unavailable`.
2. Otherwise, an applicable `unsupported` or `unavailable` result, or a
   structural/interpretation blocker, yields `indeterminate` unless the exact
   Profile defines and satisfies an explicit offline-safe alternative.
3. Otherwise, deterministic resolution of every applicable requirement with
   no violation or blocker yields `conformant`.
4. `not_applicable` is neutral and is not `satisfied`.
5. Severity and array order never participate in aggregation.

Optional absence allowed by the exact requirement may be `satisfied` when the
requirement is applicable and deterministically evaluable. Present-but-invalid
optional material may be `violated`. Applicable optional `unsupported` or
`unavailable` requirements are not silently ignored.

This specification represents those outcomes and interpretation rules; it does
not implement an evaluator or aggregation engine.

## Diagnostic collection and records

`diagnostics [0..1]` is a finite array. When present it is non-empty. Absence and
an empty array carry no accepted semantic distinction, so an empty array is
invalid and the member must be omitted.

A diagnostic record is closed and contains exactly these possible members:

| Member | Cardinality | Value |
| --- | --- | --- |
| `diagnostic_ref` | `[0..1]` | `local_reference` identifying this diagnostic occurrence |
| `diagnostic_code` | `[1]` | accepted exact diagnostic code |
| `diagnostic_category` | `[1]` | category required by the code table |
| `requirement_ref` | `[0..1]` | closed requirement-reference tagged union |
| `requirement_result_ref` | `[0..1]` | `local_reference` resolving to a requirement result |
| `subject_ref` | `[0..1]` | closed subject-reference tagged union |
| `diagnostic_severity` | `[0..1]` | `info`, `warning` or `error` |
| `message` | `[0..1]` | non-empty human-readable text string |
| `locator` | `[0..1]` | non-empty opaque diagnostic locator string |
| `related_refs` | `[1..*]` when present | array of closed related-reference tagged unions |

No diagnostic is required for every requirement result. A diagnostic that is
referenced by `diagnostic_refs` or another local reference must declare a
resolving `diagnostic_ref`.

`locator` is interpreted only as a reporting aid in the artifact/referent
context established by the diagnostic and result. It defines no universal JSON
Pointer, XPath, filesystem path, line/column, URI-fragment or navigation
language and is not identity.

Diagnostics cannot contain stack traces, exceptions, tools, models, prompts,
providers, commands, execution traces, GUI state or product-specific error
objects as binding `0.1.0` grammar.

### Subject reference tagged union

Diagnostic and related `subject_ref` is closed and has exactly one branch:

| `reference_strategy` discriminator | Required value slot | Forbidden alternate slot | Scope/meaning |
| --- | --- | --- | --- |
| `stable_artifact_identity` | `artifact_id [1]` as absolute IRI | `local_reference` | Refers to the subject through its accepted stable artifact identity. |
| `assessment_local_artifact_reference` | `local_reference [1]` | `artifact_id` | Refers to the subject occurrence in the declared local scope, including a coupled subject occurrence. |

The root `assessment_subject` remains the authority for the assessed subject
role and coupling strategy. `subject_ref` does not introduce a new subject role
or identity grammar.

### Related reference tagged union

Each `related_refs` item is a closed object. `related_ref_kind` categorizes the
referent, not a semantic relation or predicate:

| `related_ref_kind` discriminator | Required value slot | Forbidden alternate slots | Scope/meaning |
| --- | --- | --- | --- |
| `assessment_record` | `local_reference [1]` | `subject_ref`, `requirement_ref`, `requirement_result_ref`, `diagnostic_ref` | Related assessment-local record occurrence. |
| `subject` | `subject_ref [1]` | `local_reference`, `requirement_ref`, `requirement_result_ref`, `diagnostic_ref` | Related stable or assessment-local subject occurrence. |
| `requirement` | `requirement_ref [1]` | `local_reference`, `subject_ref`, `requirement_result_ref`, `diagnostic_ref` | Related exact Profile requirement occurrence. |
| `requirement_result` | `requirement_result_ref [1]` as `local_reference` | `local_reference`, `subject_ref`, `requirement_ref`, `diagnostic_ref` | Related assessment-local requirement-result occurrence. |
| `diagnostic` | `diagnostic_ref [1]` as `local_reference` | `local_reference`, `subject_ref`, `requirement_ref`, `requirement_result_ref` | Related assessment-local diagnostic occurrence. |

`related_refs` cannot be an array of strings. These categories identify only
what kind of referent is pointed to. They do not define `caused_by`,
`depends_on`, `derived_from`, `supersedes` or another semantic edge. The array
does not create a generic graph.

## Diagnostic taxonomy

Binding `0.1.0` defines exactly these code/category pairs:

| `diagnostic_code` | `diagnostic_category` | Meaning |
| --- | --- | --- |
| `requirement_violated` | `requirement_evaluation` | An applicable evaluable requirement is violated. |
| `requirement_unsupported` | `requirement_evaluation` | A valid requirement construct is not supported by the assessor. |
| `dependency_unavailable` | `dependency_availability` | A required local dependency is unavailable for assessment. |
| `requirement_not_applicable` | `requirement_evaluation` | A requirement is deterministically not applicable and the assessor chooses to report it. |
| `invalid_binding_construct` | `binding_structure` | Input uses a construct outside the declared binding grammar. |
| `unsupported_binding_construct` | `binding_structure` | Input uses a valid binding construct whose representation/processing support is not implemented. |
| `contradictory_projection_metadata` | `binding_structure` | Projection metadata contradicts accepted AI Context JSON binding member-group semantics. |
| `exact_vocabulary_unavailable` | `dependency_availability` | The exact Vocabulary edition needed for deterministic assessment is unavailable locally. |
| `profile_requirement_artifact_unavailable` | `dependency_availability` | The exact Profile requirement artifact needed for local assessment is unavailable. |
| `unresolved_requirement_reference` | `requirement_reference` | A result or diagnostic cannot resolve its exact requirement reference. |
| `missing_namespace_expansion_context` | `binding_structure` | Compact qualified terms lack required namespace expansion context. |
| `invalid_reference_availability_consistency` | `binding_structure` | Reference availability contradicts carried/omitted/reference state. |
| `invalid_source_state_reference_preservation` | `binding_structure` | Source-state or reference preservation contradicts accepted Projection and binding rules (ADRs 0025-0029). |
| `structural_validation_failed` | `binding_structure` | Required binding structure is invalid without universalizing every schema error. |
| `assessment_input_uninterpretable` | `assessment_input` | Subject/Profile input cannot be interpreted enough for deterministic assessment. |

No additional code or category belongs to binding `0.1.0`. Each code must use
the category paired with it above.

`diagnostic_severity [0..1]` is exactly `info`, `warning` or `error`:

```text
severity
!= conformance outcome
!= requirement mode
!= truth
!= execution priority
```

`warning` does not imply `conformant`; `error` does not imply
`nonconformant`.

## Assessor metadata

`assessor_metadata [0..1]` is a closed object with at least one member when
present:

| Member | Cardinality | Value |
| --- | --- | --- |
| `assessor_id` | `[0..1]` | absolute IRI identifying the assessor for reporting |
| `implementation_name` | `[0..1]` | non-empty text string |
| `implementation_version` | `[0..1]` | non-empty opaque string |
| `assessment_timestamp` | `[0..1]` | canonical UTC date-time string |

These values do not affect Profile identity, applicability, requirement
semantics, aggregation or conformance. No other metadata slot is valid under
binding `0.1.0`.

## Closed-object inventory

The following binding-defined objects are closed:

```text
root conformance_result_artifact
binding
profile_edition
local_reference
reference_scope
assessment_subject
profile_requirement_artifact_reference
assessment_context
context_entry
requirement_result
requirement_ref
diagnostic
subject_ref
related_ref
assessor_metadata
```

Unknown members are invalid except inside `context_value`, which is explicitly
Profile-defined finite non-null value content. That value is not an Extension
mechanism and cannot override binding-defined members.

## Arrays, ordering and duplicates

| Array | Requiredness/emptiness | Order | Duplicate rule |
| --- | --- | --- | --- |
| `requirement_results` | required, empty only when enumeration is blocked | no aggregation or identity meaning | one item per requirement occurrence; duplicate occurrence results invalid |
| `diagnostic_refs` | optional, non-empty when present | no priority meaning | repeated references add no meaning; exact duplicates are invalid redundancy |
| `diagnostics` | optional, non-empty when present | no outcome/priority meaning | duplicate declared `diagnostic_ref` invalid |
| `related_refs` | optional, non-empty when present | no graph/priority meaning | exact duplicate references are invalid redundancy |
| `context_entries` | required inside present context, non-empty | no binding-level precedence | key uniqueness/cardinality belongs to the exact Profile; conflicting singular-key duplicates are invalid under that Profile |

Within one declared scope, a `local_ref` that is declared as the occurrence
reference for a result-local requirement result or diagnostic must identify
exactly one occurrence. Reusing the same declared local token for different
occurrences is invalid binding-local ambiguity. This is local reference
integrity, not semantic uniqueness.

No universal uniqueness rule is created for Profile-defined context keys or
for referents that have no declared local identity. Consumers must not infer
importance or multiplicity semantics from repeated array positions.

## Reference resolution and portability

All assessment-local resolution is deterministic lookup inside the declared
finite scope. It never performs network access, registry lookup, IRI
dereference, filesystem discovery, latest-edition selection or semantic
similarity.

A detached result with a subject that lacks accepted stable artifact identity
is portable only when an explicit package/coupling scope identifies the subject
occurrence unambiguously. File path, URL as location, digest, locator and
`local_ref` without its scope are insufficient. This binding creates no hash
identity.

Locator-based requirement references similarly require unambiguous concrete
Profile artifact context. Profile edition identity alone does not identify one
artifact occurrence.

## Invalid or uninterpretable input

Binding `0.1.0` defines no requirement-level `invalid_input`, `error` or
`failed` outcome. When assessment input cannot be interpreted reliably, the
overall result is `indeterminate` with accepted structural, dependency or
assessment-input diagnostics unless a decisive applicable violation has already
been established under ADR-0030.

If reliable requirement enumeration is impossible, `requirement_results` is
the required empty array and diagnostics explain the blocker. The empty array
does not mean that the exact Profile has no requirements, that every requirement
is satisfied or that missing requirements are `not_applicable`.

## Offline and security boundary

The binding is interpretable from locally supplied artifacts, locally built-in
exact-edition support and explicit assessment context. It defines no automatic:

- Profile or Vocabulary download;
- dependency fetch;
- registry or resolver call;
- network access;
- model invocation;
- semantic-similarity decision;
- prompt execution;
- tool or command execution.

An IRI or URL transported as identity or opaque locator remains inert data and
is not a retrieval command. Semantic text, messages, locators and context values
are untrusted non-executable input.

## Profile-composition and implementation boundaries

Binding `0.1.0` contains no `profile_editions`, components, merged requirements,
aggregate outcomes, composition conflicts, inheritance, override or precedence.
An explicitly authored composite Profile edition accepted under ADR-0031 may be
assessed under ADR-0030 only when a future accepted Profile binding version can represent
that edition; this specification does not add that representation.

This specification defines no `evaluate()`, `validate()`, `load_profile()`,
`resolve()` or `fetch()` API, no public CLI and no SDK/runtime contract.

## Binding representation decisions

| Point | Representation decision | Reason | Authority boundary | Rejected interpretation |
| --- | --- | --- | --- | --- |
| Root cardinalities | Preserve every ADR-0030 root group; `requirement_results` is a required `[0..*]` array and other `?` groups remain optional. | Gives structural validation one stable root while preserving zero reliable results when enumeration is blocked. | Representation only; no new outcome. | Omit/fabricate results or add root members. |
| Empty arrays | Optional arrays are non-empty; only required `requirement_results` may be empty under the blocker rule. | Absent and present-empty have no accepted distinction for optional collections. | Reuses the accepted AI Context JSON binding convention. | Empty optional containers gain semantics. |
| Requirement locator | `requirement_locator` is a non-empty opaque string in the locator tagged-union branch. | Minimum transport without a universal path/query language. | Concrete Profile artifact binding supplies interpretation. | Locator becomes requirement identity or universal JSON Pointer. |
| Diagnostic locator | `locator` is a non-empty opaque reporting string. | Supports artifact/member location without universal navigation semantics. | Diagnostic context supplies interpretation. | Path, line or URI fragment becomes identity. |
| `related_refs` | Closed `related_ref_kind` union with five referent categories and one typed value slot. | Distinguishes referent kind without inventing semantic predicates or a graph. | Exactly the ADR-0030 referent categories. | Strings or `caused_by`/`depends_on` edges. |
| `context_value` | Any finite non-null JSON value in the labelled slot. | Reuses the accepted AI Context JSON Profile-defined-value convention. | Exact Profile defines admissible shape and meaning. | Value becomes code, query, prompt or binding grammar. |
| `reference_scope` | One optional root scope, required for any local reference; all local scope tokens must match it. | Makes local lookup explicit and deterministic. | No packaging/transport semantics. | Scope inferred from environment or path. |
| Profile artifact reference | Required for locator-only requirement refs unless explicit package/coupling context unambiguously supplies exactly one concrete matching artifact. | Preserves the ADR-0030 locator context rule. | Artifact occurrence is distinct from Profile edition identity. | Bare locator or edition pair identifies artifact occurrence. |
| Null | `null` is invalid for optional absence and all binding-defined values; `context_value` is expressly non-null. | Reuses the accepted AI Context JSON absence convention. | No condition/unknown semantics added. | `null` silently means absent or unknown. |
| Duplicates | Reject duplicate object names, duplicate requirement occurrence results and ambiguous duplicate local declarations; defer Profile context-key cardinality to the exact Profile. | Prevents binding-local ambiguity without inventing semantic uniqueness. | Local integrity only. | Array position or repetition creates identity/priority. |

These representation decisions operate within the accepted ADR-0030 member
groups. A future construct requiring a new state, identity, reference strategy,
diagnostic meaning or aggregation rule requires separate accepted normative
authority and cannot be introduced through schema-only changes.

## JSON Schema and implementation boundary

JSON Schema may encode the structural and locally expressible constraints of
this binding, but neither schema nor implementation may independently:

- add or rename members, branches, codes, categories or outcomes;
- loosen closed objects with generic additional members;
- derive outcome from severity;
- infer identity from a locator or local reference;
- introduce packaging, resolver, SDK or execution semantics;
- implement normative Profile composition without its accepted exact binding;
- create another binding or Profile edition.

See [conformance.md](conformance.md) and
[ai-context-json-binding.md](ai-context-json-binding.md) for the applicable
conformance and Profile/Projection representation boundaries.
