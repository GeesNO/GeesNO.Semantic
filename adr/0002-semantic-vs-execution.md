# ADR-0002: Semantic description is separate from execution

- **Status:** Accepted (records Foundation decisions)
- **Date:** 2026-08-30
- **Source:** `PROJECT_FOUNDATION.md` sections 2, 3, 7, 18 and 24

## Context

Semantic context can inform tools and applications, but mixing descriptions
with commands would make the standard an execution runtime and couple it to
permissions, transactions, products and AI-agent implementations.

## Decision

GeesNO.Semantic describes identity, representation, meaning, relationships,
source, provenance, confidence, review and lifecycle context. It does not
define application commands, GUI control, tool execution, agents, RAG,
retrieval, model routing or transaction orchestration.

GeesNO.Core is independent and is neither imported, required nor assumed. The
former SCA/action direction is outside GeesNO.Semantic. The AI Context Profile
is a descriptive projection, not an execution mechanism.

## Consequences

- A semantic document contains data, never executable instructions or plugins.
- Products may use GeesNO.Semantic and GeesNO.Core independently.
- Integrations, if demonstrated later, live outside both universal cores.
- Security review treats external references and extension content as untrusted
  data rather than executable capabilities.

