# AI Context JSON binding 0.1

**Binding edition:** `ai-context-json/0.1.0` (normative JSON representation).

This specification defines the concrete JSON representation established by
ADR-0029 for:

```text
binding.family  = https://geesno.com/binding/ai-context-json
binding.version = 0.1.0
```

It defines the closed member names, cardinalities, tokens and representation
constraints supported by the associated Draft 2020-12 JSON Schema. The
Profile and Projection semantics are defined in
[ai-context-profile.md](ai-context-profile.md). The public architectural
baseline is [ARCHITECTURE.md](../ARCHITECTURE.md); accepted ADRs and applicable
normative specifications remain authoritative in their respective scopes.

This document does not itself define the JSON Schema, the exact Profile
requirement set, a fixture, assessment result, evaluator or runtime. The
schema supports structural validation. The exact Profile requirement set is
materialized separately in `profiles/ai-context/v0.1/profile.json` and governed
by [ai-context-profile.md](ai-context-profile.md).

## Normative authority map

This specification makes the accepted ADR-0029 grammar implementable without
making the binding an independent semantic authority.

| Binding subject | Normative authority |
| --- | --- |
| Exact Profile identity and edition declaration | ADR-0024 |
| Projection source state, selection, scope and carried identity | ADR-0025 |
| Completeness, omission, boundedness, truncation and continuation semantics | ADR-0026 |
| Preservation, material context, trust scope and Source/Binding semantics | ADR-0027 |
| Requirement modes, applicability and exact Vocabulary semantics | ADR-0028 |
| Member groups, eight requirement kinds, requirement-body slots, descriptor groups, reference availability and binding versioning | ADR-0029 |
| Accepted Core 0.1 JSON record shapes, raw JSON rules and namespace-map semantics reused by carried content | ADR-0010, ADR-0015 and ADR-0016 |
| Separate assessment-result binding boundary | ADR-0030 |
| Composite Profile binding boundary | ADR-0031 |

Cardinalities and closed-object constraints below express the accepted
binding grammar. They do not add a semantic dimension, operator, default or
requirement kind.

## Binding roles

Binding `0.1.0` has exactly two artifact kinds:

```text
profile_requirement_artifact
projection_artifact
```

Both are inert JSON objects. A member, token or construct not defined here is
not binding `0.1.0` grammar. A new normative construct requires a future
accepted binding version or a future accepted Extension mechanism.

The binding is representation, not Profile semantic authority. Profile-defined
values may instantiate only the slots defined here and MUST NOT add operators,
selectors, evaluator logic or binding members.

## Notation and general JSON rules

Cardinality notation is:

```text
[1]     exactly one, required
[0..1]  zero or one, optional
[0..*]  finite array, zero or more
[1..*]  finite non-empty array
```

The following rules apply to both artifact kinds:

1. Binding-defined objects are closed. Unknown members are invalid, except
   inside the explicitly non-normative `artifact_metadata` object.
2. Member names and closed tokens are case-sensitive and compared exactly.
3. A required member has no default. Its absence is invalid.
4. An absent optional member makes no claim and supplies no implicit value.
5. JSON `null` MUST NOT substitute for an absent optional member or for a
   binding-defined semantic value.
6. Optional arrays, when present, MUST be non-empty. Required arrays expressly
   marked `[0..*]` MAY be empty.
7. Array order has no priority, precedence, inheritance, override, truth or
   semantic-importance meaning.
8. Duplicate JSON object member names are invalid under the accepted raw-input
   rules.
9. IRIs are identities and MUST NOT be dereferenced automatically.
10. The binding defines no byte-canonical JSON form and no member ordering.

An **absolute IRI string** reuses the accepted Core 0.1 JSON absolute-IRI lexical and exact
comparison rules. A **non-empty token** is a non-empty JSON string compared
exactly. A **non-negative count** is the exact decimal string `0` or a decimal
string beginning with `1` through `9` followed by zero or more decimal digits.

A **Profile-defined value** is any finite non-null JSON value placed in a slot
that this binding expressly labels Profile-defined. It remains inert data. The
exact Profile edition MUST define enough semantics to assess that value
deterministically; object keys inside such a value are not binding operators or
new binding grammar.

