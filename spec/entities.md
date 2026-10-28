# Entity, Concept and Representation

**Scope:** Universal abstract Entity, Concept and Representation model.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## Entity

Entity is the abstract universal semantic subject. It has exactly one semantic
identity and one core kind. The only core kinds are Concept and Representation.
Adding domain kinds would duplicate vocabulary classification and is rejected.

An Entity makes these capabilities available with cardinality `0..*` unless a
claim occurrence itself requires otherwise:

- human-readable labels;
- Type / Classification Assertions;
- Property Assertions;
- participation in Relations;
- Bindings;
- Provenance, Confidence and Review with explicit scope;
- lifecycle information;
- namespaced Extensions.

None is required merely for the Entity to exist. An identified but otherwise
unknown Entity is useful incremental semantic information.

## Concept

A Concept denotes a logical, semantic or real-world thing independently of a
digital occurrence. It may be purely semantic, may be created before source
material is known, and may continue after every known Representation has been
removed.

Concept cardinalities:

- semantic identity: exactly `1`;
- associated Representations: `0..*`;
- direct Bindings: `0..*`;
- classifications, properties and other relations: `0..*`.

A direct Binding on a Concept can be useful when the source itself contains a
native semantic record. It is never required and does not eliminate the
Concept–Representation distinction.

## Representation

A Representation denotes one digital occurrence or manifestation. Its form can
be textual, tabular, visual, geometric, database-oriented, temporal,
code-oriented or otherwise. The core does not require a representation payload
type.

Representation cardinalities:

- semantic identity: exactly `1`;
- associated Concepts: `0..*`;
- Bindings: `0..*`;
- classifications, properties and other relations: `0..*`.

`0..*` Concept associations deliberately supports:

- a Representation not yet classified or understood;
- a passage/region/record that manifests several Concepts;
- uncertain or competing associations represented as separate assertions;
- profiles that later restrict a use case to `0..1` when justified.

Accepted ADR-0008 establishes `Concept 0..* <--> 0..* Representation`. Multiple
associations are independent assertions; they are not automatically equivalent,
simultaneously true, accepted or authoritative. Each can carry Provenance,
Confidence, Review and lifecycle metadata under ADR-0005.

> **NON-NORMATIVE conceptual example**
>
> ```text
> Representation R1
>   -> Concept C1  accepted
>   -> Concept C2  inferred / confidence 0.61
>   -> Concept C3  rejected
> ```

## Association lifecycle

Concept–Representation association is a semantic claim, not an identity merge.
It can be added, reviewed, rejected, corrected or superseded while both Entity
identities remain stable. Removing a Representation does not imply removal of
its Concepts. Removing a Concept does not imply deletion of source data.
Accepted ADR-0007 also keeps association lifecycle independent from Entity,
Binding and Source lifecycle; supersession is directed and target-specific, not
automatic invalidation.

Accepted [ADR-0011](../adr/0011-canonical-json-assertion-placement.md) serializes
this as the dedicated `concept_representation` assertion category, with the
Representation as `subject` and the Concept as `concept`. It is not a generic Relation, does not require a vocabulary-specific
predicate, and does not use a singular `concept_id` shortcut.

## Excluded assumptions

Geometry, page, cell, row, file path, function, SKU, sensor, material, room and
customer are neither Entity kinds nor mandatory attributes. They belong to
Bindings, vocabularies, profiles or Extensions as appropriate.
