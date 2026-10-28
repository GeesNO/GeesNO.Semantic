# ADR-0020: Extension Vocabulary authoring and payload-compatibility conventions

- **Status:** Accepted
- **Date:** 2026-09-13
- **Accepted by:** Explicit human architecture decision on 2026-09-14
- **Decision order:** Fourth S3 architecture decision after accepted ADR-0019

## Context

Accepted ADR-0015 fixes the S2 Extension boundary: one optional `extensions`
map on a closed set of semantic record hosts, ADR-0010-qualified keys,
arbitrary inert JSON payloads, bare-core acceptance of unknown Extensions,
lossless-preservation obligations and no core override. S3 may define how a
Vocabulary describes additional meaning above that boundary, but it cannot
change the boundary itself.

Accepted ADR-0017 identifies immutable Vocabulary editions and keeps term IRI
identity independent from Vocabulary version. Accepted ADR-0018 requires one
normative definition for every member term in an edition. Accepted ADR-0019
adds edition-scoped lifecycle declarations without making deprecated or
retired terms invalid occurrences.

D4 must now define how a publisher can state that an existing Vocabulary term
is intended for use as an Extension key, describe the payload through the
term's single normative definition, optionally restrict that use to existing
S2 Extension hosts, and optionally provide an abstract deterministic payload
contract.
It must also define reproducible assessment outcomes without making
Vocabulary availability a dependency of S2 bare-core conformance.

This ADR proposes only the serialization-independent D4 model. It does not
choose a publication serialization, constraint language, profile-selection
mechanism, discovery service, authority model, schema, fixture, SDK or Base
Vocabulary.

## Prerequisite review

No unresolved prerequisite blocks D4:

1. Foundation supplies the universal, descriptive, inert, offline-capable and
   serialization-independent boundary.
2. ADR-0010 supplies the absolute term IRI obtained by expanding an Extension
   key and forbids automatic dereference or registry dependence.
3. ADR-0015 fixes the complete S2 host, key, arbitrary-JSON, unknown-
   Extension, preservation and no-override contract that D4 must not alter.
4. ADR-0016 freezes S2 `0.1.0`, exact unknown-payload number preservation and
   bare-core Layers 0–3; Extension understanding remains outside those layers.
5. ADR-0017 supplies exact immutable Vocabulary edition identity and the rule
   that incompatible denoted meaning requires a new term IRI.
6. ADR-0018 supplies a finite inert edition artifact, explicit term membership
   and exactly one publisher-declared normative definition per term.
7. ADR-0019 supplies lifecycle semantics that apply to Extension terms without
   inventing a second Extension-specific lifecycle.

Concrete publication binding, selection syntax, discovery/authority, Base
Vocabulary admission, cross-edition compatibility, profile requirements,
mature diagnostics and tooling are downstream. They are not required to define
the abstract contract and assessment boundaries below.

## Requirements

The model must:

- preserve every accepted S2 Extension host, key, payload, preservation,
  closed-core and version-dispatch rule unchanged;
- keep the expanded absolute term IRI as Extension-key identity;
- reuse the term's one ADR-0018 normative definition rather than creating a
  second potentially incompatible definition;
- let that definition state the meaning of the key and its arbitrary JSON
  payload;
- optionally restrict a term's Extension use to a non-empty subset of the
  existing S2 Extension hosts without creating a new host;
- optionally associate one deterministic abstract machine-checkable payload
  contract with that term use;
- keep the abstract contract separate from its declarative representation,
  constraint-language identity/version, payload meaning and ADR-0012 core
  values, conditions and quantities;
- permit different publisher-declared equivalent representations of the same
  abstract contract without making representation syntax semantic identity;
- preserve bare-core validity and lossless processing when a Vocabulary,
  edition, term or constraint language is unknown or unavailable;
- distinguish bare-core conformance from Extension-aware assessment;
- make every Extension-aware result relative to one explicitly selected exact
  Vocabulary edition, never a moving alias or hidden latest version;
- distinguish invalid payload from unavailable edition, undefined term,
  unsupported publication binding or constraint language and absence of a
  machine-checkable contract;
- require no network, registry, dereference, plugin, proprietary validator,
  LLM or subjective semantic judgement;