Unless a table expressly identifies an object, array, boolean, absolute IRI
string, non-negative count, Profile-defined value or accepted Core 0.1 JSON shape, every
binding-defined token or code-form literal in its Value column is a non-empty
JSON string. Enumerated literals are exact, case-sensitive JSON string values.

## Common objects

### Binding header

`binding [1]` is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `family` | `[1]` | exact string `https://geesno.com/binding/ai-context-json` |
| `version` | `[1]` | exact string `0.1.0` |

No moving alias, range, substitution or inferred compatibility is allowed.

### Profile edition

`profile_edition [1]` is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `profile_family` | `[1]` | exact JSON string constant `https://geesno.com/profile/ai-context` |
| `profile_version` | `[1]` | non-empty exact opaque JSON string token |

For the initial AI Context Profile edition, the exact values are:

```text
profile_family  = https://geesno.com/profile/ai-context
profile_version = 0.1.0
```

Binding `ai-context-json/0.1.0` represents only exact versions of the
`https://geesno.com/profile/ai-context` Profile family. A future exact version
of that same family MAY use this grammar. An arbitrary or composite Profile
family MUST NOT use binding version `0.1.0`; normative composition requires
the future accepted binding version specified by ADR-0031.

`profile_edition` MUST NOT be replaced by `profile.family`, `profile.version`,
`profile_editions`, a range or `latest`.

### Requirement identity and reference

`requirement_id` is a non-empty stable token assigned by the exact Profile
edition. Its identity scope is that exact Profile edition. It MUST NOT be an
array index, JSON Pointer, file line, byte offset or generated schema path.

`requirement_reference` is the exact `requirement_id` token of another
requirement in the same exact Profile edition. A referenced requirement MUST
have `requirement_id`; resolution is a deterministic semantic check.

### Descriptor identity and reference

Repeatable Projection descriptors MAY use `descriptor_id [0..1]`, a non-empty
token unique across all descriptor occurrences in one Projection artifact. It
is a binding-local cross-reference token, not semantic identity, record
identity or array-position identity.

