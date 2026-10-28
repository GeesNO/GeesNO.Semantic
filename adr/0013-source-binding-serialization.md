# ADR-0013: Source and Binding JSON serialization

- **Status:** Accepted
- **Date:** 2026-08-31
- **Last substantial review:** 2026-09-03
- **Accepted by:** Explicit human architecture decision on 2026-09-03
- **Decision order:** After accepted ADR-0009 through ADR-0012

## Context

Accepted ADR-0006 separates two universal roles:

```text
Source
= separately referenceable origin context

Binding
= correlation between exactly one Entity and exactly one Source
```

S2 needs one JSON placement and envelope for both without turning Source into an
Entity, a file/URL enum or a permission to retrieve data, and without turning a
native locator into semantic identity. The design must serve file-like
resources, documents, datasets, databases, API results, repositories, streams,
generated datasets and physical acquisitions without making those examples a
closed Source-kind vocabulary.

Accepted ADR-0009 supplies record identity/references, ADR-0010 supplies
qualified terms, ADR-0011 supplies canonical assertion placement and nested
trust scope, and ADR-0012 supplies the only canonical typed-value mechanism.

## Requirements

The canonical Source/Binding serialization must:

- preserve Source, Entity, Binding, locator and semantic-claim identity as
  distinct roles;
- make every Source and Binding stably referenceable without deriving identity
  from a URL, native key, locator, fingerprint, body hash or array position;
- allow an ID-only Source and a Binding without a narrower locator;
- represent multiple Source locations without privileging HTTP or filesystems;
- reuse qualified terms and ADR-0012 values instead of inventing a locator
  datatype system;
- preserve independent Binding correction, review and lifecycle;
- keep processing resolution state separate from semantic state;
- retain exact trust scope without requiring an ID on every trust occurrence;
- remain deterministic offline and safe for untrusted data; and
- add no product, format, execution, permission or dereference semantics.

## Dependencies

The decision depends on accepted ADR-0006 for abstract roles, ADR-0009 for IDs
and references, ADR-0010 for qualified terms, ADR-0011 for nested trust scope
and ADR-0012 for canonical values. Accepted ADR-0014 supplies the subordinate
temporal correction, staleness, supersession and conditional trust-target
rules. Accepted ADR-0015 supplies the subordinate Extension placement.
Neither decision is allowed to redefine Source or Binding identity.

## Source alternatives

### Alternative A — ID-only universal minimum

Every Source has only `id` as required core state. Optional universal metadata
can be added only where cross-domain interoperability justifies it.

This preserves partially known sources and does not pretend that every origin
has a URL, media type, file path, application name, revision or fingerprint.

### Alternative B — fixed universal resource fields

A fixed envelope such as `url`, `file`, `application`, `format` and `revision`
is convenient for common documents but fails for database snapshots, streams,
logical API results, physical acquisition sessions and origins without a
reachable resource. It also conflates location with identity and makes product
metadata look universal.

This alternative is rejected.

### Alternative C — minimal universal Source envelope

Require `id`; admit only a small set of optional cross-domain roles:

```text
id             [1]
locations      [0..*]
revision       [0..1]
fingerprints   [0..*]
provenance     [0..*]
confidence     [0..*]
reviews        [0..*]
lifecycle / validity hooks [optional; ADR-0014]
extensions     [optional; ADR-0015]
```

This is adopted. `location`, `revision` and `fingerprint` have distinct
shared mechanics; format/media/application/label metadata does not justify a
dedicated core member and remains vocabulary/profile/Extension material.

## Source identity

Every serialized Source has exactly one mandatory ADR-0009 primary `id`. It
participates in the document-wide addressable ID space and identifies an origin
context, not an Entity or a claim.

```text
Source ID
!= URL or Source location
!= native resource identifier
!= Source revision
!= fingerprint
!= Binding locator
!= SemanticDocument Revision
```

Two Sources may report the same location or fingerprint and still have distinct
identities. An absolute HTTP(S) IRI can be deliberately managed as a Source ID
under ADR-0009, but a processor must never infer that a location string is the
ID or that equal locations establish equal Source identities.

