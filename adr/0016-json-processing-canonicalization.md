# ADR-0016: JSON processing, schema draft and canonicalization boundary

- **Status:** Accepted
- **Date:** 2026-08-31
- **Last substantial review:** 2026-09-04
- **Accepted by:** Explicit human architecture decision on 2026-09-04
- **Decision order:** Final planned architecture decision before the S2 schema

## Context

Accepted ADR-0009 through ADR-0015 now define the semantic identity,
qualified-term, value, assertion, Source/Binding, lifecycle, version and
Extension boundaries for JSON 0.1. The remaining question is the exact
processing contract from untrusted bytes to a deterministic conformance result.

Several conditions disappear if an implementation first parses into an
ordinary host object: duplicate members may be collapsed, large numbers may be
rounded or converted to infinity, `-0` may become `0`, malformed Unicode may be
replaced, and the version may be inspected only after the wrong schema has
already been selected. JSON Schema also cannot conveniently prove every
document-wide identity, reference, namespace, graph and recursive set rule.

The governing pipeline is:

```text
raw JSON input
        -> safe JSON parsing
        -> spec_version dispatch
        -> structural JSON Schema validation
        -> deterministic semantic/integrity validation
        -> optional profile validation
```

This ADR freezes the processing, subordinate lexical and JSON-member choices
needed so the future schema can encode decisions rather than make them. It does
not write that schema, create normative fixtures, define S3 vocabularies,
design signatures or implement an SDK.

## Requirements

The S2 processing contract must:

- accept exactly UTF-8 JSON with one object root;
- detect duplicate members and malformed Unicode before a normal map model can
  discard evidence;
- select only the exactly declared supported specification contract;
- preserve arbitrary unknown Extension JSON without host numeric loss;
- distinguish semantic structure, lexical normalization and byte identity;
- state which collection orders carry meaning;
- distinguish schema checks from cross-record deterministic checks;
- close every core object while leaving only an authorized Extension payload
  arbitrary;
- freeze every member spelling, closed token and subordinate lexical rule
  needed by the first schema;
- permit offline and streaming-capable implementations without changing the
  wire model;
- require no network, vocabulary registry, LLM or official SDK; and
- treat resource refusal separately from a finding that the document is
  semantically invalid whenever the distinction is available.

## Processing pipeline

A conforming processor performs these stages in order:

1. **Raw input gate.** Apply declared defensive byte/resource limits, reject a
   UTF-8 BOM, decode strict UTF-8 and validate one complete JSON text.
2. **Safe parse.** Preserve object occurrences long enough to reject duplicate
   member names everywhere, preserve Extension numeric tokens when required,
   validate Unicode scalar sequences and require an object root.
3. **Version dispatch.** Read the single root `spec_version`, validate its
   canonical SemVer syntax and select an exactly supported contract. Missing or
   malformed is invalid; well-formed but unsupported is an unsupported-version
   outcome. No other version's schema runs.
4. **Schema validation.** Validate the selected version's required members,
   object shapes, discriminators, cardinalities, closed-core boundaries and
   basic lexical forms.
5. **Semantic/integrity validation.** Apply deterministic document-wide and
   recursive rules that are outside, or unsuitable for, JSON Schema.
6. **Profile validation.** If a caller requests a supported profile or the
   document declares one, separately evaluate that exact profile contract.
   Bare-core and profile outcomes remain distinguishable.

A processor may combine implementation passes, but it must preserve the same
ordering dependencies and outcomes. It cannot validate against `0.1.0` and
only afterwards discover another `spec_version`.

## UTF-8/Unicode policy

Normative GeesNO.Semantic JSON 0.1 is UTF-8 only.

- A leading UTF-8 BOM (`EF BB BF`) is invalid. Accepting it as transport
  decoration would create a second byte envelope and inconsistent behavior.
- Overlong forms, truncated sequences, illegal continuation bytes, UTF-8
  encodings of surrogate code points and code points above `U+10FFFF` are
  invalid.
- Every decoded member name and string, including Extension content, is a
  sequence of Unicode scalar values.
- A JSON `\u` high surrogate followed immediately by its matching low
  surrogate is decoded as one supplementary scalar. A lone, reversed or
  incorrectly paired escaped surrogate is invalid.
- Core processing performs no NFC, NFD, case, compatibility or locale
  normalization. Equality is the exact decoded scalar sequence except where an
  accepted role defines another comparison.
- Different legal JSON escape spellings for one scalar sequence do not create
  different semantic strings. A semantic/data-model round trip need not retain
  escape spelling.

This rule applies equally to core members, arbitrary Extension member names
and Extension string values.

## Parser-level rules

The raw parser accepts the JSON grammar only: no comments, trailing commas,
`NaN`, infinities, hexadecimal numbers or language-specific literals. Leading
and trailing JSON whitespace around the single text is allowed and is not
semantic.

Normative input contains exactly one JSON object root. An array, string,
number, boolean or `null` root is invalid GeesNO.Semantic input even if it is a
valid generic JSON value. Trailing non-whitespace bytes or a second JSON text
are invalid.

