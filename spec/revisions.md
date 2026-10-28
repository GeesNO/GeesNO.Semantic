# Revision, Change and lifecycle

**Scope:** Universal Revision, Change and lifecycle semantics, with Core 0.1 JSON serialization boundaries.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

This document describes the abstract lifecycle semantics accepted in
[ADR-0007](../adr/0007-lifecycle-model.md). Core 0.1 JSON placement and
identifier encoding are specified separately by accepted ADRs and the Core
JSON schema. Qualified Vocabulary/Profile completeness and retention
policies remain distinct from the universal lifecycle model.

## Boundary

Lifecycle describes semantic state and history. It is not event sourcing,
version control, synchronization, merge, replication, workflow, transaction or
execution behavior.

## Distinct concepts

| Concept | Responsibility | Not equivalent to |
| --- | --- | --- |
| SemanticDocument | Exchangeable semantic state with declared scope. | Complete historical log. |
| Revision | Referenceable semantic state/edition and optional lineage node. | Source revision, transaction or commit. |
| Change | Optional description of a transition/effect. | Command that applies a mutation. |
| Entity lifecycle | State of an identified Concept/Representation across semantic evolution. | Assertion or Binding lifecycle. |
| Assertion lifecycle | State/validity/correction/supersession of an individual claim. | Entity identity change. |
| Binding lifecycle | Creation, correction, staleness, invalidation or supersession of source correlation. | Entity removal. |
| Supersession | Directed claim that another record replaces or succeeds a prior one. | Automatic invalidation or deletion. |
| Tombstone | Explicit semantic withdrawal preserving historical identity. | Absence from a partial dataset. |
| Validity | When/where a semantic claim is intended to apply. | Membership in a Revision. |
| Provenance | Origin, evidence and method of data/lifecycle statements. | Revision or Change by itself. |

New Provenance or Review does not necessarily create a Revision or Change; a
producer/profile determines revision boundaries. When a Change is declared, it
remains descriptive.

## Accepted state-first model

The accepted model is a constrained hybrid:

- SemanticDocument state is directly consumable without replay.
- History is optional unless a profile requires it.
- The state contained in a SemanticDocument is the authoritative representation
  of its declared scope for the declared Revision.
- Revision/Change history explains lineage and effects; it does not override or
  reconstruct the authoritative scoped state.
- Change records are descriptive and optional; not every historical difference
  needs a Change record, even when some history is represented.
- Explicit Revisions are referenceable and may have `0..*` parents.
- Multiple parents mean non-linear derivation only; no merge semantics follow.
- Changes need addressability when cited, reviewed, ordered, corrected,
  deduplicated or superseded; accepted ADR-0014 requires conditional ADR-0009
  identity and no retroactive continuity for a later-minted ID.

Snapshot-only fails for fine-grained audit. Event-only fails standalone
interchange. Hybrid fails if Changes become a competing source of current
state; the state-first rule is therefore an accepted constraint.

## Minimum cases

### Document

- Initial creation can have a Revision with no parent or omit history entirely.
- A derived Revision may reference one or multiple parents.
- A partial snapshot declares scope/completeness sufficiently for its profile;
  absent content alone has no deletion meaning.
- A replaced dataset may retain lineage while presenting a standalone new state.

### Entity

- Addition/modification can preserve or introduce stable identity as appropriate.
- “Unchanged” need not generate a Change.
- Removal/tombstone is explicit and preserves historical identity.
- Restoration is allowed only as explicit continuation of the same subject, not
  ID reuse for another subject.
- Representation removal does not delete associated Concepts.
- Concept survives replacement of every Representation.

### Assertion and association assertion

- New, corrected, rejected, invalidated, conflicting, superseded and historical
  claims can coexist.
- Correction normally creates a new claim and directed supersession/history,
  rather than erasing the prior claim.
- Accepted ADR-0011 gives every serialized Assertion an ID whether or not it is
  already targeted. Purely scoped nested trust metadata may remain anonymous.
- Concept–Representation associations use these same semantics under ADR-0008.

### Binding

- Creation, locator correction, staleness, invalidation,
  Source-context change and supersession do not change Entity identity.
- Processor lookup `resolved` / `unresolved` remains a processing observation,
  not Binding lifecycle state.
- A stale/lost locator is not Entity removal.
- Corrected Bindings can retain the old Binding historically when history is
  represented.
- Accepted ADR-0013 permits one Binding ID across locator correction/relocation
  only for the same specific correlation/occurrence; a different occurrence or
  competing correlation requires a new ID even when the body matches.

## Validity versus Revision membership

An assertion may be present in a historical or current Revision while its
semantic validity differs:

