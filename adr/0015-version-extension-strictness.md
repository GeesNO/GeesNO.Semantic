# ADR-0015: Version, Extension and unknown-core-field policy

- **Status:** Accepted
- **Date:** 2026-08-31
- **Last substantial review:** 2026-09-04
- **Accepted by:** Explicit human architecture decision on 2026-09-04
- **Decision order:** After accepted ADR-0014; before ADR-0016 and the formal
  schema

## Context

The reference serialization needs both a strict universal language and an open
route for meaning that the universal core does not own. Permitting arbitrary
members on core objects would hide misspellings, produce undeclared dialects
and make a document's contract unknowable. Rejecting all non-core information
would instead make the standard unusable across unrelated domains.

The governing balance is:

```text
strict universal core + open extensibility
```

A consumer must be able to distinguish a core field, an Extension, a typo and
a member belonging to an unsupported future specification version. The
declared `spec_version` selects the core contract; explicit qualified
`extensions` carry additional inert data.

This ADR does not define the JSON Schema, normative fixtures, a registry,
Extension discovery, an S4 projection format or byte canonicalization.

## Requirements

The selected model must:

- close every core object according to its declared supported specification
  version;
- reject unknown members outside an explicit Extension boundary;
- preserve the Foundation rule that an unknown well-formed Extension does not
  invalidate bare core unless an applicable profile requires understanding it;
- permit Extensions only on hosts justified by the accepted model;
- identify every Extension key through accepted ADR-0010 qualification and
  expansion;
- define whether Extension payloads are ADR-0012 values or opaque JSON data;
- prevent Extensions from supplying, changing or weakening core meaning;
- distinguish structural collision from profile/vocabulary semantic conflict;
- define preservation obligations by processor role rather than requiring
  every reader to rewrite documents;
- keep specification, profile, vocabulary, Source and semantic Revision
  versions separate;
- fail clearly rather than validate an unsupported version with another
  version's contract;
- support documented `0.x` migration without prematurely fixing the future
  stable `1.x` compatibility policy;
- process all Extension content as untrusted, inert data; and
- remain domain-, product-, format- and AI-provider-neutral.

## Unknown-field alternatives

### Alternative A — silently accept unknown members

A processor would accept every unrecognized member on every object.

This is superficially forward-friendly, but `proprety`, `asserton` and
`confidance` become indistinguishable from intentional additions. Producers
can create local core dialects without a namespace or version change, and
different consumers can assign incompatible meanings to the same spelling.
This alternative is rejected.

### Alternative B — ignore or preserve unknown members

A reader would ignore an unknown member and a round-trip processor would try
to preserve it. This reduces immediate data loss but still cannot tell whether
the member is a typo, an experimental addition or a future core field. It also
makes conformance depend on a processor's preservation capability rather than
on the declared document contract. This alternative is rejected for core
members.

### Alternative C — closed core plus explicit Extensions

Every object has exactly the members defined by its supported
`spec_version`. Additional meaning is carried only at an explicitly permitted
`extensions` host, under an ADR-0010 qualified key. Typos and undeclared core
dialects are invalid while domain/vendor data remains open. This alternative
is selected.

## Closed-core policy

> **A core object is closed according to its declared supported specification
> version.**

An unknown member outside the explicit `extensions` member is invalid whether
it is unqualified, resembles a qualified term or can be preserved by the
implementation. In particular:

```text
unknown unqualified core member -> invalid
```

This rejects misspellings such as `proprety`, `asserton` and `confidance`
instead of silently creating another JSON dialect. A qualified-looking member
placed directly beside core members is also invalid; qualification does not
bypass the explicit Extension boundary.

The four relevant cases are distinct:

| Input | Classification |
| --- | --- |
| Member defined by the exactly supported core contract | Core field; validate under that contract. |
| Qualified entry inside a permitted `extensions` object | Extension; validate under this ADR and any applicable profile. |
| Unknown member on a core object under a supported version | Invalid core structure, commonly a typo or undeclared dialect. |
| Member defined only by a later specification while that later `spec_version` is declared | Unsupported version for a processor that lacks that exact contract; never validate it as an older version. |

