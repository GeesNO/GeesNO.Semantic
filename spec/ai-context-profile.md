# AI Context Profile and Projection semantics 0.1

**Profile edition:** `0.1.0` (normative semantic requirements).

This specification consolidates the abstract AI Context Profile and Projection
semantics accepted by ADR-0024 through ADR-0028 and defines the approved exact
AI Context Profile edition `0.1.0`. The concrete
`ai-context-json/0.1.0` representation is defined separately in
[ai-context-json-binding.md](ai-context-json-binding.md).

The public architectural baseline is
[ARCHITECTURE.md](../ARCHITECTURE.md). Applicable accepted ADRs and normative
contracts remain authoritative in their respective scopes.

This document introduces no fixture corpus, evaluator or runtime behavior.

## Normative authority map

This specification derives its rules from the following accepted authorities;
the map supplies section-level traceability without duplicating the ADR text.

| Specification subject | Normative authority |
| --- | --- |
| Scope, descriptive boundary, provider neutrality and offline operation | `ARCHITECTURE.md`; ADR-0024 through ADR-0031 |
| Exact Profile edition identity and version behavior | ADR-0024 |
| Projection definition, source state, selection, scope and carried identity | ADR-0025 |
| Completeness, omission, boundedness, truncation and both continuation distinctions | ADR-0026 |
| Material context, preservation, trust scope, Validity and Source/Binding traceability | ADR-0027 |
| Requirement modes, applicability, exact Vocabulary semantics and deterministic assessment | ADR-0028 |
| Profile/Projection artifact roles, concrete binding ownership, namespace transport and reference availability | ADR-0029 |
| Assessment-result model and separate binding boundary | ADR-0030 |
| Profile composition and conflict-policy boundary | ADR-0031 |

## Scope

The AI Context Profile defines a compact, traceable and descriptive Projection
of accepted GeesNO.Semantic content. It is universal, domain-neutral,
software-neutral, format-neutral, model-provider-neutral and offline-capable.

```text
AI Context Profile
= contextual semantic requirements

AI Context Profile
!= Core
!= Vocabulary
!= prompt
!= model configuration
!= agent
!= tool
!= runtime
```

The Profile MUST NOT define commands, application control, retrieval execution,
model routing, RAG, embeddings, vector databases, tool calls, permissions or
GeesNO.Core behavior.

## Profile edition identity

A Profile family identity is a stable absolute IRI. A Profile version is a
non-empty opaque token scoped to that family. An exact Profile edition is:

```text
Profile edition
= profile_family + exact profile_version
```

The initial AI Context Profile edition is identified by:

```text
profile_family  = https://geesno.com/profile/ai-context
profile_version = 0.1.0
```

Both values are compared exactly. A processor MUST NOT infer ordering,
compatibility, replacement or recency from version spelling. `latest`, moving
aliases, ranges, automatic upgrade and compatible-looking substitutions MUST
NOT identify the exact edition.

The Profile family IRI is identity, not a retrieval instruction. Profile
selection and assessment MUST NOT require a resolver, registry, network access
or dereference.

One exact edition identifies one immutable normative requirement set. A
material requirement change requires a new exact Profile version. A declaration
of the exact edition is not proof of conformance.

## Profile requirement semantics

An exact Profile edition is the semantic authority for its finite requirement
set. A binding represents that set but does not originate its meaning.

Profile requirements MAY address structure, cardinality, exact Vocabulary
editions or terms, Projection policy, material-context preservation,
Source/Binding participation, known Extensions and closure. They remain inert
conditions and MUST NOT execute code, select source content, mutate source
state, redefine Vocabulary meaning or assert semantic truth.

Requirement modes are:

- `required`: the applicable condition MUST be satisfied;
- `optional`: absence allowed by the requirement is not a violation, but
  present applicable material MUST satisfy the requirement;
- `prohibited`: the applicable material or condition MUST NOT be present or
  used.

```text
optional != ignored
not required != prohibited
mode != priority
requirement order != precedence
```

Applicability MUST be determinable from explicit assessable information named
by the exact Profile edition. It MAY depend on assessed content, record
category, semantic role, exact term or Vocabulary edition, Projection scope,
selection context, material-context state, Source/Binding participation,
lifecycle state or other explicit Profile-defined assessment context.

