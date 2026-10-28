# Extensions

**Scope:** Universal Core Extension semantics and Core 0.1 JSON representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md), accepted ADR-0015 and ADR-0016.

Extensibility is mandatory under the universal Core architecture. The following rules apply:

1. Extensions are namespaced/qualified.
2. Unknown Extensions do not invalidate otherwise conforming core content unless
   an explicitly applicable profile requires them.
3. Core identifiers cannot be reused with incompatible meaning.
4. Experimental Extensions are identifiable as experimental.
5. Extensions cannot silently redefine core semantics.
6. Extensions are inert data.
7. Extensions are never executable plugins.

## Extension points

ADR-0015 permits one optional `extensions` map only on these
semantic record hosts:

```text
SemanticDocument | Entity | Assertion | Source | Binding |
Revision | Tombstone | Change | Provenance | Confidence | Review
```

It does not add `extensions` to scope/history/validity helpers, references,
namespace/profile/vocabulary declarations, Source descriptors, locators or
ADR-0012 value/condition structures. Those shapes already have exact qualified
roles, or their containing semantic record is the proper Extension host. An
Extension is scoped to its host and does not automatically apply to the entire
document.

Profiles may require particular Extensions, but such content then contributes
to profile conformance, not bare core conformance. A producer must not hide data
required for core interpretation in an Extension.

## Key and payload boundary

Each map key is an ADR-0010 qualified term. Its declared prefix expands to the
absolute Extension term IRI; no registry, dereference or vendor lookup follows.

ADR-0015 compares ADR-0012-only payloads, arbitrary JSON data and an explicit
semantic/opaque envelope. It accepts arbitrary JSON data because the explicit
Extension boundary already prevents that payload from becoming an alternate
core value form. Raw numbers, objects, arrays and `null` are opaque Extension
data, never inferred Property values or semantic conditions. The payload stays
inert and may not provide or override core meaning.

## Consumer behavior

An unknown Extension remains valid for bare core when its host, key and payload
are valid and no applicable profile requires understanding. A validator or
reader need not rewrite it. A tool claiming lossless round-trip must preserve
the key's expanded identity and payload semantics without numeric or structural
loss; accepted ADR-0015 leaves the exact numeric-token mechanism to accepted
ADR-0016. A deliberately lossy projection may omit it only when
its contract permits and reports the loss.

Unknown core members remain invalid. A future core idea carried as an Extension
does not become core without an explicit new version and migration.

## Core JSON and Vocabulary ecosystem boundary

Accepted ADR-0015 fixes Core 0.1 JSON Extension hosts, qualified keys,
arbitrary-JSON payloads, unknown-field/Extension behavior, preservation
requirements, exact version dispatch and prohibition of core overrides.
Accepted ADR-0016 specifies the associated raw processing and preservation
mechanics.

The Vocabulary ecosystem is governed separately by accepted ADR-0017 through
ADR-0021, including identity/version, publication, lifecycle, Extension
Vocabulary authoring, payload compatibility, optional discovery, authority
and governance. These contracts do not introduce new Core Extension host
locations or override Core semantics.

## Further interoperability considerations

- profile declaration compatibility rules;
- concrete Vocabulary publication binding and payload-constraint language;
- discovery and authority conventions;
- projection/omission reporting under applicable accepted contracts;
- interoperable resource-limit profiles; and
- cross-edition compatibility/migration conventions for independently changing
  Extension data.

Domain-specific content must first be considered for a vocabulary or profile.
Extensions are not a route for growing a hidden universal ontology.

Accepted [ADR-0010](../adr/0010-qualified-term-namespace-model.md) governs
qualified-term identity. Accepted
[ADR-0015](../adr/0015-version-extension-strictness.md) governs Extension
placement and strictness. Accepted
[ADR-0016](../adr/0016-json-processing-canonicalization.md) governs exact
JSON processing, numeric-token preservation and related serialization rules.
These requirements are implemented by the Core 0.1 JSON schema and checker.

Accepted ADR-0017 defines Vocabulary identity/version; ADR-0018 establishes
the publication minimum; ADR-0019 covers lifecycle; ADR-0020 addresses
Extension Vocabulary authoring and payload compatibility; and ADR-0021
addresses optional discovery, authority and governance. The Vocabulary
ecosystem remains separate from the universal Core Extension contract.
