# Provenance, Confidence and Review

**Scope:** Universal Provenance, Confidence and Review capabilities and Core 0.1 JSON representation.
**Architectural authority:** [ARCHITECTURE.md](../ARCHITECTURE.md) and accepted ADRs.

These capabilities are universal because semantic claims across domains can
be authored, inferred, contested and validated. They are separate:

- **Provenance** explains origin, method and evidence.
- **Confidence** records a scoped certainty assessment.
- **Review** records a scoped disposition by a human or controlled process.

None can be derived reliably from another.

## Provenance

A Provenance occurrence has one unambiguous target scope and one origin
mechanism. Candidate conceptual origin distinctions are:

- source-authored;
- imported/native;
- deterministic rule;
- AI inference;
- user-authored;
- mapped from another standard;
- externally curated.

This list states required distinctions, not final serialized vocabulary.
Provenance may also express source/evidence references, actor or process, time,
method and tool/model version. Several provenance records or a chain may apply
to one assertion.

“Source-authored” means the claim was authoritative content of the identified
source context; “imported/native” records faithful transfer. Neither implies
that reality outside the source is correct. Syntactic validity never turns an
inference into a fact.

Actor identity can be pseudonymous or process-level. Personal data is not
required when it is unnecessary. Evidence/reference locations are not
automatically dereferenced.

## Confidence

Confidence is optional for authoritative claims and available for inferred
claims. Each assessment has one target and one score. Several assessments may
coexist when methods, actors or revisions differ.

The foundational model recommends `0.0..1.0`. Additional interpretation principles:

- missing Confidence means “not supplied”, not `1.0`;
- `0.0` and `1.0` are assessments, not formal false/true values;
- scores from different methods are not comparable unless calibration/profile
  semantics make them comparable;
- aggregation, threshold and winner-selection policies are outside the core;
- Confidence never substitutes for Provenance or Review.

Accepted ADR-0016 specifies exact score encoding and range for Core 0.1 JSON;
calibration metadata and aggregation remain Vocabulary/Profile concerns.

## Review

Review has one explicit target scope and one disposition. Illustrative
dispositions include unreviewed, accepted, rejected and corrected. Their
exact Vocabulary terms, authority conventions and transitions remain
matters for applicable Vocabularies/Profiles, not universal Core semantics.

A Review may include reviewer/process identity, time, note/evidence and a
reference to a correction. Review history is appendable: correcting or rejecting
a claim must not silently erase the reviewed claim when lifecycle history is
represented.

Assertion-level Review is the clearest scope. Entity-level Review is allowed
only when it explicitly means that all declared aspects within a defined scope
were reviewed; it cannot ambiguously imply that every current/future assertion
about the Entity is accepted.

## Attachment and identity boundary

Accepted ADR-0011 keeps Provenance, Confidence and Review nested only in the
record whose scope they qualify. It does not universally require their own IDs.
A purely scoped occurrence may remain anonymous; stable ADR-0009 identity is
required when citation, review-of-review, correction, supersession or lifecycle
needs portable independent targeting. JSON Pointer and array position are not
identity. Accepted ADR-0014 fixes the conditional lifecycle/addressability
triggers, including that a late ID cannot prove continuity with an earlier
anonymous occurrence.