The parser must expose object member occurrences and numeric tokens before
converting them to a conventional map/number model, or provide equivalent
event/token hooks. A library that silently keeps the first or last duplicate,
replaces invalid Unicode, or converts every number to binary floating point is
not by itself a conforming safe parser for this pipeline.

## Duplicate-member policy

Duplicate JSON object member names are invalid everywhere after JSON string
escape decoding and exact scalar-sequence comparison. This includes:

- the SemanticDocument root;
- every nested core object;
- namespace, structured-member and `extensions` maps; and
- every object at every depth of an arbitrary Extension payload.

Extension opacity does not legalize duplicate members. The check occurs before
first-wins/last-wins map conversion, so a schema never sees an ambiguously
collapsed object.

This lexical duplicate check is distinct from Layer 3 rules such as two
different serialized Extension keys expanding to the same absolute term IRI.

## Version dispatch

After safe parsing and before version-specific schema validation, the processor
requires one root `spec_version` string. It uses the SemVer 2.0.0 grammar with
no leading `v`, surrounding whitespace, shortened components or leading zeroes
in numeric identifiers. Contract selection compares the complete token exactly,
including prerelease and build components.

```text
safe object + no duplicate members
    -> spec_version present exactly once and canonical SemVer
    -> exact token lookup in the supported-contract table
    -> selected version-specific schema and semantic rule set
```

`0.1.0-dev` and `0.1.0` are distinct. A build-metadata spelling is processed
only if that exact contract was published and supported. There is no nearest,
major, minor, patch, prerelease or forward fallback during `0.x`.

Missing, non-string or malformed `spec_version` is invalid contract selection.
A syntactically valid but unsupported token is reported as unsupported version,
not as schema-invalid under another contract.

## JSON number handling

### Core value slots

ADR-0012 remains controlling. A raw JSON number is not a core semantic value.
Core integers and decimals use tagged exact string forms. The raw parser may
encounter JSON numbers only where the selected structural contract permits
them, principally arbitrary Extension payloads.

### Extension payloads

Three strategies were compared:

1. **Host numeric primitive.** Rejected for preservation: binary64 and bounded
   types can round `9007199254740993`, overflow `1e100000`, lose a tiny decimal,
   or collapse negative zero.
2. **Original numeric lexical token.** Preserves every distinction an unknown
   Extension contract might observe.
3. **Exact implementation-independent numeric value.** Useful for computation,
   but value-only normalization cannot prove that `1`, `1.0`, `1e0`, `1E+0`,
   `-0` and `0` are interchangeable under an unknown vocabulary.

The proposal selects strategy 2 as the minimum for a processor claiming
**lossless unknown-Extension round-trip**. It retains and re-emits the exact
accepted JSON numeric token for each unknown Extension numeric occurrence. It
may additionally parse an exact arbitrary-precision sign/coefficient/exponent
model, but that model cannot replace the token for the lossless claim.

| Token | Lossless unknown-Extension treatment |
| --- | --- |
| `1` | Preserve `1`; do not replace with `1.0` or `1e0`. |
| `1.0` | Preserve the decimal point and zero. |
| `1e0` | Preserve lowercase exponent spelling. |
| `1E+0` | Preserve uppercase `E` and explicit plus. |
| `-0` | Preserve the sign; do not replace with `0`. |
| `0` | Preserve as distinct token occurrence from `-0`. |
| `9007199254740993` | Preserve all digits; no binary64 conversion. |
| `1e100000` | Preserve without overflow or infinity conversion. |
| `0.0000000000000000000000001` | Preserve every digit; no rounding or underflow. |

A validator that never reserializes may validate the token grammar in a
streaming fashion and need not retain it after reporting. A reader may expose
an opaque token/value representation. It cannot claim lossless round-trip if
its API or internal model already destroyed the token.

An Extension-aware transformer may normalize only when the applicable known
Extension contract explicitly makes the transformation lossless. It is not a
lossless *unknown*-Extension round trip.

This obligation is narrower than full byte preservation: surrounding
whitespace, comma/colon spacing and object position need not be retained.

## Extension preservation

For an unknown Extension, a lossless semantic/data-model round-trip preserves:

- every Extension entry by expanded qualified-key identity;
- every payload object membership, member name and nested association;
- every JSON scalar type;
- each string's decoded Unicode scalar sequence;
- booleans and `null` exactly by type/value;
- array length, element order and duplicates;
- the exact lexical token of every JSON number; and
- all nested structure recursively.

It need not preserve:

- whitespace or indentation;
- object member order;
- JSON string escape choice or slash escaping; or
- the local prefix spelling if an unambiguous namespace rewrite preserves the
  same expanded Extension key identity and every other document rule.

A validator has no rewrite obligation. A lossy projection may omit Extensions
only under the explicit/reporting contract accepted by ADR-0015. Dropping or
destructively normalizing an unknown payload while claiming lossless
preservation is a processor-contract violation, not invalidity of the input.

## Object/array ordering semantics

JSON object member order has no semantic meaning in core objects, namespace
maps, qualified structured values, `extensions` maps or Extension payload
objects. Bare processing does not infer precedence from it and a lossless
semantic/data-model round trip need not preserve it. An Extension vocabulary
needing portable ordered data must use an array; S2 does not guarantee object
order.

