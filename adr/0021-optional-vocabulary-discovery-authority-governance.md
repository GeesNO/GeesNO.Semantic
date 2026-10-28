# ADR-0021: Optional Vocabulary discovery, authority and governance model

- **Status:** Accepted
- **Date:** 2026-09-14
- **Accepted by:** Explicit human architecture decision on 2026-09-15
- **Decision order:** Fifth S3 architecture decision after accepted ADR-0020

## Context

Accepted ADR-0017 separates stable Vocabulary and exact edition identity from
publication artifacts, retrieval locations and moving discovery aliases.
Accepted ADR-0018 defines a finite inert publication artifact for one exact
edition, permits equivalent artifacts and leaves discovery, authority and
integrity open. Accepted ADR-0019 defines edition-scoped lifecycle claims.
Accepted ADR-0020 requires D4 Extension-aware assessment to use an explicitly
selected exact edition and states that artifact conformance does not prove
publisher authority.

Independent consumers now need an optional way to receive candidate edition
and publication information, attribute claims and retain authority evidence.
That mechanism must help callers locate information without becoming a global
truth oracle, identity allocator, required registry or automatic fetch
instruction.

The central question is:

> How can a consumer obtain publication candidates and provenance/authority
> evidence optionally and reproducibly without making a registry, URL, alias
> or network define semantic truth?

This ADR proposes only a serialization-independent discovery, authority and
minimal governance model. It does not define JSON, an API, HTTP, DNS, a
registry service, a signature format, canonical bytes, trust policy, Base
Vocabulary, profile or implementation tooling.

## Prerequisite review

No unresolved prerequisite blocks D5:

1. Foundation requires open, offline-capable, software-neutral and descriptive
   semantics with no mandatory cloud, execution runtime or GeesNO.Core.
2. ADR-0017 supplies stable Vocabulary identity, exact immutable edition pairs
   and the separation of moving aliases, artifacts and retrieval locations.
3. ADR-0018 supplies the publication artifact subject and the distinction
   between semantic-edition equality, artifact representation and location.
4. ADR-0019 supplies lifecycle states without turning availability or
   discovery into lifecycle truth.
5. ADR-0020 supplies the exact-edition selection boundary and already keeps
   conformance, authority, trust and compatibility separate.

A concrete publication/catalog binding is not required to define the abstract
claim relationships. Signatures, fingerprints and canonical bytes are not a
prerequisite because D5 can represent attribution, authority and delegation as
claims/evidence without asserting universal cryptographic verification. Trust
remains external. Those later mechanisms may strengthen evidence without
changing the abstract distinctions below.

D6 Base Vocabulary admission and D7 equivalence/profile compatibility are
downstream and are not needed for optional discovery.

## Requirements

The model must:

- permit complete offline use when a caller directly supplies an exact edition
  pair and local publication artifact;
- require no DNS, HTTP, registry, central service, IRI dereference, package
  manager, public GeesNO service, cloud account or network;
- distinguish discovery of a Vocabulary family from location of one exact
  edition;
- return zero or more candidates without silently selecting a winner;
- associate one exact edition with zero, one or several candidate retrieval
  locations without making any location identity;
- represent moving aliases only as scoped discovery claims whose resolved
  result is an exact edition pair;
- preserve attribution and provenance for discovery, publication, location-
  operator and authority claims;
- represent publisher and retrieval-location operator roles through optional
  explicit actor-role attribution claims rather than inferring either role
  from a generic claimant, issuer, artifact or location;
- distinguish claim issuer, claimed publisher, claimed location operator and
  claimed Vocabulary authority even when one party explicitly occupies more
  than one role;
- require neither publisher nor location-operator attribution to identify a
  Vocabulary/edition, use direct offline supply or mechanically accept an
  ADR-0018 artifact;
- support scoped authority and stewardship/delegation claims without claiming
  globally proven ownership;
- keep trust as contextual external policy rather than a universal boolean;
- preserve conflicting evidence and avoid implicit precedence;
- keep authenticity/integrity evidence separate from authority, trust and
  conformance;
- retain deprecated, retired and historical Vocabulary information when a
  source chooses to publish it;
- permit deterministic generic checking of future representations without an
  LLM, network, subjective trust judgement or hidden remote state;
