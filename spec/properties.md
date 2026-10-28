# Property Assertions

**Scope:** Universal Property Assertion model and Core 0.1 JSON representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

## Responsibility and cardinality

A Property Assertion states that one Entity has one qualified property with
exactly one value or explicit semantic value condition. An Entity can have
`0..*` Property Assertions. Multiple assertions for the same property may
coexist when values, sources, methods, times or interpretations differ.

Each occurrence conceptually has:

- subject Entity `1`;
- qualified property term `1`;
- value or explicit condition `1`;
- datatype context when needed for interpretation;
- unit semantics `1` when the value is a measured quantity, unless an
  explicitly applicable profile defines a default;
- Provenance, Confidence, Review, lifecycle and Extensions each `0..*`.

The assertion does not silently overwrite another claim. Conflict resolution,
selection and aggregation are consumer/profile policies unless future core
semantics explicitly say otherwise.

## Property term

Property identifiers are qualified vocabulary terms. The core supplies the
reference mechanism, not a list of domain properties. A label such as “width”,
“status” or “temperature” is not sufficient without its vocabulary context.
Accepted ADR-0010 and ADR-0016 define Core 0.1 JSON namespace mechanics.
Vocabulary identity/version follows accepted ADR-0017 and applicable
Vocabulary/Profile contracts.

## Value semantics

The abstract value families and the difference between absent, unknown, not
applicable and intentionally redacted are defined in
[values-and-units.md](values-and-units.md). Accepted ADR-0012 and ADR-0016
define the Core 0.1 JSON value/condition and structured-value representation.

In canonical JSON, a quantity explicitly materializes its unit even when an
applicable Profile interprets source input using a default. Multiple Property
Assertions remain separate claims, not an implicit list/set aggregate.
Aggregation and claim-selection policies belong to applicable
Vocabularies/Profiles.

## Invariants

- Absence of an assertion makes no claim about applicability or knowledge.
- A value must not be interpreted without sufficient datatype semantics.
- A measured numeric value never receives a silently inferred unit except from
  an explicitly applicable profile default.
- A semantic reference targets semantic identity, not array position or an
  unscoped locator.
- Redaction state must not leak the withheld value through Extensions/evidence.
- Property assertions can be corrected or superseded without changing Entity
  identity.