Array order is role-specific:

| Array role | Order semantics | Duplicate rule |
| --- | --- | --- |
| ADR-0012 `list.items` | Semantic and preserved | Allowed and preserved. |
| ADR-0012 `set.items` | Non-semantic | Duplicate semantic values invalid at Layer 3. |
| `entities`, `sources`, `bindings`, `assertions`, `tombstones` | Non-semantic | IDs remain document-wide unique; equal bodies with permitted distinct IDs are not automatically duplicates. |
| `profiles` | Non-semantic | One declaration per profile identity; conflicting/duplicate declarations invalid at Layer 3. |
| Revision `parents` | Non-semantic | Repeated target reference invalid at Layer 3. |
| Source `locations`, `fingerprints` | Non-semantic | Equal entries are not automatically invalid; no priority is inferred. |
| `provenance`, `confidence`, `reviews` | Non-semantic | Independent assessments may coexist; no priority or truth follows from position. |
| `supersedes` | Non-semantic | Repeated target invalid; multiple distinct prior targets allowed. |
| Change `targets` | Non-semantic | Repeated target invalid; grouping creates no order or atomicity. |
| `history.revisions`, `history.changes`, `history.records` | Non-semantic | Identity/reference rules apply; order never creates chronology or replay. |
| Provenance `sources` | Non-semantic | Repeated target reference invalid. |
| Extension payload arrays | Semantic opaque data and preserved | Duplicates allowed and preserved. |

Reordering an unordered collection does not change semantic meaning. This ADR
does not prescribe byte sorting for any such collection.

Array order and duplicate constraints are independent. JSON Schema can enforce
simple lexical equality with `uniqueItems`, but cannot reliably implement
ADR-0012 recursive datatype-aware semantic equality after qualified-term
expansion. Set semantic duplicate detection belongs to Layer 3.

## Validation-layer model

### Layer 0 — raw JSON

- resource gate distinguished as refusal where possible;
- no BOM and strict UTF-8;
- valid JSON grammar and one object root;
- valid Unicode scalar sequences;
- duplicate member rejection at every depth; and
- exposure of Extension numeric tokens where the operation needs lossless
  preservation.

### Layer 1 — version dispatch

- required string `spec_version`;
- canonical SemVer syntax; and
- exact supported-contract selection with no fallback.

### Layer 2 — JSON Schema

- required and prohibited members;
- primitive/object/array shapes;
- discriminator branches and exactly-one alternatives;
- schema-expressible cardinalities;
- closed core and authorized Extension hosts;
- basic lexical patterns; and
- exact `0.1.0` token after dispatch in the released schema.

### Layer 3 — semantic structural integrity

- document-wide addressable-ID uniqueness;
- complete RFC 3987 IRI checks and exact UUID-URN specialization;
- `in-document` reference resolution and target-category checks;
- prefix declaration, expansion validity and no same-base aliases;
- expanded qualified-member and Extension-key uniqueness;
- assertion subject/target Entity-kind checks;
- Confidence exact numeric range;
- recursive set semantic equality;
- Revision and supersession self/cycle checks in a closed local graph;
- Tombstone/live-state contradiction and known category mismatch;
- conditional Change/trust identity requirements;
- known current-state/history contradiction and accepted identity-continuity
  checks when locally decidable; and
- calendar validity and locally comparable validity intervals.

### Layer 4 — profile validation

An exactly identified/versioned supported profile may require understood
vocabularies, Extensions, closure, cardinalities, history, limits or domain
rules. Profile failure does not retroactively change valid bare core. An
unsupported declared profile prevents a profile-conformance claim but does not
authorize network discovery or invalidate otherwise valid bare core unless the
selected processing claim explicitly required that profile.

Every layer is deterministic and offline-capable. None requires an LLM,
network access or an official SDK.

## JSON Schema role

JSON Schema validates the structural portion of GeesNO.Semantic conformance.
It is necessary but not sufficient:

```text
schema-valid != fully GeesNO.Semantic-conformant

full bare-core conformance
    = successful Layers 0 + 1 + 2 + 3
```

Layer 3 is a normative deterministic checker, not optional SDK advice. S5
fixtures will identify the expected failing layer. A future SDK may implement
the contract but cannot define it.

## Draft selection

The proposal confirms JSON Schema Draft 2020-12 based on actual needs:

- `$defs` and `$ref` for reusable closed record/value definitions;
- recursive `$ref` for list, set, structured and trust records;
- `oneOf` for assertion and value discriminator branches;
- `if`/`then`/`else` for complete scope and normalized decimal conditions; and
- `unevaluatedProperties` to close composed records after branch evaluation.

Draft choice is not inherited merely from the placeholder. `format` is not the
sole enforcement for normative IRI/date rules; Layer 3 performs checks that a
portable schema engine cannot guarantee.

## Schema identifier and versioning

The 0.1 schema will use:

```text
$schema = https://json-schema.org/draft/2020-12/schema
repository path = schema/v0.1/geesno-semantic.schema.json
instance contract = spec_version "0.1.0"
```

