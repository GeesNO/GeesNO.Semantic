# ADR-0022: GeesNO Base Vocabulary admission and initial term set

- **Status:** Accepted
- **Date:** 2026-09-17
- **Accepted by:** Explicit human architecture decision on 2026-09-17
- **Decision order:** Sixth S3 architecture decision after accepted ADR-0021

## Context

S3 has accepted ADR-0017 through ADR-0021. Those decisions define Vocabulary identity/version, abstract publication, lifecycle, Extension vocabulary authoring and optional discovery/authority/governance. D6 was previously blocked because the repository had no documented controlled stable absolute IRI for the GeesNO Base Vocabulary family.

Human architecture authority now explicitly authorizes the controlled domain `geesno.com` as the institutional identity base for GeesNO identifiers when a specific GeesNO.Semantic decision assigns a path. For D6, the assigned Vocabulary family identity is:

```text
https://geesno.com/vocab/base
```

This decision is about identity, not hosting. The IRI is usable and comparable offline. It does not require that a web server exists, that the path resolves, or that a processor dereference it.

This ADR records the accepted D6 abstract Base Vocabulary decision only. It does not publish a Vocabulary artifact, select a concrete publication binding, add S2 schema fields, create a registry, accept D7 or implement any network behavior.

## Prerequisite review

No unresolved prerequisite blocks the accepted D6 decision:

1. Foundation permits a deliberately small Base Vocabulary while preserving a universal, descriptive, software-neutral, format-neutral, domain-neutral and AI-provider-neutral core.
2. ADR-0017 defines Vocabulary family identity as a controlled stable absolute IRI and exact edition identity as `(Vocabulary identity, Vocabulary version)`.
3. ADR-0018 permits abstract membership and required normative definitions before any concrete publication binding exists.
4. ADR-0019 defines edition-scoped lifecycle declarations without making lifecycle state deletion, invalidity, migration or compatibility.
5. ADR-0020 keeps Extension-use declarations separate; this ADR proposes no Extension key contract or payload constraint.
6. ADR-0021 keeps discovery, retrieval locations, publisher attribution, authority and trust separate from identity and conformance.

The concrete Vocabulary publication binding, discovery catalog binding, integrity model and D7 compatibility/mapping semantics remain open.

## Controlling distinctions

```text
GeesNO Base Vocabulary
!= GeesNO.Semantic Core

Base term
!= core primitive
!= core field
!= profile requirement
!= Extension key declaration

Vocabulary identity
!= Vocabulary version
!= expansion base
!= preferred prefix
!= term IRI
!= retrieval location
!= publication URL
!= Git repository URL
!= network dependency
!= requirement to dereference

term IRI
!= local name
!= qualified spelling
!= prefix

Base Vocabulary unavailable
!= invalid bare-core document

unknown Base term
!= invalid bare-core document
```

## Alternatives

### Alternative A - Keep D6 blocked

Leaving D6 blocked would preserve the previous state but would ignore the new human decision authorizing `https://geesno.com/vocab/base` as the controlled Vocabulary family identity. This alternative is no longer necessary.

### Alternative B - Publish an empty Base Vocabulary edition

An empty first edition would be architecturally valid, but it would provide no interoperability value beyond identity allocation. The prior candidate analysis identified two terms that are natural in all six stress domains and can be defined without becoming core mechanics.

This alternative is not recommended for the initial proposal.

### Alternative C - Admit only `label`

`label` is the smallest useful human-readable term. However, many producers also need a non-identifying human-readable explanation distinct from the short designation. Without `description`, early documents would likely invent parallel local terms immediately.

This alternative remains viable if human review decides `description` is too open, but it is not the recommended initial proposal.

### Alternative D - Admit `label` and `description`

Admit only two human-readable, descriptive, optional and inert terms: `label` and `description`. Both are useful across unrelated ecosystems, do not duplicate core identity/classification/source/lifecycle mechanics, and can be bounded by definitions that avoid UI, localization, execution and mandatory profile policy.

This alternative is proposed.

### Alternative E - Admit broader structural terms

Terms such as category/type, represents, part-of, derived-from, same-as, review states, locator descriptors or lifecycle descriptors would either duplicate accepted core mechanics, belong to specialized vocabularies, require D7 compatibility/equivalence semantics or introduce ambiguous domain-specific constraints.

This alternative is rejected for D6.

## Accepted decision

### Vocabulary identity

The GeesNO Base Vocabulary family identity is:

```text
https://geesno.com/vocab/base
```

This IRI identifies the Vocabulary family. It does not include a version token and is not a retrieval location, publication URL, repository URL or network dependency. The following are not the family identity:

```text
https://www.geesno.com/vocab/base
https://geesno.com/vocab/base/0.1.0
https://geesno.com/vocab/base/latest
https://geesno.com/vocab/base.json
```

