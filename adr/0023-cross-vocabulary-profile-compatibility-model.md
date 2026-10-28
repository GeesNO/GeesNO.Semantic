# ADR-0023: Cross-Vocabulary and profile compatibility model

- **Status:** Accepted
- **Accepted by:** Explicit human architecture decision on 2026-09-17
- **Date:** 2026-09-17
- **Decision order:** Seventh S3 architecture decision after accepted ADR-0022

## Context

S3 has accepted ADR-0017 through ADR-0022. Those decisions define exact
Vocabulary identity/version, abstract publication, lifecycle, Extension
Vocabulary authoring, optional discovery/authority/governance and the initial
GeesNO Base Vocabulary.

D7 is the remaining S3 architecture decision. It must define how GeesNO.Semantic
can describe relationships between terms, Vocabulary editions and profiles
without converting similarity into identity, version spelling into
compatibility, a mapping into an executable transform or a trust claim into
truth.

The central question is:

> How can GeesNO.Semantic represent explicit, reproducible compatibility,
> equivalence, mapping, substitution and profile-acceptance claims without a
> mandatory registry, resolver, reasoner, migration engine or AI matcher?

This ADR accepts only a serialization-independent abstract model. It does not
select JSON, RDF, OWL, SHACL, JSON-LD, a mapping language, a transformation DSL,
a registry API, a resolver API, a profile schema, S4 AI Context serialization,
conformance fixtures, SDK code or any execution behavior.

## Prerequisite review

No unresolved prerequisite blocks a D7 proposal:

1. Foundation requires a universal, descriptive, offline-capable, software-,
   format-, domain- and AI-provider-neutral standard with no execution runtime.
2. ADR-0017 supplies exact Vocabulary family and edition identities, exact
   opaque version tokens and stable absolute term IRIs.
3. ADR-0018 supplies explicit edition membership and normative definitions
   without selecting a concrete publication binding.
4. ADR-0019 supplies lifecycle declarations while keeping lifecycle separate
   from compatibility, migration, validity and automatic replacement.
5. ADR-0020 supplies exact-edition Extension-aware payload assessment and keeps
   payload compatibility separate from semantic equivalence and profile
   conformance.
6. ADR-0021 supplies optional attributed discovery/authority/trust evidence and
   preserves conflicting claims without selecting a universal winner.
7. ADR-0022 supplies the GeesNO Base Vocabulary as an ordinary Vocabulary with
   no special compatibility priority.

D7 does not require S4 profile serialization. A profile-related compatibility
claim can be defined abstractly as a finite inert claim involving an exact
profile identity/version or another reproducible profile requirement-set
identifier supplied by a future profile binding. D7 does not define that
profile binding, AI Context Profile, profile schema, profile conformance result
format or profile declaration syntax.

Concrete profile serialization is therefore deferred, not a blocker for the
abstract D7 compatibility model. A D7 claim that cannot identify the relevant
profile or requirement set exactly is not reproducible enough for generic D7
processing.

## Controlling distinctions

```text
identity
!= equivalence
!= compatibility
!= similarity
!= mapping
!= substitutability
!= migration

same spelling
!= same meaning

same local name
!= same term

same prefix
!= same Vocabulary

same domain
!= same meaning

same version token
!= compatibility

higher-looking version
!= newer
!= better
!= replacement
!= compatible

newer edition claim
!= compatible edition

shared term IRI
!= whole-edition compatibility

mapping description
!= executable transformation

migration description
!= migration execution

compatibility claim
!= conformance
!= trust
!= truth

equivalence claim
!= proof of equivalence

profile requirement
!= Vocabulary meaning

Vocabulary compatibility
!= profile conformance

semantic equivalence
!= payload-contract compatibility

Base Vocabulary term
!= preferred term
!= winning term
```

## Alternatives

### Alternative A - Infer compatibility from identity, version or structure

A generic processor could infer compatibility from same term IRI, additive
membership, SemVer-looking versions, lifecycle state, same prefix, same host or
similar local names. This is rejected. None of those facts is universally safe
across independent publishers, closed profiles, Extension payload contracts or
conflicting governance.

