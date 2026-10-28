# ADR-0030: AI Context Profile conformance result and diagnostics

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-27
- **Date:** 2026-09-24
- **Decision order:** Seventh S4 architecture decision after ADR-0029 acceptance

## Context

ADR-0024 accepts exact AI Context Profile identity and the separation between
bare-core/S2 conformance and Profile conformance. ADR-0025 through ADR-0027
accept Projection, omission, boundedness, continuation, preservation and
material-context semantics. ADR-0028 accepts abstract Profile requirement
semantics: applicability, required/optional/prohibited modes, exact Vocabulary
policy, deterministic assessment, unsupported requirements and unavailable
dependencies. ADR-0029 accepts the concrete AI Context Profile/Projection
binding architecture for `profile_requirement_artifact` and `projection_artifact`
under `https://geesno.com/binding/ai-context-json` version `0.1.0`.

D7 must define how an assessor reports the deterministic assessment of one
subject against one exact Profile edition. D7 does not redefine Profile
requirements. It reports results for requirements accepted by D5 and represented
by D6.

D7 is architecture only. It does not create JSON Schema, normative fixtures, an
SDK, an evaluator, runtime behavior, diagnostics executable behavior, a registry,
a resolver, publication or release artifacts.

## Prerequisite review

D5 already defines the semantic boundary for requirement applicability,
required/optional/prohibited modes, exact Vocabulary dependencies,
deterministic assessment, unsupported requirements, unavailable dependencies and
violations. D7 must preserve these distinctions instead of collapsing them into a
binary validity result.

D6 already defines the Profile requirement artifact role, Projection artifact
role, exact Profile edition binding, optional `requirement_id`, binding grammar
ownership and the D7 diagnostics boundary. D7 must not modify D6 binding version
`0.1.0` by silently adding another artifact kind.

## Controlling distinctions

```text
conformance result
!= semantic truth

conformance result
!= Review

conformance result
!= permission

conformance result
!= execution authorization

diagnostic
!= semantic assertion

severity
!= conformance outcome

assessment artifact
!= assessed artifact mutation

Projection completeness
!= Profile conformance

assessment subject
!= source SemanticDocument automatically

assessment subject
!= Profile edition

assessment subject
!= diagnostic report

artifact reference
!= content integrity proof

diagnostic locator
!= semantic identity
```

## Definitions

**Assessment** means the deterministic evaluation of an explicitly identified
assessment subject against one exact Profile edition using locally available
artifacts and explicit assessment context.

**Assessment subject** means the artifact or SemanticDocument being assessed. A
subject has a required subject role. D7 recognizes these roles:

- `profile_requirement_artifact`;
- `projection_artifact`;
- `semantic_document`, when an exact Profile requirement applies directly to a
  SemanticDocument rather than a Projection artifact.

D7 does not automatically treat the source SemanticDocument referenced by a
Projection as the assessment subject.

**Conformance result artifact** means the D7 report artifact that records the
assessment subject, exact Profile edition, requirement-level outcomes, global
outcome and diagnostics. It is not the assessed artifact and does not mutate the
assessed artifact.

**Requirement-level outcome** means the finite assessment result for one Profile
requirement occurrence under the exact Profile edition.

**Overall outcome** means the finite aggregate outcome for the assessment as a
whole.

**Diagnostic** means a machine-readable explanatory record emitted by the
assessment. A diagnostic is not a Core Assertion, Review, Confidence,
Provenance, permission, execution authorization or semantic truth claim.

**Assessment-local artifact reference** means a reference used inside one result
artifact to identify a supplied artifact occurrence for reporting. It is not a
semantic ID, not a content-integrity proof and not portable outside the result
package unless accompanied by enough packaging context.

**Local reference scope** means an explicit finite assessment/package context
inside which assessment-local references identify artifact, result or diagnostic
occurrences. It is not a semantic namespace, registry, transport protocol or
packaging format.

**Local reference** means the binding-local structure used by assessment binding
`0.1.0` to identify one occurrence inside a declared local reference scope:

```text
local_reference:
  scope_ref
  local_ref
```

`scope_ref` identifies the applicable local reference scope. `local_ref`
identifies one occurrence inside that scope. Neither member is semantic identity,
content-integrity proof or portable outside the declared scope.

```text
local_ref
!= semantic identity

scope_ref
!= global namespace

local reference scope
!= packaging format
```

## Overall outcome alternatives

### Alternative A - Binary conformant/nonconformant

A binary result is rejected. A required and applicable requirement can be valid
but unsupported by an assessor, or can depend on a required exact Vocabulary
edition that is locally unavailable. Those cases do not prove a violation and do
not establish conformance.

### Alternative B - conformant/nonconformant/indeterminate

A three-state result is accepted. It preserves the distinction between established
conformance, established non-conformance and inability to conclude conformance
from deterministic local assessment.

### Alternative C - Add separate overall outcomes for unsupported and unavailable

This is rejected for the global outcome. Unsupported requirements and unavailable
dependencies are requirement-level or diagnostic distinctions. Multiplying global
outcomes would make aggregation less stable and would not change the core fact:
conformance cannot be concluded.

### Alternative D - not_assessed global outcome

This is rejected for valid result artifacts. If no assessment is performed, no
conformance result artifact should claim an assessment outcome. If assessment
starts but the input cannot be interpreted, D7 uses `indeterminate` with
structural diagnostics.

## Accepted decision

D7 defines a separate assessment/report binding family:

```text
binding.family  = https://geesno.com/binding/ai-context-assessment-json
binding.version = 0.1.0
artifact_kind   = conformance_result_artifact
```