- treat all discovery metadata, locations and instruction-like strings as
  inert untrusted data;
- remain outside SemanticDocument core and preserve S2 Layers 0–3 unchanged;
  and
- remain domain-, format-, software-, vendor- and AI-provider-neutral.

## Controlling distinctions

```text
discovery
!= identity

discovery result
!= semantic truth

discovery source
!= authority

retrieval location
!= Vocabulary identity
!= Vocabulary edition identity

availability
!= authenticity

authenticity
!= authority

authority
!= trust

trust
!= conformance

conformance
!= authority

claim issuer
!= claimed publisher
!= claimed location operator
!= claimed Vocabulary authority

claimed publisher
!= verified publisher
!= Vocabulary authority

claimed location operator
!= artifact publisher
!= Vocabulary authority

ability to host bytes
!= authority over Vocabulary

publishing an artifact
!= authority over Vocabulary

unknown publisher attribution
!= invalid Vocabulary edition
!= invalid publication artifact

unknown location-operator attribution
!= invalid Vocabulary edition
!= invalid publication artifact

moving alias
!= exact edition identity

latest/current/stable alias
!= Vocabulary version

discovery alias "stable"
!= lifecycle state "stable"

catalog ordering
!= version ordering
!= compatibility

found
!= preferred
!= authoritative
!= compatible

artifact publisher
!= artifact host
!= Vocabulary authority

authority claim
!= authority proof
!= trust decision

delegation claim
!= verified delegation

description
!= execution

description of permission
!= authorization

semantic state asserted at time T
!= guaranteed live state at time T+n
```

## Alternatives

### Alternative A — Mandatory global registry

One canonical registry could simplify lookup and naming, but it would make a
service operationally privileged, create a network dependency and turn
availability or registry policy into de facto semantic authority. It would
exclude offline and independent implementations. This alternative is
rejected.

### Alternative B — Dereference Vocabulary identity

Treat the Vocabulary IRI as a required URL and whatever it returns as
authoritative current content. This collapses identity into location, makes
results mutable and time-dependent, and cannot represent mirrors or offline
artifacts safely. This alternative is rejected.

### Alternative C — Catalog ranking selects the winner

Use first result, newest timestamp, HTTPS, lexical version order, catalog rank
or vendor preference to pick one artifact automatically. None of those facts
proves semantic authority or compatibility, and ADR-0017 version tokens have
no generic ordering. This alternative is rejected.

### Alternative D — Require cryptographic identity and signatures first

Signatures may later strengthen integrity and origin evidence, but they do not
by themselves prove semantic authority or trust. Making one PKI, DID,
blockchain, certificate or algorithm mandatory would block the abstract model
and violate technology neutrality. This alternative is rejected as a D5
prerequisite.

### Alternative E — Optional claim/evidence catalog with external selection

Define finite inert discovery, authority and stewardship claims. Discovery
returns candidate exact editions, artifacts and locations. Claims retain their
source and may conflict. A caller or explicitly supplied trust policy chooses,
if appropriate, and every reproducible result records the exact edition pair
actually used.

This alternative is proposed. It improves traceability while keeping direct
offline supply and independent implementations first-class.

## Proposed decision

### Offline direct-supply path

Discovery is always optional. A caller can supply:

```text
exact Vocabulary edition pair
+ local publication artifact representing that edition
```

and perform ADR-0018 processing or ADR-0020 assessment without any discovery
record, catalog, registry or network.

```text
discovery unavailable
!= Vocabulary invalid
!= Vocabulary edition invalid
!= SemanticDocument invalid
```

Failure to discover an artifact is an availability/evidence outcome. It does
not change Vocabulary, edition or term identity and cannot retroactively alter
S2 bare-core conformance.

### Abstract discovery claim

A **discovery claim** is a finite inert assertion made by an identified claim
source about a Vocabulary family, exact edition, moving alias, publication
candidate or retrieval location. It is evidence supplied for discovery, not a
fact made true by the standard.

Every discovery claim has, abstractly:

1. one identified claim source or issuer;
2. one exact claim kind;
3. one exact subject appropriate to that kind;
4. the claimed target or value required by that kind; and
5. provenance sufficient to attribute the claim to the supplied source.

