# ADR-0001: Universal project scope

- **Status:** Accepted (records Foundation decisions)
- **Date:** 2026-08-30
- **Source:** `PROJECT_FOUNDATION.md` sections 1, 3, 4, 11, 20 and 24

## Context

SCC explored useful semantic concepts in a CAD-centered predecessor. The new
project needs a common semantic contract usable across unrelated files,
applications, domains and AI systems without inheriting one product/domain's
ontology or adapter responsibilities.

## Decision

GeesNO.Semantic is universal, open, domain-neutral, software-agnostic,
serialization-independent at the abstract-model level and AI-provider-neutral.
The core defines small universal mechanics, while domain meaning belongs in
vocabularies, profiles or namespaced extensions. Product- or format-specific
adapters are outside the core repository. SCC is prototype input, not an
automatically frozen specification. The project starts at `0.1.0-dev`.

## Consequences

- Every mandatory core concept must make sense across unrelated domains.
- Geometry and CAD/BIM concepts cannot be universally required.
- Producers/consumers/adapters may be independently implemented by third parties.
- Existing predecessor code is reused only after a domain-neutrality review.
- The core remains small rather than becoming a universal ontology.

