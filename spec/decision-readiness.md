# S1 decision record

**Status: S1 COMPLETE — NON-NORMATIVE DECISION SUMMARY**

## Accepted human decisions

### ADR-0005 — common hybrid assertion contract

Accepted at the abstract level: specialized claim categories share subject,
claim body, Provenance, Confidence, Review, lifecycle/validity and Extension
semantics. S1 left occurrence identity conditional. Accepted ADR-0011 later
requires identity for every serialized Assertion while expressly retaining
conditional identity for nested trust records.

### ADR-0006 — layered Source/Binding model

Accepted: Source is separate from Entity; each optional/plural Binding
correlates exactly one Entity and one Source; locator details are qualified and
extensible. Accepted ADR-0013 now fixes the JSON shape, mandatory identities
and one-specific-correlation continuity without changing this abstract model.

### ADR-0007 — state-first, history-optional lifecycle

Accepted: every SemanticDocument is consumable without Change replay, and the
state it contains is the authoritative representation of its declared scope for
the declared Revision. History is optional but constrained when present.
Revision parents are `0..*` lineage references only; Changes are descriptive;
missing content is not deletion without explicit scope/completeness semantics;
and lifecycle claims remain untrusted.

### ADR-0008 — optional many-to-many association

Accepted: `Concept 0..* <--> 0..* Representation`; every association is an
independent assertion and can have trust/lifecycle metadata. Accepted ADR-0011
later fixes its dedicated global assertion encoding.

## S1 closure

No S1 ADR remains Proposed or awaiting human decision. The four accepted
decisions form a coherent serialization-independent model and preserve the
Foundation boundaries. S1 — Universal Core Model 0.1 is **COMPLETE**.

This S1 closure did not itself freeze JSON, replace the then-blocking schema or
start S2 implementation. The later acceptance of ADR-0009 through ADR-0016 and
their S2 implementation do not change S1 closure; remaining vocabulary,
profile, integrity and later conformance choices are listed in
[open-questions.md](open-questions.md).

## S2 closure and S3 follow-on status

ADR-0009's stable-ID/reference architecture, ADR-0010's qualified-term
expansion architecture, ADR-0012's canonical value/unit architecture,
ADR-0011's assertion placement/addressability and ADR-0013's Source/Binding
serialization and ADR-0014 lifecycle/scope/completeness are Accepted. ADR-0011
requires identity for every serialized Assertion but not every trust record;
ADR-0014 fixes the conditional addressability trigger. ADR-0015 Extension/
version strictness and ADR-0016 processing/freeze are Accepted and implemented
in the approved S2 baseline. Explicit human closure approval on 2026-09-10
makes S2 **COMPLETE** without releasing public `0.1.0`.

S3 is open at the architecture stage. ADR-0017, Vocabulary identity and version
model, and ADR-0018, the abstract Vocabulary publication contract, are
Accepted. ADR-0019, Vocabulary/edition/term lifecycle, and ADR-0020, Extension
Vocabulary authoring/payload compatibility, are also Accepted. ADR-0021,
optional Vocabulary discovery, authority and governance, is Accepted by
explicit human decision on 2026-09-15. D6 Base Vocabulary and D7 compatibility
remain Open. Progressive
conformance, AI Context serialization, chunking/continuation, signatures,
Vocabulary discovery governance and mature contributor/patent policy remain
reserved for their ordered later decisions and phases.