### Alternative B - One generic `compatible: true` relation

One boolean would be compact but ambiguous. It would hide whether the claim is
about denoted term meaning, edition membership, Extension payload acceptance,
profile acceptability, migration guidance or contextual substitutability. This
is rejected.

### Alternative C - Normative ontology/reasoner/mapping engine

D7 could define transitive closure, ontology alignment, mapping execution,
constraint comparison or AI matching. This would introduce mandatory reasoning,
technology choices and potentially executable behavior. It is rejected.

### Alternative D - Finite attributed compatibility claims

Define a small set of relation kinds, exact subjects/targets, explicit scope
and attributed finite claims. Generic processing checks only deterministic
shape, preserves conflicts and infers no unstated truth, order, trust,
transitivity, payload compatibility, profile conformance or executable
migration. This alternative is accepted.

## Accepted decision

### Compatibility claim

A **compatibility claim** is a finite inert attributed claim about one exact
relationship between identified subjects. It is issued by one identified issuer
and may be supported by separate provenance, evidence or Source records; it is
not semantic truth made true by the standard.

Every D7 claim has, abstractly:

1. one identified issuer;
2. one relation kind;
3. one exact subject;
4. one exact target or finite target set when the relation kind permits it;
5. optional exact subject/target definition contexts;
6. optional scope/context and assumptions;
7. optional declared limitations or qualities; and
8. provenance or evidence sufficient to attribute and support the claim.

The issuer is the actor, organization, process or other identified claimant
responsible for emitting the D7 claim. The issuer remains separate from every
Source, evidence source, Provenance record, Vocabulary authority, trust
decision and truth result:

```text
issuer
!= Source
!= evidence source
!= Provenance
!= Vocabulary authority
!= trusted actor
!= truth
```

A claim may reference provenance, evidence, Source records, supporting
publications/artifacts or authority/trust evidence when those are relevant, but
those roles are not inferred from the issuer and do not become the issuer. A
Source core record associated with evidence does not automatically become the
issuer of the D7 claim, and the existence of an issuer does not require that
actor to be represented as a Source. The same actor or resource may occupy more
than one role only when each role is explicitly declared.

A future binding may add claim identity, timestamps, validity intervals,
confidence, review, evidence references, labels and diagnostics using accepted
core/provenance/lifecycle mechanisms. D7 does not add a SemanticDocument core
primitive and does not choose serialization.

A mechanically well-formed claim may still be false, malicious, stale,
low-quality, unauthorized, untrusted or unusable in a particular profile.

### Subjects and targets

D7 admits the following abstract subject/target categories. These categories
are exhaustive for the known D7 relation kinds:

```text
TERM
= absolute term IRI

EDITION
= (Vocabulary identity, exact Vocabulary version)

PROFILE
= exact reproducible profile requirement set
```

No known D7 relation kind admits a generic `anything -> anything` category.

#### Term subject

Category label: `TERM`.

A term-level subject is an absolute term IRI under ADR-0010/0017.

A term claim MAY also declare one or more exact definition contexts:

```text
(term IRI, defining Vocabulary edition pair)
```

The term IRI is still the term identity. The edition context only says which
publisher-declared definition or payload contract the issuer is using as
evidence. If no exact context is supplied, generic processing cannot infer which
edition's definition, lifecycle declaration, Extension-use declaration or
payload contract was evaluated.

#### Vocabulary-edition subject

Category label: `EDITION`.

A Vocabulary-edition subject is exactly:

```text
(Vocabulary identity, exact Vocabulary version)
```

A Vocabulary identity alone, moving alias, retrieval URL, publication artifact,
file name, package name or `latest` label is not an edition subject.

#### Profile subject

Category label: `PROFILE`.

A profile-related subject or context is admissible only when it is exact and
reproducible, for example:

```text
(profile identity, exact profile version)
```

or another exact profile requirement-set identifier supplied by a future
accepted profile binding.

D7 does not define profile serialization or AI Context Profile shape. A claim
that references `latest`, `current`, `recommended`, `installed`, `default`, an
unversioned profile family or an implicit local configuration is not a generic
D7 reproducible profile subject unless an external selection policy records the
exact requirement set used.

