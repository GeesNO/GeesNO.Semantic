# ADR-0029: AI Context Profile and Projection serialization binding

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-24
- **Date:** 2026-09-22
- **Decision order:** Sixth S4 architecture decision after ADR-0028 acceptance

## Context

ADR-0024 accepts AI Context Profile identity, exact Profile versions, exact
Profile editions and the bare-core/Profile conformance boundary. ADR-0025
accepts Projection as a finite derived semantic view of an identified source
SemanticDocument state under an exact Profile edition and explicit selection
context. ADR-0026 accepts Projection completeness, omission, boundedness,
truncation, continuation and dependency-continuation semantics. ADR-0027 accepts
preservation and material-context semantics. ADR-0028 accepts abstract Profile
requirement expression semantics and the Profile/Vocabulary policy boundary.

D6 must choose a concrete, machine-readable, offline-capable binding for two
separate roles:

- an exact AI Context Profile edition and its requirement set;
- a Projection artifact produced or assessed under that exact Profile edition.

D6 represents semantics already fixed in D1-D5. It does not invent new Profile,
Projection, omission, preservation, Vocabulary, completeness or conformance
semantics.

This ADR proposes binding architecture only. It does not create a schema,
fixture suite, SDK, runtime, diagnostic/result model, registry, resolver,
publication package, canonical byte format, digital signature mechanism or
network protocol.

## Prerequisite review

1. The Foundation keeps the normative semantic model independent from
   serialization and keeps GeesNO.Semantic descriptive rather than executable.
2. The Foundation allows JSON as the initial reference serialization route but
   does not make JSON mechanics the abstract model.
3. ADR-0015 keeps Extension data inert and preserves unknown Extension payloads.
4. ADR-0016 freezes S2 Layers 0-3, the S2 schema and exact
   `spec_version: "0.1.0"` dispatch. Profile validation is a separate later
   layer.
5. ADR-0017 separates Vocabulary identity, Vocabulary version, namespace
   expansion base and term identity.
6. ADR-0023 defines inert compatibility/profile-acceptability claims without
   automatic substitution, resolver behavior or conformance.
7. ADR-0024 separates Profile identity from Profile artifact location and
   accepts the exact AI Context Profile edition identity.
8. ADR-0025 defines Projection source-state traceability and identity
   preservation while leaving Projection artifact identity to future binding.
9. ADR-0026 defines omission, boundedness, truncation and continuation while
   leaving concrete representation to D6.
10. ADR-0027 defines material-context preservation while leaving concrete
    representation to D6.
11. ADR-0028 defines abstract requirement semantics and makes D6 representation
    non-authoritative.

## Controlling distinctions

```text
semantic meaning != serialization

Profile requirement artifact != Projection artifact

Profile identity != Profile artifact location

Profile family identity != Profile artifact URL

Profile version != serialization-binding version

Profile identity != filename

Profile identity != registry location

Core spec version != Profile version
Core spec version != Vocabulary version
Core spec version != Profile-binding version

Projection != source SemanticDocument mutation

Projection artifact identity != source SemanticDocument identity

Projection artifact identity != carried semantic object identity

source SemanticDocument identity != source Revision identity

Source record identity != source SemanticDocument identity

binding representation != semantic authority

Profile semantic authority != binding grammar authority

binding representation != Profile semantic authority

binding.family + exact binding.version determines binding grammar

Profile declaration != proof of Profile conformance

reference target identity != reference availability

reference preservation != target materialization

bounded != truncated

truncated => partial

bounded + unknown is possible

continuation != URL fetch

continuation != API cursor execution

continuation != tool call

continuation != permission

projection continuation != dependency continuation

explicit omission != preservation

allowed by reference != materialized

Profile allows omission != Projection complete

P1 + P2 != merged Profile

deterministic semantic validation != byte canonicalization

fingerprint != semantic identity
```

## Definitions

**AI Context binding** means the concrete JSON-based binding proposed by D6 for
AI Context Profile requirement artifacts and AI Context Projection artifacts.
The binding is not the abstract Profile semantics and is not the abstract
Projection semantics.

**Binding family** means the identity of the concrete binding format. D6
proposes `https://geesno.com/binding/ai-context-json` as the binding family.
This IRI is an identity, not a retrieval location.

**Binding version** means the exact version of the binding format. D6 proposes
initial binding version `0.1.0`. Binding version is distinct from Core
`spec_version`, AI Context Profile version and Vocabulary version.

**Binding grammar** means the set of artifact members, requirement kinds,
requirement payload structures, operators, descriptors and interpretation rules
defined by a binding family and exact binding version. Binding grammar is the
serialization contract. It is not Profile semantic authority.

**Profile requirement artifact** means a JSON artifact whose role is to
represent the requirement set of one exact AI Context Profile edition. It does
not assert that any Projection conforms.

**Projection artifact** means a JSON artifact whose role is to represent one
finite Projection derived from an identified source SemanticDocument state under
one exact AI Context Profile edition and one explicit selection context.

**Carried semantic content** means selected S2 semantic record bodies transported
inside a Projection artifact while preserving their original semantic IDs,
reference targets, qualified terms and accepted S2 record meanings.

**Reference availability manifest** means D6 metadata that states whether a
reference target is materialized/carried in the current Projection artifact,
remains external to the artifact or has not been assessed for availability. It
may cross-reference the normative descriptor that explains an external target,
but it does not independently assert omission, continuation or material-context
preservation semantics and does not change the reference target identity.

## Artifact-role alternatives

### Alternative A - Use a full S2 SemanticDocument as the Profile artifact

The Profile requirement set could be encoded as ordinary S2 semantic content.
This is rejected for D6. A Profile requirement artifact represents normative
requirements of an exact Profile edition, not source assertions. Encoding it as
ordinary source semantic content would blur Profile requirement, semantic fact
and Vocabulary meaning.

### Alternative B - Use a full S2 SemanticDocument as the Projection artifact

A Projection artifact could simply be a filtered S2 SemanticDocument. This is
rejected as the universal D6 binding. It would confuse a Projection view with
the source SemanticDocument state, overload S2 document `scope` with
Profile-specific Projection metadata, and force either S2 core changes or lossy
side-channel metadata for omission, continuation, boundedness, preservation and
source-state traceability.

