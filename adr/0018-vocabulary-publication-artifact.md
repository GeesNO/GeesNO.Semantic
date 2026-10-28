# ADR-0018: Vocabulary publication artifact and minimum metadata contract

- **Status:** Accepted
- **Date:** 2026-09-10
- **Accepted by:** Explicit human architecture decision on 2026-09-13
- **Decision order:** Second S3 architecture decision after accepted ADR-0017

## Context

Accepted ADR-0017 defines a stable Vocabulary identity and an immutable
Vocabulary edition identity:

```text
(Vocabulary identity, Vocabulary version)
```

It deliberately leaves publication artifacts, concrete serialization,
discovery, lifecycle, authority, integrity and the Base Vocabulary to later
decisions. S3 now needs the smallest interoperable publication contract that
lets independent implementations receive one edition, enumerate its terms and
obtain a normative definition for each term without proprietary software or
network access.

The publication contract must not become another SemanticDocument dialect or
change ADR-0010 term expansion. It must also preserve the ADR-0017 distinction
between semantic-edition equality and file, byte, URL or serialization
equality.

This ADR proposes the abstract publication model only. It does not create a
Vocabulary artifact, JSON schema, registry, discovery service or Base
Vocabulary.

## Prerequisite review

No additional architectural prerequisite blocks this decision:

1. Foundation already separates universal core, Vocabularies and profiles and
   requires domain-neutral, non-executable and offline-capable semantics.
2. ADR-0010 already defines absolute term identity and direct namespace
   expansion independently from Vocabulary metadata.
3. ADR-0015 already fixes closed S2 core, inert Extensions, version-role
   separation and the S2/S3 boundary.
4. ADR-0016 already fixes the S2 namespace map, qualified-term grammar,
   Layers 0–3 and the distinction between semantic and byte canonicality.
5. ADR-0017 now identifies the exact Vocabulary edition that an artifact
   represents and makes its normative semantic content immutable.

Publication serialization, lifecycle, Extension compatibility, discovery,
authority, Base Vocabulary admission and cross-vocabulary compatibility are
downstream decisions, not prerequisites to the abstract minimum below.

## Requirements

The model must:

- represent exactly one immutable Vocabulary edition per publication artifact;
- carry the complete minimum normative content needed to process that edition
  offline;
- identify the Vocabulary and exact version using ADR-0017;
- enumerate edition membership explicitly rather than relying on discovery or
  inference from an IRI namespace;
- give every published term a normative semantic definition rather than only
  an opaque IRI or label;
- permit useful publication/authoring namespace metadata without making a
  preferred base/local decomposition Vocabulary identity, term identity,
  denoted meaning or a restriction on SemanticDocuments;
- permit one Vocabulary edition to publish more than one expansion base and
  equivalent artifacts to prefer different valid decompositions without
  creating more than one identity or meaning for a term;
- avoid a mandatory closed taxonomy of term roles that cannot cover future
  qualified uses;
- distinguish normative edition content from editorial/documentation metadata;
- permit equivalent artifacts, locations and serializations for one edition;
- require no network, registry, dereference, official service, proprietary
  software or GeesNO SDK;
- treat all artifact content as untrusted inert data; and
- remain domain-, vendor-, format-, software- and AI-provider-neutral.

## Distinctions that remain controlling

```text
Vocabulary identity
!= Vocabulary edition identity
!= namespace expansion base
!= term identity
!= publication artifact identity
!= retrieval location
!= discovery alias
!= profile identity/version
!= SemanticDocument spec_version
```

A publication artifact states which edition it represents. It does not become
the edition, own the term identities or authorize dereference of any IRI.

The following term-level roles are also separate:

```text
term IRI
!= term membership
!= term denoted meaning
!= normative definition representation
!= publication namespace/decomposition metadata
!= editorial documentation
```

In particular:

```text
publication-declared decomposition
!= term identity
!= denoted semantic meaning
!= document prefix
```

Nor does publication metadata select one SemanticDocument lexical contract:

```text
Vocabulary publication decomposition
!= compatibility with one SemanticDocument spec_version

Vocabulary version
!= SemanticDocument spec_version
```