### Relation taxonomy

D7 admits this minimal relation taxonomy.

| Relation kind | Allowed main subjects | Core meaning |
| --- | --- | --- |
| `semantic-equivalence` | terms | The issuer claims that two term meanings are the same for the declared scope/context. |
| `mapping-correspondence` | terms, editions or profile requirement sets | The issuer claims a semantic correspondence from subject to target without implying equivalence, losslessness, reversibility or execution. |
| `substitutability` | terms or editions | The issuer claims the subject may be used in place of the target for the declared scope/context. |
| `edition-compatibility` | exact Vocabulary editions | The issuer claims one exact Vocabulary edition is compatible with another for explicitly declared dimensions. |
| `profile-acceptability` | exact profile requirement set to Vocabulary edition, term or alternative set | The issuer claims a profile requirement set permits the target under declared conditions. |
| `migration-correspondence` | terms, editions or profile requirement sets | The issuer describes correspondence intended to support migration planning from subject to target. |

A future specialized interoperability Vocabulary may provide names for these
claim roles or narrower subroles. They are not added to the GeesNO Base
Vocabulary in D7.

### Allowed subject-target category matrix

Known D7 relation kinds admit only the category pairs below. A future concrete
binding must let generic processing determine these category pairs locally for
known relation kinds.

| Relation kind | Subject category | Target category |
| --- | --- | --- |
| `semantic-equivalence` | `TERM` | `TERM` |
| `mapping-correspondence` | `TERM` | `TERM` |
| `mapping-correspondence` | `EDITION` | `EDITION` |
| `mapping-correspondence` | `PROFILE` | `PROFILE` |
| `substitutability` | `TERM` | `TERM` |
| `substitutability` | `EDITION` | `EDITION` |
| `edition-compatibility` | `EDITION` | `EDITION` |
| `profile-acceptability` | `PROFILE` | `TERM` |
| `profile-acceptability` | `PROFILE` | `EDITION` |
| `migration-correspondence` | `TERM` | `TERM` |
| `migration-correspondence` | `EDITION` | `EDITION` |
| `migration-correspondence` | `PROFILE` | `PROFILE` |

All other subject/target category pairs for these known relation kinds are
invalid D7 claim shapes, not merely claims that happen to be false.

```text
invalid claim shape
!= false claim

well-formed claim
!= true claim
```

Finite target sets are allowed only when the relation kind or a future binding
permits a target set. Every target in one finite target set MUST belong to the
same allowed target category for that relation kind. Mixed-category target sets
are not admitted by the generic D7 model. For example:

```text
PROFILE -> {EDITION A, EDITION B}  valid when profile-acceptability permits alternatives
PROFILE -> {TERM X, TERM Y}        valid when profile-acceptability permits alternatives
PROFILE -> {TERM X, EDITION A}     invalid as one generic D7 claim
```

When a profile accepts both a term alternative and an edition alternative under
different rules, producers use separate `profile-acceptability` claims rather
than one mixed target set.

### `semantic-equivalence`

A `semantic-equivalence` claim states that the issuer considers two term
meanings semantically equivalent within the declared scope/context. Its only
admitted generic D7 shape is:

```text
TERM -> TERM
```

It does not imply:

- identical term IRI;
- identical local name, prefix or expansion base;
- identical normative definition text;
- identical Extension payload contract;
- identical profile acceptability;
- safe substitution in every context;
- executable migration;
- shared authority; or
- universal truth.

The relation meaning is symmetric as a claim about denoted meaning, but generic
processing does not manufacture a second stored claim, does not infer
transitive closure and does not select a winner when another issuer disagrees.

Semantic equivalence is admitted only for term-level meaning. Whole-edition
or profile equivalence is too broad for D7's universal minimum and must be
expressed through more specific edition/profile claims. `TERM -> EDITION`,
`EDITION -> EDITION`, `PROFILE -> PROFILE` and all other category pairs are
invalid `semantic-equivalence` claim shapes.

### `mapping-correspondence`