The first repository schema omits `$id`. No project-controlled public schema
URI has been established, and inventing a fetch-looking authority adds no
validation value. Internal references use document-local fragments. A future
publication decision may assign an absolute `$id` without changing instance
`spec_version` semantics.

```text
JSON Schema dialect identifier ($schema)
!= schema retrieval identity ($id, if later assigned)
!= repository version path
!= SemanticDocument spec_version
```

All required schemas are supplied locally. An HTTPS `$schema` or future HTTPS
`$id` is an identifier, never permission or a requirement to fetch content.

## Closed-core schema strategy

Simple leaf objects use `additionalProperties: false` when their complete
member set is declared in the same schema object. Composed discriminated
records use `unevaluatedProperties: false` at the final composed boundary so
members evaluated through `$ref`, `allOf` or the selected `oneOf` remain legal
while every other member is rejected.

Reusable partial envelopes must not close before a specialized branch adds its
members. Future schema tests must prove each known member remains legal and an
unknown sibling is not admitted.

The `extensions` map is allowed only on ADR-0015 hosts. Its property names use
the qualified-term lexical schema and values admit arbitrary JSON. Openness
stops at that value boundary; it does not reopen the host or another core
object. Raw duplicate and Unicode rules still apply inside the payload.

## Cross-record semantic validation

Layer 3 builds bounded indexes as needed and validates at minimum:

1. one ID table across the document, Entity, Source, Binding, Assertion,
   Revision, Tombstone, identified Change and identified trust records;
2. reference resolution and expected target category for every local edge;
3. namespace expansion, no base aliases and no duplicate expanded map key;
4. Concept/Representation categories at association endpoints;
5. semantic duplicate rules for sets and repeated reference sets;
6. locally closed Revision and supersession graph coherence;
7. Tombstone/current-state and locally decidable history/state consistency;
8. conditional identity on independently managed Change/trust records; and
9. exact numeric/calendar/range comparisons without host precision loss.

Out-of-document existence, category and remote cycles remain externally
unverifiable. The checker never dereferences them. A profile may require a
closed package, but bare core never turns availability into validity.

## Lexical freeze audit

### Semantic IDs and IRIs

Every ID is a non-empty Unicode-scalar string. A UUID-namespace spelling is
canonical only when it matches:

```regex
^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
```

Any case-insensitive `urn:uuid:` spelling that fails this expression is
invalid rather than falling through to the general IRI branch. Every other ID
must satisfy the RFC 3987 `IRI` production with a scheme; relative IRIs are
invalid and fragments are allowed. Equality is exact scalar-sequence equality;
no percent, host, path, case or Unicode normalization is inferred. Schema may
check a conservative scheme prefix; Layer 3 performs full RFC 3987 validation.
There is no normative character-count limit.

### Qualified terms and namespace prefixes

The S2 0.1 compact grammar is deliberately ASCII-safe:

```regex
prefix = ^[A-Za-z][A-Za-z0-9._-]*$
local  = ^[A-Za-z0-9_][A-Za-z0-9._-]*$
term   = ^[A-Za-z][A-Za-z0-9._-]*:[A-Za-z0-9_][A-Za-z0-9._-]*$
```

The colon is the sole structural separator because neither component admits
one. Components are non-empty and case-sensitive. Raw Unicode local names,
whitespace, slash, hash, percent escapes and additional colons are not admitted
in 0.1. A later version may expand the grammar explicitly.

Each namespace value is an absolute RFC 3987 IRI expansion base. Direct
concatenation of the base and every used local must itself produce a valid
absolute IRI. No separator is inserted. Prefix aliases for one exact base are
invalid. There is no normative maximum length.

### Date and date-time

Canonical `date` uses exactly `YYYY-MM-DD`, with year `0001` through `9999`,
Gregorian calendar validity and no extended year.

Canonical `date_time` uses:

```text
YYYY-MM-DDTHH:MM:SS[.fraction]Z
```

- uppercase `T` and `Z` only;
- the same four-digit Gregorian year range;
- hour `00..23`, minute `00..59`, second `00..59`;
- no leap-second `60` and no `24:00:00`;
- optional fraction with one or more digits whose final digit is non-zero; and
- no numeric offset in canonical exchange.

A producer may accept an RFC 3339 offset before serialization, but normalizes
the instant exactly to UTC `Z`. Retained source spelling/offset uses optional
descriptive `source_lexical` and does not alter equality. Calendar validity and
offset conversion are Layer 3; schema supplies the structural pattern.

### Integer and decimal

Canonical integer strings match:

```regex
^(?:0|-?[1-9][0-9]*)$
```

There is no `+`, leading zero, exponent, decimal point or `-0`.

A decimal coefficient is `0` or a signed non-zero integer with no leading or
trailing zero:

```regex
^(?:0|-?(?:[1-9]|[1-9][0-9]*[1-9]))$
```

Its exponent uses the canonical integer expression. Coefficient `0` requires
exponent `0`; a non-zero coefficient admits any canonical exponent. There is
no normative digit limit. Defensive refusal must not round or reclassify the
mathematical value as invalid.

