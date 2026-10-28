# ADR-0027: Projection preservation and material-context semantics

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-21
- **Date:** 2026-09-20
- **Decision order:** Fourth S4 architecture decision after ADR-0026 acceptance

## Context

ADR-0024 accepts exact AI Context Profile identity and the bare-core/Profile
conformance boundary. ADR-0025 accepts Projection as a finite derived semantic
view of an identified source SemanticDocument state under an exact Profile
edition and explicit selection context. ADR-0026 accepts scope-relative
omission, boundedness, truncation and inert continuation semantics.

D4 asks which semantic context associated with selected content must be
preserved so the Projection remains interpretable, correctly scoped and
traceable without copying the whole source SemanticDocument and without turning
preservation into truth, authority, trust, approval, permission, retrieval or
execution.

This ADR proposes abstract preservation semantics only. It does not define
concrete JSON members, Profile requirement syntax, Profile artifacts, schemas,
fixtures, diagnostics, SDK APIs, preservation flags, omission syntax,
continuation syntax, reference encoding, serialization ordering, retrieval
protocols, model integration or execution behavior.

## Prerequisite review

No unresolved prerequisite blocks D4 readiness:

1. The Foundation defines AI Context as compact descriptive context that
   preserves provenance/confidence when material, source bindings needed for
   traceability and omitted/continuation metadata, without defining prompting,
   model routing, RAG, tools, agents or execution.
2. ADR-0009 separates semantic identity from references, locators, native IDs,
   fingerprints and automatic dereference.
3. ADR-0011 gives every Assertion stable identity while keeping Provenance,
   Confidence and Review nested in the exact host whose scope they qualify.
4. ADR-0013 separates Source, Binding and Locator semantics; Source and Binding
   IDs are independent from locations, locators, fingerprints and truth.
5. ADR-0014 establishes state-first lifecycle, scoped completeness, qualified
   validity, explicit Tombstones and conditional trust-record addressability.
6. ADR-0015 separates lossless preservation from lossy projection and keeps
   unknown Extensions inert and unable to override core semantics.
7. ADR-0016 freezes S2 Layers 0-3 and leaves Profile validation to later
   layers.
8. ADR-0024 accepts exact Profile edition identity and the Profile conformance
   boundary.
9. ADR-0025 accepts Projection, selection semantics, source-state traceability,
   identity preservation and the D3/D4 boundary.
10. ADR-0026 accepts omission, boundedness, truncation and continuation
    semantics that D4 must reuse rather than redefine.

## Controlling distinctions

```text
material context
!= all context
!= semantic importance
!= ranking
!= AI relevance score
!= execution priority

preservation
!= truth
!= authority
!= approval
!= permission
!= execution authorization
!= retrieval availability

preserved Provenance
!= truth
!= authority
!= permission

preserved Confidence
!= truth
!= calibrated certainty by default
!= Review
!= Provenance

preserved Review
!= truth
!= universal approval
!= permission
!= execution authorization

preserved Validity
!= Revision membership
!= Provenance time
!= Source revision
!= latest state
!= truth

Source
!= authority
!= truth
!= location
!= Source revision
!= fingerprint

Binding
!= semantic truth
!= Entity identity
!= Source identity
Binding locator
!= semantic identity

reference preservation
!= referenced-record materialization

material context omission
!= deletion
!= false
!= invalid
!= Tombstone

trust metadata absent from Projection
!= no trust metadata exists in source

Projection preservation
!= copy whole source SemanticDocument

context preservation
!= declaration that material context is omitted

explicit omission
!= preservation of omitted content
!= deletion
!= lossless preservation

required materialization
!= material dependency allowed by reference

Profile allows omission
!= omission ceases to be omission
!= Projection complete
```

## Definitions

**Preserved content** is selected source semantic content carried into a
Projection while retaining the source semantic identity and meaning established
by accepted ADRs.

**Context record** means a Provenance, Confidence, Review, Validity, Source,
Binding, Extension or other accepted contextual record or descriptor associated
with selected content.