### Alternative C - Wrap a complete projected S2 SemanticDocument

A Projection artifact could be an envelope around a complete S2 SemanticDocument
payload. This is useful for self-contained Projections but rejected as the
universal D6 requirement. Some valid Projections intentionally preserve exact
references whose targets remain outside the Projection, and some references
that were locally available in the source are not materialized in the
Projection. Forcing a complete embedded S2 document would either require
retargeting references or impose universal self-containment.

### Alternative D - Carry S2 record bodies inside a Projection envelope

A Projection artifact could use a dedicated AI Context envelope that carries S2
record bodies and Profile/Projection metadata separately. The carried records
keep their S2 record shapes and semantic IDs, while the envelope represents
Projection scope, omission, continuation, preservation, bounds, source-state
traceability and reference availability. This is accepted.

### Alternative E - One combined Profile+Projection object

One object could include both the Profile requirement set and each Projection.
This is rejected. A Projection must refer to the exact Profile edition that
governs interpretation; it must not redefine the requirements against which it
is evaluated.

## Decision

D6 proposes two distinct JSON artifact kinds under one AI Context binding
family:

1. a **Profile requirement artifact** for one exact AI Context Profile edition;
2. a **Projection artifact** for one concrete Projection under one exact Profile
   edition and one explicit selection context.

Both artifact kinds include a binding header with:

```text
binding.family  = https://geesno.com/binding/ai-context-json
binding.version = 0.1.0
```

Both artifact kinds are inert JSON data. The binding never executes code,
prompts, callbacks, remote validators, tools, queries, transformations or
network fetches.

The two artifact kinds are distinguished by an explicit artifact-kind token:

```text
artifact_kind = profile_requirement_artifact
artifact_kind = projection_artifact
```

The exact token spelling above is part of the proposed binding. A future schema
may encode it, but the schema must derive from this decision rather than invent
it.

## Binding versioning

The binding has its own version because the concrete JSON artifact shape can
evolve independently from Core `spec_version`, AI Context Profile version,
Vocabulary version and source SemanticDocument version.

The binding version does not change semantic meaning. It identifies the syntax
and processing contract for Profile requirement artifacts and Projection
artifacts.

For a Profile requirement artifact or Projection artifact, `binding.family` plus
exact `binding.version` determines the interpretation of every normative binding
construct. An exact Profile edition may select, combine and instantiate
requirement constructs supported by that binding. It MUST NOT silently introduce
new `requirement_kind` values, normative sub-kinds, new `requirement_body`
semantics, new operators, new grammar or new execution/evaluation semantics
under the same binding version.

If future AI Context work needs a new binding construct, it requires a new
binding version or an Extension mechanism explicitly accepted by later
architecture. D6 does not design that future Extension mechanism.

A Profile artifact or Projection artifact MUST NOT use `latest`, moving aliases,
implicit ranges or automatic substitution for binding version selection.

## Profile requirement artifact

A Profile requirement artifact represents the requirement set of exactly one AI
Context Profile edition. It contains these required member groups:

- `artifact_kind`;
- `binding`;
- `profile_edition`;
- `vocabulary_dependencies`;
- `requirements`.

It may contain optional artifact metadata such as artifact authorship,
publication location, local file name, distribution channel or non-mandatory
integrity evidence. Such metadata is not Profile identity.

### Profile edition member

`profile_edition` identifies the exact Profile edition with:

- `profile_family`: `https://geesno.com/profile/ai-context`;
- `profile_version`: the exact Profile version, initially `0.1.0`.

The Profile family identity and Profile version together identify the exact
Profile edition and its normative requirement set under ADR-0024 and ADR-0028.

The Profile artifact MUST NOT treat artifact URL, filename, registry location,
package name, retrieval route or local cache path as Profile identity.

### Requirement-set representation

`requirements` is a finite array of typed requirement envelopes. Array order is
not priority, precedence, inheritance, override or truth.

Each requirement envelope contains:

- `requirement_kind`: a finite token naming the D5 requirement dimension;
- `requirement_mode`: `required`, `optional` or `prohibited` when that
  distinction applies;
- `applicability`: explicit assessable context descriptors;
- `requirement_body`: the typed requirement payload for that requirement kind;
- optional `requirement_id`.

D6 permits these eight requirement kinds because they correspond to accepted D5
semantics without duplicating envelope-level applicability:

- `structure`;
- `cardinality`;
- `vocabulary`;
- `projection`;
- `preservation`;
- `source_binding`;
- `extension`;
- `closure`.

There is no `requirement_kind = applicability` in binding `0.1.0`.
Envelope-level `applicability` is the only primary representation for normative
applicability. A requirement related to assessment context must use a concrete
requirement kind with envelope-level applicability, or a requirement reference
when it needs to coordinate with another requirement. It MUST NOT create a
second applicability requirement or recursive requirement-selection mechanism.

`requirement_mode` is the only binding `0.1.0` authority for the
required/optional/prohibited axis. A `requirement_body` identifies the target,
parameters and kind-specific policy dimensions of the requirement; it MUST NOT
restate that same mode as body-local required/optional/prohibited semantics.

```text
requirement_mode
= normative required/optional/prohibited axis

requirement_body
= target + parameters + kind-specific policy dimensions
```

A body that attempts to contradict `requirement_mode`, for example by making the
envelope required while a body-local token says prohibited, is unsupported or
invalid. D6 defines no precedence rule to repair such contradictions.

An exact Profile edition may select, combine and instantiate these binding-defined
requirement kinds and may supply Profile-specific values inside the typed
`requirement_body` slots supported by the binding. It does not own the binding
grammar. Under the same `binding.version`, the Profile MUST NOT create new
normative requirement sub-kinds, reinterpret `requirement_body`, add operators or
turn descriptors into a programming language, query language, expression
language, rule engine or evaluator.

### Requirement-body grammar for binding 0.1.0

For `binding.version = 0.1.0`, `requirement_body` is a finite declarative
object whose grammar is determined by `requirement_kind`. A Profile may supply
values inside the binding-defined slots: identifiers, references, qualified
terms, exact Vocabulary editions, count values, scope descriptors, requirement
references and Profile-defined descriptor values. A Profile MUST NOT create new
body slots, operators, selectors, evaluator semantics or requirement-body grammar
under the same binding version.

