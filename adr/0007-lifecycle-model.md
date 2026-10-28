# ADR-0007: State-first, history-optional lifecycle

- **Status:** Accepted
- **Date:** 2026-08-30
- **Accepted by:** Explicit human architecture decision on 2026-08-30
- **Scope:** Abstract lifecycle semantics only; representation details remain open

## Context

GeesNO.Semantic must describe semantic evolution while preserving identity,
traceability and historical meaning. It must do so without becoming an event-
sourcing runtime, version-control system, merge engine, synchronization
protocol, workflow engine or transaction system.

A consumer should be able to exchange and understand semantic state without
implementing history replay. Producers that have trustworthy lifecycle history
must still be able to describe derivation, correction, removal, supersession
and non-linear lineage.

## Conceptual distinctions

- **SemanticDocument:** an exchangeable semantic dataset state and its declared
  scope.
- **Revision:** a referenceable semantic state/edition in document lineage.
- **Change:** an optional description of a transition or lifecycle effect; it
  does not execute the transition.
- **Entity lifecycle:** addition, semantic modification, tombstone, explicit
  restoration or supersession while semantic identity rules remain intact.
- **Assertion lifecycle:** addition, correction, rejection, invalidation,
  supersession or historical retention of a claim.
- **Binding lifecycle:** creation, locator correction, staleness, invalidation
  or supersession without changing Entity identity.
- **Supersession:** a directed replacement claim, distinct from automatic
  invalidation.
- **Tombstone:** an explicit withdrawal marker that preserves historical
  identity and forbids silent ID reuse.
- **Validity:** when/under which semantic conditions a claim is intended to
  apply, independent of the Revision in which its record appears.
- **Provenance:** how information or a lifecycle statement originated; it is not
  itself necessarily a Revision or Change.

A Review is not automatically a Change. New Provenance is not automatically a
Revision. Source revision and semantic Revision are independent.

## Requirements

Any lifecycle model must:

1. preserve semantic identity across ordinary evolution;
2. allow a SemanticDocument state to be consumed without history replay;
3. make history optional unless a declared profile requires it;
4. distinguish omission in partial data from explicit removal/tombstone;
5. permit Entity, Assertion, Binding and Concept–Representation association
   lifecycle to evolve independently;
6. preserve historical assertions/bindings when correction or supersession is
   represented;
7. separate Revision membership from semantic validity;
8. separate Source revision from SemanticDocument Revision;
9. express directed lineage, including multiple parents, without defining
   branch/merge algorithms;
10. keep lifecycle statements descriptive and untrusted;
11. avoid mandatory domain timestamps, sequences or workflows;
12. remain serialization-independent.

## Candidate invariant evaluation

| Candidate | Evidence | Counterexample / risk | Recommendation |
| --- | --- | --- | --- |
| 1. SemanticDocument is consumable without replay. | Every domain exchanges snapshots; AI/context consumers need bounded state. | A pure audit log cannot expose current state without replay. | Adopt: the contained state authoritatively represents only the document's declared scope for the declared Revision. |
| 2. History is optional unless profile-required. | Static, derived and privacy-filtered datasets often lack trustworthy history. | Audit/regulatory profiles may require it. | Adopt: core-valid current state may have no history; profiles can tighten. |
| 3. Missing in partial data is not deletion. | Filtering, pagination, redaction and AI projections omit valid entities. | A declared complete comparison may intentionally use absence. | Adopt: absence alone never deletes; explicit tombstone/change or profile completeness semantics is required. |
| 4. Tombstone is explicit. | All domains need to distinguish withdrawn from unseen. | Verbosity when complete snapshots already imply removal. | Adopt: universal core requires explicit semantics for portable deletion claims. |
| 5. Tombstone preserves identity. | Historical relations/reviews must still target the withdrawn subject. | Privacy erasure may require physical removal. | Adopt for represented history; legal erasure can omit data but must not reassign the ID. |
| 6. IDs are not reused after tombstone. | Reuse corrupts lineage and references in every domain. | Explicit restoration of the same semantic subject. | Adopt: restoration is continuation, not reuse for a different subject. |
| 7. Entity, Assertion and Binding evolve independently. | A locator can stale while meaning remains; a claim can be corrected without replacing its subject. | Highly coupled source exports may change them together. | Adopt: coupled Changes may group effects but do not merge identities/roles. |
| 8. Source and semantic Revision are independent. | Enrichment can change with fixed source; source formatting can change without semantic change. | One-to-one synchronized profiles. | Adopt in core; profiles may assert correspondence explicitly. |
| 9. Correction/supersession does not destroy history. | Legal, scientific and review use cases require prior claims. | Privacy/minimization or snapshot-only exchange may omit history. | Adopt when history is represented; history remains optional. |
| 10. Multiple-parent lineage is expressible without Git semantics. | Collaborative documents, scientific derivation, catalog federation and software branches need non-linear provenance. | Adds graph validation and may be mistaken for merge behavior. | Adopt `0..*` parent references; explicitly provide no merge/conflict algorithm. |
| 11. Latest Revision is not semantic truth. | Newer content can be inferred, rejected or untrusted; historical claims can remain valid. | Profiles may define current-authoritative policy. | Adopt in core; authority comes from profile/trust policy, not order alone. |
| 12. Lifecycle never substitutes for Provenance/Review. | “latest”, “accepted” or “superseded” can be asserted by an untrusted producer. | Redundant metadata burden. | Adopt: lifecycle state and trust remain orthogonal. |