A future binding may add claim identity, issue/observation time, validity,
evidence references, labels and documentation. D5 does not select their
serialization or require one universal legal/person identity scheme. An
identifier for a claimant, source, publisher or host identifies the party
named by the claim; possession of that identifier proves neither control nor
authority.

D5 admits these abstract discovery-claim roles:

- **edition candidate** — a Vocabulary-family identity is associated with one
  exact `(Vocabulary identity, Vocabulary version)` candidate;
- **publication candidate** — one exact edition pair is associated with a
  supplied or separately retrievable ADR-0018 publication representation;
- **retrieval-location candidate** — one exact edition pair is associated with
  one inert retrieval-location descriptor; and
- **moving-alias target** — an alias scoped to one Vocabulary identity is
  associated with one exact edition pair for that same Vocabulary.

These roles manufacture no identity, term membership, definition, lifecycle,
compatibility or authority. Claim order is non-semantic.

### Optional discovery record and catalog

An **abstract discovery record** groups a finite set of attributed D5 claims
for processing or exchange. Those claims may include discovery, actor-role,
authority, delegation or stewardship-transfer claims. An **optional discovery
catalog** is a finite collection of such records. Neither is a SemanticDocument,
Vocabulary edition, publication artifact, profile, registry service or
authority proof.

There is no required global catalog and no assumption that a catalog is
complete. Different local bundles, publishers, communities or services may
provide overlapping or conflicting records. A consumer may use zero, one or
several sources.

Conceptually, supplied records can support:

```text
Vocabulary identity
    -> zero or more candidate exact editions

exact Vocabulary edition pair
    -> zero or more publication candidates
    -> zero or more retrieval-location candidates

publication candidate / representation
    -> zero or more claimed-publisher attributions

retrieval-location candidate
    -> zero or more claimed-location-operator attributions

(Vocabulary identity, moving alias)
    -> zero or more claimed exact-edition targets
```

This is an abstract information relationship, not an API, query language or
network protocol. A future binding may represent records in one or more forms
without modifying SemanticDocument core.

### Family discovery versus exact-edition location

Discovering a Vocabulary family returns candidates and does not establish a
reproducible edition. Exact processing continues to depend on the ADR-0017
ordered pair:

```text
(Vocabulary identity, Vocabulary version)
```

Locating an exact edition may return no publication candidate, one candidate
or several representations/mirrors. Knowing the exact pair remains useful even
when no retrieval location is known or the artifact is supplied directly.

Discovery never silently converts a family identity into a selected edition.
A caller or explicit external policy performs selection. A reproducible result
records the exact pair selected and the candidate/evidence context used; a
family identifier, alias or search result alone is insufficient.

### Moving aliases

A moving alias is discovery metadata scoped to one Vocabulary identity. A
single alias-target claim identifies exactly one exact edition pair for that
same Vocabulary. Different records or claim sources may assert different
targets.

Aliases such as `latest`, `current` or `stable` are not reserved Vocabulary
versions and are never exact edition identity while their targets can move.
Resolving an alias does not mutate the alias's former target or any historical
edition.

After an alias is resolved and a caller selects a target, any reproducible
processing or assessment records the exact edition pair actually used. It may
also retain the alias claim, source and temporal context as evidence. A profile
or configuration that says only `latest` cannot silently validate against a
different edition tomorrow while claiming the same reproducible result.

The spelling `stable` has no lifecycle implication:

```text
discovery alias "stable"
!= ADR-0019 lifecycle state "stable"
```

An alias named `stable` may point to an edition declared `experimental`, and a
lifecycle-stable edition may have no `stable` alias. Generic processing makes
no inference between them.

### Retrieval locations and availability

An exact edition may have zero, one or several candidate retrieval locations.
Locations may be mirrors, move, disappear, become temporarily unavailable or
serve conflicting content.

```text
same exact edition
!= same retrieval location

retrieval location
!= instruction to fetch
```

A location is inert discovery metadata. It does not identify the Vocabulary,
edition or artifact; prove availability, authenticity or authority; select an
artifact; or authorize network/filesystem access. D5 defines no location
syntax or retrieval operation.

An availability observation is local and temporal. Availability at one time
does not guarantee availability later, and unavailability does not invalidate
the edition. If content obtained outside D5 claims a different edition pair or
conflicts with other content for the same pair, generic processing preserves
and reports the conflict rather than trusting the location.

