# ADR-0014: Lifecycle, scope and completeness JSON serialization

- **Status:** Accepted
- **Date:** 2026-08-31
- **Last substantial review:** 2026-09-03
- **Accepted by:** Explicit human architecture decision on 2026-09-03
- **Decision order:** After accepted ADR-0013; before ADR-0015,
  ADR-0016 and formal schema

## Context

Accepted ADR-0007 requires a concrete JSON representation for current state,
scope, completeness, Revision lineage, tombstones, supersession, validity and
optional Change history. That representation must preserve identity and
historical meaning without becoming an event-sourcing runtime, version-control
system, merge engine, transaction log or replay protocol.

Accepted ADR-0011 also leaves one exact lifecycle question for nested
Provenance, Confidence and Review records: when a scoped record may remain
anonymous and when stable addressability is mandatory. Accepted ADR-0013 fixes
Source identity and Binding identity before lifecycle serialization. In
particular, a Binding ID denotes continuity of one specific correlation record,
not a tuple derived from Entity, Source or locator values.

This ADR establishes one canonical lifecycle placement. It does not create the
formal schema, normative fixtures, a lifecycle vocabulary, retention law or AI
Context/chunking protocol.

## Accepted abstract constraints from ADR-0007

The decision preserves all of these accepted constraints:

```text
STATE FIRST
HISTORY OPTIONAL
REPLAY NEVER REQUIRED
```

1. A SemanticDocument's contained state is authoritative only as the
   document's representation of its declared scope and declared Revision when
   one is present. It is not universal truth, global completeness or proof that
   the Revision is latest.
2. History may explain lineage and effects but never overrides or reconstructs
   the current state.
3. Omission alone is never portable deletion semantics.
4. Explicit Revisions are referenceable and have `0..*` parents; multiple
   parents express lineage only.
5. Tombstones are explicit, preserve target identity and prohibit reuse for a
   different subject.
6. Revision membership, semantic validity, Source revision, Provenance,
   Confidence and Review remain distinct.
7. Supersession is directed and does not automatically imply invalidation,
   rejection, correction, truth or authority.
8. Entity, Assertion, Binding, association and Source-description lifecycle
   evolve independently.
9. No mandatory timestamp, sequence, author, message or total order is
   introduced.
10. Lifecycle data is descriptive and untrusted; it never executes.

The governing rule is:

> Current state is authoritative only for its declared scope and Revision.
> History may explain state, but state never requires replay. Omission is not
> deletion. Identity continuity must not be confused with unchanged metadata.

For the accepted optional `revision context 0..1` case, omission of `revision`
means that no Revision identity or lineage is declared; it does not create an
implicit latest Revision.

## Dependencies

```text
ADR-0007 lifecycle semantics [Accepted]
    + ADR-0009 IDs/references [Accepted]
    + ADR-0010 qualified terms [Accepted]
    + ADR-0011 Assertions/trust scope [Accepted]
    + ADR-0012 canonical values [Accepted]
    + ADR-0013 Source/Binding identity [Accepted]
        -> ADR-0014 lifecycle/scope/completeness [Accepted]
            -> ADR-0015 [Accepted]
                -> ADR-0016 [Accepted]
                    -> formal schema and fixtures [Implemented candidate]
```

ADR-0014 serializes the accepted concepts without reopening their identity,
scope or execution boundaries. Accepted ADR-0015 owns unknown fields and
Extensions; accepted ADR-0016 owns parser/draft/canonicalization policy.

## Alternatives considered

### State and history placement

1. **Event/history reconstruction.** Compact for some producers, but consumers
   must replay an ordered log and incomplete history can make state unknowable.
   Rejected by accepted ADR-0007.
2. **Lifecycle only inside individual records.** Avoids a root envelope but
   leaves document lineage, history completeness and Change placement
   inconsistent. Rejected.
3. **Current category collections plus root scope/current Revision/Tombstones
   and one optional history envelope.** Keeps state standalone and history
   explanatory. Selected.

### Current Revision placement

1. **Reference to a Revision inside `history`.** Removes duplication but makes
   current Revision depend on optional history. Rejected.
2. **Inline identified current Revision descriptor.** Works with no history;
   previous Revisions use the same descriptor shape inside history. Selected.