This binding family is separate from ADR-0029
`https://geesno.com/binding/ai-context-json` version `0.1.0`.

Profile/Projection serialization is not assessment/report serialization. D7
therefore does not retrofit `conformance_result_artifact` into the accepted D6
binding version. A future accepted decision may define schema for this accepted
assessment binding, but ADR-0030 itself does not implement schema.

## Assessment binding grammar ownership

For assessment result artifacts:

```text
binding.family + exact binding.version
determines assessment binding grammar

JSON Schema
= validation of accepted assessment grammar

JSON Schema
!= origin of assessment grammar
```

A future Profile edition must not add slots, operators, result states,
diagnostic structures or assessment grammar under assessment binding version
`0.1.0`. An unknown assessment-json `0.1.0` member is not Profile-defined
assessment grammar. New assessment grammar requires a new accepted binding
version or a future accepted Extension mechanism.

For `https://geesno.com/binding/ai-context-assessment-json` version `0.1.0`, the
normative representational member groups are exactly the D7 member groups listed
below. A future schema may validate those accepted slots and tokens, but it must
not invent them for the first time. A future JSON Schema MUST NOT create
normative slots or tokens absent from accepted ADR-0030 grammar.

## Conformance result artifact model

A D7 result artifact conceptually contains these member groups:

```text
binding
artifact_kind
assessment_result_id?
profile_edition
profile_requirement_artifact_reference?
assessment_subject
assessment_context?
reference_scope?
overall_outcome
requirement_results
diagnostics?
assessor_metadata?
```

`binding` declares the assessment binding family and exact binding version. For
D7 this is `https://geesno.com/binding/ai-context-assessment-json` version
`0.1.0`.

`artifact_kind` is `conformance_result_artifact`.

`assessment_result_id` is optional. When present, it identifies the result
artifact for citation or interchange. It is distinct from Projection artifact ID,
SemanticDocument ID, Profile edition identity, Review ID and requirement ID. It
is not derived automatically from content.

`profile_edition` reuses exactly the D6 member spelling:

```text
profile_edition:
  profile_family
  profile_version
```

The pair declares the Profile family identity and exact Profile version used for
assessment. It does not use `latest`, ranges, resolver aliases, automatic fetch,
`profile.family` or `profile.version`.

`profile_requirement_artifact_reference` identifies the concrete locally supplied
Profile requirement artifact used during the assessment when such identification
is needed. It is not Profile edition identity and does not invent identity for
the Profile requirement artifact. It is a tagged union with exactly one of these
binding-defined alternatives:

```text
reference_strategy = stable_artifact_identity
artifact_id

reference_strategy = assessment_local_artifact_reference
local_reference

reference_strategy = coupled_profile_requirement_artifact
coupled_occurrence_ref = local_reference
```

`artifact_id` transports an accepted stable artifact identity when future
accepted architecture supplies one. `local_reference` identifies a Profile
requirement artifact occurrence inside a declared local reference scope.
`coupled_occurrence_ref` uses the same `local_reference` primitive, with
`scope_ref` resolving to an explicit coupling scope.

It is required in practice when any requirement reference relies only on a
binding-specific locator and the result is not explicitly coupled with that exact
Profile requirement artifact by packaging.

`assessment_subject` declares exactly one subject role and one subject reference
strategy for the assessed subject. Its closed tagged-union grammar is defined in
Subject identity and portable reporting.

`assessment_context` may carry explicit Profile-defined assessment context when
needed by accepted D5 applicability semantics. It uses the binding-defined
envelope:

```text
assessment_context:
  context_entries[]

context_entry:
  context_key
  context_value
```

The binding defines the `context_entries`, `context_key` and `context_value`
slots. The exact Profile edition may define the accepted meaning of a
`context_key` and the admissible values for that key when those semantics are
part of its requirements or applicability conditions.

```text
Profile-defined context value
!= Profile-defined binding grammar
```

Assessment context remains explicit, identifiable, deterministically assessable
and offline. It is not hidden runtime state, selector language, expression
language, query language, execution request or evaluator plug-in.

`reference_scope`, when present, declares or identifies a local reference scope
inside which assessment-local references are meaningful. Its binding-defined
minimum grammar is:

```text
reference_scope:
  scope_ref
  scope_kind = result_artifact_scope | assessment_package_scope | explicit_coupling_scope
```

`scope_ref` is the value local references use to identify this scope.
`scope_kind` states whether the scope is the current result artifact, a finite
assessment/package context or an explicit coupling context. If the result artifact
itself is the local scope, that possibility is represented explicitly with
`scope_kind = result_artifact_scope`; it is not left for schema to infer.

`reference_scope` does not define ZIP, folders, MIME, manifests, URLs, transport
protocol, global registry, global identity or content integrity.

`overall_outcome` is one of `conformant`, `nonconformant` or `indeterminate`.

`requirement_results` is a finite array. Each result corresponds to one
requirement occurrence from the exact Profile requirement set, not to each
matching source record, target record or member occurrence. Record/member-specific
failures are represented through diagnostics and locators.

A requirement result contains at minimum:

- `requirement_ref`, using the D7 tagged union `stable_requirement_reference`
  when stable `requirement_id` exists or `locator_occurrence_reference` when no
  stable requirement ID exists;
- `outcome`, one of the D7 requirement-level outcomes;
- optional `diagnostic_refs`, each using `local_reference` to point to a
  diagnostic occurrence that explains the result;
