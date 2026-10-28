# ADR-0011: Canonical JSON assertion placement and addressability

- **Status:** Accepted
- **Date:** 2026-08-31
- **Last substantial review:** 2026-09-02
- **Accepted by:** Explicit human architecture decision on 2026-09-03
- **Decision order:** After accepted ADR-0009, ADR-0010 and ADR-0012

## Context

Accepted ADR-0005 defines a hybrid abstract assertion contract: Type /
Classification Assertions, Property Assertions, Relations and
Concept–Representation associations have specialized claim bodies but share
subject, trust, review, lifecycle, validity and Extension semantics. That
abstract choice does not require a hybrid JSON layout.

S2 must select one canonical place and one stable addressing model for each
serialized assertion. Allowing an equivalent Property Assertion under both an
Entity and a document-level assertion collection would create producer
dialects, ambiguous ownership and unstable review/lifecycle targets.

The governing rule for this decision is:

> **One semantic assertion category has one canonical serialized placement.**

## Requirements

The canonical JSON assertion model must:

- represent all four accepted assertion categories without changing S1;
- identify exactly one subject and one specialized claim body per assertion;
- retain competing and independently sourced claims without selecting truth;
- provide stable targets for Provenance, Confidence, Review, correction,
  supersession and lifecycle;
- avoid identity based on array position, JSON Pointer, member order or mutable
  claim hashes;
- distinguish repeated claims from aggregate list/set values;
- keep assertion identity distinct from Entity identity;
- keep trust metadata scoped to the record it qualifies;
- remain processable without registry lookup, dereference, an LLM or an SDK;
- avoid a dependency on the future S3 base vocabulary; and
- remain viable for partial, large and cross-domain datasets.

## Placement alternatives

### Alternative A — inline assertions

Type and Property Assertions would be nested below their subject Entity, while
Relations and Concept–Representation associations would be attached to a
chosen endpoint.

Advantages:

- high locality for a human or AI reading one Entity;
- compact examples because the subject can be inferred; and
- convenient single-Entity authoring.

Costs:

- identity and lifecycle targeting become dependent on paths or repeated IDs;
- Relations and associations need an arbitrary owner and invite endpoint
  duplication;
- document-wide conflict, review and supersession processing requires walking
  several structurally different locations; and
- moving or projecting an Entity can change an assertion's structural address.

Inline placement is not recommended for canonical exchange.

### Alternative B — global assertion collection

Every assertion is one record in a top-level collection and identifies its
subject explicitly.

Advantages:

- one index and one processing path for all claims;
- stable IDs independent of document ordering;
- direct support for competing, reviewed and superseded claims;
- Relations and associations have no privileged endpoint; and
- simple structural rejection of inline/global duplicates.

Costs:

- more references and IDs in small documents;
- lower visual locality than nesting under an Entity; and
- producers must mint identity before a claim needs correction or review.

This is the recommended canonical placement.

### Alternative C — mixed placement

Some categories, or some occurrences of a category, would be inline while
others were global. This can look compact, but it permits the same semantic
fact to have two normative JSON representations and forces consumers to merge
locations.

The abstract model's hybrid contract is about shared semantics, not JSON
nesting. Mixed placement is therefore rejected for the canonical exchange
serialization.

## Canonical placement

Every serialized Type, Property, Relation and Concept–Representation
association is an identified record in the single top-level `assertions`
collection. No assertion-like `entity.type`, `entity.types`,
`entity.properties`, `entity.relations`, endpoint relation, association array
or singular `concept_id` shortcut is a second normative form.

Conceptually:

```json
{
  "entities": [
    {
      "id": "urn:uuid:00000000-0000-4000-8000-000000000010",
      "kind": "concept"
    }
  ],
  "assertions": [
    {
      "id": "urn:uuid:00000000-0000-4000-8000-000000000101",
      "kind": "property",
      "subject": {
        "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
        "location": "in-document"
      },
      "property": "core:label",
      "value": "Example"
    }
  ]
}
```

This ADR freezes the single collection and category responsibilities. Final
root requiredness, exact optional-member omission rules and
JSON Schema expressions remain part of the later serialization/schema freeze;
they cannot introduce another assertion placement.

Entity records retain identity, core kind and any separately approved Entity
state. They do not own canonical assertion arrays. Derived indexes or
application views may inline or reverse-index assertions outside the normative
document without becoming a second GeesNO.Semantic JSON encoding.

## Assertion ID alternatives

### Option A — mandatory ID on every assertion

Every serialized assertion receives an ADR-0009 semantic record ID.

Benefits:

- review, correction, supersession, conflict and lifecycle can target any
  assertion from its first appearance;
- no anonymous-to-addressable structural migration is required;
- duplicate ID detection is uniform; and
- IDs do not depend on array positions or claim content.

