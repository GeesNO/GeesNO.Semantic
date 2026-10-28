# ADR-0019: Vocabulary and term lifecycle semantics

- **Status:** Accepted
- **Date:** 2026-09-13
- **Accepted by:** Explicit human architecture decision on 2026-09-13
- **Decision order:** Third S3 architecture decision after accepted ADR-0018

## Context

Accepted ADR-0017 identifies a Vocabulary edition by the immutable ordered
pair:

```text
(Vocabulary identity, Vocabulary version)
```

Accepted ADR-0018 defines a finite, inert publication artifact for exactly one
edition. Term membership and each member's denoted meaning are normative
semantic content of that edition. Neither decision yet says how a publisher
describes experimental, stable, deprecated or retired lifecycle state for a
Vocabulary family, an edition or a term.

Lifecycle must be expressible without mutating a historical edition. A later
edition may publish a new lifecycle declaration about a subject that appeared
earlier, but that new declaration cannot rewrite the earlier edition's content
or create a global live-state oracle. An offline consumer holding only the
earlier artifact must still be able to interpret exactly what that artifact
declares without discovery.

This ADR proposes only serialization-independent lifecycle semantics. It does
not choose member names, JSON shape, schema, discovery, authority, equivalence,
profile compatibility, migration execution or a Base Vocabulary.

## Prerequisite review

No unresolved prerequisite blocks D3:

1. Foundation fixes the descriptive, inert, domain-neutral and
   serialization-independent project boundary.
2. ADR-0010 fixes absolute term IRI identity and offline namespace expansion.
3. ADR-0015 keeps Vocabulary lifecycle above the closed S2 core and prevents
   Extensions from granting authority or executing behavior.
4. ADR-0016 freezes S2 `0.1.0` and deterministic offline Layers 0–3 without
   making Vocabulary understanding bare-core conformance.
5. ADR-0017 supplies stable Vocabulary, edition and term identities and makes
   every published edition immutable.
6. ADR-0018 supplies the one-edition publication scope, explicit membership,
   normative definitions, inert processing and concrete-binding boundary.

D4 Extension vocabulary conventions, D5 discovery/authority/governance, D6
Base Vocabulary, D7 equivalence/profile compatibility and S4 projection rules
are downstream. None is needed to define the abstract lifecycle claim below.

## Requirements

The model must:

- describe lifecycle for a Vocabulary family, an exact Vocabulary edition or
  an absolute term IRI without collapsing those subjects;
- make every lifecycle declaration part of one immutable declaring edition;
- permit a later edition to make a new declaration without modifying an older
  edition;
- distinguish explicit `stable` from absence of lifecycle information;
- keep experimental terms subject to ADR-0017 meaning/identity stability;
- retain deprecated and retired identities for existing and historical use;
- make a successor optional and separate from equivalence or migration;
- infer no lifecycle state from absence in a later edition;
- require no network, registry, latest-version lookup or global chronology;
- support deterministic generic validation without semantic judgement;
- treat all lifecycle metadata as inert descriptive data; and
- add no S1/S2 primitive, SemanticDocument member, execution mechanism,
  GeesNO.Core dependency or application adapter.

## Controlling distinctions

```text
Vocabulary identity
!= Vocabulary edition identity

term identity
!= term lifecycle state

deprecated
!= deleted

retired
!= tombstoned SemanticDocument record

deprecated
!= invalid

experimental
!= semantically unconstrained

lifecycle state
!= availability
!= discovery
!= authority
!= permission
!= compatibility

replacement
!= equivalence
!= automatic migration

lifecycle declaration
!= term membership

local published lifecycle declaration
!= global/current lifecycle truth
```

## Alternatives

### Alternative A — Mutable status attached to the identity

Keep one current lifecycle value for each Vocabulary or term and update it in
place. This makes lookup convenient but silently mutates historical meaning,
requires a current authority source and prevents an offline consumer from
reproducing what an edition originally declared.

This alternative is rejected because it contradicts ADR-0017 edition
immutability and would make discovery or a registry normative.

### Alternative B — Boolean flags with absence meaning stable

Use independent `experimental`, `deprecated` and `retired` flags and treat an
unflagged subject as stable. Flags permit contradictory combinations, while
absence cannot distinguish deliberately stable from unspecified or unavailable
lifecycle information.

This alternative is rejected. Absence remains no assertion, not a hidden
`stable` value.

### Alternative C — Edition-scoped declaration with four explicit states

Each publication edition may carry normative lifecycle declarations. Every
declaration identifies exactly one subject and exactly one state from
`experimental`, `stable`, `deprecated` or `retired`. A later edition carries a
new declaration rather than modifying an earlier artifact. Term declarations
may carry optional successor references without claiming equivalence or
automatic migration.