3. **Unidentified inline metadata.** Cannot support lineage, citation or the
   ADR-0009 uniqueness/reference model. Rejected.

### Scope and completeness

1. **Boolean `partial`.** Cannot distinguish complete from unknown and invites
   global absence inference. Rejected.
2. **Rich enum containing `filtered`, `redacted` and `projection`.** Mixes a
   truth claim about completeness with causes/context. Rejected.
3. **Tri-state completeness plus one qualified scope definition.** Keeps the
   truth dimension small while profiles/vocabularies describe boundaries.
   Selected; `complete` requires an explicit definition.

### Tombstone identity

1. **Reuse the withdrawn target ID as the Tombstone ID.** Prevents historical
   target and withdrawal statement from coexisting in one uniqueness domain.
   Rejected.
2. **Independent Tombstone ID plus target reference/category.** Preserves both
   identities and supports review/provenance of the withdrawal. Selected.
3. **New tombstone Entity kind.** Violates the accepted two Entity kinds and
   conflates subject with lifecycle marker. Rejected.

### Change identity

1. **Mandatory ID for every Change.** Predictable, but imposes portable
   continuity on purely descriptive optional history.
2. **Conditional ID for independent addressability/lifecycle.** Matches the
   accepted ADR-0007 trigger while allowing anonymous scoped descriptions.
   Selected, with the explicit cost that a later ID cannot prove earlier
   anonymous continuity.
3. **No Change identity.** Cannot support citation, correction, review,
   supersession or deduplication when those are required. Rejected.

This Change choice is independently justified by Change's optional explanatory
role; it is not selected merely because trust records also have conditional
identity.

### Historical record bodies

1. **Duplicate prior record bodies inside `history`.** Creates a second
   polymorphic state store and repeats primary IDs in one document. Rejected.
2. **Retain distinct-ID historical records in canonical collections and use a
   separate standalone SemanticDocument for exact prior same-ID state.**
   Preserves one record placement, ID uniqueness and state-first consumption.
   Selected.
3. **Store only executable patches.** Requires replay and fails when history is
   partial. Rejected.

## Current-state representation

The canonical document separates current semantic state from optional history:

```text
SemanticDocument
├── id                       [1] accepted ADR-0009 document ID
├── scope                    [1]
├── revision                 [0..1] inline current Revision descriptor
├── entities                 [0..*] current/retained semantic records
├── sources                  [0..*] accepted ADR-0013 records
├── bindings                 [0..*] accepted ADR-0013 records
├── assertions               [0..*] accepted ADR-0011 records
├── tombstones               [0..*] withdrawals affecting current scope
└── history                  [0..1] descriptive history envelope
```

The collections are the state a consumer reads. `history` is not a second state
store, an ordered patch list or a prerequisite for understanding those
collections. If a locally decidable history statement contradicts the same
scope and Revision, current state remains authoritative and the contradiction
is a conformance error; replaying history is never the remedy.

Records retained for traceability stay in their one canonical category. For
example, an old Assertion with its own stable ID may remain in `assertions` and
be related to a replacement through supersession and validity. The `history`
object does not duplicate Entity, Source, Binding or Assertion collections.
Earlier complete states of the same stable record can be exchanged as separate
standalone SemanticDocuments for their own Revisions. This avoids duplicate
primary IDs and a second polymorphic snapshot dialect inside one document.

The top-level `revision` remains optional, preserving the accepted S1
`revision context 0..1` cardinality. When absent, the document makes no Revision
identity, lineage or ordering claim; its state is still directly consumable for
its declared scope. When present, it identifies the Revision of the current
state without depending on `history`.

## Revision model

Every serialized Revision descriptor has exactly one mandatory ADR-0009 ID in
the document-wide addressable ID space and `parents [0..*]` ADR-0009
references:

```text
Revision
├── id            [1]
├── parents       [0..*]
├── provenance    [0..*] scoped nested trust
├── confidence    [0..*] scoped nested trust
├── reviews       [0..*] scoped nested trust
└── extensions    [optional; ADR-0015]
```

The current Revision is an inline identified descriptor in `revision`, not a
reference that requires a matching object in `history`. `history.revisions`
contains only previous or otherwise historical Revision descriptors and must
not duplicate the current Revision ID.