- inherit ordinary ADR-0019 lifecycle without turning deprecation or
  retirement into deletion or bare-core invalidity;
- keep requirement policy in profiles rather than Vocabularies; and
- remain domain-, format-, vendor-, software- and AI-provider-neutral.

## Controlling distinctions

```text
Extension key identity
!= Vocabulary edition identity

term normative definition
!= Extension-use declaration

payload semantic meaning
!= abstract machine-checkable payload contract
!= constraint representation
!= constraint-language identity/version

abstract payload contract
!= Vocabulary semantic identity
!= term identity

payload conformance to one selected edition
!= compatibility between Vocabulary editions

arbitrary Extension JSON
!= ADR-0012 Property value
!= ADR-0012 condition
!= ADR-0012 measured quantity

allowed S2 Extension host
!= Vocabulary-declared applicable host
!= profile-required occurrence

bare-core conformance
!= Extension-aware assessment
!= profile conformance

selected exact edition
!= discovered edition
!= authoritative edition
!= compatible edition
!= moving latest alias

Vocabulary conformance
!= publisher authority
!= permission
!= execution

description of an operation, capability, limit or permission
!= operational binding, enforcement, authorization or execution
```

## Alternatives

### Alternative A — Make every Extension payload an ADR-0012 value

This would provide one existing typed-value contract, but it would contradict
ADR-0015's accepted arbitrary-JSON boundary and make raw numbers, `null`,
ordinary arrays and objects invalid or silently reinterpret them as core
values. It would reopen S2 and is rejected.

### Alternative B — Put payload schemas in the S2 SemanticDocument

Embedding Vocabulary editions or payload schemas in new core fields would
change the frozen S2 member inventory, couple bare-core validity to D4 and
create a second document dialect. It is rejected.

### Alternative C — Dereference the key IRI and validate the latest contract

This would make identity behave as location, make results change over time,
break offline reproducibility and introduce hidden authority. It is rejected.

### Alternative D — Require an executable plugin per Extension

An executable validator could express arbitrary rules, but it would turn
Vocabulary data into code loading, execution and a security boundary outside
GeesNO.Semantic's scope. It is rejected.

### Alternative E — Edition-scoped declarative Extension-use contract

An edition may optionally designate one of its existing terms for Extension-
key use, reuse that term's one normative definition for key and payload
meaning, optionally narrow its applicable existing hosts and optionally add a
deterministic abstract payload contract. One or more finite declarative
representations may express that contract under future binding rules. A
separately supplied external context selects the exact edition for an
Extension-aware assessment.

This alternative is proposed. It adds reproducible semantic and mechanical
assessment above S2 without altering bare-core processing.

## Proposed decision

### Extension Vocabulary and Extension-use declaration

An **Extension Vocabulary** is not a privileged artifact class. It is a
Vocabulary edition governed by ADR-0017/0018 that contains one or more member
terms with an **Extension-use declaration**. The same edition may also contain
terms used in other semantic roles.

An Extension-use declaration is finite, inert normative content of exactly one
Vocabulary edition and is associated with exactly one absolute term IRI. The
term MUST be a member with a normative definition in that exact edition under
ADR-0018. Within one edition, at most one Extension-use declaration may be
associated with the same term IRI.

The declaration states that the publisher defines that term for possible use
as an ADR-0015 Extension key. It MAY also carry:

1. one optional applicable-host set; and
2. one optional abstract machine-checkable payload contract.

The declaration creates no record identity, alternate term identity, new
Extension occurrence form or global registration. Its exact member names,
placement and serialization are deferred to the concrete Vocabulary
publication binding.

An Extension-use declaration is optional. A Vocabulary term without one can
still occur as a structurally valid S2 Extension key because bare core does not
load Vocabularies. Under this D4 convention, however, that edition supplies no
Extension-specific assessment contract for the term. A profile may later
require such a declaration, but D4 does not.

### One normative meaning and payload semantics

The required ADR-0018 normative definition remains the single normative
definition of the term. D4 does not add a second prose definition or allow an
Extension-use declaration to contradict it.

For a term with an Extension-use declaration, the publisher declares that the
term's single normative definition expresses:

- what the Extension key denotes on its host; and
- how the arbitrary JSON payload contributes to that denoted meaning.