`www.geesno.com`, GitHub, GitLab, a CDN or another future location may later host documentation, artifacts, mirrors or discovery records. Such locations do not change Vocabulary identity.

The path family `https://geesno.com/vocab/...` is conceptually reserved for explicitly authorized GeesNO vocabulary identities. This does not imply that every path under `https://geesno.com/` is reserved to GeesNO.Semantic and does not affect current application/download paths such as `https://www.geesno.com/tools/` or `https://www.geesno.com/assets/downloads/`.

### Initial Vocabulary version

The accepted initial exact Vocabulary version token is:

```text
0.1.0
```

This is an opaque exact token scoped to the Base Vocabulary identity under ADR-0017. Generic processing infers no SemVer ordering, range, compatibility or migration from its spelling.

```text
Base Vocabulary version
!= SemanticDocument spec_version
!= repository/package version
```

The spelling intentionally aligns with the early pre-1.0 maturity of the project, but it remains a separate Vocabulary edition token. A later change to normative Base Vocabulary content, including adding a term, requires a new Vocabulary version.

The exact accepted edition identity is:

```text
(https://geesno.com/vocab/base, 0.1.0)
```

### Expansion base

The accepted publication/authoring expansion base is:

```text
https://geesno.com/vocab/base/
```

With this metadata, direct concatenation produces the initial term IRIs:

```text
https://geesno.com/vocab/base/ + label
  = https://geesno.com/vocab/base/label

https://geesno.com/vocab/base/ + description
  = https://geesno.com/vocab/base/description
```

This expansion base is authoring/publication metadata. It is deliberately related to the Vocabulary identity, but it is not the Vocabulary identity. Changing only publication decomposition metadata in the future does not by itself change term identity, denoted meaning or semantic edition content under ADR-0018.

### Preferred prefix

The accepted preferred authoring prefix is:

```text
gbase
```

This prefix is only an editorial recommendation for examples and authoring guidance. It is not globally registered, required, semantic identity or a conformance condition. Documents may use any ADR-0010-valid local prefix whose namespace expansion produces the same absolute term IRIs.

`gbase` is preferred over `geesno` because `geesno` is broader than this one Vocabulary family, and over `base` because `base` is likely to collide conceptually in documents that use multiple organizations' base vocabularies.

## Admission criteria

A Base term must satisfy all criteria below. The default is not to admit a term:

1. It has one concise, stable and non-circular normative meaning.
2. It is natural and useful across engineering, tabular data, technical/legal documents, source repositories, scientific datasets and generic assets.
3. It is software-, format-, vendor- and AI-provider-neutral.
4. It is descriptive and inert, never executable or permission-granting.
5. It does not duplicate, alias or weaken a core primitive or core field.
6. It does not depend on profile cardinality, compatibility, migration or conformance policy.
7. It is not better owned by a domain, provenance, review, locator, lifecycle or other specialized Vocabulary.
8. Its meaning remains useful when no one domain or implementation dominates.
9. It can be interpreted from a supplied exact edition without network access, registry lookup or automatic dereference.
10. It uses the ordinary ADR-0017 through ADR-0021 identity, publication, lifecycle, discovery and authority rules without special privilege.
11. Its absolute term IRI can be minted under a documented controlled identity.
12. Cross-domain evidence and adversarial cases show that likely ambiguities can be bounded by the normative definition rather than hidden in profiles.

Admission does not create a universal closed taxonomy of term kinds. A term may be useful in more than one qualified slot, subject to the applicable core, Vocabulary and profile rules.

## Rejection criteria

Reject or move outside Base any candidate that is domain-, product-, vendor-, format-, database-, spreadsheet-, Git-, UI-, transport-, protocol-, LLM-, agent- or tool-specific; executable; an authorization/enforcement mechanism; a transaction, command, adapter, driver, registry operation or implementation convenience.

Also reject terms that duplicate or alias Entity, Source, Binding, Assertion, Provenance, Confidence, Review, Revision, Change, Tombstone, Validity or Extensions as core mechanics. A specialized Vocabulary may qualify those mechanics but cannot recreate them as Base primitives.

## Initial term set

The accepted first edition contains exactly two terms:

| Local name | Absolute term IRI | Lifecycle |
| --- | --- | --- |
| `label` | `https://geesno.com/vocab/base/label` | `experimental` |
| `description` | `https://geesno.com/vocab/base/description` | `experimental` |

The initial lifecycle state is `experimental` for both terms. They are simple and broadly useful, but the first edition still needs interoperability experience around language, multiplicity, display conventions and profile interaction. Experimental status does not relax ADR-0017 identity stability, does not imply instability of meaning inside the edition and does not create a compatibility guarantee.

