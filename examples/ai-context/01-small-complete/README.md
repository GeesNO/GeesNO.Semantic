# Small complete self-contained Projection

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show the smallest useful complete Projection without external dependencies.

## Source scope

The partial source describes two unrelated generic assets and their labels.

## Selection context

The first asset and its label are selected explicitly.

## Projection scope

The declared scope contains exactly those two identified records.

## Completeness

`complete`. Every record in the narrow declared Projection scope is carried,
even though other source records are outside that scope.

## Material context decision

No additional trust, Source, Binding or continuation context is material here.

## Key distinction

`subset of source != automatically partial`.

## Files

- `source.json`: valid S2 source SemanticDocument.
- `projection.json`: AI Context Profile `0.1.0` Projection.

## Validation

Both files are checked offline by the repository I5 example tests.

## What this example does NOT mean

It does not claim source-wide completeness or require every narrow Projection
to be self-contained.