### Publisher and claimant attribution

A **claimant** is only the party filling an exact role in a supplied claim. It
is not itself a publisher, location operator or Vocabulary authority role. D5
represents those meanings through separate finite inert **actor-role
attribution claims**. Every such claim identifies:

1. one claim source or issuer;
2. one exact attribution role;
3. one exact subject appropriate to that role;
4. one identified actor claimed to occupy the role; and
5. provenance sufficient to attribute the claim to its issuer.

D5 admits two optional attribution roles:

1. **Publication attribution** — one specific publication candidate or
   publication representation for an exact edition is associated with one
   claimed publisher.
2. **Retrieval-location attribution** — one specific retrieval-location
   candidate for an exact edition is associated with one claimed location
   operator, meaning the actor claimed to host, operate or hold custody of that
   location in the stated claim context.

The subject designator used by a future binding does not grant an artifact a
universal semantic identity or make a location part of edition identity. A
future binding may distinguish narrower host, operator or custodian subroles,
but every claim must select one exact role and generic processing infers no
equality between different roles.

D5 therefore keeps these roles separate:

```text
claim issuer
!= claimed publication-artifact publisher
!= claimed retrieval-location operator
!= claimed Vocabulary authority
```

The same party may occupy several roles only when the supplied claims state
each relationship explicitly; equality is never inferred. The issuer of a
catalog claim may differ from the claimed publisher, and an artifact operated
or hosted by organization H may represent an edition claimed as published by
organization P. Publishing an artifact or being able to host its bytes does
not establish authority for its Vocabulary.

Publication and retrieval-location attribution are both optional and have
`0..*` claim cardinality. Their absence means only that the supplied evidence
does not identify that role:

```text
no publisher attribution available
!= invalid Vocabulary
!= invalid exact edition
!= invalid ADR-0018 publication artifact

no location-operator attribution available
!= invalid retrieval-location candidate
!= invalid exact edition
```

Consequently, neither attribution is needed for direct offline supply or for
mechanical acceptance of the ADR-0018 publication minimum. Multiple claims may
name different publishers or location operators for the same subject.

Attribution makes evidence auditable. It does not verify the claimant's real-
world identity, possession of an IRI, control of a domain, legal status or
right to make the claim.

### Authority claim and scope

An **authority claim** is a finite inert claim in which one identified issuer
asserts that one identified claimant is authoritative for one exact scope. It
is evidence for an external decision, not universal proof or a trust result.

D5 admits two authority-scope kinds:

1. **Vocabulary-family scope** — exactly one ADR-0017 Vocabulary identity.
2. **Vocabulary-edition scope** — exactly one ADR-0017 edition pair.

The scopes remain independent. A family-scoped claim does not mechanically
prove authority for every edition artifact, every publisher or host, or every
external term IRI mentioned by the Vocabulary. An edition-scoped claim does
not prove family-wide stewardship.

Artifact publication, hosting and authenticity are provenance/evidence roles,
not a third semantic-authority scope. Likewise, D5 introduces no term-level
authority claim. Terms may appear in several edition or cross-Vocabulary
claims; authority/equivalence at that granularity depends on D7 and external
governance rather than implicit propagation.

An authority claim may be a self-claim or a third-party claim and may cite
optional evidence. Generic processing preserves issuer, claimant, scope and
evidence relationships. It does not decide whether the issuer was entitled to
grant authority or whether the claim should be trusted.

### Trust boundary

Trust is contextual local policy. Two consumers may receive identical
discovery, publication and authority evidence and reach different trust or
selection decisions without changing any Vocabulary, edition, term, artifact
or conformance identity.

D5 creates no universal `trusted: true`, globally trusted registry, mandatory
root authority or preferred publisher. A trust decision belongs to explicitly
supplied consumer/application/profile policy outside generic D5 conformance.
When a policy selects a candidate, a reproducible processing report should
retain the exact edition pair, selected publication evidence and enough policy
context to distinguish that decision from another policy's result. Exact
policy serialization and profile integration are deferred.

```text
mechanically conforming artifact
!= trusted artifact
!= authoritative artifact
```

### Authenticity and integrity boundary

