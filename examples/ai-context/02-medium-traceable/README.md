# Medium traceable context

**NON-NORMATIVE ILLUSTRATIVE EXAMPLE**

## Purpose

Show semantic content together with material trust and origin correlation.

## Source scope

The source contains an observation, a representation, one unrelated concept,
an origin Source, a Binding and three Assertions.

## Selection context

The observation and its directly useful representation, label and traceability
records are selected.

## Projection scope

Six identified records form an explicit deterministic scope.

## Completeness

`complete` relative to that scope. The unrelated source concept is not selected.

## Material context decision

The observation's Provenance, Confidence, Review and Validity are carried with
their host. The material Source and Binding are also carried exactly.

## Key distinction

`Source != truth`, `Binding != truth`, `Confidence != truth`, and
`Review != permission`. Prefixes `obs` and `trace` expand offline through the
preserved namespace map.

## Files

- `source.json`: valid S2 scientific-observation source.
- `projection.json`: complete traceable Projection.

## Validation

The Projection passes I2 structural and I4 semantic checks offline.

## What this example does NOT mean

It does not require every Source or Binding to appear in every Projection and
does not make review or confidence an authorization mechanism.
