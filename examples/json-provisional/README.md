# Provisional JSON design examples

**Status: PROVISIONAL / NON-NORMATIVE — NOT CONFORMANCE FIXTURES**

These Markdown examples exercise the accepted S2 candidate architecture.
ADR-0009 through ADR-0016 are Accepted. The examples are intentionally not
normative `.json` fixtures, but their fenced JSON blocks are revalidated by the
repository self-tests against bare-core Layers 0–3.

- [cross-domain.md](cross-domain.md): six unrelated domains using one candidate
  JSON structure.
- [minimal-cases.md](minimal-cases.md): cardinality, trust, lifecycle and partial
  state edge cases.
- [S2 invalid-case catalogue](../../spec/s2-invalid-case-catalogue.md): cases to
  convert into fixtures only after human decisions and schema implementation.

The examples use `example.invalid` vocabulary/source IRIs to avoid implying a
real registry, product API or dereference requirement.