| `requirement_kind` | D5 dimension represented | `requirement_body` may contain | Binding 0.1.0 constructs/tokens | Expressly outside |
| --- | --- | --- | --- | --- |
| `structure` | Accepted artifact/member/record structure targeted by `requirement_mode`. | Artifact kind, record/category target, member group, member name and allowed binding enum values. | `artifact_kind`, `record_category`, `member_group`, `member_name`, `allowed_binding_value`, `requirement_reference`. | Body-local required/optional/prohibited semantics, new S2 core fields, alternate assertion placements, schema-only semantics or Profile-defined structural operators. |
| `cardinality` | Count constraints over structures or semantic record categories when applicable. | Count target, count scope, minimum, maximum or exact count. | `count_target`, `count_scope`, `min_count`, `max_count`, `exact_count`. | Probabilistic thresholds, model scores, sampling rules or inferred source population size. |
| `vocabulary` | Exact Vocabulary edition and exact term requirements accepted by D5. | Vocabulary family identity, exact Vocabulary version, exact term identity and explicit exact alternatives. | `vocabulary_family`, `vocabulary_version`, `term_identity`, `allowed_alternative_exact_edition`, `requirement_reference`. | Latest-version aliases, compatibility inference, namespace-prefix substitution, AI similarity, automatic Vocabulary discovery or body-local required/optional/prohibited term mode. |
| `projection` | Projection scope, completeness, boundedness, truncation and Projection-continuation dimensions accepted by D2/D3/D5. | Scope descriptor, completeness policy, bound policy, truncation policy and Projection-continuation policy. | `scope_descriptor`, `completeness_policy = complete_projection | partial_projection_allowed | unknown_completeness_allowed`, `boundedness_policy`, `truncation_policy`, `projection_continuation_policy`, `requirement_reference`. | Selection algorithms, model ranking, tokenizers, execution, retrieval, summarization, dependency-continuation ownership, material preservation, self-containment, closure or redefining `complete/partial/unknown`. |
| `preservation` | Preservation/materialization policy for identity, source, trust, lifecycle and material context accepted by D4/D5. | Target context, material-context policy, materialization/reference/omission policy and dependency continuation when it is a material dependency/preservation concern. | `preservation_target`, `material_context_policy = carry | materialize | exact_reference_sufficient | omission_allowed | dependency_continuation`, `dependency_continuation_reference`, `requirement_reference`. | Treating omission as preservation, redefining trust truth, making references materialized, source-binding ownership, Projection-completeness ownership, Projection-continuation ownership, self-containment/closure ownership or changing ADR-0026/0027 completeness semantics. |
| `source_binding` | Source/Binding participation and traceability requirements accepted by D5. | Source/Binding record participation target, locator retention target, source-state or source Revision target. | `source_participation = source_record | binding_record | locator | source_state | source_revision`, `target_category`, `requirement_reference`. | Product adapters, native API calls, source mutation, permission grants, Git semantics, preservation ownership or mandatory fingerprints/signatures. |
| `extension` | Carrying, preserving or understanding known inert Extension data. | Extension term, allowed host category, Extension handling dimension and optional Profile-defined payload-constraint reference. | `extension_term`, `host_category`, `extension_handling = presence | understanding | preservation | payload_constraint`, `payload_constraint_reference`, `requirement_reference`. | Extension redefining core semantics, body-local required/optional/prohibited mode, executable plugin behavior or a second AI Context Extension grammar. |
| `closure` | Closure/self-containment policy over the Projection artifact under the exact Profile edition. | Closure scope, self-containment/external-reference policy and carried closure target descriptors. | `closure_scope`, `closure_policy = self_contained | external_references_allowed | external_references_disallowed`, `closure_target`, `requirement_reference`. | Graph traversal algorithms, automatic dereference, resolver behavior, Profile composition, dependency-continuation ownership, preservation ownership or D7 conformance results. |

```text
JSON Schema
= validation of accepted binding grammar

JSON Schema
!= origin of requirement_body grammar
```

A future schema implementation may encode object structure, required members,
enums, primitive types, cardinality and conditional validation for the grammar
above. It MUST NOT invent new normative constructs for `requirement_body`.

### Semantic owner matrix

| Semantic dimension | Primary owner in binding `0.1.0` | Non-owner treatment |
| --- | --- | --- |
| Requirement applicability | Envelope-level `applicability` member | No `applicability` requirement kind; no selector, query or hidden runtime condition. |
| Required/optional/prohibited axis | Envelope-level `requirement_mode` | `requirement_body` must not duplicate or contradict that axis. |
| Artifact/member/record structure | `structure` | Other kinds may reference structural requirements but do not redefine structure semantics. |
| Cardinality | `cardinality` | Array order, source frequency and priority are not cardinality. |
| Exact Vocabulary edition and term targets | `vocabulary` | Namespace maps, local prefixes and similar/newer editions do not own Vocabulary acceptability. |
| Projection scope, completeness, boundedness, truncation and Projection continuation | `projection` | Material dependency continuation, preservation and closure are not owned here. |
| Material-context carry/materialization/reference sufficiency/omission and dependency continuation as material dependency | `preservation` | Projection continuation, source binding and closure do not duplicate this authority. |
| Source/Binding participation and traceability | `source_binding` | Preservation may require context involving Source/Binding records but does not own their participation grammar. |
| Known inert Extension handling | `extension` | Extensions do not redefine Core or binding grammar. |
| Self-containment, closure scope, external-reference allowance/disallowance and carried closure targets | `closure` | Preservation may reference closure requirements but does not independently own self-containment or closure policy. |
| Cross-kind coordination | `requirement_reference` | Cross-reference is not duplicate semantic authority, merge, inheritance or precedence. |

```text
same semantic dimension
=> one primary requirement kind

Projection partiality policy
=> projection requirement kind

material-context omission policy
=> preservation requirement kind

cross-reference
!= duplicate semantic authority

requirement order
!= precedence
```

### Requirement identity

A requirement with no stable identity omits `requirement_id`.

A requirement with stable identity uses `requirement_id`. The value must be a
stable identifier assigned by the exact Profile edition. It MUST NOT be an array
index, JSON Pointer, file line, serialized position, byte offset or generated
schema path.