The definition may describe raw JSON scalar kinds, object members, arrays,
units, references or another domain convention, but those descriptions remain
the Vocabulary's semantics. They do not promote payload structures into core,
make nested object member names ADR-0010 terms automatically, or authorize a
generic processor to invent meaning not stated by the edition.

This is a publisher's normative semantic claim, not a generic sufficiency
test. ADR-0018's mechanical boundary remains controlling: generic validation
can require that the definition component is present and expose it, but it
does not judge its truth, precision, quality, correctness or adequacy.
Publisher and future D5 governance own semantic quality.

### Host applicability

An Extension-use declaration MAY contain one non-empty finite set of
applicable host kinds. Every member MUST be one of the hosts already permitted
by ADR-0015:

```text
SemanticDocument
Entity
Assertion
Source
Binding
Revision
Tombstone
Change
Provenance
Confidence
Review
```

The set is unordered and contains no duplicate host kind. `Entity` covers the
accepted `Concept` and `Representation` kinds, and `Assertion` covers all four
accepted categories; D4 does not create narrower serialized host variants.
The names above identify accepted abstract host kinds, not frozen Vocabulary
serialization tokens.

When the set is present, occurrence on an allowed S2 host outside that set is
Extension-aware nonconformance relative to the selected exact edition. The
same occurrence remains bare-core valid when all ADR-0015/0016 rules hold.

When the set is absent, the Vocabulary imposes no additional host restriction
beyond ADR-0015. Absence does not authorize use on objects that S2 does not
expose as Extension hosts. A Vocabulary declaration naming any non-S2 host is
invalid publication content under D4 and can never make such an occurrence
bare-core valid.

Host applicability expresses where the term is meaningful as an Extension.
It does not require the Extension to occur, set cardinality across documents,
or create conditional obligations. Requirement and occurrence policy belongs
to profiles.

### Optional machine-checkable payload constraint

The optional machine-checkable payload constraint has two distinct levels:

```text
abstract machine-checkable payload contract
!= concrete constraint representation
```

#### Abstract payload contract

An Extension-use declaration MAY contain one **abstract machine-checkable
payload contract**. The contract is a deterministic normative relation over
the ADR-0015 arbitrary JSON payload:

```text
contract P + payload
    -> accept | reject
```

For the same contract and payload, the abstract result is the same. A resource
refusal, unsupported representation or unavailable evaluator is a processing
outcome that prevents assessment; it is not a third semantic result of `P`.
D4 does not require a complete mathematical formalization or a canonical
predicate language for expressing this relation.

The abstract contract is normative Extension-contract content of the exact
declaring Vocabulary edition. It supplements but does not replace the term's
single normative semantic definition. It defines payload acceptance for
Extension-aware assessment, but it is not:

- executable behavior, a callback or an operational guard;
- an ADR-0012 value system or a transformation of the payload;
- proof of semantic truth, publisher authority or profile conformance;
- a declaration of compatibility with another edition; or
- permission to add an S2 host, loosen core validation, supply a missing core
  member or override core meaning.

Absence of an abstract contract means **no machine-checkable payload contract
supplied by that edition**. It does not mean every payload satisfies the
term's semantics, that the semantics are absent, or that a generic processor
has proved semantic conformance. The normative definition may still describe
the payload for human or domain-aware interpretation.

#### Constraint representation

A **constraint representation** is finite inert declarative data through which
a publication artifact expresses the edition's abstract contract. A concrete
representation identifies its constraint language and exact language version
and carries the corresponding constraint component. These identify how to
interpret that representation; they are not term identity, Vocabulary edition
identity or the abstract contract's semantic identity.

One representation in language A and another in language B MAY represent the
same abstract contract `P` when the publisher declares that both preserve the
same payload acceptance semantics. The same applies to different declarative
formulations in one language. A representation-only change does not
automatically change the Vocabulary edition.

A future concrete publication binding must decide:

- how the abstract contract and each representation are associated;
- how constraint-language identity and exact version are represented;
- whether one artifact may carry one or several claimed-equivalent
  representations;
- duplicate and conflicting-representation handling;
- deterministic syntax and evaluation inputs; and
- bounded resource processing and reporting.