**Material context** is context required for correct interpretation,
traceability, scoped trust, scoped validity or non-misleading presentation of
selected content under the applicable exact Profile edition or accepted
semantic rule.

Materiality is evaluated relative to selected content, declared Projection
scope and the applicable preservation requirement. It is not a universal claim
that every context record in the source must be copied.

**Preservation requirement** means a future exact Profile edition or accepted
semantic rule that deterministically states what context is required, optional,
allowed by reference, allowed to be omitted or required to be materialized for a
particular Projection use case.

Required materialization means the applicable requirement says the contextual
record itself must be carried in the Projection. A material dependency allowed
by reference means the applicable requirement allows an exact reference to
satisfy the requirement while the referenced target remains outside the
Projection.

D4 does not define the concrete expression of those requirements. D5 owns
Profile requirement expression and Vocabulary/Profile policy. D6 owns concrete
serialization binding.

## Alternatives

### Alternative A - Copy all associated context

A Projection could be required to copy every Provenance, Confidence, Review,
Validity, Source, Binding and Extension related to any selected content. This
is rejected. It defeats compact Projection, often recreates most of the source
SemanticDocument and makes self-containment universal even though accepted S4
architecture leaves self-containment to future exact Profile requirements.

### Alternative B - Preserve only selected assertions and entity records

A Projection could carry selected claims while omitting all contextual metadata.
This is rejected. It can make inferred content look source-authored, uncertain
claims look categorical, scoped Reviews look universal, limited Validity look
current everywhere, and Source/Binding traceability disappear.

### Alternative C - AI relevance determines material context

A Projection generator could use model relevance, embedding scores or prompt
salience to decide which context is material. This is rejected as normative
semantics. External implementations may use AI to suggest a Projection, but a
normative materiality rule must be expressible by an exact Profile edition or
accepted semantic rule and evaluated deterministically.

### Alternative D - Abstract material-context preservation

A Projection must preserve context that is material under the applicable exact
Profile edition or accepted semantic rule. Preservation keeps exact scope and
meaning. Non-material context may be omitted when the applicable requirement
allows it, and omitted material context must remain visible through ADR-0026
omission/continuation semantics rather than being hidden; such visibility is
not preservation of the omitted content. This is proposed.

## Proposed decision

### Material context

D4 accepts the abstract concept of material context:

```text
material context = context required for correct interpretation under the
applicable exact Profile edition or accepted semantic rule
```

Material context is not all source context. A Projection MUST NOT be required
by generic D4 semantics to include every Provenance, Confidence, Review,
Validity, Source, Binding or Extension present in the source SemanticDocument.

At the same time, a Projection MUST NOT omit context that is material under the
applicable preservation requirement in a way that makes selected content appear
more authoritative, certain, reviewed, valid, current, sourced, bound or
self-contained than it is.

```text
materiality != semantic importance
materiality != ranking
materiality != AI relevance score
materiality != execution priority
```

A normative materiality rule must be expressible by a future exact Profile
edition or accepted semantic rule. D4 does not define a materiality language,
closure algorithm, scoring model or concrete syntax.

### Material-context handling

At the abstract level, material context may be handled by these semantic
strategies when the applicable future Profile requirement allows them:

- carrying the material context record itself with its identity and scope;
- preserving an exact reference to the material context record when the target
  is allowed to remain outside the Projection and the exact reference satisfies
  the applicable requirement; or
- declaring the known omission or dependency continuation of material context
  under ADR-0026 semantics.

The first strategy preserves the carried contextual record. The second strategy
can satisfy the applicable requirement only when a future exact Profile edition
or accepted semantic rule permits the target to remain outside the Projection.
The third strategy does not preserve the omitted contextual content. It declares
that material context is not materialized or preserved in the Projection and
prevents that absence from being interpreted as inexistence, falsity, deletion,
or absence of context in the source.

```text
context preservation != declaration that material context is omitted
explicit omission != preservation of omitted content
explicit omission != deletion
explicit omission != lossless preservation
```