A `mapping-correspondence` claim states that the issuer sees a semantic
correspondence from subject to target. It is directional unless the same claim
or a separate claim explicitly states the reverse.

Generic D7 admits `mapping-correspondence` only between homogeneous categories:

```text
TERM -> TERM
EDITION -> EDITION
PROFILE -> PROFILE
```

Heterogeneous mappings such as `TERM -> EDITION`, `EDITION -> TERM` or
`PROFILE -> TERM` mix term meaning, edition structure and profile requirement
semantics. No universal need justifies admitting those pairs in the D7 minimum;
they require separate claims at the appropriate levels or a future specialized
interoperability Vocabulary.

Mapping does not imply:

- semantic equivalence;
- losslessness;
- reversibility;
- substitutability;
- profile acceptability;
- payload compatibility;
- transitive composition; or
- executable transformation.

A mapping claim may carry optional qualities such as `partial`, `lossy`,
`lossless`, `reversible` or `non-reversible` only as issuer-declared
qualifiers. D7 does not define an algorithm to prove those qualities.

### `substitutability`

A `substitutability` claim states that the subject may be used in place of the
target within the declared scope/context and assumptions. Generic D7 admits
only these homogeneous shapes:

```text
TERM -> TERM
EDITION -> EDITION
```

`TERM -> EDITION`, `EDITION -> TERM`, `PROFILE -> anything` and
`anything -> PROFILE` are invalid `substitutability` claim shapes.

Substitutability is directional and scope-dependent:

```text
A can substitute for B in context C
!= B can substitute for A in context C
!= A can substitute for B universally
```

A valid generic D7 substitutability claim MUST identify the relevant scope or
context. That context may be a profile requirement set, a consumer capability,
a declared operation expectation described inertly, a payload-contract context
or another exact externally supplied requirement context. D7 does not execute
or enforce the context.

### `edition-compatibility`

An `edition-compatibility` claim states that one exact Vocabulary edition is
compatible with another for one or more declared dimensions. The claim is
between exact edition pairs only:

```text
EDITION -> EDITION
```

Every other category pair is an invalid `edition-compatibility` claim shape.

Every edition-compatibility claim MUST declare at least one compatibility
dimension. D7 admits these abstract dimensions:

- `semantic-content` - term membership/meaning expectations as declared by the
  issuer;
- `extension-payload` - Extension-use host/payload assessment expectations as
  declared by the issuer;
- `lifecycle-policy` - lifecycle interpretation/new-use policy expectations as
  declared by the issuer;
- `profile-use` - use under an exact profile requirement set identified in the
  claim context.

The dimensions prevent a single ambiguous `compatible: true`. A claim may be
positive for one dimension and absent or negative for another. D7 defines no
constraint-language comparison and no algorithm for proving compatibility.

Edition compatibility is directional unless explicitly declared otherwise.
A shared term IRI or additive membership does not make editions compatible.
Lifecycle state does not imply compatibility.

### `profile-acceptability`

A `profile-acceptability` claim states that an exact profile requirement set
permits or accepts one or more exact Vocabulary editions, term alternatives or
compatibility assumptions under declared conditions. Its admitted generic D7
shapes are:

```text
PROFILE -> TERM
PROFILE -> EDITION
```

A finite alternative set may contain multiple targets only when every target is
in the same allowed target category. `PROFILE -> {TERM, EDITION}` is not a
single generic D7 claim shape; use separate claims when profile rules accept a
term alternative and an edition alternative under different conditions.

`TERM -> PROFILE`, `EDITION -> PROFILE`, `PROFILE -> PROFILE` and all other
category pairs are invalid `profile-acceptability` claim shapes.

It does not state that a particular SemanticDocument conforms to the profile.
It does not turn Vocabulary meaning into profile requirements. It does not
serialize profiles or open S4.

A profile may conceptually:

- require an exact Vocabulary edition;
- permit one or more explicitly identified alternatives;
- constrain terms, cardinalities, lifecycle states or payload expectations;
- declare mapping or compatibility assumptions; or
- reject an edition despite another issuer's compatibility claim.

Generic D7 processing can preserve the claim and check only deterministic
shape. Actual profile conformance remains future profile-layer work.