## Alternatives

### Alternative A — Embed Vocabulary publication in SemanticDocument

This would add Vocabulary records or metadata to the frozen S2 namespace map
or another closed core object. It would make bare-core conformance depend on an
S3 concern and create a second route for term semantics.

This alternative is rejected because it contradicts ADR-0015/0016 and would
reopen S2.

### Alternative B — Freeze one JSON manifest as the abstract model

One JSON shape would be straightforward to implement, but choosing member
names, collection shapes, format dispatch and schema mechanics here would make
serialization convenience define the abstract publication semantics. It would
also make equivalent future serializations appear secondary or incompatible.

This alternative is rejected for D2. A later binding may select JSON as the
initial reference serialization after the abstract contract is accepted.

### Alternative C — Abstract minimum with equivalent serialization bindings

Define one serialization-independent publication model with an exact edition
pair, explicit term membership and one required normative definition component
per term. It may also carry explicitly separated publication/authoring
namespace metadata. Concrete bindings must represent those roles without
changing their semantics. Several artifacts or serializations may represent
the same edition when their normative semantic content is the same, even when
their publication decomposition metadata differs.

This alternative is proposed. It supplies an interoperable minimum while
leaving byte identity, format details and integrity evidence out of D2.

### Alternative D — Dereference Vocabulary identity or use a registry

Treating the Vocabulary IRI as a required URL, or requiring a registry to
locate its current publication, would collapse identity into location and make
offline conformance dependent on infrastructure and authority policy.

This alternative is rejected. Discovery remains optional later S3 work.

### Alternative E — Identify the edition by one artifact hash

A hash can identify particular bytes or canonical content under a selected
algorithm, but ADR-0017 permits different serializations and artifacts for one
semantic edition. No signature, canonical-byte or threat model is accepted.

This alternative is rejected as the abstract edition/publication identity.
Fingerprints and signatures remain later integrity work.

## Proposed decision

### Publication artifact

1. A **Vocabulary publication artifact** is a finite, inert representation of
   exactly one Vocabulary edition under this abstract contract.
2. The artifact is self-contained for the required minimum normative content.
   Optional links may point to additional documentation, but processing the
   minimum contract never requires following them.
3. A publication artifact is not a SemanticDocument, profile, registry entry,
   package-manager object, executable module or authority proof.
4. D2 assigns no universal semantic identity to the artifact itself. A file
   name, URL, mirror location, media type, byte sequence, fingerprint or
   signature is not the ADR-0017 edition identity.

### Minimum edition metadata

Every conforming publication artifact represents one edition and carries:

1. the absolute **Vocabulary identity** accepted by ADR-0017;
2. the non-empty exact **Vocabulary version** accepted by ADR-0017;
3. a non-empty finite set of **term definitions** belonging to that edition.

The first two components form the immutable Vocabulary edition identity.
Term membership and the meaning denoted by each member are normative semantic
edition content; neither is inferred from Vocabulary identity, retrieval
location, prefix spelling, namespace shape or registry data.

Collection order is not semantic. Vocabulary identity occurs once, version
occurs once, and each absolute term IRI occurs at most once in an edition
artifact.

### Namespace bases and term identity

An artifact MAY declare a finite set of distinct absolute namespace expansion
bases as publication/authoring metadata. This supports producers that want
recommended compact authoring mechanics and Vocabularies whose terms are
organized under distinct controlled IRI stems without pretending that any
stem is the Vocabulary identity. The set is not required by the abstract
minimum because an absolute term IRI is already complete term identity.

For a term, an artifact MAY declare at most one **preferred publication
decomposition**:

```text
declared expansion base + exact local component = absolute term IRI
```

When present, the base MUST be one declared by the artifact and direct
concatenation MUST produce the term IRI exactly. No separator or normalization
is inserted. The declared local component MUST be present and non-empty under
the future binding's deterministic representation. D2 defines no universal
local-component regex and does not import the lexical grammar of any one
SemanticDocument specification version into the abstract Vocabulary model.