## Member-name/token freeze audit

These are the sole accepted 0.1 spellings. Rows with several members describe
one closed object; optional omission does not authorize aliases.

| Semantic role / object | Final JSON members | Owning decision | Status |
| --- | --- | --- | --- |
| SemanticDocument | `spec_version`, `id`, `scope`, `namespaces`, `profiles`, `revision`, `entities`, `sources`, `bindings`, `assertions`, `tombstones`, `history`, `extensions` | ADR-0009–0016 | Accepted freeze in ADR-0016 |
| Profile reference | `profile`, `version` | Foundation / ADR-0015/0016 | Accepted freeze in ADR-0016 |
| Namespace map | prefix property -> expansion-base string | ADR-0010/0016 | Accepted freeze in ADR-0016 |
| Reference | `target`, `location` | ADR-0009/0016 | Accepted freeze in ADR-0016 |
| Entity | `id`, `kind`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | S1 / ADR-0014–0016 | Accepted freeze in ADR-0016 |
| Assertion common envelope | `id`, `kind`, `subject`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | ADR-0011/0014–0016 | Accepted freeze in ADR-0016 |
| Type assertion branch | `type` | ADR-0011 | Accepted role; spelling frozen here |
| Property assertion branch | `property`, exactly one of `value` or `condition` | ADR-0011/0012 | Accepted role; spelling frozen here |
| Relation branch | `predicate`, `object` | ADR-0011 | Accepted role; spelling frozen here |
| Concept–Representation branch | `concept` | ADR-0011 | Accepted role; spelling frozen here |
| Source | `id`, `locations`, `revision`, `fingerprints`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | ADR-0013–0016 | Accepted spelling freeze |
| Source location/revision descriptor | `kind`, `value` | ADR-0013 | Accepted role; spelling frozen here |
| Fingerprint | `algorithm`, `value` | ADR-0013 | Accepted role; spelling frozen here |
| Binding | `id`, `entity`, `source`, `locator`, `method`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | ADR-0013–0016 | Accepted spelling freeze |
| Locator | `kind`, `value` | ADR-0013 | Accepted role; spelling frozen here |
| Revision | `id`, `parents`, `provenance`, `confidence`, `reviews`, `extensions` | ADR-0014–0016 | Accepted spelling freeze |
| Scope | `completeness`, `definition` | ADR-0014 | Accepted role; spelling frozen here |
| Scope/history definition | `kind`, `value` | ADR-0014 | Accepted role; spelling frozen here |
| Tombstone | `id`, `target`, `target_category`, `reason`, `provenance`, `confidence`, `reviews`, `extensions` | ADR-0014–0016 | Accepted spelling freeze |
| Validity | `kind`, `from`, `until` | ADR-0014 | Accepted role; spelling frozen here |
| Change | `id`, `revision`, `targets`, `kind`, `details`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | ADR-0014–0016 | Accepted spelling freeze |
| History | `completeness`, `definition`, `revisions`, `changes`, `records` | ADR-0014/0016 | Accepted spelling freeze |
| Historical membership | `revision`, `target` | ADR-0014 | Accepted role; spelling frozen here |
| Provenance | `id`, `kind`, `sources`, `details`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | S1 / ADR-0011/0014–0016 | Accepted subordinate shape/freeze |
| Confidence | `id`, `score`, `method`, `details`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | S1 / ADR-0011/0014–0016 | Accepted subordinate shape/freeze |
| Review | `id`, `disposition`, `details`, `provenance`, `confidence`, `reviews`, `supersedes`, `validity`, `extensions` | S1 / ADR-0011/0014–0016 | Accepted subordinate shape/freeze |
| Integer | `kind`, `value`, `source_lexical` | ADR-0012/0016 | Accepted role; spelling frozen here |
| Decimal | `kind`, `coefficient`, `exponent`, `source_lexical` | ADR-0012/0016 | Accepted role; spelling frozen here |
| Date/date-time | `kind`, `value`, `source_lexical` | ADR-0012/0016 | Accepted role; spelling frozen here |
| Reference value | `kind`, `reference` | ADR-0012/0016 | Accepted spelling freeze |
| Quantity | `kind`, `magnitude`, `unit` | ADR-0012 | Accepted role; spelling frozen here |
| List/set | `kind`, `items` | ADR-0012 | Accepted role; spelling frozen here |
| Structured value | `kind`, `datatype`, `members` | ADR-0012 | Accepted role; spelling frozen here |
| Condition | `kind`, `value` | ADR-0012 | Accepted role; spelling frozen here |
| Extension map | qualified-term property -> arbitrary JSON value | ADR-0010/0015/0016 | Host/payload/processing Accepted |

`ProfileReference.profile` is an absolute IRI and `version` is a non-empty
exact scalar string whose further grammar belongs to that profile. Declaration
order is non-semantic; the same profile identity occurs at most once.
`namespaces` maps prefixes directly to expansion-base strings; S3 vocabulary
identity/version/discovery metadata does not enter this S2 map.

