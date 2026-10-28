# ADR-0012: Value, datatype and measured-quantity model

- **Status:** Accepted
- **Date:** 2026-09-01
- **Accepted by:** Explicit human architecture decision on 2026-09-02
- **Decision order:** After accepted ADR-0009 and ADR-0010; before ADR-0011

## Context

S2 needs one portable value model for Property Assertions and other approved
typed-value positions. It must preserve datatype, numeric exactness, temporal
meaning, references, units, collection semantics and explicit value conditions
without depending on Python, JavaScript, Java, .NET, Rust, Go or another host
language.

The model must support string, boolean, integer, decimal, date, date-time,
semantic reference, measured quantity, list, set, structured value and explicit
semantic condition. It must preserve the Foundation distinction among absent,
unknown, not applicable and intentionally redacted.

## Requirements

- one normative representation per core value datatype;
- exact round-trip of arbitrary-size integer and finite base-10 decimal values;
- no silent binary-floating conversion or language-range truncation;
- unambiguous distinction between ordinary strings and dates/references;
- domain-neutral structures and unit identity;
- deterministic offline validation without registry or dereference;
- recursive composition with defensive implementation limits;
- readable enough for humans/AI while prioritizing interoperability;
- no conflation of numeric precision, measurement uncertainty and Confidence.

## Alternatives

### Alternative A — native JSON scalars where possible

Strings, booleans and JSON numbers use their native forms; wrappers cover dates,
references, quantities and special conditions. This is smallest, but JSON
numbers cannot guarantee arbitrary integer or decimal precision, arrays do not
distinguish lists from sets, and a string does not identify date/reference
semantics.

### Alternative B — tagged values everywhere

Every value is an object such as `{"kind":"string","value":"text"}`. This
is uniform and explicit but repeats information already unambiguous in native
JSON strings/booleans, increases token cost and implementation ceremony, and is
not justified merely because it simplifies schema definitions.

### Alternative C — one canonical hybrid typed model

Use native JSON only where the semantic datatype is already exact and
unambiguous: string and boolean. Use one tagged object form for integer,
decimal, date, date-time, reference, quantity, list, set and structured values,
plus one explicit condition object. Raw JSON numbers, arrays, objects and
`null` are not alternate value forms.

This preserves one representation per datatype without wrapping trivial text
and booleans. The additional schema union is bounded and deterministic.

## Proposed canonical value families

The proposed model adopts Alternative C. Conceptual examples use provisional
member names:

```json
"Column A"
```

```json
true
```

```json
{"kind": "integer", "value": "9007199254740993"}
```

```json
{"kind": "decimal", "coefficient": "1", "exponent": "-1"}
```

```json
{"kind": "date", "value": "2026-09-01"}
```

```json
{"kind": "date_time", "value": "2026-09-01T08:15:00Z"}
```

The exact JSON member names remain subordinate serialization detail, but no
datatype receives a second equivalent form.

## Numeric precision

[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) permits implementations
to limit JSON-number range and precision and identifies only integers in
`[-(2^53)+1, (2^53)-1]` as exactly interoperable across binary64-based
implementations. Therefore normative integer and decimal values are never raw
JSON numbers.

An implementation may apply documented resource limits to extremely long
numeric strings, but it must not silently round, truncate or reinterpret a
conforming value. Non-finite values (`NaN`, positive/negative infinity) are not
integer or finite-decimal values and are not universal core datatypes.

Semantic numeric value is separate from source/display spelling. Canonical
numeric fields encode mathematical value.

> **Source/display lexical metadata is descriptive only.**

An optional source-lexical string may preserve material input spelling such as
`1.2300`, but it:

- does not participate in numeric equality;
- does not change the datatype;
- does not automatically define precision, scale or significant figures;
- does not replace Provenance; and
- does not replace Confidence.

A profile or vocabulary that treats scale, significant figures or another
presentation property as semantic must declare that contract explicitly.

## Integer analysis

Integers use a tagged object containing one arbitrary-precision canonical
base-10 string:

- optional `-` only for a negative non-zero value;
- no leading `+`;
- no leading zero except the value `0`;
- no decimal point or exponent;
- zero is exactly `0`; `-0` is non-canonical and invalid.

This is more verbose than raw `42`, but one form for all magnitudes avoids a
datatype changing shape at a JavaScript-safe-integer, 64-bit or 128-bit
boundary. `42` as a raw JSON number is not a second normative integer form.

## Decimal analysis

JSON number and binary floating point cannot preserve values such as `0.1` or
`12345678901234567890.123456789` uniformly. A plain canonical decimal string is
readable but either forbids exponent notation or can require enormous strings
for values such as `1e1000`.