The cost is additional bytes and producer work. The decision accepts this cost
for stable interoperability.

### Option B — ID only when addressability is needed

This is smaller for simple claims, but a later Review or correction would need
to assign identity retrospectively. Consumers could not prove that the newly
identified record is continuous with the prior anonymous occurrence, and
equivalent producers could serialize the same claim differently.

This option is rejected.

### Option C — deterministic derived identity

Deriving identity from array position is unstable under insertion or
reordering. Deriving it from the claim body makes correction change identity
implicitly, couples identity to unresolved byte canonicalization and can merge
independent claims with identical content. A hash would also introduce an
unapproved algorithm/version contract.

This option is rejected.

### Decision

Every serialized assertion has a mandatory primary ID governed by ADR-0009.
The ID is record identity, not truth, content equality or Entity membership:

```text
Assertion has semantic record identity
!=
Assertion is Entity
```

`Entity.kind` remains limited to Concept and Representation. This ADR
introduces no new Entity kind.

## Addressability

Assertion IDs, and IDs on independently addressable nested trust records, use
the accepted ADR-0009 identifier, equality and document-wide uniqueness rules.
They are stable semantic record addresses, never JSON paths. A reference to an
addressable record uses its ID and target-location expectation. Nesting supplies
trust scope but is not a substitute for identity when independent targeting is
required. Duplicate declared IDs are invalid even when the records have
identical content.

## Subject and reference rules

Every assertion identifies exactly one semantic subject. A Type, Property or
Relation subject is an ADR-0009 reference to an Entity. A
Concept–Representation association uses its Representation as the category's
subject and one Concept reference as its association target.

An `in-document` subject or target must resolve exactly once in the document's
addressable ID space. An `out-of-document` reference is not silently treated as
resolved and does not trigger dereference. Exact policy constraints on which
profiles may use external subjects remain outside this placement decision.

Global placement never derives a subject from nesting.

## Type / Classification Assertion

The canonical claim body contains:

```text
kind = type
subject = Entity reference
type = ADR-0010 qualified term
```

An Entity can have zero or more Type Assertions, including multiple or
conflicting types. No `entity.type` shortcut is normative. Each claim retains
its own ID, trust and lifecycle envelope.

## Property Assertion

The canonical claim body contains:

```text
kind = property
subject = Entity reference
property = ADR-0010 qualified term
exactly one of value or condition = ADR-0012 form
```

Both `value` and `condition`, or neither, is a structural error. JSON `null` is
not a substitute for either branch.

Several Property Assertions for the same subject/property are repeated claims.
One Property Assertion whose value is an ADR-0012 list or set is one aggregate
claim. These are not automatically equivalent: a vocabulary/profile may assign
different cardinality or aggregation semantics.

## Relation

The canonical claim body contains:

```text
kind = relation
subject = Entity reference
predicate = ADR-0010 qualified term
object = Entity reference
```

The Relation appears once in `assertions`. It is not repeated under the subject
as outgoing, under the object as incoming or in another global relation
collection. Reverse and adjacency indexes are derived processing artifacts.

## Concept–Representation association

Three principal encodings were compared:

1. a generic Relation;
2. Relation mechanics with a required base-vocabulary predicate; and
3. a dedicated assertion category.

A generic Relation does not make the endpoint kinds or universal association
cardinality mechanically explicit. A required `represents` predicate would
make a core S1 mechanic depend on an S3 vocabulary term. A singular shortcut
would encourage one-to-one ownership and lose independent trust/lifecycle.

The decision therefore uses a dedicated `concept_representation` assertion:

```text
kind = concept_representation
subject = Representation Entity reference
concept = Concept Entity reference
```

Each pair is an independently identified assertion. Both endpoint cardinalities
remain `0..*`; the direction is a serialization role, not ownership or
exclusivity. Encoding the same association as a Relation or `concept_id`
shortcut in the normative document is invalid.

## Provenance, Confidence and Review placement

### Alternatives

- **Scoped nested records:** scope is structural and local, but shared metadata
  may repeat.
- **Global trust collections:** every assessment is referenceable and reusable,
  but simple claims become a second graph with explicit target edges.
- **Hybrid placement:** optional global promotion recreates two normative forms
  and conditional migration.

### Decision

Provenance, Confidence and Review records are nested only in the exact record
whose scope they qualify. Assertions may contain `provenance`, `confidence`
and `reviews`; a trust record may itself host scoped trust/review metadata when
another assessment qualifies that record. There is no parallel global trust
collection and no document- or Entity-wide scope inferred from proximity.