Applicability MUST NOT depend normatively on hidden runtime state, GUI state,
environment variables, filesystem state, network responses, resolver cache,
model output, implementation preference or undeclared current time. It is not a
selector, query, ranking function, expression language or execution condition.

## AI Context Profile edition 0.1.0

This section is the normative semantic authority for the Profile-defined tokens
used by the exact AI Context Profile edition:

```text
profile_family  = https://geesno.com/profile/ai-context
profile_version = 0.1.0
```

The normative structured requirement artifact is
[`../profiles/ai-context/v0.1/profile.json`](../profiles/ai-context/v0.1/profile.json).
Its repository path is local organization, not Profile identity, an artifact
IRI, a publication URL or a dereference instruction.

The exact edition contains these nine stable requirement IDs:

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

It uses only `projection`, `preservation`, `source_binding` and `closure`.
It defines no `structure`, `cardinality`, `vocabulary` or `extension`
requirement instance, and its `vocabulary_dependencies` value is exactly `[]`.
The accepted binding grammar already defines structure; no universal compactness count is
accepted; these requirements use no exact Vocabulary term or edition; and no
exact Extension term is required.

Requirement array order is editorial only:

```text
requirement array order
!= priority
!= precedence
!= execution order
!= requirement identity
```

The nine IDs and their complete bodies, modes and applicability objects in the
artifact form one immutable normative requirement set. Changing any of those
semantics, the requirement count, or Vocabulary dependencies requires a new
exact Profile version. This rule does not define a version-upgrade mechanism.

### Applicability patterns

Edition `0.1.0` defines exactly three applicability patterns.

For universal Projection applicability:

```text
subject_category = projection_artifact
basis_kind       = always
expected_value   = absent
```

This pattern applies to every Projection assessed against this exact edition.

For material-context applicability:

```text
subject_category = material_context
basis_kind       = material_context_condition
expected_value   = one exact condition token defined below
```

The condition is established from explicit assessable information, exact
Profile semantics, accepted Core/Projection semantics and locally available
exact context. These tokens are inert assessment categories, not selectors,
expressions, executable predicates, a query language, a rule engine, model
classification or hidden runtime state.

For material Source or Binding applicability:

```text
subject_category = source_record | binding_record
basis_kind       = material_to_projection
expected_value   = true
```

This pattern applies only when explicit assessable information and accepted
semantics establish that the Source or Binding is material to correct origin,
traceability or correlation in the Projection. It does not require every Source
or every Binding.

### Material-context condition tokens

`carry_required` applies when explicit content and accepted semantics establish
that material context must be transported because reference-only or absent
handling would lose or alter correct interpretation, host-scoped trust,
limiting Validity, required Provenance/traceability or other material scoped
meaning. Applicability is established before and independently of any existing
`carried` declaration.

`exact_reference_sufficient` applies when an exact independently preserved
reference or identity retains all material semantic information required by the
Projection; the target body is unnecessary for correct interpretation, trust
scope, Validity and traceability; and no accepted semantic rule requires its
carriage or materialization. Applicability does not derive circularly from the
`material-context-reference` policy itself.

`explicit_omission_required` applies when known context belongs or is material
to declared Projection scope, is not carried, and preservation is satisfied by
neither applicable carriage nor exact-reference sufficiency. The resulting
known preservation gap requires accepted omission representation and
`projection_completeness = partial`. Applicability is established independently
of whether an omission descriptor has already been emitted. Omission remains
distinct from preservation, deletion, falsity, invalidity and Tombstone.

`dependency_continuation_required` applies when an uncarried material
dependency is necessary to resolve, interpret or inspect carried semantic
content or a carried reference. The need is established independently of any
existing dependency-continuation descriptor. Its required representation is
inert and implies no retrieval, resolver action, availability, fetch, command
or Projection continuation.