The proposed decimal object instead stores a normalized decimal pair:

```text
semantic decimal value = coefficient × 10^exponent
```

Both fields are canonical arbitrary-precision base-10 integer strings. Rules:

- zero is `coefficient = "0"`, `exponent = "0"`;
- a non-zero coefficient has no leading or trailing zero and may begin with
  `-`; it never begins with `+`;
- exponent has no leading `+` or insignificant leading zero;
- moving every trailing coefficient zero into the exponent creates one tuple;
- negative zero is invalid;
- the value is finite and exact; no rounding context is implied.

Examples:

| Source meaning | Canonical coefficient | Canonical exponent |
| --- | --- | --- |
| `0.1` | `1` | `-1` |
| `1.23` or `1.2300` | `123` | `-2` |
| `12345678901234567890.123456789` | `12345678901234567890123456789` | `-9` |
| `1e1000` | `1` | `1000` |

The tuple preserves numeric value and compact extreme exponents without
preserving incidental spelling. Optional source-lexical metadata can retain
`1.2300`; an explicit profile/vocabulary must define whether its scale is
material. Integer `42` and decimal coefficient `42`/exponent `0` retain
different core datatype identities even though profiles may define broader
numeric equivalence.

## String and boolean analysis

A string uses native JSON string syntax and preserves its Unicode scalar-value
sequence exactly. Empty string is valid and distinct from absence/unknown. Core
processing performs no automatic Unicode normalization. Ill-formed Unicode
such as an unpaired surrogate is rejected for interoperable GeesNO exchange,
even where a permissive JSON parser can represent it.

Language-tagged or richly annotated text is not a second primitive string form;
it can use a qualified structured datatype/profile when required.

A boolean uses only native JSON `true` or `false`. Numeric `0`/`1`, strings
`"true"`/`"false"`, and `yes`/`no` are not boolean equivalents.

## Conditions/null semantics

Absence has no serialized value token: no corresponding Property Assertion or
value occurrence is present.

The only universal explicit conditions are:

- `unknown`;
- `not_applicable`;
- `redacted`.

They use one explicit condition object and are never ordinary strings. The
candidate does not add `withheld` (overlaps redacted), `not_measured` or
`not_provided`; more specific distinctions require vocabulary/profile evidence.

JSON `null` has no normative value or condition meaning and is invalid in a
value/condition slot. Optional structural members are omitted when absent.

## Redaction safety

> **A redacted value must not be reconstructable through auxiliary
> lexical/display metadata.**

A `redacted` condition cannot coexist in the same scoped value occurrence with
source lexical spelling, display spelling, a duplicated raw value or another
equivalent representation that discloses the hidden content. Provenance may
record that redaction occurred and how it was applied, but must not reveal the
redacted value. Implementations must apply the same rule to Extensions and
diagnostics attached to that occurrence.

## Date/time

Date and date-time are separate tagged datatypes:

- `date` represents a calendar date with no time or timezone and uses a
  validated RFC 3339 `full-date`-compatible spelling;
- `date_time` represents an unambiguous instant and requires an explicit
  offset on input; its canonical semantic spelling is normalized to UTC with
  `Z`;
- fractional seconds are exact decimal fractions; insignificant trailing
  fractional zeroes are removed in the canonical instant spelling;
- an unqualified local date-time or unknown timezone is not silently treated as
  UTC and requires a qualified structured/profile datatype;
- original offset/display spelling may be retained as optional source-lexical
  metadata but does not alter instant equality.

[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) provides the Internet
timestamp basis and explains why unqualified local time is not interoperable.
Exact leap-second and extended-year admission remain subordinate lexical
details to freeze before schema authoring.

Temporal value representation does not define lifecycle meaning. Recorded,
authored, observed or effective time remains the role of the containing
property/vocabulary/lifecycle structure, not the `date_time` datatype.

## References

A semantic-reference value uses one tagged reference form containing the
ADR-0009 reference structure. It reuses the same target semantic ID,
`in-document` / `out-of-document` expectation, equality and no-dereference
rules. It never creates a second reference model.

A JSON string that happens to contain an IRI remains a string. It is not
implicitly promoted to a reference.

## Quantity/unit analysis

A measured quantity is one tagged value containing:

```text
numeric magnitude + qualified unit term
```

Magnitude reuses the canonical integer or decimal object. Unit identity uses
the accepted ADR-0010 qualified-term mechanism. This avoids a second absolute-
identifier spelling or a GeesNO-owned unit syntax while allowing independent
UCUM-, QUDT-, organization- or community-defined unit vocabularies. No specific
registry or unit system is mandatory, and the unit term is not dereferenced.