- optional `requirement_result_ref`, using `local_reference` only when diagnostics
  or related records need to cross-reference a particular requirement result.

`requirement_results` must not duplicate `requirement_mode` as semantic
authority. The mode belongs to the exact Profile requirement. If a future binding
or report serializes a mode echo as presentation convenience, the echo is
non-authoritative and the exact requirement remains the authority.

Requirement array position does not create identity.

`diagnostics` is a finite array of diagnostic records.

`assessor_metadata` is optional reporting metadata and, for binding version
`0.1.0`, may contain only `assessor_id?`, `implementation_name?`,
`implementation_version?` and `assessment_timestamp?`. It does not affect
Profile identity, requirement semantics or aggregation.

## Assessment grammar closure table

| Construct | Binding-defined slots | Profile/package supplied values |
| --- | --- | --- |
| `local_reference` | `scope_ref`, `local_ref` | Local scope token and local occurrence token. |
| `reference_scope` | `scope_ref`, `scope_kind` | Declared result/package/coupling scope value. |
| `assessment_subject` | `subject_role`, `reference_strategy`, `artifact_id` or `local_reference` or `coupled_occurrence_ref` | Subject role and concrete subject occurrence value. |
| `profile_requirement_artifact_reference` | `reference_strategy`, `artifact_id` or `local_reference` or `coupled_occurrence_ref` | Concrete Profile artifact occurrence value. |
| `assessment_context` | `context_entries[]`; each entry has `context_key`, `context_value` | Profile-defined context keys and admissible explicit values inside binding-defined slots. |
| `requirement_result_ref` | `local_reference` | Requirement-result occurrence in a declared local reference scope. |
| `diagnostic_ref` / `diagnostic_refs` | `local_reference` | Diagnostic occurrence in a declared local reference scope. |
| `subject_ref` | stable subject strategy or `local_reference` | Subject occurrence reference. |
| `related_refs` | categorized relation plus reference value; assessment-local values use `local_reference` | Related assessment record, subject, requirement result or diagnostic occurrence. |

```text
binding-defined structure
!= Profile-supplied value

JSON Schema
= validation of accepted grammar

JSON Schema
!= origin of grammar
```

## Overall outcomes

D7 defines exactly these global outcomes:

```text
conformant
nonconformant
indeterminate
```

`conformant` means all applicable Profile requirements of the exact Profile
edition have been deterministically resolved according to their accepted
semantics, none has outcome `violated`, no applicable requirement remains
`unsupported` or `unavailable`, and no uninterpretable-input or structural
blocker remains. An explicit offline-safe alternative may substitute for a
blocker only when the exact Profile edition itself defines that alternative and
the alternative is satisfied.

`nonconformant` means at least one applicable and evaluable Profile requirement
has outcome `violated`, or an applicable structural conformance rule is
deterministically violated.

`indeterminate` means no decisive violation has been established, but conformance
cannot be established because at least one applicable Profile requirement or
structural condition cannot be deterministically resolved. Causes include
unsupported requirements, unavailable dependencies, unsupported binding
constructs that block interpretation, unresolved required Profile references,
inability to enumerate requirements, invalid or uninterpretable binding input, or
contradictory metadata that prevents reliable assessment.

## Requirement-level outcomes

D7 defines exactly these requirement-level outcomes:

```text
satisfied
violated
not_applicable
unsupported
unavailable
```

`satisfied` means the requirement applies, is evaluable, and the assessed
material meets the accepted D5 requirement semantics.

`violated` means the requirement applies, is evaluable, and the assessed material
fails the accepted D5 requirement semantics. Violation is not inferred from local
dependency absence.

`not_applicable` means the requirement's applicability condition is determinably
false from explicit assessable information.

`unsupported` means the requirement construct is valid under the exact Profile
edition and binding version, but this assessor lacks the evaluation capability
needed to decide it. Unsupported is not violated, satisfied or unavailable.

`unavailable` means the requirement cannot be evaluated because an explicitly
required local dependency for the assessment is not available. Examples include
an exact Vocabulary edition, referenced material required for assessment or an
exact Profile requirement artifact when needed locally. Unavailable is not
violated, not satisfied and not proof that the dependency does not exist.

D7 does not add a requirement-level `invalid_input` outcome. Invalid binding or
uninterpretable assessment input is represented by overall `indeterminate` and
structural diagnostics because it may prevent reliable requirement enumeration.

## Requirement modes

D7 applies D5 requirement modes without redefining them.

For `required`, the requirement defines what must be satisfied. If it applies and
is satisfied, the requirement result is `satisfied`. If it applies, is evaluable
and fails, the result is `violated`.

For `optional`, the presence of the material or condition is not mandatory.
Absence that is allowed by the optional requirement is not a violation and may be
evaluated as `satisfied` when the requirement is applicable and deterministically
evaluable. If optional material or an optional condition is present, it must meet
the conditions imposed by that exact requirement. Present-but-invalid optional
material is `violated`.

```text
optional
!= non-conformance-affecting requirement

optional absence allowed
!= optional violation ignored
```

For `prohibited`, absence of the prohibited material, use or condition in the
applicable assessment scope is `satisfied`. Presence or use of the prohibited
material or condition is `violated`.

An applicable `violated` result remains a Profile requirement violation for all
three modes. It does not require another `required` or `prohibited` requirement
to duplicate the same condition before it can affect conformance.

Requirement mode and applicability are separate. A requirement can be optional
and applicable. A requirement can be required and not applicable.

```text
not_applicable
!= satisfied
```