D4 chooses none of those serialization details and no concrete constraint
language. In particular, it does not select JSON Schema, SHACL, ShEx, JTD,
CDDL, CEL, JSONPath, JavaScript, Python or any vendor validator.

A generic processor is not required to prove that two representations express
the same abstract relation. It may validate the deterministic shape of a
representation it understands and evaluate it over particular payloads. The
publisher's equivalence claim remains a governance/integrity claim unless a
mechanical comparison actually exposes a conflict.

An implementation evaluates only representations whose publication binding,
constraint language and exact versions it explicitly supports. Every required
artifact and representation must be supplied through the explicit assessment
context; no network or IRI dereference is required. The evaluator is locally
chosen software controlled by the implementation. It never downloads or
executes code named by an artifact. An unsupported representation, language or
version produces a not-assessed outcome, not payload nonconformance and not
bare-core invalidity.

### No second core value system

The abstract contract relates to the Extension payload as the ADR-0015
arbitrary JSON data supplied at that occurrence. A supported constraint
representation evaluates that same payload without changing its semantic
category. D4 introduces no alternate universal value envelope and performs no
implicit conversion to ADR-0012.

- a raw JSON number stays an Extension number with no inferred datatype, unit,
  precision or numeric equality;
- `null` stays opaque data and does not become absent, unknown,
  not-applicable or redacted;
- an object stays an Extension object, not an ADR-0012 structured value;
- an array keeps payload order and duplicates and does not become an ADR-0012
  list or set; and
- a string is not inferred to be an identifier, reference, IRI, date, unit or
  qualified term unless the selected Vocabulary contract explicitly gives it
  that Extension-specific meaning.

If a Vocabulary deliberately requires an ADR-0012 representation inside its
payload, that is an Extension-specific constraint and interpretation. It does
not create a second canonical occurrence form for a core value or cause bare
core to interpret the payload.

Accepted ADR-0016 exact numeric-token preservation remains unchanged. A later
constraint-language binding must state its numeric and lexical evaluation
model without coercing or losing accepted payload tokens. D4 itself declares
no numeric equivalence.

### Payload-compatibility scope

In D4, payload compatibility is an occurrence-level assessment against one
exact selected edition. It asks whether the Extension occurs on an applicable
host and, when an abstract machine-checkable contract and a supported
representation exist, whether that representation evaluates the payload as
accepted by the edition's abstract contract. The result is semantically about
the abstract contract, not an identity conferred by the representation
language. It does not prove semantic truth, publisher authority,
interoperability with another edition, substitutability or a safe migration.

When no machine-checkable contract is supplied or supported, mechanical
payload compatibility is not assessed. Generic processing must not convert
the absence of a negative result into a positive compatibility claim.
Compatibility between Vocabulary editions or profiles remains D7.

### Bare-core conformance and Extension-aware assessment

Every processor keeps two independent results:

1. **Bare-core conformance** applies the exact `spec_version` contract and S2
   Layers 0–3. It has its accepted valid, invalid, unsupported-version and
   resource-refusal outcomes. No Vocabulary is needed.
2. **Extension-aware assessment** optionally evaluates an Extension occurrence
   against an explicitly selected exact Vocabulary edition and its D4
   declaration. It never repairs or weakens a bare-core failure.

Extension-aware reporting must retain enough orthogonal information to
distinguish at least:

- exact edition selected and available, or exact edition unavailable/unknown;
- edition artifact supplied but its publication binding/version or required
  deterministic feature unsupported;
- term defined, term not defined, or term defined without an Extension-use
  declaration;
- host applicable, host disallowed by that declaration, or no additional host
  restriction;
- abstract payload contract present or absent;
- payload mechanically conforming or nonconforming when evaluated through a
  supported representation of the selected edition's abstract contract;
- payload not mechanically assessed because the edition supplies no
  abstract machine-checkable contract; and
- payload not mechanically assessed because the artifact representation,
  publication binding, constraint language or exact version is unsupported.

These are semantic result categories, not frozen diagnostic codes. Mature code
names, severity policy and report serialization belong to S5 or a concrete
binding.

An unavailable/unknown edition, unsupported edition artifact, undefined term,
missing declaration, absent machine contract or unsupported constraint
representation/language MUST NOT be mislabeled as payload nonconformance.
Conversely, a supported representation of the selected abstract contract that
deterministically rejects a payload produces Extension-aware nonconformance
relative to that exact edition even when the occurrence is bare-core valid.