## Alternative A — snapshot-oriented

Each Revision is a complete or declared-partial SemanticDocument state.

### Strengths

- standalone exchange and direct AI consumption;
- no replay or event ordering implementation;
- simple current-state validation and resilient archival copies;
- high interoperability for consumers that ignore history.

### Weaknesses and failures

- repeated data and expensive storage/transfer for frequent revisions;
- diffs and causality are not explicit;
- historical correction/supersession is hard to cite without retained prior
  snapshots;
- deletion is ambiguous in partial snapshots unless tombstones/completeness are
  explicit;
- collaborative/non-linear derivation needs additional lineage metadata.

It fails as the only model when fine-grained audit or correction lineage is a
material interoperability requirement.

## Alternative B — Change/Event-oriented

State is reconstructed from ordered Change/Event records.

### Strengths

- precise transition/audit descriptions;
- compact incremental transfer;
- direct targets for corrections, supersession and provenance;
- natural representation of independent lifecycle effects.

### Weaknesses and failures

- replay is required and missing/reordered records can prevent interpretation;
- causality, total/partial ordering, checkpoints and compatibility become
  runtime-like concerns;
- merge/branch semantics and idempotency add substantial complexity;
- poor standalone AI/context consumption;
- producers with snapshots but no trustworthy event history cannot conform.

It fails the universal interoperability boundary if event replay is necessary
to understand the document.

## Alternative C — state-first hybrid

Every exchanged SemanticDocument provides a usable declared state. Revision
lineage and Change records are optional descriptive history.

### Strengths

- preserves standalone state and optional fine-grained audit;
- allows producers/consumers to ignore history unless a profile requires it;
- supports partial history, checkpoints and non-linear lineage without replay;
- fits accepted addressable assertions and independent Binding lifecycle;
- AI consumers can use state while retaining material correction provenance.

### Weaknesses and consistency problem

- snapshot and Change records can contradict each other;
- producers may duplicate data and lifecycle information;
- implementations need reference/graph validation when history is present;
- partial snapshots and partial histories need explicit scope;
- it is too complex for use cases that need only current state and too weak for
  systems requiring executable event-sourcing guarantees.

### Mitigations

- the state contained in a SemanticDocument is the authoritative representation
  of its declared scope for the declared Revision;
- Change history is explanatory, not a second reconstruction source of truth;
- consumers are never required to replay Changes;
- when a Change claims an effect on the same declared state, it must be
  consistent where that consistency is locally decidable, or explicitly scoped
  to another/historical/partial state;
- profiles may require complete history or stricter consistency, while bare core
  does not;
- lifecycle records never execute or prescribe merge behavior.

## Cross-domain evidence

| Domain | Adversarial case | Result |
| --- | --- | --- |
| Engineering-like model | One Representation disappears from one Source while its Concept remains represented elsewhere. | Independent Representation tombstone/Binding lifecycle preserves Concept; snapshot omission alone is insufficient. |
| Spreadsheet/table | A row moves, then is deleted, while row index changes. | Semantic identity survives locator correction; explicit tombstone distinguishes deletion from filtered rows. |
| Technical/legal document | A clause is replaced; old text and rejected interpretation remain historically citable. | Addressable assertion correction/supersession and separate validity/review are required; current snapshot stays readable. |
| Software repository | Two branches produce independent semantics and a later state derives from both. | Revision parents `0..*` express lineage; no merge algorithm or conflict resolution is defined. |
| Scientific dataset | Original measurement remains, but a derived property is corrected after recalibration. | Assertion lifecycle changes independently; provenance and validity remain distinct from revision order. |
| Product/asset dataset | SKU/locator changes while the commercial Concept remains. | Binding is superseded/corrected without changing Concept identity; Source and semantic revisions need not align. |