Authenticity and integrity evidence may support external decisions, but D5
selects no fingerprint, signature, canonicalization, key, certificate, DID,
DNS proof or verification algorithm.

```text
artifact bytes intact
!= artifact semantically authoritative

cryptographically authentic
!= authoritative
!= trusted

signed
!= accepted by local trust policy
```

A future binding may carry or reference finite authenticity/integrity evidence
and its provenance. Until the corresponding mechanism is accepted, generic D5
processing treats it as attributed inert evidence and does not invent a
verified result. Artifact conformance under ADR-0018 and constraint
conformance under ADR-0020 remain separate from authenticity, authority and
trust.

### Competing and conflicting claims

Multiple candidates and disagreements are first-class outcomes. Generic
processing does not automatically choose by:

- first seen or last seen;
- newest timestamp;
- lexical Vocabulary-version order;
- HTTPS or another location scheme;
- URL or host ownership;
- catalog order or ranking;
- moving-alias spelling;
- vendor preference; or
- artifact format.

At minimum, processing preserves and can report these conflict classes:

1. several sources claim different targets for the same moving alias;
2. several sources attribute different publishers to the same publication
   candidate or representation;
3. several sources attribute different operators to the same retrieval-
   location candidate;
4. publication attribution and authority claims name different parties for
   related evidence;
5. several authority-claim issuers name different claimants for the same
   family or edition scope;
6. several locations/artifacts claim one exact pair but provide conflicting
   normative semantic content; and
7. several authority sources assert incompatible claimant/delegation claims.

A disagreement between a publication attribution and an authority claim is
not resolved by treating publisher as authority or authority as publisher.
Likewise, conflicting publisher/location attributions do not invalidate an
otherwise conforming exact edition or artifact. Each claim retains its issuer,
subject, exact role, claimed actor and provenance, and generic processing
selects no winner.

Equivalent artifacts may represent the same edition under ADR-0018/0020. When
artifacts claiming the same pair differ in normative semantic content, they
are conflicting publication claims and violate ADR-0017 immutability. Generic
processing may detect mechanically observable differences but is not required
to prove semantic equivalence of definitions or abstract constraints.

The generic result may remain `conflicting claims` with no winner. Evidence
and provenance are retained so an external trust/governance policy can decide
or decline to decide.

### Delegation and stewardship transfer claims

Vocabulary identity remains stable when stewardship changes. D5 admits two
minimal authority-relation claim roles:

- **delegation claim** — an issuer asserts that a purported delegator grants a
  claimant authority for one exact family or edition scope without necessarily
  ending the delegator's role; and
- **stewardship-transfer claim** — an issuer asserts that stewardship for one
  exact family or edition scope moves from one claimant to another.

Each claim identifies issuer, purported source claimant, recipient claimant
and exact authority scope. A future binding may add effective time, validity,
evidence and rationale.

Neither claim proves that the purported delegator originally possessed the
authority, that the transfer is exclusive, that another claim is revoked, or
that signatures have been verified. A transfer claim does not change the
Vocabulary identity, mutate historical editions or erase earlier evidence.
Conflicting delegation/transfer claims remain visible for external policy.

```text
delegation claim
!= verified delegation
!= automatic trust transfer
```

### Minimal D5 governance

Governance in D5 means only the rules needed to exchange claims without losing
their scope or provenance:

1. attribute each discovery, actor-role, authority and delegation claim to its
   supplied source;
2. identify family versus exact-edition scope;
3. keep moving aliases separate from exact edition identity and record the
   exact resolved pair used by reproducible processing;
4. preserve competing claims and avoid hidden precedence;
5. keep trust decisions external and contextual;
6. allow optional finite catalogs and direct offline artifacts; and
7. keep old supplied evidence interpretable rather than treating catalog
   disappearance as deletion or revocation.

D5 defines no official GeesNO.org process, voting, steering committee, package
publication workflow, certification, contributor policy, trademark policy or
legal authority. Those belong to later S10/legal governance if needed.

Discovery records are supplied snapshots of claims. A later record or catalog
does not mutate an earlier one or an exact Vocabulary edition. D5 requires no
event replay, global current-state oracle or permanent archival service.

### Lifecycle interaction

ADR-0019 lifecycle and D5 discovery remain independent:

```text
deprecated Vocabulary
!= undiscoverable Vocabulary

retired term
!= hidden term

stable lifecycle state
!= discovery alias "stable"
```

Catalogs may continue to locate historical, deprecated or retired editions and
terms. Removing a discovery record does not retire a Vocabulary; lifecycle
status does not require hiding an artifact. No history is deleted by inference.

### D4 exact-selection interaction

D5 may find candidates for ADR-0020, but:

```text
discovery result
!= D4 exact-edition selection
```

D4 assessment begins only after the caller or explicit external policy selects
one exact edition and supplies a supported artifact/representation. Resolving
a moving alias produces candidate evidence; the exact pair actually selected
must be retained. D5 does not authorize hidden `latest` behavior or modify D4
payload semantics.

### D6 and D7 boundaries

D5 does not decide the GeesNO Base Vocabulary identity, preferred prefix/base,
admission criteria or initial term set. Those belong to D6.

A catalog may carry attributed claims about compatibility, equivalence,
mappings, substitutability, version ranges or migration, but D5 treats them as
unsupported descriptive claims. It does not make them true or use them for
generic selection. Their abstract semantics and profile-to-Vocabulary rules
belong to D7.

### Deterministic generic processing

A future concrete binding must let a generic processor validate mechanically,
without network or semantic judgement:

- admitted claim kinds and their required subject/target roles;
- Vocabulary-family and exact-edition identity relationships;
- alias scoping and exact target-pair shape;
- location-descriptor syntax selected by that binding;
- issuer, publication-attribution, location-attribution, claimant, authority-
  scope and delegation relationships;
- optional attribution cardinality and explicit same-subject conflicts without
  requiring publisher or location-operator knowledge;
- cardinality, duplicate and locally explicit conflict rules;
- provenance/evidence association; and
- bounded finite processing.

Generic conformance never answers `who should be trusted?`, proves legal
ownership, establishes authority, orders opaque version tokens, selects a
preferred candidate or requires human/LLM interpretation. A mechanically valid
claim may still be false, malicious, stale, unauthorized or untrusted.

D5 fixes no JSON members, schema, diagnostic codes, API operations, catalog
media type or network behavior. Those require a later concrete binding and
cannot modify SemanticDocument or S2 Layers 0–3.

### Security and execution boundary

Discovery records, catalogs, artifacts, evidence, identifiers, locations,
URLs, endpoint strings and instruction-like text are untrusted inert data.
They do not:

- trigger automatic network, filesystem, package or IRI access;
- execute scripts, commands, queries, tools, plugins, adapters or agents;
- activate MCP/API calls or load credentials;
- grant permission, authority, authentication or trust;
- invoke a described endpoint;
- weaken validation, privacy, redaction or lifecycle rules; or
- introduce a GeesNO.Core dependency.

```text
discovery entry
!= instruction to fetch

endpoint description
!= authorized endpoint invocation
```

Any retrieval is a separately authorized application operation outside D5.
Implementations apply bounded resource and input-safety controls to supplied
metadata and artifacts.

## Cross-domain validation

| Domain | Discovery/authority stress case | Result under the proposal |
| --- | --- | --- |
| Engineering-like object graph | A standards body edition is mirrored by a vendor and an industry archive. | Publication attribution and each mirror's location-operator attribution remain distinct; hosting proves neither publisher identity, authority nor compatibility and adds no engineering primitive. |
| Spreadsheet/table | A private business Vocabulary and artifact are bundled offline with a workbook consumer. | Direct supply needs neither discovery nor publisher/operator attribution, cloud account or spreadsheet adapter; exact edition processing remains reproducible. |
| Technical/legal document | Two organizations dispute stewardship of a legal terminology family while archived editions remain cited. | Publisher, authority and transfer claims remain separate and attributed; no global trust winner or deletion of historical evidence is inferred. |
| Source-code repository | A community Vocabulary moves hosting organizations and a catalog's `latest` alias changes. | Vocabulary/edition and claimed publisher remain independent of host, location and alias; the exact resolved pair is retained without Git semantics. |
| Scientific dataset | An offline archive contains an edition omitted by an online discipline catalog and has no operator attribution. | Catalog completeness and operator knowledge are not assumed; local exact artifacts remain valid and lifecycle/currentness is not inferred. |
| Generic product/asset data | Vendor and community catalogs attribute different publishers and authorities for one publication candidate. | Generic processing reports role-specific attributed claims/conflicts; vendor rank, URL and publication order provide no automatic winner or authority. |