For any mode, an applicable requirement with outcome `unsupported` or
`unavailable` prevents a `conformant` claim unless the exact Profile edition
itself defines an explicit offline-safe alternative for that requirement and the
alternative is satisfied.

```text
Profile requirement applicability
!= assessor-selected importance

optional
!= ignorable

optional absence allowed
!= optional requirement omitted from assessment

unsupported applicable requirement
!= conformant
```

## Aggregation rules

Aggregation from requirement-level outcomes to overall outcome is finite,
deterministic, order-independent, offline and score-free.

1. If at least one applicable and evaluable Profile requirement has outcome
   `violated`, the overall outcome is `nonconformant`.
2. If an applicable structural conformance rule is deterministically violated,
   the overall outcome is `nonconformant`.
3. If no decisive violation exists, but any applicable Profile requirement has
   outcome `unsupported` or `unavailable`, the overall outcome is
   `indeterminate`, unless the exact Profile edition defines and satisfies an
   explicit offline-safe alternative for that requirement.
4. If no decisive violation exists, but unsupported binding constructs,
   unavailable dependencies, unresolved required references, contradictory
   metadata or uninterpretable input prevent deterministic assessment, the
   overall outcome is `indeterminate`.
5. If all applicable Profile requirements of the exact Profile edition are
   deterministically resolved, none has outcome `violated`, and no blocking
   `unsupported`, `unavailable` or structural condition remains, the overall
   outcome is `conformant`.
6. `not_applicable` requirements do not count as `satisfied` and do not create
   violations.
7. Requirement array order does not create precedence and does not alter
   aggregation.
8. Diagnostic severity is never used to aggregate conformance.

If a decisive violation is established and other requirements are `unsupported`
or `unavailable`, `nonconformant` is still correct because non-conformance has
already been deterministically established.

```text
violated != unsupported
violated != unavailable

unsupported/unavailable
!= conformant

decisive established violation
=> nonconformant
```

## Subject identity and portable reporting

D7 `assessment_subject` has a binding-defined tagged-union grammar:

```text
subject_role = profile_requirement_artifact | projection_artifact | semantic_document

reference_strategy = stable_artifact_identity
artifact_id

reference_strategy = assessment_local_artifact_reference
local_reference

reference_strategy = coupled_subject
coupled_occurrence_ref = local_reference
```

Exactly one `subject_role` and exactly one reference strategy are present. The
concrete reference slot is determined by the strategy. Multiple contradictory
strategies, a strategy without its required reference slot, or a local reference
without a resolvable `scope_ref` are invalid binding structure.

### Subject with stable artifact identity

A detached standalone portable conformance result may reference the subject by
accepted stable artifact identity when the subject has one, such as
`projection_artifact_id`. Under `reference_strategy = stable_artifact_identity`,
`artifact_id` transports that accepted identity. D7 does not reinterpret it as
Entity identity, Source identity, Profile edition identity or result identity.

### Subject without stable artifact identity but inside a local reference scope

A result may use `reference_strategy = assessment_local_artifact_reference` when
the subject is included in, or explicitly coupled with, a declared local
reference scope. The `local_reference` identifies one artifact occurrence inside
that scope. It is not semantic identity and has no authority outside that
explicit scope.

```text
local reference scope
!= semantic namespace

local reference
!= semantic identity

local reference scope
!= packaging format

local reference scope
!= registry
```

D7 does not decide ZIP, folders, MIME, physical manifests, URLs or transport
protocol. However, the binding must declare or identify the local reference scope
when assessment-local references are used.

### Coupled subject

`reference_strategy = coupled_subject` means the result and subject are
explicitly bound together in the same assessment package or coupling context. It
still requires `coupled_occurrence_ref = local_reference` so the subject
occurrence is identifiable when the package contains more than one artifact.
Coupling is not content integrity proof unless a future accepted decision adds
such proof.

### Subject without stable artifact identity and not package-contained

A detached standalone result cannot unambiguously identify a subject that lacks
stable artifact identity and is not package-contained or coupled. File path, URL,
local locator, assessment-local token and content hash are insufficient by
themselves.

```text
assessment-local artifact reference
requires explicit package/coupling scope

detached portable result
+
subject without stable artifact identity
=> subject reference not portable/unambiguous
```

A Projection without `projection_artifact_id` can be assessed locally. A detached
portable external result over that Projection must either be coupled with the
subject or must state that the subject reference is not portable/unambiguous.

D7 does not invent hash/content-address identity. File paths and URLs may be
locators or package references, not semantic artifact identity. A content digest
may be an integrity mechanism in a future decision, but it is not identity here.

## Profile edition binding

Every conformance result declares exactly one Profile edition using the same D6
member names and meaning:

```text
profile_edition:
  profile_family
  profile_version
```

```text
same Profile edition identity
=> same binding member semantics where reused

assessment binding
!= second Profile identity model
```

The pair is the exact Profile edition identity for the assessment. The result may
also identify the locally supplied Profile requirement artifact used during the
assessment, but artifact location is not Profile identity.

D7 defines no resolver, registry lookup, automatic download, `latest`, version
range, compatibility substitution, `profile.family` member or `profile.version`
member. Reusing D6 `profile_edition` spelling does not merge the D6 and D7
binding families.

## Requirement references

D7 `requirement_ref` is a binding-defined tagged union with exactly these
semantic alternatives.

### Stable requirement reference

When a D6 requirement has `requirement_id`, D7 uses
`stable_requirement_reference` carrying that stable requirement ID as the primary
requirement reference.

### Locator-based occurrence reference