This list is conceptual. D4 does not define the concrete fields, reference
encoding, omission records, continuation descriptors or diagnostics.

Preserving a reference is not the same as materializing the referenced record:

```text
reference preservation != referenced-record materialization
```

A Projection MUST NOT fabricate local targets, retarget references, rewrite
semantic IDs or create local Source/Binding records merely to appear
self-contained.

### Preservation does not change scope

Preserving context means preserving its exact accepted scope and meaning. A
Projection MUST NOT elevate, propagate, fuse, widen or generalize contextual
metadata merely because the original host was selected.

Invalid interpretations include:

```text
Assertion Provenance => Entity-wide provenance
Binding Confidence => confidence in Entity truth
Source Review => approval of all assertions from that Source
Review of one Assertion => review of every related Assertion
Validity of one claim => validity of every similar claim
```

Trust and validity metadata remain scoped to the exact record they qualify.
Compaction does not authorize broader scope.

### Provenance preservation

Provenance is material when omitting it would obscure how selected content was
obtained, whether it was authored, imported, inferred, reviewed through an
external process, mapped from another standard or derived from evidence whose
scope is needed for correct interpretation.

A Projection MUST preserve these invariants:

```text
preserved provenance != truth
preserved provenance != authority
preserved provenance != permission
absence of carried provenance != proof that provenance does not exist
```

A Projection MUST NOT make inferred, derived or weakly evidenced selected
content appear source-authored merely because material Provenance was omitted.
D4 does not create new Provenance fields, Provenance vocabularies or a new
Provenance taxonomy.

### Confidence preservation

Confidence is material when omitting it would make an uncertain, estimated,
inferred or weakly supported claim appear categorical under the applicable
Profile requirement.

A Projection MUST preserve these invariants:

```text
confidence != truth
confidence != probability unless its qualified semantics define that
confidence != review
confidence != provenance
```

A Projection MUST NOT transform, recalibrate, aggregate, normalize or otherwise
reinterpret Confidence as part of generic preservation. If a selected claim has
material Confidence, that Confidence must retain its exact scope and semantics
or its omission must be represented under the applicable D3/D5/D6 mechanism.

D4 defines no new Confidence scale, calibration vocabulary or aggregation rule.

### Review preservation

Review is material when omitting it would alter the understood disposition,
review state, rejection/correction context or qualified assessment of selected
content under the applicable Profile requirement.

A Projection MUST preserve these invariants:

```text
review != truth
review != universal approval
review != permission
review != execution authorization
```

A Review nested in an Assertion qualifies only that host or nested target under
accepted rules. A Review of a Source qualifies the Source description, not
automatically every Assertion that names that Source. A Projection MUST NOT
lift Review to the Projection, Entity, Source contents or all related claims.

### Validity preservation

Validity is material when omitting it would silently broaden applicability of
selected content.

The critical failure mode is:

```text
selected claim with limiting Validity
+ Validity omitted
=> claim appears universally/currently applicable
```

A Projection MUST NOT widen validity by omission. Limiting validity context
must be carried or exactly referenced when the applicable Profile rule allows
reference satisfaction. If required limiting validity context is not preserved,
its omission must be declared as omitted material context under ADR-0026.

D4 preserves these distinctions:

```text
Validity != Revision membership
Validity != Provenance time
Validity != Source revision
Validity != latest state
Validity != truth
```

D4 does not create a temporal engine, mandatory timestamps, live-state polling,
subscriptions or freshness protocol.

### Source preservation

Source context is material when selected content needs origin traceability,
evidence context, external revision context, location/fingerprint descriptors
or Source-scoped trust metadata for correct interpretation under the applicable
Profile requirement.

D4 preserves accepted Source invariants:

```text
Source != Entity
Source ID != location
Source ID != Source revision
Source ID != fingerprint
Source != authority
Source != truth
```

A Projection MUST NOT fabricate Source records, convert a location into Source
identity, infer equality from equal locations, auto-dereference a Source IRI or
turn Source presence into trust.