The evidence supports a hybrid only when it is **state-first** and history does
not become a second authoritative state stream.

## Decision

Adopt Alternative C with these constraints:

1. A SemanticDocument is an exchangeable semantic state; history replay is
   never required for core consumption.
2. Lifecycle history is optional unless an applicable profile requires it.
3. The state contained in a SemanticDocument is the authoritative
   representation of its declared scope for the declared Revision. Change
   records describe history/effects and do not override that scoped state.
4. Every explicit Revision is referenceable and may declare `0..*` parent
   Revisions. Multiple parents express lineage only.
5. Sequence and timestamps are optional metadata, never semantic identity or a
   mandatory total order.
6. A Change must be independently addressable when it is cited, reviewed,
   ordered, deduplicated, corrected or superseded; exact identity syntax remains
   open. A Change is descriptive and optional; not every historical difference
   needs a Change record.
7. Missing content never implies deletion by itself. Tombstone/removal semantics
   are explicit or provided by an applicable completeness profile.
8. A tombstone preserves identity and prohibits silent reuse for another
   semantic subject. Explicit restoration of the same subject is allowed as
   lifecycle continuation.
9. Entity, Assertion, Binding and association assertions evolve independently.
10. Supersession is a directed lifecycle claim and does not automatically mean
    invalidation. It may have multiple replacements; exact encoding remains open.
11. Revision membership and semantic validity are independent. “Latest” does
    not imply true, accepted or currently valid.
12. Source revision and semantic Revision are independent unless an explicit
    relation/profile states otherwise.

No Timeline, Branch, Commit, Transaction, VersionGraph or HistoryManager
primitive is added. Revision, Change, Relation and Provenance cover the needed
abstract semantics.

## Conformance implications

A conforming core document may contain no history. When lifecycle records are
present, future formal constraints should treat these as structural errors:

- duplicate or malformed locally scoped Revision/Change references;
- self-parenting or cyclic Revision lineage in a declared closed graph;
- self-supersession or cyclic supersession in a declared closed graph;
- a lifecycle target that is neither resolvable nor explicitly external/
  unresolved under the applicable rules;
- reuse of a tombstoned identity for a different known subject;
- an internally comparable validity end before its start;
- a locally decidable Change/state contradiction without distinct scope.

These may remain semantically conflicting yet structurally valid:

- competing assertions;
- multiple Revision parents or parallel descendant states;
- several proposed replacements;
- different confidence/review conclusions;
- lifecycle claims from sources with different authority;
- a historical assertion that is present but no longer valid.

Exact external-reference and partial-graph validation belongs to later
specification/conformance work.

## Consequences

- Minimal consumers read current semantic state without event infrastructure.
- History-aware consumers gain referenceable lineage and corrections.
- Producers can exchange snapshots even when complete history is unavailable.
- History-capable producers bear graph/reference/consistency costs.
- Profiles may require history without making it universal core completeness.
- AI Context can distinguish omission from explicit tombstone while leaving
  chunking/continuation syntax to S4.
- Implementations receive no synchronization, merge, workflow or execution
  behavior from the standard.

## Remains open

- Revision and Change identifier syntax/scope;
- exact document/revision/history serialized placement;
- exact Change taxonomy and target/effect representation;
- assertion/Binding addressability encoding;
- completeness declarations and partial-history encoding;
- exact supersession encoding and effect vocabulary;
- validity-state vocabulary and interval encoding;
- timestamp datatypes and precision;
- out-of-document lifecycle-reference rules and separate processing-resolution
  diagnostics;
- consistency validation across partial snapshots/history;
- history retention, compaction/checkpoints and privacy erasure;
- cross-document lineage;
- exact lifecycle requirements in L0/L1/L2 or later profiles.

## Acceptance scope

The accepted decision resolves the central architectural choice: semantic state
is state-first and standalone for its declared scope and Revision, while
optional lifecycle history describes lineage and change without becoming a
replay/runtime model. It does not make undeclared or omitted content
authoritatively absent, and it does not resolve serialization, profile or
formal-conformance details.
