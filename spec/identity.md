# Identity

**Scope:** Universal semantic identity and Core 0.1 JSON identifier/reference contract.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## Responsibility

Semantic identity gives a SemanticDocument or Entity a referenceable continuity
independent of any one representation or source. It supports relationships,
cross-revision continuity and the association of several Representations with a
common Concept.

## Required conceptual properties

A semantic identity must:

- be stable for the lifetime of the semantic subject;
- be unique in a declared comparison scope;
- compare without relying on array/index position or traversal order;
- survive ordinary label, classification, property and Binding changes;
- not depend on a transient runtime/memory address;
- not depend obligatorily on a mutable path, locator or source-native ID;
- not be silently reassigned to a different semantic subject;
- be usable as the target of semantic references.

Exactly one semantic identity belongs to each SemanticDocument and Entity.
Aliases, equivalence and replacement may be expressed later, but they do not
change which identity is primary within a document occurrence.

## Semantic identity versus source/native identity

```text
semantic identity
    identifies meaning across semantic lifecycle

source/native identity
    identifies or locates information inside one source context
```

The same semantic identity can have multiple Bindings. The same native locator
appearing in different source revisions or source identities does not
automatically denote the same semantic subject. A matching label, locator or
content hash is evidence for correlation, not proof of identity.

## Lifecycle invariants

- Replacing a Representation does not replace the Concept it represented.
- Correcting an assertion does not replace its subject Entity.
- A tombstone reserves historical identity; it is not a new Entity kind.
- Identity continuity across document revisions must be explicit enough that a
  consumer does not infer continuity from collection position.
- “Same as”, merge and split semantics require explicit claims/change records;
  they must not occur as an implementation side effect.

## Accepted Core 0.1 JSON identity architecture

[ADR-0009](../adr/0009-identifier-reference-model.md) accepts one absolute
IRI-capable semantic identifier space. UUID is not a parallel system: offline
UUID identities use one lowercase canonical `urn:uuid:` spelling. Other
permitted absolute IRIs share the same exact canonical-string equality rule.

All addressable records in one SemanticDocument share one uniqueness domain,
regardless of category. SemanticDocument identity is required in Core 0.1 JSON;
accepted ADR-0011 requires every serialized Assertion to participate, and
accepted ADR-0013 requires the same for every Source and Binding. A Binding ID
denotes continuity of one specific correlation and is not derived from matching
Entity/Source/locator values. Purely scoped trust metadata is not universally
addressable, but any independently targeted trust record uses the same
ADR-0009 space.

Reference target-location expectation (`in-document` / `out-of-document`) is
separate from processing resolution state (`resolved` / `unresolved`). The
minimal base reference has no resolution-state member, and no ID or reference
is automatically dereferenced.

Accepted ADR-0014 defines lifecycle/trust addressability. Accepted ADR-0016
specifies general-IRI/Unicode rules and exact reference shape for Core 0.1
JSON. Cross-document packaging remains a separate concern.