All six domains use the same claim, scope, evidence, exact-edition and external-
trust model. None requires a domain field, product adapter, central registry,
network protocol, signature technology or execution primitive.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| 1. Exact edition is available locally with no discovery service | Valid direct-supply path. ADR-0018/0020 processing can proceed offline from the exact pair and artifact. |
| 2. Registry or catalog is unavailable | Availability failure only. Vocabulary, exact edition, SemanticDocument and locally supplied artifacts are not invalidated. |
| 3. Same exact edition is listed at two URLs | Valid candidate mirrors. URL equality is not edition or artifact equality, and neither URL is automatically preferred. |
| 4. Artifact moves to a new URL | Vocabulary and edition identities remain unchanged. Old/new locations are time-scoped discovery evidence, not semantic mutation. |
| 5. One URL serves conflicting normative content for the same edition pair | Conflicting publication claim under ADR-0017/0018. The URL grants no winner or authority; preserve supplied artifacts/evidence. |
| 6. Two catalogs disagree about `latest` | Conflicting moving-alias claims. Return both attributed candidates or no generic selection. |
| 7. Moving `latest` changes tomorrow | Earlier exact edition and resolution result remain unchanged. Future processing must record the new exact pair rather than pretending reproducibility from the alias alone. |
| 8. Discovery alias `stable` points to an edition whose lifecycle is `experimental` | Mechanically possible. Alias spelling and ADR-0019 lifecycle are independent; no lifecycle inference or automatic rejection follows. |
| 9. A lifecycle-`stable` edition is not mapped by alias `stable` | Valid. Lifecycle does not create or require discovery aliases. |
| 10. Two publishers claim the same Vocabulary identity | Competing publisher/authority claims. Generic processing records provenance and selects no owner automatically. |
| 11. Publisher and artifact host are different organizations | Valid and explicitly representable. Hosting does not imply publication authority or Vocabulary stewardship. |
| 12. Organization A transfers stewardship to organization B | Vocabulary identity may remain stable. Record an attributed transfer claim with exact scope; do not mutate editions or erase earlier evidence. |
| 13. Delegation claim exists but cannot be cryptographically verified | Preserve it as unverified attributed evidence. It is neither authority proof nor a trust result and does not block abstract D5 conformance. |
| 14. Artifact is cryptographically authentic but signer is not trusted | Authenticity evidence does not imply authority or trust. External policy may reject or ignore it. |
| 15. Trusted source points to an unavailable artifact | Trust does not create availability. Report selected/trusted evidence separately from retrieval failure. |
| 16. Untrusted catalog points to a mechanically valid artifact | Artifact conformance and catalog trust are independent. A policy may inspect or reject the candidate; bare identity remains unchanged. |
| 17. Discovery record contains malicious URLs or instruction-like strings | Inert untrusted data. No dereference, credential use, MCP/API call, plugin activation or execution occurs. |
| 18. Exact edition pair is known but no retrieval location is known | Valid discovery knowledge. The artifact may be supplied out of band or remain unavailable; the pair is still exact identity. |
| 19. Several artifacts claim the same pair and same semantics | Permitted equivalent representations under ADR-0018/0020 when their normative semantic content is the same; generic processing need not prove semantic equivalence. |
| 20. Several artifacts claim the same pair but conflicting semantics | Conflicting publication claims violating edition immutability. Preserve evidence and report conflict with no hidden winner. |
| 21. A catalog claims one edition is compatible with another | D5 treats this as attributed descriptive metadata only. It does not establish compatibility; D7 owns those semantics. |
| 22. A D4 consumer discovers multiple editions but needs one exact edition | Discovery returns candidates only. Caller/policy must select and record one exact pair before reproducible Extension-aware assessment. |
| 23. Deprecated or retired Vocabulary remains discoverable | Valid and desirable for historical interpretation. Lifecycle does not require hiding or deleting publication evidence. |
| 24. Offline bundle contains an edition newer than an online catalog claims is current | Both are evidence; generic processing infers neither version order nor global currentness and does not prefer the online claim. |
| 25. Two authority/trust policies choose different claims from identical evidence | Valid contextual divergence. Vocabulary, edition, term and artifact conformance identities remain unchanged; reports should identify their policy context. |