If a producer places a future field in a document falsely declaring an older
version, the field is invalid under that older contract. If the producer uses
the future version, an older processor reports the version as unsupported.
Unknown core fields are never a forward-compatibility channel.

## Extension host policy

The optional core member `extensions` is one object/map, not a universal member
of every JSON object. Its permitted hosts are derived from the Foundation and
accepted ADR record boundaries:

| Host | `extensions` permitted? | Accepted-model justification |
| --- | --- | --- |
| SemanticDocument | Yes | The Foundation explicitly includes document Extensions. |
| Entity (`Concept` or `Representation`) | Yes | The Foundation explicitly includes Entity Extensions; no new Entity kind follows. |
| Assertion (all four accepted categories) | Yes | Accepted ADR-0005 gives the common assertion contract Extension semantics; ADR-0011 keeps one serialized assertion host. |
| Source | Yes | Accepted ADR-0013 reserves Source-description Extensions for non-universal metadata. |
| Binding | Yes | Accepted ADR-0006/0013 make Binding qualified/extensible without product fields. |
| Revision | Yes | Accepted ADR-0014 defines Revision as an identified lifecycle record with an Extension hook. |
| Tombstone | Yes | Accepted ADR-0014 defines an independently identified withdrawal record with an Extension hook. |
| Change | Yes | Accepted ADR-0014 defines the optional descriptive Change record with an Extension hook. |
| Provenance | Yes | It is a first-class scoped trust record; qualified method/evidence additions remain scoped to that exact occurrence. |
| Confidence | Yes | It is a first-class scoped assessment whose calibration/domain additions must not become universal fields. |
| Review | Yes | It is a first-class scoped disposition whose policy-specific additions remain local to that Review. |
| Scope descriptor | No | Accepted ADR-0014 already supplies one qualified `definition`; another generic Extension point is not justified. |
| History envelope or history membership descriptor | No | These are structural containers/edges, not independent semantic payload hosts. |
| Validity descriptor | No | Accepted ADR-0014 already qualifies the validity axis and ADR-0012 boundaries. |
| ADR-0009 reference object | No | Reference location and identity mechanics must remain closed and unambiguous. |
| Namespace/profile/vocabulary declaration | No | Their identity/version roles must remain structurally exact; domain data belongs on the document host. |
| Source location/revision/fingerprint descriptor | No | Accepted ADR-0013 already qualifies these descriptor roles; extra data belongs on Source. |
| Binding locator | No | Accepted ADR-0013 already uses one qualified kind plus one ADR-0012 value; extra data belongs on Binding. |
| ADR-0012 value, condition or structured-value object | No | Core value shapes remain canonical; a structured value already uses a qualified type and qualified member keys. |
| Extension payload object | No special nested host | It is opaque JSON data, not another recursive core Extension map. |

Permitting Extensions on nested trust records is justified by their accepted
first-class, independently addressable and recursively scoped nature; it does
not create global trust collections or new identity requirements. Conversely,
the absence of an Extension host on helper objects is deliberate. Domain data
must be attached to the nearest permitted semantic record or expressed through
an already accepted qualified role.

## Extension key model

At every permitted host, `extensions` is conceptually:

```text
extensions: map<QualifiedTerm, JSON data>
```

Each key uses the one compact qualified-term form accepted by ADR-0010. The
prefix must be declared by the document namespace context, and expansion
produces the key's absolute semantic term IRI:

```text
serialized Extension key
    -> namespace expansion
    -> absolute Extension term identity
```

The local prefix is not identity. Namespace expansion base, vocabulary
identity and vocabulary version remain separate. ADR-0010's prohibition on
ambiguous same-base aliases applies, and one Extension term may occur at most
once on one host after expansion.

No key triggers a central registry lookup, network dereference, vendor plugin
load or implicit discovery. A consumer can validate placement and expansion
without understanding the expanded term's domain semantics.

## Extension value alternatives

### Alternative A — require ADR-0012 canonical values

Advantages:

- one typed value infrastructure;
- uniform exact-number and condition semantics; and
- generic structural inspection of recursively qualified data.

Costs:

- third-party data must adopt the GeesNO value model merely to be preserved;
- arbitrary external objects require translation to qualified structured
  values;
