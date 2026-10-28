# JSON Source and Binding serialization analysis

**Scope:** Core 0.1 JSON Source and Binding representation (`spec_version` `0.1.0`).
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

This design applies accepted ADR-0006, ADR-0009, ADR-0010, ADR-0011 and
ADR-0012 without making a file, URL, application, format or locator family
mandatory. Accepted ADR-0013 through ADR-0016 establish the concrete Core 0.1 JSON
member and processing rules. JSON Schema formalizes the structurally
expressible constraints; it does not independently originate semantics.

## Role and placement

```text
Source  = separately referenceable origin context
Binding = one identified Entity-to-Source correlation
Locator = where/how that correlation is expressed inside the Source
```

Source is not Entity, locator, claim, permission or retrieval instruction.
Sources and Bindings occupy separate top-level `sources` and `bindings`
collections. Neither identity nor reference target is inferred from nesting or
array position.

## Source envelope

The accepted universal Source roles are:

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

Only `id` is required. Every serialized Source uses ADR-0009 identity in the
document-wide space. A Source with no other member is valid.

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000201"
}
```

An expanded illustration is:

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000211",
  "locations": [
    {
      "kind": "origin:logical-resource",
      "value": "https://data.example.invalid/resource/42"
    },
    {
      "kind": "origin:mirror-resource",
      "value": "urn:example:mirror:42"
    }
  ],
  "revision": {
    "kind": "version:edition",
    "value": "edition-3"
  },
  "fingerprints": [
    {
      "algorithm": "digest:example-algorithm",
      "value": "example-only"
    }
  ]
}
```

The qualified namespace declarations required by the terms are omitted from
this record-level fragment. Source ID, location, revision, fingerprint and
SemanticDocument Revision are distinct. None is automatically dereferenced.

## Source metadata boundary

| Information | Accepted treatment | Reason |
| --- | --- | --- |
| Location / external resource identifier | Optional `locations [0..*]`, each qualified kind + ADR-0012 value | Supports mirrors and non-URL resources without a parallel identifier system. |
| Source revision/version | Optional one qualified kind + ADR-0012 value | Represents opaque, numeric, temporal or structured external versions without Git semantics. |
| Fingerprint | Optional `fingerprints [0..*]`, qualified algorithm + lexical value | Keeps algorithm, digest and Source ID separate; signatures remain out of scope. |
| Media/format description | Vocabulary/profile/ADR-0015 Extension | No fixed field is universal across logical and physical origins. |
| Application/vendor | Profile/ADR-0015 Extension | Product identity is not universal Source structure. |
| Label/access notes | Profile/ADR-0015 Extension | Avoids a second property system on non-Entity records and localization policy. |
| Provenance/Confidence/Review | Optional nested trust metadata | Scope is the Source description only, never all referring claims. |

Source ID denotes one origin/reference context, not its location, revision,
fingerprint, label or metadata bundle. Changing those descriptors does not
mechanically change Source identity. The same ID may continue when the producer
asserts origin-context continuity; a genuinely different origin context gets a
different ID. Core does not infer continuity from metadata equality or change.

## Binding envelope

