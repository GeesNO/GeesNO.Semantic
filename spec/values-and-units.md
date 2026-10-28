# Property values, value conditions and measured quantities

**Scope:** Abstract Core value semantics and Core 0.1 JSON representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md), accepted ADR-0012 and ADR-0016.

## Property Assertion responsibility

A Property Assertion identifies one subject Entity, one qualified property and
exactly one of:

- a value with sufficient datatype semantics; or
- an explicit semantic value condition: unknown, not applicable or
  intentionally redacted.

An absent Property Assertion makes no claim. This gives four distinct cases:

| Case | Meaning |
| --- | --- |
| Absent | No assertion about the property is present. The producer may not know or may not have considered it. |
| Unknown | The property is applicable/considered, but its value is not known. |
| Not applicable | The property is intentionally inapplicable to this subject/context. |
| Intentionally redacted | A value may exist but is withheld; disclosure and provenance policy still apply. |

These states must not be collapsed into a generic `null`. Accepted ADR-0012
serializes only unknown, not applicable and redacted as explicit universal
conditions; absence remains no Property Assertion/value occurrence. More
specialized states require future cross-domain vocabulary/profile evidence.

## Candidate value families

The abstract model must support:

- string/text;
- boolean;
- integer;
- decimal;
- date and date/time, with needed precision/time-zone semantics later defined;
- semantic reference to an identified subject;
- measured quantity;
- ordered list;
- unordered set;
- structured value whose interpretation is qualified.

These are value roles, not new Entity kinds. Domain-specific datatypes and
structures belong to vocabularies/profiles/extensions. Binary payloads and
executable code are outside the core value model; a Representation or Source
reference can describe external content.

Repeated Property Assertions are distinct claims; a list/set value is an
aggregate claim. Domain-level multi-valued-property interpretation may be
specified by an applicable Profile or Vocabulary. Lists and sets are not interchangeable:
ordering and duplicate semantics must be preserved when meaningful.

## Measured quantity semantics

A measured quantity has at least:

```text
numeric magnitude + unit semantics
```

The unit must be explicit unless an explicitly declared applicable profile
defines a default. A document-level or application convention that is not an
applicable profile is not enough for silent inference.

Accepted [ADR-0012](../adr/0012-value-measured-quantity-model.md) defines the Core 0.1 JSON
architecture: a quantity is one tagged value with an exact canonical integer or
decimal magnitude and an ADR-0010 qualified unit, and canonical exchange always
materializes that unit. No unit system, registry, dereference or conversion is
mandatory. Numeric precision is exact; source/display lexical metadata is
descriptive and does not define scale or significant figures unless an
explicit profile/vocabulary says so.

Universal uncertainty/tolerance and quantity-kind/dimension semantics remain
later vocabulary/profile work. Exact JSON members are accepted in ADR-0016 and
implemented in the Core 0.1 JSON schema/checker. Measurement uncertainty is
not Confidence and may use a qualified structured value, profile, vocabulary or
Extension until evidence supports a universal model.

## Trust and lifecycle

Every Property Assertion can carry Provenance, Confidence, Review and lifecycle
context under the common assertion contract. A redacted condition must not
leak or permit reconstruction of the withheld value through source/display
lexical metadata, evidence, diagnostics or Extensions. Provenance may state
that redaction occurred without revealing the content. A corrected value
supersedes rather than silently mutates historical meaning under accepted ADR-0014.