ADR-0011 mandates stable identity for every Assertion. It does **not**
universally mandate identity for every Provenance, Confidence or Review record.
A trust record may remain anonymous when it is purely scoped metadata nested in
its host. When citation, lifecycle, supersession, correction or another use
requires independent semantic targeting, that record requires stable
addressability and any declared ID uses ADR-0009 and the document-wide
uniqueness domain. This does not make a trust record an Entity.

A Review of an assertion is nested in that assertion. A Review of a previous
Review is nested in the Review it qualifies. A simple nested Review does not
receive an ID merely because it exists; a Review that must be cited or targeted
independently needs stable addressability under the rule coordinated with
ADR-0013 and ADR-0014. Implementations must not use a JSON Pointer or array
index as semantic identity. Defensive nesting limits are implementation
controls; accepted ADR-0014 fixes the lifecycle/addressability trigger while
exact trust-record fields remain subordinate.

## Provenance reuse

A Provenance record states that evidence/method applies in one host scope.
Applying the same method to one thousand assertions therefore does not create
one globally shared Provenance record whose scope must be inferred.

Producers may reference the same identified Source, external evidence or
method term from multiple nested Provenance records. Repetition can later be
reduced by a profile or S4 AI Context projection, but canonical core JSON keeps
scope explicit and does not introduce a second trust graph for compaction.

## Claim identity and stability

An assertion ID identifies a stable claim record. Its identity-defining claim
body comprises its category, subject and category-specific content:

- Type: subject + type term;
- Property: subject + property term + value/condition;
- Relation: subject + predicate + object; and
- Concept–Representation: Representation subject + Concept target.

Changing that claim body is not an in-place correction. It creates a new
assertion with a new ID; the prior assertion can be retained and the new record
can supersede or correct it using the lifecycle mechanism finalized by
ADR-0014. This preserves historical traceability and prevents the same ID from
denoting different claims across Revisions.

The same assertion ID may persist while its non-claim envelope evolves, for
example when scoped evidence, Confidence, Review or lifecycle state is added.
The exact Revision/change representation remains ADR-0014's responsibility.

Two different IDs may intentionally make identical claim bodies because they
represent independent producers, observations or Provenance. That is
structurally valid and is not automatically deduplicated. The same ID appearing
twice, or denoting different claim bodies, is a structural/identity error.

## Assertion order

Order in `assertions` has no semantic meaning and never contributes to identity
or conflict resolution. Reordering the collection does not change claims.
This ADR defines no byte ordering; ADR-0016 owns member/collection
canonicalization for signatures or hashes. ADR-0012 list order remains semantic
inside an individual list value.

## Document collection boundary

The candidate document keeps responsibilities conceptually separate:

```text
entities | sources | bindings | assertions | revision | history |
tombstones | extensions
```

ADR-0011 freezes only the assertion-related rule: all four assertion categories
live in `assertions`, and their trust records live only in the host they
qualify. Source/Binding and lifecycle/history/tombstone architecture is now
fixed by accepted ADR-0013/0014; Extension strictness is fixed by accepted
ADR-0015.

## Minimal-document impact

| Case | Canonical impact |
| --- | --- |
| Concept-only | Entity record only; no assertion is invented. |
| Representation-only | Entity record only; no Concept association is inferred. |
| Entity with one type | One Entity plus one identified global Type Assertion. |
| Entity with one property | One Entity plus one identified global Property Assertion. |
| One Relation | Endpoint Entities plus one identified Relation. |
| One Concept–Representation association | Two Entities plus one identified dedicated association. |

The global form costs one explicit subject reference and one assertion ID per
claim. That overhead is accepted because it removes conditional structural
migration and supports future review/correction. Exact empty-collection
omission rules remain part of the root serialization/schema freeze, not a
reason to create inline assertion shortcuts.

## AI readability

Inline forms have better immediate locality, while a global collection is more
graph-like. Canonical exchange prioritizes deterministic interoperability and
stable targeting. S4 may define a compact AI Context projection that groups or
inlines selected claims while preserving their IDs and declaring that it is a
projection, not another core-conformant JSON dialect.

## Streaming analysis

A global JSON array does not change semantic ownership or require assertion
order. Producers can emit records in any order allowed by their JSON writer;
consumers may index IDs incrementally and complete reference checks at the end.
Very large or indefinite streams may later use a framing/streaming
serialization that maps the same abstract assertions. That future transport
need does not justify mixed placement in canonical JSON 0.1.

## Cross-domain evidence