A future D7 diagnostic binding may use binding-specific locations for reporting,
but such locations are not requirement identity.

### Requirement applicability representation

`applicability` contains explicit assessable descriptors. It may refer to
assessed SemanticDocument or Projection content, record category, semantic role,
exact term or Vocabulary edition, declared Projection scope, explicit selection
context, material-context state, Source or Binding participation, lifecycle
state or other Profile-defined assessment context represented by the Profile
artifact.

In binding `0.1.0`, this envelope-level member is the unique primary
representation for normative applicability. There is no `requirement_kind =
applicability`, and D6 defines no recursive requirement that selects other
requirements.

`applicability` MUST NOT depend on ambient implementation state, hidden runtime
state, GUI state, environment variables, filesystem state, network state,
resolver cache state, model output or current wall-clock time unless a future
accepted rule supplies an explicit evaluation context with defined semantics.

D6 does not define a selector language. Applicability descriptors identify when
a requirement applies; they do not search source content, generate a Projection
or choose requirements by execution order.

```text
applicability descriptor
!= requirement selection algorithm

applicability
!= query

applicability
!= hidden runtime condition
```

### Vocabulary dependencies

`vocabulary_dependencies` declares exact Vocabulary editions needed to evaluate
requirements. Each dependency contains Vocabulary family identity, exact
Vocabulary version and dependency role.

Dependency role distinguishes:

- `required_exact_edition`;
- `allowed_alternative_exact_edition`.

A required exact edition is not satisfied by a newer edition, similar edition,
compatible-looking edition, local prefix, namespace expansion base, registry
lookup or AI similarity. Allowed alternatives must be explicitly listed as exact
Vocabulary editions.

The binding preserves:

```text
Vocabulary family identity + exact Vocabulary version
!= namespace expansion base
```

The Profile artifact does not redefine Vocabulary meaning.

## Projection artifact

A Projection artifact represents one finite derived Projection. It contains
these required member groups:

- `artifact_kind`;
- `binding`;
- `profile_edition`;
- `source_state`;
- `selection_context`;
- `projection_scope`;
- `projection_completeness`;
- `carried_content`;
- `namespaces`, when required by compact qualified terms in `carried_content`;
- `reference_availability`.

It may contain optional member groups for:

- `projection_artifact_id`;
- `boundedness`;
- `truncation`;
- `omissions`;
- `projection_continuations`;
- `dependency_continuations`;
- `material_context`;
- `profile_artifact_reference`;
- non-mandatory artifact metadata.

The Projection artifact MUST refer to the exact Profile edition that governs its
interpretation. It MUST NOT embed a different requirement set that overrides or
redefines that Profile edition.

## Binding-defined descriptor structure

D6 defines binding grammar for descriptor member groups without converting this
ADR into JSON Schema. Each descriptor has binding-defined slots and may contain
Profile-supplied values only inside those slots.

| Descriptor/member group | Binding-defined structure | Profile-supplied value boundary |
| --- | --- | --- |
| `applicability` | subject category, basis kind, explicit context reference and expected value. | The Profile supplies exact terms, roles, categories or context values; it cannot add hidden state, selectors or new operators. |
| `source_state` | source SemanticDocument identity, source scope when known, source Revision identity when exact, or explicit source-state descriptor when no Revision exists. | The Profile/source supplies identifiers and descriptors; it cannot fabricate a Revision or require source execution. |
| `selection_context` | selection context kind, explicit descriptor and optional references to Profile-defined selection inputs. | The Profile supplies values that identify the selection context; it cannot define a query language, prompt or retrieval algorithm. |
| `projection_scope` | declared scope kind, scope descriptor and optional requirement reference. | The Profile supplies scope values; it cannot redefine Projection completeness states. |
| `boundedness` | bound dimension/rule, limit value and whether the bound was reached. | The Profile supplies dimension/unit/rule values; it cannot make tokenizer or model-window behavior universal. |
| `truncation` | truncation-established indicator, affected scope and optional bound/requirement reference. | The Profile supplies references or reason values; it cannot make truncation mean unknown completeness. |
| `omissions` | omitted target/category/scope, omission category and optional requirement/dependency-continuation reference. | The Profile supplies target/category descriptors; omission semantics remain ADR-0026 semantics. |
| `projection_continuations` | continuation scope, continuation descriptor and optional source-state/Profile references. | The Profile supplies inert handles or locators; they are not fetch or execution instructions. |
| `dependency_continuations` | dependency target, dependency descriptor and optional availability/omission reference. | The Profile supplies inert handles or locators; dependency continuation remains distinct from Projection continuation. |
| `material_context` | target context, preservation state token and optional references to carried records, omissions or dependency continuations. | The Profile supplies target/context values; it cannot create a second source of reference availability, omission or continuation truth. |
| `reference_availability` | reference target and `availability_state = carried | external | unassessed`, plus optional reference to the primary descriptor explaining an external target. | The Profile supplies target references; availability does not assert omission, continuation or preservation semantics. |

```text
binding-defined structure
vs
Profile-supplied value
```

A Profile may instantiate binding-defined descriptor slots. It MUST NOT define
new descriptor slots, operators, precedence rules or grammar under the same
binding version.

## Projection artifact identity

`projection_artifact_id` is optional.

D6 does not require every Projection artifact to have a universal artifact
identity. When a Projection needs citation, continuation, exchange tracking or
future diagnostics, `projection_artifact_id` may identify that Projection
artifact or view.

When present, `projection_artifact_id` is separate from source SemanticDocument
identity, Entity IDs, Assertion IDs, Source IDs, Binding IDs, Revision IDs and
carried trust-record IDs. It is not derived automatically from content bytes, is
not a Core Entity identity and is not proof of Profile conformance.

If absent, the Projection artifact is still interpretable from its source-state,
Profile edition, selection context, Projection scope and carried content.

## Source-state traceability

`source_state` represents D2 traceability. It contains:

- source SemanticDocument identity;
- source scope when known;
- source Revision identity when the source state has an exact Revision;
- source-state descriptor supplied explicitly when no exact Revision exists.

If a source Revision exists, the binding can represent it. If no Revision is
identified, the binding MUST NOT fabricate one.