When a requirement has no `requirement_id`, D7 may use
`locator_occurrence_reference` carrying a binding-specific requirement locator
inside the exact Profile requirement artifact used for the assessment. The
locator identifies a concrete occurrence for reporting only.

```text
requirement_id
!= requirement locator

requirement locator
!= semantic identity

requirement referenced only by binding-specific locator
=> concrete Profile requirement artifact context must be unambiguously identified/coupled

Profile artifact reference
!= Profile edition identity

diagnostic path
!= requirement identity

array position
!= requirement identity

array index
!= requirement identity

JSON Pointer
!= universal semantic identity
```

A plain string that can mean either requirement ID or locator is not sufficient
D7 grammar. If any requirement is referenced only by binding-specific locator,
the concrete Profile requirement artifact context must be unambiguous. In that
case `profile_requirement_artifact_reference` is required in practice unless the
result is physically coupled with that exact artifact through explicit packaging.

No Profile artifact reference is required solely because a result uses stable
`requirement_id` references that are sufficient under the exact Profile edition.

A locator may be sufficient to reproduce or inspect a diagnostic against the
same concrete Profile requirement artifact. It must not be promoted to semantic
requirement identity.

## Requirement result references

D7 defines optional `requirement_result_ref` as a `local_reference` to one
requirement result inside one conformance result artifact or local reference
scope. Diagnostics may use it to refer to a specific requirement result.

```text
requirement result reference
!= requirement identity

requirement result reference
!= requirement_id

requirement result reference
!= array position

requirement result reference
!= JSON Pointer universal identity

diagnostic locator
!= semantic identity
```

`requirement_result_ref` has no authority outside the result artifact or explicit
package/coupling scope that contains it. It does not replace `requirement_ref`.

## Diagnostic records

A diagnostic record contains:

```text
diagnostic_ref?
diagnostic_code
diagnostic_category
requirement_ref?
requirement_result_ref?
subject_ref?
diagnostic_severity?
message?
locator?
related_refs?
```

`diagnostic_ref`, when present, is a `local_reference` to one diagnostic inside
the same result artifact or local reference scope.

`diagnostic_code` is stable within the exact assessment binding version.

`diagnostic_category` separates requirement evaluation, dependency availability,
binding structure and assessment input problems.

`requirement_ref` identifies the Profile requirement when the diagnostic concerns
one. `requirement_result_ref` may point to an assessment-local requirement result
when such a local result reference is declared.

`diagnostic_refs`, when used from requirement results or related records, are
`local_reference` values that identify diagnostics inside the same result artifact
or local reference scope. They do not make diagnostics Core Entities.

`subject_ref` refers to the assessment subject or to a subject occurrence
declared in the local reference scope. When assessment-local, it uses the same
`local_reference` primitive. It is not semantic identity unless it uses an
accepted stable artifact identity strategy.

`related_refs` is an optional list of typed or categorized references to related
assessment-local records, subjects, requirements, requirement results or
diagnostics. Any assessment-local reference inside `related_refs` uses the same
`local_reference` primitive. `related_refs` must not be a list of semantically
ambiguous strings and does not define a universal graph or generic semantic
reference system.

`message` is optional human-readable text. It is not identity and must not be
required for automatic assessment.

`locator` may identify an artifact member or binding-specific path for reporting.
It is not semantic identity.

Diagnostics must not carry stack traces, implementation internals, GUI state,
product-specific error objects, model output or execution traces as universal
normative content.

## Diagnostic code taxonomy

D7 defines this minimum finite diagnostic taxonomy for binding version `0.1.0`:

| Code | Category | Meaning |
| --- | --- | --- |
| `requirement_violated` | requirement_evaluation | An applicable evaluable requirement is violated. |
| `requirement_unsupported` | requirement_evaluation | A valid requirement construct is not supported by the assessor. |
| `dependency_unavailable` | dependency_availability | A required local dependency is unavailable for assessment. |
| `requirement_not_applicable` | requirement_evaluation | A requirement is deterministically not applicable and the assessor chooses to report it. |
| `invalid_binding_construct` | binding_structure | Input uses a construct not defined by the declared binding family/version. |
| `unsupported_binding_construct` | binding_structure | Input uses a defined binding construct whose representation or processing support is not implemented by the assessor. |
| `contradictory_projection_metadata` | binding_structure | Projection metadata contains contradictory accepted D6 member groups. |
| `exact_vocabulary_unavailable` | dependency_availability | The exact Vocabulary edition needed for deterministic assessment is unavailable locally. |
| `profile_requirement_artifact_unavailable` | dependency_availability | The exact Profile requirement artifact needed for local assessment is unavailable. |
| `unresolved_requirement_reference` | requirement_reference | A result or diagnostic cannot resolve the referenced requirement in the exact Profile artifact. |
| `missing_namespace_expansion_context` | binding_structure | Compact qualified terms lack required namespace expansion context. |
| `invalid_reference_availability_consistency` | binding_structure | Reference availability metadata contradicts carried/omitted/reference state. |
| `invalid_source_state_reference_preservation` | binding_structure | Source-state or reference preservation metadata contradicts accepted D2-D6 rules. |
| `structural_validation_failed` | binding_structure | Required binding structure is invalid without enumerating every schema error as a universal code. |
| `assessment_input_uninterpretable` | assessment_input | The supplied subject/Profile input cannot be interpreted enough to perform deterministic assessment. |

This taxonomy does not convert every future JSON Schema validation error into a
universal diagnostic code. Schema validation, Profile requirement evaluation and
dependency availability remain separate.

## Severity

D7 includes optional diagnostic severity:

```text
info
warning
error
```

Severity is presentational and prioritization metadata only.

```text
severity
!= conformance outcome

severity
!= requirement mode

severity
!= truth

severity
!= execution priority
```

`warning` does not imply `conformant`. `error` does not imply `nonconformant`.
Conformance is determined only by requirement outcomes, structural assessment
state and aggregation rules.

## Unsupported and unavailable

D7 keeps three diagnostic/result boundaries separate.

`requirement_unsupported` applies when the binding/Profile requirement has been
interpreted correctly, the construct is valid for the exact Profile edition and
binding version, and the assessor lacks semantic evaluation capability for that
valid requirement against the subject.

`unsupported_binding_construct` applies when the construct belongs to the
declared binding grammar but the assessor lacks representation or processing
support needed to interpret that construct. If this prevents interpretation of
requirements, the overall outcome is `indeterminate` with a structural diagnostic
and the assessor must not fabricate requirement-level outcomes that could not be
evaluated.

`invalid_binding_construct` applies when the construct does not belong to the
grammar of the declared binding version.

The same case must not be arbitrarily reclassified between these categories.
Classification follows the layer at which assessment becomes blocked:
requirement semantics, supported binding representation, or invalid grammar.

`unavailable` applies when assessment needs an explicit local dependency and that
dependency is not supplied or otherwise locally available. D7 does not auto-fetch
missing dependencies and does not treat network failure as semantic invalidity.

```text
violated
!= unsupported

violated
!= unavailable

unsupported
!= unavailable

dependency unavailable
!= dependency nonexistent
```

## Invalid input and invalid binding

If the subject artifact, Profile requirement artifact or result input cannot be
interpreted under its declared binding grammar, D7 represents the assessment as
`indeterminate` with structural diagnostics. D7 does not automatically report
`nonconformant` merely because assessment input cannot be interpreted, unless an
accepted Profile/core/binding requirement is itself evaluable and violated.

If the invalid input prevents requirement enumeration, requirement-level results
may be absent. The diagnostic records explain the structural blocker.

## Completeness versus conformance

Projection completeness and Profile conformance are separate.

A partial Projection may be Profile-conformant when the exact Profile edition
permits that Projection state. A complete Projection may be nonconformant if it
violates applicable Profile requirements. An unknown-completeness Projection may
be conformant, nonconformant or indeterminate according to the applicable Profile
requirements and D7 aggregation.

D7 does not make `complete` imply `conformant` and does not make `partial` imply
`nonconformant`.

## Diagnostics versus Review, trust and assertions

D7 does not reuse Core `Review`, `Confidence`, `Provenance` or Assertion records
as diagnostics. A conformance result may be cited or reviewed by future
architecture, but the diagnostic itself is not a semantic Assertion and does not
create Core truth, trust, approval or provenance semantics.

Assessor metadata, if present, does not change Profile identity or conformance
rules.

## Assessor metadata

D7 permits optional `assessor_metadata` with only these binding `0.1.0` slots:

```text
assessor_id?
implementation_name?
implementation_version?
assessment_timestamp?
```

These members are reporting metadata only. Implementation name and version do not
change conformance semantics. Assessment timestamp does not create wall-clock
applicability, does not create semantic truth and is not required for semantic
reproducibility unless a future accepted rule defines explicit timestamped
assessment context.

A future Profile edition must not invent additional normative assessor metadata
slots under assessment binding version `0.1.0`. New normative metadata slots
require a new accepted binding version or a future accepted Extension mechanism.

## Offline behavior

Assessment must be possible from locally supplied artifacts, locally built-in
exact-edition support and explicit assessment context.

D7 does not define or require automatic:

- Profile download;
- Vocabulary download;
- dependency fetch;
- registry lookup;
- resolver behavior;
- network access;
- model invocation;
- tool execution.

A missing local dependency yields `unavailable` or an availability diagnostic. It
does not initiate retrieval.

## D8 boundary

A D7 conformance result assesses one subject against one exact Profile edition.
D7 does not define multi-Profile aggregation, inheritance, merge, override,
precedence, composition or cross-Profile conflict resolution. D8 remains Open.

Two result artifacts over the same subject do not merge into one authority unless
a future accepted composition/governance rule says so.

## Schema and implementation boundary

ADR-0030 defines architecture and binding member groups only. It does not create
normative JSON Schema, normative fixtures, SDK evaluator APIs, runtime validators,
CLI diagnostics or executable behavior.

A future accepted schema may validate the D7 result artifact representation, but
schema will validate accepted semantics rather than invent them.

## Cross-domain validation

| Domain | Stress case | D7 result model response |
| --- | --- | --- |
| Engineering object graph | Projection references omitted component context by exact reference. | Result can report satisfied, violated, unavailable or indeterminate without CAD-specific semantics. |
| Spreadsheet/table dataset | Profile requires exact column-label Vocabulary edition. | Missing exact edition is `unavailable`; newer/similar edition is not automatic substitution. |
| Technical/legal document | Profile prohibits use of redacted material in a Projection. | Prohibited requirement violation yields `nonconformant` without becoming a Review record. |
| Software repository | Profile requires exact Revision/source-state preservation for selected records. | Result reports source-state preservation diagnostics without invoking Git or build tools. |
| Scientific dataset | Profile requires measured quantities preserve exact unit terms and uncertainty context. | Exact term/dependency failures are diagnostics, not AI-provider judgments. |
| Generic product/asset | Profile permits partial Projection with explicit continuation metadata. | Partial completeness does not automatically decide Profile conformance. |