- zero parent references means that no parent is represented; it does not by
  itself prove the Revision is the first state in all external history;
- one parent expresses linear derivation;
- multiple parents express non-linear lineage only, with no branch, merge,
  conflict-resolution or transaction semantics;
- array order does not create lineage order or priority;
- a parent may be explicitly out-of-document without being dereferenced.

A self-parent is invalid. A cycle is invalid when the complete cycle is
locally present in a declared closed graph. A possible cycle through an
out-of-document parent is externally unverifiable, not locally invalid merely
because the target is unavailable.

Timestamp, sequence, author and message are not required Revision members. If
material, origin/recording evidence belongs in scoped Provenance; domain
edition/order metadata belongs in qualified vocabulary/profile data or an
ADR-0015 Extension. None becomes Revision identity or a mandatory total order.

## Scope model

Every SemanticDocument has one `scope` descriptor. It bounds what the current
state purports to describe without introducing a query language:

```text
scope
├── completeness   [1] complete | partial | unknown
└── definition     [0..1]
    ├── kind       [1] ADR-0010 qualified term
    └── value      [1] ADR-0012 canonical value
```

The qualified definition can describe, under an applicable vocabulary or
profile, an entire logical dataset, an Entity set, a Source subset, a filtered
extraction, a projection, a redacted view or a partial acquisition. Structured
selections reuse ADR-0012 structured values. Core defines no path, filter,
query, continuation or chunk language.

`definition` is optional for `partial` and `unknown`, because explicitly
present records remain useful even when the producer cannot fully describe the
selection boundary. It is mandatory for `complete`; otherwise a portable
consumer cannot know the set over which absence is being claimed. A
structurally valid qualified definition may still be semantically unknown to a
consumer. In that case the completeness claim is preserved, but a bare-core
consumer must not derive portable absence or nonexistence conclusions from a
scope it cannot interpret. Such inference remains profile-dependent or
externally unverifiable rather than global.

> **`complete` is a completeness claim over the declared scope, not over the
> semantic universe.**

A consumer may derive absence/non-membership conclusions from `complete` only
when it sufficiently understands the applicable scope definition and profile
rules:

```text
complete + understood applicable scope
    -> scoped absence/non-membership inference may be permitted

complete + unknown/uninterpretable scope definition
    -> preserve completeness claim
    -> do not derive portable absence/nonexistence conclusions
```

An AI Context projection may later use a qualified definition, but ADR-0014
does not define selection, ranking, chunking or continuation for S4.

## Completeness model

The only universal completeness values are:

- `complete`: the producer claims no applicable current records are omitted
  from the explicitly declared and understood scope;
- `partial`: applicable records may be omitted; absence has no non-existence or
  deletion meaning; and
- `unknown`: no completeness claim is available; absence likewise has no
  non-existence or deletion meaning.

`filtered`, `redacted`, `projection`, `paginated`, `sampled` and
`partially_acquired` describe context or causes, not completeness truth values.
They belong in the qualified scope definition, Provenance, profile declarations
or Extensions as appropriate.

Even `complete` does not turn omission into a historical tombstone. It can
support an absence/non-membership conclusion only inside an understood
declared scope and applicable profile rules. Portable removal or withdrawal
across Revisions still uses an explicit Tombstone. No document claims
completeness for the semantic universe:

```text
omission != deletion
```

## Tombstones

Tombstones that affect the current declared state live in one top-level
`tombstones` collection and are readable without history replay:

```text
Tombstone
├── id                 [1] its own ADR-0009 ID
├── target             [1] ADR-0009 reference
├── target_category    [1] core addressable-record category
├── reason             [0..1] ADR-0010 qualified term
├── provenance         [0..*]
├── confidence         [0..*]
├── reviews            [0..*]
└── extensions         [optional; ADR-0015]
```

The Tombstone ID identifies the withdrawal record; `target` preserves the
withdrawn record's semantic ID. These IDs are distinct. `target_category`
allows a standalone consumer to distinguish an Entity, Assertion, Binding,
Source, Revision, Change or independently addressable trust record even when
the prior body is not retained. It is not a new Entity kind. The exact lexical
tokens remain subordinate schema naming, but the category role and cardinality
are fixed by this decision.