- raw JSON numbers, `null` and ordinary arrays/objects cannot be retained; and
- an Extension payload is easily mistaken for a core Property value.

ADR-0012 deliberately routes truly opaque vendor payload to ADR-0015 rather
than claiming it as a core structured value. Alternative A is therefore too
restrictive as the only Extension payload form.

### Alternative B — permit arbitrary JSON data

Advantages:

- maximum domain and vendor openness inside one explicit boundary;
- straightforward preservation of external JSON-shaped metadata; and
- no second translation layer for data whose semantics core does not own.

Costs:

- raw JSON numbers, `null`, arrays and objects are legal inside Extensions even
  though they are not legal alternatives in ADR-0012 core value slots;
- generic core validators cannot validate unknown payload meaning; and
- implementations need exact-number handling and defensive depth/size limits.

The explicit `extensions` boundary contains these costs. Alternative B is
selected.

### Alternative C — envelope distinguishing semantic value and opaque data

An envelope could discriminate an ADR-0012 `semantic_value` branch from an
`opaque_json` branch. It would make the distinction explicit, but would add a
second wrapper/discriminator system to every Extension and still require the
opaque branch. An Extension vocabulary or profile can already declare that
its payload follows ADR-0012 when typed semantics are desired.

The extra universal envelope does not add enough interoperability to justify
its complexity. Alternative C is rejected.

### Selected payload boundary

An Extension value may be any JSON data value: object, array, string, number,
boolean or `null`. It is inert and opaque to bare core unless an applicable
Extension vocabulary/profile defines more semantics.

> **Extension payload is not automatically a GeesNO.Semantic Property value.**

ADR-0012's prohibition of raw JSON numbers, arrays, objects and `null` applies
to canonical core value/condition slots, not to an opaque Extension payload.
Conversely, arbitrary JSON remains invalid outside an allowed Extension
boundary when a core slot requires an ADR-0012 value.

For nested Extension data:

- strings preserve their Unicode scalar-value sequence; no normalization or
  dereference is inferred;
- numbers are arbitrary JSON numbers with no core datatype, unit, precision,
  equality or Property-value semantics; a preserving implementation must not
  round them through a lossy host numeric type;
- `null` is opaque Extension data and never means unknown, absent, redacted or
  not applicable in core;
- arrays preserve order and duplicates as payload data;
- object member names inside the payload are arbitrary strings and are not
  ADR-0010 terms unless the Extension's own contract says so;
- recursion is permitted subject to defensive resource limits; and
- an object with duplicate member names is not a deterministic JSON map and is
  outside this payload model; ADR-0016 retains ownership of raw-parser duplicate
  detection for the whole document.

Semantic preservation of an unknown payload means retaining scalar kinds,
string content, booleans/`null`, array order/duplicates and every object
member/value association. No accepted JSON numeric token may be rounded,
truncated, overflowed, converted to infinity or otherwise lost through a host
numeric type. This ADR deliberately does **not** decide that `1`, `1.0`, `1e0`
or `1E+0` are losslessly interchangeable, and it does not decide that `-0`
and `0` are interchangeable for an unknown Extension contract. ADR-0016 owns
the exact numeric-token processing and preservation rule for a processor that
claims lossless unknown-Extension round-trip.

Lossless preservation under this ADR is semantic/data-model preservation, not
byte identity. Whitespace, JSON string escape spelling and object member order
are outside this accepted preservation minimum. Numeric lexical information is
not included in that exclusion: its exact required treatment remains the
explicit ADR-0016 decision rather than being normalized here. An Extension
that needs other lexical presentation details as data must encode them
explicitly, for example as strings.

## Unknown Extension behavior

A bare-core consumer accepts a semantically unknown Extension when all of the
following hold:

- its host permits `extensions`;
- its key is a valid declared ADR-0010 qualified term;
- its payload is valid under the selected JSON-data boundary; and
- no applicable declared profile requires that consumer to understand or
  validate the Extension's additional semantics.

The consumer may ignore the Extension for interpretation while retaining the
document's valid bare-core meaning. It must not infer truth, authority,
execution, dereference or core semantics from the unknown payload.

```text
unknown Extension != unknown core field
```