No D7 diagnostic requires CAD, IFC, PDF, Git, Excel, SQL, tokenizers, model
providers, GUI state or application runtime semantics.

## Adversarial cases

| # | Case | D7 handling | Incorrect interpretation rejected |
| --- | --- | --- | --- |
| 1 | Violated requirement is reported as unavailable | Use `violated` only when an evaluable applicable requirement fails. | Violation collapsed into availability. |
| 2 | Unavailable dependency is treated as nonconformant | Use `indeterminate` unless a decisive violation is established. | Missing local dependency proves violation. |
| 3 | Unsupported requirement is treated as conformant | Use `indeterminate` for applicable unsupported requirements unless an explicit Profile-defined offline-safe alternative is satisfied. | Unsupported means satisfied. |
| 4 | Not applicable is counted as satisfied without rule | `not_applicable` is neutral in aggregation. | Applicability false becomes satisfaction. |
| 5 | Optional requirement is confused with warning | Optional is a requirement mode, not severity. | optional = warning. |
| 6 | Prohibited requirement is confused with severity | Prohibited is evaluated by D5 mode semantics. | prohibited = error severity. |
| 7 | Diagnostic severity alters overall outcome | Aggregation ignores severity. | warning/error decides conformance. |
| 8 | Requirement array order alters global result | Aggregation is order-independent. | Earlier requirement has precedence. |
| 9 | Profile declaration is used as proof of conformance | Declaration identifies governing Profile edition only. | Declared Profile proves conformance. |
| 10 | Result refers to requirement by array index as semantic ID | Use `requirement_id` when available; otherwise locator only. | Array index is requirement identity. |
| 11 | JSON Pointer is treated as requirement identity | Pointer may locate an occurrence only. | JSON Pointer is universal semantic ID. |
| 12 | Projection without artifact ID receives ambiguous standalone report | Require coupling or explicit non-portable/ambiguous subject reference. | Unidentified Projection is portable subject identity. |
| 13 | File path is used as Projection identity | File path is locator/package reference, not identity. | Path equals artifact ID. |
| 14 | Content hash is converted into semantic identity | Hash may support future integrity, not identity here. | Digest equals semantic identity. |
| 15 | Missing Vocabulary triggers network fetch | Report `unavailable`; no auto-fetch. | Identity is dereference instruction. |
| 16 | Network outage is treated as violation | Outage may make dependency unavailable. | Network failure proves Profile violation. |
| 17 | Similar/newer Vocabulary satisfies exact edition | Exact edition or explicitly allowed alternative is required. | Newer/similar means equivalent. |
| 18 | Unknown binding construct is treated as requirement unsupported | Outside declared grammar is `invalid_binding_construct`. | Unknown grammar is requirement unsupported. |
| 19 | Valid requirement construct is semantically unsupported by assessor | Use `requirement_unsupported` after the requirement is interpreted. | Assessor limitation rewrites grammar. |
| 20 | Partial Projection is assumed nonconformant | Completeness and conformance are separate. | partial => nonconformant. |
| 21 | Complete Projection is assumed conformant | Requirements still decide conformance. | complete => conformant. |
| 22 | Diagnostic is converted into Core Review | Diagnostic remains assessment/report metadata. | Diagnostic is Review. |
| 23 | `warning` implies conformant | Severity does not aggregate. | warning => conformant. |
| 24 | `error` implies nonconformant without requirement result | Severity alone is not conformance. | error => nonconformant. |
| 25 | Two results over same subject are merged as authority | D7 defines no merge authority. | Multiple reports compose automatically. |
| 26 | Multiple Profiles in one report are interpreted as D8 composition | D7 result references one exact Profile edition. | One D7 result performs Profile composition. |
| 27 | Optional material is absent and absence is validly allowed | Requirement may be `satisfied` when applicable and evaluable. | Optional absence is unknown or ignored. |
| 28 | Optional material is present and valid | Requirement is `satisfied`. | Optional material is outside conformance. |
| 29 | Optional material is present but invalid under the exact requirement | Requirement is `violated`; aggregation can be `nonconformant`. | Optional violation has no conformance effect. |
| 30 | Optional requirement is unsupported | Overall is `indeterminate` when the optional requirement is applicable and no explicit Profile-defined offline-safe alternative is satisfied. | Optional unsupported is conformant. |
| 31 | Prohibited requirement is unsupported | Overall is `indeterminate` when the prohibited requirement is applicable and no decisive violation exists. | Prohibited unsupported is satisfied. |
| 32 | Prohibited requirement dependency is unavailable | Overall is `indeterminate` when the prohibited requirement is applicable and no decisive violation exists. | Prohibited unavailable is absence. |
| 33 | One applicable requirement is violated and another is unavailable | Overall is `nonconformant` because violation is already established. | Availability uncertainty erases violation. |
| 34 | Requirement locator is used without concrete Profile artifact context | Result is structurally blocked or diagnostic reports unresolved requirement reference. | Locator is standalone requirement identity. |
| 35 | Assessment-local artifact reference is used outside its package | Reference is not portable outside explicit package/coupling scope. | Local token becomes artifact identity. |
| 36 | Detached result references unidentified Projection by URL/path/hash only | Subject reference is not portable/unambiguous. | Locator/hash solves identity. |
| 37 | Diagnostic uses `outcome_ref` or an undefined `requirement_result_ref` | `outcome_ref` is not D7 grammar; undefined local result reference is unresolved. | Diagnostic creates implicit result identity. |
| 38 | Valid binding construct is parser/process unsupported | Use `unsupported_binding_construct` and structural `indeterminate` if interpretation is blocked. | Parser support issue becomes requirement-level unsupported. |
| 39 | Construct is outside declared assessment/profile binding grammar | Use `invalid_binding_construct`. | Invalid grammar is valid but unsupported. |
| 40 | Future schema introduces an assessment field or token not accepted by ADR-0030 | Schema is ahead of accepted grammar and cannot originate semantics. | Schema invents assessment grammar. |
| 41 | Applicable optional requirement is unsupported and assessor decides it is not necessary | Overall is `indeterminate` unless an explicit Profile-defined offline-safe alternative is satisfied. | Optional applicable unsupported is discarded as not necessary. |
| 42 | D7 uses `profile.family` while D6 uses `profile_family` | Invalid D7 profile edition representation; D7 reuses D6 `profile_edition` spelling. | Assessment binding creates a second Profile identity model. |
| 43 | Assessment subject declares two reference strategies | Invalid binding structure; exactly one strategy is allowed. | Multiple strategies repair each other. |
| 44 | Local artifact reference appears without local reference scope | Reference is not portable/unambiguous. | Local token is globally meaningful. |
| 45 | Assessment-local token is used as semantic identity | Token remains local to the result/package scope. | Local token becomes semantic identity. |
| 46 | `requirement_ref` is an ambiguous string that could be ID or locator | Use tagged `stable_requirement_reference` or `locator_occurrence_reference`. | Consumer guesses reference kind. |
| 47 | Locator-based requirement reference lacks concrete Profile artifact context | Report unresolved requirement reference or structural blocker. | Locator is standalone requirement identity. |
| 48 | Schema invents a new `assessment_subject` strategy under binding `0.1.0` | Schema is ahead of accepted grammar; new strategy needs new binding version or accepted Extension mechanism. | Schema creates normative strategy. |
| 49 | Profile adds normative assessor metadata slot under assessment binding `0.1.0` | Not D7 grammar; new slot needs new binding version or accepted Extension mechanism. | Profile extends assessment metadata grammar. |
| 50 | Stable-artifact strategy is declared without `artifact_id` | Invalid binding structure; the concrete artifact identity value is missing. | Strategy token alone identifies subject/artifact. |
| 51 | Local-reference strategy is declared without `local_ref` | Invalid binding structure; `local_reference` requires both `scope_ref` and `local_ref`. | Scope alone identifies occurrence. |
| 52 | `local_ref` appears without resolvable `scope_ref` | Reference is unresolved in the assessment binding. | Local token is portable or global. |
| 53 | `coupled_subject` lacks an occurrence reference | Invalid binding structure; `coupled_occurrence_ref` is required. | Coupling token identifies one subject by itself. |
| 54 | Profile invents new fields inside `assessment_context` | Not D7 grammar under binding `0.1.0`. | Profile-defined context creates binding slots. |
| 55 | Profile defines a `context_key` value inside the binding-defined slot | Allowed when exact Profile edition defines the key's accepted meaning and values. | Profile-defined value becomes Profile-defined grammar. |
| 56 | Diagnostic references another diagnostic | Use `diagnostic_ref`/`diagnostic_refs` with `local_reference`. | Diagnostic becomes semantic Entity identity. |
| 57 | Future schema invents `artifact_reference_value` because ADR-0030 did not define a value slot | Schema is ahead of accepted grammar; D7 already uses `artifact_id`, `local_reference` or `coupled_occurrence_ref`. | Schema originates artifact-reference grammar. |