### `migration-correspondence`

A `migration-correspondence` claim describes an issuer's migration-oriented
correspondence from subject to target. It may include declared limitations,
lossiness, reversibility, deprecated/retired source context or successor
context.

Generic D7 admits `migration-correspondence` only between homogeneous
categories:

```text
TERM -> TERM
EDITION -> EDITION
PROFILE -> PROFILE
```

Heterogeneous migration correspondence between levels, such as
`EDITION -> TERM` or `TERM -> PROFILE`, must be modelled through separate
claims or by a future specialized interoperability Vocabulary. It is not part
of the D7 universal minimum.

Migration correspondence is descriptive only:

```text
migration claim
!= migration execution
!= code
!= adapter
!= transform function
!= permission to rewrite data
```

D7 defines no transformation language and no automatic migration. Any actual
migration tool belongs outside GeesNO.Semantic or in a separate implementation
that treats D7 claims as untrusted descriptive input.

### Directionality summary

| Relation kind | Directionality | Symmetry/closure |
| --- | --- | --- |
| `semantic-equivalence` | Relation meaning is symmetric, claim record may still have a recorded source/target order. | No automatic transitive closure; no winner on conflict. |
| `mapping-correspondence` | Directional by default. | Reverse and composition require explicit claims. |
| `substitutability` | Directional and context-dependent. | Reverse and universal substitution are never inferred. |
| `edition-compatibility` | Directional unless explicitly declared otherwise. | No order/range/additive/lifecycle inference. |
| `profile-acceptability` | Directional from profile requirement set to accepted target/alternative. | Does not imply document conformance or target preference. |
| `migration-correspondence` | Directional by default. | Reverse, losslessness and execution require explicit claims and external tooling. |

### Scope and context

A D7 claim may declare:

- applicable scope;
- exact profile or requirement context;
- subject/target edition contexts;
- relevant Extension payload contract;
- assumptions;
- limitations;
- declared quality such as partial/lossy/lossless/reversible; and
- evidence/provenance.

D7 does not define a mini expression language for arbitrary conditions. Scope
and assumptions are finite descriptive data whose concrete representation is
left to a future binding or specialized Vocabulary.

When a relation is inherently context-dependent, such as substitutability or
profile acceptability, absence of exact context prevents a generic processor
from treating the claim as reproducible generic compatibility.

### Exact version rule

ADR-0017 remains controlling. Generic D7 processing infers no compatibility,
order or replacement from version-token spelling.

```text
"2.0.0" > "1.9.0"
```

is not a generic GeesNO.Semantic fact. A publisher may document a versioning
scheme and an issuer may make explicit compatibility claims, but a generic
processor treats version tokens as exact opaque tokens.

`latest`, `current`, `recommended` and `stable` aliases are not exact edition
subjects. If an external policy resolves one, the D7 claim or report records
the exact edition pair actually used.

### Same term IRI across editions

The same term IRI may appear in two editions when its denoted meaning remains
compatible under ADR-0017. That fact alone implies none of the following:

- the two editions are compatible;
- the two editions have the same membership;
- Extension payload contracts are compatible;
- lifecycle declarations are compatible;
- a profile accepts both editions;
- a migration is safe; or
- a consumer may substitute one edition for the other.

Every such result requires an explicit D7 claim or profile rule.

### Additive editions

If edition B equals edition A plus one new term, generic D7 processing infers
no automatic backward or forward compatibility. Some consumers or profiles may
accept the addition; closed profiles may reject it. Compatibility must be
explicit and dimension-scoped.

### Lifecycle boundary

Lifecycle and compatibility remain separate:

```text
stable != compatible
experimental != incompatible
deprecated != unusable
retired != invalid
```

Lifecycle may be evidence in a D7 claim or profile policy, but generic
processing never converts ADR-0019 state into compatibility, substitution or
migration.

### Extension payload contracts

Two terms may be semantically equivalent while their Extension payload
contracts differ. Two editions may share term meanings while a profile rejects
one because payload expectations changed.