Depending on the future Profile requirement, preserving material Source context
may mean carrying the Source record or preserving its exact reference when the
requirement allows reference satisfaction. Declaring material Source omission
or dependency continuation does not preserve the omitted Source content; it
declares the preservation gap under ADR-0026. D4 does not universally require
every referenced Source to be materialized inside every Projection.

### Binding preservation

Binding context is material when selected content needs source correlation,
locator/method semantics, correlation trust metadata or Binding lifecycle state
for correct interpretation under the applicable Profile requirement.

When a Binding is transported, the Projection must preserve:

- Binding ID;
- Entity anchor;
- Source anchor;
- locator kind/value semantics;
- method semantics when present;
- scoped Provenance, Confidence, Review, Validity and lifecycle semantics when
  material.

D4 preserves accepted Binding invariants:

```text
Binding != semantic truth
Binding != Entity identity
Binding != Source identity
Binding locator != semantic identity
```

A Projection MUST NOT fabricate local Bindings, retarget a Binding to a local
Source, use a native object ID as semantic identity or treat Binding presence as
proof that the correlated Entity assertion is true.

### Material context omission

ADR-0026 already defines omission, partiality and continuation. D4 reuses those
semantics without redefining them.

If context required for correct interpretation under the applicable
preservation requirement is not carried, not exactly referenced in a way the
applicable exact Profile edition or accepted semantic rule treats as
sufficient, and not outside the declared Projection scope by that rule, then
that context is omitted material context.

```text
omitted material context != deletion
omitted material context != false
omitted material context != invalid
omitted material context != Tombstone
```

Known omitted material context is known omission under ADR-0026. If known
required in-scope material context is omitted, the Projection is partial
relative to that declared Projection scope. A Profile may permit partial or
omitted context, explicit omission declarations or continuation metadata, but
that permission does not make the omitted content preserved, complete or no
longer omitted.

```text
known required in-scope material context omitted => partial
Profile permits partial/omitted context != Projection complete
Profile conformance != Projection completeness
Profile allows omission != omission ceases to be omission
```

A future exact Profile edition may define the legitimate Projection scope,
which context must be materialized, when an exact reference is sufficient,
whether partial Projections are allowed, whether explicit omission/continuation
is allowed, and whether self-containment is required. It MUST NOT redefine
`complete`, `partial` or `unknown` contrary to ADR-0026.

If the applicable exact Profile edition or accepted semantic rule establishes
in advance that an exact reference satisfies the requirement and that the
referenced record may remain outside the Projection, the referenced target is
not automatically omitted required in-scope materialized content.

```text
required materialization != material dependency allowed by reference
```

Completeness must not be manipulated by declaring a Projection scope that hides
context known to be required for correct interpretation.

Absence of carried trust, validity, Source or Binding metadata does not prove
that no such metadata exists in the source.

### References and materialization

A Projection may preserve an exact reference whose target is not included when
accepted rules or a future exact Profile edition allow that target to remain
outside the view.

An exact reference can satisfy an applicable preservation requirement only when
the exact Profile edition or accepted semantic rule permits reference
satisfaction. Otherwise, a known required materialized target that is not
carried remains omitted material context under ADR-0026.

Generic processing MUST NOT infer:

```text
referenced target unavailable = target nonexistent
referenced target outside Projection = invalid selected content
missing referenced target = fabricated local target
reference preserved = referenced record materialized
```

Dependency continuation remains distinct from retrieval instruction. D4 does
not add auto-fetch, resolver, registry, network or execution behavior.

### Anonymous trust records

Accepted ADR-0011/0014 allow anonymous Provenance, Confidence and Review records
when nesting supplies their complete scope and no independent addressability is
required.

A Projection preserving an anonymous trust record MUST preserve it inside the
host or nested trust record that establishes its scope. It MUST NOT:

- invent an ID merely for projection convenience;
- use array position or JSON Pointer as identity;
- detach the anonymous record from the host that supplies its scope;
- claim independent historical continuity that the anonymous record cannot
  support.