D6 does not require hashes, signatures or fingerprints for source-state
traceability. Integrity evidence remains separate from semantic source-state
identity unless a future accepted ADR requires it.

## Selection context

`selection_context` represents the explicit selection context required by D2 and
D5. It is inert metadata. It does not define a query language, selector
language, model prompt, embedding search, runtime retrieval or generation
algorithm.

The selection context must be explicit enough for deterministic assessment under
the exact Profile edition, but D6 does not define every possible Profile-defined
selection descriptor.

## Projection scope and completeness

`projection_scope` represents the declared Projection scope.

`projection_completeness` is exactly one of:

```text
complete
partial
unknown
```

It is interpreted only relative to the declared Projection scope under ADR-0026.
It is not copied automatically from source SemanticDocument completeness.

D6 preserves:

```text
Profile conformance != Projection completeness

known required in-scope omission => partial
```

The binding MUST NOT create a second completeness system.

## Carried semantic content

`carried_content` transports selected semantic records using the accepted S2
record shapes for the carried record bodies. It is not a new Core primitive and
it is not a mutation of the source SemanticDocument.

When a source record is transparently carried, its accepted semantic identity
must be preserved:

- Entity IDs remain Entity IDs;
- Assertion IDs remain Assertion IDs;
- Source IDs remain Source IDs;
- Binding IDs remain Binding IDs;
- identified Provenance, Confidence and Review IDs remain their IDs;
- Revision and reference targets remain their targets;
- qualified terms continue to expand to the same absolute term identities.

The binding MUST NOT re-identify carried records for Projection convenience. It
MUST NOT replace selected source content with summaries under original IDs. It
MUST NOT turn local prefixes into semantic identity.

Carried term identity must remain deterministically resolvable offline. Because
S2 qualified terms use compact `prefix:local` spelling plus the S2 `namespaces`
expansion map, a Projection artifact that carries compact qualified terms MUST
also carry the namespace expansion entries needed to expand every such term in
`carried_content`. It may carry only the needed entries, but it MUST NOT depend
on a prefix/context mapping that remains only in the source artifact and was not
transported with the Projection.

The binding reuses the accepted S2 namespace-map mechanism. It does not invent a
new Vocabulary identity mechanism, and it does not compute term identity from
Vocabulary family, Vocabulary version, preferred prefix, Profile version or AI
inference. A Projection may change local prefix spellings only when the carried
namespace expansion context preserves the same expanded absolute term identity.

```text
carried term identity must remain deterministically resolvable offline
local prefix != term identity
change of local prefix != change of absolute term identity
missing expansion context != permission to guess term identity
AI inference != term resolution
```

A Projection artifact may carry enough content to be exportable as a valid S2
SemanticDocument by a separate tool, but D6 does not require every Projection
artifact to be a standalone S2 SemanticDocument. The default D6 artifact is an
AI Context Projection envelope carrying S2 record bodies plus Projection
metadata.

## Projection namespaces

`namespaces` is the Projection artifact member group that carries the S2
namespace expansion context needed by carried S2 qualified terms. It reuses the
accepted S2 `namespaces` expansion-map semantics exactly and does not create a
second namespace mechanism.

```text
namespaces
= carried S2 namespace expansion context

compact qualified term in carried_content
whose expansion depends on prefix mapping
=> corresponding namespaces entry required
```

`namespaces` may be omitted only when no transported term needs that context,
for example when every applicable term identity is represented by a binding-
permitted absolute identity form rather than by a compact S2 qualified term. For
ordinary carried S2 record bodies using compact `prefix:local` terms, every used
prefix required for expansion must have a corresponding carried `namespaces`
entry. The map may contain only the required entries or additional valid entries
allowed by the binding, but every compact term in `carried_content` must be
resolvable deterministically offline.

The carried namespace map must preserve the expanded absolute term identities of
carried source terms. It MUST NOT replace a source term's expansion with a
different absolute term identity for Projection convenience.

```text
Projection namespaces
!= Vocabulary dependencies

namespace prefix
!= Vocabulary identity

namespace map
!= Profile requirement set
```
## Reference transport

D6 represents reference transport with `reference_availability` instead of
silently rewriting references.

When carried records contain S2 references, the reference target identity must
remain the accepted target identity. `reference_availability` describes only the
materialization status of that target within the current Projection artifact:
carried/materialized here, external/not carried here or not assessed for this
artifact.

`reference_availability` is not the normative source for omission,
continuation, dependency-continuation or material-context preservation meaning.
Known omission is represented by `omissions`; dependency continuation is
represented by `dependency_continuations`; Projection continuation is represented
by `projection_continuations`; material-context preservation is represented by
`material_context`. If `reference_availability` reflects one of those states, it
must do so only by a non-authoritative reference to the corresponding descriptor
and must remain consistent with it.

This availability statement does not retarget the reference, materialize the
target, prove target existence, assert omission, assert continuation or satisfy a
material-context requirement.

If a reference was locally resolvable in the source but the target is outside
the Projection, the binding MUST NOT fabricate a local target and MUST NOT
silently change semantic target identity. A Profile may permit the target to
remain outside the Projection by exact reference; otherwise omission and
completeness semantics apply under ADR-0026 and ADR-0027.

D6 defines no field-order precedence or winner-takes-all conflict rule between
these member groups. Contradictory duplicated metadata is not a valid conflict
resolution mechanism; D7 remains responsible for result and diagnostic shape.

D6 preserves:

```text
reference target identity
!= reference availability

reference availability
!= omission semantics

reference availability
!= continuation semantics

reference availability
!= material-context preservation semantics

reference preservation
!= target materialization

contradictory duplicated metadata
!= valid conflict-resolution mechanism
```

## Omission representation

`omissions` represents known omission inside the declared Projection scope. It is
compact descriptive metadata and does not require enumerating all unselected
source content.

An omission descriptor can identify the omitted record or target when known, the
omitted category or Profile-defined scope when exact target enumeration is not
required, and the applicable requirement or Profile-defined omission category
when present. If omitted content is also available through dependency
continuation, the dependency-continuation assertion belongs in
`dependency_continuations`; the omission descriptor may only refer to that
separate descriptor consistently.

Omission remains distinct from deletion, falsity, invalidity and Tombstone.

```text
omitted != deleted
omitted != false
omitted != invalid
omitted != Tombstone
```