Source identity denotes continuity of one origin/reference context, not an
immutable byte sequence, location, revision, fingerprint, label or metadata
bundle. Revision, fingerprint, location or descriptive metadata can evolve
under the same Source ID when the producer asserts that the origin context
continues; those changes do not mechanically require a new ID. When a producer
instead models a different acquisition, snapshot or other origin context, that
different context receives its own Source ID. Core processing cannot infer
continuity or difference from a changed URL, revision, label or digest.

## Source minimal envelope

The minimum valid Source is:

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000201"
}
```

No location, reachability, format, media type, revision, fingerprint or label is
required. Missing optional metadata means not supplied; it does not mean
unknown, inaccessible, nonexistent or redacted.

The accepted optional core members are exactly the roles listed in Alternative
C. Resource identifiers are represented through appropriately qualified
`locations` rather than a parallel `resource_identifiers` collection. A format,
media type, application name or human label may be expressed by an applicable
profile/vocabulary through an ADR-0015 Extension, but it is not a fixed Source
field. This avoids creating a second property-assertion system for non-Entity
records.

Source-level Provenance, Confidence and Review qualify only the Source
description in that record. They do not automatically qualify all Assertions or
Bindings that refer to the Source and do not establish that the source content
is true.

## Source descriptive metadata

| Information | Accepted treatment | Boundary |
| --- | --- | --- |
| Location | Optional core `locations [0..*]`; qualified kind + ADR-0012 value | Not identity, availability, permission or dereference. |
| External resource identifier | A `locations` entry with an appropriate qualified kind | Not a parallel primary-ID or reference system. |
| Source revision/version | Optional core `revision [0..1]`; qualified kind + ADR-0012 value | Not SemanticDocument Revision or Git semantics. |
| Media/format description | Vocabulary/profile data through an ADR-0015 Extension | No fixed media/application field in universal Source. |
| Fingerprint | Optional core `fingerprints [0..*]`; qualified algorithm + lexical value | Not Source ID, signature or mandatory integrity proof. |
| Provenance/Confidence/Review | Optional core nested trust metadata | Qualifies this Source description only. |
| Other descriptive data | Profile/vocabulary/ADR-0015 Extension | Cannot redefine core roles or execute behavior. |

The decision intentionally does not add a generic Source property bag. Such a
bag would create an unreviewed second assertion system for non-Entity records.

## Source location

`locations` has cardinality `0..*`. Each location is one qualified descriptor:

```text
location
├── kind  = ADR-0010 qualified term [1]
└── value = ADR-0012 canonical value [1]
```

Conceptually and non-normatively:

```json
{
  "kind": "origin:logical-resource",
  "value": "https://data.example.invalid/resource/42"
}
```

The qualified kind defines whether a string is a URL-like address, logical
resource name, physical catalogue reference, mirror endpoint or another
location family. Structured, temporal or numeric location data reuses
ADR-0012. An arbitrary raw JSON object is not an alternative location form.

Multiple locations allow mirrors, local and remote references, logical and
physical descriptions, or historical and current access points without
splitting Source identity. Location order has no identity meaning. Equal
location values neither merge Sources nor prove availability.

A location describes where a Source may be found or externally referenced. It
does not assert existence, accessibility, permission, successful resolution or
automatic dereference.

## Source revision

Source revision is an optional single qualified descriptor:

```text
revision
├── kind  = ADR-0010 qualified term [1]
└── value = ADR-0012 canonical value [1]
```

The qualified kind distinguishes external revision schemes while the value can
be an opaque string, exact integer, date/time or qualified structured value.
Compound version dimensions use one ADR-0012 structured value rather than
parallel fixed `commit`, `etag`, `timestamp` or `sequence` fields.

Source revision is descriptive metadata, not a primary semantic ID and not a
SemanticDocument Revision. No Git, timestamp-order or monotonic-sequence
semantics are inferred. A profile may constrain a particular revision kind.

## Fingerprints

`fingerprints` has cardinality `0..*`. Each fingerprint separates:

```text
algorithm = ADR-0010 qualified term [1]
value     = lexical string [1]
```

The algorithm term owns digest encoding and comparison semantics. The core
mandates no SHA family, registry, byte scope or cryptographic suitability.
Fingerprint is optional evidence about described source content; it is not
Source identity, a signature, authority or proof that content is safe. Signature
and integrity policy remain outside this ADR.

## Binding alternatives

### Alternative A — mandatory Binding ID

Every Binding has an ADR-0009 ID from first serialization. Correction,
staleness, review, supersession and competing correlations have stable targets;
several Bindings for one Entity/Source pair remain distinguishable.

### Alternative B — optional Binding ID

This saves bytes for a simple correlation, but later lifecycle or review would
require anonymous-to-addressable promotion. Continuity could not be established
portably and producers would emit two structural variants.

### Alternative C — identity derived from Entity + Source + locator

This would forbid valid multiple/competing correlations, change identity during
locator correction, require unresolved canonical hashing rules and merge
independent records with equal bodies. It is rejected.

Alternative A is adopted.

## Binding ID

Every serialized Binding has exactly one mandatory ADR-0009 `id` in the shared
document-wide addressable ID space. It identifies continuity of one specific,
producer-asserted semantic-to-source correlation record, not the aggregate
relationship between an Entity and a Source.

Binding identity is not derived from Entity + Source, Entity + Source +
locator, locator equality, a native object ID, a content hash, array position
or any other body component. It is distinct from the Entity ID, Source ID,
locator value and any Assertion ID. Two records may have the same Entity,
Source and locator yet intentionally carry different Binding IDs because they
are independent, duplicate or competing correlation records. Duplicate
Binding IDs are invalid even when their bodies are equal.

## Binding body

The minimum canonical Binding body is:

```text
id      [1] ADR-0009 ID
entity  [1] ADR-0009 reference to Concept or Representation
source  [1] ADR-0009 reference to Source
locator [0..1]
method  [0..1] ADR-0010 qualified term
provenance [0..*]
confidence [0..*]
reviews [0..*]
lifecycle / validity hooks [optional; ADR-0014]
extensions [optional; ADR-0015]
```

Conceptually:

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000202",
  "entity": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "source": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000201",
    "location": "in-document"
  },
  "locator": {
    "kind": "table:record-key",
    "value": "A-42"
  },
  "method": "mapping:source-authored"
}
```