`descriptor_reference` is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_group` | `[1]` | `boundedness`, `omissions`, `projection_continuations`, `dependency_continuations`, `material_context` or `reference_availability` |
| `descriptor_id` | `[1]` | exact local descriptor token |

The referenced descriptor MUST exist in the named group. A descriptor that is
referenced MUST carry `descriptor_id`.

### Artifact metadata

`artifact_metadata [0..1]` is a JSON object reserved for non-normative
authorship, file, distribution, publication-location or integrity evidence.
Its contents are not standardized by binding `0.1.0`, do not participate in
Profile or Projection semantics, do not establish identity or conformance, and
MUST NOT override any binding-defined member. Consumers MAY ignore it.

This open metadata envelope is not an Extension mechanism and cannot introduce
normative grammar.

## Profile requirement artifact

The root of a Profile requirement artifact is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `artifact_kind` | `[1]` | exact token `profile_requirement_artifact` |
| `binding` | `[1]` | binding header |
| `profile_edition` | `[1]` | exact Profile edition |
| `vocabulary_dependencies` | `[0..*]`, member required | finite array of Vocabulary dependency objects |
| `requirements` | `[0..*]`, member required | finite array of requirement envelopes |
| `artifact_metadata` | `[0..1]` | non-normative metadata object |

The required arrays MAY be empty. Profile artifact URL, filename, package path,
registry location, retrieval route and metadata are not Profile identity.

Profile requirement artifacts do not use a `namespaces` member. Fields that
identify a Vocabulary, term, Extension or Profile use absolute IRIs. Namespace
prefixes MUST NOT substitute for those identities.

### Vocabulary dependency object

Each `vocabulary_dependencies` item is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `vocabulary_family` | `[1]` | absolute Vocabulary family IRI |
| `vocabulary_version` | `[1]` | non-empty exact opaque version token |
| `dependency_role` | `[1]` | `required_exact_edition` or `allowed_alternative_exact_edition` |

The pair identifies one exact Vocabulary edition. A newer, similar,
compatible-looking or automatically discovered edition does not substitute for
it. Dependency role does not change Vocabulary meaning.

### Requirement envelope

Every `requirements` item is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `requirement_id` | `[0..1]` | stable requirement token scoped to the exact Profile edition |
| `requirement_kind` | `[1]` | one of the eight closed kind tokens |
| `requirement_mode` | `[1]` | `required`, `optional` or `prohibited` |
| `applicability` | `[1]` | applicability object |
| `requirement_body` | `[1]` | closed body selected by `requirement_kind` |

`requirement_mode` is the only authority for the required/optional/prohibited
axis. A body MUST NOT repeat or contradict that axis. Requirement array order
MUST NOT affect interpretation.

### Applicability object

`applicability` is one closed descriptor object, not an expression tree:

| Member | Cardinality | Value |
| --- | --- | --- |
| `subject_category` | `[1]` | non-empty Profile-defined exact token |
| `basis_kind` | `[1]` | non-empty Profile-defined exact token |
| `context_reference` | `[0..1]` | non-empty Profile-defined exact token |
| `expected_value` | `[0..1]` | Profile-defined value |

The exact Profile edition defines the admitted token/value meanings. The
descriptor MUST be deterministically assessable from explicit information. It
MUST NOT encode hidden runtime state, a selector, query, ranking expression,
arbitrary code, execution order or model judgment.

There is no `applicability` requirement kind and no recursive requirement that
selects other requirements.

## Requirement-body grammar

The eight and only eight `requirement_kind` values are:

```text
structure
cardinality
vocabulary
projection
preservation
source_binding
extension
closure
```

Binding support for a kind does not require every exact Profile edition to use
that kind.

### `structure`

The body is a closed object with these members:

| Member | Cardinality | Value |
| --- | --- | --- |
| `artifact_kind` | `[0..1]` | `profile_requirement_artifact` or `projection_artifact` |
| `record_category` | `[0..1]` | non-empty Profile-defined record/category token |
| `member_group` | `[0..1]` | non-empty JSON string naming an exact binding member group |
| `member_name` | `[0..1]` | non-empty JSON string naming an exact binding member |
| `allowed_binding_value` | `[0..1]` | exact non-empty binding token |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

At least one member other than `requirement_reference` MUST be present. This
kind can constrain accepted binding structure but MUST NOT create Core 0.1 JSON fields,
alternate assertion placement or schema-only semantics.

### `cardinality`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `count_target` | `[1]` | non-empty Profile-defined target token |
| `count_scope` | `[1]` | Profile-defined value identifying the count scope |
| `min_count` | `[0..1]` | non-negative count |
| `max_count` | `[0..1]` | non-negative count |
| `exact_count` | `[0..1]` | non-negative count |

At least one count constraint MUST be present. `exact_count` MUST NOT coexist
with `min_count` or `max_count`. When both minimum and maximum are present, the
minimum MUST NOT exceed the maximum. Count constraints do not imply order,
priority, source population size, sampling or probability.

### `vocabulary`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `vocabulary_family` | `[0..1]` | absolute Vocabulary family IRI |
| `vocabulary_version` | `[0..1]` | non-empty exact opaque JSON string token |
| `term_identity` | `[0..1]` | absolute term IRI |
| `allowed_alternative_exact_edition` | `[1..*]` when present | finite non-empty array of exact Vocabulary edition objects |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

`vocabulary_family` and `vocabulary_version` MUST occur together. The body MUST
contain that pair, `term_identity`, or both. Each alternative item contains
exactly `vocabulary_family [1]` and `vocabulary_version [1]` with the meanings
above. Absence of `allowed_alternative_exact_edition` declares no explicit
alternative list; when present, the array MUST NOT be empty.

No prefix, namespace base, `latest`, range, AI similarity or implicit
compatibility may satisfy an exact Vocabulary requirement.

### `projection`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `scope_descriptor` | `[0..1]` | Profile-defined value |
| `completeness_policy` | `[0..1]` | `complete_projection`, `partial_projection_allowed` or `unknown_completeness_allowed` |
| `boundedness_policy` | `[0..1]` | Profile-defined value |
| `truncation_policy` | `[0..1]` | Profile-defined value |
| `projection_continuation_policy` | `[0..1]` | Profile-defined value |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

At least one policy member other than `requirement_reference` MUST be present.
This body owns Projection scope, completeness, boundedness, truncation and
Projection continuation. It MUST NOT own dependency continuation, material
preservation, closure or a selection algorithm and MUST NOT redefine
`complete`, `partial` or `unknown`.

### `preservation`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `preservation_target` | `[1]` | Profile-defined value identifying material context |
| `material_context_policy` | `[1]` | `carry`, `materialize`, `exact_reference_sufficient`, `omission_allowed` or `dependency_continuation` |
| `dependency_continuation_reference` | `[0..1]` | non-empty Profile-defined exact reference token |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

`dependency_continuation_reference` MAY appear only with
`material_context_policy = dependency_continuation`. It is not a
`descriptor_reference` and does not identify a concrete Projection descriptor
occurrence.

This body MUST NOT contain `partial_projection_allowed`; Projection partiality
belongs only to the `projection` requirement kind. Explicit omission does not
preserve omitted content, and exact reference sufficiency is not
materialization.

### `source_binding`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `source_participation` | `[1]` | `source_record`, `binding_record`, `locator`, `source_state` or `source_revision` |
| `target_category` | `[0..1]` | non-empty Profile-defined target/category token |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

This kind owns Source/Binding participation and traceability. It MUST NOT
create product adapters, source mutation, permission, Git semantics, mandatory
signatures or preservation policy.

### `extension`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `extension_term` | `[1]` | absolute Extension term IRI |
| `host_category` | `[1]` | non-empty accepted host-category token |
| `extension_handling` | `[1]` | `presence`, `understanding`, `preservation` or `payload_constraint` |
| `payload_constraint_reference` | `[0..1]` | non-empty Profile-defined reference token |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

`payload_constraint_reference` is required only when `extension_handling` is
`payload_constraint` and MUST be absent otherwise. It references Profile-
defined inert constraint semantics; it is not executable code or a second
Extension grammar.

### `closure`

The body is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `closure_scope` | `[1]` | Profile-defined value |
| `closure_policy` | `[1]` | `self_contained`, `external_references_allowed` or `external_references_disallowed` |
| `closure_target` | `[0..1]` | Profile-defined value |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

This kind owns closure and external-reference policy. It MUST NOT define graph
traversal, automatic dereference, resolver behavior, Profile composition,
preservation or dependency-continuation semantics.

## Projection artifact

The root of a Projection artifact is a closed object:

| Member | Cardinality | Value |
| --- | --- | --- |
| `artifact_kind` | `[1]` | exact token `projection_artifact` |
| `binding` | `[1]` | binding header |
| `profile_edition` | `[1]` | exact Profile edition |
| `source_state` | `[1]` | source-state object |
| `selection_context` | `[1]` | selection-context object |
| `projection_scope` | `[1]` | Projection-scope object |
| `projection_completeness` | `[1]` | `complete`, `partial` or `unknown` |
| `carried_content` | `[1]` | carried-content object |
| `namespaces` | conditionally `[1]` | accepted Core 0.1 JSON namespace map when compact carried terms require it |
| `reference_availability` | `[0..*]`, member required | reference-availability array |
| `projection_artifact_id` | `[0..1]` | absolute IRI identifying this artifact/view |
| `boundedness` | `[1..*]` when present | finite array of bound descriptors |
| `truncation` | `[0..1]` | truncation descriptor |
| `omissions` | `[1..*]` when present | finite array of omission descriptors |
| `projection_continuations` | `[1..*]` when present | finite array of Projection-continuation descriptors |
| `dependency_continuations` | `[1..*]` when present | finite array of dependency-continuation descriptors |
| `material_context` | `[1..*]` when present | finite array of material-context descriptors |
| `profile_artifact_reference` | `[0..1]` | non-empty JSON string token carrying an inert artifact locator/handle |
| `artifact_metadata` | `[0..1]` | non-normative metadata object |

The exact `profile_edition` governs the Projection. The artifact MUST NOT embed
another requirement set. `profile_artifact_reference` is not Profile identity,
semantic identity or proof of conformance. It MUST NOT trigger dereference,
fetch or network access; substitute for `profile_edition`; or create package,
registry or retrieval-command semantics.

`projection_artifact_id` is separate from source SemanticDocument identity and
all carried semantic IDs. It is not a Core Entity ID, content digest or proof
of conformance.

### Source-state object

`source_state` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `semantic_document_id` | `[1]` | exact source SemanticDocument absolute IRI |
| `source_scope` | `[0..1]` | Profile-defined value preserving known source scope |
| `semantic_revision_id` | `[0..1]` | exact semantic Revision absolute IRI |
| `source_state_descriptor` | `[0..1]` | explicit Profile-defined value |

At least one of `semantic_revision_id` or `source_state_descriptor` MUST be
present. When an exact source semantic Revision exists, its ID MUST be carried;
when none is identified, `source_state_descriptor` supplies explicit derivation
state context and MUST NOT fabricate a Revision.

### Selection-context object

`selection_context` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `selection_context_kind` | `[1]` | non-empty Profile-defined exact token |
| `selection_descriptor` | `[1]` | Profile-defined value |
| `selection_input_references` | `[1..*]` when present | non-empty exact reference tokens |

The object records derivation context only. It MUST NOT contain a binding-level
query, selector, ranking, prompt, retrieval or generation program.

### Projection-scope object

`projection_scope` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `scope_kind` | `[1]` | non-empty Profile-defined exact token |
| `scope_descriptor` | `[1]` | Profile-defined value |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

This scope is distinct from source scope and selection context. Completeness is
always interpreted relative to it.

### Carried-content object

`carried_content` is a closed envelope containing only accepted Core 0.1 JSON record
shapes:

| Member | Cardinality | Core 0.1 JSON shape |
| --- | --- | --- |
| `revision` | `[0..1]` | accepted Core 0.1 JSON `revision` definition |
| `entities` | `[1..*]` when present | accepted Core 0.1 JSON `entity` items |
| `sources` | `[1..*]` when present | accepted Core 0.1 JSON `source` items |
| `bindings` | `[1..*]` when present | accepted Core 0.1 JSON `binding` items |
| `assertions` | `[1..*]` when present | accepted Core 0.1 JSON `assertion` items |
| `tombstones` | `[1..*]` when present | accepted Core 0.1 JSON `tombstone` items |
| `history` | `[0..1]` | accepted Core 0.1 JSON `history` definition |

The envelope MAY be empty when the declared Projection legitimately carries no
Core 0.1 JSON record body. It is not a SemanticDocument and therefore contains no
`spec_version`, SemanticDocument `id`, source document `scope`, `profiles`,
`namespaces` or document-level `extensions`. Projection `namespaces` is the
separate root member defined below.

Every carried record body MUST satisfy its accepted Core 0.1 JSON shape. Semantic IDs,
reference targets, qualified-term identities and scoped nesting MUST be
preserved. Identified records retain IDs; anonymous trust records remain nested
in the host that supplies their scope.

### Projection namespaces

`namespaces` reuses the accepted Core 0.1 JSON namespace-map shape and expansion semantics.
It is REQUIRED when any compact qualified term in `carried_content` depends on
a prefix mapping. It MAY be omitted only when no carried term needs it.

Every used prefix MUST be declared, and expansion MUST preserve the source
term's absolute IRI. Vocabulary dependencies, preferred prefixes, network
lookups and AI inference MUST NOT substitute for this map.

### Bound descriptor

Each `boundedness` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `bound_dimension` | `[1]` | non-empty Profile-defined exact token |
| `bound_rule` | `[1]` | non-empty Profile-defined exact token |
| `limit_value` | `[1]` | Profile-defined value |
| `bound_reached` | `[1]` | JSON boolean |

Presence declares boundedness. It does not establish truncation or any
completeness state. The exact Profile edition defines dimension, unit and rule
semantics.

### Truncation descriptor

`truncation` is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `truncation_established` | `[1]` | JSON boolean `true` |
| `affected_scope` | `[1]` | Profile-defined value |
| `bound_reference` | `[0..1]` | descriptor reference to `boundedness` |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

Absence means truncation is not established by this member; it does not mean
that no bound exists. Presence MUST coincide with
`projection_completeness = partial`.

### Omission descriptor

Each `omissions` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `omitted_target` | `[0..1]` | exact absolute IRI when the target is known |
| `omitted_category` | `[0..1]` | non-empty Profile-defined category token |
| `omitted_scope` | `[0..1]` | Profile-defined value |
| `omission_category` | `[1]` | non-empty Profile-defined exact token |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |
| `dependency_continuation_reference` | `[0..1]` | descriptor reference to `dependency_continuations` |

At least one of `omitted_target`, `omitted_category` or `omitted_scope` MUST be
present. This group represents known omission inside declared Projection scope.
It does not enumerate all unselected content and does not mean deletion,
falsity, invalidity or Tombstone.

### Projection-continuation descriptor

Each `projection_continuations` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `continuation_scope` | `[1]` | Profile-defined value |
| `continuation_descriptor` | `[1]` | inert Profile-defined value |
| `source_state_reference` | `[0..1]` | source-state object |
| `profile_edition_reference` | `[0..1]` | exact Profile-edition object |

The root source state, exact Profile edition, selection context and Projection
scope remain controlling. Optional repeated references, when present, MUST be
consistent with the root and MUST NOT silently substitute a changed state or
edition.

### Dependency-continuation descriptor

Each `dependency_continuations` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `dependency_target` | `[1]` | exact absolute target IRI |
| `dependency_descriptor` | `[1]` | inert Profile-defined value |
| `reference_availability_reference` | `[0..1]` | descriptor reference to `reference_availability` |
| `omission_reference` | `[0..1]` | descriptor reference to `omissions` |

This group is distinct from Projection continuation. It does not fetch,
materialize or prove availability of the dependency.

### Material-context descriptor

Each `material_context` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `context_target` | `[1]` | Profile-defined value identifying exact context/scope |
| `preservation_state` | `[1]` | `carried`, `exact_reference_sufficient`, `materialization_required`, `omitted` or `dependency_continuation` |
| `carried_record_reference` | `[0..1]` | exact carried record absolute IRI |
| `omission_reference` | `[0..1]` | descriptor reference to `omissions` |
| `dependency_continuation_reference` | `[0..1]` | descriptor reference to `dependency_continuations` |
| `requirement_reference` | `[0..1]` | same-edition requirement reference |

State-specific constraints are:

- `carried` requires `carried_record_reference`;
- `omitted` requires `omission_reference`;
- `dependency_continuation` requires
  `dependency_continuation_reference`;
- `exact_reference_sufficient` and `materialization_required` MUST NOT claim
  carriage merely from reference availability.

The descriptor is the primary representation of preservation state. It MUST
NOT become an independent source of omission, Projection-continuation,
reference-availability or closure truth.

### Reference-availability descriptor

Each required `reference_availability` item is closed:

| Member | Cardinality | Value |
| --- | --- | --- |
| `descriptor_id` | `[0..1]` | local descriptor token |
| `reference_target` | `[1]` | exact absolute target IRI |
| `availability_state` | `[1]` | `carried`, `external` or `unassessed` |
| `primary_descriptor_reference` | `[0..1]` | descriptor reference to the primary omission, continuation or material-context descriptor |

There MUST be exactly one semantically consistent availability entry for each
distinct reference target carried by Core 0.1 JSON records in `carried_content`.
`availability_state = carried` requires the target body to be carried;
`external` states only that it is not carried here; `unassessed` makes no
materialization determination.

Reference availability does not assert omission, continuation, preservation,
target existence, truth or dependency resolution and never retargets the
reference.

## Cross-member semantic invariants

The following are deterministic semantic rules even when some can also be
encoded as schema conditionals:

1. Every `requirement_reference` resolves within the exact Profile edition.
2. Every `descriptor_reference` resolves to the named group and local
   descriptor token.
3. Requirement and descriptor identifiers are not derived from array position.
4. Established truncation implies `projection_completeness = partial`.
5. Boundedness or `bound_reached = true` alone does not imply truncation.
6. Known required in-scope omission is inconsistent with `complete`.
7. Profile permission for omission does not turn omitted content into preserved
   content or complete Projection scope.
8. Carried record IDs and reference targets equal their source identities
   exactly; no local repair, retargeting or re-identification is permitted.
9. Every carried compact qualified term expands offline to the same absolute
   term IRI as in the source context.
10. Reference availability, omission, both continuation groups and material
    context remain single-owner dimensions; duplicated contradictory metadata
    is invalid and member order supplies no winner.
11. Carried Source, Binding, trust, lifecycle and validity context retains exact
    accepted host scope and meaning.
12. Unknown Extensions on a record claimed losslessly preserved are not dropped
    or altered.
13. Optional continuation source/Profile references are consistent with the
    root derivation context; R1 MUST NOT silently become R2.
14. Artifact and Profile declaration do not prove Profile conformance.

## Structural versus semantic validation matrix

| Rule | Structural JSON Schema? | Deterministic semantic validation? | Narrative-only invariant? | Source authority |
| --- | --- | --- | --- | --- |
| Root artifact kind and binding constants | Yes | No | No | ADR-0029 |
| Required/optional root members | Yes | No | No | ADR-0029; this binding specification |
| Closed objects and exact enum tokens | Yes | No | No | ADR-0029; this binding specification |
| Requirement body selected by `requirement_kind` | Yes, conditional schema | No | No | ADR-0029 |
| Cardinality exact/min/max structural exclusivity | Yes | Minimum not greater than maximum | No | ADR-0028/0029 |
| Vocabulary family/version pairing | Yes | Exact-edition support and no substitution | No | ADR-0028/0029 |
| Applicability has no expression/operator members | Yes | Explicit context is deterministically assessable | Hidden state is never authority | ADR-0028/0029 |
| Requirement-reference target exists | Limited | Yes | No | ADR-0028/0029 |
| Descriptor-reference target exists and group matches | Limited | Yes | No | ADR-0029; this binding specification |
| Core 0.1 JSON carried record body shape | Yes, by Core 0.1 JSON definitions | Core 0.1 JSON identity/reference integrity | No | ADR-0016/0029 |
| Required namespace map shape | Yes | Every compact term expands to preserved absolute IRI | No network guessing | ADR-0010/0016/0029 |
| Completeness token | Yes | Correct relative to declared Projection scope | No source-wide inference | ADR-0026/0029 |
| Truncation object implies `partial` | Yes, conditional schema | Consistent known incompleteness | No deletion/priority inference | ADR-0026/0029 |
| Bound descriptor shape | Yes | Dimension/rule understood under exact Profile; bound does not imply truncation | No universal token/model limit | ADR-0026/0029 |
| Known omission descriptor shape | Yes | In-scope/material omission and completeness consistency | Omission is not deletion | ADR-0026/0027/0029 |
| Continuation descriptor shape | Yes | Exact source/Profile/scope consistency | Never fetch/execute/authorize | ADR-0026/0029 |
| Material-context state shape | Yes | Carriage/reference/omission dependency consistency and exact host scope | Preservation is not truth elevation | ADR-0027/0029 |
| Reference-availability state shape | Yes | One consistent entry per carried target; carried/external accuracy | Availability owns no omission/continuation semantics | ADR-0029 |
| Profile edition declaration | Yes | Exact requirement set is locally available/supported | Declaration is not conformance | ADR-0024/0028/0029 |
| Offline processing | No | Tests MAY verify no dependency is needed | No automatic dereference/network/model/tool | ARCHITECTURE.md; ADR-0024-0029 |
| Byte ordering/canonicalization | No | No | No byte canonical form is defined | ADR-0016/0029 |

The corresponding JSON Schema MUST implement only the structural column and
locally expressible conditionals. It MUST NOT infer or replace the semantic or
narrative columns.

## Assessment and Profile-composition exclusions

Binding `0.1.0` contains no `conformant`, `valid`, diagnostic, severity,
unsupported/unavailable result or assessment-report member. The separate
`ai-context-assessment-json/0.1.0` grammar established under ADR-0030 is
defined by [ai-context-assessment-json-binding.md](ai-context-assessment-json-binding.md)
and is not reproduced here.

Binding `0.1.0` contains no Profile component, lineage, disposition, conflict,
merge, inheritance, override or precedence member. ADR-0031 requires a future
accepted exact binding version for normative composite Profile representation.

## Profile 0.1 artifact boundary

This specification defines the grammar capable of representing an exact
Profile edition. It does not define which requirement kinds or requirement
instances AI Context Profile edition `0.1.0` contains. The normative Profile
specification defines that exact finite set, materialized separately in
[`profiles/ai-context/v0.1/profile.json`](../profiles/ai-context/v0.1/profile.json).

```text
binding supports requirement kind
!= Profile 0.1 must contain that kind
```

No benchmark scale or compactness threshold is a member, Profile requirement,
Projection grammar rule, boundedness definition, completeness definition or
conformance condition in this specification.
