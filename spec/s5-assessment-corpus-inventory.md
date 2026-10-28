# S5 AI Context assessment corpus inventory

**Status: HUMAN-APPROVED S5 I3 FINITE CORPUS INVENTORY - I3/I4/I5/I6 COMPLETE; I6 HUMAN-APPROVED 2026-10-07**

**Decision status:** Human-approved

**Decision readiness:** Complete - approved 2026-10-04

**Document class:** Human-approved normative conformance expectations and
non-normative implementation allocation.

This document fixes the exact finite case inventory human-approved at commit
`d102d4f479af7850eebf20c433919675873f49b1`. That approval marks I3 Complete
and authorizes I4 materialization. It does not define evaluator behavior beyond
Accepted ADRs, modify the approved I1 grammar or alter the human-approved I2
schema.

## Authority and fixed inputs

The inventory is derived from:

1. `PROJECT_FOUNDATION.md`;
2. Accepted ADR-0024 through ADR-0031, especially ADR-0028 and ADR-0030;
3. the human-approved AI Context Profile edition `0.1.0`;
4. the human-approved `ai-context-json/0.1.0` binding;
5. the human-approved `ai-context-assessment-json/0.1.0` I1 grammar; and
6. the human-approved I2 Draft 2020-12 schema with SHA-256
   `aec4f4e42267e8486b3420e0590f976aac1a3a07c61c2ba8d7a5776e57c5346a`.

The approved inventory adds no Profile requirement, outcome, diagnostic code, reference
strategy, binding member or aggregation rule. S0-S4 artifacts remain frozen.

## Case and layer model

The exact approved inventory contains 58 cases:

| Group | IDs | Count | Later owner |
| --- | --- | ---: | --- |
| Schema-valid serialized result artifacts | `V01`-`V12` | 12 | I4 materialization and Layer A checks. |
| Invalid serialized result artifacts | `I01`-`I22` | 22 | I4 materialization; rejection at the first stated layer. |
| Semantic and adversarial assessment scenarios | `S01`-`S24` | 24 | I5 requirement assessment and I6 aggregation/result construction. |
| **Total** |  | **58** | I3 approval freezes expectations before downstream work. |

The layer labels reuse the repository-local S5 implementation split:

```text
Layer A
= assessment-result representation and I2 schema validation

S2 Layer 3 temporal check
= existing deterministic Gregorian validity check reused by I2

Layer B
= deterministic semantic assessment and binding-local reference integrity

Layer C
= D7 aggregation, diagnostics and result construction
```

`V` cases prove accepted representation coverage. Their declared outcomes are
data carried by schema-valid artifacts; Layer A validity alone does not prove
that an evaluator derived those outcomes correctly.

`I` cases are rejected artifacts. Rejection of a result artifact is not a
claim that its alleged subject is `nonconformant` or `indeterminate`, and an
invalid result must not be repaired by inference.

`S` cases define assessment expectations. Requirement-mode micro-scenarios are
direct tests of Accepted ADR-0028/ADR-0030 rules; they do not create another
Profile edition or a generic requirement language.

Case IDs and stable names are the manifest identity for repository tests.
Filenames and package layout are I4 implementation details and must preserve
these IDs without adding or dropping cases.

## Valid serialized result artifacts

Every `V` case must pass Layer A against the exact I2 schema. Local references
need only be structurally valid in this group; resolution behavior is exercised
separately by `I20` and the semantic scenarios.

