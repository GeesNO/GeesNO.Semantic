# Version 0.1 approved S2 schema

`geesno-semantic.schema.json` is the approved Draft 2020-12 S2 structural
baseline. Its `x-geesno-status` is `s2-complete`, it has no network identity
requirement, and it closes versioned core objects while retaining the accepted
qualified `extensions` boundaries.

The schema implements accepted ADR-0009 through ADR-0016. JSON Schema provides
Layer 2 structure; document-wide identity, reference, namespace, graph,
calendar, range and recursive-set integrity remain deterministic Layer 3
checks. Raw parsing and exact version dispatch are Layers 0 and 1. The paired
fixtures and runner live under `conformance/`. Explicit human closure approval
on 2026-09-10 completes S2. At that gate the project remained `0.1.0-dev`; the
approval did not release public `0.1.0`, and the instance contract remains
exactly `0.1.0`.