## Boundedness and truncation

`boundedness` represents the finite limiting policy that applied to the
Projection. A bound descriptor can represent Profile-defined dimension, unit or
rule, limit and whether the bound was reached.

A quantitative bound is meaningful only when its dimension/unit/rule is defined
by the exact Profile edition. D6 does not make token count, model context window
or tokenizer behavior a universal semantic bound.

`truncation` is separate from `boundedness`. If `truncation` is present, it
establishes known incompleteness relative to the declared Projection scope and
therefore implies `projection_completeness = partial`.

```text
bounded != truncated
truncated => partial
bounded + unknown is possible
```

## Continuation representation

Projection artifacts represent continuation with two distinct member groups:

- `projection_continuations`;
- `dependency_continuations`.

Both are inert data. A descriptor may contain binding-defined fields carrying
Profile-supplied IRI, locator, token or handle data, but the descriptor is not an
instruction to fetch, execute, dereference, call an API, run a tool or grant
permission.

Continuation semantics originate in these continuation member groups, not in
`reference_availability` or `material_context`. A target that is external in
`reference_availability` is not a dependency continuation unless a corresponding
`dependency_continuations` descriptor asserts that dependency continuation.

```text
continuation != URL fetch
continuation != API cursor execution
continuation != tool call
continuation != permission
projection continuation != dependency continuation
```

## Material context and preservation representation

`material_context` represents D4/D5 preservation decisions. It can distinguish:

- material context carried in the Projection;
- exact reference sufficient under the exact Profile edition;
- required materialization;
- explicit material omission;
- dependency continuation when the dependency is a material-context dependency.

`material_context` is the primary representation for preservation state and
requirements. It may refer consistently to carried records, omission descriptors
or dependency-continuation descriptors, but it MUST NOT become a second
independent source of reference availability, omission, Projection-continuation,
self-containment or closure truth for the same target. Self-containment and
closure policy belong to the `closure` requirement kind; preservation metadata
may reference those requirements without duplicating their authority.

D6 does not create global trust objects and does not alter trust nesting scope.
Anonymous Provenance, Confidence and Review records remain scoped to their
accepted host. Identified trust records keep their IDs when carried.

```text
explicit omission != preservation
allowed by reference != materialized
Profile allows omission != Projection complete
```

## Extensions

Profile and Projection artifacts use the accepted ADR-0015 Extension rules for
Extension data carried from S2 records. Unknown Extensions remain inert opaque
data.

A Profile requirement artifact may require a known Extension for Profile
conformance without making that Extension Core. A Projection artifact claiming
lossless preservation of a carried record MUST NOT drop or alter that record's
unknown Extensions.

D6 does not create a second Extension mechanism for AI Context.

## Profile declaration in Projection artifacts

A Projection artifact must declare the exact Profile edition it is governed by.
That declaration is not proof of Profile conformance.

D6 does not define `conformant: true`, `valid: true`, diagnostic codes,
severity, unsupported-result serialization, unavailable-dependency result
serialization or reporting format. D7 remains responsible for Profile
conformance result and diagnostics.

## Offline and deterministic processing

Profile requirement artifacts and Projection artifacts must be interpretable from
artifacts supplied locally to the assessor. The binding requires no automatic
network access, `geesno.com` availability, registry, resolver, remote schema,
remote Vocabulary, AI model, embedding service or runtime tool.

IRIs in the binding are identities, not dereference instructions.

## Profile artifact integrity

D6 distinguishes exact Profile edition semantic identity from physical artifact
integrity. The exact Profile edition is identified by Profile family identity
and exact Profile version. A future artifact fingerprint, digest, signature or
publication proof would be integrity evidence for a physical artifact, not the
Profile edition identity itself.

D6 does not require cryptographic signatures or mandatory hashes. Integrity and
signature policy remain open unless a later accepted ADR requires them.

## Canonicalization boundary

D6 does not introduce canonical byte serialization. Deterministic semantic
validation is distinct from byte canonicalization.

If future signatures, content-addressing or digests require canonicalization,
that must be handled by a later accepted decision.

## D7 boundary

D7 remains responsible for conformant/nonconformant result model, diagnostic
codes, severity, unsupported requirement result serialization, unavailable
dependency result serialization, reporting format and profile conformance
fixtures.

D6 prepares for D7 by allowing future diagnostics to refer to exact Profile
edition, optional stable requirement IDs and optional Projection artifact IDs.
It does not define D7 results. D7 may report unsupported, unavailable or invalid
binding constructs, but it must not treat Profile-invented grammar under the same
binding version as if it were normative D6 binding grammar.

## D8 boundary

D6 defines no Profile merge, inheritance, precedence, override or conflict
resolution. A Profile artifact represents one exact Profile edition. A
Projection artifact is governed by one exact Profile edition.

If future artifacts need to mention additional Profile-related metadata, that
metadata must not be interpreted as Profile composition.

```text
P1 + P2 != merged Profile
```

## S2 core boundary

D6 keeps `schema/v0.1/geesno-semantic.schema.json` intact. It does not add S2
Core members and does not modify the S2 SemanticDocument contract.

The chosen Projection envelope carries S2 record bodies and uses separate D6
metadata for Profile/Projection concerns. This avoids adding AI Context fields
to S2 Core and avoids forcing every Projection to be a self-contained S2
SemanticDocument.

When carried S2 record bodies contain compact qualified terms, D6 reuses the S2
`namespaces` expansion-map semantics through the Projection artifact's
`namespaces` member group. This preserves deterministic term expansion without
modifying S2 schema or creating a new Vocabulary identity mechanism.

No blocker requiring S2 modification was found.

## Cross-domain validation

| Domain | Stress case | Result |
| --- | --- | --- |
| Engineering-like object graph | Component assertions refer to connected components omitted from a compact Projection. | Reference targets are preserved while availability is represented separately; no fabricated local component is needed. |
| Spreadsheet/table data | A Profile requires exact Vocabulary editions for column labels and allows listed alternatives. | `vocabulary_dependencies` can distinguish required exact editions from explicit alternatives without changing Vocabulary meaning. |
| Technical/legal document | Selected clauses carry Review and Provenance, while background definitions remain by exact reference. | Material-context descriptors distinguish carried context, reference-sufficient context and explicit omission. |
| Software/source repository | A Projection cites source Revision identity when available but does not run build tools or Git operations. | `source_state` can represent source Revision without execution or Git semantics in core. |
| Scientific dataset | Measured observations require exact unit terms and uncertainty context. | Carried S2 records keep exact values/terms while Profile requirements express preservation/materialization obligations. |
| Generic product/asset data | A product summary is partial, bounded and has supplier metadata available through dependency continuation. | Completeness, boundedness, truncation and dependency continuation remain separate inert metadata. |

