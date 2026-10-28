# GeesNO Base Vocabulary

The GeesNO Base Vocabulary is a deliberately small, optional
Vocabulary intended to provide broadly reusable semantic terms
above the universal GeesNO.Semantic Core.

Its identity, initial terms and architectural boundaries are
established by the accepted
[ADR-0022](../../adr/0022-geesno-base-vocabulary.md).

The Base Vocabulary follows the ordinary Vocabulary contracts
defined by ADR-0017 through ADR-0021. Cross-Vocabulary and Profile
compatibility is addressed separately by ADR-0023.

This document explains the accepted Base Vocabulary design and
its interoperability boundaries.

It is not a machine-readable Vocabulary publication artifact.

## Architectural Boundary

The Base Vocabulary has no special parser privilege, mandatory
Profile status, hidden Core semantics, automatic discovery,
network requirement or exceptional authority mechanism.

```text
Base Vocabulary
!= Semantic Core

Base Vocabulary
!= privileged parser semantics

Base Vocabulary
!= mandatory ontology

Base Vocabulary
!= automatic Extension contract

Base Vocabulary
!= execution layer
```

Unknown Base Vocabulary terms are handled according to the
same applicable rules as other unknown qualified terms.

Bare-Core conformance does not depend on the availability or
use of the Base Vocabulary.

The Base Vocabulary does not modify the Core schema, namespace
expansion rules, conformance Layers 0-3, fixtures or
`spec_version: "0.1.0"`.

## Identity and Edition

The accepted Base Vocabulary parameters are:

| Property | Value |
| --- | --- |
| Vocabulary family identity | `https://geesno.com/vocab/base` |
| Vocabulary version | `0.1.0` |
| Qualified-term expansion base | `https://geesno.com/vocab/base/` |
| Preferred prefix | `gbase` |

Vocabulary identity, edition identity, namespace expansion,
repository paths and retrieval locations remain separate.

The Vocabulary version `0.1.0` is distinct from both Core
`spec_version: "0.1.0"` and the repository preview release
`0.1.0-preview.1`.

The identity is stable and does not depend on network access.

```text
semantic identity
!= publication location

IRI
!= runtime dereference requirement
```

A Vocabulary identity remains valid and comparable offline
even if the corresponding HTTP resource is unavailable.

## Vocabulary Publication Boundary

ADR-0018 permits the definition of abstract Vocabulary
identity, editions, membership and normative meaning
independently of a concrete publication binding.

Defining the Base Vocabulary does not itself establish:

- a machine-readable Vocabulary artifact;
- a Vocabulary JSON serialization;
- a Vocabulary JSON Schema;
- a publication media type;
- a centralized registry;
- a discovery catalog;
- a mandatory resolver.

Any future machine-readable publication must follow the
applicable accepted Vocabulary publication contract.

## Term Admission Criteria

The Base Vocabulary intentionally applies a high threshold
for admitting terms.

A candidate should satisfy all of the following criteria:

1. It has one concise, stable and non-circular normative meaning.
2. It is natural and useful across engineering, tabular data,
   technical/legal documents, source repositories, scientific
   datasets and generic assets.
3. It is software-, format-, vendor- and AI-provider-neutral.
4. It is descriptive and inert, never executable or
   permission-granting.
5. It does not duplicate, alias or weaken a Core primitive
   or Core field.
6. It does not depend on Profile cardinality, compatibility,
   migration or conformance policy.
7. It is not better owned by a domain, provenance, review,
   locator, lifecycle or other specialized Vocabulary.
8. Its meaning remains useful without dependence on one
   dominant domain or implementation.
9. It can be interpreted from an available exact edition
   without network access, registry lookup or dereferencing.
10. It follows the ordinary identity, publication, lifecycle,
    discovery and authority rules of ADR-0017 through ADR-0021.
11. Its absolute term IRI can be minted under a documented
    and controlled semantic identity.
12. Cross-domain evidence and adversarial cases demonstrate
    that likely ambiguities can be bounded by the normative
    definition rather than hidden in Profiles.

The default is to leave a term outside the Base Vocabulary
unless sufficient evidence supports admission.

Admission does not introduce a universal closed taxonomy of
term kinds.

A term may be usable in more than one qualified semantic
position, subject to the applicable Core and Profile rules.

## Rejection and Deferral Criteria

A candidate should remain outside the Base Vocabulary when
its meaning is specifically tied to:

- a domain, product or vendor;
- a software application or file format;
- a database, spreadsheet or source-control system;
- a user interface;
- a transport or communication protocol;
- an AI model, agent or tool framework;
- an executable command or transaction;
- an adapter, driver or registry operation;
- authorization or enforcement behavior;
- a convenience specific to one implementation.

Terms that duplicate or alias Core mechanics must also
remain outside Base.

This includes attempts to recreate:

- Entity;
- Source;
- Binding;
- Assertion;
- Provenance;
- Confidence;
- Review;
- Revision;
- Change;
- Tombstone;
- Validity;
- Extensions.

A specialized Vocabulary may qualify these concepts without
recreating them as new Base primitives.

## Initial Terms

The initial Base Vocabulary defines exactly two terms.

| Local name | Absolute term IRI | Lifecycle |
| --- | --- | --- |
| `label` | `https://geesno.com/vocab/base/label` | `experimental` |
| `description` | `https://geesno.com/vocab/base/description` | `experimental` |

### label

`label` denotes a concise human-readable textual designation
associated with a semantic subject to help people recognize
or refer to that subject in context.

It does not establish:

- semantic identity or uniqueness;
- a filename;
- a required display or UI instruction;
- a localization system;
- a mandatory language;
- executable behavior.

### description

`description` denotes a human-readable declarative textual
explanation of a semantic subject's meaning, role, content
or relevant context.

It does not establish:

- a renderer instruction;
- a prompt or executable instruction;
- a required UI tooltip;
- proof of semantic truth;
- an authority claim;
- a mandatory field.

### Shared Term Boundaries

Both terms are ordinary Vocabulary terms.

They are not Core fields, mandatory Profile requirements or
automatically authorized Extension keys.

Neither initial term has an Extension-use declaration or
payload contract.

Their initial lifecycle state is `experimental`.

This reflects outstanding interoperability questions about
language, multiplicity, display interpretation and interaction
with Profiles.

Experimental lifecycle status does not remove established
term identity or create a compatibility guarantee.

## Candidate Evaluation

The following semantic ideas were evaluated when selecting
the deliberately small initial Base Vocabulary.

| Candidate | Outcome | Architectural reason |
| --- | --- | --- |
| Human-readable label | Accepted as `label` | Broadly applicable when separated from identity, UI behavior, localization and mandatory occurrence. |
| Human-readable description | Accepted as `description` | Broadly useful when separated from renderer instructions, prompts, truth claims and mandatory occurrence. |
| Category/type | Rejected from Base | Qualified Type Assertions already provide classification mechanics. |
| Containment / part-of | Deferred | Physical, logical, documentary, ownership and collection interpretations require more specific direction, transitivity and scope semantics. |
| Derived-from | Deferred to provenance-focused Vocabulary work | May collapse distinct source, evidence, provenance and derivation semantics. |
| Represents | Rejected from Base | Concept-Representation already has a dedicated Core assertion category. |
| Same-as / equivalent | Rejected from initial Base | Semantic equivalence, mappings and substitutability belong to the separate compatibility architecture. |
| Provenance/method descriptors | Deferred | Authorship, import, inference and curation distinctions need a coherent specialized Vocabulary. |
| Source/Binding descriptors | Deferred | Format, locator, revision, fingerprint and method meanings vary by source family. |
| Lifecycle/change descriptors | Rejected or deferred | Core already defines Revision, Change, Tombstone, Validity and supersession mechanics. |
| Review states | Deferred | Exact state definitions and transition policies belong to a specialized review Vocabulary or Profile. |
| Validity/scope qualifiers | Deferred | Applicability and completeness often depend on domain or Profile scope. |

The evaluated candidates do not justify new Core members,
Entity kinds, assertion categories, schema fields, adapters
or executable behavior.

## Cross-Domain Interoperability

The admitted terms were evaluated against semantic subjects
from engineering, tabular data, documents, source repositories,
scientific datasets and generic assets.

`label` and `description` remain broadly applicable to
objects, rows, columns, clauses, code symbols, observations
and products.

Neither term is required to function as an identifier,
mandatory field, UI instruction, prompt or authority claim.

Ideas such as `part-of` and `derived-from` recur across
domains but exhibit materially different semantics depending
on context.

Their broad occurrence alone does not justify admission
to a universal Base Vocabulary.

