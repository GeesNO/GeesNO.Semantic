# ADR-0017: Vocabulary identity and version model

- **Status:** Accepted
- **Date:** 2026-09-10
- **Accepted by:** Explicit human architecture decision on 2026-09-10
- **Decision order:** First S3 architecture decision after S2 closure

## Context

S2 is complete. Accepted ADR-0010 lets a document expand every compact
qualified term to one absolute term IRI, while explicitly separating:

```text
namespace expansion base
!= Vocabulary identity
!= Vocabulary version
```

Accepted ADR-0015 also separates these concepts from `spec_version` and from
profile identity/version. ADR-0016 freezes the S2 namespace map as
`prefix -> expansion-base string`; it intentionally does not add Vocabulary
metadata to that map.

S3 must later define publication, discovery, experimental/deprecation
lifecycle, Extension vocabulary conventions, cross-vocabulary behavior and a
small Base Vocabulary. Each depends on being able to identify a Vocabulary and
one of its editions without confusing either with term expansion or retrieval.

This ADR addresses only that prerequisite. It does not define a JSON
Vocabulary manifest, publish terms, create a registry or change the S2 schema.

## Requirements

The model must:

- identify a conceptual Vocabulary independently from its human name,
  namespace prefix, expansion base and publication location;
- identify a particular Vocabulary edition deterministically and keep that
  edition identity stable and immutable after publication;
- prevent one edition identity from being reassigned to different normative
  semantic content, including an additive term release;
- preserve the ADR-0010 rule that expanded absolute term IRI is term identity;
- prevent version metadata from silently changing the identity or meaning of a
  term;
- work for GeesNO, standards bodies, vendors, organizations and individuals
  without a central allocation service;
- support unknown, unavailable, moved, experimental and deprecated
  vocabularies without making bare-core parsing depend on discovery;
- keep Vocabulary, profile and GeesNO.Semantic specification versions separate;
- keep edition identity, discovery aliases, publication artifacts and
  retrieval locations separate;
- avoid assuming that every Vocabulary uses Semantic Versioning;
- allow deterministic offline comparison;
- remain descriptive, inert and independent from GeesNO.Core; and
- introduce no domain-specific primitive or application adapter.

## Inherited constraints

1. Foundation keeps core mechanics, vocabularies and profiles separate and
   prohibits a giant universal ontology.
2. ADR-0009 supplies absolute IRI syntax and exact comparison principles but a
   Vocabulary identity is not a SemanticDocument record identity.
3. ADR-0010 fixes qualified-term expansion and states that prefix spelling,
   Vocabulary metadata and definition availability do not alter term equality.
4. ADR-0015 fixes closed core, inert Extensions, no core override, no automatic
   dereference and independent specification/profile/Vocabulary version roles.
5. ADR-0016 fixes the S2 JSON contract, exact `spec_version: "0.1.0"`, offline
   Layers 0–3 and the absence of Vocabulary metadata from the namespace map.
6. S2 closure does not authorize a schema change, public release, registry,
   profile implementation or SDK.

## Alternatives

### Alternative A — Expansion base is Vocabulary identity and version

Every expansion base would identify one Vocabulary edition. A new release
would normally mint a new base and therefore new term IRIs.

This is simple but collapses concepts ADR-0010 deliberately separated. Even an
editorial or additive release would change every term identity, while a moved
publication could appear to create a new Vocabulary. This alternative is not
recommended.

### Alternative B — One mutable, unversioned Vocabulary identity

One stable IRI would identify the Vocabulary and whatever its current content
happens to be. Consumers could not cite or compare exact editions, reproduce a
profile dependency or distinguish compatible clarification from incompatible
redefinition. Offline data could change meaning when the publisher updates a
remote resource. This alternative is not recommended.

### Alternative C — Stable Vocabulary identity plus exact edition token

One absolute IRI identifies the Vocabulary across editions. A non-empty exact
token identifies an edition within that Vocabulary. The pair is the
versioned-edition identity:

```text
(Vocabulary identity IRI, exact version token)
```

The version token is compared exactly. Its publisher may use SemVer, a date,
an edition number or another documented scheme; generic GeesNO.Semantic
processing infers no ordering or compatibility from its spelling.

Once published, that edition pair is immutable: it cannot later identify
different normative semantic content. A change to the normative semantic
content of the edition, including the addition of a normative term, requires a
new version token. This is semantic-edition identity, not byte or artifact
identity.

