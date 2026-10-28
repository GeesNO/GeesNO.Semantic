# Conformance suite

For the public, non-normative route across Core Layers 0-3, exact AI Context
Profile acceptance, S5 assessment outcomes, repository commands and bounded
claim wording, see the [Conformance Guide](../docs/conformance-guide.md).

The approved S2 conformance baseline is deterministic, exact-versioned and independent
of LLMs, cloud services and the reference SDK. The suite separates:

- [`valid/`](valid/README.md): documents expected to pass;
- [`invalid/`](invalid/README.md): documents expected to fail;
- [`expected/`](expected/README.md): deterministic expected outcomes/diagnostics;
- [`runner/`](runner/README.md): strict Layers 0–3 execution.

Every fixture has a same-stem expected outcome. Layer 0 covers raw bytes and
safe JSON parsing; Layer 1 exact version dispatch; Layer 2 Draft 2020-12 schema
validation; and Layer 3 deterministic semantic/integrity checks. Layer 4
profile validation remains separate and is not implemented in S2.

Explicit human closure approval on 2026-09-10 makes this suite part of the
completed S2 baseline. It does not publish `0.1.0`, define stable S5 diagnostics
or implement an SDK.
The Python runner is one non-normative reference implementation: conforming
processors may use any language, standards-compliant Draft 2020-12 engine and
equivalent deterministic Layer 3 checks. Validation requires no LLM, network
access or official SDK.