This alternative is proposed. Four explicit states keep maturity, ordinary
recommended use, discouragement and lifecycle end distinct while leaving
absence unambiguously unspecified.

### Alternative D — Reuse SemanticDocument lifecycle or Tombstones

Represent a retired term as a Tombstone or a semantic Revision/Change record.
This would collapse publication governance with the lifecycle of addressable
records inside a SemanticDocument and would reopen S1/S2.

This alternative is rejected. Vocabulary lifecycle is publication semantics,
not SemanticDocument record deletion or replay history.

## Proposed decision

### Lifecycle declaration and declaring edition

1. A **Vocabulary lifecycle declaration** is a finite, inert normative claim
   contained in one Vocabulary publication edition.
2. The exact `(Vocabulary identity, Vocabulary version)` of that publication is
   the declaration context. The declaration is normative semantic content of
   the declaring edition under ADR-0017/0018.
3. Adding, removing or changing a lifecycle declaration changes the declaring
   edition's normative semantic content and therefore requires a new
   Vocabulary version. A publisher MUST NOT revise lifecycle in place while
   retaining the same edition pair.
4. A declaration about an earlier subject does not mutate that subject's
   historical publication. It is a new claim made by the declaring edition.
5. Version tokens remain opaque. Generic processing infers no chronology or
   precedence from their spelling and does not select a globally latest
   declaration.

### Lifecycle subjects

Each declaration has exactly one subject kind and exact subject identity:

1. **Vocabulary family** — the Vocabulary identity of the declaring artifact.
2. **Vocabulary edition** — an exact ADR-0017 edition pair whose Vocabulary
   identity is the declaring artifact's Vocabulary identity. It may identify
   the declaring edition or another edition in that family.
3. **Term** — one absolute term IRI under ADR-0010.

Vocabulary-family, Vocabulary-edition and term declarations are independent.
No state propagates implicitly between them. Deprecating an edition does not
deprecate its terms or family; retiring a family does not rewrite historical
edition or term declarations.

A term declaration does not add the term to or remove it from edition
membership. It may refer to a member or non-member term. Because term IRI
shape does not prove Vocabulary ownership, a generic processor treats the
declaration as the publisher's claim and infers no authority; D5 owns that
governance question.

Within one publication artifact, at most one lifecycle declaration may exist
for the same exact subject kind and identity. This prevents contradictory
states inside one declaring edition without creating a cross-edition merge
rule.

### Lifecycle states

When a lifecycle declaration is present, it carries exactly one of these four
states:

- **`experimental`** — the publisher presents the subject for evaluation or
  early use and does not claim ordinary stable maturity. The edition remains
  immutable. Experimental status never permits incompatible redefinition of
  one term IRI; ADR-0017 still requires a new term IRI for an incompatible
  change of denoted meaning.
- **`stable`** — the publisher presents the subject as suitable for ordinary
  new use in the declaration context, rather than experimental, deprecated or
  retired. It does not guarantee availability, support duration, authority,
  compatibility with another edition/profile or future operational state.
- **`deprecated`** — the identity and denoted meaning remain valid for existing
  and historical use, but the publisher discourages new use. Deprecation does
  not delete the subject, invalidate existing SemanticDocuments, change its
  meaning or require automatic migration. A successor is optional.
- **`retired`** — the publisher considers the subject's lifecycle ended and no
  longer recommends new use. Identity, denoted meaning and historical
  references remain. Retirement is not deletion, a SemanticDocument
  Tombstone, unavailability, invalidity or an instruction to remove data.

The absence of a lifecycle declaration means **unspecified in that edition**.
It does not mean `stable`, `experimental`, `deprecated` or `retired`.

D3 defines no universal transition graph, state precedence or monotonicity
algorithm across editions. Apparently inconsistent later declarations remain
separate edition-scoped publisher claims; judging their governance correctness
or determining a current authoritative state belongs to D5.

### Immutable historical editions

Lifecycle changes are represented by a new declaring edition:

```text
Edition 1.0:
  term A lifecycle = stable

Edition 1.1:
  term A lifecycle = deprecated
  successor = term B
```

Edition 1.0 remains unchanged. A consumer holding only Edition 1.0 knows only
the `stable` declaration published there. Edition 1.1 does not retroactively
alter Edition 1.0's bytes, normative content or term meaning. Learning about
Edition 1.1 requires optional distribution or future D5 discovery; neither is
part of D3 conformance.