A current Tombstone and a live current record for the same target in the same
scope and Revision are contradictory. The target ID remains reserved across
the represented lineage and cannot denote an unrelated future subject.
Restoration is allowed only as continuity of the same subject: a later current
state may contain the live record with the same target ID and omit a current
Tombstone, while optional history describes the restoration. It is not ID
reassignment.

Tombstones apply uniformly to Entity, Assertion, Binding and any other
addressable record. They do not delete Concepts merely because a
Representation or Binding is withdrawn.

## Supersession

One canonical directed member, conceptually `supersedes [0..*]`, is carried by
the replacement addressable record and points to prior records:

```text
replacement --supersedes--> prior
```

There is no parallel canonical `superseded_by` copy. A record may supersede
several prior records, and several replacement records may independently
supersede the same prior record. The latter is structurally valid and can be a
semantic conflict; core does not pick a winner.

Supersession alone does not invalidate, reject, correct, tombstone or make the
replacement true. Those meanings remain separate:

- invalidation is an explicit qualified lifecycle/validity statement;
- rejection is a scoped Review disposition;
- correction is a qualified Change/relation semantics;
- tombstoning uses the explicit Tombstone record; and
- historical retention is record presence plus declared lifecycle context.

Self-supersession is invalid. A supersession cycle is invalid when the cycle is
fully present in a declared closed local graph because directed replacement
cannot coherently return to itself. Potential cycles through explicit
out-of-document references are externally unverifiable.

## Validity

Revision membership answers where a record is represented. Validity answers
when or under which qualified semantic axis it is intended to apply. A record
may therefore be present in the current Revision for traceability while not
being valid at a profile-defined current domain time.

The minimal optional validity descriptor is:

```text
validity
├── kind         [1] ADR-0010 qualified validity-axis term
├── from         [0..1] ADR-0012 canonical value
└── until        [0..1] ADR-0012 canonical value
```

At least one boundary is present. The qualified `kind` defines the axis,
comparison and boundary convention; core does not assume every value is a UTC
instant or introduce a temporal engine. If both values are locally comparable
under the known kind and `until` precedes `from`, the descriptor is invalid. If
the kind or comparison semantics are unknown, the descriptor is preserved and
semantic evaluation is profile-dependent.

No timestamp is mandatory. Provenance time, Source revision, Revision
membership and semantic validity remain distinct. Non-interval validity states
such as invalidated or jurisdiction-specific applicability use qualified
lifecycle/profile semantics rather than expanding a universal core enum.

## Change model

A Change is an optional description inside `history`, never a command or a
required state transition:

```text
Change
├── id             [0..1; conditionally required]
├── revision       [1] ADR-0009 reference to the affected Revision
├── targets        [1..*] ADR-0009 references
├── kind           [1] ADR-0010 qualified term
├── details        [0..1] ADR-0012 canonical value
├── provenance     [0..*]
├── confidence     [0..*]
├── reviews        [0..*]
└── extensions     [optional; ADR-0015]
```

`targets` may group related descriptive effects but creates no atomicity,
transaction or processing order. `details` is inert descriptive data; it is
not JSON Patch, a reducer input, replacement state or an executable payload.
Current state remains consumable if every Change is ignored.

Change identity is conditional rather than universally mandatory. An anonymous
Change is valid while it is only a scoped historical description. It requires
an ADR-0009 ID when it is cited, referenced, reviewed, ordered, deduplicated,
corrected, superseded, tombstoned or otherwise lifecycle-managed as an
independent target. Array position and JSON Pointer are never identity.
Consequently a Change carrying a Review cannot remain anonymous, even though an
unreviewed descriptive Change may do so.

This conclusion is not adopted merely for uniformity with trust metadata.
Assertions require IDs because their claim records are independently stable;
Tombstones require IDs because they are explicit addressable withdrawal
records. A descriptive Change need not have portable continuity. If a producer
later mints an ID for a formerly anonymous Change, core treats it as a newly
addressable record and cannot prove continuity with the anonymous occurrence.
If continuity may matter, the producer must assign the ID from its first
serialization.