If an applicable profile requires the Extension, lack of understanding or a
profile-invalid payload is a profile-conformance outcome, not retroactive
invalidity of the otherwise conforming bare core.

## Core-override boundary

> **Extensions may add meaning; they may not override core meaning.**

An Extension cannot redefine `id`, Entity kind, assertion placement,
cardinality, reference equality, required members, required unit/reference
semantics, scope/completeness, lifecycle, security or any other normative core
rule. It cannot supply a missing required member. Core validation proceeds as
if the payload cannot satisfy or alter the host's core constraints.

This produces two distinct collision classes:

1. **Structurally detectable override.** A producer places the addition beside
   core members instead of under `extensions`, omits a required core member and
   tries to supply it inside an Extension, uses an invalid Extension host/key,
   or otherwise violates a mechanically decidable core constraint. The record
   is invalid regardless of the payload's claimed meaning.
2. **Semantic/profile collision.** A well-placed qualified Extension makes a
   domain claim conceptually equivalent to or inconsistent with a core field.
   Bare core cannot know every vocabulary and does not automatically reject the
   record. A known Extension contract or applicable profile may classify it as
   an additional annotation, a semantic conflict or a prohibited override.

An opaque payload member named `id` is merely data inside that payload; it
cannot replace the host's core `id`. Likewise, an Extension asserting an
implicit quantity unit does not repair a core quantity missing its required
ADR-0012 unit. Conceptual equivalence alone does not merge, deduplicate or
promote an Extension into core.

## Preservation model

Processor obligations depend on the operation it claims to perform:

| Processor role | Unknown Extension obligation |
| --- | --- |
| Validator | Validate host, key and JSON-data boundary; report core/profile results. It need not rewrite the document. |
| Reader | May ignore unknown payload meaning after structural validation. It must not claim preservation merely because it read the document. |
| Transformer | Must declare whether its output contract preserves Extensions; any claimed preservation must retain unknown keys and payload semantics. |
| Lossless round-trip processor | Must preserve every unknown Extension key by expanded identity and preserve its payload semantics without numeric/string/structure loss. |
| Lossy projection | May omit Extension data only when its projection contract explicitly permits and reports that loss. |

A processor that claims lossless preservation of a record but drops, renames,
merges, normalizes destructively or rounds an unknown Extension commits a
processor-contract violation. It does not make the original document invalid.

Lossless is semantic/data-model preservation, not necessarily byte-for-byte
identity. A processor may reserialize whitespace or object order and may use a
different in-document prefix only if ADR-0010 expansion preserves the same
absolute Extension key identity and the whole resulting document remains
unambiguous. Byte-exact claims remain outside this ADR.

## Lossy projection boundary

A deliberately lossy projection may omit Extensions when its declared
projection/profile contract permits this. The omission must be explicit to the
caller or recipient through that contract and a processing result/diagnostic;
silent omission is not a lossless transformation.

ADR-0015 does not add a universal core `omitted_extensions` field and does not
design the S4 AI Context Profile. A future profile can standardize a portable
declaration. Until then, tooling can report loss out of band or through an
already valid profile-specific qualified mechanism.

A projection is not automatically a conforming SemanticDocument. If it omits
required core state or emits only a consumer-specific view, it must identify
its own output contract instead of claiming bare-core SemanticDocument
conformance. Dropping an Extension required by a declared profile fails that
profile even when the remaining bare core is valid.

## Specification-version model

`spec_version [1]` at SemanticDocument root is the exact identifier of the
normative serialization contract used by that document. It is a canonical
Semantic Versioning token and is compared as a complete string for contract
selection, including any prerelease component.

No leading `v`, whitespace or shortened form is equivalent. Build metadata is
valid SemVer syntax but does not name a GeesNO.Semantic contract unless that
exact version has been explicitly published; the project should not publish
multiple normative contracts distinguished only by build metadata.

The current repository/project version `0.1.0-dev` is a prerelease development
identifier. It is distinct from the future released contract `0.1.0`:

```text
0.1.0-dev != 0.1.0
```

While the schema remained `bootstrap-blocking` before ADR-0016 implementation,
neither token created a normative S2 conformance claim. The repository remains
`0.1.0-dev`; S2 candidate instances declare the intended contract token
`0.1.0`. Public release still requires human S2 closure review and a separate
release decision.

