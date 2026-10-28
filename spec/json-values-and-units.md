# JSON value, datatype and unit analysis

**Scope:** Core 0.1 JSON value, datatype, condition and unit representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md), accepted ADR-0012 and ADR-0016.

The accepted value model preserves datatype, exact numbers, collection
semantics and explicit conditions without host-language inference. Exact
member names and schema expressions are implemented by the Core 0.1 JSON schema and checker.

## Canonical hybrid representation

Native JSON is used only where it already carries the exact core datatype:

```json
"Column A"
```

```json
true
```

All other value families use one tagged form. Raw JSON numbers, arrays, objects
and `null` are not alternate value encodings.

```json
{"kind": "integer", "value": "9007199254740993"}
```

```json
{"kind": "decimal", "coefficient": "123", "exponent": "-2"}
```

```json
{"kind": "date", "value": "2026-09-01"}
```

```json
{"kind": "date_time", "value": "2026-09-01T08:15:00Z"}
```

```json
{
  "kind": "reference",
  "reference": {
    "target": "urn:uuid:00000000-0000-4000-8000-000000000010",
    "location": "in-document"
  }
}
```

The reference sketch reuses ADR-0009. Accepted ADR-0016 fixes the exact
`target`/`location` reference object implemented by the Core 0.1 JSON schema and checker.

## Numeric model

Integer is an arbitrary-precision canonical base-10 string: no leading plus,
no leading zero except `0`, and no decimal/exponent. `-0` is invalid.

Decimal is the normalized exact tuple:

```text
coefficient × 10^exponent
```

Both are canonical integer strings. Non-zero coefficient has no leading or
trailing zero; trailing powers of ten move into exponent. Decimal zero is
coefficient `0`, exponent `0`.

```json
{"kind": "decimal", "coefficient": "1", "exponent": "-1"}
```

```json
{
  "kind": "decimal",
  "coefficient": "12345678901234567890123456789",
  "exponent": "-9"
}
```

```json
{"kind": "decimal", "coefficient": "1", "exponent": "1000"}
```

These encode `0.1`, `12345678901234567890.123456789` and `1e1000` without
binary rounding or expansion to one thousand zeroes.

> **Source/display lexical metadata is descriptive only.**

Optional source-lexical metadata may preserve a spelling such as `1.2300`, but
it does not participate in numeric equality, change datatype, define precision,
scale or significant figures, or replace Provenance or Confidence. A profile
or vocabulary must declare any semantic scale/significant-figure contract.

## Conditions and null

```json
{"kind": "condition", "value": "unknown"}
```

```json
{"kind": "condition", "value": "not_applicable"}
```

```json
{"kind": "condition", "value": "redacted"}
```

Absence means no corresponding assertion/value occurrence. `null` is invalid
in normative value/condition slots. `withheld`, `not_measured` and
`not_provided` are not additional universal tokens without vocabulary/profile
evidence.

A redacted value must not be reconstructable through auxiliary lexical/display
metadata. A redacted occurrence cannot also expose source/display spelling, a
duplicated raw value or an equivalent representation. Provenance may record the
redaction event without disclosing the content; Extensions and diagnostics are
subject to the same safety boundary.

## String, boolean and temporal values

Strings preserve valid Unicode scalar values exactly, including empty string;
no Unicode normalization is inferred. Language-tagged/rich text uses a
qualified structured datatype when needed.

Only JSON `true` and `false` are booleans.

Date is a validated RFC 3339 `full-date`-compatible calendar date. Date-time is
an unambiguous instant with explicit input offset and canonical UTC `Z`
spelling. Local date-time without offset is not silently UTC. Fractional seconds
are exact and trailing zeroes are removed canonically; original spelling/offset
can be optional descriptive source metadata.

## Quantity and unit

```json
{
  "kind": "quantity",
  "magnitude": {
    "kind": "decimal",
    "coefficient": "3",
    "exponent": "2"
  },
  "unit": "units:millimetre"
}
```

Magnitude reuses integer/decimal. Unit is an accepted ADR-0010 qualified term
and is always materialized in the canonical Core 0.1 JSON representation. A profile default can interpret
source/profile input but does not make canonical exchange depend on hidden
context. No UCUM, QUDT, SI or proprietary registry is mandatory, and no unit is
automatically resolved or converted.

Measurement uncertainty is distinct from Confidence. Absolute/relative,
interval and distribution models remain qualified structured/profile/Extension
semantics rather than a premature universal mini-standard.

## Lists and sets

```json
{
  "kind": "list",
  "items": ["first", "second", "second"]
}
```

```json
{
  "kind": "set",
  "items": ["red", "blue"]
}
```

List order and duplicates are semantic. Set order is not semantic and duplicate
canonical semantic values are invalid. ADR-0012 does not impose byte ordering.
Items recursively use this same value/condition model.

## Structured values

```json
{
  "kind": "structured",
  "datatype": "geometry:interval",
  "members": {
    "geometry:start": {
      "kind": "decimal",
      "coefficient": "15",
      "exponent": "-1"
    },
    "geometry:end": {
      "kind": "decimal",
      "coefficient": "25",
      "exponent": "-1"
    }
  }
}
```

Structure datatype and member names are ADR-0010 qualified terms. Values and
conditions recurse. Unknown declared structures can be preserved without
dereference. Arbitrary unqualified objects are not a second core structured-
value form; opaque payloads belong in Extensions.

## Canonicality and security boundary

- one representation exists per core datatype;
- strings that resemble IRIs remain strings, not references;
- integer and decimal datatypes remain distinct even at equal mathematical
  magnitude;
- sets require datatype-aware canonical duplicate checks but not byte order;
- inline JSON recursion cannot cycle; graph cycles use semantic references;
- implementations apply explicit defensive depth, size and digit limits and
  must never silently round/truncate accepted values.

## Profile and processing boundaries

- Precision, significant-figure and measurement-uncertainty semantics beyond
  the universal value model belong to applicable Vocabularies or Profiles.
- Aggregation policies and interoperable resource-limit Profiles remain
  separate from the bare-Core datatype contract.
- Accepted ADR-0015 governs opaque Extension payload boundaries and their
  preservation. Accepted ADR-0016 governs exact JSON processing and numeric
  preservation; it does not impose byte-for-byte JSON canonicalization.

Accepted [ADR-0012](../adr/0012-value-measured-quantity-model.md) defines the
universal value, numeric, condition and unit architecture. The Core 0.1 JSON
schema and checker implement its representation. Further profile/integrity
policies do not alter the universal value datatypes.