A Change belongs only in `history`. A top-level or record-inline Change would
create a second canonical placement and is invalid. A locally understood Change
that claims an effect contradictory to the same declared scope and Revision is
invalid; an apparent contradiction across different or partial scopes may
remain a semantic conflict. In every case state wins and replay is forbidden.

## History model

`history` is one optional canonical envelope:

```text
history
├── completeness   [1] complete | partial | unknown
├── definition     [0..1] qualified kind + ADR-0012 value
├── revisions      [0..*] previous Revision descriptors
├── changes        [0..*] descriptive Change records
└── records        [0..*] historical membership descriptors
```

History absence is valid. When present, it may contain lineage without Changes,
Changes without a complete lineage, historical membership references, or any
combination. `history.revisions` uses the same identified Revision shape as the
current Revision. A current Revision need not appear in history and cannot be
duplicated there.

Each optional historical membership descriptor has exactly a `revision`
reference and a `target` record reference. It states only that the identified
record is represented in that historical Revision; it does not duplicate a
body, define validity or provide replay instructions. An in-document target can
point to a distinct-ID historical record retained in its canonical collection.
An out-of-document target can point to a record in a separately exchanged prior
Revision without requiring dereference.

Historical records with distinct stable IDs remain in their accepted canonical
collections when retained: for example, an old Assertion and its replacing
Assertion can coexist in `assertions`. An exact earlier body for a record whose
same ID continues, such as a corrected Binding locator or evolved Source
metadata, is carried by a separately exchangeable SemanticDocument for that
earlier Revision or described non-authoritatively by a Change. It is not copied
as a second primary record in `history`. This preserves document-wide ID
uniqueness and prevents history from becoming replacement state.

History completeness is bounded by its own qualified `definition`; `complete`
requires that definition.

> **`history.completeness` describes coverage of the declared history scope.
> It does not imply that complete historical record bodies or complete prior
> SemanticDocument snapshots are embedded in `history`.**

The exact previous state of a continuing stable record ID therefore remains a
separate SemanticDocument for that Revision. Same-ID historical bodies are not
duplicated inside `history`. A complete history claim never makes Changes a
replay log or makes history more authoritative than current state.

## Partial history

Current-state completeness and history completeness are independent:

| Current scope | History | Meaning |
| --- | --- | --- |
| `complete` | absent | Complete claim only for understood current scope; no historical claim. |
| `partial` | `complete` | Current records may be omitted even if the defined history subset is complete. |
| `complete` | `partial` | Current scoped state is complete; earlier lineage/effects may be omitted. |
| `unknown` | `unknown` | Present records are assertions; neither absence nor historical coverage is claimed. |

Partial history is valid and does not make current state incomplete. Missing
parents, Changes or earlier record states are not inferred to be nonexistent.
An out-of-document reference can state known lineage without promising that the
target is available.

## Assertion evolution

Accepted ADR-0011 fixes Assertion claim-body identity. Changing category,
subject or category-specific claim content creates a new Assertion ID. The same
ID cannot silently change from one value, relation endpoint, type or
Concept–Representation association to another.

A correction therefore normally retains the old Assertion when history is
represented, creates a new identified Assertion, and lets the new record
directedly supersede the old. Qualified Change, Provenance and Review data may
explain correction or rejection. Supersession does not itself invalidate the
old claim, and equal claim bodies under different IDs are not deduplicated.

The same Assertion ID may continue while only its non-claim envelope evolves,
such as additional scoped Provenance, Confidence, Review or validity metadata.

## Binding evolution

Accepted ADR-0013 controls Binding continuity:

- correcting `sheet:A10` to `sheet:A11` may keep the Binding ID only when both
  locators concern the same specific occurrence/correlation;
- native relocation may keep the ID under the same explicit continuity;
- a different occurrence, new independent mapping or competing correlation
  requires a different Binding ID even if Entity, Source and locator match;
- changing the Entity or Source anchor requires a new Binding ID; and
- Source revision or fingerprint change never mechanically decides Binding
  identity.

When continuity holds, the current Binding carries the current locator and an
optional Change or earlier SemanticDocument describes the prior locator. When
continuity does not hold, a new Binding such as `B2` may supersede old `B1`.
Neither Change nor history replay is required to understand the current
Binding collection. Locator loss or processor lookup failure is not Entity
removal.

