# Conformance

**Scope:** Bare-Core conformance for Core JSON `spec_version` `0.1.0` (Layers 0–3).

**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## Closed requirements

- Conformance is deterministic and does not require an LLM, cloud service or
  official SDK.
- A claim identifies the exact specification and applicable profile version.
- Syntactic validity does not establish semantic truth.
- Unknown Extensions do not invalidate core content unless a declared profile
  requires them.
- There is no certification program for pre-1.0 Public Preview
  `0.1.0-preview.1`.

Accepted abstract-Core decisions additionally require that:

- specialized assertions share the ADR-0005 common abstract contract;
- each Binding correlates exactly one Entity and one Source, remains optional/
  plural and uses Source-scoped qualified locator semantics under ADR-0006;
- Concept–Representation association is `0..*` in both directions and each
  association is an independent assertion under ADR-0008;
- lifecycle is state-first and history-optional under ADR-0007: the state
  contained in a SemanticDocument is the authoritative representation of its
  declared scope for the declared Revision, and Change replay is never required.

Accepted ADR-0009 additionally requires one absolute IRI-capable semantic-ID
space, mandatory serialized SemanticDocument identity, canonical lowercase
UUID URNs when UUID is used, exact canonical-string equality and document-wide
uniqueness across every addressable record category. Addressability remains
per-primitive rather than universal.

Accepted ADR-0010 additionally requires one compact `prefix:local` form in
qualified-term slots, declaration of every used prefix, deterministic expansion
to the absolute semantic term IRI, no same-base aliases inside a document and no
registry/dereference dependency. Expansion base, optional vocabulary identity
and optional vocabulary version remain distinct; only the expanded term IRI
controls term equality.

Accepted ADR-0012 additionally requires one canonical representation per value
datatype: native JSON only for string and boolean, tagged forms for integer,
decimal, date, date-time, reference, quantity, list, set and structured values,
and an explicit condition object for unknown, not applicable or redacted. Raw
JSON numbers, arrays, arbitrary objects and `null` are not alternate core value
forms. Integer/decimal semantics are arbitrary-precision and exact; canonical
quantities always materialize a qualified unit. Descriptive source/display
lexical metadata does not affect equality or datatype and must never reveal a
redacted value.

Accepted ADR-0011 additionally fixes one top-level `assertions` collection,
mandatory ADR-0009 identity for every serialized assertion, specialized claim
bodies, a dedicated Concept–Representation category and stable claim identity.
Provenance, Confidence and Review remain nested only in their host; ADR-0011
does not require every trust occurrence to have an ID.

## Accepted ADR-0011 assertion checks

These accepted architectural requirements are expressed by the Core 0.1 JSON schema and
Layer 3 checker:

- every serialized assertion has one globally unique ADR-0009 ID and appears
  only in the top-level `assertions` collection;
- every Type, Property and Relation has exactly one Entity subject; every
  Concept–Representation association has a Representation subject and Concept
  target;
- Property Assertions contain exactly one of accepted ADR-0012 `value` or
  `condition`;
- duplicate assertion IDs, an `in-document` subject that does not resolve
  exactly once, malformed qualified terms and missing category claim bodies are
  structural errors;
- inline Entity assertions, endpoint-duplicated Relations, anonymous assertions
  and singular `concept_id` association shortcuts are structural errors;
- two different IDs with identical claim bodies are not a structural error and
  are not automatically deduplicated; and
- every serialized Provenance, Confidence or Review record remains only in the
  host whose scope it qualifies; an ID is optional for purely scoped metadata
  and required when applicable accepted independent targeting/lifecycle rules apply.

Changing an assertion's identity-defining claim body while retaining its ID is
an identity-continuity error. Accepted ADR-0014 defines the
correction/supersession representation.

## Accepted ADR-0013 Source/Binding constraints

ADR-0013 is Accepted architecture. These constraints are covered by formal Core 0.1 JSON
schema/conformance fixtures:

- every Source and Binding has one ADR-0009 ID in the document-wide space;
- an ID-only Source and a Binding without locator are valid;
- every Binding has exactly one Entity reference and one Source reference;
- a locator, when present, has one declared ADR-0010 qualified `kind` and one
  ADR-0012 `value` rather than raw arbitrary JSON;
- multiple Source locations and multiple same-Entity/Source Bindings are valid;
- the same Binding ID twice is invalid, while different IDs with equal
  Entity/Source/locator bodies remain structurally valid because identity is
  continuity of one specific correlation, not tuple equality; and
- Source location/Binding locator data remains inert and never grants
  dereference, execution or permission semantics.

Accepted ADR-0014 encodes locator correction/staleness and exact
trust-addressability triggers without changing Binding correlation identity.

## Accepted ADR-0014 lifecycle constraints

These accepted architectural constraints are expressed by the Core 0.1 JSON schema and
Layer 3 checker where locally decidable:

- every document has scope with `complete`, `partial` or `unknown`;
- `complete` requires an explicit qualified scope definition and permits
  portable absence/non-membership inference only when the applicable scope and
  profile rules are understood; it never turns omission into deletion;
- every represented Revision and Tombstone has an ADR-0009 ID;
- current Revision is usable without history and has `0..*` lineage-only
  parents;
- local Revision/supersession self-edges and closed cycles are invalid;
- Tombstone identity is distinct from the preserved target identity/category;
- Change occurs only in optional history, is never replayed and needs an ID
  only when independently addressable/lifecycle-managed;
- current-state and history completeness remain independent;
- `history.completeness` covers the declared history scope but does not promise
  embedded complete prior bodies/snapshots or make Changes replayable;
- exact previous same-ID state uses a separate SemanticDocument for that
  Revision;
- assertion and Binding identity continuity follow accepted ADR-0011/0013; and
- a scoped anonymous trust record needs an ID from first serialization only
  when portable independent lifecycle/addressability is required.

## Accepted ADR-0015 strictness constraints

ADR-0015 is Accepted. Its architectural checks are implemented across Layers
0–3:

- every core object is closed under the exactly supported `spec_version`;
- an unknown member outside an explicit `extensions` boundary is invalid;
- `extensions` occurs only on the proposed semantic-record host matrix and each
  key is an ADR-0010 qualified term;
- an unknown Extension with valid host/key/JSON payload remains bare-core valid
  unless an applicable profile requires understanding;
- arbitrary JSON inside an Extension remains opaque/inert and does not become
  an ADR-0012 core value or supply a missing core member;
- a lossless round-trip claim requires preservation of unknown Extension key
  identity and payload semantics, while a permitted lossy projection explicitly
  reports omission; and
- missing/malformed `spec_version` is invalid, whereas a well-formed but
  unsupported version produces an unsupported-version result and never selects
  another version's schema.

Accepted ADR-0016 supplies the raw parser, exact Extension numeric-token,
validation-layer, lexical, member/token and omission decisions implemented by
the approved Core 0.1 JSON baseline.

## Bare-Core processing layers

The bare-core conformance result is the composition of four deterministic
layers:

1. **Layer 0 — raw input:** size/resource policy, BOM-free UTF-8, Unicode scalar
   validity, strict JSON grammar, one object root and duplicate decoded member
   rejection at every depth. JSON numeric tokens are retained exactly.
2. **Layer 1 — version dispatch:** `spec_version` must be canonical SemVer and
   exact supported contract `0.1.0`; well-formed unsupported versions produce a
   distinct `unsupported-version` result.
3. **Layer 2 — schema:** the local Draft 2020-12 schema validates the closed
   structural contract without network access.
4. **Layer 3 — semantic/integrity:** document-wide identity/reference/category
   checks, namespace expansion, exact confidence range, recursive set
   uniqueness, Gregorian calendar validity, comparable intervals,
   revision/supersession graphs, tombstone/live-state contradictions and
   conditional trust/Change addressability.