Provenance requires `kind` as a qualified origin/mechanism term. Confidence
requires `score`, encoded only as an ADR-0012 integer or decimal and checked at
Layer 3 to be within inclusive range 0..1; optional `method` is qualified.
Review requires qualified `disposition`. Optional `details` uses one ADR-0012
value, avoiding unqualified property bags. These choices complete the accepted
first-class trust capabilities while leaving their vocabularies to S3/profiles.

The closed tokens are:

| Token family | Tokens | Classification |
| --- | --- | --- |
| Entity `kind` | `concept`, `representation` | Closed structural core |
| Assertion `kind` | `type`, `property`, `relation`, `concept_representation` | Closed structural core |
| Value `kind` | `integer`, `decimal`, `date`, `date_time`, `reference`, `quantity`, `list`, `set`, `structured` | Closed structural core |
| Condition `kind` | `condition` | Closed structural core |
| Condition `value` | `unknown`, `not_applicable`, `redacted` | Closed semantic core |
| Completeness | `complete`, `partial`, `unknown` | Closed semantic core |
| Reference `location` | `in-document`, `out-of-document` | Closed structural core |
| Tombstone `target_category` | `entity`, `assertion`, `source`, `binding`, `revision`, `change`, `provenance`, `confidence`, `review` | Closed structural core |

All types, properties, predicates, Extension keys, unit identities, structured
datatypes/members, locator/location/revision/method kinds, Provenance kinds,
Confidence methods, Review dispositions, scope/history definitions, Change
kinds, validity axes and Tombstone reasons are ADR-0010 qualified terms, not
new core enums.

## Omission/empty/null rules

The alternatives were permitting omission and an empty container, always
emitting arrays, or choosing one omission rule. The proposal selects:

> An optional core collection or map with zero entries is omitted.

Empty root/category arrays, `parents`, `locations`, `fingerprints`, trust
arrays, `supersedes`, history arrays, `profiles`, `namespaces` and `extensions`
are invalid when present. Required non-empty arrays such as Change `targets`
use `minItems: 1`.

Three exceptions retain meaningful or required emptiness:

- `list.items: []` is the empty ordered list;
- `set.items: []` is the empty set; and
- `structured.members: {}` is an explicitly typed empty structure.

An Extension payload may be `{}` or `[]`; that is opaque data. An individual
Extension entry remains meaningful with an empty payload, but the containing
`extensions` map itself must not be empty.

`namespaces` is required and non-empty when any qualified term occurs and is
otherwise omitted when empty. Unused entries remain valid. A `history` object
always requires `completeness`; `complete` also requires `definition`. For
`partial` or `unknown`, history must additionally contain `definition` or a
non-empty `revisions`, `changes` or `records`; otherwise it is omitted.

Every optional core member is omitted when absent. No core member admits JSON
`null`; it remains valid only inside arbitrary Extension payloads. No raw-number
Property, implicit IRI reference string, null condition, inline assertion,
inferred unit or other shorthand is introduced.

## Canonicality levels

1. **Semantic canonicality:** one normative role/placement and interpretation;
   S2 closes this.
2. **Serialization normalization:** exact admitted spellings for IDs, terms,
   numeric strings, date/time, members and tokens; S2 closes required rules.
3. **Byte canonicalization:** one byte sequence covering whitespace, member
   order and escape spelling; S2 does not define it.
4. **Cryptographic canonicalization:** signature/hash-oriented canonical bytes;
   future threat-modelled work.

Semantic equivalence after unordered reordering is not byte identity. Exact
opaque numeric-token preservation is a targeted lossless obligation, not
whole-document byte canonicalization.

## Byte-canonicalization decision

The alternatives are adopting an existing byte-canonical JSON method now,
inventing a GeesNO method, or deferring. The proposal defers.

No accepted signature or canonical document-hash threat model exists. Choosing
bytes now would prematurely decide namespace rewriting, unordered collection
sorting, string escaping, numeric handling outside Extensions and signature
envelopes. Deferral does not block parsing, schema, deterministic validation,
conformance fixtures, an SDK or interoperability.

ADR-0013 Source fingerprints describe source content under their qualified
algorithm/scope. They are not a SemanticDocument hash.

## Diagnostics

A validator distinguishes raw-parse, version-dispatch, schema,
semantic/integrity, profile and resource-refusal outcomes. Diagnostics are
bounded and do not reproduce redacted values, nearby secret Extension content
or unbounded attacker-controlled strings.

A JSON Pointer may identify an ephemeral received location. It is not semantic
identity, is unstable under reordering and must never be emitted as a target ID.
Stable diagnostic codes and exact wording belong to S5; this ADR requires the
layer/category distinction and safe reporting.

## Resource/security model

Implementations set documented defensive limits for bytes, nesting, arrays,
object members, numeric tokens, strings, indexes, graph traversal, cycle checks,
allocation and time. These are not universal semantic limits unless a future
profile standardizes them.

When a well-formed value exceeds a limit, report **resource refusal**, not
semantic invalidity, where distinguishable. A processor may terminate early
for safety and state that validity was not determined. It must never truncate
and continue, round a number, discard members, replace Unicode or skip graph
edges while claiming conformance.