| ID | Stable name | Required coverage | Layer A expectation | Declared D7 outcome coverage |
| --- | --- | --- | --- | --- |
| `V01` | `minimal-stable-conformant` | Stable Projection subject and stable requirement reference; no optional root members. | Pass. | `satisfied` / `conformant`. |
| `V02` | `stable-violation-diagnostic` | Stable Projection subject, `requirement_violated` diagnostic and `error` severity. | Pass. | `violated` / `nonconformant`. |
| `V03` | `profile-subject-unsupported` | `profile_requirement_artifact` subject role and `requirement_unsupported` diagnostic with `warning`. | Pass. | `unsupported` / `indeterminate`. |
| `V04` | `semantic-document-unavailable` | `semantic_document` subject role and dependency diagnostic. | Pass. | `unavailable` / `indeterminate`. |
| `V05` | `not-applicable-neutral` | `not_applicable` plus `satisfied`, optional `requirement_not_applicable` diagnostic and `info` severity. | Pass. | `not_applicable` is neutral; declared overall `conformant`. |
| `V06` | `package-local-subject` | `assessment_local_artifact_reference` subject and `assessment_package_scope`. | Pass. | `satisfied` / `conformant`. |
| `V07` | `coupled-subject` | `coupled_subject` and `explicit_coupling_scope`; no stable identity is invented. | Pass. | `not_applicable` / `conformant`. |
| `V08` | `stable-profile-artifact-locator` | Locator requirement reference with stable concrete Profile artifact reference. | Pass. | `violated` / `nonconformant`. |
| `V09` | `package-local-profile-artifact-locator` | Locator requirement reference with package-local Profile artifact reference. | Pass. | `unsupported` / `indeterminate`. |
| `V10` | `coupled-profile-artifact-locator` | Locator requirement reference with coupled Profile artifact and explicit coupling scope. | Pass. | `satisfied` / `conformant`. |
| `V11` | `diagnostic-taxonomy-and-typed-references` | All 15 accepted code/category pairs, all three severity tokens, declared result/diagnostic refs, subject refs and all five `related_ref_kind` branches. | Pass. | Declared `nonconformant`; taxonomy presence does not independently derive it. |
| `V12` | `enumeration-blocked-context-metadata` | Empty required result array, blocker diagnostic, result ID, Profile-defined context with nested `null`, and all assessor metadata slots with canonical timestamp. | Pass. | No requirement outcome fabricated; `indeterminate`. |

Together these cases cover all three subject roles, all three subject reference
strategies, all three concrete Profile-artifact reference strategies, both
requirement reference strategies, all five requirement outcomes, all three
overall outcomes, local scopes, diagnostics, severities and assessor metadata.

```text
V11 taxonomy coverage
= representation coverage of all accepted code/category pairs

diagnostic emission semantics
= governed by ADR-0030/I1 and exercised by downstream deterministic tests
```

V11 does not prove that arbitrary combinations of otherwise valid diagnostics
are semantically correct, and it creates no additional diagnostic code.

## Invalid serialized result artifacts

Each case changes only the condition named below relative to an appropriate
valid baseline. `Layer A reject` means the I2 schema must reject the artifact.
The temporal and reference-integrity cases deliberately preserve the accepted
layer separation.

