# JSON lifecycle, scope and completeness analysis

**Scope:** Core 0.1 JSON lifecycle, scope, completeness and state/history representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

This design applies accepted ADR-0007 and accepted ADR-0009 through ADR-0014:

```text
STATE FIRST
HISTORY OPTIONAL
REPLAY NEVER REQUIRED
```

The JSON fragment below is illustrative and non-normative; it does not
represent a complete SemanticDocument fixture. Accepted ADR-0015 and
ADR-0016 establish the Core 0.1 JSON member and processing constraints.
The derived schema and conformance fixtures implement and test them.

## Accepted placement (conceptual)

```json
{
  "scope": {
    "completeness": "partial",
    "definition": {
      "kind": "scope:entity-selection",
      "value": "Selected entities from one engineering extraction"
    }
  },
  "revision": {
    "id": "urn:uuid:00000000-0000-4000-8000-000000000301",
    "parents": [
      {
        "target": "urn:uuid:00000000-0000-4000-8000-000000000300",
        "location": "out-of-document"
      }
    ]
  },
  "tombstones": [
    {
      "id": "urn:uuid:00000000-0000-4000-8000-000000000302",
      "target": {
        "target": "urn:uuid:00000000-0000-4000-8000-000000000099",
        "location": "out-of-document"
      },
      "target_category": "assertion",
      "reason": "lifecycle:withdrawn"
    }
  ],
  "history": {
    "completeness": "partial",
    "changes": [
      {
        "revision": {
          "target": "urn:uuid:00000000-0000-4000-8000-000000000301",
          "location": "in-document"
        },
        "targets": [
          {
            "target": "urn:uuid:00000000-0000-4000-8000-000000000202",
            "location": "in-document"
          }
        ],
        "kind": "lifecycle:locator-corrected",
        "details": "Corrected A10 to A11 for the same occurrence"
      }
    ]
  }
}
```

The fragment is conceptual and omits unrelated document fields and namespace
declarations. It shows that current Revision exists without complete history,
a Tombstone is current visible state, and a purely scoped descriptive Change
may remain anonymous.

## Current-state authority

The canonical current state remains in the accepted category collections:

```text
entities | sources | bindings | assertions | tombstones
```

That state is authoritative only as the SemanticDocument's representation of
its declared scope and its declared Revision when one is present. It is not a
claim of global truth, global completeness, latestness or trustworthiness.

`history` never overrides state. A consumer can discard it and still consume
the document. A locally decidable contradiction for the same scope/Revision is
an error; replaying Changes to choose another result is forbidden.

## Current Revision

`revision [0..1]` is an inline descriptor, not a reference into `history`.
Every represented Revision has a mandatory ADR-0009 ID and `parents [0..*]`.

- zero parents means none are represented, not necessarily a universal root;
- one parent expresses linear lineage;
- multiple parents express derivation only;
- self-parenting and a closed local cycle are invalid; and
- explicit out-of-document parents may remain externally unverifiable.

No merge, branch, commit, replay or total-order semantics follow. Timestamp,
sequence, author and message are never mandatory. Provenance or qualified
profile data can describe them when material.

When `revision` is absent, the document makes no Revision lineage/ordering
claim; its scoped state remains directly consumable.

## Scope and completeness

`scope` is required and has one canonical descriptor:

```text
completeness [1] = complete | partial | unknown
definition   [0..1] = ADR-0010 kind + ADR-0012 value
```

`definition` can describe an entire logical dataset, subset, filter,
projection, redacted view or partial acquisition without adding a universal
selection/query language. It is required for `complete` and optional for
`partial` or `unknown`.

- `complete` is a completeness claim over the declared scope, not over the
  semantic universe. It permits absence/non-membership reasoning only when the
  consumer sufficiently understands that applicable scope definition and the
  profile rules. An unknown qualified definition remains preservable, but a
  bare-core consumer derives no portable absence/nonexistence conclusion from
  it. It does not encode historical deletion.
- `partial` means applicable records may be omitted.
- `unknown` makes no completeness claim.

For `partial` and `unknown`, absence never implies nonexistence or deletion.
Filtering, redaction, projection, pagination and partial acquisition are scope
contexts/causes, not additional completeness values. Chunking can use an
applicable Profile-defined scope; transport/framing conventions remain
outside this Core 0.1 JSON lifecycle contract.

Even with `complete`, `omission != deletion`; portable removal or withdrawal
continues to require a Tombstone.

## Tombstone

One top-level `tombstones` collection exposes current withdrawals without
replay. Each Tombstone has:

```text
id              [1] its own ADR-0009 ID
target          [1] ADR-0009 reference to withdrawn semantic ID
target_category [1] core addressable-record category
reason          [0..1] qualified term
trust           [0..*] scoped nested records
extensions      [optional; ADR-0015]
```

Tombstone identity and target identity are distinct. The category keeps a
standalone withdrawal meaningful when the old body is unavailable. A
Tombstone is not an Entity kind.

A current live target and current Tombstone for the same ID/scope/Revision are
contradictory. The target ID cannot later identify an unrelated subject.
Restoration may use the same ID only as explicit continuity of the same subject.
Privacy erasure may omit historical bodies or even retained Tombstone metadata,
but it never authorizes ID reassignment.

## Supersession and validity

The sole canonical direction is carried by a replacement record:

```text
replacement --supersedes [0..*]--> prior record
```