The full absolute term IRI remains term identity. The decomposition only
records a publication preference for reaching that IRI through direct
expansion. It is a preferred authoring/interoperability hint, not a canonical
term spelling, a second identity, an alias declaration or part of the term's
denoted meaning. The zero-or-one rule only prevents one artifact from making
competing preferred recommendations for the same term. Different terms in the
same Vocabulary may use different declared bases.

A SemanticDocument or another implementation remains free to use any
ADR-0010-valid prefix, expansion base and local component whose direct
expansion produces exactly the same absolute term IRI. It is not invalid or
non-conforming merely because that decomposition differs from the publication
preference. A document-local prefix remains only a local alias under
ADR-0010.

Publication bases and preferred decompositions are **normative
publication/authoring metadata**: when present, their shape, uniqueness,
reference and exact-concatenation relationships are mechanically binding.
They are nevertheless separate from normative semantic edition content.
Changing only this metadata does not change term membership, term identity or
denoted meaning and therefore does not by itself require a new Vocabulary
version. Two valid base/local pairs may produce exactly the same absolute term
IRI; neither pair becomes more identity-significant because an artifact
prefers it.

For example, both pairs below directly produce the same term identity:

```text
https://example.org/ns/  + term
https://example.org/ns/t + erm
    -> https://example.org/ns/term
```

Whether a preferred publication decomposition can be used directly in a
particular SemanticDocument is a compatibility question for that document's
applicable specification contract. Under `spec_version: "0.1.0"`, the chosen
document-local prefix and local component MUST satisfy ADR-0016's S2 0.1
lexical rules, and its namespace expansion MUST satisfy ADR-0010/0016. Failure
to meet those version-specific lexical rules makes that decomposition
unavailable for direct use under that contract; it does not change the
Vocabulary edition, Vocabulary version, term identity, membership or denoted
meaning. D2 does not define a general compatibility-declaration system for
Vocabulary artifacts and present or future `spec_version` contracts.

### Minimum term definition

Every term definition requires the following universal minimum:

1. the term's absolute IRI identity;
2. one non-empty **normative definition component** that the publisher
   declares to be the normative definition of that term in this Vocabulary
   edition.

The normative definition component is a finite, inert representation of the
publisher's definition, associated unambiguously with the term. It is not
replaced by a label, comment, example or discovery link. A generic processor
must be able to associate it with the term, preserve it and expose or present
it without proprietary software. The exact representation and deterministic
non-empty shape belong to the later publication binding; absence or a
binding-defined empty representation is mechanically invalid.

The component's required presence and shape do not make generic conformance a
test of semantic prose. A generic processor is not required or authorized by
D2 to understand the domain meaning, prove that the definition is sufficiently
precise or differentiating, decide whether it is true or correct, establish
semantic equivalence with another formulation, or infer formal logic from it.
A non-empty but vague definition may therefore satisfy generic mechanical
conformance while remaining semantically poor. Definition quality, clarity,
adequacy and correctness are publisher/governance responsibilities unless a
later Vocabulary or profile rule supplies an additional deterministic
contract. Generic publication conformance depends only on deterministic
conditions defined by this abstract contract and its accepted concrete
binding; it never requires human or LLM interpretation.

D2 does not require one formal ontology language, natural language,
translation model or executable interpretation. Exact serialization,
definition representation, language metadata, multilingual documentation and
optional formal-semantics mappings remain subordinate decisions.

This minimum deliberately does not require:

- label, description, comment, language tag or example;
- experimental/deprecated/retired status or replacement;
- datatype, domain, range, cardinality or inference rules; or
- one closed term `kind` or exactly one usage role.

GeesNO.Semantic uses qualified terms in several roles, and one term may be
meaningful in more than one role. The occurrence slot in a SemanticDocument
continues to provide its core structural role. Optional machine-readable role,
constraint or formal-semantics declarations require later accepted Vocabulary
or profile conventions; D2 does not invent a universal taxonomy for them.

### Normative and editorial content

The publication contract distinguishes three layers.

The **normative semantic edition content** consists of:

- the exact edition term-membership set;
- each member's absolute term IRI; and
- the denoted meaning that the publisher expresses through the required
  normative definition component.