| Domain | Stress case | Result of proposal |
| --- | --- | --- |
| Engineering | Component classifications, dimensions and connectivity | Type, Property and Relation records share one collection; no endpoint duplication is needed. |
| Spreadsheet | Repeated cell/row claims versus one aggregate list | Separate assertion IDs preserve repeated claims; list/set remains an explicit value choice. |
| Legal | Competing interpretations and Reviews | Conflicting claims coexist; structural nesting gives every Review exact scope, while only independently targeted Reviews need an ID. |
| Software | Dependency Relation and corrected classification | Dependency has one direction/place; correction receives a new assertion ID and retains the old claim. |
| Scientific | Measured quantity with Provenance | ADR-0012 value stays inside one Property Assertion while evidence remains scoped; independent evidence targets can be identified when needed. |
| Product | Several Representations and competing mappings | Dedicated many-to-many association records avoid singular Concept ownership. |

No domain requires one assertion per property, one Concept per Representation,
a privileged relation endpoint or an application-specific field.

## Adversarial cases

| Case | Classification under proposal |
| --- | --- |
| Same Property Assertion inline and globally | **Invalid structural dialect/duplicate placement.** |
| Duplicate assertion IDs | **Invalid structural identity.** |
| Two assertions with the same claim body and different IDs | **Structurally valid; possible independent or semantically duplicate claims.** |
| Same assertion ID with different body | **Invalid identity continuity**, including across Revisions. |
| Review scoped to an assertion | **Valid** when nested in that assertion; its own ID is not universally required. |
| Review of a previous Review | **Valid** when nested in the Review it qualifies; the reviewed Review needs an ID only when portable independent targeting is required. |
| Supersession targeting an assertion | **Supported by accepted ADR-0014's replacement-to-prior encoding.** |
| Relation duplicated from both endpoints | **Invalid duplicate normative placement.** |
| Concept–Representation encoded with `concept_id` | **Invalid non-canonical shortcut.** |
| Property with both value and condition | **Invalid claim body.** |
| Property with neither value nor condition | **Invalid claim body.** |
| Anonymous assertion later needing correction | **Invalid from first serialization; every assertion requires an ID.** |
| Nested trust record requiring independent lifecycle/targeting | **Requires stable addressability under accepted ADR-0014's conditional trigger.** |

Structural conformance does not decide whether two different-ID claims are
true, duplicates, independent evidence or conflicts.

## Decision

ADR-0011 establishes:

1. one top-level `assertions` collection as the sole normative placement for
   Type, Property, Relation and Concept–Representation assertions;
2. one mandatory ADR-0009 ID on every serialized assertion;
3. one explicit Entity subject per assertion, with the Representation as the
   subject of the dedicated Concept–Representation category;
4. specialized claim bodies using accepted ADR-0010 terms, ADR-0009 references
   and ADR-0012 values/conditions;
5. a dedicated `concept_representation` category, not a Relation predicate or
   Entity shortcut;
6. nested-only Provenance, Confidence and Review, without a universal ID
   requirement; independently addressable trust records use ADR-0009 identity;
7. claim-body stability: changing the claim creates a new assertion ID, while
   scoped envelope evolution may retain the ID;
8. no semantic meaning for assertion array order; and
9. no normative inline/reverse/shortcut duplicate form.

## Consequences

- Producers mint more IDs and emit explicit subject references.
- Consumers gain one assertion index, uniform assertion duplicate-ID checks and
  stable targets wherever independent addressability is declared.
- Claims with identical content are retained when their IDs differ; content
  hashing is neither identity nor automatic deduplication.
- Associations remain a universal core mechanic without depending on S3.
- Nested trust data can repeat, but its scope cannot silently widen.
- S4 may optimize prompt locality without changing canonical exchange.
- Assertion, identified trust-record and Entity identities remain separate
  roles in one ADR-0009 uniqueness domain.

## Remains open

- final JSON Schema `$defs`, conditional expressions and diagnostics;
- exact root requiredness and empty-collection omission rules;
- exact fields/state vocabularies inside Provenance, Confidence and Review;
- formal schema expression of accepted ADR-0014 conditional trust
  addressability, supersession, validity, Revision and history rules;
- Source/Binding placement details under ADR-0013;
- out-of-document lifecycle/reference integrity in partial graphs;
- Extension member policy under ADR-0015;
- byte ordering/canonicalization under ADR-0016; and
- S4 compact projection and future streaming transport syntax.

None of these open details permits a second assertion placement, weakens
mandatory Assertion identity or makes every trust occurrence identified.

## Acceptance record

The placement alternatives, assertion addressability, four claim bodies,
Concept–Representation encoding, nested trust scope, claim stability, ordering,
minimal overhead, streaming, cross-domain evidence and adversarial outcomes
were explicitly approved by human architecture decision on 2026-09-03.

The approval includes mandatory ADR-0009 identity for every serialized
Assertion and explicitly excludes a universal identity requirement for every
Provenance, Confidence or Review occurrence. Accepted ADR-0013/0014 require
identity when a trust record needs independent semantic addressability, but
they cannot use JSON Pointer or array position as its identity.