No duplicate `superseded_by` form is canonical. Self-supersession and closed
local cycles are invalid. Multiple replacements of one prior record are
structurally valid and can be semantically conflicting. Supersession alone does
not mean invalidated, rejected, corrected, tombstoned, true or authoritative.

An optional validity descriptor contains a qualified `kind` and at least one
ADR-0012 `from`/`until` boundary. The qualified kind defines the semantic axis,
comparison and boundary convention; core does not assume UTC time. A locally
comparable end before start is invalid. Unknown comparison semantics are
preserved and evaluated by an applicable profile.

A record may be present in Revision R for traceability while not valid at the
applicable domain time. Membership and validity are never aliases.

## Change

The minimum Change roles are:

```text
id          [0..1; required for independent addressability]
revision    [1] affected Revision reference
targets     [1..*] affected record references
kind        [1] qualified term
details     [0..1] ADR-0012 value
trust       [0..*] scoped nested records
extensions  [optional; ADR-0015]
```

Multiple targets group a description but imply no atomicity or transaction.
`details` is inert information, not JSON Patch, a command, reducer input or
replacement state.

A Change is valid without an ID only while it is a scoped description. It needs
an ADR-0009 ID when cited, referenced, reviewed, identity-ordered, deduplicated,
corrected, superseded, tombstoned or otherwise managed as an independent
lifecycle target.
A later-minted ID cannot prove continuity with an earlier anonymous Change; a
producer needing continuity must identify it from first serialization.

Changes occur only inside `history`. A Change outside that envelope is a second
dialect and invalid. Not every difference needs a Change.

## Optional history

The one optional envelope is:

```text
history
├── completeness [1] complete | partial | unknown
├── definition   [0..1]; required for complete
├── revisions    [0..*] previous identified Revision descriptors
├── changes      [0..*] optional descriptive Changes
└── records      [0..*] `revision + target` membership descriptors
```

Current-state completeness and history completeness are independent. History
can be absent, partial, lineage-only or Change-only. Missing history never
weakens a valid current state or proves earlier records nonexistent.

`history.completeness` describes coverage of the declared history scope. It
does not imply that complete historical record bodies or complete prior
SemanticDocument snapshots are embedded in `history`, and it never turns
Changes into a replay log.

Each `records` entry associates one Revision reference with one record target
reference. It declares historical membership without duplicating the record
body, validity or replay behavior. Historical records with distinct IDs remain
in their one canonical collection; for example, old and replacement Assertions
can coexist and the old one can be referenced by `history.records`. Exact
earlier bodies for the same continuing ID are represented by separate
standalone SemanticDocuments for those Revisions, or only described
non-authoritatively by a Change. They are not duplicated in `history`, which
avoids duplicate primary IDs and a second embedded snapshot language.

## Identity continuity

Accepted ADR-0011 requires a new Assertion ID whenever its identity-defining
claim body changes. Correction normally creates a new Assertion that may
supersede the retained old claim.

Accepted ADR-0013 permits the same Binding ID across `A10` to `A11` only when
the specific correlation/occurrence continues. A different occurrence, new or
competing mapping, or changed Entity/Source anchor requires a new Binding ID.
Matching Entity, Source and locator values never derive Binding identity.

Source revision, fingerprint, location or label may evolve under the same
Source ID when the origin/reference context continues. Source revision remains
independent from semantic Revision.

## Trust-record addressability

Provenance, Confidence and Review remain nested only in the host they qualify.
A purely scoped record may remain anonymous. It requires an ADR-0009 ID when it
is independently cited/referenced, superseded/corrected, tombstoned, assigned
independent validity/lifecycle state or retained with portable historical
continuity.

A simple nested Review and a structurally nested Review-of-review need no ID by
existence alone. Each record independently targeted needs its own ID. A later
ID cannot retroactively prove continuity with an anonymous earlier occurrence;
producers must mint from the first serialization when continuity matters.

## Cross-document and validation boundary

Lifecycle references preserve ADR-0009 `in-document` versus `out-of-document`
expectation. Local targets resolve exactly once when declared in-document.
External targets need not be available and are never automatically
dereferenced. Existence, category or a remote cycle may be externally
unverifiable rather than locally invalid.

Structural failures include duplicate IDs, local self/cycles, known target
category mismatch, known unrelated reuse of a tombstoned ID, an understood
Change contradicting the same scope/Revision, and comparable validity end
before start. Competing claims, multiple parents/replacements and differing
Reviews can remain structurally valid semantic conflicts.

All content is untrusted inert data. Defensive processors bound recursion,
graph traversal, allocation, string length and diagnostics and never execute or
automatically dereference lifecycle content.

## Privacy boundary

History may be partial or absent and core imposes no retention law. Redacted
values must not be reconstructable through Change details, old locators,
Provenance, Extensions or diagnostics. A Tombstone need not expose the old
body or a sensitive reason. Completeness never overrides privacy policy.

## Normative authority and implementation boundary

Accepted [ADR-0014](../adr/0014-lifecycle-serialization.md) governs
scope/completeness, Revision, Tombstone, supersession, validity,
Change/history, identity continuity and conditional trust addressability.

Accepted ADR-0015 governs Extension placement and strictness; accepted
ADR-0016 governs exact Core 0.1 JSON serialization and processing rules.
The local JSON Schema, deterministic checker and conformance fixtures
implement and test these contracts; they do not independently originate
lifecycle semantics or establish objective truth.

Applicable Profiles may impose additional scope, history or Projection
requirements without changing the universal bare-Core contract.
