# Semantic assertion model

**Scope:** Universal abstract assertion model and Core 0.1 JSON correspondence.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## What is an assertion?

An assertion is a scoped semantic claim made by a producer, source, rule, user
or inference process. It has a subject and category-specific claim body, and it
may carry trust, review, lifecycle and extension context.

The specialized assertion categories are:

- Type / Classification Assertion: `Entity has qualified type`;
- Property Assertion: `Entity has qualified property value/condition`;
- Relation: `subject Entity -- qualified predicate --> object Entity`;
- Concept–Representation association: `Representation manifests/represents Concept`.

The abstract model does not prescribe this category's JSON encoding;
accepted ADR-0011 establishes one dedicated canonical assertion form.

## Common conceptual contract

The categories need consistent semantics for:

```text
claim subject [1]
claim body [1]
provenance [0..*]
confidence assessments [0..*]
reviews [0..*]
validity/lifecycle context [0..*]
extensions [0..*]
```

This contract is justified across all six review domains: classifications,
property values, links and Representation associations can all be inferred,
contested, reviewed and superseded. A vocabulary/profile cannot provide this
consistency because it is core claim mechanics, and Extensions cannot safely
redefine trust or lifecycle semantics.

Accepted ADR-0005 defines this contract as an abstract role shared by
specialized claims and does **not** make `Assertion` an Entity. The abstract
contract does not require identity for every claim occurrence; accepted
ADR-0011 requires an ID for every serialized Assertion while retaining
conditional identity for Provenance, Confidence and Review.

## Alternative A — specialized inline assertions

Type and Property Assertions are nested with an Entity, Relations are stored in
their convenient context, and Concept–Representation links may be direct.

| Concern | Assessment |
| --- | --- |
| Simplicity | High for small producers and readers. |
| Extensibility | Metadata rules can diverge between categories. |
| Traceability | Awkward when an assertion needs identity or external evidence/review references. |
| Revisions | Often requires path/index or enclosing-Entity diffs. |
| Deduplication | Repeated provenance/review records are likely. |
| Size / AI Context | Compact and locally readable. |
| Serialization | Direct, but encourages serialization shape to define semantics. |
| Implementation | Lowest initial cost. |
| Interoperability | Risk of category-specific exceptions and inconsistent metadata. |

## Alternative B — all assertions as first-class objects

Every claim has identity and lives in a common assertion collection/graph.

| Concern | Assessment |
| --- | --- |
| Simplicity | Lower; even trivial facts require indirection. |
| Extensibility | Uniform metadata and targeting. |
| Traceability | Strong; claims are independently referenceable/reviewable. |
| Revisions | Fine-grained change and supersession. |
| Deduplication | Shared records/references are possible. |
| Size / AI Context | Verbose; projections must resolve links. |
| Serialization | Graph-like, with more reference integrity rules. |
| Implementation | Higher producer/consumer burden. |
| Interoperability | Uniform if the abstract assertion taxonomy is precise. |

## Alternative C — hybrid specialized claims with a common contract

All categories obey one conceptual envelope. Claims can remain local/compact,
while claims that need independent review, citation, conflict or lifecycle can
be addressable. Core 0.1 JSON establishes one canonical placement to avoid
multiple serialized locations for equivalent claims.

| Concern | Assessment |
| --- | --- |
| Simplicity | Moderate; basic claims stay readable. |
| Extensibility | Shared envelope plus category-specific claim body. |
| Traceability | Strong when identification/addressability is used. |
| Revisions | Fine-grained where needed without forcing it universally. |
| Deduplication | Possible, but optional identity rules must be disciplined. |
| Size / AI Context | Better default compactness; projection can omit non-material metadata explicitly. |
| Serialization | Core 0.1 JSON defines canonical placement separately from the abstract contract. |
| Implementation | Moderate with a clear common interface. |
| Interoperability | Good if optional addressability and equivalence rules are unambiguous. |

## Accepted decision

ADR-0005 accepts Alternative C at the **abstract** level: specialized assertion
categories governed by a common contract, with independent addressability when
the claim must be cited or targeted for provenance, review, conflict,
correction, supersession or lifecycle.

Accepted [ADR-0011](../adr/0011-canonical-json-assertion-placement.md) now
requires an ADR-0009 ID on every serialized assertion and places every Type,
Property, Relation and dedicated Concept–Representation assertion only in the
top-level `assertions` collection. It prohibits inline Entity shortcuts and
keeps an assertion's identity-defining claim body stable.

This serialization decision does not universally require an ID on every
Provenance, Confidence or Review occurrence. Trust records remain nested only
in the host they qualify; purely scoped metadata may be anonymous, while a
record needing independent citation, correction, supersession or lifecycle
targeting requires stable ADR-0009 addressability under accepted ADR-0014.

## Conflict and incremental semantics

- Zero assertions is valid.
- Multiple assertions about the same subject/property/type may coexist.
- Conflict is semantic information, not automatically a syntax error.
- Confidence does not choose a winner by itself.
- Review can reject or correct a claim without erasing history.
- Supersession/lifecycle can state which assertion replaces another when both
  claims are addressable; accepted ADR-0007 defines that directed
  supersession does not automatically invalidate its target.
- Assertion lifecycle is independent from Entity, Binding, association and
  Source lifecycle. A lifecycle label such as latest, reviewed, accepted,
  rejected, corrected or historical does not establish objective truth.
- Missing Provenance, Confidence or Review is absence of metadata, not a default
  authoritative value.