The canonical S2 quantity always serializes its unit. A profile may define a
default for interpreting a source or compact profile representation, as the
Foundation permits, but a canonical core JSON quantity materializes the
effective unit. This stricter exchange form prevents silent dependence on
profile context and remains compatible with Foundation.

Unit identity, display symbol, source spelling and conversion target remain
distinct. The core does not silently convert to SI or another canonical unit.

Absolute/relative `±`, interval and distribution uncertainty models are not one
universal shape. Measurement uncertainty therefore remains a qualified
structured value, profile rule or Extension until cross-domain evidence
justifies a minimal shared contract. It is never Confidence: uncertainty
describes a measured quantity; Confidence assesses a claim.

## Collection semantics

A raw JSON array is not a core value because it cannot distinguish list from
set. Both collection datatypes use tagged objects whose `items` recursively use
the same value/condition model.

- **List:** ordered; duplicates allowed and semantically retained.
- **Set:** unordered; duplicate canonical semantic values invalid.

Set item order has no semantic meaning, and ADR-0012 does not define byte
ordering. Duplicate detection uses canonical datatype-aware value equality:
exact strings/booleans, normalized numeric/temporal forms, ADR-0009 target
identity for references and recursive equality for collections/structures.
Datatype-distinct numeric values are not automatically collapsed. Exact
cross-document qualified-structure comparison expands its terms under
ADR-0010.

## Structured values

A structured value uses:

- the closed core `structured` datatype token;
- one qualified semantic datatype/structure term;
- members keyed by qualified terms;
- recursively encoded values or explicit conditions.

This balances arbitrary JSON and Extension-only payloads: core can preserve and
mechanically inspect the shape without owning its domain semantics. A consumer
may preserve an unknown declared structure without dereferencing its vocabulary.
Repeated fields use an explicit list/set value rather than duplicate object
members.

An arbitrary unqualified JSON object is not a second structured-value form.
Truly opaque vendor payload belongs in an Extension governed by ADR-0015.

## Nesting and recursion

Lists, sets and structured values may recursively contain any value/condition,
including quantities, references and other structures. Inline JSON cannot form
an object cycle; semantic graph cycles use explicit ADR-0009 references.

Implementations need configurable limits for nesting depth, collection size,
numeric digit count and total bytes. These are security/resource controls, not
universal semantic limits unless a future profile supplies interoperable bounds.

## Datatype identity

Fundamental serialization types use a closed set of core discriminator tokens:

```text
integer, decimal, date, date_time, reference,
quantity, list, set, structured
```

Native JSON supplies the closed `string` and `boolean` branches. Domain semantic
datatypes use ADR-0010 qualified terms inside structured values or profiles.
GeesNO does not externalize fundamental parser mechanics into vocabularies and
does not turn domain datatypes into core tokens.

## Cross-language evidence

| Platform | Relevant behavior | Result of proposed model |
| --- | --- | --- |
| JavaScript | `Number` cannot distinguish every integer above `2^53-1`; `BigInt` is separate. | Integer/decimal strings avoid `Number` parsing. |
| Python | `int` is arbitrary precision and `decimal.Decimal` is available. | Direct exact parsing is possible without making Python normative. |
| Java | Primitive integers are bounded; `BigInteger`/`BigDecimal` are explicit arbitrary-precision types. | Canonical fields map without truncation. |
| C#/.NET | Primitive integers and `decimal` are bounded; `BigInteger` is available. | Strings avoid fixed-range assumptions. |
| Rust | Core integer primitives stop at 128 bits and decimal support is library-defined. | The wire contract remains independent of crate/type choice. |
| Go | Primitive integers are bounded; `math/big` provides multi-precision types. | Consumers can choose exact libraries and reject resource excess explicitly. |

All six platforms can preserve the wire representation without converting it to
binary floating point. Date-time is exchanged as canonical text, Unicode string
comparison remains exact, and set semantics are explicit rather than inferred
from a host collection type.

## Cross-domain evidence

| Domain | Stress case | Result |
| --- | --- | --- |
| Engineering | `1.2300` source dimension with millimetre unit | Exact numeric tuple plus optional source spelling and explicit unit; scale is not Confidence. |
| Spreadsheet/finance | `12345678901234567890.123456789` | No binary or fixed-decimal loss. |
| Legal/document | Empty text, redaction and status text | Empty string, explicit condition and vocabulary meaning stay distinct. |
| Software | Version `1.20.0` and ordered dependency path | Version remains string; list preserves order/duplicates. |
| Scientific | `1e1000`, uncertainty interval and unit vocabulary | Compact exact exponent pair; uncertainty stays qualified rather than a biased mini-standard. |
| Product | Exact price/specification and unknown vendor unit | Exact decimal and declared qualified unit remain processable offline. |