For the same material-context target and preservation obligation,
`carry_required` is incompatible with `exact_reference_sufficient`,
`explicit_omission_required` and `dependency_continuation_required` when they
describe alternative dispositions of the same material body.
`exact_reference_sufficient` is incompatible with
`explicit_omission_required` and `dependency_continuation_required` for that
same obligation because no preservation or material-dependency gap remains.
`explicit_omission_required` MAY coexist with
`dependency_continuation_required` when one known omitted material dependency
must be exposed both as omission and as inert dependency continuation.

No condition has precedence over another. Applicability determines which
requirements apply; array order never resolves a conflict.

### Projection policy tokens

`explicit_deterministic_scope` requires declared Projection scope to be
explicit and deterministically interpretable. Scope MUST NOT be narrowed after
derivation to hide material context or make a partial Projection appear
complete.

`partial_projection_allowed` permits a truthful `partial` Projection relative
to its declared scope when all applicable obligations are satisfied. It does
not require partiality, and a truthful `complete` Projection remains permitted.

`unknown_completeness_allowed` permits `unknown` only when scope-relative
completeness has not been established. It does not require `unknown` and MUST
NOT hide established partiality:

```text
established truncation => partial
known required in-scope omission => partial
```

`partial_projection_allowed` and `unknown_completeness_allowed` are cumulative
permissions. Neither permission overrides evidence that requires `partial`.

`optional_explicit_finite_bound` makes boundedness optional. Any bound used
MUST be explicit and finite and MUST declare its dimension, rule and value
under the accepted grammar. It defines no universal item, token or byte count,
model context window, semantic priority, relevance or truth.

`declare_established_truncation` requires truncation to be declared only when
it is established. Established truncation requires
`projection_completeness = partial`. Boundedness or `bound_reached = true` does
not by itself establish truncation.

Edition `0.1.0` defines no universal `projection_continuation_policy`.
Projection continuation remains available only when independently justified
and declared under ADR-0026 and the applicable AI Context JSON binding.

```text
omission != Projection continuation
projection continuation != dependency continuation
```

### Source, Binding and closure policy

`source-record-traceability` and `binding-record-traceability` are conditionally
applicable through `material_to_projection`; they do not require all Source or
Binding records. Applicable Source context preserves material origin semantics.
Applicable Binding context preserves the exact Entity/Source correlation and
material locator, method and scoped context without turning a locator into
identity or either record into semantic truth.

`external-reference-closure` uses
`closure_scope = projection_artifact_references` and
`closure_policy = external_references_allowed`. External references are
permitted, not required. A self-contained Projection remains valid. The policy
does not imply target materialization, automatic dereference, availability or
network access.

## Projection definition

A Projection is:

```text
finite derived semantic view
of an identified source SemanticDocument state
under one exact Profile edition
and one explicit selection context
```

A Projection is not a source mutation, new semantic truth, Core primitive,
Vocabulary, prompt, AI inference or generated summary. Multiple Projections MAY
be derived from the same source state and exact Profile edition when their
selection contexts or declared scopes differ.

## Source-state traceability

Every Projection MUST identify the source SemanticDocument and preserve enough
explicit state context to relate the Projection to the state from which it was
derived. The context comprises:

- source SemanticDocument identity;
- source declared scope when known;
- exact semantic Revision identity when the source state has one; or
- an explicit source-state descriptor when no exact semantic Revision is
  identified.

The source SemanticDocument ID alone does not identify every historical state.
A Projection MUST NOT fabricate a semantic Revision. Semantic Revision, Source
revision, Source identity and locator remain separate.

```text
semantic Revision != Source revision
Source != Entity
locator != identity
```

Integrity evidence, byte hashes and signatures are not source-state identity
and are outside this specification.

## Selection context

Selection is the explicit derivation context that determines which source
content is carried. The Projection MUST represent that context explicitly, but
the algorithm that proposed or performed selection is outside the standard.

```text
selection != truth
selected != true
unselected != false
unselected != deleted
unselected != invalid
unselected != Tombstone
```

Selection metadata MUST NOT contain binding-level query, ranking, prompt,
embedding, RAG, semantic-search or model-selection semantics. External software
or AI MAY suggest a selection, but that implementation choice is not normative
Projection meaning.

## Projection scope

Source scope, selection scope and declared Projection scope are distinct.
Projection scope identifies what the Projection claims to cover and the scope
against which Projection completeness is assessed.