A later declaration may explicitly target an earlier exact edition as
deprecated or retired. That statement is normative content of the later
declaring edition, not a mutation of the targeted edition.

### Term absence

Term membership remains the exact set declared under ADR-0018. If a term is
absent from another edition, generic processing infers none of the following:

```text
absent term
!= deleted
!= deprecated
!= retired
!= invalid
```

An explicit lifecycle declaration is required to communicate lifecycle state.
A declaration about a non-member term does not restore membership, and term
membership does not itself provide lifecycle state.

### Successor references

A term declaration in state `deprecated` or `retired` MAY carry a finite,
unordered set of successor term IRIs. A successor expresses only that the
publisher recommends the target as a possible choice for new use.

Successor targets:

- are absolute term IRIs and remain distinct from the deprecated/retired term;
- are unique by exact term-IRI equality within one declaration;
- may identify a term in the same edition, another edition or another
  Vocabulary;
- do not assert semantic equivalence, substitutability, compatibility or a
  lossless transformation;
- do not authorize automatic rewriting or migration; and
- require no dereference or availability.

A successor set is invalid on a Vocabulary-family or edition declaration, on
an `experimental` or `stable` term declaration, or when it contains the
subject term itself. D3 does not impose a global acyclic successor graph:
artifacts may be partial and cross-Vocabulary targets may be unavailable.
Cross-Vocabulary authority is D5; equivalence, mappings and profile
compatibility are D7.

### Deterministic generic conformance

A later concrete publication binding must let a generic validator determine
without semantic interpretation:

- admitted subject kind and required identity shape;
- one admitted lifecycle token;
- placement and cardinality;
- at most one declaration per exact subject in an artifact;
- Vocabulary-family and edition subject scoping to the declaring Vocabulary;
- successor placement, exact uniqueness and self-reference constraints; and
- finite/resource-bounded processing.

Generic conformance never requires an LLM, network access, registry lookup,
term-meaning interpretation or a subjective decision that a subject should be
experimental, deprecated or retired. Publisher/governance owns the factual and
editorial correctness of lifecycle claims unless a later deterministic
contract adds further rules.

D3 fixes no JSON member, collection shape, schema expression, diagnostic code
or publication media type. Those belong to the concrete ADR-0018 binding.
Nothing is added to the S2 SemanticDocument schema or Layers 0–3.

### Offline and temporal boundary

```text
local published lifecycle declaration
!= global/current lifecycle truth

semantic state asserted at time T
!= guaranteed live operational state at time T+n
```

A local artifact is sufficient to interpret its own lifecycle declarations.
It need not discover later editions. Optional future discovery may expose
newer claims, but D3 does not define which is authoritative or current.

Existing Provenance, Validity and Revision/lifecycle mechanisms are sufficient
foundations for later profiles to preserve temporal context. D3 introduces no
polling, subscription, event stream, telemetry, freshness protocol or live
state primitive. S4 must ensure that an AI Context projection does not present
a historical or interval-scoped semantic assertion as guaranteed live
operational state.

### Description and execution boundary

Lifecycle remains descriptive even if a future Vocabulary defines terms about
capabilities, operations, limits, preconditions, permissions or endpoints:

```text
description of a capability
!= executable capability

description of an operation
!= operational binding

description of a limit or precondition
!= enforcement

description of a permission
!= authorization
```

A declaration such as `capability deprecated`, `operation retired`, `requires
approval` or `limit = X` remains untrusted inert semantic data. It never grants
permission, enforces a condition, invokes software, activates a plugin/agent,
creates a transaction or introduces a GeesNO.Core dependency.

## Cross-domain validation

| Domain | Lifecycle stress case | Result under the proposal |
| --- | --- | --- |
| Engineering-like object graph | A classification term for a component is deprecated after a replacement practice is published. | A new edition discourages new use while old model classifications remain valid; no CAD/BIM primitive enters core. |
| Spreadsheet/table | A business-column term is experimental in one edition and stable in another. | Both edition-scoped declarations remain reproducible; no workbook adapter or inferred transition is required. |
| Technical/legal document | A legal drafting term is retired while archived documents still cite it. | Retirement ends recommended new use but preserves identity, meaning and historical citation; no deletion is inferred. |
| Source-code repository | An analysis predicate is deprecated with two possible successors. | The unordered successor set expresses recommendations without Git semantics, equivalence or automatic code migration. |
| Scientific dataset | An experimental measurement term receives an incompatible correction. | Experimental status does not relax ADR-0017: a new edition and new term IRI are required for incompatible meaning. |
| Generic product/asset dataset | A supplier edition is deprecated while its product terms remain in current datasets. | Edition state does not propagate to term invalidity, authority or availability; no vendor-specific field enters core. |