The Vocabulary identity and version pair identifies that immutable semantic
edition. The required definition component is its publisher-declared normative
representation of a term's meaning; the representation remains distinct from
the meaning it expresses.

The **normative publication/authoring metadata** consists, when present, of
the declared expansion-base set and preferred base/local decompositions. Its
deterministic constraints are conformance requirements for the artifact, but
it does not become semantic edition identity or denoted semantic content.

Adding or removing a normative term or changing a term's denoted meaning
changes normative edition content and therefore requires a new Vocabulary
version under ADR-0017. An incompatible change to a term's denoted meaning
also requires a new term IRI. Changing only publication bases or preferred
decompositions does neither.

Publisher display name, human labels, non-normative descriptions/comments,
translations, examples, authorship notes, publication dates, formatting,
mirrors, retrieval links and equivalent documentation are editorial metadata
under this minimum contract. They may change without a new Vocabulary version
when they do not change normative semantic content. They are not a second
normative definition source. Any apparent semantic contradiction is a
publisher/governance quality issue rather than a generic mechanical failure
unless a later deterministic contract defines an applicable check.

Different normative definition representations may retain the edition pair
only when the publisher claims that they express the same denoted meaning.
D2 provides no algorithm for proving that semantic equivalence; disagreement
about it is a publisher/governance issue, not generic mechanical conformance.

### Artifact and edition equality

Several files, serializations, mirrors or locations may represent the same
Vocabulary edition. They need not have equal bytes, member order, formatting,
media type, URL, publication bases, preferred decompositions or textual
definition formulation. Each must carry the same edition pair, term membership,
absolute term IRIs and denoted meanings under the abstract model. Distinct
decomposition metadata alone never makes two semantic editions.

Two artifacts that claim the same edition pair but differ in normative
semantic content are conflicting publication claims and violate ADR-0017
edition immutability. Neither a later timestamp nor a preferred URL silently
reassigns the pair. D2 does not define a fingerprint, signature, canonical
byte form or automatic proof that detects the conflict. Generic mechanical
validation can compare deterministic fields but cannot prove whether different
definition representations express the same meaning.

### Serialization boundary

The abstract model above is normative for D2. A concrete publication binding
must later define:

- its media/format identification and exact binding version;
- one unambiguous representation for every required component;
- deterministic validation, definition-presence/shape and duplicate handling;
- Unicode, member/collection and resource-limit processing; and
- how optional publication/authoring and editorial metadata are distinguished
  from required semantic components.

That binding version remains distinct from Vocabulary version,
SemanticDocument `spec_version` and profile version. A JSON binding must be a
separate Vocabulary-publication contract and MUST NOT modify the S2
SemanticDocument schema or `namespaces` map.

Equivalent bindings represent the same abstract edition; they do not create
format-specific term identities or alternate normative meanings.

### Offline and unavailable-publication behavior

Given a publication artifact, a generic processor can offline:

- identify the Vocabulary and exact edition;
- enumerate its terms and any declared namespace bases;
- validate each declared base/local/term-IRI relationship mechanically;
- validate deterministic presence and shape of each required definition;
- associate, expose and preserve every normative definition component; and
- distinguish semantic content from publication/authoring and editorial
  metadata.

It need not understand the domain meaning, judge definition adequacy, prove
semantic equivalence, accept the publisher's authority or infer compatibility
with another edition or profile.

When no publication artifact is available, ADR-0010/0015/0016 continue to
allow bare-core parsing, expansion and comparison of qualified terms from the
SemanticDocument namespace map. A Vocabulary-aware operation may report that
definitions are unavailable, but it must not invent them, dereference an IRI
automatically or retroactively invalidate otherwise conforming S2 bare core.

### Security boundary

Publication artifacts and every contained IRI or string are untrusted inert
data. They cannot:

- execute code, scripts, macros, queries, commands or tool calls;
- grant permissions, credentials, authority or conformance;
- activate plugins, adapters, agents, RAG or model routing;
- require network, filesystem or IRI dereference;
- override S2 core semantics or loosen validation; or
- introduce a GeesNO.Core dependency.