Content outside selection scope is unselected. It is not automatically omitted
inside Projection scope. A subset of source content is not automatically
partial when the declared Projection scope is narrower and fully represented.

Projection scope MUST be explicit and deterministically interpretable under the
exact Profile edition. Scope MUST NOT be narrowed after derivation merely to
hide material context known to be required for correct interpretation.

## Projection completeness

`projection_completeness` has exactly these states:

```text
complete
partial
unknown
```

- `complete` means complete only relative to declared Projection scope;
- `partial` means known incomplete relative to declared Projection scope;
- `unknown` means completeness relative to declared Projection scope has not
  been established.

Absence of omission metadata does not establish `complete`. A source
completeness claim MUST NOT be copied automatically to a different Projection
scope. `unknown` is not `partial`; `complete` is not source-wide completeness.

## Boundedness and truncation

A bounded Projection is intentionally limited by an explicit finite policy
whose dimension, unit and rule are defined by the exact Profile edition or
another accepted semantic rule. No byte, token, record or other measure is a
universal bound.

```text
bounded != complete
bounded != partial
bounded != truncated
bounded != relevance
bounded != importance
bounded != priority
```

Boundedness MAY coexist with `complete`, `partial` or `unknown`.

Truncation is established only when generation stopped before all content
required by declared Projection scope was included. Established truncation
MUST imply `projection_completeness = partial`.

```text
bound reached / bounded != truncation established
truncated => partial
truncated != unknown
truncated != deleted
```

## Omission

Unselected content and omitted content are distinct. Omitted content is inside,
or material to, declared Projection scope but not carried as required.

Omission metadata is descriptive. It MUST NOT delete source content, create a
Tombstone, change semantic identity, assert falsity, invalidate content,
authorize retrieval, retarget references or fabricate replacement state.

```text
unselected != omitted
omission != deletion
omitted != Tombstone
```

Known required in-scope material context that is omitted makes the Projection
`partial`. A Profile MAY permit a partial Projection or explicit omission, but
that permission does not preserve the omitted content or make the Projection
complete.

## Continuation

Projection continuation and dependency continuation are separate:

- Projection continuation describes additional content related to the same
  projected context outside the current segment;
- dependency continuation describes content needed to resolve, interpret or
  inspect a carried reference but not carried in the current Projection.

Continuation is inert metadata. It is not a cursor API, URL-fetch instruction,
resolver requirement, retrieval command, tool call, permission, availability
promise or trust claim.

Continuation MUST preserve source SemanticDocument identity, source-state
context, exact Profile edition, selection context and Projection scope. A
continuation of source state R1 MUST NOT silently resolve as the same
continuation against changed source state R2.

Declared continuation does not establish that additional content is available,
reachable, current or trustworthy.

## Carried semantic content

Carried content reuses accepted Core record meanings. Transparent carriage MUST
preserve:

- Entity IDs;
- Assertion IDs;
- Source IDs;
- Binding IDs;
- identified Provenance, Confidence and Review IDs;
- Revision and reference target identities; and
- expanded Vocabulary term IRIs.

A Projection MUST NOT re-identify records for convenience, fabricate IDs to
appear self-contained, silently retarget references, fabricate local targets or
replace source semantic content with an AI summary under the original IDs.

An independently derived summary would require its own identity, provenance and
accepted semantics; this specification does not define that model.

## Material context and preservation

Material context is context required for correct interpretation, traceability,
scoped trust, scoped validity or non-misleading presentation under the exact
Profile edition or another accepted semantic rule.

```text
material context != all context
material context != importance
material context != AI relevance
material context != execution priority
```

An applicable preservation requirement may be satisfied by carrying the
context record, or by preserving an exact reference when that exact requirement
permits the target to remain outside the Projection. Explicit omission or
dependency continuation declares a preservation gap; it does not preserve the
omitted content.

Preservation MUST retain exact host scope and meaning. It MUST NOT elevate,
propagate, fuse, widen or generalize Provenance, Confidence, Review, Validity,
Source or Binding context.

## Provenance, Confidence, Review and Validity