Term identity remains the ADR-0010 expanded absolute term IRI. Version
metadata describes the edition in which terms are defined; it is not a hidden
operand in term expansion. This alternative is selected.

### Alternative D — Content hash is Vocabulary or edition identity

Content addressing proves equality of one byte or canonical artifact, but S3
has no accepted byte canonicalization, signature model or single publication
serialization. Editorially equivalent artifacts could hash differently, and
moving between representations would manufacture new semantic identities.
Fingerprints may later support integrity metadata but are not the abstract
Vocabulary identity. This alternative is not recommended.

## Decision

1. A **Vocabulary identity** is a stable absolute IRI controlled or delegated
   by its publisher. It identifies the conceptual Vocabulary across editions.
2. Vocabulary identity is compared by the accepted exact IRI comparison
   discipline. Human label, preferred prefix, expansion base, network location
   and registry entry do not participate in equality.
3. A **Vocabulary version** is one non-empty exact token scoped to its
   Vocabulary identity. Generic processors compare it as an opaque exact
   token and infer no case folding, whitespace trimming, Unicode
   normalization, other generic normalization, ordering, range or
   compatibility. This ADR does not define its serialization grammar.
4. A specific **Vocabulary edition identity** is the ordered pair
   `(Vocabulary identity, Vocabulary version)`. It is stable and immutable.
   Once that pair has been published as an edition, the publisher MUST NOT
   reassign it to an edition with different normative semantic content.
5. A reference to Vocabulary identity alone identifies the Vocabulary family,
   not a reproducible edition. A future claim requiring one exact edition must
   carry both components under the publication/declaration design still to be
   decided.
6. Vocabulary edition identity, discovery alias, publication artifact and
   retrieval location are distinct. A moving alias such as `latest`,
   `current` or `stable` cannot serve as Vocabulary edition identity while its
   referent can change. If any such string is used literally as a Vocabulary
   version token, it behaves exactly like every other token: it is permanently
   bound to that edition and MUST NOT be repointed. Any future moving aliases
   belong to publication/discovery metadata.

   ```text
   Vocabulary edition identity
   != discovery alias
   != publication artifact
   != retrieval location
   ```

7. A namespace expansion base remains only the mechanical stem used to form
   absolute term IRIs. It may equal a Vocabulary identity by publisher choice,
   but equality is never assumed and the relationship is not one-to-one by
   universal rule.
8. An expanded absolute term IRI remains the identity of that term across
   documents and Vocabulary editions. A version token never changes it
   implicitly.
9. Every change to an edition's normative semantic content,
   including the addition of a new normative term, requires a new Vocabulary
   version. A change that is purely editorial and does not change normative
   semantic content does not require a new edition identity.
10. A new Vocabulary version does not by itself require new term IRIs.
    Existing term IRIs may remain stable when their denoted meanings remain
    compatible.
11. An incompatible change to one term's denoted meaning requires a new term
    IRI. Changing only Vocabulary version cannot fork one term identity into
    two incompatible meanings.
12. Byte identity and publication-artifact identity are not edition identity.
    Different serializations, mirrors, retrieval locations, formatting or
    purely editorial revisions may represent the same edition when they do not
    change its normative semantic content. Fingerprints, signatures, artifact
    identity and mechanisms for detecting conflicting claims remain later
    decisions.
13. Unknown or unavailable Vocabulary metadata never invalidates otherwise
    conforming S2 bare core. Vocabulary-aware/profile conformance may report a
    separate unsupported, unavailable or incompatible result under later
    accepted rules.
14. No network dereference, central registry or official GeesNO service is
    required to parse, preserve, expand or compare S2 qualified terms.
15. The GeesNO Base Vocabulary uses the same identity/version rules as an
    independently published Vocabulary; it gains no hidden core semantics.

The exact serialization and placement of Vocabulary identity/version metadata
remain subordinate S3 decisions. This ADR does not add them to the S2
`namespaces` map or any closed core object.

## Interoperability consequences

- Different documents may use different prefixes for the same expansion base
  and still compare terms by expanded IRI.
- Two Vocabulary editions can share term mechanics without making version an
  invisible component of each term identity.
- Independent publishers avoid Vocabulary-identity collisions by controlling
  distinct absolute IRIs; no global prefix assignment is needed.