| ID | Stable name | Invalid condition | First rejecting layer | Expected result |
| --- | --- | --- | --- | --- |
| `I01` | `wrong-assessment-binding-family` | Binding family is not the exact assessment family. | Layer A. | Artifact rejected; no D7 outcome. |
| `I02` | `wrong-assessment-binding-version` | Binding version is not exact `0.1.0`. | Layer A. | Artifact rejected; no version substitution. |
| `I03` | `wrong-result-artifact-kind` | Root kind is not `conformance_result_artifact`. | Layer A. | Artifact rejected. |
| `I04` | `missing-required-root-member` | Required `requirement_results` is absent. | Layer A. | Artifact rejected; no default or inferred array. |
| `I05` | `plural-aggregate-root-members` | Adds multi-subject or multi-Profile aggregate members such as `assessment_subjects` or `profile_editions`. | Layer A. | Artifact rejected; no implicit D8 composition. |
| `I06` | `subject-branch-slot-missing` | Subject discriminator is present without its selected value slot. | Layer A. | Artifact rejected. |
| `I07` | `requirement-reference-branches-contradict` | A requirement reference carries both stable-ID and locator branch slots. | Layer A. | Artifact rejected; no branch precedence. |
| `I08` | `invalid-overall-outcome-token` | Uses `passed`, `failed` or another non-D7 overall token. | Layer A. | Artifact rejected. |
| `I09` | `invalid-requirement-outcome-token` | Uses `failed`, `skipped` or another non-D7 requirement token. | Layer A. | Artifact rejected. |
| `I10` | `unknown-diagnostic-code` | Diagnostic code is outside the accepted 15-code set. | Layer A. | Artifact rejected. |
| `I11` | `diagnostic-code-category-mismatch` | Accepted code is paired with the wrong category. | Layer A. | Artifact rejected. |
| `I12` | `invalid-diagnostic-severity` | Severity is outside `info`, `warning`, `error`. | Layer A. | Artifact rejected; severity is not extended by convenience. |
| `I13` | `malformed-local-reference-token` | `scope_ref` or `local_ref` is empty. | Layer A. | Artifact rejected. |
| `I14` | `local-reference-without-root-scope` | A local reference occurs without `reference_scope`. | Layer A. | Artifact rejected; scope is not inferred. |
| `I15` | `locator-requirement-without-profile-artifact-context` | Locator requirement reference has neither an explicit concrete Profile artifact reference nor qualifying package/coupling scope. | Layer A. | Artifact rejected; Profile edition identity is insufficient. |
| `I16` | `null-context-value` | Binding-owned `context_value` is directly `null`. | Layer A. | Artifact rejected; nested Profile-permitted `null` remains distinct. |
| `I17` | `extra-assessment-context-grammar` | Adds an unknown binding member to `assessment_context` or a context entry. | Layer A. | Artifact rejected; context values cannot extend grammar. |
| `I18` | `extra-assessor-metadata-grammar` | Adds an unknown assessor metadata slot. | Layer A. | Artifact rejected; metadata remains closed and outcome-neutral. |
| `I19` | `invalid-gregorian-assessment-timestamp` | Uses lexical timestamp `2025-02-29T12:34:56Z`. | S2 Layer 3 temporal check after Layer A lexical pass. | Artifact rejected by deterministic Gregorian validation. |
| `I20` | `dangling-diagnostic-cross-reference` | A schema-valid `diagnostic_refs` local reference resolves to no declared diagnostic occurrence in the one scope. | Layer B reference integrity after Layer A pass. | Artifact rejected; no array-position or locator repair. |
| `I21` | `duplicate-requirement-occurrence` | A schema-valid result contains two requirement-result objects resolving to the same exact Profile requirement occurrence: at minimum the same exact Profile edition and stable `requirement_id` occur twice. The same rule applies to equal locators in the same concrete Profile artifact context. | Layer B semantic/reference integrity after Layer A pass. | Result artifact rejected as duplicate occurrence reporting; array position creates no second occurrence, and no precedence or aggregation repairs it. |
| `I22` | `ambiguous-local-reference-declaration` | Two otherwise distinct assessment-local occurrences declare the same `local_ref` under the same `scope_ref`, for example two diagnostics declaring one `diagnostic_ref` or two results declaring one `requirement_result_ref`. | Layer B reference integrity after Layer A pass. | Result artifact rejected for binding-local ambiguity; one local token cannot identify two distinct occurrences and does not become global identity. |

## Semantic and adversarial assessment scenarios

Every `S` case fixes explicit inputs and expected outputs. The eventual tests
must be deterministic, order-independent where stated and offline. Scenario
inputs may reuse frozen S4 artifacts, but they must not edit those artifacts or
turn fixture filenames into normative identity.

Every case has exactly one `Scenario basis`:

```text
exact_profile_0.1
= exercised against actual requirements in
  profiles/ai-context/v0.1/profile.json

d5_d7_micro_scenario
= tests already-Accepted ADR-0028 / ADR-0030 semantics in isolation
  without creating or claiming conformance to another Profile edition
```

An `exact_profile_0.1` case may not insert a synthetic requirement or change a
mode, Vocabulary dependency or applicability rule. A `d5_d7_micro_scenario`
may exercise generic accepted rules, but it is not a serialized normative
Profile artifact, a fictitious Profile conformance claim or a new requirement
language.

### Aggregation and requirement modes