All six domains use the same subjects, states and edition-scoped claim model.
None requires execution, live state, a registry, a profile or a domain-specific
universal primitive.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| Experimental term receives an incompatible meaning change under the same term IRI | Invalid Vocabulary evolution under ADR-0017. Experimental does not waive identity stability; the changed edition needs a new Vocabulary version and the incompatible meaning needs a new term IRI. |
| Deprecated term still appears in older SemanticDocuments | Valid. The term retains identity and meaning; deprecation does not retroactively invalidate bare core or historical use. |
| Deprecated term has no successor | Valid. A successor is optional. |
| Deprecated term has a successor with a distinct IRI | Valid when the successor rules are satisfied; the target is a recommendation for new use. |
| Successor is not semantically equivalent | Not a generic conformance error. Successor never asserts equivalence or safe substitution, and no automatic migration follows. |
| Retired term appears in a new SemanticDocument | The S2 document remains bare-core valid. D3 may inform consumers that new use is discouraged but does not prohibit or execute policy. |
| Term disappears from a later Vocabulary edition without a lifecycle declaration | No state is inferred. Absence is not deprecated, retired, deleted or invalid. |
| Older edition declares `stable`; another edition declares `deprecated` | Both immutable edition-scoped claims remain intact. The second does not mutate the first, and token spelling alone proves no chronology. |
| Offline consumer has only the older edition | It knows only that edition's declaration and remains conforming without discovery; it must not invent a global current state. |
| Vocabulary edition is deprecated while its terms keep stable identities | Valid. Edition lifecycle does not propagate to term identity, meaning, membership or lifecycle state. |
| Publisher changes lifecycle in an already published edition without changing its version | Invalid conflicting publication claim; lifecycle is normative content of the declaring edition. |
| Lifecycle metadata contains a URL or instruction-like string | Inert untrusted data. It triggers no dereference, instruction following, plugin/agent activation or execution. |
| A description of permission or capability is treated as actual authorization or execution | Invalid processing interpretation. Semantic description grants no permission, capability, enforcement or operational binding. |
| Deprecated or retired status is used to invalidate historical or otherwise bare-core-valid SemanticDocuments | Invalid D3 interpretation. Lifecycle status does not retroactively alter S2 validity. |

## Consequences

- Publishers can express lifecycle evolution without rewriting historical
  artifacts or term meanings.
- Explicit `stable` avoids interpreting missing lifecycle information as a
  positive maturity claim.
- Deprecated and retired terms remain identifiable and usable for historical
  interpretation.
- Edition, family and term lifecycle remain independent rather than
  propagating hidden invalidity.
- Optional successors support migration guidance while preserving the D7
  equivalence boundary and forbidding automatic migration.
- Offline consumers receive reproducible local claims but no false promise of
  global freshness or authoritative current state.
- Concrete binding work must represent these semantics deterministically, but
  no S2 schema or fixture changes follow from this Proposed ADR.

## Remains open

- concrete lifecycle member names, placement, collection shape, schema and
  binding-version rules under the future ADR-0018 publication binding;
- optional lifecycle rationale, documentation, Provenance and Validity
  representation;
- transition-governance policy, contradictory publisher claims and selection
  of a current authoritative declaration under D5;
- Extension vocabulary lifecycle/compatibility conventions under D4;
- discovery of later editions, moving aliases, authority and trust under D5;
- GeesNO Base Vocabulary lifecycle application under D6;
- cross-Vocabulary mappings, equivalence, compatibility and profile policy
  under D7;
- whether a profile imposes stricter new-use rules for deprecated or retired
  terms;
- migration plans or executable transformations, which remain outside D3 and
  outside GeesNO.Semantic execution semantics;
- S4 projection rules for temporal context and prevention of historical-state
  versus live-state confusion;
- publication fingerprints, signatures, canonical bytes and integrity threat
  model; and
- registry, package, HTTP/API/MCP, telemetry, subscription and public-release
  protocols.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-13. Acceptance covers the edition-scoped declaration
model, the three independent subject kinds, the four explicit lifecycle
states, unspecified absence, immutable historical editions, optional
non-equivalent successors, deterministic generic conformance and the offline,
temporal and execution boundaries recorded above.

Acceptance closes D3 and authorizes analysis of D4. It does not itself choose
a lifecycle serialization/schema, define an Extension convention, create a
discovery or authority mechanism, publish the Base Vocabulary, accept any D4–
D7 decision, or authorize a profile, SDK, adapter or execution behavior.