`entity` and `source` are explicit and never inferred from nesting. A Binding
without `locator` validly means that the Entity correlates with the Source as a
whole. Binding is optional and plural for both Concept and Representation.

Bindings live in one top-level `bindings` collection, separate from `entities`
and `sources`, so address and lifecycle do not depend on an Entity path. Two
different Binding IDs with equal bodies are structurally valid and are not
automatically deduplicated.

## Locator alternatives

1. **Fixed fields** such as page, row, cell, object ID, bounding box, symbol,
   timestamp or key are rejected as domain-biased.
2. **Opaque JSON** is rejected because no common processor can identify the
   locator family or validate the value boundary.
3. **One universal path language** is rejected because hierarchical paths do
   not cover spatial, tabular, temporal, relational and symbolic locations with
   one stable meaning.
4. **Qualified kind plus ADR-0012 value** is adopted: the core owns one
   envelope and vocabularies/profiles own locator-family semantics.

Unknown locator kinds remain mechanically preservable when their prefixes are
declared. A consumer may be unable to interpret or resolve the locator without
making the Binding structurally invalid. Profiles may require understood
locator families.

## Locator payload

One locator contains exactly:

```text
kind  = ADR-0010 qualified term
value = ADR-0012 canonical value
```

Native string keys remain strings. Exact integer indexes use ADR-0012 integer.
Compound keys, ranges, regions, temporal intervals and symbolic locations use a
qualified ADR-0012 structured value whose members are qualified terms. Lists or
sets use their existing ADR-0012 forms. There is no locator-specific typed-value
system and no raw arbitrary JSON escape hatch.