D7 therefore separates semantic equivalence from `extension-payload` edition
compatibility and from profile acceptability. It defines no algorithm for
comparing constraint languages or proving payload-contract equivalence.

### Conflicts and trust

Conflicts are first-class. Generic processing preserves all supplied D7 claims
and selects no winner by:

- timestamp;
- HTTPS;
- domain name;
- GeesNO branding;
- vendor identity;
- discovery order;
- lexical version order;
- lifecycle state;
- publication location;
- signature presence; or
- AI confidence.

```text
claim != truth
authority != trust
trust != equivalence
equivalence claim != conformance
```

D5 authority/trust evidence may accompany D7 claims. It does not make the
compatibility claim true. A trusted issuer may be wrong; an untrusted issuer may
make a useful claim. Consumers apply external policy.

### Transitivity and closure

Generic D7 processing performs no automatic logical closure.

```text
A maps-to B
B maps-to C
```

DOES NOT imply:

```text
A maps-to C
```

The same rule applies to equivalence, substitutability, edition compatibility,
profile acceptability and migration correspondence. A relation kind or future
specialized Vocabulary may define an explicit safe closure rule for its own
bounded context, but D7 creates no universal reasoner and no mandatory closure.

### Offline behavior

D7 works with directly supplied local Vocabularies, profiles and claim records.
No claim requires:

- network access;
- IRI dereference;
- geesno.com availability;
- third-party domain availability;
- catalog lookup;
- registry lookup;
- embedding search;
- LLM matching; or
- probabilistic similarity.

Unavailability means unavailable evidence, not invalid identity or automatic
incompatibility.

### Deterministic conformance boundary

A future D7 binding may let a generic processor check deterministically:

- allowed relation kind;
- required subject/target shape;
- exact edition/profile requirement-set references;
- required scope/context for relation kinds that need it;
- dimension presence for edition compatibility;
- finite target sets;
- provenance/evidence association; and
- bounded processing.

Generic conformance does not check whether a mapping is true, whether terms are
really equivalent, whether a migration is safe, whether an issuer should be
trusted, whether two payload contracts are mathematically compatible or whether
an AI suggestion is semantically correct. A known relation kind whose subject
and target categories are outside the D7 matrix is structurally/semantically
invalid as a D7 claim shape; that is distinct from a well-formed claim that may
be false.

### Security and AI boundary

D7 claims, mapping descriptions, examples, URLs, profile identifiers,
constraint references and migration notes are untrusted inert data. They do not
execute tools, download code, load plugins, call APIs, invoke models, grant
permissions, rewrite documents or activate adapters.

D7 does not admit embedding similarity, vector thresholds, LLM semantic
matching, model confidence, automatic ontology alignment, RAG, agent decisions
or probabilistic matching as normative generic semantics.

An external tool may suggest a mapping, including with AI. That suggestion is
not a D7 claim unless an identified issuer records it as finite attributed
claim evidence, and even then generic processing treats it as untrusted
claim data, not truth.

## Cross-domain validation

| Domain | D7 stress case | Result under the proposal |
| --- | --- | --- |
| Engineering-like object graph | Two component vocabularies use similar `label` and `part` terms. | No lexical or domain heuristic creates equivalence; explicit attributed claims can describe mapping or substitutability by scope. |
| Spreadsheet/table data | A profile accepts either a business Vocabulary edition or a standards-body edition for column labels. | Profile acceptability can be described against exact editions without requiring spreadsheet-specific core fields. |
| Technical/legal documents | Two legal terminology sources disagree about equivalence between clause terms. | Conflicting attributed claims are preserved; no authority, timestamp or domain wins generically. |
| Software/source repositories | A language-analysis Vocabulary publishes an additive edition. | Additive structure alone creates no compatibility; profiles or issuers must claim exact compatibility dimensions. |
| Scientific datasets | A measurement annotation term keeps its IRI while payload constraints change. | Semantic equivalence and Extension payload compatibility remain distinct; no constraint-language comparison is invented. |
| Generic product/asset data | Vendor and community vocabularies map similar product description terms. | Mappings are directional, scoped and descriptive; no preferred GeesNO or vendor term is inferred. |