`spec_version` is not derived from a schema filename, package version,
namespace, profile, vocabulary or Source. The declaration selects the
contract; storage paths and schema identifiers are derived release artifacts.

## 0.x compatibility

During `0.x`, a conforming validator/reader declares an explicit set of exact
specification versions it supports and dispatches to the matching contract:

| Received version | Required behavior |
| --- | --- |
| Earlier version that the processor explicitly supports | Use that exact version's rules/schema; migration is optional and explicit. |
| Earlier version not supported | Report unsupported version; do not substitute a newer schema. |
| Later unsupported `0.x` version | Report unsupported version; do not apply the nearest/older schema and do not accept its fields as unknown core. |
| Different unsupported major version | Report unsupported version clearly; no fallback. |
| Prerelease/development version | Support only by exact declared token; `0.1.0-dev` is not silently treated as `0.1.0` or another prerelease. |
| Malformed or missing `spec_version` | Invalid document because no exact contract can be selected. |

Every incompatible `0.x` contract change requires an ADR, CHANGELOG entry and
documented migration. A migration produces a document that declares its target
version; preserving an unknown old Extension does not authorize relabelling
unmigrated core data.

## Future 1.x boundary

This exact-match rule is the safe S2 0.1 behavior. It does not prohibit a
future stable-version policy from allowing processors to declare compatible
SemVer ranges or forward-compatible minor handling once evidence, schema rules
and conformance tests exist.

Post-1.0 minor/patch compatibility, deprecation windows and range negotiation
remain open. Until a later accepted decision establishes them, processors must
not infer them from SemVer precedence alone.

## Profile/vocabulary version separation

These identifiers remain independent:

```text
specification version
!= profile identity/version
!= namespace expansion base
!= vocabulary identity/version
!= Source revision
!= semantic Revision identity
```

One specification version can be used with zero, one or several profiles, and
profiles may evolve independently according to their own declared compatibility
rules. ADR-0015 does not design the S4 profile declaration.

Accepted ADR-0010 remains controlling: a namespace expansion base is not a
vocabulary identity and neither is a vocabulary version. None can substitute
for `spec_version`, and the specification version does not select exactly one
profile or vocabulary release.

## S2 and S3 Extension boundary

S2 freezes only the mechanics required for interoperable JSON processing and
the later schema:

```text
Extension host
Extension qualified key
Extension payload boundary
unknown-field policy
unknown-Extension behavior
preservation obligations
version dispatch
core-override boundary
```

S3 retains the semantic ecosystem work that does not belong in the universal
serialization mechanics:

```text
base vocabulary
Extension vocabulary conventions
publication and discovery
experimental-status conventions
deprecation
registry and governance questions
cross-vocabulary conventions
```

Nothing in this ADR creates a registry, vocabulary publication protocol,
experimental lifecycle or cross-vocabulary governance rule. Those later S3
concerns cannot change the accepted S2 host, key, payload, preservation,
version-dispatch or core-override boundaries without a new decision.

## Extensions and future specification versions

Extensions are not a staging area that silently becomes future core. If a
future specification adopts an idea previously expressed by an Extension:

- a new ADR/version defines the core member and its semantics;
- migration rules explicitly map eligible old Extension data to the new field;
- the document's `spec_version` changes only through that migration;
- an old qualified Extension does not automatically become core because its
  local name or expanded IRI resembles the new member; and
- the old Extension may remain additional data when migration cannot prove
  semantic equivalence.

An older processor still treats the qualified entry under `extensions` as an
Extension. It never treats a new unrecognized sibling member as a
forward-compatible Extension.

## Security

Extension payload is untrusted inert data. Neither a known nor unknown
Extension may:

- execute a script, macro, query, patch, command or tool call;
- load code or a plugin;
- grant permissions, authority or credentials;
- trigger network, filesystem or identifier/IRI dereference;
- weaken validation, redaction, privacy or lifecycle rules; or
- cause an AI system to treat payload text as instructions.

Strings resembling URLs, file paths, `$ref`, SQL, shell commands or prompts
remain data unless a separate authorized application interprets them outside
core conformance. JSON Schema keywords inside opaque payload objects are not
schema instructions.