If an identified trust record is transported, its ID must be preserved. If a
Projection needs independent continuity for an originally anonymous trust
record, D4 cannot retroactively create that continuity; the applicable Profile
must require addressability at the source or report the preservation limit.

### Nested and recursive trust

Nested trust remains structurally scoped. Cases such as Confidence with nested
Review, Review-of-review and reviewed Provenance preserve their nesting scope.

Generic processing MUST NOT turn nested trust into a global trust collection,
Entity-wide trust, document-wide trust or Projection-level trust. D4 does not
create a new trust serialization structure.

### Extensions and lossy preservation

ADR-0015 remains controlling. Unknown Extensions are inert data. Extensions may
add meaning but cannot override core meaning.

A lossy Projection may omit Extension data only when the applicable projection
contract or future exact Profile edition permits that loss. A Projection MUST
NOT claim lossless preservation of a record if it drops, rewrites or
semantically alters unknown Extension data on that record.

A future Profile may require a known Extension. D4 does not define
`omitted_extensions`, Extension-loss syntax, Extension diagnostics, concrete
Profile syntax or a new Extension preservation field.

### Preservation is not source duplication

Traceability does not require embedding every dependency. Self-containment is
not a universal D4 requirement.

```text
material context != all source context
traceability != embedding every dependency
self-containment != universal requirement
```

A future exact Profile edition may require self-contained Projection for a
particular use case. D4 does not impose that requirement generically.

### AI/runtime/security boundary

Preservation semantics must work without AI and MUST NOT depend on:

```text
LLM
RAG
embeddings
vector database
model relevance
AI ranking
tokenizer
token budget
context-window size
agent planning
tool calling
```

Semantic text, Source locations, Binding locators, Extension payloads,
continuation descriptors and trust metadata remain untrusted inert data. None
of them grants permission, executes behavior, triggers retrieval or authorizes
a tool call.

### D5 boundary

D5 remains responsible for Profile requirement expression and Vocabulary/Profile
policy. In particular, D5 owns how an exact Profile edition expresses:

- which context is required;
- required versus optional preservation;
- cardinality and closure rules;
- self-containment requirements;
- required Source/Binding materialization;
- acceptable omission;
- required trust/context closure.

```text
D4 abstract preservation semantics
!= D5 Profile requirement expression
```

D4 does not define a requirement language.

### D6 boundary

D6 remains responsible for concrete representation and binding.

D4 does not define:

- JSON fields;
- JSON schema;
- concrete Projection envelope;
- concrete trust-preservation flags;
- omission syntax;
- continuation syntax;
- reference encoding;
- Profile artifact syntax;
- serialization ordering;
- diagnostics.

```text
semantic meaning != representation
```

A future binding may represent, encode or transport preservation requirements
and metadata. It is not independent semantic authority.

### D7 boundary

D7 remains responsible for Profile conformance result and diagnostics. D4 may
identify conceptual preservation failures, but it does not freeze diagnostic
codes, result formats, severity levels, messages or fixtures.

## Cross-domain validation

| Domain | Preservation stress case | Result under the proposed decision |
| --- | --- | --- |
| Engineering-like object graph | Selected property/assertion has Source, Binding and Provenance. | Material Source/Binding/Provenance is preserved only as required for interpretation; Binding presence is not truth and no local Binding is fabricated. |
| Spreadsheet/table dataset | Computed value depends on formula/provenance context. | Material Provenance or dependency context cannot be omitted in a way that makes computed content appear source-authored or categorical. |
| Technical/legal document | Selected clause carries Review and limited Validity/applicability. | Review and Validity keep exact scope; no clause-specific Review becomes universal legal approval. |
| Software repository/source code | Selected symbol has Binding into a Source revision. | Source revision and semantic Revision stay distinct; Binding locator remains source-relative and no Git semantics become universal. |
| Scientific dataset | Measurement has Provenance, Confidence and Validity interval. | Confidence remains distinct from truth/probability; Validity does not become latest/current state; material limits remain visible. |
| Generic product/asset data | Product assertion cites external Source/Binding with partial trust metadata. | Source and Binding references can remain outside the Projection if allowed; absence does not mean nonexistent or universally unbound. |