Every serialized Binding has mandatory ADR-0009 identity. Its minimum body is
`id + entity + source`; `locator` is optional:

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
  }
}
```

This means correlation with the Source as a whole; no artificial locator is
invented. A detailed Binding adds one locator and optional qualified method:

```json
{
  "id": "urn:uuid:00000000-0000-4000-8000-000000000212",
  "entity": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  },
  "source": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000211",
    "location": "in-document"
  },
  "locator": {
    "kind": "table:record-key",
    "value": {
      "kind": "structured",
      "datatype": "table:record-key-value",
      "members": {
        "table:key": "A-42"
      }
    }
  },
  "method": "mapping:source-authored"
}
```

The complete accepted roles are:

```text
id         [1]
entity     [1] reference to Concept or Representation
source     [1] reference to Source
locator    [0..1]
method     [0..1] qualified term
provenance [0..*]
confidence [0..*]
reviews    [0..*]
lifecycle / validity hooks [optional; ADR-0014]
extensions [optional; ADR-0015]
```

Binding is optional and plural for every Entity. Multiple Bindings may share an
Entity, Source and even locator body. Different IDs are not automatically
deduplicated; a repeated ID is invalid.

## Locator model

Fixed page/cell/key/box/time fields are domain-biased; arbitrary JSON is not
interoperable; one universal path language does not cover spatial, relational,
tabular, temporal and symbolic data. The accepted sole locator form is:

```text
locator
├── kind  = ADR-0010 qualified term [1]
└── value = ADR-0012 canonical value [1]
```

A Binding has `0..1 locator`. Compound sheet/row/column,
document/page/region, database/composite-key and media/time-range locations use
one qualified ADR-0012 structured value. No second locator value system or
cross-source component list is introduced.

An unknown declared locator kind is mechanically valid and preservable, though
a profile may require an understood kind. An undeclared prefix or raw arbitrary
JSON value is invalid under the accepted term/value boundaries.

## Binding identity and stability

Binding ID identifies continuity of one specific correlation record, not an
immutable locator spelling. `entity` and `source` are required anchors:
changing either requires a new Binding ID, but the anchors do not derive
identity or impose pair uniqueness. Matching Entity, Source and locator bodies
can still identify distinct independent, duplicate or competing records.

The same Binding ID may continue when a locator is added, corrected, refined or
updated after relocation only when the same specific correlation/occurrence
continues. Correcting `A10` to `A11` may preserve one ID for the same occurrence.
A new ID represents another occurrence, competing/independent correlation or
changed Entity/Source anchor. A changed locator kind can be either refinement
or a new correlation; the producer must state continuity through identity
rather than a processor inferring it from body equality.

Accepted ADR-0014 defines the encoding for historical
correction, staleness, supersession and Source revision transitions. It may not
require replay or collapse Binding identity into locator content.

## Correlation and trust scope

Optional `method` is a qualified term, not a fixed enum of `manual`,
`automatic`, `inferred`, `exact` or `matched`. Provenance explains how the
correlation arose; Confidence assesses it; Review records a scoped disposition;
lifecycle describes current/historical state.

`stale`, Source unavailable, processor lookup unresolved and target absent are
distinct. `resolved` / `unresolved` remains processor state rather than base
Binding semantics.

Source trust qualifies the Source description only. Binding trust qualifies
the Entity-to-Source correlation only. Neither scope establishes Source truth
or the truth of Entity Assertions.

Trust records remain nested in the host they qualify. Their `id` is optional
while they are purely scoped metadata and required only when independent
citation, reference, correction, supersession or lifecycle targeting needs
ADR-0009 addressability. Accepted ADR-0014 fixes the conditional lifecycle
rules.
JSON Pointer and array index are never identity.

## Security and processing

Source locations and locators are inert, untrusted data. They grant no
permission, require no credentials, initiate no dereference, define no
filesystem traversal and execute no command/query/script. An executable-looking
ADR-0012 string stays data. Extensions remain inert under accepted ADR-0015;
exact raw processing is fixed by accepted ADR-0016 and implemented.

## Cross-domain and adversarial result

Engineering object keys, spreadsheet compound ranges, legal page regions,
source-code symbols, scientific observation coordinates, product/database
composite keys, media intervals and logical API results all fit the same
envelope. The complete eight-domain evidence and adversarial classification are
recorded in
[ADR-0013](../adr/0013-source-binding-serialization.md#cross-domain-evidence).

The result preserves these key boundaries:

- ID-only and unreachable Sources are valid;
- multiple locations and multiple same-pair Bindings are valid;
- Binding without Entity/Source and duplicate IDs are invalid;
- Binding without locator and direct Concept Binding are valid;
- Source/locator changes are lifecycle questions, not automatic identity
  changes;
- unresolved lookup is processing state; and
- URL/native equality never proves semantic identity.

## Normative and implementation boundary

Accepted ADR-0013 establishes the Source minimum and metadata boundary,
mandatory Source/Binding IDs, one qualified locator form, continuity of
one specific correlation, scoped trust, security and cross-domain rules.

Accepted ADR-0014 governs lifecycle encoding; ADR-0015 governs Extensions
and strictness; and ADR-0016 establishes exact Core 0.1 JSON member and
processing requirements.

The local JSON Schema, deterministic conformance checker and fixtures
implement or test these accepted contracts. They do not independently
originate semantic rules or grant execution or retrieval authority.