| ID | Stable name | Scenario basis | Explicit scenario | Requirement expectation | Overall/diagnostic expectation |
| --- | --- | --- | --- | --- | --- |
| `S01` | `exact-profile-all-applicable-satisfied` | `exact_profile_0.1` | Exact Profile `0.1.0` assesses a conforming frozen Projection with every applicable requirement evaluable. | Applicable occurrences `satisfied`; deterministically false conditions `not_applicable`. | `conformant`; no blocker. |
| `S02` | `required-preservation-violation` | `exact_profile_0.1` | Required material context is known applicable and is not carried as required. | `material-context-carry` is `violated`. | `nonconformant`; `requirement_violated`. |
| `S03` | `applicable-unsupported-only` | `d5_d7_micro_scenario` | A valid applicable requirement is not implemented by the assessor and no violation is established. | `unsupported`. | `indeterminate`; `requirement_unsupported`. |
| `S04` | `applicable-dependency-unavailable-only` | `d5_d7_micro_scenario` | An explicit required local dependency is absent and no violation is established. | `unavailable`, never `violated`. | `indeterminate`; dependency diagnostic. |
| `S05` | `decisive-violation-precedence-and-order` | `d5_d7_micro_scenario` | The same finite results contain `violated`, `unsupported` and `unavailable` in multiple array orders. | Tokens remain distinct. | Always `nonconformant`; order-independent. |
| `S06` | `deterministic-not-applicable-neutral` | `exact_profile_0.1` | Explicit assessable information makes one frozen Profile condition false; every applicable requirement is satisfied. | False condition is `not_applicable`, not `satisfied`. | `conformant`; neutral result does not block. |
| `S07` | `optional-absence-allowed` | `d5_d7_micro_scenario` | An applicable optional requirement explicitly allows absence and the material is absent. | `satisfied`, not omitted from assessment. | `conformant` when no other blocker exists. |
| `S08` | `optional-present-invalid` | `d5_d7_micro_scenario` | Optional material is present but violates its exact applicable condition. | `violated`. | `nonconformant`; optional does not mean ignored. |
| `S09` | `prohibited-material-absent` | `d5_d7_micro_scenario` | An applicable prohibited condition is absent. | `satisfied`. | `conformant` when all other applicable requirements resolve. |
| `S10` | `prohibited-material-present` | `d5_d7_micro_scenario` | An applicable prohibited condition is present. | `violated`. | `nonconformant`. |

### Identity, subject and reference behavior

| ID | Stable name | Scenario basis | Explicit scenario | Requirement/reference expectation | Overall/diagnostic expectation |
| --- | --- | --- | --- | --- | --- |
| `S11` | `stable-subject-identity-preserved` | `exact_profile_0.1` | Exact stable Projection identity and frozen Profile requirement IDs resolve locally. | IDs are preserved exactly; assessment does not mutate the subject. | Same `conformant` baseline as `S01`. |
| `S12` | `package-local-subject-resolves-once` | `exact_profile_0.1` | A frozen Projection subject is package-local and resolves exactly once in the declared package scope. | Local token stays local; no artifact ID is fabricated. | Same outcomes as the equivalent stable-subject assessment. |
| `S13` | `coupled-subject-resolves-once` | `d5_d7_micro_scenario` | Coupled subject resolves exactly once in explicit coupling scope. | Path, digest and local token do not become semantic identity. | Same outcomes as the equivalent supplied subject. |
| `S14` | `locator-requirement-with-exact-artifact-context` | `exact_profile_0.1` | A locator resolves the actual `projection-baseline` occurrence in one explicitly identified frozen Profile artifact. | Locator identifies that occurrence only and never becomes stable requirement identity. | Evaluated requirement result aggregates normally. |
| `S15` | `unresolved-or-ambiguous-requirement-occurrence` | `d5_d7_micro_scenario` | Required locator/artifact context is unresolved or resolves ambiguously and no decisive violation exists. | No requirement occurrence or identity is fabricated. | `indeterminate`; `unresolved_requirement_reference`; empty results only if enumeration is blocked. |
| `S16` | `result-order-and-array-index-are-nonsemantic` | `d5_d7_micro_scenario` | Identical finite requirement results are supplied in forward and reverse order; array positions differ. | Same occurrence identity and same individual outcomes. | Same overall outcome; index never creates identity or precedence. |

### Exact edition, offline and availability behavior

| ID | Stable name | Scenario basis | Explicit scenario | Requirement expectation | Overall/diagnostic expectation |
| --- | --- | --- | --- | --- | --- |
| `S17` | `exact-vocabulary-built-in-support` | `d5_d7_micro_scenario` | Assessor explicitly supports an exact identified Vocabulary edition locally; frozen Profile `0.1.0` itself has no Vocabulary dependency. | Exact semantics may be used; no substitution is inferred. | Determinate result from those semantics; `conformant` when satisfied. |
| `S18` | `similar-or-newer-vocabulary-only` | `d5_d7_micro_scenario` | Exact required Vocabulary is absent; only a similar/newer edition, remote IRI or model suggestion is available. | `unavailable`; no latest substitution, fetch or AI equivalence. | `indeterminate`; `exact_vocabulary_unavailable`. |
| `S19` | `profile-requirement-artifact-unavailable` | `exact_profile_0.1` | The exact frozen Profile `0.1.0` artifact required for reliable enumeration is unavailable locally. | No one of its nine requirement results is fabricated. | Empty results, `indeterminate`, `profile_requirement_artifact_unavailable`. |
| `S20` | `ambient-state-does-not-change-applicability` | `exact_profile_0.1` | Explicit frozen-Profile inputs are fixed while session, user, GUI, environment, filesystem, network, clock and model state vary. | Actual Profile applicability and requirement outcomes remain identical. | Identical overall result; no ambient-state diagnostic or execution. |