Review, Source and lifecycle descriptors likewise form
potentially useful specialized Vocabulary families.

## Adversarial Compatibility Cases

The following cases document the intended architectural
boundaries and expected treatment of Base Vocabulary use.

| # | Case | Expected treatment |
| --- | --- | --- |
| 1 | Term useful only in engineering | Reject from Base; use a domain Vocabulary or Profile. |
| 2 | Term useful only for AI/LLMs | Reject provider- or model-specific meaning. |
| 3 | Term duplicates a Core primitive | Reject. |
| 4 | Term aliases a Core field | Reject; no alternative serialization shortcut. |
| 5 | Term describes executable capability | Keep outside Base or describe inertly in a specialized Vocabulary; do not grant execution. |
| 6 | Generic term with Profile-specific constraints | Put the constraint in the Profile. |
| 7 | Useful in four domains but unnatural in two | Reject or defer until universality evidence is sufficient. |
| 8 | Meaning likely to evolve incompatibly | Defer; incompatible meaning requires a new term IRI. |
| 9 | No clear normative definition | Reject. |
| 10 | Requires network lookup | Reject that requirement; Base use remains offline-capable. |
| 11 | Base artifact unavailable | Bare-Core validity is unaffected; unavailable Base-aware interpretation must not be invented. |
| 12 | SemanticDocument uses no Base terms | Valid; Base membership is optional. |
| 13 | Third-party Vocabulary defines a similar term | Both may coexist; authority and preference remain external. |
| 14 | Base and third-party terms seem similar | No automatic semantic equivalence. |
| 15 | Term needs domain-specific constraints | Put them in a specialized Vocabulary or Profile. |
| 16 | Initial term later deprecated | Use a new edition-scoped lifecycle declaration under ADR-0019; preserve identity and history. |
| 17 | Later edition adds a Base term | Publish a new Vocabulary version under ADR-0017. |
| 18 | Same term IRI survives compatible evolution | Permitted when denoted meaning remains compatible. |
| 19 | Existing term receives incompatible meaning | Require a new Vocabulary version and new term IRI. |
| 20 | Preferred prefix or expansion metadata changes without semantic change | Identity and meaning remain unchanged; publication metadata may change under ADR-0018. |
| 21 | `geesno.com` unavailable or returns HTTP 404 | Semantic identity remains valid offline; no automatic fetch is required. |
| 22 | Future domain stewardship changes | Published identity is not automatically rewritten; governance remains subject to ADR-0021. |

These cases express the established architectural boundaries.
They do not introduce executable behavior or additional Core
conformance requirements.

## Extensions and Discovery

Base Vocabulary membership does not automatically authorize
a term as an Extension key.

ADR-0020 requires an edition-scoped Extension-use declaration
for Extension-aware assessment.

No Extension payload contract is defined for the two
initial Base terms.

Vocabulary discovery remains optional under ADR-0021.

The architecture does not require a global registry,
automatic network retrieval or runtime dereferencing.

## Cross-Vocabulary and Profile Compatibility

The abstract compatibility model is established separately
by [ADR-0023](../../adr/0023-cross-vocabulary-profile-compatibility-model.md).

The Base Vocabulary itself does not define:

- automatic semantic equivalence;
- cross-Vocabulary mappings;
- term substitutability;
- compatibility ranges;
- migration execution;
- composition resolution;
- Profile-to-Vocabulary compatibility enforcement.

The accepted compatibility architecture does not imply that
a machine-readable compatibility artifact has been published.

No additional Base terms follow automatically from that model.

## Publication Status

The Base Vocabulary family identity, initial edition,
admission policy and initial terms are architecturally
defined by ADR-0022.

The repository does not yet publish a machine-readable
Base Vocabulary artifact.

This documentation does not select a concrete publication
binding, establish a discovery service or create new
Profile requirements.

The Base Vocabulary remains optional, descriptive,
non-executable and independent of the universal Core.

## References

- [Vocabulary Overview](../README.md)
- [Architecture](../../ARCHITECTURE.md)
- [ADR-0017 through ADR-0023](../../adr/README.md)
- [ADR-0022 - GeesNO Base Vocabulary](../../adr/0022-geesno-base-vocabulary.md)
- [ADR-0023 - Cross-Vocabulary Compatibility](../../adr/0023-cross-vocabulary-profile-compatibility-model.md)
- [Public Preview](../../PUBLIC_PREVIEW.md)