Publisher and location attribution add these focused adversarial refinements
without replacing the cases above:

| Attribution case | Proposed classification |
| --- | --- |
| A. Catalog C issues a claim that publication representation A was published by organization P | Preserve C as claim issuer and P as claimed publisher. The claim is finite attributed evidence; it neither verifies P nor establishes Vocabulary authority. |
| B. Publication representation A is available at a location operated by H, with `P != H` | Publication attribution to P and location attribution to H coexist explicitly. Hosting/operation proves neither publication nor Vocabulary authority. |
| C. Another source claims organization Q as publisher of the same publication representation A | Preserve both publisher-attribution claims, their issuers and provenance as a conflict; generic processing selects no publisher automatically. |
| D. Publisher attribution exists but no authority claim exists | Valid incomplete evidence. Publishing does not imply authority, and no authority result is invented. |
| E. An authority claim names P while publication attribution names Q | Preserve both claims and their distinct roles. The mismatch is reportable evidence, not an implicit winner, invalid artifact or authority transfer. |
| F. No publisher attribution is available | Publisher is unknown. Vocabulary/edition identity, direct offline supply and mechanical ADR-0018 artifact acceptance remain unaffected. |
| G. No location-operator attribution is available | Location operator is unknown. The location remains an inert candidate and the edition/artifact is not invalidated. |

## Consequences

- Direct offline exact-edition processing remains a complete first-class path.
- Optional catalogs can improve findability without becoming identity,
  authority or a global registry requirement.
- Moving aliases are usable for discovery while reproducible results remain
  anchored to exact immutable edition pairs.
- Multiple locations and mirrors do not fragment edition identity.
- Optional publication/location actor-role claims make publisher and operator
  attribution explicit without making either role required or authoritative.
- Attribution, authority and stewardship claims become exchangeable evidence
  without creating universal trust or cryptographic proof.
- Competing claims remain visible instead of being resolved by arbitrary
  ranking or hidden online state.
- Historical and lifecycle-marked editions remain discoverable.
- Concrete bindings, integrity technology, trust policies, D6 content and D7
  compatibility remain explicit future decisions.
- No SemanticDocument field, S2 rule, registry, service, signature, Base
  Vocabulary, profile, SDK or adapter follows from this Proposed ADR.

## Remains open

- concrete discovery-record/catalog serialization, media type, binding version,
  canonical member names and schema;
- exact identifier representations for claim sources, claimants, publishers,
  location operators and optional claim records;
- concrete subject designation and narrower host/operator/custodian role kinds
  for publication/location actor-role attribution;
- exact retrieval-location descriptor kinds and lexical rules;
- exact issue/observation time, validity, provenance and evidence structures;
- concrete alias syntax, collision rules and catalog versioning;
- discovery transport, caching and optional network protocols;
- fingerprints, signatures, canonical bytes, keys, certificates,
  authentication and integrity threat model;
- concrete trust-policy identity, configuration and result-reporting format;
- mature diagnostic identifiers and severities;
- D6 GeesNO Base Vocabulary identity, admission criteria and initial terms;
- D7 compatibility, mappings, equivalence, substitutability, ranges,
  migrations and profile-to-Vocabulary rules;
- official registry, certification, voting, stewardship organization,
  contributor, trademark and legal governance under later S10 work; and
- any public release or official GeesNO.org discovery service.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-15. Acceptance covers optional offline/direct supply,
finite attributed discovery and actor-role claims, family versus exact-edition
discovery, non-identifying retrieval locations, exact-pair moving aliases,
family/edition authority scopes, external contextual trust, competing claims,
delegation/stewardship, lifecycle independence, deterministic processing and
the security boundaries recorded above.

Acceptance closes D5. It does not itself choose or implement a discovery
serialization/service, registry, transport, signature/integrity mechanism,
trust policy, Base Vocabulary, D7 compatibility rule, profile, schema, fixture,
SDK, adapter or execution behavior, and it does not authorize D6 or D7.
