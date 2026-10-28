# Relations

**Scope:** Universal binary Relation Assertions and Core 0.1 JSON representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## Core mechanic

```text
subject Entity -- qualified predicate --> object Entity
```

Each Relation occurrence has exactly one subject, predicate and object. The
direction is explicit. Subject and object use semantic identity, never an array
position or unscoped native locator.

A Relation is a semantic assertion and can carry zero or more Provenance
records, Confidence assessments, Reviews, lifecycle references and Extensions.
Accepted ADR-0011 gives every serialized Relation a mandatory assertion ID and
places it once in the top-level `assertions` collection.

## Predicate semantics

Predicates are qualified vocabulary terms. Multiple vocabularies can coexist,
and the core does not define a large predicate list. Symmetry, transitivity,
inverse relationships, cardinality and domain/range constraints belong to the
predicate's vocabulary or an applicable profile; consumers must not infer them
from a label.

Concept–Representation association has its own dedicated
`concept_representation` Assertion category under accepted ADR-0011, with the
Representation as `subject` and the Concept as `concept`. It is not a generic
Relation, a vocabulary-specific predicate, or a singular `concept_id` shortcut.
Its associations are independent semantic claims rather than an identity merge.

## Reference, lifecycle and modeling boundaries

- Accepted ADR-0009 and ADR-0016 distinguish `in-document` and
  `out-of-document` target-location expectations from processor resolution
  state. External targets are not automatically dereferenced or guaranteed
  available.
- A Relation targets an Entity. Literal claim values belong to Property
  Assertions rather than creating an alternate Relation object form.
- The universal Core does not define an n-ary Relation primitive. A relationship
  Concept can express some patterns through separate Assertions; other roles
  and constraints remain Vocabulary/Profile semantics.
- Parallel Relations may coexist without implicit ordering or claim priority.
  Predicates, inverse/symmetric/transitive behavior and domain/range
  restrictions are not inferred from labels.
- Accepted ADR-0014 distinguishes supersession, validity and Tombstones:
  supersession alone does not imply rejection, invalidation or deletion.
  Removing a Relation does not remove either Entity.

## Invariants

- A domain predicate never becomes a core field merely for convenience.
- Relation existence does not prove the claim is true.
- A consumer must preserve direction and qualified predicate identity.
- Conflicting or parallel Relations may coexist.
- Removing a Relation does not delete its subject or object.
