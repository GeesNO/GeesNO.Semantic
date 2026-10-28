# Source and Binding

**Status: ACCEPTED ABSTRACT CONTRACT AND ADR-0013 JSON ARCHITECTURE**

## Distinct responsibilities

**Source** describes a reference context: an origin resource, dataset,
document, service response or other information-bearing source.

**Binding** correlates one semantic Entity with a native identity or location
within one Source context.

Keeping them distinct avoids repeating source metadata for every correlation
and prevents a locator from becoming semantic identity.

## Source requirements

A Source has one reference identity within the SemanticDocument governed by
accepted ADR-0009. Accepted ADR-0013 makes that ID mandatory in JSON and admits
an ID-only Source. It may optionally describe locations, revision, fingerprints
and scoped trust; media/format, application and labels remain profile/
vocabulary/Extension concerns rather than mandatory product fields.

A Source may be partially known. “Partially known” means its reference identity
exists while descriptive details are absent or explicitly unknown; it does not
license an empty unreferenceable Source record.

Consumers must not automatically dereference Source locations.

## Binding requirements

A Binding conceptually has:

- exactly one bound Entity;
- exactly one Source context;
- zero or more locator components/details at the abstract level;
- optional correlation state/method;
- optional Provenance, Confidence, Review and lifecycle context;
- optional namespaced Extensions.

A source-level Binding with no narrower locator can mean “this Entity is
represented by/correlated with this Source as a whole.” A more specific Binding
can carry a native ID, key, region, range, symbol, segment or other qualified
locator. Accepted ADR-0013 maps this to `0..1` locator whose single ADR-0012
structured value can contain compound details.

## Cardinality scenarios

| Scenario | Conceptual result |
| --- | --- |
| Purely semantic Concept | Concept has `0` Bindings and `0` Representations. Valid. |
| Representation before source correlation | Representation has `0` Bindings. Valid but not source-locatable. |
| Partially known source | Binding references a Source whose metadata is incomplete; locator may also be incomplete. |
| One occurrence exposed in several systems | Representation or Concept has multiple Bindings, each scoped to a Source. |
| One Concept with several occurrences | Concept has `0..*` associated Representations; each Representation independently has `0..*` Bindings. |
| Native semantic registry record | Concept may bind directly to its record without inventing a Representation when no separate occurrence is useful. |
| Lost/stale locator | Binding lifecycle marks correction/invalidation/supersession; Entity identity remains. |

No Entity class requires a Binding. Profiles can require source traceability for
a use case, but that is not universal core completeness.

## Locator design alternatives

| Alternative | Advantages | Problems |
| --- | --- | --- |
| Fixed universal fields | Easy for one domain and simple validation. | Inevitably embeds domain fields and cannot cover regions, keys, symbols and temporal segments uniformly. Rejected. |
| Completely opaque payload | Maximum extensibility. | Consumers cannot discover locator kind or common semantics; weak interoperability. |
| Universal path/segment list | Compact for hierarchical sources. | Spatial, relational and temporal locators do not naturally share one path grammar. |
| Common Binding envelope plus qualified locator payload | Stable correlation/trust semantics with extensible locator families. | Requires namespace/profile rules and careful preservation of unknown locator data. |

Accepted [ADR-0006](../adr/0006-source-binding-model.md) selects the last
alternative at the abstract level. Accepted ADR-0009 governs identifier syntax.
[ADR-0013](../adr/0013-source-binding-serialization.md) is Accepted: every
Source/Binding has an ADR-0009 ID, the records use separate top-level
collections and one optional qualified locator reuses ADR-0012 without changing
this accepted abstract contract.

## Invariants

- Binding never substitutes for semantic identity.
- Binding identity denotes continuity of one specific correlation record; it
  is not derived from Entity + Source + locator or any equal body.
- Distinct Bindings may share Entity, Source and locator while keeping distinct
  IDs; no tuple uniqueness or content deduplication is inferred.
- A locator is interpreted only in its Source context.
- Correlation does not prove semantic truth or equivalence.
- Source metadata and locator detail can be enriched independently.
- Bindings are descriptive and do not grant permissions or execute retrieval.
- Source references are not automatically dereferenced.
- Profiles may restrict locator families without changing universal core.
- Product-specific locator semantics belong to qualified vocabularies/profiles
  or Extensions, not mandatory core fields.

## Lifecycle

Binding has lifecycle independent from its Entity. A locator can become stale,
be corrected, invalidated or superseded without changing Entity identity. A
Source revision does not determine semantic Revision or Entity identity. Lost
correlation is not Entity removal. Accepted ADR-0013 gives every Binding a
mandatory ADR-0009 ID and permits locator correction under the same ID only
when continuity of that specific correlation/occurrence is preserved. A new or
competing occurrence requires a new ID even if the body matches. Under accepted
ADR-0007, Binding and
Source-description lifecycle are also separable: changing or superseding either
does not silently change the other, and lifecycle claims remain descriptive and
subject to provenance/trust policy.