### Diagnostic and metadata neutrality

| ID | Stable name | Scenario basis | Explicit scenario | Neutrality expectation | Overall expectation |
| --- | --- | --- | --- | --- | --- |
| `S21` | `severity-does-not-soften-violation` | `exact_profile_0.1` | An actual `material-context-carry` violation is reported with `info`, `warning` and `error` in separate runs. | Severity changes presentation only. | Always `nonconformant`. |
| `S22` | `severity-does-not-create-violation` | `exact_profile_0.1` | An actual conditionally applicable material-context requirement is deterministically `not_applicable`, its diagnostic uses `error`, and all applicable requirements are satisfied. | Severity does not change `not_applicable` or create a violation. | `conformant`. |
| `S23` | `message-locator-and-untrusted-text-neutrality` | `exact_profile_0.1` | Message and opaque locator text attached to an actual frozen requirement vary, including command-like or prompt-like untrusted strings. | Text remains inert, non-authoritative and non-executable. | Requirement and overall outcomes remain identical. |
| `S24` | `assessor-metadata-and-diagnostic-record-neutrality` | `exact_profile_0.1` | Assessor identity, implementation text/version and valid timestamp vary for the same frozen-Profile assessment; diagnostics are inspected as reporting records. | Metadata does not affect applicability; diagnostics do not become Assertion, Review, Confidence or Provenance; subject remains unchanged. | Overall outcome remains identical. |

## Frozen Profile mapping audit

`all nine frozen IDs` means exactly:

```text
projection-baseline
projection-unknown
material-context-carry
material-context-reference
material-context-omission
material-context-dependency
source-record-traceability
binding-record-traceability
external-reference-closure
```

All nine are `required`; the frozen Profile declares no optional or prohibited
requirement and has `vocabulary_dependencies: []`.

| ID | Stable name | Scenario basis | Actual Profile 0.1 requirement mapping |
| --- | --- | --- | --- |
| `S01` | `exact-profile-all-applicable-satisfied` | `exact_profile_0.1` | All nine frozen IDs. |
| `S02` | `required-preservation-violation` | `exact_profile_0.1` | `material-context-carry`. |
| `S03` | `applicable-unsupported-only` | `d5_d7_micro_scenario` | None; accepted unsupported semantics in isolation. |
| `S04` | `applicable-dependency-unavailable-only` | `d5_d7_micro_scenario` | None; accepted dependency-unavailable semantics in isolation. |
| `S05` | `decisive-violation-precedence-and-order` | `d5_d7_micro_scenario` | None; accepted D7 aggregation tuples in isolation. |
| `S06` | `deterministic-not-applicable-neutral` | `exact_profile_0.1` | `material-context-carry` with its actual `material_context_condition` deterministically false. |
| `S07` | `optional-absence-allowed` | `d5_d7_micro_scenario` | None; Profile 0.1 has no optional requirement. |
| `S08` | `optional-present-invalid` | `d5_d7_micro_scenario` | None; Profile 0.1 has no optional requirement. |
| `S09` | `prohibited-material-absent` | `d5_d7_micro_scenario` | None; Profile 0.1 has no prohibited requirement. |
| `S10` | `prohibited-material-present` | `d5_d7_micro_scenario` | None; Profile 0.1 has no prohibited requirement. |
| `S11` | `stable-subject-identity-preserved` | `exact_profile_0.1` | All nine frozen IDs. |
| `S12` | `package-local-subject-resolves-once` | `exact_profile_0.1` | All nine frozen IDs; only subject-reference strategy changes. |
| `S13` | `coupled-subject-resolves-once` | `d5_d7_micro_scenario` | None; accepted D7 coupling semantics in isolation. |
| `S14` | `locator-requirement-with-exact-artifact-context` | `exact_profile_0.1` | `projection-baseline`, referenced as the actual occurrence in the frozen artifact. |
| `S15` | `unresolved-or-ambiguous-requirement-occurrence` | `d5_d7_micro_scenario` | None; no occurrence is fabricated for mapping. |
| `S16` | `result-order-and-array-index-are-nonsemantic` | `d5_d7_micro_scenario` | None; accepted D7 result-order rule in isolation. |
| `S17` | `exact-vocabulary-built-in-support` | `d5_d7_micro_scenario` | None; Profile 0.1 has no Vocabulary dependency. |
| `S18` | `similar-or-newer-vocabulary-only` | `d5_d7_micro_scenario` | None; Profile 0.1 has no Vocabulary dependency. |
| `S19` | `profile-requirement-artifact-unavailable` | `exact_profile_0.1` | All nine frozen IDs as the blocked set; no individual result is fabricated. |
| `S20` | `ambient-state-does-not-change-applicability` | `exact_profile_0.1` | All nine frozen IDs and only their actual applicability declarations. |
| `S21` | `severity-does-not-soften-violation` | `exact_profile_0.1` | `material-context-carry`. |
| `S22` | `severity-does-not-create-violation` | `exact_profile_0.1` | `material-context-carry` with its actual applicability condition false. |
| `S23` | `message-locator-and-untrusted-text-neutrality` | `exact_profile_0.1` | `material-context-carry`; only reporting text/locator varies. |
| `S24` | `assessor-metadata-and-diagnostic-record-neutrality` | `exact_profile_0.1` | All nine frozen IDs; only result reporting metadata varies. |