An Extension occurrence receives an Extension-aware **conforming** payload
result only when the selected exact edition is available and supported, the
term and Extension-use declaration are present, host applicability succeeds,
the abstract contract is present, and a supported representation accepts the
payload. Any missing assessment input is reported with the more precise
not-assessed category above rather than being treated as success.

If two supported representations claiming the same edition and abstract
contract produce different accept/reject results for the same payload under
their declared evaluation inputs, the artifacts expose a conflicting
publication/contract claim. Generic processing reports the conflict and the
separate evidence. It does not choose a winner by timestamp, retrieval
location, preferred language or hidden authority, and it does not collapse the
conflict into one payload-conformance result.

### Exact edition selection and reproducibility

Extension-aware assessment occurs only when external processing context
explicitly selects one exact ADR-0017 pair:

```text
(Vocabulary identity, Vocabulary version)
```

and supplies an artifact representing it. Mechanical payload assessment also
requires a supported publication binding, a supported representation of the
abstract contract, and a locally supported constraint language and exact
version. The selection may eventually come from a profile, configuration,
bundle or another explicit caller-provided context. D4 does not choose that
mechanism and adds no field to SemanticDocument.

A term IRI or namespace base alone does not select an edition. A retrieval URL,
publication timestamp, moving `latest`/`current`/`stable` alias, registry
preference or whatever happens to be online cannot silently select or replace
one. An implementation MUST NOT fetch a newer edition or follow a link during
assessment unless a separate explicitly authorized application operation does
so outside D4 conformance.

The assessment report identifies the exact selected edition. The same
bare-core-valid occurrence may receive different Extension-aware results under
two exact editions, and both results are reproducible claims about their
respective contracts. D4 does not infer which edition is newer, compatible,
preferred or authoritative.

The semantic accept/reject result is relative to the abstract contract of the
selected edition. The concrete representation, binding and constraint-language
versions used are reproducibility evidence and processing inputs, not hidden
components of the Extension term or Vocabulary semantic identity. Unsupported
evidence produces unsupported/not assessed, never payload nonconformance.

### Evolution of Extension payload contracts

An Extension-use declaration, its applicable-host set and its abstract
machine-checkable payload contract are normative Extension-contract content
of the declaring edition. Adding or removing that normative content, or
changing its semantics, requires a new Vocabulary version. A publisher MUST
NOT change it in place under the same edition pair.

A constraint representation is an expression of the abstract contract, not
the contract's semantic identity. Consistently with ADR-0018 artifact and
definition representations, different files, serializations, bindings,
constraint languages or declarative formulations MAY represent the same
edition when the publisher declares that they preserve the same abstract
contract and payload acceptance semantics. Representation difference alone
does not automatically require a new Vocabulary version.

Term identity follows ADR-0017 independently:

1. If a change incompatibly changes the meaning denoted by the key or payload,
   the new edition MUST use a new term IRI as well as a new Vocabulary version.
2. Changing from no abstract machine-checkable contract to contract `P`
   changes normative assessment expectations and requires a new Vocabulary
   version. It does not require a new term IRI when denoted meaning remains
   compatible.
3. Changing from contract `P1` to `P2` requires a new Vocabulary version when
   the normative payload acceptance relation changes. This includes a
   material narrowing, broadening or other change in which payloads are
   accepted or rejected. The term IRI MAY remain stable only when its denoted
   meaning remains compatible.
4. Removing an abstract contract likewise changes normative assessment
   expectations and requires a new Vocabulary version.
5. Changing representation A to publisher-declared equivalent representation
   B, including a change of declarative language or language version, MAY
   retain the same Vocabulary edition when term meaning, host applicability
   and abstract acceptance semantics remain unchanged.
6. Generic processing is not required to prove representation equivalence.
   The publisher's claim is subject to governance/integrity review. If two
   representations claiming one edition produce observably different results
   for the same payload, they are conflicting publication/contract claims,
   not two silently valid meanings of one immutable edition. No timestamp,
   location or language preference chooses a winner.
7. A stricter or looser abstract contract is not automatically declared
   compatible or incompatible with another edition merely because the term
   IRI is unchanged. D7 owns cross-edition and profile compatibility.