## Adversarial cases

| # | Case | Required interpretation | Must not infer |
| --- | --- | --- | --- |
| 1 | Profile IRI looks like a URL | It is Profile identity. | Mandatory dereference. |
| 2 | Profile artifact is loaded from a file path | File path is artifact location. | Profile identity. |
| 3 | Profile artifact URL changes | Artifact location changed. | Profile family identity changed. |
| 4 | Profile declares `latest` | Not an exact Profile version. | Reproducible conformance. |
| 5 | Profile version equals binding version textually | Separate version axes may share a token. | Same identity dimension. |
| 6 | Core `spec_version` is `0.1.0` | S2 instance contract. | AI Context binding version. |
| 7 | Vocabulary version is `0.1.0` | Vocabulary edition version. | Profile or binding version. |
| 8 | Requirement appears first in array | Serialization order only. | Priority or override. |
| 9 | Requirement JSON contains a string that looks like code | Inert data. | Code execution. |
| 10 | Requirement references a remote evaluator | Not allowed as normative evaluation. | Remote validation requirement. |
| 11 | Profile declaration appears in Projection | Governing exact Profile edition is declared. | Proof of Profile conformance. |
| 12 | Projection artifact has an ID | Artifact/view identity if present. | Entity ID or source document ID. |
| 13 | Projection artifact ID equals a carried Entity ID | Invalid identity collision for transparent Projection. | Same object. |
| 14 | Source document ID differs from Projection artifact ID | Correct separation. | Source mutation. |
| 15 | Source Revision absent | No exact source Revision is claimed. | Fabricated Revision. |
| 16 | Source Revision present | Traceability can identify source state. | Git branch or replay semantics. |
| 17 | Carried Assertion has same ID as source | Transparent carriage. | New Assertion. |
| 18 | Carried Assertion is re-identified | Not transparent carriage. | Same source Assertion. |
| 19 | Local source reference target is omitted | Target identity remains; availability differs. | Retargeting or fabricated target. |
| 20 | Missing dependency is represented by dependency continuation | Dependency may remain outside Projection. | Local materialization. |
| 21 | Exact reference is sufficient under Profile | Reference can satisfy requirement. | Target materialized. |
| 22 | Required material context is omitted | Omission must be explicit and completeness follows ADR-0026. | Preservation. |
| 23 | Omission descriptor exists | Known omission. | Deletion, falsity, invalidity or Tombstone. |
| 24 | Profile allows partial Projection | Profile may allow conformance. | Projection complete. |
| 25 | Bound descriptor exists | Boundedness policy applied. | Truncation. |
| 26 | Bound reached, no truncation established | Bounded and possibly unknown/complete depending on scope. | Known truncation. |
| 27 | Truncation descriptor exists | Known incomplete relative to Projection scope. | Unknown completeness. |
| 28 | Continuation contains IRI | Inert descriptor data. | URL fetch. |
| 29 | Continuation contains token | Inert descriptor data. | API cursor execution. |
| 30 | Dependency continuation present | External dependency may be needed. | More of same Projection segment. |
| 31 | Projection continuation present | More projected content may exist. | Dependency materialized. |
| 32 | Source locator appears in carried Binding | Source-relative correlation. | Semantic identity. |
| 33 | Binding source target outside Projection | External or dependency target. | Binding retargeted to a local Source. |
| 34 | Anonymous Review is carried under host | Scope is preserved. | New global Review identity. |
| 35 | Anonymous Review receives ID for extraction | New content unless source had that ID. | Continuity of original anonymous Review. |
| 36 | Unknown Extension dropped under lossless claim | Violates lossless preservation claim. | Valid lossless carriage. |
| 37 | Unknown Extension omitted in lossy Projection allowed by Profile | Explicit/lossy omission may be allowed. | Extension became Core. |
| 38 | Network outage prevents fetching Profile URL | Artifact unavailable if not local. | Invalid Profile identity. |
| 39 | `geesno.com` unavailable | No automatic dereference. | Conformance impossible solely from outage. |
| 40 | Two byte-different Profile artifacts represent same exact edition | Possible absent accepted canonicalization/integrity rule. | Semantically different solely by bytes. |
| 41 | Artifact fingerprint is present | Integrity evidence for artifact. | Profile semantic identity. |
| 42 | No artifact fingerprint is present | Integrity not claimed. | Invalid Profile identity. |
| 43 | Multiple Profile declarations are present in external packaging | D6 defines no merge. | Composed Profile. |
| 44 | Projection embeds alternate requirements | Not governing requirements unless they match exact Profile artifact role. | Projection redefines its Profile. |
| 45 | Consumer treats carried record set as a full S2 document | It is a Projection envelope payload unless separately exported/validated. | Universal self-contained S2 document. |
| 46 | Local prefix differs from source prefix | Term identity follows expanded absolute term identity. | New term identity. |
| 47 | Similar Vocabulary edition is available locally | May be evidence only if Profile allows it. | Required exact edition satisfied. |
| 48 | Binding schema later validates structure | Schema checks representation. | Schema originates D6 semantics. |
| 49 | Projection artifact claims complete with known required omission | Contradiction under ADR-0026/0027. | Complete Projection. |
| 50 | `conformant: true` appears in extension metadata | Not a D7 result. | Proof of conformance. |
| 51 | Profile edition declares a new `requirement_kind` under binding `0.1.0` | Not supported by this binding version. | Profile silently extends binding grammar. |
| 52 | Profile edition defines normative sub-kind semantics inside `requirement_body` | Requires a new binding version or later accepted Extension mechanism. | Sub-kind becomes normative under same binding version. |
| 53 | Requirement body contains an unknown operator | Unsupported/invalid binding construct. | New evaluator semantics. |
| 54 | Unaccepted Extension claims to add requirement grammar | Inert unless later architecture accepts such a mechanism. | Extension redefines D6 grammar. |
| 55 | `reference_availability` says target is carried while `omissions` says same target is omitted | Contradictory duplicated metadata; D7 may diagnose. | Field order chooses a winner. |
| 56 | Target is external in availability while `material_context` claims carried context for same target | Contradictory metadata requiring diagnosis. | External and carried are both true. |
| 57 | Dependency continuation is asserted only through `reference_availability` | No dependency continuation has been asserted. | Availability creates continuation semantics. |
| 58 | Two member groups disagree and consumer uses member order as precedence | No D6 precedence rule exists. | Earlier/later member wins. |
| 59 | Carried compact term but source prefix declaration was not carried | Term identity is not deterministically resolvable offline. | Guess namespace from source or preference. |
| 60 | Same prefix spelling maps differently in another artifact | Prefix spelling is local to carried expansion context. | Same prefix spelling means same term. |
| 61 | Prefix changes while expanded absolute term identity remains the same | Same term identity may be preserved. | New term because prefix changed. |
| 62 | Consumer guesses namespace from preferred Vocabulary prefix | Invalid term resolution. | AI or convention supplies term identity. |
| 63 | Compact carried term present but top-level `namespaces` absent | Term identity is not deterministically resolvable offline. | Source artifact context can be assumed. |
| 64 | Required namespace entry is absent | The compact term cannot be expanded by this artifact. | Consumer may invent or fetch the mapping. |
| 65 | `namespaces` maps a carried prefix differently from the source term identity | The carried term identity changed unless the absolute expansion is preserved by another allowed spelling. | Prefix spelling alone preserves identity. |
| 66 | `vocabulary_dependencies` is present but `namespaces` is absent | Vocabulary dependency is not namespace expansion context. | Preferred Vocabulary prefix substitutes for `namespaces`. |
| 67 | `requirement_body` contains a member not defined for its `requirement_kind` in binding `0.1.0` | Unsupported or invalid binding construct. | Profile-defined grammar extension. |
| 68 | Future JSON Schema validates an enum not listed by ADR-0029 | Schema is ahead of accepted grammar. | Schema originated the normative construct. |
| 69 | Profile supplies a value inside a binding-defined slot | Allowed if the slot is defined by binding `0.1.0`. | Profile created new grammar. |
| 70 | Profile supplies a new descriptor slot/operator | Not supported under binding `0.1.0`. | Descriptor grammar extension. |
| 71 | Envelope `applicability` and an obsolete `applicability` requirement kind express different conditions | The applicability-kind construct is unsupported in binding `0.1.0`; envelope `applicability` is the only primary authority. | Two applicability authorities are merged by order. |
| 72 | `requirement_mode = required` while body-local grammar says prohibited | Contradictory body-local mode is unsupported or invalid. | Body wins over envelope or creates precedence. |
| 73 | `requirement_mode = prohibited` while body-local grammar says required | Contradictory body-local mode is unsupported or invalid. | Envelope wins because it appears earlier. |
| 74 | Projection and preservation both require dependency continuation with different rules | Preservation owns dependency continuation when it is a material dependency; Projection owns Projection continuation. | Duplicate owners are reconciled by order. |
| 75 | Preservation metadata demands self-containment while closure permits external references | Closure owns self-containment and external-reference policy; the conflict requires diagnosis. | Preservation silently overrides closure. |
| 76 | Two requirement kinds govern the same semantic dimension and a consumer uses array order to decide | Same dimension must have one primary owner; order is not precedence. | First or last requirement wins. |
| 77 | Requirement references coordinate projection and preservation requirements | Cross-reference coordinates independent requirements without fusing their authority. | Cross-reference creates a merged requirement kind. |