## Source evolution

A Source ID identifies continuity of one origin/reference context, not an
immutable location, revision, fingerprint, label or metadata bundle. Those
descriptors may change across semantic Revisions while the Source ID continues.
A genuinely different origin context receives a new Source ID.

Source revision remains external descriptive metadata and is independent from
SemanticDocument Revision. A changed Source revision or digest neither proves
tampering nor forces a semantic Revision, Source replacement or Binding
replacement. Optional Change/Provenance may describe the observation without
becoming identity or truth.

## Trust-record lifecycle/addressability

The accepted nested-only placement remains unchanged. Provenance, Confidence
and Review records stay inside the exact host they qualify; there is no global
trust collection.

A nested trust record may omit an ID only while structural nesting provides its
complete scope and no portable independent target is needed. It requires an
ADR-0009 ID from the first serialization in which it:

- is cited or referenced independently;
- is the target or source of supersession/correction;
- is tombstoned or assigned independent validity/lifecycle state;
- must retain identity across historical representations; or
- otherwise participates as an addressable semantic record.

A simple nested Review may remain anonymous. A Review-of-review is valid by
nesting and does not automatically force IDs. If either Review must be cited,
superseded or historically tracked independently, that specific record needs an
ID. Reviewed Confidence or Provenance behaves the same way.

| Trust case | Identity outcome |
| --- | --- |
| Simple scoped Provenance | May remain anonymous; its host nesting supplies all scope. |
| Confidence with a nested Review | Both may remain anonymous when the Review structurally qualifies only that Confidence; an independently referenced Confidence or Review needs its own ID. |
| Review-of-review | Valid by recursive nesting; no ID is forced unless portable independent targeting is used. |
| Superseded Review | The prior and replacement Reviews require IDs because the directed edge targets stable records. |
| Historical Provenance requiring continuity | Requires an ID from first serialization in which portable continuity matters. |

An anonymous trust record may receive a newly minted ID in a later Revision,
but core cannot claim that the new addressable record is the same occurrence as
an earlier anonymous value. This is not an identity error if no continuity is
claimed; it is insufficient when portable historical continuity is required.
Producers that anticipate correction, review-of-review by reference,
supersession or historical retention must mint the ID at first serialization.

This resolves the ADR-0011 trigger without requiring universal trust IDs and
without using JSON Pointer or array position as a target.

## Cross-document behavior

Revision parents, supersession targets, Tombstone targets, Change targets and
validity reference values use ADR-0009 reference semantics:

- `in-document` targets must resolve exactly once under applicable scope rules;
- `out-of-document` targets need not be materialized or available;
- absence of an out-of-document target is not nonexistence;
- no reference triggers network or filesystem access; and
- processor `resolved`/`unresolved` observations are not serialized lifecycle
  truth.

Closed-graph acyclicity and consistency are checked only over the graph the
document declares closed and locally provides. An external parent or
supersession target is structurally valid but its existence, category,
continuity and participation in a remote cycle can be externally unverifiable.
A profile may require stronger closure without changing bare-core semantics.

## Privacy/redaction

Current state may use accepted ADR-0012 `redacted` conditions. History may be
partial or omitted for privacy, minimization or legal erasure; core defines no
universal retention mandate.

A Tombstone needs only its own ID, target ID, category and permitted metadata.
It must not reveal the withdrawn body or secret reason. When even retaining
that metadata is prohibited, the data may be physically omitted, but the
producer must never reassign the target ID to an unrelated subject.

Provenance, Change details, prior locators, Extensions, diagnostic output and
historical SemanticDocuments must not reconstruct or leak a redacted value.
Declaring `complete` does not override redaction policy or turn hidden content
into an inference target outside the explicit scope/profile contract.

## Security

All lifecycle content is untrusted inert data. IDs, references, qualified
terms, scope definitions, Change details, Source locations and locator values:

- never execute commands, queries, macros, patches, reducers or tool calls;
- never grant permission, authority or credentials;
- never trigger automatic dereference;
- never prove truth, acceptance, chronology or latest status; and
- remain subject to defensive size, depth, graph, string and processing limits.