No domain-specific field, fixed unit registry or host-language numeric type is
required.

## Adversarial cases

| Case | Proposed classification |
| --- | --- |
| `9007199254740993` | Valid only as canonical tagged integer string; raw JSON number invalid. |
| `0.1` | Valid as decimal coefficient `1`, exponent `-1`; raw JSON number invalid. |
| `-0` | Invalid canonical integer/decimal spelling; semantic zero uses positive zero tuple. |
| `1.2300` | Same numeric value as `1.23`; canonical tuple is `123 × 10^-2`; optional source spelling is distinct metadata. |
| `1e1000` | Valid as decimal coefficient `1`, exponent `1000`; raw JSON number invalid. |
| Empty string | Valid string; distinct from absent and unknown. |
| Unknown property value | Valid explicit `unknown` condition. |
| Redacted value | Valid explicit `redacted` condition; withheld content must not leak through metadata. |
| Quantity without unit | Invalid in canonical S2 quantity. |
| Quantity with unknown unit vocabulary | Valid when the ADR-0010 expansion base is declared; semantic/profile understanding may be unavailable. |
| List with duplicate values | Valid; duplicates are semantic. |
| Set with duplicate values | Invalid after canonical datatype-aware comparison. |
| Deeply nested structured value | Semantically valid; subject to documented defensive resource limits. |
| Reference encoded as plain string | It remains a string, never a reference; profile/property expectations may reject the datatype. |
| Invalid date-time or date-time without offset | Invalid core temporal value. |
| JSON `null` | Invalid in value/condition slots. |

## Accepted decision

1. Adopt the canonical hybrid model: native JSON string/boolean; one tagged
   object for every other datatype; one explicit condition object.
2. Prohibit raw JSON numbers, arrays, arbitrary objects and `null` as normative
   value alternatives.
3. Encode arbitrary-precision integers as canonical base-10 strings.
4. Encode finite decimals as normalized arbitrary-precision
   coefficient/exponent string pairs.
5. Separate canonical numeric value from optional source/display spelling;
   leave domain precision/scale meaning to explicit metadata.
6. Use explicit `unknown`, `not_applicable` and `redacted`; represent absence by
   no assertion/value occurrence.
7. Use separate date and canonical UTC date-time tagged values; reject silent
   local-time assumptions.
8. Reuse ADR-0009 for semantic-reference values.
9. Require every canonical quantity to carry a numeric magnitude and ADR-0010
   qualified unit term; mandate no unit system or conversion.
10. Define list as ordered/duplicate-preserving and set as
    unordered/duplicate-free, without byte-order rules.
11. Require qualified structured types/members and recursive canonical values;
    keep opaque JSON in Extensions.
12. Keep fundamental datatype discriminators as closed core tokens and domain
    datatypes as qualified semantic terms.

## Consequences

- Exact values survive JavaScript, fixed-width languages and differing decimal
  libraries without silent loss.
- Common strings and booleans remain compact; other types pay explicit tagging
  cost only where semantics require it.
- Decimal coefficient/exponent representation is more verbose for `0.1` than a
  JSON number but remains exact and compact for extreme exponents.
- Producers must normalize numeric and date-time forms before serialization.
- Consumers need datatype-aware recursive equality for sets.
- Canonical quantities are self-contained even when a profile supplied a source
  default.
- AI Context may later project a more compact form, but S4 cannot change core
  value identity or erase required unit/reference semantics.

## Remains open

- exact JSON member names and assertion placement, coordinated with ADR-0011;
- final ABNF/JSON constraints for integer coefficient/exponent strings without
  changing the accepted normalization principles;
- exact temporal leap-second, extended-year and fractional-second bounds;
- exact placement/name and preservation contract for optional source-lexical
  metadata;
- whether future evidence justifies universal precision/significant-figures or
  measurement-uncertainty structures;
- complete canonical equality algorithm for deeply nested sets/structures and
  associated validation complexity;
- profile rules for repeated Property Assertions versus aggregate list/set;
- final Extension preservation boundary under ADR-0015;
- concrete security/resource defaults, if any, in profiles;
- byte-level ordering/canonicalization under ADR-0016.

## Acceptance record

The canonical representation boundary, numeric exactness, conditions/null,
redaction safety, temporal/reference behavior, quantity/unit policy,
collection semantics, structured recursion and cross-language/domain risks
were explicitly approved by human architecture decision on 2026-09-02. This
ADR is normative architecture for S2; its explicitly listed subordinate JSON
member names and schema expressions remain open until the remaining S2 ADRs
are approved.
