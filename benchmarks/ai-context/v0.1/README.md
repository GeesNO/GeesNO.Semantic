# S4 AI Context exit benchmark 0.1

**NON-NORMATIVE S4 MILESTONE EVIDENCE**

This benchmark demonstrates S4 milestone evidence. It does not define
GeesNO.Semantic Profile semantics or conformance thresholds.

## Purpose

The benchmark demonstrates that one deterministic S2 source with at least
10,000 addressable semantic records can produce both a complete narrow-scope
AI Context Projection and a compact bounded partial Projection while retaining
exact identity, references and applicable material context.

## Recipe

[`recipe.json`](recipe.json) fixes generator and recipe version `0.1`, category
counts, deterministic index-derived IDs and values, material-context indices,
both Projection scopes, the bound, omission target and Projection-continuation
recipe. These choices are benchmark logic, not universal materiality or
selection semantics.

The source count is the sum of top-level ID-bearing `entities`, `assertions`,
`sources` and `bindings`. Primitive values, nested trust fields, Extension
members and descriptor members do not contribute to the 10,000-record target.
Nested material Provenance, Confidence and Review records are reported
separately and never inflate that threshold.

## Deterministic measurement serialization

Measurement uses JSON with UTF-8 encoding, `ensure_ascii=false`, sorted keys,
compact `,` and `:` separators, and exactly one trailing LF. Character count is
the number of Unicode code points in that exact serialized string, including
that LF; byte count is the length of its UTF-8 encoding.

This measurement serialization is not normative canonical JSON, artifact
identity, Profile identity, a signature format or a publication contract. It
exists only to make bytes, characters, SHA-256 digests and ratios reproducible.

## Outputs and report

- [`expected/complete-narrow.projection.json`](expected/complete-narrow.projection.json)
  is complete relative to its explicit four-record scope and has no bound or
  truncation.
- [`expected/bounded-partial.projection.json`](expected/bounded-partial.projection.json)
  carries a deterministic prefix of a larger explicit scope, declares a
  reached finite bound, established truncation, known material omission and
  Projection continuation.
- [`expected-report.json`](expected-report.json) records input/output digests,
  record and serialized-size metrics, retention checks, threshold checks and
  offline/provider-neutral properties. It is benchmark evidence, not a D7
  assessment-result artifact.

The report records `projection_binding_under_test` as metadata about the
benchmarked Projection artifacts. The benchmark report itself is not serialized
under that binding and defines no normative artifact grammar.

The full 10,100-record source is generated in memory and is not committed.

## Thresholds

Only the bounded partial Projection is required to carry no more than 10% of
the source's addressable semantic records and serialize to no more than 25% of
the source bytes. Integer cross-multiplication decides both checks.

The values 10,000, 10% and 25% are S4 milestone benchmark thresholds. They are
not Profile requirements, boundedness semantics, universal compactness limits,
token budgets or conformance conditions.

## Reproduction

From the repository root, run the repository-internal benchmark command:

```shell
python tools/benchmark/ai_context_s4_exit.py
```

The command regenerates source and both Projections, validates S2 and I2,
applies reusable I4 semantic checks plus benchmark-specific checks, compares
the expected Projections and report byte for byte, prints a short summary and
returns nonzero on any mismatch. It is not a public CLI or production
Projection engine.

## Offline and provider neutrality

Generation and verification perform no network access, DNS, IRI dereference,
model call, prompt, embedding, RAG operation, external resolution or tokenizer
measurement. Compactness uses only record counts, UTF-8 bytes and Unicode
character counts.

## Relationship to I4

The runner reuses only I4's general `structural_errors()` and
`semantic_errors()` helpers. Benchmark scope/completeness, recipe materiality,
retention and threshold checks remain separate. I4 corpus paths,
`fixture-record-set` values and fixture-specific expectations are not used.

## Limitations

The data is synthetic and the fixed distribution is designed only to exercise
the S4 exit criteria. The benchmark does not measure real-domain relevance,
model quality, wall-clock performance, token usage or arbitrary third-party
Profile conformance.