No Extension-use declaration or machine-checkable Extension payload contract is proposed for either term.

### `label`

**Term IRI:** `https://geesno.com/vocab/base/label`

**Normative definition:** A concise human-readable textual designation associated with a semantic subject to help people recognize or refer to that subject in context.

**Scope:** The term denotes a human-facing designation. It may be used where a Vocabulary/profile permits a qualified term to identify a textual property or similar descriptive assertion.

**Boundaries:** not semantic identity; not source/native identity; not required for any subject; not unique; not a filename, UI label, display instruction, localization system or rendering rule; not a language requirement; not an execution hint, command, permission or tool instruction; and not proof that the chosen wording is authoritative or complete.

`label` is not core because the core already has stable identity, assertion mechanics and optional qualified properties. `label` supplies one ordinary Vocabulary meaning that can be asserted when useful. It is not a profile rule because it does not require occurrence, cardinality, language policy or fallback behavior.

### `description`

**Term IRI:** `https://geesno.com/vocab/base/description`

**Normative definition:** A human-readable declarative textual explanation of a semantic subject's meaning, role, content or relevant context.

**Scope:** The term denotes explanatory human-readable text. It may be used where a Vocabulary/profile permits a qualified term to identify a textual property or similar descriptive assertion.

**Boundaries:** not semantic identity; not a required documentation field; not a UI tooltip, renderer instruction, formatting instruction or prompt; not executable or operational instruction text; not proof of truth, authority, completeness or current live state; not a replacement for Provenance, Confidence, Review, Source, Binding, lifecycle, profile conformance or normative Vocabulary definitions; and not a language, length or formatting policy.

`description` is not core because it is optional descriptive vocabulary meaning above accepted assertion/value mechanics. It is not a profile rule because profiles may decide whether descriptions are required, localized, bounded, reviewed or projected.

## Deferred and rejected candidates

| Candidate | D6 result | Reason |
| --- | --- | --- |
| Category/type | Rejected from Base | Qualified Type Assertions already provide classification mechanics; a generic category term would duplicate or blur core typing. |
| Represents | Rejected from Base | Concept-Representation is already a dedicated core assertion category and must not be recreated as a predicate shortcut. |
| Same-as / equivalent | Rejected from D6 | Equivalence, mappings, substitutability and compatibility belong to D7. |
| Containment / part-of | Deferred outside the initial Base | Broadly recurring but ambiguous across physical, logical, document, ownership and collection structures. Direction, transitivity and scope usually require specialized Vocabulary/profile rules. |
| Derived-from | Deferred to provenance-focused Vocabulary work | It overlaps Provenance, source/evidence and method semantics; one Base predicate risks collapsing derivation kinds. |
| Provenance/method descriptors | Deferred to a specialized Vocabulary | Source-authored, imported, deterministic, inferred, user-authored and curated distinctions need a coherent family rather than isolated Base terms. |
| Source/Binding descriptors | Deferred to source/locator Vocabularies | Format, locator, revision, fingerprint and method meanings vary by source family and must not privilege products or formats. |
| Lifecycle/change descriptors | Rejected as duplicate or deferred to lifecycle Vocabularies | Revision, Change, Tombstone, supersession and Validity mechanics are core; subordinate qualified meanings need focused Vocabulary work. |
| Review states | Deferred to a review Vocabulary/profile | `unreviewed`, `accepted`, `rejected` and `corrected` remain illustrative until exact review vocabulary and transition policy are accepted. |
| Validity/scope qualifiers | Deferred to specialized Vocabulary/profile work | Applicability and completeness often depend on profile or domain scope and must not become hidden Base policy. |

## Relationship to accepted decisions

- ADR-0017 controls Vocabulary identity, version and term identity. The Base Vocabulary gains no hidden core privilege.
- ADR-0018 controls abstract publication. This ADR proposes identity, edition, membership and definitions, but no concrete artifact or schema.
- ADR-0019 controls lifecycle. The first edition proposes `experimental` lifecycle declarations for `label` and `description`.
- ADR-0020 controls Extension vocabulary authoring. This ADR proposes no Extension-use declarations or payload contracts.
- ADR-0021 controls optional discovery, authority and governance. `geesno.com` control is an authority/governance responsibility; processing remains offline and does not require dereference.

## Cross-domain validation