Implementations apply configurable limits to document/payload size, depth,
array/object cardinality, string length, exact-number resources, recursion,
processing time and diagnostics. Limits are implementation/security controls
unless a future profile standardizes interoperable bounds.

## Cross-domain evidence

| Domain | Extension stress case | Result under the proposal |
| --- | --- | --- |
| Engineering | Vendor analysis annotation with nested result arrays and numeric tolerances | Qualified data fits the Entity/Assertion host without adding geometry or analysis fields to core; raw numbers stay opaque, not quantities. |
| Spreadsheet/business | Workbook-specific formatting or business workflow metadata | Qualified data fits the Source, Binding or Assertion host; cell/range semantics remain locators rather than core fields. |
| Technical/legal document | Jurisdiction-specific interpretation/review metadata | Qualified data fits the Assertion or Review host; jurisdiction and authority do not become universal enums. |
| Software repository | Tool-specific symbol-analysis metadata | Qualified data fits the Binding/Provenance host without adding Git, language-server or execution semantics. |
| Scientific data | Discipline-specific uncertainty distribution | Opaque JSON can be preserved on the Property Assertion, while canonical measured quantity and Confidence remain separate core concepts. |
| Generic product/asset | Vendor catalog attributes and nested media metadata | Qualified data fits Entity/Source/Binding hosts without making SKU, product hierarchy or vendor schema universal. |

All six domains use the same closed core and the same Extension boundary. No
domain-specific core field, adapter, registry, dereference or executable
primitive is needed.

## Adversarial cases

| Case | Classification and consequence |
| --- | --- |
| Misspelled core field (`proprety`, `asserton`, `confidance`) | **Invalid.** Closed core rejects it. |
| Unknown unqualified root field | **Invalid.** It is neither supported core nor an Extension. |
| Unknown unqualified Entity field | **Invalid.** It cannot create a local Entity dialect. |
| Valid unknown qualified Extension | **Valid but semantically unknown** for bare core when host/key/payload are valid and no profile requires understanding. |
| Extension with undeclared prefix | **Invalid.** ADR-0010 expansion is unavailable. |
| Extension attempting to redefine host `id` | The core `id` remains controlling; missing/invalid core `id` is **invalid**. A known semantic override claim is **invalid under its Extension/profile contract**. |
| Extension attempting to replace a required quantity unit | **Invalid core record** if the ADR-0012 quantity lacks its unit; opaque Extension data cannot repair it. |
| Extension with arbitrary JSON payload | **Valid** inside an authorized Extension boundary. |
| Extension containing `null` or a raw JSON number | **Valid but opaque** inside the Extension; neither is a canonical core value/condition. Numeric loss on claimed round-trip is a processor-contract violation. |
| Deeply nested Extension | **Valid in the abstract**; a processor may reject/resource-limit it under documented defensive policy. |
| Duplicate Extension key after ADR-0010 identity expansion | **Invalid.** One host cannot carry two values for one Extension term; ADR-0010 also disallows ambiguous aliases. |
| Duplicate member inside arbitrary payload object | Outside the deterministic JSON-data model; raw detection remains ADR-0016. It is not legalized by Extension opacity. |
| Document with unsupported `spec_version` | **Unsupported version.** Do not use another schema. |
| Document with missing/malformed `spec_version` | **Invalid.** No contract can be selected. |
| Profile version used as `spec_version` | **Invalid or unsupported version**, depending on syntax/support; the roles cannot substitute for each other. |
| Vocabulary version used as `spec_version` | **Invalid or unsupported version** for the same reason. |
| Lossless tool dropping an unknown Extension | **Processor-contract violation.** The input document need not be invalid. |
| Lossy projection explicitly dropping an optional Extension | **Valid lossy operation** when its contract permits/reports the loss; profile conformance may still fail. |
| Lossy projection silently claiming full SemanticDocument preservation | **Processor-contract violation.** |
| Future core field encoded as Extension under an older version | **Valid only as an Extension**, not future core; promotion requires an explicit versioned migration. |
| Qualified Extension conceptually duplicates a core field | **Structurally valid additional annotation** unless a known profile/vocabulary identifies a conflict or prohibited override. |
| Extension payload containing executable-looking content | **Inert data.** Execution/dereference is forbidden; resource/security controls still apply. |