8. Every validation result remains relative to the exact selected edition;
   generic processing never substitutes another edition based on guessed
   compatibility.

Changing only editorial examples, translations or comments remains governed
by ADR-0018 and need not create a new version when normative meaning, host
applicability and abstract contract semantics remain unchanged. Changing only
a valid constraint representation under the equivalence rule above likewise
need not create a new version, although each artifact must still conform to
its applicable publication binding.

### Lifecycle

Extension terms use ADR-0019 exactly like other Vocabulary terms. D4 creates no
parallel `experimental`, `stable`, `deprecated` or `retired` mechanism.

- experimental state does not relax payload or identity rules;
- deprecated state discourages new use but does not invalidate an occurrence;
- retired state does not delete, tombstone or remove a payload; and
- absence from a later edition does not imply deletion or retirement.

A selected exact edition's lifecycle declarations may be reported alongside
Extension-aware results. They do not alter S2 bare-core conformance, execute a
migration or automatically choose a successor.

### Profile, authority and discovery boundaries

A Vocabulary describes meaning, applicability and optional payload
constraints. It does not by itself require that a document contain the
Extension, forbid an otherwise bare-core-valid document from omitting it, or
declare a document conformant to a profile. Profiles own requirement,
cardinality, composition and profile-conformance policy under accepted
ADR-0015/0016 boundaries.

If a profile requires an Extension whose exact Vocabulary edition is unknown,
unavailable or unsupported, bare core remains unaffected. The profile
assessment may be unavailable or fail according to that future profile's
rules; D4 does not invent the profile result.

Supplying or mechanically conforming to an artifact does not prove that the
publisher controls the Vocabulary or term IRI, that the artifact is authentic,
or that its claims are authoritative. Two publishers may make competing
claims. D5 owns discovery, authority, trust and governance; D4 has no central
registry or winner-selection rule.

D4 also defines no automatic composition of several Vocabulary editions. If
more than one selected artifact claims a contract for the same term IRI,
generic processing reports the separate evidence and does not merge,
prioritize or intersect the contracts. D5 and D7 own authority and composition.

### Security and execution boundary

Vocabulary artifacts, definitions, constraints, payloads, IRIs, URLs and
instruction-like strings are untrusted inert data. D4 does not authorize them
to:

- execute scripts, macros, queries, expressions, patches, commands or tools;
- load a plugin, driver, adapter, agent, model or remote validator;
- access a network, filesystem, endpoint or IRI;
- grant permission, credentials, authority or operational capability;
- weaken S2 or profile validation, privacy, redaction or lifecycle rules;
- turn described limits or preconditions into enforcement; or
- introduce a GeesNO.Core dependency.

```text
constraint language
!= executable plugin
!= driver
!= adapter
!= callback
```

A constraint-language implementation is locally chosen trusted software, not
code delivered by the Vocabulary. It interprets only a language/version the
implementation explicitly supports and applies bounded resource controls.
Executable or host-language code masquerading as a payload contract is not a
D4-conforming constraint representation. Evaluating supported declarative data
for validation is not authorization to execute the payload or invoke a domain
operation. There is no auto-download, dynamic code loading, network
requirement or GeesNO.Core dependency.

## Cross-domain validation

| Domain | Extension Vocabulary stress case | Result under the proposal |
| --- | --- | --- |
| Engineering | A structural-analysis term carries nested result arrays and is meaningful only on an Assertion. | The edition defines key/payload meaning, declares `Assertion` applicability and may constrain JSON shape; no geometry or analysis field enters core. |
| Spreadsheet/tabular data | A business Vocabulary annotates an Entity or Binding with raw numeric and formatting metadata. | Arbitrary JSON stays opaque to core; an exact edition can constrain it without a workbook adapter or ADR-0012 coercion. |
| Technical/legal document | A jurisdiction term applies only to Review and contains instruction-like legal text. | Host applicability is assessed above S2; the text remains inert and cannot become authorization or an agent instruction. |
| Software repository/source code | A language-analysis term uses an object payload on Provenance and later tightens a required member. | The new constraint requires a new Vocabulary version; term IRI may remain if meaning is compatible, with no Git or plugin semantics. |
| Scientific data | An uncertainty-distribution Extension uses arrays, raw decimals and `null`. | Payload kinds retain Extension-defined meaning and do not collapse into quantity uncertainty, Confidence or core conditions. |
| Generic product/asset data | Two publishers define competing payload contracts for one claimed term IRI. | Contracts remain edition-scoped claims; D4 does not infer authority, equivalence or a winning vendor. |