## Consequences

- S4 gains an accepted architecture for deterministic AI Context Profile
  conformance results and diagnostics.
- `conformant` requires all applicable Profile requirements of the exact Profile
  edition to be deterministically resolved, except where that exact edition
  defines and satisfies an explicit offline-safe alternative.
- Assessment binding `0.1.0` has closed binding-defined member groups, reference
  strategies, local-reference slots, assessment-context slots and metadata slots;
  schema and Profile editions do not originate new assessment grammar under that
  binding version.
- D7 reuses D6 `profile_edition` spelling, `profile_family` plus
  `profile_version`, without merging the assessment and Profile/Projection
  binding families.
- Overall outcome is finite and non-binary: `conformant`, `nonconformant` or
  `indeterminate`.
- Requirement-level outcomes preserve `violated`, `unsupported` and
  `unavailable` as distinct states.
- Result/report serialization uses a separate assessment binding family instead
  of changing D6 `ai-context-json/0.1.0`.
- `projection_artifact_id` remains optional, but standalone portable reports over
  unidentified Projections are explicitly ambiguous unless coupled or
  assessment-local references are used.
- Severity is optional diagnostic metadata and does not determine conformance.
- D8 composition remains open.
- No schema, fixture, SDK, runtime validator, resolver, registry, publication,
  tag, release or execution behavior is introduced.

## Remains open

- concrete JSON Schema for conformance result artifacts after D7 acceptance;
- normative fixtures for Profile/Profile-binding conformance after D7 acceptance;
- exact packaging/media-type conventions for portable result artifacts;
- integrity/signature/canonicalization rules if ever required;
- D8 Profile composition and conflict policy;
- S5 mature diagnostic governance;
- SDK/tooling behavior.

## Acceptance record

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-27. Acceptance
closes S4 D7 only: AI Context Profile conformance result and diagnostics
architecture. It does not accept D8 Profile composition, concrete schema
implementation, normative fixtures, SDK APIs, runtime behavior,
registry/resolver behavior, publication, canonicalization, signatures, tag,
release or execution behavior.