- `valid from`: start of intended applicability;
- `valid until`: end of intended applicability;
- `invalidated`: explicitly no longer intended to apply;
- `superseded by`: directed replacement claim;
- `historical`: retained for traceability, not necessarily currently valid.

These are conceptual roles, not final fields or state vocabulary. Latest
Revision does not mean every included assertion is true/current; it can include
history, rejected interpretations and low-confidence claims.

The roles are not aliases: `superseded` identifies a directed replacement;
`invalidated` explicitly ends intended applicability; `rejected` records a
review disposition; `corrected` relates a claim to a correction; and
`historical` retains material for traceability. Declaring one does not silently
declare any of the others.

## Supersession

Supersession applies independently to Entities, Assertions, Bindings and Source
descriptions. Accepted ADR-0014 serializes it from replacement to prior and
permits more than one replacement (for example, a split). It does not
automatically invalidate the prior subject: validity effect must be explicit or
profile-defined.

Supersession needs a referenceable target. Accepted ADR-0014 uses one
replacement-to-prior `supersedes` form and rejects a parallel canonical reverse
copy. A closed local supersession graph should be acyclic; cycles are
structurally incoherent.

## Tombstone and partial data

A tombstone explicitly states semantic withdrawal while retaining the stable ID
for historical reference. It is not an Entity kind and never authorizes silent
ID reuse. A privacy erasure may omit retained history when policy or law
requires it, but omission never authorizes reassignment of the erased ID to a
different semantic subject.

```text
Entity absent from partial/filter/redacted/page/chunk/projection
    !=
Entity explicitly tombstoned
```

An understood `complete` scope can support scoped absence/non-membership
inference, but omission still does not mean portable deletion. An unknown
qualified scope definition is preserved without giving a bare-core consumer
that inference. Deletion/withdrawal requires a Tombstone. Projection
omission, boundedness and continuation semantics follow accepted ADR-0026;
partial, paged or bounded delivery does not imply portable deletion.

## Lineage, branch and merge

Parent cardinality `0..*` is sufficient to express non-linear lineage seen in
collaborative documents, scientific derivations, catalog federation, model
federation and software branches. Core does not define branch names, merge
commits, conflict-resolution algorithms, working trees or total ordering.

A parent graph expresses derivation. A declared closed local graph is acyclic.
External or unresolved parents follow the reference-location and resolution
boundaries of ADR-0009 and ADR-0016; reference alone does not guarantee
availability or require dereference.

## Temporal semantics

The universal core needs to keep two concerns distinct when present:

- **Revision/recorded time:** when a semantic state/history record was created
  or recorded;
- **valid time:** when a semantic assertion is intended to apply.

Event, authored and observed timestamps can be material, but belong to scoped
Provenance or vocabulary/profile semantics rather than being mandatory on every
Revision/Change. When expressed using Core 0.1 JSON temporal datatypes,
representation follows accepted ADR-0012 and ADR-0016; additional temporal
interpretations remain Vocabulary/Profile concerns.

## Source versus semantic Revision

Source revision and SemanticDocument Revision are independent:

- semantic enrichment can revise meaning against the same Source revision;
- a new Source revision can leave semantic meaning unchanged;
- one semantic Revision can combine several Sources at different revisions.

No synchronization, equality or automatic revision increment is inferred.

## Conformance boundary

A core-conforming document may have no history. When lifecycle content is
present, it is constrained: targets must be interpretable under the applicable
in-document/out-of-document reference-location rules; scope must be explicit; Revision parents must
form coherent lineage; reference integrity must be preserved; and Changes must
not silently contradict the authoritative state for the same declared scope and
Revision. Structural rules can additionally require acyclic closed lineage/
supersession graphs, explicit tombstones, coherent comparable validity intervals
and no known ID reassignment.

Competing claims, multiple parents, several replacements and different review/
authority conclusions can be semantically contentious while syntactically
valid. Lifecycle metadata remains untrusted and does not replace Provenance,
Confidence or Review.

Core 0.1 JSON member names and lifecycle serialization follow the accepted
schema and ADR-0014/ADR-0016. Qualified lifecycle Vocabularies, Profile
retention/L0/L1/L2 rules and cross-document packaging remain separate
concerns, not unresolved bare-Core schema decisions.

Accepted [ADR-0014](../adr/0014-lifecycle-serialization.md) defines Core 0.1
JSON placement, conditional Change/trust addressability, explicit Tombstones,
directed supersession, qualified validity and optional non-replay history.
Concrete structure follows the Core 0.1 JSON schema; additional
Vocabulary/Profile policies remain separate.