All six cases use the same declaration, applicability, optional-constraint and
exact-edition assessment model. None adds a domain primitive, product adapter,
network dependency or executable behavior.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| 1. Unknown Extension key with arbitrary valid JSON on an allowed S2 host | Bare-core valid and preservable under ADR-0015/0016. No Extension-aware claim is invented without an explicitly selected exact edition. |
| 2. Known term but selected Vocabulary artifact unavailable | Bare-core validity is unchanged. Extension-aware result is edition unavailable/unknown; neither meaning nor payload conformance is invented. A supplied artifact in an unsupported binding is reported separately as unsupported, not unavailable. |
| 3. S2-structurally valid payload rejected through a supported representation of the selected abstract contract | Bare-core valid; Extension-aware nonconforming relative to that exact edition and abstract contract. |
| 4. Same key assessed under two exact editions | Produce two edition-relative results. They may differ without either mutating the document or the other edition. |
| 5. Remote `latest` changes after an assessment | No effect. A moving alias cannot select the assessed edition, and D4 performs no hidden fetch or substitution. |
| 6. Vocabulary attempts to redefine a core member or meaning | Invalid D4 contract/interpretation. Core remains controlling and the Extension cannot repair, replace or redefine it. |
| 7. Vocabulary attempts to loosen an S2 constraint | Invalid D4 contract/interpretation. Extension-aware rules can add assessment but cannot weaken Layers 0–3. |
| 8. Payload is a raw JSON number, `null`, object or array | Bare-core valid inside a valid Extension occurrence. Each remains arbitrary Extension JSON and receives only semantics explicitly declared by the exact edition. |
| 9. Vocabulary reinterprets every payload automatically as an ADR-0012 value | Invalid D4 assumption. ADR-0012 applies only when the abstract Extension contract explicitly requires such a representation, and even then the payload does not become core. |
| 10. S2 allows the host but the selected declaration excludes it | Bare-core valid; Extension-aware nonconforming for host applicability under that edition. |
| 11. Vocabulary declares or document uses a host not exposed by S2 | The declaration is invalid D4 publication content; the document occurrence is bare-core invalid and cannot be legalized by the Vocabulary. |
| 12. Deprecated Extension term occurs in an older or newer document | Occurrence is not invalid merely because of lifecycle. Report the edition-scoped ADR-0019 claim; profiles may later impose new-use policy. |
| 13. Abstract payload contract changes in a newer edition | A new Vocabulary version is required when the payload acceptance relation changes. Exact-edition results remain separate; incompatible denoted meaning also requires a new term IRI. |
| 14. Definition, constraint or payload contains URLs or instruction-like text | Inert untrusted data. It triggers no dereference, tool call, model instruction, permission or execution. |
| 15. Artifact names an executable validator or plugin | It is not a conforming D4 constraint representation and is never auto-loaded. Assessment reports unsupported/not assessed rather than executing it. |
| 16. Two publishers claim the same term IRI | No automatic authority or merge follows. Assessments remain attributed to exact supplied editions; conflicting ownership/trust is D5. |
| 17. A profile requires an unknown Extension | Bare core remains valid. Profile conformance cannot be established or may fail under the future profile contract; D4 does not decide that policy. |
| 18. Exact selected edition defines the term and Extension use but supplies no abstract machine-checkable contract | Meaning can be exposed from the normative definition and host applicability can be assessed. Payload is recorded as not mechanically assessed because no contract was supplied, not as conforming or nonconforming. |
| 19. Same abstract payload contract represented in two different declarative languages | Both representations MAY express the same edition and contract `P` under their valid bindings. Language identity is processing evidence, not Vocabulary or term identity. Each is assessed only when explicitly supported. |
| 20. Same abstract contract represented by two different formulations in one language | Both formulations MAY represent the same edition when the publisher declares unchanged acceptance semantics. Syntax or byte difference alone does not create a new Vocabulary version. |
| 21. Publisher claims two representations are equivalent but a generic processor cannot prove it | No subjective generic conformance failure follows merely from inability to prove semantic equivalence. The claim remains publisher governance/integrity responsibility unless deterministic evaluation exposes a conflict. |
| 22. Two representations claiming the same edition produce observably different accept/reject results for one identical payload | Conflicting publication/contract claim and violation of immutable edition content. Report both results and the conflict; no hidden winner, timestamp precedence, retrieval preference or automatic authority applies. |
| 23. Edition changes from no machine-checkable contract to abstract contract `P` | Normative assessment expectations changed, so a new Vocabulary version is required. A new term IRI is not required when denoted meaning remains compatible. |
| 24. Edition changes from abstract contract `P1` to materially different `P2` | A changed acceptance relation requires a new Vocabulary version. If the Extension term's denoted meaning also changes incompatibly, ADR-0017 additionally requires a new term IRI. |
| 25. Constraint representation changes while term meaning, host applicability and abstract acceptance semantics remain unchanged | Representation-only change does not automatically require a new Vocabulary version. The publisher may claim the artifacts represent the same edition; generic processing need not prove that equivalence. |
| 26. Exact edition is otherwise available but its contract representation or constraint language/version is unsupported | Extension-aware payload assessment is unsupported/not assessed. It is not payload nonconformance, edition unavailability or bare-core invalidity. |