## One locator per Binding

A Binding has `0..1 locator`. A compound locator has one qualified kind and one
structured value rather than several independent locator components. This
preserves one normative representation for cases such as:

- sheet + row + column;
- document + page + region;
- database + composite key; and
- media + temporal range.

One Binding remains scoped to one Source. A correlation spanning several
Sources uses separate Bindings or an explicitly modelled semantic Concept; a
cross-source locator cannot weaken the exactly-one-Source invariant.

## Binding stability

A Binding ID identifies continuity of one specific correlation, not an
immutable locator spelling. `entity` and `source` are required anchors, but
neither those anchors nor the entire Binding body derive identity or impose
uniqueness. Changing either anchor changes the correlation and requires a new
Binding ID. Multiple Bindings can share the same Entity and Source, and may
even share the same locator, without becoming the same record.

The same Binding ID may continue only when semantic continuity establishes that
the record still denotes the same specific correlation or occurrence and only
its locator is added, corrected, refined or updated after native relocation.
For example, correcting `sheet:A10` to `sheet:A11` may retain the ID when A11 is
the corrected location of the same occurrence. Relocation may likewise retain
the ID when that same occurrence continues within the same Source context.

A new Binding ID is required when the record expresses a different occurrence,
a new or competing correlation, an independently sourced correlation, a
different Entity or a different Source. A different locator kind or value
alone does not mechanically decide the result: it may refine or relocate the
same correlation, or it may describe a separate one. Conversely, equal
Entity/Source/locator bodies do not prove continuity. The producer must assert
that distinction explicitly rather than deriving it from locator equality.

A Source revision and locator may change together under the same IDs when both
origin-context and correlation continuity are asserted. If the revised material
is modelled as a new Source or the mapping is a new independent correlation,
new Source and/or Binding IDs are used. Accepted ADR-0014 defines the
serialization architecture for prior state, correction, supersession, staleness and Revision
membership; it may not redefine these identity boundaries or require replay.

## Correlation metadata

The only accepted compact common correlation descriptor is optional `method`,
an ADR-0010 qualified term. Extensible method terms can distinguish manual,
automatic, inferred, matched or source-authored processes without freezing
those words as a core enum.

Confidence evaluates the correlation; Review records a scoped disposition;
lifecycle/currentness describes state over time; Provenance explains origin and
evidence. `stale` is not a method. `resolved` / `unresolved` is processor lookup
state under ADR-0009, not Binding truth or a base serialized state. Source
unavailability, target absence and locator staleness are also distinct and must
not be collapsed into one token.

Binding Provenance, Confidence and Review qualify only the correlation
`Entity <-> Source[/locator]`. They do not assert that the Entity's Assertions
are true or that the Source itself is trustworthy.

## Trust and addressability

Three policies were evaluated:

- mandatory ID for every trust record creates predictable targets but imposes
  identity on simple nested metadata;
- optional identity, required only for independent addressability, preserves
  compact scoped metadata and supports lifecycle/citation when needed; and
- no trust identity prevents portable review-of-review, correction and
  supersession targets.

The decision adopts the middle policy consistently for trust metadata nested in
Assertion, Source and Binding:

> A Provenance, Confidence or Review record may remain anonymous while it is
> purely scoped nested metadata. It requires ADR-0009 identity when it must be
> cited, referenced, corrected, superseded or lifecycle-managed as an
> independent semantic target.

All trust records remain nested only in the host whose scope they qualify; no
parallel global trust collection is introduced. A nested Review-of-review is
valid. Structural nesting establishes its scope, while portable independent
targeting requires the reviewed Review to be identified. No JSON Pointer or
array index substitutes for identity.

Accepted ADR-0014 fixes the lifecycle members and conditional validation
triggers for independently targeted trust records. That decision does not
alter Source/Binding shape or the rejection of universal trust IDs.

## Security

Source locations, locator kinds and locator values are untrusted descriptive
data. They:

- never trigger automatic dereference, filesystem traversal or network access;
- grant no credential, capability or permission;
- execute no command, script, query, macro or tool call;
- do not prove existence, availability, safety or truth; and
- remain inert when carried in an unknown Extension.

An executable-looking string can be preserved as data but must never be
executed by conformance processing. Implementations apply size, depth, string
length, allocation and time limits as security controls without inventing
universal semantic limits.

## Cross-domain evidence

| Domain | Stress case | Result |
| --- | --- | --- |
| Engineering | Model object with a native key that relocates after model revision | Source ID remains distinct from model location; one qualified locator can evolve under stable Binding continuity. |
| Spreadsheet/tabular | Sheet + row + column or stable record key | A qualified structured locator avoids core row/cell fields; Concept or Representation can bind directly. |
| Technical/legal document | Paragraph plus page region across editions | Source revision remains external metadata; structured region locator and lifecycle can preserve correction. |
| Software repository | File + symbol at an externally named source revision | No Git primitive is required; revision and locator kinds stay qualified. |
| Scientific data | Dataset observation with compound dimensions and optional digest | ADR-0012 structure handles the locator; fingerprint is separate from measurement uncertainty and Confidence. |
| Product/database | Composite business key with competing mappings | Multiple Binding IDs for one Entity/Source pair remain valid; keys never become Entity IDs. |
| Audio/video | Temporal interval plus track/channel context | One qualified structured locator covers interval and channel without a media-specific core field. |
| API/logical resource | Result with no durable URL or current reachability | ID-only Source and Source-level Binding remain valid; processor resolution is not semantic state. |

The same envelope survives all eight cases. File, CAD, table, HTTP, Git and
media concepts appear only in qualified terms/profiles, never as required core
members.

## Adversarial cases

| Case | Classification under the decision |
| --- | --- |
| Source with only ID | **Valid.** It is the minimum Source. |
| Source with no reachable location | **Valid.** Reachability is not conformance. |
| Two Sources with the same URL/location | **Valid.** Location equality does not merge identity. |
| One Source with multiple locations | **Valid.** `locations` is `0..*`. |
| Source revision change | **Lifecycle concern.** Same ID is allowed for continuing origin context; history encoding is ADR-0014. |
| Source fingerprint change | **Lifecycle/integrity observation.** It does not mechanically change Source identity or prove tampering. |
| Binding without Entity | **Invalid.** Exactly one Entity reference is required. |
| Binding without Source | **Invalid.** Exactly one Source reference is required. |
| Binding without locator | **Valid.** It correlates the Entity to the Source as a whole. |
| Concept directly bound to Source | **Valid.** Binding is not restricted to Representation. |
| Representation with several Bindings | **Valid.** Binding cardinality is `0..*`. |
| Two Bindings with the same Entity/Source | **Valid.** No pair uniqueness is imposed. |
| Same locator under different Binding IDs | **Structurally valid.** It may be independent/duplicate/competing semantics; no automatic deduplication. |
| Same Binding ID twice | **Invalid structural identity.** Document-wide uniqueness is violated. |
| Locator with undeclared qualified kind | **Invalid.** ADR-0010 expansion fails. |
| Locator as raw arbitrary JSON | **Invalid canonical locator value.** Use ADR-0012 structured value or an inert ADR-0015 Extension. |
| Locator with executable-looking value | **Structurally valid only when it is a valid ADR-0012 value; security concern.** It remains inert and is never executed. |
| Locator typo correction | **Lifecycle concern.** Same Binding ID may evolve when the intended correlation is unchanged. |
| Native object relocation | **Lifecycle concern.** Same Binding ID may continue for the same occurrence/correlation. |
| Competing locators | **Semantic conflict/independent correlations.** Use distinct Binding IDs when both claims coexist. |
| Source revision causing locator change | **Lifecycle concern.** Same IDs may continue only when Source and correlation continuity are asserted; encoding is ADR-0014. |
| Stale locator | **Lifecycle concern.** It is not processor resolution state. |
| Processor lookup unresolved | **Processing state.** It is not base Binding semantics. |
| Source unavailable | **Processing/external state.** It neither invalidates identity nor proves target absence. |
| Source URL copied/inferred as semantic identity | **Semantic modelling error, not always lexically detectable.** HTTP(S) IDs are valid only when intentionally managed as ADR-0009 identity. |
| Native object ID copied/inferred as Entity identity | **Semantic modelling error, and structurally invalid when it fails ADR-0009 syntax.** Native identity belongs in a locator unless independently minted as semantic identity. |