| Domain | `label` | `description` | Result |
| --- | --- | --- | --- |
| Engineering-like object graph | Human designation for a component, assembly or representation. | Human explanation of role, design intent or semantic interpretation. | Useful without geometry, CAD/BIM fields or adapter assumptions. |
| Spreadsheet/table data | Human designation for a table, column, row concept or derived measure. | Explanation of what a column, metric or sheet represents. | Useful without spreadsheet-specific core fields or formulas. |
| Technical/legal documents | Human designation for a clause, requirement, exhibit or defined concept. | Explanation of meaning, scope or document context. | Useful without legal-domain ontology or rendering instructions. |
| Software/source repositories | Human designation for a module, symbol, package or analysis concept. | Explanation of purpose, role or semantic interpretation. | Useful without Git semantics, code parsing or execution. |
| Scientific datasets | Human designation for an observation, variable, sample or dataset entity. | Explanation of measurement context, variable meaning or dataset content. | Useful without selecting a discipline-specific schema. |
| Generic product/asset data | Human designation for a product, asset, feature or representation. | Explanation of product/asset meaning or context. | Useful without vendor taxonomy or commerce-specific model. |

Both terms remain optional, inert and human-readable across all six domains. Neither requires a new core member, Entity kind, assertion category, schema field, adapter, network service or execution primitive.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| Document uses `https://geesno.com/vocab/base/label` while the network is unavailable or `geesno.com` is unavailable. | Term identity remains valid and exactly comparable from supplied data. Bare-core processing remains possible and no automatic fetch is required. |
| `https://geesno.com/vocab/base` returns HTTP 404. | HTTP state does not change Vocabulary identity or invalidate a locally supplied exact edition. Retrieval location and identity remain separate. |
| Public website uses `https://www.geesno.com/`. | `https://www.geesno.com/vocab/base` is not the canonical Vocabulary identity. `www` may later host documentation or mirrors only. |
| GitHub, GitLab, CDN or another host publishes artifacts. | Hosting location does not become Vocabulary identity, authority proof or edition identity. |
| Future hosting changes. | Vocabulary, edition and term identities remain unchanged; retrieval/discovery evidence may change under ADR-0021. |
| Future domain control changes. | Published identity is not automatically rewritten. Maintaining control is a governance/operation responsibility; delegation/transfer evidence remains ADR-0021 territory. |
| A document has no Base terms. | Valid. Base membership is not mandatory. |
| A document uses unknown or unavailable Base terms. | Bare-core S2 processing remains valid when the document otherwise conforms; Base-aware interpretation may be unavailable. |
| A producer treats `label` as unique identity. | Invalid interpretation. `label` is not semantic identity and has no uniqueness guarantee. |
| A producer treats `label` as a UI display command. | Invalid interpretation. It is descriptive data, not presentation instruction. |
| A producer treats `description` as an executable prompt or tool instruction. | Invalid interpretation. It is inert untrusted text. |
| A profile requires every Entity to have a label. | That requirement belongs to the profile, not the Base term. |
| A future edition adds a Base term. | Requires a new Vocabulary version under ADR-0017. |
| A future edition incompatibly changes a term meaning. | Requires both a new Vocabulary version and a new term IRI. |
| A future edition changes only preferred prefix or expansion base. | Does not by itself change term identity, denoted meaning or semantic edition content. |
| A third-party vocabulary defines similar human-readable terms. | Terms coexist by absolute IRI. No automatic equivalence or preference is inferred; D7 owns mappings/equivalence. |

## Consequences

- D6 is Accepted by ADR-0022.
- The Base Vocabulary family has a controlled stable absolute identity.
- The initial exact edition is `(https://geesno.com/vocab/base, 0.1.0)`.
- The initial term set is intentionally tiny: `label` and `description`.
- Both initial terms are experimental and optional.
- No S2 schema, fixture, `spec_version`, core field, profile, Extension contract, discovery service, registry, publication binding, SDK, adapter, resolver or web page follows from this proposal.
- D7 remains open and unstarted.

## Remains open

- concrete Vocabulary publication serialization, media type, schema and artifact production;
- concrete lifecycle/publication member names and binding details;
- optional discovery catalog, retrieval, signature and integrity bindings;
- review/provenance/source/lifecycle specialized vocabularies;
- D7 equivalence, mapping, substitutability, compatibility ranges, migrations, composition and profile-to-Vocabulary compatibility;
- whether profiles require, constrain, localize, review or project `label`/`description`; and
- long-term operational governance for continued control or delegated stewardship of `geesno.com` identities.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-17. Acceptance covers the GeesNO Base Vocabulary family
identity `https://geesno.com/vocab/base`, initial Vocabulary version `0.1.0`,
publication/authoring expansion base `https://geesno.com/vocab/base/`,
preferred prefix `gbase`, the initial experimental `label` and `description`
terms, the admission/rejection criteria and all non-core, offline, non-
dereference and non-execution boundaries recorded above.

Acceptance closes D6. It does not itself publish a Vocabulary artifact, choose
a concrete publication serialization/schema, create a discovery catalog,
registry, resolver, website, SDK, adapter or execution behavior, modify S2,
accept D7, close S3 or open S4.
