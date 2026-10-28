# AI Context assessment corpus

**Scope:** AI Context Profile 0.1 assessment-result conformance.

**Status:** Technical conformance catalogue. This document is
informative; it does not independently establish normative requirements.

The catalogue contains 58 fixed cases:

- 12 valid serialized assessment-result artifacts (`V01`–`V12`).
- 22 invalid serialized assessment-result artifacts (`I01`–`I22`).
- 24 semantic and adversarial assessment scenarios (`S01`–`S24`).

The applicable authority remains the exact Profile edition, the
assessment-result JSON binding and schema, and accepted architecture
decisions. This catalogue introduces no additional requirement language,
Profile edition, diagnostic taxonomy or evaluator behavior.

## Assessment layers

- **Layer A:** Assessment-result representation and exact JSON Schema validation.
- **S2 Layer 3 temporal check:** Deterministic Gregorian timestamp validity.
- **Layer B:** Deterministic semantic assessment and binding-local reference integrity.
- **Layer C:** Aggregation, diagnostics and result construction under the accepted assessment rules.

These checks remain distinct. Schema-valid representation does not
establish that a declared assessment outcome was correctly derived.

## Valid serialized result artifacts

The following cases cover permitted result representations. Local
references may be structurally valid without independently proving
reference resolution; that behavior is assessed separately.

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

The valid cases cover subject roles, reference strategies, requirement
outcomes, overall outcomes, diagnostics, severity and assessor metadata.

`V11` demonstrates representation coverage of accepted diagnostic
code/category pairs, not that every possible diagnostic emission is
semantically justified.

## Invalid serialized result artifacts

Each case specifies the invalid condition and the first rejecting layer.
Rejection of an artifact does not independently establish that the
alleged assessment subject is nonconformant or indeterminate.
Invalid results must not be repaired through inference.

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

Every scenario fixes explicit inputs and expected outcomes.

Two scenario bases are distinguished:

- `exact_profile_0.1`: Uses actual requirements of the exact frozen AI Context Profile.
- `d5_d7_micro_scenario`: Exercises accepted requirement-assessment and aggregation semantics independently of a serialized Profile artifact.

The second category does not create another Profile edition, a
synthetic requirement language or an additional conformance claim.

Assessment must remain deterministic and offline, and must not infer
identities, substitute versions or mutate assessed source artifacts.

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

## Execution and traceability

The `V` and `I` cases have corresponding materialized JSON fixtures.
The `S` scenarios are covered by deterministic Python tests and are
not required to exist as separate serialized JSON fixtures.

Implementation and validation resources:

- [Assessment fixture entry point](../profiles/ai-context/assessment-conformance/v0.1/README.md)
- [Assessment-result JSON binding](../spec/ai-context-assessment-json-binding.md)
- [Assessment-result JSON Schema](../profiles/ai-context/schema/v0.1/ai-context-assessment.schema.json)
- [AI Context Profile specification](../spec/ai-context-profile.md)
- [Conformance guide](../docs/conformance-guide.md)

For provenance and milestone traceability, the original
[assessment corpus inventory](../spec/s5-assessment-corpus-inventory.md)
remains available as a historical record. Its approval chronology does
not introduce additional public conformance requirements.