## Consequences

- S4 gains an accepted concrete binding architecture without changing S2 Core.
- Profile requirement artifacts and Projection artifacts are separate roles.
- The binding has its own version, distinct from Core, Profile and Vocabulary
  versions, and that exact binding version owns the concrete binding grammar.
- Profile requirements are represented as finite typed requirement envelopes,
  not as arbitrary executable code or a general expression language; exact
  Profile editions may instantiate supported constructs but may not add grammar
  under the same binding version.
- Projection artifacts use an AI Context envelope carrying S2 record bodies plus
  explicit Projection metadata, including the conditionally required
  `namespaces` member group for compact carried qualified terms.
- Carried semantic IDs, reference targets and qualified-term identities are
  preserved; compact qualified terms require transported S2 namespace expansion
  context.
- Requirement bodies have a finite declarative binding `0.1.0` grammar per
  the eight final `requirement_kind` values; future schema may validate that
  grammar but must not invent it.
- Envelope-level `applicability` is the only primary representation for
  normative requirement applicability, and envelope-level `requirement_mode` is
  the only authority for the required/optional/prohibited axis.
- Reference availability, omission, Projection continuation, dependency
  continuation and material-context preservation each have one primary
  representation, with no field-order precedence for contradictory duplicates.
- Omission, boundedness, truncation, continuation, dependency continuation and
  material-context preservation receive concrete artifact locations without new
  semantics.
- Projection artifact identity is optional and remains separate from carried
  semantic object identity.
- D7 diagnostics/results and D8 composition remain open.
- No schema, fixtures, SDK, runtime, tag, publication, registry or resolver is
  created by this ADR.

## Remains open

- concrete JSON Schema for the AI Context binding after D6 acceptance;
- Profile conformance result model and diagnostics under D7;
- normative fixtures for Profile/Profile-binding conformance;
- Profile composition and conflict policy under D8 if needed;
- artifact integrity, signatures, digests and canonicalization;
- packaging/media type/publication conventions;
- SDK/tooling behavior;
- public release status.

## Acceptance boundary

**Decision status: Accepted**

ADR-0029 is Accepted by explicit human architecture decision on 2026-09-24.
Acceptance closes S4 D6 only: concrete AI Context Profile requirement artifact
and Projection artifact binding architecture. It does not accept D7 conformance
result diagnostics, D8 Profile composition, concrete schema implementation,
fixtures, SDK APIs, runtime behavior, registry/resolver behavior, publication,
canonicalization, signatures, tag, release or execution behavior.