Cycle detection and reference validation must be bounded. Unknown qualified
kinds are preserved according to later ADR-0015/0016 policy, not executed or
trusted.

## Cross-domain evidence

| Domain | Stress case | Result under the decision |
| --- | --- | --- |
| Engineering | A represented object moves and its native locator is corrected. | Same Binding ID is allowed only for the same occurrence; current locator is direct state and optional history is explanatory. |
| Spreadsheet/tabular | A filtered row extract omits records, a cell value is corrected and its occurrence moves from `A10` to `A11`. | `partial` blocks deletion inference; the value correction gets a new Assertion ID, while the Binding ID may continue only for the same occurrence. |
| Technical/legal document | A clause interpretation is replaced but the rejected prior claim remains citable. | New Assertion ID plus directed supersession and Review preserves both claims without declaring the replacement true. |
| Software repository | A semantic Revision has two parents and one unavailable external ancestor. | Multiple parents express lineage only; the external target is valid but externally unverifiable and no merge algorithm appears. |
| Scientific data | A measurement claim is recalibrated and is not domain-time-valid at the current Revision. | New claim identity, qualified validity and Provenance remain independent from Revision membership and Confidence. |
| Generic product/asset | A Source digest changes while origin context continues and a competing supplier mapping appears. | Source ID may continue; competing Binding receives its own ID even if the locator happens to match. |

No case requires CAD, Git, spreadsheet, legal, temporal-database, AI-provider or
product-specific core fields. Domain selection, validity axes, Change kinds and
locator semantics remain qualified.

## Adversarial cases

| Case | Classification and consequence |
| --- | --- |
| Partial document missing an Entity | **Valid.** Absence has no non-existence or deletion meaning. |
| Complete scoped document missing an Entity | **Valid scoped absence claim** only when the Entity is covered by an understood explicit definition; it still is not a historical tombstone. Otherwise inference is **profile-dependent/externally unverifiable**. |
| Missing record interpreted as deleted | **Invalid core inference** without an explicit Tombstone; completeness alone does not encode historical removal. |
| Explicit well-formed Tombstone | **Valid.** It is visible in current state without replay. |
| Tombstoned target ID reused for unrelated subject | **Invalid identity continuity.** |
| Explicit restoration of the same subject | **Valid lifecycle continuation** in a later state using the same target ID; it is not unrelated reuse. |
| Assertion claim body changed under the same ID | **Invalid identity continuity** under accepted ADR-0011. |
| New Assertion superseding old Assertion | **Valid.** Supersession is directed and does not automatically invalidate the old claim. |
| Binding locator corrected under the same ID | **Valid only for the same specific correlation/occurrence.** |
| Binding ID reused for a different occurrence | **Invalid identity continuity**, even with equal Entity/Source anchors. |
| New Binding superseding old Binding | **Valid.** Both IDs may be retained; no automatic Entity change follows. |
| Current Revision without history | **Valid.** The inline descriptor does not depend on `history`. |
| Revision with zero or multiple parents | **Valid.** Zero does not prove universal root; multiple means lineage only. |
| Revision self-parent or local closed cycle | **Invalid structural lineage.** A remote possible cycle is externally unverifiable. |
| Consumer must replay Changes to obtain state | **Invalid core processing model.** Current collections are sufficient. |
| Change contradicts same scope/Revision current state | **Invalid when locally decidable.** Across distinct/partial scopes it may be a semantic conflict; current state still wins. |
| Change outside `history` | **Invalid non-canonical placement.** History absence implies no serialized Change collection. |
| Partial history | **Valid.** It does not alter current-state completeness. |
| Self-supersession | **Invalid structural lifecycle.** |
| Closed local supersession cycle | **Invalid structural lifecycle.** |
| Multiple records superseding one prior record | **Structurally valid; possible semantic conflict.** Core chooses no winner. |
| Simple nested Review without ID | **Valid** when no independent citation or lifecycle continuity is needed. |
| Review-of-review | **Valid by nesting.** IDs are required only for the records independently targeted. |
| Historical/superseded Review requiring continuity but lacking ID | **Invalid/insufficient addressability.** A later ID cannot retroactively prove anonymous continuity. |
| Source revision or fingerprint changes | **Valid under the same Source ID** when origin-context continuity is asserted; neither field is identity. |
| Out-of-document Revision parent | **Structurally valid and non-dereferencing; externally unverifiable** for existence and remote cycles. |

