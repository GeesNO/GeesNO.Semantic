# JSON identifier and reference analysis

**Scope:** Core 0.1 JSON semantic identifiers and reference representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md), accepted ADR-0009 and ADR-0016.

This document propagates the accepted
[ADR-0009](../adr/0009-identifier-reference-model.md) identity architecture.
Accepted ADR-0016 freezes the reference object as `target` plus `location`; the
Core 0.1 JSON schema/checker implement that shape.

```text
semantic ID != reference != Binding locator != Source location != qualified term
```

## Accepted identity model

All primary semantic IDs occupy one absolute IRI-capable identity space. A UUID
is used only as the canonical `urn:uuid:` form within that space; it is not a
second identity system. Other permitted absolute IRIs are valid when an owner
manages that identity externally.

Each addressable record has one primary `id`. Additional external identifiers
do not become aliases or establish equality unless explicit semantic policy
states their relationship.

Canonical UUID IDs have lowercase hexadecimal and `8-4-4-4-12` grouping:

```json
{"id": "urn:uuid:5c0e72d4-93de-4b86-8e4a-e9cdce5db3b5"}
```

An externally managed identity uses the same model:

```json
{"id": "https://data.example.org/semantic/items/42"}
```

Semantic ID equality is exact canonical serialized identifier equality. Core
processing performs no redirect following, DNS equivalence, percent-decoding,
path or trailing-slash normalization, Unicode heuristic, general case folding,
network lookup or ontology-equivalence inference. No identifier is
automatically dereferenced.

## Document identity and uniqueness

Every SemanticDocument in Core 0.1 JSON must serialize its abstract-model
semantic identity as one primary semantic ID. It shares one document-wide
uniqueness domain with every other addressable record.

A duplicate is invalid even across categories. An Entity and a Source, for
example, cannot declare the same ID when they are distinct records. The common
space also contains every Assertion under accepted ADR-0011 and every
Source and Binding under accepted ADR-0013. Revisions, Changes and
independently addressable trust records participate when their own
serialization rules require an ID.

This common space does not make every primitive addressable and does not make
an ID mandatory on every primitive. In particular, ADR-0011 does not require an
ID on purely scoped nested Provenance, Confidence or Review occurrences.

## Reference dimensions

A reference combines a target semantic ID with a target-location expectation:

- `in-document`: the target is expected in the current document/payload under
  the applicable scope rules;
- `out-of-document`: the target need not be materialized in the current
  payload.

The following sketches are conceptual and non-normative:

```json
{"target": "urn:uuid:5c0e72d4-93de-4b86-8e4a-e9cdce5db3b5", "location": "in-document"}
```

```json
{"target": "https://data.example.org/semantic/items/42", "location": "out-of-document"}
```

Accepted ADR-0016 selects exactly the object members `target` and `location`,
with closed values `in-document` and `out-of-document`.

An `in-document` reference must resolve exactly once when the applicable scope
declares a closed graph. An `out-of-document` reference can identify a target
in another document, external store, omitted projection/AI Context or future
chunk. It does not claim that the target exists, is trusted, is available or
can be fetched.

## Resolution state is not location expectation

`resolved` / `unresolved` describes what a particular processor currently has
available. It is not part of target identity and is not equivalent to
`in-document` / `out-of-document`:

| Location expectation | Processing observation | Possible interpretation |
| --- | --- | --- |
| `in-document` | resolved | Expected target was indexed once. |
| `in-document` | unresolved | Local-integrity error in a closed graph, or profile/scope diagnostic otherwise. |
| `out-of-document` | resolved | A processor happens to have the external/omitted target available. |
| `out-of-document` | unresolved | Valid absence from the payload; existence is not verified. |

The accepted minimal core reference shape therefore contains no resolution
state. Validation results and processing APIs can report it. A later profile or
optional descriptive-metadata decision may standardize it, but it cannot alter
identifier equality or target-location expectation.

## Reference behavior by context

| Context | Accepted architectural rule |
| --- | --- |
| Complete closed document | Each `in-document` reference resolves exactly once. |
| Partial/filtered document | An intentionally omitted target is `out-of-document` under applicable scope/profile rules. |
| Lifecycle history | Revision, Change and target references use the same identity space and location dimensions. |
| Cross-document relation | The target is `out-of-document`; current materialization is optional. |
| AI Context projection | Stable IDs remain; omitted targets do not become deletions or automatically “unresolved identity.” |
| Future chunks | Chunk membership never becomes identity; transport semantics remain future work. |

## Preserved distinctions

- A Source location may be an IRI but is not automatically the Source ID.
- A Binding locator is Source-scoped native correlation, not semantic identity.
- A qualified term identifies vocabulary meaning, not a record occurrence.
- Content hashes/fingerprints are evidence or integrity metadata, not default
  semantic IDs.

## Remaining interoperability boundaries

The Core 0.1 JSON contract establishes document-wide duplicate-ID checks
and conditional addressability of lifecycle and trust records under accepted
ADR-0009, ADR-0014 and ADR-0016. These are not open serialization decisions.

The following concerns remain outside the bare-Core reference contract:

- optional standardization of processing resolution-state metadata outside
  the minimal reference object;
- external evidence of identity, existence, availability or authority for
  out-of-document targets;
- cross-document identity policies and packaging conventions; and
- transport conventions for future chunked exchange.

ADR-0009 governs record identity and reference expectations. ADR-0010
governs qualified terms and namespaces as a separate semantic mechanism.