Material Provenance MUST remain scoped to the record it qualifies and MUST NOT
be treated as truth, authority or permission.

Material Confidence MUST retain its exact qualified semantics and scope. It
MUST NOT be transformed, recalibrated, aggregated or interpreted as truth or
probability unless its own accepted semantics define that meaning.

Material Review MUST remain scoped to its host. It is not truth, universal
approval, permission or execution authorization and MUST NOT be lifted to
related records.

Limiting Validity MUST NOT be silently omitted in a way that broadens the
apparent applicability or currentness of selected content. Validity remains
distinct from Revision membership, Provenance time, Source revision, latest
state and truth.

Anonymous nested trust records MUST remain nested in the host that establishes
their scope. A Projection MUST NOT invent identity, use array position or JSON
Pointer as identity, or claim independent continuity for an anonymous trust
record. Identified trust records retain their IDs.

## Source and Binding traceability

Source is separately referenceable origin context. It is not Entity, authority,
truth, locator, Source revision or fingerprint. Source records MUST NOT be
fabricated, equated by equal locations or automatically dereferenced.

Binding correlates exactly one Entity with exactly one Source under accepted
Core rules. When carried, a Binding MUST preserve its ID, Entity anchor, Source
anchor, locator semantics, method semantics and material scoped context.
Binding is not semantic truth, Entity identity or Source identity; its locator
is not identity.

An exact reference MAY remain outside the Projection only when the exact
Profile requirement permits it. Reference preservation is not target
materialization. Missing external content MUST NOT cause fabricated local
Source, Binding or other semantic records.

## Namespace context

When carried Core record bodies contain compact qualified terms, the Projection
MUST carry enough of the accepted Core namespace expansion map to recover every
expanded absolute term IRI offline. A prefix is not Vocabulary identity, and a
namespace IRI is not a dereference instruction.

Changing local prefix spelling MAY preserve term identity only when expansion
still yields the same absolute term IRI. Missing namespace context MUST NOT be
guessed from a preferred prefix, registry, network or AI inference.

## Extensions

Accepted Core Extension rules remain controlling. Unknown Extensions are inert,
opaque and non-executable. A Projection claiming lossless preservation of a
carried record MUST NOT drop, rewrite or semantically alter unknown Extensions
on that record.

A lossy Projection MAY omit Extension data only when the exact Profile edition
or another accepted semantic rule permits that loss and applicable omission
semantics are satisfied. Extensions MUST NOT redefine Core, binding grammar or
execution behavior.

## Offline and security boundary

Profile requirement artifacts and Projection artifacts MUST be interpretable
from locally supplied artifacts and explicit context. No automatic network
access, Profile or Vocabulary download, registry, resolver, model, embedding
service, continuation service or runtime tool is required.

Semantic text, IRIs, Source locations, Binding locators, Extension payloads and
continuation descriptors are untrusted inert data. They MUST NOT execute,
authorize operations or become prompt instructions merely because they occur in
an AI Context artifact.

## Binding and implementation boundary

The normative concrete representation for the two AI Context JSON artifact kinds is
[ai-context-json-binding.md](ai-context-json-binding.md). JSON Schema MUST
derive from that binding specification and MUST NOT originate semantics.

The exact Profile edition `0.1.0` requirement semantics are defined in this
specification. Its `profile_requirement_artifact` materializes the structured
requirement set, the binding specification defines representation, and the
corresponding JSON Schema validates structure. The artifact and schema do not independently
originate Profile semantics.

Binding support for a requirement kind does not require Profile edition `0.1.0`
to contain that kind.

## Assessment and composition boundaries

ADR-0030 establishes the separate assessment binding family
`https://geesno.com/binding/ai-context-assessment-json` version `0.1.0`.

The concrete assessment representation is defined separately by
[ai-context-assessment-json-binding.md](ai-context-assessment-json-binding.md).
Its structural schema and conformance material do not independently define
the Profile and Projection semantics established by this specification.

ADR-0031 accepts optional explicit composite Profile editions. Normative
composition cannot be represented by `ai-context-json/0.1.0`; it requires a
future accepted exact binding version. Composition is optional, and this specification defines no composition
members, merge, inheritance, override or precedence.