The classification intentionally distinguishes structural invalidity, semantic
conflict, incomplete information, profile-dependent meaning and facts that
cannot be verified from one document.

## Decision

ADR-0014 establishes:

1. one required scope descriptor with tri-state completeness and an optional
   qualified definition, required when completeness is `complete`;
2. one optional inline, identified current Revision with `0..*` parents,
   independent from optional history;
3. mandatory ADR-0009 identity for every serialized Revision and Tombstone;
4. one top-level current Tombstone collection with distinct Tombstone/target
   IDs and mandatory target category;
5. one directed replacement-to-prior supersession form, no canonical reverse
   duplicate and no automatic invalidation;
6. optional qualified validity intervals independent from Revision membership;
7. one optional history envelope with separate completeness, previous
   Revisions, descriptive Changes and non-duplicating historical record
   membership references;
8. conditional Change identity: mandatory only for independent addressability
   or lifecycle continuity, with late identity unable to prove earlier
   anonymous continuity;
9. `revision + targets + qualified kind` as the minimum Change semantics, with
   optional inert ADR-0012 details and no patch/replay behavior;
10. retention of distinct-ID historical records in their canonical collections
    and use of separate earlier SemanticDocuments for exact prior same-ID
    states, avoiding a second snapshot dialect;
11. accepted Assertion and Binding identity-continuity rules across lifecycle;
12. conditional trust-record identity exactly when independent targeting or
    lifecycle continuity requires it; and
13. local closed-graph/reference/consistency validation with explicit
    out-of-document uncertainty and no dereference.

## Consequences

- Minimal consumers can ignore `history` and still understand current state.
- Producers always declare current scope/completeness but need not invent
  history, timestamps or Revision lineage.
- Complete absence claims are bounded; omission never silently becomes
  portable deletion.
- Tombstones, supersession and validity remain distinct mechanisms.
- Assertion and Binding correction retain their accepted identity boundaries.
- Trust and Change metadata stay compact when purely scoped, at the cost that
  later-minted IDs cannot establish earlier anonymous continuity.
- Full prior same-ID record states use separately consumable revision documents
  instead of duplicate IDs or replay-dependent embedded snapshots.
- History-aware consumers bear bounded graph/reference consistency costs but no
  merge, transaction or event-replay obligations.
- Profiles may require understood scope, history closure, retention or temporal
  semantics without making them universal core requirements.

## Remains open

- final subordinate JSON member spelling and JSON Schema expressions;
- lexical tokens for core target categories and completeness values;
- standard qualified scope-definition, Change-kind, validity-axis and
  lifecycle vocabularies;
- profile-specific completeness and history-retention requirements;
- exact general-IRI/reference-object lexical grammar left open by ADR-0009;
- optional recorded/authored/observed timestamp vocabularies and precision;
- cross-document packaging/discovery for earlier standalone revision states;
- formal limits and diagnostics for partial/external graph validation;
- ADR-0015 Extension/unknown-field behavior and ADR-0016 processing rules; and
- S4 AI Context selection, chunking and continuation syntax.

These are subordinate vocabulary, schema, profile, transport or later-milestone
questions. They do not leave a second current-state representation, replay
requirement, identity ambiguity, deletion shortcut or trust-addressability
policy open inside ADR-0014.

## Acceptance record

The current-state, Revision, scope/completeness, Tombstone, supersession,
validity, Change/history, partial-history, identity-continuity,
trust-addressability, cross-document, privacy and security decisions were
explicitly approved by human architecture decision on 2026-09-03. That
approval includes the normative clarifications that `complete` is scoped and
permits portable absence inference only when the applicable scope/profile is
understood, and that `history.completeness` concerns declared history coverage
without embedding complete prior snapshots or enabling replay.

Six unrelated domains and the required adversarial cases require neither a
domain-specific nor executable primitive. ADR-0015 and ADR-0016 are Accepted;
the formal schema and normative fixtures are implemented as an S2 candidate,
while S2 closure and SDK implementation remain separately unapproved.