- A consumer can preserve and compare identifiers offline even when it cannot
  interpret the Vocabulary.
- Reproducible Vocabulary-aware processing can cite an exact edition pair,
  while bare S2 processing remains independent of Vocabulary metadata.
- Claims that two Vocabularies or terms are equivalent require explicit future
  vocabulary/profile semantics; similar names or bases do not prove it.

## Versioning consequences

- `spec_version` continues to select the GeesNO.Semantic serialization
  contract and remains `0.1.0` for the completed S2 baseline.
- Project/repository version remains `0.1.0-dev`; it is not Vocabulary version.
- Profile identity/version remains the separate S2 `profile` + `version` role.
- Vocabulary version tokens are exact and Vocabulary-scoped. Generic consumers
  do not interpret SemVer ranges, dates, precedence or compatibility and apply
  no generic normalization.
- A publisher may document a version scheme, but compatibility declarations
  and migrations require later S3 decisions.
- Any change to an edition's normative semantic content, including adding a
  normative term, requires a new Vocabulary version. Existing compatible terms
  need not receive new term IRIs in that new edition.
- A literal version token such as `latest`, `current` or `stable` is immutable
  once published. A repointable alias is discovery/publication metadata, not a
  Vocabulary version or edition identity.
- Reusing an edition pair for any different normative semantic content is
  invalid publication governance, whether the change is compatible, additive
  or incompatible.
- Multiple artifacts may represent the same edition when their normative
  semantic content is unchanged; edition identity therefore makes no byte
  identity or artifact identity claim.
- Fingerprints, signatures and content hashes may later identify artifacts;
  they do not replace Vocabulary or edition identity.

## Extension consequences

- ADR-0015 Extension hosts, qualified keys and arbitrary inert payloads remain
  unchanged.
- An Extension key continues to be identified by its expanded term IRI, not by
  Vocabulary version metadata.
- An Extension vocabulary can publish edition metadata under later S3 rules,
  but it cannot redefine core fields, loosen conformance or make its payload
  executable.
- An unknown Extension remains bare-core valid and preservable without loading
  its Vocabulary.
- Experimental/deprecated state and Extension compatibility are not encoded in
  prefixes, base IRIs or version spelling; later decisions must represent them
  explicitly.

## Cross-domain validation

| Domain | Stress case | Result under the decision |
| --- | --- | --- |
| Engineering-like object graph | Two organizations classify the same represented component with independently versioned terms. | Absolute Vocabulary and term IRIs avoid collisions; no CAD/BIM primitive enters core. |
| Spreadsheet/table | A workbook uses an internal business Vocabulary whose publication is unavailable offline. | Terms still expand and compare; exact edition metadata can be retained without fetching it. |
| Technical/legal document | A legal terminology edition deprecates a term but historical documents still cite it. | Stable term identity and separate edition/lifecycle metadata preserve citation without treating deprecation as deletion. |
| Source-code repository | A language-analysis Vocabulary moves from one hosting organization to another. | Publication location changes while Vocabulary, edition and term identities remain stable; no Git semantics are required. |
| Scientific dataset | A measurement Vocabulary issues an incompatible definition correction. | Version alone cannot silently change the old term; incompatible meaning requires a new term IRI. |
| Generic product/asset dataset | Supplier and community Vocabularies both define a local `category` term. | Distinct expansion bases/term IRIs coexist without a universal product ontology or preferred vendor. |

All six cases use one domain-neutral model and require no new core member,
Entity kind, Assertion category, adapter or execution primitive.

## Adversarial cases