## Consequences

- Extension publishers gain one edition-scoped authoring convention without a
  second term identity or normative definition.
- Host applicability can improve interoperability while the accepted S2 host
  matrix remains the absolute structural ceiling.
- Optional abstract deterministic contracts allow mechanical payload
  assessment while preserving arbitrary inert JSON for bare core.
- Constraint-language syntax and version remain representation concerns;
  publisher-declared equivalent representations can express one edition
  without automatic Vocabulary-version churn.
- Observably different acceptance results from supposedly equivalent
  representations expose a conflicting publication claim rather than creating
  a hidden winner.
- Exact edition selection makes assessment reproducible and prevents remote
  latest-version drift.
- Unsupported or missing semantic evidence remains distinct from invalid
  payload.
- Constraint evolution becomes visible through Vocabulary versioning without
  forcing new term IRIs for every compatible refinement.
- Profiles, discovery, authority, cross-edition compatibility and execution
  remain separate concerns.
- No schema, fixture, Vocabulary artifact, Base Vocabulary term or SDK follows
  from this Proposed ADR.

## Remains open

- concrete Vocabulary publication serialization, media type, binding version,
  member names, placement and schema;
- the initial declarative payload-constraint language or supported language
  profile, including exact numeric/lexical evaluation semantics;
- exact representation and bundling of abstract contracts and finite
  constraint components, including whether one artifact may carry several
  claimed-equivalent representations and how duplicates/conflicts are handled;
- exact external edition-selection syntax and its future profile/configuration
  integration;
- D5 discovery, moving aliases, publisher authority, authenticity, trust,
  conflicting claims and registry governance;
- D6 Base Vocabulary identity, admission criteria and initial terms;
- D7 cross-Vocabulary composition, mapping, equivalence, edition compatibility,
  migration declarations and exact profile-to-Vocabulary compatibility;
- profile rules for required Extensions, occurrence cardinality and lifecycle
  policy;
- mature S5 diagnostic identifiers, severities and result serialization;
- publication fingerprints, signatures, canonical bytes and integrity threat
  model;
- executable transformations or migrations, which remain outside
  GeesNO.Semantic; and
- S4 AI Context projection and Extension-loss reporting.

## Acceptance record

**Decision status: Accepted**

The complete reviewed decision was explicitly approved by human architecture
decision on 2026-09-14. Acceptance covers the single-definition Extension-use
declaration, optional existing-host applicability, optional abstract
deterministic payload contract, separation from its declarative
representations, exact-edition Extension-aware assessment, evolution rules and
the bare-core/profile/security boundaries recorded above.

Acceptance closes D4 and authorizes analysis of D5. It does not itself choose a
publication serialization/schema or constraint-language binding, define a
discovery or authority mechanism, publish the Base Vocabulary, accept any D5–
D7 decision, or authorize a profile, fixture, SDK, adapter or executable
behavior.