The classifications deliberately separate structural invalidity, unsupported
version, semantic unknown, profile-dependent interpretation and processor
contract violations.

## Decision

ADR-0015 establishes:

1. a required exact `spec_version` contract identifier at document root;
2. exact supported-version dispatch for S2 `0.x`, with no schema fallback;
3. closed core objects under the declared supported version;
4. invalidity of every unknown member outside an explicit Extension boundary;
5. one optional `extensions` map only on the host matrix fixed above;
6. ADR-0010 qualified Extension keys whose expanded absolute term IRI is
   identity, with no registry or dereference;
7. arbitrary JSON data as the Extension payload boundary, distinct from
   ADR-0012 core Property values and conditions;
8. acceptance of semantically unknown Extensions for bare core when placement,
   key and payload are valid and no applicable profile requires understanding;
9. the rule that Extensions may add meaning but cannot override, supply or
   weaken core meaning;
10. structural validation of mechanical override attempts and profile/
    vocabulary handling of conceptual semantic collisions;
11. separate obligations for validators, readers, transformers, lossless
    round-trip processors and lossy projections;
12. lossless preservation of unknown Extension key identity and payload
    semantics, without implying byte identity;
13. explicit declaration/reporting of permitted Extension loss without adding
    an S4 projection format;
14. strict separation of specification, profile, vocabulary, Source and
    semantic Revision versions;
15. `0.1.0-dev` as a prerelease contract token distinct from future released
    `0.1.0`, which is not normative while the schema is blocking;
16. explicit migrations for incompatible `0.x` changes and no automatic
    Extension-to-future-core promotion; and
17. inert, non-executable, non-dereferencing processing with defensive resource
    controls.

## Consequences

- Typos and undeclared future core members fail instead of fragmenting the
  universal contract.
- Domain and vendor information remains open behind one qualified boundary.
- Generic validators can validate core and Extension structure without
  understanding every Extension's semantics.
- Opaque JSON payloads improve preservation but require arbitrary-precision
  numeric handling and defensive processing from tools claiming losslessness.
- Extension/profile authors own additional payload semantics and collision
  rules; they cannot weaken bare core.
- Exact `0.x` dispatch can reject newer documents until a matching contract or
  explicit migration is available.
- Lossy projections remain possible but cannot masquerade as lossless core
  transformations.
- Future stable-version compatibility remains possible through a later ADR
  rather than accidental unknown-field tolerance.

## Remains open

- exact formal JSON Schema expressions and diagnostics for every closed host;
- exact profile declaration member shapes and profile compatibility rules;
- Extension vocabulary publication, discovery, experimental-status and
  deprecation conventions, primarily S3 work;
- a future portable projection/omission report, primarily S4/S5 work;
- interoperable resource-limit profiles;
- raw-byte parsing, duplicate-member detection, exact unknown-Extension
  numeric-token preservation and canonicalization boundaries under ADR-0016;
- migration documents for each actual incompatible `0.x` release transition;
  and
- stable `1.x` minor/patch forward-compatibility, deprecation and range policy.

These items do not leave a second unknown-field policy, Extension payload
model, host model, preservation contract or S2 `0.x` dispatch rule open.

## Acceptance record

The strict-core/open-Extension boundary, explicit host matrix, qualified key
identity, arbitrary-JSON payload model, unknown-Extension behavior,
core-override/collision rules, processor-specific preservation obligations,
lossy projection boundary, exact `spec_version` and `0.x` dispatch behavior,
version-role separation, future-core migration boundary, S2/S3 responsibility
boundary and security model were explicitly approved by human architecture
decision on 2026-09-04.

The approval expressly does not treat `1`, `1.0`, `1e0` or `1E+0` as
interchangeable for lossless processing of an unknown Extension, nor `-0` and
`0`. It prohibits numeric loss and delegates the exact token-preservation
mechanism to ADR-0016. Six unrelated domains and the required adversarial
cases introduce no domain-specific or executable core primitive.

ADR-0016 is Accepted. The formal schema and normative fixtures are implemented
as an S2 candidate; S2 closure, S4 projection design and SDK implementation
remain unapproved.