All six domains use the same claim, subject, exact-edition, scope, conflict and
trust boundaries. None requires a domain primitive, registry, resolver, AI
matcher, adapter or execution behavior.

## Adversarial cases

| # | Case | Generic processor may infer | Generic processor MUST NOT infer |
| --- | --- | --- | --- |
| 1 | Same local name, different Vocabulary | The terms are distinct unless expanded absolute IRIs match. | Equivalent meaning, same authority or compatibility. |
| 2 | Same term IRI across two editions | The term identity is the same IRI. | Whole-edition compatibility, same payload contract or profile acceptability. |
| 3 | Same term meaning but different Extension payload contract | A claim may separately describe semantic equivalence and payload incompatibility. | Payload compatibility from semantic equivalence alone. |
| 4 | One issuer claims two terms equivalent and another issuer disagrees | Conflicting attributed claims exist. | A universal winner or truth result. |
| 5 | Directional substitutability A to B but not B to A | The stated direction can be preserved. | Reverse substitution. |
| 6 | Additive Vocabulary edition | Exact editions differ. | Backward/forward compatibility from added terms. |
| 7 | Removed, deprecated or retired term | Lifecycle evidence may be reported if supplied. | Deletion, invalidity or automatic replacement. |
| 8 | Mapping with information loss | Lossiness may be preserved as issuer-declared qualifier. | Safe conversion or semantic equivalence. |
| 9 | Mapping claimed reversible but not independently verified | The reversibility claim exists as attributed evidence. | Verified reversibility. |
| 10 | Identical prefix with different namespace | Prefix is local spelling only. | Same Vocabulary or same terms. |
| 11 | Versions `1.9` and `2.0` without explicit compatibility claim | Exact opaque tokens differ. | Order, recency, compatibility or replacement. |
| 12 | `latest` alias changes | The resolved exact pair must be recorded externally. | Reproducible compatibility from the alias alone. |
| 13 | Vocabulary unavailable offline | Evidence is unavailable. | Invalid identity or incompatibility. |
| 14 | Profile requires exact edition A but B claims compatibility | Both claims can be preserved. | That B satisfies the profile unless the profile or an accepted policy permits it. |
| 15 | Profile permits explicitly declared A or B | The profile-acceptability claim can list exact alternatives. | Any unlisted edition is acceptable. |
| 16 | Same semantic meaning but different representation constraints | Semantic and representation/payload dimensions differ. | Substitution or profile conformance. |
| 17 | Base Vocabulary term versus third-party similar term | The absolute IRIs coexist. | GeesNO term wins or similar names map automatically. |
| 18 | Malicious compatibility claim | The claim is inert attributed data. | Trust, execution or truth. |
| 19 | Trusted issuer but semantically wrong claim | Trust evidence may be external context. | Truth from trust alone. |
| 20 | Untrusted issuer with potentially correct claim | The claim can be preserved. | Rejection or acceptance solely from trust absence. |
| 21 | Conflicting mapping claims | Conflict can be reported. | Automatic merge or precedence. |
| 22 | Cyclic mappings A to B to C to A | The cycle can be preserved. | Equivalence, closure or executable cycle handling. |
| 23 | Mapping A to B and B to C without explicit A to C | Two mappings exist. | A to C mapping. |
| 24 | Equivalent terms from different authorities | The equivalence claim and authorities can be preserved. | Shared authority or global truth. |
| 25 | Profile-specific compatibility | The compatibility is scoped to that profile. | Universal compatibility. |
| 26 | Document has no compatibility metadata | No D7 claim is present. | Incompatibility or compatibility. |
| 27 | Unknown relation kind | A future binding may preserve it as unknown/unsupported. | Generic D7 semantics for that relation. |
| 28 | Network unavailable | Offline supplied claims remain processable. | Network requirement or failure-derived invalidity. |
| 29 | HTTP 404 for Vocabulary identity | Retrieval failed or is unavailable. | Identity invalidity or incompatibility. |
| 30 | External tool proposes a mapping using AI | It may become attributed claim evidence if recorded by an issuer. | Normative mapping, truth, confidence or conformance from AI output. |
| 31 | Issuer is a human or organization while evidence Source is a document | Issuer and Source roles can both be represented when explicitly declared. | That the evidence Source is the issuer, or that the issuer is a Source. |
| 32 | Source supplies evidence but no issuer is identified | Evidence exists but the generic attributed D7 claim is incomplete. | An issuer from Source identity, location, publisher or provenance alone. |
| 33 | Issuer and Vocabulary authority are the same actor | The actor may occupy both roles only when both are explicitly declared. | Authority, trust or truth from issuer equality. |
| 34 | `TERM -> EDITION` semantic-equivalence | Known categories are present but the pair is outside the matrix. | A false-but-well-formed equivalence claim. |
| 35 | `TERM -> EDITION` substitutability | Known categories are present but the pair is outside the matrix. | Cross-level substitution or profile conformance. |
| 36 | `EDITION -> TERM` edition-compatibility | Known categories are present but the pair is outside the matrix. | A compatibility dimension result. |
| 37 | `TERM -> PROFILE` profile-acceptability | Direction and categories are outside the matrix. | Profile acceptance or profile conformance. |
| 38 | `PROFILE -> {TERM, EDITION}` mixed target set | Mixed target categories require separate claims. | One generic finite alternative set spanning term and edition targets. |
| 39 | `TERM -> EDITION` mapping-correspondence | Heterogeneous mapping is outside the D7 minimum matrix. | A generic cross-level mapping relation. |
| 40 | `EDITION -> TERM` migration-correspondence | Heterogeneous migration correspondence is outside the D7 minimum matrix. | Executable or cross-level migration semantics. |

