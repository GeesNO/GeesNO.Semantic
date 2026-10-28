# ADR-0009: Identifier and reference model

- **Status:** Accepted
- **Date:** 2026-08-31
- **Accepted by:** Explicit human architecture decision on 2026-08-31
- **Decision order:** First S2 architecture decision

## Context

S2 needs stable identity before it can serialize or connect SemanticDocument,
Entity, Source, Binding, assertion, Revision, Change and later addressable
records. Identity must be usable offline, independent of array position,
JSON Pointer, runtime address, locator and native-source identity, and it must
not imply network access.

The design must also distinguish the expected location of a reference target
from whether a particular processor currently has that target available.

## Alternatives considered

1. **UUID-only.** Simple and autonomous, but unnecessarily excludes identities
   managed by external semantic ecosystems.
2. **General IRI-only without a canonical UUID form.** Globally expressive, but
   leaves autonomous producers with spelling and equality ambiguity.
3. **Parallel UUID and IRI primary IDs.** Flexible, but creates two identity
   systems, alias synchronization and ambiguous equality.
4. **One absolute IRI-capable identity space, including canonical UUID URNs.**
   Offline and externally managed identities use the same equality model.

## Decision

Adopt Alternative 4.

Every primary semantic ID belongs to one absolute IRI-capable identifier space.
UUID is not a parallel identity system: a UUID used as a semantic ID is
serialized as a canonical UUID URN within that same space. Other permitted
absolute IRI forms may be used when an external owner manages the identity.

Each independently addressable record has exactly one primary semantic ID. An
additional external identifier is metadata or an explicit semantic assertion;
it does not silently become a second primary ID or establish equality.

Semantic identity remains distinct from native identity, Binding locator,
Source location, content fingerprint and qualified vocabulary term. None of
those substitutes for a primary semantic ID.

## Canonical UUID URN

The GeesNO.Semantic canonical UUID spelling is:

```text
urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

where each `x` is a lowercase hexadecimal digit and the hyphen grouping is
`8-4-4-4-12`. Braces, bare UUIDs, uppercase hexadecimal, alternate hyphenation
and other equivalent textual spellings are not canonical semantic IDs.

[RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html) permits hexadecimal
digits in either case in the general UUID string representation. This ADR
deliberately narrows that freedom to lowercase so one UUID has one canonical
serialized semantic identifier. The URN form follows the UUID namespace used
by RFC 9562 and the general URN model in
[RFC 8141](https://www.rfc-editor.org/rfc/rfc8141.html).

## Equality and processing

```text
semantic ID equality = canonical serialized identifier equality
```

Consumers compare the canonical identifier strings exactly. They do not infer
identity through HTTP redirects, DNS equivalence, percent-decoding, path
normalization, trailing-slash equivalence, Unicode normalization heuristics,
general IRI case folding, network lookup or ontology equivalence.

This exact comparison is consistent with the simple string comparison model
for IRIs used as identity tokens in
[RFC 3987](https://www.rfc-editor.org/rfc/rfc3987.html). The complete admitted
absolute-IRI grammar and Unicode policy remain open; an implementation must not
invent normalization while those details are unsettled.

An `https:` ID is still an opaque semantic identifier for core processing. No
ID, namespace or reference is automatically dereferenced. If two distinct IDs
denote the same subject, that relationship must be stated explicitly through
approved semantic vocabulary or policy, not inferred by the parser.

## One document-wide addressable ID space

All addressable records in one SemanticDocument share one uniqueness domain.
Two semantically distinct records cannot declare the same primary ID even when
they belong to different categories. For example, an Entity and a Source may
not reuse one ID.

The common space includes SemanticDocument and any Entity, Source, Assertion,
Binding, Revision, Change or other record that its serialization decision makes
addressable. This rule does **not** require every primitive to carry an ID.
Addressability and ID cardinality remain decisions of each primitive's ADR and
serialization contract.

## SemanticDocument identity

S1 already requires every SemanticDocument occurrence to have one conceptual
identity. In the S2 JSON serialization that identity must be represented by one
primary semantic ID. Otherwise exchange, lineage and cross-document reference
cannot preserve the accepted S1 identity. This requirement follows from the
model rather than implementation convenience.

The document ID participates in the same document-wide uniqueness domain as
all other addressable records. Exact JSON member naming and formal enforcement
remain serialization/schema work.

## Reference semantics

A reference carries a target semantic ID plus a target-location expectation.
The minimum expectations are:

- **`in-document`:** the target is expected in the current
  SemanticDocument/payload under the applicable scope rules. In a declared
  closed graph, failure to resolve exactly once is a conformance error.
- **`out-of-document`:** the target is not required to be materialized in the
  current payload. It may be in another SemanticDocument, an omitted
  projection/AI Context, a future chunk or an external store. This expectation
  says nothing about existence, availability, trust or network access.

Target-location expectation is independent of processing resolution state.
`resolved` and `unresolved` report what a processor currently observed; they do
not change target identity and do not mean `in-document` or `out-of-document`.

The smallest core model therefore does not put resolution-state metadata in
the base reference serialization. A validation result, processing API or
optional profile/descriptive metadata may report it without changing the
reference's identity or location expectation. Whether any standardized
optional resolution-state metadata is later admitted remains open.

Exact reference member names and object/string shape remain open. Later
serialization work must preserve these two dimensions and may not restore the
ambiguous `local = resolved` / `external = unresolved` shortcut.

## Consequences

- Autonomous and externally governed IDs interoperate through one identity
  and equality model.
- Duplicate detection is document-wide rather than collection-specific.
- SemanticDocument identity is present in every S2 exchange document.
- A processor can validate local integrity without performing network access.
- Partial documents can identify omitted targets without claiming that they
  are unavailable.
- Producers and consumers must reject or diagnose non-canonical UUID spellings.
- The decision does not define qualified semantic terms; ADR-0010 remains a
  separate vocabulary-identity decision.

## Remains open

- the complete lexical grammar for general absolute IRIs;
- exact Unicode admission, comparison and serialization handling beyond the
  accepted no-heuristic rule;
- exact external/cross-document reference representation;
- whether standardized optional resolution-state metadata exists anywhere in
  core/profile metadata;
- exact serialized reference object/string form and member names;
- addressability and ID cardinality for each primitive other than the required
  SemanticDocument and Entity identities already established by S1/S2;
- formal duplicate-ID enforcement between heterogeneous collections;
- validation policy for unresolved out-of-document references;
- cross-document identity and document+target addressing policy;
- future chunk and continuation transport semantics.