Text resembling instructions and URLs resembling API endpoints remain data.
Concrete processors apply bounded parsing and resource controls under the
future serialization binding.

## Interoperability consequences

- A publisher can distribute one edition locally, bundled, cached, mirrored
  or through independently chosen transports.
- Independent consumers receive one exact edition pair and a minimum semantic
  definition component for every enumerated term.
- Namespace mechanics may be published explicitly as preferred authoring
  metadata while remaining separate from Vocabulary identity, term identity
  and denoted meaning.
- Multiple expansion bases and different valid artifact preferences are
  supported without requiring multiple Vocabulary or term identities.
- Mechanical conformance stays deterministic; semantic-definition quality is
  not delegated to an LLM or subjective generic validator.
- Term-role taxonomies, inference rules and domain constraints do not leak
  into the universal publication minimum.
- Missing publication affects Vocabulary-aware interpretation, not S2
  bare-core validity.

## Cross-domain validation

| Domain | Publication stress case | Result under the proposal |
| --- | --- | --- |
| Engineering-like object graph | A standards body publishes component classifications under two controlled term stems. | One artifact can declare both bases and preferred decompositions; each term still has one full IRI and required definition without CAD/BIM core fields. |
| Spreadsheet/table | A company bundles business terms with an offline workbook consumer. | The local artifact supplies exact edition and definitions; no network, spreadsheet adapter or registry is required. |
| Technical/legal document | A legal terminology publication supplies publisher-declared normative definitions and separate translated labels. | Required definition presence is deterministic; semantic adequacy remains governance, labels/translations may remain editorial and jurisdiction is not a universal field. |
| Source-code repository | A community publishes analysis predicates in JSON and another equivalent representation. | Both artifacts may represent one edition; repository hosting and format do not become identity or Git semantics. |
| Scientific dataset | A discipline adds a newly defined term while retaining compatible established term IRIs. | The new term requires a new Vocabulary version; unchanged term IRIs remain stable. |
| Generic product/asset dataset | A vendor and an independent community publish unrelated `category` terms. | Distinct Vocabulary/base/term IRIs coexist; the publication contract assigns neither authority nor equivalence. |

All six domains use the same minimum. None requires a domain-specific term
class, application adapter, network service or executable primitive.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| Same edition published as JSON and another equivalent representation | Valid when both map to the same normative abstract content; serialization equality is not edition equality. |
| Same edition available at two URLs | Valid; the URLs are retrieval locations and do not participate in edition identity. |
| Artifact moved | Vocabulary, edition and term identities remain unchanged; optional discovery metadata may change later. |
| Unknown Vocabulary with a local artifact | Generic offline processing can enumerate bases/terms and expose definitions; availability does not prove authority or profile compatibility. |
| Known Vocabulary but artifact unavailable | S2 bare core remains processable; Vocabulary-aware meaning is unavailable and must not be invented or fetched automatically. |
| One term IRI belongs to several editions of one Vocabulary | Valid when explicitly included and its denoted meaning remains compatible across those editions. |
| New edition adds terms while retaining earlier term IRIs | Required new Vocabulary version; compatible existing term IRIs remain unchanged. |
| Editorial publication metadata changes | Same edition may be republished when normative semantic content is unchanged. |
| Normative content changes without changing the edition pair | Invalid conflicting publication claim under ADR-0017; D2 defines no cryptographic detection mechanism. |
| Same term IRI reached through two valid `base + local` decompositions | Valid; the absolute term IRI is the same identity. Neither decomposition is denoted meaning or a second identity. |
| Two artifacts for one edition choose different preferred publication decompositions | They may represent the same semantic edition when edition pair, membership, term IRIs and denoted meanings are unchanged; each declared decomposition must independently pass deterministic checks. |
| Same term IRI and meaning with different document-local prefix/base mechanics | Valid under ADR-0010 when each document expands exactly to that IRI; publication preference does not constrain the documents. |
| A future GeesNO.Semantic specification admits a qualified-local lexical form that S2 `0.1.0` rejects | The same Vocabulary identity/version, membership, term IRI and denoted meaning remain the same edition; no new Vocabulary version or term identity is required. Direct use of that decomposition depends on the applicable SemanticDocument specification contract. |
| Empty normative definition component | Mechanically invalid: every term requires a present, binding-defined non-empty component. |
| Non-empty but vague definition prose | May be mechanically valid when its deterministic shape is valid; possible low semantic quality does not make generic conformance subjective. |
| Two human reviewers disagree about definition quality | No effect on generic mechanical conformance; adequacy is publisher/governance responsibility unless a later deterministic rule applies. |
| Two different textual formulations are claimed to express the same denoted meaning | They may represent the same edition under the publisher's claim; a generic validator preserves them but neither proves nor invents semantic equivalence. |
| A later binding carries explicit language metadata for a definition | Permitted when that binding defines it deterministically; language representation remains separate from term identity and exact rules are deferred. |
| Two independent publishers | Distinct controlled Vocabulary IRIs coexist. If both claim one Vocabulary IRI, D2 does not resolve authority; that is D5. |
| Expansion base differs from Vocabulary identity | Valid and expected; the artifact declares the relationship explicitly without equating them. |
| One Vocabulary edition publishes several expansion bases | Valid optional authoring metadata; a term may have zero or one preferred decomposition in that artifact. |
| Terms are used in different semantic roles | Valid; term identity is unchanged and D2 imposes no single closed role class. Later Vocabulary/profile rules may add role constraints. |
| Malicious instruction-like text occurs inside a definition | Mechanically treated as inert untrusted definition data; no execution, permission, plugin activation, LLM instruction status or automatic dereference occurs. |