All IDs, IRIs, terms, strings, Source locations, locators, Extensions and
schema annotations are untrusted inert data. Validation performs no network or
filesystem dereference, code/plugin loading, query, macro, command, patch,
agent action or LLM interpretation. Schemas and supported profiles come from an
explicitly trusted local configuration.

## Streaming/large-document processing

The pipeline permits streaming. Layer 0 can tokenize and detect duplicates
with per-object name sets. Layer 2 can validate events or buffered subtrees.
Layer 3 may maintain ID/reference/namespace/graph indexes, spill them to local
storage and defer global results until end of document.

This is implementation strategy, not a new wire format. Record order remains
non-semantic and full conformance cannot be claimed before required global
checks complete.

## Cross-language evidence

| Platform | Unsafe default risk | Required portable behavior |
| --- | --- | --- |
| JavaScript | `JSON.parse` collapses duplicate keys and `Number` rounds/overflows. | Token/event precheck and retained Extension tokens; ADR-0012 strings avoid `Number`. |
| Python | `json` normally keeps the last duplicate and has parser-specific numeric types. | Pair/token hooks for duplicates and exact lexical retention for unknown Extension numbers. |
| Java | Object mappers may coerce numbers or accept duplicate properties. | Strict duplicate detection and lexical/raw number nodes. |
| .NET | DOM serializers may normalize numbers; comments/trailing comma options vary. | Strict options plus raw-token storage for preserved Extensions. |
| Rust | Direct struct/map deserialization can discard duplicates and numeric spelling. | Raw visitor/event layer before typed conversion. |
| Go | Generic maps lose duplicates and numbers commonly become `float64`. | Streaming token checks and retained raw numbers rather than `float64`. |

All six can implement the contract, but no convenient default object/numeric
API becomes normative.

## Cross-domain evidence

| Domain | Processing stress case | Result |
| --- | --- | --- |
| Engineering | Vendor Extension has `-0`, huge exponents and nested arrays. | Tokens/order survive without becoming quantity or geometry core. |
| Spreadsheet/tabular | Exact digits exceed binary64 and records reorder. | Exact values and non-semantic root collections avoid host/row-order identity. |
| Technical/legal document | Redacted claim and reordered clauses/extensions. | Diagnostics do not leak; only explicit list/Extension arrays preserve order. |
| Software repository | External references and cyclic local lineage. | Offline indexes reject local cycles and leave remote facts unverifiable without Git semantics. |
| Scientific data | Tiny decimals, exact dates and semantic set duplicates. | Exact grammar and Layer 3 equality avoid floating loss and schema overclaim. |
| Product/database | Producers use different prefixes and collection order. | Expansion identity and unordered record collections interoperate without vendor fields. |

No domain introduces a parser mode, core field, ordering convention or byte
rule.

## Adversarial cases

| Case | Accepted classification |
| --- | --- |
| UTF-8 BOM | **Invalid raw input** at Layer 0. |
| Invalid UTF-8 | **Invalid raw JSON input** at Layer 0. |
| Lone/reversed escaped surrogate | **Invalid raw JSON input** at Layer 0. |
| Duplicate root, nested core or Extension-payload member | **Invalid raw JSON input** at Layer 0 before map collapse. |
| Missing/non-string/malformed `spec_version` | **Invalid contract selection** at Layer 1; no version schema runs. |
| Well-formed unsupported `spec_version` | **Unsupported version**; no fallback. |
| Unknown core member | **Schema invalid** at Layer 2. |
| Unknown qualified Extension with valid host/key/payload | **Valid but semantically unknown** in bare core. |
| Raw number in Property value | **Schema invalid** under ADR-0012. |
| Raw number in Extension | **Valid** opaque JSON; exact token required for lossless round-trip. |
| `1`, `1.0`, `1e0`, `1E+0` in unknown Extension | Each is **valid** and its exact token is preserved; no equivalence inferred. |
| `-0` in Extension | **Valid** and not normalized to `0` by a lossless processor. |
| Huge exponent/tiny decimal in Extension | **Valid** abstractly; exact token preserved, or **resource refusal** under a documented limit. |
| Object members reordered | **Valid; same semantic/data-model object** where only order changed. |
| `assertions` reordered | **Valid; same claim set**. |
| `list.items` reordered | **Valid JSON but a different semantic list value**. |
| `set.items` reordered | **Valid; same semantic set** if no duplicates. |
| Extension array reordered | **Valid JSON but a different opaque payload**. |
| Empty optional core collection/map | **Schema invalid**; omit it. |
| Empty `extensions` object | **Schema invalid**; omit it. |
| Empty Extension payload object/array | **Valid** opaque payload. |
| Optional core member encoded as `null` | **Schema invalid**; omit it. |
| Unresolved `in-document` reference | **Semantic/integrity invalid** at Layer 3. |
| Unresolved `out-of-document` reference | **Valid but externally unverifiable**; no dereference. |
| Duplicate semantic IDs | **Semantic/integrity invalid** at Layer 3. |
| Recursive semantic Set duplicate | **Semantic/integrity invalid** at Layer 3 even if schema cannot detect it. |
| Closed local Revision or supersession cycle | **Semantic/integrity invalid** at Layer 3. |
| Possible cycle through out-of-document edge | **Externally unverifiable**, not locally rejected. |
| Validator tries network dereference | **Processor-contract/security violation**. |
| `$schema`/future `$id` URL unavailable | No effect; local validation continues. |
| Defensive limit exceeded | **Resource refusal**; validity not silently decided. |
| Profile rule failure | **Profile invalid**; bare-core result remains separately reportable. |