No listed case requires a product-specific core field or automatic dereference.

## Decision

ADR-0013 establishes:

1. separate top-level `sources` and `bindings` collections;
2. mandatory ADR-0009 identity for every serialized Source and Binding;
3. an ID-only valid Source plus optional `locations`, `revision`,
   `fingerprints`, scoped trust, later lifecycle/validity and Extensions;
4. `locations [0..*]` as qualified kind + ADR-0012 value descriptors;
5. one optional qualified Source revision descriptor, independent from semantic
   Revision;
6. optional fingerprint records with separate qualified algorithm and lexical
   value, never identity or signature;
7. Binding minimum body `id + entity + source`, with `locator [0..1]` and
   optional qualified `method`;
8. one locator form: ADR-0010 qualified `kind` plus ADR-0012 `value`, including
   qualified structured values for compound locators;
9. Binding identity as continuity of one specific semantic-to-source
   correlation: it is not derived from Entity/Source/locator/body equality;
   anchor changes or distinct/competing correlations require a new ID, while
   locator correction, refinement or relocation may preserve the ID only for
   the same continuing correlation or occurrence;
10. no uniqueness constraint on Entity/Source pairs and no content-based
    deduplication;
11. nested trust scope with optional identity required only for independent
    addressability; and
12. no dereference, execution, permission or runtime resolution semantics.

## Consequences

- Source and Binding identity are stable, explicit and never native-derived.
- Minimal producers pay one Source ID and three Binding members without
  inventing location data.
- Consumers implement one locator envelope and one existing typed-value model.
- Locator-family and method meaning moves to vocabularies/profiles while unknown
  qualified kinds remain preservable.
- Binding correction can preserve correlation continuity without conflating
  locator spelling with identity.
- Multiple locations and correlations remain expressible without implicit
  merging.
- Source descriptions and Binding correlations can carry trust metadata without
  propagating its scope to assertions or source truth.
- Accepted ADR-0014 owns temporal placement, lifecycle transitions and
  conditional addressability validation; ADR-0015 owns Extension
  shape/preservation.

## Remains open

- formal schema/vocabulary expression of accepted ADR-0014 Binding/Source
  correction, staleness, supersession, validity and historical-retention rules;
- formal schema expression of accepted ADR-0014 conditional identity for an
  independently lifecycle-managed or externally targeted trust record;
- final trust-record field sets and review/confidence vocabularies;
- exact general-IRI, reference-object and qualified-term lexical schema details
  already left subordinate by ADR-0009/0010;
- standard locator, location, revision, fingerprint-algorithm and correlation-
  method vocabularies, primarily S3/profile work;
- fingerprint lexical encodings, content scope and any future signature/
  integrity threat model;
- ADR-0015 Extension placement and preservation;
- byte-level canonicalization and defensive profile limits under ADR-0016; and
- cross-document/future-chunk reference transport policy.

These open items do not require another Source/Binding envelope, make locator a
semantic ID or reopen the accepted identity/stability decision.

## Acceptance record

The Source alternatives, mandatory identity, ID-only minimum, location
multiplicity, revision/fingerprint roles, Binding identity/body/stability, one
locator/value model, trust addressability, security, eight-domain evidence and
adversarial outcomes were explicitly approved by human architecture decision
on 2026-09-03. That approval expressly fixes Binding identity as continuity of
one specific correlation record: neither matching anchors nor matching
locators derive identity. ADR-0014, ADR-0015 and ADR-0016 are Accepted; the
latter retains its clearly bounded subordinate processing rules and may not
reopen this identity boundary.