| Case | Accepted classification |
| --- | --- |
| Same Vocabulary under different namespace prefixes | Same Vocabulary and terms when Vocabulary identity and expanded term IRIs match; prefixes are local aliases. |
| Same expansion base with different Vocabulary metadata | Term IRIs remain mechanically identical, but Vocabulary identities are distinct competing claims; no automatic equivalence or authority follows. |
| Different Vocabulary versions sharing namespace mechanics | Valid; stable term IRIs retain identity. Version metadata may affect later Vocabulary/profile compatibility but not S2 expansion. |
| Offline consumer | Can compare Vocabulary, edition-pair and term identities from supplied data; discovery is unnecessary. |
| Unknown Vocabulary | Bare core remains valid; meaning is unknown and no profile-conformance claim is inferred. |
| Vocabulary unavailable on network | No effect on identifier or bare-core validity; a Vocabulary-aware operation may report unavailable evidence. |
| Vocabulary renamed or moved | Label/location changes do not change stable Vocabulary identity or edition pair. |
| Experimental Vocabulary | Experimental status is separate lifecycle metadata to be designed later; it is not encoded by prefix or inferred from version spelling. |
| Deprecated Vocabulary | Deprecation does not erase identity or existing terms; replacement/migration rules remain a later lifecycle decision. |
| Two independent organizations defining Vocabularies | Distinct controlled absolute Vocabulary IRIs coexist without a central registry. Competing claims over one term base require explicit governance/trust handling. |
| Vocabulary version incompatible with a profile | Bare core remains separately valid. A later exact profile compatibility rule may reject or report the Vocabulary edition at Layer 4. |
| Same edition served from two URLs | Valid; both retrieval locations may expose the same immutable edition and neither URL participates in edition identity. |
| Same edition in two serializations | Valid when both carry the same normative semantic content; serialization and byte differences do not create a new edition. |
| Purely editorial correction | May retain the same edition pair when it changes no normative semantic content; changed bytes or formatting alone are not a new edition. |
| A new normative term is added to the Vocabulary | Requires a new Vocabulary version because the edition's normative semantic content changed, even when the addition is compatible. |
| Moving alias `latest`, `current` or `stable` | Not a Vocabulary edition identity; if its referent can change, it belongs to future publication/discovery metadata. |
| Literal version token `latest` | Valid only as an exact immutable edition token: once published for one edition, it cannot be repointed to another. Generic processing infers no moving-alias behavior. |
| New Vocabulary version with unchanged existing terms | Valid; existing term IRIs remain stable when their denoted meanings remain compatible. The new version identifies the changed edition, not renamed terms. |
| Incompatible change to a term's denoted meaning | Requires both a new Vocabulary version for the changed edition and a new term IRI for the incompatibly changed term. |
| Distinct artifacts claim the same edition pair but different normative content | Normative publication/governance violation: the immutable pair cannot identify both editions. This ADR does not define fingerprints, signatures or cryptographic detection. |

## Consequences

- S3 gains a stable subject for publication, discovery, lifecycle and
  compatibility decisions without reopening S2.
- Vocabulary family identity and exact edition identity are both expressible.
- An edition pair denotes immutable normative semantic content without being a
  byte or publication-artifact identifier.
- Term equality remains stable and serialization-independent.
- Additive normative evolution creates a new Vocabulary version while
  compatible existing term IRIs can remain stable.
- Publishers retain freedom to choose a version scheme, at the cost that
  generic consumers cannot infer order or compatibility from token spelling.
- Moving aliases cannot masquerade as reproducible edition identities.
- Incompatible term meaning changes require new term identities, reducing
  silent semantic drift.
- Availability, authority, trust and artifact integrity remain explicit future
  concerns rather than hidden effects of an IRI.
- No Base Vocabulary terms, registry, schema fields or SDK behavior are created
  by this decision.

## Remains open

- the machine-readable Vocabulary publication artifact and its media/storage
  forms;
- exact serialized names and placement for Vocabulary identity/version
  metadata outside the frozen S2 namespace map;
- minimum term-definition metadata, labels, language handling and documentation;
- declared version compatibility, dependencies and migration relationships;
- experimental, stable, deprecated and retired Vocabulary/term lifecycle;
- Extension vocabulary authoring and payload-conformance conventions;
- optional discovery catalogs, authority/trust and governance;
- GeesNO Base Vocabulary identity, preferred prefix, expansion base, admission
  criteria and initial term set;
- cross-vocabulary mapping/equivalence conventions;
- exact profile-to-Vocabulary compatibility declarations under future Layer 4;
- publication fingerprints, signatures and integrity threat model;
- optional moving discovery aliases and their publication metadata; and
- any future registry operation or public release process.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-10. The approval covers the stable Vocabulary identity,
the immutable ordered edition pair, the exact opaque version token, the
separation from term/artifact/location/alias identity, additive-edition
versioning and the new-term-IRI requirement for incompatible meaning changes.

The decision preserves every accepted S2 boundary, survives six unrelated
domains and classifies the required adversarial cases without network,
registry, domain or execution assumptions. It authorizes preparation of the
next S3 publication-contract decision, but does not itself publish a
Vocabulary artifact, create the Base Vocabulary or accept any downstream S3
decision.