## Consequences

- D2 gains a serialization-independent semantic publication minimum rather
  than a JSON-driven Vocabulary dialect.
- A publication is more than an IRI inventory because every term requires a
  non-empty publisher-declared normative definition component.
- Optional preferred namespace decomposition assists SemanticDocument authors
  without modifying any namespace map; direct usability is decided by the
  applicable `spec_version` lexical contract.
- Editorial flexibility is preserved without weakening immutable edition
  content.
- Concrete serialization, lifecycle, trust, discovery and compatibility work
  remain visible rather than being silently decided by one manifest shape.
- Producers bear the cost of explicit term membership and definitions.
- Generic consumers can preserve and present definitions but cannot judge
  their semantic quality or infer domain logic, authority or compatibility
  that the artifact does not state.

## Remains open

- concrete publication serialization, media type, binding version, schema and
  canonical member names;
- exact representation of the normative definition component, optional
  language tagging, multilingual documentation and formal-semantics mappings;
- deterministic binding rules for an empty versus non-empty definition
  representation;
- optional labels, descriptions, comments, examples and publisher metadata;
- machine-readable term-role/applicability and domain/range/datatype
  constraint conventions;
- D3 experimental, stable, deprecated and retired Vocabulary/term lifecycle;
- D4 Extension vocabulary authoring and payload-compatibility conventions;
- D5 optional discovery, moving aliases, authority, trust and governance;
- D6 GeesNO Base Vocabulary identity, bases, admission criteria and term set;
- D7 cross-vocabulary mappings, equivalence and profile compatibility;
- edition dependency, compatibility and migration declarations;
- fingerprints, signatures, artifact identity, semantic-equivalence proof,
  byte/cryptographic canonicalization and integrity threat model;
- registry/package protocol, HTTP/API behavior and public release process; and
- future SemanticDocument-specification internationalized qualified-local
  grammar, separate from the abstract D2 publication decomposition.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-13. Acceptance covers the one-edition finite inert
publication model, required membership and normative definition component,
optional publication/authoring decomposition, separation from term identity
and SemanticDocument lexical contracts, deterministic conformance boundary,
offline behavior and equivalent-artifact rules recorded above.

Acceptance closes D2 and authorizes analysis of D3. It does not itself choose
a concrete serialization/schema, implement a Vocabulary artifact, define
lifecycle, create a registry or Base Vocabulary, or authorize any D4–D7, S4 or
SDK work.