Profile-specific conformance is assessed separately from bare-Core Layers 0–3.
A bare-core-valid document that declares a Profile has not thereby proved
Profile conformance. For AI Context, the applicable contracts are the
[Profile](ai-context-profile.md) and
[assessment binding](ai-context-assessment-json-binding.md).
Resource refusal is distinct from semantic invalidity, and human-readable
diagnostic wording does not independently define conformance semantics.

## Conceptual Core coherence criteria

The abstract model is coherent only if:

- SemanticDocument and every Entity occurrence have semantic identity;
- Entity kind is Concept or Representation;
- native identity/locator never substitutes for semantic identity;
- Type/Property/Relation claim bodies have their required subject and target or
  value semantics;
- measured quantities have explicit unit semantics or an applicable profile
  default;
- assertion trust/lifecycle metadata has unambiguous scope;
- incomplete enrichment remains valid;
- Extensions obey the closed boundaries.

These are abstract-model invariants, not semantics originated by JSON Schema.

## Lifecycle conformance analysis

Accepted ADR-0007/0014 permit a conforming document to have no lifecycle
history. History is a capability and can become required only by a declared
profile. The contained state remains consumable without Change replay, but its
authority is bounded by the SemanticDocument's declared scope and Revision.
Even an understood `complete` scope can support only scoped absence or
non-membership inference; omission is not portable deletion, which requires a
Tombstone.

If lifecycle records are present, they are constrained rather than advisory
free text: their scope and targets must be interpretable, reference integrity
and Revision-parent coherence must be checkable under the applicable graph
rules, and a Change cannot silently contradict the contained state for the same
declared scope and Revision. Structural errors remain distinct from semantically contentious but
syntactically valid data.

The initial bare-core checker does not infer the effect of an unknown qualified
`Change.kind`. Consequently, a Change/current-state contradiction is not
locally decidable without an applicable future vocabulary/profile contract and
is not overclaimed as a generic Layer 3 failure.

Accepted structural/integrity errors covered where locally decidable include:

- duplicate/malformed locally scoped Revision or Change references;
- self-parenting or cyclic Revision lineage in a declared closed graph;
- self-supersession or cyclic supersession in a declared closed graph;
- `in-document` targets that fail applicable closed-graph integrity, without
  confusing that location expectation with processing resolution state;
- known reassignment of a tombstoned ID to a different semantic subject;
- an internally comparable validity end before its start;
- a locally decidable Change/state contradiction without distinct scope;
- treating absence from partial data as an implicit tombstone without declared
  completeness semantics.

Semantically conflicting but potentially structurally valid:

- competing Type/Property/Relation/association assertions;
- multiple Revision parents or parallel descendants;
- several proposed superseding records;
- different Confidence or Review conclusions;
- lifecycle records from actors/sources of different authority;
- historical assertions retained after validity ended.

The Core 0.1 JSON shape and bare-core validation of out-of-document references and
open/partial graphs are fixed by ADR-0009/0014/0016. Remote facts and
profile-specific consistency across partial snapshots remain externally
unverifiable or later profile work. `resolved` / `unresolved` is processing
state, not target-location expectation or identity. Lifecycle markers such as latest,
reviewed, accepted, rejected, corrected, superseded, current and historical are
untrusted data; they do not replace Provenance, Review or authority policy and
do not establish objective truth. Confidence likewise neither establishes
lifecycle state nor substitutes for it.

## Conformance boundaries

Progressive conformance levels, if defined in a future accepted contract,
cannot replace universal semantic invariants. Geometry alone cannot establish
universal semantic completeness; Relations alone do not establish trusted
lifecycle; and Binding cannot be mandatory for every Concept.

History remains optional in bare-Core conformance unless an applicable exact
Profile imposes additional requirements. Bare-Core Layers 0–3 and exact Profile
assessment are distinct conformance scopes. Any future standardized diagnostic
wording, progressive claim levels or certification mechanism needs its own
explicit normative authority. A public preview does not confer certification.