## Consequences

- D7 supplies an abstract model for explicit compatibility evidence without
  creating automatic compatibility.
- A D7 claim has one identified issuer, while Source records, evidence,
  Provenance, Vocabulary authority, trust and truth remain separate roles.
- Generic processors preserve finite attributed claims and conflicts rather
  than selecting winners.
- Exact edition and exact profile requirement-set references remain necessary
  for reproducibility.
- Relation kinds remain separated so semantic equivalence, mapping,
  substitutability, edition compatibility, profile acceptability and migration
  correspondence cannot collapse into one ambiguous boolean.
- Known D7 relation kinds have a closed subject/target category matrix. An
  outside-matrix category pair is an invalid D7 claim shape, not a false claim.
- Finite target sets, when permitted, must be homogeneous by target category.
- GeesNO Base Vocabulary receives no special priority over third-party or
  future specialized Vocabularies.
- Extension payload contracts and profile requirements remain separate from
  term meaning.
- No D7 claim serialization, schema, mapping language, resolver, registry or
  engine is selected by this ADR.
- No S2 schema, profile serialization, Vocabulary artifact, registry, resolver,
  SDK, adapter, reasoner, AI matcher or migration engine follows from this
  ADR.

## Remains open

- concrete D7 claim serialization, media type, schema and binding version;
- exact claim identity, issuer identity, evidence references, Source record
  references and provenance representation;
- concrete profile identity/version and profile requirement-set serialization;
- concrete profile conformance result model under S4/S5;
- future specialized interoperability/mapping Vocabulary terms;
- concrete diagnostics for unsupported relation kinds, missing contexts and
  conflicts;
- optional integrity/signature/fingerprint evidence for claim bundles;
- formal migration guides or executable transformations outside
  GeesNO.Semantic; and
- public release and any hosting/publication process.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-17. Acceptance covers the finite inert attributed D7
compatibility claim model, issuer/source/provenance/authority separation,
exact subject and target categories, the closed relation-kind category matrix,
directionality, scope/context requirements, conflict preservation, no automatic
version inference, no transitive closure and all offline, non-execution and
AI-neutral boundaries recorded above.

Acceptance closes D7. Formal S3 closure is recorded separately after
milestone review. This ADR does not publish any Vocabulary or D7 compatibility
artifact, choose concrete claim serialization/schema, create a registry,
resolver, reasoner, profile schema, migration engine, SDK, adapter, AI matcher
or execution behavior, modify S2 or open S4.