## READY TO WRITE SCHEMA?

| Future schema input | State after this proposal |
| --- | --- |
| Identity/reference semantics | **Accepted** — ADR-0009 |
| Qualified terms/namespaces | **Accepted** — ADR-0010 |
| Values/conditions/quantities | **Accepted** — ADR-0012 |
| Assertion placement/addressability | **Accepted** — ADR-0011 |
| Source/Binding | **Accepted** — ADR-0013 |
| Lifecycle/scope/completeness | **Accepted** — ADR-0014 |
| Extension/version/unknown fields | **Accepted** — ADR-0015 |
| Raw parsing and version dispatch | **Accepted; frozen here** |
| Extension numeric preservation | **Accepted; frozen here** |
| Validation-layer boundary | **Accepted; frozen here** |
| Draft/closed-object strategy | **Accepted; frozen here** |
| ID/term/date/time/numeric lexicals | **Accepted; frozen here; no open schema choice** |
| Reference/member names and trust shapes | **Accepted; frozen here; no aliases** |
| Closed tokens | **Accepted; fully inventoried here** |
| Omission/empty/null rules | **Accepted; frozen here** |
| Byte/cryptographic canonicalization | **Explicitly deferred; not a schema blocker** |
| Schema `$id` publication URI | **Explicitly omitted for 0.1; not a schema choice** |

The technical answer is **yes**. The explicit human architecture decision dated
2026-09-04 accepted every frozen row. No remaining processing, lexical,
member-name, token or omission question forces schema authors to invent
semantics.

## Accepted decision

ADR-0016 establishes:

1. strict UTF-8 without BOM and Unicode-scalar validity for the whole document;
2. one object root, strict JSON grammar and duplicate-member rejection at every
   depth before map conversion;
3. exact `spec_version` dispatch before version-specific schema validation;
4. exact numeric-token retention for lossless unknown-Extension round trips,
   without whole-document byte identity;
5. complete role-specific object/array order and duplicate semantics;
6. mandatory Layers 0–3 for bare-core conformance and a separate profile layer;
7. JSON Schema as structural validation only, completed by Layer 3;
8. Draft 2020-12 and the composed closed-core strategy;
9. local schema supply, the exact 0.1 path and omission of `$id` until a
   controlled publication identifier exists;
10. exact ID, qualified-term, temporal, integer and decimal lexical rules;
11. one exact member inventory, reference form, trust shape and token inventory;
12. omission of empty optional containers/null, with explicit exceptions;
13. semantic canonicality and lexical normalization now, while byte and
    cryptographic canonicalization remain deferred;
14. safe layered diagnostics and resource refusal distinct from invalidity;
15. streaming-capable, bounded, offline, non-executing validation; and
16. no schema, fixture, profile, vocabulary, SDK or adapter implementation in
    this architectural decision.

## Consequences

- Schema authors receive exact shapes and lexicals rather than authority to
  choose them.
- Generic host parsers require a token/event safety layer.
- Lossless unknown-Extension processors carry numeric tokens even when they
  also expose exact values.
- Full bare-core validation requires a deterministic checker after schema.
- Producers omit empty optional containers and normalize core lexical forms.
- Consumers may reorder unordered collections but gain no byte canonical form.
- Large-document implementations may stream/spill indexes, with full results
  deferred until global checks finish.
- Signature, document hashing and canonical bytes remain future work.

## Remains open

These later concerns do not block the S2 schema:

- human S2 closure review of the implemented schema/checker/fixtures;
- S3 base/Extension vocabularies, publication, discovery, experimental status,
  deprecation, registry and cross-vocabulary governance;
- profile vocabularies, compatibility and profile-specific limits;
- S4 AI Context projection/chunking;
- S5 stable diagnostic codes, wording and fixture harness;
- document signatures, hashes, canonical bytes and their threat model;
- interoperable resource-limit profiles;
- future internationalized qualified-local grammar; and
- future stable `1.x` compatibility policy.

None authorizes the schema to add a core member, alias, token, semantic
constraint or alternate encoding.

## Acceptance record

**Decision status: Accepted**

The decision answers the complete raw-byte-to-conformance pipeline and freezes
every subordinate processing, lexical, member-name, token, order/duplicate and
omission rule required to author the S2 schema without inventing semantics.
Cross-language, cross-domain and adversarial review found implementation burden
but no universal-core contradiction.

The full proposal was explicitly approved by human architecture decision on
2026-09-04. That approval authorizes the formal S2 schema, Layers 0–3 reference
checker and normative fixture implementation while leaving S2 closure and the
public `0.1.0` release subject to a later human review. Byte/cryptographic
canonicalization, S3, S4 and the functional SDK remain outside this decision.