The proposal remains universal, domain-neutral, software-neutral,
format-neutral, AI-provider-neutral, offline-capable and non-executable.

## Adversarial cases

| # | Case | Generic processing may infer | Generic processing MUST NOT infer |
| --- | --- | --- | --- |
| 1 | Provenance is dropped from inferred selected content. | Provenance is not carried or is omitted material context if required. | The content is source-authored. |
| 2 | Confidence is dropped from an uncertain selected claim. | Confidence is absent from the Projection or omitted if material. | The claim is categorical truth. |
| 3 | Review scoped to one Assertion is projected near its Entity. | The Review qualifies only its accepted host/scope. | Entity-wide approval. |
| 4 | Source Review is present. | The Source description has that Review. | All assertions from the Source are approved. |
| 5 | Limiting Validity is omitted from a selected claim. | Validity is absent or omitted material context if required. | The claim is universally/currently applicable. |
| 6 | Source reference is preserved but Source record is not materialized. | The exact Source target may be outside the Projection. | Source is nonexistent, invalid or auto-fetched. |
| 7 | Binding reference target lies outside the Projection. | The Binding may be an external dependency. | The selected content is invalid or locally rebound. |
| 8 | Projection fabricates a Binding to create self-containment. | The Binding is not preserved source content. | Valid preservation of the original Binding. |
| 9 | Source location is used as Source identity. | This is a modelling error under accepted Source identity rules. | Equal locations establish equal Sources. |
| 10 | Anonymous Review is given a new ID in Projection. | A new addressable record may exist only as new content. | Continuity of the original anonymous Review. |
| 11 | Anonymous trust record is detached from its host. | Its scope is lost or changed. | Valid preservation of scoped trust. |
| 12 | Identified trust record is re-identified in Projection. | It is not transparent carriage of the same trust record. | Same trust identity. |
| 13 | Trust metadata is absent from Projection. | It is absent from the Projection. | No trust metadata exists in the source. |
| 14 | Material context is explicitly omitted. | Omission/partiality semantics may apply under ADR-0026; omitted content is not preserved. | Deletion, falsity, invalidity, Tombstone or lossless preservation of omitted content. |
| 15 | Dependency continuation is present for material context. | Additional dependency content may exist or be needed outside the current Projection. | Retrieval instruction, resolver requirement, permission or preservation/materialization of the omitted dependency content. |
| 16 | Unknown Extension is omitted while claiming lossless preservation. | Processor/Profile preservation claim is violated. | Lossless preservation succeeded. |
| 17 | Complete Projection scope is used to imply complete trust context for source. | Completeness applies only to the declared Projection scope. | Universal trust completeness. |
| 18 | AI relevance selects which Provenance is material. | An implementation used an external heuristic. | Normative materiality. |
| 19 | Preserved trust metadata is interpreted as authorization. | The metadata is descriptive. | Tool permission or execution authority. |
| 20 | Binding Confidence is copied near Entity claims. | It qualifies the Binding correlation only. | Confidence in Entity truth. |
| 21 | Provenance for one Assertion appears before several assertions. | Its original scope remains the one host. | Shared provenance for all nearby assertions. |
| 22 | Review-of-review is flattened. | Scope may be changed or lost. | Equivalent preserved recursive trust. |
| 23 | Validity interval is treated as Source revision. | Validity is separate semantic applicability. | Source revision or latest state. |
| 24 | Source revision is treated as semantic Revision. | Source revision is external Source metadata. | SemanticDocument Revision identity. |
| 25 | Binding locator is copied as Entity ID. | Locator remains source-relative Binding data. | Semantic identity. |
| 26 | Material Source record remains outside the Projection through an exact reference that the applicable Profile permits as sufficient. | The preservation requirement may be satisfied by reference without local materialization. | Source materialized locally or omitted required in-scope materialized content solely because the target is outside the Projection. |
| 27 | Known required in-scope material Source record is omitted under a Profile that permits partial context. | The omission may be declared and the Profile may allow the partial Projection. | Projection completeness, lossless preservation or that omission ceases to be omission. |
| 28 | Confidence score is recalibrated to a local scale. | This changes Confidence semantics unless a future rule permits derived content. | Transparent preservation. |
| 29 | Several Reviews are merged into one summary Review. | This is derived content if represented. | Same Review records preserved. |
| 30 | Source unavailable over network. | External retrieval failed or was not attempted. | Source identity invalid or Source nonexistent. |
| 31 | Extension payload contains prompt-like text. | It is inert Extension data. | Prompt instruction or tool call. |
| 32 | Self-contained Profile later requires all referenced Sources. | That future Profile may impose the requirement. | Universal D4 self-containment. |
| 33 | Projection omits non-material Source metadata. | Omission may be allowed by the applicable Profile. | Source identity changed. |
| 34 | Projection carries Binding but omits material Binding Review. | Review may be omitted material context if required. | Binding Review did not exist. |
| 35 | A nested Confidence with nested Review is moved to a global trust section. | D4 defines no global trust collection. | Valid scope preservation. |
| 36 | Selected content has material redacted condition context. | Redaction/non-disclosure context may be material. | Redacted information is absent, false or public. |
| 37 | Source fingerprint is interpreted as signature. | Fingerprint is optional evidence under qualified algorithm. | Authority, safety or permission. |
| 38 | Complete Projection omits context outside its declared scope. | Scope-relative completeness may still hold. | Completeness for the whole source SemanticDocument. |
| 39 | Material context omission is hidden by narrowing the Projection scope after selection. | This violates the preservation/materiality boundary if context is required for interpretation. | Valid avoidance of preservation requirements. |
| 40 | Consumer treats preserved Provenance as proof of correctness. | Provenance describes origin/evidence. | Truth or correctness. |