## Integrated-suite boundary

```text
I3 assessment corpus
!= entire S5 integrated conformance suite
```

This inventory does not add unrelated Core, Extension or version-compatibility
cases merely to increase its size. Foundation-required Core, Profile,
Extension and version-compatibility integration remains an I7 responsibility
unless an approved I3 case already exercises the relevant assessment-result
boundary. No I7 work moves into I3 or I4 through this inventory.

## Coverage closure

The 58 cases jointly protect:

- all three subject roles and all accepted subject/Profile-artifact reference
  strategies;
- both requirement-reference strategies and deterministic local scopes;
- all five requirement outcomes and all three overall outcomes;
- required, optional and prohibited mode behavior;
- violation precedence, order independence and neutral `not_applicable`;
- all 15 diagnostic code/category pairs and all three severity tokens;
- exact edition support, `unsupported` versus `unavailable`, no latest/newer
  substitution and no automatic fetch;
- closed context and metadata grammar plus metadata neutrality;
- canonical UTC lexical form plus S2 Layer 3 Gregorian validity;
- one subject and one exact Profile per result, with no implicit D8
  composition;
- locator/local-reference non-identity, reference integrity and no
  array-position identity;
- rejection of duplicate reporting for one exact requirement occurrence;
- uniqueness of a declared binding-local reference within its scope;
- no network, registry, resolver, model, hidden state or execution dependency;
  and
- no subject mutation or promotion of diagnostics into semantic records.

These checks remain distinct:

```text
array order != identity
locator != identity
local reference != global identity

duplicate requirement occurrence reporting
=> invalid result artifact

one declared local token for two distinct local occurrences
=> invalid binding-local ambiguity
```

## Approval and downstream gate

Explicit human approval on 2026-10-04 means only:

```text
S5 I3 exact 58-case inventory
= human-approved conformance expectations

I3 approval
!= evaluator implemented
!= aggregation engine implemented
!= CLI implemented
```

I4 materializes `V01-V12` and `I01-I22` under
`profiles/ai-context/assessment-conformance/v0.1` and validates only their
approved first layers. I4 is Complete after explicit human approval on
2026-10-04. I5 executes the requirement-assessment portion of approved
`S01-S24` and is Complete after explicit human approval on 2026-10-06. I6
executes their aggregation, diagnostics and result-construction portion and is
Complete after explicit human approval on 2026-10-07. I7 integrates the
repository conformance suite and reference CLI and is Complete after explicit
human approval on 2026-10-09.

Current state:

```text
S5 Complete - human-approved 2026-10-10
R0 Complete
I1 Complete - human-approved 2026-10-03
I2 Complete - human-approved 2026-10-04
I3 Complete - human-approved 2026-10-04
I4 Complete - human-approved 2026-10-04
I5 Complete - human-approved 2026-10-06
I6 Complete - human-approved 2026-10-07
I7 Complete - human-approved 2026-10-09
I8 Complete - human-approved 2026-10-10
S6 not started
```

I5 adds no overall aggregation or diagnostic/result-construction behavior. I6
adds no public CLI, SDK/runtime, S6 work, tag, archive, push or publication.
I7 adds repository/reference conformance tooling without changing this approved
inventory or any corpus expectation.
