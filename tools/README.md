# Tools

Repository tooling must remain deterministic and must not modify native user
documents. [`validation/`](validation/README.md) contains dependency-free
repository guards plus self-tests for the approved S2 schema/conformance baseline.
Semantic Layers 0–3 are implemented separately under `conformance/runner/`.