## Consequences

- D4 introduces material context as an abstract preservation concept without
  requiring all source context to be copied.
- Preservation keeps exact scope and meaning; it cannot elevate Provenance,
  Confidence, Review, Validity, Source or Binding semantics.
- Provenance, Confidence, Review, Validity, Source and Binding remain distinct
  from truth, authority, approval, permission, identity and execution.
- Explicit omission or continuation for material context declares that omitted
  content is not materialized or preserved. It uses ADR-0026
  omission/partiality/continuation semantics and remains distinct from
  deletion, falsity, invalidity, Tombstone and lossless preservation.
- Reference preservation remains distinct from referenced-record
  materialization; an exact reference can satisfy a requirement only when an
  exact Profile edition or accepted semantic rule permits reference
  satisfaction.
- Anonymous trust records remain scoped by nesting; identified trust records
  keep their IDs when transported.
- Unknown Extensions remain inert; lossless preservation cannot drop or alter
  Extension semantics.
- D5 Profile requirement expression, D6 concrete serialization binding and D7
  conformance result/diagnostics remain open.

## Remains open

- D5 Profile requirement expression and Vocabulary/Profile policy;
- exact materiality rules for the AI Context Profile edition;
- concrete preservation requirement language;
- concrete Source/Binding materialization requirements;
- concrete omission, continuation and reference encoding;
- concrete AI Context/Profile serialization binding;
- Profile artifact identity and packaging;
- validation diagnostics and conformance result;
- S4 examples after the required abstract decisions are accepted;
- S5 fixtures and mature diagnostic governance; and
- SDK/tooling behavior.

## Acceptance boundary

**Decision status: Accepted**

Accepted by explicit human architecture decision on 2026-09-21. Acceptance
closes S4 D4 only. It does not implement JSON serialization, schema, fixtures,
Profile artifacts, SDK behavior, registry, resolver, network service,
retrieval protocol, AI integration, prompt format, tool call, execution
behavior or any later S4 decision.
